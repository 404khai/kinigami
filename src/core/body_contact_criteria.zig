//! Body-body contact fixture-validation criteria v1 (Q76, Q77), schema
//! version 1. Parsed through `strict_json` (every key is declared, unknown or
//! missing keys are errors) and then validated fail-closed. The registered
//! file is embedded so its identity is checked on every build.

const std = @import("std");
const strict_json = @import("strict_json.zig");
const time = @import("time.zig");

pub const schema_version: u32 = 1;

pub const Status = enum { copied, provisional };

/// A numeric value with its provenance: `copied` names a source, `provisional`
/// states a basis. Neither is evidence beyond what the field says.
pub const Num = struct { value: f64, status: Status, source: ?[]const u8 = null, basis: ?[]const u8 = null };
pub const Flag = struct { value: bool, status: Status, source: ?[]const u8 = null, basis: ?[]const u8 = null };
pub const Text = struct { value: []const u8, status: Status, source: ?[]const u8 = null, basis: ?[]const u8 = null };
pub const Vec = struct { value: [3]f64, status: Status, source: ?[]const u8 = null, basis: ?[]const u8 = null };

pub const FrictionPair = struct { id: []const u8, mu_static: f64, mu_kinetic: f64 };

pub const Fixture = struct {
    id: []const u8,
    shape: enum { cuboid },
    mass_distribution: enum { uniform },
    size_m: [3]f64,
    mass_kg: ?f64 = null,
    source: ?[]const u8 = null,
    motion: ?enum { static } = null,
    pose: ?[]const u8 = null,
    status: ?Status = null,
    basis: ?[]const u8 = null,
};

pub const Pair = struct { bottom: []const u8, top: []const u8 };

pub const Bb1 = struct {
    id: []const u8,
    fixtures: Pair,
    bottom_motion: enum { dynamic },
    poses: struct { bottom_centre_m: [3]f64, top_centre_m: [3]f64, orientation: []const u8 },
    duration_s: Num,
    window_start_s: Num,
    metrics: struct {
        inter_block_normal_force_rel_tol: Num,
        inter_block_normal_force_reference: []const u8,
        table_normal_force_rel_tol: Num,
        table_normal_force_reference: []const u8,
        tangential_force_max_rel_weight: Num,
        tangential_force_reference: []const u8,
        center_of_pressure_abs_tol_m: Num,
        drift_translation_abs_tol_m: Num,
        drift_rotation_abs_tol_rad: Num,
        max_penetration_m: Num,
        penetration_applies_to: []const u8,
        newton_third_law_rel_tol: Num,
    },
};

pub const Bb2 = struct {
    id: []const u8,
    fixtures: Pair,
    bottom_motion: enum { static },
    poses: struct { top_centre_m: [3]f64, orientation: []const u8 },
    application: Text,
    applied_on: []const u8,
    direction_world: Vec,
    threshold_force: []const u8,
    below_factor: Num,
    above_factor: Num,
    below: struct { duration_s: Num, max_displacement_m: Num, balance_window_start_s: Num, balance_rel_tol: Num, max_penetration_m: Num },
    above: struct {
        duration_s: Num,
        accel_window_start_s: Num,
        accel_window_end_s: Num,
        accel_rel_tol: Num,
        accel_reference: []const u8,
        max_penetration_m: Num,
        stays_on_slab: Flag,
    },
};

pub const Bb3 = struct {
    id: []const u8,
    fixtures: Pair,
    bottom_motion: enum { static },
    poses: struct { top_centre_m: [3]f64, orientation: []const u8 },
    initial_speed_m_s: Num,
    direction_world: Vec,
    duration_s: Num,
    stop_speed_threshold_m_s: Num,
    stop_point: []const u8,
    stop_time_tol_steps: Num,
    stop_distance_rel_tol: Num,
    stop_distance_tol_steps: Num,
    post_stop_drift_abs_tol_m: Num,
    stays_on_slab: Flag,
};

pub const Bb4 = struct {
    id: []const u8,
    fixtures: Pair,
    bottom_motion: enum { static },
    poses: struct {
        top_bottom_face_height_above_slab_top_m: Num,
        top_centre_xy_m: [2]f64,
        orientation: []const u8,
        initial_velocity: [3]f64,
    },
    settle: []const u8,
    duration_s: Num,
    rest_window_start_s: Num,
    rest_state_metrics: struct {
        normal_force_rel_tol: Num,
        normal_force_reference: []const u8,
        tangential_force_max_rel_weight: Num,
        center_of_pressure_abs_tol_m: Num,
        drift_translation_abs_tol_m: Num,
        drift_rotation_abs_tol_rad: Num,
    },
    peak_penetration: struct { max_penetration_m: Num, rest_max_penetration_m: Num, rest_penetration_window: []const u8 },
    free_flight: struct { no_contact_before_clearance_closes: Flag, no_tunnelling: Flag },
};

pub const Bb5 = struct {
    id: []const u8,
    fixtures: Pair,
    bottom_motion: enum { static },
    poses: struct { top_centre_m: [3]f64, orientation: []const u8 },
    force_frame: Text,
    force_direction_body: Vec,
    application_point_body_m: Vec,
    below_factor: Num,
    above_factor: Num,
    threshold_force: []const u8,
    threshold_note: []const u8,
    duration_s: Num,
    below_max_tilt_rad: Num,
    above_min_tilt_rad: Num,
    no_slip_until_tilt_rad: Num,
    pivot_slip_abs_tol_m: Num,
    pivot_point: []const u8,
};

pub const Bb6Body = struct {
    fixture: []const u8,
    motion: enum { static, dynamic },
    centre_m: [3]f64,
    orientation: ?[]const u8 = null,
    orientation_rotation_about_x_rad: ?f64 = null,
    orientation_rotation_about_y_rad: ?f64 = null,
    orientation_matrix: ?[3][3]f64 = null,
    orientation_note: ?[]const u8 = null,
};

pub const Bb6Config = struct {
    id: []const u8,
    kind: enum { face_face, edge_face, edge_edge },
    A: Bb6Body,
    B: Bb6Body,
    penetration_depth_m: f64,
    expected_axis: []const u8,
    expected_normal: [3]f64,
    expected_depth_m: f64,
    expected_points_m: []const [3]f64,
    expected_count: u32,
    points_on: ?[]const u8 = null,
    lowest_edge_of_B: ?[]const u8 = null,
    incident_face_tie: ?[]const u8 = null,
    edges: ?struct { A_top_edge: []const u8, B_lowest_edge: []const u8, crossing: []const u8 } = null,
    expected_point_definition: ?[]const u8 = null,
};

pub const Bb6 = struct {
    id: []const u8,
    kind: []const u8,
    friction_and_timestep: []const u8,
    run_label_note: []const u8,
    tolerance: struct { position_depth_rel_tol: Num, position_scale_m: Num, normal_component_abs_tol: Num },
    pair_order: []const u8,
    swap_check: Flag,
    point_comparison: []const u8,
    configurations: []const Bb6Config,
};

pub const Bb7Scene = struct { id: []const u8, base: []const u8, duration_s: Num, window_start_s: ?Num = null };

pub const Bb7 = struct {
    id: []const u8,
    scenes: []const Bb7Scene,
    base_note: []const u8,
    transform: struct {
        rotation_matrix_row_major: [3][3]f64,
        rotation_matrix_exact_rows: [3][3][]const u8,
        rotation_definition: []const u8,
        translation_m: [3]f64,
        applied_to: []const u8,
        gravity_direction_world: [3]f64,
        gravity_direction_exact: [3][]const u8,
        slide_direction_world: [3]f64,
        slide_direction_exact: [3][]const u8,
        minimum_table_clearance_m: Num,
    },
    comparison: []const u8,
    quantities_compared: struct { S1: []const []const u8, S3: []const []const u8 },
    rel_tol: Num,
    abs_floor: Num,
    stop_step_index_tol: Num,
};

pub const Bb8 = struct {
    id: []const u8,
    gravity_override: struct { magnitude_m_s2: f64, basis: []const u8 },
    fixtures: struct { A: []const u8, B: []const u8 },
    motion: struct { A: enum { dynamic }, B: enum { dynamic } },
    poses: struct { A_centre_m: [3]f64, B_centre_m: [3]f64, orientation: []const u8, initial_gap_m: Num, offset_x_m: Num },
    velocities: struct { A_m_s: [3]f64, B_m_s: [3]f64, angular_rad_s: [3]f64 },
    duration_s: Num,
    sliding_engaged: struct { min_peak_tangential_impulse_n_s: Num, basis: []const u8 },
    final_sample_contact_free: Flag,
    audits: struct {
        applies_to: []const u8,
        momentum: struct { form: []const u8, rel_tol_of_m_g_t: Num, abs_floor_kg_m_s: Num, M: []const u8, g_n: []const u8, note: []const u8 },
        angular_momentum: struct { form: []const u8, about: []const u8, rel_tol: Num, r_ref_m: Num, abs_floor_kg_m2_s: Num },
        impulse_accounting: struct { rel_tol_of_step_impulse_sum: Num, abs_floor_n_s: Num, definition: []const u8 },
        pose_integration: Text,
        energy: struct {
            quantity: []const u8,
            creation_rule: []const u8,
            creation_rel_tol: Num,
            abs_floor_j: Num,
            first_order_omega_dt_coefficient: Num,
            omega_ref_definition: []const u8,
            dissipation_reported: []const u8,
        },
    },
    audit_discrimination: struct { id: []const u8, controls: []const []const u8, requirement: Text },
};

pub const Bb9 = struct { id: []const u8, requirement: []const u8, source: []const u8, scope: Text };

pub const Criteria = struct {
    schema_version: u32,
    criteria_id: []const u8,
    criteria_version: u32,
    run_class: enum { fixture_validation },
    supersedes: []const u8 = "",
    decisions: []const []const u8,
    rationale: []const u8,
    protocol: struct { path: []const u8, revision: u32 },
    time_unit: struct { numerator_s: u64, denominator_s: u64 },
    physics_step_ticks: []const u64,
    physics_step_ticks_source: []const u8,
    outcome_rule: enum { all_combinations_pass_else_uncertain_if_mixed },
    outcome_rule_source: []const u8,
    gravity: struct { magnitude_m_s2: f64, direction_world: [3]f64, source: []const u8 },
    friction_law: enum { coulomb_static_kinetic },
    friction_grid: []const FrictionPair,
    friction_grid_source: []const u8,
    fixtures: []const Fixture,
    audit_allowance_source: []const u8,
    settle: struct { duration_s: Num, applies_to: []const u8, note: []const u8 },
    BB1: Bb1,
    BB2: Bb2,
    BB3: Bb3,
    BB4: Bb4,
    BB5: Bb5,
    BB6: Bb6,
    BB7: Bb7,
    BB8: Bb8,
    BB9: Bb9,
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
    InvalidWindow,
    MissingProvenance,
    NotMassBearing,
    BadExpectedAxis,
    BadFraction,
    TransformNotRotation,
    TransformMismatch,
    BadBb6Config,
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

fn provenance(x: anytype) ValidationError!void {
    switch (x.status) {
        .copied => if (x.source == null) return error.MissingProvenance,
        .provisional => if (x.basis == null) return error.MissingProvenance,
    }
}

fn posNum(n: Num) ValidationError!void {
    try provenance(n);
    try positive(n.value);
}

pub fn fixtureById(c: Criteria, id: []const u8) ?Fixture {
    for (c.fixtures) |f| if (std.mem.eql(u8, f.id, id)) return f;
    return null;
}

fn needFixture(c: Criteria, id: []const u8) ValidationError!Fixture {
    return fixtureById(c, id) orelse error.UnknownFixture;
}

fn needMass(c: Criteria, id: []const u8) ValidationError!void {
    const f = try needFixture(c, id);
    try positive(f.mass_kg orelse return error.NotMassBearing);
}

fn needStatic(c: Criteria, id: []const u8) ValidationError!void {
    const f = try needFixture(c, id);
    if (f.motion == null) return error.UnknownFixture;
}

fn window(start: f64, end: f64) ValidationError!void {
    if (!(start >= 0 and start < end)) return error.InvalidWindow;
}

/// "a/b" with integers (a may be negative): one division, as the protocol
/// constructs the BB7 transform.
pub fn fraction(text: []const u8) ValidationError!f64 {
    const at = std.mem.indexOfScalar(u8, text, '/') orelse return error.BadFraction;
    const a = std.fmt.parseInt(i64, text[0..at], 10) catch return error.BadFraction;
    const b = std.fmt.parseInt(i64, text[at + 1 ..], 10) catch return error.BadFraction;
    if (b == 0) return error.BadFraction;
    return @as(f64, @floatFromInt(a)) / @as(f64, @floatFromInt(b));
}

/// The SAT axis index named in an `expected_axis` string ("... SAT axis 2" or
/// "... SAT axis index 7").
pub fn expectedAxis(text: []const u8) ValidationError!u8 {
    const key = "SAT axis ";
    const at = std.mem.indexOf(u8, text, key) orelse return error.BadExpectedAxis;
    var rest = text[at + key.len ..];
    if (std.mem.startsWith(u8, rest, "index ")) rest = rest["index ".len..];
    var end: usize = 0;
    while (end < rest.len and rest[end] >= '0' and rest[end] <= '9') end += 1;
    const v = std.fmt.parseInt(u8, rest[0..end], 10) catch return error.BadExpectedAxis;
    if (v > 14) return error.BadExpectedAxis;
    return v;
}

fn matches(a: f64, b: f64) bool {
    return @abs(a - b) <= 1e-12;
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
    try positive(c.gravity.magnitude_m_s2);
    const gd = c.gravity.direction_world;
    if (!(gd[0] == 0 and gd[1] == 0 and gd[2] == -1.0)) return error.GravityNotVerticalDown;
    if (c.friction_grid.len == 0) return error.EmptyGrid;
    for (c.friction_grid, 0..) |p, i| {
        for (c.friction_grid[0..i]) |q| if (std.mem.eql(u8, p.id, q.id)) return error.DuplicateId;
        if (!(p.mu_kinetic > 0 and p.mu_static > p.mu_kinetic)) return error.InvalidFrictionPair;
    }
    for (c.fixtures, 0..) |f, i| {
        for (c.fixtures[0..i]) |q| if (std.mem.eql(u8, f.id, q.id)) return error.DuplicateId;
        for (f.size_m) |s| try positive(s);
        if (f.mass_kg) |m| try positive(m);
        if (f.status) |_| try provenance(.{ .status = f.status.?, .source = f.source, .basis = f.basis });
    }
    try posNum(c.settle.duration_s);

    {
        const b = c.BB1;
        try needMass(c, b.fixtures.bottom);
        try needMass(c, b.fixtures.top);
        try posNum(b.duration_s);
        try posNum(b.window_start_s);
        try window(b.window_start_s.value, b.duration_s.value);
        inline for (.{ "inter_block_normal_force_rel_tol", "table_normal_force_rel_tol", "tangential_force_max_rel_weight", "center_of_pressure_abs_tol_m", "drift_translation_abs_tol_m", "drift_rotation_abs_tol_rad", "max_penetration_m", "newton_third_law_rel_tol" }) |name|
            try posNum(@field(b.metrics, name));
    }
    {
        const b = c.BB2;
        try needStatic(c, b.fixtures.bottom);
        try needMass(c, b.fixtures.top);
        try provenance(b.application);
        try provenance(b.direction_world);
        const d = b.direction_world.value;
        if (!(matches(@sqrt(d[0] * d[0] + d[1] * d[1] + d[2] * d[2]), 1.0) and d[2] == 0)) return error.NotUnitVector;
        try posNum(b.below_factor);
        try posNum(b.above_factor);
        if (!(b.below_factor.value < 1.0 and b.above_factor.value > 1.0)) return error.ThresholdFactorAtOrAcrossOne;
        inline for (.{ "duration_s", "max_displacement_m", "balance_window_start_s", "balance_rel_tol", "max_penetration_m" }) |name| try posNum(@field(b.below, name));
        inline for (.{ "duration_s", "accel_window_start_s", "accel_window_end_s", "accel_rel_tol", "max_penetration_m" }) |name| try posNum(@field(b.above, name));
        try provenance(b.above.stays_on_slab);
        try window(b.below.balance_window_start_s.value, b.below.duration_s.value);
        try window(b.above.accel_window_start_s.value, b.above.accel_window_end_s.value);
        if (b.above.accel_window_end_s.value > b.above.duration_s.value) return error.InvalidWindow;
    }
    {
        const b = c.BB3;
        try needStatic(c, b.fixtures.bottom);
        try needMass(c, b.fixtures.top);
        try provenance(b.direction_world);
        inline for (.{ "initial_speed_m_s", "duration_s", "stop_speed_threshold_m_s", "stop_time_tol_steps", "stop_distance_rel_tol", "stop_distance_tol_steps", "post_stop_drift_abs_tol_m" }) |name| try posNum(@field(b, name));
        try provenance(b.stays_on_slab);
    }
    {
        const b = c.BB4;
        try needStatic(c, b.fixtures.bottom);
        try needMass(c, b.fixtures.top);
        try posNum(b.poses.top_bottom_face_height_above_slab_top_m);
        try posNum(b.duration_s);
        try posNum(b.rest_window_start_s);
        try window(b.rest_window_start_s.value, b.duration_s.value);
        inline for (.{ "normal_force_rel_tol", "tangential_force_max_rel_weight", "center_of_pressure_abs_tol_m", "drift_translation_abs_tol_m", "drift_rotation_abs_tol_rad" }) |name| try posNum(@field(b.rest_state_metrics, name));
        try posNum(b.peak_penetration.max_penetration_m);
        try posNum(b.peak_penetration.rest_max_penetration_m);
        try provenance(b.free_flight.no_contact_before_clearance_closes);
        try provenance(b.free_flight.no_tunnelling);
    }
    {
        const b = c.BB5;
        try needStatic(c, b.fixtures.bottom);
        try needMass(c, b.fixtures.top);
        try provenance(b.force_frame);
        try provenance(b.force_direction_body);
        try provenance(b.application_point_body_m);
        try posNum(b.below_factor);
        try posNum(b.above_factor);
        if (!(b.below_factor.value < 1.0 and b.above_factor.value > 1.0)) return error.ThresholdFactorAtOrAcrossOne;
        inline for (.{ "duration_s", "below_max_tilt_rad", "above_min_tilt_rad", "no_slip_until_tilt_rad", "pivot_slip_abs_tol_m" }) |name| try posNum(@field(b, name));
    }
    {
        const b = c.BB6;
        try posNum(b.tolerance.position_depth_rel_tol);
        try posNum(b.tolerance.position_scale_m);
        try posNum(b.tolerance.normal_component_abs_tol);
        try provenance(b.swap_check);
        if (b.configurations.len != 3) return error.BadBb6Config;
        for (b.configurations, 0..) |cf, i| {
            for (b.configurations[0..i]) |q| if (std.mem.eql(u8, cf.id, q.id)) return error.DuplicateId;
            _ = try needFixture(c, cf.A.fixture);
            _ = try needFixture(c, cf.B.fixture);
            _ = try expectedAxis(cf.expected_axis);
            if (cf.expected_count == 0 or cf.expected_count != cf.expected_points_m.len or cf.expected_count > 8) return error.BadBb6Config;
            const n = cf.expected_normal;
            if (!matches(@sqrt(n[0] * n[0] + n[1] * n[1] + n[2] * n[2]), 1.0)) return error.NotUnitVector;
            try positive(cf.expected_depth_m);
        }
    }
    {
        const b = c.BB7;
        try posNum(b.rel_tol);
        try posNum(b.abs_floor);
        try posNum(b.stop_step_index_tol);
        try posNum(b.transform.minimum_table_clearance_m);
        if (b.scenes.len != 2) return error.EmptyGrid;
        for (b.scenes) |s| try posNum(s.duration_s);
        // The exact fractions are authoritative; the decimals must agree and
        // the matrix must be a rotation (orthonormal, determinant +1).
        const t = b.transform;
        var r: [3][3]f64 = undefined;
        for (0..3) |i| for (0..3) |j| {
            r[i][j] = try fraction(t.rotation_matrix_exact_rows[i][j]);
            if (!matches(r[i][j], t.rotation_matrix_row_major[i][j])) return error.TransformMismatch;
        };
        for (0..3) |i| for (0..3) |j| {
            var d: f64 = 0;
            for (0..3) |k| d += r[i][k] * r[j][k];
            if (@abs(d - (if (i == j) @as(f64, 1) else 0)) > 1e-12) return error.TransformNotRotation;
        };
        const det = r[0][0] * (r[1][1] * r[2][2] - r[1][2] * r[2][1]) - r[0][1] * (r[1][0] * r[2][2] - r[1][2] * r[2][0]) + r[0][2] * (r[1][0] * r[2][1] - r[1][1] * r[2][0]);
        if (@abs(det - 1.0) > 1e-12) return error.TransformNotRotation;
        for (0..3) |i| {
            if (!matches(try fraction(t.gravity_direction_exact[i]), t.gravity_direction_world[i])) return error.TransformMismatch;
            if (!matches(try fraction(t.slide_direction_exact[i]), t.slide_direction_world[i])) return error.TransformMismatch;
            // g' = R (0, 0, -1), slide' = R (1, 0, 0).
            if (!matches(-r[i][2], t.gravity_direction_world[i])) return error.TransformMismatch;
            if (!matches(r[i][0], t.slide_direction_world[i])) return error.TransformMismatch;
        }
    }
    {
        const b = c.BB8;
        if (b.gravity_override.magnitude_m_s2 != 0) return error.NonPositiveValue;
        try needMass(c, b.fixtures.A);
        try needMass(c, b.fixtures.B);
        try posNum(b.poses.initial_gap_m);
        try posNum(b.poses.offset_x_m);
        try posNum(b.duration_s);
        try posNum(b.sliding_engaged.min_peak_tangential_impulse_n_s);
        try provenance(b.final_sample_contact_free);
        try posNum(b.audits.momentum.rel_tol_of_m_g_t);
        try posNum(b.audits.momentum.abs_floor_kg_m_s);
        try posNum(b.audits.angular_momentum.rel_tol);
        try posNum(b.audits.angular_momentum.r_ref_m);
        try posNum(b.audits.angular_momentum.abs_floor_kg_m2_s);
        try posNum(b.audits.impulse_accounting.rel_tol_of_step_impulse_sum);
        try posNum(b.audits.impulse_accounting.abs_floor_n_s);
        try provenance(b.audits.pose_integration);
        try posNum(b.audits.energy.creation_rel_tol);
        try posNum(b.audits.energy.abs_floor_j);
        try provenance(b.audits.energy.first_order_omega_dt_coefficient);
        if (b.audit_discrimination.controls.len != 2) return error.EmptyGrid;
        try provenance(b.audit_discrimination.requirement);
    }
    try provenance(c.BB9.scope);
}

/// The preregistered criteria file, embedded so its consistency is checked on
/// every build. Its identity is the SHA-256 of these exact bytes.
pub const v1_json = @embedFile("criteria_body_contact_v1");

/// SHA-256 recorded in criteria/REGISTER.md.
pub const v1_sha256 = "26b2f8dc2c938cd299baaec557132cb2aeb3d039b1d563107214e34a2878d883";

/// Criteria v2 (Q79): v1 with the BB6 swap rule corrected. Default.
pub const v2_json = @embedFile("criteria_body_contact_v2");

pub const v2_sha256 = "85ae950f7ff1d5647034742a0c598fa59e75c8631a3ce5f041f48c7cfc2f4a60";

/// Criteria v3 (Q80): v2 with the BB6 swap check on the contact midplane. Default.
pub const v3_json = @embedFile("criteria_body_contact_v3");

pub const v3_sha256 = "05c3d2ec402cdb37bed5b9e30c00f8d2bf465048e8258c90f8db98887918f0c2";

const testing = std.testing;

test "the embedded body-contact criteria v3 are byte-identical to the registered version and parse" {
    const identity = @import("identity.zig");
    try testing.expectEqualStrings(v3_sha256, &identity.toHex(identity.fileIdentity(v3_json)));
    const p = try parse(testing.allocator, v3_json);
    defer p.deinit();
    try testing.expectEqual(@as(u32, 3), p.value.criteria_version);
}

test "the embedded body-contact criteria v2 are byte-identical to the registered version and parse" {
    const identity = @import("identity.zig");
    try testing.expectEqualStrings(v2_sha256, &identity.toHex(identity.fileIdentity(v2_json)));
    const p = try parse(testing.allocator, v2_json);
    defer p.deinit();
    try testing.expectEqual(@as(u32, 2), p.value.criteria_version);
    try testing.expectEqual(@as(usize, 3), p.value.BB6.configurations.len);
}

test "the embedded body-contact criteria are byte-identical to the registered version" {
    const identity = @import("identity.zig");
    try testing.expectEqualStrings(v1_sha256, &identity.toHex(identity.fileIdentity(v1_json)));
}

test "the registered body-contact criteria parse and are self-consistent" {
    const p = try parse(testing.allocator, v1_json);
    defer p.deinit();
    try testing.expectEqual(@as(usize, 3), p.value.friction_grid.len);
    try testing.expectEqualSlices(u64, &.{ 500, 1000, 2000 }, p.value.physics_step_ticks);
    try testing.expectEqual(@as(usize, 3), p.value.BB6.configurations.len);
    try testing.expectEqual(@as(u8, 7), try expectedAxis(p.value.BB6.configurations[2].expected_axis));
    try testing.expectEqual(@as(f64, 1e-6), p.value.BB7.rel_tol.value);
}

fn expectInvalid(expected: anyerror, needle: []const u8, replacement: []const u8) !void {
    const gpa = testing.allocator;
    const at = std.mem.indexOf(u8, v1_json, needle) orelse return error.TestNeedleNotFound;
    const text = try std.mem.concat(gpa, u8, &.{ v1_json[0..at], replacement, v1_json[at + needle.len ..] });
    defer gpa.free(text);
    if (parse(gpa, text)) |p| {
        p.deinit();
        return error.TestUnexpectedSuccess;
    } else |err| try testing.expectEqual(expected, err);
}

test "consistency rules reject ambiguous body-contact criteria" {
    try expectInvalid(error.InvalidFrictionPair, "\"mu_static\": 0.3", "\"mu_static\": 0.2");
    try expectInvalid(error.ThresholdFactorAtOrAcrossOne, "\"value\": 0.9,\n   \"status\": \"copied\",\n   \"source\": \"analytic-v1 friction_threshold.below_factor\"", "\"value\": 1.0,\n   \"status\": \"copied\",\n   \"source\": \"analytic-v1 friction_threshold.below_factor\"");
    try expectInvalid(error.UnknownFixture, "\"bottom\": \"fixture_support_slab\"", "\"bottom\": \"missing\"");
    try expectInvalid(error.GravityNotVerticalDown, "\"direction_world\": [\n   0,\n   0,\n   -1\n  ]", "\"direction_world\": [\n   0,\n   -1,\n   0\n  ]");
}

test "strict parsing applies to the body-contact criteria" {
    try expectInvalid(error.UnknownField, "\"criteria_version\": 1,", "\"criteria_version\": 1, \"extra\": 0,");
    try expectInvalid(error.IntegerNotExact, "\"criteria_version\": 1,", "\"criteria_version\": 1.0,");
}

test "fraction and expected-axis helpers" {
    try testing.expectEqual(@as(f64, -16.0 / 45.0), try fraction("-16/45"));
    try testing.expectError(error.BadFraction, fraction("1/0"));
    try testing.expectEqual(@as(u8, 2), try expectedAxis("A local z (SAT axis 2). x"));
    try testing.expectError(error.BadExpectedAxis, expectedAxis("none"));
}
