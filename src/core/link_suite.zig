//! Runs the compliant-link qualification criteria against the rigid backend
//! (Q52). Every case runs at every (stiffness grid point × physics step)
//! combination and is evaluated by `link_eval` (the committed protocol,
//! docs/validation/compliant-link-v1-protocol.md). Results are labeled
//! `fixture` and qualify only the declared envelope (Q40, Q46).
//!
//! Recording (Q55): with a recorder, each evaluated run (not its replay)
//! writes a format-v3 recording with link records. Recording only reads
//! simulation state and never feeds back (INS-007).

const std = @import("std");
const m3 = @import("math3.zig");
const lc = @import("link_criteria.zig");
const eval = @import("link_eval.zig");
const rigid = @import("rigid.zig");
const backend = @import("backend.zig");
const canonical = @import("canonical.zig");
const time = @import("time.zig");
const recording = @import("recording.zig");
const scene_record = @import("scene_record.zig");
const fixture_suite = @import("fixture_suite.zig");

pub const Recorder = fixture_suite.Recorder;

/// Effective configuration stored as each recording's first chunk.
const LinkRunConfig = struct {
    schema: []const u8 = "kinigami.link-run.v1",
    run_class: []const u8 = "fixture_validation",
    label: []const u8,
    criteria_sha256: []const u8,
    protocol_revision: u32 = eval.protocol_revision,
    case_id: []const u8,
    sub_run: []const u8,
    grid_id: []const u8,
    time_unit_numerator_s: u64,
    time_unit_denominator_s: u64,
    physics_step_ticks: u64,
    steps: u64,
    link: rigid.LinkSpec,
    load_kind: []const u8,
    load_force_n: m3.Vec3,
    load_torque_nm: m3.Vec3,
    solver: SolverConfig,
};

/// Contact settings are those of the analytic protocol; the link
/// prediction coefficient and the sweep count are fixed in the protocol
/// document before the first evaluation. Changing any requires a revision
/// log entry there.
pub const protocol_settings: rigid.Settings = .{
    .contact_stiffness_n_m = 1.0e5,
    .contact_damping_n_s_m = 50,
    .static_slip_speed_m_s = 1e-5,
    .iterations = 100,
    .warm_start = true,
};
pub const protocol_link_settings: rigid.LinkSettings = .{ .form = .midpoint_prediction, .prediction_q = 0.25 };

/// Solver configuration of one suite run.
pub const SolverConfig = struct { settings: rigid.Settings, link_settings: rigid.LinkSettings };
pub const protocol_config: SolverConfig = .{ .settings = protocol_settings, .link_settings = protocol_link_settings };

/// The exploratory solver-settings sensitivity grid declared in Q54 (PHY-016),
/// each a one-setting change from the protocol baseline.
pub const Variant = struct { name: []const u8, config: SolverConfig };
pub const sensitivity_variants = blk: {
    const base = protocol_config;
    var v: [9]Variant = undefined;
    v[0] = .{ .name = "baseline", .config = base };
    for (.{ 10, 25, 50, 200 }, 1..) |n, i| {
        var c = base;
        c.settings.iterations = n;
        v[i] = .{ .name = std.fmt.comptimePrint("iterations_{d}", .{n}), .config = c };
    }
    var nw = base;
    nw.settings.warm_start = false;
    v[5] = .{ .name = "no_warm_start", .config = nw };
    var q0 = base;
    q0.link_settings.prediction_q = 0;
    v[6] = .{ .name = "q_0", .config = q0 };
    var q5 = base;
    q5.link_settings.prediction_q = 0.5;
    v[7] = .{ .name = "q_0.5", .config = q5 };
    var be = base;
    be.link_settings = .{ .form = .backward_euler, .prediction_q = 1.0 };
    v[8] = .{ .name = "backward_euler", .config = be };
    break :blk v;
};

/// Free-fall cases start with both centres at this height (protocol).
pub const free_fall_height_m: f64 = 10.0;

pub const ReportMetric = struct {
    name: []const u8,
    /// Null when the measured value was not finite.
    value: ?f64,
    limit: f64,
    at_least: bool,
    informational: bool,
    passed: bool,
};

pub const SubRun = struct {
    name: []const u8,
    steps: u64,
    final_state_sha256: []const u8,
    /// An immediate in-process replay produced the same final-state hash (L10).
    replay_identical: bool,
    metrics: []const ReportMetric,
    passed: bool,
};

pub const Combination = struct {
    grid_id: []const u8,
    physics_step_ticks: u64,
    status: eval.Status,
    /// ω·Δt for the resolution rule; null for cases it does not apply to.
    omega_dt: ?f64,
    sub_runs: []const SubRun,
};

pub const CaseReport = struct {
    case_id: []const u8,
    outcome: eval.CaseOutcome,
    evaluated: usize,
    outside_envelope: usize,
    combinations: []const Combination,
};

pub const Report = struct {
    schema_version: u32 = 1,
    run_class: []const u8 = "fixture_validation",
    label: []const u8 = "fixture",
    criteria_path: []const u8,
    criteria_sha256: []const u8,
    protocol: []const u8 = "docs/validation/compliant-link-v1-protocol.md",
    protocol_revision: u32 = eval.protocol_revision,
    solver_name: []const u8,
    solver_version: []const u8,
    solver_settings: rigid.Settings,
    link_settings: rigid.LinkSettings,
    free_fall_height_m: f64 = free_fall_height_m,
    cases: []const CaseReport,
};

const Ctx = struct {
    arena: std.mem.Allocator,
    scratch: std.mem.Allocator,
    c: lc.Criteria,
    unit: time.TimeUnit,
    solver: SolverConfig = protocol_config,
    recorder: ?Recorder = null,
    label: []const u8 = "fixture",
    criteria_sha256: []const u8 = "",
};

/// What to record for one run, if anything.
const RecordAs = struct { case_id: []const u8, sub_run: []const u8 };

fn recordSnapshot(rec: *recording.Writer, buf: *canonical.BufferSink, w: *const rigid.World, tick: u64, stepped: bool) !void {
    var bodies: [2]scene_record.BodyState = undefined;
    for (&bodies, w.bodies.items) |*o, b| o.* = .{
        .position_m = b.position_m,
        .orientation = .{ b.orientation.w, b.orientation.x, b.orientation.y, b.orientation.z },
        .velocity_m_s = b.velocity_m_s,
        .angular_velocity_rad_s = b.angular_velocity_rad_s,
    };
    var contacts: [8]scene_record.ContactRecord = undefined;
    const reports = if (stepped) w.reports.items else &.{};
    std.debug.assert(reports.len <= contacts.len);
    for (reports, 0..) |r, i| contacts[i] = .{
        .body_a = r.body_a,
        .body_b = r.body_b orelse scene_record.tabletop,
        .point_m = r.world_point_m,
        .normal = r.world_normal,
        .normal_force_n = r.normal_force_n,
        .tangential_force_n = r.tangential_force_n,
    };
    const lr = if (stepped) w.link_reports.items[0] else w.linkGeometryReport(0);
    const links = [1]scene_record.LinkRecord{.{ .force_on_b_n = lr.force_on_b_n, .moment_on_b_nm = lr.moment_on_b_nm, .extension_m = lr.extension_m, .rotation_rad = lr.rotation_rad }};
    buf.list.clearRetainingCapacity();
    try scene_record.encodeSnapshot(buf.encoder(), .{ .tick = tick, .bodies = &bodies, .contacts = contacts[0..reports.len], .links = &links });
    try rec.snapshot(buf.list.items);
}

const HangLoad = enum { none, shear, torque };

const Scenario = union(enum) {
    hang: HangLoad,
    /// Two free cubes; initial stretch (m), initial twist (rad), damping ratio.
    free: struct { stretch_m: f64, twist_rad: f64, zeta: f64 },
    table,
};

fn stepsFor(ctx: Ctx, duration_s: f64, step_ticks: u64) !u64 {
    const ticks_f = duration_s * @as(f64, @floatFromInt(ctx.unit.denominator)) / @as(f64, @floatFromInt(ctx.unit.numerator));
    const ticks: u64 = @intFromFloat(@round(ticks_f));
    if (@as(f64, @floatFromInt(ticks)) != ticks_f or ticks % step_ticks != 0) return error.DurationNotWholeSteps;
    return ticks / step_ticks;
}

fn sample(w: *const rigid.World, t: f64, stepped: bool, body_b: u32) eval.Sample {
    const rep = if (stepped) w.link_reports.items[0] else w.linkGeometryReport(0);
    var p: m3.Vec3 = m3.zero;
    for (w.bodies.items) |b| {
        if (b.is_static) continue;
        p = m3.add(p, m3.scale(b.velocity_m_s, b.mass_kg));
    }
    var normal: f64 = 0;
    for (w.reports.items) |r| if (r.body_a == body_b) {
        normal += r.normal_force_n;
    };
    return .{
        .t_s = t,
        .force_b_n = rep.force_on_b_n,
        .moment_b_nm = rep.moment_on_b_nm,
        .extension_m = rep.extension_m,
        .rotation_rad = rep.rotation_rad,
        .momentum_kg_m_s = p,
        .contact_normal_sum_n = normal,
    };
}

const Run = struct { samples: []eval.Sample, hash: []const u8, steps: u64 };

/// Simulates one run. Samples are owned by `ctx.scratch`, the hash by `ctx.arena`.
fn simulate(ctx: Ctx, sc: Scenario, gp: lc.GridPoint, step_ticks: u64, record_as: ?RecordAs) !Run {
    const c = ctx.c;
    const g = c.gravity.magnitude_m_s2;
    const edge = c.fixture.size_m[0];
    const half = edge / 2.0;
    const m = c.fixture.mass_kg;
    const inertia = eval.cubeInertia(m, edge);
    const l0 = c.link.rest_length_m;
    const dt = ctx.unit.seconds(.{ .ticks = step_ticks });

    var world: rigid.World = .{
        .gpa = ctx.scratch,
        .settings = ctx.solver.settings,
        .link_settings = ctx.solver.link_settings,
        .friction = .{ .mu_static = c.consistency_case.friction_pair.mu_static, .mu_kinetic = c.consistency_case.friction_pair.mu_kinetic },
        .gravity_m_s2 = m3.scale(c.gravity.direction_world, g),
        .allow_static_bodies = true,
    };
    defer world.deinit();

    const size: m3.Vec3 = c.fixture.size_m;
    var axis: m3.Vec3 = .{ 0, 0, -1 };
    var duration_s: f64 = undefined;
    var zeta: f64 = undefined;
    var mass_for_c: f64 = m;
    var inertia_for_c: f64 = inertia;
    switch (sc) {
        .hang => {
            const z_anchor_a = 1.0 - half;
            _ = try world.addBody(rigid.staticCuboid(size, .{ 0, 0, 1.0 }));
            _ = try world.addBody(rigid.cuboid(m, size, z_anchor_a - l0 - edge));
            duration_s = c.static_cases.duration_s;
            zeta = c.static_cases.damping_ratio_on_body_b;
        },
        .free => |f| {
            axis = .{ 1, 0, 0 };
            var a = rigid.cuboid(m, size, 0);
            a.position_m = .{ 0, 0, free_fall_height_m };
            var b = a;
            b.position_m = .{ edge + l0 + f.stretch_m, 0, free_fall_height_m };
            b.orientation = .{ .w = @cos(f.twist_rad / 2.0), .x = @sin(f.twist_rad / 2.0), .y = 0, .z = 0 };
            _ = try world.addBody(a);
            _ = try world.addBody(b);
            duration_s = c.dynamic_cases.duration_s;
            zeta = f.zeta;
            mass_for_c = eval.reducedMass(m, m);
            inertia_for_c = eval.reducedInertia(inertia, inertia);
        },
        .table => {
            const k = c.consistency_case;
            const z_anchor_b = edge;
            const d0 = k.pretension_over_weight * m * g / gp.k_axial_n_m;
            const z_anchor_a = z_anchor_b + l0 + d0;
            _ = try world.addBody(rigid.staticCuboid(size, .{ 0, 0, z_anchor_a + half }));
            _ = try world.addBody(rigid.cuboid(m, size, 0));
            duration_s = k.duration_s;
            zeta = k.damping_ratio_on_body_b;
        },
    }
    _ = try world.addLink(.{
        .body_a = 0,
        .body_b = 1,
        .axis_a = axis,
        .anchor_a_m = m3.scale(axis, half),
        .anchor_b_m = m3.scale(axis, -half),
        .rest_length_m = l0,
        .k_axial_n_m = gp.k_axial_n_m,
        .k_shear_n_m = gp.k_shear_n_m,
        .k_torsion_nm_rad = gp.k_torsion_nm_rad,
        .k_bend_nm_rad = gp.k_bend_nm_rad,
        .c_axial_n_s_m = eval.dampingCoefficient(zeta, gp.k_axial_n_m, mass_for_c),
        .c_shear_n_s_m = eval.dampingCoefficient(zeta, gp.k_shear_n_m, mass_for_c),
        .c_torsion_nm_s_rad = eval.dampingCoefficient(zeta, gp.k_torsion_nm_rad, inertia_for_c),
        .c_bend_nm_s_rad = eval.dampingCoefficient(zeta, gp.k_bend_nm_rad, inertia_for_c),
    });

    const n = try stepsFor(ctx, duration_s, step_ticks);
    const samples = try ctx.scratch.alloc(eval.Sample, n + 1);
    samples[0] = sample(&world, 0, false, 1);

    var rec: ?recording.Writer = null;
    defer if (rec) |*r| r.deinit();
    var snap_buf: canonical.BufferSink = .{ .gpa = ctx.scratch };
    defer snap_buf.deinit();
    if (ctx.recorder != null) if (record_as) |ra| {
        const load_kind: []const u8, const lf: m3.Vec3, const lt: m3.Vec3 = switch (sc) {
            .hang => |hl| switch (hl) {
                .none => .{ "none", m3.zero, m3.zero },
                .shear => .{ "world_force_at_center_of_mass_b", m3.scale(c.static_cases.shear_bending.load_world_direction, c.static_cases.shear_bending.load_over_weight * m * g), m3.zero },
                .torque => .{ "world_torque_on_b", m3.zero, m3.scale(axis, c.static_cases.torsion.torque_about_link_axis_nm) },
            },
            else => .{ "none", m3.zero, m3.zero },
        };
        const cfg_json = try std.json.Stringify.valueAlloc(ctx.scratch, LinkRunConfig{
            .label = ctx.label,
            .criteria_sha256 = ctx.criteria_sha256,
            .case_id = ra.case_id,
            .sub_run = ra.sub_run,
            .grid_id = gp.id,
            .time_unit_numerator_s = ctx.unit.numerator,
            .time_unit_denominator_s = ctx.unit.denominator,
            .physics_step_ticks = step_ticks,
            .steps = n,
            .link = world.links.items[0].spec,
            .load_kind = load_kind,
            .load_force_n = lf,
            .load_torque_nm = lt,
            .solver = ctx.solver,
        }, .{});
        rec = try recording.Writer.init(ctx.scratch, cfg_json);
        var infos: [2]scene_record.BodyInfo = undefined;
        for (&infos, world.bodies.items, [_][]const u8{ "fixture_link_cube_a", "fixture_link_cube_b" }) |*o, b, id| o.* = .{
            .id = id,
            .kind = if (b.is_static) .static_fixture else .fixture,
            .shape = .cuboid,
            .half_extents_m = b.half_extents_m,
            .mass_kg = if (b.is_static) 0 else b.mass_kg,
        };
        const sp = world.links.items[0].spec;
        const link_infos = [1]scene_record.LinkInfo{.{ .body_a = sp.body_a, .body_b = sp.body_b, .axes_a = world.linkAxesBodyA(0), .anchor_a_m = sp.anchor_a_m, .anchor_b_m = sp.anchor_b_m, .rest_length_m = sp.rest_length_m }};
        var hb: canonical.BufferSink = .{ .gpa = ctx.scratch };
        defer hb.deinit();
        try scene_record.encodeHeader(hb.encoder(), .{
            .time_unit_numerator_s = ctx.unit.numerator,
            .time_unit_denominator_s = ctx.unit.denominator,
            .physics_step_ticks = step_ticks,
            .snapshot_interval_steps = 1,
            .bodies = &infos,
            .links = &link_infos,
        });
        try rec.?.sceneHeader(hb.list.items);
        try recordSnapshot(&rec.?, &snap_buf, &world, 0, false);
    };
    var loads: [1]backend.AppliedLoad = undefined;
    for (1..n + 1) |i| {
        var inputs: backend.StepInputs = .{};
        if (sc == .hang) {
            const pos = world.bodies.items[1].position_m;
            switch (sc.hang) {
                .none => {},
                .shear => {
                    const s = c.static_cases.shear_bending;
                    loads[0] = .{ .body_index = 1, .world_force_n = m3.scale(s.load_world_direction, s.load_over_weight * m * g), .world_torque_nm = m3.zero, .world_point_m = pos };
                    inputs = .{ .validation_loads = &loads };
                },
                .torque => {
                    loads[0] = .{ .body_index = 1, .world_force_n = m3.zero, .world_torque_nm = m3.scale(axis, c.static_cases.torsion.torque_about_link_axis_nm), .world_point_m = pos };
                    inputs = .{ .validation_loads = &loads };
                },
            }
        }
        try world.step(dt, inputs);
        samples[i] = sample(&world, ctx.unit.seconds(.{ .ticks = i * step_ticks }), true, 1);
        if (rec) |*r| try recordSnapshot(r, &snap_buf, &world, i * step_ticks, true);
    }
    if (rec) |*r| {
        const bytes = try r.finish();
        defer ctx.scratch.free(bytes);
        const name = try std.fmt.allocPrint(ctx.scratch, "{s}__{s}__dt{d}us.kgrec", .{ record_as.?.case_id, gp.id, step_ticks });
        try ctx.recorder.?.emit(ctx.recorder.?.ptr, name, bytes);
    }

    var sink: canonical.BufferSink = .{ .gpa = ctx.scratch };
    defer sink.deinit();
    try world.encodeState(sink.encoder());
    var digest: [32]u8 = undefined;
    std.crypto.hash.sha2.Sha256.hash(sink.list.items, &digest, .{});
    const hex = std.fmt.bytesToHex(digest, .lower);
    return .{ .samples = samples, .hash = try ctx.arena.dupe(u8, &hex), .steps = n };
}

fn subRun(ctx: Ctx, name: []const u8, run1: Run, replay_hash: []const u8, e: eval.Evaluation) !SubRun {
    const metrics = try ctx.arena.alloc(ReportMetric, e.len);
    for (e.slice(), metrics) |m, *out| out.* = .{
        .name = m.name,
        .value = if (std.math.isFinite(m.value)) m.value else null,
        .limit = m.limit,
        .at_least = m.at_least,
        .informational = m.informational,
        .passed = m.passed(),
    };
    return .{ .name = name, .steps = run1.steps, .final_state_sha256 = run1.hash, .replay_identical = std.mem.eql(u8, run1.hash, replay_hash), .metrics = metrics, .passed = e.passed() };
}

const CaseKind = enum { l1, l2, l3, l4, l5, l6, l7, l8, l9 };

fn runCombination(ctx: Ctx, kind: CaseKind, case_id: []const u8, gp: lc.GridPoint, step_ticks: u64) !Combination {
    const c = ctx.c;
    const dyn = c.dynamic_cases;
    const g = c.gravity.magnitude_m_s2;
    const m = c.fixture.mass_kg;
    const edge = c.fixture.size_m[0];
    const inertia = eval.cubeInertia(m, edge);
    const dt = ctx.unit.seconds(.{ .ticks = step_ticks });
    const setup: eval.StaticSetup = .{
        .mass_kg = m,
        .g_m_s2 = g,
        .k_axial_n_m = gp.k_axial_n_m,
        .k_shear_n_m = gp.k_shear_n_m,
        .k_torsion_nm_rad = gp.k_torsion_nm_rad,
        .k_bend_nm_rad = gp.k_bend_nm_rad,
        .half_size_m = edge / 2.0,
        .window = .{ .start_s = c.static_cases.window_start_s, .end_s = c.static_cases.duration_s },
    };
    const omega_axial = eval.omega(gp.k_axial_n_m, eval.reducedMass(m, m));
    const omega_torsion = eval.omega(gp.k_torsion_nm_rad, eval.reducedInertia(inertia, inertia));

    // Resolution rule: L4-L7 only (Q52 §4).
    const omega_ref: ?f64 = switch (kind) {
        .l4, .l6, .l7 => omega_axial,
        .l5 => omega_torsion,
        else => null,
    };
    const omega_dt: ?f64 = if (omega_ref) |w| w * dt else null;
    if (omega_ref) |w| if (!eval.resolved(w, dt, c.resolution.max_omega_dt)) {
        return .{ .grid_id = gp.id, .physics_step_ticks = step_ticks, .status = .outside_envelope, .omega_dt = omega_dt, .sub_runs = &.{} };
    };

    const scenario: Scenario = switch (kind) {
        .l1 => .{ .hang = .none },
        .l2 => .{ .hang = .shear },
        .l3 => .{ .hang = .torque },
        .l4, .l8 => .{ .free = .{ .stretch_m = dyn.axial.initial_stretch_m, .twist_rad = 0, .zeta = dyn.axial.damping_ratio } },
        .l5 => .{ .free = .{ .stretch_m = 0, .twist_rad = dyn.torsion.initial_twist_rad, .zeta = dyn.torsion.damping_ratio } },
        .l6 => .{ .free = .{ .stretch_m = dyn.physical_damping.initial_stretch_m, .twist_rad = 0, .zeta = dyn.physical_damping.damping_ratio } },
        .l7 => .{ .free = .{ .stretch_m = dyn.numerical_dissipation.initial_stretch_m, .twist_rad = 0, .zeta = dyn.numerical_dissipation.damping_ratio } },
        .l9 => .table,
    };
    const r = try simulate(ctx, scenario, gp, step_ticks, .{ .case_id = case_id, .sub_run = @tagName(kind) });
    const replay = try simulate(ctx, scenario, gp, step_ticks, null);
    const e: eval.Evaluation = switch (kind) {
        .l1 => eval.axialStatics(c.static_cases.axial, setup, r.samples),
        .l2 => eval.shearBendingStatics(c.static_cases.shear_bending, setup, r.samples),
        .l3 => eval.torsionStatics(c.static_cases.torsion, setup, r.samples),
        .l4 => eval.periodCheck("period_rel_error", dyn.axial.period_rel_tol, omega_axial, .axial_extension, r.samples),
        .l5 => eval.periodCheck("period_rel_error", dyn.torsion.period_rel_tol, omega_torsion, .twist, r.samples),
        .l6 => eval.physicalDamping(dyn.physical_damping, r.samples),
        .l7 => eval.numericalDissipation(dyn.numerical_dissipation, r.samples),
        .l8 => eval.momentum(dyn.momentum, 2.0 * m, m3.scale(c.gravity.direction_world, g), r.samples),
        .l9 => eval.contactLinkConsistency(c.consistency_case, m, g, r.samples),
    };
    const subs = try ctx.arena.alloc(SubRun, 1);
    subs[0] = try subRun(ctx, @tagName(kind), r, replay.hash, e);
    return .{ .grid_id = gp.id, .physics_step_ticks = step_ticks, .status = if (subs[0].passed) .pass else .fail, .omega_dt = omega_dt, .sub_runs = subs };
}

fn caseReport(arena: std.mem.Allocator, id: []const u8, combos: []const Combination) !CaseReport {
    const statuses = try arena.alloc(eval.Status, combos.len);
    var evaluated: usize = 0;
    var outside: usize = 0;
    for (combos, statuses) |cb, *s| {
        s.* = cb.status;
        if (cb.status == .outside_envelope) outside += 1 else evaluated += 1;
    }
    return .{ .case_id = id, .outcome = eval.combine(statuses), .evaluated = evaluated, .outside_envelope = outside, .combinations = combos };
}

/// Runs the whole suite. Report memory is owned by `arena`; per-run sample
/// buffers use `scratch` and are freed as each run completes.
/// Criteria file identity recorded in the report (DAT-011).
pub const CriteriaIdentity = struct { path: []const u8, sha256: []const u8 };

/// The official criteria (Q53): v2.
pub const official_criteria: CriteriaIdentity = .{ .path = "criteria/qualification/compliant-link-v2.json", .sha256 = lc.link_v2_sha256 };

/// Official run: protocol settings, labeled `fixture`.
pub fn run(arena: std.mem.Allocator, scratch: std.mem.Allocator, c: lc.Criteria, identity: CriteriaIdentity, recorder: ?Recorder) !Report {
    return runWith(arena, scratch, c, identity, protocol_config, "fixture", recorder);
}

/// Any solver configuration. Non-protocol configurations must be labeled
/// `exploratory` (Q54); this is enforced.
pub fn runWith(arena: std.mem.Allocator, scratch: std.mem.Allocator, c: lc.Criteria, identity: CriteriaIdentity, solver: SolverConfig, label: []const u8, recorder: ?Recorder) !Report {
    const is_protocol = std.meta.eql(solver, protocol_config);
    if (!is_protocol and !std.mem.eql(u8, label, "exploratory")) return error.NonProtocolRunMustBeExploratory;
    const ctx: Ctx = .{ .arena = arena, .scratch = scratch, .c = c, .unit = .{ .numerator = c.time_unit.numerator_s, .denominator = c.time_unit.denominator_s }, .solver = solver, .recorder = recorder, .label = label, .criteria_sha256 = identity.sha256 };
    const kinds = [_]struct { CaseKind, []const u8 }{
        .{ .l1, c.static_cases.axial.id },
        .{ .l2, c.static_cases.shear_bending.id },
        .{ .l3, c.static_cases.torsion.id },
        .{ .l4, c.dynamic_cases.axial.id },
        .{ .l5, c.dynamic_cases.torsion.id },
        .{ .l6, c.dynamic_cases.physical_damping.id },
        .{ .l7, c.dynamic_cases.numerical_dissipation.id },
        .{ .l8, c.dynamic_cases.momentum.id },
        .{ .l9, c.consistency_case.id },
    };
    var cases: std.ArrayList(CaseReport) = .empty;
    var all: std.ArrayList(Combination) = .empty;
    for (kinds) |k| {
        var combos: std.ArrayList(Combination) = .empty;
        for (c.stiffness_grid) |gp| for (c.physics_step_ticks) |st| {
            var sc = std.heap.ArenaAllocator.init(scratch);
            defer sc.deinit();
            var sub_ctx = ctx;
            sub_ctx.scratch = sc.allocator();
            const cb = try runCombination(sub_ctx, k[0], k[1], gp, st);
            try combos.append(arena, cb);
            try all.append(arena, cb);
        };
        try cases.append(arena, try caseReport(arena, k[1], try combos.toOwnedSlice(arena)));
    }

    // L10: per (grid point × Δt), every executed run replayed bit-identically.
    var l10: std.ArrayList(Combination) = .empty;
    for (c.stiffness_grid) |gp| for (c.physics_step_ticks) |st| {
        var ok = true;
        var any = false;
        for (all.items) |cb| {
            if (!std.mem.eql(u8, cb.grid_id, gp.id) or cb.physics_step_ticks != st) continue;
            for (cb.sub_runs) |s| {
                any = true;
                ok = ok and s.replay_identical;
            }
        }
        try l10.append(arena, .{ .grid_id = gp.id, .physics_step_ticks = st, .status = if (any and ok) .pass else .fail, .omega_dt = null, .sub_runs = &.{} });
    };
    try cases.append(arena, try caseReport(arena, c.determinism.id, try l10.toOwnedSlice(arena)));

    return .{
        .criteria_path = identity.path,
        .criteria_sha256 = identity.sha256,
        .solver_name = "kinigami-rigid",
        .solver_version = "0.1.0",
        .label = label,
        .solver_settings = solver.settings,
        .link_settings = solver.link_settings,
        .cases = try cases.toOwnedSlice(arena),
    };
}

const testing = std.testing;

test "recording leaves link results unchanged and stores every step with link records (INS-007, Q55)" {
    const gpa = testing.allocator;
    const parsed = try lc.parse(gpa, lc.link_v2_json);
    defer parsed.deinit();
    var arena = std.heap.ArenaAllocator.init(gpa);
    defer arena.deinit();
    const Collect = struct {
        gpa: std.mem.Allocator,
        bytes: ?[]u8 = null,
        fn emit(ptr: *anyopaque, _: []const u8, b: []const u8) anyerror!void {
            const self: *@This() = @ptrCast(@alignCast(ptr));
            self.bytes = try self.gpa.dupe(u8, b);
        }
    };
    var col: Collect = .{ .gpa = gpa };
    defer if (col.bytes) |b| gpa.free(b);
    const base: Ctx = .{ .arena = arena.allocator(), .scratch = arena.allocator(), .c = parsed.value, .unit = .{ .numerator = 1, .denominator = 1_000_000 } };
    var with = base;
    with.recorder = .{ .ptr = &col, .emit = Collect.emit };
    const gp = parsed.value.stiffness_grid[1];
    const a = try runCombination(base, .l2, "L2", gp, 2000);
    const b = try runCombination(with, .l2, "L2", gp, 2000);
    try testing.expectEqualStrings(a.sub_runs[0].final_state_sha256, b.sub_runs[0].final_state_sha256);
    const rec = try recording.Recording.parse(col.bytes.?);
    try testing.expectEqual(@as(u16, 3), rec.version);
    try testing.expectEqual(@as(usize, a.sub_runs[0].steps + 1), rec.snapshot_count);
    const header = try scene_record.decodeHeader(arena.allocator(), rec.scene_header.?, rec.version);
    try testing.expectEqual(scene_record.BodyKind.static_fixture, header.bodies[0].kind);
    try testing.expectEqual(@as(usize, 1), header.links.len);
    var it = rec.snapshots();
    var last: ?scene_record.Snapshot = null;
    while (it.next()) |p| last = try scene_record.decodeSnapshot(arena.allocator(), header, p);
    // The last recorded link force is the solver's: tension ≈ m·g.
    try testing.expectApproxEqRel(@as(f64, 0.02 * 9.80665), -last.?.links[0].force_on_b_n[0], 1e-6);
}

test "non-protocol solver settings cannot be labeled fixture" {
    const gpa = testing.allocator;
    const parsed = try lc.parse(gpa, lc.link_v2_json);
    defer parsed.deinit();
    var arena = std.heap.ArenaAllocator.init(gpa);
    defer arena.deinit();
    try testing.expectError(error.NonProtocolRunMustBeExploratory, runWith(arena.allocator(), gpa, parsed.value, official_criteria, sensitivity_variants[1].config, "fixture", null));
}

test "the backward-Euler control dissipates where the protocol link does not (L7 discriminates)" {
    const gpa = testing.allocator;
    const parsed = try lc.parse(gpa, lc.link_v2_json);
    defer parsed.deinit();
    var arena = std.heap.ArenaAllocator.init(gpa);
    defer arena.deinit();
    var ctx: Ctx = .{ .arena = arena.allocator(), .scratch = arena.allocator(), .c = parsed.value, .unit = .{ .numerator = 1, .denominator = 1_000_000 } };
    const soft = parsed.value.stiffness_grid[0];
    const proto = try runCombination(ctx, .l7, "L7", soft, 2000);
    try testing.expectEqual(eval.Status.pass, proto.status);
    ctx.solver = sensitivity_variants[8].config;
    const be = try runCombination(ctx, .l7, "L7", soft, 2000);
    try testing.expectEqual(eval.Status.fail, be.status);
}

test "the suite wiring yields the registered case list, and statics at one combination run" {
    const gpa = testing.allocator;
    const parsed = try lc.parse(gpa, lc.link_v2_json);
    defer parsed.deinit();
    var arena = std.heap.ArenaAllocator.init(gpa);
    defer arena.deinit();
    const ctx: Ctx = .{ .arena = arena.allocator(), .scratch = arena.allocator(), .c = parsed.value, .unit = .{ .numerator = 1, .denominator = 1_000_000 } };
    const cb = try runCombination(ctx, .l1, "L1", parsed.value.stiffness_grid[1], 2000);
    try testing.expectEqual(@as(usize, 1), cb.sub_runs.len);
    try testing.expect(cb.sub_runs[0].replay_identical);
    try testing.expectEqual(@as(usize, 64), cb.sub_runs[0].final_state_sha256.len);
}

test "unresolved dynamic combinations are outside the envelope and run nothing" {
    const gpa = testing.allocator;
    const parsed = try lc.parse(gpa, lc.link_v2_json);
    defer parsed.deinit();
    var arena = std.heap.ArenaAllocator.init(gpa);
    defer arena.deinit();
    const ctx: Ctx = .{ .arena = arena.allocator(), .scratch = arena.allocator(), .c = parsed.value, .unit = .{ .numerator = 1, .denominator = 1_000_000 } };
    const stiff = parsed.value.stiffness_grid[2];
    const cb = try runCombination(ctx, .l4, "L4", stiff, 500);
    try testing.expectEqual(eval.Status.outside_envelope, cb.status);
    try testing.expectEqual(@as(usize, 0), cb.sub_runs.len);
    // The soft-axial 2 ms combination sits exactly on the limit and is evaluated.
    const soft = try runCombination(ctx, .l8, "L8", parsed.value.stiffness_grid[0], 2000);
    try testing.expect(soft.status != .outside_envelope);
}
