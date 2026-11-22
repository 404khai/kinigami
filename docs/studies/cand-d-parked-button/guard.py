"""Exploratory Take 43. Run with python3; dimensions in mm."""
from math import acos, cos, dist, hypot, pi, radians, sin, sqrt, tan

XP, H, A, R, S = 12.389796, 7.53675, 7.5, 4.20, 3.225
ANG = radians(28)
K, C, SN = tan(ANG), cos(ANG), sin(ANG)
REAR, OPEN, FRONT, STOCK = 7.75, 9.649, 18.4, 0.4
SKIN, PARK = 0.2, 12.8
BOSSES = [(16.57, 0, -8.65), (11.54, 9.526, 7.07), (11.54, -9.526, 7.07)]
STEM = [(22.5, 0, 0), (26, 0, 0)]
RHO = 0.48 + 0.32*11.84


def lip(x):
    return H + K*(x-XP)


def side(x):
    return 4.935 - 0.25*(x-XP)


def top(x):
    return 28.2 - 0.26*(x-XP)


def root(b):
    x, y, _ = b
    d = hypot(x-15, y)
    return (15+A*(x-15)/d, A*y/d, 0)


def work(nx):
    a = min(pi, acos(nx) + radians(1))
    return cos(a) - 0.23*sin(a)


def output(label, *v):
    print(label, *(f"{x:.6f}" for x in v))


def shell():
    for drop in (0, 5, 6, 7):
        # Convex norm on a polytope: test every vertex.
        radius = max(hypot(x+3, side(x), z-drop)
                     for x in (REAR, FRONT) for z in (lip(x), top(x)))
        output("drop / outer hood sphere radius / bottom boss floor gap",
               drop, radius, 23.65 - drop - 8.65 - R)
        if drop in (6, 7):
            assert radius < 30
    output("original shoulder radius / support along 12 deg / +X work",
           hypot(XP+RHO+3, 26.8), (XP+RHO+3)*sin(radians(12))+26.8*cos(radians(12)),
           sin(radians(12))-0.23*cos(radians(12)))
    # Intersection of each vertical stock layer with moving cone is largest at lock,
    # then largest at the uppermost layer. In X=x-XP: X^2+y^2 <= (a+kX)^2.
    a, k = 0.48+0.32*(H+STOCK), 0.32*K
    output("cone/slot rear and lateral clearances", XP-a/(1+k)-OPEN,
           S-a/sqrt(1-k*k))
    margins = (XP-RHO-REAR-SKIN, FRONT-SKIN-XP-RHO,
               (side(XP)-SKIN)/hypot(1, 0.25)-RHO,
               top(XP+RHO)-SKIN-26.8)
    output("parked cylinder rear/front/side/top shell clearance", *margins)
    assert min(margins) > 0 and side(FRONT)-S > SKIN
    # Trial rectangular bridge locks at z=13.9..14.6, x=8.2..XP+.5, |y|<=.8.
    bridge = (8.2-REAR-SKIN, side(XP+0.5)-0.8-SKIN,
              top(XP+0.5)-SKIN-(14.6+PARK))
    output("parked bridge clearances rear/side/top (axis distances)", *bridge)
    assert min(bridge) > 0
    L = [dist(root(b), b) for b in BOSSES]
    lengths = [R, *[hypot(l/2, 2) for l in L], dist(*STEM)+2.2]
    d = sqrt(R*R-S*S)
    output("reach to a generator centre: eye+boss / necks / stem", *lengths)
    output("maximum aperture penetration by those constituents", *(v-d for v in lengths))
    depth = (PARK-0.80-lip(XP+0.48-0.32*0.80))*C
    output("minimum parked depths: lower plane / open-front notch / reserve",
           depth, depth-C*STOCK, depth-C*STOCK-max(lengths)+d)
    assert depth-C*STOCK > max(lengths)-d
    output("conservative +X work per N: intact lower lip, roof, outer side, top, front",
           work(SN*d/R), work(SN), work(0.25/hypot(1, 0.25)),
           work(0.26/hypot(1, 0.26)), work(1))
    assert work(0.25/hypot(1, 0.25)) > 0


def aligned():
    def under(p, r):
        return (lip(p[0])-p[2])*C-r

    def outside(p, r):
        return (abs(p[1])-side(p[0]))/hypot(1, 0.25)-r

    gaps = (under((15-A, 0, 0), R), under(BOSSES[0], R),
            min(under(p, 2) for p in (root(BOSSES[0]), BOSSES[0])),
            min(under(p, 2.2) for p in STEM),
            outside(BOSSES[1], R),
            min(outside(p, 2) for p in (root(BOSSES[1]), BOSSES[1])))
    output("aligned hood gaps: ring, lower boss/neck, stem, upper bosses/necks", *gaps)
    output("aligned parked tip vertical gap", PARK-0.8-(7.07+R))
    assert min(gaps) > 0


def vgap(p, b, swept=True):
    # Two prismatic facets; optionally sweep infinitely aft for aligned tail exit.
    x, y, z = (x0-x1 for x0, x1 in zip(p, b))
    _, by, bz = b
    d = hypot(by, bz)
    u, v = abs((-bz*y+by*z)/d), abs((by*y+bz*z)/d)
    u1, v1, x0 = 3.8, 1.5, -R*sqrt(2)
    clamp = lambda w: min(u1, max(0, w))
    w = clamp(u)
    a = hypot(u-w, max(0, x-x0-w))
    w = clamp((x-x0+u)/2)
    a = min(a, hypot(u-w, x-x0-w))
    if not swept and x < x0+clamp(u)-STOCK:
        w = clamp((x-x0+STOCK+u)/2)
        a = hypot(u-w, x-x0+STOCK-w)
        for w in (0, u1):
            a = min(a, hypot(u-w, max(0, x-x0-w, x0+w-STOCK-x)))
    return hypot(a, max(0, v-v1))


def centres():
    count = 720
    yield "eye", [(15+A*cos(i*2*pi/count), A*sin(i*2*pi/count), 0)
                  for i in range(count)], R, A*pi/count
    for i, b in enumerate(BOSSES):
        yield f"boss{i}", [b], R, 0
    for i, (a, b) in enumerate([(root(b), b) for b in BOSSES]+[STEM]):
        yield ("stem" if i == 3 else f"neck{i}"), [
            tuple(x+(y-x)*j/100 for x, y in zip(a, b)) for j in range(101)
        ], (2.2 if i == 3 else 2), dist(a, b)/200


def face():
    output("45-degree V facet +X work", work(1/sqrt(2)))
    for i, b in enumerate(BOSSES):
        gaps = [(min(vgap(p, b) for p in pts)-r-err, name)
                for name, pts, r, err in centres() if name != f"boss{i}"]
        other, name = min(gaps)
        output(f"V{i}: intended tangent / other tail minimum ({name})",
               vgap(b, b)-R, other)
        assert abs(vgap(b, b)-R) < 1e-12 and other > 0
        bx, by, bz = b
        d = hypot(by, bz)
        hood = []
        for u in (-3.8, 0, 3.8):
            for v in (-1.5, 1.5):
                x = bx-R*sqrt(2)+abs(u)-STOCK
                y, z = by+(-u*bz+v*by)/d, bz+(u*by+v*bz)/d
                hood.append((lip(x)-z)*C if i == 0
                            else (abs(y)-side(x))/hypot(1, 0.25))
        output(f"V{i} blade stock vs hood (home then +X)", min(hood))
        assert min(hood) > 0


def wedge_distance(x, h, xedge, h0, sign):
    # Exact point distance to sign*(x-xedge)>=0 AND h>=h0, h normal to lower plane.
    a, q, dot = sign*(x-xedge), h-h0, -SN*sign
    if min(a, q) >= 0:
        return 0
    if q < 0 and a-q*dot >= 0:
        return -q
    if a < 0 and q-a*dot >= 0:
        return -a
    return sqrt((a*a-2*dot*a*q+q*q)/(1-dot*dot))


def slot_side_witness():
    # Local +X of tail = c*n+b*Y; local +Y = upslope tangent; +Z = c*Y-b*n.
    # Place terminal centre x=14.25, y=S-2.2, signed height h=.15 above lower plane.
    b, e = 0.25, 0.15
    c = sqrt(1-b*b)
    v_at_home, v_relieved, floor = [], [], []
    for name, pts, r, err in centres():
        world = []
        for xx, yy, zz in pts:
            dx = xx-26
            h = e+c*dx-b*zz
            x = 14.25-SN*(h-e)+C*yy
            y = S-2.2+b*dx+c*zz
            world.append((x, y, lip(x)+h/C))
        for offset, gaps_ in ((0, v_at_home), (-6, v_relieved)):
            gaps_.append(min(vgap(p, (bx+offset, by, bz), swept=False) for p in world
                             for bx, by, bz in BOSSES)-r-err)
        floor.append(min(p[2] for p in world)-r-err+23.65-7)
        if name == "stem":
            # Entire capsule stays in lateral opening; check front and rear limits.
            output("stem x extents", 14.25-2.2, 14.25+3.5*c*SN+2.2)
            assert 14.25-2.2 > OPEN and 14.25+3.5*c*SN+2.2 < FRONT-SKIN
            continue
        gaps = []
        for xx, yy, zz in pts:
            dx = xx-26
            h = e+c*dx-b*zz
            x = 14.25-SN*(h-e)+C*yy
            y = S-2.2+b*dx+c*zz
            # Supersets of all hood stock, except the high roof which is counted separately.
            gaps.append(min(hypot(max(0, S-abs(y)), max(0, -h)),
                            wedge_distance(x, h, OPEN, 0, -1),
                            wedge_distance(x, h, FRONT-SKIN, STOCK*C, 1),
                            (top(x)-SKIN-(lip(x)+h/C))/hypot(1, 0.26)))
        gap = min(gaps)-r-err
        output(f"side-contact pose: {name} vs hood", gap)
        assert gap > 0
    output("same pose: V stock at home / illustrative -6 relief / floor",
           min(v_at_home), min(v_relieved), min(floor))
    assert min(v_at_home) < -0.1 and min(v_relieved) > 0 and min(floor) > 0
    output("actual lateral lip-on-stem face: nominal worst +X work", -0.23)


if __name__ == "__main__":
    print("exploratory; millimetres; +X work in N/N")
    shell()
    aligned()
    face()
    slot_side_witness()
