//! Minimal 3D vector and quaternion math in binary64, SI units.
//! Operations are written out explicitly (no SIMD, no implicit fusion) so
//! results depend only on IEEE-754 semantics under the acceptance profile.

const std = @import("std");

pub const Vec3 = [3]f64;

pub const zero: Vec3 = .{ 0, 0, 0 };

pub fn add(a: Vec3, b: Vec3) Vec3 {
    return .{ a[0] + b[0], a[1] + b[1], a[2] + b[2] };
}
pub fn sub(a: Vec3, b: Vec3) Vec3 {
    return .{ a[0] - b[0], a[1] - b[1], a[2] - b[2] };
}
pub fn scale(a: Vec3, s: f64) Vec3 {
    return .{ a[0] * s, a[1] * s, a[2] * s };
}
pub fn dot(a: Vec3, b: Vec3) f64 {
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
}
pub fn cross(a: Vec3, b: Vec3) Vec3 {
    return .{ a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0] };
}
pub fn length(a: Vec3) f64 {
    return @sqrt(dot(a, a));
}
pub fn horizontalLength(a: Vec3) f64 {
    return @sqrt(a[0] * a[0] + a[1] * a[1]);
}

/// Unit quaternion (w, x, y, z) for body-to-world rotation.
pub const Quat = struct {
    w: f64,
    x: f64,
    y: f64,
    z: f64,

    pub const identity: Quat = .{ .w = 1, .x = 0, .y = 0, .z = 0 };

    pub fn mul(a: Quat, b: Quat) Quat {
        return .{
            .w = a.w * b.w - a.x * b.x - a.y * b.y - a.z * b.z,
            .x = a.w * b.x + a.x * b.w + a.y * b.z - a.z * b.y,
            .y = a.w * b.y - a.x * b.z + a.y * b.w + a.z * b.x,
            .z = a.w * b.z + a.x * b.y - a.y * b.x + a.z * b.w,
        };
    }

    pub fn normalized(q: Quat) Quat {
        const n = @sqrt(q.w * q.w + q.x * q.x + q.y * q.y + q.z * q.z);
        return .{ .w = q.w / n, .x = q.x / n, .y = q.y / n, .z = q.z / n };
    }

    /// Rotates body-frame vector `v` into the world frame.
    pub fn rotate(q: Quat, v: Vec3) Vec3 {
        const u: Vec3 = .{ q.x, q.y, q.z };
        const t = scale(cross(u, v), 2.0);
        return add(add(v, scale(t, q.w)), cross(u, t));
    }

    /// Rotates world-frame vector `v` into the body frame.
    pub fn rotateInverse(q: Quat, v: Vec3) Vec3 {
        return (Quat{ .w = q.w, .x = -q.x, .y = -q.y, .z = -q.z }).rotate(v);
    }

    /// First-order integration of world angular velocity `omega` over `h`,
    /// followed by renormalization.
    pub fn integrate(q: Quat, omega: Vec3, h: f64) Quat {
        const dq = (Quat{ .w = 0, .x = omega[0], .y = omega[1], .z = omega[2] }).mul(q);
        return (Quat{
            .w = q.w + 0.5 * h * dq.w,
            .x = q.x + 0.5 * h * dq.x,
            .y = q.y + 0.5 * h * dq.y,
            .z = q.z + 0.5 * h * dq.z,
        }).normalized();
    }

    /// Rotation angle (radians) of this unit quaternion, in [0, π].
    pub fn angle(q: Quat) f64 {
        const s = @sqrt(q.x * q.x + q.y * q.y + q.z * q.z);
        return 2.0 * std.math.atan2(s, @abs(q.w));
    }

    /// Relative rotation taking `from` to `self`: self * conj(from).
    pub fn relativeTo(q: Quat, from: Quat) Quat {
        return q.mul(.{ .w = from.w, .x = -from.x, .y = -from.y, .z = -from.z });
    }
};

/// Angle between the body z axis and world +z (tilt from upright).
pub fn tilt(q: Quat) f64 {
    const z = q.rotate(.{ 0, 0, 1 });
    return std.math.atan2(horizontalLength(z), z[2]);
}

const testing = std.testing;

test "rotation round trip and quarter turn" {
    const s = @sqrt(0.5);
    const q: Quat = .{ .w = s, .x = 0, .y = 0, .z = s }; // 90° about z
    const v = q.rotate(.{ 1, 0, 0 });
    try testing.expectApproxEqAbs(@as(f64, 0), v[0], 1e-15);
    try testing.expectApproxEqAbs(@as(f64, 1), v[1], 1e-15);
    const back = q.rotateInverse(v);
    try testing.expectApproxEqAbs(@as(f64, 1), back[0], 1e-15);
    try testing.expectApproxEqAbs(std.math.pi / 2.0, q.angle(), 1e-15);
}

test "tilt of a rotation about y" {
    const a: f64 = 0.3;
    const q: Quat = .{ .w = @cos(a / 2), .x = 0, .y = @sin(a / 2), .z = 0 };
    try testing.expectApproxEqAbs(a, tilt(q), 1e-15);
}
