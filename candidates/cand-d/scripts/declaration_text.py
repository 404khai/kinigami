#!/usr/bin/env python3
"""Writes declaration_text.json (the prose fields of the cand-d declaration, version 2).
Every number here is printed by coupler.py or joint.py; run those to reproduce it."""
import json, os
t = {}
t["author"] = "Claude Opus 5.5 (engineering lead, cand-d author)"
t["summary"] = (
    "Two-segment inline body (Family B), version 2, designed coupler-first. A long head segment (PA12 shell 33.8 x 25.4 x 24 mm) holds the cell, the coupler drive "
    "and the joint drive; a short tail segment (8.8 mm) holds the controller and carries the coupler stud. One vertical revolute joint (pin at mid-gap, 304 ears and plates, "
    "spur sector z58 driven by a 6 mm gearmotor) bends the chain in the table plane, +-15 deg working, outline contact at +-16.1 deg. The coupler is rigid and gendered: "
    "a one-piece 304 tail stud (Hirth-toothed flange, dia 4 pilot, two dia 3 lugs) enters the head cartridge, a 304 housing with a Hirth-toothed lip, axial lug slots, a stop pin "
    "and two tapped mounting ears, around a C93200 bronze cam sleeve whose two helical slots have a 20 deg capture stage and a 3 deg self-locking lock stage, on a PTFE thrust ring, "
    "retained by a 304 collar. A 6 mm gearmotor turns the sleeve to a 1.0 V stall, which seats the 36-tooth Hirth faces with 4.41 to 9.00 N preload; axial tolerance is absorbed by "
    "sleeve travel inside the lock stage. Torsion and shear are carried by the Hirth teeth with zero lash. No spring, no SMA, no magnet. BLE only, no power transfer. "
    "Version 2 closes the nine items of retention-review-v1-r1 (Q87).")
t["assembly_access"] = (
    "Each segment shell is printed as an open box closed by its end plate. Head segment: the cell slides in along x from the front; the coupler motor, joint motor and driver are "
    "fitted from the open front. The head cartridge is assembled outside the shell (sleeve and PTFE ring slid onto the housing tube from the rear, stop pin engaged, retainer collar "
    "pressed on), then inserted from inside so its lip sits in the front plate window and its two ears bear on the plate's inner face; two countersunk M1.6 A2 screws go through the "
    "plate into the ears. The front plate is screwed on last. Tail segment: the controller drops in from the open end; the end plate is screwed on, then the stud flange is screwed to "
    "the end plate from outside (2x M1.6). Hinge: the head ears are screwed to the head inner face and the tail plates to the tail inner face; the sector (part of the tail lower plate) "
    "is meshed with the joint pinion, then the pin is pressed through ears and plates from above. The harness passes the gap beside the pin. Not prototyped; the sequence is a paper statement.")
t["mount_head"] = "head cartridge in the head front plate window (r 6.45), Hirth pitch plane flush with the front plate at x 35.6, held by two tapped ears and countersunk M1.6 screws through the plate; axis (y, z) = (3.3, 1.0)"
t["mount_tail"] = "tail stud flange (r 6.3) screwed to the tail end plate, Hirth pitch plane at x -11.6; same axis (3.3, 1.0)"
t["retention"] = {
    "requires_power_to_hold": False,
    "mechanism_kind": "friction_wedge",
    "mechanism": (
        "Holding principle: a self-locking cam (friction wedge). The two 304 lugs of the tail stud sit on the 3 deg lock stage of the C93200 sleeve's helical slots. Axial lug load cannot "
        "turn the sleeve while the flank friction exceeds tan 3 deg = 0.0524: steel on bronze dry 0.15 to 0.23 and machine oil 0.10 to 0.16 (Wikipedia Leadscrew, checked in the raw "
        "wikitext) give 2.86x and 1.91x at the low ends; the PTFE thrust friction adds holding torque that is not credited. The self-locking is friction-based and not absolute under "
        "vibration (same source). The lugs are therefore axially captured and the two 36-tooth 90 deg Hirth faces (r 2.6 to 6.3, 304 on 304) are clamped with F_p = 4.41 to 9.00 N dry "
        "(5.25 to 11.35 N oiled), from a 1.0 V closing stall over flank mu, PTFE thrust mu 0.05 to 0.20 (Engineering ToolBox, raw page) and mesh efficiency 0.9 to 1.0. "
        "Tension (declared 1.220 N = 4 mu W, mu = 1): carried by the lugs on the self-locking stage; F_p_min exceeds it 3.61x, so the faces stay closed. "
        "Torsion (declared 7.75 mN m): carried by the Hirth teeth with zero lash; the axial separating force from torsion is at most 1.74 N (45 deg flanks, flank friction neglected), "
        "below F_p_min (2.53x). Roll cannot change without axial separation, which the self-locking stage resists, so the lugs never slide along the flank and the sleeve cannot be "
        "walked by torsion slip. No face friction is relied on. Beyond tooth separation the lugs bear on the 304 housing slot sides (r 2.77). "
        "Shear (declared 0.305 N): the radial Hirth teeth centre the flange (14.5x). "
        "Out-of-plane bending (declared 14.4 mN m) and in-plane bending (declared 14.5 mN m, the joint drive limit): face tipping needs F_p_min x 6.3 = 27.8 mN m (1.93x, 1.92x). "
        "All declared loads at once (an upper bound): the axial separating loads 3.27 N stay below F_p_min (1.35x), so the teeth stay seated; the residual clamp cannot hold the vector "
        "sum of both bendings (20.3 mN m), so the faces gap at one edge. Gapping is not separation: the lugs stay on the self-locking stage, the teeth on the far side stay meshed and "
        "the pilot bounds the tilt to 1.49 deg. "
        "Every load path is closed in machined metal (304 stud, 304 housing, C93200 sleeve, PTFE ring, 304 collar); PA12 carries only the mounting of the cartridge (tapped 304 ears and "
        "countersunk screws through the plate, worst screw load 1.59 N, 0.26 MPa on PA12) and of the stud flange. "
        "Axial tolerance: the seat depth spans 3.518 to 3.681 mm at the IT9 / g6 corners (lug, Hirth teeth on both parts, lip, PTFE ring and sleeve split out), inside the lock stage "
        "3.40 to 3.80 (0.118 mm margin each side). Cartridge position and plate flushness are not in this stack; they set only the PA12 plate gap (0.3 mm minimum), and the flange "
        "(r 6.3) is smaller than the lip and window (r 6.45), so it can bear only on the lip's teeth. "
        "Contact stress: lug on bronze flank (2.65 mm line), Hertz p0 163 MPa at F_p_max, 209 MPa with all declared loads at once (225 MPa oiled), against a first-yield onset of about "
        "230 MPa (1.67 x 138, rule of thumb); lug root 8.1 MPa."),
    "component_ids": ["head-cartridge", "tail-stud", "retainer-collar", "cartridge-ear-up", "cartridge-ear-low"],
    "release": {
        "bounded_independent_release": True,
        "means": (
            "The head unit's own coupler motor turns the sleeve back to the open stop (304 stop pin dia 1 at r 5.3 in an arc groove of the sleeve face; worst stop load 7.3 N, shear "
            "9.3 MPa, bronze bearing 14.6 MPa). Release is allowed only with the cell at 3.5 V or more, so the motor sees at least 3.4 V (DRV8835 on-resistance 305 mOhm at the 230 mA "
            "start current). Release torque at the worst dry corner (F_p_max 9.00 N plus all declared axial loads, flank 0.23, thrust 0.20) is 20.3 mN m at the sleeve, 19.3 mN m in "
            "the oil case, against 32.9 mN m available (3.4 V stall 10.2 mN m x 43/12 x 0.9): margins 1.62 dry and 1.70 oiled. Preload and available torque scale with the same motor "
            "constant, so the margin does not depend on motor-to-motor variation. The capture stage's outer flank pushes the stud out 1.4 mm; the reaction goes into the 304 retainer "
            "collar. Release is a physical process under load and may be slow, or blocked by loads beyond the declared ones (CPL-008). The tail unit cannot release this joint; each "
            "head releases its own joint.")}}
t["alignment"] = [
    {"kind": "geometric_guide",
     "description": "Lateral: 45 deg chamfers on the pilot nose (0.5) and the housing bore mouth (0.6), leading into the 4.10 entry bore (pilot clearance 0.050 to 0.130)",
     "justification": (
         "Presented-pose window +-1.15 mm lateral against the +-0.6 mm two-unit PA12 SLS stack (+-0.3 per feature). On a 45 deg chamfer an axial push gives a centring force "
         "(1 - mu)/(1 + mu) of it, 0.11 at the dry steel-steel upper bound 0.8 (Engineering ToolBox, raw page), so the 304 pilot centres on the 304 chamfer without wedging (mu < 1). "
         "Sequence: when the lug fronts reach the lip (5.10 behind the pitch plane), the pilot's cylindrical part (from 5.70) is 0.60 into the bore, exactly the end of the bore chamfer, "
         "so the lugs meet their slots with at most 0.130 mm of lateral error, inside their +-0.6 mm V lead-ins. The pilot is an entry guide only; the Hirth teeth centre the seat."),
     "component_ids": ["tail-stud", "head-cartridge"]},
    {"kind": "geometric_guide",
     "description": "Roll, pitch and yaw: round dia 3 lugs entering 0.6 x 45 deg V lead-ins of the lip slots and sleeve notches; final roll, centring and tilt by the 36-tooth Hirth faces",
     "justification": (
         "Roll window +-5.5 deg at the lug tip radius 6.2, against about +-1.4 deg between two units on one table (0.6 mm base flatness over 25 mm); the round lug on a 45 deg flank turns "
         "the tail unit under the axial push. In the slots the lugs index roll within 0.38 to 0.75 deg, far inside half a tooth pitch (5 deg), so the Hirth teeth always meet their own gaps "
         "and then fix roll with zero lash under preload. Pitch between two units on one table is within +-0.73 deg (0.6 mm over 47 mm). Yaw: full pilot engagement bounds it to "
         "1.49 deg before the teeth meet; the teeth align it under the draw. Joint angles do not enter: the head unit's head segment and the tail unit's tail segment are each rigid, "
         "so a joint angle error moves the far segments, not the coupler pose. The open stop puts the sleeve's entry notches over the housing slots within about +-0.3 deg (IT9), "
         "inside the +-7.1 deg the V lead-in allows at the flank radius."),
     "component_ids": ["tail-stud", "head-cartridge"]},
    {"kind": "geometric_guide",
     "description": "Axial closing and seating: the 20 deg capture stage draws the stud 1.0 mm, then the 3 deg lock stage seats the Hirth faces",
     "justification": (
         "Closing force is the coupler motor's: at the 1.0 V closing stall the sleeve gives 9.68 to 10.75 mN m, while drawing one free unit at the mu = 1 table bound needs 1.21 mN m "
         "through the capture stage. The axial push that brings the lugs to the capture stage (2.40 mm stroke, about mu W = 0.31 N plus chamfer friction) is not supplied by the "
         "candidate: it comes from the experiment's documented start configuration (Q31 item 1) or a later approach design. Tolerance is taken by sleeve travel to a stall, not by a fixed "
         "stroke: every corner of the axial stack seats inside the lock stage. No capture window is claimed (CPL-006)."),
     "component_ids": ["head-cartridge", "coupler-motor", "coupler-pinion", "tail-stud"]}]
t["limitations"] = [
    "Approach locomotion is not designed. The coupler engages from a presented pose (stud nose at the bore mouth within +-1.15 mm lateral, +-5.5 deg roll, yaw within the pilot's acceptance) with an external axial push of 2.40 mm. How a free unit reaches that pose is a Gate 2 question; Q31 starts the chain engaged. No capture window is claimed (CPL-006).",
    "Retention is a friction wedge: self-locking needs flank mu > 0.0524. The cited lower bounds give 2.86x dry and 1.91x oiled, but self-locking is not absolute under vibration or shock (Wikipedia Leadscrew); the bending chain's vibration level is not known. Torsion is kept from causing flank slip by the Hirth teeth, so walking by torsion slip is excluded; walking by vibration is not analysed.",
    "Closing preload is set by a voltage-limited stall (1.0 V average by PWM of the measured cell voltage) and scales with the actual motor constant; the datasheet gives typical values only. Retention, torsion and the release margin do not depend on it; the tooth-separation and tipping ratios do (2.53 and 1.93 at typical).",
    "There is no engagement or current sensor; the controller drives for a fixed time and cannot confirm the engaged state (Q32).",
    "Friction values are handbook values, not tests of these pairs: flank steel on bronze (Wikipedia Leadscrew, raw wikitext), PTFE on steel and steel on steel (Engineering ToolBox, raw HTML). Mesh efficiency 0.9 to 1.0 (KHK cites 0.98 to 0.995 for spur gears), bronze Poisson ratio 0.34 and the 3.4 V motor voltage under the 3.5 V cell rule are provisional.",
    "Declared loads are modelling assumptions: tension 4 mu W with mu = 1, torsion 2 W x 12.7 mm, out-of-plane bending W x 47.2 mm, in-plane bending equal to the joint drive limit. Under all of them at once the faces gap at one edge (not a separation). Joint stall at 3.6 V (fault) gives 52.2 mN m; the lug contact then reaches Hertz 252 MPa, above the bronze first-yield onset: local indentation, not separation.",
    "The joint motor torque is limited by PWM to the rated 3 mN m (14.5 mN m at the joint). Holding a curvature unpowered is not claimed (Q31 item 6). Pushing two units sideways at a table mu of 1 would need about 30 mN m: Q31 bending adequacy is unresolved.",
    "There is no joint angle sensor. Joint position control is unresolved.",
    "Stud flange mounting (two M1.6 into the PA12 end plate) is sized only by bearing pressure; screw pull-out in PA12 is not cited. The cartridge screws thread into 304 ears and bear on the PA12 plate under their heads.",
    "The Hirth ring is small (36 teeth, about 0.39 mm high, r 2.6 to 6.3) and needs fine machining (for example wire EDM); the flank contact band (0.05 mm) used for its pressure is provisional. 304 on 304 teeth and the 304 pilot in the 304 bore can gall under repeated cycles.",
    "Gear and pinion boxes are bounded at their pitch circles toward their mating gear (teeth cross the pitch line by design); shafts and the hinge pin inside bores are boxed with the bore part; the cartridge ears are part of the housing but boxed separately. Shell walls are slabs; fasteners and harness are lumped boxes.",
    "The stowed diameter margin is about 1.1 mm. PA12 SLS +-0.3 mm on outer dimensions uses up to about 0.6 mm of it.",
    "Mating roll is 0 deg only (the coupler axis is off the body centre, so a 180 deg roll would stand the unit upside down).",
    "BLE only, no inter-unit data or power path through the coupler."]
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "declaration_text.json"), "w") as f:
    json.dump(t, f, indent=1)
    f.write("\n")
