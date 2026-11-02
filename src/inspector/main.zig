//! `kinigami-inspector`: read-only viewer for Kinigami recordings (Q45, Q50).
//!
//! Usage:
//!   kinigami-inspector <recording.kgrec>                       open a window
//!   kinigami-inspector --screenshot out.bmp [--frame N] <rec>  render headlessly
//!
//! View controls (presentation only): the orientation sphere in the canvas
//! corner. Click an axis ball to look along X, Y, or Z (either sign); drag the
//! canvas to orbit; shift-drag or right-drag to pan; scroll to zoom;
//! double-click the sphere to reset the view. The sliders mirror the camera.
//!
//! The inspector never runs or modifies a simulation. It loads recordings
//! with the core reader (INS-003) and displays only recorded values. Playback
//! timing uses the host clock for presentation only; it never touches
//! recorded data.

const std = @import("std");
const zigui = @import("zigui");
const app = @import("zigui_app");
const core = @import("kinigami_core");
const inspector = @import("inspector");
const gizmo = inspector.gizmo;

/// `SDL_KMOD_LSHIFT | SDL_KMOD_RSHIFT`.
const shift_mask: u16 = 0x0003;

const AppState = struct {
    model: inspector.ui.Model,
    scrub: zigui.State(f32),
    yaw: zigui.State(f32),
    pitch: zigui.State(f32),
    zoom: zigui.State(f32),
    playing: bool = false,
    drag: enum { none, orbit, pan } = .none,
    last_x: f32 = 0,
    last_y: f32 = 0,
    /// Frames advanced per display refresh (about real time at 60 Hz).
    frames_per_refresh: usize = 1,

    fn lastIndex(self: *const AppState) usize {
        return if (self.model.frames.len == 0) 0 else self.model.frames.len - 1;
    }
    fn index(self: *const AppState) usize {
        const n = self.lastIndex();
        if (n == 0) return 0;
        return @intFromFloat(@round(std.math.clamp(self.scrub.get(), 0, 1) * @as(f32, @floatFromInt(n))));
    }
    fn setIndex(self: *AppState, i: usize) void {
        const n = self.lastIndex();
        self.scrub.set(if (n == 0) 0 else @as(f32, @floatFromInt(@min(i, n))) / @as(f32, @floatFromInt(n)));
    }
    fn togglePlay(self: *AppState) void {
        if (!self.playing and self.index() >= self.lastIndex()) self.setIndex(0);
        self.playing = !self.playing;
    }
    fn toStart(self: *AppState) void {
        self.playing = false;
        self.setIndex(0);
    }
    fn stepBack(self: *AppState) void {
        self.playing = false;
        const i = self.index();
        self.setIndex(if (i > 0) i - 1 else 0);
    }
    fn setView(self: *AppState, v: gizmo.View) void {
        self.yaw.set(@floatCast(v.yaw));
        self.pitch.set(@floatCast(v.pitch));
    }
    fn resetView(self: *AppState) void {
        const d: inspector.projection.Camera = .{};
        self.setView(.{ .yaw = d.yaw, .pitch = d.pitch });
        self.zoom.set(@floatCast(d.distance));
        self.model.pan_m = .{ 0, 0, 0 };
    }
    fn stepForward(self: *AppState) void {
        self.playing = false;
        self.setIndex(self.index() + 1);
    }
};

var g_state: ?*AppState = null;

fn frameHook() void {
    const st = g_state orelse return;
    if (!st.playing) return;
    const next = st.index() + st.frames_per_refresh;
    if (next >= st.lastIndex()) {
        st.setIndex(st.lastIndex());
        st.playing = false;
    } else st.setIndex(next);
}

/// Mouse handling for the canvas and the orientation gizmo. Consumes only
/// events that start on the canvas, so the buttons and sliders keep working.
fn onMouse(ev: app.MouseEvent) bool {
    const st = g_state orelse return false;
    const r = st.model.canvas;
    const inside = r.width > 0 and ev.x >= r.x and ev.x <= r.x + r.width and ev.y >= r.y and ev.y <= r.y + r.height;
    switch (ev.kind) {
        .down => {
            if (!inside) return false;
            const cam = st.model.view.camera;
            const lay = gizmo.layout(r.x, r.y, r.width, r.height);
            if (ev.button == 1) if (gizmo.hitTest(cam, lay, ev.x, ev.y)) |hit| switch (hit) {
                .axis => |a| {
                    st.setView(gizmo.snapTo(a, cam.yaw));
                    return true;
                },
                .sphere => if (ev.clicks >= 2) {
                    st.resetView();
                    return true;
                },
            };
            st.drag = if (ev.button == 3 or (ev.button == 1 and ev.mods & shift_mask != 0)) .pan else if (ev.button == 1) .orbit else return false;
            st.last_x = ev.x;
            st.last_y = ev.y;
            return true;
        },
        .motion => {
            if (st.drag == .none) return false;
            const dx: f64 = ev.x - st.last_x;
            const dy: f64 = ev.y - st.last_y;
            st.last_x = ev.x;
            st.last_y = ev.y;
            switch (st.drag) {
                .orbit => st.setView(gizmo.orbit(.{ .yaw = st.yaw.get(), .pitch = st.pitch.get() }, dx, dy)),
                .pan => {
                    const d = gizmo.pan(st.model.view.camera, r.height, dx, dy);
                    for (&st.model.pan_m, d) |*p, x| p.* += x;
                },
                .none => {},
            }
            return true;
        },
        .up => {
            if (st.drag == .none) return false;
            st.drag = .none;
            return true;
        },
        .wheel => {
            if (!inside) return false;
            st.zoom.set(@floatCast(gizmo.zoom(st.zoom.get(), ev.dy)));
            return true;
        },
    }
}

fn busyInterval() u32 {
    const st = g_state orelse return 0;
    return if (st.playing) 16 else 0;
}

fn body(st: *AppState) zigui.View {
    st.model.index = st.index();
    st.model.camera.yaw = @as(f64, st.yaw.get());
    st.model.camera.pitch = @as(f64, st.pitch.get());
    st.model.camera.distance = @as(f64, st.zoom.get());
    const controls = zigui.VStack(.{
        zigui.HStack(.{
            zigui.Button("Start", zigui.actionCtx(AppState, st, AppState.toStart)),
            zigui.Button("Step back", zigui.actionCtx(AppState, st, AppState.stepBack)),
            zigui.Button(if (st.playing) "Pause" else "Play", zigui.actionCtx(AppState, st, AppState.togglePlay)),
            zigui.Button("Step forward", zigui.actionCtx(AppState, st, AppState.stepForward)),
            zigui.Slider(st.scrub.binding(), 0, 1),
        }).spacing(8),
        zigui.HStack(.{
            zigui.Text("orbit"),
            zigui.Slider(st.yaw.binding(), -3.14159, 3.14159),
            zigui.Text("elevation"),
            zigui.Slider(st.pitch.binding(), @floatCast(-gizmo.max_pitch), @floatCast(gizmo.max_pitch)),
            zigui.Text("distance"),
            zigui.Slider(st.zoom.binding(), @floatCast(gizmo.min_distance_m), 2.0),
            zigui.Button("Reset view", zigui.actionCtx(AppState, st, AppState.resetView)),
        }).spacing(8),
    }).spacing(8);
    return inspector.ui.body(&st.model, controls);
}

pub fn main(init: std.process.Init) !void {
    const arena = init.arena.allocator();
    const args = try init.minimal.args.toSlice(arena);

    var screenshot: ?[]const u8 = null;
    var frame_arg: ?usize = null;
    var path: ?[]const u8 = null;
    var i: usize = 1;
    while (i < args.len) : (i += 1) {
        if (std.mem.eql(u8, args[i], "--screenshot") and i + 1 < args.len) {
            i += 1;
            screenshot = args[i];
        } else if (std.mem.eql(u8, args[i], "--frame") and i + 1 < args.len) {
            i += 1;
            frame_arg = try std.fmt.parseInt(usize, args[i], 10);
        } else path = args[i];
    }

    var model: inspector.ui.Model = .{ .source = null, .label = "-", .run_class = "-", .frames = &.{} };
    var physics_step_s: f64 = 0;
    if (path) |p| {
        const bytes = try std.Io.Dir.cwd().readFileAlloc(init.io, p, arena, .limited(1 << 30));
        const loaded = inspector.loader.load(arena, bytes) catch |err| {
            std.debug.print("inspector: cannot load {s}: {s}\n", .{ p, @errorName(err) });
            std.process.exit(1);
        };
        model = .{ .source = p, .label = loaded.label, .run_class = loaded.run_class, .title = loaded.title, .frames = loaded.frames };
        physics_step_s = loaded.physics_step_s;
    }

    var st: AppState = .{
        .model = model,
        .scrub = .init(init.gpa, 0),
        .yaw = .init(init.gpa, @floatCast(model.camera.yaw)),
        .pitch = .init(init.gpa, @floatCast(model.camera.pitch)),
        .zoom = .init(init.gpa, @floatCast(model.camera.distance)),
        .frames_per_refresh = if (physics_step_s > 0) @max(1, @as(usize, @intFromFloat(@round((1.0 / 60.0) / physics_step_s)))) else 1,
    };
    if (frame_arg) |f| st.setIndex(f);

    if (screenshot) |out| {
        st.model.index = st.index();
        var fb = try inspector.headless.render(init.gpa, &st.model, 1100, 640);
        defer fb.deinit();
        const bmp = try inspector.headless.encodeBmp(arena, &fb);
        try std.Io.Dir.cwd().writeFile(init.io, .{ .sub_path = out, .data = bmp });
        std.debug.print("wrote {s}\n", .{out});
        return;
    }

    g_state = &st;
    app.setFrameHook(frameHook);
    app.setBusyInterval(busyInterval);
    app.setMouseHandler(onMouse);
    try app.run(init.gpa, AppState, &st, .{ .title = "Kinigami inspector", .width = 1200, .height = 760 }, body, null);
}
