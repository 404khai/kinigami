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
import rear_drive as rear


ACCESSED = "2026-11-20"
DECLARED = "2026-11-20"

# ---------------------------------------------------------------- sources
SRC = {
    "pa": ("datasheet", "https://www.materialise.com/en/industrial/3d-printing-materials/pa12-sls",
           "Materialise PA12 (SLS) datasheet table: density 0.95 g/cm3, tensile strength 48 MPa (DIN EN ISO 527), tensile modulus 1650 MPa; same page gives the SLS tolerance used in Q68"),
    "ph": ("datasheet", "https://www.atimaterials.com/Products/Documents/datasheets/stainless-specialty-steel/precipitationhardening/ati_17-4_tds_en_v2.pdf",
           "ATI 17-4 H900 density 7.81 g/cm3, p3; H900 bar 170 ksi minimum proof: https://ssa-corp.com/documents/Data%20Sheet%2017-4-Stainless-Steel-AMS-5643-UNSS17400.pdf"),
    "ss": ("datasheet", "https://www.atimaterials.com/Products/Documents/datasheets/stainless-specialty-steel/austenitic/ati_302_304_304l_305_tds_en1_v1.pdf",
           "ATI 302/304/304L/305 technical data sheet (304 density 7.90 g/cm3, yield 205 MPa, UTS 515 MPa); size tolerances ISO 286 IT grades https://en.wikipedia.org/wiki/IT_Grade"),
    "br": ("datasheet", "https://www.concast.com/c95400.php",
           "Wieland Concast C95400 aluminum bronze: density 7.45 g/cm3, yield 221 MPa min (ASTM B505), modulus of elasticity 107 GPa, machinability 60, uses include nuts, bushings and worm gears"),
    "res": ("datasheet", "https://docs.rs-online.com/2f2f/0900766b816c69e9.pdf",
            "Vishay D/CRCW e3 thick film chip resistors (document 20035): CRCW0402 weight 0.65 mg, 1.0 x 0.5 x 0.35 mm"),
    "servo": ("datasheet", "https://www.feetech.cn/Data/feetechrc/upload/file/20260622/6391771882565263995959110.pdf",
              "FEETECH SCS0037-C001 A/0 pp3,4,6: 4.8..6 V; stall 0.5/0.8 A +/-10%, rated 0.50/0.60 kgf cm, stall 1.5/1.8 kgf cm; 6.1 +/-0.5 g; 28T/diam 3.9, M1.7x3.5; unmarked drawing tol +/-0.3 mm."),
    "boost": ("datasheet", "https://www.ti.com/lit/ds/symlink/tps61022.pdf",
              "TI TPS61022 rev D pp1,5,13-22: true disconnect, 6.5 A minimum valley limit, 0.585..0.615 V PWM reference; custom PCB with 1 uH inductor, input/output ceramics and true EN; power is conversion loss only."),
    "cell": ("publication", "https://www.fabtolab.com/lipo-3.7v-1S",
             "Fab.to.Lab retailer table, row 4 item 30545985163500: bare 1S 240 mAh, 30C CONTINUOUS, 30 x 20 x 5 mm, 5.8 g, no JST; not an OEM tolerance, protection or aging specification"),
    "mcu": ("datasheet", "https://www.adafruit.com/product/5405",
            "Adafruit QT Py ESP32-C3 product page (22.0 x 17.8 x 5.7 mm, 2.1 g, 600 mA peak 3.3 V regulator)"),
    "drv": ("datasheet", "https://www.pololu.com/product/2135/specs",
            "Pololu DRV8835 dual carrier specs (0.4 x 0.7 in, 0.5 g, 1.2 A continuous, 1.5 A peak); profile height 1.8 mm from https://www.pololu.com/file/0J1536/drv8835-dual-motor-driver-carrier-dimensions.pdf; quiescent from TI DRV8835 datasheet https://www.ti.com/lit/ds/symlink/drv8835.pdf (IVM 2000 uA max + IVCC 2000 uA max = 4 mA x 3.7 V = 15 mW)"),
    "mot": ("datasheet", "https://www.precisionmicrodrives.com/datasheets/206-109-V0.pdf",
            "Precision Microdrives 206-109 6 mm planetary gearmotor 136:1: 1.2 g, body 6 dia x 18.7 mm, shaft 2 dia x 3.6 mm, 3 V rated, 3.6 V max, rated 3 mN m at 140 rpm, stall 9 mN m, start current 230 mA, typical rated-load power 215 mW"),
    "al": ("publication", "https://www.thyssenkrupp-materials.co.uk/technical-knowledge-hub/density-of-metal",
           "thyssenkrupp Materials UK Al 6061-T6 density 2700 kg/m3, modulus 69 GPa"),
    "scr": ("datasheet", "https://www.westfieldfasteners.co.uk/A2-ScrewBolt-PhilCsk-M.html",
            "Westfield A2 Phillips CSK DIN 965 M1.6 x 2, 3, 4 stock; cut, deburr and measure after machining. 304 density 7.90 g/cm3 from ATI (A2 approximation). Mass uses cylindrical upper envelopes, not nominal pan-head substitutions."),
    "cu": ("datasheet", "https://aurubis.com/dam/jcr:ec116d17-1541-419a-a897-ad31b4fa6c93/c11000-cu-etp-us.pdf",
           "Aurubis C11000 density 8.9 g/cm3; wire dimensions from https://www.digikey.ca/en/products/detail/alpha-wire/2841-7-YL001/3708252 (distributor page of manufacturer data)"),
}
RHO = {"ph": 7810., "pa": 950.0, "ss": 7900.0, "br": 7450.0, "scr": 7900.0, "cu": 8900.0, "al": 2700.0, "ptfe": 2150.0}

# ---------------------------------------------------------------- geometry (mm)
YO, ZO = 12.7, 12.0          # outer half width (y) and half height (z)
T = 1.2                      # shell wall (PA12 SLS, >= 1.0 mm rule, Q68)
YI, ZI = YO - T, ZO - T
LX0, LX1 = 1.8, 35.6         # long segment (head) outer x
SX0, SX1 = -10.6, -1.8
INSET_Y, INSET_Z = 11.9, 11.2   # end plates inset 0.8 mm (rounded end edges)
LXE, SXE = LX1 - T, SX0 + T     # inner faces of the end plates       # short segment (tail) outer x
AX = (0.6, -4.6)             # installed servo axis, shared by head and tail

# Q99: head-end section and terminal flange; the mating datum is independent
# of the last keeper face. Dimensions shared with the mechanical calculations.
HX = rear.HEAD_PITCH
FLG_R, LOBE_R = rear.FLANGE_R, 9.7
SCREW_Y, SCREW_Z = 7.8, 4.2
CART_R = 6.45
FL_R = rear.TAIL_R
sx_face = rear.TAIL_PITCH

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
    add(cid, "structure", desc + " (PA12 SLS; walls other than the lids are one SLS part per segment; mass = slab volume x density)", box_from_bounds(x0, x1, y0, y1, z0, z1), mat="pa", volume_mm3=v)

# Keyed flush 304 inlays, clinched into machined SLS frames. Stock outside
# openings remains 1.2 mm: no tensile credit for a thin PA12 web.
def insert(cid, desc, x0, x1, y0, y1, top, thickness):
    zl, zh = (ZO-thickness, ZO) if top else (-ZO, -ZO+thickness)
    # Turned-up embedded 0.6 mm return at perimeter riveted through mould keys.
    v = ((x1-x0)*(y1-y0) + 2*0.6*(x1-x0+y1-y0))*thickness
    add(cid, "structure", desc, box_from_bounds(x0,x1,y0,y1,zl,zh), mat="ss", volume_mm3=v)

def inset_panel(cid, x0, x1, y0, y1, top, thickness, desc):
    zl,zh = (ZI,ZO) if top else (-ZO,-ZI)
    insert(cid,desc,x0,x1,y0,y1,top,thickness)
    for sign, a, b in (("n",-YO,y0),("p",y1,YO)):
        if b>a:
            slab(cid+"-rail-"+sign,"PA12 frame locked to perforated inlay edge",x0,x1,a,b,zl,zh)

inset_panel("L-top",LX0,22.7,-4.95,6.15,True,0.22,"Flush 304 head lid skin above trimmed case and cassette; PA12 frame outside opening.")
slab("L-top-front","PA12 head lid forward of servo",22.7,LXE,-YO,YO,ZI,ZO)
inset_panel("L-bottom",LX0,11.2,-4.2,11.5,False,0.22,"Flush keyed floor pan under swept sector and pinion.")
slab("L-bottom-mid","Intact 1.2 mm PA12 floor bolted to cassette sole",11.2,23.0,-YO,YO,-ZO,-ZI)
inset_panel("L-bottom-front",23.0,LXE,-5.9,7.1,False,0.28,"Flush keyed 304 pan under the rotor and front window.")
slab("L-side-p","Head +y side, motor collar locally relieved", LX0, LXE, YI, YO, -ZI, ZI)
slab("L-side-n","Head -y side", LX0, LXE, -YO, -YI, -ZI, ZI)
slab("L-inner","Hinge-facing wall negative side of servo pocket",LX0,LX0+T,-YI,-4.20,-10.0,ZI)
slab("L-inner-up-p","Hinge-facing wall positive side of servo pocket; upper/lower steel ear legs on outer face, tapped from inside",LX0,LX0+T,5.40,YI,-10.0,ZI)
# front wall with a window for the cartridge lip
wy0, wy1 = AX[0] - CART_R, AX[0] + CART_R
wz0, wz1 = AX[1] - CART_R, AX[1] + CART_R
fx0, fx1 = LX1 - T, LX1
slab("L-front-n", "head front wall, -y of the cartridge window", fx0, fx1, -INSET_Y, wy0, -INSET_Z, INSET_Z)
slab("L-front-p", "head front wall, +y of the cartridge window", fx0, fx1, wy1, INSET_Y, -INSET_Z, INSET_Z)
# Open down to the inset edge: do not count a 0.15 mm PA12 ligament.
# Side pillars and the full top bridge mount the flange, not a thin sill.
slab("L-front-hi", "head front wall above the cartridge window", fx0, fx1, wy0, wy1, wz1, INSET_Z)
# short (tail) segment shell
slab("S-top", "tail segment top lid, a separate part screwed on last; carries no declared load", SXE, SX1, -YO, YO, ZI, ZO)
inset_panel("S-bottom",SXE,SX1,-7.5,8.9,False,0.25,"Keyed steel pan under tail lower hinge foot and sector web; captive dimpled CSK seats at two fixing points.")
slab("S-side-p", "tail segment +y side wall", SXE, SX1, YI, YO, -ZI, ZI)
slab("S-side-n", "tail segment -y side wall", SXE, SX1, -YO, -YI, -ZI, ZI)
slab("S-inner", "tail segment inner end wall facing the hinge gap (floor slot to z -10.0 for the lower hinge plate)", SX1 - T, SX1, -YI, YI, -10.0, ZI)
slab("S-end", "tail segment end plate carrying the station flange (inset 0.8 mm at its edges)", SX0, SXE, -INSET_Y, INSET_Y, -INSET_Z, INSET_Z)

# electronics
add("cell", "energy_source", "Fab.to.Lab 30545985163500 bare 240 mAh 1S along -y wall; 3.7 V x 0.240 Ah x 3600; 30C continuous = 7.2 A retail rating. Screen delivered, insulated, untensioned cell incl tab folds against this enlarged 30.65 x 5.4 x 20.7 allocation; do not compress or trim pouch.",
    box_from_bounds(3.025, 33.675, -11.4, -6.0, -10.35, 10.35), mass_mg=5800, src="cell",
    extra={"nominal_voltage_v": 3.7, "rated_continuous_discharge_a": 7.2, "energy_mj": 3196800})
add("controller", "controller", "Adafruit QT Py ESP32-C3 (5405), 22 x 17.8 x 5.7 mm headerless across tail. BAT/GND input. Budget 0.600 A x 4.2 V from cell at both peak and average, including board regulator. No USB while installed.",
    box_from_bounds(-9.25, -3.55, -11.0, 11.0, -8.9, 8.9), mass_mg=2100, src="mcu", dim_basis="source", peak=2520, avg=2520)
add("driver", "other", "Headerless DRV8835 carrier drives joint ONLY; other channel disabled. Budget 4 mA x 4.2 V quiescent rounded up; joint input accounted separately.",
    box_from_bounds(11.85, 22.05, 9.35, 11.15, -8.9, 8.9), mass_mg=500, src="drv", dim_basis="source", peak=17, avg=17)
servo_pk = math.ceil(5.2 * 880)
loss_pk = math.ceil(servo_pk * (1 / 0.80 - 1) + 4.2 * 3)
# Gross upper masses by part envelopes: FR4+copper PCB at 3.2 g/cc,
# inductor/passives at 8.9 g/cc; no fictitious full-solid board block.
pcb_v = 15.5*10.6*0.8
coil_v = 5.3*5.5*3.1  # XEL5030-102MEC, TI Table 8-2
parts_v = 2*2*1.0 + 7*3.2*1.6*1.8 + 7.0
elec_v = pcb_v + parts_v + coil_v
# Coilcraft XEL5030 series max 0.58 g. Copper-density bound for other parts.
elec_rho = (3200*pcb_v + 8900*parts_v + 580000) / elec_v
add("servo-boost", "other", "TI TPS61022, custom 4-layer headerless PCB above rear drive; fitted 1 uH shielded power inductor, effective input >=10uF and output >=40uF, EN pulldown and forced PWM; nominal rail 5.02 V, full-load transient screen 4.80..5.20 at actual servo. 80% provisional loss floor, 3 mA extra, no typical efficiency guarantee. PCB gross mass at 3200 kg/m3, component envelopes at copper density. No USB back-power.",
    box_from_bounds(23.1,33.7,-5.35,10.15,2.3,6.55), mass_mg=round(elec_v*elec_rho/1000), src="boost", mass_basis="derived", peak=loss_pk, avg=loss_pk,
    extra={"derivation":{"density_kg_m3":elec_rho,"volume_m3":elec_v*1e-9}})
# A tiny headerless single-sided daughterboard over the controller edge.
comps[-1]["source"]["title"] += " Coilcraft XEL5030-102MEC at 0.58 g series upper: https://www.coilcraft.com/getmedia/38f73356-5dfa-4ba3-b406-5d8b038c37d2/xel5030.pdf ; effective COUT 40..50 uF at bias, include feedforward capacitor (TI 8.2.2.4)."
# Copper-density full solid bounds the laminate, solder, silicon and components.
add("ttl-interface", "other", "7.5 x 4.5 x 1.5 mm flex/circuit over board edge, IO on 3.3 V. TI SN74LVC2G125 (YZP) TX with 10k /OE pullup, RX always enabled; 100nF local bypass, 4.7k boost EN pulldown. Disabled TX and RX input tolerate 5.5 V per https://www.ti.com/lit/ds/symlink/sn74lvc2g125.pdf . Peak/avg allocation 10 mW incl pull resistors and switching; mass upper uses full 0.20 mm flex laminate, IC 2.4 x 1.4 x 0.8, 3 mm3 passives + 5 mm3 solder at copper density.",
    box_from_bounds(-8.75, -4.25, -7.95, -0.45, 9.0, 10.5), mat="cu", volume_mm3=7.5*4.5*0.20 + 2.4*1.4*0.8 + 3 + 5, peak=10, avg=10)

# coupler drive
add("coupler-servo", "actuator", "FEETECH SCS0037-C001 with long side +z. Drawing p6 tip-to-back 23.3, static axial cap 20.2, base height 17.4, spline 3.1 proud. Both tab ends trimmed OUTSIDE sealed case; retain 0.8 minimum short-ear key beyond short body edge at clevis. Source unmarked tolerance +/-0.3. Case incl lead exit is acceptance-gauged inside declared box; tip x25.35 +/-0.025 y+0.60 z-4.60. Spline in hub and short tab in trapped sole recess not boxed twice. Charge full untrimmed max 6.6 g. Rated 49.03 N mm at 4.8 V, not stall. 5.2 V x 0.88 A conservative peak/average allocation.",
    box_from_bounds(1.70,22.58,-4.10,5.30,-9.83,11.43), mass_mg=6600, src="servo", peak=servo_pk, avg=servo_pk)
# Each coaxial mechanism is an installed assembly within its allocation.
# Individual stationary/moving sections and material stock are in rear_drive.
def assembly(cid,desc,x0,x1,yr,zr,items):
    vol=sum(v for _,v,density in items)
    mass=sum(v*density/1000 for _,v,density in items)
    add(cid,"coupler_mechanism",desc+" Gross stock, mm3: "+", ".join(
        f"{name} {v:.3f}" for name,v,density in items),
        box_from_bounds(x0,x1,AX[0]-yr,AX[0]+yr,AX[1]-zr,AX[1]+zr),
        src="ph", mass_mg=math.ceil(mass),mass_basis="derived",
        extra={"derivation":{"density_kg_m3":1000*mass/vol,"volume_m3":vol*1e-9}})
    comps[-1]["source"]["title"] += "; also "+SRC["ss"][1]+" (304), "+SRC["br"][1]+" (bronze); "+rear.BALL_SOURCE+" (52100). See dossier-v7 and rear_drive.py for separated material volumes and other sources."

assembly("drive-socket","Gauged 28T keyed and screwed servo hub, with axial float to independently supported cam rotor.",
    22.58,rear.SPLIT_X,2.85,2.85,rear.stock("hub"))
assembly("head-cartridge","Q99 rotary cams, guides, mechanical stops, fixed cheeks, three keeper linkages and positively driven stripper; not a V clamp or a preload screw.",
    rear.SPLIT_X,LX1,6.30,6.30,rear.stock("cartridge"))
lobe_w, lobe_y0=3.8,4.5
assembly("head-flange","Front keeper guides and steel plate on two staggered screw ears. Tool and motion details in the section study.",
    LX1,rear.NOSE_X,LOBE_R,FLG_R,rear.stock("flange"))
for nm,sgn in (("nut-block-up",1),("nut-block-low",-1)):
    yc,zc=AX[0]+sgn*SCREW_Y,AX[1]+sgn*SCREW_Z
    add(nm,"coupler_mechanism","304 tapped M1.6 nut 2.2 square x 0.8, 0.15 recessed in front wall side pier, 0.65 boxed behind. Screw takes pullout through captive square nut bearing on pier.",
        box_from_bounds(LXE-.65,LXE,yc-1.1,yc+1.1,zc-1.1,zc+1.1),mat="ss",volume_mm3=(2.2**2-math.pi*.6**2)*.8)
assembly("tail-stations","Three radially carried, hard metal crowned members at 120 degrees. Eccentric stems leave the opposed axial and tangential poles free. No central preload or long pilot.",
    rear.TAIL_MIN,SX0,FL_R,FL_R,rear.stock("tail"))

# Thin, closed, welded 304 cassette. Top tie closes the cheek reaction;
# lower blade positively traps the ear in x, not an ABS friction clamp.
add("servo-cradle","structure","Tapped 304 sole 7 x 11 x 0.85 with an end-open channel for short ear, one integral stop and one 1.0 x 5 x 1.1 keyed gate inserted from underneath after sliding servo into cassette. Floor then traps gate without adhesive. Lower tab cropped to z-10.65, at least 0.8 of land beyond case. Two M1.6 floor screws; no Al taps, old nuts or keeper screw.",
    box_from_bounds(11.9,18.9,-4.90,6.10,-10.80,-9.95),mat="ss",volume_mm3=7*11*.85+2*1.0*5*1.1)
for side, yl, yh in (("n",-4.90,-4.10),("p",5.30,6.10)):
    add("servo-cheek-"+side,"structure","7 x 0.80 x 21.43 sheet 304 cassette side, lower edge welded to sole, upper edge welded to tie. Two fitted antirotation pad lands at least 7 x 2; swaged lips trap finished Al shims inside case allocation. No ear friction credit; mass includes shims.",
        box_from_bounds(11.9,18.9,yl,yh,-9.95,11.46), mat="ss",volume_mm3=7*.8*21.41+2*7*2*1.2*2700/7900)
add("cassette-tie","structure","Welded 0.24 x 7 top tie across both cheeks, preassembled outside shell; slip case AXIALLY through fitted collar before inserting separate floor-captive axial gate. Fit screen loaded case rotation at declared fault.",
    box_from_bounds(11.9,18.9,-4.90,6.10,11.46,11.70),mat="ss",volume_mm3=7*11*.24)
# Side braces react a horizontal couple without crediting floor rigidity.
for nm,zc in (("upper",9.82),("lower",-9.82)):
    add("cradle-brace-"+nm,"structure","Welded 304 4.0 x 1.60 side strap from positive cheek to side wall, tapped M1 along y from outside. Driver enters along x between braces before lowering cassette.",
        box_from_bounds(13.4,17.4,6.10,YI,zc-.80,zc+.80),mat="ss",volume_mm3=4*1.60*(YI-6.10))
for i, zc in enumerate((9.2, 9.75)):
    add("vsense-r%d" % (i+1), "sensor", "100 kOhm CRCW0402 divider on insulated leads beside tail logic board. Monitor loaded cell, inhibit motion below commissioned rail threshold. 4.2 V squared / 200 kOhm = 0.09 mW total; book 1 mW each.",
        box_from_bounds(-6.5, -5.5, -0.25, 0.25, zc - 0.175, zc + 0.175), mass_mg=1, src="res", dim_basis="source", peak=1, avg=1, power_basis="derived")

# joint drive (vertical axis through the pivot at x = 0, y = 0)
jx, jy = JM
ang = math.degrees(math.atan2(jy, jx))
add("joint-motor", "actuator", "Precision Microdrives 206-109 gearmotor for the body joint, axis vertical at (x, y) = (%.2f, %.2f), body z -9.85 to 8.85, shaft down, cut to 1.8 mm; provisional upper electrical allocation 230 mA at 3 V scaled linearly to a 4.2 V pulse: 1353 mW, average 215 mW rated; limit effective drive to 3.0 V. Box enlarged for clamp except 0.09 mm band relieved into +y wall" % (jx, jy),
    box_from_bounds(jx - 3.12, jx + 3.12, jy - 3.12, YI, -9.85, 8.85), mass_mg=1200, src="mot", peak=1353, avg=215)
# Split gearhead collar doubles as the attachment to the +y side wall.
# The loop is inside the enlarged round-motor/saddle allocation (not a
# cylinder added behind the motor); only the foot stands outside.
add("joint-clamp", "structure", "304 split clamp at z -8.4..-4.4. Bore to measured 6 mm gearhead, 0.12 wall band, two 2.4 x 1.4 x 4 tangential ears in +x aisle. One M1.6 CSK draws tapped ear toward side wall through machined PA12 stand-off, reacting joint torques in either direction. Actual arc in joint-motor box and <=0.10 mm relief in side wall; mass proxy at the tab location, not a free block. Prove couple without crushing or slipping; coefficient not manufacturer data.",
    box_from_bounds(9.35,11.75,7.2,11.5,-8.4,-4.4), mat="ss",
    volume_mm3=math.pi*(3.12**2-3.0**2)*4 + 2*2.4*1.4*4)
dirv = (math.cos(math.radians(ang)), math.sin(math.radians(ang)))
qz = q_axis((0, 0, 1), ang)
pc = (dirv[0] * (SECT_R + 1.8), dirv[1] * (SECT_R + 1.8))
pin_v = math.pi*(1.8**2-1.0**2)*1.5
add("joint-pinion", "actuator", "spur pinion m 0.3 z 12 on the joint motor shaft (z -11.65 to -10.15); box oriented toward the pivot and bounded at the pitch circle facing the sector; 304, pitch-disc minus 2 mm bore",
    obox((pc[0], pc[1], -10.90), (1.8, 1.8, 0.75), qz), mat="ss", volume_mm3=pin_v)
SPAN = 21.0  # deg each side: joint range 15 deg plus 6 deg of tooth engagement
sect_in = 4.5
sect_he_t = SECT_R * math.sin(math.radians(SPAN))
sc = ((SECT_R + sect_in) / 2 * dirv[0], (SECT_R + sect_in) / 2 * dirv[1])
v_sect = (math.radians(2 * SPAN) / 2) * (SECT_R ** 2 - sect_in ** 2) * 1.5
add("joint-sector", "structure", "toothed sector m 0.3 (pitch radius 8.7, z 58 equivalent), +-21 deg about the joint motor direction (%.1f deg), r 4.5 to 8.7, 1.5 mm thick at z -11.65 to -10.15; part of the tail segment's lower hinge plate, runs in the head segment's bottom layer through the L-inner wall slot; 304" % ang,
    obox((sc[0], sc[1], -10.90), ((SECT_R - sect_in) / 2, sect_he_t, 0.75), qz), mat="ss", volume_mm3=v_sect)
v_plate = 3.4 * 3.2 * 1.5 + math.pi * 1.6 ** 2 * 1.5 / 2 - math.pi * 1.0 ** 2 * 1.5
# The sector cannot float beyond its inner radius. Bound the complete
# one-piece lower blank in two adjacent boxes, split at u=4.5 along JM.
def uv_foot(u, v):
    return (u*dirv[0]-v*dirv[1], u*dirv[1]+v*dirv[0])
v_foot = (2.8*6.4 + 3.0*3.2 + math.pi*1.6**2/2 - math.pi*1.0**2 - 2*math.pi*0.6**2)*1.5
add("hinge-plate-low", "structure", "Tail lower 304 plate, one piece with sector via 1.4-wide radial web u=1.3..4.6. Foot x -5.8..-3.0 x 6.4 wide; neck to pin centre 3.2 wide; r1.6 boss. Two CSK M1.6 screws at x -4.4, y +/-1.8, through 0.25 steel floor and 0.1 shim; thread 1.25 into 1.5 steel, CSK finished in plate below first threads; no projecting screw tips. This OBB covers the foot, neck, web and inner arc of adjoining sector; boxes meet at u=4.5 along joint drive.",
    obox((*uv_foot(-0.8,1.9),-10.90), (5.3,4.7,0.75), qz), mat="ss", volume_mm3=v_foot + 3.3*1.4*1.5 + 2.8*6.4*0.1)
add("hinge-plate-up", "structure", "tail segment upper hinge plate (z 7.6 to 9.1) from the tail inner face to the pin, boss r 1.6; 304, volume = plate minus pin bore",
    box_from_bounds(-1.8, 1.6, -1.6, 1.6, 7.6, 9.1), mat="ss", volume_mm3=v_plate)
for nm, zl, zh, zleg0, zleg1 in (("low",-9.95,-8.45,-8.45,-4.95),("up",9.3,10.8,5.8,9.3)):
    add("hinge-ear-"+nm,"structure","304 r1.6 pin boss joined along +y by 1.05-wide strap x0.60..1.65 to exterior hinge-wall leg. Ear strap y0.8..8.9; minimum section 1.05 x 1.5. Box includes air over the circular boss; no material extends across servo pocket.",
        box_from_bounds(-1.6,1.65,-1.6,8.9,zl,zh),mat="ss",volume_mm3=(math.pi*(1.6**2-1.0**2)+1.05*8.1)*1.5)
    add("ear-"+nm+"-leg","structure","Tapped 304 leg outside the +y pier of the hinge wall, integral with offset strap, driven flush from INSIDE empty head before payload. 0.7 engagement in 0.8 leg. Fixing tool axis parallel to x; slot clearance for shaft before cassette/motor insertion.",
        box_from_bounds(1.0,1.8,5.7,8.9,zleg0,zleg1),mat="ss",volume_mm3=(3.2*3.5-math.pi*.6**2)*.8)
add("plate-up-leg", "structure", "Integral root leg of tail upper plate against the outer face of its inner wall; 3.2 x 3.4 x 0.8, tapped for a flush screw from inside empty tail.",
    box_from_bounds(SX1, SX1 + 0.8, -1.6, 1.6, 4.2, 7.6), mat="ss", volume_mm3=3.2*3.4*0.8 - math.pi*0.6**2*0.8)
v_pin = math.pi * 1.0 ** 2 * 22.45
add("hinge-pin", "structure", "hinge pin dia 2.0 x 22.45 (z -11.65 to 10.8), 304; box covers the exposed length z -8.45 to 7.6 between the ears and plates (the rest lies inside their bosses)",
    box_from_bounds(-1.0, 1.0, -1.0, 1.0, -8.45, 7.6), mat="ss", volume_mm3=v_pin)

# Removable steel nut ledges: install THROUGH the wall AFTER the payload,
# so they do not narrow the top opening during vertical insertion.
for cid, xl, yl in (("head-a",10.0,8.3), ("head-b",30.9,8.3),
                    ("head-c",31.2,-3.5), ("tail-n",-8.1,-11.5), ("tail-p",-8.1,8.3)):
    area = 3.2**2
    tab = 3.2*4.4*0.8
    vol = tab + area  # 1 mm PA12 boss on the lid; gross bound before holes
    rho = (RHO["ss"]*tab + RHO["pa"]*area) / vol
    add("lid-nut-"+cid, "structure", "Removable tapped 304 ledge (3.2 x 4.4 x 0.8) inserted laterally through a finished shell slot AFTER boards, ending flush outside. 1.2 of its 4.4 length is inside wall allocation; slot roof captures tab against lid lift. 3.2 square x 1.0 PA12 boss on lid sits on tab. Lid screw prevents transverse withdrawal. No fixed ledge blocks insertion.",
        box_from_bounds(xl,xl+3.2,yl,yl+3.2,9,10.8), mass_mg=round(rho*vol/1000), src="ss", mass_basis="derived",
        extra={"derivation":{"density_kg_m3":rho, "volume_m3":vol*1e-9}})
# Lengths in mm. CSK lengths INCLUDE head; other heads measured under head.
csk = ((2,2.55), (2,1.70), (2,1.60), (3,1.90), (2,2.00), (5,2.90), (1,5.3))
pan = ((1,1.7,3.5,3.5,1.4),)
# 90-degree CSK, <=3.2 head OD, <=0.2 cylindrical rim, full 1.6 shank.
head_cs = math.pi*(1.6**2*0.2 + 0.8*(1.6**2+1.6*0.8+0.8**2)/3)
v_scr = sum(n*(head_cs + math.pi*0.8**2*(l-1.0)) for n,l in csk)
v_scr += sum(n*math.pi*((hd/2)**2*ht + (dia/2)**2*l) for n,dia,l,hd,ht in pan)
v_scr += 2*math.pi*(.95**2*.60+.50**2*2.40)  # M1 CSK, gross head and shank
add("fasteners", "structure", "Mass proxy ONLY, in free space above rear module. DIN 965 A2 M1.6 CSK finished overall lengths: 2 x 2.55 flange to nut, 2 x 1.70 tail to blind flange, 2 x 1.60 lower hinge, 3 x 1.90 hinge legs, 2 x 2.00 cassette, 5 x 2.90 lids, 1 x 5.30 joint-clamp. M1.7 x 3.5 servo hub screw (procure, not supplied). Conical and cylindrical solid envelopes bound finished heads, no fictional screws installed here.",
    box_from_bounds(23.1,33.5,-5.7,0.5,6.65,8.95), mat="scr", volume_mm3=v_scr)
comps[-1]["description"] += " Two additional side brace screws M1 x 3 DIN 963, slot drive, 1.90 head, 0.60 head length, 1.8 nominal engagement after shell. https://microfasteners.com.au/product/m1-0-x-3mm-countersunk-head-slot-machine-screw-grade-304-stainless-steel/"
wire_length = 550
# Alpha 2841/7: OD 0.024 +/-0.002 in; conductor 0.012 nominal.
# Screen conductors <=0.35 mm OD, fill entire bundle at silver density.
v_h = math.pi*(0.026*25.4/2)**2*wire_length
v_cond = math.pi*(0.35/2)**2*wire_length
rho_wire = (v_cond*10500 + (v_h-v_cond)*2200)/v_h
add("harness", "other", "Mass proxy only, above rear drive. Up to 550 mm insulated wire; OD <=0.6604; full diam 0.35 conductor allocation at silver density 10.5 g/cm3, remainder PTFE 2.2 g/cm3. Trim servo pigtail/plug, retain full untrimmed servo mass as conservative allowance. Alpha Wire 2841/7 dimensional table; silver density https://periodic-table.rsc.org/element/47/silver ; 3M Dyneon TF 1620 typical 2.15 g/cm3 rounded up.",
    box_from_bounds(23.1,33.8,0.60,7.50,6.65,8.95), mass_mg=round(rho_wire*v_h/1000), src="cu", mass_basis="derived", extra={"derivation":{"density_kg_m3":rho_wire,"volume_m3":v_h*1e-9}})

# Tab insulation, finish-fitted nonstructural PCB/cell keepers, shrink
# sleeving and solder at splices. Populate the small proxy above the boost.
v_aux = 12*3*1.1*4 + 0.065*4*220  # four 12-mm PA12 ledges plus clear film strips
v_solder = 6.0
rho_aux = (950*158.4 + 1600*(v_aux-158.4) + 8900*v_solder)/(v_aux+v_solder)
add("pack-keepers","structure","Four 12 x 3 x 1.1 integral PA12 edge ledges/locators for cell/boards; 220 mm x 4 nonmetallic polyester tape up to 0.065 thick for cell/board retention and dielectric wrap; 6 mm3 splice solder. PA12 at source density, film at provisional 1.6 g/cm3 upper allocation and solder at copper density. Mass proxy over boost; edge ledges occupy unpopulated board edges or cell allowance, not a solid block over rear drive.",
    box_from_bounds(23.0,30.9,-5.7,11.15,9.0,10.75), mass_mg=round(rho_aux*(v_aux+v_solder)/1000), src="pa", mass_basis="derived",
    extra={"derivation":{"density_kg_m3":rho_aux,"volume_m3":(v_aux+v_solder)*1e-9}})

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

body = [prim_box("head-segment", "body", LX0, LXE, -YO, YO, -ZO, ZO),
        prim_box("head-front-plate", "body", LXE, LX1, -INSET_Y, INSET_Y, -INSET_Z, INSET_Z),
        prim_box("tail-segment", "body", SXE, SX1, -YO, YO, -ZO, ZO),
        prim_box("tail-end-plate", "body", SX0, SXE, -INSET_Y, INSET_Y, -INSET_Z, INSET_Z)]
coupler = [prim_cyl_x("tail-plate","coupler",FL_R,sx_face,SX0,*AX),
           prim_cyl_x("tail-three-stations-bound","coupler",rear.R_SITE+rear.R_BALL,
                      rear.TAIL_MIN,sx_face,*AX),
           prim_cyl_x("head-plate","coupler",6.30,LX1,rear.EAR_X,*AX),
           prim_box("head-flange-ear-p","coupler",LX1,rear.EAR_X,AX[0]+lobe_y0,AX[0]+LOBE_R,AX[1]+SCREW_Z-lobe_w/2,AX[1]+SCREW_Z+lobe_w/2),
           prim_box("head-flange-ear-n","coupler",LX1,rear.EAR_X,AX[0]-LOBE_R,AX[0]-lobe_y0,AX[1]-SCREW_Z-lobe_w/2,AX[1]-SCREW_Z+lobe_w/2)]
# Three separately clocked nose frames; no imaginary full disk under the shell.
for az in (90,210,330):
    a=math.radians(az)
    r=(1.8+7.55)/2
    coupler.append({"id":f"keeper-nose-{az}", "kind":"box","role":"coupler",
                    "half_extent_um":[um((rear.NOSE_X-LX1)/2),um((7.55-1.8)/2),2180],
                    "pose":{"position_um":[um((LX1+rear.NOSE_X)/2),um(AX[0]+r*math.cos(a)),um(AX[1]+r*math.sin(a))],
                            "orientation":q_axis((1,0,0),az)}})
cavity = [prim_box("cavity-envelope","cavity",SX0,LX1,-YO,YO,-ZO,ZO),
          prim_box("tail-stations-envelope","cavity",rear.TAIL_MIN,SX0,AX[0]-FL_R,AX[0]+FL_R,AX[1]-FL_R,AX[1]+FL_R),
          prim_box("head-flange-envelope","cavity",LX1,rear.NOSE_X,AX[0]-LOBE_R,AX[0]+LOBE_R,AX[1]-FLG_R,AX[1]+FLG_R)]

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
    cell = next(c for c in comps if c["kind"] == "energy_source")
    print("peak %d mW vs %.0f mW source" % (pk, cell["nominal_voltage_v"]*cell["rated_continuous_discharge_a"]*1000))
    for c in comps:
        print("   %-16s %6d mg" % (c["id"], c["mass_mg"]))
    return bad, out, tot, com

if __name__ == "__main__":
    bad, out, tot, com = run_checks()
    print("joint motor direction %.2f deg; pinion at %.2f, %.2f" % (ang, pc[0], pc[1]))
    if bad or out:
        raise SystemExit("package check failed; refusing to write declaration")
    if "--write" in sys.argv:
        import os
        here = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(here, "declaration_text.json")) as f:
            text = json.load(f)
        decl = {"schema_version": 1, "candidate_id": "cand-d", "candidate_version": 7, "family": "B",
                "declared_on": DECLARED, "author": text["author"], "summary": text["summary"],
                "stowed_geometry": {"primitives": body + coupler + cavity},
                "chain_geometry": {"primitives": body + coupler},
                "components": comps,
                "mass_budget": {"total_mass_mg": tot},
                "assembly_access": {"statement": text["assembly_access"]},
                "coupler_sites": [
                    {"id": "site-head", "position_um": [um(HX), um(AX[0]), um(AX[1])], "normal": [1.0, 0.0, 0.0], "mount": text["mount_head"]},
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
