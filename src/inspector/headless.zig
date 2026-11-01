//! Headless rendering of the inspector with zigui's pure-Zig software
//! rasterizer: no window, no GPU, no SDL. Used by tests and `--screenshot`.

const std = @import("std");
const zigui = @import("zigui");
const ui = @import("ui.zig");

pub fn render(gpa: std.mem.Allocator, m: *ui.Model, w: u32, h: u32) !zigui.Framebuffer {
    const theme = zigui.default_theme;
    var font = zigui.Font.default();
    var cache = zigui.GlyphCache.init(gpa, &font.face);
    defer cache.deinit();
    var arena = std.heap.ArenaAllocator.init(gpa);
    defer arena.deinit();
    zigui.setThemeTokens(theme);
    zigui.beginBuild(arena.allocator());
    const root = ui.body(m, null);
    zigui.endBuild();
    var hits: std.ArrayList(zigui.HitRegion) = .empty;
    var ctx = zigui.Context.init(theme, &cache, arena.allocator(), &hits);
    var canvas = zigui.Canvas.init(arena.allocator());
    const full = zigui.Rect{ .x = 0, .y = 0, .width = @floatFromInt(w), .height = @floatFromInt(h) };
    try canvas.fillRect(full, theme.colors.window_background);
    try zigui.render(&ctx, root, full, &canvas);
    var fb = try zigui.Framebuffer.init(gpa, w, h);
    errdefer fb.deinit();
    fb.clear(theme.colors.window_background);
    try zigui.raster.render(gpa, &fb, canvas.commands.items);
    return fb;
}

/// Uncompressed 24-bit BMP encoding of a framebuffer (bottom-up rows).
pub fn encodeBmp(gpa: std.mem.Allocator, fb: *const zigui.Framebuffer) ![]u8 {
    const row = (fb.width * 3 + 3) & ~@as(u32, 3);
    const size = 54 + row * fb.height;
    const out = try gpa.alloc(u8, size);
    @memset(out, 0);
    out[0] = 'B';
    out[1] = 'M';
    std.mem.writeInt(u32, out[2..6], size, .little);
    std.mem.writeInt(u32, out[10..14], 54, .little);
    std.mem.writeInt(u32, out[14..18], 40, .little);
    std.mem.writeInt(i32, out[18..22], @intCast(fb.width), .little);
    std.mem.writeInt(i32, out[22..26], @intCast(fb.height), .little);
    std.mem.writeInt(u16, out[26..28], 1, .little);
    std.mem.writeInt(u16, out[28..30], 24, .little);
    for (0..fb.height) |y| {
        const dst = out[54 + (fb.height - 1 - y) * row ..];
        for (0..fb.width) |x| {
            const c = fb.pixels[y * fb.width + x];
            dst[x * 3 + 0] = to8(c.b);
            dst[x * 3 + 1] = to8(c.g);
            dst[x * 3 + 2] = to8(c.r);
        }
    }
    return out;
}

fn to8(v: f32) u8 {
    return @intFromFloat(@round(std.math.clamp(v, 0, 1) * 255));
}

// --- Tests: synthetic scene input, used only to exercise drawing. ---

const scene_view = @import("scene_view.zig");

fn testFrame() scene_view.SceneFrame {
    const S = struct {
        const bodies = [_]scene_view.Body{.{ .position_m = .{ 0, 0, 0.01 }, .orientation = .{ .w = 1, .x = 0, .y = 0, .z = 0 }, .half_extents_m = .{ 0.02, 0.02, 0.01 }, .is_fixture = true }};
        const contacts = [_]scene_view.Contact{.{ .point_m = .{ 0.02, 0.02, 0 }, .normal_force_n = 0.098, .tangential_force_n = .{ 0, 0, 0 } }};
    };
    return .{ .tick = 0, .time_s = 0, .bodies = &S.bodies, .contacts = &S.contacts };
}

/// Counts matching pixels in the left part of the frame (the 3D view),
/// excluding the readout panel whose legend uses the same colors.
fn countColor(fb: *const zigui.Framebuffer, r: u8, g: u8, b: u8) usize {
    var n: usize = 0;
    for (fb.pixels, 0..) |c, i| {
        if (i % fb.width >= fb.width / 2) continue;
        if (@abs(@as(i32, to8(c.r)) - r) < 25 and @abs(@as(i32, to8(c.g)) - g) < 25 and @abs(@as(i32, to8(c.b)) - b) < 25) n += 1;
    }
    return n;
}

test "headless render draws fixture edges and contact markers" {
    const gpa = std.testing.allocator;
    const frames = [_]scene_view.SceneFrame{testFrame()};
    var m: ui.Model = .{ .source = "test", .label = "FIXTURE", .run_class = "fixture_validation", .frames = &frames };
    var fb = try render(gpa, &m, 640, 420);
    defer fb.deinit();
    try std.testing.expect(countColor(&fb, 70, 150, 230) > 50); // body edges
    try std.testing.expect(countColor(&fb, 230, 70, 70) > 5); // contact point
}

test "missing contact data is shown as unavailable, not drawn" {
    const gpa = std.testing.allocator;
    var f = testFrame();
    f.contacts = null;
    const frames = [_]scene_view.SceneFrame{f};
    var m: ui.Model = .{ .source = "test", .label = "FIXTURE", .run_class = "fixture_validation", .frames = &frames };
    var fb = try render(gpa, &m, 640, 420);
    defer fb.deinit();
    try std.testing.expectEqual(@as(usize, 0), countColor(&fb, 230, 70, 70));
}
