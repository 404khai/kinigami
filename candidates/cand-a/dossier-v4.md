# cand-a v4: hexagonal-prism tumbler with lift ring and roll-in peg coupler (Family A)

Authors: Claude Opus 5.5 (engineering lead, all design decisions) with Claude Sonnet 5.5 (cand-a v4 implementation agent: derived values, files, this dossier). Date: 2026-11-07. Label: **exploratory**. Declaration: `declaration.json` (schema_version 1, candidate_version 4, SHA-256 `f6c18f80dd14815538e923cdb9c1f7c3c514fc7d22d55518d0c45063ef62b05d`). File layout follows Q65: `declaration.json` is the current version; the v1, v2 and v3 bytes are kept in `declaration-v1.json`, `declaration-v2.json` and `declaration-v3.json` (v3 SHA-256 `0025a534f9fc2496d8010e97ad69754485b5e671de23a8261ec11237e16fa1bb`); the dossiers are `dossier.md` (v1), `dossier-v2.md`, `dossier-v3.md` and this file. No earlier file was edited.

This is a paper-gate dossier (Q38 Gate 1). It does not show that any mechanism works. Every number below comes from a cited source, from an explicit derivation, or is marked **UNRESOLVED**. An attractive layout is not evidence that a mechanism works. v4 answers the independent v3 reviews (`retention-review-v3-r1.md`, `originality-review-gate1-v3-r1.md`) and Q69; section 12 maps each finding to what changed. The scripts are `gen_v4.py` (declaration generator), `analysis_v4.py` (analysis, output `analysis_out_v4.txt`), `kin_v4.py`, `sweep_v4.py`, `swept_final.py`, `fbg.py`, `layout_final.py` (kinematics, swept volume, four-bar, layout checks) in the lead's scratchpad, not in the repository.

## 1. Result at a glance

Official evaluator (`zig-out/bin/kinigami-gate1`, ReleaseSafe build of the pinned toolchain, code revision 447dc70 as printed in the report). **No v4 review records exist** (no `retention-review-v4-r*.md`, no `originality-review-gate1-v4-r*.md`), so G6 to G8 cannot pass.

| Item | Outcome | Why |
| --- | --- | --- |
| G1 stowed sphere | pass | D = 58 181.29 µm (certified radius 29 090.644 µm), limit 60 000 µm. The hexagon corners set the sphere; the lobe (now parked at -z) and the peg lie inside |
| G2 packaging | pass | 2 775 pairs tested, 0 interfering, 0 capped, 0 boxes outside the shell (3 cavity primitives). **Caveat:** boxes are rectangular stand-ins for round and swept parts; several masses are upper bounds; the link, rocker, rod and yoke boxes are envelopes of swept parts; the M3 shaft stub is not boxed; no routing (section 4) |
| G3 evidence | pass | 75 components, every one cited, every basis source or derived |
| G4 budgets | pass | mass 41 741 mg declared and summed; peak 4 807 mW against 19 425 mW; average 2 899 mW; endurance 1 608.14 s (reported only) |
| G5 chain | pass | 2 sites, 3-unit straight chain. Mating roll 0 fails (table_contact false), **180 is used** and passes (contact, support, no-interference, sites meet). With the rest orientation [0, 0, 1, 0] and the lobe at body -z this is a change from v3 (roll 0 used); what the 180 degree mate means physically is for the reviewer |
| G6 | unresolved | retention-review record missing |
| G7, G8 | unresolved | originality review missing (section 13 is only the author's self-check) |

Overall evaluator outcome: **unresolved** (G1 to G5 pass; G6 to G8 unresolved because no independent reviews exist for v4).

Key numbers: stowed diameter **58.18 mm**, declared mass **41.741 g** (v3 41.849 g), peak 4.807 W against 19.425 W, average 2.899 W. Rod stroke 5.58 mm; tongue closes at z 0.0 and needs 4.6 mm.

Statements to read together with the table:

- **Two kinematic errors in v3 were the lead's** (section 14). The roll-in arc was placed on the wrong branch of its circle (v2 spec, accepted by the v2 review, carried into v3), and the arrival direction of the peg was then taken to be from below at 30 degrees from the vertical. The corrected path ends along 30 degrees from the body x axis (nearly sideways). Everything in the receiver was re-derived from the corrected path.
- **The V-shaped channel forced a layout change** that the lead decided: the whole M1 gear group is rotated 60 degrees about the ring axis, and M3 takes the vacated left interior slot (section 4).
- **The lower half-hex cup of v3 cannot exist**; the receiver is a flat seat plus a three-flat jaw (section 7.4).
- **Release under the full mu = 1 bound tension still needs more than the rated M3 torque** (rated 0.64 of the requirement, stall 1.91). **Bending at rated yaw torque holds only for table mu up to about 0.96.**
- Rod stroke at the class-f corners is 5.04 to 6.11 mm: it meets the 4.6 mm needed for the z 0.0 closing but **not** the 5.4 mm floor that applied to the old z -1.0 closing.

## 2. Concept and family membership

Family A (Q62 s3): one rigid polyhedral body that moves by pivoting or rolling over edges, with couplers on faces.

- Body: a regular hexagonal prism, circumradius 25.5 mm, 28 mm long. One moving part inside the shell for locomotion, a **lift ring** with one lobe in a slot around the girdle (lobe reaches r = 28.5 mm, parked pointing body **-z**, which is up at the rest orientation).
- Locomotion: the unit lies on a side face and rolls over a bottom hexagon edge onto the next face, one 60 degree step at a time. The ring is turned by a 6 mm gearmotor through a spur pair and a pinion. Reversing the motor reverses the roll.
- Couplers (axial, on the two end faces): a fixed 304 hexagonal **peg** on the head (6.5 mm engagement), and on the tail a receiver with a **V-shaped roll-in channel**, a **yaw turntable**, a **flat 304 seat and three-flat jaw roll lock**, a **304 thrust washer** and a **motor-driven over-centre four-bar keeper** with an outrigger bushing for its shaft. A unit docks by rolling one step onto face F3 so that the neighbour's peg slides along the arc channel into the receiver (section 7). v4 has no SMA wire and no spring.
- Exclusions (Q62 s3): **not a cube**, no flywheel or reaction wheel, no magnet. 51 mm across corners, 44.2 mm across flats, 28 mm long.

## 3. Geometry: stowed and deployed

Frame: prism axis = body y (head end +y). **Rest orientation is [0, 0, 1, 0] (180 degrees about y): body face F3 (+z) is down, the lobe parked at body -z points up.** Hexagon vertices in the x-z plane at (±R, 0) and (±R/2, ±a). The docking landing face is F3.

| Quantity | Value | Basis |
| --- | --- | --- |
| Circumradius R | 25.500 mm | unchanged |
| Apothem a | 22.0836 mm | R·√3/2 |
| Axial length H | 28.0 mm | end plates at \|y\| 12 to 14 |
| Inner cavity | cylinder r = 20.0 mm, \|y\| ≤ 12 | unchanged |
| Girdle slot, lift ring, band | as v3 (304 band, 133 T, pitch r 19.95) | unchanged |
| Lift lobe | PA12, r 21.9 to 28.5, parked at **-z** | v3: +z |
| Head peg | 304 hex 4.0 across flats, tip y 28.5, engagement 6.5 mm | unchanged |
| Stowed enclosing sphere diameter | **58.181 mm** | evaluator |

**Stowed:** three hexagon boxes, the lobe box (z -28.5 to -21.9), the head peg cylinder. **Deployed (chain geometry):** the same boxes without cavities; neighbour's tail face at y = 22. `site-head` (0, 22 000, 0) µm, `site-tail` (0, -14 000, 0). Mating roll angles 0 and 180 (180 used by the evaluator).

## 4. Q12 packaging and component list

Cavity primitives as v3. Layout facts (body frame, mm; the declaration has all boxes). **Channel keep-out:** the two arcs (radius 25.5 about the F3 bottom vertices (±12.75, 22.084)) with half-width 2.9 + 0.3 margin = 3.2, y -12 to -7, form a V opening toward +z with its vertex at the face centre. No component box intersects the tube except the caps and end plate b (which carry it) and the seat, jaw and tongue at the arc end (checked against the swept peg instead, section 7.4).

- **Why a forced layout change.** With the keep-out in place no 6 x 6 mm column exists for M3 in the upper interior (axis at least 5.6 mm from the arcs): searched on a 0.5 mm grid for every sector size from 21 to 29 teeth. The only free position is v3's, whose axis is 0.9 to 1.8 mm from the arc centreline. The lead decided: **rotate the M1 group 60 degrees about the ring axis** (all centre distances and the pinion-ring mesh preserved; M1 axis to (-12.63, 2.19), azimuth 170 degrees; M1 cylinder 0.516 mm from the slot wall, rule 0.3), **move M3 into the old M1 slot** (axis (-4.500, 12.272)) with an outrigger post, and move the IMU (+2.0 mm in x), driver-2 (to x -9.4..-7.6, next to M3) and the harness (x -13..-10, z 6.5..9.5).
- M2 (yaw motor) axis (5.25, 11.70); the worm (axis 4.72 mm from the nearest arc, 3.2 keep-out plus its 1.5 radius needs 4.70) and the sector moved up 1.7 mm (sector z 10.7 to 12.7).
- Keeper column in the gap between the arms: seat x ±2.4, y -11.0..-7.5, z -3.3..-2.05; jaw x ±2.9 (z 0 closed, +5.583 open); tongue x ±2.05; yaw shaft z 8.7 to 12.7; rod and yoke bar x -0.4..3.5, y -8.9..-7.8, z 12.7..19.72.
- Four-bar: crank plate y -7.8..-7.3 on M3 (C = (-4.500, 12.272)), link and rocker plates y -7.3..-6.8, rocker pivot (5.250, 15.322) on a PA12 boss clipped to the top of M2, outrigger post (PA12, OD 4.6, y -12..-7.9) on end plate b with a 2.6 mm bore and a 1.3 mm bushing next to the crank.
- Caps: the box is only the strip below the V (z -3.6..-1.6, y -12..-7.5); the cap and end plate b are cut into three pieces by the V (assembly statement). 304 thrust washer x ±6, y -7.5..-7.0.
- Where a box is a stand-in: link, rocker and rod/yoke boxes are envelopes of swept parts (the yoke bar AABB corner is at r 20.02, its physical outer point at 19.96; the rocker plate envelope is clipped at the wall inner face z 19.99); the M3 shaft stub is inside the crank, link plane and post boxes and not boxed.

Assembly access: wall halves separate; stack loaded with one end plate removed; the tail parts install from the tail end; M3 and M2 are columns in the interior; **no assembly sequence was verified**; the press fits, the rod through the hollow yaw shaft, the pin-in-slot and the three-piece end plate are not shown assemblable.

### Parts (access date for every source: 2026-11-06; not re-read for v4)

The source set is unchanged from v3 (EOS PA 2200 for PA12; Materialise PA12 SLS ±0.3% / ±0.3 mm, minimum wall 1 mm; ISO 2768-1 class f ±0.05 (0.5 to 6 mm), ±0.1 (6 to 30 mm); ATI 302/304/304L/305 for all machined 304 parts including the **new thrust washer, seat, jaw and keeper parts** (density 7.90 g/cm³, yield 205 MPa); Westfield screws; DigiKey harness; Aurubis C11000; Grepow GRP8020030; Adafruit QT Py ESP32-C3; Pololu LSM6DSO and DRV8835; Precision Microdrives 206-109, a sampling/target specification with **no radial shaft load rating**). v4 re-verified none of them; the dates stay 2026-11-06. The links are in `declaration.json`. Vendor product pages remain classed `datasheet`, a stretch the reviewer should note.

## 5. Mass and power budgets (reported)

**Mass (declared 41 741 mg, equal to the sum), changes from v3 (41 849 mg):**

| Group | mg | Basis |
| --- | --- | --- |
| 12 wall slabs, 2 end plates, ring carrier, band, lobe | unchanged: 2 × 4 128, 2 × 3 142, 480, 3 288, 74 | derived; end plate b is still the full hexagon (upper bound) |
| Tail cap halves (2) | 2 × 518 | derived, v3 volume kept as an upper bound |
| Yaw puck / puck column | 439 / 18 | derived |
| Yaw shaft (4.0 mm, 304) / sector (304) | 74 / 160 | derived |
| **Seat (304)** / **thrust washer (304)** | 166 / 85 | derived (v3 cup insert 101) |
| Jaw / keeper tongue / keeper rod and yoke | 278 / 97 / 91 | derived 304 (v3 keeper 694) |
| Crank / link / rocker / rocker tip (pins, stops) | 71 / 61 / 52 / 91 | derived 304 (v3 four-bar 418) |
| M3 outrigger post (PA12) / rocker boss (PA12) | 51 / 9 | derived |
| Yaw worm, spurs, layshaft, pinion | 201, 626, 95, 109, 429 | derived 304 |
| Head peg, boss, posts, fasteners, harness | 2 135, 100, 2 × 110, 585, 780 | unchanged |
| Cell / controller / IMU / drivers / motors | 8 000 / 2 100 / 600 / 2 × 500 / 3 × 1 200 | source |

The v3 keeper solid-block upper bounds (jaw 7.0 wide, tongue 7 wide, slider 4 long) shrank because the V-notch tongue is replaced by a 4.1 mm tongue and the jaw by a 5.8 mm block; the new parts add about 0.3 g.

**Peak** 2 220 + 4 + 2 × 15 + 3 × 851 = **4 807 mW** (limit 19 425 mW). **Average** 2 899 mW. **Endurance** 1 608 s (reported only).

## 6. The lift-lobe mechanism

Gears and ring unchanged (41 T / 16 T spurs module 0.2, 14 T pinion module 0.3, 133 T 304 band, speed ratio 1/3.707). The M1 group rotated 60 degrees about the ring axis meshes the ring at azimuth 170 degrees instead of 98; the pinion centre is still 17.850 mm from the axis. Tooth strength, backlash and contact ratio are **not assessed**. Ring torque 9.01 mN·m rated, 27.0 stall.

**Quasi-static lift** (declared mass 41.741 g, W = 0.4093 N; `analysis_v4.py`; body CoM x and z negated into the lobe-up analysis frame because F3 is down):

- Centre of mass (body frame) (-0.888, 0.646, -0.671) mm (v3 (0.037, 0.507, -0.127)); inside the support rectangle (margins 11.86 mm in x, 13.35 in y). Weight moment about the leading edge W·R/2 = 5.22 mN·m.
- Peak ring torque required (ratio to 9.01 rated): CoM at centre 3.06 / 3.62 / 4.93 / 6.80 mN·m at mu 0 / 0.15 / 0.5 / 1.0 (2.95, 2.49, 1.83, 1.32); rolling toward -x (CoM trailing) 3.27 / 3.87 / 5.27 / 7.28 (2.76, 2.33, 1.71, **1.24**); rolling toward +x 2.84 / 3.37 / 4.59 / 6.33 (3.17, 2.68, 1.96, 1.42). Stall ratios 3.7 to 9.5.
- Tipping at 27.5 to 30.0 degrees of body rotation; ring sweep during the push 40 to 43 degrees, 17 to 20 degrees of each 60 left. Maximum tip normal force 0.386 to 0.443 W (pivot holds while ≤ 0.5 W). Lobe root stress 0.14 MPa; ring tooth force 0.153 N at the frictionless peak, 1.36 N at stall. Landing energy 1.398 mJ.
- **Clearance after tipping:** with the ring stopped the tip rises monotonically; with the ring turning at a uniform rate it clears only 0.69 to 0.84 mm and returns to 0.0 to 0.23 mm at 60 degrees. Lead decision (control rule): the ring stops after tipping until landing is detected. Fall dynamics belong to Gate 2.
- Unchanged: reversal yes; no steering or axial motion; ring bearing friction unquantified.

## 7. The coupler (design-guidance 4.2)

Two axial couplers. Head = hex peg, tail = receiver. Sites: head (0, +22 mm, 0) normal +y; tail (0, -14 mm, 0) normal -y. No lateral couplers. Rules (lead): no functional PA12 clearance below 0.6 mm, no PA12 wall below 1.0 mm, no PA12 gear teeth; precision parts machined 304, ISO 2768-1 class f.

### 7.1 Corrected roll-in kinematics (item 1 of the review)

World frame (X horizontal, H up), unit A fixed with its peg axis at O = (0, a). B lands on F3 (body (x, z) maps to world (-x, a - z)), coming from +X and rolling about the shared bottom edge P = (R/2, 0) onto F3.

- Rotating B about P in the sense that would sink it: its lowest vertex goes to H = -4.43 at 10 degrees and -22.08 at 60 degrees (below the table; impossible). The other sense keeps the lowest vertex at H = 0 for the whole roll, and the centre height rises 22.084, 23.96, 25.11, **25.50 at 30 degrees**, 25.11, 23.96, 22.084.
- Peg in B's frame at 0, 10, 20, 30, 40, 50, 60 degrees of roll: (0, 0), (3.641, 2.550), (6.784, 5.693), (9.334, 9.334), (11.212, 13.362), (12.363, 17.656), (12.750, 22.084). The distance to B's bottom vertex (-12.75, +22.084) is 25.5 over the whole roll (error 4e-15). It starts at B's other bottom vertex (12.75, 22.084) and ends at the centre; the point at 30 degrees equals the Q69 value (9.33, 9.33) (mirrored). The peg hex turns exactly 60 degrees relative to B. The mirror image serves approach from -X.
- **The final approach is along 30 degrees from the body x axis** (tangent (-0.866, -0.5) from the +X side), i.e. nearly sideways. The chord is 60 degrees from x. A statement in the lead's v4 spec ("arrives from above, 30 degrees from the vertical") was the chord direction, not the final approach, and led to keeping a lower half-hex cup that the real path cannot enter (7.4).
- Docking lands on F3: arcs in the +z half, V opening toward +z.

### 7.2 Align

Two circular-arc slots (radius 25.5 mm, centred on the two F3 bottom vertices, running from the vertices to the face centre), **width 5.8 mm, depth 7.0 mm from the tail face** (cap y -12..-7, end plate b -14..-12), mouths flared 45 degrees x 1.5 mm. The tube keep-out is 12 OBBs per arc (half-length 1.132, half-width 3.224) in the lead's checks.

Windows (SLS ±0.3% with lower limit ±0.3 mm gives slot 5.5 to 6.1):

| Window | Nominal | With SLS minimum (5.5) |
| --- | --- | --- |
| clearance per side to the 4.619 mm peg | 0.591 mm | 0.441 mm |
| lateral at the mouth (clearance + 1.5) | ±2.09 mm | ±1.94 mm |
| height | ±0.591 mm | ±0.441 mm |
| **heading, two-point jam, engagement 6.5 mm** | **11.27 deg** | **8.21 deg**; 7.65 deg with the peg at the class-f upper limit (AF 4.05) |
| axial | ±0.5 mm | ±0.3 to ±0.7 mm |
| roll | any multiple of 60 degrees; free roll after docking ±2.58 degrees | |

The simple atan(clearance/divisor) of v3 gave ±6.7 and ±5.0 degrees with a 5 mm divisor (v2 engagement); with 6.5 mm it would be 5.19 and 3.88 degrees, which is optimistic for large tilt; the exact two-point jam is used and gives the figures above.

**There is no axial or heading pre-alignment means.** The unit has no steering and no axial motion. **A free approach cannot start a roll-in.** Docking requires B one roll step to the side in a common lane on the face adjacent to F3: axial position inside ±0.5 mm, heading inside the window above, and the peg already engaged 6.5 mm, which is only reachable by rolling out of a previous dock (a re-dock of a previously docked pair is the only case served). The capture window is not claimed (CPL-006); it is to be measured by sweeps. No cone, no magnet.

**Relative roll after docking.** B ends on F3 with A resting on the same face, relative roll 0; the 60 degrees during entry is absorbed by the hex symmetry.

**Tongue seating (V-notch dropped).** v3 declared a 6.0 mm mouth V-notch with a ±1.45 mm lateral reach. With flank friction 0.15 the lateral fraction of the closing force is (sin 30 - 0.15 cos 30)/(cos 30 + 0.15 sin 30) = 0.393 (it is negative at flank friction 1: the wedge cannot centre). Rated closing force 1.045 N gives a lateral push of 0.411 N against the neighbour's full-weight drag mu W = 0.409 N at mu 1: ratio **1.00 (rated), 3.01 (stall)**; against mu W/2 it would be 2.0 and 6.0. By the lead's rule (below 1.5 at mu 1, drop it) the V-notch is **not a declared pre-alignment means**; a 3.1 mm semicircular notch with a 30 degree lead-in wedge (0.3 mm per side, tip face 0.4 mm) remains as a seating feature only. Dropping it also makes a 4.1 mm wide tongue possible, which the swept volume needs (7.4).

### 7.3 Latch and roll lock

The keeper is **the unit's own motor driving an over-centre four-bar**, the v3 mechanism mirrored in x and moved into the left interior; all of the v3 rules are kept (crank r 2.0, stops 10 degrees past the dead centres, output arm 4.5).

**Re-solving.** The solver was rebuilt from first principles (`fbg.py`) and first validated on v3: D 10.2159, dead centres 151.14 / 328.61 degrees, travel 197.47, swing 82.69, stroke 5.583, offsets 0.4069 / 0.2834 mm, force ratio 1.0061 to 1.7215, peak lever 3.0252 mm/rad, margins 6.761 / 6.122 degrees in the v3 convention and 6.10 / 5.35 degrees with the size-based class f table (the reviewer's 6.11 / 5.36). The crank-pivot to rocker-pivot geometry is then the mirror image of v3, translated so the output pin runs inside the window above the sector (z 13.65 to 19.31). A search for a different four-bar with all parts left of the rod was made and gave strokes of 3 to 5.4 mm at class-f margins of 5.5 degrees, so the mirrored v3 geometry was kept.

| Quantity | Value |
| --- | --- |
| Crank C, r | (-4.500, 12.272), 2.0 |
| Rocker pivot Pv, link-side arm b, output arm a (at +46 deg from b, mirror branch) | (5.250, 15.322), 3.0, 4.5 (≤ 4.5) |
| Link L = D | 10.2159 mm |
| Grashof | r + L = 12.216 ≤ D + b = 13.216, crank shortest |
| Dead centres (extended / folded) | crank angle 28.86 / 211.39 deg |
| Stops (10 deg past): OPEN / CLOSED | 18.86 / 221.39 deg; crank travel 202.53 deg (the upper sweep; the other sweep (197.47 deg) has the link crossing the sector corner by 0.59 mm) |
| Rocker swing | 82.64 deg (72.61 open, 155.26 closed) |
| Output pin | open (3.095, 19.272), closed (1.056, 13.690); x 0.750 to 3.168, z 13.650 to 19.311 |
| **Rod stroke between the stops** | **5.582 mm** (needed 4.6 with the tongue closing at z 0.0, section 7.4) |
| Link-line offset from the crank axis | open 0.422 mm, closed 0.277 mm |
| Force ratio link/tongue | 1.006 to 1.739 over the stroke; 1.082 at the open stop, 1.645 at the closed stop |
| Peak lever | 2.871 mm/rad |

**Which part carries what.** The rocker pivot pin is carried by the PA12 rocker boss clipped to the top of M2 (not by the link plane); the two hard stops (1 x 1 x 2, at crank angles 18.86 and 221.39 degrees, crank radius 2.0 to 2.9) are carried by the PA12 outrigger post on end plate b. The crank is 0.5 mm from the bushing so that the bushing takes most of the crank's radial load.

**Tolerances (ISO 2768-1 class f, 1 024 corners over r, b, a ±0.05, the rocker arm angle ±1 degree, C and Pv coordinates, L ±0.1, stop ±0.05 at crank radius = ±1.43 degrees):**

| Convention | margin open / closed (degrees past the dead centre) | offsets open / closed (mm) | rod stroke min..max (mm) |
| --- | --- | --- | --- |
| v3 (all coordinates ±0.05) | 6.35 / 6.46 | 0.276 / 0.177 | 5.235 .. 5.948 |
| by size (6 to 30 mm coordinates ±0.1) | 5.64 / 6.09 | 0.245 / 0.167 | 5.088 .. 6.068 |
| all coordinates ±0.1 (conservative bound) | 5.19 / 5.41 | 0.225 / 0.149 | 5.035 .. 6.113 |

The margin stays positive in every corner. The rod stroke at the corners is **below the 5.4 mm floor** that applied to the old closing but above the 4.6 mm now needed. The pin and bar at the lowest corner come within 0.06 mm of the sector top (z 12.7) and at the highest corner the yoke bar exceeds the r ≤ 20 packing rule by about 0.2 mm; the nominal pin disc outer point is r 19.96. A 25-tooth sector (worm 0.5 mm lower) would remove both and costs yaw torque (envelope 0.89 instead of 0.96); not applied.

**Lock statement and load reversal.** Pin z has its extreme at each dead centre. A load that tries to move the tongue out of its state (open: downward; closed: upward) pushes the crank into its stop (torque F dz/dθ, lever 0.456 mm/rad at the stops): no power, no spring. The opposite load pulls the crank 10 degrees back to the dead centre; the pin moves only **0.039 mm (open) and 0.040 mm (closed)** and the dead centre is a stable equilibrium for that load sign, so the state holds. If that load then **reverses while the crank rests at the dead centre**, the equilibrium is unstable (z'' = -2.447 and +2.715 mm/rad²) and a deviation to the far side lets the state flip. With the combined reversed load 10.17 N (7.4) and an assumed 0.05 mm play at the crank radius, holding needs a pin friction coefficient of at least **0.141 (open) and 0.103 (closed)** at pin radius 0.4 mm (derived bound; real friction is not cited, UNRESOLVED). So the lock is passive for single-sign loads and for any load that tries to change the state; repeated alternating cam-out and pitch loads need a friction bias or M3 holding against the stop (power, not quantified).

**Forces** (W = m g = 0.4093 N for the declared 41.741 g; mu 1 provisional, Q47 sets the law):

| Case | Value |
| --- | --- |
| design tension 4 mu W | 1.637 N |
| **release under that tension**, peak crank torque over the stroke = 1.637 N × 2.871 mm/rad | **4.70 mN·m** against M3 rated 3 (**0.64** of the requirement) and stall 9 (**1.91**x). Rated torque covers tongue friction up to 1.045 N (64% of the bound); stall up to 3.135 N |
| release at zero tension | only the friction of the mechanism, unquantified |
| closing, minimum tongue force over the stroke | rated 1.045 N, stall 3.135 N; against the head-end drag mu W/2 = 0.205 N: 5.1x rated, 15.3x stall; against the full-weight drag mu W: 2.55x, 7.66x. Dynamics UNRESOLVED |

Release is specified at low chain tension: the controller relaxes the tension first.

**Roll lock (flat seat plus three-flat jaw).** The closed receiver encloses the peg hex section over 1.4 mm (B frame y -11.0 to -9.6): the flat 304 seat (top at z -2.05) below and the 304 jaw (upper flats 30, 90, 150 degrees of the 4.10 mm across-flats hex) above, 0.05 mm per side. The two slanted lower flats of v3 cannot exist (7.4). Free roll before corner-flat contact: **±2.58 degrees**, set by the three upper flats (the support function of the rotating peg touches them first in either direction; the seat flat never binds first). Torsion is carried by the top flat (jaw) and bottom flat (seat) corner contacts as a pure couple with arm 1.063 mm, the same pair as v3:

| Torsion | Normal force per contact | Line load over 1.4 mm | Hertz p0 (assumed 0.1 mm corner radius, nu 0.3, E* 110 GPa) |
| --- | --- | --- | --- |
| one idle neighbour tipped, 5.22 mN·m | 2.45 N | 1.75 N/mm | 783 MPa (2.29x the 342 MPa first-yield rule of thumb) |
| two neighbours, 10.44 mN·m | 4.91 N | 3.51 N/mm | 1 107 MPa (3.24x) |

The corner radius and Poisson ratio are my assumptions; local indentation is expected and not assessed further. The seat cantilever web (4.8 × 1.25 mm section, 3.3 mm lever) carries 4.91 N at 13 MPa bending stress (my estimate; yield 205 MPa). UNRESOLVED: registration of the jaw and the seat to the 0.05 mm per side fit (jaw on the keeper slider guided in PA12, seat on the washer-carried web).

**Cam-out and pitch bending on the crank.** Cam-out along the tongue axis at the design torsion: 4.91 N (the jaw's top flat). The pitch couple W/2 × 36 = 7.37 N·mm is reacted (my modelling choice, an assumption) between the jaw/seat plane (y -10.3) and the tongue plane (y -8.9), arm 1.4 mm: 5.26 N. Combined worst tongue z force **10.17 N**.

| At the | Ratio | Link force | Crank moment into the stop | Stop reaction at r 2.0 | M3 shaft radial load | Bushing pressure (d 2.0 × L 1.3), whole link force / half | Link stress (0.5 × 1.5) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| open stop | 1.082 | 11.0 N | 4.64 mN·m | 2.32 N | 11.0 N | 4.2 / 2.1 MPa | 14.7 MPa |
| closed stop | 1.645 | 16.7 N | 4.64 mN·m | 2.32 N | 16.7 N | 6.4 / 3.2 MPa | 22.3 MPa |

The PA12 bearing allowable and a PV limit are not cited (UNRESOLVED); 6.4 MPa is 0.13 of the 50 MPa tensile strength. The PMD sheet gives no radial rating, so the outrigger post exists to take the load; the gearbox bearing still carries the share the post does not (not computed). Link Euler buckling load 296 N.

**Groove engagement (new retention geometry).** The tongue closes at z 0.0 with a semicircular notch r 1.55 on the peg axis and sits on the upper half of the groove root (dia 3.0, 1.4 wide at y -9.6..-8.2; tongue 1.0 mm at y -9.4..-8.4). The tongue plate overlaps the peg shoulder between the groove root and the hex over the upper half: **3.11 mm²** (upper half-annulus 3.39 mm²; v3 claimed 1.5 mm² from two prongs). The tongue keeps the 30 degree lead-in wedge. The notch no longer wraps the groove below the axis, which is what makes the shorter stroke possible; lateral restraint then comes from the notch seat, the jaw V of the upper flats and the channel window (±0.44 mm at the SLS minimum), not from prongs.

**Tension path** (design tension 1.637 N, mu 1 provisional): peg tip-side shoulder → tongue (+y face at y -8.4) → 2 × 2 stem in the PA12 guide slot of the puck column → puck web (y -7.0 to -4.4) → **304 thrust washer** (flat thrust face) → the two cap strips (|x| 3.9 to 6.0) → tail wall ring.

| Check | Force | Area | Stress | Ratio |
| --- | --- | --- | --- | --- |
| shoulder bearing on the tongue | 1.637 N | 3.11 mm² | 0.53 MPa | 0.0026 of 304 yield 205 |
| tongue prong/web shear (2 × 0.5 × 1.0) | 1.637 N | 1.00 mm² | 1.64 MPa | 0.0138 of 0.577 × 205 = 118 |
| stem shear (2 × 1.0) | 1.637 N | 2.00 mm² | 0.82 MPa | 0.0069 of 118 |
| stem in the PA12 guide slot (2 × 2.6) | 1.637 N | 5.20 mm² | 0.32 MPa | 0.0063 of PA12 50 |
| stem cantilever bending (3.0 mm arm, section 2 × 1) | 1.637 N | M = 4.9 N·mm | 14.7 MPa | 0.07 of 205 |
| puck web on the washer (flat strip 7.2 × 1.8) | 1.637 N | 12.96 mm² | 0.13 MPa | 0.0025 of 50 |
| washer on the cap strips (2 × 2.1 × 1.8) | 1.637 N | 7.56 mm² | 0.217 MPa | 0.0043 of 50 |
| washer edge shear (2 × (12 + 1.8) × 0.5) | 1.637 N | 13.8 mm² | 0.12 MPa | 0.0010 of 118 |

All far below limits; stress concentrations, creep of PA12 and tolerance stack-up are not evaluated.

**Thrust washer.** The end-plate hole is now the slot of section 7.5: pivot inset 5.8 mm, peg axis lateral at the tail face plane ±5.8 tan 15 = ±1.554 mm; slot half-width in x = 2.309/cos 15 + 1.554 + 0.6 = **4.545**, half-height in z = 2.0 + 0.6 = **2.60**. The v3 thrust annulus (r 2.8 to 3.8 around the peg axis, 20.73 mm²) keeps only **4.28 mm²** after the V cut (6.56 mm² if only the channel is cut, 8.63 mm² if only the slot) which is below the 5 mm² rule, so thrust moves to a **304 washer**: 12.0 × 0.5 × 1.8 mm (x ±6.0, y -7.5 to -7.0, z -3.5 to -1.7), machined 304 (ATI 302/304/304L/305 data sheet, density 7.90 g/cm³, yield 205 MPa; mass 85 mg), bearing on 2 × 2.1 × 1.8 = 7.56 mm² of cap strips at 0.217 MPa, and carrying the seat web. **Line-contact issue (lead's decision):** the v3 puck is a cylinder about the z axis pressing a plane normal to y, which is a line contact, not an annulus; the washer is the flat thrust face that replaces it, and the lead's decision is that this resolves the issue. **I record one reservation:** a flat face normal to y cannot stay flat against a plane while the puck turns ±15 degrees about z, so the washer resolves the area of the load path but the compatibility of that face with the yaw rotation is still **UNRESOLVED** (section 15).

### 7.4 Receiver geometry versus the swept peg (item 2 of the review; `swept_final.py`)

Method: sample the arc at 0.5 degree roll steps for both arcs, hex AF 4.0 (and 4.05) rotating through 60 degrees, exact polygon-to-rectangle distances. Peg clearance of the open parts at the nominal stroke 5.583 mm:

| Part (closed lower edge) | clearance to the rotating hex AF 4.0 | AF 4.05 | against the 5.8 slot wall (peg floating) |
| --- | --- | --- | --- |
| jaw, half-width 2.9 (0.0) | **0.449 mm** | 0.420 | -0.142 (intrudes into the slot void) |
| **tongue, half-width 2.05, closes at 0.0 (v4)** | **1.026 mm** | 0.997 | +0.434 |
| tongue closing at -1.0 (the old geometry) | 0.285 | 0.258 | -0.320 |
| tongue with the 6.0 mm V-notch mouth (half-width 3.0, closing at -1.0) | 0.000 (collides) | 0.000 | -0.944 |

At the class-f minimum strokes 5.088 / 4.991 mm: jaw 0.104 / 0.018 mm; **tongue closing at 0.0: 0.654 / 0.583 mm**; tongue closing at -1.0: 0.000 / 0.000. The tongue closing at z 0.0 needs a stroke of 4.20 to 4.27 mm for zero clearance and 4.5 to 4.57 mm with 0.3 mm clearance, which the 5.58 mm stroke meets with 0.5 mm of margin at the corners. The jaw's clearance at the corners (0.02 to 0.10 mm) is positive but below 0.3 mm. **Against the slot wall** (the peg floating inside the 5.8 slot) the jaw needs 5.78 mm (6.08 with 0.3 mm): not met; this criterion does not close for the jaw.

**Cup versus swept peg.** Every wall with outward normal n and arrival direction d with d·n < 0 is undercut. The two lower side flats (210 and 330 degrees) of the v3 half-hex cup are undercut for entry from the opposite sides: numerically 67 percent of the 0.6 mm wall strip outside each slanted cup flat lies inside the swept hex, maximum penetration 0.60 mm (the whole wall). The reviewer's finding is confirmed in the strongest form: the cup cannot be entered. The closest feasible receiver is a flat seat, top at z -2.05 (0.05 mm below the peg flat), 4.8 mm wide, clearance to the swept hex 0.050 mm; the jaw closes the upper flats after landing. The jaw and tongue stay out of the swept peg when open (above), with the stroke window of section 7.3.

### 7.5 End plate and yaw sweep (item 3 of the review)

Slot ±4.545 (x) × ±2.6 (z) at the centre of end plate b, joined to the two channel arms (half-width 2.9). The peg hex rotates with the puck, so its section in the plane of the inner face is wider by 1/cos 15; the sweep at the tail face plane is ±1.554 mm and at the inner face (y -12) ±1.018 mm. End plate b and the caps are cut into three pieces by the V (the middle triangle hangs on the F3 wall). The thrust annulus is replaced by the washer (7.3). Class f is applied to the 304 parts per the cited table (±0.05 up to 6 mm, ±0.1 for 6 to 30 mm).

### 7.6 Data and power

BLE only (ESP32-C3). Range, occlusion and latency UNRESOLVED. No power transfer.

## 8. Passive retention when unpowered (CPL-009, Q11)

`requires_power_to_hold = false`, `mechanism_kind = geometric_interlock`. Components: keeper-tongue, jaw, keeper-rod, keeper-crank, keeper-link, keeper-rocker, keeper-rocker-tip, keeper-motor, m3-post, seat, thrust-washer, yaw-puck, head-peg. Both states are held by hard stops past dead centre with no power and no spring (qualification: section 7.3 load reversal). Only release and closing are powered; bounded independent release is declared true (M3 drives the crank over both dead centres; the release means is a motor in the unit's own receiver).

What is shown on paper: pin coordinates and dimensions, offsets and tolerance corners, the stop geometry, force balance for holding, release and closing with the four-bar's actual lever, the tension path, cam-out plus pitch bending, load reversal. What is **not** shown: friction and wear of pins and stops, shock and vibration, the radial load rating of the M3 shaft, creep of PA12, the pin-in-slot detail, the puck-to-shaft joint.

## 9. Pre-alignment justification (CPL-005, Q36)

Alignment is geometric, passive, in three parts (`geometric_guide`): the corrected roll-in channel (7.2), the tongue seating feature (explicitly not a pre-alignment means), and the hex peg on a flat seat under a three-flat jaw with the 0.5 x 45 degree tip chamfer. Forces come from sliding contact, gravity, B's own lift drive and table friction; the closing force is M3 through the four-bar. No attractive force, so an undriven unit does not self-dock. **No axial or heading pre-alignment means exists, and a free approach cannot start a roll-in** (7.2). A reviewer should expect G6 to be justified on paper only.

## 10. Chain bending (Q31) resolution

Yaw turntable in kind unchanged: the puck turns about body z through (0, -8.2), driven by M2 through a single-start worm (module 0.3, lead angle 7.125 degrees) into a 27-tooth 304 sector (pitch r 4.05, ±21.5 degrees, working ±12, hard stops ±15 degrees). The **sector radius is unchanged (27:1)**; it moved up the yaw shaft 1.7 mm (centre z 11.70) and the shaft is 4.0 mm long (v3 2.1) so that the worm (axis 4.72 mm from the nearest arc) clears the keep-out; torsion stress at M2 stall 73.6 MPa (0.62 of shear yield), unchanged. Sector alternatives (module 0.3 worm, torque at the puck rated / stall, bending envelope mu at rated): 21 T 28.1 / 84.3 mN·m, 0.747; 23 T 30.8 / 92.3, 0.819; 25 T 33.5 / 100.4, 0.890; **27 T 36.1 / 108.4, 0.964**; 29 T 38.8 / 116.4, 1.03 (min worm z 12.20).

- **Face clearance** unchanged: 5.55 mm required at 12 degrees, 7.04 mm at 15 degrees (margin 0.96 mm). Peg sweep at the tail face plane 1.55 mm; the slot of 7.5 covers it.
- **Torque.** Design load at table mu = 1 is mu W (d1 + d2) = 0.4093 × 91.6 = 37.50 mN·m; ratio **0.964 at rated, 2.89 at stall**. So at rated motor torque bending works only for table mu up to about **0.96**; at stall 2.89.
- Sector tooth load, worm self-locking and the conditions under which bending works are unchanged from v3 (9.3 N at the design load, Lewis estimate assumed, worm friction ≥ 0.125 for self-lock, bending only on F0 or F3).

## 11. Risks and unknowns

1. **No steering or axial locomotion**: no axial or heading pre-alignment; docking needs a common lane and a free approach cannot start a roll-in.
2. **Docking by roll-in is a paper idea** with a corrected path: impact dynamics, whether the ring-driven roll lands inside the windows, closing dynamics unresolved.
3. **Release under the full design tension** needs 1.56 times M3's rated torque (stall 9 is 1.91 times the requirement).
4. **Load reversal of the lock** needs pin friction ≥ 0.10 to 0.14 (assumed play).
5. **Rod stroke at the class-f corners** (5.04 to 6.11 mm) is below 5.4 mm; the closing now needs 4.6 mm. The jaw clears the swept peg by only 0.02 to 0.10 mm at the corners and does not clear the slot wall for a floating peg.
6. **M3 shaft radial load** up to 16.7 N with no gearbox rating; bushing pressure 6.4 MPa taking the whole link force, no PA12 allowable cited. The M2 worm shaft has no outrigger (worm only 4.72 mm from the channel).
7. **Yaw torque margin 0.964 at rated** at the mu 1 bound.
8. **Roll lock**: free roll ±2.58 degrees; Hertz 783 to 1 107 MPa against 342 MPa first-yield rule of thumb; registration of jaw and seat; the lower half of the hex is open.
9. **Thrust washer** compatibility with the ±15 degree yaw; puck-to-shaft joint; cut end plate b (three pieces); strength of the cap strips.
10. **Rotated M1 group**: pinion at azimuth 170 degrees (box outside r ≤ 19.5 as in v3); CoM x moved to -0.888 mm; mass-dependent figures recomputed.
11. Tolerance assumptions (hole-position class f, Materialise service data), press fits, the 0.3 mm minimum detail of PA12 features, the bar/pin envelope exceeding r ≤ 20 by 0.02 mm nominal (0.2 mm at the tolerance corners).
12. Motors run by PWM limited to 3.0 V on a sampling specification; QT Py regulator 600 mA peak; heat of three motors.
13. Lumped placements and box approximations (harness, fasteners, link/rocker/rod envelopes, M3 shaft stub, gear squares). Assembly unverified. Mass is a mix of upper bounds and omitted items.
14. Three-unit chain only; the five-unit claim of Q31 is untested.

## 12. Response to the v3 reviews

### Retention review v3 r1, section 6 (seven items)

| # | Required | What v4 does |
| --- | --- | --- |
| 1 | Re-derive the roll-in kinematics with the table-height constraint, re-cut the slots and the end-plate and cap cuts, recompute the windows, show a coordinate table | Done in 7.1: table-height check both senses, peg path coordinates every 10 degrees, the circle about the bottom vertex, centre height 25.5 at 30 degrees. Arcs re-cut through the F3 bottom vertices (V toward +z). Windows recomputed in 7.2 (clearance 0.591 / 0.441 mm per side, heading by the two-point jam with 6.5 mm engagement: 11.27, 8.21, 7.65 degrees). End plate slot ±4.545 × ±2.6 and the three-piece cut in 7.5. **Closed on paper** |
| 2 | Re-derive cup, jaw and tongue from the corrected arrival, with a swept-volume clearance check and a consistent insert box; state which parts locate the jaw and show the 0.05 mm fit survives | The swept-volume check (7.4) shows the lower half-hex cup cannot be entered (0.60 mm penetration); it is replaced by a flat seat (box z -3.3..-2.05, matches its description) and a three-flat jaw. Open jaw clearance 0.449 mm, tongue 1.026 mm at the nominal stroke, tongue 0.58 to 0.65 mm at the class-f corners. **Not closed:** which part locates the jaw relative to the seat and whether the 0.05 mm per side fit survives is UNRESOLVED (jaw on the keeper slider in PA12 guides, seat on the washer-carried web) |
| 3 | Resolve the end plate and the yaw sweep (opening size, remaining thrust area) and restate the tension path | Slot ±4.545 × ±2.6; thrust annulus 4.28 mm² < 5, thrust moved to a 304 washer (7.3); tension path restated with a new groove engagement and stress table. **Reservation:** washer vs yaw rotation compatibility UNRESOLVED |
| 4 | Say which part carries the rocker pivot and the stops; class f applied correctly; stroke with tolerances; load-reversal behaviour and the friction needed | Rocker boss on M2 carries the pivot, the outrigger post carries the stops (7.3). Class f by size, by v3 convention and as a conservative bound all given; stroke 5.04 to 6.11 mm over the corners; load reversal with the required pin friction 0.10 to 0.14. **Not closed:** the stroke at the corners is below the 5.4 mm of the old closing (meets the 4.6 mm now needed); real friction not cited |
| 5 | Rate or avoid the M3 shaft radial load; add the pitch couple to the keeper z force | Outrigger bushing post (PA12, bore 2.6, 1.3 mm bushing next to the crank); radial load 11.0 / 16.7 N, bushing pressure 4.2 / 6.4 MPa (whole link force). Pitch couple added: 5.26 N on top of 4.91 N cam-out = 10.17 N. **Not closed:** PA12 bearing allowable not cited; gearbox share not computed; M2 worm shaft unprotected |
| 6 | Re-derive the V-notch closing claim with wedge and flank friction against full-weight friction, or drop it | Re-derived (7.2): lateral fraction 0.393 at flank mu 0.15, ratio 1.00 (rated) against mu W; **dropped as a pre-alignment means**, kept as a seating feature |
| 7 | Keep the statement that no axial or heading pre-alignment exists; add that a free approach cannot start a roll-in | Both stated in 7.2, 9 and the declaration limitations |

Other points answered: the review's arithmetic items (§5): arc branch (fixed), heading divisor (6.5 mm used), class f applied by size (3), stroke with tolerances (4), end plate thrust vs the cuts (3), the insert box vs the described cup (replaced by a seat whose box matches), the closing ratio 4.8 on half-weight friction (re-stated on both bases). The reviewer's note that a re-dock of a previously docked pair is the only case served is kept in 7.2.

### Originality review v3 r1

The review passed v3 with one **high**: **C6 Roombots, D2** (a motor-driven crank-and-slider that pushes the latch into an externally non-reversible singularity with no power in the connected state, same locking principle as the v3 over-centre four-bar), and noted that a second high against Roombots would fail rule 2. **v4 does not change the locking principle**: the keeper is still a motor-driven over-centre four-bar with two stops past dead centre and no power to hold. v4 adds an outrigger bushing post, a thrust washer, a flat seat with a three-flat jaw and a V-shaped channel; none of these is taken from the Roombots connector (flat hermaphrodite plate with four hooks on a rotating clip, no pins). I do not argue the high away. The differences the review listed (gendered peg with an annular groove, tongue in groove, separate hex lock, arc roll-in entry, the whole unit rolling to dock) remain, and the roll-in entry changed geometry (V-shaped, F3 landing) without becoming closer to Roombots' scooping hook motion. Whether any v4 cell rises to a second high against Roombots is for the independent reviewer.

## 13. Author self-check against the originality corpus (NOT the official review)

This is the author's own check against `docs/originality/reference-corpus.md`. It is **not** the Q61 matrix, it is not independent (Q61 s4), and it does not count for G7 or G8. Descriptor text in the corpus comes from abstracts and search summaries, so my comparison inherits that limit. Ratings use the Q61 anchors (N, L, M, H). I also use the v3 reviewer's findings, which I did not make.

| Reference | D1 geometry | D2 coupler | D3 locomotion | D4 assembly | D5 visual | Note |
| --- | --- | --- | --- | --- | --- | --- |
| A1 BH6 microbots | N | N | N | N | N | |
| B1 Replicators | N | N | N | L | N | |
| **C6 Roombots** | N | **H** | L | L | N | Motor-driven crank mechanism into a non-reversible position, unpowered hold; the v3 reviewer's high stands for v4 (same locking principle); the form differs (section 12) |
| **Q64-C21 CONRO / C12 PolyBot G2** | L | **M** | N / M | L / M | L / N | Groove-on-pin hold retained; release principle is a motor-driven four-bar (no SMA, no spring, no latch plate) |
| **C7 / C8 M-Blocks** | L | L | **M** | **M** | L | Rigid body pivoting over an edge; unchanged |
| **Q64-C22 HEXEL, Q64-C23 hexagon pivoting** | **M** / L | L | L / **M** | L | L | Hexagon outline; unchanged |
| C4 ATRON, C13 SuperBot, C17 HyMod | N/L | M / L | N | L | N | Motor-driven hooks locked without power (v3 reviewer's moderates) |
| C11 Molecubes, C14 CKBot, C22 Sambot, C16 FreeBOT, C18/19, D1, C23, C9, X3 | L / N | L / M | N / L | L | N / L | as in v3 |

**Points the reviewer should look at first.** 1. D2 against Roombots and ATRON (motor-driven locks that hold unpowered): the principle is shared, the form differs. 2. D2 against CONRO and PolyBot: tongue in groove on a protruding pin. 3. D3/D4 against M-Blocks and hexagonal pivoting modules: edge-rolling docking. 4. v4 adds no new element I could find in the corpus: the V-shaped channel, the flat seat plus three-flat jaw and the washer are mechanical details of the same concept.

- Exclusion 1 (cube with internal flywheel): not present. Exclusion 2 (needle- or particle-like silhouette): not present. Family A: single rigid polyhedron, edge pivoting, couplers on faces; the ring, yaw puck and keeper are internal moving parts.
- What the corpus cannot tell me: whether a hexagonal log-roller with an internal ring lobe and a roll-in dock exists outside it. Nothing here claims absolute originality.

## 14. Changes from v3

| Area | v3 | v4 | Why |
| --- | --- | --- | --- |
| **Roll-in arc (lead's error 1)** | arcs centred on the bottom vertices, running from the mid-height vertices over the top to the face centre (the wrong branch of the circle) | arcs from the F3 bottom vertices (±12.75, 22.084) to the face centre, a V toward +z; verified with the table-height condition | retention review §3.1; Q69 §1. The error began in the lead's v2 spec and was carried by the v2 review and v3 |
| **Arrival direction (lead's error 2)** | v4 spec: "the peg arrives from above, 30 degrees from the vertical", so keep the v3 lower half-hex cup | the final approach is 30 degrees from the body x axis (nearly sideways); the chord is 30 degrees from the vertical | swept-volume check, section 7.4 |
| Landing face, rest orientation | F0, identity | F3, [0, 0, 1, 0]; lobe parked at body -z | lead decision |
| Receiver | lower half-hex cup insert (304) + upper jaw | flat 304 seat + three-flat 304 jaw | the cup walls lie entirely inside the swept peg |
| Tongue | 7 mm wide, 6.0 mouth V-notch, closes at z -1.0, stroke 5.2 needed | 4.1 mm wide, semicircular notch, closes at z 0.0, stroke 4.6 needed | V-notch ratio 1.00 < 1.5; swept volume; corner clearance 0.58 to 0.65 mm |
| Groove engagement | 1.5 mm² (two prongs) | 3.11 mm² (upper half annulus under the tongue) | new tongue geometry |
| Thrust | PA12 annulus on end plate b, 20.7 mm² | 304 thrust washer, 7.56 mm² on the cap strips (annulus left 4.28 mm²) | end-plate slot ±4.545 × ±2.6 and the V cut |
| Puck | journal in a dia 8.8 bore, front wall y -12..-11, box z -1.5..2.6 | rear web behind the channel (y -7.0..-4.4, z -3.5..6.9) + column | the channel occupies y -12..-7 |
| Layout | M1 (-4, 12.18), M2 (5.25, 10), M3 (11.25, 10.25) | M1 group rotated 60 deg about the ring axis; M3 (-4.5, 12.272); M2 (5.25, 11.70); sector z 10.7..12.7; IMU, driver-2, harness moved | channel keep-out; the upper interior holds two motor columns |
| Four-bar | C (11.25, 10.25), Pv (1.5, 13.3), arm +-46 deg | mirror: C (-4.5, 12.272), Pv (5.25, 15.322), arm +46 deg; crank travel 202.5 deg (upper sweep) | link crosses the sector corner in the other sweep |
| M3 shaft | unrated, loads the gearbox | outrigger post and bushing (PA12) | review item 5 |
| V-notch | declared pre-alignment | seating feature only | review item 6 |
| Tolerance application | ±0.05 on 6 to 30 mm coordinates | class f by size (and a conservative ±0.1 bound) | review §5 item 3 |
| Mass | 41.849 g | 41.741 g | new parts vs smaller tongue, jaw and four-bar |
| CoM x | +0.04 mm | -0.888 mm | M1 group moved |
| Peak / average power | 4 807 / 2 899 mW | 4 807 / 2 899 mW | unchanged |
| Yaw ratio at mu 1 | 0.96 | 0.964 | mass |

Notes from the implementation, recorded as stated:

- The v4 spec's 5.4 mm rod-stroke floor was written for the tongue closing at z -1.0. With the lead's decision to close at z 0.0 the need is 4.6 mm; the four-bar was not redesigned, so the stroke 5.58 mm is a margin, not a target.
- The lower sweep of the mirrored four-bar was rejected because its link crosses the sector top corner by 0.59 mm; the upper sweep (202.5 degrees of travel) clears it by 0.267 mm after a 0.75 mm half-width.
- The yoke-bar and rocker-plate boxes are AABB envelopes of swept parts; the rocker envelope is clipped at z 19.99 to stay out of the tail wall slab (the capsule envelope top is 20.06).
- Mating roll 0 now fails the table-contact check and 180 is used; I did not investigate why beyond the evaluator report.
- Per the lead's decision the washer is recorded as the flat thrust face; the reservation about the yaw rotation is recorded in 7.3 and 15.
- The first-draft pitch couple reaction (jaw-seat plane to tongue plane, arm 1.4 mm) is a modelling choice made by the implementation agent, not a source.

## 15. Unresolved list (for the lead)

1. SLS tolerance holds for any particular printer (Materialise is a service page); four-bar hole-position tolerances are assumed; the 0.3 mm minimum detail of PA12 features.
2. Roll-in closing dynamics, whether the ring-driven roll lands inside the windows, and the capture window (CPL-006); why mating roll 0 now fails the evaluator's table check.
3. Release under the full mu = 1 design tension (1.56x rated M3 torque); mu for steel on steel is a provisional bound; crank stop wear; pin friction; pin-in-slot design; **M3 radial shaft load rating and bushing allowable**; M3 heat and cycle life; the M2 worm shaft radial load.
4. **Load reversal** at the dead centre: required pin friction 0.10 to 0.14 for an assumed 0.05 mm play.
5. **Rod stroke** at the class-f corners (5.04 to 6.11 mm) is below the 5.4 mm floor; jaw clearance 0.02 to 0.10 mm at the corners; the jaw does not clear the slot wall for a floating peg (needs 5.78 mm).
6. Roll lock: registration of jaw and seat to the 0.05 mm per side fit; Hertz stress above first yield; the seat web as a cantilever; the open lower half of the hex.
7. **Thrust washer vs ±15 degree yaw** (a flat normal to y against a puck rotating about z); the puck-to-shaft joint, the cap bore, the three-piece end plate b and cap, the stem guide slot and the pin-in-slot slot.
8. Pin and yoke-bar envelope against r ≤ 20 (0.02 mm nominal, about 0.2 mm at corners) and the 0.06 mm approach to the sector top; a 25-tooth sector removes both at a yaw cost.
9. The rotated M1 group: pinion at azimuth 170 degrees outside r ≤ 19.5 (as v3); CoM shift; lobe analysis redone (clearance after tipping 0.69 to 0.84 mm).
10. Worm/sector friction (≥ 0.125 for self-lock); yaw margin 0.964 at rated; sector tooth strength (assumed Lewis factor).
11. Tooth strength, backlash, profile and contact ratio of all gears; press fits of the gear band; assembly sequence; lumped placements and box approximations.
12. Motor PWM voltage constraint, PMD sampling-specification status, QT Py regulator and charging; heat generally (three motors).
13. BLE range, occlusion and latency; through-coupler data and power (none declared).
14. Lateral couplers, steering, axial locomotion, **five-unit chain** (Q31).
15. Independent retention-review and originality-review records for v4; the author self-check above is not the review. The Roombots D2 high is carried over unchanged.
