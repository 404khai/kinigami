//! Run configuration, run classes, and result records (Q32, Q39, Q40, Q44,
//! Q46). Schema version 1.
//!
//! Scaffolding only: fields whose content depends on open decisions are
//! deliberately absent rather than guessed:
//! - random-number seeds (RNG algorithm and stream semantics open);
//! - physical parameters of fixtures (reference conditions open);
//! - the acceptance build profile contents (optimization level open).
//! Adding them is a schema version bump.

const std = @import("std");
const strict_json = @import("strict_json.zig");
const time = @import("time.zig");

pub const schema_version: u32 = 1;

/// What kind of run this is. Determines which inputs are permitted and the
/// strongest label a result may carry.
pub const RunClass = enum {
    /// Analytic validation of neutral fixtures (Q46). Never benchmark or
    /// Kin-candidate evidence. The only class that may carry validation forces.
    fixture_validation,
    /// Preregistered benchmark run (Q31, Q38).
    benchmark,
    /// Controller development without acceptance status (Q32).
    controller_development,
    /// Diagnostic run with privileged ground-truth access; never a pass (Q32).
    oracle_diagnostic,
    /// Anything else; the default status of results (Q40).
    exploratory,
};

/// Result labels (PRC-005). Exactly one per result.
pub const ResultLabel = enum { exploratory, oracle, fixture, uncertain, validated_acceptance };

pub const BodyKind = enum { fixture, kin_candidate };

pub const Body = struct {
    id: []const u8,
    kind: BodyKind,
};

pub const Frame = enum { world, body };

/// Validation-only external load on a fixture (Q46, PRC-013). Every field is
/// an explicit recorded input. When within a tick interval the load acts on
/// the physics (boundary semantics) follows the still-open event-phase
/// ordering decision.
pub const ValidationForce = struct {
    body: []const u8,
    frame: Frame,
    force_n: [3]f64,
    torque_nm: [3]f64,
    application_point_m: [3]f64,
    start_tick: u64,
    end_tick: u64,
};

pub const CriteriaRef = struct {
    path: []const u8,
    sha256: []const u8,
};

pub const RunConfig = struct {
    schema_version: u32,
    run_id: []const u8,
    run_class: RunClass,
    time_unit: struct { numerator_s: u64, denominator_s: u64 },
    physics_step_ticks: u64,
    duration_ticks: u64,
    bodies: []const Body,
    validation_forces: []const ValidationForce = &.{},
    criteria: ?CriteriaRef,
};

pub const ConfigError = error{
    UnsupportedSchemaVersion,
    EmptyRunId,
    DuplicateBodyId,
    UnknownForceTarget,
    ValidationForceNotPermitted,
    ForceOnNonFixture,
    CandidateInFixtureValidation,
    EmptyForceInterval,
    ForceOutsideRun,
    InvalidCriteriaHash,
} || time.Error;

/// Parses and validates a run configuration. Every rule fails closed.
pub fn parseConfig(gpa: std.mem.Allocator, text: []const u8) (strict_json.Error || ConfigError)!strict_json.Parsed(RunConfig) {
    const parsed = try strict_json.parse(RunConfig, gpa, text, .{});
    errdefer parsed.deinit();
    try validate(parsed.value);
    return parsed;
}

pub fn validate(c: RunConfig) ConfigError!void {
    if (c.schema_version != schema_version) return error.UnsupportedSchemaVersion;
    if (c.run_id.len == 0) return error.EmptyRunId;
    try (time.TimeUnit{ .numerator = c.time_unit.numerator_s, .denominator = c.time_unit.denominator_s }).validate();
    _ = try time.PhysicsStep.init(.{ .ticks = c.physics_step_ticks });

    for (c.bodies, 0..) |b, i| {
        for (c.bodies[0..i]) |prev| if (std.mem.eql(u8, prev.id, b.id)) return error.DuplicateBodyId;
        if (c.run_class == .fixture_validation and b.kind != .fixture) return error.CandidateInFixtureValidation;
    }

    for (c.validation_forces) |f| {
        if (c.run_class != .fixture_validation) return error.ValidationForceNotPermitted;
        const target = for (c.bodies) |b| {
            if (std.mem.eql(u8, b.id, f.body)) break b;
        } else return error.UnknownForceTarget;
        if (target.kind != .fixture) return error.ForceOnNonFixture;
        if (f.end_tick <= f.start_tick) return error.EmptyForceInterval;
        if (f.end_tick > c.duration_ticks) return error.ForceOutsideRun;
    }

    if (c.criteria) |cr| {
        if (cr.sha256.len != 64) return error.InvalidCriteriaHash;
        for (cr.sha256) |ch| if (!std.ascii.isDigit(ch) and !(ch >= 'a' and ch <= 'f')) return error.InvalidCriteriaHash;
    }
}

/// Inputs that determine a result's label.
pub const LabelInputs = struct {
    run_class: RunClass,
    /// All preregistered criteria evaluated and passed.
    criteria_passed: bool,
    /// Numerical or model uncertainty could change the outcome (PHY-008).
    uncertain: bool,
    /// Every model used is validated for these conditions (Q37).
    models_validated: bool,
    /// Built with the frozen acceptance build profile (BLD-004, BLD-006).
    acceptance_profile: bool,
};

/// The acceptance build profile is not frozen yet (BLD-005), so no result can
/// currently be labeled `validated_acceptance`. Flip only by decision.
pub const acceptance_profile_frozen = false;

/// Assigns exactly one label (PRC-005). Labels never upgrade beyond what the
/// run class allows: oracle and fixture runs keep those labels regardless of
/// outcome.
pub fn label(in: LabelInputs) ResultLabel {
    switch (in.run_class) {
        .oracle_diagnostic => return .oracle,
        .fixture_validation => return .fixture,
        .controller_development, .exploratory => return if (in.uncertain) .uncertain else .exploratory,
        .benchmark => {
            if (in.uncertain) return .uncertain;
            if (acceptance_profile_frozen and in.acceptance_profile and in.models_validated and in.criteria_passed)
                return .validated_acceptance;
            return .exploratory;
        },
    }
}

pub const CaseStatus = enum { pass, fail, uncertain, not_evaluated };

pub const CaseOutcome = struct {
    case_id: []const u8,
    status: CaseStatus,
};

/// Result record written as JSON (DAT-011). Field order is the serialized
/// order. Provenance fields whose producers are not built yet are `null`
/// and must be filled before any result is claimed beyond `exploratory`.
pub const Result = struct {
    schema_version: u32 = schema_version,
    run_id: []const u8,
    run_class: RunClass,
    label: ResultLabel,
    config_sha256: []const u8,
    criteria: ?CriteriaRef,
    recording_sha256: ?[]const u8,
    code_revision: ?[]const u8,
    build_profile: ?[]const u8,
    candidate_version: ?[]const u8,
    outcomes: []const CaseOutcome,
};

pub fn writeResult(gpa: std.mem.Allocator, r: Result) error{OutOfMemory}![]u8 {
    return std.json.Stringify.valueAlloc(gpa, r, .{ .whitespace = .indent_2 });
}

const testing = std.testing;

const base_config =
    \\{"schema_version":1,"run_id":"r1","run_class":"fixture_validation",
    \\ "time_unit":{"numerator_s":1,"denominator_s":1000000},
    \\ "physics_step_ticks":1000,"duration_ticks":100000,
    \\ "bodies":[{"id":"block","kind":"fixture"}],
    \\ "validation_forces":[{"body":"block","frame":"world","force_n":[1,0,0],
    \\   "torque_nm":[0,0,0],"application_point_m":[0,0,0.01],"start_tick":0,"end_tick":5000}],
    \\ "criteria":null}
;

fn expectConfigError(expected: anyerror, text: []const u8) !void {
    if (parseConfig(testing.allocator, text)) |p| {
        p.deinit();
        return error.TestUnexpectedSuccess;
    } else |err| try testing.expectEqual(expected, err);
}

fn replaced(comptime needle: []const u8, comptime replacement: []const u8) []const u8 {
    const at = comptime std.mem.indexOf(u8, base_config, needle) orelse @compileError("needle not found");
    return base_config[0..at] ++ replacement ++ base_config[at + needle.len ..];
}

test "valid fixture_validation config with a validation force" {
    const p = try parseConfig(testing.allocator, base_config);
    defer p.deinit();
    try testing.expectEqual(RunClass.fixture_validation, p.value.run_class);
    try testing.expectEqual(@as(usize, 1), p.value.validation_forces.len);
}

test "validation forces are rejected outside fixture_validation (Q46)" {
    inline for (.{ "benchmark", "controller_development", "oracle_diagnostic", "exploratory" }) |cls| {
        try expectConfigError(error.ValidationForceNotPermitted, replaced("\"fixture_validation\"", "\"" ++ cls ++ "\""));
    }
}

test "fixture_validation admits only fixtures, and forces only on fixtures" {
    try expectConfigError(error.CandidateInFixtureValidation, replaced("\"kind\":\"fixture\"", "\"kind\":\"kin_candidate\""));
    try expectConfigError(error.UnknownForceTarget, replaced("\"body\":\"block\"", "\"body\":\"other\""));
}

test "config rules fail closed" {
    try expectConfigError(error.UnsupportedSchemaVersion, replaced("\"schema_version\":1", "\"schema_version\":2"));
    try expectConfigError(error.EmptyRunId, replaced("\"run_id\":\"r1\"", "\"run_id\":\"\""));
    try expectConfigError(error.InvalidTimeUnit, replaced("\"numerator_s\":1,", "\"numerator_s\":0,"));
    try expectConfigError(error.InvalidPhysicsStep, replaced("\"physics_step_ticks\":1000", "\"physics_step_ticks\":0"));
    try expectConfigError(error.EmptyForceInterval, replaced("\"end_tick\":5000", "\"end_tick\":0"));
    try expectConfigError(error.ForceOutsideRun, replaced("\"end_tick\":5000", "\"end_tick\":100001"));
    try expectConfigError(error.DuplicateBodyId, replaced("[{\"id\":\"block\",\"kind\":\"fixture\"}]", "[{\"id\":\"block\",\"kind\":\"fixture\"},{\"id\":\"block\",\"kind\":\"fixture\"}]"));
    try expectConfigError(error.MissingField, replaced(",\n \"criteria\":null", ""));
    try expectConfigError(error.InvalidCriteriaHash, replaced("\"criteria\":null", "\"criteria\":{\"path\":\"c.json\",\"sha256\":\"ABC\"}"));
}

test "labels: oracle and fixture runs never upgrade; acceptance is unreachable until the profile is frozen" {
    const all_good: LabelInputs = .{ .run_class = .benchmark, .criteria_passed = true, .uncertain = false, .models_validated = true, .acceptance_profile = true };
    try testing.expectEqual(ResultLabel.exploratory, label(all_good));
    var in = all_good;
    in.uncertain = true;
    try testing.expectEqual(ResultLabel.uncertain, label(in));
    in.run_class = .oracle_diagnostic;
    try testing.expectEqual(ResultLabel.oracle, label(in));
    in.run_class = .fixture_validation;
    try testing.expectEqual(ResultLabel.fixture, label(in));
}

test "results round-trip through the strict parser with exact floats" {
    const gpa = testing.allocator;
    const r: Result = .{
        .run_id = "r1",
        .run_class = .fixture_validation,
        .label = .fixture,
        .config_sha256 = "0000000000000000000000000000000000000000000000000000000000000000",
        .criteria = null,
        .recording_sha256 = null,
        .code_revision = null,
        .build_profile = null,
        .candidate_version = null,
        .outcomes = &.{.{ .case_id = "rest", .status = .not_evaluated }},
    };
    const text = try writeResult(gpa, r);
    defer gpa.free(text);
    const back = try strict_json.parse(Result, gpa, text, .{});
    defer back.deinit();
    try testing.expectEqualStrings("rest", back.value.outcomes[0].case_id);
    try testing.expectEqual(ResultLabel.fixture, back.value.label);

    // Float formatting used by std.json must round-trip bit-exactly.
    const Holder = struct { x: f64 };
    for ([_]f64{ 0.1, 1.0 / 3.0, 5e-324, 1.7976931348623157e308, -0.0, 123456789.125 }) |x| {
        const t = try std.json.Stringify.valueAlloc(gpa, Holder{ .x = x }, .{});
        defer gpa.free(t);
        const p = try strict_json.parse(Holder, gpa, t, .{});
        defer p.deinit();
        try testing.expectEqual(@as(u64, @bitCast(x)), @as(u64, @bitCast(p.value.x)));
    }
}
