//! Coupler-engagement qualification criteria, schema version 1 (Q35, Q36,
//! Q40, Q41, Q43, Q46, Q47, Q48, Q52, Q53, Q54, Q56, Q57).
//!
//! Parsed through `strict_json` and validated fail-closed, in the same way as
//! `link_criteria.zig`. Every descriptive string that selects a measurement
//! or a model is an enum with a single admissible value, or an exactly
//! matched `convention_*` constant, so a criteria file that changes how
//! something is measured is rejected here rather than silently reinterpreted
//! by the evaluator. This file parses and validates criteria only; it
//! contains no solver or evaluator code.

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

pub const GuideFriction = struct { mu_static: f64, mu_kinetic: f64 };

pub const Socket = struct {
    shape: enum { square_pyramid_recess_edges_along_body_axes },
    apex_depth_m: f64,
    mouth_half_width_m: f64,
};

pub const Probe = struct {
    shape: enum { sphere_on_massless_noncolliding_stem },
    radius_m: f64,
    stem_length_m: f64,
};

pub const GuideContact = struct {
    features: enum { facets_face_rim_edges_rim_corners_voronoi_gated },
    normal_law: enum { tabletop_protocol_compliant_normal },
    contact_stiffness_n_m: f64,
    contact_damping_n_s_m: f64,
    static_slip_speed_m_s: f64,
};

pub const FullStiffness = struct {
    k_axial_n_m: f64,
    k_shear_n_m: f64,
    k_torsion_nm_rad: f64,
    k_bend_nm_rad: f64,
};

pub const FullLimits = struct { tension_n: f64, shear_n: f64, bending_nm: f64, torsion_nm: f64 };

pub const LatchLink = struct {
    model: enum { six_dof_spring_damper_between_anchor_frames },
    anchor_b: enum { probe_centre },
    anchor_a: enum { seat_point_moved_inward_by_preload_offset },
    preload_offset_m: f64,
    rest_length_m: f64,
    full_stiffness: FullStiffness,
    full_damping_ratio: f64,
    full_limits: FullLimits,
    compression: enum { no_link_limit_carried_by_seat },
    combined_loading: enum { independent_per_axis },
    engagement_law: enum { linear_in_pawl_travel_for_stiffness_damping_and_limits },
};

pub const Pawl = struct {
    travel_m: f64,
    speed_limit_m_s: f64,
    actuator_force_limit_n: f64,
    friction_coefficient: f64,
    normal_load: enum { reported_link_tension_if_positive },
    cam_out_force: enum { minus_half_sum_k_full_times_reported_coordinate_squared_over_travel },
    unpowered: enum { self_locking_no_motion },
    capture_zone: struct { radial_m: f64, axial_m: f64 },
    update: enum { after_each_step_from_that_steps_solver_report },
};

pub const Separation = struct {
    rule: enum { any_axis_solver_load_above_engagement_scaled_limit_removes_link_before_next_step },
    damage_model: enum { none },
    rearm: enum { after_pawl_returns_to_zero_travel },
};

pub const StandIn = struct {
    id: []const u8,
    socket: Socket,
    probe: Probe,
    guide_contact: GuideContact,
    latch_link: LatchLink,
    pawl: Pawl,
    separation: Separation,
};

pub const Statics = struct {
    setup: enum { body_a_static_above_body_b_hanging_coupler_axis_world_minus_z_seated_fully_engaged },
    guide_friction: GuideFriction,
    duration_s: f64,
    window_start_s: f64,
    seated_preload: struct { id: []const u8, force_rel_tol: f64 },
    seat_separation: struct {
        id: []const u8,
        below_factor: f64,
        above_factor: f64,
        force_rel_tol: f64,
        open_seat_normal_max_n: f64,
    },
};

pub const Axis = enum { tension, shear, bending, torsion };

pub const LinkLimits = struct {
    id: []const u8,
    setup: enum { link_only_two_free_bodies_in_free_fall_equal_and_opposite_loads_at_anchors },
    engagements: []const f64,
    axes: []const Axis,
    below_factor: f64,
    above_factor: f64,
    ramp_duration_s: f64,
    duration_s: f64,
    hold_window_start_s: f64,
    separation_load_rel_tol: f64,
    hold_deflection_rel_tol: f64,
};

pub const Engagement = struct {
    id: []const u8,
    setup: enum { two_free_bodies_in_free_fall_ball_at_seat_point_zero_travel_engage_from_t0 },
    guide_friction: GuideFriction,
    duration_s: f64,
    window_start_s: f64,
    blocked_axial_offset_m: f64,
    completion_time_tol_steps: u32,
    preload_rel_tol: f64,
};

pub const ReleaseUnderLoad = struct {
    id: []const u8,
    setup: enum { body_a_static_above_body_b_hanging_seated_fully_engaged_axial_load_on_b_release_from_t_release },
    guide_friction: GuideFriction,
    release_start_s: f64,
    duration_s: f64,
    below_factor: f64,
    above_factor: f64,
    reference: enum { rk4_one_dof_axial_link_only_model_step_1us },
    separation_time_tol_steps: u32,
};

pub const UnloadedRelease = struct {
    id: []const u8,
    setup: enum { two_free_bodies_in_free_fall_seated_fully_engaged_release_from_t_release },
    guide_friction: GuideFriction,
    release_start_s: f64,
    duration_s: f64,
    removal_time_tol_steps: u32,
    max_tension_step_change_over_quasi_static: f64,
};

pub const StiffDynamics = struct {
    id: []const u8,
    setup: enum { link_only_two_free_bodies_in_free_fall_pawl_held },
    engagements: []const f64,
    duration_s: f64,
    initial_stretch_m: f64,
    initial_twist_rad: f64,
    physical_damping_ratio: f64,
    period_measure: enum { mean_of_full_periods_from_linear_interpolated_zero_crossings },
    zeta_measure: enum { log_of_ratio_of_first_and_last_positive_peaks_over_full_periods_divided_by_2pi_n },
    period_rel_tol: f64,
    zeta_rel_tol: f64,
    zeta_num_max: f64,
};

pub const OffsetDirection = enum { toward_facet, toward_corner };

pub const FrictionPair = struct { id: []const u8, mu_static: f64, mu_kinetic: f64 };

pub const CaptureSweep = struct {
    id: []const u8,
    setup: enum { two_free_bodies_in_free_fall_b_approaches_along_minus_axis_engage_from_t0 },
    duration_s: f64,
    initial_axial_m: f64,
    approach_speeds_m_s: []const f64,
    lateral_offsets_m: []const f64,
    misalignments_rad: []const f64,
    offset_directions: []const OffsetDirection,
    friction_pairs: []const FrictionPair,
    outcomes: enum { classified_from_final_state_reported_not_gated },
    validity: enum { no_cube_cube_overlap_and_probe_over_face_else_outside_model },
};

pub const Audits = struct {
    applies_to: enum { every_run_of_c1_to_c8 },
    momentum: struct { rel_tol_of_m_g_t: f64, abs_floor_kg_m_s: f64 },
    impulse_accounting: struct { rel_tol_of_step_impulse_sum: f64, abs_floor_n_s: f64 },
    pose_integration: enum { bit_identical_to_semi_implicit_update },
    energy: struct {
        applies_to: enum { free_fall_runs_without_validation_loads },
        frame: enum { centre_of_mass },
        creation_rel_tol: f64,
        /// Q60: coefficient of the first-order omega*dt term of the
        /// allowance. Absent in criteria v1, where it is 0.
        first_order_omega_dt_coefficient: f64 = 0.0,
        abs_floor_j: f64,
    },
};

pub const Control = enum { velocity_snap_on_link_activation, pose_snap_on_link_activation };

pub const SweepPoint = struct {
    approach_speed_m_s: f64,
    lateral_offset_m: f64,
    misalignment_rad: f64,
    offset_direction: OffsetDirection,
    friction_pair: []const u8,
};

pub const AuditDiscrimination = struct {
    id: []const u8,
    controls: []const Control,
    sweep_point: SweepPoint,
    requirement: enum { each_control_fails_its_audit_at_every_timestep },
};

pub const ReferenceConventions = struct {
    reduced_mass: []const u8,
    reduced_inertia_about_link_axis: []const u8,
    damping_coefficient_from_ratio: []const u8,
    omega_for_resolution: []const u8,
    seat_stiffness: []const u8,
    preload: []const u8,
    seat_separation_pull: []const u8,
    release_block_tension: []const u8,
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
    stand_in: StandIn,
    solver_reference: enum { compliant_link_protocol_settings },
    statics: Statics,
    link_limits: LinkLimits,
    engagement: Engagement,
    release_under_load: ReleaseUnderLoad,
    unloaded_release: UnloadedRelease,
    stiff_dynamics: StiffDynamics,
    capture_sweep: CaptureSweep,
    audits: Audits,
    audit_discrimination: AuditDiscrimination,
    determinism: struct { id: []const u8, requirement: enum { bit_identical_final_state_hash_on_replay } },
    reference_conventions: ReferenceConventions,
};

pub const ValidationError = error{
    UnsupportedSchemaVersion,
    NonPositiveValue,
    EmptyGrid,
    DuplicateEntry,
    NotUnitVector,
    GravityNotVerticalDown,
    FixtureNotCube,
    InvalidWindow,
    DampingRatioOutOfRange,
    ProbeGeometryInconsistent,
    PreloadOffsetOutOfRange,
    FrictionCoefficientOutOfRange,
    FactorOutOfRange,
    EngagementOutOfRange,
    InvalidFrictionPair,
    ToleranceOutOfRange,
    TwistOutOfRange,
    NumericalBoundNotBelowPhysical,
    SweepListNotAscending,
    SweepPointNotInCaptureSweep,
    ConventionMismatch,
    NonDiscreteSteps,
    CaptureZoneInconsistent,
} || time.Error;

pub fn parse(gpa: std.mem.Allocator, text: []const u8) (strict_json.Error || ValidationError)!strict_json.Parsed(Criteria) {
    const parsed = try strict_json.parse(Criteria, gpa, text, .{});
    errdefer parsed.deinit();
    try validate(parsed.value);
    return parsed;
}

/// Reference conventions the evaluator implements, matched exactly.
pub const convention_reduced_mass = "m_a*m_b/(m_a+m_b)";
pub const convention_reduced_inertia = "i_a*i_b/(i_a+i_b) for uniform cubes about a face-normal axis through the centre";
pub const convention_damping = "c_full = 2*zeta*sqrt(k_full*reduced_mass_or_inertia); rows use e*c_full";
pub const convention_omega = "sqrt(e*k_axial_full/reduced_mass) for axial runs, sqrt(e*k_torsion_full/reduced_inertia) for torsion runs";
pub const convention_seat_stiffness = "k_s = 4*k_contact*sin(alpha)^2, alpha = atan(mouth_half_width/apex_depth)";
pub const convention_preload = "P = e*k_axial_full*preload_offset*k_s/(e*k_axial_full + k_s)";
pub const convention_seat_separation_pull = "F_sep = e*k_axial_full*preload_offset";
pub const convention_release_block_tension = "T_block = k*u*mu_p - sqrt((k*u*mu_p)^2 - 2*k*u*F_act), k = k_axial_full, u = travel, at e = 1";

fn positive(v: f64) ValidationError!void {
    if (!(v > 0)) return error.NonPositiveValue;
}

fn nonNegative(v: f64) ValidationError!void {
    if (!(v >= 0)) return error.NonPositiveValue;
}

/// A relative tolerance: strictly between 0 and 1.
fn relTol(v: f64) ValidationError!void {
    if (!(v > 0 and v < 1)) return error.ToleranceOutOfRange;
}

fn window(start: f64, end: f64) ValidationError!void {
    if (!(start >= 0 and start < end)) return error.InvalidWindow;
}

fn unit(v: [3]f64) ValidationError!void {
    const n = @sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);
    if (@abs(n - 1.0) > 1e-12) return error.NotUnitVector;
}

/// below_factor in (0, 1) and above_factor > 1.
fn factors(below: f64, above: f64) ValidationError!void {
    if (!(below > 0 and below < 1 and above > 1)) return error.FactorOutOfRange;
}

fn frictionZero(f: GuideFriction) ValidationError!void {
    try nonNegative(f.mu_static);
    try nonNegative(f.mu_kinetic);
}

/// Engagement lists: nonempty, each in (0, 1], no duplicates.
fn engagements(list: []const f64) ValidationError!void {
    if (list.len == 0) return error.EmptyGrid;
    for (list, 0..) |e, i| {
        if (!(e > 0 and e <= 1)) return error.EngagementOutOfRange;
        for (list[0..i]) |p| if (p == e) return error.DuplicateEntry;
    }
}

/// Sweep list: nonempty, strictly ascending (so also duplicate-free), and
/// positive (or merely nonnegative when `allow_zero`).
fn ascending(list: []const f64, allow_zero: bool) ValidationError!void {
    if (list.len == 0) return error.EmptyGrid;
    for (list, 0..) |v, i| {
        if (allow_zero) try nonNegative(v) else try positive(v);
        if (i > 0 and !(v > list[i - 1])) return error.SweepListNotAscending;
    }
}

fn distinctEnums(comptime E: type, list: []const E) ValidationError!void {
    if (list.len == 0) return error.EmptyGrid;
    for (list, 0..) |v, i| for (list[0..i]) |p| if (p == v) return error.DuplicateEntry;
}

fn contains(list: []const f64, v: f64) bool {
    for (list) |x| if (x == v) return true;
    return false;
}

pub fn validate(c: Criteria) ValidationError!void {
    if (c.schema_version != schema_version) return error.UnsupportedSchemaVersion;
    if (c.criteria_version == 0) return error.NonPositiveValue;
    const tu: time.TimeUnit = .{ .numerator = c.time_unit.numerator_s, .denominator = c.time_unit.denominator_s };
    try tu.validate();
    if (c.physics_step_ticks.len == 0) return error.EmptyGrid;
    for (c.physics_step_ticks, 0..) |s, i| {
        _ = try time.PhysicsStep.init(.{ .ticks = s });
        for (c.physics_step_ticks[0..i]) |p| if (p == s) return error.DuplicateEntry;
    }
    const grid = c.physics_step_ticks;
    try positive(c.resolution.max_omega_dt);

    if (c.decisions.len == 0) return error.EmptyGrid;
    try positive(c.gravity.magnitude_m_s2);
    try unit(c.gravity.direction_world);
    if (c.gravity.direction_world[2] != -1.0) return error.GravityNotVerticalDown;

    const f = c.fixture;
    try positive(f.mass_kg);
    for (f.size_m) |s| try positive(s);
    // The reduced-inertia convention is exact only for a cube.
    if (f.size_m[0] != f.size_m[1] or f.size_m[1] != f.size_m[2]) return error.FixtureNotCube;

    // Stand-in geometry and link/pawl parameters.
    const si = c.stand_in;
    const sk = si.socket;
    const pr = si.probe;
    try positive(sk.apex_depth_m);
    try positive(sk.mouth_half_width_m);
    try positive(pr.radius_m);
    try positive(pr.stem_length_m);
    {
        // The ball must seat on the facets strictly inside the recess:
        // seat x (along the axis from the mouth plane, positive outward)
        // = r/sin(alpha) - apex_depth, which must lie in (-apex_depth, 0).
        const alpha = std.math.atan(sk.mouth_half_width_m / sk.apex_depth_m);
        const x = pr.radius_m / @sin(alpha) - sk.apex_depth_m;
        if (!(x > -sk.apex_depth_m and x < 0)) return error.ProbeGeometryInconsistent;
    }
    const gc = si.guide_contact;
    try positive(gc.contact_stiffness_n_m);
    try positive(gc.contact_damping_n_s_m);
    try positive(gc.static_slip_speed_m_s);

    const ll = si.latch_link;
    try positive(ll.preload_offset_m);
    if (!(ll.preload_offset_m < 0.5 * pr.radius_m)) return error.PreloadOffsetOutOfRange;
    try nonNegative(ll.rest_length_m);
    try positive(ll.full_stiffness.k_axial_n_m);
    try positive(ll.full_stiffness.k_shear_n_m);
    try positive(ll.full_stiffness.k_torsion_nm_rad);
    try positive(ll.full_stiffness.k_bend_nm_rad);
    if (!(ll.full_damping_ratio > 0)) return error.DampingRatioOutOfRange;
    try positive(ll.full_limits.tension_n);
    try positive(ll.full_limits.shear_n);
    try positive(ll.full_limits.bending_nm);
    try positive(ll.full_limits.torsion_nm);

    const pw = si.pawl;
    try positive(pw.travel_m);
    try positive(pw.speed_limit_m_s);
    try positive(pw.actuator_force_limit_n);
    if (!(pw.friction_coefficient > 0 and pw.friction_coefficient < 1)) return error.FrictionCoefficientOutOfRange;
    try positive(pw.capture_zone.radial_m);
    try positive(pw.capture_zone.axial_m);
    if (c.criteria_version >= 2) {
        // Q60 item 3: the stretch at activation must lie inside the
        // load-limit stretch, which is independent of engagement.
        const delta = ll.preload_offset_m;
        const lim_ax = ll.full_limits.tension_n / ll.full_stiffness.k_axial_n_m;
        const lim_sh = ll.full_limits.shear_n / ll.full_stiffness.k_shear_n_m;
        const ax = pw.capture_zone.axial_m + delta;
        const rad = pw.capture_zone.radial_m;
        if (!(ax < lim_ax) or !(rad < lim_sh) or !(@sqrt(rad * rad + ax * ax) < lim_ax))
            return error.CaptureZoneInconsistent;
    }

    // Statics (C1, C2).
    {
        const s = c.statics;
        try frictionZero(s.guide_friction);
        try positive(s.duration_s);
        try window(s.window_start_s, s.duration_s);
        try steps(tu, grid, s.duration_s);
        try steps(tu, grid, s.window_start_s);
        try relTol(s.seated_preload.force_rel_tol);
        const sep = s.seat_separation;
        try factors(sep.below_factor, sep.above_factor);
        try relTol(sep.force_rel_tol);
        try positive(sep.open_seat_normal_max_n);
    }

    // Link limits (C3).
    {
        const l = c.link_limits;
        try engagements(l.engagements);
        try distinctEnums(Axis, l.axes);
        try factors(l.below_factor, l.above_factor);
        try positive(l.ramp_duration_s);
        try positive(l.duration_s);
        if (!(l.ramp_duration_s < l.duration_s)) return error.InvalidWindow;
        try window(l.hold_window_start_s, l.duration_s);
        if (!(l.hold_window_start_s >= l.ramp_duration_s)) return error.InvalidWindow;
        try steps(tu, grid, l.ramp_duration_s);
        try steps(tu, grid, l.duration_s);
        try steps(tu, grid, l.hold_window_start_s);
        try relTol(l.separation_load_rel_tol);
        try relTol(l.hold_deflection_rel_tol);
    }

    // Engagement (C4).
    {
        const e = c.engagement;
        try frictionZero(e.guide_friction);
        try positive(e.duration_s);
        try window(e.window_start_s, e.duration_s);
        try steps(tu, grid, e.duration_s);
        try steps(tu, grid, e.window_start_s);
        try positive(e.blocked_axial_offset_m);
        if (e.completion_time_tol_steps == 0) return error.NonPositiveValue;
        try relTol(e.preload_rel_tol);
    }

    // Release under load (C5).
    {
        const r = c.release_under_load;
        try frictionZero(r.guide_friction);
        try positive(r.release_start_s);
        try positive(r.duration_s);
        try window(r.release_start_s, r.duration_s);
        try steps(tu, grid, r.release_start_s);
        try steps(tu, grid, r.duration_s);
        try factors(r.below_factor, r.above_factor);
        if (r.separation_time_tol_steps == 0) return error.NonPositiveValue;
    }

    // Unloaded release (C6).
    {
        const u = c.unloaded_release;
        try frictionZero(u.guide_friction);
        try positive(u.release_start_s);
        try positive(u.duration_s);
        try window(u.release_start_s, u.duration_s);
        try steps(tu, grid, u.release_start_s);
        try steps(tu, grid, u.duration_s);
        if (u.removal_time_tol_steps == 0) return error.NonPositiveValue;
        try positive(u.max_tension_step_change_over_quasi_static);
    }

    // Stiff dynamics (C7).
    {
        const d = c.stiff_dynamics;
        try engagements(d.engagements);
        try positive(d.duration_s);
        try steps(tu, grid, d.duration_s);
        try positive(d.initial_stretch_m);
        try positive(d.initial_twist_rad);
        if (d.initial_twist_rad >= std.math.pi / 2.0) return error.TwistOutOfRange;
        if (!(d.physical_damping_ratio > 0 and d.physical_damping_ratio < 1)) return error.DampingRatioOutOfRange;
        try relTol(d.period_rel_tol);
        try relTol(d.zeta_rel_tol);
        // Numerics must not be able to masquerade as physics (PHY-006).
        if (!(d.zeta_num_max > 0 and d.zeta_num_max < d.physical_damping_ratio)) return error.NumericalBoundNotBelowPhysical;
    }

    // Capture sweep (C8).
    const cs = c.capture_sweep;
    {
        try positive(cs.duration_s);
        try steps(tu, grid, cs.duration_s);
        try positive(cs.initial_axial_m);
        try ascending(cs.approach_speeds_m_s, false);
        try ascending(cs.lateral_offsets_m, true);
        try ascending(cs.misalignments_rad, true);
        try distinctEnums(OffsetDirection, cs.offset_directions);
        if (cs.friction_pairs.len == 0) return error.EmptyGrid;
        for (cs.friction_pairs, 0..) |p, i| {
            for (cs.friction_pairs[0..i]) |q| if (std.mem.eql(u8, p.id, q.id)) return error.DuplicateEntry;
            try nonNegative(p.mu_kinetic);
            if (!(p.mu_static > p.mu_kinetic)) return error.InvalidFrictionPair;
        }
    }

    // Audits.
    {
        const a = c.audits;
        try relTol(a.momentum.rel_tol_of_m_g_t);
        try positive(a.momentum.abs_floor_kg_m_s);
        try relTol(a.impulse_accounting.rel_tol_of_step_impulse_sum);
        try positive(a.impulse_accounting.abs_floor_n_s);
        try relTol(a.energy.creation_rel_tol);
        try nonNegative(a.energy.first_order_omega_dt_coefficient);
        if (c.criteria_version >= 2 and !(a.energy.first_order_omega_dt_coefficient > 0)) return error.NonPositiveValue;
        try positive(a.energy.abs_floor_j);
    }

    // Audit discrimination (C9): the control point is a member of C8.
    {
        const d = c.audit_discrimination;
        try distinctEnums(Control, d.controls);
        const sp = d.sweep_point;
        if (!contains(cs.approach_speeds_m_s, sp.approach_speed_m_s) or
            !contains(cs.lateral_offsets_m, sp.lateral_offset_m) or
            !contains(cs.misalignments_rad, sp.misalignment_rad)) return error.SweepPointNotInCaptureSweep;
        if (std.mem.indexOfScalar(OffsetDirection, cs.offset_directions, sp.offset_direction) == null) return error.SweepPointNotInCaptureSweep;
        var pair_found = false;
        for (cs.friction_pairs) |p| {
            if (std.mem.eql(u8, p.id, sp.friction_pair)) pair_found = true;
        }
        if (!pair_found) return error.SweepPointNotInCaptureSweep;
    }

    const rc = c.reference_conventions;
    if (!std.mem.eql(u8, rc.reduced_mass, convention_reduced_mass) or
        !std.mem.eql(u8, rc.reduced_inertia_about_link_axis, convention_reduced_inertia) or
        !std.mem.eql(u8, rc.damping_coefficient_from_ratio, convention_damping) or
        !std.mem.eql(u8, rc.omega_for_resolution, convention_omega) or
        !std.mem.eql(u8, rc.seat_stiffness, convention_seat_stiffness) or
        !std.mem.eql(u8, rc.preload, convention_preload) or
        !std.mem.eql(u8, rc.seat_separation_pull, convention_seat_separation_pull) or
        !std.mem.eql(u8, rc.release_block_tension, convention_release_block_tension)) return error.ConventionMismatch;
}

/// A time must be a whole number of steps at every grid timestep.
fn steps(tu: time.TimeUnit, step_ticks: []const u64, duration_s: f64) ValidationError!void {
    const ticks_f = duration_s * @as(f64, @floatFromInt(tu.denominator)) / @as(f64, @floatFromInt(tu.numerator));
    const ticks: u64 = @intFromFloat(@round(ticks_f));
    if (@as(f64, @floatFromInt(ticks)) != ticks_f) return error.NonDiscreteSteps;
    for (step_ticks) |s| if (ticks % s != 0) return error.NonDiscreteSteps;
}

/// The preregistered criteria file, embedded so its consistency is checked
/// on every build. Its identity is the SHA-256 of these exact bytes.
pub const coupler_v1_json = @embedFile("criteria_coupler_v1");

/// SHA-256 recorded in criteria/REGISTER.md. Registered files are never
/// edited in place; a revision is a new file and a new register entry.
pub const coupler_v1_sha256 = "1f07a24b1b3de9cd5da825b9ef5153bb8f693f0cf399484b14921f5f6e0e8bdc";

/// Criteria v2 (Q60), registered before the code that consumes it.
pub const coupler_v2_json = @embedFile("criteria_coupler_v2");
pub const coupler_v2_sha256 = "72307066686fdd54c15e4052a12cdf3cdde785569d4bdb0e466e91d33dc58a02";

const testing = std.testing;

test "the embedded coupler criteria file is byte-identical to its registered version" {
    const identity = @import("identity.zig");
    try testing.expectEqualStrings(coupler_v1_sha256, &identity.toHex(identity.fileIdentity(coupler_v1_json)));
}

test "the registered coupler criteria file parses and is self-consistent" {
    const p = try parse(testing.allocator, coupler_v1_json);
    defer p.deinit();
    const v = p.value;
    try testing.expectEqualSlices(u64, &.{ 50, 100, 200 }, v.physics_step_ticks);
    try testing.expectEqual(@as(f64, 5e-5), v.stand_in.latch_link.preload_offset_m);
    try testing.expectEqual(@as(f64, 1e-3), v.stand_in.pawl.travel_m);
    try testing.expectEqual(@as(usize, 6), v.capture_sweep.lateral_offsets_m.len);
    try testing.expectEqual(@as(usize, 3), v.capture_sweep.approach_speeds_m_s.len);
    try testing.expectEqual(@as(usize, 2), v.capture_sweep.misalignments_rad.len);
    try testing.expectEqual(@as(usize, 2), v.capture_sweep.offset_directions.len);
    try testing.expectEqual(@as(usize, 2), v.capture_sweep.friction_pairs.len);
    try testing.expectEqual(@as(usize, 4), v.link_limits.axes.len);
    try testing.expectEqual(@as(usize, 2), v.audit_discrimination.controls.len);
    try testing.expectEqualStrings("mu_low", v.audit_discrimination.sweep_point.friction_pair);
}

fn expectInvalid(expected: anyerror, needle: []const u8, replacement: []const u8) !void {
    const gpa = testing.allocator;
    const at = std.mem.indexOf(u8, coupler_v1_json, needle) orelse return error.TestNeedleNotFound;
    const text = try std.mem.concat(gpa, u8, &.{ coupler_v1_json[0..at], replacement, coupler_v1_json[at + needle.len ..] });
    defer gpa.free(text);
    if (parse(gpa, text)) |p| {
        p.deinit();
        return error.TestUnexpectedSuccess;
    } else |err| try testing.expectEqual(expected, err);
}

test "numeric bound violations are rejected" {
    try expectInvalid(error.NonPositiveValue, "\"travel_m\": 0.001,", "\"travel_m\": 0.0,");
    try expectInvalid(error.NonPositiveValue, "\"actuator_force_limit_n\": 0.3", "\"actuator_force_limit_n\": -0.3");
    try expectInvalid(error.DampingRatioOutOfRange, "\"full_damping_ratio\": 0.2", "\"full_damping_ratio\": 0.0");
    try expectInvalid(error.PreloadOffsetOutOfRange, "\"preload_offset_m\": 0.00005", "\"preload_offset_m\": 0.002");
    try expectInvalid(error.FrictionCoefficientOutOfRange, "\"friction_coefficient\": 0.3", "\"friction_coefficient\": 1.5");
    try expectInvalid(error.FactorOutOfRange, "\"below_factor\": 0.9, \"above_factor\": 1.1, \"force_rel_tol\"", "\"below_factor\": 1.0, \"above_factor\": 1.1, \"force_rel_tol\"");
    try expectInvalid(error.FactorOutOfRange, "\"above_factor\": 1.1,\n    \"ramp", "\"above_factor\": 0.95,\n    \"ramp");
    try expectInvalid(error.EngagementOutOfRange, "[1.0, 0.5],\n    \"axes\"", "[1.0, 1.5],\n    \"axes\"");
    try expectInvalid(error.ToleranceOutOfRange, "\"creation_rel_tol\": 0.02", "\"creation_rel_tol\": 1.5");
    try expectInvalid(error.NumericalBoundNotBelowPhysical, "\"zeta_num_max\": 0.01", "\"zeta_num_max\": 0.05");
    try expectInvalid(error.TwistOutOfRange, "\"initial_twist_rad\": 0.002", "\"initial_twist_rad\": 2.0");
}

test "geometry, gravity, fixture, windows and friction consistency" {
    // Ball larger than the recess cannot seat inside it.
    try expectInvalid(error.ProbeGeometryInconsistent, "\"radius_m\": 0.002, \"stem", "\"radius_m\": 0.006, \"stem");
    try expectInvalid(error.GravityNotVerticalDown, "\"direction_world\": [0, 0, -1]", "\"direction_world\": [0, -1, 0]");
    try expectInvalid(error.FixtureNotCube, "\"size_m\": [0.02, 0.02, 0.02]", "\"size_m\": [0.02, 0.02, 0.03]");
    try expectInvalid(error.InvalidWindow, "\"window_start_s\": 0.4,", "\"window_start_s\": 0.6,");
    try expectInvalid(error.InvalidFrictionPair, "\"mu_static\": 0.3, \"mu_kinetic\": 0.2", "\"mu_static\": 0.2, \"mu_kinetic\": 0.3");
}

test "durations must be whole numbers of steps at every grid timestep" {
    try expectInvalid(error.NonDiscreteSteps, "\"duration_s\": 0.5,\n    \"window_start_s\": 0.4", "\"duration_s\": 0.500025,\n    \"window_start_s\": 0.4");
}

test "a convention string that differs from the implemented one is rejected" {
    try expectInvalid(error.ConventionMismatch, "\"reduced_mass\": \"m_a*m_b/(m_a+m_b)\"", "\"reduced_mass\": \"m_a+m_b\"");
    try expectInvalid(error.ConventionMismatch, "\"seat_separation_pull\": \"F_sep = e*k_axial_full*preload_offset\"", "\"seat_separation_pull\": \"F_sep = k_axial_full*preload_offset\"");
}

test "sweep lists and the audit control point are checked" {
    // Strictly ascending also rules out duplicates.
    try expectInvalid(error.SweepListNotAscending, "[0.0, 0.001, 0.002, 0.003", "[0.0, 0.001, 0.001, 0.003");
    try expectInvalid(error.SweepListNotAscending, "[0.02, 0.1, 0.3]", "[0.1, 0.02, 0.3]");
    try expectInvalid(error.NonPositiveValue, "[0.02, 0.1, 0.3]", "[-0.02, 0.1, 0.3]");
    try expectInvalid(error.EmptyGrid, "[0.0, 0.15]", "[]");
    try expectInvalid(error.DuplicateEntry, "[\"toward_facet\", \"toward_corner\"]", "[\"toward_facet\", \"toward_facet\"]");
    // C9 sweep point must be a member of the C8 lists.
    try expectInvalid(error.SweepPointNotInCaptureSweep, "\"approach_speed_m_s\": 0.1,", "\"approach_speed_m_s\": 0.15,");
    try expectInvalid(error.SweepPointNotInCaptureSweep, "\"lateral_offset_m\": 0.002,", "\"lateral_offset_m\": 0.0025,");
    try expectInvalid(error.SweepPointNotInCaptureSweep, "\"friction_pair\": \"mu_low\"", "\"friction_pair\": \"mu_high\"");
}

test "strict parsing still applies to the coupler criteria file" {
    try expectInvalid(error.UnknownField, "\"criteria_version\": 1,", "\"criteria_version\": 1, \"extra\": 0,");
    try expectInvalid(error.IntegerNotExact, "\"completion_time_tol_steps\": 2", "\"completion_time_tol_steps\": 2.0");
    try expectInvalid(error.InvalidEnumTag, "\"shape\": \"cuboid\"", "\"shape\": \"sphere\"");
    try expectInvalid(error.InvalidEnumTag, "\"velocity_snap_on_link_activation\"", "\"velocity_snap\"");
    try expectInvalid(error.MissingField, "\"completion_time_tol_steps\": 2,\n    ", "");
}

test "the embedded coupler criteria v2 file is byte-identical to its registered version" {
    const identity = @import("identity.zig");
    try testing.expectEqualStrings(coupler_v2_sha256, &identity.toHex(identity.fileIdentity(coupler_v2_json)));
}

test "criteria v2 parses with its key values and v1 still parses with a zero coefficient" {
    const p = try parse(testing.allocator, coupler_v2_json);
    defer p.deinit();
    const v = p.value;
    try testing.expectEqual(@as(u32, 2), v.criteria_version);
    try testing.expectEqual(@as(f64, 5e-5), v.stand_in.pawl.capture_zone.radial_m);
    try testing.expectEqual(@as(f64, 1e-4), v.stand_in.pawl.capture_zone.axial_m);
    try testing.expectEqualSlices(f64, &.{ 0.0, 0.005, 0.15 }, v.capture_sweep.misalignments_rad);
    try testing.expectEqual(@as(f64, 1.0), v.audits.energy.first_order_omega_dt_coefficient);
    const p1 = try parse(testing.allocator, coupler_v1_json);
    defer p1.deinit();
    try testing.expectEqual(@as(f64, 0.0), p1.value.audits.energy.first_order_omega_dt_coefficient);
    try testing.expectEqual(@as(f64, 2e-4), p1.value.stand_in.pawl.capture_zone.radial_m);
}

fn expectInvalidV2(expected: anyerror, needle: []const u8, replacement: []const u8) !void {
    const gpa = testing.allocator;
    const at = std.mem.indexOf(u8, coupler_v2_json, needle) orelse return error.TestNeedleNotFound;
    const text = try std.mem.concat(gpa, u8, &.{ coupler_v2_json[0..at], replacement, coupler_v2_json[at + needle.len ..] });
    defer gpa.free(text);
    if (parse(gpa, text)) |p| {
        p.deinit();
        return error.TestUnexpectedSuccess;
    } else |err| try testing.expectEqual(expected, err);
}

test "v2 capture-zone consistency rule and energy coefficient are enforced" {
    const zone = "\"capture_zone\": { \"radial_m\": 0.00005, \"axial_m\": 0.0001 }";
    // v1's zone (0.2 mm / 0.2 mm) violates the rule under version 2.
    try expectInvalidV2(error.CaptureZoneInconsistent, zone, "\"capture_zone\": { \"radial_m\": 0.0002, \"axial_m\": 0.0002 }");
    // Radial alone at the shear-limit stretch (0.1 mm) is rejected.
    try expectInvalidV2(error.CaptureZoneInconsistent, zone, "\"capture_zone\": { \"radial_m\": 0.0002, \"axial_m\": 0.0001 }");
    try expectInvalidV2(error.CaptureZoneInconsistent, zone, "\"capture_zone\": { \"radial_m\": 0.0001, \"axial_m\": 0.0001 }");
    // Axial plus preload offset at the tension-limit stretch is rejected.
    try expectInvalidV2(error.CaptureZoneInconsistent, zone, "\"capture_zone\": { \"radial_m\": 0.00005, \"axial_m\": 0.00015 }");
    // Combined: each inside its own limit, the norm outside (0.09 mm, 0.19 mm total axial).
    try expectInvalidV2(error.CaptureZoneInconsistent, zone, "\"capture_zone\": { \"radial_m\": 0.00009, \"axial_m\": 0.00014 }");
    // Coefficient: negative and zero are rejected for v2.
    try expectInvalidV2(error.NonPositiveValue, "\"first_order_omega_dt_coefficient\": 1.0", "\"first_order_omega_dt_coefficient\": -1.0");
    try expectInvalidV2(error.NonPositiveValue, "\"first_order_omega_dt_coefficient\": 1.0", "\"first_order_omega_dt_coefficient\": 0.0");
    // The v2 text still passes the other v2-aware mutations of v1 tests.
    try expectInvalidV2(error.ToleranceOutOfRange, "\"creation_rel_tol\": 0.02", "\"creation_rel_tol\": 1.5");
}
