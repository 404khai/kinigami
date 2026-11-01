//! Runs the analytic fixture-validation criteria against the rigid backend
//! (Q46–Q48). Every case runs at every (friction pair × physics step)
//! combination and is evaluated by `fixture_eval` (the committed protocol).
//! Results are always labeled `fixture` and are never benchmark or
//! Kin-candidate evidence (Q46).

const std = @import("std");
const m3 = @import("math3.zig");
const analytic = @import("analytic.zig");
const criteria = @import("criteria.zig");
const eval = @import("fixture_eval.zig");
const rigid = @import("rigid.zig");
const backend = @import("backend.zig");
const canonical = @import("canonical.zig");
const time = @import("time.zig");
const recording = @import("recording.zig");
const scene_record = @import("scene_record.zig");

/// Receives each run's finished recording (format v2, Q51). The core never
/// performs file I/O; the caller decides where recordings go. Recording only
/// reads simulation state and never feeds back into it (INS-007).
pub const Recorder = struct {
    ptr: *anyopaque,
    emit: *const fn (ptr: *anyopaque, name: []const u8, bytes: []const u8) anyerror!void,
};

/// Effective configuration stored as each recording's first chunk.
const FixtureRunConfig = struct {
    schema: []const u8 = "kinigami.fixture-run.v1",
    run_class: []const u8 = "fixture_validation",
    criteria_sha256: []const u8 = criteria.analytic_v1_sha256,
    protocol_revision: u32 = eval.protocol_revision,
    case_id: []const u8,
    sub_run: []const u8,
    friction_id: []const u8,
    mu_static: f64,
    mu_kinetic: f64,
    time_unit_numerator_s: u64,
    time_unit_denominator_s: u64,
    physics_step_ticks: u64,
    steps: u64,
    preroll_s: f64,
    initial_velocity_m_s: m3.Vec3,
    load_kind: []const u8,
    load_force_n: m3.Vec3,
    load_point_m: m3.Vec3,
    solver: rigid.Settings,
};

/// Solver configuration fixed in docs/validation/fixture-analytic-v1-protocol.md
/// before the first evaluation. Changing it requires a protocol revision entry.
/// Protocol revision 2: fixtures that start on the table are first settled,
/// unloaded, for this long; the evaluation clock starts afterwards.
pub const preroll_s: f64 = 0.5;

pub const protocol_settings: rigid.Settings = .{
    .contact_stiffness_n_m = 1.0e5,
    .contact_damping_n_s_m = 50,
    .static_slip_speed_m_s = 1e-5,
    .iterations = 100,
    .warm_start = true,
};

pub const SubRun = struct {
    name: []const u8,
    steps: u64,
    final_state_sha256: []const u8,
    metrics: []const eval.Metric,
    passed: bool,
};

pub const Combination = struct {
    friction_id: []const u8,
    physics_step_ticks: u64,
    passed: bool,
    sub_runs: []const SubRun,
};

pub const CaseReport = struct {
    case_id: []const u8,
    outcome: eval.CaseOutcome,
    combinations: []const Combination,
};

pub const Report = struct {
    schema_version: u32 = 1,
    run_class: []const u8 = "fixture_validation",
    label: []const u8 = "fixture",
    criteria_path: []const u8 = "criteria/fixture-validation/analytic-v1.json",
    criteria_sha256: []const u8 = criteria.analytic_v1_sha256,
    protocol: []const u8 = "docs/validation/fixture-analytic-v1-protocol.md",
    protocol_revision: u32 = eval.protocol_revision,
    preroll_s: f64 = preroll_s,
    solver_name: []const u8,
    solver_version: []const u8,
    solver_settings: rigid.Settings,
    cases: []const CaseReport,
};

const Load = union(enum) {
    none,
    /// World-frame force applied at the centre of mass.
    com_world: m3.Vec3,
    /// Body-frame force at a body-frame point.
    body: struct { force: m3.Vec3, point: m3.Vec3 },
};

const RunSpec = struct {
    name: []const u8,
    case_id: []const u8,
    fixture: criteria.Fixture,
    bottom_z_m: f64,
    initial_velocity_m_s: m3.Vec3 = m3.zero,
    duration_s: f64,
    load: Load = .none,
};

const Ctx = struct {
    arena: std.mem.Allocator,
    scratch: std.mem.Allocator,
    c: criteria.Criteria,
    g: f64,
    unit: time.TimeUnit,
    recorder: ?Recorder = null,
};

fn stepsFor(ctx: Ctx, duration_s: f64, step_ticks: u64) !u64 {
    const ticks_f = duration_s * @as(f64, @floatFromInt(ctx.unit.denominator)) / @as(f64, @floatFromInt(ctx.unit.numerator));
    const ticks: u64 = @intFromFloat(@round(ticks_f));
    if (@as(f64, @floatFromInt(ticks)) != ticks_f or ticks % step_ticks != 0) return error.DurationNotWholeSteps;
    return ticks / step_ticks;
}

/// Simulates one run, returning its samples (owned by `scratch`) and the
/// final canonical-state hash (owned by `arena`).
fn simulate(ctx: Ctx, spec: RunSpec, fr: criteria.FrictionPair, step_ticks: u64) !struct { samples: []eval.Sample, hash: []const u8, steps: u64 } {
    var world: rigid.World = .{
        .gpa = ctx.scratch,
        .settings = protocol_settings,
        .friction = .{ .mu_static = fr.mu_static, .mu_kinetic = fr.mu_kinetic },
        .gravity_m_s2 = m3.scale(ctx.c.gravity.direction_world, ctx.g),
    };
    defer world.deinit();
    _ = try world.addBody(rigid.cuboid(spec.fixture.mass_kg, spec.fixture.size_m, spec.bottom_z_m));

    const n = try stepsFor(ctx, spec.duration_s, step_ticks);
    const dt = ctx.unit.seconds(.{ .ticks = step_ticks });
    // Settle unloaded on the table before t = 0 (protocol revision 2), so the
    // run starts from the contact's own equilibrium rather than from an
    // uncompressed contact.
    if (spec.bottom_z_m == 0) {
        const pre = try stepsFor(ctx, preroll_s, step_ticks);
        for (0..pre) |_| try world.step(dt, .{});
    }
    world.bodies.items[0].velocity_m_s = m3.add(world.bodies.items[0].velocity_m_s, spec.initial_velocity_m_s);
    const samples = try ctx.scratch.alloc(eval.Sample, n + 1);
    samples[0] = sample(&world, 0);

    var rec: ?recording.Writer = null;
    defer if (rec) |*r| r.deinit();
    var snap_buf: canonical.BufferSink = .{ .gpa = ctx.scratch };
    defer snap_buf.deinit();
    if (ctx.recorder != null) {
        const load_kind: []const u8, const lf: m3.Vec3, const lp: m3.Vec3 = switch (spec.load) {
            .none => .{ "none", m3.zero, m3.zero },
            .com_world => |f| .{ "world_force_at_center_of_mass", f, m3.zero },
            .body => |l| .{ "body_force_at_body_point", l.force, l.point },
        };
        const cfg_json = try std.json.Stringify.valueAlloc(ctx.scratch, FixtureRunConfig{
            .case_id = spec.case_id,
            .sub_run = spec.name,
            .friction_id = fr.id,
            .mu_static = fr.mu_static,
            .mu_kinetic = fr.mu_kinetic,
            .time_unit_numerator_s = ctx.unit.numerator,
            .time_unit_denominator_s = ctx.unit.denominator,
            .physics_step_ticks = step_ticks,
            .steps = n,
            .preroll_s = if (spec.bottom_z_m == 0) preroll_s else 0,
            .initial_velocity_m_s = spec.initial_velocity_m_s,
            .load_kind = load_kind,
            .load_force_n = lf,
            .load_point_m = lp,
            .solver = protocol_settings,
        }, .{});
        rec = try recording.Writer.init(ctx.scratch, cfg_json);
        var hb: canonical.BufferSink = .{ .gpa = ctx.scratch };
        defer hb.deinit();
        try scene_record.encodeHeader(hb.encoder(), .{
            .time_unit_numerator_s = ctx.unit.numerator,
            .time_unit_denominator_s = ctx.unit.denominator,
            .physics_step_ticks = step_ticks,
            .snapshot_interval_steps = 1,
            .bodies = &.{.{ .id = spec.fixture.id, .kind = .fixture, .shape = .cuboid, .half_extents_m = m3.scale(spec.fixture.size_m, 0.5), .mass_kg = spec.fixture.mass_kg }},
        });
        try rec.?.sceneHeader(hb.list.items);
        try recordSnapshot(&rec.?, &snap_buf, &world, 0);
    }
    var loads: [1]backend.AppliedLoad = undefined;
    for (1..n + 1) |i| {
        const b = world.bodies.items[0];
        const inputs: backend.StepInputs = switch (spec.load) {
            .none => .{},
            .com_world => |f| blk: {
                loads[0] = .{ .body_index = 0, .world_force_n = f, .world_torque_nm = m3.zero, .world_point_m = b.position_m };
                break :blk .{ .validation_loads = &loads };
            },
            .body => |l| blk: {
                loads[0] = .{
                    .body_index = 0,
                    .world_force_n = b.orientation.rotate(l.force),
                    .world_torque_nm = m3.zero,
                    .world_point_m = m3.add(b.position_m, b.orientation.rotate(l.point)),
                };
                break :blk .{ .validation_loads = &loads };
            },
        };
        try world.step(dt, inputs);
        samples[i] = sample(&world, ctx.unit.seconds(.{ .ticks = i * step_ticks }));
        if (rec) |*r| try recordSnapshot(r, &snap_buf, &world, i * step_ticks);
    }
    if (rec) |*r| {
        const bytes = try r.finish();
        defer ctx.scratch.free(bytes);
        const name = try std.fmt.allocPrint(ctx.scratch, "{s}__{s}__dt{d}us__{s}.kgrec", .{ spec.case_id, fr.id, step_ticks, spec.name });
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

fn recordSnapshot(rec: *recording.Writer, buf: *canonical.BufferSink, w: *rigid.World, tick: u64) !void {
    var bodies: [1]scene_record.BodyState = undefined;
    const b = w.bodies.items[0];
    bodies[0] = .{
        .position_m = b.position_m,
        .orientation = .{ b.orientation.w, b.orientation.x, b.orientation.y, b.orientation.z },
        .velocity_m_s = b.velocity_m_s,
        .angular_velocity_rad_s = b.angular_velocity_rad_s,
    };
    var contacts: [8]scene_record.ContactRecord = undefined;
    const reports = w.reports.items;
    std.debug.assert(reports.len <= contacts.len);
    for (reports, 0..) |r, i| contacts[i] = .{
        .body_a = r.body_a,
        .body_b = r.body_b orelse scene_record.tabletop,
        .point_m = r.world_point_m,
        .normal = r.world_normal,
        .normal_force_n = r.normal_force_n,
        .tangential_force_n = r.tangential_force_n,
    };
    buf.list.clearRetainingCapacity();
    try scene_record.encodeSnapshot(buf.encoder(), .{ .tick = tick, .bodies = &bodies, .contacts = contacts[0..reports.len] });
    try rec.snapshot(buf.list.items);
}

fn sample(w: *rigid.World, t: f64) eval.Sample {
    const b = w.bodies.items[0];
    var fn_sum: f64 = 0;
    var ft: m3.Vec3 = m3.zero;
    var cop: m3.Vec3 = m3.zero;
    var pen: f64 = 0;
    for (w.reports.items) |r| {
        fn_sum += r.normal_force_n;
        ft = m3.add(ft, r.tangential_force_n);
        cop = m3.add(cop, m3.scale(r.world_point_m, r.normal_force_n));
        pen = @max(pen, -r.world_point_m[2]);
    }
    return .{
        .t_s = t,
        .position_m = b.position_m,
        .orientation = b.orientation,
        .velocity_m_s = b.velocity_m_s,
        .angular_velocity_rad_s = b.angular_velocity_rad_s,
        .normal_force_sum_n = fn_sum,
        .tangential_force_sum_n = ft,
        .center_of_pressure_m = if (fn_sum > 0) m3.scale(cop, 1.0 / fn_sum) else null,
        .max_penetration_m = pen,
    };
}

fn fixtureById(c: criteria.Criteria, id: []const u8) criteria.Fixture {
    for (c.fixtures) |f| if (std.mem.eql(u8, f.id, id)) return f;
    unreachable; // criteria.validate guarantees resolution
}

fn subRun(ctx: Ctx, name: []const u8, steps: u64, hash: []const u8, e: eval.Evaluation) !SubRun {
    return .{ .name = name, .steps = steps, .final_state_sha256 = hash, .metrics = try ctx.arena.dupe(eval.Metric, e.slice()), .passed = e.passed() };
}

const CaseKind = enum { rest, free_fall, friction_threshold, slide_to_stop, tipping };

fn runCombination(ctx: Ctx, kind: CaseKind, case_id: []const u8, fr: criteria.FrictionPair, step_ticks: u64) ![]const SubRun {
    const c = ctx.c;
    const g = ctx.g;
    const dt = ctx.unit.seconds(.{ .ticks = step_ticks });
    var out: std.ArrayList(SubRun) = .empty;
    switch (kind) {
        .rest => {
            const f = fixtureById(c, c.rest.fixture);
            const r = try simulate(ctx, .{ .name = "rest", .case_id = case_id, .fixture = f, .bottom_z_m = 0, .duration_s = c.rest.duration_s }, fr, step_ticks);
            try out.append(ctx.arena, try subRun(ctx, "rest", r.steps, r.hash, eval.rest(c.rest, f, g, r.samples)));
        },
        .free_fall => {
            const f = fixtureById(c, c.free_fall.fixture);
            const r = try simulate(ctx, .{ .name = "free_fall", .case_id = case_id, .fixture = f, .bottom_z_m = c.free_fall.initial_clearance_m, .duration_s = c.free_fall.duration_s }, fr, step_ticks);
            const z0 = c.free_fall.initial_clearance_m + f.size_m[2] / 2.0;
            try out.append(ctx.arena, try subRun(ctx, "free_fall", r.steps, r.hash, eval.freeFall(c.free_fall, g, dt, z0, r.samples)));
        },
        .friction_threshold => {
            const t = c.friction_threshold;
            const f = fixtureById(c, t.fixture);
            const threshold = analytic.slidingThreshold(f.mass_kg, g, fr.mu_static);
            const below = t.below_factor * threshold;
            const rb = try simulate(ctx, .{ .name = "below", .case_id = case_id, .fixture = f, .bottom_z_m = 0, .duration_s = t.duration_s, .load = .{ .com_world = m3.scale(t.direction_world, below) } }, fr, step_ticks);
            try out.append(ctx.arena, try subRun(ctx, "below_threshold", rb.steps, rb.hash, eval.frictionBelow(t, below, rb.samples)));
            const above = t.above_factor * threshold;
            const ra = try simulate(ctx, .{ .name = "above", .case_id = case_id, .fixture = f, .bottom_z_m = 0, .duration_s = t.duration_s, .load = .{ .com_world = m3.scale(t.direction_world, above) } }, fr, step_ticks);
            const a_ref = analytic.slidingAcceleration(f.mass_kg, g, fr.mu_kinetic, above);
            try out.append(ctx.arena, try subRun(ctx, "above_threshold", ra.steps, ra.hash, eval.frictionAbove(t, a_ref, ra.samples)));
        },
        .slide_to_stop => {
            const s = c.slide_to_stop;
            const f = fixtureById(c, s.fixture);
            const r = try simulate(ctx, .{ .name = "slide", .case_id = case_id, .fixture = f, .bottom_z_m = 0, .duration_s = s.duration_s, .initial_velocity_m_s = m3.scale(s.direction_world, s.initial_speed_m_s) }, fr, step_ticks);
            try out.append(ctx.arena, try subRun(ctx, "slide_to_stop", r.steps, r.hash, eval.slideToStop(s, f, g, fr.mu_kinetic, dt, r.samples)));
        },
        .tipping => {
            const t = c.tipping;
            const f = fixtureById(c, t.fixture);
            const h = t.application_point_body_m[2] + f.size_m[2] / 2.0;
            const threshold = analytic.tippingThreshold(f.mass_kg, g, f.size_m[0] / 2.0, h);
            inline for (.{ .{ "below_threshold", false }, .{ "above_threshold", true } }) |variant| {
                const factor = if (variant[1]) t.above_factor else t.below_factor;
                const r = try simulate(ctx, .{ .name = variant[0], .case_id = case_id, .fixture = f, .bottom_z_m = 0, .duration_s = t.duration_s, .load = .{ .body = .{ .force = m3.scale(t.force_direction_body, factor * threshold), .point = t.application_point_body_m } } }, fr, step_ticks);
                const e = if (variant[1]) eval.tippingAbove(t, f, r.samples) else eval.tippingBelow(t, r.samples);
                try out.append(ctx.arena, try subRun(ctx, variant[0], r.steps, r.hash, e));
            }
        },
    }
    return out.toOwnedSlice(ctx.arena);
}

/// Runs the whole suite. Report memory is owned by `arena`; per-run sample
/// buffers use `scratch` and are freed as each run completes.
pub fn run(arena: std.mem.Allocator, scratch: std.mem.Allocator, c: criteria.Criteria, recorder: ?Recorder) !Report {
    const ctx: Ctx = .{
        .arena = arena,
        .scratch = scratch,
        .c = c,
        .g = c.gravity.magnitude_m_s2,
        .unit = .{ .numerator = c.time_unit.numerator_s, .denominator = c.time_unit.denominator_s },
        .recorder = recorder,
    };
    const kinds = [_]struct { CaseKind, []const u8 }{
        .{ .rest, c.rest.id },
        .{ .free_fall, c.free_fall.id },
        .{ .friction_threshold, c.friction_threshold.id },
        .{ .slide_to_stop, c.slide_to_stop.id },
        .{ .tipping, c.tipping.id },
    };
    var cases: std.ArrayList(CaseReport) = .empty;
    for (kinds) |k| {
        var combos: std.ArrayList(Combination) = .empty;
        var passes: std.ArrayList(bool) = .empty;
        for (c.friction_grid) |fr| for (c.physics_step_ticks) |st| {
            var sc = std.heap.ArenaAllocator.init(scratch);
            defer sc.deinit();
            var sub_ctx = ctx;
            sub_ctx.scratch = sc.allocator();
            const subs = try runCombination(sub_ctx, k[0], k[1], fr, st);
            var ok = subs.len > 0;
            for (subs) |s| ok = ok and s.passed;
            try combos.append(arena, .{ .friction_id = fr.id, .physics_step_ticks = st, .passed = ok, .sub_runs = subs });
            try passes.append(arena, ok);
        };
        try cases.append(arena, .{ .case_id = k[1], .outcome = eval.combine(passes.items), .combinations = try combos.toOwnedSlice(arena) });
    }
    return .{
        .solver_name = "kinigami-rigid",
        .solver_version = "0.1.0",
        .solver_settings = protocol_settings,
        .cases = try cases.toOwnedSlice(arena),
    };
}

test "slide-to-stop replay is bit-identical (final state hash)" {
    const gpa = std.testing.allocator;
    const parsed = try criteria.parse(gpa, criteria.analytic_v1_json);
    defer parsed.deinit();
    var hashes: [2][]const u8 = undefined;
    var arena = std.heap.ArenaAllocator.init(gpa);
    defer arena.deinit();
    const ctx: Ctx = .{ .arena = arena.allocator(), .scratch = arena.allocator(), .c = parsed.value, .g = parsed.value.gravity.magnitude_m_s2, .unit = .{ .numerator = 1, .denominator = 1_000_000 } };
    for (&hashes) |*h| {
        const subs = try runCombination(ctx, .slide_to_stop, "slide_to_stop", parsed.value.friction_grid[2], 2000);
        h.* = subs[0].final_state_sha256;
    }
    try std.testing.expectEqualStrings(hashes[0], hashes[1]);
}

test "recording leaves results unchanged and captures every step (INS-007, Q51)" {
    const gpa = std.testing.allocator;
    const parsed = try criteria.parse(gpa, criteria.analytic_v1_json);
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

    const base: Ctx = .{ .arena = arena.allocator(), .scratch = arena.allocator(), .c = parsed.value, .g = parsed.value.gravity.magnitude_m_s2, .unit = .{ .numerator = 1, .denominator = 1_000_000 } };
    var with = base;
    with.recorder = .{ .ptr = &col, .emit = Collect.emit };
    const a = try runCombination(base, .slide_to_stop, "slide_to_stop", parsed.value.friction_grid[2], 2000);
    const b = try runCombination(with, .slide_to_stop, "slide_to_stop", parsed.value.friction_grid[2], 2000);
    try std.testing.expectEqualStrings(a[0].final_state_sha256, b[0].final_state_sha256);

    const rec = try recording.Recording.parse(col.bytes.?);
    try std.testing.expectEqual(@as(u16, 2), rec.version);
    try std.testing.expectEqual(@as(usize, a[0].steps + 1), rec.snapshot_count);
    const header = try scene_record.decodeHeader(arena.allocator(), rec.scene_header.?);
    var it = rec.snapshots();
    var prev: ?u64 = null;
    while (it.next()) |p| {
        const s = try scene_record.decodeSnapshot(arena.allocator(), header, p);
        if (prev) |t| try std.testing.expectEqual(t + header.physics_step_ticks, s.tick);
        prev = s.tick;
    }
}
