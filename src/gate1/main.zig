//! `kinigami-gate1`: evaluates Gate 1 paper-gate declarations (Q38, Q61, Q62)
//! and writes a JSON report.
//! Usage: kinigami-gate1 <report.json> <candidate dir>...
//!
//! Each candidate directory holds `declaration.json` and, once written, the
//! independent review records `retention-review-v<version>-r<n>.md` and
//! `originality-review-gate1-v<version>-r<n>.md` (protocol sections 8 and 9).
//! A declaration that fails strict parsing is reported as `rejected` with the
//! reason and gets no outcome. Results are labeled `exploratory`: a paper-gate
//! pass never becomes `validated_acceptance`.
//!
//! The exit status is 0 only when every candidate evaluates to `pass`.

const std = @import("std");
const core = @import("kinigami_core");
const build_info = @import("build_info");

const gate1 = core.gate1_eval;

const Entry = struct {
    directory: []const u8,
    declaration_sha256: ?[]const u8,
    status: []const u8,
    rejection: ?[]const u8,
    report: ?gate1.CandidateReport,
};

const Output = struct {
    code_revision: []const u8,
    working_tree_dirty: bool,
    optimize_mode: []const u8,
    target: []const u8,
    zig_version: []const u8,
    label: []const u8,
    criteria_path: []const u8,
    criteria_sha256: []const u8,
    protocol_path: []const u8,
    protocol_revision: u32,
    candidates: []const Entry,
};

pub fn main(init: std.process.Init) !void {
    const arena = init.arena.allocator();
    const args = try init.minimal.args.toSlice(arena);
    if (args.len < 3) {
        std.debug.print("usage: kinigami-gate1 <report.json> <candidate dir>...\n", .{});
        std.process.exit(2);
    }
    const criteria = try core.gate1_criteria.parse(arena, core.gate1_criteria.gate1_v1_json);

    var entries: std.ArrayList(Entry) = .empty;
    var all_pass = true;
    for (args[2..]) |dir_arg| {
        const entry = try evaluateDirectory(init, arena, criteria.value, dir_arg);
        if (entry.report) |r| {
            if (r.outcome != .pass) all_pass = false;
        } else all_pass = false;
        try entries.append(arena, entry);
    }

    const out: Output = .{
        .code_revision = std.mem.trim(u8, @embedFile("git_revision"), " \n\r"),
        .working_tree_dirty = std.mem.trim(u8, @embedFile("git_status"), " \n\r").len != 0,
        .optimize_mode = @tagName(@import("builtin").mode),
        .target = build_info.target,
        .zig_version = @import("builtin").zig_version_string,
        .label = gate1.label,
        .criteria_path = "criteria/gates/gate1-v1.json",
        .criteria_sha256 = core.gate1_criteria.gate1_v1_sha256,
        .protocol_path = criteria.value.protocol.path,
        .protocol_revision = criteria.value.protocol.revision,
        .candidates = entries.items,
    };
    const json = try std.json.Stringify.valueAlloc(arena, out, .{ .whitespace = .indent_2 });
    try std.Io.Dir.cwd().writeFile(init.io, .{ .sub_path = args[1], .data = json });

    std.debug.print("gate 1 paper gate (label: {s}), criteria {s}\n", .{ gate1.label, core.gate1_criteria.gate1_v1_sha256[0..12] });
    for (entries.items) |e| printEntry(e);
    std.debug.print("report written to {s}\n", .{args[1]});
    if (!all_pass) std.process.exit(1);
}

fn printEntry(e: Entry) void {
    if (e.report) |r| {
        std.debug.print("  {s} v{d}: {s}\n", .{ r.candidate_id, r.candidate_version, @tagName(r.outcome) });
        for (r.items) |it| {
            std.debug.print("      {s} {s}", .{ it.id, @tagName(it.outcome) });
            for (it.reasons) |reason| std.debug.print("  [{s}]", .{reason});
            std.debug.print("\n", .{});
        }
    } else {
        std.debug.print("  {s}: rejected ({s})\n", .{ e.directory, e.rejection orelse "unknown" });
    }
}

fn baseName(path: []const u8) []const u8 {
    const trimmed = std.mem.trimEnd(u8, path, "/");
    const at = std.mem.lastIndexOfScalar(u8, trimmed, '/') orelse return trimmed;
    return trimmed[at + 1 ..];
}

fn rejected(directory: []const u8, sha: ?[]const u8, reason: []const u8) Entry {
    return .{ .directory = directory, .declaration_sha256 = sha, .status = "rejected", .rejection = reason, .report = null };
}

fn evaluateDirectory(init: std.process.Init, arena: std.mem.Allocator, criteria: core.gate1_criteria.Criteria, dir_path: []const u8) !Entry {
    const cwd = std.Io.Dir.cwd();
    const decl_path = try std.fmt.allocPrint(arena, "{s}/declaration.json", .{std.mem.trimEnd(u8, dir_path, "/")});
    const bytes = cwd.readFileAlloc(init.io, decl_path, arena, .limited(16 << 20)) catch |err| {
        return rejected(dir_path, null, try std.fmt.allocPrint(arena, "declaration_unreadable:{s}", .{@errorName(err)}));
    };
    const sha = try arena.dupe(u8, &core.identity.toHex(core.identity.fileIdentity(bytes)));
    const parsed = core.gate1_declaration.parse(arena, bytes, baseName(dir_path)) catch |err| {
        return rejected(dir_path, sha, @errorName(err));
    };
    const d = parsed.value;

    const retention_prefix = try std.fmt.allocPrint(arena, "retention-review-v{d}-r", .{d.candidate_version});
    const originality_prefix = try std.fmt.allocPrint(arena, "originality-review-gate1-v{d}-r", .{d.candidate_version});
    var retention: std.ArrayList(gate1.RecordFile) = .empty;
    var originality: std.ArrayList(gate1.RecordFile) = .empty;

    var dir = cwd.openDir(init.io, dir_path, .{ .iterate = true }) catch |err| {
        return rejected(dir_path, sha, try std.fmt.allocPrint(arena, "directory_unreadable:{s}", .{@errorName(err)}));
    };
    defer dir.close(init.io);
    var it = dir.iterate();
    while (try it.next(init.io)) |entry| {
        if (entry.kind != .file) continue;
        const list = if (recordRevision(entry.name, retention_prefix) != null) &retention else if (recordRevision(entry.name, originality_prefix) != null) &originality else continue;
        const prefix = if (list == &retention) retention_prefix else originality_prefix;
        const revision = recordRevision(entry.name, prefix).?;
        const path = try std.fmt.allocPrint(arena, "{s}/{s}", .{ std.mem.trimEnd(u8, dir_path, "/"), entry.name });
        const text = cwd.readFileAlloc(init.io, path, arena, .limited(4 << 20)) catch continue;
        try list.append(arena, .{ .revision = revision, .text = text });
    }

    const report = try gate1.evaluate(arena, criteria, d, .{
        .declaration_sha256 = sha,
        .retention_records = retention.items,
        .originality_records = originality.items,
    });
    return .{ .directory = dir_path, .declaration_sha256 = sha, .status = "evaluated", .rejection = null, .report = report };
}

/// `<prefix><n>.md` with a canonical decimal revision, else null.
fn recordRevision(name: []const u8, prefix: []const u8) ?u32 {
    if (!std.mem.startsWith(u8, name, prefix) or !std.mem.endsWith(u8, name, ".md")) return null;
    const digits = name[prefix.len .. name.len - 3];
    if (digits.len == 0 or (digits.len > 1 and digits[0] == '0')) return null;
    return std.fmt.parseInt(u32, digits, 10) catch null;
}
