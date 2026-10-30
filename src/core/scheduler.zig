//! Deterministic event scheduler (Q43, TIM-004).
//!
//! Events are totally ordered by `(tick, phase, source_id, sequence)`:
//!
//! - `phase` is a caller-supplied enum whose integer values define the order
//!   of phases within a tick. The concrete phase list and its order are still
//!   an open decision, so this module is generic over it.
//! - `sequence` is assigned per source in the order that source schedules its
//!   events, so it reflects the source's own declared emission order. Events
//!   from different sources never depend on insertion order.
//!
//! Scheduling fails closed: an event may not be placed before the last event
//! already delivered, so delivered order can never be violated retroactively.

const std = @import("std");
const time = @import("time.zig");

pub const Error = error{ EventBeforeCursor, SequenceExhausted, OutOfMemory };

pub fn Scheduler(comptime Phase: type, comptime Payload: type) type {
    if (@typeInfo(Phase) != .@"enum") @compileError("Phase must be an enum whose values define phase order");

    return struct {
        const Self = @This();

        pub const Key = struct {
            tick: u64,
            phase: Phase,
            source_id: u64,
            sequence: u64,

            pub fn order(a: Key, b: Key) std.math.Order {
                if (a.tick != b.tick) return std.math.order(a.tick, b.tick);
                const pa = @intFromEnum(a.phase);
                const pb = @intFromEnum(b.phase);
                if (pa != pb) return std.math.order(pa, pb);
                if (a.source_id != b.source_id) return std.math.order(a.source_id, b.source_id);
                return std.math.order(a.sequence, b.sequence);
            }
        };

        pub const Event = struct {
            key: Key,
            payload: Payload,

            pub fn at(self: Event) time.Instant {
                return .{ .ticks = self.key.tick };
            }
        };

        fn compare(_: void, a: Event, b: Event) std.math.Order {
            return Key.order(a.key, b.key);
        }

        queue: std.PriorityQueue(Event, void, compare) = .empty,
        next_sequence: std.AutoHashMapUnmanaged(u64, u64) = .empty,
        cursor: ?Key = null,

        pub const empty: Self = .{};

        pub fn deinit(self: *Self, gpa: std.mem.Allocator) void {
            self.queue.deinit(gpa);
            self.next_sequence.deinit(gpa);
            self.* = undefined;
        }

        /// Schedules `payload` from `source_id` at `at` in `phase`.
        /// Returns the event's full ordering key, for recording.
        pub fn schedule(self: *Self, gpa: std.mem.Allocator, at: time.Instant, phase: Phase, source_id: u64, payload: Payload) Error!Key {
            const gop = try self.next_sequence.getOrPut(gpa, source_id);
            if (!gop.found_existing) gop.value_ptr.* = 0;
            const sequence = gop.value_ptr.*;
            const key: Key = .{ .tick = at.ticks, .phase = phase, .source_id = source_id, .sequence = sequence };
            if (self.cursor) |c| if (Key.order(key, c) != .gt) return error.EventBeforeCursor;
            try self.queue.push(gpa, .{ .key = key, .payload = payload });
            gop.value_ptr.* = std.math.add(u64, sequence, 1) catch return error.SequenceExhausted;
            return key;
        }

        /// Removes and returns the next event in total order.
        pub fn next(self: *Self) ?Event {
            const ev = self.queue.pop() orelse return null;
            self.cursor = ev.key;
            return ev;
        }

        /// The time of the next pending event, without removing it.
        pub fn peekTime(self: *const Self) ?time.Instant {
            const ev = self.queue.peek() orelse return null;
            return ev.at();
        }

        pub fn pending(self: *const Self) usize {
            return self.queue.count();
        }
    };
}

const testing = std.testing;

// Test-only phase list. The real phase order is an open decision.
const TestPhase = enum(u8) { first, second, third };
const TestScheduler = Scheduler(TestPhase, u32);

test "orders by tick, then phase, then source, then per-source sequence" {
    const gpa = testing.allocator;
    var s: TestScheduler = .empty;
    defer s.deinit(gpa);
    _ = try s.schedule(gpa, .{ .ticks = 5 }, .first, 1, 50);
    _ = try s.schedule(gpa, .{ .ticks = 2 }, .third, 9, 23);
    _ = try s.schedule(gpa, .{ .ticks = 2 }, .first, 9, 21);
    _ = try s.schedule(gpa, .{ .ticks = 2 }, .first, 3, 20);
    _ = try s.schedule(gpa, .{ .ticks = 2 }, .third, 9, 24); // same source, later sequence
    const expected = [_]u32{ 20, 21, 23, 24, 50 };
    for (expected) |want| try testing.expectEqual(want, s.next().?.payload);
    try testing.expectEqual(@as(?TestScheduler.Event, null), s.next());
}

test "delivery order is independent of the insertion order of different sources" {
    const gpa = testing.allocator;
    const Spec = struct { tick: u64, phase: TestPhase, source: u64 };
    const specs = [_]Spec{
        .{ .tick = 7, .phase = .second, .source = 4 }, .{ .tick = 7, .phase = .second, .source = 2 },
        .{ .tick = 7, .phase = .first, .source = 8 },  .{ .tick = 1, .phase = .third, .source = 4 },
        .{ .tick = 3, .phase = .first, .source = 1 },  .{ .tick = 7, .phase = .third, .source = 0 },
    };
    // Sequence numbers are per source and follow that source's emission
    // order, so compare which events are delivered, not their raw keys.
    // (Source 4's two events are at different ticks, so their relative
    // order does not depend on emission order.)
    const expected = [_]u32{ 3, 4, 2, 1, 0, 5 };
    var order: [specs.len]usize = .{ 0, 1, 2, 3, 4, 5 };
    // Deterministic shuffles from a fixed test-only seed (not simulation RNG).
    var prng = std.Random.DefaultPrng.init(0x4b494e);
    for (0..50) |round| {
        if (round > 0) prng.random().shuffle(usize, &order);
        var s: TestScheduler = .empty;
        defer s.deinit(gpa);
        for (order) |i| _ = try s.schedule(gpa, .{ .ticks = specs[i].tick }, specs[i].phase, specs[i].source, @intCast(i));
        var got: [specs.len]u32 = undefined;
        for (&got) |*p| p.* = s.next().?.payload;
        try testing.expectEqualSlices(u32, &expected, &got);
    }
}

test "scheduling before the delivery cursor fails closed" {
    const gpa = testing.allocator;
    var s: TestScheduler = .empty;
    defer s.deinit(gpa);
    _ = try s.schedule(gpa, .{ .ticks = 10 }, .second, 5, 0);
    _ = s.next();
    try testing.expectError(error.EventBeforeCursor, s.schedule(gpa, .{ .ticks = 9 }, .third, 5, 1));
    try testing.expectError(error.EventBeforeCursor, s.schedule(gpa, .{ .ticks = 10 }, .first, 5, 1));
    try testing.expectError(error.EventBeforeCursor, s.schedule(gpa, .{ .ticks = 10 }, .second, 4, 1));
    // Same tick and phase, later in total order: allowed.
    _ = try s.schedule(gpa, .{ .ticks = 10 }, .second, 6, 2);
    _ = try s.schedule(gpa, .{ .ticks = 10 }, .third, 0, 3);
    try testing.expectEqual(@as(u32, 2), s.next().?.payload);
    try testing.expectEqual(@as(u32, 3), s.next().?.payload);
}

test "rejected schedule does not consume a sequence number" {
    const gpa = testing.allocator;
    var s: TestScheduler = .empty;
    defer s.deinit(gpa);
    _ = try s.schedule(gpa, .{ .ticks = 4 }, .first, 1, 0);
    _ = s.next();
    try testing.expectError(error.EventBeforeCursor, s.schedule(gpa, .{ .ticks = 3 }, .first, 1, 0));
    const k = try s.schedule(gpa, .{ .ticks = 5 }, .first, 1, 0);
    try testing.expectEqual(@as(u64, 1), k.sequence);
}
