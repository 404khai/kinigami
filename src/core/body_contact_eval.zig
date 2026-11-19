//! Evaluation of the body-body contact fixture-validation criteria v1 (Q76,
//! Q77; `docs/validation/body-contact-v1-protocol.md`). Every metric is a pure
//! function of per-step `Sample`s recorded after each physics step and of the
//! generator output; the block-on-block analogues of analytic-v1 metrics are
//! computed by `fixture_eval` itself on the interface under test (same
//! definitions, protocol "Conventions").

const std = @import("std");
const m3 = @import("math3.zig");
const analytic = @import("analytic.zig");
const bcc = @import("body_contact_criteria.zig");
const fe = @import("fixture_eval.zig");
const box_contact = @import("box_contact.zig");

pub const Metric = fe.Metric;

pub const BodyState = struct {
    position_m: m3.Vec3,
    orientation: m3.Quat,
    velocity_m_s: m3.Vec3,
    angular_velocity_rad_s: m3.Vec3,
};

/// Solver-native contact output summed over one interface in one step.
pub const Iface = struct {
    normal_force_sum_n: f64 = 0,
    tangential_force_sum_n: m3.Vec3 = m3.zero,
    /// Fn-weighted mean contact point; null when no row carries load.
    center_of_pressure_m: ?m3.Vec3 = null,
    max_penetration_m: f64 = 0,
    rows: u32 = 0,
    /// Norm of the vector sum of the step's tangential impulses (N s).
    tangential_impulse_n_s: f64 = 0,
};

/// State after step n. Bodies are (0, 1): bottom/top (BB1), static slab and
/// block (BB2..BB5, BB7), A and B (BB8).
pub const Sample = struct {
    t_s: f64,
    bodies: [2]BodyState,
    /// Body-body interface (all rows of the pair).
    bb: Iface = .{},
    /// Tabletop interface (contacts of every body against z = 0).
    table: Iface = .{},
    /// Impulse the solver actually applied to each body through body-body rows
    /// during the step (warm start included).
    applied_n_s: [2]m3.Vec3 = .{ m3.zero, m3.zero },
    /// Impulse the solver reports for each body (contact reports times h).
    reported_n_s: [2]m3.Vec3 = .{ m3.zero, m3.zero },
};

/// A growing list of metrics; names given to `addFrom` are copied.
pub const List = struct {
    items: std.ArrayList(Metric) = .empty,

    pub fn add(self: *List, a: std.mem.Allocator, m: Metric) !void {
        try self.items.append(a, m);
    }

    pub fn addFrom(self: *List, a: std.mem.Allocator, prefix: []const u8, e: fe.Evaluation) !void {
        for (e.slice()) |m| {
            var c = m;
            c.name = try std.fmt.allocPrint(a, "{s}{s}", .{ prefix, m.name });
            try self.items.append(a, c);
        }
    }

    pub fn passed(self: List) bool {
        if (self.items.items.len == 0) return false;
        for (self.items.items) |m| if (!m.passed()) return false;
        return true;
    }
};

pub const Which = enum { bb, table };

/// The analytic-v1 evaluator's view of body `k` with the named interface.
pub fn toEval(s: Sample, k: usize, which: Which) fe.Sample {
    const i = switch (which) {
        .bb => s.bb,
        .table => s.table,
    };
    const b = s.bodies[k];
    return .{
        .t_s = s.t_s,
        .position_m = b.position_m,
        .orientation = b.orientation,
        .velocity_m_s = b.velocity_m_s,
        .angular_velocity_rad_s = b.angular_velocity_rad_s,
        .normal_force_sum_n = i.normal_force_sum_n,
        .tangential_force_sum_n = i.tangential_force_sum_n,
        .center_of_pressure_m = i.center_of_pressure_m,
        .max_penetration_m = i.max_penetration_m,
    };
}

pub fn evalSamples(a: std.mem.Allocator, samples: []const Sample, k: usize, which: Which) ![]fe.Sample {
    const out = try a.alloc(fe.Sample, samples.len);
    for (samples, 0..) |s, i| out[i] = toEval(s, k, which);
    return out;
}

/// Equal and opposite (BB1): at every step |F_on_A + F_on_B| / |F_on_A| of the
/// impulses the solver applied to the two bodies.
pub fn newtonThirdLaw(samples: []const Sample, tol: f64) Metric {
    var worst: f64 = 0;
    for (samples[1..]) |s| {
        const a = m3.length(s.applied_n_s[0]);
        const sum = m3.length(m3.add(s.applied_n_s[0], s.applied_n_s[1]));
        worst = @max(worst, if (a > 0) sum / a else if (sum > 0) std.math.inf(f64) else 0);
    }
    return .{ .name = "newton_third_law_rel_error", .value = worst, .limit = tol };
}

/// Slab footprint (BB2 above, BB3): the block CoM stays within the slab
/// half-size less the block half-size on each horizontal axis. Value is the
/// largest excess (<= 0 passes).
pub fn staysOnSlab(samples: []const Sample, slab_half_m: m3.Vec3, block_half_m: m3.Vec3) Metric {
    var worst = -std.math.inf(f64);
    const c = samples[0].bodies[0].position_m;
    for (samples) |s| {
        const d = m3.sub(s.bodies[1].position_m, c);
        worst = @max(worst, @max(@abs(d[0]) - (slab_half_m[0] - block_half_m[0]), @abs(d[1]) - (slab_half_m[1] - block_half_m[1])));
    }
    return .{ .name = "stays_on_slab_excess_m", .value = worst, .limit = 0 };
}

/// BB4 free flight and tunnelling. `slab_top_m` is the slab top height.
/// Contact rows come from the step-start pose, so the first sample that may
/// carry force is the one after the first sample with separation <= 0.
pub fn freeFlight(a: std.mem.Allocator, list: *List, samples: []const Sample, slab_top_m: f64, block_half_thickness_m: f64, peak_limit_m: f64) !void {
    var closed: ?usize = null;
    var first_force: ?usize = null;
    var early: f64 = 0;
    var min_z = std.math.inf(f64);
    for (samples, 0..) |s, i| {
        const sep = s.bodies[1].position_m[2] - block_half_thickness_m - slab_top_m;
        if (closed == null and sep <= 0) closed = i;
        const force = s.bb.normal_force_sum_n != 0;
        if (force and first_force == null) first_force = i;
        if (force and closed == null) early = 1;
        if (force and closed != null and i <= closed.?) early = 1;
        min_z = @min(min_z, s.bodies[1].position_m[2]);
    }
    try list.add(a, .{ .name = "force_before_clearance_closes", .value = early, .limit = 0 });
    try list.add(a, .{ .name = "contact_after_clearance_closes", .value = if (first_force != null and closed != null and first_force.? > closed.?) 1 else 0, .limit = 1, .at_least = true });
    try list.add(a, .{ .name = "tunnelling_margin_m", .value = min_z - (slab_top_m + block_half_thickness_m - peak_limit_m), .limit = 0, .at_least = true });
}

pub fn maxBbPenetration(samples: []const Sample) f64 {
    var p: f64 = 0;
    for (samples) |s| p = @max(p, s.bb.max_penetration_m);
    return p;
}

// --- BB6 ---

pub const Bb6Result = struct {
    axis: u8,
    count: u8,
    normal: m3.Vec3,
    depths: [box_contact.max_points]f64,
    points: [box_contact.max_points]m3.Vec3,
};

fn lessPoint(_: void, a: m3.Vec3, b: m3.Vec3) bool {
    if (a[0] != b[0]) return a[0] < b[0];
    if (a[1] != b[1]) return a[1] < b[1];
    return a[2] < b[2];
}

/// Generator output for one ordered pair, points sorted by (x, y, z).
pub fn bb6Result(a: box_contact.Box, b: box_contact.Box) ?Bb6Result {
    const m = box_contact.collide(a, b) orelse return null;
    var r: Bb6Result = .{ .axis = m.axis, .count = m.count, .normal = m.normal, .depths = @splat(0), .points = @splat(m3.zero) };
    for (m.slice(), 0..) |p, i| {
        r.points[i] = p.point;
        r.depths[i] = p.depth;
    }
    std.mem.sort(m3.Vec3, r.points[0..r.count], {}, lessPoint);
    return r;
}

/// Compares a generator result with the closed form of configuration `cf`.
/// `swapped` negates the expected normal and skips the axis check (the axis
/// index refers to the other box order). With `swap_translate` (criteria v2,
/// Q79) each expected point is the (A, B) point translated by the depth along
/// the (A, B) normal, since swapping exchanges the incident box.
pub fn bb6Check(a: std.mem.Allocator, list: *List, prefix: []const u8, cf: bcc.Bb6Config, expected_axis: u8, tol: anytype, got: ?Bb6Result, swapped: bool, swap_translate: bool) !void {
    const nm = struct {
        fn n(al: std.mem.Allocator, p: []const u8, s: []const u8) ![]const u8 {
            return std.fmt.allocPrint(al, "{s}{s}", .{ p, s });
        }
    }.n;
    const r = got orelse {
        try list.add(a, .{ .name = try nm(a, prefix, "generated"), .value = 0, .limit = 1, .at_least = true });
        return;
    };
    try list.add(a, .{ .name = try nm(a, prefix, "count_error"), .value = @abs(@as(f64, @floatFromInt(r.count)) - @as(f64, @floatFromInt(cf.expected_count))), .limit = 0 });
    if (!swapped) try list.add(a, .{ .name = try nm(a, prefix, "axis_error"), .value = @abs(@as(f64, @floatFromInt(r.axis)) - @as(f64, @floatFromInt(expected_axis))), .limit = 0 });
    const sign: f64 = if (swapped) -1.0 else 1.0;
    var nerr: f64 = 0;
    for (0..3) |i| nerr = @max(nerr, @abs(r.normal[i] - sign * cf.expected_normal[i]));
    try list.add(a, .{ .name = try nm(a, prefix, "normal_component_error"), .value = nerr, .limit = tol.normal_component_abs_tol });
    var derr: f64 = 0;
    var perr: f64 = 0;
    var exp_pts: [box_contact.max_points]m3.Vec3 = @splat(m3.zero);
    const n = @min(cf.expected_points_m.len, box_contact.max_points);
    for (cf.expected_points_m[0..n], 0..) |p, i| exp_pts[i] = if (swapped and swap_translate) m3.add(p, m3.scale(cf.expected_normal, cf.expected_depth_m)) else p;
    std.mem.sort(m3.Vec3, exp_pts[0..n], {}, lessPoint);
    if (r.count == n) {
        for (0..n) |i| {
            derr = @max(derr, @abs(r.depths[i] - cf.expected_depth_m) / @max(@abs(cf.expected_depth_m), tol.position_scale_m));
            for (0..3) |k| perr = @max(perr, @abs(r.points[i][k] - exp_pts[i][k]) / @max(@abs(exp_pts[i][k]), tol.position_scale_m));
        }
    } else {
        derr = std.math.inf(f64);
        perr = std.math.inf(f64);
    }
    try list.add(a, .{ .name = try nm(a, prefix, "depth_rel_error"), .value = derr, .limit = tol.position_depth_rel_tol });
    try list.add(a, .{ .name = try nm(a, prefix, "point_rel_error"), .value = perr, .limit = tol.position_depth_rel_tol });
}

// --- BB7 ---

fn mean(xs: []const f64) f64 {
    var s: f64 = 0;
    for (xs) |x| s += x;
    return if (xs.len > 0) s / @as(f64, @floatFromInt(xs.len)) else std.math.nan(f64);
}

fn inWindow(s: Sample, a: f64, b: f64) bool {
    return s.t_s >= a and s.t_s <= b;
}

pub const Bb7Tol = struct { rel_tol: f64, abs_floor: f64, step_index_tol: f64 };

fn ratio(a: f64, b: f64, scale: f64, tol: Bb7Tol, extra: f64) f64 {
    if (!std.math.isFinite(a) or !std.math.isFinite(b)) return std.math.nan(f64);
    return @abs(a - b) / (tol.rel_tol * @max(@abs(b), scale) + tol.abs_floor + extra);
}

/// Body-relative quantities of the rest scene S1 (protocol "BB7 transform").
pub const S1Quantities = struct {
    normal_force_mean_n: f64,
    tangential_force_max_n: f64,
    cop_top_frame_m: m3.Vec3,
    max_penetration_m: f64,
    rotation_vs_slab_rad: f64,
    displacement_slab_frame_m: f64,
};

pub fn s1Quantities(samples: []const Sample, window_start_s: f64, end_s: f64) S1Quantities {
    var fsum: f64 = 0;
    var n: f64 = 0;
    var tmax: f64 = 0;
    var cop = m3.zero;
    var rot: f64 = 0;
    var disp: f64 = 0;
    var ref: ?Sample = null;
    for (samples) |s| {
        if (!inWindow(s, window_start_s, end_s)) continue;
        const r = ref orelse blk: {
            ref = s;
            break :blk s;
        };
        n += 1;
        fsum += s.bb.normal_force_sum_n;
        tmax = @max(tmax, m3.length(s.bb.tangential_force_sum_n));
        const top = s.bodies[1];
        if (s.bb.center_of_pressure_m) |c| {
            cop = m3.add(cop, top.orientation.rotateInverse(m3.sub(c, top.position_m)));
        } else cop = .{ std.math.nan(f64), 0, 0 };
        const q_slab = s.bodies[0].orientation;
        rot = @max(rot, (m3.Quat{ .w = q_slab.w, .x = -q_slab.x, .y = -q_slab.y, .z = -q_slab.z }).mul(top.orientation).angle());
        disp = @max(disp, m3.length(q_slab.rotateInverse(m3.sub(top.position_m, r.bodies[1].position_m))));
    }
    return .{
        .normal_force_mean_n = if (n > 0) fsum / n else std.math.nan(f64),
        .tangential_force_max_n = tmax,
        .cop_top_frame_m = if (n > 0) m3.scale(cop, 1.0 / n) else .{ std.math.nan(f64), 0, 0 },
        .max_penetration_m = maxBbPenetration(samples),
        .rotation_vs_slab_rad = rot,
        .displacement_slab_frame_m = disp,
    };
}

pub fn compareS1(a: std.mem.Allocator, list: *List, id: []const u8, got: S1Quantities, ref: S1Quantities, tol: Bb7Tol) !void {
    const f = struct {
        fn name(al: std.mem.Allocator, i: []const u8, s: []const u8) ![]const u8 {
            return std.fmt.allocPrint(al, "{s}.{s}", .{ i, s });
        }
    }.name;
    try list.add(a, .{ .name = try f(a, id, "normal_force_mean_over_allowance"), .value = ratio(got.normal_force_mean_n, ref.normal_force_mean_n, 1, tol, 0), .limit = 1 });
    try list.add(a, .{ .name = try f(a, id, "tangential_force_max_over_allowance"), .value = ratio(got.tangential_force_max_n, ref.tangential_force_max_n, 1, tol, 0), .limit = 1 });
    var cop: f64 = 0;
    for (0..3) |i| cop = @max(cop, ratio(got.cop_top_frame_m[i], ref.cop_top_frame_m[i], 0.04, tol, 0));
    try list.add(a, .{ .name = try f(a, id, "cop_top_frame_over_allowance"), .value = cop, .limit = 1 });
    try list.add(a, .{ .name = try f(a, id, "max_penetration_over_allowance"), .value = ratio(got.max_penetration_m, ref.max_penetration_m, 0.04, tol, 0), .limit = 1 });
    try list.add(a, .{ .name = try f(a, id, "rotation_vs_slab_over_allowance"), .value = ratio(got.rotation_vs_slab_rad, ref.rotation_vs_slab_rad, 1, tol, 0), .limit = 1 });
    try list.add(a, .{ .name = try f(a, id, "displacement_slab_frame_over_allowance"), .value = ratio(got.displacement_slab_frame_m, ref.displacement_slab_frame_m, 0.04, tol, 0), .limit = 1 });
}

/// Body-relative quantities of the slide scene S3. The stop is the first
/// sample whose bottom-face-centre speed (v + w x r, r from the CoM to the
/// bottom-face centre), taken in the slab frame and ignoring the slab-normal
/// component, is <= the threshold (analytic-v1 revision 2 definition made
/// frame independent).
pub const S3Quantities = struct {
    stopped: bool,
    stop_index: f64,
    stop_time_s: f64,
    stop_distance_m: f64,
    post_stop_drift_m: f64,
    max_penetration_m: f64,
};

pub fn s3Quantities(samples: []const Sample, half_thickness_m: f64, threshold_m_s: f64, slide_dir_world: m3.Vec3) S3Quantities {
    var out: S3Quantities = .{ .stopped = false, .stop_index = 0, .stop_time_s = 0, .stop_distance_m = 0, .post_stop_drift_m = 0, .max_penetration_m = maxBbPenetration(samples) };
    const x0 = samples[0].bodies[1].position_m;
    var stop: ?Sample = null;
    for (samples[1..], 1..) |s, i| {
        const top = s.bodies[1];
        const qs = s.bodies[0].orientation;
        if (stop) |st| {
            const d = qs.rotateInverse(m3.sub(top.position_m, st.bodies[1].position_m));
            out.post_stop_drift_m = @max(out.post_stop_drift_m, m3.horizontalLength(d));
        } else {
            const r = top.orientation.rotate(.{ 0, 0, -half_thickness_m });
            const v = qs.rotateInverse(m3.add(top.velocity_m_s, m3.cross(top.angular_velocity_rad_s, r)));
            if (m3.horizontalLength(v) <= threshold_m_s) {
                stop = s;
                out.stopped = true;
                out.stop_index = @floatFromInt(i);
                out.stop_time_s = s.t_s;
                out.stop_distance_m = m3.dot(m3.sub(top.position_m, x0), slide_dir_world);
            }
        }
    }
    return out;
}

pub fn compareS3(a: std.mem.Allocator, list: *List, id: []const u8, got: S3Quantities, ref: S3Quantities, tol: Bb7Tol, dt_s: f64) !void {
    const nm = struct {
        fn name(al: std.mem.Allocator, i: []const u8, s: []const u8) ![]const u8 {
            return std.fmt.allocPrint(al, "{s}.{s}", .{ i, s });
        }
    }.name;
    try list.add(a, .{ .name = try nm(a, id, "stopped_both"), .value = if (got.stopped and ref.stopped) 1 else 0, .limit = 1, .at_least = true });
    if (!(got.stopped and ref.stopped)) return;
    try list.add(a, .{ .name = try nm(a, id, "stop_step_index_difference"), .value = @abs(got.stop_index - ref.stop_index), .limit = tol.step_index_tol });
    // The stop time is index x step, so it inherits the index allowance.
    try list.add(a, .{ .name = try nm(a, id, "stop_time_over_allowance"), .value = ratio(got.stop_time_s, ref.stop_time_s, 1, tol, tol.step_index_tol * dt_s), .limit = 1 });
    try list.add(a, .{ .name = try nm(a, id, "stop_distance_over_allowance"), .value = ratio(got.stop_distance_m, ref.stop_distance_m, 0.04, tol, 0), .limit = 1 });
    try list.add(a, .{ .name = try nm(a, id, "post_stop_drift_over_allowance"), .value = ratio(got.post_stop_drift_m, ref.post_stop_drift_m, 0.04, tol, 0), .limit = 1 });
    try list.add(a, .{ .name = try nm(a, id, "max_penetration_over_allowance"), .value = ratio(got.max_penetration_m, ref.max_penetration_m, 0.04, tol, 0), .limit = 1 });
}

// --- BB8 ---

pub const Bb8Body = struct { mass_kg: f64, inertia_kg_m2: m3.Vec3 };

pub const Bb8Params = struct {
    bodies: [2]Bb8Body,
    g_n: f64,
    mom_rel: f64,
    mom_floor: f64,
    ang_rel: f64,
    ang_floor: f64,
    r_ref_m: f64,
    imp_rel: f64,
    imp_floor: f64,
    energy_rel: f64,
    energy_coeff: f64,
    energy_floor: f64,
    omega_ref_rad_s: f64,
    dt_s: f64,
    min_peak_tangential_impulse: f64,
};

/// One body's kinematic state for the momentum audits (mutable copy).
pub const Kin = struct { v: m3.Vec3, w: m3.Vec3 };

fn worldInertiaOmega(b: Bb8Body, q: m3.Quat, w: m3.Vec3) m3.Vec3 {
    const wb = q.rotateInverse(w);
    return q.rotate(.{ b.inertia_kg_m2[0] * wb[0], b.inertia_kg_m2[1] * wb[1], b.inertia_kg_m2[2] * wb[2] });
}

fn linMomentum(p: Bb8Params, kin: [2]Kin) m3.Vec3 {
    return m3.add(m3.scale(kin[0].v, p.bodies[0].mass_kg), m3.scale(kin[1].v, p.bodies[1].mass_kg));
}

fn angMomentum(p: Bb8Params, s: Sample, kin: [2]Kin) m3.Vec3 {
    var l = m3.zero;
    for (0..2) |k| {
        const b = s.bodies[k];
        l = m3.add(l, m3.cross(b.position_m, m3.scale(kin[k].v, p.bodies[k].mass_kg)));
        l = m3.add(l, worldInertiaOmega(p.bodies[k], b.orientation, kin[k].w));
    }
    return l;
}

fn kinOf(s: Sample) [2]Kin {
    return .{ .{ .v = s.bodies[0].velocity_m_s, .w = s.bodies[0].angular_velocity_rad_s }, .{ .v = s.bodies[1].velocity_m_s, .w = s.bodies[1].angular_velocity_rad_s } };
}

/// Linear and angular momentum audit ratios over t > 0 for a kinematic trace
/// (`kins[i]` goes with `samples[i]`); pass when both <= 1.
pub fn momentumAudit(p: Bb8Params, samples: []const Sample, kins: []const [2]Kin) struct { linear: f64, angular: f64 } {
    const m_total = p.bodies[0].mass_kg + p.bodies[1].mass_kg;
    const p0 = linMomentum(p, kins[0]);
    const l0 = angMomentum(p, samples[0], kins[0]);
    var lin: f64 = 0;
    var ang: f64 = 0;
    for (samples[1..], 1..) |s, i| {
        const dp = m3.length(m3.sub(linMomentum(p, kins[i]), p0));
        const dl = m3.length(m3.sub(angMomentum(p, s, kins[i]), l0));
        lin = @max(lin, dp / (p.mom_rel * m_total * p.g_n * s.t_s + p.mom_floor));
        ang = @max(ang, dl / (p.ang_rel * m_total * p.g_n * s.t_s * p.r_ref_m + p.ang_floor));
    }
    return .{ .linear = lin, .angular = ang };
}

fn kineticEnergy(p: Bb8Params, s: Sample) f64 {
    var e: f64 = 0;
    for (0..2) |k| {
        const b = s.bodies[k];
        e += 0.5 * p.bodies[k].mass_kg * m3.dot(b.velocity_m_s, b.velocity_m_s);
        e += 0.5 * m3.dot(b.angular_velocity_rad_s, worldInertiaOmega(p.bodies[k], b.orientation, b.angular_velocity_rad_s));
    }
    return e;
}

/// Control applied to a copy of the trace from the first sample with body-body
/// rows on (CPL-004 style): B's linear velocity is set to A's, or B's angular
/// velocity is reset to its pre-contact value (zero); the change persists in
/// every later sample.
pub const Control = enum { velocity_snap, angular_velocity_snap };

pub fn applyControl(a: std.mem.Allocator, samples: []const Sample, control: Control) ![][2]Kin {
    const kins = try a.alloc([2]Kin, samples.len);
    for (samples, 0..) |s, i| kins[i] = kinOf(s);
    var first: ?usize = null;
    for (samples, 0..) |s, i| if (s.bb.rows > 0) {
        first = i;
        break;
    };
    const f = first orelse return kins;
    const dv = m3.sub(kins[f][0].v, kins[f][1].v);
    // B spins up with A in this scene (equal sense, equal magnitude by the
    // symmetry of the eccentric impulse), so "B's w := A's w" would be a null
    // change. The angular snap instead undoes the contact's angular impulse on
    // B: its angular velocity returns to the pre-contact value, which is zero.
    const dw = m3.scale(kins[f][1].w, -1.0);
    for (kins[f..]) |*k| switch (control) {
        .velocity_snap => k[1].v = m3.add(k[1].v, dv),
        .angular_velocity_snap => k[1].w = m3.add(k[1].w, dw),
    };
    return kins;
}

/// BB8 audits on the real trace plus the two discrimination controls.
pub fn bb8(a: std.mem.Allocator, list: *List, p: Bb8Params, samples: []const Sample, final_overlap: bool) !void {
    const kins = try a.alloc([2]Kin, samples.len);
    for (samples, 0..) |s, i| kins[i] = kinOf(s);
    const au = momentumAudit(p, samples, kins);
    try list.add(a, .{ .name = "momentum_over_allowance", .value = au.linear, .limit = 1 });
    try list.add(a, .{ .name = "angular_momentum_over_allowance", .value = au.angular, .limit = 1 });

    var acct: f64 = 0;
    var pose_bad: f64 = 0;
    var peak_tan: f64 = 0;
    for (samples[1..], 1..) |s, i| {
        const prev = samples[i - 1];
        for (0..2) |k| {
            const dp = m3.scale(m3.sub(s.bodies[k].velocity_m_s, prev.bodies[k].velocity_m_s), p.bodies[k].mass_kg);
            const rep = s.reported_n_s[k];
            acct = @max(acct, m3.length(m3.sub(dp, rep)) / (p.imp_rel * m3.length(rep) + p.imp_floor));
            const h = p.dt_s;
            const pos = m3.add(prev.bodies[k].position_m, m3.scale(s.bodies[k].velocity_m_s, h));
            const q = prev.bodies[k].orientation.integrate(s.bodies[k].angular_velocity_rad_s, h);
            const qb = s.bodies[k].orientation;
            if (!std.meta.eql(pos, s.bodies[k].position_m) or q.w != qb.w or q.x != qb.x or q.y != qb.y or q.z != qb.z) pose_bad += 1;
        }
        peak_tan = @max(peak_tan, s.bb.tangential_impulse_n_s);
    }
    try list.add(a, .{ .name = "impulse_accounting_over_allowance", .value = acct, .limit = 1 });
    try list.add(a, .{ .name = "pose_integration_mismatches", .value = pose_bad, .limit = 0 });
    const e0 = kineticEnergy(p, samples[0]);
    const ef = kineticEnergy(p, samples[samples.len - 1]);
    const allowance = (p.energy_rel + p.energy_coeff * p.omega_ref_rad_s * p.dt_s) * e0 + p.energy_floor;
    try list.add(a, .{ .name = "energy_creation_over_allowance", .value = ef - e0 - allowance, .limit = 0 });
    try list.add(a, .{ .name = "energy_dissipated_j", .value = e0 - ef, .limit = 0, .informational = true });
    try list.add(a, .{ .name = "final_sample_overlap", .value = if (final_overlap) 1 else 0, .limit = 0 });
    try list.add(a, .{ .name = "peak_tangential_impulse_n_s", .value = peak_tan, .limit = p.min_peak_tangential_impulse, .at_least = true });
    inline for (.{ Control.velocity_snap, Control.angular_velocity_snap }) |c| {
        const ck = try applyControl(a, samples, c);
        const ca = momentumAudit(p, samples, ck);
        const detected = ca.linear > 1 or ca.angular > 1;
        try list.add(a, .{ .name = "control_" ++ @tagName(c) ++ "_undetected", .value = if (detected) 0 else 1, .limit = 0 });
    }
}
