//! `kinigami-validate`: runs the analytic fixture-validation suite and writes
//! a JSON report. Usage: kinigami-validate <report.json>
//!
//! Results are labeled `fixture` (Q46). They qualify nothing beyond the
//! declared conditions and are never benchmark or Kin-candidate evidence.

const std = @import("std");
const core = @import("kinigami_core");
const build_info = @import("build_info");

const Output = struct {
    code_revision: []const u8,
    working_tree_dirty: bool,
    optimize_mode: []const u8,
    target: []const u8,
    zig_version: []const u8,
    report: core.fixture_suite.Report,
};

pub fn main(init: std.process.Init) !void {
    const arena = init.arena.allocator();
    const args = try init.minimal.args.toSlice(arena);
    if (args.len != 2) {
        std.debug.print("usage: kinigami-validate <report.json>\n", .{});
        std.process.exit(2);
    }

    const parsed = try core.criteria.parse(arena, core.criteria.analytic_v1_json);
    const report = try core.fixture_suite.run(arena, init.gpa, parsed.value);

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
    std.debug.print("fixture validation (label: fixture), criteria {s}\n", .{report.criteria_sha256[0..12]});
    for (report.cases) |c| {
        var n_pass: usize = 0;
        for (c.combinations) |cb| {
            if (cb.passed) n_pass += 1;
        }
        std.debug.print("  {s:<32} {s:<10} ({d}/{d} combinations)\n", .{ c.case_id, @tagName(c.outcome), n_pass, c.combinations.len });
        for (c.combinations) |cb| {
            if (cb.passed) continue;
            for (cb.sub_runs) |s| for (s.metrics) |m| if (!m.passed()) {
                std.debug.print("      {s} dt={d}us {s}.{s}: {e} (limit {s} {e})\n", .{ cb.friction_id, cb.physics_step_ticks, s.name, m.name, m.value, if (m.at_least) ">=" else "<=", m.limit });
            };
        }
        if (c.outcome != .pass) all_pass = false;
    }
    std.debug.print("report written to {s}\n", .{args[1]});
    if (!all_pass) std.process.exit(1);
}
