# cand-a v3: hexagonal-prism tumbler with lift ring and roll-in peg coupler (Family A)

Authors: Claude Opus 5.5 (engineering lead, all design decisions) with Claude Sonnet 5.5 (cand-a v3 implementation agent: derived values, files, this dossier). Date: 2026-11-06. Label: **exploratory**. Declaration: `declaration.json` (schema_version 1, candidate_version 3, SHA-256 `0025a534f9fc2496d8010e97ad69754485b5e671de23a8261ec11237e16fa1bb`). File layout follows Q65: `declaration.json` is the current version, the v1 and v2 bytes are kept in `declaration-v1.json` and `declaration-v2.json`, the v1 dossier is `dossier.md`, the v2 dossier is `dossier-v2.md` (where they say `declaration.json` they mean the matching preserved file), and this file is `dossier-v3.md`. No v1 or v2 file was edited.

This is a paper-gate dossier (Q38 Gate 1). It does not show that any mechanism works. Every number below comes from a cited source, from an explicit derivation, or is marked **UNRESOLVED**. An attractive layout is not evidence that a mechanism works. Where a number is an assumption it is called one. v3 answers the independent v2 reviews (`retention-review-v2-r1.md`, `originality-review-gate1-v2-r1.md`) and Q67; section 12 maps each finding to what changed.

## 1. Result at a glance

Official evaluator (`zig-out/bin/kinigami-gate1`, pinned toolchain build, code revision 3f6d1ec plus the uncommitted v3 files, working tree dirty). **No v3 review records exist yet** (no `retention-review-v3-r*.md`, no `originality-review-gate1-v3-r*.md`), so G6 to G8 cannot pass.

| Item | Outcome | Why |
| --- | --- | --- |
| G1 stowed sphere | pass | D = 58 181.29 µm (Welzl radius 29 090.644, certified radius 29 090.644, centre at the origin), limit 60 000 µm, margin 1.819 mm. The hexagon corners (√(25.5² + 14²) = 29.09 mm) set the sphere; the lobe tip (28.61 mm) and the peg tip (√(2.31² + 28.5²) = 28.59 mm) lie inside it |
| G2 packaging | pass | 2 145 pairs tested, 0 interfering, 0 capped, 0 boxes outside the shell (3 cavity primitives). **Caveat:** boxes are rectangular stand-ins for round and toothed parts, several masses are upper bounds, and the gear train, yaw worm, keeper four-bar and harness are not routed (section 4) |
| G3 evidence | pass | 66 components, every one cited, every basis source or derived, derived masses within 1 mg |
| G4 budgets | pass | mass 41 849 mg declared and summed; peak 4 807 mW against 19 425 mW; average 2 899 mW; endurance 1 608.14 s (about 27 min, reported only; the protocol-literal figure is 1 608 140.74 s) |
| G5 chain | pass | 2 sites, 3-unit straight chain, roll 0 used, contact, support and no-interference checks pass |
| G6 | unresolved | retention-review record missing |
| G7, G8 | unresolved | originality review missing (section 13 is only the author's self-check) |

Overall evaluator outcome: **unresolved** (G1 to G5 pass; G6 to G8 unresolved because no independent reviews exist for v3).

Key numbers: stowed diameter **58.18 mm** (v2 58.18), declared mass **41.849 g** (v2 36.550 g), peak **4.807 W** worst case against a 19.425 W limit (v2 8.899 W), average 2.899 W. The mass rises by 5.3 g, of which 3.29 g is the 304 internal-gear band (a lead decision).

Statements that need to be read together with the table:

- The first v3 spec put the keeper's crank axis 11.25 mm from the yaw axis with an 8.0 mm link and a rocker pivot on the yaw axis. That linkage cannot close (the link end cannot reach the folded dead centre; the crank could rock only 94.5 degrees instead of rotating through both dead centres). The lead replaced it by the four-bar of section 7. All keeper numbers here are for the four-bar.
- **Release under the full mu = 1 bound tension needs more than the rated torque of M3** (section 7). This is stated, not hidden: rated M3 torque is 0.60 times the requirement, stall is 1.81 times.
- **Bending at rated yaw torque holds only for table mu up to about 0.96** (section 10), so the mu = 1 bound is just outside the operating envelope for bending.

## 2. Concept and family membership

Family A (Q62 s3): one rigid polyhedral body that moves by pivoting or rolling over edges, with couplers on faces.

- Body: a regular hexagonal prism, circumradius 25.5 mm, 28 mm long. One moving part inside the shell for locomotion, a **lift ring** with one lobe in a slot around the girdle. The lobe reaches r = 28.5 mm, outside the hexagon outline: parked it points +z and its tip is part of the stowed envelope (section 3).
- Locomotion: the unit lies on a side face and rolls over a bottom hexagon edge onto the next face, one 60 degree step at a time, like a hexagonal log. The ring is turned by a 6 mm gearmotor through a spur pair and a pinion. The lobe tip presses on the table, lifts the trailing side until the centre of mass passes the leading edge, and gravity completes the step. Reversing the motor reverses the roll.
- Couplers (axial, on the two hexagonal end faces): a fixed 304 hexagonal **peg** on the head (6.5 mm engagement), and on the tail a receiver with a **roll-in channel**, a **yaw turntable**, a **304 hex-in-hex roll lock** (cup insert plus keeper jaw) and a **motor-driven over-centre four-bar keeper**. A unit docks to a neighbour by rolling one step about its leading bottom edge so that the neighbour's peg slides along the arc channel into the receiver (section 7). v3 has no SMA wire and no spring anywhere.
- Exclusions (Q62 s3): **not a cube**, no flywheel or reaction wheel, no magnet. 51 mm across corners, 44.2 mm across flats, 28 mm long, so no needle or particle silhouette.

## 3. Geometry: stowed and deployed

Frame: prism axis = body y (head end +y). Rest orientation identity (bottom side face F0 has normal -z). Hexagon vertices in the x-z plane at (±R, 0) and (±R/2, ±a).

| Quantity | Value | Basis |
| --- | --- | --- |
| Circumradius R | 25.500 mm | lead decision (unchanged from v2) |
| Apothem a | 22.0836 mm | R·√3/2, derived |
| Axial length H | 28.0 mm | design choice (end plates at \|y\| 12 to 14, 2 mm thick) |
| Inner cavity | cylinder r = 20.0 mm, \|y\| ≤ 12 | design choice; wall radial thickness 2.08 mm at face centres |
| Girdle slot | \|y\| ≤ 1.75, cuts the walls fully | lift ring slot. The head and tail wall halves are joined by two PA12 posts (y -6.9 to 12.0) and the end plate a; the tail end plate is joined through the cap halves |
| Lift ring | PA12 carrier annulus r 20.6 to 21.9 with a pressed-in **304 internal-gear band** r 19.5 to 20.6, \|y\| ≤ 1.5, module 0.3, 133 T, pitch r 19.95 (tips 19.65, roots 20.325) | lead decision (v2 had PA12 teeth) |
| Lift lobe | PA12, radial r 21.9 to 28.5 (L = 28.5), tangential 4.0, axial 3.0, tip rounded r 2; parked pointing +z | unchanged |
| Head peg | 304 hex 4.0 across flats (4.619 across corners), 19.5 long from root y 9 to **tip y = 28.5 mm**, 14.5 mm beyond the head face; engagement 6.5 mm in the neighbour | lead decision (v2: 18 long, tip y 27, engagement 5) |
| Stowed enclosing sphere diameter | **58.181 mm** | evaluator, centre at the origin |

**Stowed:** the hexagon is three overlapping boxes (half extents 12 750, 14 000 and 22 084 µm, rotated 0, 60 and 120 degrees about y), the lobe a box (x ±2.0, y ±1.5, z 21.9 to 28.5; the rounded tip is ignored, so the box is an upper bound), and the head peg a coupler-role cylinder (r 2.31 mm, y 14 to 28.5). The hexagon corners at (r 25.5, y ±14) define the sphere. The 1.82 mm margin is the room for SLS tolerance and is not a measured tolerance.

**Deployed (chain geometry):** the same boxes without cavities. The neighbour's tail face sits at y = 22 mm of this unit (gap g = 8 mm from the head face at y = 14, 6.5 mm peg engagement). `site-head` is at (0, 22 000, 0) µm, `site-tail` at (0, -14 000, 0). Mating roll angles are 0 and 180 degrees (180 fails the table check because the parked lobe would then point into the table; 0 is the operating mate).

## 4. Q12 packaging and component list

Cavity primitives: `cavity-main` (cylinder r 25.501 mm, half height 14 mm, axis y), `cavity-girdle` (r 29.0 mm, half height 1.75 mm, holds the lobe), `peg-envelope` (r 3.1 mm, **y 13.9 to 28.6**, holds the protruding peg). Each component box lies in one of them (evaluator rule).

Layout facts (body frame, mm; the declaration has all boxes):

- Cell flat under the axis: x -15.5..15.5, y -11.9..8.1, z -11.2..-3.7. Controller z -17.35..-11.65 (y -12.0..10.0). IMU x -10.43..12.43, y -4.35..8.35, z 1.73..4.27.
- driver-1 (M1 and M2) lies flat above the right side: x 7.4..17.6, y -6.4..11.4, z 4.6..6.4. driver-2 (M3) stands on edge at x -17.4..-15.6.
- M1 (lift motor) axis along y at x -4.0, z 12.18, output +y. M2 (yaw motor) axis along y at x 5.25, z 10, worm at y -10.3..-6.7. **M3 (keeper motor)**: axis along y at x 11.25, z 10.25, output end -y, body y -8.4..10.3, shaft y -12.0..-8.4 carrying the crank at y -9.2..-8.4.
- Tail receiver: cap halves x ±3.9..14.5, **y -12..-7** (roll-in channel depth 7.0 from the tail face), yaw puck (dia 7.6, runs in a dia 8.8 bore, journal y -12.0..-8.5) turning about body z through (0, -8.2), 304 cup insert (box x ±2.4, y -11.0..-9.6, z -3.5..-1.6; the puck box was shrunk to z -1.5..2.6 so the boxes do not overlap, mass unchanged), keeper (tongue, slider, jaw) above, keeper four-bar in the box x -0.9..8.2, y -9.2..-7.6, **z 11.6..17.3**.
- The keeper-linkage box is 0.9 mm higher than the 16.4 mm first asked for: the rocker's output pin travels z 11.63 to 17.29, and a stroke of at least 5.4 mm cannot fit a 4.8 mm tall box. The crank and the link end lie in the M3 shaft zone (x 9.2 to 13.3, outside the box) and the rod's lower run is inside the hollow yaw shaft. Both are box approximations.

Assembly access: the wall halves are separate parts so the ring (PA12 carrier segments with pressed-in 304 band segments) can be dropped into the girdle slot; stack loaded along the axis with one end plate removed; no assembly sequence was verified, and the press fits of the gear band and the cup insert, the rod through the hollow yaw shaft and the pin-in-slot are not shown assemblable.

### Parts (access date for every source: 2026-11-06)

| Component | Part | Source | Verified there | Caveats |
| --- | --- | --- | --- | --- |
| PA12 structure (walls, end plates, ring carrier, lobe, caps, puck, boss, posts) | EOS PA 2200 (PA12, laser-sintered) | [EOS PA 2200 data sheet](https://3dprinting.com/wp-content/uploads/2019/05/EOS-pa2200-white-datasheet-TDS.pdf) | density 930 kg/m³, tensile strength 50 MPa, modulus 1 700 MPa | strength beyond the coupler checks not assessed |
| SLS accuracy | Materialise PA12 (SLS) | [Materialise page](https://www.materialise.com/en/industrial/3d-printing-materials/pa12-sls) | "±0.3% (with a lower limit of ±0.3 mm)", minimum wall 1 mm, minimum detail 0.3 mm (read by the lead 2026-11-06) | a service-provider page, not the EOS material data; not shown for any particular printer. Cited in the descriptions of the cap halves and the roll-in alignment; component sources stay the material datasheets |
| Machined 304 tolerances | ISO 2768-1 general tolerances | [amesweb table](https://amesweb.info/fits-tolerances/iso-2768-linear-dimensions-tolerances.aspx) | class f ±0.05 mm (0.5 to 6 mm), ±0.1 mm (6 to 30 mm); class m ±0.1 / ±0.2 | a secondary table of the standard; v3 specifies class f for all 304 coupler parts |
| Metal parts (peg, tongue, slider, jaw, cup insert, four-bar parts, yaw shaft, worm, sector, gear band, spurs, layshaft, pinion, screws) | 304 stainless | [ATI 302/304/304L/305 TDS](https://www.atimaterials.com/Products/Documents/datasheets/stainless-specialty-steel/austenitic/ati_302_304_304l_305_tds_en1_v1.pdf) | density 7.90 g/cm³, yield 205 MPa, UTS 515 MPa, modulus 200 GPa | density of the A2 screws taken as 304 (assumption); the Lee spring is gone |
| Fasteners | 4x M1.6 x 4 A2 pan head | [Westfield Fasteners](https://www.westfieldfasteners.co.uk/A2-ScrewBolt-PoziPan-M1.6.html) | dk 3.2, k 1.3 | lumped box, not at real screw positions; volume is an upper bound |
| Harness | Alpha Wire 2841/7 30 AWG 7/38 PTFE | [DigiKey page](https://www.digikey.ca/en/products/detail/alpha-wire/2841-7-YL001/3708252) | OD 0.024 in (0.61 mm) | distributor page; 300 mm assumed; copper density from [Aurubis C11000](https://aurubis.com/dam/jcr:ec116d17-1541-419a-a897-ad31b4fa6c93/c11000-cu-etp-us.pdf) (8.9 g/cm³); lumped upper bound |
| Energy source | Grepow GRP8020030, 1S LiPo | [Grepow 15C table](https://www.grepow.com/high-discharge-rate-battery/15c-high-power-lipo.html) | 350 mAh, 15C, 3.7 V, 5.25 A max continuous, 7.5 x 20.0 x 31.0 mm, 8.0 g | the page also has a series "45C" statement that contradicts the row; the row is used. Energy 4 662 000 mJ nominal, not usable |
| Controller | Adafruit QT Py ESP32-C3 (5405) | [Adafruit](https://www.adafruit.com/product/5405) | 22.0 x 17.8 x 5.7 mm, 2.1 g, Wi-Fi + BLE, "3.3V regulator with 600mA peak output" | no LiPo charger; dropout limits use near end of charge; 2 220 mW is a bound |
| IMU | Pololu LSM6DSO carrier (2798) | [Pololu specs](https://www.pololu.com/product/2798/specs) | 0.5 x 0.9 x 0.1 in, 0.6 g, 1 mA | counted separately from the controller rail (conservative) |
| Drivers (two) | Pololu DRV8835 dual carrier (2135) | [Pololu specs](https://www.pololu.com/product/2135/specs); [dimension drawing](https://www.pololu.com/file/0J1536/drv8835-dual-motor-driver-carrier-dimensions.pdf); [TI DRV8835](https://www.ti.com/lit/ds/symlink/drv8835.pdf) | 0.4 x 0.7 in, 0.5 g, 1.2 A continuous / 1.5 A peak per channel; profile height 1.8 mm; IVM + IVCC 4 mA max | 15 mW quiescent bound each. driver-2 drives only M3 (start current 0.23 A, below 1.2 A); the 1.336 A SMA pulse of v2 is gone |
| Motors (three) | Precision Microdrives 206-109, 6 mm planetary 136:1 | [datasheet](https://www.precisionmicrodrives.com/datasheets/206-109-V0.pdf) | 1.2 g, body dia 6 x 18.7 mm, shaft dia 2 x 3.6 mm, rated 3 V, max 3.6 V, rated 3 mN·m at 140 rpm, stall 9 mN·m, start current 230 mA, rated-load power 215 mW | headed as a **sampling/target specification**; PWM-limited to 3.0 V effective (control constraint); **no radial shaft load rating in the sheet** (the crank link loads the M3 shaft radially) |

Vendor product pages (Grepow, Adafruit, Pololu, DigiKey, Materialise, amesweb) are classed `datasheet` because the schema allows only `datasheet` or `publication`. A reviewer should treat that as a stretch. The evaluator does not fetch URLs.

## 5. Mass and power budgets (reported)

**Mass (declared 41 849 mg, equal to the sum):**

| Group | mg | Basis |
| --- | --- | --- |
| 12 wall slabs | 2 × 4 128 | derived (unchanged) |
| 2 end plates | 2 × 3 142 | derived, solid hexagon (upper bound) |
| 12 ring carrier segments (PA12, r 20.6 to 21.9) | 480 | derived |
| **12 gear band segments (304, r 19.5 to 20.6)** | **3 288** (12 × 274) | derived, full annulus, teeth voids ignored (upper bound) |
| Lift lobe | 74 | derived, solid box |
| Tail cap halves (2, now y -12..-7) | 2 × 518 | derived, solid boxes (upper bound) (v2: 2 × 362) |
| Yaw puck / yaw shaft (304, hollow) | 439 / 39 | derived (puck: solid cylinder, upper bound; shaft was 6 mg PA12) |
| Yaw sector (304) | 160 | derived |
| Peg boss, posts (2 × 18.9 mm) | 100, 110 + 110 | derived |
| Head peg (19.5 mm) | 2 135 | derived 304, hex x length, groove ignored (upper bound) (v2: 1 970) |
| **Keeper (tongue, slider, jaw; 87.89 mm³)** | 694 | derived 304, jaw is a solid-block upper bound |
| **Cup insert (12.77 mm³)** | 101 | derived 304, solid block (upper bound) |
| **Keeper four-bar (crank, link, rocker, rod, stops, pins; 52.95 mm³)** | 418 | derived 304 |
| Yaw worm | 201 | derived 304 |
| Spurs, layshaft, pinion | 626, 95, 109, 429 | derived 304 |
| Fasteners (4) | 585 | derived 304, upper bound |
| Harness | 780 | derived copper, upper bound |
| Cell / controller / IMU | 8 000 / 2 100 / 600 | source |
| Drivers (2) | 2 × 500 | source |
| Motors (3) | 3 × 1 200 | source |

v2's release SMA (1 mg) and the Lee spring are removed. Many entries are solid-volume upper bounds, so the total is probably an overestimate for structure and an underestimate for anything not modelled; neither direction is quantified.

**Peak (worst case, all at once, per protocol s6):** controller 2 220 + IMU 4 + two drivers 2 × 15 + three motors 3 × 851 (max start current 230 mA x 3.7 V) = **4 807 mW**. Limit 3.7 V x 5.25 A = 19 425 mW. The SMA term of v2 (4 943 mW) is gone.

**Average:** 2 220 + 4 + 30 + 3 × 215 = **2 899 mW**. All three motors at continuous rated load is a conservative bound (M3 runs only for keeper moves).

**Endurance (reported only, never gates):** 4 662 000 mJ / 2 899 mW = 1 608 s (about 27 min), a lower bound on a quantity whose duty cycle is undecided, not a mission claim.

## 6. The lift-lobe mechanism

M1 (3 mN·m rated at 140 rpm, 9 mN·m stall) turns a 41 T spur (module 0.2, pitch r 4.1) that drives a 16 T layshaft spur (pitch r 1.6, centre distance 5.70). The layshaft carries a 14 T pinion (module 0.3, pitch r 2.1, tip r 2.4) at (x -2.484, z 17.676), 17.85 mm from the ring axis, that meshes the **304 band's** 133 internal teeth (pitch r 19.95, tips 19.65, roots 20.325). Speed ratio ring/motor = (16/41)·(14/133) = 1/3.707, so torque is multiplied by 3.707. Tooth strength, backlash, profile and contact ratio are **not assessed**. The band is machined 304 (ISO 2768-1 f); the SLS minimum-detail value of 0.3 mm (Materialise) no longer limits the teeth, but pressing a 1.1 mm band into a 1.3 mm carrier is not shown to be buildable.

Ring torque available (efficiency 0.9 per spur stage, 2 stages): **9.01 mN·m rated, 27.0 mN·m at stall**; ring speed 37.8 rpm, so one 60 degree push takes about 0.265 s at rated load.

**Quasi-static lift** (R 25.5, L 28.5, declared mass 41.849 g so W = m g = 0.4104 N, script `analysis_v3.py` in the scratchpad):

- Tipping needs L > R. Tip-to-pivot distance at tipping √(L² - R²) = 12.73 mm. The lobe touches the table when the body is flat and the lobe is 39.21 degrees from the bottom normal. Ring sweep from the parked +z position to first contact is 140.8 degrees; during the push the ring turns 42.7 degrees, leaving 17.3 degrees of each 60.
- Centre of mass (mass-weighted box centres) (0.037, 0.507, -0.127) mm, inside the support rectangle (margins 12.71 mm in x, 13.49 mm in y). Weight moment about the leading edge at the start W·R/2 = 5.23 mN·m.
- Peak ring torque required:

| Tip friction mu | W·mm | mN·m | Ratio rated (9.01) | Ratio stall (27.0) |
| --- | --- | --- | --- | --- |
| 0 | 7.47 | 3.06 | 2.94 | 8.8 |
| 0.15 | 8.84 | 3.63 | 2.48 | 7.5 |
| 0.5 | 12.04 | 4.94 | 1.82 | 5.5 |
| 1.0 | 16.62 | 6.82 | 1.32 | 3.96 |

- Maximum tip normal force 0.414 W; the pivot holds horizontally while N_T ≤ W/2 (equal friction). Ring tooth tangential force 0.154 N at the frictionless peak and 1.36 N at stall. Rough Lewis estimate (assumed form factor 0.3, width 3 mm) now applies to a 304 band, about 5 MPa at stall against 205 MPa yield; it was a flag against PA12 in v2 and is not evidence. Lobe root bending stress 0.14 MPa.
- **Clearance after tipping.** With the ring stopped the tip rises monotonically from the table. If the ring keeps turning at a uniform rate the tip clears only 0.69 mm and returns to the table at 60 degrees. Lead decision (control rule, unchanged): the ring stops after tipping until landing is detected. The real fall dynamics belong to Gate 2.
- Landing energy m g (R - a) = 0.4104 N x 3.416 mm = **1.402 mJ**.
- Parked: the lobe points +z. Reversal: yes. **Steering and axial motion are not provided.** The ring angle is open-loop (IMU sees tilt onset only).
- Friction: the ring runs in grooves of the wall-half faces (PA12 bearing); its friction is not quantified and is not subtracted from 9.01 mN·m. UNRESOLVED.

## 7. The coupler (design-guidance 4.2)

Two axial couplers. Head = hex peg, tail = receiver. Sites: head (0, +22 mm, 0) normal +y; tail (0, -14 mm, 0) normal -y. No lateral couplers. Design rules (lead): no functional PA12 clearance below 0.6 mm (2 x the Materialise 0.3 mm), no PA12 wall below 1.0 mm, no PA12 gear teeth; precision parts are machined 304, ISO 2768-1 class f.

### 7.1 Peg and receiver stations

In the receiving unit's frame (B frame), y runs from the tail face: end plate -14..-12; **puck front wall -12.0..-11.0 (1.0 mm, the PA12 minimum)**; jaw and cup zone -11.0..-9.6; groove -9.6..-8.2 (dia 3.0, width 1.4); **tongue 1.0 mm at -9.4..-8.4**; peg tip -7.5 (0.5 x 45 degree chamfer). In the peg's own (A) frame: neighbour face y 22, groove centre y = 22 + 5.1 = **27.1** (edges 26.4 and 27.8), peg tip 28.5, so the tip is 1.4 mm beyond the groove centre and 0.7 mm beyond the groove far edge; the hex section y 25.0 to 26.4 is the part enclosed by the cup insert and jaw. Engagement depth 6.5 mm.

### 7.2 Align

Two circular-arc slots in the tail cap halves (radius 25.5 mm, centred on the two bottom vertices, running from the mid-height vertices to the face centre; **width 5.8 mm (4.619 + 2 x 0.59), depth 7.0 mm from the tail face**, mouths flared 45 degrees x 1.5 mm). Why arcs: when unit B rolls one step about its leading bottom edge, a neighbour's peg on the common axis moves, in B's frame, along exactly this arc (the v2 review checked it), keeps its direction and turns 60 degrees about its own axis (hex symmetry), so B can roll into a docked pose using its own lift drive and gravity.

Windows, with the cited SLS accuracy (±0.3% with a lower limit of ±0.3 mm gives ±0.3 mm on 5.8 mm, so the width is 5.5 to 6.1):

| Window | Nominal | With SLS minimum (slot 5.5 mm) |
| --- | --- | --- |
| clearance per side to the 4.619 mm across-corner peg | 0.59 mm | 0.44 mm (0.41 mm with the peg at its ISO-f upper limit) |
| lateral at the mouth (clearance + 1.5 flare) | ±2.09 mm | ±1.94 mm |
| height | ±0.59 mm | ±0.44 mm |
| heading, atan(clearance/5) | ±6.7 degrees | ±5.0 degrees |
| final lateral seating by the tongue V-notch (6.0 mouth, 3.1 notch, 30 degree half angle, depth 2.51 mm) | ±1.45 mm | ±1.45 mm (machined) |
| axial: lash of the joint = groove play ±0.2 + puck-slot play ±0.3 | ±0.5 mm | ±0.3 to ±0.7 mm (ISO f on the tongue and groove, SLS on the slot) |
| tongue lead-in capture (30 degree half-angle wedge, 0.3 mm per side, tip face 0.4 mm) | ±0.5 mm | |
| roll | any multiple of 60 degrees; free roll after docking ±2.6 degrees | |

**There is no axial or heading pre-alignment means.** The unit has no steering and no axial motion. The windows above are all there is, so docking requires a common lane (axial error and heading inside the windows) as a precondition, not as a capability; the pre-alignment covers only the in-plane roll-in. The capture window is not claimed (CPL-006); it is to be measured by sweeps. Channel depth 7.0 against an engagement of 6.5 mm leaves 0.5 mm. No cone, no magnet.

**Relative roll after docking.** B rolls from F1 (or F5) onto F0 and A rests on F0, so the relative roll about the axis is 0 after the step. During entry the peg turns 60 degrees relative to B; the hex symmetry absorbs that. The roll lock then has only ±2.6 degrees of free roll.

### 7.3 Latch and roll lock

The keeper is **the unit's own motor driving an over-centre four-bar**. Dimensions (x, z in body mm; the plane of motion is x-z at y about -9.2 to -7.6):

- Crank: r = 2.0 on the M3 axis C = (11.25, 10.25).
- Rocker (bell crank): pivot Pv = (1.5, 13.3), off the yaw axis; link-side arm b = 3.0; output arm a = 4.5 at -46 degrees from the link-side arm; upper branch (rocker pin above the pivot).
- Link: L = D = |C - Pv| = **10.2159 mm**. The lead asked to be told if D differs from 9.75 by more than 0.1: **it differs by +0.47 mm**, and L = D was used.
- Push rod: dia 0.8, on the yaw axis (x 0) through the hollow 304 yaw shaft, driven from the rocker output pin through a pin-in-slot (slot not designed; the pin moves 2.4 mm in x).
- Grashof check: r + L = 12.22 ≤ D + b = 13.22, so the crank can rotate fully.

Dead centres are at the crank-link collinear positions: extended (|B - C| = L + r = 12.22) at crank angle 151.14 degrees, folded (L - r = 8.22) at 328.61 degrees. Stops sit 10 degrees past each. The crank travels **197.5 degrees** between the stops. **CLOSED = the folded-dead-centre stop (output pin low, z 11.67), OPEN = the extended-dead-centre stop (output pin high, z 17.25).** (The lead's text said "closed = 10 degrees past top dead centre"; "top" and "bottom" are interchangeable for the lock, which works the same at both stops. I assigned the labels so that closed is the low rod position.)

| Quantity | Value |
| --- | --- |
| rocker swing between the stops | 82.7 degrees (107.46 to 24.77) |
| rod (output pin) stroke between the stops | **5.58 mm** (asked ≥ 5.4, needed 5.2) |
| output pin range over the whole travel | z 11.63 to 17.29, x 3.58 to 6.00 |
| link-line offset from the crank axis at the closed stop | 0.283 mm |
| link-line offset from the crank axis at the open stop | 0.407 mm |
| tongue-to-link force ratio over the stroke (interior) | min 1.006, max 1.722; at the closed stop 1.72, at the open stop 1.01 |
| largest tongue-to-crank lever over the stroke | 3.025 mm (at crank angle 225.6 degrees) |

(The 0.35 mm offset of the first spec, 2.0 x sin 10 degrees, belonged to the layout that did not close; for the real four-bar the offsets are the two values above.)

**Lock statement.** At either stop the link line passes on the stop side of the crank axis, so a force on the tongue loads the link along its line and its moment about the crank pushes the crank into its stop. No power and no spring is needed; this is passive retention (CPL-009). The output pin has its extreme position at each dead centre, so a load that tries to move the tongue out of its state moves the crank further past the dead centre, into the stop.

**Tolerance.** With ISO 2768-1 class f on all of r, b, the pivot and crank coordinates (±0.05 each, an assumption that the hole positions are held to class f), the link (±0.1) and the stop position (±0.05 at the crank radius, ±1.43 degrees), the worst of the 256 corner cases leaves the stop **6.76 degrees past the dead centre at the open stop and 6.12 degrees at the closed stop**, with link-line offsets 0.271 mm and 0.176 mm. The margin is positive in every case. Link tolerance is the largest term. Bearing play of the M3 shaft and pin clearances are not included. UNRESOLVED.

**Forces.** All derived from W = m g = 0.4104 N (41.849 g) and a table friction bound mu ≤ 1 (provisional, Q47 sets the law, no coefficient is decided).

| Case | Value |
| --- | --- |
| design tension 4·mu·W | 1.642 N |
| **release under that tension** (tongue friction mu 1.0 steel on steel, provisional, no coefficient cited), peak crank torque over the stroke = 1.642 N x 3.025 mm | **4.97 mN·m** against M3 rated 3 (0.60 of the requirement) and stall 9 (1.81x). Rated torque covers tongue friction up to 0.99 N (60 % of the bound); stall up to 2.98 N |
| release at zero tension | only the friction of the mechanism, unquantified |
| closing, minimum tongue force over the stroke | rated 0.99 N, stall 2.98 N, against the other unit's head-end friction mu W/2 = 0.205 N at mu 1: **4.8x rated, 14.5x stall**. The wedge factor and tongue flank friction are not applied; dynamics UNRESOLVED |

Release is specified at low chain tension: the controller relaxes the tension first (chain yaw 0, no drag). Release at the mu 1 bound tension is **not** supported by the rated torque; it needs more than rated torque (about 1.66x), which M3 can give only toward stall.

**Roll lock (hex in hex).** When closed, the peg's hex section (4.0 mm across flats) is fully enclosed over 1.4 mm (B frame y -11.0 to -9.6) by the 304 **cup insert** (lower half-hex, pressed into the puck) and the **upper half-hex jaw** on the keeper slider, both 4.10 mm across flats (0.05 mm clearance per side). Free roll before the corners touch the flats: ±2.58 degrees (total 5.2). With class f ±0.05 on both parts the clearance per side runs from 0 to 0.10 mm, free roll 0 to ±5.4 degrees (line-to-line at one extreme, which is a fit that needs checking for assembly). Torsion contact (two opposite corner-flat contacts, couple 2·F·arm with arm 1.063 mm at the lash limit):

| Torsion | Normal force per contact | Line load over 1.4 mm | Flat-bearing width for 205 MPa | Hertz p0 (assumed 0.1 mm corner radius, nu 0.3) |
| --- | --- | --- | --- | --- |
| one idle neighbour tipped, 5.23 mN·m | 2.46 N | 1.76 N/mm | 0.009 mm | 784 MPa (2.3x the 342 MPa first-yield rule of thumb) |
| two neighbours, 10.47 mN·m | 4.92 N | 3.52 N/mm | 0.017 mm | 1 109 MPa (3.2x) |

The corner radius and Poisson ratio are my assumptions. The Hertz figures say a sharp 0.1 mm edge would dent the 304 flats locally until a contact patch of about 0.02 mm width forms; it needs a corner radius of about 1 mm to stay below first yield, which a hexagon corner does not have. Local indentation is expected and is not assessed further. UNRESOLVED.

**Cam-out along the tongue axis.** The upper jaw flat's normal is along z (the tongue's retract axis). At the lash limit and the design torsion 10.47 mN·m the force is **4.92 N** (v2 reviewer's model for the half-hex cup gave about 4 N at 4.57 mN·m; my v2-style lash-limit model for the open 4.6 mm cup would have been about 25 N, which the full enclosure removes). Slanted flat pairs give 0.5x in z. It is carried by the over-centre lock, not by a spring: at the closed stop the tongue-to-link ratio is 1.72, so the link carries 8.5 N, the moment into the stop is F_tongue x |dz/dθ| = 2.40 mN·m (stop reaction at the crank radius 1.2 N), and the M3 shaft sees about 8.5 N radially (no rating in the PMD sheet). Link 7.1 MPa, rod 9.8 MPa (Euler buckling of the dia 0.8 rod over 18 mm: 122 N), pins 8.4 MPa in double shear. The spring in v2 was 0.33 N; there is none now.

**Tension path** (design tension 1.642 N): peg groove shoulder → tongue → puck front wall → puck front face → end plate b inner face.

| Check | Force | Area | Stress | Ratio |
| --- | --- | --- | --- | --- |
| tongue on groove shoulders (2 x 0.5 x 1.5) | 1.642 N | 1.5 mm² | 1.09 MPa | 0.0053 of 304 yield 205 MPa |
| tongue shear (2 x 1.0 x 1.5) | 1.642 N | 3.0 mm² | 0.55 MPa | 0.0046 of 0.577 x 205 = 118 MPa |
| tongue on PA12 puck slot wall (7 x 3, overlap assumed) | 1.642 N | 21 mm² | 0.078 MPa | 0.0016 of PA12 50 MPa |
| **puck front wall shear-out**, 2·(7 + 3)·1.0 | 1.642 N | 20 mm² | 0.082 MPa | 0.0033 of 25 MPa (0.5 x 50, **assumed** shear allowable) |
| **end plate b thrust**, annulus r 2.8 to 3.8 around the dia 5.6 peg hole | 1.642 N | 20.7 mm² | 0.079 MPa | 0.0016 of 50 MPa |

All far below limits; stress concentrations, creep of PA12 and tolerance stack-up are not evaluated.

**Puck bearing.** The puck (dia 7.6) is a journal in the dia 8.8 bore of the cap halves over y -12.0 to -8.5 (length 3.5, 0.6 mm radial clearance), thrusting on end plate b, located vertically by PA12 shoulders in the caps. Pitch moment W/2 x 36 = 7.39 N·mm over the 3.5 mm journal gives 2.11 N; projected pressure 0.079 MPa nominal, 0.32 MPa if loaded over a quarter of the projected area (0.006 of 50 MPa). The 0.6 mm clearance allows a puck tilt up to 18.9 degrees in the bore (geometric, not a limit on use). Torsion and yaw torque pass through the yaw shaft only.

**Yaw shaft (304, OD 2.0, ID 1.0, 2.1 long).** Torsion tau = 16·T·D / (π (D⁴ - d⁴)): 73.5 MPa at M2 stall (108.2 N·mm at the puck; 0.62 of the 118 MPa shear yield), 24.5 MPa at rated torque, 25.5 MPa at the mu 1 design load. The shaft is no longer the weak point that the PA12 shaft was; the sector-to-shaft and puck-to-shaft joints are not designed.

**Data.** BLE only (ESP32-C3). Range, occlusion and latency UNRESOLVED. **Power.** No power transfer.

## 8. Passive retention when unpowered (CPL-009, Q11)

`requires_power_to_hold = false`, `mechanism_kind = geometric_interlock`. Components: keeper, keeper-linkage, keeper-motor, yaw-puck, head-peg. Both states of the keeper are held by hard stops past dead centre and need no power and no spring. Only release and closing are powered, and bounded independent release is declared true: M3 drives the crank over both dead centres (section 7.3). The release means is a motor in the unit's own receiver; it needs no help from the neighbour.

What is shown on paper: pin coordinates and dimensions, over-centre offsets and their tolerance, the stop geometry, a force balance for holding (all states) and for release and closing with the four-bar's actual lever, the tension path with the puck wall and bearing, and a hex-in-hex roll lock. What is **not** shown: friction in the pins and stops (ignored in the torque figures), crank stop wear, shock and vibration, the radial load rating of the M3 shaft, creep of the PA12 front wall, and the pin-in-slot detail.

## 9. Pre-alignment justification (CPL-005, Q36)

Alignment is geometric, passive and has three parts (`geometric_guide`): the roll-in channel (windows in section 7.2), the tongue V-notch seating (±1.45 mm, with axial capture ±0.5 mm and a closing force of at least 0.99 N against 0.205 N of head-end friction), and the hex peg in the lower half-hex cup of the cup insert with the 0.5 x 45 degree tip chamfer. Pre-alignment forces come from sliding contact, gravity, B's own lift drive and table friction; the closing force is M3 through the four-bar. There is no attractive force, so an undriven unit does not self-dock. **No axial or heading pre-alignment means exists** (section 7.2). A reviewer should expect G6 to be justified only on paper.

## 10. Chain bending (Q31) resolution

The **yaw turntable** is unchanged in kind: the puck turns about body z through (0, -8.2), driven by M2 through a single-start worm (module 0.3, lead angle 7.13 degrees) into a 304 sector (pitch r 4.05, 27 teeth per turn, ±21.5 degrees, working range ±12, hard stops ±15 degrees). The yaw shaft is now 304 (section 7.3). The sector, worm, spurs and pinion are machined 304 (ISO 2768-1 f).

- **Face clearance.** With pivot inset p = 5.8 mm and g = 8 mm: 5.55 mm required at 12 degrees, 7.04 mm at 15 degrees (margin 0.96 mm). The peg at the tail face plane sweeps 1.23 mm (12 degrees) or 1.55 mm (15 degrees); the longer 6.5 mm engagement does not change this, but the roll-in channel and the peg's travel in it are not re-checked at yaw angle.
- **Torque.** Available at the puck: rated 36.1 mN·m (3 x 27 x worm efficiency 0.445 at an assumed worm friction of 0.15), stall 108.2. Design load at table mu = 1: mu W (d1 + d2) = 0.4104 x 91.6 = **37.6 mN·m**. Ratio **0.96 at rated torque, 2.88 at stall**. At mu 0.5: 18.8 mN·m, ratio 1.92 rated and 5.76 stall. **So at rated motor torque bending works only for table mu up to about 0.96; that is the bound operating envelope for bending** (v2 had 1.10 at 36.55 g; the heavier 304 band is the cause). At stall it covers mu up to 2.88, but see the sector load.
- **Sector tooth load.** 9.3 N at the mu 1 design load, 8.9 N at rated, 26.7 N at stall. The sector is 304. A rough Lewis estimate (width 2 mm, module 0.3, form factor 0.3, **assumed, not cited**) gives 52, 49 and 148 MPa: 0.25, 0.24 and 0.72 of the 205 MPa yield. A flag, not evidence; tooth strength UNRESOLVED, a stall-current limit on M2 is advisable.
- **Holding a bend.** Unpowered only if the worm self-locks, which needs worm/sector friction ≥ tan 7.13 = 0.125 (UNRESOLVED), so a bend is treated as actively maintained.
- **When it works.** Bending works only while the chain rests on F0 or F3 (yaw axis vertical). Steering a single unit is not provided.

## 11. Risks and unknowns

1. **No steering or axial locomotion**, so there is no axial or heading pre-alignment: docking needs a common lane.
2. **Docking by roll-in is a paper idea.** Impact dynamics, whether the ring-driven roll lands inside the windows, and the closing dynamics are unresolved.
3. **Release under the full design tension** needs about 1.66 times M3's rated torque (stall 9 mN·m is 1.81 times the requirement), so release is specified only at low tension.
4. **Yaw torque margin 0.96 at rated** at the mu 1 bound.
5. **Crank stop wear and the rod's pin-in-slot** are undesigned. The M3 shaft takes a radial link force (up to about 8.5 N in the roll-lock cam-out case) with no rating in the PMD sheet.
6. **Tolerance assumptions.** Hole-position tolerances ±0.05 for the four-bar are my assumption. The 0 to 0.1 mm roll-lock clearance includes zero. The Materialise page is a service-provider statement, not EOS material data.
7. **Contact stress** at the peg corners on the 304 flats (assumed 0.1 mm radius): Hertz 784 to 1 109 MPa against a 342 MPa first-yield rule of thumb.
8. **Worm self-locking is conditional** on friction ≥ 0.125.
9. **Press fits** (gear band into the carrier, cup insert into the puck) and a **0.3 mm minimum detail** for the PA12 puck slot and cup features are not shown buildable.
10. **M3 adds 1.2 g and 851 mW peak**; the 304 band adds 3.29 g. Heat of three motors in a closed body is not assessed.
11. **Motors** run from the 3.7 V cell by PWM limited to 3.0 V effective, and the PMD datasheet is a sampling/target specification. The QT Py regulator has 600 mA peak, no LiPo charger, and its dropout limits use near end of charge.
12. **Lumped placements** (fasteners, harness) and box approximations (peg root, keeper and cup insert inside the puck volume, the crank and link end in the M3 shaft zone, the rod inside the yaw shaft, the jaw as a solid block, meshing gears as squares).
13. **Assembly** is unverified. **Strength** of the PA12 walls (2.08 mm at face centres) and the cut tail cap, and heat, are not assessed. **Ring bearing friction** is unquantified. **Mass** is a mix of upper bounds and omitted items.
14. **Three-unit chain only**; the five-unit claim of Q31 is untested.

## 12. Response to the v2 reviews

### Retention review v2 r1, section 6 (six items)

| # | Required | What v3 does |
| --- | --- | --- |
| 1 | Specify the toggle: pin coordinates, over-centre offset and tolerance, the stop, the spring, bistable or not; resolve Q066 item 4; force balance for closing, holding, opening, open-state holding | The SMA and the spring are removed (Q67 item 4 preferred a release principle other than an SMA latch). The toggle is a motor-driven four-bar with every pivot, link and arm dimension given (section 7.3), two geometric stable states, over-centre offsets 0.283 and 0.407 mm, class f tolerance corner analysis (stops stay at least 6.1 degrees past the dead centre), a closing force of at least 0.99 N, release torque at the bound tension 4.97 mN·m, and open-state holding by the second stop. Bistability is a property of the stops, not of a spring. **Not closed:** friction and wear of the stops, the pin-in-slot detail, release at full tension within rated torque |
| 2 | Fix the tension path; declare how the puck is carried to the body with a stress check for tension, pitch and roll | Dimensions made consistent: the groove at y -9.6..-8.2, a 1.0 mm puck front wall, thrust on end plate b through an annulus of 20.7 mm². The puck is a journal in the dia 8.8 bore (length 3.5); torsion goes through the 304 hollow yaw shaft. Bearing, shear-out, thrust, journal pressure and shaft torsion are checked (section 7.3). **Not closed:** creep of PA12, joints of shaft to puck and sector, stress concentrations |
| 3 | Redo the torsion check for a half-hex cup (cam-out) and the release force under design tension | The roll lock is now a full hex-in-hex enclosure (cup insert plus jaw, 4.10 mm across flats) over 1.4 mm. Contact forces, line loads and Hertz stress are computed at the lash limit; cam-out along the tongue axis is 4.92 N at the design torsion, carried by the crank stop. Release under the design tension is computed with the four-bar's lever and found to exceed rated torque. **Not closed:** Hertz stress above first-yield rule of thumb; friction coefficient is a provisional bound |
| 4 | Declare cup opening direction, cup-to-peg clearance and tongue tip form; restate the axial lane from the real play | Cup opens upward and is closed by the jaw; clearance 0.05 mm per side; tongue tip is a 30 degree half-angle wedge with a 0.4 mm tip face (no zero-width edge); axial lash ±0.5 mm (±0.3 to ±0.7 with tolerances) replaces the ±0.8 mm quoted in v2 (section 7.2) |
| 5 | Supply axial and heading pre-alignment, or state that none exists; handle the 60 degree relative roll | Stated plainly: none exists, docking needs a common lane. The relative roll after docking is 0 (B rolls from F1 or F5 onto F0; A rests on F0) and the 60 degrees during entry is absorbed by hex symmetry |
| 6 | Cite an SLS tolerance and show the slot clearance and over-centre offset survive it | Materialise PA12 (SLS) ±0.3% with a lower limit ±0.3 mm and ISO 2768-1 class f for machined parts are cited. Slot clearance 0.44 mm per side at the SLS minimum (v2 0.39 nominal with no tolerance); the over-centre offset is on machined 304 parts and survives class f with at least 6.1 degrees of margin. The Materialise page is not EOS material data |

Other retention-review points answered: the V-notch seating no longer rests on a spring snap force (the closing force is M3's); the arithmetic items of review section 5 are corrected by the new dimensions.

### Originality review v2 r1

The review rated D2 **high** against both CONRO (Q64-C21) and PolyBot G2 (C12): an SMA-wire-released latch that engages grooves on protruding pins and holds without power. Q67 item 4 asked v3 to prefer a release principle other than an SMA-released latch. v3 changed the release principle: **no SMA wire and no spring-closed latch.** The latch tongue is now moved by a gearmotor through an over-centre four-bar with two geometric stable states. What did **not** change: the tongue still engages an annular groove on a protruding pin and the lock still holds without power, so the groove-on-pin hold of CONRO and PolyBot G2 is retained. The moderate cells (M-Blocks C7/C8 D3 and D4, PolyBot C12 D3/D4, CKBot C14 D3, CONRO D3/D4, HEXEL Q64-C22 D1, Q64-C23 D3, Toyota X3 D2) are unaffected by the coupler change except X3 D2, whose SMA bistable latch no longer has an SMA element to compare. The locomotion and body are unchanged (D3 and D1 moderates stay). Whether D2 now drops below high is for the independent reviewer to decide; this dossier does not argue it away (section 13).

## 13. Author self-check against the originality corpus (NOT the official review)

This is the author's own check against `docs/originality/reference-corpus.md`. It is **not** the Q61 matrix, it is not independent (Q61 s4), and it does not count for G7 or G8. Identifiers follow Q65 (Q64-C21 to Q64-C29 for the Q64 additions; plain C21 to C23 are the section-C entries). Descriptor text in the corpus comes from abstracts and search summaries, so my comparison inherits that limit. Ratings use the Q61 anchors (N, L, M, H).

| Reference | D1 geometry | D2 coupler | D3 locomotion | D4 assembly | D5 visual | Note |
| --- | --- | --- | --- | --- | --- | --- |
| A1 BH6 microbots | N | N | N | N | N | Large single unit, flat-faced, no particle swarm, no magnetic legs |
| B1 Replicators | N | N | N | L | N | |
| **Q64-C21 CONRO** | L | **M to H** | N | L | L | Groove-on-pin hold shared; release is now a gearmotor-driven over-centre four-bar, not an SMA pull-back of a spring-closed latch. The review rated v2 H; I would rate v3 M to H and the reviewer decides |
| **C12 PolyBot (Yim et al., G2 interface)** | L | **M to H** | M | M | N | Latch plate around pin grooves with SMA release in the source; v3 keeps tongue-in-groove but not the SMA, spring or latch plate |
| **C7 M-Blocks / C8 3D M-Blocks** | L | L | **M** | **M** | L | Rigid body pivoting over an edge; unchanged |
| **Q64-C22 HEXEL** | **M** | L | L | L | L | Hexagon outline only; press-release summary |
| C11 Molecubes | L | L | N | L | L | |
| C14 CKBot, C22 Sambot (section C) | L | L | M / N | L | N | |
| C4 ATRON, C6 Roombots, C16 FreeBOT | N | L | N | L | N | |
| C18 Telecube, C19 Crystalline | N | L | N | L | N | |
| D1 Cubelets, C23 Blinky Blocks (section C) | L | L | N | L | L | Magnetic cubes |
| C9 Kilobot | N | N | L | N | N | |
| X3 Toyota SMA latch patent US9140243B2 | N | L to M | N | N | N | Both states held mechanically; v3 has no SMA, a four-bar with stops |

**Originality-sensitive points the reviewer should look at first.** I list them; I do not argue them away.

1. **vs Q64-C21 CONRO and C12 PolyBot G2 (D2).** The tongue-in-groove-on-pin hold with an unpowered default state is the shared principle and remains. Differences I can state: no SMA, no spring, no latch plate; a motor-driven over-centre four-bar with two stops; a hex-in-hex roll lock that is independent of the groove; a lateral roll-in arc entry; a yaw turntable inside the coupler. The roll-in dock and the hex enclosure are, as far as I found, not in the corpus, but the corpus is not exhaustive.
2. **vs C7/C8 M-Blocks (D3, D4).** A rigid body that pivots over its edge to dock with a neighbour remains the closest locomotion and docking idea. No flywheel or magnet.
3. **vs Q64-C22 HEXEL and Q64-C23 hexagon pivoting modules (D1, D3).** A hexagonal rolling body; the paper-level sources could not be fully read (review section 9).

- **Exclusion 1 (cube with internal flywheel):** not present. **Exclusion 2 (needle- or particle-like silhouette):** not present.
- **Family membership:** meets Family A (single rigid polyhedron, edge pivoting, couplers on faces). The lift ring, yaw puck and keeper are internal moving parts; the Family A reading is for the reviewer.
- **What the corpus cannot tell me:** whether a hexagonal log-roller with an internal ring lobe and a roll-in dock exists outside the corpus. Nothing here claims absolute originality.

## 14. Changes from v2

| Area | v2 | v3 | Why |
| --- | --- | --- | --- |
| Release / keeper | Flexinol SMA pulse + Lee spring + two-link toggle + trip | M3 (206-109) driving a four-bar crank-rocker with two geometric stops; no SMA, no spring | retention review §6 item 1; Q67 §2–4 |
| Keeper geometry | none declared | crank r 2.0, rocker pivot (1.5, 13.3), arms 3.0 / 4.5, link 10.216, rod stroke 5.58 mm | answer the review; first spec did not close |
| Roll lock | open half-hex cup with a round-neck tongue | 304 cup insert + upper jaw, 4.10 mm across flats, 1.4 mm | torsion/cam-out (review item 3) |
| Peg | 18 long, tip y 27, groove 1.6 wide at y 24.5 | 19.5 long, tip y 28.5, groove 1.4 wide at y 27.1, engagement 6.5 mm | consistent tension path (item 2) |
| Tongue | 0.8 mm | 1.0 mm in a 1.4 mm groove; 30 degree wedge, 0.4 mm tip | item 4 |
| Roll-in channel | width 5.4, depth 5.5 | width 5.8, depth 7.0 | SLS clearance rule (item 6) |
| Puck | box only | journal in a dia 8.8 bore, thrust on end plate b, front wall 1.0 mm | item 2 |
| Yaw shaft | PA12 solid, SMA bore ignored | 304 hollow OD 2 / ID 1 | torsion at M2 stall |
| Ring teeth | PA12 teeth | 304 band in PA12 carrier (+3.29 g) | SLS minimum detail 0.3 mm; no PA12 gear teeth |
| Posts, caps | posts y -8.4..12; caps y -12..-8.5 | posts y -6.9..12 (18.9 mm); caps y -12..-7 | channel depth 7.0 |
| Tolerances | uncited | Materialise PA12 SLS, ISO 2768-1 class f | item 6 |
| Placements | v2 layout | qtpy, imu, drivers (swapped roles), harness, fasteners, posts repacked by the lead | M3 added |
| Mass | 36.550 g | 41.849 g | M3, bands, longer peg, jaw, insert, caps |
| Peak / average power | 8 899 / 2 684 mW | 4 807 / 2 899 mW | SMA pulse removed, third motor added |
| Endurance | 1 737 s | 1 608 s | |
| Yaw ratio at mu 1 | 1.10 | 0.96 | heavier unit |

Notes from the implementation, recorded as stated:

- The first spec's groove arithmetic said "tip 1.5 mm beyond groove end"; with groove centre 25.5 and tip 27 that is 1.5 mm beyond the groove centre and 0.8 mm beyond the far edge. For the current 6.5 mm engagement the corresponding figures are 1.4 and 0.7 mm.
- The four keeper pins are budgeted at 7.54 mm³ (the lead's figure); four dia 0.8 x 3 pins would be 6.03 mm³, so the figure is an upper bound.
- post-1 and post-2 now have the same 18.9 mm length as their boxes (post-1 was a 24 mm volume in a 20.4 mm box in the first draft).
- The cup model in the first draft (open half-hex, "tongue-notch flat" as the second reaction) was replaced by the full enclosure; the V-notch still seats on the round groove, not on the hex flats.
- The tongue-tip wedge was read as a 0.3 mm lead-in in y per side, leaving a 0.4 mm tip face.
- Jaw dimensions (7.0 x 1.4 x 3.05) are my sizing; the lead gave only 4.10 mm across flats.
- Mass-dependent loads are all recomputed from the declared 41.849 g: the first spec's figures (1.434 N, 1.97 N, 3.94 mN·m, yaw ratio 1.10) were for 36.55 g and are superseded.
- The linkage box is z 11.6..17.3, not 16.4 (section 4).

## 15. Unresolved list (for the lead)

1. SLS tolerance holds for any particular printer (Materialise is a service page); tolerance on four-bar hole positions is assumed.
2. Roll-in closing dynamics, whether the ring-driven roll lands inside the windows, and the capture window (CPL-006, measured by sweeps).
3. Release under the full mu = 1 design tension needs about 1.66x rated M3 torque; mu for steel on steel is a provisional bound; crank stop wear; pin friction; pin-in-slot design; M3 radial shaft load rating (none in the sheet); M3 heat and cycle life.
4. Keeper behaviour under shock and vibration; creep of the 1.0 mm PA12 front wall.
5. Hex-in-hex fit (0 to 0.1 mm clearance per side over ISO f, line-to-line at one extreme) and Hertz contact stress at the peg corners; the jaw's solid-block mass.
6. Worm/sector friction (≥ 0.125 for self-lock); yaw torque margin 0.96 at rated (bound operating envelope mu ≤ 0.96); sector tooth strength (assumed Lewis factor; 0.72 of yield at stall).
7. Ring bearing friction; real fall dynamics and fall time per step.
8. Tooth strength, backlash, profile and contact ratio of all gears (including the 304 band).
9. Press fit of the gear band into the PA12 carrier and of the cup insert into the puck; assembly sequence; lumped placements (fasteners, harness) and box approximations.
10. Motor PWM voltage constraint, PMD sampling-specification status, QT Py regulator variance and charging.
11. PA12 wall and tail-cap strength beyond the coupler checks; heat generally (three motors).
12. BLE range, occlusion and latency; through-coupler data and power (none declared).
13. Lateral couplers, steering, axial locomotion, **five-unit chain** (Q31).
14. Independent retention-review and originality-review records for v3; the author self-check above is not the review.
