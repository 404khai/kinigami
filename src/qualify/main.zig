//! `kinigami-qualify`: runs the compliant-link qualification suite (Q52) and
//! writes a JSON report. Usage: kinigami-qualify <report.json> [--recordings <dir>]
//! `kinigami-qualify --coupler <report.json> [--recordings <dir>]` runs the
//! coupler-engagement suite (Q56, Q57) instead.
//! With `--recordings`, every evaluated run writes a format-v3 recording
//! with link records (Q55) for the inspector (the coupler suite: every run of
//! C1-C9, including each capture-sweep run). Recording never changes results.
//!
//! Results are labeled `fixture` (Q46). They qualify nothing beyond the
//! declared envelope and are never benchmark or Kin-candidate evidence.

const std = @import("std");
const core = @import("kinigami_core");
const build_info = @import("build_info");

const Output = struct {
    code_revision: []const u8,
    working_tree_dirty: bool,
    optimize_mode: []const u8,
    target: []const u8,
    zig_version: []const u8,
    report: core.link_suite.Report,
};

const CouplerOutput = struct {
    code_revision: []const u8,
    working_tree_dirty: bool,
    optimize_mode: []const u8,
    target: []const u8,
    zig_version: []const u8,
    report: core.coupler_suite.Report,
};

const RecordingWriter = struct {
    io: std.Io,
    dir: std.Io.Dir,
    count: usize = 0,

    fn emit(ptr: *anyopaque, name: []const u8, bytes: []const u8) anyerror!void {
        const self: *RecordingWriter = @ptrCast(@alignCast(ptr));
        try self.dir.writeFile(self.io, .{ .sub_path = name, .data = bytes });
        self.count += 1;
    }
};

pub fn main(init: std.process.Init) !void {
    const arena = init.arena.allocator();
    const args = try init.minimal.args.toSlice(arena);
    const usage = "usage: kinigami-qualify <report.json> [--recordings <dir>]\n       kinigami-qualify --sensitivity <dir>   (exploratory, Q54)\n       kinigami-qualify --coupler <report.json>   (coupler engagement, Q56/Q57)\n       kinigami-qualify --coupler <report.json> --recordings <dir>\n";
    if (args.len >= 3 and std.mem.eql(u8, args[1], "--coupler")) {
        if (args.len == 5 and std.mem.eql(u8, args[3], "--recordings")) return coupler(init, arena, args[2], args[4]);
        if (args.len != 3) {
            std.debug.print(usage, .{});
            std.process.exit(2);
        }
        return coupler(init, arena, args[2], null);
    }
    const with_recordings = args.len == 4 and std.mem.eql(u8, args[2], "--recordings");
    if (args.len != 2 and !with_recordings and !(args.len == 3 and std.mem.eql(u8, args[1], "--sensitivity"))) {
        std.debug.print(usage, .{});
        std.process.exit(2);
    }
    if (args.len == 3) return sensitivity(init, arena, args[2]);

    var writer: RecordingWriter = .{ .io = init.io, .dir = undefined };
    var recorder: ?core.link_suite.Recorder = null;
    if (with_recordings) {
        try std.Io.Dir.cwd().createDirPath(init.io, args[3]);
        writer.dir = try std.Io.Dir.cwd().openDir(init.io, args[3], .{});
        recorder = .{ .ptr = &writer, .emit = RecordingWriter.emit };
    }

    // Official criteria: v2 (Q53). v1 run 1 is preserved as superseded evidence.
    const parsed = try core.link_criteria.parse(arena, core.link_criteria.link_v2_json);
    const report = try core.link_suite.run(arena, init.gpa, parsed.value, core.link_suite.official_criteria, recorder);
    if (recorder != null) std.debug.print("{d} recordings written to {s}\n", .{ writer.count, args[3] });

    const json = try std.json.Stringify.valueAlloc(arena, provenance(report), .{ .whitespace = .indent_2 });
    try std.Io.Dir.cwd().writeFile(init.io, .{ .sub_path = args[1], .data = json });

    _ = printSummary(report);
    std.debug.print("report written to {s}\n", .{args[1]});
    if (!allPass(report)) std.process.exit(1);
}

fn coupler(init: std.process.Init, arena: std.mem.Allocator, out_path: []const u8, recordings_dir: ?[]const u8) !void {
    const parsed = try core.coupler_criteria.parse(arena, core.coupler_criteria.coupler_v1_json);
    var writer: RecordingWriter = .{ .io = init.io, .dir = undefined };
    var recorder: ?core.coupler_suite.Recorder = null;
    if (recordings_dir) |d| {
        try std.Io.Dir.cwd().createDirPath(init.io, d);
        writer.dir = try std.Io.Dir.cwd().openDir(init.io, d, .{});
        recorder = .{ .ptr = &writer, .emit = RecordingWriter.emit };
    }
    const report = try core.coupler_suite.run(arena, init.gpa, parsed.value, core.coupler_suite.official_criteria, recorder);
    if (recordings_dir) |d| std.debug.print("{d} recordings written to {s}\n", .{ writer.count, d });
    const out: CouplerOutput = .{
        .code_revision = std.mem.trim(u8, @embedFile("git_revision"), " \n\r"),
        .working_tree_dirty = std.mem.trim(u8, @embedFile("git_status"), " \n\r").len != 0,
        .optimize_mode = @tagName(@import("builtin").mode),
        .target = build_info.target,
        .zig_version = @import("builtin").zig_version_string,
        .report = report,
    };
    const json = try std.json.Stringify.valueAlloc(arena, out, .{ .whitespace = .indent_2 });
    try std.Io.Dir.cwd().writeFile(init.io, .{ .sub_path = out_path, .data = json });
    const ok = printCouplerSummary(report);
    std.debug.print("report written to {s}\n", .{out_path});
    if (!ok) std.process.exit(1);
}

fn printCouplerSummary(report: core.coupler_suite.Report) bool {
    var all_pass = true;
    std.debug.print("coupler-engagement qualification (label: {s}), criteria {s}\n", .{ report.label, report.criteria_sha256[0..12] });
    for (report.cases) |c| {
        std.debug.print("  {s:<32} {s:<10} (evaluated {d}, outside envelope {d})\n", .{ c.case_id, @tagName(c.outcome), c.evaluated, c.outside_envelope });
        for (c.combinations) |cb| {
            if (cb.status != .fail) continue;
            for (cb.sub_runs) |s| for (s.metrics) |m| if (!m.passed) {
                std.debug.print("      {s} dt={d}us {s}: {?e} (limit {s} {e})\n", .{ cb.grid_id, cb.physics_step_ticks, m.name, m.value, if (m.at_least) ">=" else "<=", m.limit });
            };
            if (cb.sub_runs.len == 0) std.debug.print("      {s} dt={d}us failed\n", .{ cb.grid_id, cb.physics_step_ticks });
        }
        if (c.outcome != .pass) all_pass = false;
    }
    printCaptureSummary(report);
    printAuditDiscrimination(report);
    return all_pass;
}

/// C8 is reported, never gated on its class: capture radii per
/// (pair, direction, theta0, v) at each timestep, with the counts.
fn printCaptureSummary(report: core.coupler_suite.Report) void {
    const s = report.capture_summary;
    std.debug.print("  C8 capture sweep: {d} runs, {d} evaluated, {d} outside_model (listed, not counted), {d} with failing audits, {d} offsets with dt_disagreement\n", .{ s.runs, s.evaluated, s.outside_model, s.audit_failed_runs, s.dt_disagreement_offsets });
    std.debug.print("      classes (valid runs): captured {d}, partial {d}, separated {d}, latch_blocked {d}, missed {d}; {d} runs replayed for C10\n", .{ s.captured, s.partial, s.separated, s.latch_blocked, s.missed, s.replayed_runs });
    std.debug.print("      capture radius [mm] per pair / direction / theta0 [rad] / v [m/s]; columns are timesteps (- = none captured; * = dt_disagreement)\n", .{});
    var i: usize = 0;
    while (i < report.capture_sweep.len) {
        const first = report.capture_sweep[i];
        std.debug.print("      {s:<7} {s:<13} th={d:<5} v={d:<5}", .{ first.friction_pair, first.offset_direction, first.misalignment_rad, first.approach_speed_m_s });
        var j = i;
        while (j < report.capture_sweep.len) : (j += 1) {
            const e = report.capture_sweep[j];
            if (!std.mem.eql(u8, e.friction_pair, first.friction_pair) or !std.mem.eql(u8, e.offset_direction, first.offset_direction) or e.misalignment_rad != first.misalignment_rad or e.approach_speed_m_s != first.approach_speed_m_s) break;
            if (e.capture_radius_m) |r| {
                std.debug.print("  {d}us: {d:.0}{s}", .{ e.physics_step_ticks, r * 1000.0, if (e.dt_disagreement) "*" else "" });
            } else {
                std.debug.print("  {d}us: -{s}", .{ e.physics_step_ticks, if (e.dt_disagreement) "*" else "" });
            }
        }
        std.debug.print("\n", .{});
        i = j;
    }
}

fn printAuditDiscrimination(report: core.coupler_suite.Report) void {
    std.debug.print("  C9 audit discrimination (controls are labeled `control`, never counted in C8):\n", .{});
    for (report.audit_discrimination) |e| {
        std.debug.print("      {s:<8} {s:<36} dt={d}us named audit {s:<18} requirement {s}; tripped:", .{ e.label, e.control, e.physics_step_ticks, e.named_audit, if (e.requirement_met) "met" else "NOT MET" });
        if (e.audits_tripped.len == 0) std.debug.print(" none", .{});
        for (e.audits_tripped) |a| std.debug.print(" {s}", .{a});
        std.debug.print("\n", .{});
    }
}

fn provenance(report: core.link_suite.Report) Output {
    return .{
        .code_revision = std.mem.trim(u8, @embedFile("git_revision"), " \n\r"),
        .working_tree_dirty = std.mem.trim(u8, @embedFile("git_status"), " \n\r").len != 0,
        .optimize_mode = @tagName(@import("builtin").mode),
        .target = build_info.target,
        .zig_version = @import("builtin").zig_version_string,
        .report = report,
    };
}

fn allPass(report: core.link_suite.Report) bool {
    for (report.cases) |c| if (c.outcome != .pass) return false;
    return true;
}

/// Runs every variant of the Q54 sensitivity grid, labeled `exploratory`,
/// writing one report per variant into `dir`. Never sets the exit status
/// from outcomes: the study documents behavior and gates nothing.
fn sensitivity(init: std.process.Init, arena: std.mem.Allocator, dir_path: []const u8) !void {
    const parsed = try core.link_criteria.parse(arena, core.link_criteria.link_v2_json);
    try std.Io.Dir.cwd().createDirPath(init.io, dir_path);
    var dir = try std.Io.Dir.cwd().openDir(init.io, dir_path, .{});
    defer dir.close(init.io);
    for (core.link_suite.sensitivity_variants) |v| {
        const report = try core.link_suite.runWith(arena, init.gpa, parsed.value, core.link_suite.official_criteria, v.config, if (std.meta.eql(v.config, core.link_suite.protocol_config)) "fixture" else "exploratory", null);
        const json = try std.json.Stringify.valueAlloc(arena, provenance(report), .{ .whitespace = .indent_2 });
        const name = try std.fmt.allocPrint(arena, "{s}.json", .{v.name});
        try dir.writeFile(init.io, .{ .sub_path = name, .data = json });
        std.debug.print("== {s} ({s})\n", .{ v.name, report.label });
        _ = printSummary(report);
    }
}

fn printSummary(report: core.link_suite.Report) bool {
    var all_pass = true;
    std.debug.print("compliant-link qualification (label: fixture), criteria {s}\n", .{report.criteria_sha256[0..12]});
    for (report.cases) |c| {
        std.debug.print("  {s:<32} {s:<10} (evaluated {d}, outside envelope {d})\n", .{ c.case_id, @tagName(c.outcome), c.evaluated, c.outside_envelope });
        for (c.combinations) |cb| {
            if (cb.status != .fail) continue;
            for (cb.sub_runs) |s| for (s.metrics) |m| if (!m.passed) {
                std.debug.print("      {s} dt={d}us {s}: {?e} (limit {s} {e})\n", .{ cb.grid_id, cb.physics_step_ticks, m.name, m.value, if (m.at_least) ">=" else "<=", m.limit });
            };
        }
        if (c.outcome != .pass) all_pass = false;
    }
    return all_pass;
}
