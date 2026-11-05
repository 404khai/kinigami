# Candidate B (`cand-b`), version 1: Z-link two-segment body

Family B (Q62 §3): an elongated two-segment body with one internal revolute joint, chain-native, couplers at the segment ends.

| Field | Value |
| --- | --- |
| Result label | `exploratory` (paper gate, Q38/Q40). Nothing here is validated |
| Declaration | `candidates/cand-b/declaration.json`, SHA-256 `d973b4cc57b45381b0be9b7e35bdf4508aa3ef449e5fb613c648834454f69a5a` at the time of writing. Any later edit changes the hash and invalidates reviews |
| Author | Claude Sonnet 5.5 (agent task-5). Not a reviewer. No independent review exists yet |
| Declared | 2026-11-04. All source access dates are 2026-11-04 |
| Criteria | `criteria/gates/gate1-v1.json`, protocol revision 1 |
| Governs | Q12 envelope (ENV-004), Q31, Q36, Q37, Q38, Q61, Q62; CPL-005, CPL-009, SEL-001..009 |

**Status in one line:** the stowed envelope and packaging pass my own numeric checks, but the candidate is not a Gate 1 pass. Placeholders leave G3 unresolved, G5 is expected to fail on a protocol artifact (§10), and G6, G7 and G8 have no review records yet.

All dimensions are in millimetres in this document and in integer micrometres in the declaration. Design dimensions (segment sizes, wall thickness) are choices of this candidate. They are declared geometry, not physical properties, and stay provisional until Gate 2.

## 1. Concept

Two PA12 shells, **A** and **B**, are joined at a servo pivot placed in the middle of the body. The segments are not collinear. B is offset sideways from A by one segment width (16 mm), so the straight unit is a **Z-link**, like a crank link. This offset is what lets a single revolute fold the body flat. A unit with the pivot on the centreline cannot fold 180° without the segments colliding.

- **Deployed:** A and B overlap in x over the pivot zone and are offset in y. The socket (head) is at the +x end of A. The plug (tail) is at the −x end of B.
- **Stowed:** the servo turns B 180° about the vertical pivot. B ends up beside A, and both couplers face +x.
- **Chain:** a plug seats in the next unit's socket. Units are mated with a 180° roll about the chain axis so the 16 mm offsets alternate and the chain zigzags about a straight mean line. A roll of 0° makes the chain drift 16 mm sideways per unit.

The joint axis is vertical when the unit rests on the tabletop, so bending happens in the table plane (Q31 requires nominally planar bending with full 3D physics).

### 1.1 Deliberate differentiation (corpus entries C1–C3, C12–C14, C22)

The nearest published systems are single-joint chain modules. Family B itself puts this candidate close to them in kind. Differences chosen on purpose:

| Reference | What it shares in kind | What this candidate does differently |
| --- | --- | --- |
| M-TRAN (C1–C3) | Two body halves with a joint between them; chain use | M-TRAN halves are cuboid-and-semicylinder blocks with magnet faces and two joints. Here: a single joint at mid-body, an offset Z-link, a plain spring-hook mechanical latch with **no magnets**, and a 180° fold to a side-by-side pair |
| PolyBot (C12), CKBot (C14) | One rotational joint per module; snake-like chains | Those are cube modules with genderless face plates; the rotation axis runs through the module. Here: the pivot is offset from the chain line, the two ends carry different connectors (plug and socket), and the unit is elongated, not cubic |
| SuperBot (C13) | Boxy articulated modules | Single joint, not three; no docking faces on the sides |
| Sambot (C22) | One hinged docking arm | No wheels or tracks; docking is at the two segment ends, not on a swung arm |

These are statements of intent for the independent reviewer to check. They are not a review.

## 2. Geometry

Body frame: origin on the pivot axis at the mid-height of the unit. x runs along the chain and z is the pivot axis (up on the table). Both segments are drawn as boxes in the declaration. These boxes are conservative envelopes. Real shells would be rounded, and the inner ends would be rounded about the pivot (§12 risk R3).

### 2.1 Deployed (straight, joint 0°)

| Item | Extent (x, y, z) |
| --- | --- |
| Segment A | x −8 to 26, y −8 to 8, z ±15 (34 × 16 × 30) |
| Segment B | x −26 to 8, y 8 to 24, z ±15 (34 × 16 × 30) |
| Plug (cylinder, ⌀8 × 5 long) | centred (−28.5, 16, 0), axis x, protrudes from B's −x face |
| Socket | recess in A's +x face at (26, 0, 0), flush, no protrusion |
| Pivot | (0, 0), vertical axis through the servo output |
| Footprint of the unit | x −31 to 26 (57 mm including plug), y −8 to 24 (32 mm), z ±15 (30 mm) |

Enclosing sphere of the deployed unit (my script, same method as protocol §3): 68.0 mm. That is larger than 60 mm. Q12 limits only the stowed sphere. Whether ENV-003 (30–60 mm class, Q1 text not available) is meant to bound the deployed size is **unresolved**. Q37 item 2 says the class is a reference scale and deployed geometry is evaluated independently.

### 2.2 Stowed (joint 180°)

| Item | Extent |
| --- | --- |
| Segment A | unchanged: x −8 to 26, y −8 to 8, z ±15 |
| Segment B | x −8 to 26, y −24 to −8, z ±15 |
| Plug | centred (28.5, −16, 0), protrudes to x = 31 |
| Overall | x −8 to 31, y −24 to 8, z ±15 |

### 2.3 Joint range

| Quantity | Value | Basis |
| --- | --- | --- |
| Required travel | 0° (straight) to 180° (stowed), one-sided (B swings toward −y only) | design |
| Servo range of motion | 300° | SCS0009 spec page, §5 |
| Margin | 120° of servo range beyond the required travel | derived |
| Backward bend (negative angle) | not possible; B would meet A | design limit |
| Hard stops | at 0° and 180° | design intent, not detailed |

One-sided travel means a single unit can curve a chain in one direction only. Alternating roll angles, or paired units, are needed for S-shapes. Whether that supports the Q31 curvature change is **unresolved** (Gate 2).

## 3. Q12 packaging

| Check | Result | How |
| --- | --- | --- |
| Stowed enclosing sphere | **55.50 mm** (limit 60 mm, Q12) | My Python replica of protocol §3 on the declared body and coupler primitives. The Welzl radius and the certified radius coincide because all body parts are boxes. This is not the registered evaluator, and the plug cylinder is included |
| Margin | 4.50 mm | derived |
| Component boxes inside one cavity | all 12 inside cavity-a or cavity-b | script |
| Pairwise component interference | none (touching allowed) | script, axis-aligned boxes |
| Cavity A | x −6.5 to 24.5, y ±6.5, z ±13.5 (31 × 13 × 27) | wall 1.5 mm, design |
| Cavity B | same, centred y = −16 | |

Packing detail (stowed coordinates):

- **Segment A cavity:** servo at x −5.8 to 17.4 (full width, 12.1 of 13 mm). Behind the shaft there is 0.7 mm of cavity. In front of the servo, from x 17.4 to 24.5, sit the SMA wire (x 17.5), the latch (x 17.6 to 21.0) and the pogo pins (x 21.0 to 24.5), in 7.1 mm.
- **Segment B cavity:** battery (30 along x, 7 thick), controller (21 along x, 4 thick, estimate), and the boost converter beside the controller (x 15.5 to 24.5).
- **Hinge arm:** a 12 × 12 × 0.8 mm plate on top of the servo, z 12.7 to 13.5, 75 µm above the servo top.
- **Margins are very small:** servo-to-wall 0.45 mm each side in y, latch and pogo stack zero spare length. Any component taller than its placeholder breaks the packing (R1).

Sweep check (not in Gate 1, so recorded here): while B rotates, its nearest edge passes 8 mm from the pivot, exactly at A's inner end face (x = −8). Clearance is **zero**, and the servo's rear corners (radius 8.4 mm from the shaft) lie outside an 8 mm rounded end. See R3.

**Assembly access (Q38 Gate 1):** each shell is a clamshell split in the plane of the segment mid-width. Components go into the open half, the halves are screwed together, and the hinge arm is fitted to the servo horn through the open inner end of A. Not prototyped. Whether the servo horn can be reached with B fitted is unresolved.

## 4. Component list

Source column: URL, access date 2026-11-04. **Verified** means I opened the page or PDF this session and read the cited value there. **Search-result only** means a web-search result showed the value and I did not open the source. No component has a manufacturer datasheet that I verified for every value used, except where marked.

| # | Component | Role | Source | Values used | Verification |
| --- | --- | --- | --- | --- | --- |
| 1 | Feetech SCS0009 serial-bus servo | Hinge actuator | [retailer spec page](https://partsbaba.com/products/scs0009-6v-2-3kg-300deg-serial-bus-servo-motor) | 23.2 × 12.1 × 25.25 mm, **13.2 ± 1 g**, 4–7.4 V, stall 2.3 kg·cm and 1.0 A at 6 V, 300° range, 10-bit magnetic encoder | Page read. Feetech's own datasheet was **not located**. Another listing's snippet said 9 g (not opened). I used the explicit 13.2 g |
| 2 | Seeed XIAO nRF52840 Sense | Controller, BLE radio, IMU (LSM6DS3TR-C), LiPo charger | [Seeed wiki](https://wiki.seeedstudio.com/XIAO_BLE/) | 21 × 17.8 mm, BLE, IMU, charge current 50/100 mA | Wiki read. **No mass and no thickness published** there; both are placeholders |
| 3 | Bitcraze 250 mAh 1S LiPo | Energy source | [Bitcraze datasheet Rev 1](https://www.bitcraze.io/documentation/hardware/250mah_battery/250mah_battery-datasheet.pdf) | 7.1 g, 20 × 7 × 30 mm, 3.7 V, "Discharge: 15C" | PDF downloaded and read. The sheet says "Discharge: 15C" without the word continuous (R6) |
| 4 | Pololu U1V10F5 5 V step-up | 5 V rail for the servo (servo minimum 4 V is above a LiPo's 3.0–3.7 V) | [Pololu product page](https://www.pololu.com/product/2564) | 9 × 11.5 × 2.5 mm, input 0.5–5.5 V, "input currents up to 1.2 A" | Page read through a fetch summary. **Weight not found**; placeholder. Output current rating not found |
| 5 | Diodes DMG1012T MOSFET (SOT523) | PWM switch for the SMA wire | [Diodes datasheet](https://www.diodes.com/assets/Datasheets/DMG1012T.pdf) | 0.002 g, SOT523 (D 1.50–1.70, A2 0.60–0.80 mm), RDS(on) 0.5 Ω max at 2.5 V | PDF read. Box 1.6 × 0.8 × 0.8 mm taken from package outline |
| 6 | Dynalloy Flexinol 0.10 mm SMA wire | Latch release actuator | [Dynalloy wire data](https://www.dynalloy.com/tech_data_wire.php) | 3.2 Ω/in, 200 mA for 1 s contraction, 0.31 lb pull, cooling about 1 s | Page read. **Density not verified.** A search snippet said 6.45 g/cm³ and the PDF I downloaded did not show it, so the wire mass is a placeholder (about 1 mg) |
| 7 | Mill-Max 0906 series spring-loaded pins, ×4 | Through-coupler contacts | [Mouser Mill-Max page](https://www.mouser.com/new/mill-max/millmax_0900_0906/) | 2 A continuous, 3 A peak, pin height 3.48–5.99 mm, 25 g initial spring force | **Search-result only.** The page text was not parsed. Pin mass and barrel diameter are placeholders |
| 8 | PA12 (HP MJF-type) printed shells and arm | Structure | [Weerg Nylon PA12 datasheet](https://weerg.com/hubfs/Datasheets/Datasheets%202024/ENG/EN_NylonPA12.pdf) | Density 1.01 g/cm³ (ASTM D792) | PDF downloaded and read. Masses derived from my geometry |
| 9 | Latch assembly (spring-hook ring) | Retention | none | placeholder mass 600 mg, placeholder size | **Uncited.** Declared with a deliberately invalid URL (`https://invalid.example/uncited`) so nothing looks sourced |
| 10 | Wiring and fasteners | Interconnect | none | placeholder mass 300 mg | **Uncited**, same marking |

Unit-level notes:

- Components 9 and 10 are custom or generic items. They are not purchasable as one part. The latch hook and spring would be spring-steel wire. No supplier was selected, and this is unresolved.
- The SCS0009 and XIAO are purchasable modules. The Pololu converter, MOSFET, pins, battery and SMA wire are purchasable parts.
- Bus interface for the servo (single-wire half-duplex TTL from the nRF52840 UART) needs a buffer or a resistor/diode arrangement that is **not in the list**. Its mass and board space are unresolved (R7).

## 5. Mass and power budgets

### 5.1 Mass (G4 item 1: total equals the sum of the components)

| Component | Mass (mg) | Basis |
| --- | ---: | --- |
| Servo | 13 200 | source |
| Battery | 7 100 | source |
| Shell B + plug | 5 747 | derived: 5 690 mm³ solid × 1.01 g/cm³ |
| Shell A | 5 493 | derived: 5 439 mm³ solid × 1.01 g/cm³ |
| Controller | 1 500 | **estimate (placeholder)** |
| Latch assembly | 600 | **estimate (placeholder)** |
| Boost converter | 400 | **estimate (placeholder)** |
| Wiring, fasteners | 300 | **estimate (placeholder)** |
| Hinge arm plate | 116 | derived: 115.2 mm³ × 1.01 g/cm³ |
| Pogo pin block | 100 | **estimate (placeholder)** |
| MOSFET | 2 | source |
| SMA wire | 1 | **estimate** (density unverified) |
| **Total** | **34 559** | equals the declared `total_mass_mg` |

The shell masses are solid-wall upper bounds: outer box minus cavity, with no rounding or lightening. A real printed shell with ribs and rounded edges would weigh less. Estimates total 2 901 mg, 8.4 % of the total. The servo alone is 38 %.

### 5.2 Power (G4 item 2) and energy (item 3)

| Component | Peak (mW) | Basis |
| --- | ---: | --- |
| Servo | 5 000 | derived: 5 V × 1.0 A (the 6 V stall current), output side. Boost-converter losses are **not** included |
| SMA wire | 4 534 | derived worst case: switch stuck on, 3.7 V across 2.52 Ω wire (3.2 Ω/in × 20 mm) plus 0.5 Ω RDS(on) → 1.225 A |
| Controller | 60 | **estimate (placeholder)** |
| Others | 0 | |
| **Sum** | **9 594** | |
| Source limit | 13 875 | 3.7 V × 3.75 A (0.25 Ah × 15C, §4 row 3) |

Margin 4 281 mW. At the stall peak the converter must supply the servo at an efficiency of at least 0.54 for the sum to stay under the limit (5 000 mW / (13 875 − 4 594 mW)). Converter efficiency is unresolved (R6). The SMA fault case is a worst-case bound. Normal release uses PWM at about 200 mA average.

**Endurance (reported only, never gates).** Assumed average draw is 195 mW (servo 150, controller 25, SMA 20, all **estimates**). Usable energy is declared as 3 330 000 mJ (0.25 Ah × 3.7 V = 0.925 Wh, nominal, not usable energy). In SI units that is 3 330 000 mJ / 195 mW ≈ 17 000 s (4.7 h). The protocol formula as written (`energy_mj · 1000 / P_avg_mW`) gives a figure 1 000 times larger. I believe that is a typo and report both. The threshold stays `unresolved` (Q62).

## 6. Coupler layout (design-guidance 4.2)

Two sites, both on the chain line, genderless pair broken on purpose: the tail is a plug, the head is a socket. Any unit's plug mates with any unit's socket.

| Step | Mechanism |
| --- | --- |
| **Align** | A conical funnel in the socket mouth meets a tapered plug tip. Two flats on the plug fit matching flats in the socket and allow only 0° or 180° roll about the chain axis. The funnel and keys also align the four pogo pins to their pads |
| **Latch** | The plug pushes past spring-loaded hooks that have a ramped lead-in. The hooks snap into a groove on the plug neck. A hook shoulder square to the pull direction blocks withdrawal |
| **Transmit force** | Tension: hook shoulders in the neck groove. Compression: the plug shoulder against the socket floor and the B end face against the A end face. Shear and bending: the plug cylinder in the socket bore plus the contacting end faces. Torsion about the chain axis: the two keying flats. Per-axis stiffnesses, limits and damping are **not available** and must come from Gate 2/3 (Q35) |
| **Detach** | The MCU pulses the SMA wire (PWM through the MOSFET). The wire contracts and pulls the hook ring radially out of the groove against the hook spring. The unit then backs away. Release is a physical process that can take about 1 s to heat and about 1 s to cool (wire data) and can be blocked by load on the hook shoulder (CPL-008) |
| **Data** | Four spring pins in the socket floor touch pads on the plug tip: GND, TX, RX, engagement sense. Mechanical engagement does not guarantee electrical contact (Q36, COM-003). The sense pin lets a controller distinguish "contact" from "seated" |
| **Power** | Inter-unit power transfer is **not provided** in v1 (PWR-001 makes it optional). Only the 3.3 V logic signals cross. No power path means no conversion or protection parts are needed on the coupler |
| **Contactless channel** | BLE from the XIAO. Its range and reachability are not shaped to the 60 mm class and are unresolved (R8) |

Locomotion to reach a neighbour is **not designed**. A one-joint unit has very little independent mobility. See R2.

## 7. Passive retention when unpowered (CPL-009, Q11)

Retention is a **geometric interlock plus spring preload**. The hooks are held in the groove by their springs. Nothing in the holding path takes electrical power, and `requires_power_to_hold` is `false` in the declaration. Release needs power (SMA), which is allowed: CPL-009 asks for bounded independent release, not power-free release.

- Independent release: the unit's own SMA wire releases its own socket. A neighbour does not have to help.
- Bounded: the hook ring stop limits the stroke.
- Not shown: any holding force, the load the hooks and the PA12 groove can carry, creep of PA12 under a constant hook load, and the wear of the groove. No number is claimed. Gate 2/3 must derive them from the solver (Q35) and evaluate them under declared loads.
- The **hinge** holds its angle only while the servo is powered or its gear train resists back-driving. Q31 item 6 says not to assume every curvature can be locked without power. Nothing here claims a passively locked curvature.

An independent retention review record (`retention-review-v1-r<n>.md`, protocol §8 check 6) does **not** exist. G6 is therefore `unresolved`.

## 8. Pre-alignment justification (CPL-005, Q36)

No magnet is used. The pre-alignment force is **contact reaction on a conical funnel**, driven by the approach push of the moving unit:

- The plug tip taper meets the funnel wall. The wall reaction has a component perpendicular to the chain axis that pushes the plug toward the axis. A contact reaction on a sloped wall is the same kind of force the physics core already handles (contact and friction, Q35).
- Friction on the funnel wall opposes the centring component. Whether the plug centres or jams depends on the funnel half-angle versus the friction coefficient. Neither is set. **No friction coefficient and no half-angle are declared.** Both are unresolved. Their numbers need Gate 2/3 evidence.
- Geometric capture bound from the declared plug size: the plug radius is 4 mm, so a lateral offset must be smaller than the funnel mouth radius minus 4 mm. The mouth radius is not declared. The measured capture window must come from sweeps (CPL-006).
- Roll alignment: the two flats. They only allow two angles and give no roll-centring force beyond the flat flanks.

This is a statement of a plausible geometric principle, not evidence. The protocol leaves the judgement to an independent reviewer.

## 9. Self-check against the corpus

Author's quick check against `docs/originality/reference-corpus.md`. It is **not** the Q61 review: it is not independent, it uses the corpus descriptors (summaries) and not primary sources, and ratings are my judgement only. The Q61 review must be done by someone else.

| Reference | D1 geometry | D2 coupler | D3 actuation | D4 assembly | D5 visual | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| A1 Big Hero 6 microbots (F1) | none | none | none | low | not rated | Not needle-like or particle-like; chain use is generic. No swarm silhouette. D5 depends on final visuals |
| B1–B4 fictional swarms (F2) | none | none | none | low | not rated | No shared distinctive feature found. Corpus entries are secondary descriptions |
| C1–C3 M-TRAN | moderate | low | moderate | moderate | not rated | Shares "two halves with a joint" and chain/lattice use. Differs: single joint, offset Z-link, no magnets, plug and socket, 180° fold |
| C12 PolyBot | low | low | moderate | moderate | not rated | Both single-DOF chain modules. Differs: not cubic, offset pivot, different end connectors |
| C14 CKBot | low | low | moderate | moderate | not rated | Servo-driven single joint is shared. Differs: pivot offset, no cube, mechanical hooks |
| C13 SuperBot | low | low | low | moderate | not rated | |
| C22 Sambot | low | low | low | low | not rated | |
| C4 ATRON | none | low | low | low | not rated | Hook-based connectors are shared in kind (low) |
| C5 SMORES-EP | none | none | low | low | not rated | |
| C7, C8 M-Blocks | none | none | none | none | not rated | |

- **Moderate cells and the differentiation they need** are the M-TRAN D1, D3, D4, PolyBot D3, D4, CKBot D3, D4 and SuperBot D4 cells. The notes above give what differs; the reviewer decides if that is enough.
- **No cell is rated high in this check.** Two-high-against-one-reference and F1-high rules are not triggered by my ratings, which counts for little because of the independence rule.
- **Exclusions (Q62 §3):** *cube with an internal flywheel* — not present (no cube, no flywheel; the only moving part is the servo). *Needle- or particle-like silhouette* — not present: stowed 39 × 32 × 30 mm, deployed 57 × 32 × 30 mm, aspect about 1.8 to 1 (compare a dense black needle). Both to be recorded by the reviewer.
- **Family check:** an elongated two-segment body, one revolute joint, couplers at the segment ends. It is "elongated" by a modest ratio only (§12 R9).
- **D5 (visual identity):** no visual design exists, so it is not rated. Q61 §7 requires a separate final-visuals review.
- The corpus lists PolyPod and several others only as partly verified. Nothing found suggests overlap, but the corpus is not exhaustive and this makes no claim of absolute originality.

## 10. Expected Gate 1 outcomes (my own checks, not the evaluator)

| Item | Expected | Reason |
| --- | --- | --- |
| G1 | pass (55.50 mm) | script replica; confirm with the registered evaluator |
| G2 | pass | no component interference; every box in one cavity; assembly statement present. Shell boxes are placeholders (§4 note) |
| G3 | **unresolved** | components 9 and 10 uncited; several estimates in mass, dimension, power |
| G4 | mass pass; power pass (9 594 ≤ 13 875 mW); endurance reported only | the item is `unresolved` if the evaluator reads any estimate as a missing input; the protocol does not say |
| G5 | **expected fail (protocol artifact)** | the COM test uses the declared component poses, which are in the stowed layout. In the stowed layout segment B's contents sit at y −9 to −22, so the computed COM is (12.3, −9.1) mm. The unit's chain footprint reaches only y = −8 on that side, so the COM falls outside the support hull. With B's contents moved to their deployed positions the COM is (0.1, 7.2) mm, inside the footprint. I did not change the declaration to dodge this. Declaring the deployed layout for the components and cavity-b together would pass G5 but mix frames with the stowed body boxes |
| G6 | **unresolved** | no independent retention review record |
| G7 | **unresolved** | no Q61 review |
| G8 | **unresolved** | no Q61 review |

Overall: `fail` if the evaluator confirms G5 as above (fail dominates unresolved, Q62 §2); otherwise `unresolved`. Never `pass` at v1.

## 11. Protocol observations (for the lead; not changes)

1. **G5 COM versus G2 layout.** A folding body has two component layouts. The protocol takes one pose set for both tests (see G5 above).
2. **Shell mass has no valid box.** G2 needs every component box inside a cavity, and G4 needs shell mass in the budget. A shell cannot lie inside its own cavity. I used 1 mm lumped placeholder boxes in cavity corners for shell-a and shell-b, and marked their dimensions as estimates.
3. **Endurance formula** appears to carry a stray factor of 1 000 (§5.2).
4. **Placeholder URL.** G3 counts a component as uncited only on a malformed source. A well-formed placeholder URL passes the format test. I relied on the `estimate` bases and the text `UNCITED` to keep G3 unresolved. A reviewer should check the two `invalid.example` entries.

## 12. Risks and unknowns

| ID | Risk or unknown | Effect |
| --- | --- | --- |
| R1 | Packing margin is tiny (0.45 mm servo-to-wall, zero spare length in the latch and pin stack). Several placeholders (controller thickness, pin barrel, latch size) could break it | G2 or assembly would fail once real sizes replace placeholders |
| R2 | Mobility. A single-joint unit has no wheels, legs or reaction wheel. How a unit approaches a neighbour on the tabletop is not designed. Friction-driven inchworming is plausible but unevaluated | Docking may only be possible with help from other units. Gate 2 may fail it |
| R3 | The inner ends must be rounded about the pivot (radius 8 mm) so B can sweep past A. Zero clearance at the closest approach, and the servo's rear corners (8.4 mm radius) poke outside that arc. Boxes in the declaration hide this | Fold may jam, or the shell must be thicker, or the servo moved |
| R4 | The servo's output axis direction on the 25.25 mm dimension is assumed. If wrong, the hinge geometry changes | Redesign |
| R5 | Servo mass: 13.2 g from one page, 9 g elsewhere. No manufacturer datasheet read | Mass budget off by 4 g |
| R6 | Battery "15C" not marked continuous. Boost converter efficiency and output rating unknown. The 5 V servo stall draw may exceed what the converter and cell deliver. SMA release current heats the cell | G4 power could fail |
| R7 | Servo bus interface hardware (half-duplex buffer) is not listed. Controller thickness unknown | Packing and mass |
| R8 | BLE has no short range. The contactless channel does not match Q33's "short-range" wording without a range limit | Communication model unresolved (COM-007, COM-008) |
| R9 | Aspect ratio is only about 1.8 to 1 deployed. "Elongated" is modest | Family-B reviewer judgement |
| R10 | SMA latch: thermal cycling, the 4 % strain limit, and slow cool-down limit release rate. Release under load is unproven | Gate 2/3 |
| R11 | PA12 groove under constant hook load can creep. PA12 hook wear and friction are unknown | Retention over time is unknown |
| R12 | One-sided joint travel (0° to 180°). S-curves require unit rolls. Curvature change per unit and swept volume at intermediate angles are not checked | Q31 chain bending may be harder than planned |
| R13 | Deployed size (57 mm long, 68 mm enclosing sphere) and ENV-003 | Interpretation of the 30–60 mm class |
| R14 | Part availability and prices not checked. Parts could be discontinued | Procurement |
| R15 | 3D-printed PA12 shell tolerances at 1.5 mm walls were not checked | Fit and stiffness |

## 13. Unresolved items (complete list)

1. Controller mass and thickness; boost converter mass and output rating; pogo pin mass and size; latch assembly mass and size; wiring mass; SMA wire density. All declared as placeholders or `estimate`.
2. Servo manufacturer datasheet, output-axis direction, true mass (13.2 g versus 9 g), and efficiency of the 5 V rail.
3. Servo bus interface parts.
4. Funnel half-angle, mouth radius, friction coefficient, hook geometry, spring rate, holding force, release force, release time.
5. Average power values, so the endurance figure.
6. Intermediate-angle swept volume and inner-end clearance.
7. Locomotion and approach strategy.
8. Contactless range and the actual BLE channel model.
9. The independent retention review (G6) and the Q61 originality review (G7, G8).
10. G3: each placeholder must be replaced by a cited value, which needs a new declaration version.
11. Deployed size against ENV-003.

## 14. Honest summary

The envelope fits with 4.5 mm to spare and the packaging has no overlaps. That is all this paper pass shows. The design depends on a stack of placeholders, a pivot clearance that is zero on paper, and no plan for how a single-joint unit reaches its neighbour. I do not regard it as feasible yet. The Z-link idea is the part I would keep if it is revised.
