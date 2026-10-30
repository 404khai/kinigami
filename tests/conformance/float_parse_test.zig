//! Decimal-to-binary64 conversion must round to nearest, ties to even
//! (DAT-009). Checked bit-exactly, including halfway cases that need the
//! slow (big-decimal) path, subnormals, and overflow.

const std = @import("std");
const testing = std.testing;

fn bits(text: []const u8) !u64 {
    return @bitCast(try std.fmt.parseFloat(f64, text));
}

fn expectBits(expected: u64, text: []const u8) !void {
    const actual = try bits(text);
    if (actual != expected) {
        std.debug.print("parseFloat(\"{s}\") = 0x{x:0>16}, expected 0x{x:0>16}\n", .{ text, actual, expected });
        return error.TestExpectedEqual;
    }
}

test "common values" {
    try expectBits(0x3FB999999999999A, "0.1");
    try expectBits(0x3FF0000000000000, "1");
    try expectBits(0x8000000000000000, "-0.0");
    try expectBits(0x4009_21FB_5444_2D18, "3.141592653589793");
}

test "integer halfway cases round to even" {
    // 2^53 + 1 lies halfway between 2^53 and 2^53 + 2.
    try expectBits(0x4340000000000000, "9007199254740993");
    // 2^53 + 3 lies halfway between 2^53 + 2 and 2^53 + 4; even is +4.
    try expectBits(0x4340000000000002, "9007199254740995");
}

test "long decimal exactly at and just above a halfway point" {
    // 1 + 2^-53 exactly: ties to even, giving 1.0.
    try expectBits(0x3FF0000000000000, "1.00000000000000011102230246251565404236316680908203125");
    // One unit in the last decimal place above halfway rounds up.
    try expectBits(0x3FF0000000000001, "1.00000000000000011102230246251565404236316680908203126");
    // One unit below halfway rounds down.
    try expectBits(0x3FF0000000000000, "1.00000000000000011102230246251565404236316680908203124");
}

test "subnormal boundary" {
    try expectBits(0x000FFFFFFFFFFFFF, "2.2250738585072011e-308");
    try expectBits(0x0010000000000000, "2.2250738585072012e-308");
    try expectBits(0x0000000000000001, "4.9406564584124654e-324");
    // Just below 2^-1075 (half the smallest subnormal) rounds to zero;
    // just above rounds to the smallest subnormal.
    try expectBits(0x0000000000000000, "2.4703282292062327e-324");
    try expectBits(0x0000000000000001, "2.4703282292062328e-324");
}

test "overflow boundary" {
    try expectBits(0x7FEFFFFFFFFFFFFF, "1.7976931348623157e308");
    try expectBits(0x7FF0000000000000, "1.7976931348623159e308");
}
