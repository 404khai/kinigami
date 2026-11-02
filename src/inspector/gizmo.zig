//! Viewport orientation gizmo for the inspector canvas: a small sphere in
//! the top-right corner showing the world X (red), Y (green), and Z (blue)
//! axes as seen from the current camera.
//!
//! - Click an axis ball to look along that axis: +X views from +X toward
//!   the target, and so on. +Z is top-down, −Z bottom-up.
//! - Drag the sphere (or empty canvas) to orbit; shift-drag or right-drag to
//!   pan; scroll to zoom; double-click the sphere to reset the view.
//!
//! Presentation only: the gizmo changes the camera, never recorded data
//! (INS-004, INS-005). Pure math, no SDL, so it is unit-tested headlessly.

const std = @import("std");
const projection = @import("projection.zig");

pub const Vec3 = projection.Vec3;

/// Largest elevation magnitude. The camera basis is singular exactly at
/// ±π/2 (looking straight along world z), so top and bottom views stop just
/// short of it.
pub const max_pitch: f64 = 1.55;
pub const min_distance_m: f64 = 0.02;
pub const max_distance_m: f64 = 20.0;
/// Orbit sensitivity, radians per point of mouse travel.
pub const orbit_rad_per_pt: f64 = 0.01;
/// Zoom factor per wheel line.
pub const zoom_per_line: f64 = 1.12;

pub const Axis = enum {
    px,
    nx,
    py,
    ny,
    pz,
    nz,

    pub fn dir(a: Axis) Vec3 {
        return switch (a) {
            .px => .{ 1, 0, 0 },
            .nx => .{ -1, 0, 0 },
            .py => .{ 0, 1, 0 },
            .ny => .{ 0, -1, 0 },
            .pz => .{ 0, 0, 1 },
            .nz => .{ 0, 0, -1 },
        };
    }

    pub fn positive(a: Axis) bool {
        return a == .px or a == .py or a == .pz;
    }

    pub fn label(a: Axis) []const u8 {
        return switch (a) {
            .px => "X",
            .py => "Y",
            .pz => "Z",
            else => "",
        };
    }
};

pub const Layout = struct {
    cx: f64,
    cy: f64,
    /// Sphere radius in points.
    r: f64,
    /// Axis-ball centres sit this far from the centre (fraction of r).
    pub const arm: f64 = 0.72;
    pub fn ballRadius(self: Layout, a: Axis) f64 {
        return if (a.positive()) self.r * 0.2 else self.r * 0.14;
    }
};

/// Top-right corner of the canvas `x, y, w, h` (points).
pub fn layout(x: f64, y: f64, w: f64, h: f64) Layout {
    const r = @max(40.0, @min(60.0, @min(w, h) * 0.12));
    const margin = 14.0;
    return .{ .cx = x + w - margin - r, .cy = y + margin + r + 18.0, .r = r };
}

const Basis = struct { right: Vec3, up: Vec3, toward_viewer: Vec3 };

fn basis(cam: projection.Camera) Basis {
    const cp = @cos(cam.pitch);
    const back: Vec3 = .{ -@sin(cam.yaw) * cp, -@cos(cam.yaw) * cp, @sin(cam.pitch) };
    const fwd = scale(back, -1);
    const right = normalize(cross(fwd, .{ 0, 0, 1 }));
    return .{ .right = right, .up = cross(right, fwd), .toward_viewer = back };
}

pub const Ball = struct {
    axis: Axis,
    /// Screen centre of the ball.
    x: f64,
    y: f64,
    /// > 0 points toward the viewer (drawn on top, hit first).
    depth: f64,
};

/// The six axis balls, sorted back to front (draw order; reverse for hits).
pub fn balls(cam: projection.Camera, lay: Layout) [6]Ball {
    const b = basis(cam);
    var out: [6]Ball = undefined;
    for (std.enums.values(Axis), 0..) |a, i| {
        const d = a.dir();
        out[i] = .{
            .axis = a,
            .x = lay.cx + lay.r * Layout.arm * dot(d, b.right),
            .y = lay.cy - lay.r * Layout.arm * dot(d, b.up),
            .depth = dot(d, b.toward_viewer),
        };
    }
    std.mem.sort(Ball, &out, {}, struct {
        fn lt(_: void, p: Ball, q: Ball) bool {
            return p.depth < q.depth;
        }
    }.lt);
    return out;
}

pub const Hit = union(enum) { axis: Axis, sphere };

/// What the point (x, y) is over: the front-most axis ball under it, else
/// the sphere, else nothing.
pub fn hitTest(cam: projection.Camera, lay: Layout, x: f64, y: f64) ?Hit {
    const bs = balls(cam, lay);
    var i: usize = bs.len;
    while (i > 0) {
        i -= 1;
        const b = bs[i];
        const rr = lay.ballRadius(b.axis) + 2.0;
        if ((x - b.x) * (x - b.x) + (y - b.y) * (y - b.y) <= rr * rr) return .{ .axis = b.axis };
    }
    if ((x - lay.cx) * (x - lay.cx) + (y - lay.cy) * (y - lay.cy) <= lay.r * lay.r) return .sphere;
    return null;
}

pub const View = struct { yaw: f64, pitch: f64 };

/// Camera angles that look along `a` toward the target from its positive
/// side (`a` points from the target to the eye). Top and bottom views keep
/// the current yaw so the horizontal orientation does not jump.
pub fn snapTo(a: Axis, current_yaw: f64) View {
    return switch (a) {
        .px => .{ .yaw = -std.math.pi / 2.0, .pitch = 0 },
        .nx => .{ .yaw = std.math.pi / 2.0, .pitch = 0 },
        .py => .{ .yaw = std.math.pi, .pitch = 0 },
        .ny => .{ .yaw = 0, .pitch = 0 },
        .pz => .{ .yaw = current_yaw, .pitch = max_pitch },
        .nz => .{ .yaw = current_yaw, .pitch = -max_pitch },
    };
}

/// Orbit by a mouse drag of (dx, dy) points. The scene turns with the
/// cursor, as in common 3D viewports: dragging right swings the camera left
/// around the target, and dragging down raises the camera. Yaw wraps to
/// (−π, π].
pub fn orbit(v: View, dx: f64, dy: f64) View {
    var yaw = v.yaw - dx * orbit_rad_per_pt;
    yaw = std.math.atan2(@sin(yaw), @cos(yaw));
    const pitch = std.math.clamp(v.pitch + dy * orbit_rad_per_pt, -max_pitch, max_pitch);
    return .{ .yaw = yaw, .pitch = pitch };
}

/// Zoom by `lines` wheel lines (positive = away from the user = zoom in).
pub fn zoom(distance_m: f64, lines: f64) f64 {
    return std.math.clamp(distance_m * std.math.pow(f64, zoom_per_line, -lines), min_distance_m, max_distance_m);
}

/// Pan offset change for a drag of (dx, dy) points in a canvas `h` points
/// tall: the scene follows the cursor in the view plane.
pub fn pan(cam: projection.Camera, h: f64, dx: f64, dy: f64) Vec3 {
    const b = basis(cam);
    const m_per_pt = 2.0 * cam.distance * @tan(cam.fov_y / 2.0) / h;
    return add(scale(b.right, -dx * m_per_pt), scale(b.up, dy * m_per_pt));
}

fn add(a: Vec3, b: Vec3) Vec3 {
    return .{ a[0] + b[0], a[1] + b[1], a[2] + b[2] };
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

test "snapping to an axis puts that axis toward the viewer" {
    for (std.enums.values(Axis)) |a| {
        const v = snapTo(a, 0.3);
        const cam: projection.Camera = .{ .yaw = v.yaw, .pitch = v.pitch };
        const d = dot(a.dir(), basis(cam).toward_viewer);
        try testing.expect(d > 0.99);
    }
}

test "the snapped axis ball is the front-most ball and sits at the sphere centre" {
    const lay = layout(0, 0, 800, 600);
    const v = snapTo(.px, 0);
    const bs = balls(.{ .yaw = v.yaw, .pitch = v.pitch }, lay);
    try testing.expectEqual(Axis.px, bs[5].axis);
    try testing.expectApproxEqAbs(lay.cx, bs[5].x, 1e-9);
    try testing.expectApproxEqAbs(lay.cy, bs[5].y, 1e-9);
}

test "hit testing finds the axis ball under the cursor, then the sphere, then nothing" {
    const lay = layout(0, 0, 800, 600);
    const cam: projection.Camera = .{};
    for (balls(cam, lay)) |b| {
        if (b.depth < 0) continue; // a back ball may hide behind a front one
        const hit = hitTest(cam, lay, b.x, b.y).?;
        try testing.expectEqual(b.axis, hit.axis);
    }
    try testing.expect(hitTest(cam, lay, lay.cx + lay.r * 0.95, lay.cy) != null);
    try testing.expectEqual(@as(?Hit, null), hitTest(cam, lay, 10, 500));
}

test "the default view shows +Z up on screen and +X to the right" {
    const lay = layout(0, 0, 800, 600);
    var z: Ball = undefined;
    var x: Ball = undefined;
    for (balls(.{ .yaw = 0, .pitch = 0.3 }, lay)) |b| switch (b.axis) {
        .pz => z = b,
        .px => x = b,
        else => {},
    };
    try testing.expect(z.y < lay.cy);
    try testing.expect(x.x > lay.cx);
}

test "orbit clamps elevation short of the poles and wraps yaw" {
    const v = orbit(.{ .yaw = 3.1, .pitch = 1.5 }, -10, 1000);
    try testing.expectEqual(max_pitch, v.pitch);
    try testing.expect(v.yaw <= std.math.pi and v.yaw > -std.math.pi);
    try testing.expect(v.yaw < 0); // wrapped past π
}

test "zoom is monotone and clamped" {
    try testing.expect(zoom(0.25, 1) < 0.25);
    try testing.expect(zoom(0.25, -1) > 0.25);
    try testing.expectEqual(min_distance_m, zoom(0.03, 50));
    try testing.expectEqual(max_distance_m, zoom(10, -50));
}

test "panning moves the target in the view plane, opposite to a rightward drag" {
    const cam: projection.Camera = .{ .yaw = 0, .pitch = 0 };
    const d = pan(cam, 600, 10, 0);
    try testing.expect(d[0] < 0); // looking along +y, right is +x
    try testing.expectApproxEqAbs(@as(f64, 0), d[2], 1e-15);
}
