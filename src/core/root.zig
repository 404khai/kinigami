//! Kinigami simulation core. Zig standard library only (Q42, BLD-002).

pub const identity = @import("identity.zig");
pub const time = @import("time.zig");
pub const scheduler = @import("scheduler.zig");
pub const rng = @import("rng.zig");
pub const strict_json = @import("strict_json.zig");

test {
    _ = identity;
    _ = time;
    _ = scheduler;
    _ = rng;
    _ = strict_json;
}
