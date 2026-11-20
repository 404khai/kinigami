#!/usr/bin/env python3
"""Generate candidates/cand-d/declaration.json and check packaging on paper.

Plain Python 3, no third-party packages. All lengths below are in mm and are
converted to integer micrometres on output. Run from the repository root:

    python3 candidates/cand-d/scripts/gen_declaration.py [--write]

Without --write it only prints the checks. The registered evaluator
(zig-out/bin/kinigami-gate1) is the authority for G1-G8; the checks here
(component box overlap with the protocol's 1 um erosion, cavity containment,
mass sum, centre of mass) are a design aid that must agree with it.
"""
import json, math, sys, itertools

ACCESSED = "2026-11-20"
DECLARED = "2026-11-20"

# ---------------------------------------------------------------- sources
SRC = {
    "pa": ("datasheet", "https://3dprinting.com/wp-content/uploads/2019/05/EOS-pa2200-white-datasheet-TDS.pdf",
           "EOS PA 2200 material data sheet (density 930 kg/m3, tensile strength 50 MPa, modulus 1700 MPa)"),
    "ss": ("datasheet", "https://www.atimaterials.com/Products/Documents/datasheets/stainless-specialty-steel/austenitic/ati_302_304_304l_305_tds_en1_v1.pdf",
           "ATI 302/304/304L/305 technical data sheet (304 density 7.90 g/cm3, yield 205 MPa, UTS 515 MPa); size tolerances ISO 286 IT grades https://en.wikipedia.org/wiki/IT_Grade"),
    "br": ("datasheet", "https://www.concast.com/c93200.php",
           "Wieland Concast C93200 (SAE 660) leaded tin bearing bronze: density 8.91 g/cm3, yield 138 MPa min, modulus 100 GPa, machinability 70, uses bushings and bearings"),
    "cell": ("datasheet", "https://www.grepow.com/high-discharge-rate-battery/15c-high-power-lipo.html",
             "Grepow 15C high-power LiPo table, row GRP8020030 (350 mAh, 3.7 V, Max. Cont. Discharge Current 5.25 A, 7.5 x 20.0 x 31.0 mm, 8.0 g)"),
    "mcu": ("datasheet", "https://www.adafruit.com/product/5405",
            "Adafruit QT Py ESP32-C3 product page (22.0 x 17.8 x 5.7 mm, 2.1 g, 600 mA peak 3.3 V regulator)"),
    "drv": ("datasheet", "https://www.pololu.com/product/2135/specs",
            "Pololu DRV8835 dual carrier specs (0.4 x 0.7 in, 0.5 g, 1.2 A continuous, 1.5 A peak); profile height 1.8 mm from https://www.pololu.com/file/0J1536/drv8835-dual-motor-driver-carrier-dimensions.pdf; quiescent from TI DRV8835 datasheet https://www.ti.com/lit/ds/symlink/drv8835.pdf (IVM 2000 uA max + IVCC 2000 uA max = 4 mA x 3.7 V = 15 mW)"),
    "mot": ("datasheet", "https://www.precisionmicrodrives.com/datasheets/206-109-V0.pdf",
            "Precision Microdrives 206-109 6 mm planetary gearmotor 136:1: 1.2 g, body 6 dia x 18.7 mm, shaft 2 dia x 3.6 mm, 3 V rated, 3.6 V max, rated 3 mN m at 140 rpm, stall 9 mN m, start current 230 mA, typical rated-load power 215 mW"),
    "scr": ("datasheet", "https://www.atimaterials.com/Products/Documents/datasheets/stainless-specialty-steel/austenitic/ati_302_304_304l_305_tds_en1_v1.pdf",
            "ATI 304 density 7.90 g/cm3 (A2 = 18/8 304 family, assumption); screw dimensions from https://www.westfieldfasteners.co.uk/A2-ScrewBolt-PoziPan-M1.6.html"),
    "cu": ("datasheet", "https://aurubis.com/dam/jcr:ec116d17-1541-419a-a897-ad31b4fa6c93/c11000-cu-etp-us.pdf",
           "Aurubis C11000 density 8.9 g/cm3; wire dimensions from https://www.digikey.ca/en/products/detail/alpha-wire/2841-7-YL001/3708252 (distributor page of manufacturer data)"),
}
RHO = {"pa": 930.0, "ss": 7900.0, "br": 8910.0, "scr": 7900.0, "cu": 8900.0, "ptfe": 2150.0}

# ---------------------------------------------------------------- geometry (mm)
YO, ZO = 12.7, 12.0          # outer half width (y) and half height (z)
T = 1.2                      # shell wall (PA12 SLS, >= 1.0 mm rule, Q68)
YI, ZI = YO - T, ZO - T
LX0, LX1 = 1.8, 35.6         # long segment (head) outer x
SX0, SX1 = -10.6, -1.8
INSET_Y, INSET_Z = 11.9, 11.2   # end plates inset 0.8 mm (rounded end edges)
LXE, SXE = LX1 - T, SX0 + T     # inner faces of the end plates       # short segment (tail) outer x
AX = (3.3, 1.0)              # coupler axis (y, z), same for head and tail

# head cartridge (304 housing + C93200 cam sleeve with gear) along x
LIP = 0.8                    # housing lip thickness (front thrust face)
CART_X0 = 28.0               # rear of gear ring
CART_R = 6.45                # gear pitch radius = cartridge box half extent
# tail stud (304, one piece: flange, pilot, two lugs)
FL_T, FL_R = 1.0, 6.5        # flange thickness and radius
STUD_R, STUD_L = 2.0, 6.2    # pilot radius, length beyond the flange face
LUG_R, LUG_S, LUG_REACH = 1.5, 3.6, 5.9   # lug radius, nominal depth of lug axis below flange face, lug tip radius

PIN_DIST = 6.45 + 1.8        # coupler pinion centre distance (gear z43 m0.3 + pinion z12 m0.3)
JM = (6.2, 8.47)             # joint motor axis (x, y), vertical
SECT_R = 8.7                 # joint sector pitch radius (z58 m0.3)

def q_axis(axis, deg):
    a = math.radians(deg) / 2
    s = math.sin(a)
    return [math.cos(a), axis[0] * s, axis[1] * s, axis[2] * s]

QI = [1.0, 0.0, 0.0, 0.0]

def um(v):
    return int(round(v * 1000))

def box_from_bounds(x0, x1, y0, y1, z0, z1):
    return ([(x1 - x0) / 2, (y1 - y0) / 2, (z1 - z0) / 2], [(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2], QI)

def obox(center, he, q):
    return (list(he), list(center), q)

# ---------------------------------------------------------------- components
comps = []

def add(cid, kind, desc, box, mass_mg=None, mat=None, volume_mm3=None, src=None,
        peak=0, avg=0, mass_basis=None, dim_basis="derived", power_basis="derived", extra=None):
    he, c, q = box
    e = {"id": cid, "kind": kind, "description": desc}
    if mat is not None:
        rho = RHO[mat]
        m = rho * volume_mm3 * 1e-9 * 1e6  # mg
        e["mass_mg"] = int(round(m))
        e["mass_basis"] = "derived"
        e["derivation"] = {"density_kg_m3": rho, "volume_m3": volume_mm3 * 1e-9}
        src = src or mat
    else:
        e["mass_mg"] = mass_mg
        e["mass_basis"] = mass_basis or "source"
    e["box"] = {"half_extent_um": [um(v) for v in he], "pose": {"position_um": [um(v) for v in c], "orientation": q}}
    e["dimension_basis"] = dim_basis
    e["peak_power_mw"] = peak
    e["average_power_mw"] = avg
    e["power_basis"] = power_basis
    k, url, title = SRC[src]
    e["source"] = {"kind": k, "url": url, "accessed": ACCESSED, "title": title}
    if extra:
        e.update(extra)
    comps.append(e)

def slab(cid, desc, x0, x1, y0, y1, z0, z1):
    v = (x1 - x0) * (y1 - y0) * (z1 - z0)
    add(cid, "structure", desc + " (PA12 SLS; mass = slab volume x density)", box_from_bounds(x0, x1, y0, y1, z0, z1), mat="pa", volume_mm3=v)

# long (head) segment shell
slab("L-top", "head segment top wall", LX0, LXE, -YO, YO, ZI, ZO)
slab("L-bottom", "head segment bottom wall", LX0, LXE, -YO, YO, -ZO, -ZI)
slab("L-side-p", "head segment +y side wall", LX0, LXE, YI, YO, -ZI, ZI)
slab("L-side-n", "head segment -y side wall", LX0, LXE, -YO, -YI, -ZI, ZI)
# inner end wall facing the hinge gap; open below z -9.0 for the joint sector
slab("L-inner", "head segment inner end wall (slot z -10.8 to -9.0 for the joint sector)", LX0, LX0 + T, -YI, YI, -9.0, ZI)
# front wall with a window for the cartridge lip
wy0, wy1 = AX[0] - CART_R, AX[0] + CART_R
wz0, wz1 = AX[1] - CART_R, AX[1] + CART_R
fx0, fx1 = LX1 - T, LX1
slab("L-front-n", "head front wall, -y of the cartridge window", fx0, fx1, -INSET_Y, wy0, -INSET_Z, INSET_Z)
slab("L-front-p", "head front wall, +y of the cartridge window", fx0, fx1, wy1, INSET_Y, -INSET_Z, INSET_Z)
slab("L-front-lo", "head front wall below the cartridge window", fx0, fx1, wy0, wy1, -INSET_Z, wz0)
slab("L-front-hi", "head front wall above the cartridge window", fx0, fx1, wy0, wy1, wz1, INSET_Z)
# short (tail) segment shell
slab("S-top", "tail segment top wall", SXE, SX1, -YO, YO, ZI, ZO)
slab("S-bottom", "tail segment bottom wall", SXE, SX1, -YO, YO, -ZO, -ZI)
slab("S-side-p", "tail segment +y side wall", SXE, SX1, YI, YO, -ZI, ZI)
slab("S-side-n", "tail segment -y side wall", SXE, SX1, -YO, -YI, -ZI, ZI)
slab("S-inner", "tail segment inner end wall facing the hinge gap", SX1 - T, SX1, -YI, YI, -ZI, ZI)
slab("S-end", "tail segment end plate carrying the stud flange (inset 0.8 mm at its edges)", SX0, SXE, -INSET_Y, INSET_Y, -INSET_Z, INSET_Z)

# electronics
add("cell", "energy_source", "Grepow GRP8020030 1S LiPo, 350 mAh, 15C, 3.7 V, 7.5 x 20.0 x 31.0 mm, 8.0 g; stands on edge along the -y wall of the head segment (31 along x, 7.5 along y, 20 along z)",
    box_from_bounds(3.3, 34.3, -YI, -YI + 7.5, -10.0, 10.0), mass_mg=8000, src="cell", dim_basis="source",
    extra={"nominal_voltage_v": 3.7, "rated_continuous_discharge_a": 5.25, "energy_mj": 4662000})
add("controller", "controller", "Adafruit QT Py ESP32-C3 (product 5405), 22.0 x 17.8 x 5.7 mm, 2.1 g, BLE; stands across the tail segment (5.7 along x, 22 along y, 17.8 along z). Power derived: 3.3 V regulator 600 mA peak x 3.7 V = 2220 mW, used as both peak and average bound",
    box_from_bounds(-9.3, -3.6, -11.0, 11.0, -8.9, 8.9), mass_mg=2100, src="mcu", dim_basis="source", peak=2220, avg=2220)
add("driver", "other", "Pololu DRV8835 dual driver carrier: channel A coupler motor, channel B joint motor; 10.2 x 17.8 x 1.8 mm, 0.5 g; stands along the +y wall of the head segment (10.2 along x, 1.8 along y, 17.8 along z); quiescent 15 mW bound",
    box_from_bounds(10.0, 20.2, YI - 1.8, YI, -8.9, 8.9), mass_mg=500, src="drv", dim_basis="source", peak=15, avg=15)

# coupler drive
my, mz = AX[0], AX[1] - PIN_DIST
add("coupler-motor", "actuator", "Precision Microdrives 206-109 gearmotor driving the cam sleeve; axis along x at (y, z) = (%.2f, %.2f), body x 9.3 to 28.0, shaft cut to 1.5 mm (to x 29.5; the shaft inside the pinion is not boxed separately). Peak 851 mW (230 mA start x 3.7 V), average 215 mW (rated-load bound)" % (my, mz),
    box_from_bounds(9.3, 28.0, my - 3.0, my + 3.0, mz - 3.0, mz + 3.0), mass_mg=1200, src="mot", dim_basis="source", peak=851, avg=215)
pin_v = math.pi * 1.8 ** 2 * 1.5 - math.pi * 1.0 ** 2 * 1.5
add("coupler-pinion", "actuator", "spur pinion m 0.3 z 12 (pitch radius 1.8 mm, 1.5 mm face) on the coupler motor shaft; box bounded at the pitch circle toward the sleeve gear (tooth tips cross the pitch line by design); 304, volume = pitch-disc minus 2 mm bore",
    box_from_bounds(CART_X0, CART_X0 + 1.5, my - 1.8, my + 1.8, mz - 1.8, mz + 1.8), mat="ss", volume_mm3=pin_v)

# head cartridge: 304 housing (tube r 2.0..4.0 with lip r 6.45) + C93200 sleeve (r 4.05..5.8) with gear ring (to pitch r 6.45)
hous_tube = math.pi * (3.5 ** 2 - 2.0 ** 2) * (LX1 - CART_X0) - 2 * 3.05 * 1.5 * 5.4
hous_lip = math.pi * (CART_R ** 2 - 2.0 ** 2) * LIP - 2 * 4.25 * 3.9 * LIP
v_ss = hous_tube + hous_lip
sleeve_x0 = CART_X0 + 1.5
sleeve_x1 = LX1 - LIP - 0.3   # 0.3 mm PTFE thrust ring in front of the sleeve
v_sleeve = math.pi * (6.0 ** 2 - 3.55 ** 2) * (sleeve_x1 - sleeve_x0) - 2 * 3.1 * 10.4 * 2.45
v_gear = math.pi * (CART_R ** 2 - 3.55 ** 2) * 1.5
v_ptfe = math.pi * (4.4 ** 2 - 3.6 ** 2) * 0.3
v_br = v_sleeve + v_gear
m_cart = RHO["ss"] * v_ss * 1e-3 * 1e-3 + RHO["br"] * v_br * 1e-3 * 1e-3  # g
v_cart = v_ss + v_br + v_ptfe
rho_eff = (RHO["ss"] * v_ss + RHO["br"] * v_br + RHO["ptfe"] * v_ptfe) / v_cart
add("head-cartridge", "coupler_mechanism",
    "head coupler cartridge, one subassembly of three concentric parts: 304 housing (tube r 2.0 to 3.5 with pilot bore 4.0 H7 and two axial lug slots 3.05 wide; front lip 0.8 thick with V lead-ins and a 0.6 x 45 deg bore chamfer; %.1f mm3), C93200 cam sleeve (r 3.55 to 6.0, two two-stage helical slots 20 deg / 3 deg, gear ring m 0.3 z 43 on its rear; %.1f mm3) and a PTFE thrust ring (r 3.6 to 4.4 x 0.3 between the sleeve and the lip; %.1f mm3). Effective density = (7900 V_304 + 8910 V_bronze + 2150 V_PTFE) / V = %.1f kg/m3 from the three cited densities. Box bounded at the gear pitch circle toward the pinion" % (v_ss, v_br, v_ptfe, rho_eff),
    box_from_bounds(CART_X0, LX1, AX[0] - CART_R, AX[0] + CART_R, AX[1] - CART_R, AX[1] + CART_R),
    mass_mg=None, src="ss")
comps[-1]["mass_mg"] = int(round(rho_eff * v_cart * 1e-9 * 1e6))
comps[-1]["mass_basis"] = "derived"
comps[-1]["derivation"] = {"density_kg_m3": rho_eff, "volume_m3": v_cart * 1e-9}
comps[-1]["source"]["title"] = SRC["ss"][2] + "; C93200 bronze from " + SRC["br"][1] + " (density 8.91 g/cm3, yield 138 MPa); PTFE from https://multimedia.3m.com/mws/media/132393O/ptfe-tf-1620-data-sheet (3M Dyneon TF 1620, specific gravity 2.15)"

# tail stud: flange + pilot + lugs, 304, one machined part, outside the shell
v_stud = math.pi * FL_R ** 2 * FL_T + math.pi * STUD_R ** 2 * STUD_L + 2 * math.pi * LUG_R ** 2 * (LUG_REACH - STUD_R)
sx_face = SX0 - FL_T
add("tail-stud", "coupler_mechanism",
    "tail stud, one machined 304 part: flange r 6.5 x 1.0 (face at x %.1f, screwed to the tail end wall), pilot r 2.0 g6 x 6.4, two lugs r 1.5 (dia 3.0 g6) to radius 5.9 with their axis 3.6 below the flange face (nominal)" % sx_face,
    box_from_bounds(sx_face - STUD_L, SX0, AX[0] - FL_R, AX[0] + FL_R, AX[1] - FL_R, AX[1] + FL_R), mat="ss", volume_mm3=v_stud)

# joint drive (vertical axis through the pivot at x = 0, y = 0)
jx, jy = JM
ang = math.degrees(math.atan2(jy, jx))
add("joint-motor", "actuator", "Precision Microdrives 206-109 gearmotor for the body joint, axis vertical at (x, y) = (%.2f, %.2f), body z -8.9 to 9.8, shaft down, cut to 1.8 mm; peak 851 mW, average 215 mW" % (jx, jy),
    box_from_bounds(jx - 3.0, jx + 3.0, jy - 3.0, jy + 3.0, -8.9, 9.8), mass_mg=1200, src="mot", dim_basis="source", peak=851, avg=215)
dirv = (math.cos(math.radians(ang)), math.sin(math.radians(ang)))
qz = q_axis((0, 0, 1), ang)
pc = (dirv[0] * (SECT_R + 1.8), dirv[1] * (SECT_R + 1.8))
add("joint-pinion", "actuator", "spur pinion m 0.3 z 12 on the joint motor shaft (z -10.7 to -9.2); box oriented toward the pivot and bounded at the pitch circle facing the sector; 304, pitch-disc minus 2 mm bore",
    obox((pc[0], pc[1], -9.95), (1.8, 1.8, 0.75), qz), mat="ss", volume_mm3=pin_v)
SPAN = 21.0  # deg each side: joint range 15 deg plus 6 deg of tooth engagement
sect_in = 4.5
sect_he_t = SECT_R * math.sin(math.radians(SPAN))
sc = ((SECT_R + sect_in) / 2 * dirv[0], (SECT_R + sect_in) / 2 * dirv[1])
v_sect = (math.radians(2 * SPAN) / 2) * (SECT_R ** 2 - sect_in ** 2) * 1.5
add("joint-sector", "structure", "toothed sector m 0.3 (pitch radius 8.7, z 58 equivalent), +-21 deg about the joint motor direction (%.1f deg), r 4.5 to 8.7, 1.5 mm thick at z -10.7 to -9.2; part of the tail segment's lower hinge plate, runs in the head segment's bottom layer through the L-inner wall slot; 304" % ang,
    obox((sc[0], sc[1], -9.95), ((SECT_R - sect_in) / 2, sect_he_t, 0.75), qz), mat="ss", volume_mm3=v_sect)
v_plate = 3.4 * 3.2 * 1.5 + math.pi * 1.6 ** 2 * 1.5 / 2 - math.pi * 1.0 ** 2 * 1.5
add("hinge-plate-low", "structure", "tail segment lower hinge plate (z -10.7 to -9.2) from the tail inner face (x -1.8) to the pin, boss r 1.6 around the pin (0.2 mm clear of the head inner face at every joint angle); carries the sector; 304, volume = plate minus pin bore",
    box_from_bounds(-1.8, 1.6, -1.6, 1.6, -10.7, -9.2), mat="ss", volume_mm3=v_plate)
add("hinge-plate-up", "structure", "tail segment upper hinge plate (z 7.6 to 9.1) from the tail inner face to the pin, boss r 1.6; 304, volume = plate minus pin bore",
    box_from_bounds(-1.8, 1.6, -1.6, 1.6, 7.6, 9.1), mat="ss", volume_mm3=v_plate)
add("hinge-ear-low", "structure", "head segment lower ear (z -9.0 to -7.5) from the head inner face (x 1.8) to the pin, boss r 1.6, pin pressed in; 304, volume = plate minus pin bore",
    box_from_bounds(-1.6, 1.8, -1.6, 1.6, -9.0, -7.5), mat="ss", volume_mm3=v_plate)
add("hinge-ear-up", "structure", "head segment upper ear (z 9.3 to 10.8) from the head inner face to the pin, boss r 1.6, pin pressed in; 304, volume = plate minus pin bore",
    box_from_bounds(-1.6, 1.8, -1.6, 1.6, 9.3, 10.8), mat="ss", volume_mm3=v_plate)
v_pin = math.pi * 1.0 ** 2 * 21.5
add("hinge-pin", "structure", "hinge pin dia 2.0 x 21.5 (z -10.7 to 10.8), 304; box covers the exposed length z -7.5 to 7.6 between the ears and plates (the rest lies inside their bosses)",
    box_from_bounds(-1.0, 1.0, -1.0, 1.0, -7.5, 7.6), mat="ss", volume_mm3=v_pin)

# lumps
v_scr = 14 * 18.50
add("fasteners", "structure", "14x M1.6 x 4 A2 pan head screws (dk 3.2, k 1.3); bounding volume pi*1.6^2*1.3 + pi*0.8^2*4 = 18.50 mm3 each (upper bound), 304 density assumed for A2; LUMPED box, not at the real screw positions",
    box_from_bounds(12.0, 26.0, -3.8, -0.2, 4.0, 9.0), mat="scr", volume_mm3=v_scr)
v_h = math.pi * 0.305 ** 2 * 200
add("harness", "other", "harness lump: 200 mm Alpha Wire 2841/7 30 AWG PTFE, OD 0.61 mm; bounding volume pi*0.305^2*200 at copper density (upper bound); lumped box, no routing",
    box_from_bounds(4.0, 11.0, -3.8, -0.2, 4.0, 9.0), mat="cu", volume_mm3=v_h)

# ---------------------------------------------------------------- primitives
def prim_box(pid, role, x0, x1, y0, y1, z0, z1):
    he, c, q = box_from_bounds(x0, x1, y0, y1, z0, z1)
    return {"id": pid, "kind": "box", "half_extent_um": [um(v) for v in he],
            "pose": {"position_um": [um(v) for v in c], "orientation": q}, "role": role}

def prim_cyl_x(pid, role, r, x0, x1, y, z):
    return {"id": pid, "kind": "cylinder", "radius_um": um(r), "half_height_um": um((x1 - x0) / 2),
            "pose": {"position_um": [um((x0 + x1) / 2), um(y), um(z)], "orientation": q_axis((0, 1, 0), 90)}, "role": role}

def prim_cyl_y(pid, role, r, half, x, y, z):
    return {"id": pid, "kind": "cylinder", "radius_um": um(r), "half_height_um": um(half),
            "pose": {"position_um": [um(x), um(y), um(z)], "orientation": q_axis((1, 0, 0), 90)}, "role": role}

lug_x = sx_face - LUG_S
body = [prim_box("head-segment", "body", LX0, LXE, -YO, YO, -ZO, ZO),
        prim_box("head-front-plate", "body", LXE, LX1, -INSET_Y, INSET_Y, -INSET_Z, INSET_Z),
        prim_box("tail-segment", "body", SXE, SX1, -YO, YO, -ZO, ZO),
        prim_box("tail-end-plate", "body", SX0, SXE, -INSET_Y, INSET_Y, -INSET_Z, INSET_Z)]
coupler = [prim_cyl_x("stud-flange", "coupler", FL_R, sx_face, SX0, AX[0], AX[1]),
           prim_cyl_x("stud-pilot", "coupler", STUD_R, sx_face - STUD_L, sx_face, AX[0], AX[1]),
           prim_cyl_y("stud-lugs", "coupler", LUG_R, LUG_REACH, lug_x, AX[0], AX[1])]
cavity = [prim_box("cavity-envelope", "cavity", SX0, LX1, -YO, YO, -ZO, ZO),
          prim_box("stud-envelope", "cavity", sx_face - STUD_L, SX0, AX[0] - FL_R, AX[0] + FL_R, AX[1] - FL_R, AX[1] + FL_R)]

# ---------------------------------------------------------------- checks
def rotm(q):
    w, x, y, z = q
    return [[1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
            [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
            [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)]]

def obb(c):
    he = [v / 1000 - 0.001 for v in c["box"]["half_extent_um"]]
    p = [v / 1000 for v in c["box"]["pose"]["position_um"]]
    R = rotm(c["box"]["pose"]["orientation"])
    ax = [[R[0][i], R[1][i], R[2][i]] for i in range(3)]
    return p, ax, he

def dot(a, b): return sum(x * y for x, y in zip(a, b))
def cross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]

def sat_overlap(A, B):
    pa, aa, ha = A
    pb, ab, hb = B
    d = [pb[i] - pa[i] for i in range(3)]
    axes = aa + ab + [cross(u, v) for u in aa for v in ab]
    for L in axes:
        n = math.sqrt(dot(L, L))
        if n < 1e-9: continue
        L = [v / n for v in L]
        ra = sum(ha[i] * abs(dot(aa[i], L)) for i in range(3))
        rb = sum(hb[i] * abs(dot(ab[i], L)) for i in range(3))
        if abs(dot(d, L)) > ra + rb: return False
    return True

def corners(c):
    p, ax, he = obb(c)
    he = [v + 0.001 for v in he]
    out = []
    for s in itertools.product((-1, 1), repeat=3):
        out.append([p[i] + sum(s[k] * he[k] * ax[k][i] for k in range(3)) for i in range(3)])
    return out

def inside_box_prim(pt, pr):
    he = [v / 1000 for v in pr["half_extent_um"]]
    p = [v / 1000 for v in pr["pose"]["position_um"]]
    return all(abs(pt[i] - p[i]) <= he[i] + 1e-6 for i in range(3))

def run_checks():
    bad = []
    for a, b in itertools.combinations(comps, 2):
        if sat_overlap(obb(a), obb(b)):
            bad.append((a["id"], b["id"]))
    print("overlapping pairs:", bad if bad else "none", "of", len(comps) * (len(comps) - 1) // 2)
    out = [c["id"] for c in comps if not any(all(inside_box_prim(pt, pr) for pt in corners(c)) for pr in cavity)]
    print("boxes outside every cavity primitive:", out if out else "none")
    tot = sum(c["mass_mg"] for c in comps)
    com = [sum(c["mass_mg"] * c["box"]["pose"]["position_um"][i] for c in comps) / tot / 1000 for i in range(3)]
    print("total mass %d mg, W = %.4f N, COM (mm) = (%.2f, %.2f, %.2f)" % (tot, tot * 1e-6 * 9.80665, *com))
    pk = sum(c["peak_power_mw"] for c in comps if c["kind"] != "energy_source")
    print("peak %d mW vs 3.7 x 5.25 = 19425 mW" % pk)
    for c in comps:
        print("   %-16s %6d mg" % (c["id"], c["mass_mg"]))
    return bad, out, tot, com

if __name__ == "__main__":
    bad, out, tot, com = run_checks()
    print("joint motor direction %.2f deg; pinion at %.2f, %.2f" % (ang, pc[0], pc[1]))
    if "--write" in sys.argv:
        import os
        here = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(here, "declaration_text.json")) as f:
            text = json.load(f)
        decl = {"schema_version": 1, "candidate_id": "cand-d", "candidate_version": 1, "family": "B",
                "declared_on": DECLARED, "author": text["author"], "summary": text["summary"],
                "stowed_geometry": {"primitives": body + coupler + cavity},
                "chain_geometry": {"primitives": body + coupler},
                "components": comps,
                "mass_budget": {"total_mass_mg": tot},
                "assembly_access": {"statement": text["assembly_access"]},
                "coupler_sites": [
                    {"id": "site-head", "position_um": [um(LX1), um(AX[0]), um(AX[1])], "normal": [1.0, 0.0, 0.0], "mount": text["mount_head"]},
                    {"id": "site-tail", "position_um": [um(sx_face), um(AX[0]), um(AX[1])], "normal": [-1.0, 0.0, 0.0], "mount": text["mount_tail"]}],
                "chain": {"head_site": "site-head", "tail_site": "site-tail", "rest_orientation": QI, "mating_roll_deg": [0]},
                "retention": text["retention"],
                "alignment": text["alignment"],
                "limitations": text["limitations"]}
        path = os.path.join(here, "..", "declaration.json")
        with open(path, "w") as f:
            json.dump(decl, f, indent=2)
            f.write("\n")
        print("wrote", os.path.normpath(path))
