//! Custom production rigid-body backend, first capability: rigid cuboids
//! with gravity and compliant contact against the reference tabletop
//! (Q35, Q41, Q47, PHY-001, PHY-002, PHY-005..007).
//!
//! Status: implemented, **not qualified**. Fixture links are qualified only
//! by their own suite. The reduced fixture coupler (below) is implemented,
//! qualification pending (Q56/Q57). General body-body contact does not exist.
//!
//! Formulation (velocity-level time stepping, fixed step h):
//! 1. Contacts are cuboid vertices with z ≤ 0 against the plane z = 0.
//!    Coulomb coefficient per contact: μs if its tangential speed at step
//!    start is ≤ `static_slip_speed_m_s`, else μk (Q47).
//! 2. External loads (gravity, validation loads) update velocities.
//! 3. Projected Gauss–Seidel over contacts in a fixed order, a fixed number
//!    of sweeps. Normal: implicit spring-damper (stiffness k, damping c):
//!      ΔP = −(Jv + C·k/(hk + c) + P/s) / (K + 1/s),  s = h(hk + c),  P ≥ 0
//!    where C = z of the contact point (negative when penetrating). This is
//!    the impulse form of f = −k·C − c·Ċ integrated implicitly, so the
//!    compliance is the declared physical stiffness and damping, not solver
//!    stabilization (PHY-006). Friction: rigid tangential velocity
//!    constraint, impulse clamped to the circular cone |Pt| ≤ μ·Pn.
//! 4. Semi-implicit Euler integration; quaternion first-order update.
//!
//! Contact reports are the solver's own impulses divided by h (PHY-005).
//! Warm-start impulses are part of the authoritative state and are hashed.
//!
//! Fixture links (Q52 §1, compliant-link slice): a 6-DOF generalized
//! spring-damper between two anchor frames, solved as six implicit compliant
//! rows (axial, shear 1, shear 2, torsion, bend 1, bend 2) in the SAME
//! Gauss–Seidel sweeps as contacts. For a row with constraint coordinate C,
//! rate Jv, stiffness k and damping c, the impulse is
//!   P = −h·k·C̃ − h·c·Jv′,   C̃ = C_n + q·h·(Jv′ − Jv₀),
//! where Jv′ is the post-step rate and Jv₀ the rate at step start before
//! external loads. With c = 0 this step map has determinant exactly 1
//! (no numerical damping) for any q, is unconditionally stable for q > 0,
//! and for q = 1/4 has the implicit-midpoint frequency tan(φ/2) = ωh/2. At
//! rest Jv′ = Jv₀, so C̃ = C_n and statics are exact. All damping is the
//! declared c; there is no stabilization term (PHY-006). Small-angle
//! approximations: the rotational rate is ω_B − ω_A, and rotation of the
//! anchor frame during a step is neglected.
//!
//! Reduced fixture coupler (Q56, Q57; implemented, qualification pending): a
//! ball probe on body B in a square-pyramid socket on body A. It has
//! (1) guide contacts, sphere-versus-socket features from
//! `coupler_geometry`, solved as two-body compliant-normal and Coulomb rows
//! with the tabletop's law, in the same Gauss–Seidel sweep after tabletop
//! contacts and before link rows; (2) an engagement-scaled latch link, a
//! normal 6-DOF link whose k and c are multiplied by e = u/travel (it exists
//! only while the pawl is out and not separated); (3) a massless first-order
//! pawl coordinate u, advanced AFTER each step from that step's solver-native
//! link report (cam-out force and friction); and (4) load-limit separation
//! decided from the link report with engagement-scaled limits. The discrete
//! states are never read by the solver (CPL-001). The pawl work is reported.
//!
//! Static bodies (infinite mass, never move) are permitted only when the
//! world is flagged `allow_static_bodies` by fixture-validation code.

const std = @import("std");
const m3 = @import("math3.zig");
const canonical = @import("canonical.zig");
const backend_mod = @import("backend.zig");
const coupler_geometry = @import("coupler_geometry.zig");

pub const Settings = struct {
    contact_stiffness_n_m: f64,
    contact_damping_n_s_m: f64,
    static_slip_speed_m_s: f64,
    iterations: u32,
    warm_start: bool,
};

pub const Friction = struct { mu_static: f64, mu_kinetic: f64 };

pub const Body = struct {
    mass_kg: f64,
    /// Principal moments about the centre of mass, body frame.
    inertia_kg_m2: m3.Vec3,
    half_extents_m: m3.Vec3,
    position_m: m3.Vec3,
    orientation: m3.Quat = .identity,
    velocity_m_s: m3.Vec3 = m3.zero,
    angular_velocity_rad_s: m3.Vec3 = m3.zero,
    /// Accumulated (normal, tangent x, tangent y) impulses per vertex from the
    /// previous step, for warm starting.
    warm: [8][3]f64 = @splat(.{ 0, 0, 0 }),
    /// Infinite mass; never moves, never collides. Fixture validation only.
    is_static: bool = false,

    pub fn vertexBody(self: Body, i: usize) m3.Vec3 {
        const h = self.half_extents_m;
        return .{
            if (i & 1 != 0) h[0] else -h[0],
            if (i & 2 != 0) h[1] else -h[1],
            if (i & 4 != 0) h[2] else -h[2],
        };
    }

    fn invInertiaWorld(self: Body, v: m3.Vec3) m3.Vec3 {
        if (self.is_static) return m3.zero;
        const b = self.orientation.rotateInverse(v);
        return self.orientation.rotate(.{ b[0] / self.inertia_kg_m2[0], b[1] / self.inertia_kg_m2[1], b[2] / self.inertia_kg_m2[2] });
    }

    fn applyImpulse(self: *Body, r: m3.Vec3, p: m3.Vec3) void {
        if (self.is_static) return;
        self.velocity_m_s = m3.add(self.velocity_m_s, m3.scale(p, 1.0 / self.mass_kg));
        self.angular_velocity_rad_s = m3.add(self.angular_velocity_rad_s, self.invInertiaWorld(m3.cross(r, p)));
    }

    fn pointVelocity(self: Body, r: m3.Vec3) m3.Vec3 {
        return m3.add(self.velocity_m_s, m3.cross(self.angular_velocity_rad_s, r));
    }

    fn applyAngularImpulse(self: *Body, l: m3.Vec3) void {
        if (self.is_static) return;
        self.angular_velocity_rad_s = m3.add(self.angular_velocity_rad_s, self.invInertiaWorld(l));
    }

    fn effectiveMass(self: Body, r: m3.Vec3, d: m3.Vec3) f64 {
        if (self.is_static) return 0.0;
        const rd = m3.cross(r, d);
        return 1.0 / self.mass_kg + m3.dot(rd, self.invInertiaWorld(rd));
    }
};

const Contact = struct {
    body: u32,
    vertex: u8,
    r: m3.Vec3,
    point: m3.Vec3,
    mu: f64,
    kn: f64,
    kt: [2]f64,
    p: [3]f64,
};

/// Declared fixture link (Q52 §1). Stiffness and damping per axis: isotropic
/// in the two shear and the two bend directions.
pub const LinkSpec = struct {
    body_a: u32,
    body_b: u32,
    /// Unit link axis in body A's frame.
    axis_a: m3.Vec3,
    /// Anchor points in each body's frame.
    anchor_a_m: m3.Vec3,
    anchor_b_m: m3.Vec3,
    rest_length_m: f64,
    /// Relative orientation conj(q_A)·q_B at rest.
    rest_relative_orientation: m3.Quat = .identity,
    k_axial_n_m: f64,
    k_shear_n_m: f64,
    k_torsion_nm_rad: f64,
    k_bend_nm_rad: f64,
    c_axial_n_s_m: f64,
    c_shear_n_s_m: f64,
    c_torsion_nm_s_rad: f64,
    c_bend_nm_s_rad: f64,
};

/// Link solver state that affects future steps: the previous step's row
/// impulses (warm start).
const Link = struct {
    spec: LinkSpec,
    p: [6]f64 = @splat(0),
    /// Inactive links create no rows and report zero loads.
    active: bool = true,
    /// Multiplies k and c of every row (engagement); exactly 1.0 skips the
    /// multiplication so unscaled links are bit-identical.
    scale: f64 = 1.0,
    /// Index of this link's first row in `link_rows` this step (if active).
    row0: u32 = 0,
};

/// Reduced fixture coupler declaration (Q56). All lengths in metres.
pub const CouplerSpec = struct {
    body_a: u32,
    body_b: u32,
    /// Unit coupler axis in A's frame, out of A.
    axis_a: m3.Vec3,
    /// A's centre to the coupler face plane, along `axis_a`.
    face_offset_a_m: f64,
    geom: coupler_geometry.Params,
    ball_radius_m: f64,
    /// Ball centre in B's frame.
    ball_centre_b_m: m3.Vec3,
    preload_offset_m: f64,
    k_axial_full: f64,
    k_shear_full: f64,
    k_torsion_full: f64,
    k_bend_full: f64,
    c_axial_full: f64,
    c_shear_full: f64,
    c_torsion_full: f64,
    c_bend_full: f64,
    limit_tension_n: f64,
    limit_shear_n: f64,
    limit_bending_nm: f64,
    limit_torsion_nm: f64,
    travel_m: f64,
    speed_limit_m_s: f64,
    actuator_force_n: f64,
    pawl_friction: f64,
    capture_radial_m: f64,
    capture_axial_m: f64,
    guide_enabled: bool,
    guide_mu_static: f64,
    guide_mu_kinetic: f64,
};

const Coupler = struct {
    spec: CouplerSpec,
    link: u32,
    /// Pawl travel.
    u_m: f64 = 0,
    armed: bool = true,
    separation: backend_mod.SeparationKind = .none,
    guide_warm: [13][3]f64 = @splat(.{ 0, 0, 0 }),
    // Per-step transients (set at step start, read by the update).
    e_during: f64 = 0,
    was_active: bool = false,
};

const GuideRow = struct {
    coupler: u32,
    feature: u8,
    r_a: m3.Vec3,
    r_b: m3.Vec3,
    point: m3.Vec3,
    n: m3.Vec3,
    t: [2]m3.Vec3,
    mu: f64,
    kn: f64,
    kt: [2]f64,
    c_coord: f64,
    p: [3]f64,
};

/// AUDIT CONTROL ONLY: deliberately violates CPL-004. Applied at coupler
/// link activation to prove the audits discriminate.
pub const AuditControl = enum {
    none,
    /// AUDIT CONTROL ONLY: sets B's velocity to A's on activation (an
    /// unmodeled velocity correction).
    velocity_snap_on_activation,
    /// AUDIT CONTROL ONLY: translates B by minus the link's world extension on
    /// activation (an unmodeled pose correction).
    pose_snap_on_activation,
};

const LinkRow = struct {
    link: u32,
    index: u8,
    rot: bool,
    e: m3.Vec3,
    c_coord: f64,
    jv0: f64,
    kin: f64,
    k: f64,
    c: f64,
    p: f64,
};

pub const LinkForm = enum {
    /// C̃ = C_n + q·h·(Jv′ − Jv₀): zero numerical damping (protocol).
    midpoint_prediction,
    /// C̃ = C_n + h·Jv′: the conventional backward-Euler soft constraint,
    /// which dissipates about ζ ≈ ω·h/2. A sensitivity control only (Q54).
    backward_euler,
};

pub const LinkSettings = struct {
    form: LinkForm,
    /// Coefficient q of the spring-term prediction C̃ = C_n + q·h·(Jv′ − Jv₀).
    prediction_q: f64,
};

pub const AddError = error{ OutOfMemory, StaticBodyNotPermitted, InvalidLink };

const n_axis: m3.Vec3 = .{ 0, 0, 1 };
const t_axes = [2]m3.Vec3{ .{ 1, 0, 0 }, .{ 0, 1, 0 } };

pub const World = struct {
    gpa: std.mem.Allocator,
    settings: Settings,
    friction: Friction,
    gravity_m_s2: m3.Vec3,
    bodies: std.ArrayList(Body) = .empty,
    contacts: std.ArrayList(Contact) = .empty,
    reports: std.ArrayList(backend_mod.ContactReport) = .empty,
    link_settings: LinkSettings = .{ .form = .midpoint_prediction, .prediction_q = 0.25 },
    /// Set only by fixture-validation harness code (Q52 §1).
    allow_static_bodies: bool = false,
    links: std.ArrayList(Link) = .empty,
    link_rows: std.ArrayList(LinkRow) = .empty,
    link_geoms: std.ArrayList(LinkGeometry) = .empty,
    link_reports: std.ArrayList(backend_mod.LinkReport) = .empty,
    couplers: std.ArrayList(Coupler) = .empty,
    guide_rows: std.ArrayList(GuideRow) = .empty,
    coupler_reports: std.ArrayList(backend_mod.CouplerReport) = .empty,
    /// AUDIT CONTROL ONLY: deliberately violates CPL-004. `step` refuses any
    /// value but `.none` unless `allow_static_bodies` (fixture validation).
    audit_control: AuditControl = .none,

    pub fn deinit(self: *World) void {
        self.couplers.deinit(self.gpa);
        self.guide_rows.deinit(self.gpa);
        self.coupler_reports.deinit(self.gpa);
        self.bodies.deinit(self.gpa);
        self.contacts.deinit(self.gpa);
        self.reports.deinit(self.gpa);
        self.links.deinit(self.gpa);
        self.link_rows.deinit(self.gpa);
        self.link_geoms.deinit(self.gpa);
        self.link_reports.deinit(self.gpa);
    }

    pub fn addBody(self: *World, b: Body) AddError!u32 {
        if (b.is_static and !self.allow_static_bodies) return error.StaticBodyNotPermitted;
        try self.bodies.append(self.gpa, b);
        return @intCast(self.bodies.items.len - 1);
    }

    pub fn addLink(self: *World, spec: LinkSpec) AddError!u32 {
        const n = self.bodies.items.len;
        if (spec.body_a >= n or spec.body_b >= n or spec.body_a == spec.body_b) return error.InvalidLink;
        if (self.bodies.items[spec.body_b].is_static) return error.InvalidLink;
        if (@abs(m3.length(spec.axis_a) - 1.0) > 1e-12) return error.InvalidLink;
        try self.links.append(self.gpa, .{ .spec = spec });
        return @intCast(self.links.items.len - 1);
    }

    /// Adds a reduced fixture coupler (Q56) and its latch link, which starts
    /// inactive with the pawl retracted (u = 0). Returns the coupler index.
    pub fn addCoupler(self: *World, spec: CouplerSpec) AddError!u32 {
        const n = self.bodies.items.len;
        if (spec.body_a >= n or spec.body_b >= n or spec.body_a == spec.body_b) return error.InvalidLink;
        if (self.bodies.items[spec.body_b].is_static) return error.InvalidLink;
        if (@abs(m3.length(spec.axis_a) - 1.0) > 1e-12) return error.InvalidLink;
        if (!(spec.travel_m > 0) or !(spec.speed_limit_m_s >= 0)) return error.InvalidLink;
        const seat_x = coupler_geometry.seatX(spec.geom, spec.ball_radius_m);
        const li = try self.addLink(.{
            .body_a = spec.body_a,
            .body_b = spec.body_b,
            .axis_a = spec.axis_a,
            .anchor_a_m = m3.scale(spec.axis_a, spec.face_offset_a_m + seat_x - spec.preload_offset_m),
            .anchor_b_m = spec.ball_centre_b_m,
            .rest_length_m = 0,
            .k_axial_n_m = spec.k_axial_full,
            .k_shear_n_m = spec.k_shear_full,
            .k_torsion_nm_rad = spec.k_torsion_full,
            .k_bend_nm_rad = spec.k_bend_full,
            .c_axial_n_s_m = spec.c_axial_full,
            .c_shear_n_s_m = spec.c_shear_full,
            .c_torsion_nm_s_rad = spec.c_torsion_full,
            .c_bend_nm_s_rad = spec.c_bend_full,
        });
        self.links.items[li].active = false;
        try self.couplers.append(self.gpa, .{ .spec = spec, .link = li });
        return @intCast(self.couplers.items.len - 1);
    }

    /// Sets pawl travel and link activity directly (initial conditions of a
    /// run); the coupler is armed and has no separation history.
    pub fn setCoupler(self: *World, ci: u32, u_m: f64, active: bool) void {
        const cp = &self.couplers.items[ci];
        cp.u_m = u_m;
        cp.armed = true;
        cp.separation = .none;
        const lk = &self.links.items[cp.link];
        lk.active = active;
        lk.p = @splat(0);
    }

    /// World position of the seat point (ball centre at zero penetration).
    pub fn couplerSeatPointWorld(self: *const World, ci: usize) m3.Vec3 {
        const sp = self.couplers.items[ci].spec;
        const a = self.bodies.items[sp.body_a];
        const seat_x = coupler_geometry.seatX(sp.geom, sp.ball_radius_m);
        return m3.add(a.position_m, a.orientation.rotate(m3.scale(sp.axis_a, sp.face_offset_a_m + seat_x)));
    }

    /// Ball centre in the coupler frame of A (x axial from the face plane).
    fn ballCentreCoupler(self: *const World, sp: CouplerSpec) m3.Vec3 {
        const a = self.bodies.items[sp.body_a];
        const b = self.bodies.items[sp.body_b];
        const perp = perpendiculars(sp.axis_a);
        const cw = m3.add(b.position_m, b.orientation.rotate(sp.ball_centre_b_m));
        const la = a.orientation.rotateInverse(m3.sub(cw, a.position_m));
        return .{ m3.dot(sp.axis_a, la) - sp.face_offset_a_m, m3.dot(perp[0], la), m3.dot(perp[1], la) };
    }

    /// Anchor-A frame axes (axial, shear 1, shear 2) in body A's frame, as
    /// the link rows use them. For recording (Q55).
    pub fn linkAxesBodyA(self: *const World, li: usize) [3]m3.Vec3 {
        const a = self.links.items[li].spec.axis_a;
        const p = perpendiculars(a);
        return .{ a, p[0], p[1] };
    }

    /// Unit vectors perpendicular to `a` and to each other, deterministic:
    /// s1 = normalize(a × t) with t the world axis of smallest |a_i| (lowest
    /// index on ties), s2 = a × s1.
    fn perpendiculars(a: m3.Vec3) [2]m3.Vec3 {
        var i: usize = 0;
        for (1..3) |j| if (@abs(a[j]) < @abs(a[i])) {
            i = j;
        };
        var t: m3.Vec3 = m3.zero;
        t[i] = 1;
        const c = m3.cross(a, t);
        const s1 = m3.scale(c, 1.0 / m3.length(c));
        return .{ s1, m3.cross(a, s1) };
    }

    const LinkGeometry = struct { extension_world: m3.Vec3, rotation_world: m3.Vec3, r_a: m3.Vec3, r_b: m3.Vec3, axes_world: [3]m3.Vec3 };

    fn linkGeometry(self: *const World, spec: LinkSpec) LinkGeometry {
        const a = self.bodies.items[spec.body_a];
        const b = self.bodies.items[spec.body_b];
        const r_a = a.orientation.rotate(spec.anchor_a_m);
        const r_b = b.orientation.rotate(spec.anchor_b_m);
        const perp = perpendiculars(spec.axis_a);
        const axes: [3]m3.Vec3 = .{ a.orientation.rotate(spec.axis_a), a.orientation.rotate(perp[0]), a.orientation.rotate(perp[1]) };
        const anchor_a = m3.add(a.position_m, r_a);
        const anchor_b = m3.add(b.position_m, r_b);
        const ext = m3.sub(m3.sub(anchor_b, anchor_a), m3.scale(axes[0], spec.rest_length_m));
        const q_rel = (m3.Quat{ .w = a.orientation.w, .x = -a.orientation.x, .y = -a.orientation.y, .z = -a.orientation.z }).mul(b.orientation);
        const theta_a = q_rel.relativeTo(spec.rest_relative_orientation).rotationVector();
        return .{ .extension_world = ext, .rotation_world = a.orientation.rotate(theta_a), .r_a = r_a, .r_b = r_b, .axes_world = axes };
    }

    fn rowRate(self: *const World, row: LinkRow) f64 {
        const g = self.link_geoms.items[row.link];
        const spec = self.links.items[row.link].spec;
        const a = self.bodies.items[spec.body_a];
        const b = self.bodies.items[spec.body_b];
        if (row.rot) return m3.dot(row.e, m3.sub(b.angular_velocity_rad_s, a.angular_velocity_rad_s));
        return m3.dot(row.e, m3.sub(b.pointVelocity(g.r_b), a.pointVelocity(g.r_a)));
    }

    fn applyRowImpulse(self: *World, row: LinkRow, dp: f64) void {
        const g = self.link_geoms.items[row.link];
        const spec = self.links.items[row.link].spec;
        const a = &self.bodies.items[spec.body_a];
        const b = &self.bodies.items[spec.body_b];
        const imp = m3.scale(row.e, dp);
        if (row.rot) {
            b.applyAngularImpulse(imp);
            a.applyAngularImpulse(m3.scale(imp, -1.0));
        } else {
            b.applyImpulse(g.r_b, imp);
            a.applyImpulse(g.r_a, m3.scale(imp, -1.0));
        }
    }

    pub fn backend(self: *World) backend_mod.Backend {
        return .{ .ptr = self, .vtable = &.{ .identity = identityFn, .step = stepFn, .encodeState = encodeFn, .contacts = contactsFn } };
    }

    pub fn step(self: *World, h: f64, inputs: backend_mod.StepInputs) backend_mod.StepError!void {
        if (!(h > 0)) return error.InvalidInput;
        if (self.audit_control != .none and !self.allow_static_bodies) return error.InvalidInput;
        const s = self.settings;
        self.contacts.clearRetainingCapacity();

        // 0. Coupler engagement at step start: link scale e = u/travel.
        for (self.couplers.items) |*cp| {
            const lk = &self.links.items[cp.link];
            cp.was_active = lk.active;
            cp.e_during = cp.u_m / cp.spec.travel_m;
            if (lk.active) lk.scale = cp.e_during;
        }

        // 1. Contact detection and friction regime from step-start velocities.
        for (self.bodies.items, 0..) |*b, bi| {
            if (b.is_static) continue;
            for (0..8) |vi| {
                const r = b.orientation.rotate(b.vertexBody(vi));
                const p = m3.add(b.position_m, r);
                if (p[2] > 0) continue;
                const vt = b.pointVelocity(r);
                const slip = m3.horizontalLength(vt);
                try self.contacts.append(self.gpa, .{
                    .body = @intCast(bi),
                    .vertex = @intCast(vi),
                    .r = r,
                    .point = p,
                    .mu = if (slip <= s.static_slip_speed_m_s) self.friction.mu_static else self.friction.mu_kinetic,
                    .kn = b.effectiveMass(r, n_axis),
                    .kt = .{ b.effectiveMass(r, t_axes[0]), b.effectiveMass(r, t_axes[1]) },
                    .p = if (s.warm_start) b.warm[vi] else .{ 0, 0, 0 },
                });
            }
            // Vertices not in contact this step start from zero next step.
            b.warm = @splat(.{ 0, 0, 0 });
        }

        // 1b. Link rows from step-start state, before external loads.
        self.link_rows.clearRetainingCapacity();
        self.link_geoms.clearRetainingCapacity();
        for (self.links.items, 0..) |*lk, li| {
            const g = self.linkGeometry(lk.spec);
            try self.link_geoms.append(self.gpa, g);
            lk.row0 = @intCast(self.link_rows.items.len);
            if (!lk.active) continue;
            const sp = lk.spec;
            const ba = self.bodies.items[sp.body_a];
            const bb = self.bodies.items[sp.body_b];
            const ks = [6]f64{ sp.k_axial_n_m, sp.k_shear_n_m, sp.k_shear_n_m, sp.k_torsion_nm_rad, sp.k_bend_nm_rad, sp.k_bend_nm_rad };
            const cs = [6]f64{ sp.c_axial_n_s_m, sp.c_shear_n_s_m, sp.c_shear_n_s_m, sp.c_torsion_nm_s_rad, sp.c_bend_nm_s_rad, sp.c_bend_nm_s_rad };
            for (0..6) |ri| {
                const rot = ri >= 3;
                const e = g.axes_world[ri % 3];
                var k_row = ks[ri];
                var c_row = cs[ri];
                if (lk.scale != 1.0) {
                    k_row = k_row * lk.scale;
                    c_row = c_row * lk.scale;
                }
                var row: LinkRow = .{
                    .link = @intCast(li),
                    .index = @intCast(ri),
                    .rot = rot,
                    .e = e,
                    .c_coord = m3.dot(e, if (rot) g.rotation_world else g.extension_world),
                    .jv0 = 0,
                    .kin = if (rot) m3.dot(e, ba.invInertiaWorld(e)) + m3.dot(e, bb.invInertiaWorld(e)) else ba.effectiveMass(g.r_a, e) + bb.effectiveMass(g.r_b, e),
                    .k = k_row,
                    .c = c_row,
                    .p = if (s.warm_start) lk.p[ri] else 0,
                };
                row.jv0 = self.rowRate(row);
                try self.link_rows.append(self.gpa, row);
            }
        }

        // 1c. Guide contacts from the step-start pose.
        try self.detectGuides();

        // 2. External loads.
        for (self.bodies.items) |*b| {
            if (b.is_static) continue;
            b.velocity_m_s = m3.add(b.velocity_m_s, m3.scale(self.gravity_m_s2, h));
        }
        for (inputs.validation_loads) |l| {
            if (l.body_index >= self.bodies.items.len) return error.InvalidInput;
            const b = &self.bodies.items[l.body_index];
            if (b.is_static) return error.InvalidInput;
            const r = m3.sub(l.world_point_m, b.position_m);
            const torque = m3.add(l.world_torque_nm, m3.cross(r, l.world_force_n));
            b.velocity_m_s = m3.add(b.velocity_m_s, m3.scale(l.world_force_n, h / b.mass_kg));
            b.angular_velocity_rad_s = m3.add(b.angular_velocity_rad_s, b.invInertiaWorld(m3.scale(torque, h)));
        }

        // 3. Warm start, then projected Gauss–Seidel.
        for (self.contacts.items) |c| {
            const b = &self.bodies.items[c.body];
            b.applyImpulse(c.r, m3.add(m3.scale(n_axis, c.p[0]), m3.add(m3.scale(t_axes[0], c.p[1]), m3.scale(t_axes[1], c.p[2]))));
        }
        for (self.guide_rows.items) |g| self.applyGuideImpulse(g, m3.add(m3.scale(g.n, g.p[0]), m3.add(m3.scale(g.t[0], g.p[1]), m3.scale(g.t[1], g.p[2]))));
        for (self.link_rows.items) |row| self.applyRowImpulse(row, row.p);
        const soft = h * (h * s.contact_stiffness_n_m + s.contact_damping_n_s_m);
        const bias_gain = s.contact_stiffness_n_m / (h * s.contact_stiffness_n_m + s.contact_damping_n_s_m);
        for (0..s.iterations) |_| {
            for (self.contacts.items) |*c| {
                const b = &self.bodies.items[c.body];
                const vn = m3.dot(b.pointVelocity(c.r), n_axis);
                const dpn = -(vn + bias_gain * c.point[2] + c.p[0] / soft) / (c.kn + 1.0 / soft);
                const pn = @max(c.p[0] + dpn, 0.0);
                b.applyImpulse(c.r, m3.scale(n_axis, pn - c.p[0]));
                c.p[0] = pn;

                const vel = b.pointVelocity(c.r);
                var pt = [2]f64{
                    c.p[1] - m3.dot(vel, t_axes[0]) / c.kt[0],
                    c.p[2] - m3.dot(vel, t_axes[1]) / c.kt[1],
                };
                const mag = @sqrt(pt[0] * pt[0] + pt[1] * pt[1]);
                const limit = c.mu * c.p[0];
                if (mag > limit) {
                    const k = if (mag > 0) limit / mag else 0;
                    pt = .{ pt[0] * k, pt[1] * k };
                }
                b.applyImpulse(c.r, m3.add(m3.scale(t_axes[0], pt[0] - c.p[1]), m3.scale(t_axes[1], pt[1] - c.p[2])));
                c.p[1] = pt[0];
                c.p[2] = pt[1];
            }
            for (self.guide_rows.items) |*g| {
                const a = self.bodies.items[self.couplers.items[g.coupler].spec.body_a];
                const b = self.bodies.items[self.couplers.items[g.coupler].spec.body_b];
                const vn = m3.dot(m3.sub(b.pointVelocity(g.r_b), a.pointVelocity(g.r_a)), g.n);
                const dpn = -(vn + bias_gain * g.c_coord + g.p[0] / soft) / (g.kn + 1.0 / soft);
                const pn = @max(g.p[0] + dpn, 0.0);
                self.applyGuideImpulse(g.*, m3.scale(g.n, pn - g.p[0]));
                g.p[0] = pn;

                const a2 = self.bodies.items[self.couplers.items[g.coupler].spec.body_a];
                const b2 = self.bodies.items[self.couplers.items[g.coupler].spec.body_b];
                const vel = m3.sub(b2.pointVelocity(g.r_b), a2.pointVelocity(g.r_a));
                var pt = [2]f64{
                    g.p[1] - m3.dot(vel, g.t[0]) / g.kt[0],
                    g.p[2] - m3.dot(vel, g.t[1]) / g.kt[1],
                };
                const mag = @sqrt(pt[0] * pt[0] + pt[1] * pt[1]);
                const limit = g.mu * g.p[0];
                if (mag > limit) {
                    const k = if (mag > 0) limit / mag else 0;
                    pt = .{ pt[0] * k, pt[1] * k };
                }
                self.applyGuideImpulse(g.*, m3.add(m3.scale(g.t[0], pt[0] - g.p[1]), m3.scale(g.t[1], pt[1] - g.p[2])));
                g.p[1] = pt[0];
                g.p[2] = pt[1];
            }
            const ls = self.link_settings;
            for (self.link_rows.items) |*row| {
                const dp = switch (ls.form) {
                    .midpoint_prediction => blk: {
                        const q = ls.prediction_q;
                        const gamma = q * h * h * row.k + h * row.c;
                        break :blk -(gamma * self.rowRate(row.*) + h * row.k * row.c_coord - q * h * h * row.k * row.jv0 + row.p) / (1.0 + gamma * row.kin);
                    },
                    .backward_euler => blk: {
                        const gamma = h * h * row.k + h * row.c;
                        break :blk -(gamma * self.rowRate(row.*) + h * row.k * row.c_coord + row.p) / (1.0 + gamma * row.kin);
                    },
                };
                self.applyRowImpulse(row.*, dp);
                row.p += dp;
            }
        }

        // 4. Store warm-start impulses, report contacts, integrate.
        self.reports.clearRetainingCapacity();
        for (self.contacts.items) |c| {
            const b = &self.bodies.items[c.body];
            b.warm[c.vertex] = c.p;
            try self.reports.append(self.gpa, .{
                .body_a = c.body,
                .body_b = null,
                .world_point_m = c.point,
                .world_normal = n_axis,
                .normal_force_n = c.p[0] / h,
                .tangential_force_n = .{ c.p[1] / h, c.p[2] / h, 0 },
            });
        }
        for (self.couplers.items) |*cp| cp.guide_warm = @splat(.{ 0, 0, 0 });
        for (self.guide_rows.items) |g| {
            self.couplers.items[g.coupler].guide_warm[g.feature] = g.p;
            const sp = self.couplers.items[g.coupler].spec;
            try self.reports.append(self.gpa, .{
                .body_a = sp.body_a,
                .body_b = sp.body_b,
                .world_point_m = g.point,
                .world_normal = g.n,
                .normal_force_n = g.p[0] / h,
                .tangential_force_n = m3.scale(m3.add(m3.scale(g.t[0], g.p[1]), m3.scale(g.t[1], g.p[2])), 1.0 / h),
            });
        }
        for (self.bodies.items) |*b| {
            if (b.is_static) continue;
            b.position_m = m3.add(b.position_m, m3.scale(b.velocity_m_s, h));
            b.orientation = b.orientation.integrate(b.angular_velocity_rad_s, h);
            inline for (.{ b.position_m, b.velocity_m_s, b.angular_velocity_rad_s }) |v|
                for (v) |x| if (!std.math.isFinite(x)) return error.NumericalFailure;
        }
        try self.finishLinks(h);

        // 5. Coupler updates (pawl, lifecycle, separation) in index order.
        self.coupler_reports.clearRetainingCapacity();
        for (0..self.couplers.items.len) |ci| {
            const cmd: backend_mod.Command = if (ci < inputs.coupler_commands.len) inputs.coupler_commands[ci] else .hold;
            try self.couplerUpdate(ci, cmd, h);
        }
    }

    fn applyGuideImpulse(self: *World, g: GuideRow, imp: m3.Vec3) void {
        const sp = self.couplers.items[g.coupler].spec;
        self.bodies.items[sp.body_b].applyImpulse(g.r_b, imp);
        self.bodies.items[sp.body_a].applyImpulse(g.r_a, m3.scale(imp, -1.0));
    }

    /// Guide-contact rows of every enabled coupler from the step-start pose
    /// (Q56 §4). Normals point from A toward B.
    fn detectGuides(self: *World) error{OutOfMemory}!void {
        self.guide_rows.clearRetainingCapacity();
        const s = self.settings;
        for (self.couplers.items, 0..) |*cp, ci| {
            const sp = cp.spec;
            if (!sp.guide_enabled) continue;
            const a = self.bodies.items[sp.body_a];
            const b = self.bodies.items[sp.body_b];
            const perp = perpendiculars(sp.axis_a);
            const cw = m3.add(b.position_m, b.orientation.rotate(sp.ball_centre_b_m));
            const cc = self.ballCentreCoupler(sp);
            var out: [13]?coupler_geometry.Contact = undefined;
            _ = coupler_geometry.contacts(sp.geom, cc, sp.ball_radius_m, &out);
            for (out, 0..) |maybe, fi| {
                const ct = maybe orelse continue;
                const n_a = m3.add(m3.scale(sp.axis_a, ct.normal[0]), m3.add(m3.scale(perp[0], ct.normal[1]), m3.scale(perp[1], ct.normal[2])));
                const n = a.orientation.rotate(n_a);
                const p = m3.sub(cw, m3.scale(n, sp.ball_radius_m));
                const r_a = m3.sub(p, a.position_m);
                const r_b = m3.sub(p, b.position_m);
                const t = perpendiculars(n);
                const vrel = m3.sub(b.pointVelocity(r_b), a.pointVelocity(r_a));
                const vt = m3.sub(vrel, m3.scale(n, m3.dot(vrel, n)));
                try self.guide_rows.append(self.gpa, .{
                    .coupler = @intCast(ci),
                    .feature = @intCast(fi),
                    .r_a = r_a,
                    .r_b = r_b,
                    .point = p,
                    .n = n,
                    .t = t,
                    .mu = if (m3.length(vt) <= s.static_slip_speed_m_s) sp.guide_mu_static else sp.guide_mu_kinetic,
                    .kn = a.effectiveMass(r_a, n) + b.effectiveMass(r_b, n),
                    .kt = .{ a.effectiveMass(r_a, t[0]) + b.effectiveMass(r_b, t[0]), a.effectiveMass(r_a, t[1]) + b.effectiveMass(r_b, t[1]) },
                    .c_coord = -ct.depth,
                    .p = if (s.warm_start) cp.guide_warm[fi] else .{ 0, 0, 0 },
                });
            }
        }
    }

    /// Pawl, link lifecycle and separation after a step (Q56 §6, §7), from
    /// that step's solver-native link report.
    fn couplerUpdate(self: *World, ci: usize, command: backend_mod.Command, h: f64) error{OutOfMemory}!void {
        const cp = &self.couplers.items[ci];
        const sp = cp.spec;
        const lk = &self.links.items[cp.link];
        const rep = self.link_reports.items[cp.link];
        const was_active = cp.was_active;
        const e_d = cp.e_during;
        const coords = [6]f64{ rep.extension_m[0], rep.extension_m[1], rep.extension_m[2], rep.rotation_rad[0], rep.rotation_rad[1], rep.rotation_rad[2] };
        const ks = [6]f64{ sp.k_axial_full, sp.k_shear_full, sp.k_shear_full, sp.k_torsion_full, sp.k_bend_full, sp.k_bend_full };
        var t_n: f64 = 0;
        var s_n: f64 = 0;
        var mb: f64 = 0;
        var mt: f64 = 0;
        var twice_v: f64 = 0; // Σ k_i C_i² (twice the full-engagement potential)
        if (was_active) {
            t_n = @max(0.0, -rep.force_on_b_n[0]);
            s_n = @sqrt(rep.force_on_b_n[1] * rep.force_on_b_n[1] + rep.force_on_b_n[2] * rep.force_on_b_n[2]);
            mb = @sqrt(rep.moment_on_b_nm[1] * rep.moment_on_b_nm[1] + rep.moment_on_b_nm[2] * rep.moment_on_b_nm[2]);
            mt = @abs(rep.moment_on_b_nm[0]);
            for (0..6) |i| twice_v += ks[i] * coords[i] * coords[i];
        }
        var separated_now = false;
        if (was_active and (t_n > e_d * sp.limit_tension_n or s_n > e_d * sp.limit_shear_n or
            mb > e_d * sp.limit_bending_nm or mt > e_d * sp.limit_torsion_nm))
        {
            lk.active = false;
            lk.p = @splat(0);
            cp.separation = if (command == .release) .released_under_load else .separated_overload;
            cp.armed = false;
            separated_now = true;
        }

        // Pawl.
        const q_abs = 0.5 * twice_v / sp.travel_m;
        const fr = sp.pawl_friction * t_n;
        var stalled = false;
        switch (command) {
            .hold => {},
            .engage => if (cp.u_m < sp.travel_m and !separated_now) {
                var ok = cp.armed and (cp.u_m > 0 or blk: {
                    const cc = self.ballCentreCoupler(sp);
                    const seat_x = coupler_geometry.seatX(sp.geom, sp.ball_radius_m);
                    break :blk @sqrt(cc[1] * cc[1] + cc[2] * cc[2]) <= sp.capture_radial_m and @abs(cc[0] - seat_x) <= sp.capture_axial_m;
                });
                if (ok and !(sp.actuator_force_n - q_abs > fr)) ok = false;
                if (ok) cp.u_m = @min(sp.travel_m, cp.u_m + sp.speed_limit_m_s * h) else stalled = true;
            },
            .release => if (cp.u_m > 0) {
                if (sp.actuator_force_n + q_abs > fr) {
                    cp.u_m = @max(0.0, cp.u_m - sp.speed_limit_m_s * h);
                } else stalled = true;
            },
        }

        // Link lifecycle.
        var removed = separated_now;
        if (cp.u_m > 0 and !lk.active and cp.armed and cp.separation == .none) {
            lk.active = true;
            lk.p = @splat(0);
            switch (self.audit_control) {
                .none => {},
                .velocity_snap_on_activation => self.bodies.items[sp.body_b].velocity_m_s = self.bodies.items[sp.body_a].velocity_m_s,
                .pose_snap_on_activation => {
                    const g = self.linkGeometry(lk.spec);
                    const b = &self.bodies.items[sp.body_b];
                    b.position_m = m3.sub(b.position_m, g.extension_world);
                },
            }
        }
        if (cp.u_m == 0) {
            if (lk.active) removed = true;
            lk.active = false;
            lk.p = @splat(0);
            cp.armed = true;
            cp.separation = .none;
        }
        const e_after = cp.u_m / sp.travel_m;
        const e_after_eff: f64 = if (removed) 0 else e_after;
        const work: f64 = if (was_active) 0.5 * twice_v * (e_after_eff - e_d) else 0;
        try self.coupler_reports.append(self.gpa, .{
            .u_m = cp.u_m,
            .e_during = e_d,
            .e_after = e_after,
            .active_during = was_active,
            .active_after = lk.active,
            .armed = cp.armed,
            .separation = cp.separation,
            .separated_this_step = separated_now,
            .pawl_stalled = stalled,
            .pawl_work_j = work,
            .tension_n = t_n,
            .shear_n = s_n,
            .bending_nm = mb,
            .torsion_nm = mt,
        });
    }

    /// Stores link warm-start impulses and builds the solver-native link
    /// reports (force and moment from the step's impulses ÷ h; extension and
    /// rotation from the post-step state), in the anchor-A frame.
    fn finishLinks(self: *World, h: f64) error{OutOfMemory}!void {
        self.link_reports.clearRetainingCapacity();
        for (self.links.items) |*lk| {
            if (lk.active) for (0..6) |ri| {
                lk.p[ri] = self.link_rows.items[lk.row0 + ri].p;
            };
            const g = self.linkGeometry(lk.spec);
            const a = self.bodies.items[lk.spec.body_a];
            const ext_loc = a.orientation.rotateInverse(g.extension_world);
            const rot_loc = a.orientation.rotateInverse(g.rotation_world);
            const perp = perpendiculars(lk.spec.axis_a);
            const basis: [3]m3.Vec3 = .{ lk.spec.axis_a, perp[0], perp[1] };
            var rep: backend_mod.LinkReport = .{ .body_a = lk.spec.body_a, .body_b = lk.spec.body_b, .force_on_b_n = m3.zero, .moment_on_b_nm = m3.zero, .extension_m = m3.zero, .rotation_rad = m3.zero };
            for (0..3) |i| {
                rep.force_on_b_n[i] = lk.p[i] / h;
                rep.moment_on_b_nm[i] = lk.p[3 + i] / h;
                rep.extension_m[i] = m3.dot(basis[i], ext_loc);
                rep.rotation_rad[i] = m3.dot(basis[i], rot_loc);
            }
            try self.link_reports.append(self.gpa, rep);
        }
    }

    /// Link geometry at the current state, for the initial sample before any
    /// step has produced forces (forces and moments are zero).
    pub fn linkGeometryReport(self: *const World, li: usize) backend_mod.LinkReport {
        const spec = self.links.items[li].spec;
        const g = self.linkGeometry(spec);
        const a = self.bodies.items[spec.body_a];
        const ext_loc = a.orientation.rotateInverse(g.extension_world);
        const rot_loc = a.orientation.rotateInverse(g.rotation_world);
        const perp = perpendiculars(spec.axis_a);
        const basis: [3]m3.Vec3 = .{ spec.axis_a, perp[0], perp[1] };
        var rep: backend_mod.LinkReport = .{ .body_a = spec.body_a, .body_b = spec.body_b, .force_on_b_n = m3.zero, .moment_on_b_nm = m3.zero, .extension_m = m3.zero, .rotation_rad = m3.zero };
        for (0..3) |i| {
            rep.extension_m[i] = m3.dot(basis[i], ext_loc);
            rep.rotation_rad[i] = m3.dot(basis[i], rot_loc);
        }
        return rep;
    }

    /// Canonical state order (DAT-004): body count, then per body: position,
    /// orientation (w, x, y, z), velocity, angular velocity, 8×3 warm impulses.
    pub fn encodeState(self: *World, e: canonical.BufferEncoder) backend_mod.EncodeError!void {
        try e.int(u32, @intCast(self.bodies.items.len));
        for (self.bodies.items) |b| {
            for (b.position_m) |x| try e.float(x);
            inline for (.{ "w", "x", "y", "z" }) |f| try e.float(@field(b.orientation, f));
            for (b.velocity_m_s) |x| try e.float(x);
            for (b.angular_velocity_rad_s) |x| try e.float(x);
            for (b.warm) |w| for (w) |x| try e.float(x);
        }
        // Link section: present only when the world has links, so link-free
        // worlds keep their original encoding. Per link, in declaration
        // order: the six warm-start row impulses (axial, shear 1, shear 2,
        // torsion, bend 1, bend 2).
        if (self.links.items.len > 0) {
            try e.int(u32, @intCast(self.links.items.len));
            for (self.links.items) |lk| for (lk.p) |x| try e.float(x);
        }
        // Coupler section: present only when the world has couplers, appended
        // after the link section. Per coupler: pawl travel, link-active,
        // armed, separation tag, then 13×3 guide warm-start impulses.
        if (self.couplers.items.len > 0) {
            try e.int(u32, @intCast(self.couplers.items.len));
            for (self.couplers.items) |cp| {
                try e.float(cp.u_m);
                try e.int(u32, @intFromBool(self.links.items[cp.link].active));
                try e.int(u32, @intFromBool(cp.armed));
                try e.int(u32, @intFromEnum(cp.separation));
                for (cp.guide_warm) |w| for (w) |x| try e.float(x);
            }
        }
    }

    fn identityFn(_: *anyopaque) backend_mod.Identity {
        return .{ .name = "kinigami-rigid", .version = "0.1.0" };
    }
    fn stepFn(ptr: *anyopaque, h: f64, inputs: backend_mod.StepInputs) backend_mod.StepError!void {
        const self: *World = @ptrCast(@alignCast(ptr));
        return self.step(h, inputs);
    }
    fn encodeFn(ptr: *anyopaque, e: canonical.BufferEncoder) backend_mod.EncodeError!void {
        const self: *World = @ptrCast(@alignCast(ptr));
        return self.encodeState(e);
    }
    fn contactsFn(ptr: *anyopaque) []const backend_mod.ContactReport {
        const self: *World = @ptrCast(@alignCast(ptr));
        return self.reports.items;
    }
};

/// Static (infinite-mass) cuboid centred at `centre_m`. Fixture validation only.
pub fn staticCuboid(size_m: m3.Vec3, centre_m: m3.Vec3) Body {
    return .{
        .mass_kg = 1.0, // unused: static bodies have infinite mass
        .inertia_kg_m2 = .{ 1, 1, 1 },
        .half_extents_m = m3.scale(size_m, 0.5),
        .position_m = centre_m,
        .is_static = true,
    };
}

/// Uniform solid cuboid resting with its bottom face on z = `bottom_z_m`.
pub fn cuboid(mass_kg: f64, size_m: m3.Vec3, bottom_z_m: f64) Body {
    const analytic = @import("analytic.zig");
    return .{
        .mass_kg = mass_kg,
        .inertia_kg_m2 = analytic.cuboidInertia(mass_kg, size_m),
        .half_extents_m = m3.scale(size_m, 0.5),
        .position_m = .{ 0, 0, bottom_z_m + size_m[2] / 2.0 },
    };
}

const testing = std.testing;

const test_settings: Settings = .{
    .contact_stiffness_n_m = 1e5,
    .contact_damping_n_s_m = 50,
    .static_slip_speed_m_s = 1e-5,
    .iterations = 100,
    .warm_start = true,
};

test "a body above the table falls freely with no contacts" {
    var w: World = .{ .gpa = testing.allocator, .settings = test_settings, .friction = .{ .mu_static = 0.5, .mu_kinetic = 0.4 }, .gravity_m_s2 = .{ 0, 0, -9.80665 } };
    defer w.deinit();
    _ = try w.addBody(cuboid(0.04, .{ 0.04, 0.04, 0.02 }, 0.1));
    for (0..10) |_| try w.step(0.001, .{});
    try testing.expectEqual(@as(usize, 0), w.reports.items.len);
    try testing.expectApproxEqRel(@as(f64, -9.80665 * 0.01), w.bodies.items[0].velocity_m_s[2], 1e-12);
}

test "a resting body is supported by four contacts carrying its weight" {
    var w: World = .{ .gpa = testing.allocator, .settings = test_settings, .friction = .{ .mu_static = 0.5, .mu_kinetic = 0.4 }, .gravity_m_s2 = .{ 0, 0, -9.80665 } };
    defer w.deinit();
    _ = try w.addBody(cuboid(0.04, .{ 0.04, 0.04, 0.02 }, 0));
    for (0..2000) |_| try w.step(0.0005, .{});
    var sum: f64 = 0;
    for (w.reports.items) |r| sum += r.normal_force_n;
    try testing.expectEqual(@as(usize, 4), w.reports.items.len);
    try testing.expectApproxEqRel(@as(f64, 0.04 * 9.80665), sum, 1e-6);
}

test "identical worlds produce identical canonical state (determinism)" {
    var a: World = .{ .gpa = testing.allocator, .settings = test_settings, .friction = .{ .mu_static = 0.5, .mu_kinetic = 0.4 }, .gravity_m_s2 = .{ 0, 0, -9.80665 } };
    defer a.deinit();
    var b: World = .{ .gpa = testing.allocator, .settings = test_settings, .friction = .{ .mu_static = 0.5, .mu_kinetic = 0.4 }, .gravity_m_s2 = .{ 0, 0, -9.80665 } };
    defer b.deinit();
    inline for (.{ &a, &b }) |w| {
        var body = cuboid(0.04, .{ 0.04, 0.04, 0.02 }, 0);
        body.velocity_m_s = .{ 0.3, 0.1, 0 };
        body.angular_velocity_rad_s = .{ 0, 0, 2 };
        _ = try w.addBody(body);
        for (0..500) |_| try w.step(0.001, .{});
    }
    var sa: canonical.BufferSink = .{ .gpa = testing.allocator };
    defer sa.deinit();
    var sb: canonical.BufferSink = .{ .gpa = testing.allocator };
    defer sb.deinit();
    try a.encodeState(sa.encoder());
    try b.encodeState(sb.encoder());
    try testing.expectEqualSlices(u8, sa.list.items, sb.list.items);
}

test "capture isolation with the real solver: live publication leaves checkpoint hashes unchanged (INS-007)" {
    const driver = @import("driver.zig");
    const snapshot = @import("snapshot.zig");
    const gpa = testing.allocator;
    var ring = try snapshot.BoundedRing.init(gpa, 8, 4096);
    defer ring.deinit(gpa);
    var with: [200]driver.Checkpoint = undefined;
    var without: [200]driver.Checkpoint = undefined;
    inline for (.{ &with, &without }, 0..) |out, i| {
        var w: World = .{ .gpa = gpa, .settings = test_settings, .friction = .{ .mu_static = 0.6, .mu_kinetic = 0.45 }, .gravity_m_s2 = .{ 0, 0, -9.80665 } };
        defer w.deinit();
        var body = cuboid(0.04, .{ 0.04, 0.04, 0.02 }, 0);
        body.velocity_m_s = .{ 0.4, 0.1, 0 };
        _ = try w.addBody(body);
        try driver.run(gpa, w.backend(), .{
            .unit = .{ .numerator = 1, .denominator = 1_000_000 },
            .step = .{ .step = .{ .ticks = 1000 } },
            .steps = 200,
            .publisher = if (i == 0) ring.publisher() else null,
        }, out);
    }
    try testing.expectEqualSlices(driver.Checkpoint, &without, &with);
    try testing.expectEqual(@as(u64, 200), ring.published);
}

// --- Fixture link tests (solver sanity; qualification is in link_suite) ---

const cube_edge = 0.02;
const cube_mass = 0.02;

fn linkWorld(gpa: std.mem.Allocator) World {
    return .{ .gpa = gpa, .settings = test_settings, .friction = .{ .mu_static = 0.6, .mu_kinetic = 0.45 }, .gravity_m_s2 = .{ 0, 0, -9.80665 }, .allow_static_bodies = true };
}

fn cubeLink(a: u32, b: u32, axis: m3.Vec3, k: f64, kt: f64, c: f64, ct: f64) LinkSpec {
    const half = cube_edge / 2.0;
    return .{ .body_a = a, .body_b = b, .axis_a = axis, .anchor_a_m = m3.scale(axis, half), .anchor_b_m = m3.scale(axis, -half), .rest_length_m = 0.01, .k_axial_n_m = k, .k_shear_n_m = k, .k_torsion_nm_rad = kt, .k_bend_nm_rad = kt, .c_axial_n_s_m = c, .c_shear_n_s_m = c, .c_torsion_nm_s_rad = ct, .c_bend_nm_s_rad = ct };
}

test "static bodies are refused unless the world is a fixture-validation world" {
    var w: World = .{ .gpa = testing.allocator, .settings = test_settings, .friction = .{ .mu_static = 0.5, .mu_kinetic = 0.4 }, .gravity_m_s2 = .{ 0, 0, -9.80665 } };
    defer w.deinit();
    try testing.expectError(error.StaticBodyNotPermitted, w.addBody(staticCuboid(.{ 1, 1, 1 }, m3.zero)));
}

test "a hanging body settles at the statics: tension = m·g, elongation = m·g/k" {
    var w = linkWorld(testing.allocator);
    defer w.deinit();
    const a = try w.addBody(staticCuboid(.{ cube_edge, cube_edge, cube_edge }, .{ 0, 0, 1 }));
    var body = cuboid(cube_mass, .{ cube_edge, cube_edge, cube_edge }, 0.96);
    body.position_m = .{ 0, 0, 0.97 };
    const b = try w.addBody(body);
    const k = 1000.0;
    _ = try w.addLink(cubeLink(a, b, .{ 0, 0, -1 }, k, 0.1, 2.0 * @sqrt(k * cube_mass), 2.0 * @sqrt(0.1 * cube_mass * cube_edge * cube_edge / 6.0)));
    for (0..4000) |_| try w.step(0.0005, .{});
    const r = w.link_reports.items[0];
    try testing.expectApproxEqRel(cube_mass * 9.80665, -r.force_on_b_n[0], 1e-6);
    try testing.expectApproxEqRel(cube_mass * 9.80665 / k, r.extension_m[0], 1e-6);
    try testing.expectEqual(m3.zero, w.bodies.items[a].velocity_m_s);
}

test "a free link oscillates at the analytic period with no numerical damping, and conserves momentum" {
    var w = linkWorld(testing.allocator);
    defer w.deinit();
    var ba = cuboid(cube_mass, .{ cube_edge, cube_edge, cube_edge }, 0);
    ba.position_m = .{ 0, 0, 10 };
    var bb = ba;
    bb.position_m = .{ 0.0305, 0, 10 };
    const a = try w.addBody(ba);
    const b = try w.addBody(bb);
    const k = 100.0;
    _ = try w.addLink(cubeLink(a, b, .{ 1, 0, 0 }, k, 0.01, 0, 0));
    const h = 0.002; // ω·h = 0.2
    var prev = w.linkGeometryReport(0).extension_m[0];
    var crossings: usize = 0;
    var first: f64 = 0;
    var last: f64 = 0;
    var peak: f64 = 0;
    var t: f64 = 0;
    for (0..500) |_| {
        try w.step(h, .{});
        t += h;
        const x = w.link_reports.items[0].extension_m[0];
        if ((prev > 0) != (x > 0)) {
            const tc = t - h + h * prev / (prev - x);
            if (crossings == 0) first = tc;
            last = tc;
            crossings += 1;
        }
        if (t > 0.5) peak = @max(peak, @abs(x));
        prev = x;
    }
    const period = 2.0 * (last - first) / @as(f64, @floatFromInt(crossings - 1));
    try testing.expectApproxEqRel(2.0 * std.math.pi / 100.0, period, 5e-3);
    try testing.expect(peak > 0.99 * 5e-4); // no decay
    const p = m3.add(m3.scale(w.bodies.items[a].velocity_m_s, cube_mass), m3.scale(w.bodies.items[b].velocity_m_s, cube_mass));
    try testing.expectApproxEqAbs(-2.0 * cube_mass * 9.80665 * t, p[2], 1e-10);
    try testing.expectApproxEqAbs(@as(f64, 0), p[0], 1e-12);
}

test "worlds with links are deterministic and include link state in the hash" {
    var sinks: [2]canonical.BufferSink = .{ .{ .gpa = testing.allocator }, .{ .gpa = testing.allocator } };
    defer for (&sinks) |*s| s.deinit();
    for (&sinks) |*sink| {
        var w = linkWorld(testing.allocator);
        defer w.deinit();
        const a = try w.addBody(staticCuboid(.{ cube_edge, cube_edge, cube_edge }, .{ 0, 0, 1 }));
        var body = cuboid(cube_mass, .{ cube_edge, cube_edge, cube_edge }, 0.96);
        body.position_m = .{ 0, 0, 0.97 };
        const b = try w.addBody(body);
        _ = try w.addLink(cubeLink(a, b, .{ 0, 0, -1 }, 1000, 0.1, 1, 1e-4));
        for (0..300) |_| try w.step(0.001, .{ .validation_loads = &.{.{ .body_index = b, .world_force_n = .{ 0.01, 0, 0 }, .world_torque_nm = m3.zero, .world_point_m = w.bodies.items[b].position_m }} });
        try w.encodeState(sink.encoder());
        try testing.expect(w.links.items[0].p[0] != 0);
    }
    try testing.expectEqualSlices(u8, sinks[0].list.items, sinks[1].list.items);
}

// --- Reduced fixture coupler tests (Q56/Q57; solver sanity, not qualification) ---

const cp_g: f64 = 9.80665;
const cp_dt: f64 = 1e-4;
const cp_travel: f64 = 1e-3;
const cp_speed: f64 = 0.01;
const cp_k: f64 = 1e4;
const cp_delta: f64 = 5e-5;
const cp_ks: f64 = 4.0 * 1e5 * 0.5; // 4·k_contact·sin²(45°)

fn testCouplerSpec(a: u32, b: u32, axis: m3.Vec3, guide: bool) CouplerSpec {
    const c_t = 2.0 * 0.2 * @sqrt(cp_k * 0.01);
    const c_r = 2.0 * 0.2 * @sqrt(1.0 * (0.02 * 0.0004 / 6.0 / 2.0));
    return .{
        .body_a = a,
        .body_b = b,
        .axis_a = axis,
        .face_offset_a_m = 0.01,
        .geom = .{ .apex_depth_m = 0.004, .mouth_half_width_m = 0.004, .face_half_size_m = 0.01 },
        .ball_radius_m = 0.002,
        .ball_centre_b_m = m3.scale(axis, -0.014),
        .preload_offset_m = cp_delta,
        .k_axial_full = cp_k,
        .k_shear_full = cp_k,
        .k_torsion_full = 1.0,
        .k_bend_full = 1.0,
        .c_axial_full = c_t,
        .c_shear_full = c_t,
        .c_torsion_full = c_r,
        .c_bend_full = c_r,
        .limit_tension_n = 2.0,
        .limit_shear_n = 1.0,
        .limit_bending_nm = 0.01,
        .limit_torsion_nm = 0.005,
        .travel_m = cp_travel,
        .speed_limit_m_s = cp_speed,
        .actuator_force_n = 0.3,
        .pawl_friction = 0.3,
        .capture_radial_m = 2e-4,
        .capture_axial_m = 2e-4,
        .guide_enabled = guide,
        .guide_mu_static = 0,
        .guide_mu_kinetic = 0,
    };
}

/// A static or dynamic cube A at `pa`, and B placed with its ball at the seat
/// point plus `offset_axial` along the axis. Returns the coupler index.
fn couplerPair(w: *World, a_static: bool, pa: m3.Vec3, axis: m3.Vec3, guide: bool, offset_axial: f64) !void {
    var ba = cuboid(cube_mass, .{ cube_edge, cube_edge, cube_edge }, 0);
    ba.position_m = pa;
    if (a_static) ba.is_static = true;
    const a = try w.addBody(ba);
    var bb = ba;
    bb.is_static = false;
    const seat_x = coupler_geometry.seatX(testCouplerSpec(0, 1, axis, guide).geom, 0.002);
    bb.position_m = m3.add(pa, m3.scale(axis, 0.01 + seat_x + 0.014 + offset_axial));
    const b = try w.addBody(bb);
    _ = try w.addCoupler(testCouplerSpec(a, b, axis, guide));
}

fn guideAxial(w: *const World, axis: m3.Vec3) struct { n: usize, axial: f64 } {
    var n: usize = 0;
    var sum: f64 = 0;
    for (w.reports.items) |r| {
        if (r.body_b == null) continue;
        if (r.normal_force_n > 0) n += 1;
        sum += r.normal_force_n * m3.dot(r.world_normal, axis);
    }
    return .{ .n = n, .axial = sum };
}

fn hangTest(extra_pull_total_factor: ?f64) !struct { t_mean: f64, n_mean: f64, n_guide: usize, n_reports: usize } {
    var w = linkWorld(testing.allocator);
    defer w.deinit();
    const axis: m3.Vec3 = .{ 0, 0, -1 };
    try couplerPair(&w, true, .{ 0, 0, 1 }, axis, true, 0);
    w.setCoupler(0, cp_travel, true);
    const f = cube_mass * cp_g;
    var extra: f64 = 0;
    if (extra_pull_total_factor) |fac| extra = fac * cp_k * cp_delta - f;
    var t_sum: f64 = 0;
    var n_sum: f64 = 0;
    var cnt: f64 = 0;
    var n_guide: usize = 0;
    var n_reports: usize = 0;
    for (0..5000) |i| {
        const load: backend_mod.AppliedLoad = .{ .body_index = 1, .world_force_n = m3.scale(axis, extra), .world_torque_nm = m3.zero, .world_point_m = w.bodies.items[1].position_m };
        try w.step(cp_dt, .{ .validation_loads = if (extra_pull_total_factor != null) &.{load} else &.{} });
        if (i >= 4000) {
            const g = guideAxial(&w, axis);
            t_sum += -w.link_reports.items[0].force_on_b_n[0];
            n_sum += g.axial;
            cnt += 1;
            n_guide = g.n;
            n_reports = 0;
            for (w.reports.items) |r| {
                if (r.body_b != null) n_reports += 1;
            }
        }
    }
    return .{ .t_mean = t_sum / cnt, .n_mean = n_sum / cnt, .n_guide = n_guide, .n_reports = n_reports };
}

test "coupler T1: seated, fully engaged, hanging: tension and seat force match the series-spring statics" {
    const f = cube_mass * cp_g;
    const t_ref = cp_k * (f + cp_ks * cp_delta) / (cp_k + cp_ks);
    const n_ref = cp_ks * (cp_k * cp_delta - f) / (cp_k + cp_ks);
    const r = try hangTest(null);
    std.debug.print("\nT1 tension {d:.6} (ref {d:.6}); seat force {d:.6} (ref {d:.6})\n", .{ r.t_mean, t_ref, r.n_mean, n_ref });
    try testing.expectApproxEqAbs(t_ref, r.t_mean, 1e-3);
    try testing.expectApproxEqAbs(n_ref, r.n_mean, 1e-3);
    try testing.expectEqual(@as(usize, 4), r.n_reports);
    try testing.expectEqual(@as(usize, 4), r.n_guide);
}

test "coupler T2: a pull above k·delta unseats the ball, below keeps four guide contacts" {
    const above = try hangTest(1.1);
    try testing.expectEqual(@as(usize, 0), above.n_guide);
    try testing.expectApproxEqAbs(1.1 * cp_k * cp_delta, above.t_mean, 1e-3);
    const below = try hangTest(0.9);
    try testing.expectEqual(@as(usize, 4), below.n_guide);
}

fn freeFallEngage(w: *World, axis: m3.Vec3, offset_axial: f64, steps: usize, cmd: backend_mod.Command, rec: ?*std.ArrayList(backend_mod.CouplerReport)) !void {
    try couplerPair(w, false, .{ 0, 0, 10 }, axis, true, offset_axial);
    for (0..steps) |_| {
        try w.step(cp_dt, .{ .coupler_commands = &.{cmd} });
        if (rec) |r| try r.append(testing.allocator, w.coupler_reports.items[0]);
    }
}

test "coupler T3: engagement ramps continuously in free fall and the preload settles at P" {
    var w = linkWorld(testing.allocator);
    defer w.deinit();
    var rec: std.ArrayList(backend_mod.CouplerReport) = .empty;
    defer rec.deinit(testing.allocator);
    const axis: m3.Vec3 = .{ 1, 0, 0 };
    try couplerPair(&w, false, .{ 0, 0, 10 }, axis, true, 0);
    var t_sum: f64 = 0;
    var cnt: f64 = 0;
    for (0..3000) |i| {
        try w.step(cp_dt, .{ .coupler_commands = &.{.engage} });
        try rec.append(testing.allocator, w.coupler_reports.items[0]);
        if (i >= 2500) {
            t_sum += -w.link_reports.items[0].force_on_b_n[0];
            cnt += 1;
        }
    }
    var reach: usize = 0;
    var prev_u: f64 = 0;
    var prev_e: f64 = 0;
    for (rec.items, 0..) |r, i| {
        if (reach == 0 and r.u_m >= cp_travel * (1 - 1e-9)) reach = i + 1;
        if (r.active_during) try testing.expect(prev_u > 0);
        try testing.expect(@abs(r.e_after - prev_e) <= cp_speed * cp_dt / cp_travel * (1 + 1e-12));
        prev_u = r.u_m;
        prev_e = r.e_after;
    }
    const expect_steps: f64 = cp_travel / (cp_speed * cp_dt);
    const p_ref = cp_delta * cp_k * cp_ks / (cp_k + cp_ks);
    std.debug.print("\nT3 steps to full travel {d} (expected {d}); final tension {d:.6} (P {d:.6})\n", .{ reach, expect_steps, t_sum / cnt, p_ref });
    try testing.expect(@abs(@as(f64, @floatFromInt(reach)) - expect_steps) <= 2);
    try testing.expect(!rec.items[0].active_during);
    try testing.expect(rec.items[3].active_during);
    try testing.expectApproxEqAbs(p_ref, t_sum / cnt, 1e-3);
}

test "coupler T4: engage is blocked outside the capture zone" {
    var w = linkWorld(testing.allocator);
    defer w.deinit();
    var rec: std.ArrayList(backend_mod.CouplerReport) = .empty;
    defer rec.deinit(testing.allocator);
    try freeFallEngage(&w, .{ 1, 0, 0 }, 1e-3, 300, .engage, &rec);
    for (rec.items) |r| {
        try testing.expectEqual(@as(f64, 0), r.u_m);
        try testing.expect(!r.active_during and !r.active_after);
        try testing.expect(r.pawl_stalled);
    }
}

fn overloadRun(factor: f64) !struct { sep_step: ?usize, w_force_after_zero: bool, kind: backend_mod.SeparationKind, ordered: bool, active_after: bool } {
    var w = linkWorld(testing.allocator);
    defer w.deinit();
    const axis: m3.Vec3 = .{ 1, 0, 0 };
    try couplerPair(&w, false, .{ 0, 0, 10 }, axis, false, -cp_delta);
    w.setCoupler(0, cp_travel, true);
    const target = factor * 2.0;
    var sep: ?usize = null;
    var zero_after = true;
    var ordered = true;
    for (0..6000) |i| {
        const t = @as(f64, @floatFromInt(i)) * cp_dt;
        const l = target * @min(t / 0.5, 1.0);
        const ba = w.bodies.items[0].position_m;
        const bb = w.bodies.items[1].position_m;
        const loads = [2]backend_mod.AppliedLoad{
            .{ .body_index = 1, .world_force_n = m3.scale(axis, l), .world_torque_nm = m3.zero, .world_point_m = bb },
            .{ .body_index = 0, .world_force_n = m3.scale(axis, -l), .world_torque_nm = m3.zero, .world_point_m = ba },
        };
        try w.step(cp_dt, .{ .validation_loads = &loads });
        const r = w.coupler_reports.items[0];
        const f = w.link_reports.items[0].force_on_b_n;
        if (sep) |_| {
            if (!(f[0] == 0 and f[1] == 0 and f[2] == 0) or w.links.items[0].active) zero_after = false;
        } else if (r.separated_this_step) {
            sep = i;
            if (!(r.tension_n > 2.0)) ordered = false;
        } else if (r.tension_n > 2.0) ordered = false;
    }
    return .{ .sep_step = sep, .w_force_after_zero = zero_after, .kind = w.couplers.items[0].separation, .ordered = ordered, .active_after = w.links.items[0].active };
}

test "coupler T5: overload separation at 1.1x the tension limit, none at 0.9x" {
    const hi = try overloadRun(1.1);
    std.debug.print("\nT5 1.1x: separated at step {?d}\n", .{hi.sep_step});
    try testing.expect(hi.sep_step != null);
    try testing.expect(hi.ordered);
    try testing.expect(hi.w_force_after_zero);
    try testing.expectEqual(backend_mod.SeparationKind.separated_overload, hi.kind);
    try testing.expect(!hi.active_after);
    const lo = try overloadRun(0.9);
    try testing.expect(lo.sep_step == null);
    try testing.expect(lo.ordered);
    try testing.expectEqual(backend_mod.SeparationKind.none, lo.kind);
    try testing.expect(lo.active_after);
}

test "coupler T6: coupler worlds are deterministic and include coupler state in the hash" {
    var sinks: [2]canonical.BufferSink = .{ .{ .gpa = testing.allocator }, .{ .gpa = testing.allocator } };
    defer for (&sinks) |*s| s.deinit();
    for (&sinks) |*sink| {
        var w = linkWorld(testing.allocator);
        defer w.deinit();
        try freeFallEngage(&w, .{ 1, 0, 0 }, 0, 400, .engage, null);
        try w.encodeState(sink.encoder());
        try testing.expect(w.couplers.items[0].u_m > 0);
    }
    try testing.expectEqualSlices(u8, sinks[0].list.items, sinks[1].list.items);
}

test "coupler T8: audit controls are refused outside fixture-validation worlds" {
    var w: World = .{ .gpa = testing.allocator, .settings = test_settings, .friction = .{ .mu_static = 0.5, .mu_kinetic = 0.4 }, .gravity_m_s2 = .{ 0, 0, -9.80665 } };
    defer w.deinit();
    _ = try w.addBody(cuboid(0.04, .{ 0.04, 0.04, 0.02 }, 0.1));
    w.audit_control = .velocity_snap_on_activation;
    try testing.expectError(error.InvalidInput, w.step(0.001, .{}));
    w.audit_control = .pose_snap_on_activation;
    try testing.expectError(error.InvalidInput, w.step(0.001, .{}));
    w.audit_control = .none;
    try w.step(0.001, .{});
}
