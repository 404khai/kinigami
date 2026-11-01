//! Inspector layout (Q45, Q50). Pure zigui core (no SDL), so the same view
//! tree renders on screen and headlessly in tests.

const std = @import("std");
const zigui = @import("zigui");
const scene_view = @import("scene_view.zig");
const projection = @import("projection.zig");

pub const Model = struct {
    /// Where the frames came from (recording path), or null if none loaded.
    source: ?[]const u8,
    /// Result label of the run being shown (PRC-005), shown prominently.
    label: []const u8,
    /// Run class of the run being shown (PRC-012).
    run_class: []const u8,
    frames: []const scene_view.SceneFrame,
    index: usize = 0,
    camera: projection.Camera = .{},
    /// Built per frame by `body`; must outlive the paint pass.
    view: scene_view.View = undefined,
};

pub fn body(m: *Model) zigui.View {
    const t = zigui.default_theme.colors;
    if (m.frames.len == 0) {
        return zigui.VStack(.{
            zigui.Text("Kinigami inspector").font(.title),
            zigui.Text(if (m.source) |s| s else "No recording loaded").foreground(t.secondary_label),
            zigui.Text("Recordings do not yet carry snapshot payloads (open decision), so there is nothing to display.").foreground(t.secondary_label),
        }).spacing(10).padding(24);
    }
    const i = @min(m.index, m.frames.len - 1);
    m.view = .{ .frame = &m.frames[i], .camera = m.camera, .theme_text = t.label };
    return zigui.VStack(.{
        zigui.HStack(.{
            zigui.Text(m.label).font(.headline),
            zigui.Text(m.run_class).foreground(t.secondary_label),
            zigui.Spacer(),
            zigui.Text(zigui.components.fmt("frame {d} / {d}", .{ i + 1, m.frames.len })).foreground(t.secondary_label),
        }).spacing(12),
        zigui.Drawing(scene_view.View, &m.view, scene_view.View.draw),
    }).spacing(8).padding(16);
}
