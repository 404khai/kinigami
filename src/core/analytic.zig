//! Closed-form references for the analytic fixture-validation cases
//! (Q46, Q47, Q48). Pure functions of declared parameters: no solver, no
//! state. Each documents the assumptions under which it is exact.

const std = @import("std");

/// Uniform solid cuboid with edge lengths `size` (x, y, z). Principal
/// moments of inertia about its centre of mass.
pub fn cuboidInertia(mass_kg: f64, size_m: [3]f64) [3]f64 {
    const x2 = size_m[0] * size_m[0];
    const y2 = size_m[1] * size_m[1];
    const z2 = size_m[2] * size_m[2];
    return .{ mass_kg * (y2 + z2) / 12.0, mass_kg * (x2 + z2) / 12.0, mass_kg * (x2 + y2) / 12.0 };
}

/// Rest: total normal force equals weight.
pub fn weight(mass_kg: f64, g: f64) f64 {
    return mass_kg * g;
}

/// Free fall from rest, before contact: downward speed and distance after `t`.
pub fn freeFallSpeed(g: f64, t: f64) f64 {
    return g * t;
}
pub fn freeFallDistance(g: f64, t: f64) f64 {
    return 0.5 * g * t * t;
}
/// Time to fall `clearance` from rest.
pub fn freeFallContactTime(g: f64, clearance_m: f64) f64 {
    return @sqrt(2.0 * clearance_m / g);
}

/// Coulomb static threshold for a horizontal push on a body resting on a
/// horizontal plane: sliding starts above μs·m·g.
pub fn slidingThreshold(mass_kg: f64, g: f64, mu_s: f64) f64 {
    return mu_s * mass_kg * g;
}

/// Horizontal acceleration while sliding under push `force_n` (> threshold).
pub fn slidingAcceleration(mass_kg: f64, g: f64, mu_k: f64, force_n: f64) f64 {
    return (force_n - mu_k * mass_kg * g) / mass_kg;
}

/// Sliding to a stop from initial speed `v0` with no applied load.
pub fn stopTime(g: f64, mu_k: f64, v0: f64) f64 {
    return v0 / (mu_k * g);
}
pub fn stopDistance(g: f64, mu_k: f64, v0: f64) f64 {
    return v0 * v0 / (2.0 * mu_k * g);
}

/// Horizontal push at height `h` above the base that just balances the
/// gravity moment about the far bottom edge, for a body whose centre of mass
/// is horizontally `arm` from that edge. Exact for a sharp-edged support
/// when friction is sufficient to prevent sliding first.
pub fn tippingThreshold(mass_kg: f64, g: f64, arm_m: f64, h_m: f64) f64 {
    return mass_kg * g * arm_m / h_m;
}

const testing = std.testing;
const eps = 1e-12;

test "cuboid inertia" {
    const i = cuboidInertia(0.040, .{ 0.040, 0.040, 0.020 });
    try testing.expectApproxEqRel(@as(f64, 0.040 * (0.0016 + 0.0004) / 12.0), i[0], eps);
    try testing.expectApproxEqRel(@as(f64, 0.040 * 0.0032 / 12.0), i[2], eps);
}

test "stopping kinematics agree with constant deceleration" {
    const g = 9.80665;
    const t = stopTime(g, 0.2, 0.5);
    const d = stopDistance(g, 0.2, 0.5);
    try testing.expectApproxEqRel(0.5 * t - 0.5 * 0.2 * g * t * t, d, eps);
}

test "tipping threshold for the tall fixture is one fifth of its weight" {
    const g = 9.80665;
    try testing.expectApproxEqRel(0.2 * 0.030 * g, tippingThreshold(0.030, g, 0.010, 0.050), eps);
}
