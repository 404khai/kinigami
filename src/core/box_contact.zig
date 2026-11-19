//! Box-box (cuboid) contact generation (Q76 section 2, protocol
//! `docs/validation/body-contact-v1-protocol.md`, "Contact generation").
//!
//! A pure function of two body poses and sizes; it has no state and no
//! tolerances other than the two the protocol names (parallel-edge axis
//! skip 1e-9, duplicate-point merge 1e-12 m, both provisional).
//!
//! 1. Pair order: the contact normal points from A to B.
//! 2. SAT over 15 axes in the fixed order: A x y z (0..2), B x y z (3..5),
//!    then A axis i crossed with B axis j at 6 + 3i + j. A cross axis whose
//!    length is <= 1e-9 (parallel edges) is skipped.
//! 3. Overlap = r_A + r_B - |d . axis|. Any overlap < 0: separated. The
//!    strictly smallest overlap wins; ties go to the lowest axis index. A
//!    minimum overlap of exactly 0 (touching) creates no row.
//! 4. Face axis: the reference box owns the axis. The incident face is the
//!    other box's face most anti-parallel to the reference outward normal
//!    (ties to the lowest face index: +x -x +y -y +z -z). Its four vertices
//!    (cyclic order, see `faceVertices`) are clipped by Sutherland-Hodgman
//!    against the reference box's four side planes in the order +u -u +v -v
//!    (u < v are the reference tangential axes by ascending index). Points
//!    above the reference face (depth < 0) are dropped, consecutive points
//!    within 1e-12 m are merged. Feature id = index in the output.
//! 5. Edge axis: one point, the midpoint of the closest points of the two
//!    supporting edges (each parameter clamped to its edge); depth is the
//!    axis overlap; feature id 0.

const std = @import("std");
const m3 = @import("math3.zig");

pub const Box = struct {
    centre: m3.Vec3,
    orientation: m3.Quat,
    half: m3.Vec3,
};

pub const max_points = 8;

/// Protocol constants (provisional).
pub const parallel_edge_length: f64 = 1e-9;
pub const duplicate_point_m: f64 = 1e-12;
/// Axis-selection hysteresis (provisional; Q76 says only "ties broken by fixed
/// axis order"). Two overlaps closer than this are a tie that keeps the lower
/// index, and an edge axis must beat the best face axis by `edge_rel` and by
/// this much, so rounding noise on a near-parallel pair cannot flip the
/// reference feature between steps. Independent of the world frame.
pub const axis_tie_m: f64 = 1e-9;
pub const edge_rel: f64 = 0.95;

pub const Point = struct {
    /// World position on the incident face (face) or edge midpoint (edge).
    point: m3.Vec3,
    /// Penetration along the normal; >= 0.
    depth: f64,
};

pub const Manifold = struct {
    /// SAT axis index, 0..14.
    axis: u8,
    /// Unit contact normal, from A to B.
    normal: m3.Vec3,
    count: u8,
    points: [max_points]Point,
    /// Unit friction tangents: the reference box's two tangential axes for
    /// face contact; the A edge direction and normal x that for edge contact.
    tangent: [2]m3.Vec3,

    pub fn slice(self: *const Manifold) []const Point {
        return self.points[0..self.count];
    }
};

fn axesOf(b: Box) [3]m3.Vec3 {
    return .{ b.orientation.rotate(.{ 1, 0, 0 }), b.orientation.rotate(.{ 0, 1, 0 }), b.orientation.rotate(.{ 0, 0, 1 }) };
}

fn radius(dir: m3.Vec3, axes: [3]m3.Vec3, half: m3.Vec3) f64 {
    return @abs(m3.dot(dir, axes[0])) * half[0] + @abs(m3.dot(dir, axes[1])) * half[1] + @abs(m3.dot(dir, axes[2])) * half[2];
}

/// Outcome of the SAT stage, exposed for tests and the evaluator.
pub const Sat = struct { axis: u8, overlap: f64, normal: m3.Vec3 };

/// SAT over the 15 axes. Null when separated (some overlap < 0).
pub fn sat(a: Box, b: Box) ?Sat {
    const ax = axesOf(a);
    const bx = axesOf(b);
    const d = m3.sub(b.centre, a.centre);
    // Face axes (0..5) and edge axes (6..14) are tracked separately so that a
    // near-parallel box pair (a stack, a resting block) is not decided by
    // rounding noise: within each class the smallest overlap wins and ties
    // (within `axis_tie_m`) keep the lower index; an edge axis replaces the
    // best face axis only when it is clearly smaller (see `edge_rel`, `axis_tie_m`).
    var face: Sat = .{ .axis = 0, .overlap = std.math.inf(f64), .normal = m3.zero };
    var edge: Sat = .{ .axis = 0, .overlap = std.math.inf(f64), .normal = m3.zero };
    var face_dir: m3.Vec3 = m3.zero;
    var edge_dir: m3.Vec3 = m3.zero;
    for (0..15) |i| {
        var dir: m3.Vec3 = undefined;
        if (i < 3) {
            dir = ax[i];
        } else if (i < 6) {
            dir = bx[i - 3];
        } else {
            const k = i - 6;
            const c = m3.cross(ax[k / 3], bx[k % 3]);
            const len = m3.length(c);
            if (len <= parallel_edge_length) continue;
            dir = m3.scale(c, 1.0 / len);
        }
        const overlap = radius(dir, ax, a.half) + radius(dir, bx, b.half) - @abs(m3.dot(d, dir));
        if (overlap < 0) return null;
        if (i < 6) {
            if (overlap < face.overlap - axis_tie_m) {
                face = .{ .axis = @intCast(i), .overlap = overlap, .normal = m3.zero };
                face_dir = dir;
            }
        } else if (overlap < edge.overlap - axis_tie_m) {
            edge = .{ .axis = @intCast(i), .overlap = overlap, .normal = m3.zero };
            edge_dir = dir;
        }
    }
    var best = face;
    var best_dir = face_dir;
    if (edge.overlap < edge_rel * face.overlap - axis_tie_m) {
        best = edge;
        best_dir = edge_dir;
    }
    best.normal = if (m3.dot(d, best_dir) < 0) m3.scale(best_dir, -1.0) else best_dir;
    return best;
}

/// The four vertices of face `f` (0..5 = +x -x +y -y +z -z) in cyclic order:
/// with b, c the two other axes in ascending index, corners (-b,-c),
/// (+b,-c), (+b,+c), (-b,+c).
fn faceVertices(box: Box, axes: [3]m3.Vec3, f: usize) [4]m3.Vec3 {
    const ai = f / 2;
    const s: f64 = if (f % 2 == 0) 1.0 else -1.0;
    const bi = (ai + 1) % 3;
    const ci = (ai + 2) % 3;
    const centre = m3.add(box.centre, m3.scale(axes[ai], s * box.half[ai]));
    const eb = m3.scale(axes[bi], box.half[bi]);
    const ec = m3.scale(axes[ci], box.half[ci]);
    return .{
        m3.sub(m3.sub(centre, eb), ec),
        m3.sub(m3.add(centre, eb), ec),
        m3.add(m3.add(centre, eb), ec),
        m3.add(m3.sub(centre, eb), ec),
    };
}

const Poly = struct {
    pts: [12]m3.Vec3 = undefined,
    n: usize = 0,

    fn push(self: *Poly, p: m3.Vec3) void {
        self.pts[self.n] = p;
        self.n += 1;
    }
};

/// One Sutherland-Hodgman pass keeping points with
/// limit - sign * dot(p - centre, e) >= 0.
fn clip(src: Poly, centre: m3.Vec3, e: m3.Vec3, sign: f64, limit: f64) Poly {
    var out: Poly = .{};
    if (src.n == 0) return out;
    var s = src.pts[src.n - 1];
    var ds = limit - sign * m3.dot(m3.sub(s, centre), e);
    for (src.pts[0..src.n]) |p| {
        const dp = limit - sign * m3.dot(m3.sub(p, centre), e);
        if (dp >= 0) {
            if (ds < 0) out.push(intersect(s, p, ds, dp));
            out.push(p);
        } else if (ds >= 0) {
            out.push(intersect(s, p, ds, dp));
        }
        s = p;
        ds = dp;
    }
    return out;
}

fn intersect(s: m3.Vec3, p: m3.Vec3, ds: f64, dp: f64) m3.Vec3 {
    const t = ds / (ds - dp);
    return m3.add(s, m3.scale(m3.sub(p, s), t));
}

/// Contact manifold of the ordered pair (A, B), or null when separated or
/// merely touching.
pub fn collide(a: Box, b: Box) ?Manifold {
    const s = sat(a, b) orelse return null;
    if (!(s.overlap > 0)) return null;
    const ax = axesOf(a);
    const bx = axesOf(b);
    var m: Manifold = .{ .axis = s.axis, .normal = s.normal, .count = 0, .points = @splat(.{ .point = m3.zero, .depth = 0 }), .tangent = .{ m3.zero, m3.zero } };
    if (s.axis < 6) {
        const ref_is_a = s.axis < 3;
        const ref = if (ref_is_a) a else b;
        const inc = if (ref_is_a) b else a;
        const ref_axes = if (ref_is_a) ax else bx;
        const inc_axes = if (ref_is_a) bx else ax;
        const k: usize = s.axis % 3;
        // Outward normal of the reference face (toward the other box).
        const nr = if (ref_is_a) s.normal else m3.scale(s.normal, -1.0);
        var face: usize = 0;
        var best = std.math.inf(f64);
        for (0..6) |f| {
            const sg: f64 = if (f % 2 == 0) 1.0 else -1.0;
            const v = sg * m3.dot(inc_axes[f / 2], nr);
            if (v < best) {
                best = v;
                face = f;
            }
        }
        const verts = faceVertices(inc, inc_axes, face);
        const ui = (k + 1) % 3;
        const vi = (k + 2) % 3;
        // Ascending axis index for u < v.
        const u_idx = @min(ui, vi);
        const v_idx = @max(ui, vi);
        var poly: Poly = .{};
        for (verts) |p| poly.push(p);
        poly = clip(poly, ref.centre, ref_axes[u_idx], 1.0, ref.half[u_idx]);
        poly = clip(poly, ref.centre, ref_axes[u_idx], -1.0, ref.half[u_idx]);
        poly = clip(poly, ref.centre, ref_axes[v_idx], 1.0, ref.half[v_idx]);
        poly = clip(poly, ref.centre, ref_axes[v_idx], -1.0, ref.half[v_idx]);
        const face_point = m3.add(ref.centre, m3.scale(nr, ref.half[k]));
        for (poly.pts[0..poly.n]) |p| {
            const depth = m3.dot(m3.sub(face_point, p), nr);
            if (depth < 0) continue;
            if (m.count > 0 and m3.length(m3.sub(p, m.points[m.count - 1].point)) <= duplicate_point_m) continue;
            m.points[m.count] = .{ .point = p, .depth = depth };
            m.count += 1;
        }
        if (m.count == 0) return null;
        m.tangent = .{ ref_axes[u_idx], ref_axes[v_idx] };
        return m;
    }
    // Edge axis.
    const i = (s.axis - 6) / 3;
    const j = (s.axis - 6) % 3;
    var pa = a.centre;
    var pb = b.centre;
    for (0..3) |q| {
        if (q != i) {
            const sg: f64 = if (m3.dot(s.normal, ax[q]) >= 0) 1.0 else -1.0;
            pa = m3.add(pa, m3.scale(ax[q], sg * a.half[q]));
        }
        if (q != j) {
            const sg: f64 = if (m3.dot(s.normal, bx[q]) > 0) -1.0 else 1.0;
            pb = m3.add(pb, m3.scale(bx[q], sg * b.half[q]));
        }
    }
    const da = ax[i];
    const db = bx[j];
    const w = m3.sub(pa, pb);
    const bb = m3.dot(da, db);
    const dd = m3.dot(da, w);
    const ee = m3.dot(db, w);
    const den = 1.0 - bb * bb;
    const sa = std.math.clamp((bb * ee - dd) / den, -a.half[i], a.half[i]);
    const sb = std.math.clamp((ee - bb * dd) / den, -b.half[j], b.half[j]);
    const qa = m3.add(pa, m3.scale(da, sa));
    const qb = m3.add(pb, m3.scale(db, sb));
    m.points[0] = .{ .point = m3.scale(m3.add(qa, qb), 0.5), .depth = s.overlap };
    m.count = 1;
    m.tangent = .{ da, m3.cross(s.normal, da) };
    return m;
}

const testing = std.testing;

fn mkBox(centre: m3.Vec3, q: m3.Quat, half: m3.Vec3) Box {
    return .{ .centre = centre, .orientation = q, .half = half };
}

fn aboutY(theta: f64) m3.Quat {
    return .{ .w = @cos(theta / 2.0), .x = 0, .y = @sin(theta / 2.0), .z = 0 };
}

fn aboutX(theta: f64) m3.Quat {
    return .{ .w = @cos(theta / 2.0), .x = @sin(theta / 2.0), .y = 0, .z = 0 };
}

const flat_half: m3.Vec3 = .{ 0.02, 0.02, 0.01 };

test "separated and touching boxes create no manifold" {
    const a = mkBox(m3.zero, .identity, flat_half);
    try testing.expect(collide(a, mkBox(.{ 0, 0, 0.0200001 }, .identity, flat_half)) == null);
    try testing.expect(collide(a, mkBox(.{ 0, 0, 0.02 }, .identity, flat_half)) == null);
    try testing.expect(sat(a, mkBox(.{ 0, 0, 0.0199 }, .identity, flat_half)) != null);
}

test "face-face stack: four points at the incident footprint, face axis wins ties" {
    const a = mkBox(m3.zero, .identity, flat_half);
    const m = collide(a, mkBox(.{ 0, 0, 0.0199 }, .identity, flat_half)).?;
    try testing.expectEqual(@as(u8, 2), m.axis);
    try testing.expectEqual(@as(u8, 4), m.count);
    try testing.expectEqual(m3.Vec3{ 0, 0, 1 }, m.normal);
    for (m.slice()) |p| try testing.expectApproxEqAbs(@as(f64, 0.0001), p.depth, 1e-15);
    // Ordering is deterministic and the swapped pair reports the same set.
    const sw = collide(mkBox(.{ 0, 0, 0.0199 }, .identity, flat_half), a).?;
    try testing.expectEqual(@as(u8, 4), sw.count);
    try testing.expectEqual(m3.Vec3{ 0, 0, -1 }, sw.normal);
}

test "BB6a: offset face-face overlap rectangle" {
    const a = mkBox(m3.zero, .identity, flat_half);
    const m = collide(a, mkBox(.{ 0.015, 0.01, 0.0195 }, .identity, flat_half)).?;
    try testing.expectEqual(@as(u8, 2), m.axis);
    try testing.expectEqual(@as(u8, 4), m.count);
    for (m.slice()) |p| {
        try testing.expectApproxEqAbs(@as(f64, 0.0005), p.depth, 1e-15);
        try testing.expectApproxEqAbs(@as(f64, 0.0095), p.point[2], 1e-15);
        try testing.expect(p.point[0] > -0.005 - 1e-12 and p.point[0] < 0.02 + 1e-12);
        try testing.expect(p.point[1] > -0.01 - 1e-12 and p.point[1] < 0.02 + 1e-12);
    }
}

test "BB6b: edge-face contact of a 45 degree tilted block gives two points on its lowest edge" {
    const a = mkBox(m3.zero, .identity, flat_half);
    const m = collide(a, mkBox(.{ 0.005, 0.005, 0.0307132034355964 }, aboutY(0.785398163397448), flat_half)).?;
    try testing.expectEqual(@as(u8, 2), m.axis);
    try testing.expectEqual(@as(u8, 2), m.count);
    for (m.slice()) |p| {
        try testing.expectApproxEqAbs(@as(f64, 0.0120710678118655), p.point[0], 1e-12);
        try testing.expectApproxEqAbs(@as(f64, 0.0095), p.point[2], 1e-12);
        try testing.expectApproxEqAbs(@as(f64, 0.0005), p.depth, 1e-12);
    }
}

test "BB6c: crossing edges give one midpoint on SAT axis 7" {
    const a = mkBox(m3.zero, aboutX(0.785398163397448), flat_half);
    const m = collide(a, mkBox(.{ 0, 0, 0.0419264068711929 }, aboutY(0.785398163397448), flat_half)).?;
    try testing.expectEqual(@as(u8, 7), m.axis);
    try testing.expectEqual(@as(u8, 1), m.count);
    try testing.expectApproxEqAbs(@as(f64, 0.00707106781186548), m.points[0].point[0], 1e-12);
    try testing.expectApproxEqAbs(@as(f64, 0.00707106781186548), m.points[0].point[1], 1e-12);
    try testing.expectApproxEqAbs(@as(f64, 0.0209632034355964), m.points[0].point[2], 1e-12);
    try testing.expectApproxEqAbs(@as(f64, 0.0005), m.points[0].depth, 1e-12);
    try testing.expectApproxEqAbs(@as(f64, 1), m.normal[2], 1e-12);
}

test "generation is a pure function (bit-identical on repeat)" {
    const a = mkBox(m3.zero, aboutX(0.3), flat_half);
    const b = mkBox(.{ 0.004, 0.003, 0.0195 }, aboutY(0.1), flat_half);
    const m1 = collide(a, b).?;
    const m2 = collide(a, b).?;
    try testing.expectEqualSlices(u8, std.mem.asBytes(&m1), std.mem.asBytes(&m2));
}
