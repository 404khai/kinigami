//! Evaluation protocol for the compliant-link qualification criteria v1
//! (Q52, PHY-012, PHY-013). Committed before any link solver code, together
//! with docs/validation/compliant-link-v1-protocol.md.
//!
//! The evaluator sees only `Sample`s recorded after each physics step. Every
//! metric is a pure function of the samples, the criteria, and closed-form
//! references. Precise definitions (the protocol document is the prose form
//! of this file):
//!
//! - Sample n is the state after step n at t_n = n·Δt, computed from exact
//!   tick counts. Sample 0 is the initial state: its link forces and moments
//!   are zero because no step has produced them, and its extension and
//!   rotation are the initial geometry.
//! - A window [a, b] includes every sample with a ≤ t ≤ b.
//! - Link quantities are the solver's own report (PHY-005), resolved in
//!   anchor A's frame: forces and moments are those acting on body B, with
//!   components ordered [link axis, shear 1, shear 2] and
//!   [torsion, bend 1, bend 2]. Tension is −force[0]. Extension and rotation
//!   vector are measured from the rest geometry after the step.
//! - Static metrics use the window mean of each component; magnitudes of the
//!   two perpendicular components are taken after averaging.
//! - Dynamic metrics use the whole run.

const std = @import("std");
const m3 = @import("math3.zig");
const lc = @import("link_criteria.zig");
const fixture_eval = @import("fixture_eval.zig");

pub const Metric = fixture_eval.Metric;
pub const CaseOutcome = fixture_eval.CaseOutcome;

/// Protocol revision implemented here (see the revision log in the protocol
/// document).
pub const protocol_revision: u32 = 2;

pub const max_metrics = 12;

pub const Sample = struct {
    t_s: f64,
    /// Force on body B at anchor B, anchor-A-frame components [axial, shear 1, shear 2], N.
    force_b_n: m3.Vec3 = m3.zero,
    /// Moment on body B from the link, components [torsion, bend 1, bend 2], N·m.
    moment_b_nm: m3.Vec3 = m3.zero,
    /// Anchor B relative to anchor A minus the rest offset, components [axial, shear 1, shear 2], m.
    extension_m: m3.Vec3 = m3.zero,
    /// Relative rotation vector of B from rest, components [twist, bend 1, bend 2], rad.
    rotation_rad: m3.Vec3 = m3.zero,
    /// Total linear momentum Σ m·v of the dynamic bodies, kg·m/s.
    momentum_kg_m_s: m3.Vec3 = m3.zero,
    /// Sum of contact normal forces on body B (solver output), N.
    contact_normal_sum_n: f64 = 0,
};

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

    /// Nothing evaluated, or any non-informational metric failing, is a failure.
    pub fn passed(self: *const Evaluation) bool {
        if (self.len == 0) return false;
        for (self.slice()) |m| if (!m.passed()) return false;
        return true;
    }
};

pub const Window = struct { start_s: f64, end_s: f64 };

// --- Resolution rule (Q43, Q52 §4, PHY-018) ---

/// Floating-point representation slack for the ω·Δt comparison. The grid is
/// designed so soft-axial at 2 ms sits exactly on the limit; the comparison
/// must not depend on the last bit of √ and the tick-to-seconds conversion.
pub const resolution_slack_rel: f64 = 1e-12;

pub fn resolved(omega_rad_s: f64, dt_s: f64, max_omega_dt: f64) bool {
    return omega_rad_s * dt_s <= max_omega_dt * (1.0 + resolution_slack_rel);
}

// --- Closed-form references (reference_conventions in the criteria) ---

pub fn reducedMass(m_a: f64, m_b: f64) f64 {
    return m_a * m_b / (m_a + m_b);
}

/// Moment of inertia of a uniform cube about any axis through its centre.
pub fn cubeInertia(mass_kg: f64, edge_m: f64) f64 {
    return mass_kg * edge_m * edge_m / 6.0;
}

pub fn reducedInertia(i_a: f64, i_b: f64) f64 {
    return i_a * i_b / (i_a + i_b);
}

/// c = 2·ζ·√(k·m) (or inertia).
pub fn dampingCoefficient(zeta: f64, k: f64, mass_or_inertia: f64) f64 {
    return 2.0 * zeta * @sqrt(k * mass_or_inertia);
}

pub fn omega(k: f64, mass_or_inertia: f64) f64 {
    return @sqrt(k / mass_or_inertia);
}

// --- Helpers ---

fn inWindow(s: Sample, w: Window) bool {
    return s.t_s >= w.start_s and s.t_s <= w.end_s;
}

const WindowMean = struct {
    force: m3.Vec3,
    moment: m3.Vec3,
    extension: m3.Vec3,
    rotation: m3.Vec3,
    normal_sum: f64,
    n: usize,
};

fn windowMean(samples: []const Sample, w: Window) WindowMean {
    var out: WindowMean = .{ .force = m3.zero, .moment = m3.zero, .extension = m3.zero, .rotation = m3.zero, .normal_sum = 0, .n = 0 };
    for (samples) |s| {
        if (!inWindow(s, w)) continue;
        out.force = m3.add(out.force, s.force_b_n);
        out.moment = m3.add(out.moment, s.moment_b_nm);
        out.extension = m3.add(out.extension, s.extension_m);
        out.rotation = m3.add(out.rotation, s.rotation_rad);
        out.normal_sum += s.contact_normal_sum_n;
        out.n += 1;
    }
    if (out.n == 0) {
        const nan = std.math.nan(f64);
        return .{ .force = .{ nan, nan, nan }, .moment = .{ nan, nan, nan }, .extension = .{ nan, nan, nan }, .rotation = .{ nan, nan, nan }, .normal_sum = nan, .n = 0 };
    }
    const k = 1.0 / @as(f64, @floatFromInt(out.n));
    out.force = m3.scale(out.force, k);
    out.moment = m3.scale(out.moment, k);
    out.extension = m3.scale(out.extension, k);
    out.rotation = m3.scale(out.rotation, k);
    out.normal_sum *= k;
    return out;
}

fn perp(v: m3.Vec3) f64 {
    return @sqrt(v[1] * v[1] + v[2] * v[2]);
}

fn relErr(value: f64, reference: f64) f64 {
    return @abs(value - reference) / @abs(reference);
}

/// Largest peak-to-peak spread of the window tension, over m·g: how settled
/// the window is. Informational only.
fn tensionSpread(samples: []const Sample, w: Window, weight_n: f64) f64 {
    var lo = std.math.inf(f64);
    var hi = -std.math.inf(f64);
    for (samples) |s| {
        if (!inWindow(s, w)) continue;
        lo = @min(lo, -s.force_b_n[0]);
        hi = @max(hi, -s.force_b_n[0]);
    }
    return (hi - lo) / weight_n;
}

// --- Static checks (every combination) ---

pub const StaticSetup = struct {
    mass_kg: f64,
    g_m_s2: f64,
    k_axial_n_m: f64,
    k_shear_n_m: f64,
    k_torsion_nm_rad: f64,
    k_bend_nm_rad: f64,
    /// Anchor-to-centre-of-mass lever arm: half the cube edge.
    half_size_m: f64,
    window: Window,
};

/// L1: tension vs m·g, elongation vs m·g/k_axial.
pub fn axialStatics(c: lc.AxialStatics, s: StaticSetup, samples: []const Sample) Evaluation {
    var e: Evaluation = .{};
    const w = s.mass_kg * s.g_m_s2;
    const mean = windowMean(samples, s.window);
    e.add(.{ .name = "tension_rel_error", .value = relErr(-mean.force[0], w), .limit = c.force_rel_tol });
    e.add(.{ .name = "elongation_rel_error", .value = relErr(mean.extension[0], w / s.k_axial_n_m), .limit = c.elongation_rel_tol });
    e.add(.{ .name = "tension_window_spread_over_weight", .value = tensionSpread(samples, s.window, w), .limit = c.force_rel_tol, .informational = true });
    return e;
}

/// Exact static bending angle of the L2 setup (Q53): the root φ ∈ [0, π/2]
/// of k_bend·φ = h·(F·cos φ − T·sin φ), by 200 bisection halvings. The left
/// side increases and the right side decreases on the interval, so the root
/// is unique. T is the closed-form tension m·g.
pub fn bendingAngleWithTensionLever(k_bend: f64, half_size_m: f64, load_n: f64, tension_n: f64) f64 {
    var lo: f64 = 0;
    var hi: f64 = std.math.pi / 2.0;
    for (0..200) |_| {
        const mid = 0.5 * (lo + hi);
        if (k_bend * mid - half_size_m * (load_n * @cos(mid) - tension_n * @sin(mid)) > 0) hi = mid else lo = mid;
    }
    return 0.5 * (lo + hi);
}

/// L2: with a horizontal load F at B's centre of mass. Gated references:
/// shear force F, shear displacement F/k_shear, and the bending moment and
/// angle selected by `moment_reference`:
/// - `load_times_half_size` (v1, Q52): M = F·h, φ = M/k_bend;
/// - `torque_balance_with_tension_lever` (v2, Q53): φ from
///   `bendingAngleWithTensionLever`, M = k_bend·φ.
///
/// Informational (never gates): the moment's deviation from F·h, so the
/// size of the lever effect stays visible, and the bending angle against
/// the solver's own measured moment / k_bend (report self-consistency).
pub fn shearBendingStatics(c: lc.ShearBendingStatics, s: StaticSetup, samples: []const Sample) Evaluation {
    var e: Evaluation = .{};
    const f = c.load_over_weight * s.mass_kg * s.g_m_s2;
    const mean = windowMean(samples, s.window);
    const shear = perp(mean.force);
    const moment = perp(mean.moment);
    const disp = perp(mean.extension);
    const angle = perp(mean.rotation);
    const m_simple = f * s.half_size_m;
    const angle_ref = switch (c.moment_reference) {
        .load_times_half_size => m_simple / s.k_bend_nm_rad,
        .torque_balance_with_tension_lever => bendingAngleWithTensionLever(s.k_bend_nm_rad, s.half_size_m, f, s.mass_kg * s.g_m_s2),
    };
    const m_ref = s.k_bend_nm_rad * angle_ref;
    e.add(.{ .name = "shear_force_rel_error", .value = relErr(shear, f), .limit = c.force_rel_tol });
    e.add(.{ .name = "bending_moment_rel_error", .value = relErr(moment, m_ref), .limit = c.moment_rel_tol });
    e.add(.{ .name = "shear_displacement_rel_error", .value = relErr(disp, f / s.k_shear_n_m), .limit = c.displacement_rel_tol });
    e.add(.{ .name = "bending_angle_rel_error", .value = relErr(angle, angle_ref), .limit = c.angle_rel_tol });
    e.add(.{ .name = "info_moment_rel_deviation_from_load_times_half_size", .value = relErr(moment, m_simple), .limit = c.moment_rel_tol, .informational = true });
    e.add(.{ .name = "info_angle_rel_error_vs_measured_moment", .value = relErr(angle, moment / s.k_bend_nm_rad), .limit = c.angle_rel_tol, .informational = true });
    return e;
}

/// L3: link torque vs the applied torque, twist vs τ/k_torsion. Signed: the
/// link resists a torque applied along +axis, so its moment on B is negative
/// and the twist positive.
pub fn torsionStatics(c: lc.TorsionStatics, s: StaticSetup, samples: []const Sample) Evaluation {
    var e: Evaluation = .{};
    const tau = c.torque_about_link_axis_nm;
    const mean = windowMean(samples, s.window);
    e.add(.{ .name = "torque_rel_error", .value = relErr(-mean.moment[0], tau), .limit = c.torque_rel_tol });
    e.add(.{ .name = "twist_rel_error", .value = relErr(mean.rotation[0], tau / s.k_torsion_nm_rad), .limit = c.twist_rel_tol });
    return e;
}

// --- Dynamic measurements ---

pub const Channel = enum {
    axial_extension,
    twist,

    fn value(self: Channel, s: Sample) f64 {
        return switch (self) {
            .axial_extension => s.extension_m[0],
            .twist => s.rotation_rad[0],
        };
    }
};

/// Mean full period from linearly interpolated zero crossings.
///
/// A crossing lies between consecutive samples n and n+1 when
/// (x_n > 0) != (x_{n+1} > 0) (a value of exactly 0 counts as not positive);
/// its time is t_n + Δt·x_n/(x_n − x_{n+1}). With crossing times t_1..t_m, the
/// full periods are t_{i+2} − t_i for i = 1..m−2 and the measure is their
/// mean. Needs m ≥ 3, otherwise null (fail closed).
pub fn meanPeriod(samples: []const Sample, ch: Channel) ?f64 {
    var count: usize = 0;
    var first: [2]f64 = undefined;
    var last: [2]f64 = undefined;
    for (samples[0 .. samples.len - 1], samples[1..]) |a, b| {
        const xa = ch.value(a);
        const xb = ch.value(b);
        if ((xa > 0) == (xb > 0)) continue;
        const t = a.t_s + (b.t_s - a.t_s) * (xa / (xa - xb));
        if (count < 2) first[count] = t;
        last = if (count == 0) .{ t, t } else .{ last[1], t };
        count += 1;
    }
    if (count < 3) return null;
    // Σ_{i=1}^{m−2}(t_{i+2} − t_i) = t_m + t_{m−1} − t_1 − t_2
    return (last[1] + last[0] - first[0] - first[1]) / @as(f64, @floatFromInt(count - 2));
}

pub const DampingMeasure = struct {
    /// ln(first/last)/(2π n); positive for decaying amplitude.
    zeta: f64,
    peaks: usize,
};

/// Damping ratio from the first and last positive peaks.
///
/// A peak is an interior sample n (1 ≤ n ≤ N−1) with x_n > 0, x_n > x_{n−1}
/// and x_n ≥ x_{n+1}. Its value is refined by the three-point parabola
/// through samples n−1, n, n+1. Sample 0 is never a peak, so the initial
/// release does not bias the first peak. With p peaks, n = p − 1 full
/// periods separate the first and the last. Needs p ≥ 2, otherwise null.
pub fn dampingFromPeaks(samples: []const Sample, ch: Channel) ?DampingMeasure {
    var count: usize = 0;
    var first: f64 = 0;
    var last: f64 = 0;
    var i: usize = 1;
    while (i + 1 < samples.len) : (i += 1) {
        const a = ch.value(samples[i - 1]);
        const b = ch.value(samples[i]);
        const c = ch.value(samples[i + 1]);
        if (!(b > 0 and b > a and b >= c)) continue;
        const denom = a - 2.0 * b + c;
        const peak = if (denom == 0) b else b - 0.25 * (a - c) * (0.5 * (a - c) / denom);
        if (count == 0) first = peak;
        last = peak;
        count += 1;
    }
    if (count < 2 or !(last > 0)) return null;
    const n: f64 = @floatFromInt(count - 1);
    return .{ .zeta = @log(first / last) / (2.0 * std.math.pi * n), .peaks = count };
}

// --- Dynamic checks (resolved combinations only) ---

/// L4/L5: mean period vs 2π/ω.
pub fn periodCheck(name: []const u8, tol_rel: f64, omega_ref_rad_s: f64, ch: Channel, samples: []const Sample) Evaluation {
    var e: Evaluation = .{};
    const t_ref = 2.0 * std.math.pi / omega_ref_rad_s;
    const t_meas = meanPeriod(samples, ch);
    e.add(.{ .name = name, .value = if (t_meas) |t| relErr(t, t_ref) else std.math.inf(f64), .limit = tol_rel });
    return e;
}

/// L6: measured ζ vs the declared ζ.
pub fn physicalDamping(c: lc.PhysicalDamping, samples: []const Sample) Evaluation {
    var e: Evaluation = .{};
    const z = dampingFromPeaks(samples, .axial_extension);
    e.add(.{ .name = "zeta_rel_error", .value = if (z) |d| relErr(d.zeta, c.damping_ratio) else std.math.inf(f64), .limit = c.zeta_rel_tol });
    return e;
}

/// L7: with c = 0 any measured decay is the integrator's. Gated on |ζ_num|
/// so numerical energy injection cannot pass as low dissipation. The signed
/// value is also reported (informational).
pub fn numericalDissipation(c: lc.NumericalDissipation, samples: []const Sample) Evaluation {
    var e: Evaluation = .{};
    const z = dampingFromPeaks(samples, .axial_extension);
    e.add(.{ .name = "abs_zeta_num", .value = if (z) |d| @abs(d.zeta) else std.math.inf(f64), .limit = c.zeta_num_max });
    e.add(.{ .name = "info_zeta_num_signed", .value = if (z) |d| d.zeta else std.math.nan(f64), .limit = c.zeta_num_max, .informational = true });
    return e;
}

// --- Momentum and consistency ---

/// L8: |p(t) − (p₀ + M·g⃗·t)| / (rel·M·g·t + floor), worst over t > 0 (≤ 1 passes).
pub fn momentum(c: lc.Momentum, total_mass_kg: f64, gravity_m_s2: m3.Vec3, samples: []const Sample) Evaluation {
    var e: Evaluation = .{};
    const p0 = samples[0].momentum_kg_m_s;
    const g_mag = m3.length(gravity_m_s2);
    var worst: f64 = 0;
    for (samples[1..]) |s| {
        const expected = m3.add(p0, m3.scale(gravity_m_s2, total_mass_kg * s.t_s));
        const err = m3.length(m3.sub(s.momentum_kg_m_s, expected));
        worst = @max(worst, err / (c.rel_tol_of_m_g_t * total_mass_kg * g_mag * s.t_s + c.abs_floor_kg_m_s));
    }
    e.add(.{ .name = "momentum_error_over_allowance", .value = worst, .limit = 1 });
    return e;
}

/// L9: window-mean (Σ contact normal + link tension) vs m·g, and both
/// positive throughout the window.
pub fn contactLinkConsistency(c: lc.ConsistencyCase, mass_kg: f64, g_m_s2: f64, samples: []const Sample) Evaluation {
    var e: Evaluation = .{};
    const w: Window = .{ .start_s = c.window_start_s, .end_s = c.duration_s };
    const weight = mass_kg * g_m_s2;
    const mean = windowMean(samples, w);
    e.add(.{ .name = "load_sum_rel_error", .value = relErr(mean.normal_sum - mean.force[0], weight), .limit = c.sum_rel_tol });
    var min_normal = std.math.inf(f64);
    var min_tension = std.math.inf(f64);
    for (samples) |s| {
        if (!inWindow(s, w)) continue;
        min_normal = @min(min_normal, s.contact_normal_sum_n);
        min_tension = @min(min_tension, -s.force_b_n[0]);
    }
    e.add(.{ .name = "contact_normal_not_positive", .value = if (min_normal > 0) 0 else 1, .limit = 0 });
    e.add(.{ .name = "link_tension_not_positive", .value = if (min_tension > 0) 0 else 1, .limit = 0 });
    return e;
}

// --- Outcome aggregation (Q48, Q52 §6) ---

pub const Status = enum { pass, fail, outside_envelope };

/// A case passes only if every evaluated combination passes, fails if all
/// evaluated combinations fail, and is otherwise uncertain. Combinations
/// outside the envelope are not counted. Nothing evaluated is a failure
/// (fail closed).
pub fn combine(statuses: []const Status) CaseOutcome {
    var any_pass = false;
    var any_fail = false;
    for (statuses) |s| switch (s) {
        .pass => any_pass = true,
        .fail => any_fail = true,
        .outside_envelope => {},
    };
    if (any_pass and !any_fail) return .pass;
    if (any_fail and !any_pass) return .fail;
    if (any_pass and any_fail) return .uncertain;
    return .fail;
}

// --- Tests on synthetic data (no solver) ---

const testing = std.testing;

/// Samples of x(t) = A·e^{−ζωt}·cos(ω_d t) on the extension channel.
fn oscillator(comptime n: usize, buf: *[n]Sample, dt: f64, omega_rad_s: f64, zeta: f64, amplitude: f64) []const Sample {
    const wd = omega_rad_s * @sqrt(1.0 - zeta * zeta);
    for (buf, 0..) |*s, i| {
        const t = @as(f64, @floatFromInt(i)) * dt;
        s.* = .{ .t_s = t, .extension_m = .{ amplitude * @exp(-zeta * omega_rad_s * t) * @cos(wd * t), 0, 0 } };
    }
    return buf;
}

test "mean period recovers an undamped period from interpolated zero crossings" {
    var buf: [1001]Sample = undefined;
    const s = oscillator(1001, &buf, 0.001, 100.0, 0, 5e-4);
    const t = meanPeriod(s, .axial_extension).?;
    try testing.expectApproxEqRel(2.0 * std.math.pi / 100.0, t, 1e-5);
}

test "mean period fails closed with fewer than three crossings" {
    var buf: [101]Sample = undefined;
    const s = oscillator(101, &buf, 0.001, 10.0, 0, 1);
    try testing.expect(meanPeriod(s, .axial_extension) == null);
}

test "damping from peaks recovers a declared ratio and reads zero for an undamped signal" {
    var buf: [1001]Sample = undefined;
    const damped = oscillator(1001, &buf, 0.001, 100.0, 0.05, 5e-4);
    const d = dampingFromPeaks(damped, .axial_extension).?;
    // The registered measure is δ/2π, which reads 0.05006 for ζ = 0.05 (0.12 % high).
    try testing.expectApproxEqRel(@as(f64, 0.05), d.zeta, 5e-3);
    try testing.expect(d.peaks >= 10);
    const undamped = oscillator(1001, &buf, 0.001, 100.0, 0, 5e-4);
    try testing.expect(@abs(dampingFromPeaks(undamped, .axial_extension).?.zeta) < 1e-6);
    // Growth reads as a negative ζ and still fails an |ζ| gate.
    const grow = oscillator(1001, &buf, 0.001, 100.0, -0.02, 5e-4);
    try testing.expect(dampingFromPeaks(grow, .axial_extension).?.zeta < -0.015);
}

test "damping measurement needs two peaks" {
    var buf: [101]Sample = undefined;
    const s = oscillator(101, &buf, 0.001, 20.0, 0, 1);
    try testing.expect(dampingFromPeaks(s, .axial_extension) == null);
}

test "resolution rule: the soft-axial 2 ms combination sits exactly on the limit and is resolved" {
    try testing.expect(resolved(omega(100.0, 0.01), 0.002, 0.2));
    try testing.expect(!resolved(omega(1000.0, 0.01), 0.001, 0.2));
    try testing.expect(!resolved(omega(0.01, reducedInertia(cubeInertia(0.02, 0.02), cubeInertia(0.02, 0.02))), 0.002, 0.2));
}

test "reference conventions: reduced mass and inertia, damping coefficient" {
    try testing.expectEqual(@as(f64, 0.01), reducedMass(0.02, 0.02));
    try testing.expectApproxEqRel(@as(f64, 0.02 * 0.0004 / 6.0), cubeInertia(0.02, 0.02), 1e-15);
    try testing.expectApproxEqRel(@as(f64, 2.0 * 0.5 * @sqrt(100.0 * 0.02)), dampingCoefficient(0.5, 100.0, 0.02), 1e-15);
}

test "outcome aggregation: outside_envelope is not counted, and nothing evaluated fails closed" {
    try testing.expectEqual(CaseOutcome.pass, combine(&.{ .pass, .outside_envelope, .pass }));
    try testing.expectEqual(CaseOutcome.fail, combine(&.{ .fail, .outside_envelope }));
    try testing.expectEqual(CaseOutcome.uncertain, combine(&.{ .pass, .fail, .outside_envelope }));
    try testing.expectEqual(CaseOutcome.fail, combine(&.{ .outside_envelope, .outside_envelope }));
    try testing.expectEqual(CaseOutcome.fail, combine(&.{}));
}

const test_static: StaticSetup = .{
    .mass_kg = 0.02,
    .g_m_s2 = 9.80665,
    .k_axial_n_m = 1000,
    .k_shear_n_m = 1000,
    .k_torsion_nm_rad = 0.1,
    .k_bend_nm_rad = 0.1,
    .half_size_m = 0.01,
    .window = .{ .start_s = 1.5, .end_s = 2.0 },
};

test "axial statics: exact equilibrium passes; a 1% tension error fails" {
    const c: lc.AxialStatics = .{ .id = "L1", .force_rel_tol = 1e-3, .elongation_rel_tol = 1e-2 };
    const w = 0.02 * 9.80665;
    var samples: [5]Sample = undefined;
    for (&samples, 0..) |*s, i| s.* = .{ .t_s = 1.5 + 0.125 * @as(f64, @floatFromInt(i)), .force_b_n = .{ -w, 0, 0 }, .extension_m = .{ w / 1000.0, 0, 0 } };
    try testing.expect(axialStatics(c, test_static, &samples).passed());
    for (&samples) |*s| s.force_b_n[0] = -w * 1.01;
    try testing.expect(!axialStatics(c, test_static, &samples).passed());
}

test "statics with no sample in the window fail closed" {
    const c: lc.AxialStatics = .{ .id = "L1", .force_rel_tol = 1e-3, .elongation_rel_tol = 1e-2 };
    const samples = [_]Sample{.{ .t_s = 0.5 }};
    try testing.expect(!axialStatics(c, test_static, &samples).passed());
}

test "shear and bending statics: closed-form values pass; the informational lever metric does not gate" {
    const c: lc.ShearBendingStatics = .{ .id = "L2", .load_world_direction = .{ 1, 0, 0 }, .load_over_weight = 0.1, .application = .center_of_mass_b, .force_rel_tol = 1e-3, .moment_rel_tol = 1e-3, .displacement_rel_tol = 2e-2, .angle_rel_tol = 2e-2 };
    const f = 0.1 * 0.02 * 9.80665;
    const m = f * 0.01;
    const w = 0.02 * 9.80665;
    var s: [2]Sample = undefined;
    s[0] = .{ .t_s = 1.5, .force_b_n = .{ -w, -f, 0 }, .moment_b_nm = .{ 0, m, 0 }, .extension_m = .{ w / 1000.0, f / 1000.0, 0 }, .rotation_rad = .{ 0, m / 0.1, 0 } };
    s[1] = s[0];
    s[1].t_s = 2.0;
    var ev = shearBendingStatics(c, test_static, &s);
    try testing.expect(ev.passed());
    // A moment 2.4 % off its reference fails the 1e-3 gate.
    s[0].moment_b_nm[1] = m * 1.024;
    s[1].moment_b_nm[1] = m * 1.024;
    ev = shearBendingStatics(c, test_static, &s);
    try testing.expect(!ev.passed());
}

test "the tension-lever bending angle solves the exact torque balance and reduces the moment" {
    const m = 0.02;
    const g = 9.80665;
    const f = 0.1 * m * g;
    // Independent values (hand-solved torque balance, Q53): deviation of M from F·h.
    const expected = [_]f64{ 0.164078787944781, 0.019237821095197, 0.001957509823605 };
    for ([_]f64{ 0.01, 0.1, 1.0 }, expected) |kb, dev| {
        const phi = bendingAngleWithTensionLever(kb, 0.01, f, m * g);
        try testing.expectApproxEqAbs(@as(f64, 0), kb * phi - 0.01 * (f * @cos(phi) - m * g * @sin(phi)), 1e-18);
        try testing.expectApproxEqAbs(dev, 1.0 - kb * phi / (f * 0.01), 1e-12);
    }
}

test "torsion statics are signed: a twist of the wrong sign fails" {
    const c: lc.TorsionStatics = .{ .id = "L3", .torque_about_link_axis_nm = 1e-4, .torque_rel_tol = 1e-3, .twist_rel_tol = 1e-2 };
    var s: [2]Sample = .{
        .{ .t_s = 1.5, .moment_b_nm = .{ -1e-4, 0, 0 }, .rotation_rad = .{ 1e-4 / 0.1, 0, 0 } },
        .{ .t_s = 2.0, .moment_b_nm = .{ -1e-4, 0, 0 }, .rotation_rad = .{ 1e-4 / 0.1, 0, 0 } },
    };
    try testing.expect(torsionStatics(c, test_static, &s).passed());
    s[0].rotation_rad[0] = -s[0].rotation_rad[0];
    s[1].rotation_rad[0] = -s[1].rotation_rad[0];
    try testing.expect(!torsionStatics(c, test_static, &s).passed());
}

test "momentum: gravity-only drift passes; a leaked impulse fails" {
    const c: lc.Momentum = .{ .id = "L8", .rel_tol_of_m_g_t = 1e-9, .abs_floor_kg_m_s = 1e-12 };
    const g: m3.Vec3 = .{ 0, 0, -9.80665 };
    var s: [101]Sample = undefined;
    for (&s, 0..) |*x, i| {
        const t = @as(f64, @floatFromInt(i)) * 0.01;
        x.* = .{ .t_s = t, .momentum_kg_m_s = m3.scale(g, 0.04 * t) };
    }
    try testing.expect(momentum(c, 0.04, g, &s).passed());
    s[50].momentum_kg_m_s[0] += 1e-6;
    try testing.expect(!momentum(c, 0.04, g, &s).passed());
}

test "contact-link consistency: shares summing to m·g pass; a negative share or a wrong sum fails" {
    const c: lc.ConsistencyCase = .{ .id = "L9", .setup = .body_b_resting_on_tabletop_vertical_link_to_static_body_a_above, .pretension_over_weight = 0.5, .damping_ratio_on_body_b = 1, .friction_pair = .{ .mu_static = 0.6, .mu_kinetic = 0.45 }, .duration_s = 2, .window_start_s = 1.5, .sum_rel_tol = 1e-3 };
    const w = 0.02 * 9.80665;
    var s: [2]Sample = .{
        .{ .t_s = 1.5, .force_b_n = .{ -0.6 * w, 0, 0 }, .contact_normal_sum_n = 0.4 * w },
        .{ .t_s = 2.0, .force_b_n = .{ -0.6 * w, 0, 0 }, .contact_normal_sum_n = 0.4 * w },
    };
    try testing.expect(contactLinkConsistency(c, 0.02, 9.80665, &s).passed());
    s[0].contact_normal_sum_n = 0.41 * w;
    s[1].contact_normal_sum_n = 0.41 * w;
    try testing.expect(!contactLinkConsistency(c, 0.02, 9.80665, &s).passed());
    // Sums to m·g but the table pulls (negative normal share).
    s[0] = .{ .t_s = 1.5, .force_b_n = .{ -1.1 * w, 0, 0 }, .contact_normal_sum_n = -0.1 * w };
    s[1] = s[0];
    s[1].t_s = 2.0;
    try testing.expect(!contactLinkConsistency(c, 0.02, 9.80665, &s).passed());
}

test "a non-finite measurement never passes" {
    const m: Metric = .{ .name = "x", .value = std.math.nan(f64), .limit = 1 };
    try testing.expect(!m.passed());
}
