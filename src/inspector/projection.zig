//! Orbit camera and perspective projection for the wireframe 3D view (Q50).
//! Presentation-only math: it never feeds back into simulation or recorded
//! data. World frame: z up, tabletop at z = 0 (Q21), SI units.

const std = @import("std");

pub const Vec3 = [3]f64;
pub const Point2 = struct { x: f64, y: f64 };

pub const Camera = struct {
    /// Point the camera orbits and looks at (metres, world frame).
    target: Vec3 = .{ 0, 0, 0.01 },
    /// Horizontal angle around world z, radians (0 looks along +y).
    yaw: f64 = -0.6,
    /// Elevation above the tabletop plane, radians (0 = level, π/2 = top-down).
    pitch: f64 = 0.45,
    /// Distance from target, metres.
    distance: f64 = 0.25,
    /// Vertical field of view, radians.
    fov_y: f64 = 0.7,
    /// Points closer than this along the view axis are not drawn.
    near: f64 = 0.005,

    fn basis(self: Camera) struct { eye: Vec3, fwd: Vec3, right: Vec3, up: Vec3 } {
        const cp = @cos(self.pitch);
        const back: Vec3 = .{ -@sin(self.yaw) * cp, -@cos(self.yaw) * cp, @sin(self.pitch) };
        const eye = add(self.target, scale(back, self.distance));
        const fwd = scale(back, -1);
        const right = normalize(cross(fwd, .{ 0, 0, 1 }));
        const up = cross(right, fwd);
        return .{ .eye = eye, .fwd = fwd, .right = right, .up = up };
    }

    /// Projects a world point into a viewport of `width × height` (y down).
    /// Returns null if the point is behind or too close to the camera.
    pub fn project(self: Camera, p: Vec3, width: f64, height: f64) ?Point2 {
        const b = self.basis();
        const d = sub(p, b.eye);
        const z = dot(d, b.fwd);
        if (z < self.near) return null;
        const f = (height / 2.0) / @tan(self.fov_y / 2.0);
        return .{
            .x = width / 2.0 + f * dot(d, b.right) / z,
            .y = height / 2.0 - f * dot(d, b.up) / z,
        };
    }
};

fn add(a: Vec3, b: Vec3) Vec3 {
    return .{ a[0] + b[0], a[1] + b[1], a[2] + b[2] };
}
fn sub(a: Vec3, b: Vec3) Vec3 {
    return .{ a[0] - b[0], a[1] - b[1], a[2] - b[2] };
}
fn scale(a: Vec3, s: f64) Vec3 {
    return .{ a[0] * s, a[1] * s, a[2] * s };
}
fn dot(a: Vec3, b: Vec3) f64 {
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
}
fn cross(a: Vec3, b: Vec3) Vec3 {
    return .{ a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0] };
}
fn normalize(a: Vec3) Vec3 {
    return scale(a, 1.0 / @sqrt(dot(a, a)));
}

const testing = std.testing;

test "the target projects to the viewport centre" {
    const cam: Camera = .{};
    const p = cam.project(cam.target, 800, 600).?;
    try testing.expectApproxEqAbs(@as(f64, 400), p.x, 1e-9);
    try testing.expectApproxEqAbs(@as(f64, 300), p.y, 1e-9);
}

test "higher points appear higher on screen; points behind the camera are culled" {
    const cam: Camera = .{ .yaw = 0, .pitch = 0 };
    const low = cam.project(.{ 0, 0, 0 }, 800, 600).?;
    const high = cam.project(.{ 0, 0, 0.05 }, 800, 600).?;
    try testing.expect(high.y < low.y);
    try testing.expectEqual(@as(?Point2, null), cam.project(.{ 0, -1, 0.01 }, 800, 600));
}

test "+x appears to the right when looking along +y" {
    const cam: Camera = .{ .yaw = 0, .pitch = 0 };
    const c = cam.project(cam.target, 800, 600).?;
    const r = cam.project(.{ 0.02, 0, cam.target[2] }, 800, 600).?;
    try testing.expect(r.x > c.x);
}
