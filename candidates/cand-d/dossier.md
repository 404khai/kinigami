# Candidate D (`cand-d`), version 1: two-segment inline body, coupler-first

Family B (Q62 §3): an elongated two-segment body with one internal revolute joint and couplers at the segment ends. Started by Q85.

| Field | Value |
| --- | --- |
| Result label | `exploratory` (paper gate, Q38/Q40). Nothing here is validated |
| Declaration | `candidates/cand-d/declaration.json`, SHA-256 `4b6788a544f6a4226d7bcf0e8951fbf789e44b6c67cbf2ae2eb312ff31bbf64a` at the time of writing. Any edit changes the hash and invalidates the reviews |
| Author | Claude Opus 5.5 (engineering lead). Not a reviewer |
| Declared | 2026-11-20. All source access dates are 2026-11-20 |
| Criteria | `criteria/gates/gate1-v1.json` (sha `ffe13533…`), protocol revision 2 |
| Reproduce | `python3 candidates/cand-d/scripts/declaration_text.py && python3 candidates/cand-d/scripts/gen_declaration.py --write`; numbers from `coupler.py` and `joint.py` (see `scripts/README.md`) |

All dimensions are in millimetres here and in integer micrometres in the declaration. Body frame: x along the chain (head at +x), z up (the unit rests on z = -12), origin on the joint axis.

## 1. Why this candidate (lessons from cand-a, Q83, Q84)

cand-a's nine coupler attempts failed for one reason. Its coupler also did chain bending (a yaw turntable) and docking by roll-in, and its tolerance stack ran through PA12 parts into a fixed-stroke lock. cand-d separates the functions:

1. **Chain bending is in the body joint**, so the coupler is rigid.
2. **The coupler's preload loop is all machined metal.** It runs 304 stud, 304 housing lip, PTFE ring, C93200 sleeve, 304 lugs. PA12 carries only mounting loads.
3. **Tolerance is taken by travel to a torque stop.** A cam sleeve turns until its motor stalls at a set voltage. The seat lands anywhere inside a self-locking lock stage that is longer than the whole axial stack.
4. **Every declared load has a named carrier at every tolerance and friction corner** (§5).
5. **No SMA, no spring-closed latch, no magnet, no over-centre crank** (the CONRO, PolyBot, A1 and Roombots principles; Q83 §2 item 5).

## 2. Geometry

| Item | Extent |
| --- | --- |
| Head segment (PA12 shell, wall 1.2) | x 1.8 to 35.6, y ±12.7, z ±12; front plate x 34.4 to 35.6 inset to y ±11.9, z ±11.2 |
| Tail segment | x -10.6 to -1.8, y ±12.7, z ±12; end plate x -10.6 to -9.4 inset as above |
| Hinge gap | x -1.8 to 1.8; pin dia 2 at the origin, vertical |
| Coupler axis | (y, z) = (3.3, 1.0) on both ends |
| Head coupler face | x 35.6 (cartridge flush with the front plate) |
| Tail coupler face | stud flange face x -11.6 (flange 1.0 on the end plate); pilot to x -17.8 |
| Site-to-site pitch | 47.2 |

Stowed = straight (joint 0). **Registered evaluator, draft:** stowed diameter **58.862 mm** (Welzl centre x 11.12), margin 1.14 mm. G2: 496 pairs, no interference, every box inside a cavity primitive. G5: a three-unit chain is supported at roll 0. Mass 30.247 g (W = 0.2966 N). Peak 3937 mW against 19 425 mW.

### 2.1 Layout

Head segment (inner x 3.0 to 34.4, y ±11.5, z ±10.8):
- **Cell:** stands on edge along the -y wall, x 3.3 to 34.3, y -11.5 to -4.0, z ±10.
- **Head cartridge:** at the front, x 28.0 to 35.6, ±6.45 about the axis.
- **Coupler motor:** axis along x at (3.3, -7.25) below the cartridge, body x 9.3 to 28.0. Its pinion meshes the sleeve gear.
- **Joint motor:** vertical at (6.2, 8.47) behind the inner wall.
- **Driver:** stands on the +y wall.

Tail segment: the controller stands across it, x -9.3 to -3.6.

### 2.2 Joint

| Quantity | Value | Source |
| --- | --- | --- |
| Drive | 206-109 + pinion z12 m0.3 on a sector z58 (pitch r 8.7) fixed to the tail lower plate; ratio 4.83 | design, `joint.py` |
| Working range | ±15 deg; the outline (inner face corners) first touches at ±16.13 deg | `joint.py` (analytic and swept) |
| Sector sweep | 17.8 to 89.8 deg in the head frame, r ≤ 9.0; 0.73 mm clear of the coupler motor, y ≥ 1.38 (cell at y ≤ -3.8) | `joint.py` |
| Bosses | r 1.6 against the opposite inner face at 1.8 from the pivot: 0.2 mm at every angle | design |
| Torque at the drive limit (PWM to the rated 3 mN m) | 14.5 mN m (η = 1 bound); stall at 3.6 V 52.2 mN m (fault) | datasheet × ratio |
| Unpowered hold | not claimed (Q31 item 6) | |

Chain bending (Q31) uses the joint. A chain of five has four joints, so ±60 deg of total turning. Bending adequacy is **unresolved**. Pushing two units sideways needs 8.7 mN m at a table μ of 0.3 (provisional) and about 29 mN m at μ = 1. There is no joint angle sensor (limitation).

## 3. Components

All entries are in the declaration with their sources (accessed 2026-11-20). Shell walls are slabs (PA12, derived mass). The cartridge mass uses an effective density from three cited densities (304, C93200, PTFE), stated in its description.

| id | kind | mass mg | basis | peak mW | source |
| --- | --- | ---: | --- | ---: | --- |
| L-top | structure | 924 | derived | 0 | https://3dprinting.com/wp-content/uploads/2019/05/EOS-pa2200-white-datasheet-TDS.pdf |
| L-bottom | structure | 924 | derived | 0 | https://3dprinting.com/wp-content/uploads/2019/05/EOS-pa2200-white-datasheet-TDS.pdf |
| L-side-p | structure | 786 | derived | 0 | https://3dprinting.com/wp-content/uploads/2019/05/EOS-pa2200-white-datasheet-TDS.pdf |
| L-side-n | structure | 786 | derived | 0 | https://3dprinting.com/wp-content/uploads/2019/05/EOS-pa2200-white-datasheet-TDS.pdf |
| L-inner | structure | 508 | derived | 0 | https://3dprinting.com/wp-content/uploads/2019/05/EOS-pa2200-white-datasheet-TDS.pdf |
| L-front-n | structure | 219 | derived | 0 | https://3dprinting.com/wp-content/uploads/2019/05/EOS-pa2200-white-datasheet-TDS.pdf |
| L-front-p | structure | 54 | derived | 0 | https://3dprinting.com/wp-content/uploads/2019/05/EOS-pa2200-white-datasheet-TDS.pdf |
| L-front-lo | structure | 83 | derived | 0 | https://3dprinting.com/wp-content/uploads/2019/05/EOS-pa2200-white-datasheet-TDS.pdf |
| L-front-hi | structure | 54 | derived | 0 | https://3dprinting.com/wp-content/uploads/2019/05/EOS-pa2200-white-datasheet-TDS.pdf |
| S-top | structure | 215 | derived | 0 | https://3dprinting.com/wp-content/uploads/2019/05/EOS-pa2200-white-datasheet-TDS.pdf |
| S-bottom | structure | 215 | derived | 0 | https://3dprinting.com/wp-content/uploads/2019/05/EOS-pa2200-white-datasheet-TDS.pdf |
| S-side-p | structure | 183 | derived | 0 | https://3dprinting.com/wp-content/uploads/2019/05/EOS-pa2200-white-datasheet-TDS.pdf |
| S-side-n | structure | 183 | derived | 0 | https://3dprinting.com/wp-content/uploads/2019/05/EOS-pa2200-white-datasheet-TDS.pdf |
| S-inner | structure | 554 | derived | 0 | https://3dprinting.com/wp-content/uploads/2019/05/EOS-pa2200-white-datasheet-TDS.pdf |
| S-end | structure | 595 | derived | 0 | https://3dprinting.com/wp-content/uploads/2019/05/EOS-pa2200-white-datasheet-TDS.pdf |
| cell | energy_source | 8000 | source | 0 | https://www.grepow.com/high-discharge-rate-battery/15c-high-power-lipo.html |
| controller | controller | 2100 | source | 2220 | https://www.adafruit.com/product/5405 |
| driver | other | 500 | source | 15 | https://www.pololu.com/product/2135/specs |
| coupler-motor | actuator | 1200 | source | 851 | https://www.precisionmicrodrives.com/datasheets/206-109-V0.pdf |
| coupler-pinion | actuator | 83 | derived | 0 | https://www.atimaterials.com/Products/Documents/datasheets/stainless-specialty-steel/austenitic/ati_302_304_304l_305_tds_en1_v1.pdf |
| head-cartridge | coupler_mechanism | 4801 | derived | 0 | https://www.atimaterials.com/Products/Documents/datasheets/stainless-specialty-steel/austenitic/ati_302_304_304l_305_tds_en1_v1.pdf |
| tail-stud | coupler_mechanism | 2100 | derived | 0 | https://www.atimaterials.com/Products/Documents/datasheets/stainless-specialty-steel/austenitic/ati_302_304_304l_305_tds_en1_v1.pdf |
| joint-motor | actuator | 1200 | source | 851 | https://www.precisionmicrodrives.com/datasheets/206-109-V0.pdf |
| joint-pinion | actuator | 83 | derived | 0 | https://www.atimaterials.com/Products/Documents/datasheets/stainless-specialty-steel/austenitic/ati_302_304_304l_305_tds_en1_v1.pdf |
| joint-sector | structure | 241 | derived | 0 | https://www.atimaterials.com/Products/Documents/datasheets/stainless-specialty-steel/austenitic/ati_302_304_304l_305_tds_en1_v1.pdf |
| hinge-plate-low | structure | 139 | derived | 0 | https://www.atimaterials.com/Products/Documents/datasheets/stainless-specialty-steel/austenitic/ati_302_304_304l_305_tds_en1_v1.pdf |
| hinge-plate-up | structure | 139 | derived | 0 | https://www.atimaterials.com/Products/Documents/datasheets/stainless-specialty-steel/austenitic/ati_302_304_304l_305_tds_en1_v1.pdf |
| hinge-ear-low | structure | 139 | derived | 0 | https://www.atimaterials.com/Products/Documents/datasheets/stainless-specialty-steel/austenitic/ati_302_304_304l_305_tds_en1_v1.pdf |
| hinge-ear-up | structure | 139 | derived | 0 | https://www.atimaterials.com/Products/Documents/datasheets/stainless-specialty-steel/austenitic/ati_302_304_304l_305_tds_en1_v1.pdf |
| hinge-pin | structure | 534 | derived | 0 | https://www.atimaterials.com/Products/Documents/datasheets/stainless-specialty-steel/austenitic/ati_302_304_304l_305_tds_en1_v1.pdf |
| fasteners | structure | 2046 | derived | 0 | https://www.atimaterials.com/Products/Documents/datasheets/stainless-specialty-steel/austenitic/ati_302_304_304l_305_tds_en1_v1.pdf |
| harness | other | 520 | derived | 0 | https://aurubis.com/dam/jcr:ec116d17-1541-419a-a897-ad31b4fa6c93/c11000-cu-etp-us.pdf |
| **total** | | **30 247** | | **3 937** | |

## 4. Coupler

### 4.1 Parts

- **Tail stud.** One machined 304 part:
  - flange r 6.5 × 1.0, screwed to the tail end plate;
  - pilot dia 4.0 g6 × 6.2 with a 0.5 × 45 deg nose chamfer;
  - two lugs dia 3.0 g6 along ±y, reaching r 5.9, their axis 3.6 behind the flange face (nominal).
- **Head cartridge:**
  - 304 housing: tube r 2.0 to 3.5 with a pilot bore 4.0 H7 and two axial lug slots 3.05 wide (IT9). Its front lip is 0.8 thick, with 0.6 × 45 deg V lead-ins on the slots and a 0.6 × 45 deg bore chamfer. The lip face is the seat.
  - PTFE thrust ring: r 3.6 to 4.4 × 0.3, behind the lip.
  - C93200 cam sleeve: r 3.55 to 6.0, turning on the housing tube, with a gear ring m 0.3 z 43 on its rear. Two helical through-slots each have an axial entry notch, a **capture stage** (20 deg lead, 1.0 mm draw) and a **lock stage** (3 deg lead, 0.4 mm draw).
- **Drive:** 206-109 + pinion z12 (ratio 3.58). Closing uses a 1.2 V average (PWM) stall; release uses 3.6 V.

### 4.2 Cycle

1. **Presented pose.** The tail unit's stud nose is at the bore mouth (§6).
2. **Entry.** An axial push from the approach (not designed) brings the pilot past the bore chamfer. The lugs then pass the lip V lead-ins and stand at the sleeve's entry notches.
3. **Capture.** The sleeve turns, and the capture stage draws the stud 1.0 mm. Drawing one free unit at μ = 1 needs 1.39 mN m at the sleeve, against 11.6 mN m available at the closing stall.
4. **Lock.** The lock stage draws until the flange seats on the lip, then builds preload until the motor stalls. F_p is 4.24 to 11.08 N.
5. **Hold, unpowered.**
6. **Release.** The sleeve turns back at 3.6 V to the open stop, and the slot's outer flank pushes the stud out by 1.4 mm.

The sleeve turns 79.6 deg to the nominal seat. Slot extent is -25.5 to 144.1 deg, with a 10.5 deg web (0.86 mm) to the other slot's entry.

### 4.3 Numbers (`coupler.py`)

| Check | Result |
| --- | --- |
| Axial stack at seating (IT10 / g6: flange-to-lug 3.6, lug radius, lip 0.8, lip-to-flank 2.8) | ±0.068: seat 3.532 to 3.668 inside the lock stage 3.40 to 3.80, **margin 0.132 each side** |
| Self-locking, tan 3 deg = 0.0524 | steel on bronze dry 0.15 to 0.35: **2.86x** at the low end; machine oil 0.10 to 0.16: **1.91x**. PTFE thrust friction adds holding torque that is not credited |
| Preload | 4.24 (flank 0.35, thrust 0.20, η 0.9) to 11.08 N (0.15, 0.05, η 1.0) |
| Release | worst 26.8 mN m (F_p_max + tension, flank 0.35, thrust 0.20) against 34.8 mN m (3.6 V, η 0.9): **1.30**. Oil case 19.8 mN m |
| Lug on bronze flank, Hertz p0 (line 2.35 mm, R 1.5, E* 73.6 GPa) | 202 MPa design, 222 MPa with drive-limit bending, onset about 230 (1.67 × 138, rule of thumb); fault 268 |
| Lug root bending | 6.3 MPa (fault 11.1) against 304 yield 205 |
| PTFE ring pressure | 0.61 MPa |

Friction sources (all accessed 2026-11-20):
- [Wikipedia, Leadscrew](https://en.wikipedia.org/wiki/Leadscrew): steel on bronze, dry 0.15 to 0.23, oil 0.10 to 0.16.
- [Engineering ToolBox](https://www.engineeringtoolbox.com/friction-coefficients-d_778.html): bronze on steel dry static 0.35; steel on steel clean dry static 0.5 to 0.8, greased 0.16; PTFE on steel 0.05 to 0.2.

Mesh efficiency: [KHK ABCs of Gearing](https://khkgears.us/media/fqrlut1m/abcs-of-gearing-b.pdf) gives 98 to 99.5 percent for spur gears; I use 0.9 to 1.0 (provisional). Tolerances: ISO 286 IT grades from [Wikipedia, IT Grade](https://en.wikipedia.org/wiki/IT_Grade).

## 5. Declared loads and their carriers

Loads are **provisional modelling assumptions** for the Q31 tabletop chain of five (W = 0.2966 N).

| Load | Value | Carrier (every corner) | Ratio |
| --- | --- | --- | --- |
| Tension | 4 μ W, μ = 1: 1.186 N | lugs on the self-locking lock stage (geometric while self-locked); faces stay closed because F_p_min 4.24 N > 1.186 N | 3.6 (preload / load) |
| Torsion about the axis | 2 W × 12.7: 7.53 mN m | (1) no slip: dry 304 face friction 0.5 × 4.24 × r_eff 4.62 = 9.79 mN m; (2) beyond slip, geometric: lugs on the 304 housing slot sides at r 2.75, lash 0.39 to 0.76 deg each way | 1.30 (no slip) |
| Out-of-plane bending | W × 47.2: 14.0 mN m (one neighbour fully cantilevered) | face tipping F_p_min × 6.45 = 27.4 mN m; beyond it the H7/g6 pilot couple | 1.95 |
| In-plane bending | joint drive limit 14.5 mN m | face tipping 27.4 mN m; beyond it the lug pair as differential axial load on the self-locking stage | 1.89 |
| In-plane bending, fault | joint stall at 3.6 V: 52.2 mN m | as above. Extra lug load 4.67 N; Hertz 268 MPa means local indentation, not separation | n/a |
| Shear | W: 0.297 N | pilot in bore (clearance 0.004 to 0.024); dry face friction 2.12 N | 7.1 |

Why torsion must not slip: if the lugs slid on the 3 deg flank under cyclic torsion, the sleeve could be walked in the release direction. This is the mechanism by which bolts loosen under transverse slip. The preload was therefore chosen (closing at 1.2 V) so that the declared torsion is held by face friction with margin 1.30 at the dry lower bound. A greased face (μ 0.16) would slip above 3.1 mN m (limitation).

## 6. Pre-alignment

| Means | Window | Against | Physical reason |
| --- | --- | --- | --- |
| 45 deg chamfers: nose 0.5, bore 0.6 | lateral ±1.10 | ±0.6 mm two-unit PA12 stack (axis height and position, ±0.3 per feature) | the axial push gives a centring force (1 - μ)/(1 + μ), 0.11 of the push at μ 0.8 (no wedging while μ < 1) |
| Sequence: pilot before lugs | lugs see ≤ 0.024 mm lateral | n/a | the pilot's cylinder (from 5.70) is 0.60 into the bore, the end of the chamfer, when the lug fronts (5.10) reach the lip |
| Round lugs in 0.6 × 45 deg V lead-ins | roll ±7.3 deg | about ±1.4 deg (0.6 mm base flatness over 25 mm) | round lug on a 45 deg flank turns the tail unit under the axial push |
| Capture stage, then the lip seat | axial: travel to a stall | ±0.068 mm stack | motor torque through the 20 deg stage (11.6 vs 1.39 mN m); seat on machined faces |

**No capture window is claimed (CPL-006).** These are presented-pose windows on paper. The approach that brings a free unit into them is not designed (limitations).

## 7. Originality self-check (author, not the Q61 review)

This is not independent and must not be used as the review.
- **Exclusions:** no cube with an internal flywheel (no flywheel). No needle or particle silhouette: 47.2 × 25.4 × 24 mm, aspect about 1.9.
- **D2 (coupler):** a motor-turned cam sleeve with a self-locking helical stage that draws a lugged stud onto a flat seat. Shared in kind with:
  - ATRON: a motor latch held unpowered by a non-backdrivable lead screw (moderate on cand-a);
  - HiGen: a motor latch with an unpowered hold;
  - bayonet and breech-lock mounts: generic machine elements.

  It does not share the Roombots crank to a singularity, the CONRO and PolyBot SMA-released spring latch on grooved pins, or magnets (A1, M-TRAN, M-Blocks).
- **D1 and D3 (body and joint):** a two-segment body with one joint, servo-like, in chains. Likely moderate against PolyBot, CKBot and M-TRAN, as cand-b's self-check found.
- **D4:** chain only.
- **Highs I expect:** none. The reviewer decides.

## 8. Expected Gate 1 outcomes (author's checks)

| Item | Expected | Basis |
| --- | --- | --- |
| G1 | pass, 58.862 mm | registered evaluator on the draft |
| G2 | pass | same |
| G3 | pass | every component cited, no estimate basis |
| G4 | pass, 3937 ≤ 19 425 mW; endurance 1749 s reported only | same |
| G5 | pass at roll 0 | same |
| G6 | needs an independent review | §4 to §6 |
| G7, G8 | need the independent Q61 review | §7 |

## 9. Limitations

The declaration's `limitations` list is the complete record. The main ones:
- approach locomotion is not designed;
- self-locking is friction-based (2.86x dry, 1.91x oiled) and vibration-sensitive;
- no engagement or joint angle sensor;
- friction bands come from handbooks, not tests of these pairs;
- the torsion no-slip margin (1.30) depends on the motor constant and on a dry face;
- PA12 screw pull-out is not cited;
- 304-on-304 galling is possible at the pilot;
- Q31 bending adequacy at high table friction is unresolved;
- the stowed margin is 1.1 mm, against a PA12 outer tolerance of up to 0.6 mm.
