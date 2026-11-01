//! `kinigami-inspector`: read-only viewer for Kinigami recordings (Q45, Q50).
//!
//! Usage:
//!   kinigami-inspector [recording.kgrec]                 open a window
//!   kinigami-inspector --screenshot out.bmp [recording]  render headlessly
//!
//! The inspector never runs or modifies a simulation. It validates a
//! recording's container with the core reader (INS-003) and displays only
//! recorded values.

const std = @import("std");
const zigui = @import("zigui");
const app = @import("zigui_app");
const core = @import("kinigami_core");
const inspector = @import("inspector");

const AppState = struct {
    model: inspector.ui.Model,
};

fn body(st: *AppState) zigui.View {
    return inspector.ui.body(&st.model);
}

pub fn main(init: std.process.Init) !void {
    const arena = init.arena.allocator();
    const args = try init.minimal.args.toSlice(arena);

    var screenshot: ?[]const u8 = null;
    var path: ?[]const u8 = null;
    var i: usize = 1;
    while (i < args.len) : (i += 1) {
        if (std.mem.eql(u8, args[i], "--screenshot") and i + 1 < args.len) {
            i += 1;
            screenshot = args[i];
        } else path = args[i];
    }

    var source: ?[]const u8 = null;
    if (path) |p| {
        const bytes = try std.Io.Dir.cwd().readFileAlloc(init.io, p, arena, .limited(1 << 30));
        _ = core.recording.Recording.parse(bytes) catch |err| {
            std.debug.print("inspector: {s} is not a valid recording: {s}\n", .{ p, @errorName(err) });
            std.process.exit(1);
        };
        source = try std.fmt.allocPrint(arena, "{s} (valid recording container, format v{d})", .{ p, core.recording.format_version });
    }

    var st: AppState = .{ .model = .{ .source = source, .label = "-", .run_class = "-", .frames = &.{} } };

    if (screenshot) |out| {
        var fb = try inspector.headless.render(init.gpa, &st.model, 900, 600);
        defer fb.deinit();
        const bmp = try inspector.headless.encodeBmp(arena, &fb);
        try std.Io.Dir.cwd().writeFile(init.io, .{ .sub_path = out, .data = bmp });
        std.debug.print("wrote {s}\n", .{out});
        return;
    }
    try app.run(init.gpa, AppState, &st, .{ .title = "Kinigami inspector", .width = 1000, .height = 700 }, body, null);
}
