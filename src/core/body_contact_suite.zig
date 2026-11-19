//! Runs the body-body contact fixture-validation criteria v1 against the rigid
//! backend (Q76, Q77; `docs/validation/body-contact-v1-protocol.md`). Cases
//! BB1-BB5, BB7, BB8 run at every (friction pair x physics step) combination,
//! BB6 once, BB9 replays every run. Results are always labeled `fixture` and
//! qualify box-box contact only within the declared conditions.

const std = @import("std");
const m3 = @import("math3.zig");
const analytic = @import("analytic.zig");
const bcc = @import("body_contact_criteria.zig");
const bce = @import("body_contact_eval.zig");
const crit = @import("criteria.zig");
const fe = @import("fixture_eval.zig");
const fs = @import("fixture_suite.zig");
const rigid = @import("rigid.zig");
const box_contact = @import("box_contact.zig");
const backend = @import("backend.zig");
const canonical = @import("canonical.zig");
const time = @import("time.zig");

pub const protocol_revision: u32 = 1;

pub const SubRun = fs.SubRun;
pub const Combination = fs.Combination;
pub const CaseReport = fs.CaseReport;

pub const Report = struct {
    schema_version: u32 = 1,
    run_class: []const u8 = "fixture_validation",
    label: []const u8 = "fixture",
    criteria_path: []const u8 = "criteria/fixture-validation/body-contact-v2.json",
    criteria_sha256: []const u8 = bcc.v2_sha256,
    protocol: []const u8 = "docs/validation/body-contact-v1-protocol.md",
    protocol_revision: u32 = protocol_revision,
    settle_s: f64,
    solver_name: []const u8,
    solver_version: []const u8,
    solver_settings: rigid.Settings,
    cases: []const CaseReport,
};

const Ctx = struct {
    arena: std.mem.Allocator,
    scratch: std.mem.Allocator,
    c: bcc.Criteria,
    g: f64,
    unit: time.TimeUnit,
};

fn stepsFor(ctx: Ctx, duration_s: f64, step_ticks: u64) !u64 {
    const ticks_f = duration_s * @as(f64, @floatFromInt(ctx.unit.denominator)) / @as(f64, @floatFromInt(ctx.unit.numerator));
    const ticks: u64 = @intFromFloat(@round(ticks_f));
    if (@as(f64, @floatFromInt(ticks)) != ticks_f or ticks % step_ticks != 0) return error.DurationNotWholeSteps;
    return ticks / step_ticks;
}

fn fixtureOf(ctx: Ctx, id: []const u8) bcc.Fixture {
    return bcc.fixtureById(ctx.c, id) orelse unreachable; // validate guarantees resolution
}

fn critFixture(f: bcc.Fixture) crit.Fixture {
    return .{ .id = f.id, .shape = .cuboid, .mass_distribution = .uniform, .size_m = f.size_m, .mass_kg = f.mass_kg orelse 0 };
}

// --- Rigid transform (BB7) ---

const Xf = struct {
    r: [3][3]f64,
    q: m3.Quat,
    t: m3.Vec3,

    const identity: Xf = .{ .r = .{ .{ 1, 0, 0 }, .{ 0, 1, 0 }, .{ 0, 0, 1 } }, .q = .identity, .t = m3.zero };

    fn dir(self: Xf, v: m3.Vec3) m3.Vec3 {
        return .{
            self.r[0][0] * v[0] + self.r[0][1] * v[1] + self.r[0][2] * v[2],
            self.r[1][0] * v[0] + self.r[1][1] * v[1] + self.r[1][2] * v[2],
            self.r[2][0] * v[0] + self.r[2][1] * v[1] + self.r[2][2] * v[2],
        };
    }

    fn point(self: Xf, p: m3.Vec3) m3.Vec3 {
        return m3.add(self.dir(p), self.t);
    }
};

/// The BB7 transform, constructed from the exact fractions (one division each).
fn transformOf(c: bcc.Criteria) !Xf {
    const t = c.BB7.transform;
    var r: [3][3]f64 = undefined;
    for (0..3) |i| for (0..3) |j| {
        r[i][j] = try bcc.fraction(t.rotation_matrix_exact_rows[i][j]);
    };
    const tr = r[0][0] + r[1][1] + r[2][2];
    if (!(tr > 0)) return error.TransformNotRotation;
    const s = @sqrt(1.0 + tr) * 2.0;
    const q = (m3.Quat{ .w = s / 4.0, .x = (r[2][1] - r[1][2]) / s, .y = (r[0][2] - r[2][0]) / s, .z = (r[1][0] - r[0][1]) / s }).normalized();
    return .{ .r = r, .q = q, .t = t.translation_m };
}

// --- Simulation ---

const Load = union(enum) {
    none,
    /// World-frame force at the centre of mass of body 1.
    com_world: m3.Vec3,
    /// Body-frame force at a body-frame point of body 1.
    body: struct { force: m3.Vec3, point: m3.Vec3 },
};

const Scene = struct {
    b0: rigid.Body,
    b1: rigid.Body,
    gravity: m3.Vec3,
    tabletop: bool = true,
    settle: bool,
    duration_s: f64,
    velocity_after_settle: m3.Vec3 = m3.zero,
    load: Load = .none,
};

fn blockAt(f: bcc.Fixture, centre: m3.Vec3, xf: Xf) rigid.Body {
    var b = rigid.cuboid(f.mass_kg.?, f.size_m, 0);
    b.position_m = xf.point(centre);
    b.orientation = xf.q;
    return b;
}

fn slabAt(f: bcc.Fixture, xf: Xf) rigid.Body {
    var b = rigid.staticCuboid(f.size_m, xf.point(.{ 0, 0, f.size_m[2] / 2.0 }));
    b.orientation = xf.q;
    return b;
}

fn bodyState(b: rigid.Body) bce.BodyState {
    return .{ .position_m = b.position_m, .orientation = b.orientation, .velocity_m_s = b.velocity_m_s, .angular_velocity_rad_s = b.angular_velocity_rad_s };
}

fn sample(w: *rigid.World, t: f64, h: f64, stepped: bool) bce.Sample {
    var s: bce.Sample = .{ .t_s = t, .bodies = .{ bodyState(w.bodies.items[0]), bodyState(w.bodies.items[1]) } };
    if (!stepped) return s;
    var bb_cop = m3.zero;
    var tb_cop = m3.zero;
    var tan_imp = m3.zero;
    for (w.reports.items) |r| {
        if (r.body_b) |bi| {
            s.bb.rows += 1;
            s.bb.normal_force_sum_n += r.normal_force_n;
            s.bb.tangential_force_sum_n = m3.add(s.bb.tangential_force_sum_n, r.tangential_force_n);
            bb_cop = m3.add(bb_cop, m3.scale(r.world_point_m, r.normal_force_n));
            s.bb.max_penetration_m = @max(s.bb.max_penetration_m, r.penetration_m);
            const imp = m3.scale(m3.add(m3.scale(r.world_normal, r.normal_force_n), r.tangential_force_n), h);
            s.reported_n_s[bi] = m3.add(s.reported_n_s[bi], imp);
            s.reported_n_s[r.body_a] = m3.sub(s.reported_n_s[r.body_a], imp);
            tan_imp = m3.add(tan_imp, m3.scale(r.tangential_force_n, h));
        } else {
            s.table.rows += 1;
            s.table.normal_force_sum_n += r.normal_force_n;
            s.table.tangential_force_sum_n = m3.add(s.table.tangential_force_sum_n, r.tangential_force_n);
            tb_cop = m3.add(tb_cop, m3.scale(r.world_point_m, r.normal_force_n));
            s.table.max_penetration_m = @max(s.table.max_penetration_m, -r.world_point_m[2]);
        }
    }
    s.bb.tangential_impulse_n_s = m3.length(tan_imp);
    if (s.bb.normal_force_sum_n > 0) s.bb.center_of_pressure_m = m3.scale(bb_cop, 1.0 / s.bb.normal_force_sum_n);
    if (s.table.normal_force_sum_n > 0) s.table.center_of_pressure_m = m3.scale(tb_cop, 1.0 / s.table.normal_force_sum_n);
    if (w.bb_applied.items.len >= 2) s.applied_n_s = .{ w.bb_applied.items[0], w.bb_applied.items[1] };
    return s;
}

const Trace = struct { samples: []bce.Sample, hash: []const u8, steps: u64, dt: f64, final: [2]rigid.Body };

fn simulate(ctx: Ctx, scene: Scene, fr: crit.FrictionPair, step_ticks: u64) !Trace {
    var world: rigid.World = .{
        .gpa = ctx.scratch,
        .settings = fs.protocol_settings,
        .friction = .{ .mu_static = fr.mu_static, .mu_kinetic = fr.mu_kinetic },
        .gravity_m_s2 = scene.gravity,
        .allow_static_bodies = true,
        .body_contact = true,
        .tabletop_contact = scene.tabletop,
    };
    defer world.deinit();
    _ = try world.addBody(scene.b0);
    _ = try world.addBody(scene.b1);
    const n = try stepsFor(ctx, scene.duration_s, step_ticks);
    const dt = ctx.unit.seconds(.{ .ticks = step_ticks });
    if (scene.settle) {
        const pre = try stepsFor(ctx, ctx.c.settle.duration_s.value, step_ticks);
        for (0..pre) |_| try world.step(dt, .{});
    }
    world.bodies.items[1].velocity_m_s = m3.add(world.bodies.items[1].velocity_m_s, scene.velocity_after_settle);
    const samples = try ctx.scratch.alloc(bce.Sample, n + 1);
    samples[0] = sample(&world, 0, dt, false);
    var loads: [1]backend.AppliedLoad = undefined;
    for (1..n + 1) |i| {
        const b = world.bodies.items[1];
        const inputs: backend.StepInputs = switch (scene.load) {
            .none => .{},
            .com_world => |f| blk: {
                loads[0] = .{ .body_index = 1, .world_force_n = f, .world_torque_nm = m3.zero, .world_point_m = b.position_m };
                break :blk .{ .validation_loads = &loads };
            },
            .body => |l| blk: {
                loads[0] = .{ .body_index = 1, .world_force_n = b.orientation.rotate(l.force), .world_torque_nm = m3.zero, .world_point_m = m3.add(b.position_m, b.orientation.rotate(l.point)) };
                break :blk .{ .validation_loads = &loads };
            },
        };
        try world.step(dt, inputs);
        samples[i] = sample(&world, ctx.unit.seconds(.{ .ticks = i * step_ticks }), dt, true);
    }
    var sink: canonical.BufferSink = .{ .gpa = ctx.scratch };
    defer sink.deinit();
    try world.encodeState(sink.encoder());
    var digest: [32]u8 = undefined;
    std.crypto.hash.sha2.Sha256.hash(sink.list.items, &digest, .{});
    const hex = std.fmt.bytesToHex(digest, .lower);
    return .{ .samples = samples, .hash = try ctx.arena.dupe(u8, &hex), .steps = n, .dt = dt, .final = .{ world.bodies.items[0], world.bodies.items[1] } };
}

fn subRun(_: Ctx, name: []const u8, steps: u64, hash: []const u8, list: bce.List) !SubRun {
    return .{ .name = name, .steps = steps, .final_state_sha256 = hash, .metrics = list.items.items, .passed = list.passed() };
}

fn gravityDown(ctx: Ctx, xf: Xf) m3.Vec3 {
    return xf.dir(m3.scale(ctx.c.gravity.direction_world, ctx.g));
}

// --- Cases ---

const CaseKind = enum { bb1, bb2, bb3, bb4, bb5, bb7, bb8 };

fn restCase(id: []const u8, duration: f64, window: f64, nf: f64, tan: f64, cop: f64, dt: f64, dr: f64, pen: f64) crit.RestCase {
    return .{ .id = id, .fixture = "", .duration_s = duration, .window_start_s = window, .normal_force_rel_tol = nf, .tangential_force_max_rel_weight = tan, .center_of_pressure_abs_tol_m = cop, .drift_translation_abs_tol_m = dt, .drift_rotation_abs_tol_rad = dr, .max_penetration_m = pen };
}

fn bb1(ctx: Ctx, fr: crit.FrictionPair, st: u64, out: *std.ArrayList(SubRun)) !void {
    const b = ctx.c.BB1;
    const fb = fixtureOf(ctx, b.fixtures.bottom);
    const ft = fixtureOf(ctx, b.fixtures.top);
    const tr = try simulate(ctx, .{
        .b0 = blockAt(fb, b.poses.bottom_centre_m, .identity),
        .b1 = blockAt(ft, b.poses.top_centre_m, .identity),
        .gravity = gravityDown(ctx, .identity),
        .settle = true,
        .duration_s = b.duration_s.value,
    }, fr, st);
    const m = b.metrics;
    var list: bce.List = .{};
    const top_c = restCase("BB1", b.duration_s.value, b.window_start_s.value, m.inter_block_normal_force_rel_tol.value, m.tangential_force_max_rel_weight.value, m.center_of_pressure_abs_tol_m.value, m.drift_translation_abs_tol_m.value, m.drift_rotation_abs_tol_rad.value, m.max_penetration_m.value);
    try list.addFrom(ctx.arena, "inter_block.", fe.rest(top_c, critFixture(ft), ctx.g, try bce.evalSamples(ctx.scratch, tr.samples, 1, .bb)));
    var both = critFixture(fb);
    both.mass_kg += critFixture(ft).mass_kg;
    var tab_c = top_c;
    tab_c.normal_force_rel_tol = m.table_normal_force_rel_tol.value;
    try list.addFrom(ctx.arena, "table.", fe.rest(tab_c, both, ctx.g, try bce.evalSamples(ctx.scratch, tr.samples, 0, .table)));
    try list.add(ctx.arena, bce.newtonThirdLaw(tr.samples, m.newton_third_law_rel_tol.value));
    try out.append(ctx.arena, try subRun(ctx, "stacked_rest", tr.steps, tr.hash, list));
}

fn frictionCase(b: bcc.Bb2) crit.FrictionThresholdCase {
    return .{
        .id = b.id,
        .fixture = b.fixtures.top,
        .application = .center_of_mass,
        .direction_world = b.direction_world.value,
        .below_factor = b.below_factor.value,
        .above_factor = b.above_factor.value,
        .duration_s = b.below.duration_s.value,
        .below_max_displacement_m = b.below.max_displacement_m.value,
        .below_balance_window_start_s = b.below.balance_window_start_s.value,
        .below_balance_rel_tol = b.below.balance_rel_tol.value,
        .above_accel_window_start_s = b.above.accel_window_start_s.value,
        .above_accel_window_end_s = b.above.accel_window_end_s.value,
        .above_accel_rel_tol = b.above.accel_rel_tol.value,
        .max_penetration_m = b.below.max_penetration_m.value,
    };
}

fn slabScene(ctx: Ctx, bottom: []const u8, top: []const u8, top_centre: m3.Vec3, xf: Xf, duration_s: f64) Scene {
    return .{
        .b0 = slabAt(fixtureOf(ctx, bottom), xf),
        .b1 = blockAt(fixtureOf(ctx, top), top_centre, xf),
        .gravity = gravityDown(ctx, xf),
        .settle = true,
        .duration_s = duration_s,
    };
}

fn bb2(ctx: Ctx, fr: crit.FrictionPair, st: u64, out: *std.ArrayList(SubRun)) !void {
    const b = ctx.c.BB2;
    const f = fixtureOf(ctx, b.fixtures.top);
    const slab = fixtureOf(ctx, b.fixtures.bottom);
    const case = frictionCase(b);
    const threshold = analytic.slidingThreshold(f.mass_kg.?, ctx.g, fr.mu_static);
    const dir = b.direction_world.value;

    var sc = slabScene(ctx, b.fixtures.bottom, b.fixtures.top, b.poses.top_centre_m, .identity, b.below.duration_s.value);
    const below = b.below_factor.value * threshold;
    sc.load = .{ .com_world = m3.scale(dir, below) };
    const rb = try simulate(ctx, sc, fr, st);
    var lb: bce.List = .{};
    try lb.addFrom(ctx.arena, "", fe.frictionBelow(case, below, try bce.evalSamples(ctx.scratch, rb.samples, 1, .bb)));
    try out.append(ctx.arena, try subRun(ctx, "below_threshold", rb.steps, rb.hash, lb));

    sc = slabScene(ctx, b.fixtures.bottom, b.fixtures.top, b.poses.top_centre_m, .identity, b.above.duration_s.value);
    const above = b.above_factor.value * threshold;
    sc.load = .{ .com_world = m3.scale(dir, above) };
    const ra = try simulate(ctx, sc, fr, st);
    var la: bce.List = .{};
    var ac = case;
    ac.max_penetration_m = b.above.max_penetration_m.value;
    try la.addFrom(ctx.arena, "", fe.frictionAbove(ac, analytic.slidingAcceleration(f.mass_kg.?, ctx.g, fr.mu_kinetic, above), try bce.evalSamples(ctx.scratch, ra.samples, 1, .bb)));
    try la.add(ctx.arena, bce.staysOnSlab(ra.samples, m3.scale(slab.size_m, 0.5), m3.scale(f.size_m, 0.5)));
    try out.append(ctx.arena, try subRun(ctx, "above_threshold", ra.steps, ra.hash, la));
}

fn bb3(ctx: Ctx, fr: crit.FrictionPair, st: u64, out: *std.ArrayList(SubRun)) !void {
    const b = ctx.c.BB3;
    const f = fixtureOf(ctx, b.fixtures.top);
    const slab = fixtureOf(ctx, b.fixtures.bottom);
    var sc = slabScene(ctx, b.fixtures.bottom, b.fixtures.top, b.poses.top_centre_m, .identity, b.duration_s.value);
    sc.velocity_after_settle = m3.scale(b.direction_world.value, b.initial_speed_m_s.value);
    const tr = try simulate(ctx, sc, fr, st);
    const case: crit.SlideToStopCase = .{
        .id = b.id,
        .fixture = b.fixtures.top,
        .initial_speed_m_s = b.initial_speed_m_s.value,
        .direction_world = b.direction_world.value,
        .duration_s = b.duration_s.value,
        .stop_speed_threshold_m_s = b.stop_speed_threshold_m_s.value,
        .stop_time_tol_steps = b.stop_time_tol_steps.value,
        .stop_distance_rel_tol = b.stop_distance_rel_tol.value,
        .stop_distance_tol_steps = b.stop_distance_tol_steps.value,
        .post_stop_drift_abs_tol_m = b.post_stop_drift_abs_tol_m.value,
    };
    var list: bce.List = .{};
    try list.addFrom(ctx.arena, "", fe.slideToStop(case, critFixture(f), ctx.g, fr.mu_kinetic, tr.dt, try bce.evalSamples(ctx.scratch, tr.samples, 1, .bb)));
    try list.add(ctx.arena, bce.staysOnSlab(tr.samples, m3.scale(slab.size_m, 0.5), m3.scale(f.size_m, 0.5)));
    try out.append(ctx.arena, try subRun(ctx, "slide_to_stop", tr.steps, tr.hash, list));
}

fn bb4(ctx: Ctx, fr: crit.FrictionPair, st: u64, out: *std.ArrayList(SubRun)) !void {
    const b = ctx.c.BB4;
    const f = fixtureOf(ctx, b.fixtures.top);
    const slab = fixtureOf(ctx, b.fixtures.bottom);
    const slab_top = slab.size_m[2];
    const half_t = f.size_m[2] / 2.0;
    const centre: m3.Vec3 = .{ b.poses.top_centre_xy_m[0], b.poses.top_centre_xy_m[1], slab_top + b.poses.top_bottom_face_height_above_slab_top_m.value + half_t };
    var sc = slabScene(ctx, b.fixtures.bottom, b.fixtures.top, centre, .identity, b.duration_s.value);
    sc.settle = false;
    var body1 = sc.b1;
    body1.velocity_m_s = b.poses.initial_velocity;
    sc.b1 = body1;
    const tr = try simulate(ctx, sc, fr, st);
    var list: bce.List = .{};
    const m = b.rest_state_metrics;
    const rc = restCase("BB4", b.duration_s.value, b.rest_window_start_s.value, m.normal_force_rel_tol.value, m.tangential_force_max_rel_weight.value, m.center_of_pressure_abs_tol_m.value, m.drift_translation_abs_tol_m.value, m.drift_rotation_abs_tol_rad.value, b.peak_penetration.rest_max_penetration_m.value);
    const all = try bce.evalSamples(ctx.scratch, tr.samples, 1, .bb);
    var first_rest: usize = 0;
    while (first_rest < all.len and all[first_rest].t_s < b.rest_window_start_s.value) first_rest += 1;
    try list.addFrom(ctx.arena, "rest.", fe.rest(rc, critFixture(f), ctx.g, all[first_rest..]));
    try list.add(ctx.arena, .{ .name = "peak_penetration_m", .value = bce.maxBbPenetration(tr.samples), .limit = b.peak_penetration.max_penetration_m.value });
    try bce.freeFlight(ctx.arena, &list, tr.samples, slab_top, half_t, b.peak_penetration.max_penetration_m.value);
    try out.append(ctx.arena, try subRun(ctx, "drop", tr.steps, tr.hash, list));
}

fn bb5(ctx: Ctx, fr: crit.FrictionPair, st: u64, out: *std.ArrayList(SubRun)) !void {
    const b = ctx.c.BB5;
    const f = fixtureOf(ctx, b.fixtures.top);
    const case: crit.TippingCase = .{
        .id = b.id,
        .fixture = b.fixtures.top,
        .force_frame = .body,
        .force_direction_body = b.force_direction_body.value,
        .application_point_body_m = b.application_point_body_m.value,
        .below_factor = b.below_factor.value,
        .above_factor = b.above_factor.value,
        .duration_s = b.duration_s.value,
        .below_max_tilt_rad = b.below_max_tilt_rad.value,
        .above_min_tilt_rad = b.above_min_tilt_rad.value,
        .no_slip_until_tilt_rad = b.no_slip_until_tilt_rad.value,
        .pivot_slip_abs_tol_m = b.pivot_slip_abs_tol_m.value,
    };
    const h = b.application_point_body_m.value[2] + f.size_m[2] / 2.0;
    const threshold = analytic.tippingThreshold(f.mass_kg.?, ctx.g, f.size_m[0] / 2.0, h);
    inline for (.{ .{ "below_threshold", false }, .{ "above_threshold", true } }) |variant| {
        var sc = slabScene(ctx, b.fixtures.bottom, b.fixtures.top, b.poses.top_centre_m, .identity, b.duration_s.value);
        const factor = if (variant[1]) b.above_factor.value else b.below_factor.value;
        sc.load = .{ .body = .{ .force = m3.scale(b.force_direction_body.value, factor * threshold), .point = b.application_point_body_m.value } };
        const tr = try simulate(ctx, sc, fr, st);
        const es = try bce.evalSamples(ctx.scratch, tr.samples, 1, .bb);
        var list: bce.List = .{};
        try list.addFrom(ctx.arena, "", if (variant[1]) fe.tippingAbove(case, critFixture(f), es) else fe.tippingBelow(case, es));
        try out.append(ctx.arena, try subRun(ctx, variant[0], tr.steps, tr.hash, list));
    }
}

fn bb7(ctx: Ctx, fr: crit.FrictionPair, st: u64, out: *std.ArrayList(SubRun)) !void {
    const b = ctx.c.BB7;
    const xf = try transformOf(ctx.c);
    const tol: bce.Bb7Tol = .{ .rel_tol = b.rel_tol.value, .abs_floor = b.abs_floor.value, .step_index_tol = b.stop_step_index_tol.value };
    const b2 = ctx.c.BB2;
    const b3 = ctx.c.BB3;
    const f = fixtureOf(ctx, b2.fixtures.top);
    // S1: rest of the block on the slab (BB1 rest metrics definition).
    {
        const s = b.scenes[0];
        const dur = s.duration_s.value;
        const ws = s.window_start_s.?.value;
        const id = try runPair(ctx, slabScene(ctx, b2.fixtures.bottom, b2.fixtures.top, b2.poses.top_centre_m, .identity, dur), fr, st);
        const tf = try runPair(ctx, slabScene(ctx, b2.fixtures.bottom, b2.fixtures.top, b2.poses.top_centre_m, xf, dur), fr, st);
        var list: bce.List = .{};
        try bce.compareS1(ctx.arena, &list, s.id, bce.s1Quantities(tf.samples, ws, dur), bce.s1Quantities(id.samples, ws, dur), tol);
        try out.append(ctx.arena, try subRun(ctx, "S1_identity_vs_transformed", id.steps, id.hash, list));
        try out.append(ctx.arena, .{ .name = "S1_transformed_run", .steps = tf.steps, .final_state_sha256 = tf.hash, .metrics = &.{}, .passed = true });
    }
    // S3: slide to a stop on the slab.
    {
        const s = b.scenes[1];
        const dur = s.duration_s.value;
        const speed = b3.initial_speed_m_s.value;
        const slide: m3.Vec3 = b3.direction_world.value;
        var si = slabScene(ctx, b3.fixtures.bottom, b3.fixtures.top, b3.poses.top_centre_m, .identity, dur);
        si.velocity_after_settle = m3.scale(xf_identity_dir(slide), speed);
        var sx = slabScene(ctx, b3.fixtures.bottom, b3.fixtures.top, b3.poses.top_centre_m, xf, dur);
        sx.velocity_after_settle = m3.scale(xf.dir(slide), speed);
        const id = try runPair(ctx, si, fr, st);
        const tf = try runPair(ctx, sx, fr, st);
        const half = f.size_m[2] / 2.0;
        const thr = b3.stop_speed_threshold_m_s.value;
        var list: bce.List = .{};
        try bce.compareS3(ctx.arena, &list, s.id, bce.s3Quantities(tf.samples, half, thr, xf.dir(slide)), bce.s3Quantities(id.samples, half, thr, slide), tol, id.dt);
        try out.append(ctx.arena, try subRun(ctx, "S3_identity_vs_transformed", id.steps, id.hash, list));
        try out.append(ctx.arena, .{ .name = "S3_transformed_run", .steps = tf.steps, .final_state_sha256 = tf.hash, .metrics = &.{}, .passed = true });
    }
}

fn xf_identity_dir(v: m3.Vec3) m3.Vec3 {
    return Xf.identity.dir(v);
}

fn runPair(ctx: Ctx, sc: Scene, fr: crit.FrictionPair, st: u64) !Trace {
    return simulate(ctx, sc, fr, st);
}

fn bb8(ctx: Ctx, fr: crit.FrictionPair, st: u64, out: *std.ArrayList(SubRun)) !void {
    const b = ctx.c.BB8;
    const fa = fixtureOf(ctx, b.fixtures.A);
    const fb = fixtureOf(ctx, b.fixtures.B);
    var ba = blockAt(fa, b.poses.A_centre_m, .identity);
    ba.velocity_m_s = b.velocities.A_m_s;
    ba.angular_velocity_rad_s = b.velocities.angular_rad_s;
    var bb = blockAt(fb, b.poses.B_centre_m, .identity);
    bb.velocity_m_s = b.velocities.B_m_s;
    bb.angular_velocity_rad_s = b.velocities.angular_rad_s;
    const tr = try simulate(ctx, .{
        .b0 = ba,
        .b1 = bb,
        .gravity = m3.scale(ctx.c.gravity.direction_world, b.gravity_override.magnitude_m_s2),
        .tabletop = false,
        .settle = false,
        .duration_s = b.duration_s.value,
    }, fr, st);
    const au = b.audits;
    const k = fs.protocol_settings.contact_stiffness_n_m;
    const m_red = ba.mass_kg * bb.mass_kg / (ba.mass_kg + bb.mass_kg);
    const p: bce.Bb8Params = .{
        .bodies = .{ .{ .mass_kg = ba.mass_kg, .inertia_kg_m2 = ba.inertia_kg_m2 }, .{ .mass_kg = bb.mass_kg, .inertia_kg_m2 = bb.inertia_kg_m2 } },
        .g_n = ctx.c.gravity.magnitude_m_s2,
        .mom_rel = au.momentum.rel_tol_of_m_g_t.value,
        .mom_floor = au.momentum.abs_floor_kg_m_s.value,
        .ang_rel = au.angular_momentum.rel_tol.value,
        .ang_floor = au.angular_momentum.abs_floor_kg_m2_s.value,
        .r_ref_m = au.angular_momentum.r_ref_m.value,
        .imp_rel = au.impulse_accounting.rel_tol_of_step_impulse_sum.value,
        .imp_floor = au.impulse_accounting.abs_floor_n_s.value,
        .energy_rel = au.energy.creation_rel_tol.value,
        .energy_coeff = au.energy.first_order_omega_dt_coefficient.value,
        .energy_floor = au.energy.abs_floor_j.value,
        .omega_ref_rad_s = @sqrt(4.0 * k / m_red),
        .dt_s = tr.dt,
        .min_peak_tangential_impulse = b.sliding_engaged.min_peak_tangential_impulse_n_s.value,
    };
    const overlap = box_contact.collide(
        .{ .centre = tr.final[0].position_m, .orientation = tr.final[0].orientation, .half = tr.final[0].half_extents_m },
        .{ .centre = tr.final[1].position_m, .orientation = tr.final[1].orientation, .half = tr.final[1].half_extents_m },
    ) != null;
    var list: bce.List = .{};
    try bce.bb8(ctx.arena, &list, p, tr.samples, overlap);
    try out.append(ctx.arena, try subRun(ctx, "collision", tr.steps, tr.hash, list));
}

fn runCombination(ctx: Ctx, kind: CaseKind, fr: crit.FrictionPair, st: u64) ![]const SubRun {
    var out: std.ArrayList(SubRun) = .empty;
    switch (kind) {
        .bb1 => try bb1(ctx, fr, st, &out),
        .bb2 => try bb2(ctx, fr, st, &out),
        .bb3 => try bb3(ctx, fr, st, &out),
        .bb4 => try bb4(ctx, fr, st, &out),
        .bb5 => try bb5(ctx, fr, st, &out),
        .bb7 => try bb7(ctx, fr, st, &out),
        .bb8 => try bb8(ctx, fr, st, &out),
    }
    return out.toOwnedSlice(ctx.arena);
}

// --- BB6 ---

fn quatOf(b: bcc.Bb6Body) m3.Quat {
    if (b.orientation_rotation_about_x_rad) |t| return .{ .w = @cos(t / 2.0), .x = @sin(t / 2.0), .y = 0, .z = 0 };
    if (b.orientation_rotation_about_y_rad) |t| return .{ .w = @cos(t / 2.0), .x = 0, .y = @sin(t / 2.0), .z = 0 };
    return .identity;
}

fn boxOf(ctx: Ctx, b: bcc.Bb6Body) box_contact.Box {
    return .{ .centre = b.centre_m, .orientation = quatOf(b), .half = m3.scale(fixtureOf(ctx, b.fixture).size_m, 0.5) };
}

fn hashResult(h: *std.crypto.hash.sha2.Sha256, r: ?bce.Bb6Result) void {
    const x = r orelse {
        h.update("none");
        return;
    };
    h.update(std.mem.asBytes(&x.axis));
    h.update(std.mem.asBytes(&x.count));
    h.update(std.mem.asBytes(&x.normal));
    h.update(std.mem.asBytes(&x.depths));
    h.update(std.mem.asBytes(&x.points));
}

fn runBb6(ctx: Ctx) ![]const SubRun {
    const b = ctx.c.BB6;
    const tol = .{ .position_depth_rel_tol = b.tolerance.position_depth_rel_tol.value, .position_scale_m = b.tolerance.position_scale_m.value, .normal_component_abs_tol = b.tolerance.normal_component_abs_tol.value };
    var out: std.ArrayList(SubRun) = .empty;
    for (b.configurations) |cf| {
        const a = boxOf(ctx, cf.A);
        const bx = boxOf(ctx, cf.B);
        const exp_axis = try bcc.expectedAxis(cf.expected_axis);
        const fwd = bce.bb6Result(a, bx);
        const swp = bce.bb6Result(bx, a);
        var list: bce.List = .{};
        try bce.bb6Check(ctx.arena, &list, "", cf, exp_axis, tol, fwd, false, false);
        if (b.swap_check.value) try bce.bb6Check(ctx.arena, &list, "swapped.", cf, exp_axis, tol, swp, true, ctx.c.criteria_version >= 2);
        var h = std.crypto.hash.sha2.Sha256.init(.{});
        hashResult(&h, fwd);
        hashResult(&h, swp);
        var digest: [32]u8 = undefined;
        h.final(&digest);
        const hex = std.fmt.bytesToHex(digest, .lower);
        try out.append(ctx.arena, try subRun(ctx, cf.id, 0, try ctx.arena.dupe(u8, &hex), list));
    }
    return out.toOwnedSlice(ctx.arena);
}

fn replayMismatches(a: []const SubRun, b: []const SubRun) f64 {
    if (a.len != b.len) return @floatFromInt(@max(a.len, b.len));
    var n: f64 = 0;
    for (a, b) |x, y| if (!std.mem.eql(u8, x.final_state_sha256, y.final_state_sha256)) {
        n += 1;
    };
    return n;
}

const case_ids = [_]struct { CaseKind, []const u8 }{
    .{ .bb1, "BB1_stacked_rest" },
    .{ .bb2, "BB2_friction_threshold_on_block" },
    .{ .bb3, "BB3_slide_to_stop_on_block" },
    .{ .bb4, "BB4_drop_onto_block" },
    .{ .bb5, "BB5_tipping_on_block" },
    .{ .bb7, "BB7_frame_invariance" },
    .{ .bb8, "BB8_two_dynamic_bodies" },
};

/// Runs the whole suite. Report memory is owned by `arena`; per-run buffers
/// use `scratch` and are freed as each combination completes.
pub fn run(arena: std.mem.Allocator, scratch: std.mem.Allocator, c: bcc.Criteria) !Report {
    const ctx: Ctx = .{
        .arena = arena,
        .scratch = scratch,
        .c = c,
        .g = c.gravity.magnitude_m_s2,
        .unit = .{ .numerator = c.time_unit.numerator_s, .denominator = c.time_unit.denominator_s },
    };
    var cases: std.ArrayList(CaseReport) = .empty;
    var first: [case_ids.len]std.ArrayList(Combination) = @splat(.empty);

    for (case_ids, 0..) |k, ki| {
        var passes: std.ArrayList(bool) = .empty;
        for (c.friction_grid) |fr| for (c.physics_step_ticks) |st| {
            var sc = std.heap.ArenaAllocator.init(scratch);
            defer sc.deinit();
            var sub_ctx = ctx;
            sub_ctx.scratch = sc.allocator();
            const subs = try runCombination(sub_ctx, k[0], .{ .id = fr.id, .mu_static = fr.mu_static, .mu_kinetic = fr.mu_kinetic }, st);
            var ok = subs.len > 0;
            for (subs) |s| ok = ok and s.passed;
            try first[ki].append(arena, .{ .friction_id = fr.id, .physics_step_ticks = st, .passed = ok, .sub_runs = subs });
            try passes.append(arena, ok);
        };
        try cases.append(arena, .{ .case_id = k[1], .outcome = fe.combine(passes.items), .combinations = first[ki].items });
    }

    // BB6: once, no friction pair and no timestep.
    const bb6_subs = try runBb6(ctx);
    {
        var ok = bb6_subs.len > 0;
        for (bb6_subs) |s| ok = ok and s.passed;
        const combos = try arena.dupe(Combination, &.{.{ .friction_id = "not_applicable", .physics_step_ticks = 0, .passed = ok, .sub_runs = bb6_subs }});
        try cases.append(arena, .{ .case_id = c.BB6.id, .outcome = fe.combine(&.{ok}), .combinations = combos });
    }

    // BB9: every run is executed again from the same configuration.
    {
        var combos: std.ArrayList(Combination) = .empty;
        var passes: std.ArrayList(bool) = .empty;
        var ci: usize = 0;
        for (c.friction_grid) |fr| for (c.physics_step_ticks) |st| {
            var subs: std.ArrayList(SubRun) = .empty;
            for (case_ids, 0..) |k, ki| {
                var sc = std.heap.ArenaAllocator.init(scratch);
                defer sc.deinit();
                var sub_ctx = ctx;
                sub_ctx.scratch = sc.allocator();
                const again = try runCombination(sub_ctx, k[0], .{ .id = fr.id, .mu_static = fr.mu_static, .mu_kinetic = fr.mu_kinetic }, st);
                const mm = replayMismatches(first[ki].items[ci].sub_runs, again);
                const ms = try arena.dupe(Metric, &.{.{ .name = "replay_hash_mismatches", .value = mm, .limit = 0 }});
                try subs.append(arena, .{ .name = k[1], .steps = 0, .final_state_sha256 = "", .metrics = ms, .passed = mm == 0 });
            }
            const bb6_again = try runBb6(ctx);
            const mm6 = replayMismatches(bb6_subs, bb6_again);
            const ms6 = try arena.dupe(Metric, &.{.{ .name = "replay_hash_mismatches", .value = mm6, .limit = 0 }});
            try subs.append(arena, .{ .name = c.BB6.id, .steps = 0, .final_state_sha256 = "", .metrics = ms6, .passed = mm6 == 0 });
            var ok = true;
            for (subs.items) |s| ok = ok and s.passed;
            try combos.append(arena, .{ .friction_id = fr.id, .physics_step_ticks = st, .passed = ok, .sub_runs = try subs.toOwnedSlice(arena) });
            try passes.append(arena, ok);
            ci += 1;
        };
        try cases.append(arena, .{ .case_id = c.BB9.id, .outcome = fe.combine(passes.items), .combinations = try combos.toOwnedSlice(arena) });
    }

    const v1 = c.criteria_version < 2;
    return .{
        // Superseded criteria v1 can only be re-run as `exploratory` (Q79).
        .label = if (v1) "exploratory" else "fixture",
        .criteria_path = if (v1) "criteria/fixture-validation/body-contact-v1.json" else "criteria/fixture-validation/body-contact-v2.json",
        .criteria_sha256 = if (v1) bcc.v1_sha256 else bcc.v2_sha256,
        .settle_s = c.settle.duration_s.value,
        .solver_name = "kinigami-rigid",
        .solver_version = "0.1.0",
        .solver_settings = fs.protocol_settings,
        .cases = try cases.toOwnedSlice(arena),
    };
}

const Metric = bce.Metric;

const testing = std.testing;

fn loadCriteria() !@import("strict_json.zig").Parsed(bcc.Criteria) {
    return bcc.parse(testing.allocator, bcc.v1_json);
}

test "the BB7 transform built from fractions is a rotation with the registered quaternion" {
    const p = try loadCriteria();
    defer p.deinit();
    const xf = try transformOf(p.value);
    // Rotating the z axis by the quaternion reproduces the third matrix column.
    const z = xf.q.rotate(.{ 0, 0, 1 });
    for (0..3) |i| try testing.expectApproxEqAbs(xf.r[i][2], z[i], 1e-15);
    const x = xf.q.rotate(.{ 1, 0, 0 });
    for (0..3) |i| try testing.expectApproxEqAbs(xf.r[i][0], x[i], 1e-15);
}

test "BB6 configurations: the criteria orientation matrices match the quaternions used" {
    const p = try loadCriteria();
    defer p.deinit();
    for (p.value.BB6.configurations) |cf| for ([2]bcc.Bb6Body{ cf.A, cf.B }) |b| {
        const m = b.orientation_matrix orelse continue;
        const q = quatOf(b);
        const cols = [3]m3.Vec3{ q.rotate(.{ 1, 0, 0 }), q.rotate(.{ 0, 1, 0 }), q.rotate(.{ 0, 0, 1 }) };
        for (0..3) |j| for (0..3) |i| try testing.expectApproxEqAbs(m[i][j], cols[j][i], 1e-12);
    };
}

test "BB6 v2 swap rule: passes for face-face; edge-face and edge-edge swapped points are not translated (known, Q79 rule not met)" {
    const p = try bcc.parse(testing.allocator, bcc.v2_json);
    defer p.deinit();
    var arena = std.heap.ArenaAllocator.init(testing.allocator);
    defer arena.deinit();
    const ctx: Ctx = .{ .arena = arena.allocator(), .scratch = arena.allocator(), .c = p.value, .g = 9.80665, .unit = .{ .numerator = 1, .denominator = 1_000_000 } };
    const subs = try runBb6(ctx);
    try testing.expectEqual(@as(usize, 3), subs.len);
    // The generator chooses the reference box by SAT axis index. Swapping the
    // pair exchanges the incident box only for BB6a (axis tie 2 vs 5). For BB6b
    // (axis 5 beats the tying cross axis in either order) and BB6c (edge-edge
    // midpoint) the swapped points equal the (A, B) points, so the v2 rule
    // "translated by the depth along the normal" misses by one depth
    // (5e-4 / 0.04 = 1.25e-2). Recorded, not tuned.
    for (subs) |s| {
        var failing: usize = 0;
        for (s.metrics) |m| if (!m.passed()) {
            failing += 1;
            try testing.expectEqualStrings("swapped.point_rel_error", m.name);
            try testing.expectApproxEqAbs(@as(f64, 0.0005 / 0.04), m.value, 1e-9);
        };
        if (std.mem.startsWith(u8, s.name, "BB6a")) try testing.expectEqual(@as(usize, 0), failing) else try testing.expectEqual(@as(usize, 1), failing);
    }
}

test "BB6 under superseded v1 still reports the one-depth swapped point discrepancy" {
    const p = try loadCriteria();
    defer p.deinit();
    var arena = std.heap.ArenaAllocator.init(testing.allocator);
    defer arena.deinit();
    const ctx: Ctx = .{ .arena = arena.allocator(), .scratch = arena.allocator(), .c = p.value, .g = 9.80665, .unit = .{ .numerator = 1, .denominator = 1_000_000 } };
    const subs = try runBb6(ctx);
    for (subs) |s| {
        var failing: usize = 0;
        for (s.metrics) |m| if (!m.passed()) {
            failing += 1;
            try testing.expectEqualStrings("swapped.point_rel_error", m.name);
            try testing.expectEqualStrings("BB6a_face_face_offset", s.name);
            try testing.expectApproxEqAbs(@as(f64, 0.0005 / 0.04), m.value, 1e-9);
        };
        try testing.expect(failing <= 1);
    }
}

test "BB6 replay is bit-identical" {
    const p = try loadCriteria();
    defer p.deinit();
    var arena = std.heap.ArenaAllocator.init(testing.allocator);
    defer arena.deinit();
    const ctx: Ctx = .{ .arena = arena.allocator(), .scratch = arena.allocator(), .c = p.value, .g = 9.80665, .unit = .{ .numerator = 1, .denominator = 1_000_000 } };
    const a = try runBb6(ctx);
    const b = try runBb6(ctx);
    try testing.expectEqual(@as(f64, 0), replayMismatches(a, b));
}

test "BB1 stacked rest replay is bit-identical (final state hash)" {
    const p = try loadCriteria();
    defer p.deinit();
    var arena = std.heap.ArenaAllocator.init(testing.allocator);
    defer arena.deinit();
    const ctx: Ctx = .{ .arena = arena.allocator(), .scratch = arena.allocator(), .c = p.value, .g = 9.80665, .unit = .{ .numerator = 1, .denominator = 1_000_000 } };
    const fr: crit.FrictionPair = .{ .id = "mu_high", .mu_static = 0.9, .mu_kinetic = 0.7 };
    const a = try runCombination(ctx, .bb1, fr, 2000);
    const b = try runCombination(ctx, .bb1, fr, 2000);
    try testing.expectEqual(@as(f64, 0), replayMismatches(a, b));
}
