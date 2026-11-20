#!/usr/bin/env python3
"""cand-d coupler on paper: cam layout, tolerance stack, self-locking, preload,
release, load carriers, contact stresses and pre-alignment windows.

Plain Python 3, no third-party packages. Lengths mm, forces N, torques mN m
(N mm). Every input is either a declared dimension of cand-d, a cited value
(source noted next to it), or marked PROVISIONAL. Run: python3 coupler.py
"""
import math

def tand(a): return math.tan(math.radians(a))
def atand(x): return math.degrees(math.atan(x))

# ------------------------------------------------------------------ declared geometry
LIP = 0.8            # housing lip (thrust face) thickness
LUG_R = 1.5          # lug radius (dia 3.0, g6)
CLR = 0.1            # axial running clearance of the lug in the slot ends
D1, LAM1 = 1.0, 20.0 # capture stage: draw (mm), lead angle (deg)
D2, LAM2 = 0.4, 3.0  # lock stage: draw, lead angle
SLEEVE_RI, SLEEVE_RO = 3.55, 6.0
LUG_TIP = 5.9        # lug tip radius
STUD_R = 2.0         # pilot radius (dia 4.0 g6)
HOUSING_RO = 3.5     # housing tube outer radius (slot wall r 2.0..3.5)
SLOT_W = 3.05        # housing lug slot width (IT9)
LIP_V = 0.6          # V lead-in depth per side on the lip slot (45 deg)
BORE_CH = 0.6        # bore mouth chamfer (45 deg) in the lip
NOSE_CH = 0.5        # pilot nose chamfer (45 deg)
FACE_RO, FACE_RI = 6.45, 2.0   # flange-to-lip contact annulus (housing lip r 6.45, bore r 2.0)
GEAR_I = 43 / 12     # sleeve gear z43 / pinion z12
SECTOR_I = 58 / 12   # joint sector z58 / pinion z12

c0 = LIP + LUG_R + CLR            # lug-axis depth at capture start
c1 = c0 + D1
c2 = c1 + D2
s_nom = (c1 + c2) / 2
RC = (SLEEVE_RI + LUG_TIP) / 2     # mean flank contact radius
L_CONTACT = LUG_TIP - SLEEVE_RI    # contact length along the lug

# ------------------------------------------------------------------ cited values
# Friction, steel on bronze: dry 0.15 to 0.23, machine oil 0.10 to 0.16
# (https://en.wikipedia.org/wiki/Leadscrew, accessed 2026-11-20; same values used in
#  docs/studies/coupler-k4-gonogo.md). Self-locking when mu > tan(lead angle).
# Engineering ToolBox (https://www.engineeringtoolbox.com/friction-coefficients-d_778.html,
# accessed 2026-11-20): bronze on steel clean and dry static 0.35, greased 0.16; steel on steel
# clean and dry static 0.5 to 0.8 (kinetic 0.42), greased static 0.16; PTFE on steel static 0.05 to 0.2.
# The flank band is the union of both sources: dry 0.15 to 0.35.
MU_DRY = (0.15, 0.35)
MU_OIL = (0.10, 0.16)
MU_T = (0.05, 0.20)          # thrust: C93200 sleeve face on a PTFE washer on the 304 lip
MU_FACE_DRY = 0.5            # 304 flange on 304 lip, clean and dry static, lower bound
MU_FACE_OIL = 0.16           # same pair greased (contamination case)
# 206-109: rated 3 mN m at 3 V, stall 9 mN m at 3 V, max 3.6 V (datasheet).
T_STALL_3V = 9.0
V_MAX = 3.6
# Materials: 304 E 193 GPa nu 0.29 (ATI data sheet), yield 205 MPa; C93200 E 100 GPa
# (Concast), yield 138 MPa; nu 0.34 for bronze is PROVISIONAL (typical copper alloy).
E_SS, NU_SS, SY_SS = 193e3, 0.29, 205.0
E_BR, NU_BR, SY_BR = 100e3, 0.34, 138.0
# ISO 286 IT grades (https://en.wikipedia.org/wiki/IT_Grade): IT9 1..3 mm 25 um,
# 3..6 mm 30 um; IT10 1..3 mm 40 um, 3..6 mm 48 um.
IT9 = {"1-3": 0.025, "3-6": 0.030}
IT10 = {"1-3": 0.040, "3-6": 0.048}
# Spur mesh efficiency: KHK, ABCs of Gearing (https://khkgears.us/media/fqrlut1m/abcs-of-gearing-b.pdf,
# accessed 2026-11-20) gives 98.0 to 99.5 percent for spur gears. Used as the band 0.90..1.00
# (lower bound widened, PROVISIONAL, for small unlubricated gears): 1.0 bounds the preload
# from above, 0.9 bounds the available release torque from below.
ETA = (0.9, 1.0)
R_THRUST = 4.0       # PTFE thrust ring r 3.6..4.4 between the sleeve front face and the lip
# Unit weight from the declaration (gen_declaration.py): 30.247 g, W = 0.2966 N.
W = 0.2966
HALF_WIDTH = 12.7
UNIT_LEN = 47.2      # site-to-site pitch
MU_TABLE_BOUND = 1.0 # PROVISIONAL upper bound, as cand-a v5

def section(t): print("\n== " + t)

section("1. cam slot layout")
arc1 = D1 / tand(LAM1)
arc2 = D2 / tand(LAM2)
a1, a2 = math.degrees(arc1 / RC), math.degrees(arc2 / RC)
half_lug = math.degrees(LUG_R / RC)
entry_half = math.degrees((LUG_R + LIP_V) / RC)
slot_end = a1 + a2 + half_lug
web = 180 - entry_half - slot_end
print("capture start depth c0 = %.2f, capture end c1 = %.2f, lock end c2 = %.2f, nominal seat s = %.2f" % (c0, c1, c2, s_nom))
print("mean flank radius Rc = %.3f, contact length %.2f" % (RC, L_CONTACT))
print("capture arc %.2f mm = %.1f deg, lock arc %.2f mm = %.1f deg; slot spans -%.1f .. %.1f deg; web to the other slot's entry %.1f deg (%.2f mm at Rc)" %
      (arc1, a1, arc2, a2, entry_half, slot_end, web, math.radians(web) * RC))
print("sleeve rotation to the nominal seat: %.1f deg; lock stage covers seat depth %.2f..%.2f" % (a1 + a2 / 2, c1, c2))
slot_end_depth = c2 + LUG_R + CLR
print("slot end depth %.2f; sleeve from depth %.2f to %.2f (0.7 rear wall), gear ring behind it to depth %.2f" % (slot_end_depth, LIP, slot_end_depth + 0.7, slot_end_depth + 0.7 + 1.5))

section("2. axial tolerance stack at seating (flange face on lip face)")
stack = [("tail: flange face to lug axis (3.6 mm, IT10)", IT10["3-6"] / 2),
         ("tail: lug radius (dia 3 g6, -2..-8 um)", 0.004),
         ("head: lip thickness (0.8 mm, IT10)", IT10["1-3"] / 2),
         ("head: lip rear face to flank at the seat angle (2.8 mm, IT10)", IT10["1-3"] / 2),
         ("head: thrust running play under load", 0.0)]
tot = sum(v for _, v in stack)
for n, v in stack: print("  +-%.4f  %s" % (v, n))
lo, hi = s_nom - tot, s_nom + tot
print("seat depth range %.3f..%.3f inside the lock stage %.2f..%.2f: margins %.3f / %.3f" % (lo, hi, c1, c2, lo - c1, c2 - hi))
assert c1 < lo and hi < c2

section("3. self-locking of the lock stage")
t2 = tand(LAM2)
for name, mus in (("dry (declared condition)", MU_DRY), ("machine oil (contamination case)", MU_OIL)):
    print("  %s: mu %.2f..%.2f vs tan(3 deg) = %.4f -> margin %.2f..%.2f" % (name, mus[0], mus[1], t2, mus[0] / t2, mus[1] / t2))
print("  capture stage tan(20 deg) = %.3f: NOT self-locking (never a holding position by the stack check above)" % tand(LAM1))

section("4. closing preload from a voltage-limited stall")
r_t = R_THRUST
def k_close(mu, lam, mut): return RC * tand(lam + atand(mu)) + mut * r_t
def k_release(mu, lam, mut): return RC * tand(atand(mu) - lam) + mut * r_t
V_C = 1.2  # closing voltage (PWM average), chosen from the torsion no-slip requirement in section 7; motor stall torque scales with voltage
t_motor_c = T_STALL_3V * V_C / 3.0
Ts_c = [t_motor_c * GEAR_I * e for e in ETA]
F_min = Ts_c[0] / k_close(MU_DRY[1], LAM2, MU_T[1])
F_max = Ts_c[1] / k_close(MU_DRY[0], LAM2, MU_T[0])
print("closing at %.1f V: motor stall %.2f mN m, sleeve %.2f..%.2f mN m; preload F_p = %.2f..%.2f N (flank mu 0.35 / 0.15, thrust 0.20 / 0.05)" % (V_C, t_motor_c, Ts_c[0], Ts_c[1], F_min, F_max))
print("self-locking with the thrust credited (not relied on): holding torque per newton at mu_min %.3f mm" % (RC * tand(atand(MU_DRY[0]) - LAM2) + MU_T[0] * r_t))

section("5. declared loads (PROVISIONAL modelling assumptions, Q31 tabletop chain of 5)")
T_TENSION = 4 * MU_TABLE_BOUND * W            # drag of four units at the friction bound
T_TORSION = 2 * W * HALF_WIDTH                # two neighbours each tipping on an edge
M_OOP = W * UNIT_LEN                          # out-of-plane bending: one neighbour fully cantilevered (upper bound)
V_JD = 3.0 * 1.0                              # joint drive limited to the rated 3 mN m motor torque (controller rule)
M_INPLANE = 3.0 * SECTOR_I * ETA[1]           # joint torque at the drive limit
M_INPLANE_FAULT = T_STALL_3V * V_MAX / 3.0 * SECTOR_I
SHEAR = W
for n, v, u in (("tension (4 mu W, mu = 1)", T_TENSION, "N"), ("torsion (2 W x 12.7)", T_TORSION, "mN m"),
                ("out-of-plane bending (W x 47.2)", M_OOP, "mN m"), ("in-plane bending at the joint drive limit (3 mN m x 58/12)", M_INPLANE, "mN m"),
                ("in-plane bending, fault: joint stalled at 3.6 V", M_INPLANE_FAULT, "mN m"), ("shear (W)", SHEAR, "N")):
    print("  %-60s %7.3f %s" % (n, v, u))

section("6. release (bounded, independent: the head unit's own motor)")
ts_avail = T_STALL_3V * V_MAX / 3.0 * GEAR_I * ETA[0]
worst = (F_max + T_TENSION) * k_release(MU_DRY[1], LAM2, MU_T[1])
print("release torque, worst corner (F_p %.2f closed at the low-friction corner, + tension %.3f, released at flank 0.35 / thrust 0.20): %.2f mN m at the sleeve" % (F_max, T_TENSION, worst))
print("available at 3.6 V stall, eta 0.9: %.2f mN m -> margin %.2f" % (ts_avail, ts_avail / worst))
print("closing preload and available release torque both scale with the same motor constant, so this margin does not depend on motor-to-motor variation; F_p_min does (see limitations)")
Fo = Ts_c[1] / k_close(MU_OIL[0], LAM2, MU_T[0])
print("oil case (flank 0.10..0.16): preload up to %.2f N, release needs %.2f mN m" % (Fo, (Fo + T_TENSION) * k_release(MU_OIL[1], LAM2, MU_T[1])))
cap_drag = MU_TABLE_BOUND * W
print("capture stage drawing one free unit at mu = 1: %.2f mN m (vs closing %.2f)" % (cap_drag * k_close(MU_DRY[1], LAM1, MU_T[1]), Ts_c[0]))
print("ejection at release: the capture stage pushes the stud out by %.1f mm (the slot's outer flank)" % (D1 + D2))

section("7. carriers per load at every tolerance corner")
# tension: lugs on the lock stage; joint stays closed while F_p_min > tension
print("tension: F_p_min %.2f N > %.3f N -> faces stay in contact (no separation); geometric carrier: lugs on the self-locking stage" % (F_min, T_TENSION))
# torsion: geometric carrier = lugs on the housing slot sides
clr_max = (SLOT_W + IT9["3-6"] / 2) - (3.0 - 0.008)
clr_min = (SLOT_W - IT9["3-6"] / 2) - (3.0 - 0.002)
r_slot = (STUD_R + HOUSING_RO) / 2
r_eff = 2 / 3 * (FACE_RO ** 3 - FACE_RI ** 3) / (FACE_RO ** 2 - FACE_RI ** 2)
t_face = MU_FACE_DRY * F_min * r_eff
print("torsion, no slip (keeps the lugs from sliding on the sleeve flank, which could walk the sleeve): dry face friction mu %.2f x F_p_min %.2f x r_eff %.2f = %.2f mN m vs %.2f (ratio %.2f)" %
      (MU_FACE_DRY, F_min, r_eff, t_face, T_TORSION, t_face / T_TORSION))
print("  greased face (contamination case, mu 0.16): %.2f mN m, slip possible above that" % (MU_FACE_OIL * F_min * r_eff))
print("torsion, geometric carrier beyond slip: lugs bear on the 304 housing slot sides at r %.2f, lash %.2f..%.2f deg each way, force %.2f N per lug" %
      (r_slot, math.degrees(clr_min / 2 / r_slot), math.degrees(clr_max / 2 / r_slot), T_TORSION / (2 * r_slot)))
assert t_face / T_TORSION >= 1.25
# out-of-plane bending (about y): face tipping capacity; then pilot couple
print("out-of-plane bending: face tipping at F_p_min x %.2f = %.2f mN m vs %.2f (ratio %.2f); beyond it the pilot (H7/g6, 0.004..0.024 mm) bears as a couple" %
      (FACE_RO, F_min * FACE_RO, M_OOP, F_min * FACE_RO / M_OOP))
# in-plane bending (about z): lugs at +-Rc in y plus face
print("in-plane bending at the drive limit: face tipping %.2f mN m vs %.2f (ratio %.2f); fault %.2f: extra lug load %.2f N" %
      (F_min * FACE_RO, M_INPLANE, F_min * FACE_RO / M_INPLANE, M_INPLANE_FAULT, M_INPLANE_FAULT / (RC + FACE_RO)))
print("shear: pilot in bore, plus dry face friction mu F_p = %.2f N vs %.3f N" % (MU_FACE_DRY * F_min, SHEAR))

section("8. stresses")
Fl = (F_max + T_TENSION) / 2
Fl_fault = Fl + M_INPLANE_FAULT / (RC + FACE_RO)
Fl_lim = Fl + M_INPLANE / (RC + FACE_RO)
Es = 1 / ((1 - NU_SS ** 2) / E_SS + (1 - NU_BR ** 2) / E_BR)
def hertz_line(F, R, L): return math.sqrt(F * Es / (math.pi * R * L))
onset = 1.67 * SY_BR  # first yield of the softer body at p0 = 1.67 sigma_y (line contact, Tresca); PROVISIONAL rule of thumb
for n, F in (("design (F_p max + tension)", Fl), ("plus in-plane bending at the drive limit", Fl_lim), ("plus fault bending", Fl_fault)):
    print("  lug on bronze flank, %s: %.2f N per lug, Hertz p0 %.0f MPa (onset %.0f)" % (n, F, hertz_line(F, LUG_R, L_CONTACT), onset))
lever = RC - STUD_R
Z = math.pi * (2 * LUG_R) ** 3 / 32
print("  lug root bending: %.1f N mm, %.1f MPa (304 yield 205); fault %.1f MPa" % (Fl * lever, Fl * lever / Z, Fl_fault * lever / Z))
A_net = math.pi * STUD_R ** 2 - 2 * LUG_R * 2 * STUD_R * 0  # lugs are integral, no cross hole
print("  pilot tension %.2f N over %.2f mm2: %.2f MPa" % (2 * Fl_fault, math.pi * STUD_R ** 2, 2 * Fl_fault / (math.pi * STUD_R ** 2)))
print("  PTFE thrust ring r 3.6..4.4: %.2f N over %.2f mm2: %.2f MPa" % (2 * Fl, math.pi * (4.4 ** 2 - 3.6 ** 2), 2 * Fl / (math.pi * (4.4 ** 2 - 3.6 ** 2))))

section("9. pre-alignment windows (presented pose; not a capture window, CPL-006)")
lat = (STUD_R + BORE_CH) - (STUD_R - NOSE_CH)
print("lateral (bore chamfer %.1f + nose chamfer %.1f): +-%.2f mm" % (BORE_CH, NOSE_CH, lat))
print("lug across its axis (z direction for lugs along y): +-%.2f mm (V lead-in %.1f per side, round lug)" % (LIP_V, LIP_V))
roll = math.degrees(LIP_V / (HOUSING_RO + 0.5 * (LUG_TIP - HOUSING_RO)))
print("roll about the axis: +-%.1f deg at the lug's outer contact radius" % roll)
lead_ratio = (1 - 0.8) / (1 + 0.8)
print("45 deg chamfers (304 nose on 304 bore chamfer) centre under an axial push when mu < 1 (tan 45): at the cited dry steel-steel upper bound 0.8 the lateral/axial ratio is %.2f (positive: no wedging)" % lead_ratio)
print("stack the window must absorb (two units on one table, PA12 SLS +-0.3 per feature, coupler axis height and lateral position): +-0.6 mm")

STUD_L = 6.2         # pilot length beyond the flange face (nose chamfer NOSE_CH)
lug_front = s_nom + LUG_R
pilot_cyl = STUD_L - NOSE_CH
print("sequence: when the lug front (%.2f from the flange face) reaches the lip face, the pilot's cylindrical part (from %.2f) is %.2f deep, the bore chamfer ends at %.2f:" % (lug_front, pilot_cyl, pilot_cyl - lug_front, BORE_CH))
print("  the pilot is already in the cylindrical bore, so the lugs meet the lip slots with lateral error <= the pilot clearance 0.024 mm; only roll is left to the V lead-ins")
assert pilot_cyl - lug_front >= BORE_CH - 1e-9
