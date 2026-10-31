//! Kinigami simulation core. Zig standard library only (Q42, BLD-002).

pub const identity = @import("identity.zig");
pub const time = @import("time.zig");
pub const scheduler = @import("scheduler.zig");
pub const rng = @import("rng.zig");
pub const strict_json = @import("strict_json.zig");
pub const canonical = @import("canonical.zig");
pub const recording = @import("recording.zig");
pub const run = @import("run.zig");
pub const backend = @import("backend.zig");
pub const snapshot = @import("snapshot.zig");
pub const driver = @import("driver.zig");
pub const analytic = @import("analytic.zig");
pub const criteria = @import("criteria.zig");

test {
    _ = identity;
    _ = time;
    _ = scheduler;
    _ = rng;
    _ = strict_json;
    _ = canonical;
    _ = recording;
    _ = run;
    _ = backend;
    _ = snapshot;
    _ = driver;
    _ = analytic;
    _ = criteria;
}
