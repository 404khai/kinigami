//! Gate 1 paper-feasibility criteria, schema version 1 (Q38, Q61, Q62).
//!
//! Parsed through `strict_json` and validated fail-closed, in the same way as
//! `link_criteria.zig`. Each item carries a fixed set of named parameters.
//! The evaluator implements specific conventions (the 64 rim points, the 26
//! sphere directions, three chain units, the GJK test), so a parameter that
//! selects one of them must hold exactly the implemented value, and a file
//! that changes it is rejected here rather than reinterpreted. Numeric
//! tolerances are read from the file. This file parses and validates only;
//! it contains no evaluator code.

const std = @import("std");
const strict_json = @import("strict_json.zig");

pub const schema_version: u32 = 1;

pub const Status = enum { evidence, provisional };

/// One named parameter: a value, whether it is evidence or provisional, and
/// the written basis.
pub fn Param(comptime T: type) type {
    return struct {
        value: T,
        status: Status,
        basis: []const u8,
    };
}

pub const Threshold = struct {
    status: enum { unresolved },
    reason: []const u8,
};

pub const Endurance = struct {
    reported: bool,
    threshold: Threshold,
};

/// Superset of every item's parameters. Each item must carry exactly its own
/// set (checked in `validate`); the rest stay null.
pub const Params = struct {
    // G1
    max_diameter_um: ?Param(f64) = null,
    uncertain_band_um: ?Param(f64) = null,
    round_rim_points: ?Param(u32) = null,
    sphere_seed_directions: ?Param(u32) = null,
    // G2 (interference_erosion_um is shared with G5)
    interference_erosion_um: ?Param(f64) = null,
    min_clearance_um: ?Param(f64) = null,
    containment_tolerance_um: ?Param(f64) = null,
    intersection_algorithm: ?Param([]const u8) = null,
    gjk_iteration_cap: ?Param(u32) = null,
    assembly_access_statement_min_chars: ?Param(u32) = null,
    // G3
    allowed_source_kinds: ?Param([]const []const u8) = null,
    allowed_bases: ?Param([]const []const u8) = null,
    access_date_format: ?Param([]const u8) = null,
    // G4
    mass_sum_tolerance_mg: ?Param(f64) = null,
    derived_mass_tolerance_mg: ?Param(f64) = null,
    peak_power_rule: ?Param([]const u8) = null,
    exactly_one_energy_source: ?Param(bool) = null,
    // G5
    min_coupler_sites: ?Param(u32) = null,
    chain_units: ?Param(u32) = null,
    contact_tolerance_um: ?Param(f64) = null,
    support_rule: ?Param([]const u8) = null,
    tabletop_penetration_tolerance_um: ?Param(f64) = null,
    // G6
    requires_power_to_hold: ?Param(bool) = null,
    bounded_independent_release_declared: ?Param(bool) = null,
    magnetism_requires_declared_component: ?Param(bool) = null,
    justification_record_path_pattern: ?Param([]const u8) = null,
    // G7
    review_stage: ?Param([]const u8) = null,
    reviewer_must_differ_from_author: ?Param(bool) = null,
    review_path_pattern: ?Param([]const u8) = null,
    // G8
    forbidden_reference_classes: ?Param([]const []const u8) = null,
    exclusions: ?Param([]const []const u8) = null,
};

pub const Item = struct {
    id: []const u8,
    title: []const u8,
    requirements: []const []const u8,
    check: []const u8,
    params: Params,
    endurance: ?Endurance = null,
    unresolved_when: []const []const u8,
};

pub const Criteria = struct {
    schema_version: u32,
    criteria_id: []const u8,
    criteria_version: u32,
    run_class: []const u8,
    result_label: []const u8,
    decisions: []const []const u8,
    requirements: []const []const u8,
    protocol: struct { path: []const u8, revision: u32 },
    rationale: []const u8,
    declaration: struct {
        schema_version: u32,
        path_pattern: []const u8,
        length_unit: []const u8,
        mass_unit: []const u8,
        power_unit: []const u8,
        families: []const []const u8,
    },
    outcome_rule: []const u8,
    item_outcomes: []const []const u8,
    items: []const Item,
    result_labels_allowed: []const []const u8,

    pub fn item(self: Criteria, index: usize) Item {
        return self.items[index];
    }
};

pub const ValidationError = error{
    UnsupportedSchemaVersion,
    WrongCriteriaIdentity,
    ConventionMismatch,
    ItemSetMismatch,
    ParameterSetMismatch,
    ParameterOutOfRange,
    EvidenceStatusMismatch,
    EmptyText,
    EnduranceThresholdNotUnresolved,
};

pub const ParseError = strict_json.Error || ValidationError;

pub fn parse(gpa: std.mem.Allocator, text: []const u8) ParseError!strict_json.Parsed(Criteria) {
    const parsed = try strict_json.parse(Criteria, gpa, text, .{});
    errdefer parsed.deinit();
    try validate(parsed.value);
    return parsed;
}

const item_ids = [_][]const u8{ "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8" };

const item_checks = [_][]const u8{
    "enclosing_sphere_of_stowed_primitives_certified_upper_bound",
    "no_pairwise_component_box_interference_all_boxes_inside_one_cavity_primitive_assembly_access_present",
    "every_component_cites_source_and_no_estimate_basis",
    "mass_sum_exact_peak_power_not_above_rated_continuous_discharge_endurance_reported_only",
    "at_least_two_coupler_sites_and_three_unit_chain_all_supported_on_tabletop",
    "declaration_consistency_and_independent_justification_record",
    "q61_gate1_review_complete_independent_and_not_failing",
    "no_high_rating_against_f1_or_f2_references_and_both_family_exclusions_not_present",
};

/// The parameter names each item must carry, as field names of `Params`.
const item_params = [_][]const []const u8{
    &.{ "max_diameter_um", "uncertain_band_um", "round_rim_points", "sphere_seed_directions" },
    &.{ "interference_erosion_um", "min_clearance_um", "containment_tolerance_um", "intersection_algorithm", "gjk_iteration_cap", "assembly_access_statement_min_chars" },
    &.{ "allowed_source_kinds", "allowed_bases", "access_date_format" },
    &.{ "mass_sum_tolerance_mg", "derived_mass_tolerance_mg", "peak_power_rule", "exactly_one_energy_source" },
    &.{ "min_coupler_sites", "chain_units", "contact_tolerance_um", "support_rule", "interference_erosion_um", "tabletop_penetration_tolerance_um" },
    &.{ "requires_power_to_hold", "bounded_independent_release_declared", "magnetism_requires_declared_component", "justification_record_path_pattern" },
    &.{ "review_stage", "reviewer_must_differ_from_author", "review_path_pattern" },
    &.{ "forbidden_reference_classes", "exclusions" },
};

fn nonEmpty(s: []const u8) ValidationError!void {
    if (std.mem.trim(u8, s, " \t\r\n").len == 0) return error.EmptyText;
}

fn exactStrings(list: []const []const u8, expected: []const []const u8) ValidationError!void {
    if (list.len != expected.len) return error.ConventionMismatch;
    for (list, expected) |a, b| if (!std.mem.eql(u8, a, b)) return error.ConventionMismatch;
}

fn exactStr(a: []const u8, b: []const u8) ValidationError!void {
    if (!std.mem.eql(u8, a, b)) return error.ConventionMismatch;
}

fn isPresent(params: Params, comptime name: []const u8) bool {
    return @field(params, name) != null;
}

/// Counts the parameters that are present and checks that they are exactly
/// the expected set.
fn checkParamSet(params: Params, expected: []const []const u8) ValidationError!void {
    var present: usize = 0;
    const names = @typeInfo(Params).@"struct".field_names;
    inline for (names) |name| {
        if (@field(params, name) != null) present += 1;
    }
    if (present != expected.len) return error.ParameterSetMismatch;
    inline for (names) |name| {
        const wanted = for (expected) |e| {
            if (std.mem.eql(u8, e, name)) break true;
        } else false;
        if (wanted != isPresent(params, name)) return error.ParameterSetMismatch;
    }
}

fn finitePositive(p: Param(f64)) ValidationError!void {
    if (!(p.value > 0) or !std.math.isFinite(p.value)) return error.ParameterOutOfRange;
}

fn finiteNonNegative(p: Param(f64)) ValidationError!void {
    if (!(p.value >= 0) or !std.math.isFinite(p.value)) return error.ParameterOutOfRange;
}

fn mustBeEvidence(status: Status) ValidationError!void {
    if (status != .evidence) return error.EvidenceStatusMismatch;
}

pub fn validate(c: Criteria) ValidationError!void {
    if (c.schema_version != schema_version) return error.UnsupportedSchemaVersion;
    try exactStr(c.criteria_id, "gate1-paper");
    if (c.criteria_version != 1) return error.UnsupportedSchemaVersion;
    try exactStr(c.run_class, "paper_gate");
    try exactStr(c.result_label, "exploratory");
    try exactStrings(c.result_labels_allowed, &.{"exploratory"});
    try exactStr(c.protocol.path, "docs/validation/gate1-v1-protocol.md");
    if (c.protocol.revision != 1) return error.ConventionMismatch;
    if (c.declaration.schema_version != 1) return error.UnsupportedSchemaVersion;
    try exactStr(c.declaration.path_pattern, "candidates/<candidate_id>/declaration.json");
    try exactStr(c.declaration.length_unit, "micrometre_integer_positions_and_extents");
    try exactStr(c.declaration.mass_unit, "milligram_integer");
    try exactStr(c.declaration.power_unit, "milliwatt_integer");
    try exactStrings(c.declaration.families, &.{ "A", "B", "C" });
    try exactStr(c.outcome_rule, "fail_if_any_item_fail_else_unresolved_if_any_item_unresolved_else_pass");
    try exactStrings(c.item_outcomes, &.{ "pass", "fail", "unresolved" });
    try nonEmpty(c.rationale);
    if (c.decisions.len == 0 or c.requirements.len == 0) return error.EmptyText;

    if (c.items.len != item_ids.len) return error.ItemSetMismatch;
    for (c.items, item_ids, item_checks, item_params) |it, id, check, names| {
        if (!std.mem.eql(u8, it.id, id)) return error.ItemSetMismatch;
        try exactStr(it.check, check);
        try nonEmpty(it.title);
        if (it.requirements.len == 0 or it.unresolved_when.len == 0) return error.EmptyText;
        try checkParamSet(it.params, names);
        const is_g4 = std.mem.eql(u8, id, "G4");
        if (is_g4 != (it.endurance != null)) return error.ItemSetMismatch;
    }

    try validateG1(c.items[0].params);
    try validateG2(c.items[1].params);
    try validateG3(c.items[2].params);
    try validateG4(c.items[3]);
    try validateG5(c.items[4].params, c.items[1].params);
    try validateG6(c.items[5].params);
    try validateG7(c.items[6].params);
    try validateG8(c.items[7].params);
}

fn validateG1(p: Params) ValidationError!void {
    const max_d = p.max_diameter_um.?;
    try finitePositive(max_d);
    try mustBeEvidence(max_d.status);
    if (max_d.value != 60000) return error.ConventionMismatch; // Q12, exact
    const band = p.uncertain_band_um.?;
    try finitePositive(band);
    // The band must be a rounding margin only, far below any physical size.
    if (band.value > 1.0) return error.ParameterOutOfRange;
    if (p.round_rim_points.?.value != 64) return error.ConventionMismatch;
    if (p.sphere_seed_directions.?.value != 26) return error.ConventionMismatch;
}

fn validateG2(p: Params) ValidationError!void {
    const erosion = p.interference_erosion_um.?;
    try finitePositive(erosion);
    if (erosion.value > 100.0) return error.ParameterOutOfRange;
    try finiteNonNegative(p.min_clearance_um.?);
    if (p.min_clearance_um.?.value != 0) return error.ConventionMismatch; // pure geometric non-overlap
    const tol = p.containment_tolerance_um.?;
    try finiteNonNegative(tol);
    if (tol.value > 1.0) return error.ParameterOutOfRange;
    try exactStr(p.intersection_algorithm.?.value, "gjk_boolean");
    const cap = p.gjk_iteration_cap.?.value;
    if (cap < 8 or cap > 1024) return error.ParameterOutOfRange;
    if (p.assembly_access_statement_min_chars.?.value != 1) return error.ConventionMismatch;
}

fn validateG3(p: Params) ValidationError!void {
    try exactStrings(p.allowed_source_kinds.?.value, &.{ "datasheet", "publication" });
    try exactStrings(p.allowed_bases.?.value, &.{ "source", "derived" });
    try exactStr(p.access_date_format.?.value, "YYYY-MM-DD");
}

fn validateG4(it: Item) ValidationError!void {
    const p = it.params;
    if (p.mass_sum_tolerance_mg.?.value != 0) return error.ConventionMismatch;
    const dm = p.derived_mass_tolerance_mg.?;
    try finiteNonNegative(dm);
    if (dm.value > 1000.0) return error.ParameterOutOfRange;
    try exactStr(p.peak_power_rule.?.value, "sum_of_component_peak_power_not_above_nominal_voltage_times_rated_continuous_discharge_current");
    if (!p.exactly_one_energy_source.?.value) return error.ConventionMismatch;
    const e = it.endurance.?;
    if (!e.reported) return error.ConventionMismatch;
    // Q31 has no task duration, so the threshold stays unresolved and never gates.
    if (e.threshold.status != .unresolved) return error.EnduranceThresholdNotUnresolved;
}

fn validateG5(p: Params, g2: Params) ValidationError!void {
    if (p.min_coupler_sites.?.value != 2) return error.ConventionMismatch;
    if (p.chain_units.?.value != 3) return error.ConventionMismatch;
    const ct = p.contact_tolerance_um.?;
    try finitePositive(ct);
    if (ct.value > 100.0) return error.ParameterOutOfRange;
    try exactStr(p.support_rule.?.value, "centre_of_mass_projection_inside_convex_hull_of_contact_points_with_nonzero_area");
    try finitePositive(p.interference_erosion_um.?);
    // G5 uses the same eroded-shape test as G2, so the two values agree.
    if (p.interference_erosion_um.?.value != g2.interference_erosion_um.?.value) return error.ConventionMismatch;
    try finitePositive(p.tabletop_penetration_tolerance_um.?);
    if (p.tabletop_penetration_tolerance_um.?.value != ct.value) return error.ConventionMismatch;
}

fn validateG6(p: Params) ValidationError!void {
    if (p.requires_power_to_hold.?.value) return error.ConventionMismatch;
    if (!p.bounded_independent_release_declared.?.value) return error.ConventionMismatch;
    if (!p.magnetism_requires_declared_component.?.value) return error.ConventionMismatch;
    try exactStr(p.justification_record_path_pattern.?.value, "candidates/<candidate_id>/retention-review-v<candidate_version>-r<n>.md");
}

fn validateG7(p: Params) ValidationError!void {
    try exactStr(p.review_stage.?.value, "gate1");
    if (!p.reviewer_must_differ_from_author.?.value) return error.ConventionMismatch;
    try exactStr(p.review_path_pattern.?.value, "candidates/<candidate_id>/originality-review-gate1-v<candidate_version>-r<n>.md");
}

fn validateG8(p: Params) ValidationError!void {
    try exactStrings(p.forbidden_reference_classes.?.value, &.{ "F1", "F2" });
    try exactStrings(p.exclusions.?.value, &.{ "cube_with_internal_flywheel", "needle_or_particle_like_silhouette" });
}

/// The preregistered criteria file, embedded so its consistency is checked
/// on every build. Its identity is the SHA-256 of these exact bytes.
pub const gate1_v1_json = @embedFile("criteria_gate1_v1");

/// SHA-256 recorded in criteria/REGISTER.md. Registered files are never
/// edited in place; a revision is a new file and a new register entry.
pub const gate1_v1_sha256 = "ffe135329340ca7d3f630a1f14c0dd91616d8ab91e64f0985585eeabb532ddbf";

// --- Tests

const testing = std.testing;

test "the embedded gate1 criteria file is byte-identical to its registered version" {
    const identity = @import("identity.zig");
    try testing.expectEqualStrings(gate1_v1_sha256, &identity.toHex(identity.fileIdentity(gate1_v1_json)));
}

test "the registered gate1 criteria file parses and carries the expected values" {
    const p = try parse(testing.allocator, gate1_v1_json);
    defer p.deinit();
    const c = p.value;
    try testing.expectEqual(@as(usize, 8), c.items.len);
    try testing.expectEqual(@as(f64, 60000), c.items[0].params.max_diameter_um.?.value);
    try testing.expectEqual(Status.evidence, c.items[0].params.max_diameter_um.?.status);
    try testing.expectEqual(@as(f64, 0.001), c.items[0].params.uncertain_band_um.?.value);
    try testing.expectEqual(@as(u32, 64), c.items[1].params.gjk_iteration_cap.?.value);
    try testing.expectEqual(@as(u32, 3), c.items[4].params.chain_units.?.value);
    try testing.expect(c.items[3].endurance.?.reported);
}

fn expectInvalid(expected: anyerror, needle: []const u8, replacement: []const u8) !void {
    const gpa = testing.allocator;
    const at = std.mem.indexOf(u8, gate1_v1_json, needle) orelse return error.TestNeedleNotFound;
    const text = try std.mem.concat(gpa, u8, &.{ gate1_v1_json[0..at], replacement, gate1_v1_json[at + needle.len ..] });
    defer gpa.free(text);
    if (parse(gpa, text)) |p| {
        p.deinit();
        return error.TestUnexpectedSuccess;
    } else |err| try testing.expectEqual(expected, err);
}

test "strict parsing rejects structural mutations" {
    try expectInvalid(error.UnknownField, "\"schema_version\": 1,\n  \"criteria_id\"", "\"extra\": 1, \"schema_version\": 1,\n  \"criteria_id\"");
    try expectInvalid(error.DuplicateField, "\"criteria_version\": 1,", "\"criteria_version\": 1, \"criteria_version\": 1,");
    try expectInvalid(error.MissingField, "\"run_class\": \"paper_gate\",", "");
    try expectInvalid(error.IntegerNotExact, "\"criteria_version\": 1,", "\"criteria_version\": 1.0,");
    try expectInvalid(error.InvalidEnumTag, "\"status\": \"evidence\", \"basis\": \"Q12", "\"status\": \"proven\", \"basis\": \"Q12");
    try expectInvalid(error.TypeMismatch, "\"value\": 60000,", "\"value\": \"60000\",");
    try expectInvalid(error.SyntaxError, "\"result_labels_allowed\": [\"exploratory\"]\n}", "\"result_labels_allowed\": [\"exploratory\"]\n} {}");
}

test "convention, range and status violations are rejected" {
    try expectInvalid(error.ConventionMismatch, "\"value\": 60000,", "\"value\": 61000,");
    try expectInvalid(error.ConventionMismatch, "\"value\": 64, \"status\": \"provisional\", \"basis\": \"Welzl", "\"value\": 32, \"status\": \"provisional\", \"basis\": \"Welzl");
    try expectInvalid(error.ConventionMismatch, "\"value\": \"gjk_boolean\"", "\"value\": \"sat\"");
    try expectInvalid(error.ConventionMismatch, "\"chain_units\": { \"value\": 3", "\"chain_units\": { \"value\": 5");
    try expectInvalid(error.ConventionMismatch, "\"result_label\": \"exploratory\"", "\"result_label\": \"validated_acceptance\"");
    try expectInvalid(error.ParameterOutOfRange, "\"uncertain_band_um\": { \"value\": 0.001", "\"uncertain_band_um\": { \"value\": 5.0");
    try expectInvalid(error.EvidenceStatusMismatch, "\"max_diameter_um\": { \"value\": 60000, \"status\": \"evidence\"", "\"max_diameter_um\": { \"value\": 60000, \"status\": \"provisional\"");
    try expectInvalid(error.InvalidEnumTag, "\"threshold\": { \"status\": \"unresolved\"", "\"threshold\": { \"status\": \"evidence\"");
}

test "an item missing a parameter, or carrying a foreign one, is rejected" {
    try expectInvalid(error.ParameterSetMismatch, "\"round_rim_points\"", "\"min_coupler_sites\"");
    try expectInvalid(error.UnknownField, "\"min_coupler_sites\"", "\"min_coupler_sitez\"");
    try expectInvalid(error.ItemSetMismatch, "\"id\": \"G2\"", "\"id\": \"G9\"");
}
