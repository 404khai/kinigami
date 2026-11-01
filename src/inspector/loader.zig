//! Loads a format-v2 recording (Q51) into scene frames using the core's
//! reusable reader (INS-003). Every value shown comes from the recording; the
//! loader computes nothing physical (INS-005).

const std = @import("std");
const core = @import("kinigami_core");
const scene_view = @import("scene_view.zig");

pub const Loaded = struct {
    frames: []const scene_view.SceneFrame,
    /// From the recorded effective configuration.
    run_class: []const u8,
    /// Result-label ceiling implied by the run class (PRC-005).
    label: []const u8,
    title: []const u8,
    physics_step_s: f64,
};

pub const LoadError = core.recording.ReadError || core.scene_record.DecodeError || error{ NotVersion2, InvalidConfig, OutOfMemory };

pub fn load(arena: std.mem.Allocator, bytes: []const u8) LoadError!Loaded {
    const rec = try core.recording.Recording.parse(bytes);
    if (rec.version != 2) return error.NotVersion2;
    const header = try core.scene_record.decodeHeader(arena, rec.scene_header.?);

    const cfg = std.json.parseFromSliceLeaky(std.json.Value, arena, rec.effective_config, .{}) catch return error.InvalidConfig;
    if (cfg != .object) return error.InvalidConfig;
    const run_class = str(cfg, "run_class") orelse return error.InvalidConfig;
    const label = if (std.mem.eql(u8, run_class, "fixture_validation")) "FIXTURE" else if (std.mem.eql(u8, run_class, "oracle_diagnostic")) "ORACLE" else "EXPLORATORY";
    const title = try std.fmt.allocPrint(arena, "{s} / {s} / {s} / dt {d} µs", .{
        str(cfg, "case_id") orelse "?",
        str(cfg, "sub_run") orelse "?",
        str(cfg, "friction_id") orelse "?",
        header.physics_step_ticks,
    });

    const unit_s = @as(f64, @floatFromInt(header.time_unit_numerator_s)) / @as(f64, @floatFromInt(header.time_unit_denominator_s));
    const frames = try arena.alloc(scene_view.SceneFrame, rec.snapshot_count);
    var it = rec.snapshots();
    for (frames) |*f| {
        const s = try core.scene_record.decodeSnapshot(arena, header, it.next().?);
        const bodies = try arena.alloc(scene_view.Body, s.bodies.len);
        for (bodies, s.bodies, header.bodies) |*b, st, info| b.* = .{
            .position_m = st.position_m,
            .orientation = .{ .w = st.orientation[0], .x = st.orientation[1], .y = st.orientation[2], .z = st.orientation[3] },
            .half_extents_m = info.half_extents_m,
            .is_fixture = info.kind == .fixture,
        };
        const contacts = try arena.alloc(scene_view.Contact, s.contacts.len);
        for (contacts, s.contacts) |*c, r| c.* = .{
            .point_m = r.point_m,
            .normal_force_n = r.normal_force_n,
            .tangential_force_n = r.tangential_force_n,
        };
        f.* = .{
            .tick = s.tick,
            .time_s = @as(f64, @floatFromInt(s.tick)) * unit_s,
            .bodies = bodies,
            .contacts = contacts,
            .velocities_m_s = try velocities(arena, s),
        };
    }
    return .{
        .frames = frames,
        .run_class = run_class,
        .label = label,
        .title = title,
        .physics_step_s = @as(f64, @floatFromInt(header.physics_step_ticks)) * unit_s,
    };
}

fn velocities(arena: std.mem.Allocator, s: core.scene_record.Snapshot) ![]const scene_view.Vec3 {
    const v = try arena.alloc(scene_view.Vec3, s.bodies.len);
    for (v, s.bodies) |*o, b| o.* = b.velocity_m_s;
    return v;
}

fn str(v: std.json.Value, key: []const u8) ?[]const u8 {
    const x = v.object.get(key) orelse return null;
    return if (x == .string) x.string else null;
}

test "loads a v2 recording into frames with recorded values only" {
    const gpa = std.testing.allocator;
    var arena_state = std.heap.ArenaAllocator.init(gpa);
    defer arena_state.deinit();
    const arena = arena_state.allocator();
    const sr = core.scene_record;

    var w = try core.recording.Writer.init(gpa, "{\"run_class\":\"fixture_validation\",\"case_id\":\"rest\",\"sub_run\":\"rest\",\"friction_id\":\"mu_low\"}");
    defer w.deinit();
    var hb: core.canonical.BufferSink = .{ .gpa = arena };
    try sr.encodeHeader(hb.encoder(), .{ .time_unit_numerator_s = 1, .time_unit_denominator_s = 1_000_000, .physics_step_ticks = 500, .snapshot_interval_steps = 1, .bodies = &.{.{ .id = "b", .kind = .fixture, .shape = .cuboid, .half_extents_m = .{ 0.02, 0.02, 0.01 }, .mass_kg = 0.04 }} });
    try w.sceneHeader(hb.list.items);
    for (0..3) |k| {
        var sb: core.canonical.BufferSink = .{ .gpa = arena };
        try sr.encodeSnapshot(sb.encoder(), .{
            .tick = k * 500,
            .bodies = &.{.{ .position_m = .{ 0.001 * @as(f64, @floatFromInt(k)), 0, 0.01 }, .orientation = .{ 1, 0, 0, 0 }, .velocity_m_s = .{ 0.5, 0, 0 }, .angular_velocity_rad_s = .{ 0, 0, 0 } }},
            .contacts = &.{.{ .body_a = 0, .body_b = sr.tabletop, .point_m = .{ 0.02, 0.02, 0 }, .normal = .{ 0, 0, 1 }, .normal_force_n = 0.098, .tangential_force_n = .{ -0.02, 0, 0 } }},
        });
        try w.snapshot(sb.list.items);
    }
    const bytes = try w.finish();
    defer gpa.free(bytes);

    const l = try load(arena, bytes);
    try std.testing.expectEqual(@as(usize, 3), l.frames.len);
    try std.testing.expectEqualStrings("FIXTURE", l.label);
    try std.testing.expectEqual(@as(u64, 1000), l.frames[2].tick);
    try std.testing.expectEqual(@as(f64, 0.001), l.frames[2].time_s);
    try std.testing.expectEqual(@as(f64, 0.002), l.frames[2].bodies[0].position_m[0]);
    try std.testing.expectEqual(@as(f64, 0.098), l.frames[1].contacts.?[0].normal_force_n);
}

test "version-1 recordings are rejected with a clear error, not misread" {
    const gpa = std.testing.allocator;
    var sink: core.canonical.BufferSink = .{ .gpa = gpa };
    defer sink.deinit();
    const e = sink.encoder();
    try e.bytesRaw(core.recording.magic);
    try e.int(u16, 1);
    try e.int(u16, 0);
    try e.int(u32, 1);
    try e.bytes("{}");
    try e.int(u32, 0xFFFF_FFFF);
    try e.int(u64, 0);
    try std.testing.expectError(error.NotVersion2, load(gpa, sink.list.items));
}
