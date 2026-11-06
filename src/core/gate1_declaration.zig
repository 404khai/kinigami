//! Gate 1 candidate declaration, schema version 1 (Q62, protocol
//! `docs/validation/gate1-v1-protocol.md` section 2).
//!
//! Parsed through `strict_json` and validated fail-closed (DAT-005): unknown
//! fields, missing required fields, duplicate keys, type mismatches and
//! out-of-range values are rejected, and a rejected declaration gets no
//! outcome. Fields whose presence depends on another field (the primitive
//! kind fields, `derivation`, the energy-source-only component fields) are
//! typed as optionals, and their presence is checked against the raw JSON so
//! that an absent key and an explicit `null` are told apart.
//!
//! Content that the protocol assigns an `unresolved` or `fail` outcome to
//! (a missing or malformed `source`, an empty statement, an empty roll list,
//! no coupler sites) is accepted here as structure and judged by the
//! evaluator. This file contains no evaluator code.

const std = @import("std");
const strict_json = @import("strict_json.zig");

pub const schema_version: u32 = 1;

pub const Pose = struct {
    position_um: [3]i64,
    orientation: [4]f64,
};

pub const PrimitiveKind = enum { sphere, box, cylinder };
pub const PrimitiveRole = enum { body, coupler, cavity };

pub const Primitive = struct {
    id: []const u8,
    kind: PrimitiveKind,
    radius_um: ?u64 = null,
    half_extent_um: ?[3]u64 = null,
    half_height_um: ?u64 = null,
    pose: Pose,
    role: PrimitiveRole,
};

pub const Geometry = struct { primitives: []const Primitive };

pub const ComponentKind = enum {
    controller,
    energy_source,
    actuator,
    sensor,
    communication,
    coupler_mechanism,
    magnet,
    structure,
    other,
};

pub const Basis = enum { source, derived, estimate };

pub const Derivation = struct { density_kg_m3: f64, volume_m3: f64 };

pub const ComponentBox = struct { half_extent_um: [3]u64, pose: Pose };

/// Strings stay strings: an unknown kind, a malformed URL or a bad date makes
/// the component uncited (G3, unresolved) rather than rejecting the file.
pub const Source = struct {
    kind: []const u8,
    url: []const u8,
    accessed: []const u8,
    title: []const u8,
};

pub const Component = struct {
    id: []const u8,
    kind: ComponentKind,
    description: []const u8,
    mass_mg: u64,
    mass_basis: Basis,
    derivation: ?Derivation = null,
    box: ComponentBox,
    dimension_basis: Basis,
    peak_power_mw: u64,
    average_power_mw: u64,
    power_basis: Basis,
    source: ?Source = null,
    nominal_voltage_v: ?f64 = null,
    rated_continuous_discharge_a: ?f64 = null,
    energy_mj: ?u64 = null,
};

pub const Site = struct {
    id: []const u8,
    position_um: [3]i64,
    normal: [3]f64,
    mount: []const u8,
};

pub const Chain = struct {
    head_site: []const u8,
    tail_site: []const u8,
    rest_orientation: [4]f64,
    mating_roll_deg: []const f64,
};

pub const MechanismKind = enum { geometric_interlock, spring_preload, friction_wedge, permanent_magnet, other };

pub const Retention = struct {
    requires_power_to_hold: bool,
    mechanism_kind: MechanismKind,
    mechanism: []const u8,
    component_ids: []const []const u8,
    release: struct { bounded_independent_release: bool, means: []const u8 },
};

pub const AlignmentKind = enum { geometric_guide, magnetic, other };

pub const Alignment = struct {
    kind: AlignmentKind,
    description: []const u8,
    justification: []const u8,
    component_ids: []const []const u8,
};

pub const Family = enum { A, B, C };

pub const Declaration = struct {
    schema_version: u32,
    candidate_id: []const u8,
    candidate_version: u32,
    family: Family,
    declared_on: []const u8,
    author: []const u8,
    summary: []const u8,
    stowed_geometry: Geometry,
    chain_geometry: Geometry,
    components: []const Component,
    mass_budget: struct { total_mass_mg: u64 },
    assembly_access: struct { statement: []const u8 },
    coupler_sites: []const Site,
    chain: Chain,
    retention: Retention,
    alignment: []const Alignment,
    limitations: []const []const u8 = &.{},
};

pub const ValidationError = error{
    UnsupportedSchemaVersion,
    InvalidCandidateId,
    CandidateIdMismatch,
    InvalidCandidateVersion,
    InvalidDate,
    EmptyAuthor,
    DuplicateId,
    PrimitiveFieldsMismatch,
    ExtentNotPositive,
    NotUnitQuaternion,
    CavityInChainGeometry,
    FieldPresenceMismatch,
    InvalidDerivation,
    EnergySourceCount,
    InvalidEnergySourceField,
    NotUnitVector,
    UnknownSiteId,
    UnknownComponentId,
    NotAnObject,
};

pub const ParseError = strict_json.Error || ValidationError;

/// Parses and validates `text`. `expected_id` is the candidate's directory
/// name when known; the declaration's `candidate_id` must equal it.
pub fn parse(gpa: std.mem.Allocator, text: []const u8, expected_id: ?[]const u8) ParseError!strict_json.Parsed(Declaration) {
    const parsed = try strict_json.parse(Declaration, gpa, text, .{});
    errdefer parsed.deinit();
    try validate(parsed.value, expected_id);
    try checkPresence(gpa, parsed.value, text);
    return parsed;
}

pub fn validate(d: Declaration, expected_id: ?[]const u8) ValidationError!void {
    if (d.schema_version != schema_version) return error.UnsupportedSchemaVersion;
    if (d.candidate_id.len == 0) return error.InvalidCandidateId;
    for (d.candidate_id) |ch| {
        const ok = (ch >= 'a' and ch <= 'z') or (ch >= '0' and ch <= '9') or ch == '-';
        if (!ok) return error.InvalidCandidateId;
    }
    if (expected_id) |e| if (!std.mem.eql(u8, e, d.candidate_id)) return error.CandidateIdMismatch;
    if (d.candidate_version < 1) return error.InvalidCandidateVersion;
    if (!isValidDate(d.declared_on)) return error.InvalidDate;
    if (std.mem.trim(u8, d.author, " \t\r\n").len == 0) return error.EmptyAuthor;

    try validatePrimitives(d.stowed_geometry.primitives, true);
    try validatePrimitives(d.chain_geometry.primitives, false);

    // Component ids unique; exactly one energy source; geometry and poses valid.
    var sources: usize = 0;
    for (d.components, 0..) |c, i| {
        for (d.components[0..i]) |o| if (std.mem.eql(u8, o.id, c.id)) return error.DuplicateId;
        try checkExtents(&c.box.half_extent_um);
        try checkPose(c.box.pose);
        if (c.mass_basis == .derived) {
            const dv = c.derivation orelse return error.InvalidDerivation;
            if (!(dv.density_kg_m3 > 0) or !(dv.volume_m3 > 0)) return error.InvalidDerivation;
        }
        if (c.kind == .energy_source) {
            sources += 1;
            const v = c.nominal_voltage_v orelse return error.InvalidEnergySourceField;
            if (!(v > 0)) return error.InvalidEnergySourceField;
            if (c.rated_continuous_discharge_a) |a| if (!(a > 0)) return error.InvalidEnergySourceField;
            const e = c.energy_mj orelse return error.InvalidEnergySourceField;
            if (e == 0) return error.InvalidEnergySourceField;
        }
    }
    if (sources != 1) return error.EnergySourceCount;

    for (d.coupler_sites, 0..) |s, i| {
        for (d.coupler_sites[0..i]) |o| if (std.mem.eql(u8, o.id, s.id)) return error.DuplicateId;
        const n = @sqrt(s.normal[0] * s.normal[0] + s.normal[1] * s.normal[1] + s.normal[2] * s.normal[2]);
        if (!(@abs(n - 1.0) <= 1e-9)) return error.NotUnitVector;
    }
    _ = findSite(d.coupler_sites, d.chain.head_site) orelse return error.UnknownSiteId;
    _ = findSite(d.coupler_sites, d.chain.tail_site) orelse return error.UnknownSiteId;
    try checkQuat(d.chain.rest_orientation);

    for (d.retention.component_ids) |id| if (!hasComponent(d.components, id)) return error.UnknownComponentId;
    for (d.alignment) |a| for (a.component_ids) |id| if (!hasComponent(d.components, id)) return error.UnknownComponentId;
}

pub fn findSite(sites: []const Site, id: []const u8) ?usize {
    for (sites, 0..) |s, i| if (std.mem.eql(u8, s.id, id)) return i;
    return null;
}

pub fn hasComponent(components: []const Component, id: []const u8) bool {
    for (components) |c| if (std.mem.eql(u8, c.id, id)) return true;
    return false;
}

pub fn componentById(components: []const Component, id: []const u8) ?Component {
    for (components) |c| if (std.mem.eql(u8, c.id, id)) return c;
    return null;
}

fn validatePrimitives(prims: []const Primitive, allow_cavity: bool) ValidationError!void {
    for (prims, 0..) |p, i| {
        for (prims[0..i]) |o| if (std.mem.eql(u8, o.id, p.id)) return error.DuplicateId;
        if (!allow_cavity and p.role == .cavity) return error.CavityInChainGeometry;
        switch (p.kind) {
            .sphere => {
                if (p.half_extent_um != null or p.half_height_um != null) return error.PrimitiveFieldsMismatch;
                const r = p.radius_um orelse return error.PrimitiveFieldsMismatch;
                if (r == 0) return error.ExtentNotPositive;
            },
            .box => {
                if (p.radius_um != null or p.half_height_um != null) return error.PrimitiveFieldsMismatch;
                const h = p.half_extent_um orelse return error.PrimitiveFieldsMismatch;
                try checkExtents(&h);
            },
            .cylinder => {
                if (p.half_extent_um != null) return error.PrimitiveFieldsMismatch;
                const r = p.radius_um orelse return error.PrimitiveFieldsMismatch;
                const hh = p.half_height_um orelse return error.PrimitiveFieldsMismatch;
                if (r == 0 or hh == 0) return error.ExtentNotPositive;
            },
        }
        try checkPose(p.pose);
    }
}

fn checkExtents(h: []const u64) ValidationError!void {
    for (h) |v| if (v == 0) return error.ExtentNotPositive;
}

fn checkPose(p: Pose) ValidationError!void {
    try checkQuat(p.orientation);
}

fn checkQuat(q: [4]f64) ValidationError!void {
    const n = @sqrt(q[0] * q[0] + q[1] * q[1] + q[2] * q[2] + q[3] * q[3]);
    if (!(@abs(n - 1.0) <= 1e-9)) return error.NotUnitQuaternion;
}

/// Calendar validity of `YYYY-MM-DD` (four-digit year, leap years honoured).
pub fn isValidDate(s: []const u8) bool {
    if (s.len != 10 or s[4] != '-' or s[7] != '-') return false;
    for (s, 0..) |ch, i| {
        if (i == 4 or i == 7) continue;
        if (ch < '0' or ch > '9') return false;
    }
    const y = std.fmt.parseInt(u32, s[0..4], 10) catch return false;
    const m = std.fmt.parseInt(u32, s[5..7], 10) catch return false;
    const day = std.fmt.parseInt(u32, s[8..10], 10) catch return false;
    if (m < 1 or m > 12 or day < 1) return false;
    const leap = (y % 4 == 0 and y % 100 != 0) or y % 400 == 0;
    const days = [_]u32{ 31, if (leap) 29 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
    return day <= days[m - 1];
}

// --- Raw-JSON presence checks (absent key versus explicit null).

fn objectOf(v: std.json.Value) ValidationError!std.json.ObjectMap {
    return switch (v) {
        .object => |o| o,
        else => error.NotAnObject,
    };
}

fn arrayItems(v: ?std.json.Value) ValidationError![]const std.json.Value {
    const val = v orelse return error.NotAnObject;
    return switch (val) {
        .array => |a| a.items,
        else => error.NotAnObject,
    };
}

fn checkPresence(gpa: std.mem.Allocator, d: Declaration, text: []const u8) (ValidationError || std.mem.Allocator.Error)!void {
    var arena_state = std.heap.ArenaAllocator.init(gpa);
    defer arena_state.deinit();
    const arena = arena_state.allocator();
    // The strict parse already rejected duplicate keys and malformed input,
    // so a failure here can only be an allocation failure.
    const root = std.json.parseFromSliceLeaky(std.json.Value, arena, text, .{}) catch |err| switch (err) {
        error.OutOfMemory => return error.OutOfMemory,
        else => return error.NotAnObject,
    };
    const root_obj = try objectOf(root);

    for ([_][]const u8{ "stowed_geometry", "chain_geometry" }) |name| {
        const geo = try objectOf(root_obj.get(name) orelse return error.NotAnObject);
        const items = try arrayItems(geo.get("primitives"));
        for (items) |item| {
            const o = try objectOf(item);
            const kind = switch ((o.get("kind") orelse return error.NotAnObject)) {
                .string => |s| s,
                else => return error.NotAnObject,
            };
            const has_radius = o.contains("radius_um");
            const has_half = o.contains("half_extent_um");
            const has_hh = o.contains("half_height_um");
            const ok = if (std.mem.eql(u8, kind, "sphere"))
                has_radius and !has_half and !has_hh
            else if (std.mem.eql(u8, kind, "box"))
                has_half and !has_radius and !has_hh
            else
                has_radius and has_hh and !has_half;
            if (!ok) return error.PrimitiveFieldsMismatch;
        }
    }

    const comps = try arrayItems(root_obj.get("components"));
    if (comps.len != d.components.len) return error.FieldPresenceMismatch;
    for (comps, d.components) |item, c| {
        const o = try objectOf(item);
        if (o.contains("derivation") != (c.mass_basis == .derived)) return error.FieldPresenceMismatch;
        const is_src = c.kind == .energy_source;
        for ([_][]const u8{ "nominal_voltage_v", "rated_continuous_discharge_a", "energy_mj" }) |k| {
            if (o.contains(k) != is_src) return error.FieldPresenceMismatch;
        }
    }
}

// --- Tests

const testing = std.testing;

/// A minimal complete declaration used by the tests here and in
/// `gate1_eval.zig`. One energy source, one body box, one cavity.
pub const sample_json =
    \\{
    \\  "schema_version": 1,
    \\  "candidate_id": "sample-a",
    \\  "candidate_version": 1,
    \\  "family": "A",
    \\  "declared_on": "2026-11-05",
    \\  "author": "author-agent",
    \\  "summary": "test sample",
    \\  "stowed_geometry": { "primitives": [
    \\    { "id": "shell", "kind": "box", "half_extent_um": [15000, 15000, 15000], "pose": { "position_um": [0, 0, 0], "orientation": [1, 0, 0, 0] }, "role": "body" },
    \\    { "id": "cavity", "kind": "box", "half_extent_um": [14000, 14000, 14000], "pose": { "position_um": [0, 0, 0], "orientation": [1, 0, 0, 0] }, "role": "cavity" }
    \\  ] },
    \\  "chain_geometry": { "primitives": [
    \\    { "id": "shell", "kind": "box", "half_extent_um": [15000, 15000, 15000], "pose": { "position_um": [0, 0, 0], "orientation": [1, 0, 0, 0] }, "role": "body" }
    \\  ] },
    \\  "components": [
    \\    { "id": "cell", "kind": "energy_source", "description": "cell", "mass_mg": 1000, "mass_basis": "source",
    \\      "box": { "half_extent_um": [5000, 5000, 5000], "pose": { "position_um": [-8000, 0, 0], "orientation": [1, 0, 0, 0] } },
    \\      "dimension_basis": "source", "peak_power_mw": 0, "average_power_mw": 0, "power_basis": "source",
    \\      "source": { "kind": "datasheet", "url": "https://example.org/cell.pdf", "accessed": "2026-11-04", "title": "Cell" },
    \\      "nominal_voltage_v": 3.7, "rated_continuous_discharge_a": 1.0, "energy_mj": 5000 },
    \\    { "id": "mcu", "kind": "controller", "description": "mcu", "mass_mg": 500, "mass_basis": "source",
    \\      "box": { "half_extent_um": [3000, 3000, 3000], "pose": { "position_um": [8000, 0, 0], "orientation": [1, 0, 0, 0] } },
    \\      "dimension_basis": "source", "peak_power_mw": 100, "average_power_mw": 10, "power_basis": "source",
    \\      "source": { "kind": "datasheet", "url": "https://example.org/mcu.pdf", "accessed": "2026-11-04", "title": "MCU" } }
    \\  ],
    \\  "mass_budget": { "total_mass_mg": 1500 },
    \\  "assembly_access": { "statement": "two-part shell, screws on the seam" },
    \\  "coupler_sites": [
    \\    { "id": "s-plus", "position_um": [15000, 0, 0], "normal": [1, 0, 0], "mount": "face +x" },
    \\    { "id": "s-minus", "position_um": [-15000, 0, 0], "normal": [-1, 0, 0], "mount": "face -x" }
    \\  ],
    \\  "chain": { "head_site": "s-plus", "tail_site": "s-minus", "rest_orientation": [1, 0, 0, 0], "mating_roll_deg": [0] },
    \\  "retention": { "requires_power_to_hold": false, "mechanism_kind": "geometric_interlock", "mechanism": "interlock",
    \\    "component_ids": ["mcu"], "release": { "bounded_independent_release": true, "means": "pull-off" } },
    \\  "alignment": [ { "kind": "geometric_guide", "description": "guide", "justification": "chamfer", "component_ids": ["mcu"] } ],
    \\  "limitations": []
    \\}
;

test "the sample declaration parses" {
    const p = try parse(testing.allocator, sample_json, "sample-a");
    defer p.deinit();
    try testing.expectEqual(@as(usize, 2), p.value.components.len);
    try testing.expectEqual(Family.A, p.value.family);
}

fn expectRejected(expected: anyerror, needle: []const u8, replacement: []const u8) !void {
    const gpa = testing.allocator;
    const at = std.mem.indexOf(u8, sample_json, needle) orelse return error.TestNeedleNotFound;
    const text = try std.mem.concat(gpa, u8, &.{ sample_json[0..at], replacement, sample_json[at + needle.len ..] });
    defer gpa.free(text);
    if (parse(gpa, text, "sample-a")) |p| {
        p.deinit();
        return error.TestUnexpectedSuccess;
    } else |err| try testing.expectEqual(expected, err);
}

test "strict structure: unknown, duplicate, missing, type and number mutations" {
    try expectRejected(error.UnknownField, "\"summary\": \"test sample\",", "\"summary\": \"test sample\", \"extra\": 1,");
    try expectRejected(error.DuplicateField, "\"candidate_version\": 1,", "\"candidate_version\": 1, \"candidate_version\": 1,");
    try expectRejected(error.MissingField, "\"author\": \"author-agent\",", "");
    try expectRejected(error.TypeMismatch, "\"candidate_version\": 1,", "\"candidate_version\": \"1\",");
    try expectRejected(error.IntegerNotExact, "\"mass_mg\": 1000,", "\"mass_mg\": 1000.5,");
    try expectRejected(error.IntegerNotExact, "\"position_um\": [15000, 0, 0]", "\"position_um\": [20000.0, 0, 0]");
    try expectRejected(error.IntegerOutOfRange, "\"mass_mg\": 500,", "\"mass_mg\": -5,");
    try expectRejected(error.InvalidEnumTag, "\"family\": \"A\"", "\"family\": \"D\"");
    try expectRejected(error.InvalidEnumTag, "\"mass_mg\": 500, \"mass_basis\": \"source\",", "\"mass_mg\": 500, \"mass_basis\": \"guess\",");
}

test "value validation: ids, dates, quaternions, extents, vectors" {
    try expectRejected(error.CandidateIdMismatch, "\"candidate_id\": \"sample-a\"", "\"candidate_id\": \"sample-b\"");
    try expectRejected(error.InvalidCandidateId, "\"candidate_id\": \"sample-a\"", "\"candidate_id\": \"Sample_A\"");
    try expectRejected(error.InvalidCandidateVersion, "\"candidate_version\": 1", "\"candidate_version\": 0");
    try expectRejected(error.InvalidDate, "\"declared_on\": \"2026-11-05\"", "\"declared_on\": \"2026-02-30\"");
    try expectRejected(error.NotUnitQuaternion, "\"id\": \"shell\", \"kind\": \"box\", \"half_extent_um\": [15000, 15000, 15000], \"pose\": { \"position_um\": [0, 0, 0], \"orientation\": [1, 0", "\"id\": \"shell\", \"kind\": \"box\", \"half_extent_um\": [15000, 15000, 15000], \"pose\": { \"position_um\": [0, 0, 0], \"orientation\": [1, 0.1");
    try expectRejected(error.ExtentNotPositive, "\"half_extent_um\": [15000, 15000, 15000]", "\"half_extent_um\": [15000, 0, 15000]");
    try expectRejected(error.NotUnitVector, "\"normal\": [1, 0, 0]", "\"normal\": [1, 0.1, 0]");
}

test "cross-field rules: kind fields, derivation, energy source, ids" {
    try expectRejected(error.PrimitiveFieldsMismatch, "\"kind\": \"box\", \"half_extent_um\": [14000", "\"kind\": \"sphere\", \"half_extent_um\": [14000");
    try expectRejected(error.PrimitiveFieldsMismatch, "\"kind\": \"box\", \"half_extent_um\": [14000", "\"kind\": \"cylinder\", \"radius_um\": 5, \"half_extent_um\": [14000");
    try expectRejected(error.FieldPresenceMismatch, "\"mass_mg\": 500, \"mass_basis\": \"source\",", "\"mass_mg\": 500, \"mass_basis\": \"source\", \"derivation\": { \"density_kg_m3\": 1, \"volume_m3\": 1 },");
    try expectRejected(error.InvalidDerivation, "\"mass_mg\": 500, \"mass_basis\": \"source\",", "\"mass_mg\": 500, \"mass_basis\": \"derived\",");
    try expectRejected(error.InvalidDerivation, "\"mass_mg\": 500, \"mass_basis\": \"source\",", "\"mass_mg\": 500, \"mass_basis\": \"derived\", \"derivation\": { \"density_kg_m3\": 0, \"volume_m3\": 1 },");
    try expectRejected(error.FieldPresenceMismatch, "\"description\": \"mcu\",", "\"description\": \"mcu\", \"energy_mj\": 5,");
    try expectRejected(error.EnergySourceCount, "\"kind\": \"energy_source\"", "\"kind\": \"controller\"");
    try expectRejected(error.UnknownSiteId, "\"head_site\": \"s-plus\"", "\"head_site\": \"nope\"");
    try expectRejected(error.UnknownComponentId, "\"component_ids\": [\"mcu\"], \"release\"", "\"component_ids\": [\"ghost\"], \"release\"");
    try expectRejected(error.DuplicateId, "\"id\": \"mcu\"", "\"id\": \"cell\"");
    try expectRejected(error.CavityInChainGeometry, "\"role\": \"body\" }\n  ] },\n  \"components\"", "\"role\": \"cavity\" }\n  ] },\n  \"components\"");
}

test "an explicit null rated discharge is accepted for the energy source, absence is not" {
    const gpa = testing.allocator;
    const needle = "\"rated_continuous_discharge_a\": 1.0,";
    const at = std.mem.indexOf(u8, sample_json, needle).?;
    const with_null = try std.mem.concat(gpa, u8, &.{ sample_json[0..at], "\"rated_continuous_discharge_a\": null,", sample_json[at + needle.len ..] });
    defer gpa.free(with_null);
    const p = try parse(gpa, with_null, null);
    defer p.deinit();
    try testing.expectEqual(@as(?f64, null), p.value.components[0].rated_continuous_discharge_a);
    const absent = try std.mem.concat(gpa, u8, &.{ sample_json[0..at], sample_json[at + needle.len ..] });
    defer gpa.free(absent);
    try testing.expectError(error.FieldPresenceMismatch, parse(gpa, absent, null));
}

test "a missing source is accepted as structure (G3 judges it)" {
    const gpa = testing.allocator;
    const needle = "\"source\": { \"kind\": \"datasheet\", \"url\": \"https://example.org/mcu.pdf\", \"accessed\": \"2026-11-04\", \"title\": \"MCU\" }";
    const at = std.mem.indexOf(u8, sample_json, needle).?;
    const text = try std.mem.concat(gpa, u8, &.{ sample_json[0..at], "\"source\": null", sample_json[at + needle.len ..] });
    defer gpa.free(text);
    const p = try parse(gpa, text, null);
    defer p.deinit();
    try testing.expectEqual(@as(?Source, null), p.value.components[1].source);
}

test "calendar dates" {
    try testing.expect(isValidDate("2024-02-29"));
    try testing.expect(!isValidDate("2026-02-29"));
    try testing.expect(!isValidDate("2026-13-01"));
    try testing.expect(!isValidDate("2026-1-01"));
    try testing.expect(!isValidDate("2026/11/01"));
    try testing.expect(!isValidDate("2026-11-0a"));
}
