//! Wireframe scene view for the inspector (Q45, Q50).
//!
//! Draws exactly one `SceneFrame`: recorded body poses and recorded,
//! solver-produced contact forces (INS-005). Nothing here computes physics;
//! a value absent from the frame is not drawn and is reported as
//! unavailable. Depends only on the pure-Zig zigui core (no SDL).

const std = @import("std");
const zigui = @import("zigui");
const projection = @import("projection.zig");

pub const Vec3 = projection.Vec3;

pub const Quat = struct {
    w: f64,
    x: f64,
    y: f64,
    z: f64,

    pub fn rotate(q: Quat, v: Vec3) Vec3 {
        const u: Vec3 = .{ q.x, q.y, q.z };
        const t = scale(cross(u, v), 2.0);
        return add(add(v, scale(t, q.w)), cross(u, t));
    }
};

pub const Body = struct {
    position_m: Vec3,
    orientation: Quat,
    half_extents_m: Vec3,
    /// Q40/INS-009: fixtures are labeled as fixtures, never as Kins.
    is_fixture: bool,
};

pub const Contact = struct {
    point_m: Vec3,
    normal_force_n: f64,
    tangential_force_n: Vec3,
};

/// One recorded instant. `contacts == null` means contact data was not
/// recorded for this frame (shown as unavailable), which is different from
/// an empty list (recorded: no contacts).
pub const SceneFrame = struct {
    tick: u64,
    time_s: f64,
    bodies: []const Body,
    contacts: ?[]const Contact,
};

pub const Style = struct {
    /// Screen length of a force arrow per newton.
    px_per_newton: f64 = 120,
    grid_spacing_m: f64 = 0.01,
    grid_half_extent_m: f64 = 0.08,
};

pub const View = struct {
    frame: *const SceneFrame,
    camera: projection.Camera,
    style: Style = .{},
    theme_text: zigui.Color,

    pub fn draw(self: *const View, pen: *zigui.view.Pen, rect: zigui.Rect) std.mem.Allocator.Error!void {
        const w: f64 = rect.width;
        const h: f64 = rect.height;
        const grid = zigui.Color.fromRgba8(120, 130, 145, 90);
        const edge = zigui.Color.fromRgba8(70, 150, 230, 255);
        const normal_c = zigui.Color.fromRgba8(60, 190, 110, 255);
        const friction_c = zigui.Color.fromRgba8(235, 140, 50, 255);
        const point_c = zigui.Color.fromRgba8(230, 70, 70, 255);

        // Tabletop grid (z = 0).
        const s = self.style;
        var g: f64 = -s.grid_half_extent_m;
        while (g <= s.grid_half_extent_m + 1e-12) : (g += s.grid_spacing_m) {
            try self.segment(pen, rect, .{ g, -s.grid_half_extent_m, 0 }, .{ g, s.grid_half_extent_m, 0 }, 1, grid, w, h);
            try self.segment(pen, rect, .{ -s.grid_half_extent_m, g, 0 }, .{ s.grid_half_extent_m, g, 0 }, 1, grid, w, h);
        }

        // Bodies: the 12 edges of each cuboid at its recorded pose.
        for (self.frame.bodies) |b| {
            var corners: [8]Vec3 = undefined;
            for (&corners, 0..) |*c, i| {
                const local: Vec3 = .{
                    if (i & 1 != 0) b.half_extents_m[0] else -b.half_extents_m[0],
                    if (i & 2 != 0) b.half_extents_m[1] else -b.half_extents_m[1],
                    if (i & 4 != 0) b.half_extents_m[2] else -b.half_extents_m[2],
                };
                c.* = add(b.position_m, b.orientation.rotate(local));
            }
            for (0..8) |i| for ([_]usize{ 1, 2, 4 }) |bit| {
                if (i & bit == 0) try self.segment(pen, rect, corners[i], corners[i | bit], 2, edge, w, h);
            };
        }

        // Contacts: point, normal force (green), friction force (orange).
        if (self.frame.contacts) |contacts| {
            for (contacts) |c| {
                const scale_m = s.px_per_newton / pxPerMetreAt(self.camera, c.point_m, h);
                try self.segment(pen, rect, c.point_m, add(c.point_m, .{ 0, 0, c.normal_force_n * scale_m }), 2, normal_c, w, h);
                try self.segment(pen, rect, c.point_m, add(c.point_m, scale(c.tangential_force_n, scale_m)), 2, friction_c, w, h);
                if (self.camera.project(c.point_m, w, h)) |p|
                    try pen.fill(.{ .x = rect.x + @as(f32, @floatCast(p.x)) - 3, .y = rect.y + @as(f32, @floatCast(p.y)) - 3, .width = 6, .height = 6 }, 3, point_c);
            }
        } else {
            try pen.text("contact data: unavailable (not recorded)", 12, self.theme_text, .{ .x = rect.x + 10, .y = rect.y + rect.height - 22 });
        }

        try pen.text(pen.fmt("t = {d:.4} s   (tick {d})", .{ self.frame.time_s, self.frame.tick }), 13, self.theme_text, .{ .x = rect.x + 10, .y = rect.y + 8 });
    }

    fn segment(self: *const View, pen: *zigui.view.Pen, rect: zigui.Rect, a: Vec3, b: Vec3, width: f32, color: zigui.Color, w: f64, h: f64) !void {
        const pa = self.camera.project(a, w, h) orelse return;
        const pb = self.camera.project(b, w, h) orelse return;
        try pen.line(
            .{ .x = rect.x + @as(f32, @floatCast(pa.x)), .y = rect.y + @as(f32, @floatCast(pa.y)) },
            .{ .x = rect.x + @as(f32, @floatCast(pb.x)), .y = rect.y + @as(f32, @floatCast(pb.y)) },
            width,
            color,
        );
    }
};

/// Approximate screen pixels per metre at a world point, so force arrows have
/// a consistent on-screen length per newton regardless of depth.
fn pxPerMetreAt(cam: projection.Camera, p: Vec3, h: f64) f64 {
    const a = cam.project(p, 1, h) orelse return 1;
    const b = cam.project(add(p, .{ 0, 0, 0.001 }), 1, h) orelse return 1;
    const d = @sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y));
    return if (d > 0) d / 0.001 else 1;
}

fn add(a: Vec3, b: Vec3) Vec3 {
    return .{ a[0] + b[0], a[1] + b[1], a[2] + b[2] };
}
fn scale(a: Vec3, s: f64) Vec3 {
    return .{ a[0] * s, a[1] * s, a[2] * s };
}
fn cross(a: Vec3, b: Vec3) Vec3 {
    return .{ a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0] };
}
