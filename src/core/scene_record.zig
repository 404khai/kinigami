//! Payload layouts for recording formats v2 (Q51) and v3 (Q55): the scene
//! header and the per-step snapshot. Every field is written explicitly,
//! little-endian, with exact `f64` bit patterns (DAT-002). Decoding
//! validates fail-closed. Encoders always write v3; decoders read v2 and v3.
//!
//! v3 adds, after the v2 header bodies:
//!   link_count u32 | link_count × { body_a u32 | body_b u32 |
//!     axes_a 3×(3×f64) | anchor_a_m 3×f64 | anchor_b_m 3×f64 | rest_length_m f64 }
//! and after the v2 snapshot contacts:
//!   link_count u32 | link_count × { force_on_b_n 3×f64 | moment_on_b_nm 3×f64 |
//!     extension_m 3×f64 | rotation_rad 3×f64 }
//! plus body kind 2 (static_fixture, mass_kg written as 0 meaning infinite).
//!
//! scene_header:
//!   time_unit_numerator_s u64 | time_unit_denominator_s u64 |
//!   physics_step_ticks u64 | snapshot_interval_steps u32 | body_count u32 |
//!   body_count × { id bytes | kind u8 (0 fixture, 1 kin_candidate) |
//!                  shape u8 (0 cuboid) | half_extents_m 3×f64 | mass_kg f64 }
//!
//! snapshot:
//!   tick u64 | body_count u32 |
//!   body_count × { position_m 3×f64 | orientation (w,x,y,z) 4×f64 |
//!                  velocity_m_s 3×f64 | angular_velocity_rad_s 3×f64 } |
//!   contact_count u32 |
//!   contact_count × { body_a u32 | body_b u32 (0xFFFFFFFF = tabletop) |
//!                     point_m 3×f64 | normal 3×f64 | normal_force_n f64 |
//!                     tangential_force_n 3×f64 }

const std = @import("std");
const canonical = @import("canonical.zig");

pub const tabletop: u32 = 0xFFFF_FFFF;

pub const Vec3 = [3]f64;

pub const BodyKind = enum(u8) { fixture = 0, kin_candidate = 1, static_fixture = 2 };

/// Newest payload version written by the encoders (matches recording.format_version).
pub const payload_version: u16 = 3;
pub const Shape = enum(u8) { cuboid = 0 };

pub const BodyInfo = struct {
    id: []const u8,
    kind: BodyKind,
    shape: Shape,
    half_extents_m: Vec3,
    mass_kg: f64,
};

/// Link geometry (v3). `axes_a` are the anchor-A frame axes (axial,
/// shear 1, shear 2) in body A's frame, as the solver uses them.
pub const LinkInfo = struct {
    body_a: u32,
    body_b: u32,
    axes_a: [3]Vec3,
    anchor_a_m: Vec3,
    anchor_b_m: Vec3,
    rest_length_m: f64,
};

pub const SceneHeader = struct {
    time_unit_numerator_s: u64,
    time_unit_denominator_s: u64,
    physics_step_ticks: u64,
    snapshot_interval_steps: u32,
    bodies: []const BodyInfo,
    links: []const LinkInfo = &.{},
    /// Payload version the header was decoded from (2 or 3).
    version: u16 = payload_version,
};

pub const BodyState = struct {
    position_m: Vec3,
    /// (w, x, y, z)
    orientation: [4]f64,
    velocity_m_s: Vec3,
    angular_velocity_rad_s: Vec3,
};

pub const ContactRecord = struct {
    body_a: u32,
    /// `tabletop` for contacts against the reference tabletop.
    body_b: u32,
    point_m: Vec3,
    normal: Vec3,
    normal_force_n: f64,
    tangential_force_n: Vec3,
};

/// Solver-native link report (v3), anchor-A components (PHY-005).
pub const LinkRecord = struct {
    force_on_b_n: Vec3,
    moment_on_b_nm: Vec3,
    extension_m: Vec3,
    rotation_rad: Vec3,
};

pub const Snapshot = struct {
    tick: u64,
    bodies: []const BodyState,
    contacts: []const ContactRecord,
    links: []const LinkRecord = &.{},
};

pub const DecodeError = canonical.Decoder.DecodeError || error{
    InvalidEnum,
    InvalidHeader,
    BodyCountMismatch,
    InvalidContactBody,
    InvalidLinkBody,
    LinkCountMismatch,
    UnsupportedVersion,
    TrailingPayload,
    OutOfMemory,
};

fn vec(e: canonical.BufferEncoder, v: Vec3) !void {
    for (v) |x| try e.float(x);
}
fn readVec(d: *canonical.Decoder) !Vec3 {
    return .{ try d.float(), try d.float(), try d.float() };
}

pub fn encodeHeader(e: canonical.BufferEncoder, h: SceneHeader) canonical.BufferEncoder.WriteError!void {
    try e.int(u64, h.time_unit_numerator_s);
    try e.int(u64, h.time_unit_denominator_s);
    try e.int(u64, h.physics_step_ticks);
    try e.int(u32, h.snapshot_interval_steps);
    try e.int(u32, @intCast(h.bodies.len));
    for (h.bodies) |b| {
        try e.bytes(b.id);
        try e.int(u8, @intFromEnum(b.kind));
        try e.int(u8, @intFromEnum(b.shape));
        try vec(e, b.half_extents_m);
        try e.float(b.mass_kg);
    }
    try e.int(u32, @intCast(h.links.len));
    for (h.links) |l| {
        try e.int(u32, l.body_a);
        try e.int(u32, l.body_b);
        for (l.axes_a) |a| try vec(e, a);
        try vec(e, l.anchor_a_m);
        try vec(e, l.anchor_b_m);
        try e.float(l.rest_length_m);
    }
}

/// `version` is the recording's format version (2 or 3).
pub fn decodeHeader(arena: std.mem.Allocator, payload: []const u8, version: u16) DecodeError!SceneHeader {
    if (version != 2 and version != 3) return error.UnsupportedVersion;
    var d: canonical.Decoder = .{ .bytes = payload };
    var h: SceneHeader = .{
        .time_unit_numerator_s = try d.int(u64),
        .time_unit_denominator_s = try d.int(u64),
        .physics_step_ticks = try d.int(u64),
        .snapshot_interval_steps = try d.int(u32),
        .bodies = undefined,
        .version = version,
    };
    if (h.time_unit_numerator_s == 0 or h.time_unit_denominator_s == 0 or h.physics_step_ticks == 0 or h.snapshot_interval_steps == 0)
        return error.InvalidHeader;
    const n = try d.int(u32);
    const bodies = try arena.alloc(BodyInfo, n);
    for (bodies) |*b| {
        b.* = .{
            .id = try arena.dupe(u8, try d.bytesPrefixed()),
            .kind = std.enums.fromInt(BodyKind, try d.int(u8)) orelse return error.InvalidEnum,
            .shape = std.enums.fromInt(Shape, try d.int(u8)) orelse return error.InvalidEnum,
            .half_extents_m = try readVec(&d),
            .mass_kg = try d.float(),
        };
        if (version < 3 and b.kind == .static_fixture) return error.InvalidEnum;
    }
    h.bodies = bodies;
    if (version >= 3) {
        const nl = try d.int(u32);
        const links = try arena.alloc(LinkInfo, nl);
        for (links) |*l| {
            l.body_a = try d.int(u32);
            l.body_b = try d.int(u32);
            if (l.body_a >= n or l.body_b >= n or l.body_a == l.body_b) return error.InvalidLinkBody;
            for (&l.axes_a) |*a| a.* = try readVec(&d);
            l.anchor_a_m = try readVec(&d);
            l.anchor_b_m = try readVec(&d);
            l.rest_length_m = try d.float();
        }
        h.links = links;
    }
    if (!d.done()) return error.TrailingPayload;
    return h;
}

pub fn encodeSnapshot(e: canonical.BufferEncoder, s: Snapshot) canonical.BufferEncoder.WriteError!void {
    try e.int(u64, s.tick);
    try e.int(u32, @intCast(s.bodies.len));
    for (s.bodies) |b| {
        try vec(e, b.position_m);
        for (b.orientation) |x| try e.float(x);
        try vec(e, b.velocity_m_s);
        try vec(e, b.angular_velocity_rad_s);
    }
    try e.int(u32, @intCast(s.contacts.len));
    for (s.contacts) |c| {
        try e.int(u32, c.body_a);
        try e.int(u32, c.body_b);
        try vec(e, c.point_m);
        try vec(e, c.normal);
        try e.float(c.normal_force_n);
        try vec(e, c.tangential_force_n);
    }
    try e.int(u32, @intCast(s.links.len));
    for (s.links) |l| inline for (.{ "force_on_b_n", "moment_on_b_nm", "extension_m", "rotation_rad" }) |f| try vec(e, @field(l, f));
}

/// Decodes one snapshot, checking it against the scene header.
pub fn decodeSnapshot(arena: std.mem.Allocator, header: SceneHeader, payload: []const u8) DecodeError!Snapshot {
    var d: canonical.Decoder = .{ .bytes = payload };
    const tick = try d.int(u64);
    const nb = try d.int(u32);
    if (nb != header.bodies.len) return error.BodyCountMismatch;
    const bodies = try arena.alloc(BodyState, nb);
    for (bodies) |*b| {
        b.position_m = try readVec(&d);
        for (&b.orientation) |*x| x.* = try d.float();
        b.velocity_m_s = try readVec(&d);
        b.angular_velocity_rad_s = try readVec(&d);
    }
    const nc = try d.int(u32);
    const contacts = try arena.alloc(ContactRecord, nc);
    for (contacts) |*c| {
        c.body_a = try d.int(u32);
        c.body_b = try d.int(u32);
        if (c.body_a >= nb or (c.body_b != tabletop and c.body_b >= nb)) return error.InvalidContactBody;
        c.point_m = try readVec(&d);
        c.normal = try readVec(&d);
        c.normal_force_n = try d.float();
        c.tangential_force_n = try readVec(&d);
    }
    var links: []LinkRecord = &.{};
    if (header.version >= 3) {
        const nl = try d.int(u32);
        if (nl != header.links.len) return error.LinkCountMismatch;
        links = try arena.alloc(LinkRecord, nl);
        for (links) |*l| inline for (.{ "force_on_b_n", "moment_on_b_nm", "extension_m", "rotation_rad" }) |f| {
            @field(l, f) = try readVec(&d);
        };
    }
    if (!d.done()) return error.TrailingPayload;
    return .{ .tick = tick, .bodies = bodies, .contacts = contacts, .links = links };
}

const testing = std.testing;

test "header and snapshot round trip exactly" {
    var arena = std.heap.ArenaAllocator.init(testing.allocator);
    defer arena.deinit();
    const a = arena.allocator();
    const header: SceneHeader = .{
        .time_unit_numerator_s = 1,
        .time_unit_denominator_s = 1_000_000,
        .physics_step_ticks = 500,
        .snapshot_interval_steps = 1,
        .bodies = &.{.{ .id = "fixture_flat_block", .kind = .fixture, .shape = .cuboid, .half_extents_m = .{ 0.02, 0.02, 0.01 }, .mass_kg = 0.04 }},
    };
    var hs: canonical.BufferSink = .{ .gpa = a };
    try encodeHeader(hs.encoder(), header);
    const h2 = try decodeHeader(a, hs.list.items, 3);
    try testing.expectEqualStrings("fixture_flat_block", h2.bodies[0].id);
    try testing.expectEqual(@as(u64, 500), h2.physics_step_ticks);

    const snap: Snapshot = .{
        .tick = 1000,
        .bodies = &.{.{ .position_m = .{ 0, 0, 0.01 }, .orientation = .{ 1, 0, 0, -0.0 }, .velocity_m_s = .{ 0.1, 0, 0 }, .angular_velocity_rad_s = .{ 0, 0, 0 } }},
        .contacts = &.{.{ .body_a = 0, .body_b = tabletop, .point_m = .{ 0.02, 0.02, 0 }, .normal = .{ 0, 0, 1 }, .normal_force_n = 0.098, .tangential_force_n = .{ -0.01, 0, 0 } }},
    };
    var ss: canonical.BufferSink = .{ .gpa = a };
    try encodeSnapshot(ss.encoder(), snap);
    const s2 = try decodeSnapshot(a, h2, ss.list.items);
    try testing.expectEqual(@as(u64, 1000), s2.tick);
    try testing.expectEqual(@as(u64, @bitCast(@as(f64, -0.0))), @as(u64, @bitCast(s2.bodies[0].orientation[3])));
    try testing.expectEqual(tabletop, s2.contacts[0].body_b);
}

test "snapshot decoding fails closed" {
    var arena = std.heap.ArenaAllocator.init(testing.allocator);
    defer arena.deinit();
    const a = arena.allocator();
    const header: SceneHeader = .{ .time_unit_numerator_s = 1, .time_unit_denominator_s = 1, .physics_step_ticks = 1, .snapshot_interval_steps = 1, .bodies = &.{} };
    var s: canonical.BufferSink = .{ .gpa = a };
    const e = s.encoder();
    try e.int(u64, 0);
    try e.int(u32, 1); // one body, but the header declares none
    try testing.expectError(error.BodyCountMismatch, decodeSnapshot(a, header, s.list.items));

    var s2: canonical.BufferSink = .{ .gpa = a };
    const e2 = s2.encoder();
    try e2.int(u64, 0);
    try e2.int(u32, 0);
    try e2.int(u32, 1);
    try e2.int(u32, 0); // body_a 0 with no bodies
    try e2.int(u32, tabletop);
    try testing.expectError(error.InvalidContactBody, decodeSnapshot(a, header, s2.list.items));

    var hb: canonical.BufferSink = .{ .gpa = a };
    try encodeHeader(hb.encoder(), header);
    hb.list.items[24] = 0; // snapshot_interval_steps = 0
    try testing.expectError(error.InvalidHeader, decodeHeader(a, hb.list.items, 3));
}

test "v3 links round trip; link count must match the header" {
    var arena = std.heap.ArenaAllocator.init(testing.allocator);
    defer arena.deinit();
    const a = arena.allocator();
    const header: SceneHeader = .{
        .time_unit_numerator_s = 1,
        .time_unit_denominator_s = 1_000_000,
        .physics_step_ticks = 1000,
        .snapshot_interval_steps = 1,
        .bodies = &.{
            .{ .id = "a", .kind = .static_fixture, .shape = .cuboid, .half_extents_m = .{ 0.01, 0.01, 0.01 }, .mass_kg = 0 },
            .{ .id = "b", .kind = .fixture, .shape = .cuboid, .half_extents_m = .{ 0.01, 0.01, 0.01 }, .mass_kg = 0.02 },
        },
        .links = &.{.{ .body_a = 0, .body_b = 1, .axes_a = .{ .{ 0, 0, -1 }, .{ 0, 1, 0 }, .{ 1, 0, 0 } }, .anchor_a_m = .{ 0, 0, -0.01 }, .anchor_b_m = .{ 0, 0, 0.01 }, .rest_length_m = 0.01 }},
    };
    var hs: canonical.BufferSink = .{ .gpa = a };
    try encodeHeader(hs.encoder(), header);
    const h2 = try decodeHeader(a, hs.list.items, 3);
    try testing.expectEqual(BodyKind.static_fixture, h2.bodies[0].kind);
    try testing.expectEqual(@as(f64, -1), h2.links[0].axes_a[0][2]);
    // A v3 header is not a valid v2 header (static kind, trailing link section).
    try testing.expect(std.meta.isError(decodeHeader(a, hs.list.items, 2)));

    const rec: LinkRecord = .{ .force_on_b_n = .{ -0.196, 0, 0 }, .moment_on_b_nm = .{ 0, 1e-4, 0 }, .extension_m = .{ 1.96e-3, 0, 0 }, .rotation_rad = .{ 0, 0.01, 0 } };
    const snap: Snapshot = .{ .tick = 0, .bodies = &.{
        .{ .position_m = .{ 0, 0, 1 }, .orientation = .{ 1, 0, 0, 0 }, .velocity_m_s = .{ 0, 0, 0 }, .angular_velocity_rad_s = .{ 0, 0, 0 } },
        .{ .position_m = .{ 0, 0, 0.97 }, .orientation = .{ 1, 0, 0, 0 }, .velocity_m_s = .{ 0, 0, 0 }, .angular_velocity_rad_s = .{ 0, 0, 0 } },
    }, .contacts = &.{}, .links = &.{rec} };
    var ss: canonical.BufferSink = .{ .gpa = a };
    try encodeSnapshot(ss.encoder(), snap);
    const s2 = try decodeSnapshot(a, h2, ss.list.items);
    try testing.expectEqual(rec, s2.links[0]);

    var no_links = h2;
    no_links.links = &.{};
    try testing.expectError(error.LinkCountMismatch, decodeSnapshot(a, no_links, ss.list.items));
}
