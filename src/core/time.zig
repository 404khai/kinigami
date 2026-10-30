//! Integer simulation time (Q43, TIM-001..003, TIM-011).
//!
//! Simulation time is an integer tick count. The physical length of one tick
//! (the time unit) is declared per experiment as an exact rational number of
//! seconds; this module does not choose it (TIM-012 is unresolved). All
//! arithmetic is checked: overflow is an error, never a silent wrap.

const std = @import("std");

pub const Error = error{ TimeOverflow, InvalidTimeUnit, InvalidPhysicsStep };

/// A point in simulated time, in ticks since the start of the run.
pub const Instant = struct {
    ticks: u64,

    pub const zero: Instant = .{ .ticks = 0 };

    pub fn add(self: Instant, d: Duration) Error!Instant {
        return .{ .ticks = std.math.add(u64, self.ticks, d.ticks) catch return error.TimeOverflow };
    }

    /// Duration from `earlier` to `self`. Errors if `earlier` is later.
    pub fn since(self: Instant, earlier: Instant) Error!Duration {
        return .{ .ticks = std.math.sub(u64, self.ticks, earlier.ticks) catch return error.TimeOverflow };
    }

    pub fn order(a: Instant, b: Instant) std.math.Order {
        return std.math.order(a.ticks, b.ticks);
    }
};

/// A span of simulated time, in ticks.
pub const Duration = struct {
    ticks: u64,

    pub const zero: Duration = .{ .ticks = 0 };

    pub fn add(a: Duration, b: Duration) Error!Duration {
        return .{ .ticks = std.math.add(u64, a.ticks, b.ticks) catch return error.TimeOverflow };
    }

    pub fn mul(self: Duration, n: u64) Error!Duration {
        return .{ .ticks = std.math.mul(u64, self.ticks, n) catch return error.TimeOverflow };
    }
};

/// Exact length of one tick: `numerator / denominator` seconds.
/// Declared per experiment and recorded with every run (TIM-011).
pub const TimeUnit = struct {
    numerator: u64,
    denominator: u64,

    pub fn validate(self: TimeUnit) Error!void {
        if (self.numerator == 0 or self.denominator == 0) return error.InvalidTimeUnit;
        if (std.math.gcd(self.numerator, self.denominator) != 1) return error.InvalidTimeUnit;
    }

    /// Seconds for a duration, for handing to physics as a binary64 value.
    /// Exact tick arithmetic stays in integers; only this conversion rounds.
    pub fn seconds(self: TimeUnit, d: Duration) f64 {
        const num: f64 = @floatFromInt(@as(u128, d.ticks) * self.numerator);
        const den: f64 = @floatFromInt(self.denominator);
        return num / den;
    }
};

/// The fixed physics timestep (Q43: fixed-step only in the initial slices).
/// Being a tick count, it is an integer multiple of the time unit by
/// construction (TIM-002). Its value is unresolved and supplied by the run
/// configuration.
pub const PhysicsStep = struct {
    step: Duration,

    pub fn init(step: Duration) Error!PhysicsStep {
        if (step.ticks == 0) return error.InvalidPhysicsStep;
        return .{ .step = step };
    }

    /// The boundary at or after `t`. Whether a command ready exactly at a
    /// boundary applies at that boundary is an event-phase ordering question
    /// (still open), not something this function decides.
    pub fn boundaryAtOrAfter(self: PhysicsStep, t: Instant) Error!Instant {
        const rem = t.ticks % self.step.ticks;
        if (rem == 0) return t;
        return t.add(.{ .ticks = self.step.ticks - rem });
    }

    /// The first boundary strictly after `t`.
    pub fn boundaryAfter(self: PhysicsStep, t: Instant) Error!Instant {
        const rem = t.ticks % self.step.ticks;
        return t.add(.{ .ticks = self.step.ticks - rem });
    }

    /// The most recent boundary at or before `t` (the last completed physics
    /// state a sensor sampling at `t` can observe, TIM-005).
    pub fn boundaryAtOrBefore(self: PhysicsStep, t: Instant) Instant {
        return .{ .ticks = t.ticks - t.ticks % self.step.ticks };
    }
};

const testing = std.testing;

test "checked arithmetic reports overflow instead of wrapping" {
    const near_end: Instant = .{ .ticks = std.math.maxInt(u64) - 1 };
    try testing.expectEqual(@as(u64, std.math.maxInt(u64)), (try near_end.add(.{ .ticks = 1 })).ticks);
    try testing.expectError(error.TimeOverflow, near_end.add(.{ .ticks = 2 }));
    try testing.expectError(error.TimeOverflow, (Duration{ .ticks = 1 << 63 }).mul(2));
    try testing.expectError(error.TimeOverflow, (Instant{ .ticks = 3 }).since(.{ .ticks = 4 }));
}

test "time unit must be a reduced positive rational" {
    try (TimeUnit{ .numerator = 1, .denominator = 1_000_000_000 }).validate();
    try testing.expectError(error.InvalidTimeUnit, (TimeUnit{ .numerator = 0, .denominator = 1 }).validate());
    try testing.expectError(error.InvalidTimeUnit, (TimeUnit{ .numerator = 1, .denominator = 0 }).validate());
    try testing.expectError(error.InvalidTimeUnit, (TimeUnit{ .numerator = 2, .denominator = 4 }).validate());
}

test "seconds conversion is exact where representable" {
    const unit: TimeUnit = .{ .numerator = 1, .denominator = 1024 };
    try testing.expectEqual(@as(f64, 0.5), unit.seconds(.{ .ticks = 512 }));
}

test "physics boundaries" {
    const p = try PhysicsStep.init(.{ .ticks = 10 });
    try testing.expectEqual(@as(u64, 20), (try p.boundaryAtOrAfter(.{ .ticks = 20 })).ticks);
    try testing.expectEqual(@as(u64, 30), (try p.boundaryAtOrAfter(.{ .ticks = 21 })).ticks);
    try testing.expectEqual(@as(u64, 30), (try p.boundaryAfter(.{ .ticks = 20 })).ticks);
    try testing.expectEqual(@as(u64, 20), p.boundaryAtOrBefore(.{ .ticks = 29 }).ticks);
    try testing.expectError(error.InvalidPhysicsStep, PhysicsStep.init(.zero));
    try testing.expectError(error.TimeOverflow, p.boundaryAfter(.{ .ticks = std.math.maxInt(u64) - 3 }));
}
