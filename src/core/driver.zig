//! Fixed-step run driver (Q43, Q45, TIM-008, INS-007).
//!
//! Advances a backend through fixed physics steps on the integer clock and
//! produces a checkpoint state hash after every step. An optional publisher
//! receives the canonical state bytes; it has no path back into the run.
//!
//! Sensors, controllers, messages, and validation-force timing are not
//! driven here yet: their scheduling semantics depend on the still-open
//! event-phase order.

const std = @import("std");
const time = @import("time.zig");
const canonical = @import("canonical.zig");
const backend_mod = @import("backend.zig");
const snapshot = @import("snapshot.zig");

pub const Checkpoint = struct {
    tick: u64,
    state_sha256: [32]u8,
};

pub const Options = struct {
    unit: time.TimeUnit,
    step: time.PhysicsStep,
    steps: u64,
    publisher: ?snapshot.Publisher = null,
};

pub const Error = backend_mod.StepError || backend_mod.EncodeError || time.Error;

/// Domain tag prefixed to every checkpoint hash, versioned with the encoding.
pub const checkpoint_domain = "kinigami.checkpoint.v1";

pub fn run(gpa: std.mem.Allocator, b: backend_mod.Backend, opts: Options, out: []Checkpoint) Error!void {
    std.debug.assert(out.len == opts.steps);
    try opts.unit.validate();
    const dt_s = opts.unit.seconds(opts.step.step);
    var now: time.Instant = .zero;
    var buf: canonical.BufferSink = .{ .gpa = gpa };
    defer buf.deinit();

    for (out) |*cp| {
        try b.step(dt_s, .{});
        now = try now.add(opts.step.step);

        // One canonical encoding per checkpoint: the hash is over exactly the
        // bytes that are published, so a viewer sees what was hashed.
        buf.list.clearRetainingCapacity();
        const e = buf.encoder();
        try e.bytes(checkpoint_domain);
        try e.int(u64, now.ticks);
        const id = b.identity();
        try e.bytes(id.name);
        try e.bytes(id.version);
        try b.encodeState(e);

        var digest: [32]u8 = undefined;
        std.crypto.hash.sha2.Sha256.hash(buf.list.items, &digest, .{});
        cp.* = .{ .tick = now.ticks, .state_sha256 = digest };

        if (opts.publisher) |p| p.publish(now.ticks, buf.list.items);
    }
}

// --- Tests with a test-only stand-in backend (not physics). ---

const Stand = struct {
    x: f64 = 0,
    v: f64 = 1,

    comptime {
        if (!@import("builtin").is_test) @compileError("driver.Stand is test-only");
    }

    fn backend(self: *Stand) backend_mod.Backend {
        return .{ .ptr = self, .vtable = &.{ .identity = ident, .step = stepFn, .encodeState = enc, .contacts = noContacts } };
    }
    fn ident(_: *anyopaque) backend_mod.Identity {
        return .{ .name = "test-stand", .version = "0" };
    }
    fn stepFn(ptr: *anyopaque, dt: f64, _: backend_mod.StepInputs) backend_mod.StepError!void {
        const s: *Stand = @ptrCast(@alignCast(ptr));
        s.v -= 0.1 * s.x * dt;
        s.x += s.v * dt;
    }
    fn enc(ptr: *anyopaque, e: canonical.BufferEncoder) backend_mod.EncodeError!void {
        const s: *Stand = @ptrCast(@alignCast(ptr));
        try e.float(s.x);
        try e.float(s.v);
    }
    fn noContacts(_: *anyopaque) []const backend_mod.ContactReport {
        return &.{};
    }
};

const test_opts: Options = .{
    .unit = .{ .numerator = 1, .denominator = 1000 },
    .step = .{ .step = .{ .ticks = 10 } },
    .steps = 64,
};

test "replay reproduces every checkpoint hash" {
    var a: [64]Checkpoint = undefined;
    var b: [64]Checkpoint = undefined;
    var s1: Stand = .{};
    var s2: Stand = .{};
    try run(std.testing.allocator, s1.backend(), test_opts, &a);
    try run(std.testing.allocator, s2.backend(), test_opts, &b);
    try std.testing.expectEqualSlices(Checkpoint, &a, &b);
    try std.testing.expectEqual(@as(u64, 640), a[63].tick);
}

test "capture isolation: live publication does not change checkpoint hashes (INS-007)" {
    var ring = try snapshot.BoundedRing.init(std.testing.allocator, 4, 256);
    defer ring.deinit(std.testing.allocator);
    var with: [64]Checkpoint = undefined;
    var without: [64]Checkpoint = undefined;
    var s1: Stand = .{};
    var s2: Stand = .{};
    var opts = test_opts;
    opts.publisher = ring.publisher();
    try run(std.testing.allocator, s1.backend(), opts, &with);
    try run(std.testing.allocator, s2.backend(), test_opts, &without);
    try std.testing.expectEqualSlices(Checkpoint, &without, &with);
    try std.testing.expectEqual(@as(u64, 64), ring.published);
    try std.testing.expectEqual(@as(u64, 60), ring.dropped);
    // The newest retained snapshot hashes to the matching checkpoint.
    var last: ?@TypeOf(ring.take().?) = null;
    while (ring.take()) |snap| last = snap;
    var digest: [32]u8 = undefined;
    std.crypto.hash.sha2.Sha256.hash(last.?.bytes, &digest, .{});
    try std.testing.expectEqual(with[63].tick, last.?.tick);
    try std.testing.expectEqualSlices(u8, &with[63].state_sha256, &digest);
}

test "a different initial state gives different checkpoint hashes" {
    var a: [64]Checkpoint = undefined;
    var b: [64]Checkpoint = undefined;
    var s1: Stand = .{};
    var s2: Stand = .{ .v = 1.0000000000000002 };
    try run(std.testing.allocator, s1.backend(), test_opts, &a);
    try run(std.testing.allocator, s2.backend(), test_opts, &b);
    try std.testing.expect(!std.mem.eql(u8, &a[0].state_sha256, &b[0].state_sha256));
}
