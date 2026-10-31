//! Fused-operation policy (Q42, BLD-004): the compiler must not contract
//! `a * b + c` into a fused multiply-add on its own. FMA happens only through
//! explicit `@mulAdd`. This test runs under every optimize mode.

const std = @import("std");
const testing = std.testing;

// a * b = 1 - 2^-60 exactly, which rounds to 1.0 in binary64. Unfused,
// a * b + c is therefore 0; fused, it is -2^-60.
const a_init: f64 = 1.0 + 0x1p-30;
const b_init: f64 = 1.0 - 0x1p-30;
const c_init: f64 = -1.0;

fn mulThenAdd(a: f64, b: f64, c: f64) f64 {
    return a * b + c;
}

test "a * b + c is not implicitly fused" {
    var a: f64 = a_init;
    var b: f64 = b_init;
    var c: f64 = c_init;
    std.mem.doNotOptimizeAway(&a);
    std.mem.doNotOptimizeAway(&b);
    std.mem.doNotOptimizeAway(&c);
    try testing.expectEqual(@as(u64, 0), @as(u64, @bitCast(mulThenAdd(a, b, c))));
}

test "explicit @mulAdd is fused" {
    var a: f64 = a_init;
    var b: f64 = b_init;
    var c: f64 = c_init;
    std.mem.doNotOptimizeAway(&a);
    std.mem.doNotOptimizeAway(&b);
    std.mem.doNotOptimizeAway(&c);
    try testing.expectEqual(-0x1p-60, @mulAdd(f64, a, b, c));
}
