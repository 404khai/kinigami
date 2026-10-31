//! Analytic fixture-validation criteria, schema version 1 (Q39, Q44, Q46,
//! Q47, Q48).
//!
//! Parsed through `strict_json` and then validated fail-closed, including
//! physical self-consistency checks: every case must remain analytically
//! clean at every friction pair and timestep in the grid (for example, the
//! tipping case must tip before it can slide). A criteria file that could
//! make a case ambiguous is rejected before any solver runs.

const std = @import("std");
const strict_json = @import("strict_json.zig");
const time = @import("time.zig");
const analytic = @import("analytic.zig");

pub const schema_version: u32 = 1;

pub const FrictionPair = struct { id: []const u8, mu_static: f64, mu_kinetic: f64 };

pub const Fixture = struct {
    id: []const u8,
    shape: enum { cuboid },
    mass_distribution: enum { uniform },
    size_m: [3]f64,
    mass_kg: f64,
};

pub const RestCase = struct {
    id: []const u8,
    fixture: []const u8,
    duration_s: f64,
    window_start_s: f64,
    normal_force_rel_tol: f64,
    tangential_force_max_rel_weight: f64,
    center_of_pressure_abs_tol_m: f64,
    drift_translation_abs_tol_m: f64,
    drift_rotation_abs_tol_rad: f64,
    max_penetration_m: f64,
};

pub const FreeFallCase = struct {
    id: []const u8,
    fixture: []const u8,
    initial_clearance_m: f64,
    duration_s: f64,
    velocity_rel_tol: f64,
    velocity_abs_floor_m_s: f64,
    /// |Δz| ≤ position_tol_factor · g · Δt · t
    position_tol_factor: f64,
};

pub const FrictionThresholdCase = struct {
    id: []const u8,
    fixture: []const u8,
    application: enum { center_of_mass },
    direction_world: [3]f64,
    below_factor: f64,
    above_factor: f64,
    duration_s: f64,
    below_max_displacement_m: f64,
    below_balance_window_start_s: f64,
    below_balance_rel_tol: f64,
    above_accel_window_start_s: f64,
    above_accel_window_end_s: f64,
    above_accel_rel_tol: f64,
    max_penetration_m: f64,
};

pub const SlideToStopCase = struct {
    id: []const u8,
    fixture: []const u8,
    initial_speed_m_s: f64,
    direction_world: [3]f64,
    duration_s: f64,
    stop_speed_threshold_m_s: f64,
    stop_time_tol_steps: f64,
    stop_distance_rel_tol: f64,
    /// Additional distance tolerance of this many steps of initial-speed travel.
    stop_distance_tol_steps: f64,
    post_stop_drift_abs_tol_m: f64,
};

pub const TippingCase = struct {
    id: []const u8,
    fixture: []const u8,
    force_frame: enum { body },
    force_direction_body: [3]f64,
    /// Body frame: origin at the centre of mass, axes along the cuboid edges.
    application_point_body_m: [3]f64,
    below_factor: f64,
    above_factor: f64,
    duration_s: f64,
    below_max_tilt_rad: f64,
    above_min_tilt_rad: f64,
    no_slip_until_tilt_rad: f64,
    pivot_slip_abs_tol_m: f64,
};

pub const Criteria = struct {
    schema_version: u32,
    criteria_id: []const u8,
    criteria_version: u32,
    run_class: enum { fixture_validation },
    decisions: []const []const u8,
    rationale: []const u8,
    time_unit: struct { numerator_s: u64, denominator_s: u64 },
    physics_step_ticks: []const u64,
    outcome_rule: enum { all_combinations_pass_else_uncertain_if_mixed },
    gravity: struct { magnitude_m_s2: f64, direction_world: [3]f64, source: []const u8 },
    friction_law: enum { coulomb_static_kinetic },
    friction_grid: []const FrictionPair,
    friction_grid_rationale: []const u8,
    fixtures: []const Fixture,
    rest: RestCase,
    free_fall: FreeFallCase,
    friction_threshold: FrictionThresholdCase,
    slide_to_stop: SlideToStopCase,
    tipping: TippingCase,
};

pub const ValidationError = error{
    UnsupportedSchemaVersion,
    NonPositiveValue,
    EmptyGrid,
    DuplicateId,
    UnknownFixture,
    InvalidFrictionPair,
    ThresholdFactorAtOrAcrossOne,
    NotUnitVector,
    GravityNotVerticalDown,
    DirectionNotHorizontal,
    InvalidWindow,
    FreeFallReachesTable,
    FrictionCaseCouldTip,
    TippingCouldSlideFirst,
    PointOutsideFixture,
    SlideDoesNotStop,
} || time.Error;

pub fn parse(gpa: std.mem.Allocator, text: []const u8) (strict_json.Error || ValidationError)!strict_json.Parsed(Criteria) {
    const parsed = try strict_json.parse(Criteria, gpa, text, .{});
    errdefer parsed.deinit();
    try validate(parsed.value);
    return parsed;
}

fn positive(v: f64) ValidationError!void {
    if (!(v > 0)) return error.NonPositiveValue;
}

fn unit(v: [3]f64) ValidationError!void {
    const n = @sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);
    if (@abs(n - 1.0) > 1e-12) return error.NotUnitVector;
}

fn factors(below: f64, above: f64) ValidationError!void {
    try positive(below);
    if (!(below < 1.0 and above > 1.0)) return error.ThresholdFactorAtOrAcrossOne;
}

fn window(start: f64, end: f64) ValidationError!void {
    if (!(start >= 0 and start < end)) return error.InvalidWindow;
}

fn fixture(c: Criteria, id: []const u8) ValidationError!Fixture {
    for (c.fixtures) |f| if (std.mem.eql(u8, f.id, id)) return f;
    return error.UnknownFixture;
}

pub fn validate(c: Criteria) ValidationError!void {
    if (c.schema_version != schema_version) return error.UnsupportedSchemaVersion;
    if (c.criteria_version == 0) return error.NonPositiveValue;
    try (time.TimeUnit{ .numerator = c.time_unit.numerator_s, .denominator = c.time_unit.denominator_s }).validate();
    if (c.physics_step_ticks.len == 0) return error.EmptyGrid;
    for (c.physics_step_ticks, 0..) |s, i| {
        _ = try time.PhysicsStep.init(.{ .ticks = s });
        for (c.physics_step_ticks[0..i]) |p| if (p == s) return error.DuplicateId;
    }

    const g = c.gravity.magnitude_m_s2;
    try positive(g);
    try unit(c.gravity.direction_world);
    if (c.gravity.direction_world[2] != -1.0) return error.GravityNotVerticalDown;

    if (c.friction_grid.len == 0) return error.EmptyGrid;
    var mu_s_min: f64 = std.math.inf(f64);
    var mu_s_max: f64 = 0;
    var mu_k_min: f64 = std.math.inf(f64);
    for (c.friction_grid, 0..) |p, i| {
        for (c.friction_grid[0..i]) |q| if (std.mem.eql(u8, p.id, q.id)) return error.DuplicateId;
        // Q47: separate coefficients, μs > μk > 0 so onset and sliding differ.
        if (!(p.mu_kinetic > 0 and p.mu_static > p.mu_kinetic)) return error.InvalidFrictionPair;
        mu_s_min = @min(mu_s_min, p.mu_static);
        mu_s_max = @max(mu_s_max, p.mu_static);
        mu_k_min = @min(mu_k_min, p.mu_kinetic);
    }

    for (c.fixtures, 0..) |f, i| {
        for (c.fixtures[0..i]) |q| if (std.mem.eql(u8, f.id, q.id)) return error.DuplicateId;
        try positive(f.mass_kg);
        for (f.size_m) |s| try positive(s);
    }

    const dt_max_s = blk: {
        var m: u64 = 0;
        for (c.physics_step_ticks) |s| m = @max(m, s);
        const tu: time.TimeUnit = .{ .numerator = c.time_unit.numerator_s, .denominator = c.time_unit.denominator_s };
        break :blk tu.seconds(.{ .ticks = m });
    };

    // Rest.
    {
        const r = c.rest;
        _ = try fixture(c, r.fixture);
        try window(r.window_start_s, r.duration_s);
        inline for (.{ "normal_force_rel_tol", "tangential_force_max_rel_weight", "center_of_pressure_abs_tol_m", "drift_translation_abs_tol_m", "drift_rotation_abs_tol_rad", "max_penetration_m" }) |name|
            try positive(@field(r, name));
    }

    // Free fall: the observation window must end before contact.
    {
        const ff = c.free_fall;
        _ = try fixture(c, ff.fixture);
        try positive(ff.initial_clearance_m);
        try positive(ff.duration_s);
        try positive(ff.velocity_rel_tol);
        try positive(ff.velocity_abs_floor_m_s);
        try positive(ff.position_tol_factor);
        if (ff.duration_s >= analytic.freeFallContactTime(g, ff.initial_clearance_m)) return error.FreeFallReachesTable;
    }

    // Friction threshold: horizontal push at the centre of mass must never tip
    // the fixture, even at the largest load in the grid.
    {
        const fr = c.friction_threshold;
        const f = try fixture(c, fr.fixture);
        try unit(fr.direction_world);
        if (fr.direction_world[2] != 0) return error.DirectionNotHorizontal;
        try factors(fr.below_factor, fr.above_factor);
        try positive(fr.below_max_displacement_m);
        try positive(fr.below_balance_rel_tol);
        try positive(fr.above_accel_rel_tol);
        try positive(fr.max_penetration_m);
        try window(fr.below_balance_window_start_s, fr.duration_s);
        try window(fr.above_accel_window_start_s, fr.above_accel_window_end_s);
        if (fr.above_accel_window_end_s > fr.duration_s) return error.InvalidWindow;
        const push = fr.above_factor * analytic.slidingThreshold(f.mass_kg, g, mu_s_max);
        const half_width = @min(f.size_m[0], f.size_m[1]) / 2.0;
        const tip = analytic.tippingThreshold(f.mass_kg, g, half_width, f.size_m[2] / 2.0);
        if (push >= tip) return error.FrictionCaseCouldTip;
    }

    // Sliding to a stop: must stop well within the run at every μk.
    {
        const s = c.slide_to_stop;
        _ = try fixture(c, s.fixture);
        try unit(s.direction_world);
        if (s.direction_world[2] != 0) return error.DirectionNotHorizontal;
        inline for (.{ "initial_speed_m_s", "stop_speed_threshold_m_s", "stop_time_tol_steps", "stop_distance_rel_tol", "stop_distance_tol_steps", "post_stop_drift_abs_tol_m" }) |name|
            try positive(@field(s, name));
        const t_stop = analytic.stopTime(g, mu_k_min, s.initial_speed_m_s);
        if (t_stop + s.stop_time_tol_steps * dt_max_s >= s.duration_s) return error.SlideDoesNotStop;
    }

    // Tipping: the above-threshold push must stay below the smallest static
    // friction limit, so the fixture tips before it can slide.
    {
        const t = c.tipping;
        const f = try fixture(c, t.fixture);
        try unit(t.force_direction_body);
        try factors(t.below_factor, t.above_factor);
        inline for (.{ "below_max_tilt_rad", "above_min_tilt_rad", "no_slip_until_tilt_rad", "pivot_slip_abs_tol_m", "duration_s" }) |name|
            try positive(@field(t, name));
        for (t.application_point_body_m, 0..) |p, i| if (@abs(p) > f.size_m[i] / 2.0) return error.PointOutsideFixture;
        if (!(t.force_direction_body[0] == 1.0 and t.application_point_body_m[0] == -f.size_m[0] / 2.0)) return error.PointOutsideFixture;
        const h = t.application_point_body_m[2] + f.size_m[2] / 2.0;
        try positive(h);
        const tip = analytic.tippingThreshold(f.mass_kg, g, f.size_m[0] / 2.0, h);
        if (t.above_factor * tip >= analytic.slidingThreshold(f.mass_kg, g, mu_s_min)) return error.TippingCouldSlideFirst;
    }
}

/// The preregistered criteria file, embedded so its consistency is checked
/// on every build. Its identity is the SHA-256 of these exact bytes.
pub const analytic_v1_json = @embedFile("criteria_analytic_v1");

/// SHA-256 recorded in criteria/REGISTER.md. Registered files are never
/// edited in place; a revision is a new file and a new register entry.
pub const analytic_v1_sha256 = "565ef6b62aeebe92aabf6dc2a4763aef02d9e4e51579985513c2cff4f9df3e78";

const testing = std.testing;

test "the embedded criteria file is byte-identical to its registered version" {
    const identity = @import("identity.zig");
    try testing.expectEqualStrings(analytic_v1_sha256, &identity.toHex(identity.fileIdentity(analytic_v1_json)));
}

test "the registered analytic criteria file parses and is self-consistent" {
    const p = try parse(testing.allocator, analytic_v1_json);
    defer p.deinit();
    try testing.expectEqual(@as(usize, 3), p.value.friction_grid.len);
    try testing.expectEqualSlices(u64, &.{ 500, 1000, 2000 }, p.value.physics_step_ticks);
    try testing.expectEqual(@as(f64, 9.80665), p.value.gravity.magnitude_m_s2);
}

fn expectInvalid(expected: anyerror, needle: []const u8, replacement: []const u8) !void {
    const gpa = testing.allocator;
    const at = std.mem.indexOf(u8, analytic_v1_json, needle) orelse return error.TestNeedleNotFound;
    const text = try std.mem.concat(gpa, u8, &.{ analytic_v1_json[0..at], replacement, analytic_v1_json[at + needle.len ..] });
    defer gpa.free(text);
    if (parse(gpa, text)) |p| {
        p.deinit();
        return error.TestUnexpectedSuccess;
    } else |err| try testing.expectEqual(expected, err);
}

test "consistency rules reject ambiguous criteria" {
    // μs must exceed μk (Q47).
    try expectInvalid(error.InvalidFrictionPair, "\"mu_static\": 0.3", "\"mu_static\": 0.2");
    // Thresholds are never tested at equality (Q46).
    try expectInvalid(error.ThresholdFactorAtOrAcrossOne, "\"below_factor\": 0.9", "\"below_factor\": 1.0");
    // Free fall must end before contact.
    try expectInvalid(error.FreeFallReachesTable, "\"initial_clearance_m\": 0.1", "\"initial_clearance_m\": 0.01");
    // A low enough static friction would let the tall fixture slide before tipping.
    try expectInvalid(error.TippingCouldSlideFirst, "\"mu_static\": 0.3", "\"mu_static\": 0.21");
    // Fixture references must resolve; gravity must point down.
    try expectInvalid(error.UnknownFixture, "\"fixture\": \"fixture_tall_block\"", "\"fixture\": \"missing\"");
    try expectInvalid(error.GravityNotVerticalDown, "\"direction_world\": [0, 0, -1]", "\"direction_world\": [0, -1, 0]");
}

test "strict parsing still applies to the criteria file" {
    try expectInvalid(error.UnknownField, "\"criteria_version\": 1,", "\"criteria_version\": 1, \"extra\": 0,");
    try expectInvalid(error.IntegerNotExact, "\"criteria_version\": 1", "\"criteria_version\": 1.0");
}
