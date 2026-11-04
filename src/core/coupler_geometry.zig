//! Pure geometry of the fixture coupler stand-in's guide contacts (Q56 §3, §4):
//! sphere versus a square-pyramid socket and its surrounding face, in the
//! coupler frame of body A. No dynamics, no allocation, std only.
//!
//! Frame: origin at the centre of A's coupler face plane, +x along the coupler
//! axis (out of A), y and z along A's body axes (mouth edges along y and z).
//! Material of A is x <= 0 minus the recess. The recess is the square pyramid
//! with apex (-D, 0, 0) and mouth |y|,|z| <= w at x = 0; its half-width at
//! depth x is w(x + D)/D.
//!
//! Voronoi / tie rules (each reported contact is a local minimum of distance
//! to the surface, so a single geometric contact is never counted twice):
//!
//! * Facet i (outward coordinate u = s*c[axis]): signed distance to its plane
//!   toward free space is sd = (w(cx + D) - D*u)/N, N = sqrt(D^2 + w^2).
//!   A facet reports only if sd >= 0 for ALL four facet planes (the centre is
//!   inside the pyramid extended above the mouth, so the segment to the
//!   contact point cannot be occluded by the face) and the orthogonal
//!   projection q lies in the facet: -D <= qx <= 0 and |q_lat| <= w(qx+D)/D.
//!   Concave ridges: several facets may report simultaneously (a ball in the
//!   recess touches each of them). A projection exactly on a ridge is owned by
//!   the lower-index facet: facet_py/ny use the closed lateral bound,
//!   facet_pz/nz the strict one. The apex is covered by the facet clamp.
//! * Face: cx >= 0, |cy|,|cz| <= H, and max(|cy|,|cz|) > w (strict), so the
//!   mouth boundary belongs to the rim.
//! * Rim edge (side with outward coordinate u): u <= w, |c_lat| < w (strict),
//!   cx >= 0 and D*cx + w(u - w) > 0 (strict; equality is the facet-projection
//!   -on-rim tie, owned by the facet). This is the exact normal cone of the
//!   convex 135 degree rim edge.
//! * Corner: the mouth corner is a reflex vertex of the face (the face wraps
//!   270 degrees around it), so it is the nearest surface point only for
//!   centres exactly on the ray above it: cx >= 0, cy == +-w, cz == +-w
//!   (exact floating-point equality). At that ray the strict face/edge tests
//!   above exclude all other pieces, so the corner reports alone.
//!
//! A valid feature is reported iff depth = rho - distance >= -1e-15 m (a
//! rounding guard; the nominal rule is depth >= 0).

const std = @import("std");
const m3 = @import("math3.zig");

pub const Params = struct {
    apex_depth_m: f64,
    mouth_half_width_m: f64,
    face_half_size_m: f64,
};

pub const Feature = enum(u8) {
    facet_py,
    facet_ny,
    facet_pz,
    facet_nz,
    face,
    edge_py,
    edge_ny,
    edge_pz,
    edge_nz,
    corner_pp,
    corner_pn,
    corner_np,
    corner_nn,
};

pub const Contact = struct {
    feature: Feature,
    /// Closest point on A's surface, coupler frame.
    point: m3.Vec3,
    /// Unit, from A's surface toward the ball centre, coupler frame.
    normal: m3.Vec3,
    /// rho - distance; > 0 penetrating.
    depth: f64,
};

/// Rounding guard on the "depth >= 0" activation test (1 fm), so a ball seated
/// exactly at depth 0 is not lost to the last bit of binary64.
const depth_eps: f64 = 1e-15;

const axis_of = [4]usize{ 1, 1, 2, 2 };
const lat_of = [4]usize{ 2, 2, 1, 1 };
const sign_of = [4]f64{ 1, -1, 1, -1 };

pub fn seatX(p: Params, rho: f64) f64 {
    const alpha = std.math.atan2(p.mouth_half_width_m, p.apex_depth_m);
    return rho / @sin(alpha) - p.apex_depth_m;
}

fn unit(v: m3.Vec3) m3.Vec3 {
    return m3.scale(v, 1.0 / m3.length(v));
}

fn facetNormal(p: Params, i: usize) m3.Vec3 {
    const n = @sqrt(p.apex_depth_m * p.apex_depth_m + p.mouth_half_width_m * p.mouth_half_width_m);
    var v: m3.Vec3 = .{ p.mouth_half_width_m / n, 0, 0 };
    v[axis_of[i]] = -sign_of[i] * p.apex_depth_m / n;
    return v;
}

/// Fills `out` (indexed by `Feature`) with active guide contacts and returns
/// their count.
pub fn contacts(p: Params, centre: m3.Vec3, rho: f64, out: *[13]?Contact) usize {
    out.* = @splat(null);
    var count: usize = 0;
    const D = p.apex_depth_m;
    const w = p.mouth_half_width_m;
    const H = p.face_half_size_m;
    const cx = centre[0];
    const N = @sqrt(D * D + w * w);

    // Facets.
    var sd: [4]f64 = undefined;
    var all_free = true;
    for (0..4) |i| {
        sd[i] = (w * (cx + D) - D * sign_of[i] * centre[axis_of[i]]) / N;
        if (!(sd[i] >= 0)) all_free = false;
    }
    if (all_free) {
        for (0..4) |i| {
            const nrm = facetNormal(p, i);
            const q = m3.sub(centre, m3.scale(nrm, sd[i]));
            if (q[0] < -D or q[0] > 0) continue;
            const lw = w * (q[0] + D) / D;
            const lat = @abs(q[lat_of[i]]);
            const inside = if (i < 2) lat <= lw else lat < lw;
            if (!inside) continue;
            const depth = rho - sd[i];
            if (depth >= -depth_eps) {
                out[i] = .{ .feature = @enumFromInt(i), .point = q, .normal = nrm, .depth = depth };
                count += 1;
            }
        }
    }

    // Face.
    if (cx >= 0 and @abs(centre[1]) <= H and @abs(centre[2]) <= H and
        @max(@abs(centre[1]), @abs(centre[2])) > w)
    {
        const depth = rho - cx;
        if (depth >= -depth_eps) {
            out[4] = .{
                .feature = .face,
                .point = .{ 0, centre[1], centre[2] },
                .normal = .{ 1, 0, 0 },
                .depth = depth,
            };
            count += 1;
        }
    }

    // Rim edges.
    for (0..4) |i| {
        const a = axis_of[i];
        const l = lat_of[i];
        const s = sign_of[i];
        const u = s * centre[a];
        if (!(cx >= 0 and u <= w and @abs(centre[l]) < w and D * cx + w * (u - w) > 0)) continue;
        var q: m3.Vec3 = .{ 0, 0, 0 };
        q[a] = s * w;
        q[l] = centre[l];
        const d = m3.sub(centre, q);
        const dist = m3.length(d);
        const depth = rho - dist;
        if (depth < -depth_eps) continue;
        const nrm = if (dist > 0) m3.scale(d, 1.0 / dist) else unit(m3.add(.{ 1, 0, 0 }, facetNormal(p, i)));
        out[5 + i] = .{ .feature = @enumFromInt(5 + i), .point = q, .normal = nrm, .depth = depth };
        count += 1;
    }

    // Corners: only on the exact ray above the corner point.
    for (0..4) |i| {
        const sy: f64 = if (i < 2) 1 else -1;
        const sz: f64 = if (i % 2 == 0) 1 else -1;
        if (!(cx >= 0 and centre[1] == sy * w and centre[2] == sz * w)) continue;
        const depth = rho - cx;
        if (depth < -depth_eps) continue;
        out[9 + i] = .{
            .feature = @enumFromInt(9 + i),
            .point = .{ 0, sy * w, sz * w },
            .normal = .{ 1, 0, 0 },
            .depth = depth,
        };
        count += 1;
    }
    return count;
}

// ---------------------------------------------------------------- tests

const testing = std.testing;

const P: Params = .{ .apex_depth_m = 0.004, .mouth_half_width_m = 0.004, .face_half_size_m = 0.01 };
const RHO: f64 = 0.002;
const s45 = @sqrt(0.5);

test "seatX matches Q56" {
    try testing.expectApproxEqAbs(-1.1716e-3, seatX(P, RHO), 1e-7);
}

test "seated ball touches four facets with zero depth" {
    var out: [13]?Contact = undefined;
    const n = contacts(P, .{ seatX(P, RHO), 0, 0 }, RHO, &out);
    try testing.expectEqual(@as(usize, 4), n);
    var sum: m3.Vec3 = m3.zero;
    for (0..4) |i| {
        const c = out[i].?;
        try testing.expect(@abs(c.depth) < 1e-12);
        try testing.expectApproxEqAbs(s45, c.normal[0], 1e-12);
        sum = m3.add(sum, c.normal);
    }
    for (4..13) |i| try testing.expect(out[i] == null);
    try testing.expectApproxEqAbs(4 * s45, sum[0], 1e-12);
    try testing.expectApproxEqAbs(@as(f64, 0), sum[1], 1e-12);
    try testing.expectApproxEqAbs(@as(f64, 0), sum[2], 1e-12);
    // y/z normal components are exactly +-s45 on the right axes.
    try testing.expectApproxEqAbs(-s45, out[0].?.normal[1], 1e-12);
    try testing.expectApproxEqAbs(s45, out[1].?.normal[1], 1e-12);
    try testing.expectApproxEqAbs(-s45, out[2].?.normal[2], 1e-12);
    try testing.expectApproxEqAbs(s45, out[3].?.normal[2], 1e-12);
}

test "pushed 0.05 mm deeper" {
    var out: [13]?Contact = undefined;
    const n = contacts(P, .{ seatX(P, RHO) - 0.05e-3, 0, 0 }, RHO, &out);
    try testing.expectEqual(@as(usize, 4), n);
    for (0..4) |i| try testing.expectApproxEqAbs(0.05e-3 * s45, out[i].?.depth, 1e-12);
}

test "far above: no contacts" {
    var out: [13]?Contact = undefined;
    try testing.expectEqual(@as(usize, 0), contacts(P, .{ 0.01, 0, 0 }, RHO, &out));
}

test "resting on the face" {
    var out: [13]?Contact = undefined;
    const n = contacts(P, .{ RHO, 0.006, 0.001 }, RHO, &out);
    try testing.expectEqual(@as(usize, 1), n);
    const c = out[@intFromEnum(Feature.face)].?;
    try testing.expectEqual(@as(f64, 0), c.depth);
    try testing.expectEqual(@as(f64, 1), c.normal[0]);
    try testing.expectEqual(@as(f64, 0), c.normal[1]);
}

test "over a rim edge" {
    var out: [13]?Contact = undefined;
    const centre: m3.Vec3 = .{ 1e-3, 0.0035, 0 };
    const n = contacts(P, centre, RHO, &out);
    try testing.expectEqual(@as(usize, 1), n);
    const c = out[@intFromEnum(Feature.edge_py)].?;
    try testing.expectEqual(@as(f64, 0.004), c.point[1]);
    const d = m3.sub(centre, c.point);
    const u = unit(d);
    for (0..3) |k| try testing.expectApproxEqAbs(u[k], c.normal[k], 1e-12);
    try testing.expectApproxEqAbs(RHO - m3.length(d), c.depth, 1e-15);
}

test "over a corner" {
    var out: [13]?Contact = undefined;
    const n = contacts(P, .{ 1e-3, 0.004, 0.004 }, RHO, &out);
    try testing.expectEqual(@as(usize, 1), n);
    try testing.expect(out[@intFromEnum(Feature.corner_pp)] != null);
    const n2 = contacts(P, .{ 1e-3, 0.004, -0.004 }, RHO, &out);
    try testing.expectEqual(@as(usize, 1), n2);
    try testing.expect(out[@intFromEnum(Feature.corner_pn)] != null);
}

// Brute-force reference ------------------------------------------------

fn segClosest(c: m3.Vec3, a: m3.Vec3, b: m3.Vec3) m3.Vec3 {
    const ab = m3.sub(b, a);
    var t = m3.dot(m3.sub(c, a), ab) / m3.dot(ab, ab);
    t = @min(@max(t, 0), 1);
    return m3.add(a, m3.scale(ab, t));
}

/// Exact distance from `c` to the union surface by brute force over pieces.
fn bruteDistance(c: m3.Vec3) f64 {
    const D = P.apex_depth_m;
    const w = P.mouth_half_width_m;
    const H = P.face_half_size_m;
    var best: f64 = std.math.inf(f64);
    const apex: m3.Vec3 = .{ -D, 0, 0 };
    const sg = [2]f64{ 1, -1 };
    for (sg) |sy| for (sg) |sz| {
        const corner: m3.Vec3 = .{ 0, sy * w, sz * w };
        best = @min(best, m3.length(m3.sub(c, segClosest(c, corner, apex))));
    };
    for (sg) |s| {
        const e1 = segClosest(c, .{ 0, s * w, -w }, .{ 0, s * w, w });
        const e2 = segClosest(c, .{ 0, -w, s * w }, .{ 0, w, s * w });
        best = @min(best, m3.length(m3.sub(c, e1)));
        best = @min(best, m3.length(m3.sub(c, e2)));
    }
    // Face: clamp to the half-size square; outside the mouth only.
    const fy = @min(@max(c[1], -H), H);
    const fz = @min(@max(c[2], -H), H);
    if (@max(@abs(fy), @abs(fz)) >= w) best = @min(best, m3.length(m3.sub(c, .{ 0, fy, fz })));
    // Facet interiors.
    const N = @sqrt(D * D + w * w);
    for (0..4) |i| {
        const s = sign_of[i];
        const sdi = (w * (c[0] + D) - D * s * c[axis_of[i]]) / N;
        const q = m3.sub(c, m3.scale(facetNormal(P, i), sdi));
        if (q[0] >= -D and q[0] <= 0 and @abs(q[lat_of[i]]) <= w * (q[0] + D) / D)
            best = @min(best, @abs(sdi));
    }
    return best;
}

fn isFree(c: m3.Vec3) bool {
    if (c[0] > 0) return true;
    if (c[0] < -P.apex_depth_m) return false;
    const w = P.mouth_half_width_m;
    const lim = w * (c[0] + P.apex_depth_m) / P.apex_depth_m;
    return @abs(c[1]) <= lim and @abs(c[2]) <= lim;
}

fn onSurface(f: Feature, q: m3.Vec3) bool {
    const D = P.apex_depth_m;
    const w = P.mouth_half_width_m;
    const H = P.face_half_size_m;
    const tol = 1e-12;
    const i = @intFromEnum(f);
    switch (f) {
        .facet_py, .facet_ny, .facet_pz, .facet_nz => {
            const lw = w * (q[0] + D) / D;
            return @abs(sign_of[i] * q[axis_of[i]] - lw) <= tol and q[0] >= -D - tol and
                q[0] <= tol and @abs(q[lat_of[i]]) <= lw + tol;
        },
        .face => return @abs(q[0]) <= tol and @abs(q[1]) <= H + tol and @abs(q[2]) <= H + tol and
            @max(@abs(q[1]), @abs(q[2])) >= w - tol,
        .edge_py, .edge_ny, .edge_pz, .edge_nz => {
            const k = i - 5;
            return @abs(q[0]) <= tol and @abs(sign_of[k] * q[axis_of[k]] - w) <= tol and
                @abs(q[lat_of[k]]) <= w + tol;
        },
        else => return @abs(q[0]) <= tol and @abs(@abs(q[1]) - w) <= tol and @abs(@abs(q[2]) - w) <= tol,
    }
}

const Lcg = struct {
    s: u64,
    fn next(self: *Lcg) f64 {
        self.s = self.s *% 6364136223846793005 +% 1442695040888963407;
        return @as(f64, @floatFromInt(self.s >> 11)) / 9007199254740992.0;
    }
};

test "property: contacts are exact, consistent, and complete" {
    var rng: Lcg = .{ .s = 0x9E3779B97F4A7C15 };
    var out: [13]?Contact = undefined;
    var tested: usize = 0;
    var touching: usize = 0;
    var multi: usize = 0;
    for (0..2000) |_| {
        const c: m3.Vec3 = .{
            -0.004 + 0.012 * rng.next(),
            -0.006 + 0.012 * rng.next(),
            -0.006 + 0.012 * rng.next(),
        };
        if (!isFree(c)) continue;
        tested += 1;
        const n = contacts(P, c, RHO, &out);
        try testing.expect(n <= 4);
        const brute = bruteDistance(c);
        var cnt: usize = 0;
        var min_dist: f64 = std.math.inf(f64);
        for (out, 0..) |maybe, idx| {
            const ct = maybe orelse continue;
            cnt += 1;
            try testing.expectEqual(idx, @intFromEnum(ct.feature));
            try testing.expect(ct.depth >= -1e-15);
            try testing.expect(onSurface(ct.feature, ct.point));
            const d = m3.sub(c, ct.point);
            const dist = m3.length(d);
            try testing.expectApproxEqAbs(RHO - ct.depth, dist, 1e-12);
            const u = unit(d);
            for (0..3) |k| try testing.expectApproxEqAbs(u[k], ct.normal[k], 1e-9);
            try testing.expect(brute <= dist + 1e-12);
            min_dist = @min(min_dist, dist);
        }
        try testing.expectEqual(n, cnt);
        if (brute > RHO + 1e-15) try testing.expectEqual(@as(usize, 0), n);
        if (brute <= RHO - 1e-9) {
            try testing.expect(n >= 1);
            try testing.expectApproxEqAbs(brute, min_dist, 1e-12);
        }
        if (n > 0) touching += 1;
        if (n > 1) multi += 1;
    }
    try testing.expect(tested > 500);
    try testing.expect(touching > 100);
    try testing.expect(multi > 0);
}

test "determinism: identical inputs give bit-identical outputs" {
    var a: [13]?Contact = undefined;
    var b: [13]?Contact = undefined;
    const c: m3.Vec3 = .{ -0.0007, 0.0011, -0.0003 };
    const na = contacts(P, c, RHO, &a);
    const nb = contacts(P, c, RHO, &b);
    try testing.expectEqual(na, nb);
    try testing.expect(std.mem.eql(u8, std.mem.asBytes(&a), std.mem.asBytes(&b)));
}
