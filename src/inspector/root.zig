//! Inspector library: layout, wireframe view, and headless rendering. Uses
//! only the pure-Zig zigui core; the SDL window layer is used by `main.zig`
//! alone. Never imported by the simulation core (Q42, Q45).

pub const projection = @import("projection.zig");
pub const gizmo = @import("gizmo.zig");
pub const scene_view = @import("scene_view.zig");
pub const ui = @import("ui.zig");
pub const headless = @import("headless.zig");
pub const loader = @import("loader.zig");

test {
    _ = projection;
    _ = gizmo;
    _ = scene_view;
    _ = ui;
    _ = headless;
    _ = loader;
}
