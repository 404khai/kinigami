//! Payload layouts for recording format v2 (Q51): the scene header and the
//! per-step snapshot. Every field is written explicitly, little-endian, with
//! exact `f64` bit patterns (DAT-002). Decoding validates fail-closed.
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

pub const BodyKind = enum(u8) { fixture = 0, kin_candidate = 1 };
pub const Shape = enum(u8) { cuboid = 0 };

pub const BodyInfo = struct {
    id: []const u8,
    kind: BodyKind,
    shape: Shape,
    half_extents_m: Vec3,
    mass_kg: f64,
};

pub const SceneHeader = struct {
    time_unit_numerator_s: u64,
    time_unit_denominator_s: u64,
    physics_step_ticks: u64,
    snapshot_interval_steps: u32,
    bodies: []const BodyInfo,
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

pub const Snapshot = struct {
    tick: u64,
    bodies: []const BodyState,
    contacts: []const ContactRecord,
};

pub const DecodeError = canonical.Decoder.DecodeError || error{
    InvalidEnum,
    InvalidHeader,
    BodyCountMismatch,
    InvalidContactBody,
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
}

pub fn decodeHeader(arena: std.mem.Allocator, payload: []const u8) DecodeError!SceneHeader {
    var d: canonical.Decoder = .{ .bytes = payload };
    var h: SceneHeader = .{
        .time_unit_numerator_s = try d.int(u64),
        .time_unit_denominator_s = try d.int(u64),
        .physics_step_ticks = try d.int(u64),
        .snapshot_interval_steps = try d.int(u32),
        .bodies = undefined,
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
    }
    if (!d.done()) return error.TrailingPayload;
    h.bodies = bodies;
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
    if (!d.done()) return error.TrailingPayload;
    return .{ .tick = tick, .bodies = bodies, .contacts = contacts };
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
    const h2 = try decodeHeader(a, hs.list.items);
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
    try testing.expectError(error.InvalidHeader, decodeHeader(a, hb.list.items));
}
