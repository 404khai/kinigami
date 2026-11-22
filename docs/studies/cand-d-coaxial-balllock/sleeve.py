"""Take 80: Coaxial axial-sleeve roller-keeper coupler feasibility screen (exploratory).

Tests an internal coaxial tri-roller ball-lock topology (barrel OD <= 22 mm, no external
radial guide tower) with:
  - 6 fixed V-seat flats on the housing front (3 registry balls at -90, 30, 150 deg, r=8.20 mm)
  - 3 hardened steel cylindrical rollers (Ø3.0 x 3.0 mm) at 0, 120, 240 deg in a captive cage
  - Tri-flat 45-deg locking lands on the central tail pin + tri-flat 0-deg lands inside the
    axially sliding locking sleeve (true line contact on both sides, anti-rotates sleeve)
  - 360-deg annular positive ejector ring pushing directly on the tail flange

Checks:
  A. Worst-case 6-DOF loaded retention (70 g provisional service/table/fault boxes,
     no equal load sharing) at 40 N axial draw cap.
  B. Loaded axial-sleeve unlock force and M3 leadscrew torque (mu=0.23, 1.5x eccentric drag),
     plus loaded annular ejection under 20 N compression + tabletop drag + worst moment.
  C. Line-contact Hertzian stress on Ø3.0 x 3.0 mm hardened steel rollers.
  D. Nonlinear finite-flat form closure (Take 77 method) with 0.025 mm seat / 0.040 mm roller recess.
  E. Coaxial radial/axial envelope screen against Ø60 mm.
"""
from math import cos, sin, tan, radians, degrees, sqrt, hypot, pi, asin
import json
import numpy as np
from scipy.optimize import linprog

# ---- Geometry (mm) ----
R_REG = 8.20             # 3 registry balls at -90, 30, 150 deg
R_REG_BALL = 1.50
V_ANGLE = radians(65.0)  # V-seat half-angle

R_NECK = 3.20            # tail central pin flat-to-center distance at neck
R_HEAD = 4.60            # tail central head flat-to-center distance
R_ROLLER = 1.50          # Ø3.0 mm hardened steel roller
L_ROLLER = 3.00          # 3.0 mm roller length (tangential chord fits inside r=6.43: half-len 1.50 mm)
GROOVE_ANGLE = radians(45.0)
X_ROLLER = -4.20         # roller axis X relative to front housing lip (x=0)
X_REG = 0.0

R_CONTACT = 3.85
R_KLOCK = R_CONTACT + R_ROLLER * cos(GROOVE_ANGLE)   # 4.9107 mm roller axis at lock
R_KOUT_LOCK = R_KLOCK + R_ROLLER                     # 6.4107 mm roller outer flat at lock
R_SLEEVE_LOCK = R_KOUT_LOCK + 0.02                   # 6.4307 mm 0-deg flat land inside sleeve

R_KUNLOCK = R_HEAD + 0.30 + R_ROLLER                 # 6.40 mm roller axis at unlock
R_KOUT_UNLOCK = R_KUNLOCK + R_ROLLER                 # 7.90 mm
R_SLEEVE_UNLOCK = R_KOUT_UNLOCK + 0.05               # 7.95 mm unlock relief flat
# Corner radius of unlock relief flat of half-width 1.65 mm: hypot(7.95, 1.65) = 8.119 mm
R_SLEEVE_POCKET_CORNER = hypot(R_SLEEVE_UNLOCK, L_ROLLER / 2.0 + 0.15)
R_SLEEVE_OD = 9.60                                   # >= 1.48 mm wall at pocket corner
R_BARREL_ID = 9.70
R_BARREL_OD = 10.90                                  # Ø21.8 mm barrel OD

MU = 0.23
G = 9.81
M_PROV = 0.070  # 70 g provisional mass
W = M_PROV * G  # 0.6867 N
DRAW_CAP_N = 45.0  # force-limited axial draw cap (N)

BOXES = {
    "service": (-4*W,  4*W,  W,    W,    46*W,   50.8*W, 52.2),
    "table":   (-20.0, W,    25*W, 40*W, 46*W,   50.8*W, hypot(50.8, 46)*W),
    "fault":   (-4*W,  4*W,  4*W,  4*W,  46*W,   50.8*W, 52.2),
}


def build_contacts():
    pts, norms = [], []
    for deg in (-90.0, 30.0, 150.0):
        th = radians(deg)
        er = np.array([0.0, cos(th), sin(th)])
        et = np.array([0.0, -sin(th), cos(th)])
        c = np.array([X_REG, 0.0, 0.0]) + R_REG * er
        for sgn in (-1.0, 1.0):
            n = np.array([cos(V_ANGLE), 0.0, 0.0]) + sgn * sin(V_ANGLE) * et
            n /= np.linalg.norm(n)
            p = c - R_REG_BALL * n
            pts.append(p)
            norms.append(n)
    for deg in (0.0, 120.0, 240.0):
        th = radians(deg)
        er = np.array([0.0, cos(th), sin(th)])
        n = np.array([-sin(GROOVE_ANGLE), 0.0, 0.0]) - cos(GROOVE_ANGLE) * er
        n /= np.linalg.norm(n)
        c = np.array([X_ROLLER, 0.0, 0.0]) + R_KLOCK * er
        p = c + R_ROLLER * n
        pts.append(p)
        norms.append(n)
    return np.array(pts), np.array(norms)


def check_retention():
    pts, norms = build_contacts()
    A = np.zeros((6, 9))
    for i in range(9):
        A[:3, i] = norms[i]
        A[3:, i] = np.cross(pts[i], norms[i])

    ns_sym = sin(GROOVE_ANGLE) / (2.0 * cos(V_ANGLE))
    w_sym = np.array([ns_sym]*6 + [1.0]*3)
    null_res = float(np.linalg.norm(A @ w_sym))

    results = {}
    for name, (fx0, fx1, fy, fz, mx, my, mz) in BOXES.items():
        max_roller_req = 0.0
        min_sum_k = 0.0
        max_seat_req = 0.0
        worst_corner = None
        for s_fx in (fx0, fx1):
            for s_fy in (-fy, fy):
                for s_fz in (-fz, fz):
                    for s_mx in (-mx, mx):
                        for s_my in (-my, my):
                            for s_mz in (-mz, mz):
                                w_ext = np.array([s_fx, s_fy, s_fz, s_mx, s_my, s_mz])
                                c_obj = np.array([0.0]*6 + [1.0]*3)
                                res = linprog(c_obj, A_eq=A, b_eq=-w_ext, bounds=(0, None), method="highs")
                                if not res.success:
                                    raise RuntimeError(f"Infeasible {name}: {w_ext}")
                                if res.fun > min_sum_k:
                                    min_sum_k = float(res.fun)
                                # Max single roller normal under DRAW_CAP_N axial draw cap
                                A_ub = np.array([[0.0]*6 + [sin(GROOVE_ANGLE)]*3])
                                b_ub = np.array([DRAW_CAP_N])
                                for k_idx in (6, 7, 8):
                                    c_max = np.zeros(9)
                                    c_max[k_idx] = -1.0
                                    r2 = linprog(c_max, A_ub=A_ub, b_ub=b_ub, A_eq=A, b_eq=-w_ext, bounds=(0, None), method="highs")
                                    if r2.success and -r2.fun > max_roller_req:
                                        max_roller_req = float(-r2.fun)
                                        worst_corner = w_ext.tolist()
                                for s_idx in range(6):
                                    c_s = np.zeros(9)
                                    c_s[s_idx] = -1.0
                                    r3 = linprog(c_s, A_ub=A_ub, b_ub=b_ub, A_eq=A, b_eq=-w_ext, bounds=(0, None), method="highs")
                                    if r3.success and -r3.fun > max_seat_req:
                                        max_seat_req = float(-r3.fun)
        results[name] = {
            "min_axial_draw_all_seated_N": round(min_sum_k * sin(GROOVE_ANGLE), 3),
            "max_single_roller_normal_at_cap_N": round(max_roller_req, 3),
            "max_single_seat_normal_at_cap_N": round(max_seat_req, 3),
            "worst_corner": [round(v, 3) for v in worst_corner],
        }
    return null_res, results


def check_release_and_hertz(max_roller_N):
    # Max total radial force on locking sleeve at DRAW_CAP_N axial draw (with adverse mu=0.23 on 45-deg tail face)
    f_r_factor = cos(GROOVE_ANGLE) + MU * sin(GROOVE_ANGLE)  # 0.8697
    max_sum_nk = DRAW_CAP_N / sin(GROOVE_ANGLE)              # 63.64 N total normal
    max_total_fr = max_sum_nk * f_r_factor                   # 55.35 N total radial on sleeve
    f_sleeve_unlock = MU * max_total_fr                      # 12.73 N axial
    f_sleeve_unlock_ecc = f_sleeve_unlock * 1.5              # 19.10 N axial (1.5x eccentric drag)

    # M3 x 0.5 mm leadscrew (d_m=2.68, lead=0.50, mu=0.23, thrust collar r_c=2.0)
    d_m, lead, mu_th, r_c = 2.68, 0.50, 0.23, 2.0
    def screw_torque(F):
        return (F * (d_m / 2.0) * (lead + pi * mu_th * d_m) / (pi * d_m - mu_th * lead)
                + F * mu_th * r_c)

    t_unlock_m3 = screw_torque(f_sleeve_unlock_ecc)
    # Also draw-up torque to reach 45 N axial draw:
    t_draw_m3 = screw_torque(DRAW_CAP_N * 1.2)
    # Annular ejector: 20 N table compression + 2.45 N tabletop drag + 10 N side/roller pushout = 32.45 N -> 35 N
    t_eject_m3 = screw_torque(35.0)
    lead_deg = degrees(asin(lead / hypot(lead, pi * d_m)))
    fric_deg = degrees(asin(mu_th / hypot(mu_th, 1.0)))

    # Line-contact Hertzian stress: cylinder (R=1.50, L=3.00) on flat steel (E=210 GPa, nu=0.30)
    # p0 = sqrt(F * E_star / (pi * L * R))
    E, nu = 210000.0, 0.30
    E_star = E / (2.0 * (1.0 - nu**2))
    p0_tail = sqrt(max_roller_N * E_star / (pi * L_ROLLER * R_ROLLER))
    b_half = sqrt(4.0 * max_roller_N * R_ROLLER / (pi * L_ROLLER * E_star))
    p0_sleeve = sqrt((max_roller_N * f_r_factor) * E_star / (pi * L_ROLLER * R_ROLLER))

    return {
        "draw_cap_N": DRAW_CAP_N,
        "max_total_radial_on_sleeve_N": round(max_total_fr, 3),
        "sleeve_unlock_axial_N": round(f_sleeve_unlock, 3),
        "sleeve_unlock_axial_1p5x_ecc_N": round(f_sleeve_unlock_ecc, 3),
        "M3_unlock_torque_Nmm": round(t_unlock_m3, 3),
        "M3_draw_54N_torque_Nmm": round(t_draw_m3, 3),
        "M3_eject_35N_torque_Nmm": round(t_eject_m3, 3),
        "lead_angle_deg": round(lead_deg, 2),
        "friction_angle_deg": round(fric_deg, 2),
        "self_locking": lead_deg < fric_deg,
        "hertz_roller_on_tail_flat_MPa": round(p0_tail, 1),
        "hertz_contact_halfwidth_mm": round(b_half, 4),
        "hertz_roller_on_sleeve_flat_MPa": round(p0_sleeve, 1),
    }


def check_nonlinear_form_closure():
    """Nonlinear finite-flat connected-component bound (Take 77 method) over 9 unilateral contacts."""
    pts, norms = build_contacts()
    # Contact ball/roller center radii relative to origin (0,0,0)
    centers = []
    for deg in (-90.0, 30.0, 150.0):
        th = radians(deg)
        c = np.array([X_REG, R_REG * cos(th), R_REG * sin(th)])
        centers.extend([c, c])
    for deg in (0.0, 120.0, 240.0):
        th = radians(deg)
        c = np.array([X_ROLLER, R_KLOCK * cos(th), R_KLOCK * sin(th)])
        centers.append(c)
    centers = np.array(centers)
    radii = np.linalg.norm(centers, axis=1)

    A = np.column_stack((norms, np.cross(centers, norms) / R_REG))
    assert np.linalg.matrix_rank(A) == 6

    # Trial finite-angle rotation envelope beta = 1.20 deg, normal tilt delta = 0.60 deg
    beta = radians(1.20)
    H = np.r_[np.full(6, 0.250), np.full(3, 0.250)]
    delta = np.radians([0.60]*6 + [1.00]*3)
    E = np.r_[np.full(6, 0.025), np.full(3, 0.040)]
    curve = (1.0 - cos(beta)) * radii
    e_eff = E + 2.0 * np.sin(delta / 2.0) * H + curve

    # Bound max ||t||, max ||theta||, and max contact center displacement via LP over 26 directions
    # plus exact vertex enumeration of a 6-subset is C(9,6)=84 subsets — fast!
    from itertools import combinations
    verts = []
    for idx in combinations(range(9), 6):
        subA = A[list(idx)]
        if abs(np.linalg.det(subA)) < 1e-9:
            continue
        v = np.linalg.solve(subA, -e_eff[list(idx)])
        if np.min(A @ v + e_eff) >= -1e-10:
            verts.append(v)
    verts = np.array(verts)
    assert len(verts) > 0, "No feasible vertices!"
    max_t = float(np.max(np.linalg.norm(verts[:, :3], axis=1)))
    max_theta = asin(float(np.max(np.linalg.norm(verts[:, 3:], axis=1) / R_REG)))
    m_disp = np.max([np.linalg.norm(v[:3] + np.cross(v[3:], centers) / R_REG, axis=1) for v in verts], axis=0)
    disp = m_disp + (1.0 - cos(max_theta)) * radii
    return {
        "feasible_vertices": int(len(verts)),
        "max_translation_mm": round(max_t, 4),
        "max_rotation_deg": round(degrees(max_theta), 3),
        "beta_margin_deg": round(degrees(beta - max_theta), 3),
        "max_seat_disp_mm": round(float(np.max(disp[:6])), 4),
        "max_roller_disp_mm": round(float(np.max(disp[6:])), 4),
        "min_H_margin_mm": round(float(np.min(H - disp)), 4),
    }


def check_envelope():
    Lx, Ly, Lz = 48.0, 25.4, 24.0
    return {
        "sleeve_pocket_corner_r_mm": round(R_SLEEVE_POCKET_CORNER, 3),
        "sleeve_od_mm": round(2 * R_SLEEVE_OD, 2),
        "barrel_od_mm": round(2 * R_BARREL_OD, 2),
        "box_48x25p4x24_sphere_mm": round(sqrt(Lx**2 + Ly**2 + Lz**2), 3),
        "radial_margin_y_mm": round((Ly - 2 * R_BARREL_OD) / 2.0, 2),
        "radial_margin_z_mm": round((Lz - 2 * R_BARREL_OD) / 2.0, 2),
    }


def main():
    null_res, ret = check_retention()
    max_r = max(v["max_single_roller_normal_at_cap_N"] for v in ret.values())
    rel = check_release_and_hertz(max_r)
    fc = check_nonlinear_form_closure()
    env = check_envelope()
    print(json.dumps({
        "label": "exploratory",
        "preload_nullspace_residual": null_res,
        "retention_boxes_70g_provisional": ret,
        "loaded_release_and_hertz": rel,
        "nonlinear_form_closure": fc,
        "envelope_screen": env,
    }, indent=2))


if __name__ == "__main__":
    main()
