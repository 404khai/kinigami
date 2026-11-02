//! Compliant-link qualification criteria, schema version 1 (Q35, Q41, Q43,
//! Q46, Q48, Q52).
//!
//! Parsed through `strict_json` and validated fail-closed, in the same way as
//! `criteria.zig`. Every descriptive string that selects a measurement
//! (period measure, damping measure, rotation measure, conventions) is an
//! enum or an exactly matched constant with a single admissible value, so a
//! criteria file that changes how something is measured is rejected here
//! rather than silently reinterpreted by the evaluator.

const std = @import("std");
const strict_json = @import("strict_json.zig");
const time = @import("time.zig");

pub const schema_version: u32 = 1;

pub const Fixture = struct {
    id: []const u8,
    shape: enum { cuboid },
    mass_distribution: enum { uniform },
    size_m: [3]f64,
    mass_kg: f64,
};

pub const GridPoint = struct {
    id: []const u8,
    k_axial_n_m: f64,
    k_shear_n_m: f64,
    k_torsion_nm_rad: f64,
    k_bend_nm_rad: f64,
};

pub const AxialStatics = struct { id: []const u8, force_rel_tol: f64, elongation_rel_tol: f64 };

pub const ShearBendingStatics = struct {
    id: []const u8,
    load_world_direction: [3]f64,
    load_over_weight: f64,
    application: enum { center_of_mass_b },
    /// Reference for the bending moment and angle. Schema default (v1, Q52):
    /// F·h. Criteria v2 (Q53): the exact torque balance of body B including
    /// the tension lever, k_bend·φ = h·(F·cos φ − m·g·sin φ).
    moment_reference: MomentReference = .load_times_half_size,
    force_rel_tol: f64,
    moment_rel_tol: f64,
    displacement_rel_tol: f64,
    angle_rel_tol: f64,
};

pub const MomentReference = enum { load_times_half_size, torque_balance_with_tension_lever };

pub const TorsionStatics = struct { id: []const u8, torque_about_link_axis_nm: f64, torque_rel_tol: f64, twist_rel_tol: f64 };

pub const StaticCases = struct {
    setup: enum { body_a_static_above_body_b_hanging_link_axis_world_minus_z },
    damping_ratio_on_body_b: f64,
    duration_s: f64,
    window_start_s: f64,
    axial: AxialStatics,
    shear_bending: ShearBendingStatics,
    torsion: TorsionStatics,
};

pub const AxialDynamics = struct {
    id: []const u8,
    initial_stretch_m: f64,
    damping_ratio: f64,
    period_measure: enum { mean_of_full_periods_from_linear_interpolated_zero_crossings_of_axial_extension },
    period_rel_tol: f64,
};

pub const TorsionDynamics = struct {
    id: []const u8,
    initial_twist_rad: f64,
    damping_ratio: f64,
    period_measure: enum { mean_of_full_periods_from_linear_interpolated_zero_crossings_of_twist },
    period_rel_tol: f64,
};

pub const PhysicalDamping = struct {
    id: []const u8,
    initial_stretch_m: f64,
    damping_ratio: f64,
    zeta_measure: enum { log_of_ratio_of_first_and_last_positive_peaks_over_full_periods_divided_by_2pi_n },
    zeta_rel_tol: f64,
};

pub const NumericalDissipation = struct {
    id: []const u8,
    initial_stretch_m: f64,
    damping_ratio: f64,
    zeta_measure: enum { log_of_ratio_of_first_and_last_positive_peaks_over_full_periods_divided_by_2pi_n },
    zeta_num_max: f64,
};

pub const Momentum = struct { id: []const u8, rel_tol_of_m_g_t: f64, abs_floor_kg_m_s: f64 };

pub const DynamicCases = struct {
    setup: enum { two_free_bodies_in_free_fall_no_contact_link_axis_world_x },
    duration_s: f64,
    axial: AxialDynamics,
    torsion: TorsionDynamics,
    physical_damping: PhysicalDamping,
    numerical_dissipation: NumericalDissipation,
    momentum: Momentum,
};

pub const ConsistencyCase = struct {
    id: []const u8,
    setup: enum { body_b_resting_on_tabletop_vertical_link_to_static_body_a_above },
    pretension_over_weight: f64,
    damping_ratio_on_body_b: f64,
    friction_pair: struct { mu_static: f64, mu_kinetic: f64 },
    duration_s: f64,
    window_start_s: f64,
    sum_rel_tol: f64,
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
    outcome_rule: enum { evaluated_combinations_all_pass_else_uncertain_if_mixed },
    resolution: struct {
        max_omega_dt: f64,
        applies_to: enum { dynamic_checks },
        beyond_limit: enum { outside_envelope_not_counted },
    },
    gravity: struct { magnitude_m_s2: f64, direction_world: [3]f64 },
    fixture: Fixture,
    link: struct {
        model: enum { six_dof_spring_damper_between_anchor_frames },
        rest_length_m: f64,
        anchors: enum { facing_face_centres },
        rotation_measure: enum { relative_rotation_vector_in_anchor_a_frame },
        solve: enum { implicit_compliant_constraint_same_pass_as_contact },
    },
    stiffness_grid: []const GridPoint,
    static_cases: StaticCases,
    dynamic_cases: DynamicCases,
    consistency_case: ConsistencyCase,
    determinism: struct { id: []const u8, requirement: enum { bit_identical_final_state_hash_on_replay } },
    reference_conventions: struct {
        reduced_mass: []const u8,
        reduced_inertia_about_link_axis: []const u8,
        damping_coefficient_from_ratio: []const u8,
        omega_for_resolution: []const u8,
    },
};

pub const ValidationError = error{
    UnsupportedSchemaVersion,
    NonPositiveValue,
    EmptyGrid,
    DuplicateId,
    NotUnitVector,
    GravityNotVerticalDown,
    DirectionNotHorizontal,
    InvalidWindow,
    FixtureNotCube,
    GridNotIsotropic,
    DampingRatioOutOfRange,
    PhysicalDampingNotUnderdamped,
    NumericalBoundNotBelowPhysical,
    StretchExceedsRestLength,
    TwistOutOfRange,
    PretensionOutOfRange,
    InvalidFrictionPair,
    LoadFractionOutOfRange,
    TooFewPeriods,
    ConventionMismatch,
    NonDiscreteSteps,
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

fn window(start: f64, end: f64) ValidationError!void {
    if (!(start >= 0 and start < end)) return error.InvalidWindow;
}

fn unit(v: [3]f64) ValidationError!void {
    const n = @sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);
    if (@abs(n - 1.0) > 1e-12) return error.NotUnitVector;
}

/// Reference conventions the evaluator implements, matched exactly.
pub const convention_reduced_mass = "m_a*m_b/(m_a+m_b)";
pub const convention_reduced_inertia = "i_a*i_b/(i_a+i_b) for uniform cubes about a face-normal axis through the centre";
pub const convention_damping = "c = 2*zeta*sqrt(k*mass_or_inertia) with body-b mass for static cases and reduced mass for dynamic cases";
pub const convention_omega = "sqrt(k_axial/reduced_mass) for axial cases, sqrt(k_torsion/reduced_inertia) for torsion";

/// Smallest number of full periods a run must contain at the slowest grid
/// point. Three zero crossings (one full period) and two positive peaks are
/// the least the period and damping measures need; two periods is a margin
/// of one over that definitional minimum.
pub const min_periods_in_run: f64 = 2.0;

pub fn validate(c: Criteria) ValidationError!void {
    if (c.schema_version != schema_version) return error.UnsupportedSchemaVersion;
    if (c.criteria_version == 0) return error.NonPositiveValue;
    const tu: time.TimeUnit = .{ .numerator = c.time_unit.numerator_s, .denominator = c.time_unit.denominator_s };
    try tu.validate();
    if (c.physics_step_ticks.len == 0) return error.EmptyGrid;
    for (c.physics_step_ticks, 0..) |s, i| {
        _ = try time.PhysicsStep.init(.{ .ticks = s });
        for (c.physics_step_ticks[0..i]) |p| if (p == s) return error.DuplicateId;
    }
    try positive(c.resolution.max_omega_dt);

    try positive(c.gravity.magnitude_m_s2);
    try unit(c.gravity.direction_world);
    if (c.gravity.direction_world[2] != -1.0) return error.GravityNotVerticalDown;

    const f = c.fixture;
    try positive(f.mass_kg);
    for (f.size_m) |s| try positive(s);
    // The reduced-inertia convention is exact only for a cube.
    if (f.size_m[0] != f.size_m[1] or f.size_m[1] != f.size_m[2]) return error.FixtureNotCube;
    try positive(c.link.rest_length_m);

    if (c.stiffness_grid.len == 0) return error.EmptyGrid;
    for (c.stiffness_grid, 0..) |p, i| {
        for (c.stiffness_grid[0..i]) |q| if (std.mem.eql(u8, p.id, q.id)) return error.DuplicateId;
        inline for (.{ "k_axial_n_m", "k_shear_n_m", "k_torsion_nm_rad", "k_bend_nm_rad" }) |name| try positive(@field(p, name));
        // Q52 §3: k_axial = k_shear and k_torsion = k_bend.
        if (p.k_axial_n_m != p.k_shear_n_m or p.k_torsion_nm_rad != p.k_bend_nm_rad) return error.GridNotIsotropic;
    }

    if (!std.mem.eql(u8, c.reference_conventions.reduced_mass, convention_reduced_mass) or
        !std.mem.eql(u8, c.reference_conventions.reduced_inertia_about_link_axis, convention_reduced_inertia) or
        !std.mem.eql(u8, c.reference_conventions.damping_coefficient_from_ratio, convention_damping) or
        !std.mem.eql(u8, c.reference_conventions.omega_for_resolution, convention_omega)) return error.ConventionMismatch;

    // Static cases.
    {
        const s = c.static_cases;
        if (!(s.damping_ratio_on_body_b >= 0)) return error.DampingRatioOutOfRange;
        try window(s.window_start_s, s.duration_s);
        inline for (.{ s.axial.force_rel_tol, s.axial.elongation_rel_tol, s.shear_bending.force_rel_tol, s.shear_bending.moment_rel_tol, s.shear_bending.displacement_rel_tol, s.shear_bending.angle_rel_tol, s.torsion.torque_about_link_axis_nm, s.torsion.torque_rel_tol, s.torsion.twist_rel_tol }) |v| try positive(v);
        try unit(s.shear_bending.load_world_direction);
        if (s.shear_bending.load_world_direction[2] != 0) return error.DirectionNotHorizontal;
        if (!(s.shear_bending.load_over_weight > 0 and s.shear_bending.load_over_weight < 1)) return error.LoadFractionOutOfRange;
        try steps(tu, c.physics_step_ticks, s.duration_s);
    }

    // Dynamic cases.
    {
        const d = c.dynamic_cases;
        try positive(d.duration_s);
        try steps(tu, c.physics_step_ticks, d.duration_s);
        if (d.axial.damping_ratio != 0 or d.torsion.damping_ratio != 0 or d.numerical_dissipation.damping_ratio != 0) return error.DampingRatioOutOfRange;
        const pd = d.physical_damping;
        if (!(pd.damping_ratio > 0 and pd.damping_ratio < 1)) return error.PhysicalDampingNotUnderdamped;
        // Numerics must not be able to masquerade as physics (PHY-006).
        if (!(d.numerical_dissipation.zeta_num_max > 0 and d.numerical_dissipation.zeta_num_max < pd.damping_ratio)) return error.NumericalBoundNotBelowPhysical;
        for ([_]f64{ d.axial.initial_stretch_m, pd.initial_stretch_m, d.numerical_dissipation.initial_stretch_m }) |x| {
            try positive(x);
            if (x >= c.link.rest_length_m) return error.StretchExceedsRestLength;
        }
        try positive(d.torsion.initial_twist_rad);
        if (d.torsion.initial_twist_rad >= std.math.pi / 2.0) return error.TwistOutOfRange;
        inline for (.{ d.axial.period_rel_tol, d.torsion.period_rel_tol, pd.zeta_rel_tol, d.momentum.rel_tol_of_m_g_t, d.momentum.abs_floor_kg_m_s }) |v| try positive(v);

        // Every grid point must contain enough periods to measure (slowest
        // axial and torsional oscillators).
        const m = f.mass_kg;
        const inertia = m * f.size_m[0] * f.size_m[0] / 6.0;
        for (c.stiffness_grid) |p| {
            const t_axial = 2.0 * std.math.pi * @sqrt((m / 2.0) / p.k_axial_n_m);
            const t_torsion = 2.0 * std.math.pi * @sqrt((inertia / 2.0) / p.k_torsion_nm_rad);
            if (d.duration_s < min_periods_in_run * @max(t_axial, t_torsion)) return error.TooFewPeriods;
        }
    }

    // Consistency case.
    {
        const k = c.consistency_case;
        if (!(k.pretension_over_weight > 0 and k.pretension_over_weight < 1)) return error.PretensionOutOfRange;
        if (!(k.damping_ratio_on_body_b >= 0)) return error.DampingRatioOutOfRange;
        if (!(k.friction_pair.mu_kinetic > 0 and k.friction_pair.mu_static > k.friction_pair.mu_kinetic)) return error.InvalidFrictionPair;
        try window(k.window_start_s, k.duration_s);
        try positive(k.sum_rel_tol);
        try steps(tu, c.physics_step_ticks, k.duration_s);
    }
}

/// A duration must be a whole number of steps at every grid timestep.
fn steps(tu: time.TimeUnit, step_ticks: []const u64, duration_s: f64) ValidationError!void {
    const ticks_f = duration_s * @as(f64, @floatFromInt(tu.denominator)) / @as(f64, @floatFromInt(tu.numerator));
    const ticks: u64 = @intFromFloat(@round(ticks_f));
    if (@as(f64, @floatFromInt(ticks)) != ticks_f) return error.NonDiscreteSteps;
    for (step_ticks) |s| if (ticks % s != 0) return error.NonDiscreteSteps;
}

/// The preregistered criteria file, embedded so its consistency is checked
/// on every build. Its identity is the SHA-256 of these exact bytes.
pub const link_v1_json = @embedFile("criteria_link_v1");

/// SHA-256 recorded in criteria/REGISTER.md. Registered files are never
/// edited in place; a revision is a new file and a new register entry.
pub const link_v1_sha256 = "7e147a9dda34caf73932b1734b41cccb70f0574cb3211b640624785312eb77f8";

/// Criteria v2 (Q53): supersedes v1's L2 bending references. v1 stays
/// embedded and checked so run 1 remains reproducible.
pub const link_v2_json = @embedFile("criteria_link_v2");
pub const link_v2_sha256 = "8cfe7c42b6829f4d90694e3b35378b45abe902fc1ecc221d30076e702b7e0c6e";

const testing = std.testing;

test "the embedded link criteria v2 file is byte-identical to its registered version" {
    const identity = @import("identity.zig");
    try testing.expectEqualStrings(link_v2_sha256, &identity.toHex(identity.fileIdentity(link_v2_json)));
}

test "criteria v2 selects the tension-lever bending reference; v1 keeps the schema default" {
    const v2 = try parse(testing.allocator, link_v2_json);
    defer v2.deinit();
    try testing.expectEqual(@as(u32, 2), v2.value.criteria_version);
    try testing.expectEqual(MomentReference.torque_balance_with_tension_lever, v2.value.static_cases.shear_bending.moment_reference);
    const v1 = try parse(testing.allocator, link_v1_json);
    defer v1.deinit();
    try testing.expectEqual(MomentReference.load_times_half_size, v1.value.static_cases.shear_bending.moment_reference);
}

test "the embedded link criteria file is byte-identical to its registered version" {
    const identity = @import("identity.zig");
    try testing.expectEqualStrings(link_v1_sha256, &identity.toHex(identity.fileIdentity(link_v1_json)));
}

test "the registered link criteria file parses and is self-consistent" {
    const p = try parse(testing.allocator, link_v1_json);
    defer p.deinit();
    try testing.expectEqual(@as(usize, 3), p.value.stiffness_grid.len);
    try testing.expectEqualSlices(u64, &.{ 500, 1000, 2000 }, p.value.physics_step_ticks);
    try testing.expectEqual(@as(f64, 0.2), p.value.resolution.max_omega_dt);
    try testing.expectEqual(@as(f64, 0.01), p.value.dynamic_cases.numerical_dissipation.zeta_num_max);
}

fn expectInvalid(expected: anyerror, needle: []const u8, replacement: []const u8) !void {
    const gpa = testing.allocator;
    const at = std.mem.indexOf(u8, link_v1_json, needle) orelse return error.TestNeedleNotFound;
    const text = try std.mem.concat(gpa, u8, &.{ link_v1_json[0..at], replacement, link_v1_json[at + needle.len ..] });
    defer gpa.free(text);
    if (parse(gpa, text)) |p| {
        p.deinit();
        return error.TestUnexpectedSuccess;
    } else |err| try testing.expectEqual(expected, err);
}

test "consistency rules reject ambiguous or self-defeating link criteria" {
    // Numerics must stay below physical damping (PHY-006).
    try expectInvalid(error.NumericalBoundNotBelowPhysical, "\"zeta_num_max\": 0.01", "\"zeta_num_max\": 0.05");
    try expectInvalid(error.PhysicalDampingNotUnderdamped, "\"damping_ratio\": 0.05", "\"damping_ratio\": 1.0");
    // The L7 case must have c = 0.
    try expectInvalid(error.DampingRatioOutOfRange, "\"initial_stretch_m\": 0.0005, \"damping_ratio\": 0.0, \"zeta_measure\"", "\"initial_stretch_m\": 0.0005, \"damping_ratio\": 0.01, \"zeta_measure\"");
    // Q52 grid isotropy.
    try expectInvalid(error.GridNotIsotropic, "\"k_shear_n_m\": 100.0", "\"k_shear_n_m\": 101.0");
    // Gravity must point down; the load must be horizontal.
    try expectInvalid(error.GravityNotVerticalDown, "\"direction_world\": [0, 0, -1]", "\"direction_world\": [0, -1, 0]");
    try expectInvalid(error.DirectionNotHorizontal, "\"load_world_direction\": [1, 0, 0]", "\"load_world_direction\": [0, 0, 1]");
    // The reduced-inertia reference is exact only for a cube.
    try expectInvalid(error.FixtureNotCube, "\"size_m\": [0.02, 0.02, 0.02]", "\"size_m\": [0.02, 0.02, 0.03]");
    // Windows, pretension, stretch, and measurement conventions.
    try expectInvalid(error.InvalidWindow, "\"window_start_s\": 1.5,\n    \"axial\"", "\"window_start_s\": 2.5,\n    \"axial\"");
    try expectInvalid(error.PretensionOutOfRange, "\"pretension_over_weight\": 0.5", "\"pretension_over_weight\": 1.5");
    try expectInvalid(error.StretchExceedsRestLength, "\"initial_stretch_m\": 0.0005, \"damping_ratio\": 0.05", "\"initial_stretch_m\": 0.05, \"damping_ratio\": 0.05");
    try expectInvalid(error.ConventionMismatch, "\"reduced_mass\": \"m_a*m_b/(m_a+m_b)\"", "\"reduced_mass\": \"m_a+m_b\"");
    // A run too short to contain periods at the slowest grid point.
    try expectInvalid(error.TooFewPeriods, "\"duration_s\": 1.0,", "\"duration_s\": 0.1,");
    // A duration that is not a whole number of steps at every grid timestep.
    try expectInvalid(error.NonDiscreteSteps, "\"duration_s\": 1.0,", "\"duration_s\": 1.0003,");
}

test "strict parsing still applies to the link criteria file" {
    try expectInvalid(error.UnknownField, "\"criteria_version\": 1,", "\"criteria_version\": 1, \"extra\": 0,");
    try expectInvalid(error.IntegerNotExact, "\"criteria_version\": 1", "\"criteria_version\": 1.0");
    try expectInvalid(error.InvalidEnumTag, "\"outcome_rule\": \"evaluated_combinations_all_pass_else_uncertain_if_mixed\"", "\"outcome_rule\": \"all_combinations_pass_else_uncertain_if_mixed\"");
    try expectInvalid(error.MissingField, "\"momentum\": { \"id\": \"L8_momentum\", ", "\"momentum\": { ");
}
