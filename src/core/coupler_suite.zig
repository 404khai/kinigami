//! Runs the coupler-engagement qualification criteria v1 against the rigid
//! backend (Q56, Q57; protocol revision 2, Q58). Every case runs at every
//! physics step of the criteria and is evaluated by `coupler_eval`
//! (docs/validation/coupler-engagement-v1-protocol.md). The audits run on
//! every C1-C7 run as gating metrics of that run. Results are labeled
//! `fixture` and qualify only the declared envelope for this stand-in (Q40).
//!
//! Part 1 covers C1-C7 and C10. C8 (capture sweep) and C9 (audit
//! discrimination) are part 2: the report already carries their sections,
//! empty for now.
//!
//! Scenarios are built from the parsed criteria only. The few constants the
//! protocol's Setups table fixes (hang position, free-fall height, axes) are
//! named below.

const std = @import("std");
const m3 = @import("math3.zig");
const cc = @import("coupler_criteria.zig");
const ce = @import("coupler_eval.zig");
const le = @import("link_eval.zig");
const rigid = @import("rigid.zig");
const backend = @import("backend.zig");
const canonical = @import("canonical.zig");
const time = @import("time.zig");
const geometry = @import("coupler_geometry.zig");
const link_suite = @import("link_suite.zig");
const fixture_suite = @import("fixture_suite.zig");

pub const Recorder = fixture_suite.Recorder;

/// Protocol revision implemented by the suite (Q58 made it revision 2).
pub const protocol_revision: u32 = 2;

pub const protocol_settings = link_suite.protocol_settings;
pub const protocol_link_settings = link_suite.protocol_link_settings;

/// Protocol "Setups": static A of the hang cases, and the free-fall height.
const hang_centre_a_m: m3.Vec3 = .{ 0, 0, 1.0 };
const hang_axis: m3.Vec3 = .{ 0, 0, -1 };
const free_centre_a_m: m3.Vec3 = .{ 0, 0, 10.0 };
const free_axis: m3.Vec3 = .{ 1, 0, 0 };

pub const ReportMetric = link_suite.ReportMetric;
pub const SubRun = link_suite.SubRun;
pub const Combination = link_suite.Combination;
pub const CaseReport = link_suite.CaseReport;
pub const CriteriaIdentity = link_suite.CriteriaIdentity;

/// Part 2 shape of one capture-sweep line (C8): reported, not gated.
pub const CaptureSweepEntry = struct {
    friction_pair: []const u8,
    offset_direction: []const u8,
    misalignment_rad: f64,
    approach_speed_m_s: f64,
    physics_step_ticks: u64,
    captured_offsets_m: []const f64,
    capture_radius_m: ?f64,
    dt_disagreement: bool,
};

/// Part 2 shape of one audit-discrimination line (C9).
pub const AuditDiscriminationEntry = struct {
    control: []const u8,
    physics_step_ticks: u64,
    audit: []const u8,
    caught: bool,
};

pub const Report = struct {
    schema_version: u32 = 1,
    run_class: []const u8 = "fixture_validation",
    label: []const u8 = "fixture",
    criteria_path: []const u8,
    criteria_sha256: []const u8,
    protocol: []const u8 = "docs/validation/coupler-engagement-v1-protocol.md",
    protocol_revision: u32 = protocol_revision,
    solver_name: []const u8,
    solver_version: []const u8,
    solver_settings: rigid.Settings,
    link_settings: rigid.LinkSettings,
    cases: []const CaseReport,
    // part 2: filled by the capture sweep and the audit-discrimination controls.
    capture_sweep: []const CaptureSweepEntry = &.{},
    audit_discrimination: []const AuditDiscriminationEntry = &.{},
};

pub const official_criteria: CriteriaIdentity = .{ .path = "criteria/qualification/coupler-engagement-v1.json", .sha256 = cc.coupler_v1_sha256 };

const Ctx = struct {
    arena: std.mem.Allocator,
    scratch: std.mem.Allocator,
    c: cc.Criteria,
    unit: time.TimeUnit,
    solver: link_suite.SolverConfig = link_suite.protocol_config,
    /// part 2: recordings. Unused in part 1.
    recorder: ?Recorder = null,
    /// Criteria the scenario is *built* from. Null: `c`. Only the wrong-spec
    /// test sets it, to prove the evaluators are not vacuous.
    build_c: ?cc.Criteria = null,

    fn built(self: Ctx) cc.Criteria {
        return self.build_c orelse self.c;
    }
};

// --- Scenarios ---

const Geometry = enum { hang, free };

const LimitLoad = struct { axis: cc.Axis, e: f64, factor: f64 };

const LoadSpec = union(enum) {
    none,
    /// C1/C2/C5: validation force (N) on B at its centre of mass, along the
    /// world direction of the coupler axis (away from A).
    pull: f64,
    /// C3: equal and opposite ramped loads on both bodies.
    limit: LimitLoad,
};

const Scenario = struct {
    geometry: Geometry,
    guide: bool,
    friction: cc.GuideFriction = .{ .mu_static = 0, .mu_kinetic = 0 },
    /// Initial pawl travel as a fraction of u_full; the link is active iff `link_active`.
    e0: f64,
    link_active: bool,
    /// Ball centre offset from the seat point along the coupler axis (m).
    offset_axial_m: f64 = 0,
    twist_rad: f64 = 0,
    /// Damping ratio defining c_full as c = 2ζ·√(e_ref·k·μ_red) = e_ref·c_full.
    zeta: f64,
    zeta_at_e: f64 = 1.0,
    duration_s: f64,
    command_first: backend.Command,
    command_then: backend.Command,
    /// Step starts at or after this time use `command_then`; null: never.
    switch_s: ?f64 = null,
    load: LoadSpec = .none,
};

fn axisOf(g: Geometry) m3.Vec3 {
    return switch (g) {
        .hang => hang_axis,
        .free => free_axis,
    };
}

fn centreA(g: Geometry) m3.Vec3 {
    return switch (g) {
        .hang => hang_centre_a_m,
        .free => free_centre_a_m,
    };
}

fn edgeOf(c: cc.Criteria) f64 {
    return c.fixture.size_m[0];
}

fn inertiaOf(c: cc.Criteria) f64 {
    return le.cubeInertia(c.fixture.mass_kg, edgeOf(c));
}

fn geomParams(c: cc.Criteria) geometry.Params {
    return .{
        .apex_depth_m = c.stand_in.socket.apex_depth_m,
        .mouth_half_width_m = c.stand_in.socket.mouth_half_width_m,
        .face_half_size_m = edgeOf(c) / 2.0,
    };
}

/// Damping so that rows at engagement `e_ref` have c = 2ζ·√(e_ref·k·m).
/// The solver multiplies the declared c_full by the actual engagement.
fn dampFull(zeta: f64, e_ref: f64, k: f64, mass_or_inertia: f64) f64 {
    return le.dampingCoefficient(zeta, e_ref * k, mass_or_inertia) / e_ref;
}

fn couplerSpec(c: cc.Criteria, sc: Scenario) rigid.CouplerSpec {
    const axis = axisOf(sc.geometry);
    const lk = c.stand_in.latch_link;
    const k = lk.full_stiffness;
    const pw = c.stand_in.pawl;
    const mu_red = le.reducedMass(c.fixture.mass_kg, c.fixture.mass_kg);
    const i_red = le.reducedInertia(inertiaOf(c), inertiaOf(c));
    const z = sc.zeta;
    const e = sc.zeta_at_e;
    return .{
        .body_a = 0,
        .body_b = 1,
        .axis_a = axis,
        .face_offset_a_m = edgeOf(c) / 2.0,
        .geom = geomParams(c),
        .ball_radius_m = c.stand_in.probe.radius_m,
        .ball_centre_b_m = m3.scale(axis, -(edgeOf(c) / 2.0 + c.stand_in.probe.stem_length_m)),
        .preload_offset_m = lk.preload_offset_m,
        .k_axial_full = k.k_axial_n_m,
        .k_shear_full = k.k_shear_n_m,
        .k_torsion_full = k.k_torsion_nm_rad,
        .k_bend_full = k.k_bend_nm_rad,
        .c_axial_full = dampFull(z, e, k.k_axial_n_m, mu_red),
        .c_shear_full = dampFull(z, e, k.k_shear_n_m, mu_red),
        .c_torsion_full = dampFull(z, e, k.k_torsion_nm_rad, i_red),
        .c_bend_full = dampFull(z, e, k.k_bend_nm_rad, i_red),
        .limit_tension_n = lk.full_limits.tension_n,
        .limit_shear_n = lk.full_limits.shear_n,
        .limit_bending_nm = lk.full_limits.bending_nm,
        .limit_torsion_nm = lk.full_limits.torsion_nm,
        .travel_m = pw.travel_m,
        .speed_limit_m_s = pw.speed_limit_m_s,
        .actuator_force_n = pw.actuator_force_limit_n,
        .pawl_friction = pw.friction_coefficient,
        .capture_radial_m = pw.capture_zone.radial_m,
        .capture_axial_m = pw.capture_zone.axial_m,
        .guide_enabled = sc.guide,
        .guide_mu_static = sc.friction.mu_static,
        .guide_mu_kinetic = sc.friction.mu_kinetic,
    };
}

/// The evaluator's description of the run. Built from the evaluation
/// criteria and the world's own coupler spec geometry.
fn bodiesFor(c: cc.Criteria, sc: Scenario, dt: f64) ce.Bodies {
    const axis = axisOf(sc.geometry);
    const spec = couplerSpec(c, sc);
    const seat_x = geometry.seatX(spec.geom, spec.ball_radius_m);
    const m = c.fixture.mass_kg;
    const i = inertiaOf(c);
    return .{
        .body = .{ .{ .mass_kg = m, .inertia_kg_m2 = i, .is_static = sc.geometry == .hang }, .{ .mass_kg = m, .inertia_kg_m2 = i } },
        .half_edge_m = edgeOf(c) / 2.0,
        .dt_s = dt,
        .gravity_m_s2 = m3.scale(c.gravity.direction_world, c.gravity.magnitude_m_s2),
        .axes_a = ce.couplerAxes(axis),
        .anchor_a_m = m3.scale(axis, spec.face_offset_a_m + seat_x - spec.preload_offset_m),
        .anchor_b_m = spec.ball_centre_b_m,
        .face_offset_a_m = spec.face_offset_a_m,
        .ball_centre_b_m = spec.ball_centre_b_m,
        .k_contact_n_m = c.stand_in.guide_contact.contact_stiffness_n_m,
    };
}

fn stepsFor(ctx: Ctx, duration_s: f64, step_ticks: u64) !u64 {
    const ticks = try ticksOf(ctx, duration_s);
    if (ticks % step_ticks != 0) return error.DurationNotWholeSteps;
    return ticks / step_ticks;
}

fn ticksOf(ctx: Ctx, seconds: f64) !u64 {
    const ticks_f = seconds * @as(f64, @floatFromInt(ctx.unit.denominator)) / @as(f64, @floatFromInt(ctx.unit.numerator));
    const ticks: u64 = @intFromFloat(@round(ticks_f));
    if (@as(f64, @floatFromInt(ticks)) != ticks_f) return error.DurationNotWholeSteps;
    return ticks;
}

// --- Samples ---

fn takeSample(world: *const rigid.World, t_s: f64, stepped: bool, cmd: backend.Command, loads: []const ce.Load) !ce.Sample {
    var s: ce.Sample = .{ .t_s = t_s };
    for (0..2) |i| {
        const b = world.bodies.items[i];
        s.pos[i] = b.position_m;
        s.quat[i] = b.orientation;
        s.vel[i] = b.velocity_m_s;
        s.omega[i] = b.angular_velocity_rad_s;
    }
    const cp = world.couplers.items[0];
    if (stepped) {
        if (world.reports.items.len > ce.max_contacts or loads.len > ce.max_loads) return error.SampleCapacityExceeded;
        for (world.reports.items, 0..) |r, i| s.contacts[i] = .{
            .body_a = r.body_a,
            .body_b = r.body_b,
            .point_m = r.world_point_m,
            .normal = r.world_normal,
            .normal_force_n = r.normal_force_n,
            .tangential_force_n = r.tangential_force_n,
        };
        s.n_contacts = world.reports.items.len;
        for (loads, 0..) |l, i| s.loads[i] = l;
        s.n_loads = loads.len;
        const lr = world.link_reports.items[0];
        s.force_b_n = lr.force_on_b_n;
        s.moment_b_nm = lr.moment_on_b_nm;
        s.extension_m = lr.extension_m;
        s.rotation_rad = lr.rotation_rad;
        const cr = world.coupler_reports.items[0];
        s.u_m = cr.u_m;
        s.e_during = cr.e_during;
        s.e_after = cr.e_after;
        s.active_during = cr.active_during;
        s.active_after = cr.active_after;
        s.pawl_work_j = cr.pawl_work_j;
        s.command = cmd;
    } else {
        const lr = world.linkGeometryReport(0);
        s.extension_m = lr.extension_m;
        s.rotation_rad = lr.rotation_rad;
        // Sample 0 is the initial state: the link has rows iff it is active.
        const e = cp.u_m / cp.spec.travel_m;
        const active = world.links.items[0].active;
        s.u_m = cp.u_m;
        s.e_during = e;
        s.e_after = e;
        s.active_during = active;
        s.active_after = active;
    }
    return s;
}

const StepLoads = struct {
    applied: [2]backend.AppliedLoad = undefined,
    rec: [2]ce.Load = undefined,
    n: usize = 0,
    /// C3 applied magnitude L(t) (0 otherwise).
    magnitude: f64 = 0,

    fn add(self: *StepLoads, body: u32, force: m3.Vec3, torque: m3.Vec3, point: m3.Vec3) void {
        self.applied[self.n] = .{ .body_index = body, .world_force_n = force, .world_torque_nm = torque, .world_point_m = point };
        self.rec[self.n] = .{ .body = body, .force_n = force, .torque_nm = torque, .point_m = point };
        self.n += 1;
    }

    fn appliedSlice(self: *const StepLoads) []const backend.AppliedLoad {
        return self.applied[0..self.n];
    }

    fn recSlice(self: *const StepLoads) []const ce.Load {
        return self.rec[0..self.n];
    }
};

/// Validation loads of step `t_s`' sample (protocol "C3 loads": directions are
/// the world axes at t = 0, force points the world anchor positions at step
/// start, magnitude L(t_n) of the sample the step produces).
fn stepLoads(c: cc.Criteria, sc: Scenario, world: *const rigid.World, axes0: [3]m3.Vec3, t_s: f64) StepLoads {
    var out: StepLoads = .{};
    switch (sc.load) {
        .none => {},
        .pull => |f_val| out.add(1, m3.scale(axes0[0], f_val), m3.zero, world.bodies.items[1].position_m),
        .limit => |l| {
            const sp = world.links.items[0].spec;
            const a = world.bodies.items[0];
            const b = world.bodies.items[1];
            const pa = m3.add(a.position_m, a.orientation.rotate(sp.anchor_a_m));
            const pb = m3.add(b.position_m, b.orientation.rotate(sp.anchor_b_m));
            const mag = ce.loadAt(c, l.axis, l.e, l.factor, t_s);
            out.magnitude = mag;
            const dir = if (l.axis == .shear or l.axis == .bending) axes0[1] else axes0[0];
            const v = m3.scale(dir, mag);
            const nv = m3.scale(dir, -mag);
            switch (l.axis) {
                .tension, .shear => {
                    out.add(1, v, m3.zero, pb);
                    out.add(0, nv, m3.zero, pa);
                },
                .bending, .torsion => {
                    out.add(1, m3.zero, v, pb);
                    out.add(0, m3.zero, nv, pa);
                },
            }
        },
    }
    return out;
}

const RunResult = struct {
    samples: []ce.Sample,
    /// L(t_n) applied per sample (C3), zero elsewhere; `samples.len` long.
    load_n: []f64,
    hash: []const u8,
    steps: u64,
};

/// Simulates one run. With `collect` false only the hash is produced (the
/// replay). Samples are owned by `ctx.scratch`, the hash by `ctx.arena`.
fn simulate(ctx: Ctx, sc: Scenario, step_ticks: u64, collect: bool) !RunResult {
    const c = ctx.built();
    const g = c.gravity.magnitude_m_s2;
    const edge = edgeOf(c);
    const half = edge / 2.0;
    const m = c.fixture.mass_kg;
    const dt = ctx.unit.seconds(.{ .ticks = step_ticks });
    const axis = axisOf(sc.geometry);

    var world: rigid.World = .{
        .gpa = ctx.scratch,
        .settings = ctx.solver.settings,
        .link_settings = ctx.solver.link_settings,
        .friction = .{ .mu_static = 0, .mu_kinetic = 0 }, // no tabletop contact occurs in any coupler setup
        .gravity_m_s2 = m3.scale(c.gravity.direction_world, g),
        .allow_static_bodies = true,
    };
    defer world.deinit();

    const spec = couplerSpec(c, sc);
    const seat_x = geometry.seatX(spec.geom, spec.ball_radius_m);
    const size: m3.Vec3 = c.fixture.size_m;
    const pa = centreA(sc.geometry);
    var a = rigid.cuboid(m, size, 0);
    a.position_m = pa;
    if (sc.geometry == .hang) a.is_static = true;
    var b = rigid.cuboid(m, size, 0);
    // B's centre: ball centre at the seat point (plus offset), stem and half edge behind it.
    b.position_m = m3.add(pa, m3.scale(axis, half + seat_x + (half + c.stand_in.probe.stem_length_m) + sc.offset_axial_m));
    if (sc.twist_rad != 0) {
        const h = 0.5 * sc.twist_rad;
        b.orientation = .{ .w = @cos(h), .x = axis[0] * @sin(h), .y = axis[1] * @sin(h), .z = axis[2] * @sin(h) };
    }
    _ = try world.addBody(a);
    _ = try world.addBody(b);
    _ = try world.addCoupler(spec);
    world.setCoupler(0, sc.e0 * spec.travel_m, sc.link_active);

    const n = try stepsFor(ctx, sc.duration_s, step_ticks);
    const switch_ticks: ?u64 = if (sc.switch_s) |s| try ticksOf(ctx, s) else null;
    const axes0 = blk: {
        const ax = ce.couplerAxes(axis);
        break :blk [3]m3.Vec3{ ax[0], ax[1], ax[2] };
    };

    const samples: []ce.Sample = if (collect) try ctx.scratch.alloc(ce.Sample, n + 1) else &.{};
    const load_n: []f64 = if (collect) try ctx.scratch.alloc(f64, n + 1) else &.{};
    if (collect) {
        samples[0] = try takeSample(&world, 0, false, .hold, &.{});
        load_n[0] = 0;
        // part 2: recorder hook, initial snapshot.
    }
    for (1..n + 1) |i| {
        const t_s = ctx.unit.seconds(.{ .ticks = i * step_ticks });
        const start_ticks = (i - 1) * step_ticks;
        const cmd: backend.Command = if (switch_ticks) |st| (if (start_ticks >= st) sc.command_then else sc.command_first) else sc.command_first;
        const loads = stepLoads(c, sc, &world, axes0, t_s);
        const cmds = [1]backend.Command{cmd};
        try world.step(dt, .{ .validation_loads = loads.appliedSlice(), .coupler_commands = &cmds });
        if (collect) {
            samples[i] = try takeSample(&world, t_s, true, cmd, loads.recSlice());
            load_n[i] = loads.magnitude;
            // part 2: recorder hook, per-step snapshot.
        }
    }

    var sink: canonical.BufferSink = .{ .gpa = ctx.scratch };
    defer sink.deinit();
    try world.encodeState(sink.encoder());
    var digest: [32]u8 = undefined;
    std.crypto.hash.sha2.Sha256.hash(sink.list.items, &digest, .{});
    const hex = std.fmt.bytesToHex(digest, .lower);
    return .{ .samples = samples, .load_n = load_n, .hash = try ctx.arena.dupe(u8, &hex), .steps = n };
}

// --- Evaluation packaging ---

const max_evals = 8;

const EvalList = struct {
    items: [max_evals]ce.Evaluation = undefined,
    len: usize = 0,

    fn add(self: *EvalList, e: ce.Evaluation) void {
        self.items[self.len] = e;
        self.len += 1;
    }

    /// The audits that apply to every C1-C7 run; energy only where the
    /// protocol lists it (C4, C6, C7: free fall without validation loads).
    fn addAudits(self: *EvalList, c: cc.Criteria, b: ce.Bodies, samples: []const ce.Sample, with_energy: bool) void {
        self.add(ce.auditMomentum(c, b, samples));
        self.add(ce.auditImpulse(c, b, samples));
        self.add(ce.auditPose(b, samples));
        if (with_energy) self.add(ce.auditEnergy(c, b, samples));
    }

    fn slice(self: *const EvalList) []const ce.Evaluation {
        return self.items[0..self.len];
    }
};

fn subRun(ctx: Ctx, name: []const u8, run1: RunResult, replay_hash: []const u8, evals: []const ce.Evaluation) !SubRun {
    var total: usize = 0;
    for (evals) |e| total += e.len;
    const metrics = try ctx.arena.alloc(ReportMetric, total);
    var i: usize = 0;
    var all_passed = total > 0;
    for (evals) |e| {
        if (!e.passed()) all_passed = false;
        for (e.slice()) |m| {
            metrics[i] = .{
                .name = m.name,
                .value = if (std.math.isFinite(m.value)) m.value else null,
                .limit = m.limit,
                .at_least = m.at_least,
                .informational = m.informational,
                .passed = m.passed(),
            };
            i += 1;
        }
    }
    return .{ .name = name, .steps = run1.steps, .final_state_sha256 = run1.hash, .replay_identical = std.mem.eql(u8, run1.hash, replay_hash), .metrics = metrics, .passed = all_passed };
}

fn combination(ctx: Ctx, label: []const u8, step_ticks: u64, omega_dt: ?f64, sub: SubRun) !Combination {
    const subs = try ctx.arena.alloc(SubRun, 1);
    subs[0] = sub;
    return .{ .grid_id = label, .physics_step_ticks = step_ticks, .status = if (sub.passed) .pass else .fail, .omega_dt = omega_dt, .sub_runs = subs };
}

/// Runs a scenario, its replay, and returns the packaged combination.
/// `evaluate` fills the evaluation list from the run.
fn execute(ctx: Ctx, label: []const u8, sc: Scenario, step_ticks: u64, omega_dt: ?f64, comptime Evaluate: type, args: Evaluate) !Combination {
    const dt = ctx.unit.seconds(.{ .ticks = step_ticks });
    const r = try simulate(ctx, sc, step_ticks, true);
    const replay = try simulate(ctx, sc, step_ticks, false);
    const b = bodiesFor(ctx.built(), sc, dt);
    var evs: EvalList = .{};
    try args.fill(ctx, b, r, &evs);
    return combination(ctx, label, step_ticks, omega_dt, try subRun(ctx, label, r, replay.hash, evs.slice()));
}

// --- Cases ---

const StaticEval = struct {
    which: enum { c1, c2_below, c2_above },
    fn fill(self: StaticEval, ctx: Ctx, b: ce.Bodies, r: RunResult, evs: *EvalList) !void {
        const c = ctx.c;
        evs.add(switch (self.which) {
            .c1 => ce.c1(c, b, r.samples),
            .c2_below => ce.c2Below(c, b, r.samples),
            .c2_above => ce.c2Above(c, b, r.samples),
        });
        evs.addAudits(c, b, r.samples, false);
    }
};

fn hangScenario(c: cc.Criteria, friction: cc.GuideFriction, duration_s: f64, load: LoadSpec) Scenario {
    return .{
        .geometry = .hang,
        .guide = true,
        .friction = friction,
        .e0 = 1.0,
        .link_active = true,
        .zeta = c.stand_in.latch_link.full_damping_ratio,
        .duration_s = duration_s,
        .command_first = .hold,
        .command_then = .hold,
        .load = load,
    };
}

fn weightOf(c: cc.Criteria) f64 {
    return c.fixture.mass_kg * c.gravity.magnitude_m_s2;
}

fn runC1(ctx: Ctx, step_ticks: u64) !Combination {
    const c = ctx.built();
    const sc = hangScenario(c, c.statics.guide_friction, c.statics.duration_s, .none);
    return execute(ctx, "hang", sc, step_ticks, null, StaticEval, .{ .which = .c1 });
}

fn runC2(ctx: Ctx, step_ticks: u64, above: bool) !Combination {
    const c = ctx.built();
    const sep = c.statics.seat_separation;
    const factor = if (above) sep.above_factor else sep.below_factor;
    // Total pull F = m·g + F_val = factor·F_sep.
    const f_val = factor * ce.separationForce(c, 1.0) - weightOf(c);
    const sc = hangScenario(c, c.statics.guide_friction, c.statics.duration_s, .{ .pull = f_val });
    return execute(ctx, if (above) "above" else "below", sc, step_ticks, null, StaticEval, .{ .which = if (above) .c2_above else .c2_below });
}

const LimitEval = struct {
    axis: cc.Axis,
    e: f64,
    above: bool,
    fn fill(self: LimitEval, ctx: Ctx, b: ce.Bodies, r: RunResult, evs: *EvalList) !void {
        const c = ctx.c;
        evs.add(if (self.above) ce.c3Above(c, self.axis, self.e, r.samples, r.load_n) else ce.c3Below(c, self.axis, self.e, r.samples));
        evs.addAudits(c, b, r.samples, false);
    }
};

fn runC3(ctx: Ctx, step_ticks: u64, axis: cc.Axis, e: f64, above: bool) !Combination {
    const c = ctx.built();
    const l = c.link_limits;
    const sc: Scenario = .{
        .geometry = .free,
        .guide = false,
        .e0 = e,
        .link_active = true,
        .offset_axial_m = -c.stand_in.latch_link.preload_offset_m,
        .zeta = c.stand_in.latch_link.full_damping_ratio,
        .duration_s = l.duration_s,
        .command_first = .hold,
        .command_then = .hold,
        .load = .{ .limit = .{ .axis = axis, .e = e, .factor = if (above) l.above_factor else l.below_factor } },
    };
    const label = try std.fmt.allocPrint(ctx.arena, "{s}_e{d:.1}_{s}", .{ @tagName(axis), e, if (above) "above" else "below" });
    return execute(ctx, label, sc, step_ticks, null, LimitEval, .{ .axis = axis, .e = e, .above = above });
}

const FreeEval = struct {
    which: enum { c4_engage, c4_blocked, c6 },
    fn fill(self: FreeEval, ctx: Ctx, b: ce.Bodies, r: RunResult, evs: *EvalList) !void {
        const c = ctx.c;
        evs.add(switch (self.which) {
            .c4_engage => ce.c4Engage(c, b, r.samples),
            .c4_blocked => ce.c4Blocked(r.samples),
            .c6 => ce.c6(c, b, r.samples),
        });
        evs.addAudits(c, b, r.samples, true);
    }
};

fn runC4(ctx: Ctx, step_ticks: u64, blocked: bool) !Combination {
    const c = ctx.built();
    const en = c.engagement;
    const sc: Scenario = .{
        .geometry = .free,
        .guide = true,
        .friction = en.guide_friction,
        .e0 = 0,
        .link_active = false,
        .offset_axial_m = if (blocked) en.blocked_axial_offset_m else 0,
        .zeta = c.stand_in.latch_link.full_damping_ratio,
        .duration_s = en.duration_s,
        .command_first = .engage,
        .command_then = .engage,
    };
    return execute(ctx, if (blocked) "blocked" else "engage", sc, step_ticks, null, FreeEval, .{ .which = if (blocked) .c4_blocked else .c4_engage });
}

const ReleaseEval = struct {
    above: bool,
    force_n: f64,
    fn fill(self: ReleaseEval, ctx: Ctx, b: ce.Bodies, r: RunResult, evs: *EvalList) !void {
        const c = ctx.c;
        evs.add(if (self.above) ce.c5Above(c, r.samples) else ce.c5Below(c, b, r.samples, self.force_n));
        evs.addAudits(c, b, r.samples, false);
    }
};

fn runC5(ctx: Ctx, step_ticks: u64, above: bool) !Combination {
    const c = ctx.built();
    const r = c.release_under_load;
    const factor = if (above) r.above_factor else r.below_factor;
    // Total axial pull F = m·g + F_val = factor·T_block.
    const force = factor * ce.blockTension(c);
    var sc = hangScenario(c, r.guide_friction, r.duration_s, .{ .pull = force - weightOf(c) });
    sc.command_then = .release;
    sc.switch_s = r.release_start_s;
    return execute(ctx, if (above) "above" else "below", sc, step_ticks, null, ReleaseEval, .{ .above = above, .force_n = force });
}

fn runC6(ctx: Ctx, step_ticks: u64) !Combination {
    const c = ctx.built();
    const u = c.unloaded_release;
    const sc: Scenario = .{
        .geometry = .free,
        .guide = true,
        .friction = u.guide_friction,
        .e0 = 1.0,
        .link_active = true,
        .zeta = c.stand_in.latch_link.full_damping_ratio,
        .duration_s = u.duration_s,
        .command_first = .hold,
        .command_then = .release,
        .switch_s = u.release_start_s,
    };
    return execute(ctx, "unloaded", sc, step_ticks, null, FreeEval, .{ .which = .c6 });
}

const C7Eval = struct {
    kind: ce.C7Kind,
    e: f64,
    /// The ζ = 0 runs are scored for period and numerical dissipation
    /// (axial) or period (torsion); the ζ = 0.05 run for damping.
    damped: bool,
    fn fill(self: C7Eval, ctx: Ctx, b: ce.Bodies, r: RunResult, evs: *EvalList) !void {
        const c = ctx.c;
        const buf = try ctx.scratch.alloc(le.Sample, r.samples.len);
        const ls = ce.toLinkSamples(buf, r.samples);
        if (self.damped) {
            evs.add(ce.c7Damping(c, ls));
        } else {
            evs.add(ce.c7Period(c, b, self.kind, self.e, ls));
            if (self.kind == .axial) evs.add(ce.c7Numerical(c, ls));
        }
        evs.addAudits(c, b, r.samples, true);
    }
};

fn runC7(ctx: Ctx, step_ticks: u64, kind: ce.C7Kind, e: f64, damped: bool) !Combination {
    const c = ctx.built();
    const d = c.stiff_dynamics;
    const dt = ctx.unit.seconds(.{ .ticks = step_ticks });
    const zeta: f64 = if (damped) d.physical_damping_ratio else 0;
    const label = try std.fmt.allocPrint(ctx.arena, "{s}_e{d:.1}_zeta{d}", .{ @tagName(kind), e, zeta });
    var sc: Scenario = .{
        .geometry = .free,
        .guide = false,
        .e0 = e,
        .link_active = true,
        .offset_axial_m = -c.stand_in.latch_link.preload_offset_m,
        .zeta = zeta,
        .zeta_at_e = e,
        .duration_s = d.duration_s,
        .command_first = .hold,
        .command_then = .hold,
    };
    switch (kind) {
        .axial => sc.offset_axial_m += d.initial_stretch_m,
        .torsion => sc.twist_rad = d.initial_twist_rad,
    }
    const b = bodiesFor(ctx.c, sc, dt);
    const omega_dt = ce.c7Omega(ctx.c, b, kind, e) * dt;
    if (!ce.c7Resolved(ctx.c, b, kind, e)) {
        return .{ .grid_id = label, .physics_step_ticks = step_ticks, .status = .outside_envelope, .omega_dt = omega_dt, .sub_runs = &.{} };
    }
    return execute(ctx, label, sc, step_ticks, omega_dt, C7Eval, .{ .kind = kind, .e = e, .damped = damped });
}

fn caseReport(arena: std.mem.Allocator, id: []const u8, combos: []const Combination) !CaseReport {
    const statuses = try arena.alloc(le.Status, combos.len);
    var evaluated: usize = 0;
    var outside: usize = 0;
    for (combos, statuses) |cb, *s| {
        s.* = cb.status;
        if (cb.status == .outside_envelope) outside += 1 else evaluated += 1;
    }
    return .{ .case_id = id, .outcome = le.combine(statuses), .evaluated = evaluated, .outside_envelope = outside, .combinations = combos };
}

/// The case ids this part of the suite reports, in report order.
pub fn caseIds(c: cc.Criteria) [8][]const u8 {
    return .{
        c.statics.seated_preload.id,
        c.statics.seat_separation.id,
        c.link_limits.id,
        c.engagement.id,
        c.release_under_load.id,
        c.unloaded_release.id,
        c.stiff_dynamics.id,
        c.determinism.id,
    };
}

const Job = enum { c1, c2, c3, c4, c5, c6, c7 };

fn runJob(ctx: Ctx, job: Job, step_ticks: u64, out: *std.ArrayList(Combination)) !void {
    const c = ctx.c;
    const arena = ctx.arena;
    switch (job) {
        .c1 => try out.append(arena, try runC1(ctx, step_ticks)),
        .c2 => {
            try out.append(arena, try runC2(ctx, step_ticks, false));
            try out.append(arena, try runC2(ctx, step_ticks, true));
        },
        .c3 => for (c.link_limits.axes) |axis| for (c.link_limits.engagements) |e| {
            try out.append(arena, try runC3(ctx, step_ticks, axis, e, false));
            try out.append(arena, try runC3(ctx, step_ticks, axis, e, true));
        },
        .c4 => {
            try out.append(arena, try runC4(ctx, step_ticks, false));
            try out.append(arena, try runC4(ctx, step_ticks, true));
        },
        .c5 => {
            try out.append(arena, try runC5(ctx, step_ticks, false));
            try out.append(arena, try runC5(ctx, step_ticks, true));
        },
        .c6 => try out.append(arena, try runC6(ctx, step_ticks)),
        .c7 => for (c.stiff_dynamics.engagements) |e| {
            try out.append(arena, try runC7(ctx, step_ticks, .axial, e, false));
            try out.append(arena, try runC7(ctx, step_ticks, .axial, e, true));
            try out.append(arena, try runC7(ctx, step_ticks, .torsion, e, false));
        },
    }
}

/// Official run: protocol settings, labeled `fixture`.
/// Report memory is owned by `arena`; per-run sample buffers use `scratch`
/// and are freed as each combination completes.
pub fn run(arena: std.mem.Allocator, scratch: std.mem.Allocator, c: cc.Criteria, identity: CriteriaIdentity, recorder: ?Recorder) !Report {
    const base: Ctx = .{
        .arena = arena,
        .scratch = scratch,
        .c = c,
        .unit = .{ .numerator = c.time_unit.numerator_s, .denominator = c.time_unit.denominator_s },
        .recorder = recorder,
    };
    const ids = caseIds(c);
    var cases: std.ArrayList(CaseReport) = .empty;
    var all: std.ArrayList(Combination) = .empty;
    for ([_]Job{ .c1, .c2, .c3, .c4, .c5, .c6, .c7 }, 0..) |job, ji| {
        var combos: std.ArrayList(Combination) = .empty;
        for (c.physics_step_ticks) |st| {
            var sc = std.heap.ArenaAllocator.init(scratch);
            defer sc.deinit();
            var sub_ctx = base;
            sub_ctx.scratch = sc.allocator();
            const before = combos.items.len;
            try runJob(sub_ctx, job, st, &combos);
            try all.appendSlice(arena, combos.items[before..]);
        }
        try cases.append(arena, try caseReport(arena, ids[ji], try combos.toOwnedSlice(arena)));
    }

    // part 2: C8 capture sweep and C9 audit-discrimination controls run here.

    // C10: per physics step, every executed run replayed bit-identically.
    var c10: std.ArrayList(Combination) = .empty;
    for (c.physics_step_ticks) |st| {
        var ok = true;
        var any = false;
        for (all.items) |cb| {
            if (cb.physics_step_ticks != st) continue;
            for (cb.sub_runs) |s| {
                any = true;
                ok = ok and s.replay_identical;
            }
        }
        try c10.append(arena, .{ .grid_id = "all_runs", .physics_step_ticks = st, .status = if (any and ok) .pass else .fail, .omega_dt = null, .sub_runs = &.{} });
    }
    try cases.append(arena, try caseReport(arena, ids[7], try c10.toOwnedSlice(arena)));

    return .{
        .criteria_path = identity.path,
        .criteria_sha256 = identity.sha256,
        .solver_name = "kinigami-rigid",
        .solver_version = "0.1.0",
        .solver_settings = base.solver.settings,
        .link_settings = base.solver.link_settings,
        .cases = try cases.toOwnedSlice(arena),
    };
}

// --- Tests ---

const testing = std.testing;

fn testCtx(arena: std.mem.Allocator, c: cc.Criteria) Ctx {
    return .{ .arena = arena, .scratch = arena, .c = c, .unit = .{ .numerator = c.time_unit.numerator_s, .denominator = c.time_unit.denominator_s } };
}

test "wiring: the suite's case list equals the criteria ids, in order, C8 and C9 left to part 2" {
    const parsed = try cc.parse(testing.allocator, cc.coupler_v1_json);
    defer parsed.deinit();
    const c = parsed.value;
    const ids = caseIds(c);
    try testing.expectEqualStrings("C1_seated_preload_statics", ids[0]);
    try testing.expectEqualStrings(c.statics.seat_separation.id, ids[1]);
    try testing.expectEqualStrings(c.link_limits.id, ids[2]);
    try testing.expectEqualStrings(c.engagement.id, ids[3]);
    try testing.expectEqualStrings(c.release_under_load.id, ids[4]);
    try testing.expectEqualStrings(c.unloaded_release.id, ids[5]);
    try testing.expectEqualStrings(c.stiff_dynamics.id, ids[6]);
    try testing.expectEqualStrings(c.determinism.id, ids[7]);
    const prefixes = [_][]const u8{ "C1_", "C2_", "C3_", "C4_", "C5_", "C6_", "C7_", "C10_" };
    for (ids, prefixes) |id, p| try testing.expect(std.mem.startsWith(u8, id, p));
    // The ids exclude the part 2 cases.
    for (ids) |id| {
        try testing.expect(!std.mem.eql(u8, id, c.capture_sweep.id));
        try testing.expect(!std.mem.eql(u8, id, c.audit_discrimination.id));
    }
}

test "C1 at 200 us runs, audits included, and passes" {
    const parsed = try cc.parse(testing.allocator, cc.coupler_v1_json);
    defer parsed.deinit();
    var arena = std.heap.ArenaAllocator.init(testing.allocator);
    defer arena.deinit();
    const cb = try runC1(testCtx(arena.allocator(), parsed.value), 200);
    const s = cb.sub_runs[0];
    for (s.metrics) |m| if (!m.passed) std.debug.print("C1 failing metric {s}: {?e} limit {e}\n", .{ m.name, m.value, m.limit });
    try testing.expectEqual(le.Status.pass, cb.status);
    try testing.expect(s.replay_identical);
    // Case metrics plus momentum (n/a), impulse x2, pose x2.
    try testing.expectEqual(@as(usize, 4 + 1 + 2 + 2), s.metrics.len);
}

test "C7 axial at 50 us (e = 1, zeta = 0): period, numerical dissipation and every audit but energy pass" {
    const parsed = try cc.parse(testing.allocator, cc.coupler_v1_json);
    defer parsed.deinit();
    var arena = std.heap.ArenaAllocator.init(testing.allocator);
    defer arena.deinit();
    const cb = try runC7(testCtx(arena.allocator(), parsed.value), 50, .axial, 1.0, false);
    // OPEN FINDING (reported, not tuned): the energy-creation audit fails at
    // ratio ~ omega*dt/2 / 2 % (first-order fluctuation of KE + V of the
    // semi-implicit step), so the combination as a whole does not pass.
    // Everything else must pass; the energy metric must be present.
    var energy_seen = false;
    for (cb.sub_runs) |s| for (s.metrics) |m| {
        if (std.mem.eql(u8, m.name, "energy_creation_over_allowance")) {
            energy_seen = true;
            std.debug.print("C7 axial 50us energy_creation_over_allowance {?e} (limit {e})\n", .{ m.value, m.limit });
            continue;
        }
        if (!m.passed) std.debug.print("C7 failing metric {s}: {?e} limit {e}\n", .{ m.name, m.value, m.limit });
        try testing.expect(m.passed);
    };
    try testing.expect(energy_seen);
    // Torsion at 200 us, e = 1, is beyond the resolution limit.
    const t = try runC7(testCtx(arena.allocator(), parsed.value), 200, .torsion, 1.0, false);
    try testing.expectEqual(le.Status.outside_envelope, t.status);
}

test "a deliberately wrong spec (halved preload offset) fails C1: the evaluators are not vacuous" {
    const parsed = try cc.parse(testing.allocator, cc.coupler_v1_json);
    defer parsed.deinit();
    var arena = std.heap.ArenaAllocator.init(testing.allocator);
    defer arena.deinit();
    var ctx = testCtx(arena.allocator(), parsed.value);
    var wrong = parsed.value;
    wrong.stand_in.latch_link.preload_offset_m *= 0.5;
    ctx.build_c = wrong;
    const cb = try runC1(ctx, 200);
    try testing.expectEqual(le.Status.fail, cb.status);
}

test "determinism: two runs of the same scenario give the same hashes" {
    const parsed = try cc.parse(testing.allocator, cc.coupler_v1_json);
    defer parsed.deinit();
    var arena = std.heap.ArenaAllocator.init(testing.allocator);
    defer arena.deinit();
    const ctx = testCtx(arena.allocator(), parsed.value);
    const a = try runC1(ctx, 200);
    const b = try runC1(ctx, 200);
    try testing.expectEqualStrings(a.sub_runs[0].final_state_sha256, b.sub_runs[0].final_state_sha256);
    try testing.expectEqual(@as(usize, 64), a.sub_runs[0].final_state_sha256.len);
    try testing.expect(a.sub_runs[0].replay_identical and b.sub_runs[0].replay_identical);
}
