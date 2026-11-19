"""K4w go/no-go: M2x0.4 lead screw along y on the M3 axis, nut carries an inclined-slot wedge plate that moves a follower
pin on the yaw axis (rod through the hollow yaw shaft, as the v5 rod) up and down. Exploratory; selects nothing.
Run: python3 k4w_gonogo.py (needs ../declaration.json, jawwin.py, k4_gonogo.py, pin2.py). Plain Python 3."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import k4_gonogo as K
from jawwin import clearance

# ---- inputs: derived or cited (access 2026-11-20); nothing else is invented
W = 0.4208                               # N, declared
F_CLOSE_REQ = (1 + 1.0) * W / 2          # (1+mu) W/2 at mu = 1 (provisional bound): 0.4208 N
T_TENS = 4 * 1.0 * W                     # 1.683 N design tension at mu 1
F_REL_REQ = 2 * 1.0 * T_TENS             # 3.366 N on the rod (shoulder + stem faces, dossier v5 7.4)
T_RATED, T_STALL = 3.0, 9.01             # mN m: rated 3 (study K4, dossier v5), stall 9.66/1.07
SCREW_TQ_PER_N = 0.346                   # mN m per N axial, M2 x 0.4 with 1 mm collar at mu 0.15 (study K4, derived)
TAN_LAM = math.tan(math.atan(0.4 / (math.pi * 1.740)))
MU = {'wedge greased (static, steel/steel) [ToolBox]': 0.16, 'wedge dry kinetic [ToolBox]': 0.42,
      'wedge dry static lower [ToolBox]': 0.5, 'wedge dry static upper [ToolBox]': 0.8}
S_REQ = {}
for part in ('jaw', 'tongue'):
    lo, hi = 3.0, 9.0
    for _ in range(40):
        m = (lo + hi) / 2
        if clearance(m, 0.35, part, 301) >= 0.30: hi = m
        else: lo = m
    S_REQ[part] = hi
TOL = 0.25                                # open-position chain, class f arithmetic (same declared assumption as the K4 study)
SEAT_LOW = 1.0                            # peg up to 0.90 low (escape table) -> jaw edge at e - 0.10
S_MAX = S_REQ['jaw'] + 2 * TOL
TRAVEL = S_MAX + SEAT_LOW                 # vertical travel of the follower = jaw
LY = (11.6 - 6.7) - 1.6                   # screw y -11.6..-6.7 (M3 face at -6.7, bearing 0.4 off the end plate), nut 1.6 long -> 3.30
ALPHA = math.degrees(math.atan(TRAVEL / LY))

def check1():
    print('jaw S_min %.3f (tongue %.3f); open chain +-%.2f -> S nominal %.3f, S_max %.3f; closed travel below nominal %.1f; follower travel %.3f' % (S_REQ['jaw'], S_REQ['tongue'], TOL, S_REQ['jaw'] + TOL, S_MAX, SEAT_LOW, TRAVEL))
    print('stroke is a free design choice here (wedge), so the window itself is met by construction: jaw clearance at S_min, peg +0.35: %.3f (need 0.30)' % clearance(S_REQ['jaw'], 0.35, 'jaw', 301))
    print('screw stroke (nut travel) %.2f mm, wedge angle %.1f deg (tan %.3f)' % (LY, ALPHA, TRAVEL / LY))

def check2():
    a = math.radians(ALPHA)
    print('jam limit (closing impossible when mu_wedge >= cot(alpha)): %.3f' % (1 / math.tan(a)))
    for k, mu in MU.items():
        phi = math.atan(mu)
        cot = 1 / math.tan(a + phi) if a + phi < math.pi / 2 else float('-inf')
        print('  %-48s mu %.2f alpha+phi %.1f deg  net closing factor cot(a+phi)-mu_g (mu_g = mu) = %s' % (k, mu, math.degrees(a + phi), ('%.4f' % (cot - mu)) if cot > -1e9 else 'jammed (>= 90 deg)'))
    print('wedge self-holds only if mu > tan(alpha) = %.2f; highest cited mu is 0.8 -> the wedge does NOT hold the jaw; the screw must' % math.tan(a))
    print('screw: tan(lambda) %.4f, dry lower 0.15 -> %.2fx, oiled lower 0.10 -> %.2fx (cited, previous study)' % (TAN_LAM, 0.15 / TAN_LAM, 0.10 / TAN_LAM))
    f = math.tan(a - math.atan(0.16))
    print('jaw load F_v back-drives the screw with axial F_v x tan(alpha - phi) = %.2f F_v (greased wedge); the lock holds at any load if mu_screw > tan(lambda), vibration-sensitive' % f)

def forces():
    a = math.radians(ALPHA); phi = math.atan(0.16); mug = 0.16
    fac = 1 / math.tan(a + phi) - mug
    fw_r = T_RATED / SCREW_TQ_PER_N
    print('greased wedge and guide (mu 0.16): net vertical per axial N = %.4f' % fac)
    print('closing at rated torque: axial %.2f N -> jaw %.2f N; required %.4f N -> %.1fx' % (fw_r, fw_r * fac, F_CLOSE_REQ, fw_r * fac / F_CLOSE_REQ))
    fw_need = F_REL_REQ / fac
    print('release at the mu-1 bound tension %.3f N: rod force %.3f N -> axial %.1f N -> torque %.1f mN m = %.2fx rated, %.2fx stall' % (T_TENS, F_REL_REQ, fw_need, fw_need * SCREW_TQ_PER_N, fw_need * SCREW_TQ_PER_N / T_RATED, fw_need * SCREW_TQ_PER_N / T_STALL))
    print('release allowed up to T = %.3f N at rated (v5 rule 0.5225 N)' % (fw_r * fac / (2 * 1.0)))
    print('dry wedge (mu 0.42 kinetic or higher): jammed, no closing force')

REMOVED_K4W = {'keeper-crank', 'keeper-link', 'keeper-rocker', 'keeper-rocker-tip', 'frame-rocker-post', 'keeper-rod'}
def v5_boxes():
    d = json.load(open(os.path.join(HERE, '..', 'declaration.json')))
    return {c['id']: K.quat_aabb(c) for c in d['components'] if c.get('box') and c['id'] not in REMOVED_K4W and not c['id'].startswith(('wall-', 'endplate-', 'ring-'))}

def free_window(env_y, x=(-1.0, 1.0), zres=0.05):
    """largest vertical height H of a plate envelope (x, env_y) free of every remaining v5 box, r <= 20 and the arc keep-out (parts at y < -7)."""
    obs = v5_boxes(); best = (0, None)
    zs = [-4 + i * zres for i in range(int(26 / zres))]
    free = []
    for z in zs:
        b = (x[0], x[1], env_y[0], env_y[1], z, z + zres)
        top_r = math.hypot(max(abs(x[0]), abs(x[1])), z + zres)
        ok = top_r <= 20.0 and not any(K.overlap(b, o) for o in obs.values())
        if ok and b[2] < -7 and K.keepout(b) < 3.2: ok = False
        free.append(ok)
    run = 0; start = None
    for i, f in enumerate(free):
        if f:
            if run == 0: start = zs[i]
            run += 1
            if run * zres > best[0]: best = (run * zres, (start, zs[i] + zres))
        else: run = 0
    return best

def check3():
    h_req = TRAVEL + 0.8 + 2 * 0.6               # slot travel + pin dia 0.8 + 2 x 0.6 walls (304, my sizing)
    plate = LY + 0.8 + 2 * 0.6                   # plate length along y
    env = (-8.2 - (LY + 0.4 + 0.6), -8.2 - (LY + 0.4 + 0.6) + plate + LY)
    print('follower at y -8.2 (yaw axis). plate height needed %.2f mm, plate %.2f long, envelope over the nut travel y %.2f..%.2f' % (h_req, plate, env[0], env[1]))
    print('  envelope y_min %.2f against the |y| <= 12 rule: %s' % (env[0], 'violates' if env[0] < -12 else 'ok'))
    for label, ey in (('envelope as sized', env), ('clipped to y >= -12', (max(env[0], -12.0), env[1]))):
        h, rng = free_window(ey)
        print('  largest free vertical window on the yaw axis (%s): %.2f mm at z %s -> %s' % (label, h, rng, 'FAIL' if h < h_req else 'ok'))
    h2, r2 = free_window((-11.4, env[1]))
    print('  with the plate y_min at -11.4 (clear of the frame base): %.2f mm at z %s' % (h2, r2))
    print('  best case shortfall: %.2f mm' % (h_req - max(h2, free_window(env)[0])))
    # K1 pin, 5 mm and 2 mm pockets, with the K4w screw/nut/arm boxes
    obs = v5_boxes()
    obs.update({'screw': (-5.5, -3.5, -11.6, -6.7, 11.27, 13.27), 'nut-env': (-5.7, -3.3, -11.6, -6.7, 11.07, 13.47)})
    main = [p for m in (False, True) for p in K.path_pts((0, 0), m, 121)]
    for ytop in (-12.0, -9.0):
        out = {}
        for r in (8, 10, 12):
            fr = []
            for a in range(0, 360, 15):
                dd = (r * math.sin(math.radians(a)), r * math.cos(math.radians(a)))
                ps = [pp for m in ((False,) if a % 180 == 0 else (False, True)) for pp in K.path_pts(dd, m, 241)]
                if min(math.hypot(p[0]-q[0], p[1]-q[1]) for p in ps[::4] for q in main[::4]) < 4.95: continue
                if any(b[2] < ytop and b[3] > -14 and min(K.rect_dist(pp, b) for pp in ps) < 1.35 for b in obs.values()): continue
                fr.append(a)
            out[r] = fr
        print('  K1 pin pocket y -14..%.0f free angles: %s (0.14 MPa needs the 5 mm pocket; 2 mm gives %.2f MPa)' % (ytop, out, 0.14 * 5 / 2))

if __name__ == '__main__':
    print('== check 1 jaw window'); check1()
    print('== check 2 self-locking'); check2()
    print('== check 4 forces'); forces()
    print('== check 3 packing'); check3()
