//! `kinigami-inspector`: read-only viewer for Kinigami recordings (Q45, Q50).
//!
//! Usage:
//!   kinigami-inspector <recording.kgrec>                       open a window
//!   kinigami-inspector --screenshot out.bmp [--frame N] <rec>  render headlessly
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

const AppState = struct {
    model: inspector.ui.Model,
    scrub: zigui.State(f32),
    yaw: zigui.State(f32),
    pitch: zigui.State(f32),
    zoom: zigui.State(f32),
    playing: bool = false,
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
            zigui.Slider(st.pitch.binding(), 0.05, 1.5),
            zigui.Text("distance"),
            zigui.Slider(st.zoom.binding(), 0.08, 0.6),
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
    try app.run(init.gpa, AppState, &st, .{ .title = "Kinigami inspector", .width = 1200, .height = 760 }, body, null);
}
