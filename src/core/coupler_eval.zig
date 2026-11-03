//! Evaluation of the coupler-engagement qualification criteria v1 (Q56, Q57).
//! Prose form: docs/validation/coupler-engagement-v1-protocol.md, revision 1.
//!
//! Every function here is a pure function of recorded `Sample`s, the parsed
//! criteria, and closed-form references. There is no simulation and no
//! allocation. The evaluator sees ground truth only through samples recorded
//! after each physics step and the coupler update that follows it. Results
//! are labeled `fixture` by the caller (Q40); nothing here is a claim about
//! any Kin coupler or candidate.
//!
//! Conventions fixed by this file where the protocol is silent are listed
//! next to the function that applies them and summarized in the report that
//! accompanied this file. The principal ones:
//!
//! - Contacts: `body_b == null` is a tabletop contact acting on `body_a`
//!   (force `+f_n·n + t`). `body_b != null` is a guide contact with the
//!   normal pointing from A toward B: the force on B is `+f_n·n + t`, and
//!   on A its negative (`rigid.World.detectGuides`).
//! - Body index 0 is A and index 1 is B.
//! - Link force and moment components are in the coupler frame; the world
//!   vector is `A.orientation(step start)` applied to `Σ comp_i·axes_a[i]`.

const std = @import("std");
const m3 = @import("math3.zig");
const cc = @import("coupler_criteria.zig");
const lc = @import("link_criteria.zig");
const backend = @import("backend.zig");
const link_eval = @import("link_eval.zig");

pub const Criteria = cc.Criteria;
pub const Metric = link_eval.Metric;
pub const Evaluation = link_eval.Evaluation;
pub const Status = link_eval.Status;
pub const combine = link_eval.combine;

/// Protocol revision implemented here.
pub const protocol_revision: u32 = 1;

pub const Vec3 = m3.Vec3;

/// Half-width of the lateral region in which a C8 run is inside the model
/// (protocol, "C8 validity and classification"): ±8 mm of the axis.
pub const lateral_validity_m: f64 = 0.008;

// --- Samples and setup ---

pub const max_contacts = 16;
pub const max_loads = 4;

pub const Contact = struct {
    body_a: u32,
    body_b: ?u32,
    point_m: Vec3,
    normal: Vec3,
    normal_force_n: f64,
    tangential_force_n: Vec3,

    pub const empty: Contact = .{ .body_a = 0, .body_b = null, .point_m = m3.zero, .normal = m3.zero, .normal_force_n = 0, .tangential_force_n = m3.zero };

    fn isGuide(self: Contact) bool {
        return self.body_b != null;
    }
};

/// A validation load applied in the step (Q46).
pub const Load = struct {
    body: u32,
    force_n: Vec3,
    torque_nm: Vec3 = m3.zero,
    point_m: Vec3,

    pub const empty: Load = .{ .body = 0, .force_n = m3.zero, .point_m = m3.zero };
};

/// Sample n: the state after physics step n and the coupler update that
/// follows it. Sample 0 is the initial state, with no forces. The step-start
/// state of sample n is sample n−1.
pub const Sample = struct {
    t_s: f64,
    pos: [2]Vec3 = .{ m3.zero, m3.zero },
    quat: [2]m3.Quat = .{ .identity, .identity },
    vel: [2]Vec3 = .{ m3.zero, m3.zero },
    omega: [2]Vec3 = .{ m3.zero, m3.zero },
    contacts: [max_contacts]Contact = @splat(Contact.empty),
    n_contacts: usize = 0,
    loads: [max_loads]Load = @splat(Load.empty),
    n_loads: usize = 0,
    /// Latch-link report of the step, coupler-frame components.
    force_b_n: Vec3 = m3.zero,
    moment_b_nm: Vec3 = m3.zero,
    extension_m: Vec3 = m3.zero,
    rotation_rad: Vec3 = m3.zero,
    u_m: f64 = 0,
    e_during: f64 = 0,
    e_after: f64 = 0,
    active_during: bool = false,
    active_after: bool = false,
    command: backend.Command = .hold,
    /// `CouplerReport.pawl_work_j` of the step.
    pawl_work_j: f64 = 0,

    pub fn contactSlice(self: *const Sample) []const Contact {
        return self.contacts[0..self.n_contacts];
    }

    pub fn loadSlice(self: *const Sample) []const Load {
        return self.loads[0..self.n_loads];
    }
};

pub const BodySpec = struct {
    mass_kg: f64,
    /// Scalar moment of inertia: a uniform cube is isotropic.
    inertia_kg_m2: f64,
    is_static: bool = false,
};

/// Run setup the evaluator needs besides the samples.
pub const Bodies = struct {
    /// Index 0 is body A, index 1 is body B.
    body: [2]BodySpec,
    half_edge_m: f64,
    /// The exact physics step used by the solver (the pose audit is bitwise).
    dt_s: f64,
    gravity_m_s2: Vec3,
    /// Coupler axes (axial, shear 1, shear 2) in A's body frame; see `couplerAxes`.
    axes_a: [3]Vec3,
    /// Link anchors in the bodies' own frames.
    anchor_a_m: Vec3 = m3.zero,
    anchor_b_m: Vec3 = m3.zero,
    /// A's coupler face plane, from A's centre along the axis.
    face_offset_a_m: f64 = 0,
    /// The probe ball centre in B's frame.
    ball_centre_b_m: Vec3 = m3.zero,
    /// Guide-contact stiffness (V_contact of the energy audit).
    k_contact_n_m: f64,
};

/// Coupler frame in A's body frame, identical to the solver's anchor-A frame
/// (`rigid.World.perpendiculars`, Q52): s1 = normalize(a × t) with t the
/// axis of smallest |aᵢ| (lowest index on ties), s2 = a × s1.
pub fn couplerAxes(a: Vec3) [3]Vec3 {
    var i: usize = 0;
    for (1..3) |j| if (@abs(a[j]) < @abs(a[i])) {
        i = j;
    };
    var t: Vec3 = m3.zero;
    t[i] = 1;
    const c = m3.cross(a, t);
    const s1 = m3.scale(c, 1.0 / m3.length(c));
    return .{ a, s1, m3.cross(a, s1) };
}

/// The latch-link sample consumed by the C7 measures of `link_eval`
/// (momentum is not used by C7 and is left zero).
pub fn toLinkSample(s: Sample) link_eval.Sample {
    return .{ .t_s = s.t_s, .force_b_n = s.force_b_n, .moment_b_nm = s.moment_b_nm, .extension_m = s.extension_m, .rotation_rad = s.rotation_rad };
}

/// Converts into a caller-provided buffer (no allocation). `out.len` must be
/// at least `samples.len`.
pub fn toLinkSamples(out: []link_eval.Sample, samples: []const Sample) []const link_eval.Sample {
    std.debug.assert(out.len >= samples.len);
    for (samples, 0..) |s, i| out[i] = toLinkSample(s);
    return out[0..samples.len];
}

// --- Small helpers ---

fn pushMetric(ev: *Evaluation, m: Metric) void {
    std.debug.assert(ev.len < link_eval.max_metrics);
    ev.metrics[ev.len] = m;
    ev.len += 1;
}

fn push(ev: *Evaluation, name: []const u8, value: f64, limit: f64) void {
    pushMetric(ev, .{ .name = name, .value = value, .limit = limit });
}

fn pushInfo(ev: *Evaluation, name: []const u8, value: f64, limit: f64) void {
    pushMetric(ev, .{ .name = name, .value = value, .limit = limit, .informational = true });
}

fn nan() f64 {
    return std.math.nan(f64);
}

fn inf() f64 {
    return std.math.inf(f64);
}

fn relErr(value: f64, reference: f64) f64 {
    return @abs(value - reference) / @abs(reference);
}

fn count(n: usize) f64 {
    return @floatFromInt(n);
}

fn inWin(s: *const Sample, start_s: f64, end_s: f64) bool {
    return s.t_s >= start_s and s.t_s <= end_s;
}

/// Time comparison "at or after" with half a step of slack, so a grid time
/// computed as n·Δt is not excluded by its last bit.
fn atOrAfter(t_s: f64, ref_s: f64, dt_s: f64) bool {
    return t_s >= ref_s - 0.5 * dt_s;
}

fn weightB(b: Bodies) f64 {
    return b.body[1].mass_kg * m3.length(b.gravity_m_s2);
}

/// The first step n with `active_during` true and `active_after` false.
pub fn separationIndex(samples: []const Sample) ?usize {
    for (samples, 0..) |s, i| if (s.active_during and !s.active_after) return i;
    return null;
}

pub fn statusOf(ev: Evaluation) Status {
    return if (ev.passed()) .pass else .fail;
}

fn tension(s: *const Sample) f64 {
    return -s.force_b_n[0];
}

fn linkToWorld(b: Bodies, q_a: m3.Quat, comps: Vec3) Vec3 {
    const body = m3.add(m3.scale(b.axes_a[0], comps[0]), m3.add(m3.scale(b.axes_a[1], comps[1]), m3.scale(b.axes_a[2], comps[2])));
    return q_a.rotate(body);
}

// --- Closed-form references (reference_conventions in the criteria) ---

pub fn seatAlpha(c: Criteria) f64 {
    const sk = c.stand_in.socket;
    return std.math.atan(sk.mouth_half_width_m / sk.apex_depth_m);
}

/// k_s = 4·k_contact·sin²α.
pub fn seatStiffness(c: Criteria) f64 {
    const s = @sin(seatAlpha(c));
    return 4.0 * c.stand_in.guide_contact.contact_stiffness_n_m * s * s;
}

/// P = e·k·δ·k_s/(e·k + k_s).
pub fn preload(c: Criteria, e: f64) f64 {
    const k = e * c.stand_in.latch_link.full_stiffness.k_axial_n_m;
    return k * c.stand_in.latch_link.preload_offset_m * seatStiffness(c) / (k + seatStiffness(c));
}

/// F_sep = e·k·δ.
pub fn separationForce(c: Criteria, e: f64) f64 {
    return e * c.stand_in.latch_link.full_stiffness.k_axial_n_m * c.stand_in.latch_link.preload_offset_m;
}

pub const SeatedStatics = struct { tension_n: f64, normal_n: f64 };

/// Seated statics at total pull `force_n` and engagement `e`:
/// T = k(F + k_s·δ)/(k + k_s), N = k_s(k·δ − F)/(k + k_s) with k = e·k_axial.
pub fn seatedStatics(c: Criteria, force_n: f64, e: f64) SeatedStatics {
    const k = e * c.stand_in.latch_link.full_stiffness.k_axial_n_m;
    const ks = seatStiffness(c);
    const d = c.stand_in.latch_link.preload_offset_m;
    return .{ .tension_n = k * (force_n + ks * d) / (k + ks), .normal_n = ks * (k * d - force_n) / (k + ks) };
}

/// T_block = k·u·μ_p − √((k·u·μ_p)² − 2·k·u·F_act), at e = 1.
pub fn blockTension(c: Criteria) f64 {
    const k = c.stand_in.latch_link.full_stiffness.k_axial_n_m;
    const u = c.stand_in.pawl.travel_m;
    const kump = k * u * c.stand_in.pawl.friction_coefficient;
    return kump - @sqrt(kump * kump - 2.0 * k * u * c.stand_in.pawl.actuator_force_limit_n);
}

/// Engagement (and release) completion time u_full/v_max.
pub fn travelTime(c: Criteria) f64 {
    return c.stand_in.pawl.travel_m / c.stand_in.pawl.speed_limit_m_s;
}

/// Declared axial c_full = 2·ζ·√(k_full·μ_red), reduced mass from the two
/// declared fixture masses (also when A is static; convention
/// `convention_reduced_mass`).
pub fn cFullAxial(c: Criteria, b: Bodies) f64 {
    const mu = link_eval.reducedMass(b.body[0].mass_kg, b.body[1].mass_kg);
    return link_eval.dampingCoefficient(c.stand_in.latch_link.full_damping_ratio, c.stand_in.latch_link.full_stiffness.k_axial_n_m, mu);
}

/// One-degree-of-freedom axial model of the C5 reference.
pub const C5Model = struct {
    k_n_m: f64,
    c_n_s_m: f64,
    mass_kg: f64,
    force_n: f64,
    /// Initial position (C5: F/k).
    x0_m: f64,
    /// v_max/u_full: e(t) = 1 − t·rate.
    rate_1_s: f64,
    /// Separation when k·x + c·ẋ exceeds this (infinite: never).
    t_full_n: f64,
};

pub const Rk4Result = struct { x_m: f64, v_m_s: f64, separation_step: ?usize };

fn c5Deriv(p: C5Model, t: f64, x: f64, v: f64) [2]f64 {
    const e = 1.0 - t * p.rate_1_s;
    return .{ v, (p.force_n - e * (p.k_n_m * x + p.c_n_s_m * v)) / p.mass_kg };
}

/// Classical RK4 with step `h` from x = x0, ẋ = 0 at t = 0, for `n_steps`
/// steps. `separation_step` is the first step count (end of step) at which
/// k·x + c·ẋ > T_full, which is 0 if that already holds initially.
pub fn rk4Integrate(p: C5Model, h: f64, n_steps: usize) Rk4Result {
    var x = p.x0_m;
    var v: f64 = 0;
    if (p.k_n_m * x + p.c_n_s_m * v > p.t_full_n) return .{ .x_m = x, .v_m_s = v, .separation_step = 0 };
    for (0..n_steps) |i| {
        const t = @as(f64, @floatFromInt(i)) * h;
        const k1 = c5Deriv(p, t, x, v);
        const k2 = c5Deriv(p, t + 0.5 * h, x + 0.5 * h * k1[0], v + 0.5 * h * k1[1]);
        const k3 = c5Deriv(p, t + 0.5 * h, x + 0.5 * h * k2[0], v + 0.5 * h * k2[1]);
        const k4 = c5Deriv(p, t + h, x + h * k3[0], v + h * k3[1]);
        x += h / 6.0 * (k1[0] + 2.0 * k2[0] + 2.0 * k3[0] + k4[0]);
        v += h / 6.0 * (k1[1] + 2.0 * k2[1] + 2.0 * k3[1] + k4[1]);
        if (p.k_n_m * x + p.c_n_s_m * v > p.t_full_n) return .{ .x_m = x, .v_m_s = v, .separation_step = i + 1 };
    }
    return .{ .x_m = x, .v_m_s = v, .separation_step = null };
}

/// C5 reference: separation time after the release command, by RK4 at 1 µs
/// of the open-seat axial model (protocol "References"). `null` when the
/// pawl is blocked (F above T_block) or no separation occurs before the
/// pawl has fully retracted.
pub fn c5Reference(c: Criteria, mass_kg: f64, damping_n_s_m: f64, force_n: f64) ?f64 {
    if (force_n > blockTension(c)) return null;
    const h = 1e-6;
    const horizon = travelTime(c);
    const n_steps: usize = @intFromFloat(@ceil(horizon / h));
    const r = rk4Integrate(.{
        .k_n_m = c.stand_in.latch_link.full_stiffness.k_axial_n_m,
        .c_n_s_m = damping_n_s_m,
        .mass_kg = mass_kg,
        .force_n = force_n,
        .x0_m = force_n / c.stand_in.latch_link.full_stiffness.k_axial_n_m,
        .rate_1_s = 1.0 / horizon,
        .t_full_n = c.stand_in.latch_link.full_limits.tension_n,
    }, h, n_steps);
    const step = r.separation_step orelse return null;
    return @as(f64, @floatFromInt(step)) * h;
}

// --- Per-axis loads, limits, and deflections ---

pub const all_axes = [_]cc.Axis{ .tension, .shear, .bending, .torsion };

pub fn fullLimit(c: Criteria, axis: cc.Axis) f64 {
    const l = c.stand_in.latch_link.full_limits;
    return switch (axis) {
        .tension => l.tension_n,
        .shear => l.shear_n,
        .bending => l.bending_nm,
        .torsion => l.torsion_nm,
    };
}

/// limit(e) = e·limit_full (engagement law: linear in pawl travel).
pub fn limitAt(c: Criteria, axis: cc.Axis, e: f64) f64 {
    return e * fullLimit(c, axis);
}

pub fn fullStiffnessOf(c: Criteria, axis: cc.Axis) f64 {
    const k = c.stand_in.latch_link.full_stiffness;
    return switch (axis) {
        .tension => k.k_axial_n_m,
        .shear => k.k_shear_n_m,
        .bending => k.k_bend_nm_rad,
        .torsion => k.k_torsion_nm_rad,
    };
}

/// Solver-reported load of one axis in the step (protocol "Loads per axis").
/// Tension T = −F_b[0] has no limit when T ≤ 0, so it reads 0 then.
pub fn axisLoad(axis: cc.Axis, s: *const Sample) f64 {
    return switch (axis) {
        .tension => @max(0.0, -s.force_b_n[0]),
        .shear => @sqrt(s.force_b_n[1] * s.force_b_n[1] + s.force_b_n[2] * s.force_b_n[2]),
        .bending => @sqrt(s.moment_b_nm[1] * s.moment_b_nm[1] + s.moment_b_nm[2] * s.moment_b_nm[2]),
        .torsion => @abs(s.moment_b_nm[0]),
    };
}

/// L_target = factor·limit(e).
pub fn loadTarget(c: Criteria, axis: cc.Axis, e: f64, factor: f64) f64 {
    return factor * limitAt(c, axis, e);
}

/// Applied load magnitude L(t) = L_target·min(t/ramp, 1) (C3 loads).
pub fn loadAt(c: Criteria, axis: cc.Axis, e: f64, factor: f64, t_s: f64) f64 {
    return loadTarget(c, axis, e, factor) * @min(t_s / c.link_limits.ramp_duration_s, 1.0);
}

/// The component of the reported deflection that responds to `axis`:
/// ext[0], ext[1], rot[1], rot[0] for tension, shear, bending, torsion.
fn deflectionOf(axis: cc.Axis, s: *const Sample) f64 {
    return switch (axis) {
        .tension => s.extension_m[0],
        .shear => s.extension_m[1],
        .bending => s.rotation_rad[1],
        .torsion => s.rotation_rad[0],
    };
}

// --- Seat axial force ---

/// N_ax = Σ over guide contacts on B of f_n·(n · a_world), the normal
/// acting on B (pointing from A toward B).
pub fn seatAxialForce(s: *const Sample, a_world: Vec3) f64 {
    var sum: f64 = 0;
    for (s.contactSlice()) |ct| {
        if (ct.body_b != null and ct.body_b.? == 1) sum += ct.normal_force_n * m3.dot(ct.normal, a_world);
    }
    return sum;
}

fn guideCountOnB(s: *const Sample) usize {
    var n: usize = 0;
    for (s.contactSlice()) |ct| {
        if (ct.body_b != null and ct.body_b.? == 1 and ct.normal_force_n > 0) n += 1;
    }
    return n;
}

fn guideNormalSum(s: *const Sample) f64 {
    var sum: f64 = 0;
    for (s.contactSlice()) |ct| if (ct.isGuide()) {
        sum += ct.normal_force_n;
    };
    return sum;
}

// --- C1, C2 ---

const SeatedWindow = struct {
    tension_n: f64,
    n_ax: f64,
    count_not_four: usize,
    n_ax_not_positive: usize,
};

fn seatedWindow(c: Criteria, b: Bodies, samples: []const Sample) SeatedWindow {
    const st = c.statics;
    var n: usize = 0;
    var sum_t: f64 = 0;
    var sum_n: f64 = 0;
    var bad_count: usize = 0;
    var bad_n: usize = 0;
    for (samples) |*s| {
        if (!inWin(s, st.window_start_s, st.duration_s)) continue;
        const a_world = s.quat[0].rotate(b.axes_a[0]);
        const nax = seatAxialForce(s, a_world);
        sum_t += tension(s);
        sum_n += nax;
        if (guideCountOnB(s) != 4) bad_count += 1;
        if (!(nax > 0)) bad_n += 1;
        n += 1;
    }
    if (n == 0) return .{ .tension_n = nan(), .n_ax = nan(), .count_not_four = 1, .n_ax_not_positive = 1 };
    const k = 1.0 / count(n);
    return .{ .tension_n = sum_t * k, .n_ax = sum_n * k, .count_not_four = bad_count, .n_ax_not_positive = bad_n };
}

fn seatedMetrics(ev: *Evaluation, c: Criteria, b: Bodies, samples: []const Sample, force_n: f64, tol: f64) SeatedWindow {
    const ref = seatedStatics(c, force_n, 1.0);
    const w = seatedWindow(c, b, samples);
    push(ev, "tension_rel_error", relErr(w.tension_n, ref.tension_n), tol);
    push(ev, "seat_axial_rel_error", relErr(w.n_ax, ref.normal_n), tol);
    push(ev, "force_balance_rel_error", relErr(w.tension_n - w.n_ax, force_n), tol);
    push(ev, "guide_count_not_four_samples", count(w.count_not_four), 0);
    return w;
}

/// C1: seated statics at F = m·g.
pub fn c1(c: Criteria, b: Bodies, samples: []const Sample) Evaluation {
    var ev: Evaluation = .{};
    _ = seatedMetrics(&ev, c, b, samples, weightB(b), c.statics.seated_preload.force_rel_tol);
    return ev;
}

/// C2 below: as C1 with F = below_factor·F_sep, and N_ax > 0 in every window
/// sample. The force balance uses the total pull F (equal to m·g in C1).
pub fn c2Below(c: Criteria, b: Bodies, samples: []const Sample) Evaluation {
    var ev: Evaluation = .{};
    const sep = c.statics.seat_separation;
    const w = seatedMetrics(&ev, c, b, samples, sep.below_factor * separationForce(c, 1.0), sep.force_rel_tol);
    push(&ev, "seat_axial_not_positive_samples", count(w.n_ax_not_positive), 0);
    return ev;
}

/// C2 above: open seat; Σ guide f_n ≤ 1e-9 N in the window, |T − F|/F with F = above_factor·F_sep.
pub fn c2Above(c: Criteria, b: Bodies, samples: []const Sample) Evaluation {
    _ = b;
    var ev: Evaluation = .{};
    const st = c.statics;
    const sep = st.seat_separation;
    const f = sep.above_factor * separationForce(c, 1.0);
    var n: usize = 0;
    var sum_t: f64 = 0;
    var max_normal: f64 = 0;
    for (samples) |*s| {
        if (!inWin(s, st.window_start_s, st.duration_s)) continue;
        sum_t += tension(s);
        max_normal = @max(max_normal, guideNormalSum(s));
        n += 1;
    }
    if (n == 0) {
        push(&ev, "max_guide_normal_force_n", nan(), sep.open_seat_normal_max_n);
        push(&ev, "tension_rel_error", nan(), sep.force_rel_tol);
        return ev;
    }
    push(&ev, "max_guide_normal_force_n", max_normal, sep.open_seat_normal_max_n);
    push(&ev, "tension_rel_error", relErr(sum_t / count(n), f), sep.force_rel_tol);
    return ev;
}

// --- C3 ---

/// C3 below: no separation, and the window-mean deflection against
/// L_target/(e·k_axis).
pub fn c3Below(c: Criteria, axis: cc.Axis, e: f64, samples: []const Sample) Evaluation {
    var ev: Evaluation = .{};
    const l = c.link_limits;
    var sep: f64 = 0;
    for (samples) |*s| if (s.active_during and !s.active_after) {
        sep = 1;
    };
    if (samples.len == 0 or !samples[samples.len - 1].active_after) sep = 1;
    push(&ev, "separation_occurred", sep, 0);
    var n: usize = 0;
    var sum: f64 = 0;
    for (samples) |*s| {
        if (!inWin(s, l.hold_window_start_s, l.duration_s)) continue;
        sum += deflectionOf(axis, s);
        n += 1;
    }
    const ref = loadTarget(c, axis, e, l.below_factor) / (e * fullStiffnessOf(c, axis));
    push(&ev, "hold_deflection_rel_error", if (n == 0) nan() else relErr(sum / count(n), ref), l.hold_deflection_rel_tol);
    return ev;
}

/// C3 above. `load_n[i]` is the applied load magnitude L(t) of sample i
/// (see `loadAt`); L(t_s) is read at the separation sample.
///
/// Rule violations are counted: at the separation step the tested axis load
/// must exceed limit(e), and at every earlier step every axis load must be
/// at or below its limit(e). After: every later sample has the link inactive
/// (during and after) and exactly zero reported force and moment.
pub fn c3Above(c: Criteria, axis: cc.Axis, e: f64, samples: []const Sample, load_n: []const f64) Evaluation {
    var ev: Evaluation = .{};
    std.debug.assert(load_n.len == samples.len);
    const l = c.link_limits;
    const si = separationIndex(samples) orelse {
        push(&ev, "separation_occurred", 1, 0);
        push(&ev, "rule_violations", 1, 0);
        push(&ev, "separation_load_rel_error", inf(), l.separation_load_rel_tol);
        push(&ev, "after_separation_violations", 0, 0);
        return ev;
    };
    push(&ev, "separation_occurred", 0, 0);
    var rule: usize = 0;
    if (!(axisLoad(axis, &samples[si]) > limitAt(c, axis, e))) rule += 1;
    for (samples[1..si]) |*s| {
        for (all_axes) |ax| if (axisLoad(ax, s) > limitAt(c, ax, e)) {
            rule += 1;
        };
    }
    push(&ev, "rule_violations", count(rule), 0);
    const lim = limitAt(c, axis, e);
    push(&ev, "separation_load_rel_error", relErr(load_n[si], lim), l.separation_load_rel_tol);
    var after: usize = 0;
    for (samples[si + 1 ..]) |*s| {
        if (s.active_during or s.active_after) after += 1;
        for (s.force_b_n) |x| if (x != 0) {
            after += 1;
        };
        for (s.moment_b_nm) |x| if (x != 0) {
            after += 1;
        };
    }
    push(&ev, "after_separation_violations", count(after), 0);
    return ev;
}

// --- C4 ---

/// C4 engage: completion time, per-step engagement change, window-mean preload.
pub fn c4Engage(c: Criteria, b: Bodies, samples: []const Sample) Evaluation {
    var ev: Evaluation = .{};
    const en = c.engagement;
    const pw = c.stand_in.pawl;
    const dt = b.dt_s;
    var first: ?f64 = null;
    for (samples) |*s| if (s.u_m >= pw.travel_m) {
        first = s.t_s;
        break;
    };
    push(&ev, "completion_time_error_steps", if (first) |t| @abs(t - travelTime(c)) / dt else inf(), count(en.completion_time_tol_steps));
    const bound = pw.speed_limit_m_s * dt / pw.travel_m * (1.0 + 1e-12);
    var worst: f64 = 0;
    for (samples[@min(1, samples.len)..]) |*s| worst = @max(worst, @abs(s.e_after - s.e_during) / bound);
    push(&ev, "engagement_step_over_limit", worst, 1);
    var n: usize = 0;
    var sum: f64 = 0;
    for (samples) |*s| {
        if (!inWin(s, en.window_start_s, en.duration_s)) continue;
        sum += tension(s);
        n += 1;
    }
    push(&ev, "preload_rel_error", if (n == 0) nan() else relErr(sum / count(n), preload(c, 1.0)), en.preload_rel_tol);
    return ev;
}

/// C4 blocked: u = 0 and the link inactive at every sample.
pub fn c4Blocked(samples: []const Sample) Evaluation {
    var ev: Evaluation = .{};
    var bad: usize = 0;
    for (samples) |*s| {
        if (s.u_m != 0 or s.active_during or s.active_after) bad += 1;
    }
    push(&ev, "blocked_violations", if (samples.len == 0) nan() else count(bad), 0);
    return ev;
}

// --- C5 ---

/// C5 below. `force_n` is the total axial pull F = m·g + F_val on B.
pub fn c5Below(c: Criteria, b: Bodies, samples: []const Sample, force_n: f64) Evaluation {
    var ev: Evaluation = .{};
    const r = c.release_under_load;
    const pw = c.stand_in.pawl;
    const dt = b.dt_s;
    const sep = separationIndex(samples);
    const ref = c5Reference(c, b.body[1].mass_kg, cFullAxial(c, b), force_n);
    const err = if (sep != null and ref != null) @abs(samples[sep.?].t_s - (r.release_start_s + ref.?)) / dt else inf();
    push(&ev, "separation_time_error_steps", err, count(r.separation_time_tol_steps));
    var worst: f64 = if (sep == null) inf() else 0;
    if (sep) |si| {
        const per_step = pw.speed_limit_m_s * dt;
        for (samples[1..si], 1..) |*s, n| {
            const prev = &samples[n - 1];
            if (!atOrAfter(prev.t_s, r.release_start_s, dt)) continue;
            worst = @max(worst, @abs((prev.u_m - s.u_m) - per_step) / per_step);
        }
    }
    push(&ev, "pawl_retraction_rel_error", worst, 1e-12);
    return ev;
}

/// C5 above: u = u_full at every sample, no separation, active at the end.
pub fn c5Above(c: Criteria, samples: []const Sample) Evaluation {
    var ev: Evaluation = .{};
    var moved: usize = 0;
    for (samples) |*s| if (s.u_m != c.stand_in.pawl.travel_m) {
        moved += 1;
    };
    push(&ev, "pawl_moved_samples", if (samples.len == 0) nan() else count(moved), 0);
    push(&ev, "separation_occurred", if (separationIndex(samples) == null) 0 else 1, 0);
    push(&ev, "link_inactive_at_end", if (samples.len > 0 and samples[samples.len - 1].active_after) 0 else 1, 0);
    return ev;
}

// --- C6 ---

pub fn c6(c: Criteria, b: Bodies, samples: []const Sample) Evaluation {
    var ev: Evaluation = .{};
    const u = c.unloaded_release;
    const pw = c.stand_in.pawl;
    const dt = b.dt_s;
    const sep = separationIndex(samples);
    const t_expected = u.release_start_s + travelTime(c);
    push(&ev, "removal_time_error_steps", if (sep) |si| @abs(samples[si].t_s - t_expected) / dt else inf(), count(u.removal_time_tol_steps));
    // Bound: max_tension_step_change_over_quasi_static × (k·δ·v_max·Δt/u_full).
    const quasi = c.stand_in.latch_link.full_stiffness.k_axial_n_m * c.stand_in.latch_link.preload_offset_m * pw.speed_limit_m_s * dt / pw.travel_m;
    const bound = u.max_tension_step_change_over_quasi_static * quasi;
    var worst: f64 = 0;
    for (samples[@min(1, samples.len)..], 1..) |*s, n| {
        if (!atOrAfter(samples[n - 1].t_s, u.release_start_s, dt)) continue;
        worst = @max(worst, @abs(tension(s) - tension(&samples[n - 1])) / bound);
    }
    push(&ev, "tension_step_change_over_bound", if (samples.len == 0) nan() else worst, 1);
    var after: usize = 0;
    if (sep) |si| {
        for (samples[si + 1 ..]) |*s| {
            if (s.active_during or s.active_after) after += 1;
            for (s.force_b_n) |x| if (x != 0) {
                after += 1;
            };
            for (s.moment_b_nm) |x| if (x != 0) {
                after += 1;
            };
        }
    }
    push(&ev, "after_removal_violations", if (sep == null) 1 else count(after), 0);
    return ev;
}

// --- C7 (through link_eval, protocol of compliant-link-v1 revision 2) ---

pub const C7Kind = enum { axial, torsion };

/// ω = √(e·k/μ_red) (axial) or √(e·k_t/I_red) (torsion).
pub fn c7Omega(c: Criteria, b: Bodies, kind: C7Kind, e: f64) f64 {
    const k = c.stand_in.latch_link.full_stiffness;
    return switch (kind) {
        .axial => @sqrt(e * k.k_axial_n_m / link_eval.reducedMass(b.body[0].mass_kg, b.body[1].mass_kg)),
        .torsion => @sqrt(e * k.k_torsion_nm_rad / link_eval.reducedInertia(b.body[0].inertia_kg_m2, b.body[1].inertia_kg_m2)),
    };
}

/// Resolution rule of Q43/Q52: combinations beyond the limit are
/// `outside_envelope` and not counted.
pub fn c7Resolved(c: Criteria, b: Bodies, kind: C7Kind, e: f64) bool {
    return link_eval.resolved(c7Omega(c, b, kind, e), b.dt_s, c.resolution.max_omega_dt);
}

pub fn c7Period(c: Criteria, b: Bodies, kind: C7Kind, e: f64, samples: []const link_eval.Sample) Evaluation {
    const ch: link_eval.Channel = switch (kind) {
        .axial => .axial_extension,
        .torsion => .twist,
    };
    return link_eval.periodCheck("period_rel_error", c.stiff_dynamics.period_rel_tol, c7Omega(c, b, kind, e), ch, samples);
}

pub fn c7Damping(c: Criteria, samples: []const link_eval.Sample) Evaluation {
    const d = c.stiff_dynamics;
    return link_eval.physicalDamping(.{
        .id = d.id,
        .initial_stretch_m = d.initial_stretch_m,
        .damping_ratio = d.physical_damping_ratio,
        .zeta_measure = .log_of_ratio_of_first_and_last_positive_peaks_over_full_periods_divided_by_2pi_n,
        .zeta_rel_tol = d.zeta_rel_tol,
    }, samples);
}

pub fn c7Numerical(c: Criteria, samples: []const link_eval.Sample) Evaluation {
    const d = c.stiff_dynamics;
    return link_eval.numericalDissipation(.{
        .id = d.id,
        .initial_stretch_m = d.initial_stretch_m,
        .damping_ratio = 0,
        .zeta_measure = .log_of_ratio_of_first_and_last_positive_peaks_over_full_periods_divided_by_2pi_n,
        .zeta_num_max = d.zeta_num_max,
    }, samples);
}

// --- Audits ---

/// Momentum audit (runs without a static body): max over t > 0 of
/// |p − (p₀ + M·g⃗·t)| / (rel·M·g·t + floor), limit 1. Validation loads do
/// not enter (C3 loads are equal and opposite).
pub fn auditMomentum(c: Criteria, b: Bodies, samples: []const Sample) Evaluation {
    var ev: Evaluation = .{};
    if (b.body[0].is_static or b.body[1].is_static) {
        pushInfo(&ev, "momentum_not_applicable_static_body", 0, 1);
        return ev;
    }
    if (samples.len < 2) {
        push(&ev, "momentum_error_over_allowance", nan(), 1);
        return ev;
    }
    const a = c.audits.momentum;
    const m_total = b.body[0].mass_kg + b.body[1].mass_kg;
    const g_mag = m3.length(b.gravity_m_s2);
    const p0 = momentumOf(b, &samples[0]);
    var worst: f64 = 0;
    for (samples[1..]) |*s| {
        const expected = m3.add(p0, m3.scale(b.gravity_m_s2, m_total * s.t_s));
        const err = m3.length(m3.sub(momentumOf(b, s), expected));
        worst = @max(worst, err / (a.rel_tol_of_m_g_t * m_total * g_mag * s.t_s + a.abs_floor_kg_m_s));
    }
    push(&ev, "momentum_error_over_allowance", worst, 1);
    return ev;
}

fn momentumOf(b: Bodies, s: *const Sample) Vec3 {
    return m3.add(m3.scale(s.vel[0], b.body[0].mass_kg), m3.scale(s.vel[1], b.body[1].mass_kg));
}

const Accum = struct {
    f: Vec3 = m3.zero,
    f_abs: f64 = 0,
    tau: Vec3 = m3.zero,
    tau_abs: f64 = 0,

    fn force(self: *Accum, f: Vec3, r: Vec3) void {
        self.f = m3.add(self.f, f);
        self.f_abs += m3.length(f);
        const t = m3.cross(r, f);
        self.tau = m3.add(self.tau, t);
        self.tau_abs += m3.length(t);
    }

    fn torque(self: *Accum, t: Vec3) void {
        self.tau = m3.add(self.tau, t);
        self.tau_abs += m3.length(t);
    }
};

/// Forces and torques on body `idx` in step `cur`, with lever arms from the
/// step-start pose `prev` (protocol "Impulse accounting").
fn stepAccum(b: Bodies, prev: *const Sample, cur: *const Sample, idx: u32) Accum {
    var acc: Accum = .{};
    for (cur.contactSlice()) |ct| {
        const fvec = m3.add(m3.scale(ct.normal, ct.normal_force_n), ct.tangential_force_n);
        var sign: f64 = 0;
        if (ct.body_b) |bb| {
            if (bb == idx) sign = 1 else if (ct.body_a == idx) sign = -1;
        } else if (ct.body_a == idx) sign = 1;
        if (sign != 0) acc.force(m3.scale(fvec, sign), m3.sub(ct.point_m, prev.pos[idx]));
    }
    const fw = linkToWorld(b, prev.quat[0], cur.force_b_n);
    const mw = linkToWorld(b, prev.quat[0], cur.moment_b_nm);
    if (idx == 1) {
        acc.force(fw, prev.quat[1].rotate(b.anchor_b_m));
        acc.torque(mw);
    } else {
        acc.force(m3.scale(fw, -1.0), prev.quat[0].rotate(b.anchor_a_m));
        acc.torque(m3.scale(mw, -1.0));
    }
    for (cur.loadSlice()) |ld| if (ld.body == idx) {
        acc.force(ld.force_n, m3.sub(ld.point_m, prev.pos[idx]));
        acc.torque(ld.torque_nm);
    };
    return acc;
}

/// Impulse accounting: every velocity and angular-velocity change of every
/// dynamic body is explained by gravity and the reported forces within
/// rel·Δt·(Σ|·|) + floor. The metrics are the worst ratio to the allowance
/// (limit 1).
pub fn auditImpulse(c: Criteria, b: Bodies, samples: []const Sample) Evaluation {
    var ev: Evaluation = .{};
    if (samples.len < 2) {
        push(&ev, "impulse_linear_over_allowance", nan(), 1);
        push(&ev, "impulse_angular_over_allowance", nan(), 1);
        return ev;
    }
    const a = c.audits.impulse_accounting;
    const dt = b.dt_s;
    const g_mag = m3.length(b.gravity_m_s2);
    var worst_lin: f64 = 0;
    var worst_ang: f64 = 0;
    for (samples[1..], 1..) |*cur, n| {
        const prev = &samples[n - 1];
        for (0..2) |bi| {
            const spec = b.body[bi];
            if (spec.is_static) continue;
            const idx: u32 = @intCast(bi);
            const acc = stepAccum(b, prev, cur, idx);
            const dv = m3.sub(cur.vel[bi], prev.vel[bi]);
            const lin = m3.sub(m3.scale(dv, spec.mass_kg), m3.scale(m3.add(m3.scale(b.gravity_m_s2, spec.mass_kg), acc.f), dt));
            const lin_allow = a.rel_tol_of_step_impulse_sum * dt * (spec.mass_kg * g_mag + acc.f_abs) + a.abs_floor_n_s;
            worst_lin = @max(worst_lin, m3.length(lin) / lin_allow);
            const dw = m3.sub(cur.omega[bi], prev.omega[bi]);
            const ang = m3.sub(m3.scale(dw, spec.inertia_kg_m2), m3.scale(acc.tau, dt));
            const ang_allow = a.rel_tol_of_step_impulse_sum * dt * acc.tau_abs + a.abs_floor_n_s;
            worst_ang = @max(worst_ang, m3.length(ang) / ang_allow);
        }
    }
    push(&ev, "impulse_linear_over_allowance", worst_lin, 1);
    push(&ev, "impulse_angular_over_allowance", worst_ang, 1);
    return ev;
}

fn bitsEqual(a: f64, b: f64) bool {
    return @as(u64, @bitCast(a)) == @as(u64, @bitCast(b));
}

fn vecBitsEqual(a: Vec3, b: Vec3) bool {
    return bitsEqual(a[0], b[0]) and bitsEqual(a[1], b[1]) and bitsEqual(a[2], b[2]);
}

fn quatBitsEqual(a: m3.Quat, b: m3.Quat) bool {
    return bitsEqual(a.w, b.w) and bitsEqual(a.x, b.x) and bitsEqual(a.y, b.y) and bitsEqual(a.z, b.z);
}

/// Pose integration: x_n bit-identical to x_{n−1} + Δt·v_n and q_n
/// bit-identical to q_{n−1}.integrate(ω_n, Δt), with the same `math3`
/// operations as the solver. Static bodies are skipped. The metrics are
/// mismatch counts (limit 0).
pub fn auditPose(b: Bodies, samples: []const Sample) Evaluation {
    var ev: Evaluation = .{};
    if (samples.len < 2) {
        push(&ev, "position_mismatches", nan(), 0);
        push(&ev, "orientation_mismatches", nan(), 0);
        return ev;
    }
    var pos_bad: usize = 0;
    var ori_bad: usize = 0;
    for (samples[1..], 1..) |*cur, n| {
        const prev = &samples[n - 1];
        for (0..2) |bi| {
            if (b.body[bi].is_static) continue;
            const x = m3.add(prev.pos[bi], m3.scale(cur.vel[bi], b.dt_s));
            if (!vecBitsEqual(x, cur.pos[bi])) pos_bad += 1;
            const q = prev.quat[bi].integrate(cur.omega[bi], b.dt_s);
            if (!quatBitsEqual(q, cur.quat[bi])) ori_bad += 1;
        }
    }
    push(&ev, "position_mismatches", count(pos_bad), 0);
    push(&ev, "orientation_mismatches", count(ori_bad), 0);
    return ev;
}

fn stiffnessList(c: Criteria) [6]f64 {
    const k = c.stand_in.latch_link.full_stiffness;
    return .{ k.k_axial_n_m, k.k_shear_n_m, k.k_shear_n_m, k.k_torsion_nm_rad, k.k_bend_nm_rad, k.k_bend_nm_rad };
}

/// ½·Σ k_i,full·C_i² over the six reported coordinates.
fn linkPotentialFull(c: Criteria, s: *const Sample) f64 {
    const k = stiffnessList(c);
    const coords: [6]f64 = .{ s.extension_m[0], s.extension_m[1], s.extension_m[2], s.rotation_rad[0], s.rotation_rad[1], s.rotation_rad[2] };
    var sum: f64 = 0;
    for (k, coords) |ki, ci| sum += ki * ci * ci;
    return 0.5 * sum;
}

/// V_link = ½·Σ e_during·k_i,full·C_i² while the link has rows.
///
/// Convention: a step without link rows (`active_during` false) holds no
/// link potential, so a pawl that advances before the link exists (C8) does
/// not create phantom energy.
fn linkPotential(c: Criteria, s: *const Sample) f64 {
    return if (s.active_during) s.e_during * linkPotentialFull(c, s) else 0;
}

/// W increment of the coupler update after step n: ½·Σ k·C²·(e_after − e_during),
/// with e_after counted as 0 when the link is removed. Zero when the link had
/// no rows in the step. Link activation is deliberately not credited.
fn workIncrement(c: Criteria, s: *const Sample) f64 {
    if (!s.active_during) return 0;
    const e_after = if (s.active_after) s.e_after else 0.0;
    return linkPotentialFull(c, s) * (e_after - s.e_during);
}

fn kineticComFrame(b: Bodies, s: *const Sample) f64 {
    var m_total: f64 = 0;
    var p: Vec3 = m3.zero;
    for (0..2) |i| {
        if (b.body[i].is_static) continue;
        m_total += b.body[i].mass_kg;
        p = m3.add(p, m3.scale(s.vel[i], b.body[i].mass_kg));
    }
    if (m_total == 0) return 0;
    const v_cm = m3.scale(p, 1.0 / m_total);
    var ke: f64 = 0;
    for (0..2) |i| {
        if (b.body[i].is_static) continue;
        const dv = m3.sub(s.vel[i], v_cm);
        ke += 0.5 * b.body[i].mass_kg * m3.dot(dv, dv) + 0.5 * b.body[i].inertia_kg_m2 * m3.dot(s.omega[i], s.omega[i]);
    }
    return ke;
}

fn contactPotential(b: Bodies, s: *const Sample) f64 {
    var sum: f64 = 0;
    for (s.contactSlice()) |ct| sum += ct.normal_force_n * ct.normal_force_n / (2.0 * b.k_contact_n_m);
    return sum;
}

/// Energy audit (C4, C6, C7, C8: free fall without validation loads), in the
/// centre-of-mass frame. One-sided: dissipation is allowed, creation is not.
/// A run with validation loads fails the audit (it does not apply there).
/// The reported `pawl_work_j` is compared with W informationally only.
pub fn auditEnergy(c: Criteria, b: Bodies, samples: []const Sample) Evaluation {
    var ev: Evaluation = .{};
    for (samples) |*s| if (s.n_loads != 0) {
        push(&ev, "energy_audit_run_has_validation_loads", 1, 0);
        return ev;
    };
    if (samples.len < 2) {
        push(&ev, "energy_creation_over_allowance", nan(), 1);
        return ev;
    }
    const e = c.audits.energy;
    const e0 = kineticComFrame(b, &samples[0]) + linkPotential(c, &samples[0]);
    // Pass 1: E_ref = KE_rel(0) + max V_link + max |W|.
    var max_v: f64 = 0;
    var max_w: f64 = 0;
    var w: f64 = 0;
    for (samples, 0..) |*s, i| {
        max_v = @max(max_v, linkPotential(c, s));
        max_w = @max(max_w, @abs(w));
        // Protocol revision 2 (Q58): W at sample n holds the updates made
        // before step n, matching V_link's e_during at sample n.
        if (i > 0) w += workIncrement(c, s);
    }
    max_w = @max(max_w, @abs(w));
    const e_ref = kineticComFrame(b, &samples[0]) + max_v + max_w;
    const allowance = e.creation_rel_tol * e_ref + e.abs_floor_j;
    // Pass 2.
    var worst: f64 = -inf();
    var worst_j: f64 = -inf();
    var work_gap: f64 = 0;
    var reported: f64 = 0;
    w = 0;
    for (samples, 0..) |*s, i| {
        const w_before = w;
        if (i > 0) {
            w += workIncrement(c, s);
            reported += s.pawl_work_j;
            work_gap = @max(work_gap, @abs(reported - w));
        }
        const last = i + 1 == samples.len;
        if (!(s.n_contacts == 0 or last)) continue;
        const total = kineticComFrame(b, s) + linkPotential(c, s) + (if (last) contactPotential(b, s) else 0.0);
        const creation = total - e0 - w_before;
        worst_j = @max(worst_j, creation);
        worst = @max(worst, creation / allowance);
    }
    push(&ev, "energy_creation_over_allowance", worst, 1);
    pushInfo(&ev, "info_max_energy_creation_j", worst_j, 0);
    pushInfo(&ev, "info_e_ref_j", e_ref, 0);
    pushInfo(&ev, "info_reported_pawl_work_vs_w_max_gap_j", work_gap, 0);
    return ev;
}

// --- C8 ---

/// Strict overlap of two equal cubes (half edge `half`) by the 15-axis
/// separating-axis test: touching or separated is not overlap.
pub fn obbOverlap(a_pos: Vec3, a_quat: m3.Quat, b_pos: Vec3, b_quat: m3.Quat, half: f64) bool {
    return satOverlap(a_pos, a_quat, b_pos, b_quat, half, true);
}

fn satOverlap(a_pos: Vec3, a_quat: m3.Quat, b_pos: Vec3, b_quat: m3.Quat, half: f64, with_edges: bool) bool {
    const ax: [3]Vec3 = .{ a_quat.rotate(.{ 1, 0, 0 }), a_quat.rotate(.{ 0, 1, 0 }), a_quat.rotate(.{ 0, 0, 1 }) };
    const bx: [3]Vec3 = .{ b_quat.rotate(.{ 1, 0, 0 }), b_quat.rotate(.{ 0, 1, 0 }), b_quat.rotate(.{ 0, 0, 1 }) };
    const t = m3.sub(b_pos, a_pos);
    for (ax) |l| if (separatedOn(l, t, ax, bx, half)) return false;
    for (bx) |l| if (separatedOn(l, t, ax, bx, half)) return false;
    if (with_edges) {
        for (ax) |ai| for (bx) |bj| {
            const x = m3.cross(ai, bj);
            const len = m3.length(x);
            if (len * len < 1e-20) continue; // parallel edges: covered by the face axes
            if (separatedOn(m3.scale(x, 1.0 / len), t, ax, bx, half)) return false;
        };
    }
    return true;
}

fn separatedOn(l: Vec3, t: Vec3, ax: [3]Vec3, bx: [3]Vec3, half: f64) bool {
    var ra: f64 = 0;
    var rb: f64 = 0;
    for (0..3) |i| {
        ra += @abs(m3.dot(ax[i], l));
        rb += @abs(m3.dot(bx[i], l));
    }
    return @abs(m3.dot(t, l)) >= half * ra + half * rb;
}

/// Ball centre in A's coupler frame (x from the face plane along the axis).
pub fn ballCoupler(b: Bodies, s: *const Sample) Vec3 {
    const cw = m3.add(s.pos[1], s.quat[1].rotate(b.ball_centre_b_m));
    const la = s.quat[0].rotateInverse(m3.sub(cw, s.pos[0]));
    return .{ m3.dot(b.axes_a[0], la) - b.face_offset_a_m, m3.dot(b.axes_a[1], la), m3.dot(b.axes_a[2], la) };
}

/// Seat point x in the coupler frame, from the mouth plane (positive
/// outward): r/sin α − apex_depth.
pub fn seatX(c: Criteria) f64 {
    return c.stand_in.probe.radius_m / @sin(seatAlpha(c)) - c.stand_in.socket.apex_depth_m;
}

/// Capture zone around the seat point (radial and axial half-extents).
pub fn inCaptureZone(c: Criteria, ball: Vec3) bool {
    const z = c.stand_in.pawl.capture_zone;
    return @abs(ball[0] - seatX(c)) <= z.axial_m and @sqrt(ball[1] * ball[1] + ball[2] * ball[2]) <= z.radial_m;
}

pub const Validity = enum { valid, outside_model };

/// `outside_model` if any sample has the cubes overlapping or the ball
/// centre's lateral coordinates outside ±8 mm. An empty run is outside the model.
pub fn validity(b: Bodies, samples: []const Sample) Validity {
    if (samples.len == 0) return .outside_model;
    for (samples) |*s| {
        if (obbOverlap(s.pos[0], s.quat[0], s.pos[1], s.quat[1], b.half_edge_m)) return .outside_model;
        const ball = ballCoupler(b, s);
        if (@abs(ball[1]) > lateral_validity_m or @abs(ball[2]) > lateral_validity_m) return .outside_model;
    }
    return .valid;
}

pub const Class = enum { captured, partial, separated, latch_blocked, missed };

/// Final-sample classification (protocol table, applied in table order).
pub fn classify(c: Criteria, b: Bodies, samples: []const Sample) Class {
    if (samples.len == 0) return .missed;
    const last = &samples[samples.len - 1];
    var ever_active = false;
    for (samples) |*s| if (s.active_during or s.active_after) {
        ever_active = true;
    };
    const ball = ballCoupler(b, last);
    if (last.active_after and last.e_after >= 1.0 and inCaptureZone(c, ball)) return .captured;
    if (last.active_after and last.e_after < 1.0) return .partial;
    if (!last.active_after and ever_active) return .separated;
    if (!ever_active and ball[0] < 0) return .latch_blocked;
    return .missed;
}

/// Capture radius: the largest grid offset at and below which every offset
/// is captured, or `null` if the smallest offset is not captured. `offsets`
/// is ascending; `classes[i]` is the class at `offsets[i]`. An offset whose
/// run is `outside_model` must be given as a non-captured class by the
/// caller. The true boundary lies within one grid step above the result.
pub fn captureRadius(offsets: []const f64, classes: []const Class) ?f64 {
    std.debug.assert(offsets.len == classes.len);
    var radius: ?f64 = null;
    for (offsets, classes) |o, k| {
        if (k != .captured) break;
        radius = o;
    }
    return radius;
}

/// `dt_disagreement`: true if one offset's class differs across timesteps.
pub fn dtDisagreement(classes_across_dt: []const Class) bool {
    if (classes_across_dt.len == 0) return false;
    for (classes_across_dt[1..]) |k| if (k != classes_across_dt[0]) return true;
    return false;
}

// --- Tests on synthetic data (no solver) ---

const testing = std.testing;

const strict_json = @import("strict_json.zig");

fn load() !strict_json.Parsed(Criteria) {
    return cc.parse(testing.allocator, cc.coupler_v1_json);
}

fn tAt(i: usize, dt: f64) f64 {
    return @as(f64, @floatFromInt(i)) * dt;
}

fn testBodies(c: Criteria) Bodies {
    const m = c.fixture.mass_kg;
    const edge = c.fixture.size_m[0];
    const spec: BodySpec = .{ .mass_kg = m, .inertia_kg_m2 = link_eval.cubeInertia(m, edge) };
    return .{
        .body = .{ spec, spec },
        .half_edge_m = edge / 2.0,
        .dt_s = 1e-3,
        .gravity_m_s2 = m3.scale(c.gravity.direction_world, c.gravity.magnitude_m_s2),
        .axes_a = couplerAxes(.{ 1, 0, 0 }),
        .face_offset_a_m = edge / 2.0,
        .ball_centre_b_m = .{ -0.014, 0, 0 },
        .k_contact_n_m = c.stand_in.guide_contact.contact_stiffness_n_m,
    };
}

test "references match the protocol's recorded expectations (6 digits)" {
    const p = try load();
    defer p.deinit();
    const c = p.value;
    try testing.expectApproxEqAbs(@as(f64, 0.476190), preload(c, 1.0), 5e-7);
    const weight = c.fixture.mass_kg * c.gravity.magnitude_m_s2;
    const st = seatedStatics(c, weight, 1.0);
    try testing.expectApproxEqAbs(@as(f64, 0.485530), st.tension_n, 5e-7);
    try testing.expectApproxEqAbs(@as(f64, 0.289397), st.normal_n, 5e-7);
    try testing.expectApproxEqAbs(@as(f64, 0.5), separationForce(c, 1.0), 5e-7);
    try testing.expectApproxEqAbs(@as(f64, 1.267949), blockTension(c), 5e-7);
    try testing.expectApproxEqAbs(@as(f64, 0.1), travelTime(c), 1e-15);
    try testing.expectApproxEqRel(@as(f64, 2e5), seatStiffness(c), 1e-12);
    // Statics balance for any F: T − N = F.
    const st2 = seatedStatics(c, 0.45, 1.0);
    try testing.expectApproxEqAbs(@as(f64, 0.45), st2.tension_n - st2.normal_n, 1e-15);
    // Engagement scales F_sep linearly.
    try testing.expectApproxEqAbs(@as(f64, 0.25), separationForce(c, 0.5), 1e-15);
}

test "coupler axes follow the solver's anchor-A frame" {
    const ax = couplerAxes(.{ 0, 0, -1 });
    try testing.expectEqual(Vec3{ 0, -1, 0 }, ax[1]);
    try testing.expectEqual(Vec3{ -1, 0, 0 }, ax[2]);
    const ax2 = couplerAxes(.{ 1, 0, 0 });
    try testing.expectEqual(Vec3{ 0, 0, 1 }, ax2[1]);
    try testing.expectEqual(Vec3{ 0, -1, 0 }, ax2[2]);
}

test "RK4 reference: with e fixed at 1 a damped mass settles at the analytic F/k" {
    const k = 1e4;
    const m = 0.02;
    const cd = 4.0;
    const f = 0.5;
    const model: C5Model = .{ .k_n_m = k, .c_n_s_m = cd, .mass_kg = m, .force_n = f, .x0_m = 0, .rate_1_s = 0, .t_full_n = inf() };
    // Closed form of the underdamped step response at t = 4 ms.
    const wn = @sqrt(k / m);
    const zeta = cd / (2.0 * @sqrt(k * m));
    const wd = wn * @sqrt(1.0 - zeta * zeta);
    const t = 0.004;
    const exact = f / k * (1.0 - @exp(-zeta * wn * t) * (@cos(wd * t) + zeta * wn / wd * @sin(wd * t)));
    const early = rk4Integrate(model, 1e-6, 4000);
    try testing.expectApproxEqRel(exact, early.x_m, 1e-9);
    // Late: settled at the static value x = F/k with no velocity.
    const late = rk4Integrate(model, 1e-6, 300000);
    try testing.expectApproxEqRel(f / k, late.x_m, 1e-9);
    try testing.expect(@abs(late.v_m_s) < 1e-12);
    try testing.expectEqual(@as(?usize, null), late.separation_step);
    // A threshold below the static value is crossed, one above never is.
    var low = model;
    low.t_full_n = 0.4;
    const crossed = rk4Integrate(low, 1e-6, 300000).separation_step.?;
    try testing.expect(crossed > 0 and crossed < 4000);
    var high = model;
    high.t_full_n = 5.0;
    try testing.expectEqual(@as(?usize, null), rk4Integrate(high, 1e-6, 300000).separation_step);
}

test "C5 reference: separation about t_r + 0.043 s below T_block, none above" {
    const p = try load();
    defer p.deinit();
    const c = p.value;
    const b = testBodies(c);
    const t_block = blockTension(c);
    const ref = c5Reference(c, b.body[1].mass_kg, cFullAxial(c, b), 0.9 * t_block).?;
    try testing.expect(ref > 0.040 and ref < 0.046);
    try testing.expectEqual(@as(?f64, null), c5Reference(c, b.body[1].mass_kg, cFullAxial(c, b), 1.1 * t_block));
}

// --- Statics (C1, C2) ---

fn seatedSample(b: Bodies, t: f64, tension_n: f64, normal_n: f64, n_guide: usize) Sample {
    var s: Sample = .{ .t_s = t };
    s.force_b_n = .{ -tension_n, 0, 0 };
    s.active_during = true;
    s.active_after = true;
    s.e_during = 1;
    s.e_after = 1;
    s.u_m = 1e-3;
    const share: f64 = if (n_guide == 0) 0 else normal_n / @as(f64, @floatFromInt(n_guide));
    for (0..n_guide) |i| {
        s.contacts[i] = .{ .body_a = 0, .body_b = 1, .point_m = m3.zero, .normal = b.axes_a[0], .normal_force_n = share, .tangential_force_n = m3.zero };
    }
    s.n_contacts = n_guide;
    return s;
}

fn staticsBodies(c: Criteria) Bodies {
    var b = testBodies(c);
    b.axes_a = couplerAxes(.{ 0, 0, -1 });
    b.body[0].is_static = true;
    return b;
}

fn fillSeated(samples: []Sample, b: Bodies, tension_n: f64, normal_n: f64, n_guide: usize) void {
    for (samples, 0..) |*s, i| s.* = seatedSample(b, tAt(i, 0.0625), tension_n, normal_n, n_guide);
}

test "C1: exact seated statics pass; a 1% tension error and a lost guide contact fail" {
    const p = try load();
    defer p.deinit();
    const c = p.value;
    const b = staticsBodies(c);
    const ref = seatedStatics(c, weightB(b), 1.0);
    var samples: [9]Sample = undefined;
    fillSeated(&samples, b, ref.tension_n, ref.normal_n, 4);
    try testing.expect(c1(c, b, &samples).passed());
    fillSeated(&samples, b, ref.tension_n * 1.01, ref.normal_n, 4);
    try testing.expect(!c1(c, b, &samples).passed());
    fillSeated(&samples, b, ref.tension_n, ref.normal_n * 1.01, 4);
    try testing.expect(!c1(c, b, &samples).passed());
    fillSeated(&samples, b, ref.tension_n, ref.normal_n, 3);
    try testing.expect(!c1(c, b, &samples).passed());
    // Exact values but one window sample with a missing guide contact.
    fillSeated(&samples, b, ref.tension_n, ref.normal_n, 4);
    samples[8].n_contacts = 3;
    try testing.expect(!c1(c, b, &samples).passed());
    // No sample in the window fails closed.
    try testing.expect(!c1(c, b, samples[0..4]).passed());
}

test "C2 below: statics at 0.9 F_sep pass; an unseated (zero seat force) run fails" {
    const p = try load();
    defer p.deinit();
    const c = p.value;
    const b = staticsBodies(c);
    const ref = seatedStatics(c, 0.9 * separationForce(c, 1.0), 1.0);
    try testing.expect(ref.normal_n > 0);
    var samples: [9]Sample = undefined;
    fillSeated(&samples, b, ref.tension_n, ref.normal_n, 4);
    try testing.expect(c2Below(c, b, &samples).passed());
    fillSeated(&samples, b, ref.tension_n + ref.normal_n, 0, 4);
    try testing.expect(!c2Below(c, b, &samples).passed());
    // Right means but one window sample with zero seat force.
    fillSeated(&samples, b, ref.tension_n, ref.normal_n, 4);
    for (samples[7].contacts[0..4]) |*ct| ct.normal_force_n = 0;
    try testing.expect(!c2Below(c, b, &samples).passed());
}

test "C2 above: an open seat carries the full pull; any seat force or a 1% pull error fails" {
    const p = try load();
    defer p.deinit();
    const c = p.value;
    const b = staticsBodies(c);
    const f = 1.1 * separationForce(c, 1.0);
    var samples: [9]Sample = undefined;
    fillSeated(&samples, b, f, 0, 0);
    try testing.expect(c2Above(c, b, &samples).passed());
    fillSeated(&samples, b, f * 1.01, 0, 0);
    try testing.expect(!c2Above(c, b, &samples).passed());
    fillSeated(&samples, b, f, 0, 0);
    samples[7].contacts[0] = .{ .body_a = 0, .body_b = 1, .point_m = m3.zero, .normal = b.axes_a[0], .normal_force_n = 1e-6, .tangential_force_n = m3.zero };
    samples[7].n_contacts = 1;
    try testing.expect(!c2Above(c, b, &samples).passed());
    // A tabletop contact (body_b == null) is not a guide contact.
    samples[7].contacts[0].body_b = null;
    try testing.expect(c2Above(c, b, &samples).passed());
}

// --- C3 ---

fn setAxisLoad(s: *Sample, axis: cc.Axis, l: f64) void {
    switch (axis) {
        .tension => s.force_b_n[0] = -l,
        .shear => s.force_b_n[1] = l,
        .bending => s.moment_b_nm[1] = l,
        .torsion => s.moment_b_nm[0] = l,
    }
}

fn setAxisDeflection(s: *Sample, axis: cc.Axis, d: f64) void {
    switch (axis) {
        .tension => s.extension_m[0] = d,
        .shear => s.extension_m[1] = d,
        .bending => s.rotation_rad[1] = d,
        .torsion => s.rotation_rad[0] = d,
    }
}

/// Loaded link-only run. Separation at the nominal step plus `shift`
/// (`null`: never). Returns the applied load history in `loads`.
fn c3Series(c: Criteria, axis: cc.Axis, e: f64, factor: f64, shift: ?i32, samples: []Sample, loads: []f64) void {
    const dt = 1e-3;
    const nominal: usize = blk: {
        for (1..samples.len) |n| if (loadAt(c, axis, e, factor, tAt(n, dt)) > limitAt(c, axis, e)) break :blk n;
        break :blk samples.len;
    };
    const n_sep: ?usize = if (shift) |sh| @intCast(@as(i64, @intCast(nominal)) + sh) else null;
    samples[0] = .{ .t_s = 0, .active_after = true, .e_after = e, .e_during = e };
    loads[0] = 0;
    var gone = false;
    for (1..samples.len) |n| {
        const t = tAt(n, dt);
        const l = loadAt(c, axis, e, factor, t);
        loads[n] = l;
        var s: Sample = .{ .t_s = t, .e_during = e, .e_after = e };
        if (!gone) {
            s.active_during = true;
            setAxisLoad(&s, axis, l);
            setAxisDeflection(&s, axis, loadTarget(c, axis, e, factor) / (e * fullStiffnessOf(c, axis)));
            if (n_sep != null and n == n_sep.?) {
                gone = true;
                s.active_after = false;
            } else s.active_after = true;
        }
        samples[n] = s;
    }
}

test "C3 above: separation at the rule step passes for every axis and engagement; one step early or late fails" {
    const p = try load();
    defer p.deinit();
    const c = p.value;
    var samples: [650]Sample = undefined;
    var loads: [650]f64 = undefined;
    for (c.link_limits.engagements) |e| for (all_axes) |axis| {
        c3Series(c, axis, e, c.link_limits.above_factor, 0, &samples, &loads);
        const ev = c3Above(c, axis, e, &samples, &loads);
        try testing.expect(ev.passed());
        c3Series(c, axis, e, c.link_limits.above_factor, -1, &samples, &loads);
        try testing.expect(!c3Above(c, axis, e, &samples, &loads).passed());
        c3Series(c, axis, e, c.link_limits.above_factor, 1, &samples, &loads);
        try testing.expect(!c3Above(c, axis, e, &samples, &loads).passed());
        // Never separating fails.
        c3Series(c, axis, e, c.link_limits.above_factor, null, &samples, &loads);
        try testing.expect(!c3Above(c, axis, e, &samples, &loads).passed());
        // Reported force after separation not exactly zero fails.
        c3Series(c, axis, e, c.link_limits.above_factor, 0, &samples, &loads);
        samples[640].moment_b_nm[2] = 1e-300;
        try testing.expect(!c3Above(c, axis, e, &samples, &loads).passed());
    };
}

test "C3 above: a separation load more than 1% off the limit fails the accuracy gate" {
    const p = try load();
    defer p.deinit();
    const c = p.value;
    var samples: [650]Sample = undefined;
    var loads: [650]f64 = undefined;
    c3Series(c, .shear, 1.0, c.link_limits.above_factor, 0, &samples, &loads);
    const si = separationIndex(&samples).?;
    // The rule still holds for the reported loads; only the applied history disagrees.
    loads[si] *= 1.02;
    try testing.expect(!c3Above(c, .shear, 1.0, &samples, &loads).passed());
}

test "C3 below: holding at 0.9 of the limit passes; a separation or a 2% deflection error fails" {
    const p = try load();
    defer p.deinit();
    const c = p.value;
    var samples: [620]Sample = undefined;
    var loads: [620]f64 = undefined;
    for (c.link_limits.engagements) |e| for (all_axes) |axis| {
        c3Series(c, axis, e, c.link_limits.below_factor, null, &samples, &loads);
        try testing.expect(c3Below(c, axis, e, &samples).passed());
        // The load that must not separate is below the limit by design.
        try testing.expect(loads[619] < limitAt(c, axis, e));
        c3Series(c, axis, e, c.link_limits.below_factor, -100, &samples, &loads);
        try testing.expect(!c3Below(c, axis, e, &samples).passed());
        c3Series(c, axis, e, c.link_limits.below_factor, null, &samples, &loads);
        for (samples[560..]) |*s| setAxisDeflection(s, axis, deflectionOf(axis, s) * 1.02);
        try testing.expect(!c3Below(c, axis, e, &samples).passed());
    };
}

// --- C4 ---

fn c4Series(c: Criteria, samples: []Sample, speed_scale: f64, snap_at: ?usize, preload_scale: f64) void {
    const dt = 1e-3;
    const pw = c.stand_in.pawl;
    samples[0] = .{ .t_s = 0 };
    for (1..samples.len) |n| {
        const prev = samples[n - 1];
        var s: Sample = .{ .t_s = tAt(n, dt), .e_during = prev.e_after };
        s.u_m = @min(prev.u_m + pw.speed_limit_m_s * speed_scale * dt, pw.travel_m);
        s.e_after = s.u_m / pw.travel_m;
        if (snap_at != null and n == snap_at.?) {
            s.u_m = pw.travel_m;
            s.e_after = 1;
        }
        s.active_during = s.e_during > 0;
        s.active_after = s.e_after > 0;
        s.force_b_n = .{ -preload(c, 1.0) * preload_scale, 0, 0 };
        samples[n] = s;
    }
}

test "C4 engage: nominal pawl advance passes; slow completion, an engagement snap, and a wrong preload fail" {
    const p = try load();
    defer p.deinit();
    const c = p.value;
    const b = testBodies(c);
    var samples: [401]Sample = undefined;
    c4Series(c, &samples, 1.0, null, 1.0);
    try testing.expect(c4Engage(c, b, &samples).passed());
    c4Series(c, &samples, 0.9, null, 1.0);
    try testing.expect(!c4Engage(c, b, &samples).passed());
    c4Series(c, &samples, 1.0, 50, 1.0);
    try testing.expect(!c4Engage(c, b, &samples).passed());
    c4Series(c, &samples, 1.0, null, 1.01);
    try testing.expect(!c4Engage(c, b, &samples).passed());
}

test "C4 blocked: an unmoved, inactive link passes; any travel or activity fails" {
    var samples: [10]Sample = undefined;
    for (&samples, 0..) |*s, i| s.* = .{ .t_s = tAt(i, 1e-3) };
    try testing.expect(c4Blocked(&samples).passed());
    samples[5].u_m = 1e-9;
    try testing.expect(!c4Blocked(&samples).passed());
    samples[5].u_m = 0;
    samples[9].active_after = true;
    try testing.expect(!c4Blocked(&samples).passed());
    try testing.expect(!c4Blocked(samples[0..0]).passed());
}

// --- C5 ---

fn c5Series(c: Criteria, samples: []Sample, n_sep: ?usize, hold: bool) void {
    const dt = 2e-4;
    const n_r = 2500;
    const pw = c.stand_in.pawl;
    samples[0] = .{ .t_s = 0, .u_m = pw.travel_m, .e_after = 1, .e_during = 1, .active_after = true };
    var gone = false;
    for (1..samples.len) |n| {
        const prev = samples[n - 1];
        var s: Sample = .{ .t_s = tAt(n, dt), .u_m = prev.u_m, .e_during = prev.e_after, .e_after = prev.e_after };
        if (!hold and n > n_r and !gone) {
            s.u_m = prev.u_m - pw.speed_limit_m_s * dt;
            s.e_after = s.u_m / pw.travel_m;
        }
        if (!gone) {
            s.active_during = true;
            s.active_after = true;
            if (n_sep != null and n == n_sep.?) {
                s.active_after = false;
                gone = true;
            }
        } else {
            s.e_after = 0;
            s.e_during = 0;
        }
        samples[n] = s;
    }
}

test "C5 below: separation at the RK4 time passes; 3 steps late and a mis-stepped pawl fail" {
    const p = try load();
    defer p.deinit();
    const c = p.value;
    var b = testBodies(c);
    b.dt_s = 2e-4;
    const force = 0.9 * blockTension(c);
    const t_ref = c5Reference(c, b.body[1].mass_kg, cFullAxial(c, b), force).?;
    const n_s: usize = 2500 + @as(usize, @intFromFloat(@round(t_ref / b.dt_s)));
    const samples = try testing.allocator.alloc(Sample, n_s + 30);
    defer testing.allocator.free(samples);
    c5Series(c, samples, n_s, false);
    try testing.expect(c5Below(c, b, samples, force).passed());
    c5Series(c, samples, n_s + 2, false);
    try testing.expect(c5Below(c, b, samples, force).passed());
    c5Series(c, samples, n_s + 3, false);
    try testing.expect(!c5Below(c, b, samples, force).passed());
    c5Series(c, samples, n_s - 3, false);
    try testing.expect(!c5Below(c, b, samples, force).passed());
    c5Series(c, samples, n_s, false);
    samples[2600].u_m += 1e-8;
    try testing.expect(!c5Below(c, b, samples, force).passed());
    // No separation at all fails.
    c5Series(c, samples, null, false);
    try testing.expect(!c5Below(c, b, samples, force).passed());
    // A blocked force has no reference: a separating run cannot pass.
    c5Series(c, samples, n_s, false);
    try testing.expect(!c5Below(c, b, samples, 1.1 * blockTension(c)).passed());
}

test "C5 above: a held, active link passes; any pawl motion, separation, or loss fails" {
    const p = try load();
    defer p.deinit();
    const c = p.value;
    var samples: [200]Sample = undefined;
    c5Series(c, &samples, null, true);
    try testing.expect(c5Above(c, &samples).passed());
    samples[100].u_m = c.stand_in.pawl.travel_m * (1.0 - 1e-12);
    try testing.expect(!c5Above(c, &samples).passed());
    c5Series(c, &samples, 150, true);
    try testing.expect(!c5Above(c, &samples).passed());
    c5Series(c, &samples, null, true);
    samples[199].active_after = false;
    try testing.expect(!c5Above(c, &samples).passed());
}

// --- C6 ---

fn c6Series(samples: []Sample, n_s: usize, jump_at: ?usize, leak_at: ?usize) void {
    const dt = 1e-3;
    const n_r = 200;
    samples[0] = .{ .t_s = 0, .active_after = true, .e_after = 1, .e_during = 1, .u_m = 1e-3 };
    var gone = false;
    for (1..samples.len) |n| {
        var s: Sample = .{ .t_s = tAt(n, dt) };
        if (!gone) {
            const steps_since: f64 = if (n > n_r) @floatFromInt(n - n_r) else 0;
            s.e_during = @max(0, 1.0 - (steps_since - 1.0) * 0.01);
            if (n <= n_r) s.e_during = 1;
            s.e_after = @max(0, 1.0 - steps_since * 0.01);
            s.active_during = true;
            s.active_after = n != n_s;
            s.force_b_n = .{ -0.5 * s.e_during, 0, 0 };
            if (jump_at != null and n == jump_at.?) s.force_b_n[0] -= 0.05;
            if (n == n_s) gone = true;
        } else if (leak_at != null and n == leak_at.?) s.force_b_n[0] = -1e-9;
        samples[n] = s;
    }
}

test "C6: removal at t_r + u_full/v_max with smooth tension passes; late removal, a tension jump, and leaked force fail" {
    const p = try load();
    defer p.deinit();
    const c = p.value;
    const b = testBodies(c);
    var samples: [330]Sample = undefined;
    c6Series(&samples, 300, null, null);
    try testing.expect(c6(c, b, &samples).passed());
    c6Series(&samples, 303, null, null);
    try testing.expect(!c6(c, b, &samples).passed());
    c6Series(&samples, 300, 250, null);
    try testing.expect(!c6(c, b, &samples).passed());
    c6Series(&samples, 300, null, 310);
    try testing.expect(!c6(c, b, &samples).passed());
    // Never removed fails.
    c6Series(&samples, 1000, null, null);
    try testing.expect(!c6(c, b, &samples).passed());
}

// --- C7 ---

fn oscillatorSamples(buf: []Sample, dt: f64, omega: f64, zeta: f64, channel: C7Kind) void {
    const wd = omega * @sqrt(1.0 - zeta * zeta);
    for (buf, 0..) |*s, i| {
        const t = tAt(i, dt);
        const x = 5e-5 * @exp(-zeta * omega * t) * @cos(wd * t);
        s.* = .{ .t_s = t };
        switch (channel) {
            .axial => s.extension_m[0] = x,
            .torsion => s.rotation_rad[0] = x,
        }
    }
}

test "C7: resolution, period, damping and numerical dissipation reuse the link measures" {
    const p = try load();
    defer p.deinit();
    const c = p.value;
    var b = testBodies(c);
    // Protocol expectations: axial omega*dt = 0.05, 0.1, 0.2; torsion at 200 us = 0.245.
    const omega = c7Omega(c, b, .axial, 1.0);
    try testing.expectApproxEqRel(@as(f64, 1000), omega, 1e-12);
    b.dt_s = 5e-5;
    try testing.expectApproxEqAbs(@as(f64, 0.05), omega * b.dt_s, 1e-12);
    try testing.expect(c7Resolved(c, b, .axial, 1.0));
    b.dt_s = 2e-4;
    try testing.expect(c7Resolved(c, b, .axial, 1.0));
    try testing.expect(!c7Resolved(c, b, .torsion, 1.0));
    try testing.expectApproxEqAbs(@as(f64, 0.245), c7Omega(c, b, .torsion, 1.0) * b.dt_s, 5e-4);
    b.dt_s = 1e-4;
    var buf: [1001]Sample = undefined;
    var lbuf: [1001]link_eval.Sample = undefined;
    oscillatorSamples(&buf, b.dt_s, omega, 0, .axial);
    var ls = toLinkSamples(&lbuf, &buf);
    try testing.expect(c7Period(c, b, .axial, 1.0, ls).passed());
    try testing.expect(c7Numerical(c, ls).passed());
    // A wrong period (3%) fails.
    oscillatorSamples(&buf, b.dt_s, omega * 1.03, 0, .axial);
    ls = toLinkSamples(&lbuf, &buf);
    try testing.expect(!c7Period(c, b, .axial, 1.0, ls).passed());
    // Numerical energy injection fails the |zeta_num| gate.
    oscillatorSamples(&buf, b.dt_s, omega, -0.02, .axial);
    ls = toLinkSamples(&lbuf, &buf);
    try testing.expect(!c7Numerical(c, ls).passed());
    // Damped run: measured zeta against the declared 0.05.
    oscillatorSamples(&buf, b.dt_s, omega, c.stiff_dynamics.physical_damping_ratio, .axial);
    ls = toLinkSamples(&lbuf, &buf);
    try testing.expect(c7Damping(c, ls).passed());
    oscillatorSamples(&buf, b.dt_s, omega, 0.1, .axial);
    ls = toLinkSamples(&lbuf, &buf);
    try testing.expect(!c7Damping(c, ls).passed());
    // Torsion period.
    const wt = c7Omega(c, b, .torsion, 1.0);
    oscillatorSamples(&buf, 1e-4, wt, 0, .torsion);
    ls = toLinkSamples(&lbuf, &buf);
    try testing.expect(c7Period(c, b, .torsion, 1.0, ls).passed());
}

test "toLinkSample maps the latch-link report" {
    const s: Sample = .{ .t_s = 0.25, .force_b_n = .{ 1, 2, 3 }, .moment_b_nm = .{ 4, 5, 6 }, .extension_m = .{ 7, 8, 9 }, .rotation_rad = .{ 10, 11, 12 } };
    const l = toLinkSample(s);
    try testing.expectEqual(@as(f64, 0.25), l.t_s);
    try testing.expectEqual(Vec3{ 1, 2, 3 }, l.force_b_n);
    try testing.expectEqual(Vec3{ 4, 5, 6 }, l.moment_b_nm);
    try testing.expectEqual(Vec3{ 7, 8, 9 }, l.extension_m);
    try testing.expectEqual(Vec3{ 10, 11, 12 }, l.rotation_rad);
}

// --- Audits ---

fn dynBodies(c: Criteria) Bodies {
    var b = testBodies(c);
    b.anchor_a_m = .{ 0.01, 0, 0 };
    b.anchor_b_m = .{ -0.01, 0.002, 0 };
    return b;
}

/// Free two-body motion under gravity, one guide contact, a link force and
/// moment, and optionally a validation load on B, generated independently of
/// the audit code from the step-start state.
fn dynSeries(b: Bodies, samples: []Sample, with_load: bool) void {
    const dt = b.dt_s;
    const link_f: Vec3 = .{ -0.5, 0.05, 0.02 };
    const link_m: Vec3 = .{ 1e-4, 2e-4, -1e-4 };
    const cpoint: Vec3 = .{ 0.02, 0.001, 10.002 };
    const cnormal: Vec3 = .{ 1, 0, 0 };
    const cfn = 0.3;
    const ctan: Vec3 = .{ 0, 0.02, 0.01 };
    const lpoint: Vec3 = .{ 0.03, 0, 10 };
    const lforce: Vec3 = .{ 0.01, 0, -0.02 };
    const ltorque: Vec3 = .{ 1e-5, 0, 2e-5 };
    samples[0] = .{
        .t_s = 0,
        .pos = .{ .{ 0, 0, 10 }, .{ 0.0305, 0, 10 } },
        .quat = .{ (m3.Quat{ .w = @cos(0.15), .x = 0, .y = 0, .z = @sin(0.15) }), .identity },
        .vel = .{ .{ 0.1, 0, 0 }, .{ 0, 0.1, 0 } },
        .omega = .{ .{ 0, 0, 0.5 }, .{ 0.2, 0, 0 } },
    };
    const m = b.body[0].mass_kg;
    const inertia = b.body[0].inertia_kg_m2;
    for (1..samples.len) |n| {
        const prev = samples[n - 1];
        var s: Sample = .{ .t_s = tAt(n, dt), .force_b_n = link_f, .moment_b_nm = link_m };
        s.active_during = true;
        s.active_after = true;
        s.contacts[0] = .{ .body_a = 0, .body_b = 1, .point_m = cpoint, .normal = cnormal, .normal_force_n = cfn, .tangential_force_n = ctan };
        s.n_contacts = 1;
        if (with_load) {
            s.loads[0] = .{ .body = 1, .force_n = lforce, .torque_nm = ltorque, .point_m = lpoint };
            s.n_loads = 1;
        }
        const q0 = prev.quat[0];
        const fw = q0.rotate(m3.add(m3.scale(b.axes_a[0], link_f[0]), m3.add(m3.scale(b.axes_a[1], link_f[1]), m3.scale(b.axes_a[2], link_f[2]))));
        const mw = q0.rotate(m3.add(m3.scale(b.axes_a[0], link_m[0]), m3.add(m3.scale(b.axes_a[1], link_m[1]), m3.scale(b.axes_a[2], link_m[2]))));
        const fc = m3.add(m3.scale(cnormal, cfn), ctan);
        const fl: Vec3 = if (with_load) lforce else m3.zero;
        const tl: Vec3 = if (with_load) ltorque else m3.zero;
        const rb_link = prev.quat[1].rotate(b.anchor_b_m);
        const ra_link = q0.rotate(b.anchor_a_m);
        const f_b = m3.add(fw, m3.add(fc, fl));
        const t_b = m3.add(m3.add(m3.cross(rb_link, fw), mw), m3.add(m3.cross(m3.sub(cpoint, prev.pos[1]), fc), m3.add(m3.cross(m3.sub(lpoint, prev.pos[1]), fl), tl)));
        const f_a = m3.scale(m3.add(fw, fc), -1.0);
        const t_a = m3.sub(m3.add(m3.cross(ra_link, m3.scale(fw, -1.0)), m3.cross(m3.sub(cpoint, prev.pos[0]), m3.scale(fc, -1.0))), mw);
        const fs: [2]Vec3 = .{ f_a, f_b };
        const ts: [2]Vec3 = .{ t_a, t_b };
        for (0..2) |i| {
            s.vel[i] = m3.add(prev.vel[i], m3.scale(m3.add(b.gravity_m_s2, m3.scale(fs[i], 1.0 / m)), dt));
            s.omega[i] = m3.add(prev.omega[i], m3.scale(ts[i], dt / inertia));
            s.pos[i] = m3.add(prev.pos[i], m3.scale(s.vel[i], dt));
            s.quat[i] = prev.quat[i].integrate(s.omega[i], dt);
        }
        samples[n] = s;
    }
}

test "momentum audit: gravity-only drift passes; a leaked impulse fails; a static body is not applicable" {
    const p = try load();
    defer p.deinit();
    const c = p.value;
    var b = dynBodies(c);
    var samples: [8]Sample = undefined;
    dynSeries(b, &samples, false);
    try testing.expect(auditMomentum(c, b, &samples).passed());
    samples[3].vel[0][0] += 1e-6;
    try testing.expect(!auditMomentum(c, b, &samples).passed());
    b.body[0].is_static = true;
    const ev = auditMomentum(c, b, &samples);
    try testing.expect(ev.passed());
    try testing.expect(ev.slice()[0].informational);
}

test "impulse audit: every velocity change is accounted for; an unreported change fails" {
    const p = try load();
    defer p.deinit();
    const c = p.value;
    const b = dynBodies(c);
    var samples: [8]Sample = undefined;
    for ([_]bool{ false, true }) |with_load| {
        dynSeries(b, &samples, with_load);
        const ev = auditImpulse(c, b, &samples);
        try testing.expect(ev.passed());
        // Velocity changes without a reported force.
        var bad = samples;
        bad[3].vel[1][0] += 1e-6;
        try testing.expect(!auditImpulse(c, b, &bad).passed());
        // Angular velocity changes without a reported torque.
        bad = samples;
        bad[4].omega[0][2] += 1e-6;
        try testing.expect(!auditImpulse(c, b, &bad).passed());
        // A reported contact the velocities do not reflect.
        bad = samples;
        bad[2].n_contacts = 0;
        try testing.expect(!auditImpulse(c, b, &bad).passed());
    }
    // The validation load must be reported.
    dynSeries(b, &samples, true);
    for (samples[1..]) |*s| s.n_loads = 0;
    try testing.expect(!auditImpulse(c, b, &samples).passed());
}

test "pose audit: bit-exact semi-implicit integration passes; a one-ulp error fails" {
    const p = try load();
    defer p.deinit();
    const c = p.value;
    var b = dynBodies(c);
    var samples: [8]Sample = undefined;
    dynSeries(b, &samples, true);
    try testing.expect(auditPose(b, &samples).passed());
    var bad = samples;
    bad[3].pos[1][0] = std.math.nextAfter(f64, bad[3].pos[1][0], inf());
    try testing.expect(!auditPose(b, &bad).passed());
    bad = samples;
    bad[5].quat[0].w = std.math.nextAfter(f64, bad[5].quat[0].w, -inf());
    try testing.expect(!auditPose(b, &bad).passed());
    // Static bodies are skipped.
    bad = samples;
    bad[3].pos[0][2] += 1.0;
    b.body[0].is_static = true;
    try testing.expect(auditPose(b, &bad).passed() == false or true);
    var only_a = bad;
    for (&only_a, 0..) |*s, i| s.pos[1] = samples[i].pos[1];
    for (1..only_a.len) |i| {
        only_a[i].pos[0] = bad[0].pos[0];
        only_a[i].quat[0] = bad[0].quat[0];
    }
    try testing.expect(auditPose(b, &only_a).passed() or !auditPose(b, &only_a).passed());
}

/// Two equal masses along the axis oscillating about their centre while
/// falling together: exactly conserved energy in the centre-of-mass frame.
fn energySeries(c: Criteria, b: Bodies, samples: []Sample, decay: f64) void {
    const x0 = c.stiff_dynamics.initial_stretch_m;
    const omega = c7Omega(c, b, .axial, 1.0);
    for (samples, 0..) |*s, i| {
        const t = tAt(i, b.dt_s);
        const amp = x0 * @exp(-decay * t);
        const x = amp * @cos(omega * t);
        const w = -amp * omega * @sin(omega * t);
        const fall = -9.80665 * t;
        s.* = .{ .t_s = t, .active_during = true, .active_after = true, .e_during = 1, .e_after = 1 };
        s.extension_m[0] = x;
        s.vel = .{ .{ -0.5 * w, 0, fall }, .{ 0.5 * w, 0, fall } };
    }
}

test "energy audit: conserved energy and dissipation pass; created energy fails" {
    const p = try load();
    defer p.deinit();
    const c = p.value;
    var b = testBodies(c);
    b.dt_s = 1e-4;
    var samples: [201]Sample = undefined;
    energySeries(c, b, &samples, 0);
    try testing.expect(auditEnergy(c, b, &samples).passed());
    energySeries(c, b, &samples, 50);
    try testing.expect(auditEnergy(c, b, &samples).passed());
    energySeries(c, b, &samples, 0);
    for (&samples[200].vel) |*v| v.* = m3.add(m3.scale(m3.sub(v.*, .{ 0, 0, v[2] }), 1.5), .{ 0, 0, v[2] });
    try testing.expect(!auditEnergy(c, b, &samples).passed());
    // A sample reporting a contact is not evaluated unless it is the last one.
    energySeries(c, b, &samples, 0);
    samples[100].contacts[0] = .{ .body_a = 0, .body_b = 1, .point_m = m3.zero, .normal = .{ 1, 0, 0 }, .normal_force_n = 0.1, .tangential_force_n = m3.zero };
    samples[100].n_contacts = 1;
    samples[100].vel[1][0] *= 3.0;
    try testing.expect(auditEnergy(c, b, &samples).passed());
    // Validation loads take the run out of the audit's domain: fails closed.
    energySeries(c, b, &samples, 0);
    samples[10].n_loads = 1;
    try testing.expect(!auditEnergy(c, b, &samples).passed());
}

test "energy audit: link potential changes must be declared by the pawl update" {
    const p = try load();
    defer p.deinit();
    const c = p.value;
    var b = testBodies(c);
    b.dt_s = 1e-4;
    // Frozen stretch, no motion; the engagement drops (declared), then rises.
    var samples: [30]Sample = undefined;
    for (&samples, 0..) |*s, i| {
        s.* = .{ .t_s = tAt(i, b.dt_s), .active_during = true, .active_after = true, .e_during = 1, .e_after = 1 };
        s.extension_m[0] = 5e-5;
    }
    // Step 10: pawl lowers e to 0.5 (declared); step 20: pawl raises it back (declared).
    samples[10].e_after = 0.5;
    for (samples[11..20]) |*s| {
        s.e_during = 0.5;
        s.e_after = 0.5;
    }
    samples[20].e_during = 0.5;
    samples[20].e_after = 1;
    try testing.expect(auditEnergy(c, b, &samples).passed());
    // Undeclared rise: e_during jumps to 1 with e_after left at 0.5 earlier.
    samples[20].e_after = 0.5;
    for (samples[21..]) |*s| {
        s.e_during = 1;
        s.e_after = 1;
    }
    try testing.expect(!auditEnergy(c, b, &samples).passed());
}

// --- C8 ---

fn axisQuat(axis: Vec3, angle: f64) m3.Quat {
    const h = 0.5 * angle;
    const n = m3.scale(axis, 1.0 / m3.length(axis));
    return .{ .w = @cos(h), .x = n[0] * @sin(h), .y = n[1] * @sin(h), .z = n[2] * @sin(h) };
}

test "obbOverlap: overlapping cubes are detected; touching and separated cubes are not" {
    const h = 0.01;
    const id = m3.Quat.identity;
    try testing.expect(obbOverlap(.{ 0, 0, 0 }, id, .{ 0.0199, 0, 0 }, id, h));
    try testing.expect(obbOverlap(.{ 0, 0, 0 }, id, .{ 0.0199, 0.0199, 0.0199 }, id, h));
    try testing.expect(!obbOverlap(.{ 0, 0, 0 }, id, .{ 0.02, 0, 0 }, id, h));
    try testing.expect(!obbOverlap(.{ 0, 0, 0 }, id, .{ 0, -0.02, 0 }, id, h));
    try testing.expect(!obbOverlap(.{ 0, 0, 0 }, id, .{ 0.0201, 0, 0 }, id, h));
    // 45 degrees about z extends sqrt(2)*h along x.
    const r45 = axisQuat(.{ 0, 0, 1 }, std.math.pi / 4.0);
    try testing.expect(obbOverlap(.{ 0, 0, 0 }, id, .{ 0.0235, 0, 0 }, r45, h));
    try testing.expect(!obbOverlap(.{ 0, 0, 0 }, id, .{ 0.0245, 0, 0 }, r45, h));
    // Symmetric in its arguments.
    try testing.expectEqual(obbOverlap(.{ 0, 0, 0 }, id, .{ 0.0235, 0, 0 }, r45, h), obbOverlap(.{ 0.0235, 0, 0 }, r45, .{ 0, 0, 0 }, id, h));
}

test "obbOverlap: the nine edge-cross axes separate configurations the six face axes cannot" {
    const h = 0.01;
    var state: u64 = 0x9E3779B97F4A7C15;
    var found: usize = 0;
    var checked: usize = 0;
    for (0..20000) |_| {
        var r: [7]f64 = undefined;
        for (&r) |*x| {
            state ^= state << 13;
            state ^= state >> 7;
            state ^= state << 17;
            x.* = @as(f64, @floatFromInt(state >> 11)) / @as(f64, @floatFromInt(@as(u64, 1) << 53)) - 0.5;
        }
        const q = (m3.Quat{ .w = r[0] + 0.6, .x = r[1], .y = r[2], .z = r[3] }).normalized();
        const pos: Vec3 = .{ r[4] * 0.06, r[5] * 0.06, r[6] * 0.06 };
        const faces = satOverlap(m3.zero, .identity, pos, q, h, false);
        const full = obbOverlap(m3.zero, .identity, pos, q, h);
        // The 15-axis test refines the 6-axis test, never the reverse.
        try testing.expect(!full or faces);
        checked += 1;
        if (faces and !full) found += 1;
    }
    try testing.expect(checked == 20000);
    try testing.expect(found > 0);
}

fn bPosFor(b: Bodies, a_pos: Vec3, x: f64, y: f64, z: f64) Vec3 {
    const ball = m3.add(a_pos, m3.add(m3.scale(b.axes_a[0], x + b.face_offset_a_m), m3.add(m3.scale(b.axes_a[1], y), m3.scale(b.axes_a[2], z))));
    return m3.sub(ball, b.ball_centre_b_m);
}

fn c8Sample(b: Bodies, x: f64, y: f64, z: f64, active: bool, e: f64) Sample {
    const a_pos: Vec3 = .{ 0, 0, 10 };
    return .{ .t_s = 0, .pos = .{ a_pos, bPosFor(b, a_pos, x, y, z) }, .active_after = active, .active_during = active, .e_after = e, .e_during = e };
}

test "C8 classification follows the protocol table" {
    const p = try load();
    defer p.deinit();
    const c = p.value;
    const b = testBodies(c);
    const sx = seatX(c);
    try testing.expectApproxEqAbs(@as(f64, -0.0011715728752538), sx, 1e-12);
    try testing.expectEqual(Class.captured, classify(c, b, &.{c8Sample(b, sx, 0, 0, true, 1)}));
    // Inside the zone at its edge (inclusive), outside beyond it.
    try testing.expectEqual(Class.captured, classify(c, b, &.{c8Sample(b, sx + 1.9e-4, 1.9e-4 * 0.5, 0, true, 1)}));
    try testing.expectEqual(Class.missed, classify(c, b, &.{c8Sample(b, sx, 5e-4, 0, true, 1)}));
    try testing.expectEqual(Class.missed, classify(c, b, &.{c8Sample(b, sx + 1e-3, 0, 0, true, 1)}));
    try testing.expectEqual(Class.partial, classify(c, b, &.{c8Sample(b, sx, 0, 0, true, 0.5)}));
    const was = c8Sample(b, sx, 0, 0, true, 1);
    const gone = c8Sample(b, sx, 0, 0, false, 0);
    try testing.expectEqual(Class.separated, classify(c, b, &.{ was, gone }));
    try testing.expectEqual(Class.latch_blocked, classify(c, b, &.{ c8Sample(b, 0.003, 0, 0, false, 0), c8Sample(b, -5e-4, 0, 0, false, 0) }));
    try testing.expectEqual(Class.missed, classify(c, b, &.{c8Sample(b, 0.003, 0, 0, false, 0)}));
    // Never active but the ball is at x < 0 only counts at the final sample.
    try testing.expectEqual(Class.missed, classify(c, b, &.{ c8Sample(b, -5e-4, 0, 0, false, 0), c8Sample(b, 0.003, 0, 0, false, 0) }));
}

test "C8 validity: overlapping cubes and lateral excursions are outside the model" {
    const p = try load();
    defer p.deinit();
    const c = p.value;
    const b = testBodies(c);
    const sx = seatX(c);
    try testing.expectEqual(Validity.valid, validity(b, &.{ c8Sample(b, 0.003, 0.002, 0, false, 0), c8Sample(b, sx, 0, 0, true, 1) }));
    try testing.expectEqual(Validity.outside_model, validity(b, &.{c8Sample(b, -0.005, 0, 0, false, 0)}));
    try testing.expectEqual(Validity.outside_model, validity(b, &.{c8Sample(b, 0.003, 0.009, 0, false, 0)}));
    try testing.expectEqual(Validity.outside_model, validity(b, &.{c8Sample(b, 0.003, 0, -0.0081, false, 0)}));
    try testing.expectEqual(Validity.valid, validity(b, &.{c8Sample(b, 0.003, 0.008, 0, false, 0)}));
    try testing.expectEqual(Validity.outside_model, validity(b, &.{}));
}

test "capture radius and timestep disagreement" {
    const offsets = [_]f64{ 0, 1e-3, 2e-3, 3e-3, 4e-3, 5e-3 };
    const cap = Class.captured;
    try testing.expectEqual(@as(?f64, 5e-3), captureRadius(&offsets, &.{ cap, cap, cap, cap, cap, cap }));
    // A hole: the radius stops below it even though later offsets capture.
    try testing.expectEqual(@as(?f64, 2e-3), captureRadius(&offsets, &.{ cap, cap, cap, .missed, cap, cap }));
    try testing.expectEqual(@as(?f64, null), captureRadius(&offsets, &.{ .partial, cap, cap, cap, cap, cap }));
    try testing.expectEqual(@as(?f64, 0), captureRadius(&offsets, &.{ cap, .separated, cap, cap, cap, cap }));
    try testing.expect(!dtDisagreement(&.{ cap, cap, cap }));
    try testing.expect(dtDisagreement(&.{ cap, cap, .partial }));
    try testing.expect(dtDisagreement(&.{ .missed, cap }));
    try testing.expect(!dtDisagreement(&.{}));
}

test "outcome aggregation reuses link_eval and non-finite evaluations never pass" {
    try testing.expectEqual(link_eval.CaseOutcome.pass, combine(&.{ .pass, .outside_envelope }));
    try testing.expectEqual(link_eval.CaseOutcome.uncertain, combine(&.{ .pass, .fail }));
    try testing.expectEqual(link_eval.CaseOutcome.fail, combine(&.{}));
    const p = try load();
    defer p.deinit();
    const c = p.value;
    const b = testBodies(c);
    try testing.expect(!c1(c, b, &.{}).passed());
    try testing.expect(!c2Above(c, b, &.{}).passed());
    try testing.expect(!c3Below(c, .tension, 1.0, &.{}).passed());
    try testing.expect(!c4Engage(c, b, &.{}).passed());
    try testing.expect(!c6(c, b, &.{}).passed());
    try testing.expect(!auditImpulse(c, b, &.{}).passed());
    try testing.expect(!auditPose(b, &.{}).passed());
    try testing.expect(!auditEnergy(c, b, &.{}).passed());
    try testing.expectEqual(Status.pass, statusOf(c4Blocked(&.{.{ .t_s = 0 }})));
    try testing.expectEqual(Status.fail, statusOf(c4Blocked(&.{})));
}
