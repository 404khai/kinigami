//! Inspector layout (Q45, Q50). Pure zigui core (no SDL), so the same view
//! tree renders on screen and headlessly in tests.

const std = @import("std");
const zigui = @import("zigui");
const scene_view = @import("scene_view.zig");
const projection = @import("projection.zig");

pub const Model = struct {
    /// Where the frames came from (recording path), or null if none loaded.
    source: ?[]const u8,
    /// Result-label ceiling of the run being shown (PRC-005), shown prominently.
    label: []const u8,
    /// Run class of the run being shown (PRC-012).
    run_class: []const u8,
    title: []const u8 = "",
    frames: []const scene_view.SceneFrame,
    index: usize = 0,
    camera: projection.Camera = .{},
    /// Camera pan from the orientation gizmo (shift/right drag), added to the
    /// followed target. Presentation only.
    pan_m: projection.Vec3 = .{ 0, 0, 0 },
    /// Canvas rectangle from the last draw, for gizmo hit tests.
    canvas: zigui.Rect = .{ .x = 0, .y = 0, .width = 0, .height = 0 },
    /// Built per frame by `body`; must outlive the paint pass.
    view: scene_view.View = undefined,
};

/// `controls` is supplied by the windowed app (playback buttons, sliders);
/// headless renders pass null.
pub fn body(m: *Model, controls: ?zigui.View) zigui.View {
    const t = zigui.default_theme.colors;
    if (m.frames.len == 0) {
        return zigui.VStack(.{
            zigui.Text("Kinigami inspector").font(.title),
            zigui.Text(if (m.source) |s| s else "No recording loaded").foreground(t.secondary_label),
            zigui.Text("Open a format-v2 or v3 recording: kinigami-inspector <file.kgrec>").foreground(t.secondary_label),
        }).spacing(10).padding(24);
    }
    const i = @min(m.index, m.frames.len - 1);
    const f = &m.frames[i];
    // Presentation only: the camera follows the first dynamic body so a
    // sliding fixture stays in view horizontally; it follows height too for
    // bodies well above the tabletop (hanging or free-falling link fixtures,
    // Q55). Recorded values are never changed.
    var cam = m.camera;
    if (f.bodies.len > 0) {
        const p = f.bodies[scene_view.followedBody(f.*)].position_m;
        cam.target = .{ p[0], p[1], if (p[2] > 0.1) p[2] else m.camera.target[2] };
    }
    for (&cam.target, m.pan_m) |*x, d| x.* += d;
    m.view = .{ .frame = f, .camera = cam, .theme_text = t.label, .canvas_out = &m.canvas };

    return zigui.VStack(.{
        zigui.HStack(.{
            zigui.Text(m.label).font(.headline).foreground(zigui.Color.fromRgb8(200, 120, 20)),
            zigui.Text("not Kin evidence").foreground(t.secondary_label),
            zigui.Text(m.title),
            zigui.Spacer(),
            zigui.Text(zigui.components.fmt("frame {d} / {d}", .{ i + 1, m.frames.len })).foreground(t.secondary_label),
        }).spacing(12),
        zigui.HStack(.{
            zigui.Drawing(scene_view.View, &m.view, scene_view.View.draw),
            readout(f).frame(250, 360),
        }).spacing(12),
        controls orelse zigui.Spacer(),
    }).spacing(10).padding(16);
}

/// Recorded values for the current frame. Sums are presentation aggregates
/// of recorded solver forces; nothing is recomputed (INS-005).
fn readout(f: *const scene_view.SceneFrame) zigui.View {
    const t = zigui.default_theme.colors;
    const fmt = zigui.components.fmt;
    const fi = scene_view.followedBody(f.*);
    const b = f.bodies[fi];
    var fn_sum: f64 = 0;
    var ft: [3]f64 = .{ 0, 0, 0 };
    var n_contacts: usize = 0;
    if (f.contacts) |cs| {
        n_contacts = cs.len;
        for (cs) |c| {
            fn_sum += c.normal_force_n;
            for (&ft, c.tangential_force_n) |*a, x| a.* += x;
        }
    }
    const v = if (f.velocities_m_s) |vs| fmt("{d:.5}, {d:.5}, {d:.5} m/s", .{ vs[fi][0], vs[fi][1], vs[fi][2] }) else "unavailable";
    return zigui.VStack(.{
        zigui.Text("Recorded state").font(.headline),
        zigui.Text(fmt("t = {d:.4} s  (tick {d})", .{ f.time_s, f.tick })),
        zigui.Text("position").foreground(t.secondary_label),
        zigui.Text(fmt("{d:.5}, {d:.5}, {d:.5} m", .{ b.position_m[0], b.position_m[1], b.position_m[2] })),
        zigui.Text("velocity").foreground(t.secondary_label),
        zigui.Text(v),
        zigui.Text("contacts (solver output)").foreground(t.secondary_label),
        if (f.contacts == null) zigui.Text("unavailable") else zigui.Text(fmt("{d} points", .{n_contacts})),
        zigui.Text(fmt("Σ normal  {d:.5} N", .{fn_sum})),
        zigui.Text(fmt("Σ friction {d:.5} N", .{@sqrt(ft[0] * ft[0] + ft[1] * ft[1] + ft[2] * ft[2])})),
        zigui.Text("green: normal force").foreground(zigui.Color.fromRgb8(60, 160, 90)),
        zigui.Text("orange: friction force").foreground(zigui.Color.fromRgb8(215, 120, 40)),
        zigui.Text("red: contact point").foreground(zigui.Color.fromRgb8(210, 60, 60)),
        zigui.Spacer(),
    }).spacing(6);
}
