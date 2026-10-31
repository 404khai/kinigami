//! Versioned binary recording container, format version 1 (Q44, DAT-002,
//! DAT-010).
//!
//! This fixes the **container** only. The payload layouts for snapshots,
//! events, sensor samples, and actuator records, and the snapshot interval,
//! are still open decisions; their chunk types are added to the registry
//! (with a format version bump if the container changes) once decided.
//!
//! Layout (all integers little-endian, via `canonical`):
//!
//! ```text
//! header   magic "KINIGREC" (8 bytes) | format_version u16 | flags u16 (must be 0)
//! chunk*   chunk_type u32 | payload_length u64 | payload
//! ```
//!
//! Rules, enforced by the reader (fail closed):
//! - the first chunk is `effective_config`: the exact bytes of the effective
//!   run configuration JSON, so every recording is self-describing (DAT-006);
//! - the last chunk is `end` with an empty payload, and nothing follows it,
//!   so truncation is detected;
//! - unknown chunk types, unsupported versions, and nonzero flags are
//!   rejected, never skipped or reinterpreted.
//!
//! A recording's file identity is the SHA-256 of its exact bytes (DAT-003).

const std = @import("std");
const canonical = @import("canonical.zig");

pub const magic = "KINIGREC";
pub const format_version: u16 = 1;

pub const ChunkType = enum(u32) {
    effective_config = 1,
    end = 0xFFFF_FFFF,
};

pub const ReadError = canonical.Decoder.DecodeError || error{
    BadMagic,
    UnsupportedVersion,
    UnsupportedFlags,
    UnsupportedChunkType,
    MissingEffectiveConfig,
    DuplicateEffectiveConfig,
    MissingEnd,
    NonEmptyEnd,
    TrailingBytes,
};

pub const Writer = struct {
    sink: canonical.BufferSink,
    finished: bool = false,

    pub fn init(gpa: std.mem.Allocator, effective_config_json: []const u8) error{OutOfMemory}!Writer {
        var w: Writer = .{ .sink = .{ .gpa = gpa } };
        errdefer w.sink.deinit();
        const e = w.sink.encoder();
        try e.bytesRaw(magic);
        try e.int(u16, format_version);
        try e.int(u16, 0);
        try w.chunk(.effective_config, effective_config_json);
        return w;
    }

    fn chunk(self: *Writer, t: ChunkType, payload: []const u8) error{OutOfMemory}!void {
        const e = self.sink.encoder();
        try e.int(u32, @intFromEnum(t));
        try e.int(u64, payload.len);
        try e.bytesRaw(payload);
    }

    /// Appends the end marker and returns the complete recording bytes.
    /// The caller owns the result; the writer must not be used afterwards.
    pub fn finish(self: *Writer) error{OutOfMemory}![]u8 {
        std.debug.assert(!self.finished);
        try self.chunk(.end, "");
        self.finished = true;
        return self.sink.list.toOwnedSlice(self.sink.gpa);
    }

    pub fn deinit(self: *Writer) void {
        self.sink.deinit();
    }
};

pub const Chunk = struct {
    type: ChunkType,
    payload: []const u8,
};

/// A validated recording. Payload slices point into the input bytes.
pub const Recording = struct {
    effective_config: []const u8,

    /// Validates the whole container before returning anything.
    pub fn parse(bytes: []const u8) ReadError!Recording {
        var d: canonical.Decoder = .{ .bytes = bytes };
        if (!std.mem.eql(u8, try d.take(magic.len), magic)) return error.BadMagic;
        if (try d.int(u16) != format_version) return error.UnsupportedVersion;
        if (try d.int(u16) != 0) return error.UnsupportedFlags;

        var config: ?[]const u8 = null;
        while (true) {
            if (d.done()) return error.MissingEnd;
            const raw_type = try d.int(u32);
            const t = std.enums.fromInt(ChunkType, raw_type) orelse return error.UnsupportedChunkType;
            const payload = try d.bytesPrefixed();
            switch (t) {
                .effective_config => {
                    if (config != null) return error.DuplicateEffectiveConfig;
                    config = payload;
                },
                .end => {
                    if (payload.len != 0) return error.NonEmptyEnd;
                    if (!d.done()) return error.TrailingBytes;
                    break;
                },
            }
            if (config == null) return error.MissingEffectiveConfig;
        }
        return .{ .effective_config = config orelse return error.MissingEffectiveConfig };
    }
};

const testing = std.testing;

fn sample(gpa: std.mem.Allocator) ![]u8 {
    var w = try Writer.init(gpa, "{\"schema_version\":1}");
    defer w.deinit();
    return w.finish();
}

test "round trip" {
    const bytes = try sample(testing.allocator);
    defer testing.allocator.free(bytes);
    const r = try Recording.parse(bytes);
    try testing.expectEqualStrings("{\"schema_version\":1}", r.effective_config);
    try testing.expectEqualStrings(magic, bytes[0..8]);
}

test "every strict prefix is rejected (truncation is detected)" {
    const bytes = try sample(testing.allocator);
    defer testing.allocator.free(bytes);
    for (0..bytes.len) |n| {
        if (Recording.parse(bytes[0..n])) |_| return error.TestUnexpectedSuccess else |_| {}
    }
}

test "rejects bad magic, version, flags, trailing bytes" {
    const gpa = testing.allocator;
    const bytes = try sample(gpa);
    defer gpa.free(bytes);
    const copy = try gpa.dupe(u8, bytes);
    defer gpa.free(copy);

    copy[0] = 'X';
    try testing.expectError(error.BadMagic, Recording.parse(copy));
    @memcpy(copy, bytes);
    copy[8] = 2;
    try testing.expectError(error.UnsupportedVersion, Recording.parse(copy));
    @memcpy(copy, bytes);
    copy[10] = 1;
    try testing.expectError(error.UnsupportedFlags, Recording.parse(copy));

    const longer = try std.mem.concat(gpa, u8, &.{ bytes, "x" });
    defer gpa.free(longer);
    try testing.expectError(error.TrailingBytes, Recording.parse(longer));
}

test "rejects unknown chunk types and a missing leading config" {
    var sink: canonical.BufferSink = .{ .gpa = testing.allocator };
    defer sink.deinit();
    const e = sink.encoder();
    try e.bytesRaw(magic);
    try e.int(u16, format_version);
    try e.int(u16, 0);
    try e.int(u32, 7); // unregistered chunk type
    try e.int(u64, 0);
    try testing.expectError(error.UnsupportedChunkType, Recording.parse(sink.list.items));

    sink.list.items.len = 12;
    try e.int(u32, @intFromEnum(ChunkType.end));
    try e.int(u64, 0);
    try testing.expectError(error.MissingEffectiveConfig, Recording.parse(sink.list.items));
}

test "rejects a duplicated config chunk and a non-empty end" {
    var sink: canonical.BufferSink = .{ .gpa = testing.allocator };
    defer sink.deinit();
    const e = sink.encoder();
    try e.bytesRaw(magic);
    try e.int(u16, format_version);
    try e.int(u16, 0);
    for (0..2) |_| {
        try e.int(u32, @intFromEnum(ChunkType.effective_config));
        try e.bytes("{}");
    }
    try testing.expectError(error.DuplicateEffectiveConfig, Recording.parse(sink.list.items));

    sink.list.items.len = 12 + 4 + 8 + 2;
    try e.int(u32, @intFromEnum(ChunkType.end));
    try e.bytes("x");
    try testing.expectError(error.NonEmptyEnd, Recording.parse(sink.list.items));
}
