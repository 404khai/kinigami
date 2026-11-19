"""Second (torsion) pin: roll-in path in B's body frame and a packing map against the declared boxes.
Body frame: x, z with +z DOWN at rest (F3 down), peg axis along y. B-frame y of the pin tip: y_B = Lp - 22 (A head face y 14, B tail face at A-frame y 22).
Path (same table-height method as the peg, dossier 7.1): p(phi) = V + R(phi) [ (25.5, 0) + R(-60) d ],
V = (-12.75, 22.084), R(t) = [[cos t, sin t], [-sin t, cos t]], phi 0..60 deg; at phi = 60 p = d (pin docks at the same body offset d)."""
import math

R = 25.5
AP = 22.0836
V = (-R / 2, AP)

def Rot(t, v):
    c, s = math.cos(math.radians(t)), math.sin(math.radians(t))
    return (v[0] * c + v[1] * s, -v[0] * s + v[1] * c)

def path(d, mirror=False, n=61):
    out = []
    for i in range(n):
        phi = 60.0 * i / (n - 1)
        q0 = Rot(-60, d)
        q = Rot(phi, (R + q0[0], q0[1]))
        p = (V[0] + q[0], V[1] + q[1])
        out.append((-p[0], p[1]) if mirror else p)
    return out

def in_hex(p, m=0.0):
    x, z = abs(p[0]), p[1]
    return abs(z) <= AP - m and x <= R - m - abs(z) * (R / 2) / AP * (1) * (R / (R / 2)) / (R / (R / 2)) * 1.0 if False else (abs(z) <= AP - m and 0.8660254 * x + 0.5 * abs(z) <= AP - m)

# obstacles: (name, kind, params, ymin, ymax); rect = (x0, x1, z0, z1), circ = (cx, cz, r)
OBST = [
    ('cell', 'rect', (-15.5, 15.5, -11.2, -3.7), -11.9, 8.1),
    ('controller', 'rect', (-8.9, 8.9, -17.35, -11.65), -12.0, 10.0),
    ('lift-motor', 'circ', (-12.55, 2.63, 3.0), -11.16, 9.6),
    ('yaw-puck', 'rect', (-3.6, 3.6, -3.5, 6.9), -7.0, -4.4),
    ('seat', 'rect', (-2.4, 2.4, -3.3, -2.45), -11.0, -7.5),
    ('tongue-stroke', 'rect', (-2.05, 2.05, 0.0, 8.6), -9.4, -8.4),
    ('collar+saddle', 'rect', (-2.15, 2.15, 9.3, 10.7), -12.0, -7.4),
    ('frame-m3', 'rect', (-6.8, -2.2, 9.97, 14.57), -12.0, -7.9),
    ('frame-base', 'rect', (-2.2, 6.3, 10.7, 14.3), -12.0, -11.4),
    ('rocker-post', 'rect', (4.25, 6.25, 14.3, 16.3), -12.0, -7.3),
    ('cap-strip-l', 'rect', (-14.5, -3.9, -3.6, -1.6), -12.0, -7.0),
    ('cap-strip-r', 'rect', (3.9, 14.5, -3.6, -1.6), -12.0, -7.0),
]

def dist_obst(p, o):
    kind, par = o[1], o[2]
    if kind == 'rect':
        x0, x1, z0, z1 = par
        dx = max(x0 - p[0], 0, p[0] - x1)
        dz = max(z0 - p[1], 0, p[1] - z1)
        return math.hypot(dx, dz)
    cx, cz, r = par
    return max(0.0, math.hypot(p[0] - cx, p[1] - cz) - r)

def hits(p, ytop, rpin=0.75, clr=0.3, skip=()):
    """obstacles within rpin+clr of a pin occupying y_B in [-14, ytop]."""
    return [o[0] for o in OBST if o[0] not in skip and o[3] < ytop and dist_obst(p, o) < rpin + clr]

if __name__ == '__main__':
    for ytop in (-12.0, -11.5, -10.0, -9.0):
        print('pin occupies y_B -14 .. %.1f' % ytop)
        for r in (8, 9, 10, 12):
            free = []
            for a in range(0, 360, 15):
                d = (r * math.sin(math.radians(a)), r * math.cos(math.radians(a)))   # a=0 down (+z)
                if not hits(d, ytop):
                    free.append(a)
            print('  r %2d free angles (0 = down, 90 = +x, 180 = up):' % r, free)
