# cand-a v1: hexagonal-prism tumbler (Family A)

Author: Claude Sonnet 5.5 (task-4 agent). Date: 2026-11-04. Label: **exploratory**. Declaration: `declaration.json` (schema_version 1).

This is a paper-gate dossier (Q38 Gate 1). It does not show that any mechanism works. The numbers below come from a cited source, from an explicit derivation, or are marked **UNRESOLVED**. Nothing was tuned to pass a gate. The one geometry change made during layout (24 mm to 26 mm circumradius) was forced by packing, and is reported in section 3.

## 1. Result at a glance

Official evaluator (`zig-out/bin/kinigami-gate1`, run on the declaration only, no review records exist yet): **unresolved**.

| Item | Outcome | Why |
| --- | --- | --- |
| G1 stowed sphere | pass | D = 59 059.8 µm (Welzl and certified radius equal), limit 60 000 µm |
| G2 packaging | pass | 153 pairs tested, no interference, all boxes in the cavity. **Caveat:** the locomotion mechanism is only a reserved volume (section 6), so this pass is weak |
| G3 evidence | unresolved | 13 estimate-basis flags on controller, motor driver, two SMA wires and a placeholder (section 4) |
| G4 budgets | pass | mass sum exact; peak 2 861 mW against a 19 425 mW limit. **Caveat:** several terms are 0 placeholders (section 5), so both sums are lower bounds |
| G5 chain | pass | 2 sites, 3-unit straight chain on the table at roll 0 |
| G6 | unresolved | retention-review record missing |
| G7, G8 | unresolved | originality review missing (section 11 is only the author's self-check) |

Key numbers: stowed diameter **59.06 mm**, declared mass **39.814 g (lower bound)**, peak electrical draw **2.861 W worst case (lower bound)**, endurance not meaningful (section 5).

Honest summary: the body fits 60 mm, but the design is **incomplete where it matters most**. The kick mechanism that makes it move is not designed, and the volume reserved for it is too small (section 6). Treat G2 and G4 passes as bookkeeping on an incomplete layout.

## 2. Concept and family membership

Family A (Q62 s3): one rigid polyhedral body that moves by pivoting or rolling over edges, with couplers on faces.

- Body: a regular hexagonal prism, no internal joint, no moving outer parts when stowed.
- Locomotion intent: the unit lies on one rectangular side face and tumbles over a bottom hexagon edge onto the next face, like a hexagonal log. One step is 60 degrees. A spring-returned kick strut on the trailing edge of the bottom face pushes against the table to lift the trailing side until the centre of mass passes the leading edge. Gravity completes the step.
- Couplers: one on each hexagonal end face (head and tail), so units join end to end along the prism axis. Faces of this kind are "couplers on faces".
- Exclusions (Q62 s3): **not a cube**, no flywheel or other reaction wheel, no magnet. The proportions are 52.0 mm across corners, 45.0 mm across flats and 28 mm long (aspect about 1.9:1.0 against the long axis, with a flat face), so there is no needle or particle silhouette.

## 3. Geometry: stowed and deployed

Frame: prism axis = body y, rest orientation = identity (bottom side face down, vertex line along ±x at mid-height).

| Quantity | Value | Basis |
| --- | --- | --- |
| Circumradius R | 26.000 mm | design choice, see below |
| Across corners | 52.000 mm | 2R |
| Apothem (across flats / 2) | 22.517 mm | R·√3/2, derived |
| Axial length H | 28.000 mm | design choice (sphere constraint: H ≤ 2·√(30² − R²) = 29.9 mm) |
| Stowed enclosing sphere diameter | **59.060 mm** | evaluator: 2 × 29 529.9 µm, centre at origin |
| End plates | 2 mm thick, y = ±12 to ±14 mm | design choice |
| Wall | radial 20.000 to 22.516 mm, between the plates | design choice |
| Inner cavity | cylinder r = 20 mm, |y| ≤ 12 mm | design choice |

**Stowed:** all coupler hardware is retracted flush inside the end plates (pins of radius 3 mm, half-height 1 mm in the declaration). The kick struts are retracted flush with their faces. Nothing protrudes. The declaration models the hexagon as three overlapping boxes (rectangle 26 × 45 mm rotated 0, 60 and 120 degrees about y, each corner on a hexagon vertex).

**Deployed (chain geometry):** the head pin extends about 4 mm beyond the head end plate (y = 14 to 18 mm, radius 3 mm). The tail bore (radius 3.2 mm, 4 mm deep) receives it. A kick strut extends about 14 mm out of a bottom face during a step (section 6). Deployed extents are not constrained by Q12. They are evaluated separately (ENV-005) and the strut sweep has not been analysed beyond section 6.

**Why 26 mm and not 24 mm.** The first layout used R = 24 mm, H = 34 mm. With a 18 mm inner radius it could not hold the cell, controller board, one gearmotor with its shaft, a driver and the coupler hardware. A randomised and a grid packing search found no arrangement for three Pololu motors, and none with two motors plus couplers and a cell. The problem is the motor, which is 25 mm long plus a 10 mm shaft. Enlarging R to 26 mm and shortening H to 28 mm still satisfies the sphere (D = 59.06 mm) and gave a feasible hand layout. This was a packing necessity. It is not a gate tuning step, because the Q12 limit was met with margin at both sizes.

## 4. Q12 packaging and component list

Cavity: one cylinder r = 26.001 mm, half-height 14 mm (envelope). Walls and end plates are components inside it. Interior boxes keep all corners within r ≤ 20 mm so they do not overlap the wall slabs. The author's own SAT check and the official evaluator agree: no interference.

Hand layout (body frame, mm, centre of box):

- cell stood on edge, 31 × 7.5 × 20 (x, y, z), centre (0, −5, 0)
- gearmotor along x including its shaft, 35 × 10 × 12, centre (0, 3.8, 0)
- controller board, 21 × 17.5 × 4 (**thickness assumed, UNRESOLVED**), centre (0, 0, 12.2)
- motor driver, 10.2 × 12.7 × 3 (**thickness assumed, UNRESOLVED**), centre (0, 0, −12)
- SMA wires, 1 × 18 × 1, at (±17, 0, −8), 25 mm wire folded or run along y (**UNRESOLVED**)
- coupler housings, 8 × 3 × 8, at y = ±10.5
- kick-mechanism reserve, 8 × 6 × 6, centre (0, 4, −16.5) (**placeholder, section 6**)

Assembly access: end plate removed, stack loaded along the axis. No assembly sequence was verified.

### Parts (access date for every source: 2026-11-04)

| Component | Part | Source | Verified there | Unresolved |
| --- | --- | --- | --- | --- |
| Energy source | Grepow GRP8020030, 1S LiPo | [Grepow 15C high-power LiPo table](https://www.grepow.com/high-discharge-rate-battery/15c-high-power-lipo.html) | 350 mAh, 15C, 7.5 ± 0.3 × 20.0 ± 0.5 × 31.0 ± 0.5 mm, 8.0 ± 0.5 g | The 3.7 V label came from a search-result row and was not on the fetched excerpt. The page does not say that 15C is a **continuous** rating. I read it as 15 × 0.35 = 5.25 A and flagged that reading. Tolerances on mass and size are not carried into the declaration |
| Controller + IMU + radio | Seeed XIAO nRF52840 Sense (nRF52840, BLE, LSM6DS3TR-C) | [Seeed wiki](https://wiki.seeedstudio.com/XIAO_BLE/); [Seeed TDS via Distrelec](https://media.distrelec.com/Web/Downloads/_t/ds/102010469_eng_tds.pdf) | Footprint 21 × 17.5 mm (wiki says 17.8), IMU and MCU part numbers | **Mass** (4 g seen only on reseller listings, not manufacturer), **thickness**, **current draw** and the nRF52840 radio range were not found. All recorded as `estimate` |
| Kick actuator | Pololu 150:1 Micro Metal Gearmotor MP 6V | [Pololu 2368](https://www.pololu.com/product/2368) (specs tab) | 9.5 g, 10 × 12 × 25 mm plus 10 mm shaft, 6 V, no-load 0.07 A, stall 0.67 A, stall torque 1.3 kg·cm, 150 rpm | Operation at 3.7 V is a derivation (section 5), not a rated point |
| Motor driver | Pololu DRV8838 single driver carrier | [Pololu 2990](https://www.pololu.com/product/2990) | 0.5 × 0.4 in, motor supply 0–11 V, 1.7 A continuous, 1.8 A peak | **Mass and thickness not stated** |
| Coupler release | Dynalloy Flexinol, 0.004 in wire | [Flexinol technical data](https://cdn.robotshop.com/media/d/dyn/rb-dyn-01/pdf/flexinol-technical-data.pdf) (text extracted from the PDF) | 3.0 Ω/in, max pull 150 g, approx. current 180 mA, contraction about 1 s, off time 0.8 s (LT wire) | **Wire mass, density, strain percentage and the stroke needed to free the ball-lock** are not in the sheet. The SMA switch and current limiting are not selected |
| Structure material | EOS PA 2200 (PA12, laser-sintered) | [EOS PA 2200 Performance 1.0 data sheet](https://3dprinting.com/wp-content/uploads/2019/05/EOS-pa2200-white-datasheet-TDS.pdf) (text extracted from the PDF) | density 930 kg/m³ | The wall thickness is below any minimum-wall guidance I looked up (none was checked). Strength is not assessed |

Not selected and not in the declaration: cam/strut position sensor (the Pololu magnetic encoder kit, [product 3081](https://www.pololu.com/product/3081), needs a gearmotor with an extended back shaft; no such part was verified), fasteners, springs, balls, wiring, PCB interconnect, SMA switch. They are lumped in `unresolved-bucket` with **0 mg and 0 mW recorded as a placeholder, not a measurement**.

Vendor product pages (Grepow, Pololu, Seeed) are classed `datasheet` because the schema allows only `datasheet` or `publication`. A reviewer should treat that as a stretch.

## 5. Mass and power budgets (reported)

**Mass (declared 39 814 mg, equal to the sum):**

| Group | mg | Basis |
| --- | --- | --- |
| 6 wall slabs | 6 × 1 859 | derived: (hexagon area − π·20²) × 24 mm × 930 kg/m³, split in six |
| 2 end plates | 2 × 3 267 | derived: hexagon area × 2 mm × 930 kg/m³ (solid, ignores coupler bores) |
| Cell | 8 000 | source (nominal) |
| Gearmotor | 9 500 | source |
| Controller | 4 000 | estimate (reseller figure) |
| 2 coupler housings | 2 × 179 | derived: solid-fill PA12 upper bound of an 8 × 8 × 3 mm box; balls, springs, sleeve are missing |
| Kick-mechanism reserve | 268 | derived: solid-fill PA12 of the 8 × 6 × 6 mm reserve; not the real mechanism |
| Driver, 2 SMA wires, bucket | 0 | UNRESOLVED placeholders |

The total is a **lower bound**. The shell is solid PA12, so it may be an overestimate, but nothing counts the real fasteners, springs or wiring.

**Peak (worst case, all at once, per protocol s6):** motor at stall from the 3.7 V cell 1 529 mW, plus two SMA wires 2 × 666 mW = **2 861 mW**. Limit: 3.7 V × 5.25 A = 19 425 mW.

- Motor stall: 0.67 A × (3.7 V / 6 V) = 0.413 A, assuming I_stall = V / R. Not a rated point.
- SMA: 180 mA × 3.7 V, assuming linear drive from the cell. The wire is about 2.95 Ω (3.0 Ω/in × 0.98 in), so 180 mA needs only about 0.53 V. A real driver would draw less, but its design is open.
- Controller, driver and bucket draw are 0 placeholders. The sum is a **lower bound**, and G4 passing with a 6.8× margin makes the pass robust to those terms only if they are small. I did not verify that.

**Continuous:** UNRESOLVED. The duty cycle of the kick motor is not defined. Pololu rates the motor at 6 V, and I found no continuous-current rating at 3.7 V.

**Endurance (reported only, never gates):** energy = 0.35 Ah × 3.7 V = 1.295 Wh = 4 662 000 mJ (nominal, not usable). Average power recorded = 160 mW (the motor at no-load speed, derived as 0.07 A × 3.7/6 × 3.7 V). Result 29 137 s (about 8.1 h) as mJ/mW. **This figure is not meaningful:** it ignores the controller, the driver, loaded operation and all duty cycles, so it is an upper bound on a quantity that was not specified. The evaluator also prints 29 137 500 s ("protocol literal"). The protocol formula `energy_mj · 1000 / P_avg_mW` carries an extra factor of 1000 for mJ over mW. I used mJ/mW and report the discrepancy to the lead.

## 6. Locomotion: the unfinished part

Analytic checks (frictionless pivot, rigid body, centre of mass at the geometric centre; the evaluator does not compute these):

- Centre of mass must rise R − apothem = 3.48 mm to pass over the leading edge. Energy at 39.8 g is about **1.36 mJ**. The weight moment about the leading edge at the start is about 5.1 mN·m.
- A strut pushing near the trailing edge of the bottom face (11 mm from the face centre) must extend about **14 mm** to carry the body to the 30 degree tipping point. At 6 mm offset it is about 11 mm. These come from a 2D rotation about the leading edge with the strut normal tilting with the body.
- Pushing from a lower **side** face instead needs 25 mm or more even to touch the table (computed for R = 24 mm), so that option was discarded.

Consequences:

1. **The reserved volume is far too small.** A strut that extends 14 mm needs at least 14 mm of guide, and there are six faces. The 8 × 6 × 6 mm reserve in the declaration cannot hold that. Struts on the bottom face would also run through the driver and cell region. The layout that passes G2 therefore does not contain a working kick mechanism. **I did not solve this.**
2. **One direction only, as conceived.** A strut at the trailing edge of each face rolls the unit one way. Reversal needs six more struts, and steering needs tilting over end-plate edges, which is not designed.
3. **Drive and sensing:** I intended one motor with a rotating cam selecting among six spring-returned struts, with a position sensor. None of that is laid out. The motor's shaft is inside the 35 mm box, but nothing connects it to a cam.
4. **Friction** at the pivot edge and strut tip is unresolved (Q47 gives a reference law; I did not apply it). If the pivot edge slips the step fails.

## 7. Coupler layout (design-guidance 4.2)

Two couplers, one on each hexagonal end face. Head = pin, tail = bore, so a chain has a direction. Sites: head (0, +14 mm, 0), normal +y; tail (0, −14 mm, 0), normal −y. No lateral couplers in v1 (no branching, no lattice).

- **Align:** the conical lead-in on pin and bore centres a laterally offset unit. A hexagonal outline key on the end plate fixes roll to the six 60 degree positions. Geometry only, no magnet.
- **Latch:** a spring-preloaded ball-lock. Balls in the head pin press into a groove in the tail bore, held by a sprung sleeve. Pushing the units together drives the balls in by the lead-in ramp, so latching needs no actuator.
- **Transmit force:** tension through balls in shear on the groove, compression through the end-plate faces, bending and torsion through the hex key. Strength is **unresolved**: the ball size, the groove geometry and the load limits are not designed or computed.
- **Detach:** a Flexinol wire on each coupler pulls the sleeve back against its spring, freeing the balls. It works from the unit's own side and needs no help from the neighbour (bounded independent release). Heating time of about 1 s and cooling time of about 0.8 s come from the sheet. The stroke and the force needed are **unresolved**.
- **Data:** no through-coupler contacts are declared (COM-001 allows that). The only declared channel is the nRF52840 BLE radio, which is contactless. Its range, occlusion in a chain and latency are **unresolved**. COM-008 stays open.
- **Power:** no power transfer. Each unit runs on its own cell (the isolated baseline of Q34). PWR-001 optional, not provided.

## 8. Passive retention when unpowered (CPL-009, Q11)

The ball-lock is held by a spring and the hex key is geometry, so retention needs no power. `requires_power_to_hold = false`. Only release is powered. What holds under declared loads is not shown: the spring preload, the ball-groove contact and the plate-to-plate friction are not sized, and the loaded tests belong to later gates. The Q31 benchmark also needs the chain to bend, see risk 3.

## 9. Pre-alignment justification (CPL-005, Q36)

Pre-alignment forces come only from sliding contact on the conical lead-in and the key chamfers, plus gravity and table friction. They push the units together only if something pushes them (the kick strut or a neighbour). There is no attractive force, so a unit that is not driven does not self-dock. The justification record requires the dimensions, and the cone angle, lead-in depth and key chamfer are **not chosen**. The capture window is not claimed and must be measured by sweeps (CPL-006). A reviewer should expect to find G6 justified only in principle at this point.

## 10. Risks and unknowns

1. **No working locomotion mechanism** (section 6). This is the main risk, and the declaration's G2 pass does not cover it.
2. **Steering and reversal** are not provided.
3. **Chain articulation (Q31):** units have no internal joint. Bending a chain must come from the couplers allowing some hinge motion and from units pushing against the table. The ball-lock plus hex key is rigid by design, so bending is not demonstrated and may need a different coupler.
4. **Motor choice is oversized for the task** (9.5 g, 35 mm with shaft) and dominates the packing. A smaller part was not searched for.
5. **Cell:** the continuous rating is an interpretation; mass tolerance ± 0.5 g; stood-on-edge mounting may stress the pouch (not checked).
6. **Controller** mass, thickness and power are unknown; the radio's real range as a "contactless channel" is unknown.
7. **PA12 walls** 2.5 mm at face centres were not checked for stiffness, and the fastener choice is open.
8. **Heat:** the SMA wires and motor at stall inside a closed body were not assessed.
9. **Mass lower bound:** the true mass will be higher than 39.8 g.
10. **The evaluator checks static boxes** (protocol limitation). Box layout is a hand layout, shaft routing and wiring are not modelled.
11. **Three-unit chain only**; the five-unit claim of Q31 is untested.

## 11. Author self-check against the originality corpus (NOT the official review)

This is the author's own check against `docs/originality/reference-corpus.md`. It is not independent (Q61 s4), it is not the Q61 matrix, and it does not count for G7 or G8. It is a list of where an independent reviewer should look first. Ratings use the Q61 anchors. Descriptor text in the corpus was written from abstracts, not full texts, and my comparison inherits that limit.

| Reference | D1 geometry | D2 coupler | D3 locomotion | D4 assembly | D5 visual | Note |
| --- | --- | --- | --- | --- | --- | --- |
| A1 BH6 microbots | none | none | none | none | none | Large single unit, flat-faced, no particle swarm, no magnetic legs |
| B1 Replicators | none | none | none | low | none | |
| C7 M-Blocks / C8 3D M-Blocks | low | low | **moderate** | low | low | Same idea: a whole rigid body that pivots over an edge. Different: hexagonal prism not a cube, ground-contact kick strut not a flywheel, ball-lock not magnets. A reviewer should confirm D3 is not "high" |
| C11 Molecubes | low | low | none | low | low | |
| C12 PolyBot, C14 CKBot, C22 Sambot | low | low | none | low | low | Genderless or active dock plates on faces; the ball-lock with hex key is a different form |
| C4 ATRON, C6 Roombots, C16 FreeBOT | none | low | none | low | none | Spheres or peanut shapes |
| C18 Telecube, C19 Crystalline | none | low | none | low | none | |
| D1 Cubelets, C23 Blinky Blocks | low | low | none | low | low | Cubes with magnetic faces |
| C9 Kilobot | none | none | low | none | none | Leg-on-ground motion is the only link |

- **Exclusion 1 (cube with internal flywheel):** not present. The body is a hexagonal prism and has no flywheel or reaction wheel.
- **Exclusion 2 (needle- or particle-like silhouette):** not present. A 52 mm hexagonal prism, 28 mm long, with large flat faces.
- **Highest author rating:** one **moderate** (D3 against M-Blocks), with the differentiation note above. No cell rated high. I expect no Q61 fail rule to trigger, but that is for the independent reviewer to decide.
- **Things the corpus cannot tell me:** whether a hexagonal log-roller with ground-kick struts exists outside the corpus. The corpus is not exhaustive, so nothing here claims absolute originality.
- **Family membership:** meets the Family A constraint (single rigid polyhedron, edge pivoting, couplers on faces), subject to the locomotion mechanism being designed.

## 12. Unresolved list (for the lead)

1. Kick-strut/cam mechanism geometry, stroke, drive, position sensing, reversal and steering.
2. Controller mass, thickness, current.
3. Motor driver mass and thickness.
4. SMA wire mass, strain and stroke needed; SMA switching and current limit.
5. Cell "continuous" rating semantics and the 3.7 V label.
6. Coupler strength, ball and groove sizes, spring preload, lead-in angles, capture window.
7. Fasteners, springs, balls, wiring, PCB interconnect (zero placeholders).
8. Continuous power and any meaningful endurance figure.
9. Through-coupler data channel and BLE range.
10. Lateral couplers, chain bending (Q31), and the five-unit chain.
11. Retention-review and originality-review records (independent reviewers).
12. Protocol note: the endurance formula in `gate1-v1-protocol.md` s6 has an extra ×1000 for mJ/mW.
