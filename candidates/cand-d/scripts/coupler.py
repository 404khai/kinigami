#!/usr/bin/env python3
"""cand-d coupler on paper (version 2): cam layout, axial tolerance stack,
self-locking, preload, release, Hirth face coupling, load carriers alone and
combined, contact stresses, stops, mount, pre-alignment windows.

Plain Python 3, no third-party packages. Lengths mm, forces N, torques mN m
(N mm). Every input is a declared dimension of cand-d, a cited value (source and
how it was checked noted next to it), or marked PROVISIONAL. Run: python3 coupler.py
Hard assertions stop the script if a claimed margin is lost. The unit weight is
read from ../declaration.json.
"""
import math, json, os

def tand(a): return math.tan(math.radians(a))
def atand(x): return math.degrees(math.atan(x))
def section(t): print("\n== " + t)

# ------------------------------------------------------------------ declared geometry
LIP = 0.8            # housing lip thickness behind the Hirth pitch plane
R_THRUST = 4.0       # PTFE thrust ring r 3.6..4.4 x 0.3
LUG_R = 1.5          # lug radius (dia 3.0 g6)
CLR = 0.1            # axial clearance of the lug at the slot ends
D1, LAM1 = 1.0, 20.0 # capture stage: draw (mm), lead angle (deg)
D2, LAM2 = 0.4, 3.0  # lock stage
SLEEVE_RI, SLEEVE_RO = 3.55, 6.3
LUG_TIP = 6.2
STUD_R = 2.0         # pilot radius (dia 4.0 g6)
BORE_R = 2.05        # bore dia 4.10 (+0.018/0): an entry guide only; the Hirth ring centres at the seat
PILOT_CLR = (0.050, 0.130)
HOUSING_RO = 3.5
SLOT_W = 3.05        # housing lug slots (IT9)
LIP_V = 0.6          # V lead-in per side on the lip slots and sleeve notches (45 deg)
BORE_CH, NOSE_CH = 0.6, 0.5
STUD_L = 6.2         # pilot length beyond the Hirth pitch plane
HIRTH_N, HIRTH_RI, HIRTH_RO = 36, 2.6, 6.3   # face teeth, 90 deg included, on the stud flange and the housing lip
HIRTH_RM = (HIRTH_RI + HIRTH_RO) / 2
GEAR_I = 43 / 12     # sleeve gear z43 / pinion z12
SECTOR_I = 58 / 12

c0 = LIP + LUG_R + CLR
c1, c2 = c0 + D1, c0 + D1 + D2
s_nom = (c1 + c2) / 2
RC = (SLEEVE_RI + LUG_TIP) / 2
L_CONTACT = LUG_TIP - SLEEVE_RI

# ------------------------------------------------------------------ cited values (each checked against raw source text)
# Wikipedia "Leadscrew" (https://en.wikipedia.org/wiki/Leadscrew, accessed 2026-11-20; checked in the raw
# wikitext, index.php?action=raw, friction table): steel on bronze dry 0.15-0.23, machine oil 0.10-0.16.
# Same page: self-locking when mu > tan(lead angle); "not absolute" under vibration or shock.
MU_DRY = (0.15, 0.23)
MU_OIL = (0.10, 0.16)
# Engineering ToolBox (https://www.engineeringtoolbox.com/friction-coefficients-d_778.html, accessed
# 2026-11-20; checked in the raw HTML): PTFE on steel clean and dry 0.05-0.2; steel on steel clean and dry
# static 0.5-0.8, kinetic 0.42. The page has no dry bronze-on-steel row (only "Grease 0.16").
MU_T = (0.05, 0.20)
MU_SS_MAX = 0.8
# 206-109 datasheet (pdftotext of https://www.precisionmicrodrives.com/datasheets/206-109-V0.pdf): rated
# 3 mN m at 3 V, stall 9 mN m, max 3.6 V. Stall torque is taken proportional to the applied voltage.
T_STALL_3V = 9.0
# Release supply rule (controller): release only with the cell at >= 3.5 V. The DRV8835 bridge
# (TI datasheet https://www.ti.com/lit/ds/symlink/drv8835.pdf, HS + LS on-resistance 305 mOhm typical)
# drops about 0.07 V at the 230 mA start current; 3.4 V at the motor is used (rounded down, PROVISIONAL).
V_RELEASE = 3.4
V_C = 1.0            # closing voltage (PWM average of the measured cell voltage)
# Materials: 304 E 193 GPa, nu 0.29, yield 205 MPa (ATI data sheet); C93200 E 100 GPa, yield 138 MPa
# (Concast page); bronze nu 0.34 PROVISIONAL.
E_SS, NU_SS, SY_SS = 193e3, 0.29, 205.0
E_BR, NU_BR, SY_BR = 100e3, 0.34, 138.0
# ISO 286 IT grades (https://en.wikipedia.org/wiki/IT_Grade): IT9 1..3 mm 25 um, 3..6 mm 30 um.
IT9 = {"1-3": 0.025, "3-6": 0.030}
# Spur mesh efficiency: KHK, ABCs of Gearing (https://khkgears.us/media/fqrlut1m/abcs-of-gearing-b.pdf):
# 98.0-99.5 percent. Used as 0.90..1.00 (lower bound widened, PROVISIONAL, small unlubricated gears).
ETA = (0.9, 1.0)

_here = os.path.dirname(os.path.abspath(__file__))
_decl = json.load(open(os.path.join(_here, "..", "declaration.json")))
MASS_MG = sum(c["mass_mg"] for c in _decl["components"])
W = MASS_MG * 1e-6 * 9.80665
HALF_WIDTH = 12.7
UNIT_LEN = 47.2
MU_TABLE_BOUND = 1.0 # PROVISIONAL upper bound, as cand-a v5

section("0. unit")
print("declared mass %d mg, W = %.4f N" % (MASS_MG, W))

section("1. cam slot layout")
arc1, arc2 = D1 / tand(LAM1), D2 / tand(LAM2)
a1, a2 = math.degrees(arc1 / RC), math.degrees(arc2 / RC)
half_lug = math.degrees(LUG_R / RC)
entry_half = math.degrees((LUG_R + LIP_V) / RC)
slot_end = a1 + a2 + half_lug
web = 180 - entry_half - slot_end
print("capture start depth %.2f, capture end %.2f, lock end %.2f, nominal seat %.2f (below the Hirth pitch plane)" % (c0, c1, c2, s_nom))
print("Rc %.3f, flank contact length %.2f; capture %.1f deg, lock %.1f deg; slot -%.1f..%.1f deg; web %.1f deg (%.2f mm)" %
      (RC, L_CONTACT, a1, a2, entry_half, slot_end, web, math.radians(web) * RC))
print("sleeve rotation to the nominal seat %.1f deg; stop pin arc: open stop at 0, closing over-travel stop at %.1f deg (lock stage end)" % (a1 + a2 / 2, a1 + a2))
assert web > 5

section("2. axial tolerance stack at seating (Hirth teeth fully meshed)")
stack = [("tail: Hirth pitch plane to lug axis (3.6 mm, IT9)", IT9["3-6"] / 2),
         ("tail: lug radius (dia 3 g6, -2..-8 um)", 0.004),
         ("tail: Hirth tooth form, axial effect (IT9 on the 0.4 mm teeth)", IT9["1-3"] / 2),
         ("head: Hirth tooth form, axial effect (IT9)", IT9["1-3"] / 2),
         ("head: lip, pitch plane to rear face (0.8 mm, IT9)", IT9["1-3"] / 2),
         ("head: PTFE ring (0.3 mm, IT9; creep at 0.6 MPa not counted)", IT9["1-3"] / 2),
         ("head: sleeve front face to flank at the seat angle (2.5 mm, IT9)", IT9["1-3"] / 2),
         ("head: thrust running play (0 under load: the lug load pushes the sleeve forward)", 0.0)]
tot = sum(v for _, v in stack)
for n, v in stack: print("  +-%.4f  %s" % (v, n))
lo, hi = s_nom - tot, s_nom + tot
print("seat depth %.3f..%.3f inside the lock stage %.2f..%.2f: margins %.3f / %.3f" % (lo, hi, c1, c2, lo - c1, c2 - hi))
print("not in the stack: the cartridge position in the PA12 plate and the plate flushness. They set only the PA12 gap between")
print("  the two units' plates: nominal 1.0 (flange), minus 0.3 + 0.3 (SLS) and 0.1 (cartridge seating) = 0.3 mm minimum.")
print("  The flange (r 6.3) is smaller than the lip and the window (r 6.45), so it can only bear on the lip's teeth")
assert c1 < lo and hi < c2

section("3. self-locking of the lock stage")
t2 = tand(LAM2)
for name, mus in (("dry (declared condition)", MU_DRY), ("machine oil (contamination case)", MU_OIL)):
    print("  %s: mu %.2f..%.2f vs tan 3 deg = %.4f -> margin %.2f..%.2f" % (name, mus[0], mus[1], t2, mus[0] / t2, mus[1] / t2))
print("  the PTFE thrust friction adds holding torque; not credited")

section("4. closing preload (voltage-limited stall)")
def k_close(mu, lam, mut): return RC * tand(lam + atand(mu)) + mut * R_THRUST
def k_release(mu, lam, mut): return RC * tand(atand(mu) - lam) + mut * R_THRUST
t_motor_c = T_STALL_3V * V_C / 3.0
Ts_c = [t_motor_c * GEAR_I * e for e in ETA]
F_min = Ts_c[0] / k_close(MU_DRY[1], LAM2, MU_T[1])
F_max = Ts_c[1] / k_close(MU_DRY[0], LAM2, MU_T[0])
Fo_min = Ts_c[0] / k_close(MU_OIL[1], LAM2, MU_T[1])
Fo_max = Ts_c[1] / k_close(MU_OIL[0], LAM2, MU_T[0])
print("closing at %.1f V: motor stall %.2f mN m, sleeve %.2f..%.2f mN m" % (V_C, t_motor_c, Ts_c[0], Ts_c[1]))
print("preload F_p dry %.2f..%.2f N; oil %.2f..%.2f N" % (F_min, F_max, Fo_min, Fo_max))
print("F_p scales with the actual motor constant (typical datasheet values only); retention does not depend on F_p (sections 6-8)")

section("5. declared loads (PROVISIONAL modelling assumptions, Q31 tabletop chain of 5)")
T_TENSION = 4 * MU_TABLE_BOUND * W
T_TORSION = 2 * W * HALF_WIDTH
M_OOP = W * UNIT_LEN
M_INPLANE = 3.0 * SECTOR_I * ETA[1]
M_INPLANE_FAULT = T_STALL_3V * 3.6 / 3.0 * SECTOR_I
SHEAR = W
for n, v, u in (("tension (4 mu W, mu = 1)", T_TENSION, "N"), ("torsion (2 W x 12.7)", T_TORSION, "mN m"),
                ("out-of-plane bending (W x 47.2)", M_OOP, "mN m"), ("in-plane bending at the joint drive limit", M_INPLANE, "mN m"),
                ("in-plane bending, fault (joint stall at 3.6 V)", M_INPLANE_FAULT, "mN m"), ("shear (W)", SHEAR, "N")):
    print("  %-52s %7.3f %s" % (n, v, u))

section("6. Hirth face coupling (torsion and shear, zero lash under preload)")
pitch = 2 * math.pi * HIRTH_RM / HIRTH_N
print("36 teeth, 90 deg included, r %.1f..%.1f; pitch at r_m %.2f = %.3f mm, tooth height about %.2f mm" % (HIRTH_RI, HIRTH_RO, HIRTH_RM, pitch, pitch / 2))
F_t = T_TORSION / HIRTH_RM
F_sep_t = F_t * tand(45)
print("torsion: tangential %.2f N at r_m; axial separating force <= %.2f N (45 deg flanks, flank friction neglected: upper bound)" % (F_t, F_sep_t))
print("  the teeth stay seated while F_p_min %.2f > %.2f (ratio %.2f). Roll cannot change without axial separation, and axial" % (F_min, F_sep_t, F_min / F_sep_t))
print("  separation is resisted by the self-locking stage. The lugs never slide along the flank, so the sleeve cannot be walked")
print("  by torsion slip, and no face friction is relied on")
print("shear %.3f N: the radial teeth centre the flange (separating force <= shear x tan 45); the pilot (clearance %.3f..%.3f) is an entry guide" % (SHEAR, *PILOT_CLR))
r_slot = (BORE_R + HOUSING_RO) / 2
clr_min, clr_max = (SLOT_W - IT9["3-6"] / 2) - (3.0 - 0.002), (SLOT_W + IT9["3-6"] / 2) - (3.0 - 0.008)
print("roll indexing: the lugs index roll within the slot lash %.2f..%.2f deg (r %.2f); half a tooth pitch is 5 deg, so the" %
      (math.degrees(clr_min / 2 / r_slot), math.degrees(clr_max / 2 / r_slot), r_slot))
print("  teeth always meet their own gaps; the tooth phase to the slots (one set-up, IT9) is within about +-0.2 deg")

section("7. carriers, each load alone")
print("tension: F_p_min %.2f > %.3f N, faces stay closed (ratio %.2f); geometric carrier: lugs on the self-locking stage" % (F_min, T_TENSION, F_min / T_TENSION))
print("torsion: Hirth teeth, ratio %.2f to tooth separation; beyond separation the lugs on the housing slot sides (r %.2f)" % (F_min / F_sep_t, r_slot))
tip = F_min * HIRTH_RO
print("out-of-plane bending: tipping %.2f mN m vs %.2f (ratio %.2f); beyond it the pilot couple bounds the tilt to <= %.2f deg" % (tip, M_OOP, tip / M_OOP, math.degrees(PILOT_CLR[1] / 5.0)))
print("in-plane bending: tipping %.2f vs %.2f (ratio %.2f); beyond it the lug pair (lever %.2f mm) as axial load on the self-locking stage" % (tip, M_INPLANE, tip / M_INPLANE, RC + HIRTH_RO))
print("shear: Hirth teeth (ratio %.1f of preload to separating force)" % (F_min / SHEAR))
assert F_min > T_TENSION and F_min > F_sep_t and tip > M_OOP and tip > M_INPLANE

section("8. all declared loads at once (an upper bound; not a stated operating case)")
sep_axial = T_TENSION + F_sep_t + SHEAR
print("axial separating loads: tension %.3f + torsion %.3f + shear %.3f = %.3f N vs F_p_min %.2f: the teeth stay seated (ratio %.2f)" %
      (T_TENSION, F_sep_t, SHEAR, sep_axial, F_min, F_min / sep_axial))
rem = F_min - sep_axial
M_comb = math.hypot(M_OOP, M_INPLANE)
print("residual clamp %.2f N: tipping capacity %.2f mN m against the vector sum of both bendings %.2f mN m: the faces gap at one edge" % (rem, rem * HIRTH_RO, M_comb))
print("  gapping is not separation: the lugs stay on the self-locking stage (geometric while self-locked), the teeth on the")
print("  far side stay meshed, the pilot bounds the tilt. Retention holds; stiffness falls (Gate 2)")
assert sep_axial < F_min

section("9. release (bounded, independent: the head unit's own motor)")
ts_avail = T_STALL_3V * V_RELEASE / 3.0 * GEAR_I * ETA[0]
worst = (F_max + sep_axial) * k_release(MU_DRY[1], LAM2, MU_T[1])
worst_o = (Fo_max + sep_axial) * k_release(MU_OIL[1], LAM2, MU_T[1])
print("release needs, worst dry corner (F_p_max %.2f + all axial loads, flank 0.23, thrust 0.20): %.2f mN m" % (F_max, worst))
print("release needs, oil case: %.2f mN m" % worst_o)
print("available at %.1f V at the motor (cell >= 3.5 V rule), eta 0.9: %.2f mN m -> margins %.2f dry, %.2f oil" % (V_RELEASE, ts_avail, ts_avail / worst, ts_avail / worst_o))
print("preload and available torque scale with the same motor constant: the margin does not depend on motor-to-motor variation")
print("capture stage drawing one free unit at mu = 1: %.2f mN m (vs closing %.2f)" % (MU_TABLE_BOUND * W * k_close(MU_DRY[1], LAM1, MU_T[1]), Ts_c[0]))
print("ejection: the outer flank pushes the stud out %.1f mm; the reaction pushes the sleeve rearward onto the 304 retainer collar" % (D1 + D2))
assert ts_avail / worst > 1.25 and ts_avail / worst_o > 1.25

section("10. stresses")
Es = 1 / ((1 - NU_SS ** 2) / E_SS + (1 - NU_BR ** 2) / E_BR)
def hertz_line(F, R, L): return math.sqrt(F * Es / (math.pi * R * L))
onset = 1.67 * SY_BR
lever = RC + HIRTH_RO
cases = [("F_p_max alone (dry)", F_max / 2),
         ("F_p_max + all axial loads + in-plane bending at the drive limit (dry)", (F_max + sep_axial) / 2 + M_INPLANE / lever),
         ("same, oil case", (Fo_max + sep_axial) / 2 + M_INPLANE / lever),
         ("fault bending (joint stall at 3.6 V), dry", (F_max + sep_axial) / 2 + M_INPLANE_FAULT / lever)]
for n, F in cases:
    print("  lug on bronze flank, %s: %.2f N per lug, Hertz p0 %.0f MPa (onset %.0f = 1.67 x yield, rule of thumb)" % (n, F, hertz_line(F, LUG_R, L_CONTACT), onset))
assert hertz_line(cases[1][1], LUG_R, L_CONTACT) < onset and hertz_line(cases[2][1], LUG_R, L_CONTACT) < onset
Z = math.pi * (2 * LUG_R) ** 3 / 32
print("  lug root bending, combination: %.1f MPa (304 yield 205)" % (cases[1][1] * (RC - STUD_R) / Z))
print("  PTFE ring r 3.6..4.4: %.2f MPa at the combination" % (2 * cases[1][1] / (math.pi * (4.4 ** 2 - 3.6 ** 2))))
band = 0.05   # PROVISIONAL flank contact band width per tooth flank
print("  Hirth flanks: %.2f N on 72 flanks, contact band %.2f mm (PROVISIONAL): %.1f MPa" % (F_max + sep_axial, band, (F_max + sep_axial) / (72 * (HIRTH_RO - HIRTH_RI) * band)))

section("11. stops, retainer and mount")
t_stop = T_STALL_3V * 3.6 / 3.0 * GEAR_I * ETA[1]
r_pin, d_pin = 5.3, 1.0
F_pin = t_stop / r_pin
print("stop pin dia %.1f (304), pressed into the lip rear face at r %.1f, runs in an arc groove (0.5 deep) of the sleeve front face;" % (d_pin, r_pin))
print("  worst stop torque %.1f mN m (3.6 V stall, eta 1): %.2f N, shear %.1f MPa, bronze bearing %.1f MPa" % (t_stop, F_pin, F_pin / (math.pi * d_pin ** 2 / 4), F_pin / (d_pin * 0.5)))
print("  open stop sets the entry notch over the housing slot: the V lead-in allows +-%.1f deg at Rc; stop position tolerance (IT9) about +-0.3 deg" % math.degrees(LIP_V / RC))
F_ej = MU_TABLE_BOUND * W + 0.5
print("rear retainer collar (304, pressed on the housing tube, r 2.05..4.9 x 0.4): ejection reaction <= %.2f N (drag of one free unit at mu 1 plus a" % F_ej)
print("  PROVISIONAL 0.5 N for pilot and teeth friction) on the gear rear face r 3.55..4.9: %.2f MPa" % (F_ej / (math.pi * (4.9 ** 2 - 3.55 ** 2))))
ear_z = 7.4
M_mount = max(M_OOP, M_INPLANE)
F_scr = M_mount / (2 * ear_z) + T_TENSION / 2
print("mount: two tapped 304 ears of the housing (M1.6, 1.6 thick, behind the front plate, axis offsets z +-%.1f) and countersunk M1.6" % ear_z)
print("  A2 screws through the 1.2 mm PA12 plate. Pull-out (tension %.3f N) bears the ears on the plate's inner face; push-in bears the" % T_TENSION)
print("  countersunk heads on the plate. Worst screw load (bending %.1f mN m over 2 x %.1f mm plus half the tension) %.2f N;" % (M_mount, ear_z, F_scr))
print("  PA12 bearing under a 3.2 mm countersunk head about %.2f MPa (PA2200 tensile strength 50 MPa)" % (F_scr / (math.pi / 4 * (3.2 ** 2 - 1.6 ** 2))))

section("12. pre-alignment windows (presented pose; not a capture window, CPL-006)")
lat = (BORE_R + BORE_CH) - (STUD_R - NOSE_CH)
print("lateral: bore chamfer 0.6, nose chamfer 0.5 and the clearance: +-%.2f mm vs the +-0.6 mm two-unit PA12 stack" % lat)
print("no wedging on the 45 deg chamfers while mu < 1: at the dry steel-steel upper bound 0.8 the centring force is %.2f of the push" % ((1 - MU_SS_MAX) / (1 + MU_SS_MAX)))
lug_front = s_nom + LUG_R
pilot_cyl = STUD_L - NOSE_CH
print("sequence: the lug fronts are at %.2f, the pilot cylinder starts at %.2f: the pilot is %.2f deep (bore chamfer %.2f) when the lugs" % (lug_front, pilot_cyl, pilot_cyl - lug_front, BORE_CH))
print("  reach the lip, so the lateral error at the lugs is <= the pilot clearance %.3f mm, inside the +-0.6 mm V lead-ins" % PILOT_CLR[1])
assert pilot_cyl - lug_front >= BORE_CH - 1e-9
print("roll: V lead-in 0.6 at the lug tip radius %.1f: +-%.1f deg vs about +-1.4 deg (0.6 mm base flatness over 25 mm)" % (LUG_TIP, math.degrees(LIP_V / LUG_TIP)))
print("pitch: both units stand on the table; flatness stack 0.6 mm over 47 mm = +-%.2f deg" % math.degrees(math.atan(0.6 / 47)))
print("yaw and the joint angles: only the relative pose of the head unit's head segment and the tail unit's tail segment matters;")
print("  each is rigid, so a joint angle error moves the far segments, not the coupler. Full pilot engagement bounds the yaw to")
print("  clearance / length = %.2f deg before the Hirth teeth meet, and the teeth align it under the draw" % math.degrees(PILOT_CLR[1] / 5.0))
print("axial push to reach the capture stage: not supplied by the candidate. Stroke %.2f mm, force about mu W = %.2f N at mu 1 plus" % (c0, W))
print("  chamfer friction; it comes from the experiment's documented start configuration (Q31 item 1) or a later approach design")
