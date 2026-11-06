# cand-a v2: hexagonal-prism tumbler with lift ring and roll-in peg coupler (Family A)

Authors: Claude Opus 5.5 (engineering lead, all design decisions) with Claude Sonnet 5.5 (cand-a v2 implementation agent: derived values, files, this dossier). Date: 2026-11-06. Label: **exploratory**. Declaration: `declaration.json` (schema_version 1, candidate_version 2, SHA-256 `b7a6e94d20b91df9e1bd27ba3af124ba66237d7fd0585594b87084e79812e54c`). File layout follows Q65: `declaration.json` is the current version, the v1 bytes are kept in `declaration-v1.json`, the v1 dossier is `dossier.md` (where it says `declaration.json` it means `declaration-v1.json`), and this file is `dossier-v2.md`. No v1 file was edited.

This is a paper-gate dossier (Q38 Gate 1). It does not show that any mechanism works. Every number below comes from a cited source, from an explicit derivation, or is marked **UNRESOLVED**. An attractive layout is not evidence that a mechanism works. Where a number is an assumption it is called one.

## 1. Result at a glance

Official evaluator (`zig-out/bin/kinigami-gate1`, pinned toolchain build of the current tree, code revision 3c2399d plus the uncommitted v2 files, working tree dirty). **No v2 review records exist yet** (no `retention-review-v2-r*.md`, no `originality-review-gate1-v2-r*.md`), so G6 to G8 cannot pass.

| Item | Outcome | Why |
| --- | --- | --- |
| G1 stowed sphere | pass | D = 58 181.29 µm (Welzl radius 29 090.644, certified radius 29 090.644, centre at the origin), limit 60 000 µm, margin 1.819 mm. The sphere is set by the hexagon corners (√(25.5² + 14²) = 29.09 mm); the lobe tip (28.61 mm) and peg tip (27.10 mm) lie inside it |
| G2 packaging | pass | 1 326 pairs tested, 0 interfering, 0 capped, 0 boxes outside the shell (3 cavity primitives). **Caveat:** boxes are rectangular stand-ins for round and toothed parts, several masses are upper bounds, and the gear train, yaw worm, SMA run and harness are not routed |
| G3 evidence | pass | every component cited, every basis source or derived, derived masses within 1 mg |
| G4 budgets | pass | mass 36 550 mg declared and summed; peak 8 899 mW against 19 425 mW; average 2 684 mW; endurance 1 736.96 s (about 29 min, reported only, not meaningful beyond a lower bound; the protocol-literal figure is 1 736 959.76 s) |
| G5 chain | pass | 2 sites, 3-unit straight chain, roll 0 used, contact, support and no-interference checks pass |
| G6 | unresolved | retention-review record missing |
| G7, G8 | unresolved | originality review missing (section 12 is only the author's self-check) |

Overall evaluator outcome: **unresolved** (G1 to G5 pass; G6 to G8 unresolved because no independent reviews exist for v2).

Key numbers: stowed diameter **58.18 mm** (v1 59.06), declared mass **36.550 g** (v1 39.814 g), peak **8.899 W** worst case against a 19.425 W limit, average 2.684 W.

A first layout of this revision put the lift pinion into the M1 gearmotor (the evaluator reported pinion versus ring segment, motor and driver). The engineering lead judged that clash real and revised the lift drive geometry (pinion 14 T, M1 moved, 41 T:16 T spur pair, free parts repacked). The numbers here are for the revised layout. Nothing else was tuned to pass a gate.

## 2. Concept and family membership

Family A (Q62 s3): one rigid polyhedral body that moves by pivoting or rolling over edges, with couplers on faces.

- Body: a regular hexagonal prism, circumradius 25.5 mm, 28 mm long. One moving part inside the shell, a **lift ring** with one lobe in a slot around the girdle. The lobe reaches r = 28.5 mm, outside the hexagon outline: parked it points +z and its tip is part of the stowed envelope (section 3).
- Locomotion: the unit lies on a side face and rolls over a bottom hexagon edge onto the next face, one 60 degree step at a time, like a hexagonal log. The ring is turned by a 6 mm gearmotor through a spur pair and a pinion. The lobe tip presses on the table, lifts the trailing side until the centre of mass passes the leading edge, and gravity completes the step. Reversing the motor reverses the roll.
- Couplers (axial, on the two hexagonal end faces): a fixed 304 hexagonal **peg** on the head, and on the tail a receiver with a **roll-in channel**, a **yaw turntable**, a **dead-centre toggle keeper** and an **SMA pulse release**. A unit docks to a neighbour by rolling one step about its leading bottom edge so that the neighbour's peg slides along the arc channel into the receiver (section 7).
- Exclusions (Q62 s3): **not a cube**, no flywheel or reaction wheel, no magnet. 51 mm across corners, 44.2 mm across flats, 28 mm long, so no needle or particle silhouette.

## 3. Geometry: stowed and deployed

Frame: prism axis = body y (head end +y). Rest orientation identity (bottom side face F0 has normal -z). Hexagon vertices in the x-z plane at (±R, 0) and (±R/2, ±a).

| Quantity | Value | Basis |
| --- | --- | --- |
| Circumradius R | 25.500 mm | lead decision; v1 was 26.0. Reason: SLS tolerance margin on G1 (v1 margin 0.94 mm). Both pass; not tuned to a gate |
| Apothem a | 22.0836 mm | R·√3/2, derived |
| Axial length H | 28.0 mm | design choice (end plates at |y| 12 to 14, 2 mm thick) |
| Inner cavity | cylinder r = 20.0 mm, |y| ≤ 12 | design choice; wall radial thickness 2.08 mm at face centres |
| Girdle slot | |y| ≤ 1.75, cuts the walls fully | lift ring slot. The head and tail wall halves are joined by two PA12 posts, the end plates and the tail cap |
| Lift ring | PA12 annulus r 19.5 to 21.9, |y| ≤ 1.5, internal teeth module 0.3, 133 T, pitch r 19.95 (tips 19.65, roots 20.325) | lead decision |
| Lift lobe | PA12, radial r 21.9 to 28.5 (L = 28.5), tangential 4.0, axial 3.0, tip rounded r 2; parked pointing +z | lead decision |
| Head peg | 304 hex 4.0 across flats (4.619 across corners), 18 long, tip y = 27 mm, 13 mm beyond the head face | lead decision |
| Stowed enclosing sphere diameter | **58.181 mm** | evaluator, centre at the origin |

**Stowed:** the declaration models the hexagon as three overlapping boxes (half extents 12 750, 14 000 and 22 084 µm, rotated 0, 60 and 120 degrees about y), the lobe as a box (x ±2.0, y ±1.5, z 21.9 to 28.5; the rounded tip is ignored, so the box is an upper bound on the envelope), and the head peg as a coupler-role cylinder (r 2.31 mm, y 14 to 27). The hexagon corners at (r 25.5, y ±14) define the sphere (radius 29.09 mm); the lobe tip (28.61 mm from the centre) and the peg tip (27.10 mm) are inside it. The 1.82 mm margin is the room for SLS tolerance and is not a measured tolerance.

**Deployed (chain geometry):** the same boxes without cavities. Neighbour tail face sits at y = 22 mm of this unit (gap g = 8 mm from the head face at y = 14, 5 mm peg engagement). `site-head` is at (0, 22 000, 0) µm, `site-tail` at (0, -14 000, 0). Mating roll angles are 0 and 180 degrees (180 fails the table check because the parked lobe would then point into the table; 0 is the operating mate). The lobe sweeps out of the hexagon when it works (section 6). That swept volume is not constrained by Q12; the lobe is declared in its parked position.

## 4. Q12 packaging and component list

Cavity primitives: `cavity-main` (cylinder r 25.501 mm, half height 14 mm, axis y), `cavity-girdle` (r 29.0 mm, half height 1.75 mm, holds the lobe), `peg-envelope` (r 3.1 mm, y 13.9 to 27.1, holds the protruding peg). Each component box must lie in one of them (evaluator rule).

Component boxes and placement (body frame, mm) are in the declaration. Notable layout facts:

- Cell lies flat under the axis: x -15.5..15.5, y -11.9..8.1, z -11.2..-3.7.
- Controller (QT Py ESP32-C3) lowest: z -17.35..-11.65. IMU at z 2.23..4.77. Driver boards stand on edge at x ±16 (driver-1 x -17.4..-15.6, driver-2 x 14.6..16.4).
- M1 (lift motor) axis along y at x -4.0, z 12.18, output +y; the motor spur (41 T) and layshaft spur (16 T) sit in the plane y 9.6 to 11.1; the layshaft runs to y 1.8 and the pinion (y ±1.5) is at (x -2.484, z 17.676), 17.85 mm from the ring axis, 8 degrees off +z.
- M2 (yaw motor) axis along y at x 5.25, z 10; its worm is at y -10.3..-6.7 and meshes the sector on the yaw shaft.
- Tail receiver: cap halves x ±3.9..14.5, y -12..-8.5, yaw puck turning about body z through (0, -8.2), keeper above it, SMA run along the yaw axis.

Assembly access: the wall halves are separate parts so the ring can be dropped into the girdle slot; stack loaded along the axis with one end plate removed; no assembly sequence was verified (see risks).

### Parts (access date for every source: 2026-11-06)

| Component | Part | Source | Verified there | Caveats |
| --- | --- | --- | --- | --- |
| Structure (walls, end plates, ring, lobe, caps, puck, shaft, boss, posts) | EOS PA 2200 (PA12, laser-sintered) | [EOS PA 2200 data sheet](https://3dprinting.com/wp-content/uploads/2019/05/EOS-pa2200-white-datasheet-TDS.pdf) | PDF read: density 930 kg/m³, tensile strength 50 MPa, modulus 1 700 MPa | SLS dimensional tolerance **not cited**; fine features (0.3 module teeth, 0.8 mm walls) are not shown to be printable; strength beyond the coupler bearing checks not assessed |
| Metal parts (peg, keeper, worm, sector, spurs, layshaft, pinion, screws) | 304 stainless | [ATI 302/304/304L/305 TDS](https://www.atimaterials.com/Products/Documents/datasheets/stainless-specialty-steel/austenitic/ati_302_304_304l_305_tds_en1_v1.pdf) | density 7.90 g/cm³, yield 205 MPa, UTS 515 MPa | density of the Lee A313 spring wire and A2 screws taken as 304 (assumption) |
| Keeper spring | Lee LC 014A 01 S | [Lee Spring](https://www.leespring.com/product/compression-spring-lc014a01s-stainless-steel) | OD 0.12 in, wire 0.014 in, free 0.25 in, solid 0.088 in, rate 9.4 lb/in (1.646 N/mm), 6.29 coils, stainless ASTM A313 | page values only; spring wire volume 5.28 mm³ is derived |
| Fasteners | 4x M1.6 x 4 A2 pan head | [Westfield Fasteners](https://www.westfieldfasteners.co.uk/A2-ScrewBolt-PoziPan-M1.6.html) | dk 3.2, k 1.3 | lumped box, not at real screw positions; volume is an upper bound |
| Release SMA | Dynalloy Flexinol 0.004 in HT | [TCF1140 Rev H, SparkFun copy](https://cdn.sparkfun.com/datasheets/Components/General/TCF1140.pdf) | 6.45 g/cm³, 3.2 Ω/in, 143 g pull (at 172 MPa), about 200 mA for 1 s, cooling 1.1 s LT / 0.9 s HT, strain no more than 4 to 5 percent | the Dynalloy site was blocked, so a distributor copy was read; mass 0.18 mm³ x 6 450 = 1 mg |
| Harness | Alpha Wire 2841/7 30 AWG 7/38 PTFE | [DigiKey page](https://www.digikey.ca/en/products/detail/alpha-wire/2841-7-YL001/3708252) | OD 0.024 in (0.61 mm) | distributor page of manufacturer data; 300 mm assumed length; copper density from [Aurubis C11000](https://aurubis.com/dam/jcr:ec116d17-1541-419a-a897-ad31b4fa6c93/c11000-cu-etp-us.pdf) (8.9 g/cm³); lumped upper bound |
| Energy source | Grepow GRP8020030, 1S LiPo | [Grepow 15C table](https://www.grepow.com/high-discharge-rate-battery/15c-high-power-lipo.html) | row verified: 350 mAh, 15C, 3.7 V, "Max. Cont. Discharge Current" 5.25 A, 7.5 x 20.0 x 31.0 mm, 8.0 g | the page also has a series "45C" statement that contradicts the row; the row is used. Energy 0.35 Ah x 3.7 V = 4 662 000 mJ nominal, not usable |
| Controller | Adafruit QT Py ESP32-C3 (product 5405) | [Adafruit](https://www.adafruit.com/product/5405) | 22.0 x 17.8 x 5.7 mm, 2.1 g, ESP32-C3FN4 (Wi-Fi + BLE), "3.3V regulator with 600mA peak output" | no LiPo charger on the board; regulator dropout limits use near the end of charge; later revisions may use a different regulator; 2 220 mW is a bound (600 mA x 3.7 V), regulator quiescent not stated |
| IMU | Pololu LSM6DSO carrier (2798) | [Pololu specs](https://www.pololu.com/product/2798/specs) | 0.5 x 0.9 x 0.1 in, 0.6 g, supply current 1 mA | counted separately from the controller rail (conservative) |
| Drivers (two) | Pololu DRV8835 dual carrier (2135) | [Pololu specs](https://www.pololu.com/product/2135/specs); [dimension drawing](https://www.pololu.com/file/0J1536/drv8835-dual-motor-driver-carrier-dimensions.pdf); [TI DRV8835](https://www.ti.com/lit/ds/symlink/drv8835.pdf) | 0.4 x 0.7 in, 0.5 g, 1.2 A continuous / 1.5 A peak per channel, 0 to 11 V; profile height 1.8 mm (drawing dated 06 July 2018); IVM 2 000 µA max + IVCC 2 000 µA max | 4 mA x 3.7 V = 15 mW quiescent bound for each; the SMA channel runs at 1.336 A, above 1.2 A continuous, pulsed only |
| Motors (two) | Precision Microdrives 206-109, 6 mm planetary 136:1 | [datasheet](https://www.precisionmicrodrives.com/datasheets/206-109-V0.pdf) | 1.2 g, body dia 6 x 18.7 mm, shaft dia 2 x 3.6 mm, rated 3 V, max operating 3.6 V, rated 3 mN·m at 140 rpm, no load 240 rpm, stall 9 mN·m typical, max start current 230 mA, resistance 14.5 Ω, rated-load power 215 mW, 100 mm lead (in unit weight) | the datasheet is headed as a **sampling/target specification**; the motors must be PWM-limited to 3.0 V effective from a 3.7 V cell (a control constraint); peak 851 mW is the start current at 3.7 V (bound); average is the datasheet rated-load power, assuming continuous rated load |

Vendor product pages (Grepow, Adafruit, Pololu, DigiKey) are classed `datasheet` because the schema allows only `datasheet` or `publication`. A reviewer should treat that as a stretch. The evaluator does not fetch URLs; the cited values were read on 2026-11-06 and are checked by sampling at the gate record.

## 5. Mass and power budgets (reported)

**Mass (declared 36 550 mg, equal to the sum):**

| Group | mg | Basis |
| --- | --- | --- |
| 12 wall slabs (6 head half + 6 tail half) | 2 × 4 128 | derived: (hexagon area - π·20²) × 10.25 mm × 930 kg/m³ per half |
| 2 end plates | 2 × 3 142 | derived, solid hexagon x 2 mm (upper bound, peg hole and receiver relief ignored) |
| 12 ring segments | 876 | derived annulus r 19.5 to 21.9 x 3 mm |
| Lift lobe | 74 | derived, solid box (upper bound) |
| Tail cap halves (2) | 2 × 362 | derived, solid boxes (upper bound) |
| Yaw puck / shaft | 439 / 6 | derived PA12 (puck is a solid cylinder, upper bound) |
| Yaw sector | 160 | derived 304 (changed from PA12 by the lead, see section 10) |
| Peg boss, posts (2) | 100, 140 + 119 | derived |
| Head peg | 1 970 | derived 304, hex x length, groove ignored (upper bound) |
| Keeper (tongue, links, pins, spring) | 476 | derived 304, 60.3 mm³ |
| Yaw worm | 201 | derived 304 |
| M1 spur (41 T) / layshaft spur (16 T) / layshaft / pinion | 626 / 95 / 109 / 429 | derived 304, solid discs (upper bounds) |
| Fasteners (4) | 585 | derived 304, bounding volume (upper bound) |
| Release SMA | 1 | derived NiTi, 0.178 mm³ |
| Harness | 780 | derived copper, bounding volume (upper bound) |
| Cell | 8 000 | source |
| Controller / IMU | 2 100 / 600 | source |
| Drivers (2) | 2 × 500 | source |
| Motors (2) | 2 × 1 200 | source |

Many entries are solid-volume upper bounds, so the total is probably an overestimate for structure and an underestimate for anything not modelled (wiring routing, the gear details, any glue or lubricant, real screw count, the tail cap relief). Neither direction is quantified.

**Peak (worst case, all at once, per protocol s6):** controller 2 220 + IMU 4 + two drivers 2 × 15 + two motors 2 × 851 (max start current 230 mA x 3.7 V) + release SMA 4 943 = **8 899 mW**. Limit 3.7 V x 5.25 A = 19 425 mW. The SMA term is 3.7 V into 2.77 Ω (22 mm = 0.866 in x 3.2 Ω/in) = 1.336 A for about 1 s; an exact 2.7717 Ω gives 4 939 mW and the declaration keeps the slightly larger 4 943 as a bound. The Flexinol datasheet recommends about 200 mA for a 1 s pulse, so a real current-limited driver would draw far less, but the driver design is open (UNRESOLVED), so the full-voltage figure is declared. The 1.336 A also exceeds the DRV8835 1.2 A continuous rating (below the 1.5 A peak rating): pulsed use only.

**Average:** controller 2 220 + IMU 4 + drivers 30 + motors 2 × 215 + SMA 0 (pulse about 1 s, rare) = **2 684 mW**.

**Endurance (reported only, never gates):** 4 662 000 mJ / 2 684 mW = 1 737 s (about 29 min). This assumes the controller draws its regulator's peak limit all the time and both motors run at rated load all the time, so it is a lower bound on a quantity whose duty cycle is undecided. It is not a mission claim. The evaluator also prints 1 736 959.76 s ("protocol literal", the extra factor 1 000 flagged in Q63).

## 6. The lift-lobe mechanism

M1 (3 mN·m rated at 140 rpm, 9 mN·m stall) turns a 41 T spur (module 0.2, pitch r 4.1) that drives a 16 T layshaft spur (pitch r 1.6, centre distance 5.70). The layshaft carries a 14 T pinion (module 0.3, pitch r 2.1, tip r 2.4) at (x -2.484, z 17.676), 17.85 mm from the ring axis, that meshes the ring's 133 internal teeth (pitch r 19.95). Speed ratio ring/motor = (16/41)·(14/133) = 1/3.707, so torque is multiplied by 3.707. Tooth counts are integers (133 T x 0.3/2 = 19.95, 14 T x 0.3/2 = 2.1, centre distance 17.85; 41 T x 0.2/2 = 4.1, 16 T x 0.2/2 = 1.6). Tooth strength, backlash, profile and contact ratio are **not assessed**. The pinion tip reaches 17.85 + 2.4 = 20.25 mm, 0.075 mm inside the ring root circle (20.325).

Ring torque available (efficiency 0.9 per spur stage, 2 stages: 0.81): **9.01 mN·m rated, 27.0 mN·m at stall.** Ring speed 140/3.707 = 37.8 rpm, so one 60 degree step takes **0.265 s** at rated load (assuming rated speed is sustained).

**Quasi-static lift** (R 25.5, L 28.5, declared mass 36.550 g so W = m g = 0.3584 N; rigid body, frictionless pivot, script `analysis_v2.py`):

- Tipping needs L > R: 28.5 > 25.5, true. Tip-to-pivot distance at tipping sqrt(L² - R²) = 12.73 mm.
- The lobe touches the table when the body is flat and the lobe is 39.21 degrees from the bottom normal (acos(a/L)). Ring sweep from the parked +z position to first contact is 140.8 degrees. During the push the ring turns 42.7 degrees (to 3.5 degrees on the other side of the bottom normal at tipping); of each 60 degree step, 17.3 degrees remain after tipping. Continuous ring rotation gives continuous rolling; every 60 degrees of ring rotation is one step.
- Centre of mass (mass-weighted box centres) is (0.015, 0.756, -0.986) mm, i.e. 1.0 mm below the geometric centre. Including this offset changes the torques below by less than 1 percent between roll directions. The weight moment about the leading edge at the start is W·R/2 = 4.57 mN·m.
- Peak ring torque required (at the start of contact, where the tip normal force is highest; tip sliding friction mu has no moment about the pivot because tip and pivot are at table height, but it adds mu·N_T times the lobe-axis height to the ring torque):

| Tip friction mu | Peak ring torque (W·mm) | mN·m | Ratio rated (9.01) | Ratio stall (27.0) |
| --- | --- | --- | --- | --- |
| 0 | 7.47 W·mm | 2.68 | 3.37 | 10.1 |
| 0.15 | 8.84 | 3.17 | 2.84 | 8.5 |
| 0.5 | 12.04 | 4.32 | 2.09 | 6.3 |
| 1.0 | 16.62 | 5.96 | 1.51 | 4.54 |

- Maximum tip normal force is 0.414 W. The pivot holds horizontally while N_T <= W/2 (equal friction coefficients), true.
- Ring tooth tangential force at the pitch circle: 0.134 N at the frictionless peak and 1.36 N at motor stall. A rough Lewis estimate (width 3 mm, module 0.3, form factor Y = 0.3, **assumed, not cited**) gives about 5 MPa at stall against 50 MPa. Lobe root bending stress at the peak normal force (lever 6.6 mm, section 4 x 3 mm) is 0.12 MPa.
- **Clearance after tipping.** If the ring stops after tipping, the lobe tip rises monotonically from the table (to 6.4 mm at the end of the fall, computed for a rigid fall with the ring fixed relative to the body). If the ring keeps turning at a uniform rate (my assumed distribution of the remaining 17.3 degrees over the fall), the tip rises only to about **0.69 mm** at 44.8 degrees of body angle and returns to the table at 60 degrees, which is the next step's contact. **Lead decision (control rule):** the ring is not turned continuously through the fall. After tipping (seen by the IMU) the ring stops until landing is detected, then turns the remaining 17.3 degrees to the next contact. With the ring stopped the tip clearance is 6.4 mm. Continuous rotation is not a declared operating mode. The real fall dynamics are not solved and belong to Gate 2. The step time therefore adds the fall time (not computed) to the 0.265 s push.
- Landing energy m g (R - a) = 0.3584 N x 3.416 mm = **1.225 mJ**.
- Parked: the lobe points +z (away from the table) when the unit rests on F0, so it does not carry load at rest.
- Reversal: yes (reverse the motor). **Steering and axial motion are not provided:** the body rolls only perpendicular to its axis. Self-indexing: the IMU sees tilt onset when the lobe meets the table; there is no dedicated ring sensor, so the ring angle is open-loop (limitation).
- Friction: the ring runs on flanges in grooves of the wall-half faces (plain PA12 bearing); its friction is not quantified, and the 9.01 mN·m figure does not subtract it. UNRESOLVED.

## 7. The coupler (design-guidance 4.2)

Two axial couplers. Head = hex peg, tail = receiver. Sites: head (0, +22 mm, 0) normal +y; tail (0, -14 mm, 0) normal -y. No lateral couplers (no branching, no lattice).

**Align.** Two circular-arc slots in the tail cap halves (radius 25.5 mm, centred on the two bottom vertices at (∓R/2, -a), running from the mid-height vertices (±R, 0) to the face centre; width 5.4 mm; depth from the tail face 5.5 mm; mouths flared 45 degrees x 1.5 mm). Why arcs: when unit B rolls one step about its leading bottom edge, a neighbour's peg on the common axis moves, in B's frame, along exactly this arc, keeps its direction (parallel to y) and turns 60 degrees about its own axis (hex symmetry), so B can roll into a docked pose using its own lift drive and gravity as the closing force. Either unit can leave by rolling the other way about the same edge. Nominal windows (geometric estimate only, CPL-006 says the window is measured by sweeps and never declared): slot width 5.4 against 4.619 across corners gives 0.39 mm per side; with the flare, lateral ±(0.39 + 1.5) = **±1.89 mm** at the mouth; height ±0.39 mm; heading ±atan(0.39/5) = **±4.46 degrees**; roll any multiple of 60 degrees; axial ±0.8 mm (tongue 0.8 mm in a 1.6 mm groove with 0.4 x 45 degree chamfers), which is a lane precondition. Final lateral seating by the tongue V-notch (notch 3.1 mm for the 3.0 mm groove, mouth 6.0 mm, 30 degree half angle): (6.0 - 3.1)/2 = ±1.45 mm. The peg tip is chamfered 0.5 x 45 degrees. No cone is used (v1's cone is dropped). SLS tolerance is not cited, so all windows are nominal. UNRESOLVED.

**Latch.** The peg's annular groove (dia 3.0, 1.6 wide, centred 2.5 mm inside the neighbour's face, i.e. at y 24.5) is closed by a 304 tongue (0.8 mm thick) driven by a two-link dead-centre toggle (links 0.8 x 1.5 x 5 mm, three pins dia 1 x 4) biased by the Lee LC 014A 01 S spring at 0.2 mm installed compression: 1.646 N/mm x 0.2 mm = **0.329 N**. The seat is a half-hex cup in the yaw puck. Closing is passive: an edge-triggered trip lever in the cup bottom, pushed by the arriving peg, moves the knee past centre. Work needed at most 0.82 N x 0.3 mm = **0.247 mJ**; landing energy is 1.225 mJ (ratio 5.0), but the fraction delivered to the trip is **UNRESOLVED** (dynamic, Gate 2). The snap force 0.33 to 0.82 N must exceed the other unit's head-end friction mu W/2 (0.179 N at mu = 1): ratio 1.84 at the low end of the spring range, which is thin and dynamic.

**Transmit force.** Design loads (Q31 item 6, CPL-009), all derived from W = m g = 0.3584 N and a table friction coefficient bound mu <= 1 (provisional bound; Q47 sets the law, no coefficient is decided):

| Load | Value | Carried by | Stress | Ratio to limit |
| --- | --- | --- | --- | --- |
| axial tension 4·mu·W | 1.434 N | tongue on groove shoulders (area 2 x 0.5 x 1.5 = 1.5 mm²) | 0.96 MPa | 0.0047 of 304 yield 205 MPa |
| axial tension | 1.434 N | tongue shear (2 x 0.8 x 1.5 = 2.4 mm²) | 0.60 MPa | 0.0051 of 0.577 x 205 = 118 MPa (von Mises shear yield, derived) |
| axial tension | 1.434 N | tongue on PA12 puck wall (7 x 3 = 21 mm²) | 0.068 MPa | 0.0014 of PA12 50 MPa |
| torsion about y, one idle neighbour tipped: W·R/2 | 4.57 mN·m | hex flats on PA12 cup, force M/(2 x 1.5 mm) = 1.52 N on 1 x 5 mm² | 0.30 MPa | 0.006 of 50 MPa |
| torsion, two neighbours: 2·W·R/2 | 9.14 mN·m | same | 0.61 MPa | 0.012 |
| pitch bending W/2 x 36 mm | 6.45 mN·m | couple on the cup, arm 5 mm (engagement depth, my assumption), 1.29 N on 1 x 5 mm² | 0.26 MPa | 0.005 |
| yaw (section 10) | up to 32.8 mN·m | worm and sector, not the peg | see below | |

All coupler bearing stresses are far below the limits, so strength is not what limits this coupler at these loads (bearing areas are the spec's own and are small; stress concentrations at chamfers, notches and the 3.0 mm groove, creep of PA12 and tolerance stack-up are not evaluated). The toggle carries none of the peg loads directly: the tension path is peg groove shoulder to tongue to puck wall. The toggle links see only the component of the tongue force along their axis, and at dead centre the load line passes through the link pins, so no moment acts on the knee and the peg loads cannot back-drive it. The dead-centre geometry's dimensions (link pin positions, over-centre distance, stop) are not otherwise specified in the declaration. UNRESOLVED.

**Detach.** An SMA pulse pulls the toggle knee 0.3 mm past centre, then the spring snaps it open and it stays open unpowered. Force needed at the knee <= 0.329 + 1.646 x 0.3 = **0.823 N**. Flexinol 0.004 in recommended pull 143 g = 1.402 N (173 MPa on 0.00811 mm²), margin **1.70**. Stroke at 4 percent strain of a 22 mm wire = 0.88 mm against 0.3 mm needed, margin **2.93**. Pulse energy at the declared full-voltage bound about 4.9 J (0.1 percent of the cell) per release. The wire runs along the yaw axis from the keeper knee up through the hollow yaw shaft to an anchor at z = 19 mm, so yaw does not change its length. Heat, cycle life, cooling time (0.9 to 1.1 s per the sheet) and pulse current limiting are UNRESOLVED. The release acts only on the unit's own receiver and needs no help from the neighbour.

**Data.** BLE only (ESP32-C3), no through-coupler contacts. Range, occlusion in a chain and latency are UNRESOLVED. COM-008 stays open.

**Power.** No power transfer (isolated baseline of Q34). PWR-001 optional, not provided.

## 8. Passive retention when unpowered (CPL-009, Q11)

`requires_power_to_hold = false`, `mechanism_kind = geometric_interlock`. Components: keeper, yaw-puck, head-peg, release-sma. With the toggle at or past dead centre and the spring biasing it closed, the tongue holds the peg in its groove with no power; the hex peg in the half-hex cup carries torsion; nothing is powered to hold. Only release is powered, and bounded independent release is declared true (the unit's own SMA pulse). What is **not** shown: the dead-centre geometry (over-centre distance, stops), the friction in the toggle pins and the puck bearing, and whether the keeper stays closed under vibration and impact. Those are Gate 2 matters. The loaded tests of CPL-009 also remain. In the closed state the only energy storage is a 0.33 N spring, which is weak against any tolerance error in the toggle; if the toggle is not actually past centre the lock holds only by the spring, not geometrically. UNRESOLVED.

## 9. Pre-alignment justification (CPL-005, Q36)

Alignment is geometric, passive, and has three parts (all declared as `geometric_guide`): the roll-in channel (nominal windows in section 7), the tongue V-notch seating (±1.45 mm, needs snap force above head-end friction, 1.84x at low spring force and mu 1), and the hex peg in the half-hex cup with a 0.5 x 45 degree tip chamfer (six equivalent roll positions every 60 degrees). Pre-alignment forces come from sliding contact, gravity, B's own lift drive and table friction. There is no attractive force, so a unit that is not driven does not self-dock. Docking needs a common lane: axial error <= about 0.8 mm and heading <= about 4.5 degrees. The capture window is not claimed (CPL-006) and must be measured by sweeps. A reviewer should expect G6 to be justified only on paper.

## 10. Chain bending (Q31) resolution

v1 had no way to bend a chain. v2 adds a **yaw turntable** in the tail receiver: the puck turns about body z through (0, -8.2), 5.8 mm inside the tail face, driven by M2 through a single-start worm (module 0.3, OD 3.0, pitch dia 2.4, lead angle atan(0.3/2.4) = 7.13 degrees) into a 304 stainless sector (pitch r 4.05, module 0.3, 27 teeth per turn, ratio 27:1, ±21.5 degrees of sector, working range ±12 degrees, hard stops ±15 degrees).

- **Face clearance.** With pivot inset p = 5.8 mm, the end faces clear when g >= (p + R sin b)/cos b - p: 5.55 mm at 12 degrees and **7.04 mm at 15 degrees**. The gap g = 8 mm gives 0.96 mm of margin at 15 degrees. The peg at the tail face plane sweeps p·tan b = 1.23 mm (12 degrees) and 1.55 mm (15 degrees); the face opening is relieved to ±4.2 mm (x) around the centre (the relief is not modelled in the end plate, whose mass is solid).
- **Torque.** Available at the puck: rated 3 mN·m x 27 x worm efficiency tan(7.13)/tan(7.13 + atan(0.15)) = 0.445 (at an assumed worm/sector friction coefficient of 0.15) = **36.1 mN·m**, stall 108.2 mN·m. Design load: dragging the two units on one side at table mu = 1 (bound): mu W (d1 + d2) with d1 = 5.8 + 8 + 14 = 27.8 mm and d2 = d1 + 36 = 63.8 mm (unit pitch 36 mm) = 32.8 mN·m. Ratio **1.10 rated, 3.29 stall at mu 1**; at mu 0.5 the load is 16.4 mN·m, ratio **2.20 rated, 6.59 stall**. At mu 1 the rated ratio is only 1.10, so the margin on this bound is thin.
- **Sector tooth load.** The tangential force at the pitch circle is 8.1 N at the mu 1 design load, 8.9 N at rated torque and **26.7 N at stall**. A rough Lewis estimate (width 2 mm, module 0.3, form factor Y = 0.3, **assumed, not cited**) gave 45, 49 and 148 MPa. Against PA12 (50 MPa) that failed at stall, so the lead changed the sector to **304 stainless** (yield 205 MPa): the same crude estimate is then 0.72 of yield at stall and 0.24 at the design load. Because Y is uncited the estimate is a flag, not evidence; tooth strength stays **UNRESOLVED**, and a stall-current limit on M2 is advisable.
- **Holding a bend.** The bend angle is held unpowered only if the worm self-locks, which needs a worm/sector friction coefficient of at least tan(7.13) = 0.125 (UNRESOLVED). It is classified as actively maintained unless shown.
- **When it works.** Bending works only while the chain rests on F0 or F3 (yaw axis vertical). A straight chain rolls as one hexagonal log when all units step together (common pivot edge line). Steering a single unit is not provided.

## 11. Risks and unknowns

1. **No steering or axial locomotion.** The body rolls only perpendicular to its axis. A chain can lengthen only by rolling in from the side.
2. **Docking by roll-in is a paper idea.** Impact dynamics, the trip energy fraction, capture windows and the ring-driven roll closing the toggle are all unresolved. The ring stops after tipping (control rule, section 6).
3. **PA12 ring teeth at module 0.3** (3 mm wide); print resolution and strength of SLS at that scale are not cited. The yaw sector is 304 after a crude tooth-stress flag (section 10).
4. **SLS tolerances not cited**, so every window and clearance is nominal. The 0.075 mm pinion tip to ring root clearance and the 0.15 mm spur pitch-face contact are well inside any realistic SLS tolerance on the box-scale details.
5. **Worm self-locking is conditional** on friction >= 0.125. **Yaw torque is only 1.10 times the mu 1 bound at rated motor torque.**
6. **Release SMA current.** The full-voltage bound of 1.336 A exceeds the DRV8835 1.2 A continuous rating; a real driver would limit current, but that is not designed. Heat inside a closed body is not assessed.
7. **Motors run from 3.7 V cell by PWM limited to 3.0 V effective**, and the PMD datasheet is a sampling/target specification. The QT Py regulator may vary by board revision, has 600 mA peak, no LiPo charger, and its dropout limits use near the end of charge.
8. **Lumped placements.** Fasteners and harness boxes are stand-ins at positions with no real screws or routing. Box approximations: peg root inside the plate and boss boxes, keeper inside the puck volume, meshing gears as overlapping squares.
9. **Assembly.** No sequence verified. The ring in the girdle slot, the gear train through the wall, the SMA through the hollow yaw shaft and the harness through a moving yaw puck are not shown assemblable.
10. **Strength** of the PA12 walls (2.08 mm at face centres) and the cut tail cap beyond the coupler bearing checks, and **heat**, are not assessed.
11. **Ring bearing friction** (PA12 flanges in grooves) is unquantified and not subtracted from the available torque.
12. **Mass** is a mix of upper bounds and omitted items; neither direction is quantified.
13. **Three-unit chain only**; the five-unit claim of Q31 is untested.

## 12. Author self-check against the originality corpus (NOT the official review)

This is the author's own check against `docs/originality/reference-corpus.md`. It is **not** the Q61 matrix, it is not independent (Q61 s4), and it does not count for G7 or G8. Identifiers follow Q65: entries added by Q64 are written Q64-C21 to Q64-C29; plain C21 to C23 are the section-C entries. Descriptor text in the corpus comes from abstracts and search summaries, and my comparison inherits that limit. Ratings use the Q61 anchors (N, L, M, H).

| Reference | D1 geometry | D2 coupler | D3 locomotion | D4 assembly | D5 visual | Note |
| --- | --- | --- | --- | --- | --- | --- |
| A1 BH6 microbots | N | N | N | N | N | Large single unit, flat-faced, no particle swarm, no magnetic legs |
| B1 Replicators | N | N | N | L | N | |
| **Q64-C21 CONRO** | L | **M to H** | N | L | L | **Originality-sensitive, see below.** Spring-closed latch released by an SMA wire, holds unpowered, gendered connector |
| **C7 M-Blocks / C8 3D M-Blocks** | L | L | **M** | L | L | Whole rigid body pivoting over an edge, now with an internal moving part acting on the ground |
| **Q64-C22 hexagonal electrohydraulic modules (Keplinger group)** | **M** | L | **M** | L | L | Hexagonal rolling body; search summary only |
| C11 Molecubes | L | L | N | L | L | |
| C12 PolyBot, C14 CKBot, C22 Sambot (section C) | L | L | N | L | L | Face dock plates; the hex peg with toggle keeper is a different form |
| C4 ATRON, C6 Roombots, C16 FreeBOT | N | L | N | L | N | |
| C18 Telecube, C19 Crystalline | N | L | N | L | N | |
| D1 Cubelets, C23 Blinky Blocks (section C) | L | L | N | L | L | Cubes with magnetic faces |
| C9 Kilobot | N | N | L | N | N | Leg-on-ground motion is the only link |

**Originality-sensitive changes the reviewer should look at first.** I list them; I do not argue them away.

1. **vs Q64-C21 CONRO (SMA-released latch on a grooved pin).** v2's release path is an SMA wire pulling a latch element out of a pin groove; the latch is spring-biased and holds unpowered. Differences I can state: the latch element is a 304 tongue on a **dead-centre two-link toggle** that is bistable (the SMA only pulls it past centre and the spring completes the motion), the peg is a **hexagonal** peg with an annular groove (the roll-in dock lets the *neighbour* push it in by *rolling*), the receiver includes a **yaw turntable** and **arc-shaped roll-in channels**, and the sleeve/ball-lock of v1 is gone. Similarities that remain: SMA release, spring-closed unpowered hold, pin-and-groove concept, head/tail gendering, and a hinged (yaw) joint at the connector. The v1 ball-lock plus SMA sleeve was already near this region (my v1 author self-check did not list CONRO, as it was not yet in the corpus; Q64 added it after run 1). I expect D2 to be at least moderate against CONRO and the reviewer may rate it high.
2. **vs C7/C8 M-Blocks.** v1's difference was a hexagonal prism with a ground-kick strut instead of a flywheel. In v2 the locomotion is a ring-mounted lobe pushing on the table: still a whole rigid body pivoting over an edge by an internal actuator. No flywheel and no magnet (Q62 exclusion 1 is not triggered), but the *idea* of a rigid body rolling over its own edges to dock with a neighbour is the M-Blocks idea. The roll-in dock (the unit rolls into the neighbour) is closer to M-Blocks-style face-to-face docking than v1's linear pin insertion was.
3. **vs Q64-C22 hexagonal modules (Keplinger group).** A hexagonal rolling body is the closest published geometry in the corpus. The prism here is mechanically driven by a gearmotor and a lobe, not electrohydraulic, but D1 and D3 should be re-checked against the primary source. I only had the corpus entry (a search summary).
4. **vs C12 PolyBot / C14 CKBot / Q64-C21 CONRO for the yaw joint in a chain.** A single-DoF yaw between units is a common reconfigurable-robot feature; here it is a turntable inside the coupler and works only on certain faces.
5. Other changes with originality relevance: the roll-in arc channels (no match found in the corpus, but the corpus is not exhaustive), and the lift ring itself (a ring with one lobe in a girdle slot, no match found).

- **Exclusion 1 (cube with internal flywheel):** not present.
- **Exclusion 2 (needle- or particle-like silhouette):** not present.
- **Family membership:** meets Family A (single rigid polyhedron with one internal moving part, edge pivoting, couplers on faces). The yaw puck and lift ring are internal moving parts; I judge the body still single-rigid for stowed geometry (nothing deploys beyond the lobe's step swing), but a reviewer should confirm that the Family A "single rigid body" reading survives the internal ring and yaw puck.
- **What the corpus cannot tell me:** whether a hexagonal log-roller with an internal ring lobe and a roll-in dock exists outside the corpus. Nothing here claims absolute originality.

## 13. Changes from v1

| Area | v1 | v2 | Why |
| --- | --- | --- | --- |
| Circumradius | 26.0 mm | 25.5 mm | G1 tolerance margin (v1 margin 0.94 mm, v2 1.82 mm); not a pass/fail tuning |
| Stowed D | 59.06 mm | 58.18 mm | consequence of the above plus lobe and peg |
| Locomotion | reserved volume only, kick strut not designed | lift ring with one lobe, M1 + 41T:16T spurs + 14T pinion + 133T internal ring, ratio 3.707, quasi-static torques computed | close v1's main gap |
| Coupler | ball-lock pin/bore + hex key, SMA sleeve release, 4 mm engagement | fixed hex peg, roll-in channel, yaw puck, dead-centre toggle keeper, SMA pulse release, 5 mm engagement, gap 8 mm | docking by rolling, passive closing, chain bending |
| Chain bending | not provided | yaw turntable ±12 deg working | Q31 |
| Alignment | conical lead-in + hex key (cone) | roll-in arc channel, V-notch seating, hex peg chamfer; cone dropped | different docking motion |
| Retention | spring_preload | geometric_interlock (toggle); toggle adds a bistable state | |
| Controller | Seeed XIAO nRF52840 Sense, mass/power estimate | Adafruit QT Py ESP32-C3 + Pololu LSM6DSO, mass and power sourced/derived | v1 had estimate bases |
| Driver | Pololu DRV8838 single, mass/thickness not stated | two Pololu DRV8835 dual carriers, mass/thickness sourced | |
| Motor | Pololu 150:1 micro metal gearmotor, 9.5 g | two Precision Microdrives 206-109 6 mm planetary, 1.2 g each | smaller, two needed |
| SMA | two wires, mass 0, estimated | one wire, mass derived, power derived | |
| Fasteners, harness | zero-mass bucket | counted components (4x M1.6 screws, 300 mm wire) | v1 sums were lower bounds |
| Mass | 39.814 g (lower bound) | 36.550 g | |
| Peak power | 2 861 mW (lower bound) | 8 899 mW | |
| Endurance | 29 137 s (not meaningful) | 1 737 s (also not a claim) | |
| G3 | unresolved (13 estimate flags) | pass | |
| Evidence date | 2026-11-04 | 2026-11-06 | |

## 14. Unresolved list (for the lead)

1. SLS PA12 dimensional tolerance (every window and clearance is nominal).
2. Trip energy fraction and the closing dynamics of the roll-in dock.
3. Capture window (measured by sweeps, CPL-006).
4. Dead-centre geometry of the toggle (link pin positions, over-centre distance, stops) and keeper behaviour under shock and vibration.
5. Worm/sector friction coefficient (>= 0.125 for self-lock); yaw torque margin at table mu 1 is 1.10 at rated; sector tooth strength (304 sector, crude assumed-Y estimate 0.72 of yield at stall).
6. Ring bearing friction; real fall dynamics and the fall time per step (the ring-stop rule avoids the 0.69 mm clearance of continuous rotation).
7. Tooth strength, backlash, profile and contact ratio of all gears (module 0.3 PA12 ring; module 0.2 and 0.3 steel spurs, pinion and sector).
8. SMA driver design (current limit, switch), heat, cycle life; DRV8835 channel above its continuous rating during the pulse.
9. Motor PWM voltage constraint, the PMD 206-109 sampling-specification status, QT Py regulator variance and charging.
10. Lumped placements (fasteners, harness), box approximations, and assembly sequence.
11. PA12 wall and tail-cap strength beyond the coupler bearing checks; heat generally.
12. BLE range, occlusion and latency; through-coupler data and power (none declared).
13. Lateral couplers, steering, axial locomotion, five-unit chain (Q31).
14. Retention-review and originality-review records for v2 (independent reviewers); the author self-check above is not the review.
