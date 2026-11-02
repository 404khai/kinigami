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
    if (args.len != 2) {
        std.debug.print("usage: kinigami-qualify <report.json>\n", .{});
        std.process.exit(2);
    }

    // Official criteria: v2 (Q53). v1 run 1 is preserved as superseded evidence.
    const parsed = try core.link_criteria.parse(arena, core.link_criteria.link_v2_json);
    const report = try core.link_suite.run(arena, init.gpa, parsed.value, core.link_suite.official_criteria);

    const out: Output = .{
        .code_revision = std.mem.trim(u8, @embedFile("git_revision"), " \n\r"),
        .working_tree_dirty = std.mem.trim(u8, @embedFile("git_status"), " \n\r").len != 0,
        .optimize_mode = @tagName(@import("builtin").mode),
        .target = build_info.target,
        .zig_version = @import("builtin").zig_version_string,
        .report = report,
    };
    const json = try std.json.Stringify.valueAlloc(arena, out, .{ .whitespace = .indent_2 });
    try std.Io.Dir.cwd().writeFile(init.io, .{ .sub_path = args[1], .data = json });

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
    std.debug.print("report written to {s}\n", .{args[1]});
    if (!all_pass) std.process.exit(1);
}
