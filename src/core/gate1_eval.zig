//! Gate 1 paper-gate evaluator (Q38, Q61, Q62; protocol
//! `docs/validation/gate1-v1-protocol.md`, revision 1).
//!
//! Evaluates one validated declaration against the preregistered criteria and
//! produces one outcome per item, G1..G8, and one per candidate (fail beats
//! unresolved beats pass). Results are labeled `exploratory`: a paper-gate
//! pass never becomes `validated_acceptance`. An evaluator error or an
//! incomplete computation yields `unresolved`, never `pass`.
//!
//! The module is pure: it reads no files. Review records (G6 retention
//! review, G7/G8 originality review) are handed in as text by the caller.
//! Geometry is computed in binary64 from the integer inputs in a fixed order,
//! so the same declaration and build give the same result.

const std = @import("std");
const math3 = @import("math3.zig");
const crit = @import("gate1_criteria.zig");
const decl_mod = @import("gate1_declaration.zig");

const Vec3 = math3.Vec3;
const Quat = math3.Quat;
const Declaration = decl_mod.Declaration;
const Primitive = decl_mod.Primitive;
const Allocator = std.mem.Allocator;

pub const label = "exploratory";

pub const Outcome = enum { pass, fail, unresolved };

pub const ItemResult = struct {
    id: []const u8,
    outcome: Outcome,
    reasons: []const []const u8,
};

pub const RecordFile = struct {
    revision: u32,
    text: []const u8,
};

pub const Inputs = struct {
    /// Lowercase hex SHA-256 of the exact declaration file bytes.
    declaration_sha256: []const u8,
    /// Files `retention-review-v<version>-r<n>.md` found for this candidate.
    retention_records: []const RecordFile = &.{},
    /// Files `originality-review-gate1-v<version>-r<n>.md` found for this candidate.
    originality_records: []const RecordFile = &.{},
};

// --- Report types

pub const G1Values = struct {
    primitives_considered: u32 = 0,
    seed_points: u32 = 0,
    welzl_centre_um: ?[3]f64 = null,
    welzl_radius_um: ?f64 = null,
    certified_radius_um: ?f64 = null,
    /// D = 2 * certified radius; a conservative upper bound for round parts.
    diameter_um: ?f64 = null,
    limit_um: f64 = 0,
    band_um: f64 = 0,
};

pub const PairId = struct { a: []const u8, b: []const u8 };

pub const G2Values = struct {
    pairs_tested: u32 = 0,
    interfering_pairs: []const PairId = &.{},
    capped_pairs: []const PairId = &.{},
    boxes_outside_shell: []const []const u8 = &.{},
    cavity_primitives: u32 = 0,
    assembly_access_statement_present: bool = false,
};

pub const G4Values = struct {
    declared_total_mass_mg: u64 = 0,
    summed_mass_mg: u64 = 0,
    p_peak_mw: u64 = 0,
    p_lim_mw: ?f64 = null,
    p_avg_mw: u64 = 0,
    /// "reported" or "not_applicable" (average power 0). Never gates.
    endurance_status: []const u8 = "not_applicable",
    /// energy_mj / p_avg_mw: millijoules over milliwatts is seconds.
    endurance_s: ?f64 = null,
    /// The protocol text writes energy_mj * 1000 / p_avg_mw; kept for traceability.
    endurance_s_protocol_literal: ?f64 = null,
    endurance_enters_outcome: bool = false,
    endurance_threshold: []const u8 = "unresolved",
};

pub const RollResult = struct {
    roll_deg: f64,
    status: []const u8,
    table_contact: bool = false,
    static_support: bool = false,
    no_interference: bool = false,
    sites_meet: bool = false,
    detail: []const u8 = "",
};

pub const G5Values = struct {
    coupler_sites: u32 = 0,
    rolls: []const RollResult = &.{},
    roll_deg_used: ?f64 = null,
};

pub const CandidateReport = struct {
    candidate_id: []const u8,
    candidate_version: u32,
    family: []const u8,
    label: []const u8 = label,
    declaration_sha256: []const u8,
    outcome: Outcome,
    failed_items: []const []const u8,
    unresolved_items: []const []const u8,
    items: []const ItemResult,
    g1: G1Values,
    g2: G2Values,
    g4: G4Values,
    g5: G5Values,
};

// --- Entry point

pub fn evaluate(arena: Allocator, c: crit.Criteria, d: Declaration, inputs: Inputs) Allocator.Error!CandidateReport {
    const g1 = try evalG1(arena, c.items[0].params, d);
    const g2 = try evalG2(arena, c.items[1].params, d);
    const g3 = try evalG3(arena, c, d);
    const g4 = try evalG4(arena, c.items[3].params, d);
    const g5 = try evalG5(arena, c, d);
    const g6 = try evalG6(arena, d, inputs);
    const rev = try selectOriginality(arena, d, inputs);
    const g7 = try evalG7(arena, rev);
    const g8 = try evalG8(arena, rev);

    const items = try arena.dupe(ItemResult, &.{ g1.item, g2.item, g3, g4.item, g5.item, g6, g7, g8 });
    var failed: std.ArrayList([]const u8) = .empty;
    var unresolved: std.ArrayList([]const u8) = .empty;
    for (items) |it| switch (it.outcome) {
        .fail => try failed.append(arena, it.id),
        .unresolved => try unresolved.append(arena, it.id),
        .pass => {},
    };
    return .{
        .candidate_id = d.candidate_id,
        .candidate_version = d.candidate_version,
        .family = @tagName(d.family),
        .declaration_sha256 = inputs.declaration_sha256,
        .outcome = aggregate(items),
        .failed_items = try failed.toOwnedSlice(arena),
        .unresolved_items = try unresolved.toOwnedSlice(arena),
        .items = items,
        .g1 = g1.values,
        .g2 = g2.values,
        .g4 = g4.values,
        .g5 = g5.values,
    };
}

/// Protocol section 10: any fail is fail; else any unresolved is unresolved.
pub fn aggregate(items: []const ItemResult) Outcome {
    var any_unresolved = false;
    for (items) |it| switch (it.outcome) {
        .fail => return .fail,
        .unresolved => any_unresolved = true,
        .pass => {},
    };
    return if (any_unresolved) .unresolved else .pass;
}

/// Item outcome from collected reasons: a definite failure dominates.
fn combine(fails: usize, unresolved: usize) Outcome {
    if (fails > 0) return .fail;
    if (unresolved > 0) return .unresolved;
    return .pass;
}

const Reasons = struct {
    fails: std.ArrayList([]const u8) = .empty,
    unresolved: std.ArrayList([]const u8) = .empty,

    fn fail(self: *Reasons, a: Allocator, r: []const u8) !void {
        try self.fails.append(a, r);
    }
    fn unres(self: *Reasons, a: Allocator, r: []const u8) !void {
        try self.unresolved.append(a, r);
    }
    fn result(self: *Reasons, a: Allocator, id: []const u8) !ItemResult {
        var all: std.ArrayList([]const u8) = .empty;
        for (self.fails.items) |r| try all.append(a, try std.fmt.allocPrint(a, "fail: {s}", .{r}));
        for (self.unresolved.items) |r| try all.append(a, try std.fmt.allocPrint(a, "unresolved: {s}", .{r}));
        return .{ .id = id, .outcome = combine(self.fails.items.len, self.unresolved.items.len), .reasons = try all.toOwnedSlice(a) };
    }
};

// --- Geometry primitives

const Shape = struct {
    kind: decl_mod.PrimitiveKind,
    /// Sphere and cylinder radius (µm).
    r: f64 = 0,
    /// Box half extents, or (0, 0, half_height) for a cylinder (µm).
    h: Vec3 = math3.zero,
    c: Vec3,
    q: Quat,
};

fn vecOf(p: [3]i64) Vec3 {
    return .{ @floatFromInt(p[0]), @floatFromInt(p[1]), @floatFromInt(p[2]) };
}

fn quatOf(o: [4]f64) Quat {
    return (Quat{ .w = o[0], .x = o[1], .y = o[2], .z = o[3] }).normalized();
}

fn shapeOfPrimitive(p: Primitive) Shape {
    var s: Shape = .{ .kind = p.kind, .c = vecOf(p.pose.position_um), .q = quatOf(p.pose.orientation) };
    switch (p.kind) {
        .sphere => s.r = @floatFromInt(p.radius_um.?),
        .box => {
            const h = p.half_extent_um.?;
            s.h = .{ @floatFromInt(h[0]), @floatFromInt(h[1]), @floatFromInt(h[2]) };
        },
        .cylinder => {
            s.r = @floatFromInt(p.radius_um.?);
            s.h = .{ 0, 0, @floatFromInt(p.half_height_um.?) };
        },
    }
    return s;
}

fn shapeOfBox(b: decl_mod.ComponentBox) Shape {
    const h = b.half_extent_um;
    return .{
        .kind = .box,
        .h = .{ @floatFromInt(h[0]), @floatFromInt(h[1]), @floatFromInt(h[2]) },
        .c = vecOf(b.pose.position_um),
        .q = quatOf(b.pose.orientation),
    };
}

/// Shape moved by a rigid transform (rotation `rq`, then translation `t`).
fn transformShape(s: Shape, rq: Quat, t: Vec3) Shape {
    var out = s;
    out.c = math3.add(rq.rotate(s.c), t);
    out.q = rq.mul(s.q);
    return out;
}

/// Erodes by `delta` (protocol section 4). Null when the shape becomes empty.
fn erode(s: Shape, delta: f64) ?Shape {
    var out = s;
    switch (s.kind) {
        .sphere => {
            out.r = s.r - delta;
            if (!(out.r > 0)) return null;
        },
        .box => {
            out.h = .{ s.h[0] - delta, s.h[1] - delta, s.h[2] - delta };
            if (!(out.h[0] > 0 and out.h[1] > 0 and out.h[2] > 0)) return null;
        },
        .cylinder => {
            out.r = s.r - delta;
            out.h = .{ 0, 0, s.h[2] - delta };
            if (!(out.r > 0 and out.h[2] > 0)) return null;
        },
    }
    return out;
}

fn sgn(x: f64) f64 {
    return if (x < 0) -1.0 else 1.0; // sgn(0) = +1
}

/// Support point in the world frame for the world direction `d`.
fn support(s: Shape, d: Vec3) Vec3 {
    const dl = s.q.rotateInverse(d);
    const local: Vec3 = switch (s.kind) {
        .sphere => math3.scale(dl, s.r),
        .box => .{ sgn(dl[0]) * s.h[0], sgn(dl[1]) * s.h[1], sgn(dl[2]) * s.h[2] },
        .cylinder => blk: {
            const rho = math3.horizontalLength(dl);
            if (rho == 0) break :blk .{ s.r, 0, sgn(dl[2]) * s.h[2] };
            break :blk .{ s.r * dl[0] / rho, s.r * dl[1] / rho, sgn(dl[2]) * s.h[2] };
        },
    };
    return math3.add(s.c, s.q.rotate(local));
}

/// Signed distance from `p` to a convex shape (negative inside).
fn signedDistance(s: Shape, p: Vec3) f64 {
    const l = s.q.rotateInverse(math3.sub(p, s.c));
    switch (s.kind) {
        .sphere => return math3.length(l) - s.r,
        .box => {
            const q: Vec3 = .{ @abs(l[0]) - s.h[0], @abs(l[1]) - s.h[1], @abs(l[2]) - s.h[2] };
            const out = math3.length(.{ @max(q[0], 0), @max(q[1], 0), @max(q[2], 0) });
            return out + @min(@max(q[0], @max(q[1], q[2])), 0);
        },
        .cylinder => {
            const dr = math3.horizontalLength(l) - s.r;
            const dz = @abs(l[2]) - s.h[2];
            const out = @sqrt(@max(dr, 0) * @max(dr, 0) + @max(dz, 0) * @max(dz, 0));
            return out + @min(@max(dr, dz), 0);
        },
    }
}

// --- GJK boolean test (protocol section 4)

pub const Intersection = enum { separate, interfere, capped };

const gjk_epsilon: f64 = 1e-9;

fn mdSupport(a: Shape, b: Shape, d: Vec3) Vec3 {
    return math3.sub(support(a, d), support(b, math3.scale(d, -1)));
}

const Simplex = struct {
    pts: [4]Vec3 = undefined,
    n: usize = 0,

    /// New point goes first (index 0 is the newest, "a").
    fn push(self: *Simplex, p: Vec3) void {
        var i: usize = if (self.n < 4) self.n else 3;
        while (i > 0) : (i -= 1) self.pts[i] = self.pts[i - 1];
        self.pts[0] = p;
        if (self.n < 4) self.n += 1;
    }
};

fn sameDirection(a: Vec3, b: Vec3) bool {
    return math3.dot(a, b) > 0;
}

/// Returns true when the origin is enclosed. Otherwise updates the simplex
/// and the search direction `d`.
fn nextSimplex(s: *Simplex, d: *Vec3) bool {
    return switch (s.n) {
        2 => lineCase(s, d),
        3 => triangleCase(s, d),
        4 => tetrahedronCase(s, d),
        else => false,
    };
}

fn lineCase(s: *Simplex, d: *Vec3) bool {
    const a = s.pts[0];
    const b = s.pts[1];
    const ab = math3.sub(b, a);
    const ao = math3.scale(a, -1);
    if (sameDirection(ab, ao)) {
        d.* = math3.cross(math3.cross(ab, ao), ab);
    } else {
        s.n = 1;
        d.* = ao;
    }
    return false;
}

fn triangleCase(s: *Simplex, d: *Vec3) bool {
    const a = s.pts[0];
    const b = s.pts[1];
    const c = s.pts[2];
    const ab = math3.sub(b, a);
    const ac = math3.sub(c, a);
    const ao = math3.scale(a, -1);
    const abc = math3.cross(ab, ac);
    if (sameDirection(math3.cross(abc, ac), ao)) {
        if (sameDirection(ac, ao)) {
            s.pts[1] = c;
            s.n = 2;
            d.* = math3.cross(math3.cross(ac, ao), ac);
        } else {
            s.n = 2;
            return lineCase(s, d);
        }
    } else if (sameDirection(math3.cross(ab, abc), ao)) {
        s.n = 2;
        return lineCase(s, d);
    } else if (sameDirection(abc, ao)) {
        d.* = abc;
    } else {
        s.pts[1] = c;
        s.pts[2] = b;
        d.* = math3.scale(abc, -1);
    }
    return false;
}

fn tetrahedronCase(s: *Simplex, d: *Vec3) bool {
    const a = s.pts[0];
    const b = s.pts[1];
    const c = s.pts[2];
    const dd = s.pts[3];
    const ab = math3.sub(b, a);
    const ac = math3.sub(c, a);
    const ad = math3.sub(dd, a);
    const ao = math3.scale(a, -1);
    const abc = math3.cross(ab, ac);
    const acd = math3.cross(ac, ad);
    const adb = math3.cross(ad, ab);
    if (sameDirection(abc, ao)) {
        s.n = 3;
        return triangleCase(s, d);
    }
    if (sameDirection(acd, ao)) {
        s.pts[1] = c;
        s.pts[2] = dd;
        s.n = 3;
        return triangleCase(s, d);
    }
    if (sameDirection(adb, ao)) {
        s.pts[1] = dd;
        s.pts[2] = b;
        s.n = 3;
        return triangleCase(s, d);
    }
    return true;
}

/// GJK boolean test on the Minkowski difference of two convex shapes. Initial
/// direction (1, 0, 0), at most `cap` iterations, termination when the new
/// support point does not pass the origin within 1e-9 µm.
pub fn gjk(a: Shape, b: Shape, cap: u32) Intersection {
    var simplex: Simplex = .{};
    var d: Vec3 = .{ 1, 0, 0 };
    var iter: u32 = 0;
    while (iter < cap) : (iter += 1) {
        const len = math3.length(d);
        // The search direction vanished: the origin lies on the simplex.
        if (!(len > 1e-12)) return .interfere;
        const dn = math3.scale(d, 1.0 / len);
        const w = mdSupport(a, b, dn);
        if (math3.dot(w, dn) < gjk_epsilon) return .separate;
        simplex.push(w);
        if (simplex.n == 1) {
            d = math3.scale(w, -1);
            continue;
        }
        if (nextSimplex(&simplex, &d)) return .interfere;
    }
    return .capped;
}

/// Interference of the eroded shapes (an empty eroded shape never interferes).
pub fn interferes(a: Shape, b: Shape, erosion: f64, cap: u32) Intersection {
    const ea = erode(a, erosion) orelse return .separate;
    const eb = erode(b, erosion) orelse return .separate;
    return gjk(ea, eb, cap);
}

// --- G1: enclosing sphere

const Ball = struct { c: Vec3 = math3.zero, r: f64 = -1, valid: bool = false };

const welzl_step_cap: u64 = 10_000_000;
const inside_slack: f64 = 1e-12;

fn ballInside(b: Ball, p: Vec3) bool {
    if (!b.valid) return false;
    return math3.length(math3.sub(p, b.c)) <= b.r + inside_slack * b.r;
}

fn ballOfTwo(a: Vec3, b: Vec3) Ball {
    const c = math3.scale(math3.add(a, b), 0.5);
    return .{ .c = c, .r = math3.length(math3.sub(a, c)), .valid = true };
}

/// Circumcircle in the plane of three points, or null when collinear.
fn ballOfThree(a: Vec3, b: Vec3, c: Vec3) ?Ball {
    const u = math3.sub(b, a);
    const v = math3.sub(c, a);
    const w = math3.cross(u, v);
    const ww = math3.dot(w, w);
    const uu = math3.dot(u, u);
    const vv = math3.dot(v, v);
    if (!(ww > 1e-18 * uu * vv)) return null;
    const num = math3.add(math3.scale(math3.cross(w, u), vv), math3.scale(math3.cross(v, w), uu));
    const off = math3.scale(num, 1.0 / (2.0 * ww));
    const centre = math3.add(a, off);
    return .{ .c = centre, .r = math3.length(off), .valid = true };
}

/// Circumsphere of four points by the 3x3 linear system (Cramer's rule), or
/// null when coplanar.
fn ballOfFour(a: Vec3, b: Vec3, c: Vec3, e: Vec3) ?Ball {
    const u = math3.sub(b, a);
    const v = math3.sub(c, a);
    const w = math3.sub(e, a);
    const det = math3.dot(u, math3.cross(v, w));
    const scale_ = math3.length(u) * math3.length(v) * math3.length(w);
    if (!(@abs(det) > 1e-12 * scale_)) return null;
    const uu = math3.dot(u, u);
    const vv = math3.dot(v, v);
    const ww = math3.dot(w, w);
    // x = (uu (v x w) + vv (w x u) + ww (u x v)) / (2 det)
    const num = math3.add(math3.add(math3.scale(math3.cross(v, w), uu), math3.scale(math3.cross(w, u), vv)), math3.scale(math3.cross(u, v), ww));
    const off = math3.scale(num, 1.0 / (2.0 * det));
    return .{ .c = math3.add(a, off), .r = math3.length(off), .valid = true };
}

fn containsAll(b: Ball, r: []const Vec3) bool {
    for (r) |p| if (!ballInside(b, p)) return false;
    return true;
}

/// Minimal-dimension fallback for a degenerate support set: the smallest ball
/// through a subset (sizes 1..3, index order) that contains every point.
fn degenerateBall(r: []const Vec3) Ball {
    var best: Ball = .{};
    const n = r.len;
    for (0..n) |i| {
        const b: Ball = .{ .c = r[i], .r = 0, .valid = true };
        if (containsAll(b, r) and (!best.valid or b.r < best.r)) best = b;
    }
    for (0..n) |i| for (i + 1..n) |j| {
        const b = ballOfTwo(r[i], r[j]);
        if (containsAll(b, r) and (!best.valid or b.r < best.r)) best = b;
    };
    for (0..n) |i| for (i + 1..n) |j| for (j + 1..n) |k| {
        if (ballOfThree(r[i], r[j], r[k])) |b| {
            if (containsAll(b, r) and (!best.valid or b.r < best.r)) best = b;
        }
    };
    if (best.valid) return best;
    // No subset ball contains the set: fall back to the farthest pair.
    var far: Ball = .{};
    for (0..n) |i| for (i + 1..n) |j| {
        const b = ballOfTwo(r[i], r[j]);
        if (!far.valid or b.r > far.r) far = b;
    };
    return far;
}

fn circumball(r: []const Vec3) Ball {
    switch (r.len) {
        0 => return .{},
        1 => return .{ .c = r[0], .r = 0, .valid = true },
        2 => return ballOfTwo(r[0], r[1]),
        3 => return ballOfThree(r[0], r[1], r[2]) orelse degenerateBall(r),
        else => return ballOfFour(r[0], r[1], r[2], r[3]) orelse degenerateBall(r),
    }
}

const WelzlError = error{StepCapReached};

const Welzl = struct {
    pts: []const Vec3,
    steps: u64 = 0,

    /// welzl(P, R): removes the points of P in sorted order, last point first.
    fn run(self: *Welzl, n: usize, r_set: *[4]Vec3, r: usize) WelzlError!Ball {
        self.steps += 1;
        if (self.steps > welzl_step_cap) return error.StepCapReached;
        if (n == 0 or r == 4) return circumball(r_set[0..r]);
        const p = self.pts[n - 1];
        const ball = try self.run(n - 1, r_set, r);
        if (ballInside(ball, p)) return ball;
        r_set[r] = p;
        return self.run(n - 1, r_set, r + 1);
    }
};

fn lessVec(_: void, a: Vec3, b: Vec3) bool {
    if (a[0] != b[0]) return a[0] < b[0];
    if (a[1] != b[1]) return a[1] < b[1];
    return a[2] < b[2];
}

/// Seed points of one primitive in the body frame (protocol section 3).
fn appendSeeds(arena: Allocator, list: *std.ArrayList(Vec3), p: Primitive, rim_points: u32) Allocator.Error!void {
    const s = shapeOfPrimitive(p);
    switch (p.kind) {
        .box => {
            for ([_]f64{ -1, 1 }) |sx| for ([_]f64{ -1, 1 }) |sy| for ([_]f64{ -1, 1 }) |sz| {
                const local: Vec3 = .{ sx * s.h[0], sy * s.h[1], sz * s.h[2] };
                try list.append(arena, math3.add(s.c, s.q.rotate(local)));
            };
        },
        .cylinder => {
            for ([_]f64{ -1, 1 }) |side| {
                var k: u32 = 0;
                while (k < rim_points) : (k += 1) {
                    const ang = 2.0 * std.math.pi * @as(f64, @floatFromInt(k)) / @as(f64, @floatFromInt(rim_points));
                    const local: Vec3 = .{ s.r * @cos(ang), s.r * @sin(ang), side * s.h[2] };
                    try list.append(arena, math3.add(s.c, s.q.rotate(local)));
                }
            }
            for ([_]f64{ -1, 1 }) |side| {
                try list.append(arena, math3.add(s.c, s.q.rotate(.{ 0, 0, side * s.h[2] })));
            }
        },
        .sphere => {
            try list.append(arena, s.c);
            const steps = [_]f64{ -1, 0, 1 };
            for (steps) |dx| for (steps) |dy| for (steps) |dz| {
                if (dx == 0 and dy == 0 and dz == 0) continue;
                const u = math3.scale(.{ dx, dy, dz }, 1.0 / math3.length(.{ dx, dy, dz }));
                try list.append(arena, math3.add(s.c, math3.scale(u, s.r)));
            };
        },
    }
}

fn sortedSeeds(arena: Allocator, prims: []const Primitive, roles: []const decl_mod.PrimitiveRole, rim_points: u32) Allocator.Error![]Vec3 {
    var list: std.ArrayList(Vec3) = .empty;
    for (prims) |p| {
        const wanted = for (roles) |r| {
            if (r == p.role) break true;
        } else false;
        if (wanted) try appendSeeds(arena, &list, p, rim_points);
    }
    std.mem.sort(Vec3, list.items, {}, lessVec);
    // Drop exact duplicates.
    var out: usize = 0;
    for (list.items, 0..) |p, i| {
        if (i > 0 and std.meta.eql(p, list.items[out - 1])) continue;
        list.items[out] = p;
        out += 1;
    }
    return list.items[0..out];
}

/// Exact farthest-point distance from `c` to a primitive (protocol section 3).
fn farthest(c: Vec3, s: Shape) f64 {
    switch (s.kind) {
        .sphere => return math3.length(math3.sub(s.c, c)) + s.r,
        .box => {
            var m: f64 = 0;
            for ([_]f64{ -1, 1 }) |sx| for ([_]f64{ -1, 1 }) |sy| for ([_]f64{ -1, 1 }) |sz| {
                const local: Vec3 = .{ sx * s.h[0], sy * s.h[1], sz * s.h[2] };
                const corner = math3.add(s.c, s.q.rotate(local));
                m = @max(m, math3.length(math3.sub(corner, c)));
            };
            return m;
        },
        .cylinder => {
            const axis = s.q.rotate(.{ 0, 0, 1 });
            const rel = math3.sub(c, s.c);
            const t = math3.dot(rel, axis);
            const radial = math3.sub(rel, math3.scale(axis, t));
            const rho = math3.length(radial);
            const ax = @abs(t) + s.h[2];
            const rd = rho + s.r;
            return @sqrt(ax * ax + rd * rd);
        },
    }
}

const G1Result = struct { item: ItemResult, values: G1Values };

pub fn evalG1(arena: Allocator, p: crit.Params, d: Declaration) Allocator.Error!G1Result {
    const limit = p.max_diameter_um.?.value;
    const band = p.uncertain_band_um.?.value;
    const rim = p.round_rim_points.?.value;
    var values: G1Values = .{ .limit_um = limit, .band_um = band };
    var rs: Reasons = .{};

    const roles = [_]decl_mod.PrimitiveRole{ .body, .coupler };
    var considered: u32 = 0;
    for (d.stowed_geometry.primitives) |pr| if (pr.role != .cavity) {
        considered += 1;
    };
    values.primitives_considered = considered;
    if (considered == 0) {
        try rs.unres(arena, "no_stowed_primitives");
        return .{ .item = try rs.result(arena, "G1"), .values = values };
    }

    const seeds = try sortedSeeds(arena, d.stowed_geometry.primitives, &roles, rim);
    values.seed_points = @intCast(seeds.len);
    var w: Welzl = .{ .pts = seeds };
    var r_set: [4]Vec3 = undefined;
    const ball = w.run(seeds.len, &r_set, 0) catch {
        try rs.unres(arena, "computation_not_completed");
        return .{ .item = try rs.result(arena, "G1"), .values = values };
    };

    var r_cert: f64 = 0;
    for (d.stowed_geometry.primitives) |pr| {
        if (pr.role == .cavity) continue;
        r_cert = @max(r_cert, farthest(ball.c, shapeOfPrimitive(pr)));
    }
    const diameter = 2.0 * r_cert;
    values.welzl_centre_um = ball.c;
    values.welzl_radius_um = ball.r;
    values.certified_radius_um = r_cert;
    values.diameter_um = diameter;

    if (@abs(diameter - limit) <= band) {
        try rs.unres(arena, "within_uncertain_band");
    } else if (diameter > limit) {
        try rs.fail(arena, "diameter_above_limit");
    }
    return .{ .item = try rs.result(arena, "G1"), .values = values };
}

// --- G2: packaging

const G2Result = struct { item: ItemResult, values: G2Values };

pub fn evalG2(arena: Allocator, p: crit.Params, d: Declaration) Allocator.Error!G2Result {
    const erosion = p.interference_erosion_um.?.value;
    const tol = p.containment_tolerance_um.?.value;
    const cap = p.gjk_iteration_cap.?.value;
    var values: G2Values = .{};
    var rs: Reasons = .{};

    var interfering: std.ArrayList(PairId) = .empty;
    var capped: std.ArrayList(PairId) = .empty;
    var outside: std.ArrayList([]const u8) = .empty;

    for (d.components, 0..) |a, i| for (d.components[i + 1 ..]) |b| {
        values.pairs_tested += 1;
        switch (interferes(shapeOfBox(a.box), shapeOfBox(b.box), erosion, cap)) {
            .separate => {},
            .interfere => try interfering.append(arena, .{ .a = a.id, .b = b.id }),
            .capped => try capped.append(arena, .{ .a = a.id, .b = b.id }),
        }
    };
    values.interfering_pairs = try interfering.toOwnedSlice(arena);
    values.capped_pairs = try capped.toOwnedSlice(arena);
    if (values.interfering_pairs.len > 0) try rs.fail(arena, "component_boxes_interfere");
    if (values.capped_pairs.len > 0) try rs.unres(arena, "intersection_cap_reached");

    var cavities: std.ArrayList(Shape) = .empty;
    for (d.stowed_geometry.primitives) |pr| if (pr.role == .cavity) try cavities.append(arena, shapeOfPrimitive(pr));
    values.cavity_primitives = @intCast(cavities.items.len);
    if (cavities.items.len == 0) {
        try rs.unres(arena, "cavity_missing");
    } else {
        for (d.components) |c| {
            const box = shapeOfBox(c.box);
            const fits = for (cavities.items) |cav| {
                if (boxInside(box, cav, tol)) break true;
            } else false;
            if (!fits) try outside.append(arena, c.id);
        }
        if (outside.items.len > 0) try rs.fail(arena, "box_outside_shell");
    }
    values.boxes_outside_shell = try outside.toOwnedSlice(arena);

    values.assembly_access_statement_present = std.mem.trim(u8, d.assembly_access.statement, " \t\r\n").len >= 1;
    if (!values.assembly_access_statement_present) try rs.fail(arena, "assembly_access_statement_missing");

    return .{ .item = try rs.result(arena, "G2"), .values = values };
}

fn boxInside(box: Shape, cavity: Shape, tol: f64) bool {
    for ([_]f64{ -1, 1 }) |sx| for ([_]f64{ -1, 1 }) |sy| for ([_]f64{ -1, 1 }) |sz| {
        const local: Vec3 = .{ sx * box.h[0], sy * box.h[1], sz * box.h[2] };
        const corner = math3.add(box.c, box.q.rotate(local));
        if (signedDistance(cavity, corner) > tol) return false;
    };
    return true;
}

// --- G3: evidence

const earliest_access_date = "2000-01-01";

fn isCited(c: decl_mod.Component, declared_on: []const u8) bool {
    const s = c.source orelse return false;
    if (!(std.mem.eql(u8, s.kind, "datasheet") or std.mem.eql(u8, s.kind, "publication"))) return false;
    const scheme: usize = if (std.mem.startsWith(u8, s.url, "https://")) 8 else if (std.mem.startsWith(u8, s.url, "http://")) 7 else return false;
    if (s.url.len <= scheme) return false;
    if (!decl_mod.isValidDate(s.accessed)) return false;
    if (std.mem.order(u8, s.accessed, earliest_access_date) == .lt) return false;
    if (std.mem.order(u8, s.accessed, declared_on) == .gt) return false;
    return true;
}

pub fn evalG3(arena: Allocator, c: crit.Criteria, d: Declaration) Allocator.Error!ItemResult {
    // The derived-mass tolerance (1 mg, provisional) is a G4 parameter.
    const derived_tol = c.items[3].params.derived_mass_tolerance_mg.?.value;
    var rs: Reasons = .{};
    if (d.components.len == 0) try rs.unres(arena, "no_components");
    for (d.components) |comp| {
        if (!isCited(comp, d.declared_on)) {
            try rs.unres(arena, try std.fmt.allocPrint(arena, "uncited_component:{s}", .{comp.id}));
        }
        if (comp.mass_basis == .estimate) try rs.unres(arena, try std.fmt.allocPrint(arena, "mass_basis_estimate:{s}", .{comp.id}));
        if (comp.dimension_basis == .estimate) try rs.unres(arena, try std.fmt.allocPrint(arena, "dimension_basis_estimate:{s}", .{comp.id}));
        if (comp.power_basis == .estimate) try rs.unres(arena, try std.fmt.allocPrint(arena, "power_basis_estimate:{s}", .{comp.id}));
        if (comp.mass_basis == .derived) {
            const dv = comp.derivation.?;
            const derived_mg = dv.density_kg_m3 * dv.volume_m3 * 1.0e6;
            const diff = @abs(@as(f64, @floatFromInt(comp.mass_mg)) - derived_mg);
            if (diff > derived_tol) {
                try rs.fail(arena, try std.fmt.allocPrint(arena, "derived_mass_inconsistent:{s}", .{comp.id}));
            }
        }
    }
    return rs.result(arena, "G3");
}

// --- G4: budgets

const G4Result = struct { item: ItemResult, values: G4Values };

pub fn evalG4(arena: Allocator, p: crit.Params, d: Declaration) Allocator.Error!G4Result {
    _ = p;
    var values: G4Values = .{ .declared_total_mass_mg = d.mass_budget.total_mass_mg };
    var rs: Reasons = .{};

    var source: ?decl_mod.Component = null;
    for (d.components) |c| {
        values.summed_mass_mg += c.mass_mg;
        if (c.kind == .energy_source) {
            source = c;
        } else {
            values.p_peak_mw += c.peak_power_mw;
            values.p_avg_mw += c.average_power_mw;
        }
    }
    if (values.summed_mass_mg != values.declared_total_mass_mg) try rs.fail(arena, "mass_budget_not_equal_to_component_sum");

    const s = source orelse {
        try rs.unres(arena, "budget_input_missing");
        return .{ .item = try rs.result(arena, "G4"), .values = values };
    };
    if (s.rated_continuous_discharge_a) |amps| {
        const lim = s.nominal_voltage_v.? * amps * 1000.0;
        values.p_lim_mw = lim;
        if (@as(f64, @floatFromInt(values.p_peak_mw)) > lim) try rs.fail(arena, "peak_power_above_rated_continuous_discharge");
    } else {
        try rs.unres(arena, "source_without_rated_continuous_discharge");
    }

    // Endurance is reported only. It never changes the outcome.
    if (values.p_avg_mw == 0) {
        values.endurance_status = "not_applicable";
    } else {
        const energy: f64 = @floatFromInt(s.energy_mj.?);
        const avg: f64 = @floatFromInt(values.p_avg_mw);
        values.endurance_status = "reported";
        values.endurance_s = energy / avg;
        values.endurance_s_protocol_literal = energy * 1000.0 / avg;
    }
    return .{ .item = try rs.result(arena, "G4"), .values = values };
}

// --- G5: coupler layout and tabletop chain

const G5Result = struct { item: ItemResult, values: G5Values };

const Unit = struct { q: Quat, t: Vec3 };

fn unitPoint(u: Unit, p: Vec3) Vec3 {
    return math3.add(u.q.rotate(p), u.t);
}

fn axisAngle(axis: Vec3, ang: f64) Quat {
    const s = @sin(ang / 2.0);
    return .{ .w = @cos(ang / 2.0), .x = axis[0] * s, .y = axis[1] * s, .z = axis[2] * s };
}

/// Shortest-arc rotation taking unit vector `u` to unit vector `v`. For the
/// antiparallel case the axis is perpendicular to `u`, taken from the first
/// coordinate axis (x, y, z) least aligned with it.
fn shortestArc(u: Vec3, v: Vec3) Quat {
    const dt = math3.dot(u, v);
    if (dt > -1.0 + 1e-12) {
        const cr = math3.cross(u, v);
        return (Quat{ .w = 1.0 + dt, .x = cr[0], .y = cr[1], .z = cr[2] }).normalized();
    }
    var e: Vec3 = .{ 1, 0, 0 };
    if (@abs(u[1]) < @abs(u[0])) e = .{ 0, 1, 0 };
    if (@abs(u[2]) < @abs(e[0] * u[0] + e[1] * u[1] + e[2] * u[2])) e = .{ 0, 0, 1 };
    const ax = math3.cross(u, e);
    const n = math3.scale(ax, 1.0 / math3.length(ax));
    return .{ .w = 0, .x = n[0], .y = n[1], .z = n[2] };
}

fn cross2(o: [2]f64, a: [2]f64, b: [2]f64) f64 {
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
}

fn lessPoint2(_: void, a: [2]f64, b: [2]f64) bool {
    if (a[0] != b[0]) return a[0] < b[0];
    return a[1] < b[1];
}

/// Convex hull (counter-clockwise, monotone chain) of points sorted in place.
/// A result with fewer than 3 points means zero area.
fn hull2(arena: Allocator, pts: [][2]f64) Allocator.Error![][2]f64 {
    std.mem.sort([2]f64, pts, {}, lessPoint2);
    if (pts.len < 3) return arena.dupe([2]f64, pts);
    var h = try arena.alloc([2]f64, 2 * pts.len);
    var k: usize = 0;
    for (pts) |p| {
        while (k >= 2 and cross2(h[k - 2], h[k - 1], p) <= 0) k -= 1;
        h[k] = p;
        k += 1;
    }
    const lower = k + 1;
    var i: usize = pts.len - 1;
    while (i > 0) : (i -= 1) {
        const p = pts[i - 1];
        while (k >= lower and cross2(h[k - 2], h[k - 1], p) <= 0) k -= 1;
        h[k] = p;
        k += 1;
    }
    return h[0 .. k - 1];
}

fn hullContains(h: []const [2]f64, p: [2]f64) bool {
    if (h.len < 3) return false;
    for (h, 0..) |a, i| {
        const b = h[(i + 1) % h.len];
        if (cross2(a, b, p) < 0) return false;
    }
    return true;
}

fn hullArea(h: []const [2]f64) f64 {
    var a: f64 = 0;
    for (h, 0..) |p, i| {
        const q = h[(i + 1) % h.len];
        a += p[0] * q[1] - q[0] * p[1];
    }
    return a / 2.0;
}

const RollEval = struct { result: RollResult, capped: bool };

fn evalRoll(arena: Allocator, p: crit.Params, cap: u32, d: Declaration, seeds: []const Vec3, roll_deg: f64) Allocator.Error!RollEval {
    const contact_tol = p.contact_tolerance_um.?.value;
    const erosion = p.interference_erosion_um.?.value;
    const n_units = p.chain_units.?.value;
    var out: RollEval = .{ .result = .{ .roll_deg = roll_deg, .status = "fail" }, .capped = false };

    const head = d.coupler_sites[decl_mod.findSite(d.coupler_sites, d.chain.head_site).?];
    const tail = d.coupler_sites[decl_mod.findSite(d.coupler_sites, d.chain.tail_site).?];
    const head_pos = vecOf(head.position_um);
    const tail_pos = vecOf(tail.position_um);
    const tail_n = tail.normal;

    // Unit 1 rests on the table; the rest are mated to their predecessor.
    var units: std.ArrayList(Unit) = .empty;
    const q1 = quatOf(d.chain.rest_orientation);
    var min_z = std.math.inf(f64);
    for (seeds) |s| min_z = @min(min_z, q1.rotate(s)[2]);
    try units.append(arena, .{ .q = q1, .t = .{ 0, 0, -min_z } });

    const psi = roll_deg * std.math.pi / 180.0;
    var sites_meet = true;
    var k: u32 = 1;
    while (k < n_units) : (k += 1) {
        const prev = units.items[k - 1];
        const ph = unitPoint(prev, head_pos);
        const nh = prev.q.rotate(head.normal);
        const base = shortestArc(tail_n, math3.scale(nh, -1));
        const qn = axisAngle(nh, psi).mul(base).normalized();
        const next: Unit = .{ .q = qn, .t = math3.sub(ph, qn.rotate(tail_pos)) };
        const tail_world = unitPoint(next, tail_pos);
        const tail_normal_world = next.q.rotate(tail_n);
        if (math3.length(math3.sub(tail_world, ph)) > contact_tol) sites_meet = false;
        if (math3.length(math3.add(tail_normal_world, nh)) > 1e-9) sites_meet = false;
        try units.append(arena, next);
    }
    out.result.sites_meet = sites_meet;

    // Body-role mass-weighted centre of mass (body frame).
    var m_total: f64 = 0;
    var com: Vec3 = math3.zero;
    for (d.components) |c| {
        const m: f64 = @floatFromInt(c.mass_mg);
        m_total += m;
        com = math3.add(com, math3.scale(vecOf(c.box.pose.position_um), m));
    }
    if (!(m_total > 0)) {
        out.result.detail = "total_mass_zero";
        out.result.status = "unresolved";
        out.capped = true;
        return out;
    }
    com = math3.scale(com, 1.0 / m_total);

    // 1 and 2: table contact and static support, every unit.
    var contact_ok = true;
    var support_ok = true;
    for (units.items) |u| {
        var lowest = std.math.inf(f64);
        for (seeds) |s| lowest = @min(lowest, unitPoint(u, s)[2]);
        if (@abs(lowest) > contact_tol) contact_ok = false;
        var ground: std.ArrayList([2]f64) = .empty;
        for (seeds) |s| {
            const w = unitPoint(u, s);
            if (w[2] <= contact_tol) try ground.append(arena, .{ w[0], w[1] });
        }
        const h = try hull2(arena, ground.items);
        const c_world = unitPoint(u, com);
        if (h.len < 3 or !(hullArea(h) > 0) or !hullContains(h, .{ c_world[0], c_world[1] })) support_ok = false;
    }
    out.result.table_contact = contact_ok;
    out.result.static_support = support_ok;

    // 3: no inter-unit interference between body-role primitives.
    var clear = true;
    for (units.items, 0..) |ua, i| for (units.items[i + 1 ..]) |ub| {
        for (d.chain_geometry.primitives) |pa| {
            if (pa.role != .body) continue;
            for (d.chain_geometry.primitives) |pb| {
                if (pb.role != .body) continue;
                const sa = transformShape(shapeOfPrimitive(pa), ua.q, ua.t);
                const sb = transformShape(shapeOfPrimitive(pb), ub.q, ub.t);
                switch (interferes(sa, sb, erosion, cap)) {
                    .separate => {},
                    .interfere => clear = false,
                    .capped => out.capped = true,
                }
            }
        }
    };
    out.result.no_interference = clear and !out.capped;

    if (out.capped) {
        out.result.status = "unresolved";
        out.result.detail = "intersection_cap_reached";
    } else if (contact_ok and support_ok and clear and sites_meet) {
        out.result.status = "pass";
    } else {
        out.result.status = "fail";
    }
    return out;
}

pub fn evalG5(arena: Allocator, c: crit.Criteria, d: Declaration) Allocator.Error!G5Result {
    // G5 uses the same eroded-shape GJK test and cap as G2.
    const p = c.items[4].params;
    const cap = c.items[1].params.gjk_iteration_cap.?.value;
    return evalG5With(arena, p, cap, d);
}

fn evalG5With(arena: Allocator, p: crit.Params, cap: u32, d: Declaration) Allocator.Error!G5Result {
    var values: G5Values = .{ .coupler_sites = @intCast(d.coupler_sites.len) };
    var rs: Reasons = .{};

    if (d.coupler_sites.len < p.min_coupler_sites.?.value) {
        try rs.fail(arena, "fewer_than_2_coupler_sites");
        return .{ .item = try rs.result(arena, "G5"), .values = values };
    }
    if (std.mem.eql(u8, d.chain.head_site, d.chain.tail_site)) try rs.unres(arena, "head_and_tail_site_identical");
    if (d.chain.mating_roll_deg.len == 0) try rs.unres(arena, "mating_roll_deg_missing");
    const roles = [_]decl_mod.PrimitiveRole{.body};
    const seeds = try sortedSeeds(arena, d.chain_geometry.primitives, &roles, 64);
    if (seeds.len == 0) try rs.unres(arena, "chain_geometry_body_primitives_missing");
    if (rs.unresolved.items.len > 0) return .{ .item = try rs.result(arena, "G5"), .values = values };

    var results: std.ArrayList(RollResult) = .empty;
    var any_capped = false;
    var passed = false;
    for (d.chain.mating_roll_deg) |roll| {
        const ev = try evalRoll(arena, p, cap, d, seeds, roll);
        try results.append(arena, ev.result);
        if (ev.capped) any_capped = true;
        if (std.mem.eql(u8, ev.result.status, "pass")) {
            values.roll_deg_used = roll;
            passed = true;
            break;
        }
    }
    values.rolls = try results.toOwnedSlice(arena);
    if (!passed) {
        if (any_capped) try rs.unres(arena, "intersection_cap_reached_or_mass_zero") else try rs.fail(arena, "no_mating_roll_gives_a_supported_chain");
    }
    return .{ .item = try rs.result(arena, "G5"), .values = values };
}

// --- Review records (G6 retention review, G7/G8 originality review)
//
// Records are Markdown files written by an independent reviewer (protocol
// sections 8 and 9, Q61 section 6). The evaluator reads only the recorded
// verdict and completeness, from `key: value` lines that start in column 0.
// A key that appears twice makes the record incomplete. Keys:
//
//   candidate_id, candidate_version, author, reviewer, outcome   (both records)
//   declaration_sha256, stage                                     (originality)
//   high_cells_f1_f2                                              (originality: count of
//                                                                  high cells against F1/F2)
//   exclusion_cube_with_internal_flywheel,
//   exclusion_needle_or_particle_silhouette                       (originality: present | not_present)
//
// `outcome` is pass, fail, or unresolved.

const RecordStatus = enum { valid, wrong_candidate, hash_mismatch, incomplete, not_independent };

const Lookup = union(enum) { absent, duplicate, value: []const u8 };

fn lookup(text: []const u8, key: []const u8) Lookup {
    var found: ?[]const u8 = null;
    var lines = std.mem.splitScalar(u8, text, '\n');
    while (lines.next()) |raw| {
        const line = std.mem.trimEnd(u8, raw, " \t\r");
        if (!std.mem.startsWith(u8, line, key)) continue;
        if (line.len <= key.len or line[key.len] != ':') continue;
        if (found != null) return .duplicate;
        found = std.mem.trim(u8, line[key.len + 1 ..], " \t");
    }
    return if (found) |f| .{ .value = f } else .absent;
}

fn valueOf(text: []const u8, key: []const u8) ?[]const u8 {
    return switch (lookup(text, key)) {
        .value => |v| if (v.len > 0) v else null,
        else => null,
    };
}

fn parseOutcome(s: []const u8) ?Outcome {
    return std.meta.stringToEnum(Outcome, s);
}

const Chosen = struct {
    revision: u32,
    outcome: Outcome,
    /// null when the key is absent or malformed.
    high_cells: ?u32 = null,
    flywheel: ?bool = null,
    needle: ?bool = null,
};

const Evaluated = struct { status: RecordStatus, chosen: ?Chosen = null };

fn presentFlag(text: []const u8, key: []const u8) ?bool {
    const v = valueOf(text, key) orelse return null;
    if (std.mem.eql(u8, v, "present")) return true;
    if (std.mem.eql(u8, v, "not_present")) return false;
    return null;
}

fn evaluateRecord(rec: RecordFile, d: Declaration, hash_hex: []const u8, originality: bool) Evaluated {
    const text = rec.text;
    const id = valueOf(text, "candidate_id") orelse return .{ .status = .incomplete };
    const ver = valueOf(text, "candidate_version") orelse return .{ .status = .incomplete };
    const author = valueOf(text, "author") orelse return .{ .status = .incomplete };
    const reviewer = valueOf(text, "reviewer") orelse return .{ .status = .incomplete };
    const outcome_text = valueOf(text, "outcome") orelse return .{ .status = .incomplete };
    const outcome = parseOutcome(outcome_text) orelse return .{ .status = .incomplete };
    const ver_n = std.fmt.parseInt(u32, ver, 10) catch return .{ .status = .incomplete };
    if (!std.mem.eql(u8, id, d.candidate_id) or ver_n != d.candidate_version) return .{ .status = .wrong_candidate };

    if (originality) {
        const stage = valueOf(text, "stage") orelse return .{ .status = .incomplete };
        if (!std.mem.eql(u8, stage, "gate1")) return .{ .status = .incomplete };
        const h = valueOf(text, "declaration_sha256") orelse return .{ .status = .incomplete };
        if (!std.mem.eql(u8, h, hash_hex)) return .{ .status = .hash_mismatch };
    }

    // Independence (Q61 section 4): the reviewer differs from the author.
    if (std.ascii.eqlIgnoreCase(reviewer, author) or std.ascii.eqlIgnoreCase(reviewer, std.mem.trim(u8, d.author, " \t\r\n"))) {
        return .{ .status = .not_independent };
    }

    var chosen: Chosen = .{ .revision = rec.revision, .outcome = outcome };
    if (originality) {
        if (valueOf(text, "high_cells_f1_f2")) |v| chosen.high_cells = std.fmt.parseInt(u32, v, 10) catch null;
        chosen.flywheel = presentFlag(text, "exclusion_cube_with_internal_flywheel");
        chosen.needle = presentFlag(text, "exclusion_needle_or_particle_silhouette");
    }
    return .{ .status = .valid, .chosen = chosen };
}

const Selection = struct { chosen: ?Chosen, reason: []const u8 };

fn revisionDescending(_: void, a: RecordFile, b: RecordFile) bool {
    return a.revision > b.revision;
}

/// The latest revision that is complete, independent, for this candidate
/// version, and (originality) bound to the current declaration hash.
fn selectRecord(arena: Allocator, d: Declaration, hash_hex: []const u8, records: []const RecordFile, originality: bool) Allocator.Error!Selection {
    if (records.len == 0) return .{ .chosen = null, .reason = "review_record_missing" };
    const sorted = try arena.dupe(RecordFile, records);
    std.mem.sort(RecordFile, sorted, {}, revisionDescending);
    var latest_reason: []const u8 = "review_record_missing";
    for (sorted, 0..) |rec, i| {
        const ev = evaluateRecord(rec, d, hash_hex, originality);
        if (ev.status == .valid) return .{ .chosen = ev.chosen, .reason = "" };
        if (i == 0) latest_reason = switch (ev.status) {
            .wrong_candidate => "record_for_other_candidate_or_version",
            .hash_mismatch => "declaration_hash_differs_re_review_needed",
            .incomplete => "review_incomplete",
            .not_independent => "reviewer_not_independent",
            .valid => unreachable,
        };
    }
    return .{ .chosen = null, .reason = latest_reason };
}

fn selectOriginality(arena: Allocator, d: Declaration, inputs: Inputs) Allocator.Error!Selection {
    return selectRecord(arena, d, inputs.declaration_sha256, inputs.originality_records, true);
}

fn isBlank(s: []const u8) bool {
    return std.mem.trim(u8, s, " \t\r\n").len == 0;
}

fn hasMagnet(d: Declaration, ids: []const []const u8) bool {
    for (ids) |id| {
        const c = decl_mod.componentById(d.components, id) orelse continue;
        if (c.kind == .magnet) return true;
    }
    return false;
}

pub fn evalG6(arena: Allocator, d: Declaration, inputs: Inputs) Allocator.Error!ItemResult {
    var rs: Reasons = .{};
    const r = d.retention;

    // Checks 1 to 5 (statements that contradict the requirement fail;
    // statements that are missing leave the item unresolved).
    if (r.requires_power_to_hold) try rs.fail(arena, "retention_requires_power_to_hold");
    if (!r.release.bounded_independent_release) try rs.fail(arena, "no_bounded_independent_release");
    if (isBlank(r.release.means)) try rs.unres(arena, "release_means_statement_missing");
    if (isBlank(r.mechanism)) try rs.unres(arena, "retention_statement_missing");
    if (r.component_ids.len == 0) try rs.fail(arena, "retention_names_no_component");
    if (r.mechanism_kind == .permanent_magnet and !hasMagnet(d, r.component_ids)) {
        try rs.fail(arena, "magnetic_retention_without_declared_magnet_component");
    }
    if (d.alignment.len == 0) try rs.unres(arena, "alignment_statement_missing");
    for (d.alignment, 0..) |a, i| {
        if (isBlank(a.justification)) try rs.unres(arena, try std.fmt.allocPrint(arena, "alignment_justification_missing:{d}", .{i}));
        if (a.component_ids.len == 0) try rs.fail(arena, try std.fmt.allocPrint(arena, "alignment_names_no_component:{d}", .{i}));
        if (a.kind == .magnetic and !hasMagnet(d, a.component_ids)) {
            try rs.fail(arena, try std.fmt.allocPrint(arena, "magnetic_alignment_without_declared_magnet_component:{d}", .{i}));
        }
    }
    if (rs.fails.items.len > 0) return rs.result(arena, "G6");

    // Check 6: the independent justification record.
    const sel = try selectRecord(arena, d, inputs.declaration_sha256, inputs.retention_records, false);
    if (sel.chosen) |ch| switch (ch.outcome) {
        .pass => {},
        .fail => try rs.fail(arena, "retention_review_outcome_fail"),
        .unresolved => try rs.unres(arena, "retention_review_outcome_unresolved"),
    } else try rs.unres(arena, try std.fmt.allocPrint(arena, "justification_record:{s}", .{sel.reason}));
    return rs.result(arena, "G6");
}

fn evalG7(arena: Allocator, sel: Selection) Allocator.Error!ItemResult {
    var rs: Reasons = .{};
    if (sel.chosen) |ch| switch (ch.outcome) {
        .pass => {},
        .fail => try rs.fail(arena, "originality_review_outcome_fail"),
        .unresolved => try rs.unres(arena, "originality_review_outcome_unresolved"),
    } else try rs.unres(arena, sel.reason);
    return rs.result(arena, "G7");
}

fn evalG8(arena: Allocator, sel: Selection) Allocator.Error!ItemResult {
    var rs: Reasons = .{};
    const ch = sel.chosen orelse {
        try rs.unres(arena, sel.reason);
        return rs.result(arena, "G8");
    };
    // A recorded copying finding is definite whatever else is missing.
    if (ch.high_cells) |n| if (n > 0) try rs.fail(arena, "high_cell_against_f1_or_f2_reference");
    if (ch.flywheel == true) try rs.fail(arena, "exclusion_present:cube_with_internal_flywheel");
    if (ch.needle == true) try rs.fail(arena, "exclusion_present:needle_or_particle_silhouette");
    if (rs.fails.items.len > 0) return rs.result(arena, "G8");
    if (ch.high_cells == null) try rs.unres(arena, "f1_f2_matrix_summary_not_recorded");
    if (ch.flywheel == null) try rs.unres(arena, "exclusion_check_not_recorded:cube_with_internal_flywheel");
    if (ch.needle == null) try rs.unres(arena, "exclusion_check_not_recorded:needle_or_particle_silhouette");
    if (ch.outcome == .unresolved) try rs.unres(arena, "review_incomplete");
    return rs.result(arena, "G8");
}

// --- Tests

const testing = std.testing;

fn sphere(id: []const u8, x: i64, r: u64, role: decl_mod.PrimitiveRole) Primitive {
    return .{ .id = id, .kind = .sphere, .radius_um = r, .pose = .{ .position_um = .{ x, 0, 0 }, .orientation = .{ 1, 0, 0, 0 } }, .role = role };
}

fn boxPrim(id: []const u8, h: [3]u64, role: decl_mod.PrimitiveRole) Primitive {
    return .{ .id = id, .kind = .box, .half_extent_um = h, .pose = .{ .position_um = .{ 0, 0, 0 }, .orientation = .{ 1, 0, 0, 0 } }, .role = role };
}

const Fixture = struct {
    crit_parsed: @import("strict_json.zig").Parsed(crit.Criteria),
    arena_state: std.heap.ArenaAllocator,

    fn init() !Fixture {
        return .{
            .crit_parsed = try crit.parse(testing.allocator, crit.gate1_v1_json),
            .arena_state = std.heap.ArenaAllocator.init(testing.allocator),
        };
    }
    fn deinit(self: *Fixture) void {
        self.crit_parsed.deinit();
        self.arena_state.deinit();
    }
    fn arena(self: *Fixture) Allocator {
        return self.arena_state.allocator();
    }
};

const sample_hash = "0000000000000000000000000000000000000000000000000000000000000000";

fn parseSample(fx: *Fixture, mutate_needle: ?[]const u8, replacement: []const u8) !Declaration {
    const text = if (mutate_needle) |n| blk: {
        const at = std.mem.indexOf(u8, decl_mod.sample_json, n) orelse return error.TestNeedleNotFound;
        break :blk try std.mem.concat(fx.arena(), u8, &.{ decl_mod.sample_json[0..at], replacement, decl_mod.sample_json[at + n.len ..] });
    } else decl_mod.sample_json;
    const p = try decl_mod.parse(fx.arena(), text, null);
    return p.value;
}

fn itemOutcome(rep: CandidateReport, id: []const u8) Outcome {
    for (rep.items) |it| if (std.mem.eql(u8, it.id, id)) return it.outcome;
    unreachable;
}

fn g1Diameter(fx: *Fixture, prims: []const Primitive) !G1Result {
    var d = try parseSample(fx, null, "");
    d.stowed_geometry = .{ .primitives = prims };
    return evalG1(fx.arena(), fx.crit_parsed.value.items[0].params, d);
}

test "G1: the enclosing sphere of known geometry is exact" {
    var fx = try Fixture.init();
    defer fx.deinit();
    // Two spheres whose extreme points are 59998 / 60000 / 60001 / 60002 um apart.
    const pass = try g1Diameter(&fx, &.{ sphere("a", -10000, 19999, .body), sphere("b", 10000, 19999, .body) });
    try testing.expectEqual(@as(f64, 59998), pass.values.diameter_um.?);
    try testing.expectEqual(Outcome.pass, pass.item.outcome);

    const edge = try g1Diameter(&fx, &.{ sphere("a", -10000, 20000, .body), sphere("b", 10000, 20000, .body) });
    try testing.expectEqual(@as(f64, 60000), edge.values.diameter_um.?);
    // Exactly at the limit lies inside the numerical band: not a pass.
    try testing.expectEqual(Outcome.unresolved, edge.item.outcome);

    const fail1 = try g1Diameter(&fx, &.{ sphere("a", -10000, 20000, .body), sphere("b", 10001, 20000, .body) });
    try testing.expectEqual(@as(f64, 60001), fail1.values.diameter_um.?);
    try testing.expectEqual(Outcome.fail, fail1.item.outcome);

    const just_under = try g1Diameter(&fx, &.{ sphere("a", -10000, 20000, .body), sphere("b", 9999, 20000, .body) });
    try testing.expectEqual(@as(f64, 59999), just_under.values.diameter_um.?);
    try testing.expectEqual(Outcome.pass, just_under.item.outcome);
}

test "G1: a single sphere, a cube and a cylinder" {
    var fx = try Fixture.init();
    defer fx.deinit();
    const s = try g1Diameter(&fx, &.{sphere("s", 5000, 29999, .body)});
    try testing.expectApproxEqAbs(@as(f64, 59998), s.values.diameter_um.?, 1e-6);
    try testing.expectEqual(Outcome.pass, s.item.outcome);
    const s_big = try g1Diameter(&fx, &.{sphere("s", 0, 30001, .body)});
    try testing.expectEqual(Outcome.fail, s_big.item.outcome);

    // Cube half 15000: corner radius 15000*sqrt(3), D = 51961.5...
    const cube = try g1Diameter(&fx, &.{boxPrim("c", .{ 15000, 15000, 15000 }, .body)});
    try testing.expectApproxEqAbs(2.0 * 15000.0 * @sqrt(3.0), cube.values.diameter_um.?, 1e-6);
    try testing.expectEqual(cube.values.welzl_radius_um.?, cube.values.certified_radius_um.?);
    try testing.expectEqual(Outcome.pass, cube.item.outcome);

    // The 3-4-5 cylinder: radius 18000, half height 24000 gives R = 30000 exactly.
    const cyl = try g1Diameter(&fx, &.{.{ .id = "y", .kind = .cylinder, .radius_um = 18000, .half_height_um = 24000, .pose = .{ .position_um = .{ 0, 0, 0 }, .orientation = .{ 1, 0, 0, 0 } }, .role = .body }});
    try testing.expectApproxEqAbs(@as(f64, 60000), cyl.values.diameter_um.?, 1e-6);
    // The certified diameter is never below the Welzl diameter.
    try testing.expect(cyl.values.certified_radius_um.? >= cyl.values.welzl_radius_um.? * (1 - 1e-12));
}

test "G1: cavity primitives are excluded, and no body primitive is unresolved" {
    var fx = try Fixture.init();
    defer fx.deinit();
    const only_cavity = try g1Diameter(&fx, &.{boxPrim("v", .{ 90000, 90000, 90000 }, .cavity)});
    try testing.expectEqual(Outcome.unresolved, only_cavity.item.outcome);
    const with_cavity = try g1Diameter(&fx, &.{ sphere("s", 0, 20000, .body), boxPrim("v", .{ 90000, 90000, 90000 }, .cavity) });
    try testing.expectEqual(Outcome.pass, with_cavity.item.outcome);
}

test "GJK: overlap, separation, erosion and caps" {
    const unit_box = Shape{ .kind = .box, .h = .{ 1000, 1000, 1000 }, .c = .{ 0, 0, 0 }, .q = Quat.identity };
    var other = unit_box;
    other.c = .{ 1500, 0, 0 };
    try testing.expectEqual(Intersection.interfere, interferes(unit_box, other, 1.0, 64));
    other.c = .{ 2500, 0, 0 };
    try testing.expectEqual(Intersection.separate, interferes(unit_box, other, 1.0, 64));
    // Touching faces and overlap smaller than twice the erosion do not interfere.
    other.c = .{ 2000, 0, 0 };
    try testing.expectEqual(Intersection.separate, interferes(unit_box, other, 1.0, 64));
    other.c = .{ 1999, 0, 0 };
    try testing.expectEqual(Intersection.separate, interferes(unit_box, other, 1.0, 64));
    other.c = .{ 1990, 0, 0 };
    try testing.expectEqual(Intersection.interfere, interferes(unit_box, other, 1.0, 64));
    // A rotated box against a sphere, and a cylinder against a box.
    const rot = Quat.normalized(.{ .w = 1, .x = 0, .y = 0, .z = 1 });
    var rb = unit_box;
    rb.q = rot;
    const sph = Shape{ .kind = .sphere, .r = 500, .c = .{ 1300, 0, 0 }, .q = Quat.identity };
    try testing.expectEqual(Intersection.interfere, interferes(rb, sph, 1.0, 64));
    const far_sph = Shape{ .kind = .sphere, .r = 500, .c = .{ 1500, 0, 0 }, .q = Quat.identity };
    try testing.expectEqual(Intersection.separate, interferes(rb, far_sph, 1.0, 64));
    const cyl = Shape{ .kind = .cylinder, .r = 300, .h = .{ 0, 0, 2000 }, .c = .{ 0, 900, 0 }, .q = Quat.identity };
    try testing.expectEqual(Intersection.interfere, interferes(unit_box, cyl, 1.0, 64));
    // The iteration cap makes the result capped, never a silent pass.
    other.c = .{ 1500, 400, 200 };
    try testing.expectEqual(Intersection.capped, gjk(unit_box, other, 1));
    // An eroded-away shape never interferes.
    const tiny = Shape{ .kind = .sphere, .r = 0.5, .c = .{ 0, 0, 0 }, .q = Quat.identity };
    try testing.expectEqual(Intersection.separate, interferes(unit_box, tiny, 1.0, 64));
}

test "sample declaration: the paper gate resolves except for missing review records" {
    var fx = try Fixture.init();
    defer fx.deinit();
    const d = try parseSample(&fx, null, "");
    const rep = try evaluate(fx.arena(), fx.crit_parsed.value, d, .{ .declaration_sha256 = sample_hash });
    for ([_][]const u8{ "G1", "G2", "G3", "G4", "G5" }) |id| try testing.expectEqual(Outcome.pass, itemOutcome(rep, id));
    try testing.expectEqual(Outcome.unresolved, itemOutcome(rep, "G6"));
    try testing.expectEqual(Outcome.unresolved, itemOutcome(rep, "G7"));
    try testing.expectEqual(Outcome.unresolved, itemOutcome(rep, "G8"));
    try testing.expectEqual(Outcome.unresolved, rep.outcome);
    try testing.expectEqualStrings("exploratory", rep.label);
    try testing.expectEqual(@as(usize, 3), rep.unresolved_items.len);
    try testing.expectEqual(@as(?f64, 0), rep.g5.roll_deg_used);
}

test "G2: overlapping boxes fail, a box outside the cavity fails, a missing statement fails" {
    var fx = try Fixture.init();
    defer fx.deinit();
    const overlap = try parseSample(&fx, "\"position_um\": [8000, 0, 0]", "\"position_um\": [-6000, 0, 0]");
    const g2 = try evalG2(fx.arena(), fx.crit_parsed.value.items[1].params, overlap);
    try testing.expectEqual(Outcome.fail, g2.item.outcome);
    try testing.expectEqual(@as(usize, 1), g2.values.interfering_pairs.len);
    try testing.expectEqualStrings("cell", g2.values.interfering_pairs[0].a);
    try testing.expectEqualStrings("mcu", g2.values.interfering_pairs[0].b);

    const outside = try parseSample(&fx, "\"position_um\": [8000, 0, 0]", "\"position_um\": [12000, 0, 0]");
    const g2b = try evalG2(fx.arena(), fx.crit_parsed.value.items[1].params, outside);
    try testing.expectEqual(Outcome.fail, g2b.item.outcome);
    try testing.expectEqualStrings("mcu", g2b.values.boxes_outside_shell[0]);

    const no_access = try parseSample(&fx, "\"statement\": \"two-part shell, screws on the seam\"", "\"statement\": \"  \"");
    const g2c = try evalG2(fx.arena(), fx.crit_parsed.value.items[1].params, no_access);
    try testing.expectEqual(Outcome.fail, g2c.item.outcome);
}

test "G2: no cavity primitive is unresolved, boxes that only touch pass" {
    var fx = try Fixture.init();
    defer fx.deinit();
    var d = try parseSample(&fx, null, "");
    d.stowed_geometry = .{ .primitives = d.stowed_geometry.primitives[0..1] };
    const g2 = try evalG2(fx.arena(), fx.crit_parsed.value.items[1].params, d);
    try testing.expectEqual(Outcome.unresolved, g2.item.outcome);
    // cell spans x in [-13000, -3000]; mcu moved to touch at -3000 from the right.
    const touching = try parseSample(&fx, "\"position_um\": [8000, 0, 0]", "\"position_um\": [0, 0, 0]");
    const g2t = try evalG2(fx.arena(), fx.crit_parsed.value.items[1].params, touching);
    try testing.expectEqual(Outcome.pass, g2t.item.outcome);
}

test "G3: a missing citation is unresolved; estimates are unresolved; a derived-mass mismatch fails" {
    var fx = try Fixture.init();
    defer fx.deinit();
    const missing = try parseSample(&fx, "\"source\": { \"kind\": \"datasheet\", \"url\": \"https://example.org/mcu.pdf\", \"accessed\": \"2026-11-04\", \"title\": \"MCU\" }", "\"source\": null");
    const g3 = try evalG3(fx.arena(), fx.crit_parsed.value, missing);
    try testing.expectEqual(Outcome.unresolved, g3.outcome);
    try testing.expectEqualStrings("unresolved: uncited_component:mcu", g3.reasons[0]);

    const estimate = try parseSample(&fx, "\"power_basis\": \"source\",\n", "\"power_basis\": \"estimate\",\n");
    try testing.expectEqual(Outcome.unresolved, (try evalG3(fx.arena(), fx.crit_parsed.value, estimate)).outcome);

    // Malformed URL, bad kind, and an access date after declared_on are uncited.
    const bad_url = try parseSample(&fx, "https://example.org/mcu.pdf", "ftp://example.org/mcu.pdf");
    try testing.expectEqual(Outcome.unresolved, (try evalG3(fx.arena(), fx.crit_parsed.value, bad_url)).outcome);
    const bad_kind = try parseSample(&fx, "\"kind\": \"datasheet\", \"url\": \"https://example.org/mcu.pdf\"", "\"kind\": \"forum\", \"url\": \"https://example.org/mcu.pdf\"");
    try testing.expectEqual(Outcome.unresolved, (try evalG3(fx.arena(), fx.crit_parsed.value, bad_kind)).outcome);
    const future = try parseSample(&fx, "\"accessed\": \"2026-11-04\", \"title\": \"MCU\"", "\"accessed\": \"2026-12-31\", \"title\": \"MCU\"");
    try testing.expectEqual(Outcome.unresolved, (try evalG3(fx.arena(), fx.crit_parsed.value, future)).outcome);

    // Derived mass: 2700 kg/m3 * 1.85e-7 m3 = 499.5 mg, so 500 passes and 502 fails.
    const derived_ok = try parseSample(&fx, "\"mass_mg\": 500, \"mass_basis\": \"source\",", "\"mass_mg\": 500, \"mass_basis\": \"derived\", \"derivation\": { \"density_kg_m3\": 2700, \"volume_m3\": 1.85e-7 },");
    try testing.expectEqual(Outcome.pass, (try evalG3(fx.arena(), fx.crit_parsed.value, derived_ok)).outcome);
    const derived_bad = try parseSample(&fx, "\"mass_mg\": 500, \"mass_basis\": \"source\",", "\"mass_mg\": 502, \"mass_basis\": \"derived\", \"derivation\": { \"density_kg_m3\": 2700, \"volume_m3\": 1.85e-7 },");
    try testing.expectEqual(Outcome.fail, (try evalG3(fx.arena(), fx.crit_parsed.value, derived_bad)).outcome);
}

test "G4: budget closure passes and fails; discharge limit; endurance is reported only" {
    var fx = try Fixture.init();
    defer fx.deinit();
    const params = fx.crit_parsed.value.items[3].params;
    const ok = try parseSample(&fx, null, "");
    const g4 = try evalG4(fx.arena(), params, ok);
    try testing.expectEqual(Outcome.pass, g4.item.outcome);
    try testing.expectEqual(@as(u64, 1500), g4.values.summed_mass_mg);
    try testing.expectEqual(@as(u64, 100), g4.values.p_peak_mw);
    try testing.expectApproxEqAbs(@as(f64, 3700), g4.values.p_lim_mw.?, 1e-9);
    // 5000 mJ at 10 mW is 500 s; the protocol's literal formula says 500000.
    try testing.expectEqualStrings("reported", g4.values.endurance_status);
    try testing.expectApproxEqAbs(@as(f64, 500), g4.values.endurance_s.?, 1e-9);
    try testing.expectApproxEqAbs(@as(f64, 500000), g4.values.endurance_s_protocol_literal.?, 1e-6);
    try testing.expect(!g4.values.endurance_enters_outcome);

    const mass_off = try parseSample(&fx, "\"total_mass_mg\": 1500", "\"total_mass_mg\": 1501");
    try testing.expectEqual(Outcome.fail, (try evalG4(fx.arena(), params, mass_off)).item.outcome);

    const hot = try parseSample(&fx, "\"peak_power_mw\": 100", "\"peak_power_mw\": 3701");
    try testing.expectEqual(Outcome.fail, (try evalG4(fx.arena(), params, hot)).item.outcome);
    const at_limit = try parseSample(&fx, "\"peak_power_mw\": 100", "\"peak_power_mw\": 3700");
    try testing.expectEqual(Outcome.pass, (try evalG4(fx.arena(), params, at_limit)).item.outcome);

    const no_rating = try parseSample(&fx, "\"rated_continuous_discharge_a\": 1.0", "\"rated_continuous_discharge_a\": null");
    try testing.expectEqual(Outcome.unresolved, (try evalG4(fx.arena(), params, no_rating)).item.outcome);
    // A definite failure still dominates a missing rating.
    const both = try parseSample(&fx, "\"rated_continuous_discharge_a\": 1.0, \"energy_mj\": 5000", "\"rated_continuous_discharge_a\": null, \"energy_mj\": 5000");
    var both_d = both;
    both_d.mass_budget = .{ .total_mass_mg = 9 };
    try testing.expectEqual(Outcome.fail, (try evalG4(fx.arena(), params, both_d)).item.outcome);

    // Zero average power: endurance is not applicable and the outcome is unchanged.
    const idle = try parseSample(&fx, "\"average_power_mw\": 10", "\"average_power_mw\": 0");
    const gi = try evalG4(fx.arena(), params, idle);
    try testing.expectEqualStrings("not_applicable", gi.values.endurance_status);
    try testing.expectEqual(Outcome.pass, gi.item.outcome);
}

test "G5: fewer than two coupler sites fails; the sample chain passes; the first passing roll is recorded" {
    var fx = try Fixture.init();
    defer fx.deinit();
    const c = fx.crit_parsed.value;
    var d = try parseSample(&fx, null, "");
    const ok = try evalG5(fx.arena(), c, d);
    try testing.expectEqual(Outcome.pass, ok.item.outcome);
    try testing.expectEqual(@as(?f64, 0), ok.values.roll_deg_used);

    d.coupler_sites = d.coupler_sites[0..1];
    try testing.expectEqual(Outcome.fail, (try evalG5(fx.arena(), c, d)).item.outcome);

    // A 45 degree roll buries the cube in the table; the next roll passes.
    const rolls = try parseSample(&fx, "\"mating_roll_deg\": [0]", "\"mating_roll_deg\": [45, 0]");
    const g5 = try evalG5(fx.arena(), c, rolls);
    try testing.expectEqual(Outcome.pass, g5.item.outcome);
    try testing.expectEqual(@as(?f64, 0), g5.values.roll_deg_used);
    try testing.expectEqual(@as(usize, 2), g5.values.rolls.len);
    try testing.expectEqualStrings("fail", g5.values.rolls[0].status);

    const only_bad = try parseSample(&fx, "\"mating_roll_deg\": [0]", "\"mating_roll_deg\": [45]");
    try testing.expectEqual(Outcome.fail, (try evalG5(fx.arena(), c, only_bad)).item.outcome);
}

test "G5: prerequisites give unresolved; an unsupported rest orientation fails" {
    var fx = try Fixture.init();
    defer fx.deinit();
    const c = fx.crit_parsed.value;
    const no_roll = try parseSample(&fx, "\"mating_roll_deg\": [0]", "\"mating_roll_deg\": []");
    try testing.expectEqual(Outcome.unresolved, (try evalG5(fx.arena(), c, no_roll)).item.outcome);
    const same = try parseSample(&fx, "\"tail_site\": \"s-minus\"", "\"tail_site\": \"s-plus\"");
    try testing.expectEqual(Outcome.unresolved, (try evalG5(fx.arena(), c, same)).item.outcome);
    // Rest on an edge (cube rolled 45 degrees about x): only a line touches the table.
    const edge = try parseSample(&fx, "\"rest_orientation\": [1, 0, 0, 0]", "\"rest_orientation\": [0.9238795325112867, 0.3826834323650898, 0, 0]");
    try testing.expectEqual(Outcome.fail, (try evalG5(fx.arena(), c, edge)).item.outcome);
}

test "G5: a centre of mass outside the contact hull fails" {
    var fx = try Fixture.init();
    defer fx.deinit();
    // Put a component's box centre (and so the mass centre) beyond the footprint.
    var d = try parseSample(&fx, null, "");
    var comps = try fx.arena().dupe(decl_mod.Component, d.components);
    comps[0].box.pose.position_um = .{ 40000, 0, 0 };
    d.components = comps;
    try testing.expectEqual(Outcome.fail, (try evalG5(fx.arena(), fx.crit_parsed.value, d)).item.outcome);
}

fn record(arena: Allocator, extra: []const u8, outcome: []const u8, reviewer: []const u8, hash: []const u8) ![]const u8 {
    return std.fmt.allocPrint(arena,
        \\# Review
        \\candidate_id: sample-a
        \\candidate_version: 1
        \\declaration_sha256: {s}
        \\stage: gate1
        \\author: author-agent
        \\reviewer: {s}
        \\outcome: {s}
        \\{s}
    , .{ hash, reviewer, outcome, extra });
}

const good_original_extra =
    \\high_cells_f1_f2: 0
    \\exclusion_cube_with_internal_flywheel: not_present
    \\exclusion_needle_or_particle_silhouette: not_present
;

test "G6, G7, G8 read independent review records; the candidate passes with all of them" {
    var fx = try Fixture.init();
    defer fx.deinit();
    const a = fx.arena();
    const d = try parseSample(&fx, null, "");
    const ret = [_]RecordFile{.{ .revision = 1, .text = try record(a, "", "pass", "reviewer-1", sample_hash) }};
    const org = [_]RecordFile{.{ .revision = 1, .text = try record(a, good_original_extra, "pass", "reviewer-2", sample_hash) }};
    const rep = try evaluate(a, fx.crit_parsed.value, d, .{ .declaration_sha256 = sample_hash, .retention_records = &ret, .originality_records = &org });
    for (rep.items) |it| try testing.expectEqual(Outcome.pass, it.outcome);
    try testing.expectEqual(Outcome.pass, rep.outcome);
    try testing.expectEqual(@as(usize, 0), rep.unresolved_items.len);
}

test "review records: verdicts, independence, hash binding, latest revision" {
    var fx = try Fixture.init();
    defer fx.deinit();
    const a = fx.arena();
    const d = try parseSample(&fx, null, "");
    const params_in = struct {
        fn run(arena: Allocator, c: crit.Criteria, dd: Declaration, ret: []const RecordFile, org: []const RecordFile) !CandidateReport {
            return evaluate(arena, c, dd, .{ .declaration_sha256 = sample_hash, .retention_records = ret, .originality_records = org });
        }
    }.run;
    const c = fx.crit_parsed.value;

    // outcome: fail
    const failed = [_]RecordFile{.{ .revision = 1, .text = try record(a, good_original_extra, "fail", "reviewer-2", sample_hash) }};
    var rep = try params_in(a, c, d, &failed, &failed);
    try testing.expectEqual(Outcome.fail, itemOutcome(rep, "G6"));
    try testing.expectEqual(Outcome.fail, itemOutcome(rep, "G7"));
    try testing.expectEqual(Outcome.pass, itemOutcome(rep, "G8"));
    try testing.expectEqual(Outcome.fail, rep.outcome);

    // outcome: unresolved is incomplete, not a pass
    const unres = [_]RecordFile{.{ .revision = 1, .text = try record(a, good_original_extra, "unresolved", "reviewer-2", sample_hash) }};
    rep = try params_in(a, c, d, &unres, &unres);
    try testing.expectEqual(Outcome.unresolved, itemOutcome(rep, "G7"));
    try testing.expectEqual(Outcome.unresolved, itemOutcome(rep, "G8"));

    // reviewer == author: not independent
    const same = [_]RecordFile{.{ .revision = 1, .text = try record(a, good_original_extra, "pass", "Author-Agent", sample_hash) }};
    rep = try params_in(a, c, d, &same, &same);
    try testing.expectEqual(Outcome.unresolved, itemOutcome(rep, "G6"));
    try testing.expectEqual(Outcome.unresolved, itemOutcome(rep, "G7"));

    // declaration hash differs: re-review needed (G7/G8); G6 does not bind the hash
    const stale_hash = "1111111111111111111111111111111111111111111111111111111111111111";
    const stale = [_]RecordFile{.{ .revision = 1, .text = try record(a, good_original_extra, "pass", "reviewer-2", stale_hash) }};
    rep = try params_in(a, c, d, &stale, &stale);
    try testing.expectEqual(Outcome.pass, itemOutcome(rep, "G6"));
    try testing.expectEqual(Outcome.unresolved, itemOutcome(rep, "G7"));
    try testing.expectEqual(Outcome.unresolved, itemOutcome(rep, "G8"));
    try testing.expectEqualStrings("unresolved: declaration_hash_differs_re_review_needed", rep.items[6].reasons[0]);

    // latest valid revision wins: r2 fail over r1 pass, regardless of order given
    const two = [_]RecordFile{
        .{ .revision = 2, .text = try record(a, good_original_extra, "fail", "reviewer-2", sample_hash) },
        .{ .revision = 1, .text = try record(a, good_original_extra, "pass", "reviewer-2", sample_hash) },
    };
    rep = try params_in(a, c, d, &.{}, &two);
    try testing.expectEqual(Outcome.fail, itemOutcome(rep, "G7"));
    // an invalid newest revision falls back to the older valid one
    const fallback = [_]RecordFile{
        .{ .revision = 1, .text = try record(a, good_original_extra, "pass", "reviewer-2", sample_hash) },
        .{ .revision = 2, .text = try record(a, good_original_extra, "pass", "reviewer-2", stale_hash) },
    };
    rep = try params_in(a, c, d, &.{}, &fallback);
    try testing.expectEqual(Outcome.pass, itemOutcome(rep, "G7"));

    // duplicate key makes the record incomplete
    const dup_text = try std.mem.concat(a, u8, &.{ try record(a, good_original_extra, "pass", "reviewer-2", sample_hash), "\noutcome: fail\n" });
    const dup = [_]RecordFile{.{ .revision = 1, .text = dup_text }};
    rep = try params_in(a, c, d, &.{}, &dup);
    try testing.expectEqual(Outcome.unresolved, itemOutcome(rep, "G7"));
}

test "G8: a high cell or a present exclusion fails; a missing exclusion check is unresolved" {
    var fx = try Fixture.init();
    defer fx.deinit();
    const a = fx.arena();
    const d = try parseSample(&fx, null, "");
    const c = fx.crit_parsed.value;
    const cases = [_]struct { extra: []const u8, want: Outcome }{
        .{ .extra = "high_cells_f1_f2: 1\nexclusion_cube_with_internal_flywheel: not_present\nexclusion_needle_or_particle_silhouette: not_present\n", .want = .fail },
        .{ .extra = "high_cells_f1_f2: 0\nexclusion_cube_with_internal_flywheel: present\nexclusion_needle_or_particle_silhouette: not_present\n", .want = .fail },
        .{ .extra = "high_cells_f1_f2: 0\nexclusion_cube_with_internal_flywheel: not_present\nexclusion_needle_or_particle_silhouette: present\n", .want = .fail },
        .{ .extra = "high_cells_f1_f2: 0\nexclusion_cube_with_internal_flywheel: not_present\n", .want = .unresolved },
        .{ .extra = "exclusion_cube_with_internal_flywheel: not_present\nexclusion_needle_or_particle_silhouette: not_present\n", .want = .unresolved },
        .{ .extra = "high_cells_f1_f2: 0\nexclusion_cube_with_internal_flywheel: maybe\nexclusion_needle_or_particle_silhouette: not_present\n", .want = .unresolved },
    };
    for (cases) |cs| {
        const org = [_]RecordFile{.{ .revision = 1, .text = try record(a, cs.extra, "pass", "reviewer-2", sample_hash) }};
        const rep = try evaluate(a, c, d, .{ .declaration_sha256 = sample_hash, .originality_records = &org });
        try testing.expectEqual(cs.want, itemOutcome(rep, "G8"));
    }
}

test "G6: contradicting statements fail, missing statements are unresolved, magnetism needs a magnet component" {
    var fx = try Fixture.init();
    defer fx.deinit();
    const a = fx.arena();
    const ret = [_]RecordFile{.{ .revision = 1, .text = try record(a, "", "pass", "reviewer-1", sample_hash) }};
    const inputs: Inputs = .{ .declaration_sha256 = sample_hash, .retention_records = &ret };

    const powered = try parseSample(&fx, "\"requires_power_to_hold\": false", "\"requires_power_to_hold\": true");
    try testing.expectEqual(Outcome.fail, (try evalG6(a, powered, inputs)).outcome);
    const no_release = try parseSample(&fx, "\"bounded_independent_release\": true", "\"bounded_independent_release\": false");
    try testing.expectEqual(Outcome.fail, (try evalG6(a, no_release, inputs)).outcome);
    const magnet = try parseSample(&fx, "\"mechanism_kind\": \"geometric_interlock\"", "\"mechanism_kind\": \"permanent_magnet\"");
    try testing.expectEqual(Outcome.fail, (try evalG6(a, magnet, inputs)).outcome);
    const magnetic_align = try parseSample(&fx, "\"kind\": \"geometric_guide\"", "\"kind\": \"magnetic\"");
    try testing.expectEqual(Outcome.fail, (try evalG6(a, magnetic_align, inputs)).outcome);
    // A magnet component that is declared and referenced makes magnetism acceptable.
    const with_magnet = try parseSample(&fx, "\"id\": \"mcu\", \"kind\": \"controller\"", "\"id\": \"mcu\", \"kind\": \"magnet\"");
    var wm = with_magnet;
    wm.retention.mechanism_kind = .permanent_magnet;
    try testing.expectEqual(Outcome.pass, (try evalG6(a, wm, inputs)).outcome);
    const no_just = try parseSample(&fx, "\"justification\": \"chamfer\"", "\"justification\": \"\"");
    try testing.expectEqual(Outcome.unresolved, (try evalG6(a, no_just, inputs)).outcome);
    const no_record = try parseSample(&fx, null, "");
    try testing.expectEqual(Outcome.unresolved, (try evalG6(a, no_record, .{ .declaration_sha256 = sample_hash })).outcome);
}

test "evaluation is deterministic" {
    var fx = try Fixture.init();
    defer fx.deinit();
    const a = fx.arena();
    const d = try parseSample(&fx, "\"mating_roll_deg\": [0]", "\"mating_roll_deg\": [45, 90, 0]");
    const ret = [_]RecordFile{.{ .revision = 1, .text = try record(a, "", "pass", "reviewer-1", sample_hash) }};
    const inputs: Inputs = .{ .declaration_sha256 = sample_hash, .retention_records = &ret };
    const first = try std.json.Stringify.valueAlloc(a, try evaluate(a, fx.crit_parsed.value, d, inputs), .{});
    const second = try std.json.Stringify.valueAlloc(a, try evaluate(a, fx.crit_parsed.value, d, inputs), .{});
    try testing.expectEqualStrings(first, second);
    // Welzl on a rotated, multi-primitive shape is repeatable to the bit.
    const prims = [_]Primitive{ sphere("a", -3000, 12000, .body), boxPrim("b", .{ 5000, 7000, 9000 }, .coupler), .{ .id = "c", .kind = .cylinder, .radius_um = 8000, .half_height_um = 11000, .pose = .{ .position_um = .{ 1000, 2000, 3000 }, .orientation = .{ 0.5, 0.5, 0.5, 0.5 } }, .role = .body } };
    var dd = d;
    dd.stowed_geometry = .{ .primitives = &prims };
    const g_a = try evalG1(a, fx.crit_parsed.value.items[0].params, dd);
    const g_b = try evalG1(a, fx.crit_parsed.value.items[0].params, dd);
    try testing.expectEqual(@as(u64, @bitCast(g_a.values.diameter_um.?)), @as(u64, @bitCast(g_b.values.diameter_um.?)));
}

test "aggregation: fail beats unresolved beats pass" {
    const mk = struct {
        fn item(o: Outcome) ItemResult {
            return .{ .id = "X", .outcome = o, .reasons = &.{} };
        }
    }.item;
    try testing.expectEqual(Outcome.pass, aggregate(&.{ mk(.pass), mk(.pass) }));
    try testing.expectEqual(Outcome.unresolved, aggregate(&.{ mk(.pass), mk(.unresolved) }));
    try testing.expectEqual(Outcome.fail, aggregate(&.{ mk(.unresolved), mk(.fail), mk(.pass) }));
}
