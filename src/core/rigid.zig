//! Custom production rigid-body backend, first capability: rigid cuboids
//! with gravity and compliant contact against the reference tabletop
//! (Q35, Q41, Q47, PHY-001, PHY-002, PHY-005..007).
//!
//! Status: implemented, **not qualified**. Capabilities beyond cuboid-vs-
//! tabletop contact (body-body contact, links, couplers) do not exist yet.
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
//! Static bodies (infinite mass, never move) are permitted only when the
//! world is flagged `allow_static_bodies` by fixture-validation code.

const std = @import("std");
const m3 = @import("math3.zig");
const canonical = @import("canonical.zig");
const backend_mod = @import("backend.zig");

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

    pub fn deinit(self: *World) void {
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
        const s = self.settings;
        self.contacts.clearRetainingCapacity();

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
        for (self.links.items, 0..) |lk, li| {
            const g = self.linkGeometry(lk.spec);
            try self.link_geoms.append(self.gpa, g);
            const sp = lk.spec;
            const ba = self.bodies.items[sp.body_a];
            const bb = self.bodies.items[sp.body_b];
            const ks = [6]f64{ sp.k_axial_n_m, sp.k_shear_n_m, sp.k_shear_n_m, sp.k_torsion_nm_rad, sp.k_bend_nm_rad, sp.k_bend_nm_rad };
            const cs = [6]f64{ sp.c_axial_n_s_m, sp.c_shear_n_s_m, sp.c_shear_n_s_m, sp.c_torsion_nm_s_rad, sp.c_bend_nm_s_rad, sp.c_bend_nm_s_rad };
            for (0..6) |ri| {
                const rot = ri >= 3;
                const e = g.axes_world[ri % 3];
                var row: LinkRow = .{
                    .link = @intCast(li),
                    .index = @intCast(ri),
                    .rot = rot,
                    .e = e,
                    .c_coord = m3.dot(e, if (rot) g.rotation_world else g.extension_world),
                    .jv0 = 0,
                    .kin = if (rot) m3.dot(e, ba.invInertiaWorld(e)) + m3.dot(e, bb.invInertiaWorld(e)) else ba.effectiveMass(g.r_a, e) + bb.effectiveMass(g.r_b, e),
                    .k = ks[ri],
                    .c = cs[ri],
                    .p = if (s.warm_start) lk.p[ri] else 0,
                };
                row.jv0 = self.rowRate(row);
                try self.link_rows.append(self.gpa, row);
            }
        }

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
        for (self.bodies.items) |*b| {
            if (b.is_static) continue;
            b.position_m = m3.add(b.position_m, m3.scale(b.velocity_m_s, h));
            b.orientation = b.orientation.integrate(b.angular_velocity_rad_s, h);
            inline for (.{ b.position_m, b.velocity_m_s, b.angular_velocity_rad_s }) |v|
                for (v) |x| if (!std.math.isFinite(x)) return error.NumericalFailure;
        }
        try self.finishLinks(h);
    }

    /// Stores link warm-start impulses and builds the solver-native link
    /// reports (force and moment from the step's impulses ÷ h; extension and
    /// rotation from the post-step state), in the anchor-A frame.
    fn finishLinks(self: *World, h: f64) error{OutOfMemory}!void {
        self.link_reports.clearRetainingCapacity();
        for (self.links.items, 0..) |*lk, li| {
            for (0..6) |ri| lk.p[ri] = self.link_rows.items[li * 6 + ri].p;
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
