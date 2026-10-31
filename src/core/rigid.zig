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

    pub fn vertexBody(self: Body, i: usize) m3.Vec3 {
        const h = self.half_extents_m;
        return .{
            if (i & 1 != 0) h[0] else -h[0],
            if (i & 2 != 0) h[1] else -h[1],
            if (i & 4 != 0) h[2] else -h[2],
        };
    }

    fn invInertiaWorld(self: Body, v: m3.Vec3) m3.Vec3 {
        const b = self.orientation.rotateInverse(v);
        return self.orientation.rotate(.{ b[0] / self.inertia_kg_m2[0], b[1] / self.inertia_kg_m2[1], b[2] / self.inertia_kg_m2[2] });
    }

    fn applyImpulse(self: *Body, r: m3.Vec3, p: m3.Vec3) void {
        self.velocity_m_s = m3.add(self.velocity_m_s, m3.scale(p, 1.0 / self.mass_kg));
        self.angular_velocity_rad_s = m3.add(self.angular_velocity_rad_s, self.invInertiaWorld(m3.cross(r, p)));
    }

    fn pointVelocity(self: Body, r: m3.Vec3) m3.Vec3 {
        return m3.add(self.velocity_m_s, m3.cross(self.angular_velocity_rad_s, r));
    }

    fn effectiveMass(self: Body, r: m3.Vec3, d: m3.Vec3) f64 {
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

    pub fn deinit(self: *World) void {
        self.bodies.deinit(self.gpa);
        self.contacts.deinit(self.gpa);
        self.reports.deinit(self.gpa);
    }

    pub fn addBody(self: *World, b: Body) error{OutOfMemory}!u32 {
        try self.bodies.append(self.gpa, b);
        return @intCast(self.bodies.items.len - 1);
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

        // 2. External loads.
        for (self.bodies.items) |*b| {
            b.velocity_m_s = m3.add(b.velocity_m_s, m3.scale(self.gravity_m_s2, h));
        }
        for (inputs.validation_loads) |l| {
            if (l.body_index >= self.bodies.items.len) return error.InvalidInput;
            const b = &self.bodies.items[l.body_index];
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
            b.position_m = m3.add(b.position_m, m3.scale(b.velocity_m_s, h));
            b.orientation = b.orientation.integrate(b.angular_velocity_rad_s, h);
            inline for (.{ b.position_m, b.velocity_m_s, b.angular_velocity_rad_s }) |v|
                for (v) |x| if (!std.math.isFinite(x)) return error.NumericalFailure;
        }
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
