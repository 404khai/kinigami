//! std.json behavior under the pinned toolchain, for typed (struct) parsing
//! with default options (DAT-005, DAT-007, DAT-008).

const std = @import("std");
const json = std.json;
const testing = std.testing;

const Sample = struct {
    count: u32,
    ratio: f64,
    mode: enum { strict, loose },
};

fn parse(comptime T: type, text: []const u8) !json.Parsed(T) {
    return json.parseFromSlice(T, testing.allocator, text, .{});
}

fn expectParseError(comptime T: type, text: []const u8) !void {
    if (parse(T, text)) |parsed| {
        parsed.deinit();
        return error.TestUnexpectedSuccess;
    } else |_| {}
}

test "accepts a well-formed document" {
    const p = try parse(Sample, "{\"count\":3,\"ratio\":0.5,\"mode\":\"strict\"}");
    defer p.deinit();
    try testing.expectEqual(@as(u32, 3), p.value.count);
    try testing.expectEqual(@as(f64, 0.5), p.value.ratio);
}

test "rejects unknown fields" {
    try testing.expectError(error.UnknownField, parse(Sample, "{\"count\":3,\"ratio\":0.5,\"mode\":\"strict\",\"extra\":1}"));
}

test "rejects duplicate keys" {
    try testing.expectError(error.DuplicateField, parse(Sample, "{\"count\":3,\"count\":4,\"ratio\":0.5,\"mode\":\"strict\"}"));
}

test "rejects missing required fields" {
    try testing.expectError(error.MissingField, parse(Sample, "{\"count\":3,\"mode\":\"strict\"}"));
}

test "rejects invalid enum names" {
    try testing.expectError(error.InvalidEnumTag, parse(Sample, "{\"count\":3,\"ratio\":0.5,\"mode\":\"medium\"}"));
}

test "rejects non-numeric strings and structural mismatches in number fields" {
    try expectParseError(Sample, "{\"count\":\"three\",\"ratio\":0.5,\"mode\":\"strict\"}");
    try expectParseError(Sample, "{\"count\":[3],\"ratio\":0.5,\"mode\":\"strict\"}");
    try expectParseError(Sample, "{\"count\":true,\"ratio\":0.5,\"mode\":\"strict\"}");
    try expectParseError(Sample, "{\"count\":null,\"ratio\":0.5,\"mode\":\"strict\"}");
}

test "rejects trailing content and malformed documents" {
    try expectParseError(Sample, "{\"count\":3,\"ratio\":0.5,\"mode\":\"strict\"} {}");
    try expectParseError(Sample, "{\"count\":3,\"ratio\":0.5,\"mode\":\"strict\",}");
    try expectParseError(Sample, "{\"count\":3,\"ratio\":0.5,\"mode\":\"strict\"");
}

test "rejects out-of-range integers for the target type" {
    try expectParseError(Sample, "{\"count\":4294967296,\"ratio\":0.5,\"mode\":\"strict\"}");
    try expectParseError(Sample, "{\"count\":-1,\"ratio\":0.5,\"mode\":\"strict\"}");
}

test "rejects non-JSON number grammar" {
    const bad = [_][]const u8{ "NaN", "Infinity", "-Infinity", "0x10", "+1", "01", ".5", "1." };
    for (bad) |n| {
        var buf: [96]u8 = undefined;
        const text = try std.fmt.bufPrint(&buf, "{{\"count\":3,\"ratio\":{s},\"mode\":\"strict\"}}", .{n});
        try expectParseError(Sample, text);
    }
}

// --- Lenient behaviors: the strict layer must reject these (DAT-005, DAT-008). ---

test "lenient: float-formatted integral numbers are accepted into integer fields" {
    const p = try parse(Sample, "{\"count\":3.0,\"ratio\":0.5,\"mode\":\"strict\"}");
    defer p.deinit();
    try testing.expectEqual(@as(u32, 3), p.value.count);
    const q = try parse(Sample, "{\"count\":3e0,\"ratio\":0.5,\"mode\":\"strict\"}");
    defer q.deinit();
    try testing.expectEqual(@as(u32, 3), q.value.count);
}

test "lenient: enum fields accept bare integer tag values" {
    const p = try parse(Sample, "{\"count\":3,\"ratio\":0.5,\"mode\":1}");
    defer p.deinit();
    try testing.expectEqual(.loose, p.value.mode);
}

test "lenient: decimal overflow becomes infinity in float fields" {
    const p = try parse(Sample, "{\"count\":3,\"ratio\":1e400,\"mode\":\"strict\"}");
    defer p.deinit();
    try testing.expect(std.math.isPositiveInf(p.value.ratio));
}

test "lenient: integers above 2^53 are accepted into wide integer fields" {
    const Wide = struct { tick: u64 };
    const p = try parse(Wide, "{\"tick\":9007199254740993}");
    defer p.deinit();
    try testing.expectEqual(@as(u64, 9007199254740993), p.value.tick);
}

test "lenient: numeric strings are accepted into number fields" {
    const p = try parse(Sample, "{\"count\":\"3\",\"ratio\":\"0.5\",\"mode\":\"strict\"}");
    defer p.deinit();
    try testing.expectEqual(@as(u32, 3), p.value.count);
    try testing.expectEqual(@as(f64, 0.5), p.value.ratio);
}

test "lenient: non-finite spellings inside strings are accepted into float fields" {
    const p = try parse(Sample, "{\"count\":3,\"ratio\":\"nan\",\"mode\":\"strict\"}");
    defer p.deinit();
    try testing.expect(std.math.isNan(p.value.ratio));
    const q = try parse(Sample, "{\"count\":3,\"ratio\":\"-inf\",\"mode\":\"strict\"}");
    defer q.deinit();
    try testing.expect(std.math.isNegativeInf(q.value.ratio));
}

test "lenient: integer literals are accepted into float fields" {
    const p = try parse(Sample, "{\"count\":3,\"ratio\":1,\"mode\":\"strict\"}");
    defer p.deinit();
    try testing.expectEqual(@as(f64, 1.0), p.value.ratio);
}
