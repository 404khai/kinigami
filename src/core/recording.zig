//! Versioned binary recording container (Q44, Q51, DAT-002, DAT-010).
//!
//! Layout (all integers little-endian, via `canonical`):
//!
//! ```text
//! header   magic "KINIGREC" (8 bytes) | format_version u16 | flags u16 (must be 0)
//! chunk*   chunk_type u32 | payload_length u64 | payload
//! ```
//!
//! Version 1 (Q44): `effective_config`, `end`.
//! Version 2 (Q51): `effective_config`, `scene_header`, `snapshot`*, `end`.
//! Payload layouts for `scene_header` and `snapshot` are in `scene_record.zig`.
//!
//! The reader enforces, failing closed:
//! - the first chunk is `effective_config`, holding the exact bytes of the
//!   effective run configuration JSON;
//! - v2 only: `scene_header` comes second and exactly once, then snapshots;
//! - the last chunk is `end` with an empty payload, and nothing follows it;
//! - unknown or version-inappropriate chunk types, unsupported versions, and
//!   nonzero flags are rejected, never skipped or reinterpreted.
//!
//! The writer always produces the newest version. Version-1 files remain
//! readable. A recording's file identity is the SHA-256 of its bytes (DAT-003).

const std = @import("std");
const canonical = @import("canonical.zig");

pub const magic = "KINIGREC";
pub const format_version: u16 = 2;

pub const ChunkType = enum(u32) {
    effective_config = 1,
    scene_header = 2,
    snapshot = 3,
    end = 0xFFFF_FFFF,
};

pub const ReadError = canonical.Decoder.DecodeError || error{
    BadMagic,
    UnsupportedVersion,
    UnsupportedFlags,
    UnsupportedChunkType,
    MissingEffectiveConfig,
    DuplicateEffectiveConfig,
    MissingSceneHeader,
    ChunkOutOfOrder,
    MissingEnd,
    NonEmptyEnd,
    TrailingBytes,
};

pub const Writer = struct {
    sink: canonical.BufferSink,
    state: enum { header_due, snapshots, finished } = .header_due,

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

    /// Exactly once, before any snapshot.
    pub fn sceneHeader(self: *Writer, payload: []const u8) error{OutOfMemory}!void {
        std.debug.assert(self.state == .header_due);
        try self.chunk(.scene_header, payload);
        self.state = .snapshots;
    }

    pub fn snapshot(self: *Writer, payload: []const u8) error{OutOfMemory}!void {
        std.debug.assert(self.state == .snapshots);
        try self.chunk(.snapshot, payload);
    }

    /// Appends the end marker and returns the complete recording bytes.
    pub fn finish(self: *Writer) error{OutOfMemory}![]u8 {
        std.debug.assert(self.state == .snapshots);
        try self.chunk(.end, "");
        self.state = .finished;
        return self.sink.list.toOwnedSlice(self.sink.gpa);
    }

    pub fn deinit(self: *Writer) void {
        self.sink.deinit();
    }
};

/// A validated recording. Payload slices point into the input bytes.
pub const Recording = struct {
    version: u16,
    effective_config: []const u8,
    /// Null for version-1 recordings.
    scene_header: ?[]const u8,
    snapshot_count: usize,
    /// Byte region holding the snapshot chunks, for `snapshots()`.
    snapshot_region: []const u8,

    /// Validates the whole container before returning anything.
    pub fn parse(bytes: []const u8) ReadError!Recording {
        var d: canonical.Decoder = .{ .bytes = bytes };
        if (!std.mem.eql(u8, try d.take(magic.len), magic)) return error.BadMagic;
        const version = try d.int(u16);
        if (version != 1 and version != 2) return error.UnsupportedVersion;
        if (try d.int(u16) != 0) return error.UnsupportedFlags;

        var r: Recording = .{ .version = version, .effective_config = undefined, .scene_header = null, .snapshot_count = 0, .snapshot_region = &.{} };
        var have_config = false;
        var region_start: ?usize = null;
        var region_end: usize = 0;
        while (true) {
            if (d.done()) return error.MissingEnd;
            const chunk_start = d.pos;
            const t = std.enums.fromInt(ChunkType, try d.int(u32)) orelse return error.UnsupportedChunkType;
            const payload = try d.bytesPrefixed();
            if (version == 1 and (t == .scene_header or t == .snapshot)) return error.UnsupportedChunkType;
            switch (t) {
                .effective_config => {
                    if (have_config) return error.DuplicateEffectiveConfig;
                    have_config = true;
                    r.effective_config = payload;
                    continue;
                },
                .end => {
                    if (!have_config) return error.MissingEffectiveConfig;
                    if (version == 2 and r.scene_header == null) return error.MissingSceneHeader;
                    if (payload.len != 0) return error.NonEmptyEnd;
                    if (!d.done()) return error.TrailingBytes;
                    break;
                },
                .scene_header => {
                    if (!have_config) return error.MissingEffectiveConfig;
                    if (r.scene_header != null) return error.ChunkOutOfOrder;
                    r.scene_header = payload;
                },
                .snapshot => {
                    if (!have_config) return error.MissingEffectiveConfig;
                    if (r.scene_header == null) return error.MissingSceneHeader;
                    if (region_start == null) region_start = chunk_start;
                    region_end = d.pos;
                    r.snapshot_count += 1;
                },
            }
        }
        if (region_start) |s| r.snapshot_region = bytes[s..region_end];
        return r;
    }

    /// Iterates snapshot payloads in recorded order.
    pub fn snapshots(self: Recording) SnapshotIterator {
        return .{ .d = .{ .bytes = self.snapshot_region } };
    }
};

pub const SnapshotIterator = struct {
    d: canonical.Decoder,

    pub fn next(self: *SnapshotIterator) ?[]const u8 {
        if (self.d.done()) return null;
        _ = self.d.int(u32) catch return null; // validated by parse
        return self.d.bytesPrefixed() catch null;
    }
};

const testing = std.testing;

fn sample(gpa: std.mem.Allocator) ![]u8 {
    var w = try Writer.init(gpa, "{\"schema_version\":1}");
    defer w.deinit();
    try w.sceneHeader("H");
    try w.snapshot("s0");
    try w.snapshot("s1");
    return w.finish();
}

fn v1Sample(gpa: std.mem.Allocator) ![]u8 {
    var sink: canonical.BufferSink = .{ .gpa = gpa };
    errdefer sink.deinit();
    const e = sink.encoder();
    try e.bytesRaw(magic);
    try e.int(u16, 1);
    try e.int(u16, 0);
    try e.int(u32, @intFromEnum(ChunkType.effective_config));
    try e.bytes("{\"v\":1}");
    try e.int(u32, @intFromEnum(ChunkType.end));
    try e.int(u64, 0);
    return sink.list.toOwnedSlice(gpa);
}

test "v2 round trip with snapshots in order" {
    const bytes = try sample(testing.allocator);
    defer testing.allocator.free(bytes);
    const r = try Recording.parse(bytes);
    try testing.expectEqual(@as(u16, 2), r.version);
    try testing.expectEqualStrings("H", r.scene_header.?);
    try testing.expectEqual(@as(usize, 2), r.snapshot_count);
    var it = r.snapshots();
    try testing.expectEqualStrings("s0", it.next().?);
    try testing.expectEqualStrings("s1", it.next().?);
    try testing.expect(it.next() == null);
}

test "version-1 recordings remain readable (DAT-010)" {
    const bytes = try v1Sample(testing.allocator);
    defer testing.allocator.free(bytes);
    const r = try Recording.parse(bytes);
    try testing.expectEqual(@as(u16, 1), r.version);
    try testing.expectEqualStrings("{\"v\":1}", r.effective_config);
    try testing.expect(r.scene_header == null);
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
    copy[8] = 3;
    try testing.expectError(error.UnsupportedVersion, Recording.parse(copy));
    @memcpy(copy, bytes);
    copy[10] = 1;
    try testing.expectError(error.UnsupportedFlags, Recording.parse(copy));
    const longer = try std.mem.concat(gpa, u8, &.{ bytes, "x" });
    defer gpa.free(longer);
    try testing.expectError(error.TrailingBytes, Recording.parse(longer));
}

fn rawRecording(gpa: std.mem.Allocator, version: u16, chunks: []const struct { ChunkType, []const u8 }) ![]u8 {
    var sink: canonical.BufferSink = .{ .gpa = gpa };
    errdefer sink.deinit();
    const e = sink.encoder();
    try e.bytesRaw(magic);
    try e.int(u16, version);
    try e.int(u16, 0);
    for (chunks) |c| {
        try e.int(u32, @intFromEnum(c[0]));
        try e.bytes(c[1]);
    }
    return sink.list.toOwnedSlice(gpa);
}

test "structural rules fail closed" {
    const gpa = testing.allocator;
    const cases = .{
        .{ error.MissingSceneHeader, 2, &[_]struct { ChunkType, []const u8 }{ .{ .effective_config, "{}" }, .{ .snapshot, "s" }, .{ .end, "" } } },
        .{ error.MissingSceneHeader, 2, &[_]struct { ChunkType, []const u8 }{ .{ .effective_config, "{}" }, .{ .end, "" } } },
        .{ error.ChunkOutOfOrder, 2, &[_]struct { ChunkType, []const u8 }{ .{ .effective_config, "{}" }, .{ .scene_header, "h" }, .{ .scene_header, "h" }, .{ .end, "" } } },
        .{ error.MissingEffectiveConfig, 2, &[_]struct { ChunkType, []const u8 }{ .{ .scene_header, "h" }, .{ .end, "" } } },
        .{ error.DuplicateEffectiveConfig, 2, &[_]struct { ChunkType, []const u8 }{ .{ .effective_config, "{}" }, .{ .effective_config, "{}" } } },
        .{ error.NonEmptyEnd, 2, &[_]struct { ChunkType, []const u8 }{ .{ .effective_config, "{}" }, .{ .scene_header, "h" }, .{ .end, "x" } } },
        .{ error.UnsupportedChunkType, 1, &[_]struct { ChunkType, []const u8 }{ .{ .effective_config, "{}" }, .{ .scene_header, "h" }, .{ .end, "" } } },
    };
    inline for (cases) |c| {
        const bytes = try rawRecording(gpa, c[1], c[2]);
        defer gpa.free(bytes);
        try testing.expectError(c[0], Recording.parse(bytes));
    }
}

test "unknown chunk types are rejected" {
    const gpa = testing.allocator;
    var sink: canonical.BufferSink = .{ .gpa = gpa };
    defer sink.deinit();
    const e = sink.encoder();
    try e.bytesRaw(magic);
    try e.int(u16, format_version);
    try e.int(u16, 0);
    try e.int(u32, 7);
    try e.int(u64, 0);
    try testing.expectError(error.UnsupportedChunkType, Recording.parse(sink.list.items));
}
