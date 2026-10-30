//! Kinigami simulation core. Zig standard library only (Q42, BLD-002).

pub const identity = @import("identity.zig");
pub const time = @import("time.zig");
pub const scheduler = @import("scheduler.zig");

test {
    _ = identity;
    _ = time;
    _ = scheduler;
}
