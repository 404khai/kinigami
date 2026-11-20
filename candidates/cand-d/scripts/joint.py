#!/usr/bin/env python3
"""cand-d body joint on paper: rotation range from the segment outlines, sector
sweep clearance, joint torque at the drive limit. Lengths mm, torques mN m.
Plain Python 3. Run: python3 joint.py
"""
import math

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

# sector sweep (tail part) through the head bottom layer: z -10.7..-9.2
R_TIP = 8.7 + 0.3
jm = (6.2, 8.47)
ang = math.degrees(math.atan2(jm[1], jm[0]))
span = 21 + 15
lo, hi = ang - span, ang + span
print("sector swept sector in the head frame: %.1f..%.1f deg, r <= %.2f" % (lo, hi, R_TIP))
# nearest head part in that layer is the coupler motor box x >= 9.3, y 0.3..6.3, z -10.25..-4.25
xmax = max(R_TIP * math.cos(math.radians(a)) for a in [lo + i * 0.1 for i in range(int((hi - lo) * 10) + 1)])
print("sector reaches x <= %.2f; coupler motor box starts at x 9.30: clearance %.2f" % (xmax, 9.30 - xmax))
ymin = R_TIP * math.sin(math.radians(lo))
print("sector stays at y >= %.2f at the tip (cell box y <= -3.80)" % min(ymin, 4.5 * math.sin(math.radians(lo))))

# torque
I = 58 / 12
for n, tm in (("rated 3 mN m (drive limit)", 3.0), ("stall at 3.0 V", 9.0), ("stall at 3.6 V (fault)", 10.8)):
    print("joint torque, motor %s: %.1f mN m (eta 1, upper bound)" % (n, tm * I))
W = 0.2966
for n_units in (1, 2):
    lever = 47.2 * n_units / 2 + 1.8
    print("  pushing %d unit(s) sideways at mu 0.3 (PROVISIONAL), lever %.1f mm: %.1f mN m" % (n_units, lever, 0.3 * W * n_units * lever))
