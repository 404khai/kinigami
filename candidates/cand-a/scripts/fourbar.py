"""cand-a keeper four-bar (crank - link - rocker - output arm), plain Python 3.
Plane (x, z) of the body frame. Crank pivot C, rocker pivot Pv, crank radius r,
link L, rocker link-side arm b, output arm a at +delta from the link-side arm.
"""
import math, itertools

NOM = dict(Cx=-4.500, Cz=12.272, Px=5.250, Pz=15.322, r=2.0, b=3.0, a=4.5,
           L=None, delta=46.0, stop_open=18.86, stop_closed=221.39)
NOM['L'] = math.hypot(NOM['Px'] - NOM['Cx'], NOM['Pz'] - NOM['Cz'])

def rocker_pin(p, th_deg, branch):
    """Rocker link-pin position for crank angle th; branch +1/-1 picks the circle intersection."""
    th = math.radians(th_deg)
    qx = p['Cx'] + p['r'] * math.cos(th)
    qz = p['Cz'] + p['r'] * math.sin(th)
    dx, dz = p['Px'] - qx, p['Pz'] - qz
    d = math.hypot(dx, dz)
    # intersection of circle(q, L) and circle(P, b)
    x = (d * d + p['L'] ** 2 - p['b'] ** 2) / (2 * d)   # from q along q->P
    h2 = p['L'] ** 2 - x * x
    if h2 < 0:
        return None
    h = math.sqrt(h2)
    ux, uz = dx / d, dz / d
    mx, mz = qx + x * ux, qz + x * uz
    return (mx - branch * h * uz, mz + branch * h * ux), (qx, qz)

def solve(p, th_deg, branch, sgn):
    """Returns (rocker angle phi of Pv->rocker pin [deg], output pin (x, z)) or None."""
    r = rocker_pin(p, th_deg, branch)
    if r is None:
        return None
    (rx, rz), _ = r
    phi = math.atan2(rz - p['Pz'], rx - p['Px'])
    psi = phi + sgn * math.radians(p['delta'])
    return math.degrees(phi), (p['Px'] + p['a'] * math.cos(psi), p['Pz'] + p['a'] * math.sin(psi))

def dead_centres(p):
    """Crank angles (deg, 0..360) at which crank and link are collinear: extended (L+r) and folded (L-r)."""
    out = {}
    for name, D in (('ext', p['L'] + p['r']), ('fold', p['L'] - p['r'])):
        # distance from C to rocker pin = D, pin on circle(Pv, b)
        dcp = math.hypot(p['Px'] - p['Cx'], p['Pz'] - p['Cz'])
        c = (dcp ** 2 + p['b'] ** 2 - D ** 2) / (2 * dcp * p['b'])
        if abs(c) > 1:
            out[name] = []
            continue
        base = math.atan2(p['Cz'] - p['Pz'], p['Cx'] - p['Px'])   # Pv -> C
        res = []
        for s in (1, -1):
            ang = base + s * math.acos(c)
            ax, az = p['Px'] + p['b'] * math.cos(ang), p['Pz'] + p['b'] * math.sin(ang)
            a0 = math.degrees(math.atan2(az - p['Cz'], ax - p['Cx']))
            res.append((a0 + (180.0 if name == 'fold' else 0.0)) % 360)
        out[name] = res
    return out


def corners(tol, stop_mode='shared'):
    """Enumerate +-tolerance corners. tol: dict name->half-width over
    Cx, Cz, Px, Pz, r, b, a, L, delta (deg), stop (mm at crank radius).
    stop_mode 'shared': one sign moves both stops the same way (10 factors);
    'indep': open and closed stop signs independent (11 factors)."""
    names = ['Cx', 'Cz', 'Px', 'Pz', 'r', 'b', 'a', 'L', 'delta']
    n = len(names) + (1 if stop_mode == 'shared' else 2)
    for signs in itertools.product((-1, 1), repeat=n):
        p = dict(NOM)
        for nm, s in zip(names, signs):
            p[nm] = NOM[nm] + s * tol[nm]
        if stop_mode == 'shared':
            so = sc = signs[-1]
        else:
            so, sc = signs[-2], signs[-1]
        dth = math.degrees(tol['stop'] / p['r'])
        p['th_open'] = NOM['stop_open'] + so * dth
        p['th_closed'] = NOM['stop_closed'] + sc * dth
        yield p

def evaluate(p):
    dc = dead_centres(p)
    ext = min(dc['ext'], key=lambda t: abs(t - 28.86))
    fold = min(dc['fold'], key=lambda t: abs(t - 211.39))
    m_open = ext - p['th_open']
    m_closed = p['th_closed'] - fold
    a = solve(p, p['th_open'], 1, 1)
    c = solve(p, p['th_closed'], 1, 1)
    stroke = abs(a[1][1] - c[1][1])
    # link-line offset from the crank axis at each stop (perpendicular distance C -> link line)
    def off(th):
        rp = rocker_pin(p, th, 1)
        (rx, rz), (qx, qz) = rp
        ux, uz = rx - qx, rz - qz
        n = math.hypot(ux, uz)
        return abs((p['Cx'] - qx) * uz - (p['Cz'] - qz) * ux) / n
    return m_open, m_closed, stroke, off(p['th_open']), off(p['th_closed'])

def summarize(tol, stop_mode='shared', **kw):
    mo = mc = so = sc = 1e9
    smin, smax = 1e9, -1e9
    for p in corners(tol, stop_mode):
        for k, v in kw.items():
            p[k] = v
        a, b, s, oo, oc = evaluate(p)
        mo, mc = min(mo, a), min(mc, b)
        so, sc = min(so, oo), min(sc, oc)
        smin, smax = min(smin, s), max(smax, s)
    return dict(margin_open=mo, margin_closed=mc, off_open=so, off_closed=sc, stroke_min=smin, stroke_max=smax)

CASES = {
    'class_f_size': dict(Cx=.05, Px=.05, Cz=.1, Pz=.1, r=.05, b=.05, a=.05, L=.1, delta=1.0, stop=.05),
    'every_coord_0.1': dict(Cx=.1, Px=.1, Cz=.1, Pz=.1, r=.05, b=.05, a=.05, L=.1, delta=1.0, stop=.05),
    'frame_plus_play': dict(Cx=.15, Px=.15, Cz=.15, Pz=.15, r=.1, b=.1, a=.1, L=.2, delta=1.0, stop=.05),
}

if __name__ == '__main__':
    print('nominal', evaluate(dict(NOM, th_open=18.86, th_closed=221.39)))
    for mode in ('shared', 'indep'):
        for k, t in CASES.items():
            print(mode, k, summarize(t, mode))
