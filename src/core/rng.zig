//! Seeded randomness interface (Q32, Q43, TIM-007).
//!
//! **Unresolved, deliberately not chosen here:** the generator algorithm, the
//! seed width, how independent streams are derived (per Kin, per sensor, per
//! channel), and how raw bits become floats or bounded integers. Those are
//! recorded decisions still to be made.
//!
//! What this module fixes now:
//! - Randomness reaches simulation code only through an explicit `Source`
//!   passed in by the caller; there is no ambient or global generator.
//! - Every source identifies its algorithm and seed so a run can record them
//!   (`Provenance`), and replay can reconstruct the identical stream.
//! - `expectDeterministic` is the conformance check any future algorithm must
//!   pass.

const std = @import("std");
const builtin = @import("builtin");

/// What a recording must store to reproduce a source exactly.
pub const Provenance = struct {
    /// Stable algorithm identifier, including its version.
    algorithm: []const u8,
    /// Exact seed bytes, as the algorithm consumes them.
    seed: []const u8,
};

pub const Source = struct {
    ptr: *anyopaque,
    vtable: *const VTable,

    pub const VTable = struct {
        nextU64: *const fn (ptr: *anyopaque) u64,
        provenance: *const fn (ptr: *anyopaque) Provenance,
    };

    pub fn nextU64(self: Source) u64 {
        return self.vtable.nextU64(self.ptr);
    }

    pub fn provenance(self: Source) Provenance {
        return self.vtable.provenance(self.ptr);
    }
};

/// Conformance check for any generator `G` with `init(seed: []const u8) G`
/// and `source(*G) Source`: identical seeds give identical streams, the
/// provenance round-trips the seed, and distinct seeds diverge within `n`
/// outputs.
pub fn expectDeterministic(comptime G: type, seed_a: []const u8, seed_b: []const u8, n: usize) !void {
    var a1 = G.init(seed_a);
    var a2 = G.init(seed_a);
    var b = G.init(seed_b);
    const s1 = a1.source();
    const s2 = a2.source();
    const sb = b.source();
    try std.testing.expectEqualSlices(u8, seed_a, s1.provenance().seed);
    var diverged = false;
    for (0..n) |_| {
        const x = s1.nextU64();
        try std.testing.expectEqual(x, s2.nextU64());
        if (x != sb.nextU64()) diverged = true;
    }
    try std.testing.expect(diverged);
}

/// Test-only stand-in that exercises the interface. It is **not** random
/// and can never be selected for simulation runs.
pub const TestCounter = struct {
    seed: [8]u8,
    state: u64,

    comptime {
        if (!builtin.is_test) @compileError("rng.TestCounter is test-only");
    }

    pub fn init(seed: []const u8) TestCounter {
        var s: [8]u8 = @splat(0);
        @memcpy(s[0..@min(8, seed.len)], seed[0..@min(8, seed.len)]);
        return .{ .seed = s, .state = std.mem.readInt(u64, &s, .little) };
    }

    pub fn source(self: *TestCounter) Source {
        return .{ .ptr = self, .vtable = &.{ .nextU64 = next, .provenance = prov } };
    }

    fn next(ptr: *anyopaque) u64 {
        const self: *TestCounter = @ptrCast(@alignCast(ptr));
        self.state +%= 1;
        return self.state;
    }

    fn prov(ptr: *anyopaque) Provenance {
        const self: *TestCounter = @ptrCast(@alignCast(ptr));
        return .{ .algorithm = "test-counter-v0", .seed = &self.seed };
    }
};

test "interface wiring and conformance harness" {
    try expectDeterministic(TestCounter, &.{ 1, 0, 0, 0, 0, 0, 0, 0 }, &.{ 2, 0, 0, 0, 0, 0, 0, 0 }, 16);
    var c = TestCounter.init(&.{ 5, 0, 0, 0, 0, 0, 0, 0 });
    try std.testing.expectEqualStrings("test-counter-v0", c.source().provenance().algorithm);
}
