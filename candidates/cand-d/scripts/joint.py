#!/usr/bin/env python3
"""cand-d body joint on paper: rotation range from the segment outlines, sector
sweep clearance, joint torque at the drive limit. Lengths mm, torques mN m.
Plain Python 3. Run: python3 joint.py
"""
import math
import json
from pathlib import Path

decl = json.loads((Path(__file__).resolve().parents[1] / "declaration.json").read_text())
comps = {c["id"]: c for c in decl["components"]}

GAP_HALF = 1.8       # segment inner faces at x = +-1.8, pivot at the origin
YO = 12.7            # segment outer half width
theta_max = math.degrees(2 * math.atan(GAP_HALF / YO))
print("segment outline contact (corner of one inner face on the other): +-%.2f deg" % theta_max)

# brute-force check of the plan outlines (rectangles) over the range
def rot(p, t):
    c, s = math.cos(t), math.sin(t)
    return (c * p[0] - s * p[1], s * p[0] + c * p[1])
def inside_L(p): return 1.8 < p[0] < 35.6 and abs(p[1]) < YO
S_corners = [(-1.8, YO), (-1.8, -YO)]
first = None
for k in range(0, 2001):
    t = math.radians(k * 0.01)
    for sgn in (1, -1):
        for c in S_corners:
            if inside_L(rot(c, sgn * t)) and first is None:
                first = k * 0.01
print("first outline contact found by sweep at %.2f deg (working range +-15, stop margin %.2f deg)" % (first, first - 15))

# hinge bosses: r 1.6 against the opposite inner face line at distance 1.8 from the pivot
print("boss r 1.6 to the opposite inner face: 0.20 mm at every angle (the face line stays 1.8 from the pivot)")

# Sector sweep (tail part); take its layer from the versioned declaration.
R_TIP = 8.7 + 0.3
jm = comps["joint-motor"]["box"]["pose"]["position_um"][:2]
ang = math.degrees(math.atan2(jm[1], jm[0]))
span = 21 + 15
lo, hi = ang - span, ang + span
print("sector swept sector in the head frame: %.1f..%.1f deg, r <= %.2f" % (lo, hi, R_TIP))
def axis_bounds(box):
    """Conservative AABB even for rotated parts."""
    w, x, y, z = box["pose"]["orientation"]
    m = [[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)],
         [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)],
         [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]]
    he = box["half_extent_um"]
    dh = [sum(abs(a)*h for a, h in zip(row, he)) for row in m]
    return [((c-h)/1000, (c+h)/1000) for c, h in zip(box["pose"]["position_um"], dh)]

# Each wedge contains its entire annular arc (inner chord inside, outer
# chord tangent). Unlike sampling poses, gaps between angles aren't omitted.
def wedge(deg0, deg1):
    r = R_TIP/math.cos(math.radians(deg1-deg0)/2)
    return [rot((rr, 0), math.radians(t)) for rr, t in
            ((4.5, deg0), (r, deg0), (r, deg1), (4.5, deg1))]

def overlaps(a, b):
    for poly in (a, b):
        for p, q in zip(poly, poly[1:]+poly[:1]):
            nx, ny = q[1]-p[1], p[0]-q[0]
            proj_a = [nx*x+ny*y for x,y in a]
            proj_b = [nx*x+ny*y for x,y in b]
            if max(proj_a) < min(proj_b) or max(proj_b) < min(proj_a):
                return False
    return True

sector_z = axis_bounds(comps["joint-sector"]["box"])[2]
wedges = [wedge(lo+i, lo+i+1) for i in range(2*span)]
for cid, c in comps.items():
    if cid in ("joint-pinion", "joint-sector", "hinge-plate-low"):
        continue  # intended gear mesh / sector stock
    (x0,x1), (y0,y1), (z0,z1) = axis_bounds(c["box"])
    if x1 < 0 or z0 >= sector_z[1] or z1 <= sector_z[0]:
        continue
    rect = [(x0,y0), (x1,y0), (x1,y1), (x0,y1)]
    assert not any(overlaps(w, rect) for w in wedges), f"sector sweep not clear of {cid}"
print("full swept sector clears stationary component box bounds (excluding intended gear mesh)")

# torque
I = 58 / 12
for n, tm in (("rated 3 mN m (drive limit)", 3.0), ("stall at 3.0 V", 9.0), ("stall at 3.6 V (fault)", 10.8)):
    print("joint torque, motor %s: %.1f mN m (eta 1, upper bound)" % (n, tm * I))
W = sum(c["mass_mg"] for c in comps.values())*1e-6*9.80665
for n_units in (1, 2):
    lever = 47.2 * n_units / 2 + 1.8
    print("  pushing %d unit(s) sideways at mu 0.3 (PROVISIONAL), lever %.1f mm: %.1f mN m" % (n_units, lever, 0.3 * W * n_units * lever))
