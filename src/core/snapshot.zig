//! Live snapshot publication boundary (Q45, INS-006, INS-007).
//!
//! The simulation hands immutable snapshot bytes to a `Publisher`. Publishing
//! can never block, fail into the simulation, draw from the simulation RNG,
//! or schedule events: the call returns nothing and has no inputs other than
//! the bytes. Whether anything is listening cannot change simulated results.
//!
//! `BoundedRing` is a preallocated, fixed-capacity store with dropped-frame
//! accounting. When full, it drops the **oldest** snapshot so a live viewer
//! sees the freshest state. Transport to the separate inspector process is
//! not built yet; it will consume this ring.

const std = @import("std");

pub const Publisher = struct {
    ptr: *anyopaque,
    publishFn: *const fn (ptr: *anyopaque, tick: u64, bytes: []const u8) void,

    pub fn publish(self: Publisher, tick: u64, bytes: []const u8) void {
        self.publishFn(self.ptr, tick, bytes);
    }
};

pub const BoundedRing = struct {
    slots: []Slot,
    storage: []u8,
    slot_capacity: usize,
    head: usize = 0,
    len: usize = 0,
    published: u64 = 0,
    dropped: u64 = 0,
    oversized: u64 = 0,

    pub const Slot = struct { tick: u64, len: usize };

    /// Allocates everything up front; publishing never allocates.
    pub fn init(gpa: std.mem.Allocator, slot_count: usize, slot_capacity: usize) error{OutOfMemory}!BoundedRing {
        std.debug.assert(slot_count > 0);
        const slots = try gpa.alloc(Slot, slot_count);
        errdefer gpa.free(slots);
        const storage = try gpa.alloc(u8, slot_count * slot_capacity);
        return .{ .slots = slots, .storage = storage, .slot_capacity = slot_capacity };
    }

    pub fn deinit(self: *BoundedRing, gpa: std.mem.Allocator) void {
        gpa.free(self.slots);
        gpa.free(self.storage);
    }

    pub fn publisher(self: *BoundedRing) Publisher {
        return .{ .ptr = self, .publishFn = publishImpl };
    }

    fn publishImpl(ptr: *anyopaque, tick: u64, bytes: []const u8) void {
        const self: *BoundedRing = @ptrCast(@alignCast(ptr));
        if (bytes.len > self.slot_capacity) {
            self.oversized += 1;
            return;
        }
        if (self.len == self.slots.len) {
            self.head = (self.head + 1) % self.slots.len;
            self.len -= 1;
            self.dropped += 1;
        }
        const i = (self.head + self.len) % self.slots.len;
        self.slots[i] = .{ .tick = tick, .len = bytes.len };
        @memcpy(self.storage[i * self.slot_capacity ..][0..bytes.len], bytes);
        self.len += 1;
        self.published += 1;
    }

    /// Consumer side: oldest retained snapshot, or null.
    pub fn take(self: *BoundedRing) ?struct { tick: u64, bytes: []const u8 } {
        if (self.len == 0) return null;
        const i = self.head;
        self.head = (self.head + 1) % self.slots.len;
        self.len -= 1;
        return .{ .tick = self.slots[i].tick, .bytes = self.storage[i * self.slot_capacity ..][0..self.slots[i].len] };
    }
};

test "full ring drops the oldest and counts it" {
    var ring = try BoundedRing.init(std.testing.allocator, 2, 4);
    defer ring.deinit(std.testing.allocator);
    const p = ring.publisher();
    p.publish(1, "a");
    p.publish(2, "b");
    p.publish(3, "c");
    p.publish(4, "toolong");
    try std.testing.expectEqual(@as(u64, 1), ring.dropped);
    try std.testing.expectEqual(@as(u64, 1), ring.oversized);
    try std.testing.expectEqual(@as(u64, 2), ring.take().?.tick);
    const last = ring.take().?;
    try std.testing.expectEqual(@as(u64, 3), last.tick);
    try std.testing.expectEqualStrings("c", last.bytes);
    try std.testing.expect(ring.take() == null);
}
