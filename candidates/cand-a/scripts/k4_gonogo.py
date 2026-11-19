"""cand-a v6 = K4 (lead-screw keeper) + K1 (torsion pin): go/no-go arithmetic. Exploratory; selects nothing.
Run: python3 k4_gonogo.py   (needs ../declaration.json, jawwin.py, pin2.py). Plain Python 3.
Boxes are mm, body frame (x, y axis, z; +z down at rest), (x0, x1, y0, y1, z0, z1)."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from jawwin import clearance
import pin2

# ---------------- check 1: self-locking ----------------
def check1():
    P, d = 0.4, 2.0
    dp = d - 0.6495 * P                      # ISO 68-1 basic profile pitch diameter, derived
    lam = math.atan(P / (math.pi * dp)); t = math.tan(lam)
    print('K4 screw M2x0.4: dp %.3f lead %.2f lambda %.3f deg tan %.4f (cos30 corrected %.4f)' % (dp, P, math.degrees(lam), t, t * math.cos(math.radians(30))))
    for name, mu in (('steel/bronze dry, lower bound 0.15', 0.15), ('steel/bronze oiled, lower bound 0.10', 0.10)):
        print('  %-40s margin %.2fx' % (name, mu / t))
    print('  mu needed for 1.5x margin: %.4f' % (1.5 * t))

# ---------------- boxes ----------------
def quat_aabb(c):
    b = c['box']; h = [v / 1000 for v in b['half_extent_um']]; p = [v / 1000 for v in b['pose']['position_um']]
    w, x, y, z = b['pose']['orientation']
    R = [[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)], [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)], [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]]
    e = [sum(abs(R[i][j]) * h[j] for j in range(3)) for i in range(3)]
    return (p[0]-e[0], p[0]+e[0], p[1]-e[1], p[1]+e[1], p[2]-e[2], p[2]+e[2])

REMOVED = {'keeper-crank', 'keeper-link', 'keeper-rocker', 'keeper-rocker-tip', 'frame-rocker-post', 'keeper-rod', 'frame-m3', 'keeper-motor',
           'yaw-shaft', 'yaw-sector', 'puck-column', 'driver-2'}      # removed or replaced by the modified versions below
DRV2 = (-8.0, 9.8, -4.0, 6.2, 6.5, 8.3)   # driver-2 relocated and turned (17.8 along x); found by grid search, no v5 position fits
NEW = {   # (box, group)
 'yaw-shaft*':     ((-1.5, 1.5, -9.7, -6.7, 8.7, 9.3), 'nest'),     # OD 3.0 (was 2.0), bore 2.1 for the M2 screw
 'yaw-sector*':    ((-1.5, 3.7, -9.67, -6.73, 10.7, 12.7), 'nest'),  # hub r 1.5 (was 1.0)
 'puck-column*':   ((-1.4, 1.4, -6.7, -4.4, 6.9, 10.2), None),       # y_min trimmed from -7.0 to -6.7
 'driver-2*':      (DRV2, None),                                           # relocated (searched below)
 'm3-motor':       ((-8.2, -2.2, -7.0, 11.7, 10.55, 16.55), None),   # axis y at x -5.2, z 13.55; shaft tip y -10.6
 'm3-pinion':      ((-6.4, -4.0, -10.6, -10.1, 12.35, 14.75), 'mesh1'),   # module 0.2, 10 T, pitch r 1.0
 'worm-gear':      ((-4.4, -0.6, -10.6, -10.1, 11.65, 15.45), 'mesh1'),   # module 0.2, 17 T, pitch r 1.7, centre distance 2.7
 'worm':           ((-3.5, -1.5, -9.2, -7.4, 12.55, 14.55), 'mesh2'),    # module 0.2, pitch r 0.8, OD 2.0, lead angle 7.1 deg
 'worm-shaft':     ((-3.0, -2.0, -11.3, -7.5, 13.05, 14.05), 'mesh1'),
 'wheel-nut':      ((-1.9, 1.9, -10.1, -6.3, 12.8, 14.3), 'mesh2'),     # module 0.2, 17 T, pitch r 1.7, M2 internal thread hub
 'worm-bearing':   ((-3.5, -1.5, -11.4, -10.6, 12.65, 14.45), 'frame'), # on the frame base
 'bridge':         ((-0.5, 2.0, -11.4, -6.2, 14.32, 15.1), 'frame'),    # thrust plate over the wheel, on the frame base
 'screw-lower':    ((-1.0, 1.0, -9.2, -7.2, 3.0, 8.7), 'moving'),
 'screw-upper':    ((-1.0, 1.0, -9.2, -7.2, 15.1, 19.97), 'nest'),      # top at r 20 (box corner r 19.99)
}
EXEMPT_GROUPS = [{'mesh1'}, {'mesh2'}, {'frame'}, {'moving'}]
EXEMPT_PAIRS = {frozenset(p) for p in [
 ('screw-lower', 'keeper-tongue'), ('screw-lower', 'jaw'),           # rigid moving group
 ('bridge', 'screw-upper'), ('bridge', 'frame-base'), ('worm-bearing', 'frame-base'), ('bridge', 'frame-saddle'),   # frame / nested
 ('worm-bearing', 'worm-shaft'), ('worm-shaft', 'worm'), ('worm', 'worm-gear'), ('worm-shaft', 'worm-gear'),       # one shaft
 ('m3-pinion', 'worm-gear'), ('worm', 'wheel-nut'), ('m3-motor', 'm3-pinion'), ('m3-motor', 'worm-shaft'),                                                     # gear meshes by design
]}

def all_boxes():
    d = json.load(open(os.path.join(HERE, '..', 'declaration.json')))
    old = {c['id']: quat_aabb(c) for c in d['components'] if c.get('box') and c['id'] not in REMOVED}
    return old, {k: v[0] for k, v in NEW.items()}

def overlap(a, b, tol=1e-9):
    return all(a[2*i] < b[2*i+1] - tol and b[2*i] < a[2*i+1] - tol for i in range(3))

# ---------------- channel keep-out ----------------
def rect_dist(p, b):
    return math.hypot(max(b[0] - p[0], 0, p[0] - b[1]), max(b[4] - p[1], 0, p[1] - b[5]))
def path_pts(d, mirror=False, n=1201):
    return pin2.path(d, mirror, n)
def keepout(box, d=(0.0, 0.0)):
    return min(rect_dist(p, box) for m in (False, True) for p in path_pts(d, m))

def check2():
    old, new = all_boxes()
    print('-- keep-out validation against dossier-v5 (distance box to arc centreline, wall 2.9 + 0.3):')
    d = json.load(open(os.path.join(HERE, '..', 'declaration.json')))
    for c in d['components']:
        if c['id'] in ('frame-base', 'frame-rocker-post', 'frame-saddle', 'frame-m3'):
            print('   %-18s %.2f  (dossier 3.31 / 4.98 / 4.82 / 5.65)' % (c['id'], keepout(quat_aabb(c))))
    ok = True; rows = []
    for k, b in new.items():
        if k.startswith(('screw', 'worm-bearing', 'bridge')) and False: pass
        ov = [n for n, o in {**{a: c for a, c in old.items() if not a.startswith('ring-')}, **{kk: vv for kk, vv in new.items() if kk != k}}.items() if overlap(b, o)
              and frozenset((k, n)) not in EXEMPT_PAIRS and not any(NEW.get(k, (0, None))[1] in g and NEW.get(n, (0, None))[1] in g for g in EXEMPT_GROUPS)]
        r = max(math.hypot(max(abs(b[0]), abs(b[1])), max(abs(b[4]), abs(b[5]))), 0)
        girdle = b[2] < 1.75 and b[3] > -1.75
        lim = 19.5 if girdle else 20.0
        yok = b[2] >= -12 and b[3] <= 12
        ch = keepout(b) if (b[2] < -7 and b[3] > -14 and NEW[k][1] != 'moving') else None
        bad = bool(ov) or r > lim + 1e-9 or not yok or (ch is not None and ch < 3.2)
        ok &= not bad
        rows.append((k, ov, r, lim, ch, bad))
    for k, ov, r, lim, ch, bad in rows:
        print('   %-14s r_corner %.2f (limit %.1f) channel %s overlaps %s %s' % (k, r, lim, ('%.2f' % ch) if ch is not None else 'n/a (y > -7)', ov or '-', 'FAIL' if bad else 'ok'))
    print('   packing of the K4 parts (stroke-capped at screw top r 20):', 'PASS' if ok else 'FAIL')
    # K1 pin, 1.5 mm, pocket y -14..-9: path clear of all boxes (1.35 = 0.75 + 0.3 + 0.3) and of the main arcs (4.95 = 2.9 + 1.05 + 1.0 wall)
    allb = {n: b for n, b in {**old, **new}.items() if not n.startswith(('wall-', 'endplate-', 'ring-'))}
    main = [p for m in (False, True) for p in path_pts((0.0, 0.0), m, 121)]
    free = {}
    for ytop in (-12.0, -9.0):       # pin pocket y -14..-12 (end plate only, 2 mm) or y -14..-9 (5 mm, as the study)
        free[ytop] = {}
        for r in (8, 10, 12):
            fr = []
            for a in range(0, 360, 15):
                dd = (r * math.sin(math.radians(a)), r * math.cos(math.radians(a)))
                sym = a % 180 == 0      # pin on x = 0: one channel serves both roll-in directions
                ps = [pp for m in ((False,) if sym else (False, True)) for pp in path_pts(dd, m, 241)]
                if min(math.hypot(p[0]-q[0], p[1]-q[1]) for p in ps[::4] for q in main[::4]) < 4.95: continue   # 2.9 + 1.05 + 1.0 PA12 wall
                if any(bb[2] < ytop and bb[3] > -14 and min(rect_dist(pp, bb) for pp in ps) < 1.35 for bb in allb.values()): continue   # 0.75 + 0.3 + 0.3
                fr.append(a)
            free[ytop][r] = fr
        print('-- K1 pin pocket y -14..%.0f: free angles by r (0 = +z, 180 = -z; 0 and 180 serve both directions):' % ytop, free[ytop])
    return ok, free

# ---------------- check 3: jaw window and seating travel ----------------
def check3():
    s_req = {}
    for part in ('jaw', 'tongue'):
        lo, hi = 3.0, 9.0
        for _ in range(40):
            m = (lo + hi) / 2
            if clearance(m, 0.35, part, 301) >= 0.30: hi = m
            else: lo = m
        s_req[part] = hi
    print('S_min so that the open %s clears the swept peg (hex AF 4.0, 60 deg along the arc) by >= 0.30 with the peg 0.35 toward it: jaw %.3f, tongue %.3f' % ('part', s_req['jaw'], s_req['tongue']))
    tol = 0.25   # open-position chain, class f, arithmetic: stop 0.1 + jaw height 0.05 + two 0.05 (declared here, not cited)
    s_nom = s_req['jaw'] + tol; s_max = s_nom + tol
    seat_low = 1.0   # jaw closes onto a peg up to 0.90 low (escape table, loose corner), jaw edge = e - 0.10
    nut_z0, eng = 12.8, 1.2
    top_needed = nut_z0 + eng + seat_low + s_max
    print('open stroke corners: min %.3f nominal %.3f max %.3f; closed travel below nominal %.2f' % (s_req['jaw'], s_nom, s_max, seat_low))
    print('screw top needed with %.1f mm engaged in the nut at z %.1f: %.2f mm against the r 20 limit 19.97 -> short by %.2f mm' % (eng, nut_z0, top_needed, top_needed - 19.97))
    print('best case (zero tolerance, no travel below nominal): screw top %.2f, margin to 19.97 %.2f mm' % (nut_z0 + eng + s_req['jaw'], 19.97 - (nut_z0 + eng + s_req['jaw'])))
    smax_pack = 19.97 - (nut_z0 + eng + seat_low)
    print('stroke the screw can supply (packing limit): S_max %.2f -> jaw clearance at S_min=%.2f with peg +0.35: %.3f (need 0.30)' % (smax_pack, smax_pack - 2 * tol, clearance(smax_pack - 2 * tol, 0.35, 'jaw', 301)))
    return s_req, s_max, top_needed

if __name__ == '__main__':
    print('== check 1'); check1(); print('== check 2'); check2(); print('== check 3'); check3()
