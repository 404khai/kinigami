//! `kinigami-qualify`: runs the compliant-link qualification suite (Q52) and
//! writes a JSON report. Usage: kinigami-qualify <report.json>
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

pub fn main(init: std.process.Init) !void {
    const arena = init.arena.allocator();
    const args = try init.minimal.args.toSlice(arena);
    const usage = "usage: kinigami-qualify <report.json>\n       kinigami-qualify --sensitivity <dir>   (exploratory, Q54)\n";
    if (args.len != 2 and !(args.len == 3 and std.mem.eql(u8, args[1], "--sensitivity"))) {
        std.debug.print(usage, .{});
        std.process.exit(2);
    }
    if (args.len == 3) return sensitivity(init, arena, args[2]);

    // Official criteria: v2 (Q53). v1 run 1 is preserved as superseded evidence.
    const parsed = try core.link_criteria.parse(arena, core.link_criteria.link_v2_json);
    const report = try core.link_suite.run(arena, init.gpa, parsed.value, core.link_suite.official_criteria);

    const json = try std.json.Stringify.valueAlloc(arena, provenance(report), .{ .whitespace = .indent_2 });
    try std.Io.Dir.cwd().writeFile(init.io, .{ .sub_path = args[1], .data = json });

    _ = printSummary(report);
    std.debug.print("report written to {s}\n", .{args[1]});
    if (!allPass(report)) std.process.exit(1);
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
        const report = try core.link_suite.runWith(arena, init.gpa, parsed.value, core.link_suite.official_criteria, v.config, if (std.meta.eql(v.config, core.link_suite.protocol_config)) "fixture" else "exploratory");
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
