//! Canonical binary encoding (Q44, DAT-002, DAT-004).
//!
//! Defines the byte-level encoding primitives shared by checkpoint state
//! hashes and binary recordings:
//!
//! - integers: fixed width, little-endian
//! - `f64`: the exact IEEE-754 bit pattern as a little-endian `u64`
//!   (so `-0.0` and `+0.0` encode differently, as exact replay requires)
//! - `bool`: one byte, 0 or 1
//! - byte strings: `u64` length, then the bytes
//!
//! Raw Zig structs are never encoded. Each state type writes its fields
//! explicitly and in a documented order, so a field reorder in source can
//! never silently change a hash.
//!
//! Non-finite floats (NaN, ±inf) are rejected with `error.NonFiniteValue`.
//! Authoritative state containing them signals numerical failure, and a
//! hash must not quietly absorb it. This is fail-closed and may be revisited
//! by decision if a model ever needs to record non-finite values.

const std = @import("std");
const Sha256 = std.crypto.hash.sha2.Sha256;

pub const Error = error{NonFiniteValue};

/// Encoder over any sink with `fn update(self: *Sink, bytes: []const u8) SinkError!void`.
pub fn Encoder(comptime Sink: type, comptime SinkError: type) type {
    return struct {
        const Self = @This();
        pub const WriteError = Error || SinkError;

        sink: *Sink,

        pub fn bytesRaw(self: Self, raw: []const u8) SinkError!void {
            try self.sink.update(raw);
        }

        pub fn int(self: Self, comptime T: type, v: T) SinkError!void {
            var buf: [@sizeOf(T)]u8 = undefined;
            std.mem.writeInt(T, &buf, v, .little);
            try self.sink.update(&buf);
        }

        pub fn boolean(self: Self, v: bool) SinkError!void {
            try self.int(u8, @intFromBool(v));
        }

        pub fn float(self: Self, v: f64) WriteError!void {
            if (!std.math.isFinite(v)) return error.NonFiniteValue;
            try self.int(u64, @bitCast(v));
        }

        pub fn bytes(self: Self, v: []const u8) SinkError!void {
            try self.int(u64, v.len);
            try self.sink.update(v);
        }
    };
}

/// Sink that feeds a SHA-256 checkpoint state hash.
pub const HashSink = struct {
    hasher: Sha256 = .init(.{}),

    pub fn update(self: *HashSink, b: []const u8) error{}!void {
        self.hasher.update(b);
    }

    pub fn encoder(self: *HashSink) StateHasher {
        return .{ .sink = self };
    }

    pub fn final(self: *HashSink) [Sha256.digest_length]u8 {
        return self.hasher.finalResult();
    }
};

pub const StateHasher = Encoder(HashSink, error{});

/// Sink that appends to a growable byte buffer (used by recordings).
pub const BufferSink = struct {
    gpa: std.mem.Allocator,
    list: std.ArrayList(u8) = .empty,

    pub fn update(self: *BufferSink, b: []const u8) error{OutOfMemory}!void {
        try self.list.appendSlice(self.gpa, b);
    }

    pub fn encoder(self: *BufferSink) BufferEncoder {
        return .{ .sink = self };
    }

    pub fn deinit(self: *BufferSink) void {
        self.list.deinit(self.gpa);
    }
};

pub const BufferEncoder = Encoder(BufferSink, error{OutOfMemory});

/// Bounds-checked little-endian decoder over a byte slice.
pub const Decoder = struct {
    bytes: []const u8,
    pos: usize = 0,

    pub const DecodeError = error{ Truncated, NonFiniteValue, InvalidBool };

    pub fn take(self: *Decoder, n: usize) DecodeError![]const u8 {
        if (n > self.bytes.len - self.pos) return error.Truncated;
        defer self.pos += n;
        return self.bytes[self.pos..][0..n];
    }

    pub fn int(self: *Decoder, comptime T: type) DecodeError!T {
        const b = try self.take(@sizeOf(T));
        return std.mem.readInt(T, b[0..@sizeOf(T)], .little);
    }

    pub fn boolean(self: *Decoder) DecodeError!bool {
        return switch (try self.int(u8)) {
            0 => false,
            1 => true,
            else => error.InvalidBool,
        };
    }

    pub fn float(self: *Decoder) DecodeError!f64 {
        const v: f64 = @bitCast(try self.int(u64));
        if (!std.math.isFinite(v)) return error.NonFiniteValue;
        return v;
    }

    pub fn bytesPrefixed(self: *Decoder) DecodeError![]const u8 {
        const n = try self.int(u64);
        if (n > self.bytes.len - self.pos) return error.Truncated;
        return self.take(@intCast(n));
    }

    pub fn done(self: *const Decoder) bool {
        return self.pos == self.bytes.len;
    }
};

const testing = std.testing;

test "encoding is little-endian and exact for floats" {
    var sink: BufferSink = .{ .gpa = testing.allocator };
    defer sink.deinit();
    const e = sink.encoder();
    try e.int(u32, 0x01020304);
    try e.float(-0.0);
    try e.boolean(true);
    try e.bytes("ab");
    try testing.expectEqualSlices(u8, &.{
        0x04, 0x03, 0x02, 0x01,
        0, 0, 0, 0, 0, 0, 0, 0x80,
        1,
        2, 0, 0, 0, 0, 0, 0, 0, 'a', 'b',
    }, sink.list.items);

    var d: Decoder = .{ .bytes = sink.list.items };
    try testing.expectEqual(@as(u32, 0x01020304), try d.int(u32));
    try testing.expectEqual(@as(u64, 0x8000000000000000), @as(u64, @bitCast(try d.float())));
    try testing.expect(try d.boolean());
    try testing.expectEqualStrings("ab", try d.bytesPrefixed());
    try testing.expect(d.done());
}

test "non-finite values are rejected on encode and decode" {
    var h: HashSink = .{};
    const e = h.encoder();
    try testing.expectError(error.NonFiniteValue, e.float(std.math.nan(f64)));
    try testing.expectError(error.NonFiniteValue, e.float(std.math.inf(f64)));
    var nan_bytes: [8]u8 = undefined;
    std.mem.writeInt(u64, &nan_bytes, @bitCast(std.math.nan(f64)), .little);
    var d: Decoder = .{ .bytes = &nan_bytes };
    try testing.expectError(error.NonFiniteValue, d.float());
}

test "decoder rejects truncation and invalid booleans" {
    var d: Decoder = .{ .bytes = &.{ 1, 2, 3 } };
    try testing.expectError(error.Truncated, d.int(u32));
    var d2: Decoder = .{ .bytes = &.{ 255, 0, 0, 0, 0, 0, 0, 0 } };
    try testing.expectError(error.Truncated, d2.bytesPrefixed());
    var d3: Decoder = .{ .bytes = &.{2} };
    try testing.expectError(error.InvalidBool, d3.boolean());
}

test "state hash distinguishes signed zero and field order" {
    var a: HashSink = .{};
    try a.encoder().float(0.0);
    var b: HashSink = .{};
    try b.encoder().float(-0.0);
    try testing.expect(!std.mem.eql(u8, &a.final(), &b.final()));

    var c: HashSink = .{};
    try c.encoder().int(u8, 1);
    try c.encoder().int(u8, 2);
    var d: HashSink = .{};
    try d.encoder().int(u8, 2);
    try d.encoder().int(u8, 1);
    try testing.expect(!std.mem.eql(u8, &c.final(), &d.final()));
}

test "hash and buffer encoders produce the same bytes" {
    var buf: BufferSink = .{ .gpa = testing.allocator };
    defer buf.deinit();
    var hs: HashSink = .{};
    inline for (.{ buf.encoder(), hs.encoder() }) |e| {
        try e.int(u64, 42);
        try e.float(1.5);
        try e.bytes("kin");
    }
    var direct: [32]u8 = undefined;
    Sha256.hash(buf.list.items, &direct, .{});
    try testing.expectEqualSlices(u8, &direct, &hs.final());
}
