//! Evaluation protocol for the analytic fixture-validation criteria v1
//! (Q46–Q48, BEN-010..015). Committed before any production solver code.
//!
//! The evaluator sees ground truth only through `Sample`s recorded after
//! each physics step (Q32: evaluator, not controller). Every metric is a
//! pure function of the samples, the criteria, and the closed-form
//! references in `analytic.zig`. Precise definitions:
//!
//! - Sample times are the end-of-step times t_n = n·Δt, n = 1..N; the initial
//!   state is sample 0 at t = 0.
//! - A window [a, b] includes every sample with a ≤ t ≤ b.
//! - "Horizontal" means the world x–y components.
//! - Contact forces are the solver-native outputs of the step that produced
//!   the sample (PHY-005): their sums, and the centre of pressure
//!   Σ(Fn_i · p_i) / Σ Fn_i over contacts with Fn_i > 0.
//! - Penetration is max(0, −z) over contact points.

const std = @import("std");
const m3 = @import("math3.zig");
const analytic = @import("analytic.zig");
const criteria = @import("criteria.zig");

pub const Sample = struct {
    t_s: f64,
    position_m: m3.Vec3,
    orientation: m3.Quat,
    velocity_m_s: m3.Vec3,
    angular_velocity_rad_s: m3.Vec3 = m3.zero,
    normal_force_sum_n: f64,
    tangential_force_sum_n: m3.Vec3,
    /// Null when no contact carries normal load.
    center_of_pressure_m: ?m3.Vec3,
    max_penetration_m: f64,
};

pub const Metric = struct {
    name: []const u8,
    value: f64,
    limit: f64,
    /// `value ≤ limit` passes unless `at_least` (then `value ≥ limit`).
    at_least: bool = false,
    /// Reported for transparency only; never affects the outcome.
    informational: bool = false,

    pub fn passed(m: Metric) bool {
        if (m.informational) return true;
        if (!std.math.isFinite(m.value)) return false;
        return if (m.at_least) m.value >= m.limit else m.value <= m.limit;
    }
};

pub const max_metrics = 8;

/// Protocol revision implemented here (see the revision log).
pub const protocol_revision: u32 = 2;

pub const Evaluation = struct {
    metrics: [max_metrics]Metric = undefined,
    len: usize = 0,

    fn add(self: *Evaluation, m: Metric) void {
        self.metrics[self.len] = m;
        self.len += 1;
    }

    pub fn slice(self: *const Evaluation) []const Metric {
        return self.metrics[0..self.len];
    }

    pub fn passed(self: *const Evaluation) bool {
        if (self.len == 0) return false;
        for (self.slice()) |m| if (!m.passed()) return false;
        return true;
    }
};

fn inWindow(s: Sample, a: f64, b: f64) bool {
    return s.t_s >= a and s.t_s <= b;
}

fn maxPenetration(samples: []const Sample) f64 {
    var p: f64 = 0;
    for (samples) |s| p = @max(p, s.max_penetration_m);
    return p;
}

/// Rest: all metrics over the window [window_start_s, duration_s] except
/// penetration (whole run). Drift is measured from the first window sample.
pub fn rest(c: criteria.RestCase, f: criteria.Fixture, g: f64, samples: []const Sample) Evaluation {
    var e: Evaluation = .{};
    const w = analytic.weight(f.mass_kg, g);
    var sum: f64 = 0;
    var n: f64 = 0;
    var max_tan: f64 = 0;
    var max_cop: f64 = 0;
    var max_drift: f64 = 0;
    var max_rot: f64 = 0;
    var ref: ?Sample = null;
    for (samples) |s| {
        if (!inWindow(s, c.window_start_s, c.duration_s)) continue;
        const r = ref orelse blk: {
            ref = s;
            break :blk s;
        };
        sum += s.normal_force_sum_n;
        n += 1;
        max_tan = @max(max_tan, m3.length(s.tangential_force_sum_n));
        max_cop = @max(max_cop, if (s.center_of_pressure_m) |cop| m3.horizontalLength(m3.sub(cop, s.position_m)) else std.math.inf(f64));
        max_drift = @max(max_drift, m3.horizontalLength(m3.sub(s.position_m, r.position_m)));
        max_rot = @max(max_rot, s.orientation.relativeTo(r.orientation).angle());
    }
    const mean = if (n > 0) sum / n else std.math.nan(f64);
    e.add(.{ .name = "normal_force_rel_error", .value = @abs(mean - w) / w, .limit = c.normal_force_rel_tol });
    e.add(.{ .name = "tangential_force_rel_weight", .value = max_tan / w, .limit = c.tangential_force_max_rel_weight });
    e.add(.{ .name = "center_of_pressure_offset_m", .value = max_cop, .limit = c.center_of_pressure_abs_tol_m });
    e.add(.{ .name = "drift_translation_m", .value = max_drift, .limit = c.drift_translation_abs_tol_m });
    e.add(.{ .name = "drift_rotation_rad", .value = max_rot, .limit = c.drift_rotation_abs_tol_rad });
    e.add(.{ .name = "max_penetration_m", .value = maxPenetration(samples), .limit = c.max_penetration_m });
    return e;
}

/// Free fall from rest: every sample with 0 < t ≤ duration. Each metric is the
/// largest ratio error/allowance (pass when ≤ 1), since the allowance grows
/// with t. Position allowance: factor·g·Δt·t; velocity: rel·g·t + floor.
pub fn freeFall(c: criteria.FreeFallCase, g: f64, dt_s: f64, z0_m: f64, samples: []const Sample) Evaluation {
    var e: Evaluation = .{};
    var worst_v: f64 = 0;
    var worst_z: f64 = 0;
    var any_contact: f64 = 0;
    for (samples) |s| {
        if (!(s.t_s > 0 and s.t_s <= c.duration_s)) continue;
        const v_ref = -analytic.freeFallSpeed(g, s.t_s);
        const z_ref = z0_m - analytic.freeFallDistance(g, s.t_s);
        worst_v = @max(worst_v, @abs(s.velocity_m_s[2] - v_ref) / (c.velocity_rel_tol * g * s.t_s + c.velocity_abs_floor_m_s));
        worst_z = @max(worst_z, @abs(s.position_m[2] - z_ref) / (c.position_tol_factor * g * dt_s * s.t_s));
        if (s.normal_force_sum_n != 0) any_contact = 1;
    }
    e.add(.{ .name = "velocity_error_over_allowance", .value = worst_v, .limit = 1 });
    e.add(.{ .name = "position_error_over_allowance", .value = worst_z, .limit = 1 });
    e.add(.{ .name = "contact_during_fall", .value = any_contact, .limit = 0 });
    return e;
}

/// Friction threshold, below: push 0.9·μs·m·g at the centre of mass.
pub fn frictionBelow(c: criteria.FrictionThresholdCase, push_n: f64, samples: []const Sample) Evaluation {
    var e: Evaluation = .{};
    const x0 = samples[0].position_m;
    var max_disp: f64 = 0;
    var sum: f64 = 0;
    var n: f64 = 0;
    for (samples) |s| {
        if (s.t_s > c.duration_s) break;
        max_disp = @max(max_disp, m3.horizontalLength(m3.sub(s.position_m, x0)));
        if (inWindow(s, c.below_balance_window_start_s, c.duration_s)) {
            sum += m3.horizontalLength(s.tangential_force_sum_n);
            n += 1;
        }
    }
    const mean = if (n > 0) sum / n else std.math.nan(f64);
    e.add(.{ .name = "max_displacement_m", .value = max_disp, .limit = c.below_max_displacement_m });
    e.add(.{ .name = "friction_balance_rel_error", .value = @abs(mean - push_n) / push_n, .limit = c.below_balance_rel_tol });
    e.add(.{ .name = "max_penetration_m", .value = maxPenetration(samples), .limit = c.max_penetration_m });
    return e;
}

/// Friction threshold, above: mean acceleration along the push direction
/// between the samples nearest the window ends, against (F − μk·m·g)/m.
pub fn frictionAbove(c: criteria.FrictionThresholdCase, expected_accel_m_s2: f64, samples: []const Sample) Evaluation {
    var e: Evaluation = .{};
    const a = nearest(samples, c.above_accel_window_start_s);
    const b = nearest(samples, c.above_accel_window_end_s);
    const d = c.direction_world;
    const accel = (m3.dot(b.velocity_m_s, d) - m3.dot(a.velocity_m_s, d)) / (b.t_s - a.t_s);
    e.add(.{ .name = "acceleration_rel_error", .value = @abs(accel - expected_accel_m_s2) / expected_accel_m_s2, .limit = c.above_accel_rel_tol });
    e.add(.{ .name = "max_penetration_m", .value = maxPenetration(samples), .limit = c.max_penetration_m });
    return e;
}

fn nearest(samples: []const Sample, t: f64) Sample {
    var best = samples[0];
    for (samples) |s| if (@abs(s.t_s - t) < @abs(best.t_s - t)) {
        best = s;
    };
    return best;
}

/// Sliding to a stop (protocol revision 2): the stop is the first sample
/// whose bottom-face-centre horizontal speed (the sliding contact patch,
/// v + ω × r with r from the centre of mass to the bottom-face centre) is ≤
/// the threshold. Distance is horizontal CoM displacement from t = 0 to the
/// stop. Drift is the largest horizontal CoM displacement after the stop.
///
/// The revision-1 definition (CoM speed) is still reported as an
/// informational metric. It also captures post-stop rocking on the compliant
/// contact (v_com = ω·h), which is contact relaxation, not sliding.
pub fn slideToStop(c: criteria.SlideToStopCase, f: criteria.Fixture, g: f64, mu_k: f64, dt_s: f64, samples: []const Sample) Evaluation {
    var e: Evaluation = .{};
    const t_ref = analytic.stopTime(g, mu_k, c.initial_speed_m_s);
    const d_ref = analytic.stopDistance(g, mu_k, c.initial_speed_m_s);
    const x0 = samples[0].position_m;
    const bottom: m3.Vec3 = .{ 0, 0, -f.size_m[2] / 2.0 };
    var stop: ?Sample = null;
    var com_stop: ?Sample = null;
    var drift: f64 = 0;
    for (samples[1..]) |s| {
        if (com_stop == null and m3.horizontalLength(s.velocity_m_s) <= c.stop_speed_threshold_m_s) com_stop = s;
        if (stop) |st| {
            drift = @max(drift, m3.horizontalLength(m3.sub(s.position_m, st.position_m)));
        } else {
            const r = s.orientation.rotate(bottom);
            const v_patch = m3.add(s.velocity_m_s, m3.cross(s.angular_velocity_rad_s, r));
            if (m3.horizontalLength(v_patch) <= c.stop_speed_threshold_m_s) stop = s;
        }
    }
    if (stop) |st| {
        const d = m3.horizontalLength(m3.sub(st.position_m, x0));
        e.add(.{ .name = "stop_time_error_s", .value = @abs(st.t_s - t_ref), .limit = c.stop_time_tol_steps * dt_s });
        e.add(.{ .name = "stop_distance_error_m", .value = @abs(d - d_ref), .limit = c.stop_distance_rel_tol * d_ref + c.stop_distance_tol_steps * c.initial_speed_m_s * dt_s });
        e.add(.{ .name = "post_stop_drift_m", .value = drift, .limit = c.post_stop_drift_abs_tol_m });
    } else {
        e.add(.{ .name = "stopped", .value = 0, .limit = 1, .at_least = true });
    }
    e.add(.{
        .name = "rev1_com_speed_stop_time_error_s",
        .value = if (com_stop) |cs| @abs(cs.t_s - t_ref) else std.math.inf(f64),
        .limit = c.stop_time_tol_steps * dt_s,
        .informational = true,
    });
    return e;
}

/// Pivot reference point: midpoint of the bottom edge on the +x side, in the
/// body frame (the edge about which a +x push tips the fixture).
pub fn pivotBody(f: criteria.Fixture) m3.Vec3 {
    return .{ f.size_m[0] / 2.0, 0, -f.size_m[2] / 2.0 };
}

pub fn tippingBelow(c: criteria.TippingCase, samples: []const Sample) Evaluation {
    var e: Evaluation = .{};
    var max_tilt: f64 = 0;
    for (samples) |s| max_tilt = @max(max_tilt, m3.tilt(s.orientation));
    e.add(.{ .name = "max_tilt_rad", .value = max_tilt, .limit = c.below_max_tilt_rad });
    return e;
}

/// Above threshold: the fixture must reach the minimum tilt by the end of the
/// run, and the pivot point must not slip horizontally while tilt is below
/// `no_slip_until_tilt_rad`.
pub fn tippingAbove(c: criteria.TippingCase, f: criteria.Fixture, samples: []const Sample) Evaluation {
    var e: Evaluation = .{};
    const pivot = pivotBody(f);
    const p0 = m3.add(samples[0].position_m, samples[0].orientation.rotate(pivot));
    var max_tilt: f64 = 0;
    var slip: f64 = 0;
    for (samples) |s| {
        const tl = m3.tilt(s.orientation);
        max_tilt = @max(max_tilt, tl);
        if (tl < c.no_slip_until_tilt_rad) {
            const p = m3.add(s.position_m, s.orientation.rotate(pivot));
            slip = @max(slip, m3.horizontalLength(m3.sub(p, p0)));
        }
    }
    e.add(.{ .name = "max_tilt_rad", .value = max_tilt, .limit = c.above_min_tilt_rad, .at_least = true });
    e.add(.{ .name = "pivot_slip_m", .value = slip, .limit = c.pivot_slip_abs_tol_m });
    return e;
}

/// Combines per-combination outcomes under the Q48 rule.
pub const CaseOutcome = enum { pass, fail, uncertain };
pub fn combine(passes: []const bool) CaseOutcome {
    if (passes.len == 0) return .fail; // nothing evaluated: fail closed
    var any_pass = false;
    var any_fail = false;
    for (passes) |p| {
        if (p) any_pass = true else any_fail = true;
    }
    if (any_pass and !any_fail) return .pass;
    if (any_fail and !any_pass) return .fail;
    return .uncertain;
}

// --- Tests on synthetic data (no solver). ---

const testing = std.testing;

fn restingSample(t: f64, w: f64) Sample {
    return .{
        .t_s = t,
        .position_m = .{ 0, 0, 0.01 },
        .orientation = .identity,
        .velocity_m_s = m3.zero,
        .normal_force_sum_n = w,
        .tangential_force_sum_n = m3.zero,
        .center_of_pressure_m = .{ 0, 0, 0 },
        .max_penetration_m = 1e-6,
    };
}

const flat: criteria.Fixture = .{ .id = "f", .shape = .cuboid, .mass_distribution = .uniform, .size_m = .{ 0.04, 0.04, 0.02 }, .mass_kg = 0.04 };

test "rest: exact equilibrium passes; a 1% weight error fails" {
    const c: criteria.RestCase = .{ .id = "r", .fixture = "f", .duration_s = 2, .window_start_s = 1, .normal_force_rel_tol = 1e-3, .tangential_force_max_rel_weight = 1e-6, .center_of_pressure_abs_tol_m = 1e-4, .drift_translation_abs_tol_m = 1e-6, .drift_rotation_abs_tol_rad = 1e-6, .max_penetration_m = 1e-4 };
    const w = 0.04 * 9.80665;
    var good: [5]Sample = undefined;
    for (&good, 0..) |*s, i| s.* = restingSample(@as(f64, @floatFromInt(i)) * 0.5, w);
    var ev = rest(c, flat, 9.80665, &good);
    try testing.expect(ev.passed());
    for (&good) |*s| s.normal_force_sum_n = w * 1.01;
    ev = rest(c, flat, 9.80665, &good);
    try testing.expect(!ev.passed());
}

test "free fall: exact semi-implicit Euler trajectory passes" {
    const c: criteria.FreeFallCase = .{ .id = "ff", .fixture = "f", .initial_clearance_m = 0.1, .duration_s = 0.1, .velocity_rel_tol = 1e-9, .velocity_abs_floor_m_s = 1e-12, .position_tol_factor = 1 };
    const g = 9.80665;
    const dt = 0.001;
    var samples: [101]Sample = undefined;
    var v: f64 = 0;
    var z: f64 = 0.11;
    for (&samples, 0..) |*s, i| {
        if (i > 0) {
            v -= g * dt;
            z += v * dt;
        }
        s.* = restingSample(@as(f64, @floatFromInt(i)) * dt, 0);
        s.velocity_m_s = .{ 0, 0, v };
        s.position_m = .{ 0, 0, z };
    }
    const ev = freeFall(c, g, dt, 0.11, &samples);
    try testing.expect(ev.passed());
}

test "combine follows the Q48 outcome rule" {
    try testing.expectEqual(CaseOutcome.pass, combine(&.{ true, true }));
    try testing.expectEqual(CaseOutcome.fail, combine(&.{ false, false }));
    try testing.expectEqual(CaseOutcome.uncertain, combine(&.{ true, false }));
    try testing.expectEqual(CaseOutcome.fail, combine(&.{}));
}

test "a non-finite metric never passes" {
    const m: Metric = .{ .name = "x", .value = std.math.nan(f64), .limit = 1 };
    try testing.expect(!m.passed());
}
