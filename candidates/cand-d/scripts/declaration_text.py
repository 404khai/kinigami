#!/usr/bin/env python3
"""Writes declaration_text.json (the prose fields of the cand-d declaration, version 4).
Every number here is printed by coupler.py or joint.py; run those to reproduce it."""
import json, os
t = {}
t["author"] = "Claude Opus 5.5 (engineering lead, cand-d author)"
t["summary"] = (
    "Two-segment inline body (Family B), version 4, designed coupler-first. A long head segment (PA12 shell 33.8 x 25.4 x 24 mm) holds the cell, the coupler drive "
    "and the joint drive; a short tail segment (8.8 mm) holds the controller and carries the coupler stud. One vertical revolute joint (pin at mid-gap, 304 ears and plates, "
    "spur sector z58 driven by a 6 mm gearmotor) bends the chain in the table plane, +-15 deg working, outline contact at +-16.1 deg. The coupler is rigid and gendered: "
    "a one-piece 304 tail stud (Hirth-toothed flange, dia 4 pilot, two dia 3 lugs) enters the head cartridge: a one-piece 304 housing (front flange with a Hirth ring, lying on the front plate's outer face "
    "and screwed through it into two nut blocks, and a tube with axial lug slots) around a C93200 bronze cam sleeve whose two helical slots have a 20 deg capture stage and a 3 deg self-locking lock stage, on a PTFE thrust ring, "
    "retained by a 304 collar. A 6 mm gearmotor turns the sleeve to a 1.0 V stall, which seats the 36-tooth Hirth faces with 4.41 to 9.00 N preload; axial tolerance is absorbed by "
    "sleeve travel inside the lock stage. Torsion and shear are carried by the Hirth teeth with zero lash. No spring, no SMA, no magnet. BLE only, no power transfer. "
    "Version 4 closes the six items of retention-review-v3-r1 (Q91): every coupler and hinge joint to PA12 is a countersunk screw into 304 thread, each shell is one SLS part with a separate top lid.")
t["assembly_access"] = (
    "Each segment shell is one SLS part (bottom, two sides, end plate and inner wall) closed by a separate top lid that carries no declared load; all internal parts go in through the top. Head segment: the cell, coupler motor, joint motor, driver and hinge-ear legs are fitted from the top. The head cartridge is assembled outside the shell (PTFE ring and sleeve slid onto the housing tube from the rear, stop pin engaged, retainer collar "
    "pressed on); the cartridge is pushed through the plate window from the front until its flange lies on the plate's outer face, and two countersunk "
    "M1.6 A2 screws go through the flange lobes and the plate into the two nut blocks held behind it. Tail segment: the controller drops in from the top; the stud flange is held on the end plate's outer face by two countersunk M1.6 screws "
    "driven from inside into the flange's blind tapped holes; the lower hinge plate lies on the tail floor and is screwed from below. Hinge: the head ears' legs are screwed through the head inner wall from the gap side, the tail upper plate's leg through the tail inner wall "
    "from inside; the sector (part of the tail lower plate) is meshed with the joint pinion, then the pin is pressed through ears and plates from above. The harness passes the gap beside the pin. Not prototyped; the sequence is a paper statement.")
t["mount_head"] = "head cartridge through the head front plate window; its 304 front flange (0.8 thick) lies on the plate's outer face, Hirth pitch plane at x 36.4, held by two countersunk M1.6 screws through the flange lobes and the plate into 304 nut blocks; axis (y, z) = (3.3, 1.0)"
t["mount_tail"] = "tail stud flange (r 6.3) on the tail end plate's outer face, held by two countersunk M1.6 A2 screws from inside into blind holes of the 304 flange; Hirth pitch plane at x -11.6; same axis (3.3, 1.0)"
t["retention"] = {
    "requires_power_to_hold": False,
    "mechanism_kind": "friction_wedge",
    "mechanism": (
        "Holding principle: a self-locking cam (friction wedge). The two 304 lugs of the tail stud sit on the 3 deg lock stage of the C93200 sleeve's helical slots. Axial lug load cannot turn "
        "the sleeve while flank friction exceeds tan 3 deg = 0.0524: steel on bronze dry 0.15 to 0.23 and machine oil 0.10 to 0.16 (Wikipedia Leadscrew, raw wikitext) give 2.86x and 1.91x "
        "at the low ends; PTFE thrust friction adds holding torque that is not credited. Self-locking is friction-based and not absolute under vibration (same source). "
        "While the stage holds, the stud can move axially only by elastic deflection of the metal loop: an axial load 20 N above any preload opens the faces by at most 0.001 mm (loop stiffness "
        "lower bound 20 kN/mm, the two lugs alone 194 kN/mm), against a Hirth tooth height of 0.39 mm. So the two 36-tooth 90 deg Hirth faces (r 2.6 to 6.3, 304 on 304) stay geometrically "
        "engaged at any preload, including zero, and roll is bounded by the tooth flanks to 0.013 deg. "
        "Preload from the 1.0 V closing stall: typical 4.41 to 9.00 N dry (flank mu 0.15 to 0.23, PTFE thrust 0.05 to 0.20, mesh 0.9 to 1.0); guaranteed lower bound 0.88 N "
        "(datasheet rated load 3 mN m at 3 V and max start voltage 0.5 V give stall >= 1.2 (V - 0.5) mN m). Preload decides only whether the faces stay in contact, not retention. "
        "Tension (declared 1.220 N = 4 mu W, mu = 1): lugs on the self-locking stage; faces stay closed at typical F_p (3.61x), may gap by micrometres at the lower bound (0.72x). "
        "Torsion (declared 7.75 mN m): Hirth teeth, zero lash, independent of face friction; no tooth separation at typical F_p (2.53x). The lug slots (3.40) are wide enough that with the teeth "
        "seated the lugs keep at least 2.29 deg of clearance to the slot sides at the contact radius 3.5 and the worst tooth-to-slot phase (IT9 on both parts, +-0.88 deg), so torsion goes only through the teeth "
        "and the lugs cannot slide along the flank: the sleeve cannot be walked by torsion slip. "
        "Shear (declared 0.305 N): Hirth teeth (radial). "
        "Out-of-plane bending (declared 14.7 mN m): face tipping 27.8 mN m at typical F_p (1.89x); beyond it the pilot couple bounds tilt to 1.49 deg. In-plane bending (declared 14.5 mN m, the "
        "joint drive limit): tipping about the edge at y 5.87 (the lug slots remove 35 percent of the head ring along +-y) 25.9 mN m (1.78x); beyond it the lug pair on the self-locking stage. "
        "All declared loads at once: axial separating 3.27 N below typical F_p (1.35x); the faces gap at one edge under the combined bending. Gapping is not separation (see the elastic argument). "
        "Every load path is closed in machined metal (304 stud, one-piece 304 housing with its front flange, C93200 sleeve, PTFE ring, 304 collar). "
        "Mount to the shell: the flange (disc r 7.0, lobes at +-z to r 9.4) lies on the PA12 front plate's outer face; two countersunk M1.6 A2 screws through the lobes and the plate into 304 nut "
        "blocks. Pull-out: screws and nut blocks, 0.61 N each. In-plane bending pivots the flange on its disc edge at 7.0 mm, both screws hold: 1.65 N each (fault 4.34 N, 1.53 MPa on PA12; "
        "thread stripping about 454 N). Out-of-plane bending pivots on a lobe tip, far screw at 17.2 mm: 1.46 N. "
        "Tail stud mount: two countersunk M1.6 A2 screws from inside the end plate into blind 0.6 mm holes of the 304 flange (z +-4.6): worst 4.76 N per screw (in-plane fault), "
        "0.94 MPa on the PA12 countersink, thread stripping about 341 N; torsion 0.85 N per screw in shear, 0.44 MPa on PA12. The front plate is one SLS part with the head shell: under a "
        "nut block at the fault load it bends to 5.9 MPa (clamped plate, Roark) against 50 MPa. Hinge ears and plates are 304 with root legs screwed through PA12 into 304 thread; worst ear "
        "force 1.42 N, pin bearing 0.47 MPa. "
        "Teeth seating: if the lower-bound motor cannot tilt a unit flat (1.25 N needed at mu 0.8 against 0.88 N guaranteed), the teeth seat with up to 0.73 deg residual pitch, stay engaged by "
        "at least 0.23 mm, and the seat depth stays in the lock stage (+-0.162 against +-0.20). "
        "Axial tolerance: seat depth 3.518 to 3.681 at the IT9 / g6 corners, inside the lock stage 3.40 to 3.80 (0.118 margin each side); plate position and flushness set only the PA12 gap "
        "(0.7 mm minimum outside r 6.3). Contact stress: lug on bronze flank (2.65 mm line) Hertz p0 163 MPa at typical F_p_max, 209 MPa with all loads (225 oiled), onset about 230 (1.67 x 138)."),
    "component_ids": ["head-cartridge", "head-flange", "tail-stud", "retainer-collar", "nut-block-up", "nut-block-low", "coupler-motor", "S-end", "L-front-n", "L-front-p", "L-front-lo", "L-front-hi", "fasteners"],
    "release": {
        "bounded_independent_release": True,
        "means": (
            "The head unit's own coupler motor turns the sleeve back to the open stop (304 stop pin dia 1 in the flange's rear face at r 5.3, running in an arc groove of the sleeve face; worst "
            "stop load 7.3 N, shear 9.3 MPa, bronze bearing 14.6 MPa). Release is allowed only with the cell at 3.5 V or more, so the motor sees at least 3.4 V (DRV8835 on-resistance 305 mOhm at "
            "the 230 mA start current). Release needs at most 20.3 mN m at the sleeve (typical F_p_max 9.00 N plus all declared axial loads, flank 0.23, thrust 0.20; 19.3 oiled) against 32.9 mN m "
            "(typical 3.4 V stall x 43/12 x 0.9): margin 1.62. Closing and release use the same motor, so with the voltage-linear model the margin is independent of motor-to-motor variation; with the "
            "datasheet start-voltage offset (up to 0.5 V) the ratio of release to closing torque only rises ((3.4 - f)/(1.0 - f) for f in 0..0.5). The capture stage's outer flank pushes the stud out "
            "1.4 mm; the reaction goes into the 304 retainer collar. Release is a physical process under load and may be slow or blocked by loads beyond the declared ones (CPL-008). The tail unit cannot "
            "release this joint; each head releases its own joint.")}}
t["alignment"] = [
    {"kind": "geometric_guide",
     "description": "Lateral: 45 deg chamfers on the pilot nose (0.3) and the flange's bore mouth (0.4, from the inner land recessed 0.25 below the pitch plane), leading into the 4.10 entry bore (pilot clearance 0.050 to 0.130)",
     "justification": (
         "Presented-pose window +-0.75 mm lateral against the +-0.6 mm two-unit PA12 SLS stack. On a 45 deg chamfer an axial push gives a centring force (1 - mu)/(1 + mu) of it, 0.11 at the dry "
         "steel-steel upper bound 0.8 (Engineering ToolBox, raw page): no wedging while mu < 1. Reference planes: the head flange front face is the head Hirth pitch plane (crest +0.2, root -0.2); both inner lands "
         "are recessed 0.25, so they never touch; the chamfer runs 0.4 from the land. Sequence: when the lug fronts reach the head pitch plane (5.10 behind the stud's) the pilot's "
         "cylindrical part (from 5.90) is 0.80 past the head pitch plane, 0.15 past the end of the chamfer at 0.65, so the lugs meet their slots with at most 0.130 mm of lateral error, inside their +-0.6 mm "
         "V lead-ins. The pilot is an entry guide only; the Hirth teeth centre the seat."),
     "component_ids": ["tail-stud", "head-flange", "head-cartridge"]},
    {"kind": "geometric_guide",
     "description": "Roll, pitch and yaw: round dia 3 lugs entering 0.6 x 45 deg V lead-ins of the flange and housing slots and the sleeve notches; final roll, centring and tilt by the 36-tooth Hirth faces",
     "justification": (
         "Roll window +-5.5 deg at the lug tip radius 6.2 against about +-1.4 deg between two units on one table. Before the teeth meet, the lugs index roll within the slot lash, 3.17 to 3.46 deg at "
         "the contact radius 3.5, less than half a tooth pitch (5 deg), so the teeth always meet their own gaps and then fix roll with zero lash. Pitch between two units on one table is within "
         "+-0.73 deg (0.6 mm over 47 mm). Yaw: full pilot engagement bounds it to 1.49 deg before the teeth meet; the teeth align it under the draw. Joint angles do not enter: the head unit's head "
         "segment and the tail unit's tail segment are each rigid. The open stop puts the sleeve notches over the slots within about +-0.3 deg (IT9), inside the +-7.1 deg the V lead-in allows."),
     "component_ids": ["tail-stud", "head-flange", "head-cartridge"]},
    {"kind": "geometric_guide",
     "description": "Axial closing and seating: the 20 deg capture stage draws the stud 1.0 mm, then the 3 deg lock stage seats the Hirth faces",
     "justification": (
         "Closing force is the coupler motor's: at the 1.0 V closing stall the sleeve gives 9.68 to 10.75 mN m typical (2.0 mN m at the guaranteed lower bound), while drawing one free unit at the "
         "mu = 1 table bound needs 1.21 mN m through the capture stage. The axial push that brings the lugs to the capture stage (2.40 mm stroke, about mu W = 0.31 N plus chamfer friction) is not "
         "supplied by the candidate: it comes from the experiment's documented start configuration (Q31 item 1) or a later approach design. Tolerance is taken by sleeve travel to a stall: every "
         "corner of the axial stack seats inside the lock stage. No capture window is claimed (CPL-006)."),
     "component_ids": ["head-cartridge", "coupler-motor", "coupler-pinion", "tail-stud"]}]
t["limitations"] = [
    "Approach locomotion is not designed. The coupler engages from a presented pose (stud nose at the bore mouth within +-0.75 mm lateral, +-5.5 deg roll, yaw within the pilot's acceptance) with an external axial push of 2.40 mm. Q31 starts the chain engaged. No capture window is claimed (CPL-006).",
    "Retention is a friction wedge: self-locking needs flank mu > 0.0524. The cited lower bounds give 2.86x dry and 1.91x oiled, but self-locking is not absolute under vibration or shock (Wikipedia Leadscrew); the bending chain's vibration level is not known. Walking by torsion slip is excluded by the Hirth teeth; walking by vibration is not analysed (Gate 2/3).",
    "Preload is typical 4.41 to 9.00 N; the guaranteed lower bound from the datasheet is only 0.88 N. At that bound the faces gap by micrometres under the declared tension, torsion or bending (retention and tooth engagement do not depend on it). There is no engagement or current sensor; the controller drives for a fixed time and cannot confirm the engaged state (Q32).",
    "Friction values are handbook values, not tests of these pairs: flank steel on bronze (Wikipedia Leadscrew, raw wikitext), PTFE on steel and steel on steel (Engineering ToolBox, raw HTML). Mesh efficiency 0.9 to 1.0, bronze Poisson ratio 0.34, the 20 kN/mm loop-stiffness lower bound and the 3.4 V motor voltage under the 3.5 V cell rule are provisional.",
    "Declared loads are modelling assumptions: tension 4 mu W with mu = 1, torsion 2 W x 12.7 mm, out-of-plane bending W x 48.0 mm (site-to-site pitch), in-plane bending equal to the joint drive limit. Under all of them at once the faces gap at one edge (not a separation). Joint stall at 3.6 V (fault) gives 52.2 mN m; the lug contact then reaches Hertz 252 MPa, above the bronze first-yield onset: local indentation, not separation.",
    "The joint motor torque is limited by PWM to the rated 3 mN m (14.5 mN m at the joint). Holding a curvature unpowered is not claimed (Q31 item 6). Pushing two units sideways at a table mu of 1 would need about 30 mN m: Q31 bending adequacy is unresolved.",
    "There is no joint angle sensor. Joint position control is unresolved.",
    "All screw joints to PA12 put the thread in 304 (nut blocks, the stud flange, hinge legs and the lower plate); PA12 sees bearing only, compared with the EOS PA 2200 tensile strength 50 MPa (no compressive or bearing strength is cited). Thread engagements are short (0.6 to 0.8 mm, 0.4 to 0.5 d); the loads are a few newtons against a stripping capacity of several hundred.",
    "The Hirth rings are small (36 teeth, about 0.39 mm high, r 2.6 to 6.3; the head ring loses 33 percent to the lug slots) and need fine machining (for example wire EDM); the 0.05 mm flank contact band used for their pressure is provisional. At the guaranteed-lower-bound motor torque the teeth may seat with up to 0.73 deg residual pitch (still engaged by 0.23 mm). 304 on 304 teeth and the 304 pilot in the 304 bore can gall.",
    "Gear and pinion boxes are bounded at their pitch circles toward their mating gear; shafts and the hinge pin inside bores are boxed with the bore part; the housing tube and its front flange are one part declared as two boxes (head-cartridge and head-flange) joined at x 35.6. Shell walls are slabs; fasteners and harness are lumped boxes.",
    "The stowed diameter margin is reported by the evaluator. PA12 SLS +-0.3 mm on outer dimensions uses up to about 0.6 mm of it.",
    "Mating roll is 0 deg only (the coupler axis is off the body centre, so a 180 deg roll would stand the unit upside down).",
    "BLE only, no inter-unit data or power path through the coupler."]
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "declaration_text.json"), "w") as f:
    json.dump(t, f, indent=1)
    f.write("\n")
