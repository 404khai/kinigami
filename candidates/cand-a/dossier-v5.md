# cand-a v5: hexagonal-prism tumbler with lift ring, roll-in peg coupler and machined keeper frame (Family A)

Authors: Claude Opus 5.5 (engineering lead, all design decisions) with Claude Sonnet 5.5 (cand-a v5 implementation agent: derived values, files, this dossier). Date: 2026-11-07. Label: **exploratory**. Declaration: `declaration.json` (schema_version 1, candidate_version 5, SHA-256 `c1a3adceedfb3201676891c769c3e0b27667ee5c0330e7c3a5ab8a9e350ad169`). File layout follows Q65: `declaration.json` is the current version; the v1 to v4 bytes are kept in `declaration-v1.json` to `declaration-v4.json` (v4 SHA-256 `f6c18f80dd14815538e923cdb9c1f7c3c514fc7d22d55518d0c45063ef62b05d`); the dossiers are `dossier.md` (v1), `dossier-v2.md` to `dossier-v4.md` and this file. No earlier file was edited.

This is a paper-gate dossier (Q38 Gate 1). It does not show that any mechanism works. Every number below comes from a cited source, from an explicit derivation, or is marked **UNRESOLVED**. v5 answers `retention-review-v4-r1.md` (sections 5 and 7); section 12 maps each item to what changed. The scripts are `gen_v5.py` (declaration generator, with `gen_v5_head.py` and `gen_v5_tail.py`), `analysis_v5.py` (output `analysis_out_v5.txt`), `v5calc.py` (loads, tolerance corners, thrust), `v5geo.py` (configuration-space search of the closed receiver), `fbg.py`, `fr5.py`, `grv5.py`, `jc5.py` in the lead's scratchpad, not in the repository.

## 1. Result at a glance

Official evaluator (`zig-out/bin/kinigami-gate1`, ReleaseSafe build of the pinned toolchain, code revision a96e210). **No v5 review records exist**, so G6 to G8 cannot pass.

| Item | Outcome | Why |
| --- | --- | --- |
| G1 stowed sphere | pass | D = 58 181.29 µm (certified radius 29 090.644 µm), limit 60 000 µm |
| G2 packaging | pass | 2 926 pairs tested, 0 interfering, 0 capped, 0 boxes outside the shell (3 cavity primitives). **Caveat:** boxes are rectangular stand-ins; the saddle box is mostly bore void and its insert material lies in the end plate b window; the stop lugs and M3 shaft stub are not boxed; several masses are upper bounds |
| G3 evidence | pass | 77 components, every one cited |
| G4 budgets | pass | mass 42 905 mg declared and summed; peak 4 807 mW against 19 425 mW; average 2 899 mW; endurance 1 608.14 s (reported only) |
| G5 chain | pass | 2 sites, 3-unit straight chain. Mating roll 0 fails (table_contact false) as in v4, **180 is used** and passes |
| G6 | unresolved | retention-review record missing |
| G7, G8 | unresolved | originality review missing (section 13 is only the author's self-check) |

Overall evaluator outcome: **unresolved** (G1 to G5 pass; G6 to G8 unresolved).

Key numbers: stowed diameter 58.18 mm, declared mass **42.905 g** (v4 41.741 g; +1.16 g of 304 frame parts), W = 0.4208 N. Four-bar (size-rule class f on the frame): margin 5.64 / 6.09 deg, stroke 5.088 to 6.068 mm. Vertical free play P 0.05 to 1.05 mm (nominal 0.55). Thrust Hertz 28 to 36 MPa (304 on 304). T_rel = 0.522 N. Release at the mu = 1 bound needs 1.07 x M3 stall: blocked.

Statements to read together with the table:

- **The vertical stack is not absorbed.** A 304 flexure in the push rod (the first v5 plan) was found infeasible (section 7.3): 0.7 mm of travel at 0.41 N stores about 0.6 mJ, 50 to 130 mm³ of fully stressed spring against about 30 mm³ for the whole keeper. By the lead's decision there is no flexure; the stack becomes a **declared vertical free play** (7.3).
- **The roll lock is not a qualified function.** Roll lash is +-0.5 deg at the tight corner, +-12 deg nominal and unlimited (the 60 deg hex period) at the loose corner.
- **Reduced margins that do not close:** open-jaw clearance to the swept peg is 0.104 mm at the size-rule worst stroke (0.052 and 0.000 mm in the wider cases) with no allowance for peg height; the tongue overlap falls to 0.14 mm² when the peg sits 0.9 mm low.
- **Release at the full mu = 1 bound tension is blocked** (1.07 x stall); the operating rule is release at T <= 0.522 N.
- **The frame is one machined part only on the middle-triangle piece**; the seat is not registered to it.

## 2. Concept and family membership

Unchanged from v4. Family A (Q62 s3): one rigid polyhedral body, a regular hexagonal prism (circumradius 25.5 mm, 28 mm long) that rolls over its edges, driven by an internal lift ring with one lobe; axial couplers on the two end faces: a 304 hex peg (head) and a tail receiver with a V-shaped roll-in channel, a yaw turntable, a seat and jaw, a keeper tongue and a motor-driven over-centre four-bar. v5 changes the thrust face (304 collar on a 304 saddle), moves the lock geometry onto a machined 304 frame, and replaces the v4 jaw cavity by a larger pocket with a declared free play. No SMA, no spring, not a cube, no flywheel, no magnet.

## 3. Geometry: stowed and deployed

Unchanged from v4: rest orientation [0, 0, 1, 0] (F3 down, lobe parked at body -z); R 25.5 mm, apothem 22.0836 mm, cavity r 20 mm, head peg tip y 28.5 (engagement 6.5 mm), stowed sphere 58.181 mm (evaluator). Sites: head (0, 22 000, 0) µm, tail (0, -14 000, 0).

## 4. Q12 packaging and component list

Layout as v4 (M1 group rotated 60 deg, M3 at C = (-4.500, 12.272), M2 (5.25, 11.70), sector z 10.7 to 12.7). v5 changes:

- **Removed:** PA12 outrigger post (`m3-post`), PA12 rocker boss on M2, 304 thrust washer.
- **Keeper frame (new, all 304, machined ISO 2768-1 class f), fixed to the middle triangle piece of end plate b** (the piece between the two arms of the V cut): `frame-m3` (bearing block OD 4.6, y -12 to -7.9, bore dia 2.0 over 2.4 mm, carries the two stop lugs), `frame-rocker-post` (2 x 2, z 14.32 to 16.32, carries the dia 1.0 pivot pin), `frame-base` (0.6 mm plate, x -2.2 to 6.3, y -12 to -11.4, z 10.7 to 14.32, joins the block, post and saddle into one part), `frame-saddle` (concave bore r 4.2, 1.4 high, |x| <= 2.6; the bore bottom at y -12.4 is 0.4 mm below the end plate inner face, so the saddle is an insert in a window of end plate b, flush with its outer face).
- **Puck collar** (new, 304): disc r 3.8, z 9.3 to 10.7, on the yaw shaft **above** the jaw and tongue envelope (their boxes reach z 8.63; 9.16 at the largest class-f stroke), so the thrust face cannot sit on the v4 column at z 6.9 to 8.6. The yaw-shaft box shrinks to z 8.7 to 9.3; the puck column (PA12) becomes x +-1.4, z 6.9 to 10.2.
- **Seat** top moves to z -2.45 (box z -3.3 to -2.45, 113 mg).
- **Channel clearance of the new parts** (distance to the arc centreline, wall 2.9, keep-out 3.2): base 3.31, rocker post 4.98, saddle box 4.82, M3 block 5.65 (surface 3.35 from the wall line), 249 deg stop lug 3.29 (0.39 mm clear of the wall; the v4 r 2.9 stop corner was 2.71).
- Where a box is a stand-in: the saddle (bore), collar (disc), crank envelope (contains the lugs), link, rocker, rod and yoke envelopes; the yoke bar corner is at r 20.02 (physical 19.96).

Assembly: no sequence verified; the puck-to-collar joint, the saddle insert window and the press fits are not shown assemblable.

### Parts (access date for every source: 2026-11-06; not re-read for v5)

Source set unchanged from v4 (EOS PA 2200; Materialise PA12 SLS +-0.3% / +-0.3 mm; amesweb ISO 2768-1 class f; ATI 302/304/304L/305 for all 304 parts including the frame and collar; Westfield; DigiKey; Aurubis; Grepow; Adafruit; Pololu; Precision Microdrives 206-109, a sampling/target specification with no radial load rating). Vendor product pages remain classed `datasheet`.

## 5. Mass and power budgets (reported)

**Mass 42 905 mg** (v4 41 741): removed washer 85, outrigger post 51, rocker boss 9; added frame-m3 488, frame-base 146, frame-rocker-post 149, frame-saddle 108 (insert volume), puck-collar 467; puck column 18 to 22, seat 166 to 113. Everything else as v4. **Peak 4 807 mW, average 2 899 mW, endurance 1 608 s** (reported only).

## 6. The lift-lobe mechanism

Gears and ring unchanged. Quasi-static lift at W = 0.4208 N (`analysis_out_v5.txt`): body-frame CoM (-0.885, 0.348, -0.294) mm, inside the support rectangle. Peak ring torque (ratio to 9.01 mN m rated) for CoM centred 3.14 / 3.72 / 5.07 / 6.99 mN m at mu 0 / 0.15 / 0.5 / 1.0 (2.87, 2.42, 1.78, 1.29); rolling toward -x 3.36 / 3.98 / 5.42 / 7.48 (2.68, 2.27, 1.66, **1.20**); rolling toward +x 2.92 / 3.46 / 4.72 / 6.51 (3.08, 2.60, 1.91, 1.38). Stall ratios 3.6 to 9.3. Maximum tip normal force 0.386 W. Lobe root stress 0.14 MPa; landing energy 1.437 mJ. With the ring turning at a uniform rate the tip clears 0.69 to 0.82 mm and returns to 0.0 to 0.19 mm at 60 deg; lead rule: the ring stops after tipping until landing is detected. Dynamics belong to Gate 2.

## 7. The coupler (design-guidance 4.2)

Head = hex peg, tail = receiver; no lateral couplers. Rules (lead): no functional PA12 clearance below 0.6 mm, no PA12 wall below 1.0 mm, no PA12 gear teeth; precision parts machined 304 class f.

### 7.1 Roll-in kinematics (time-ordered labels, review item 6)

World frame (X horizontal, H up), unit A fixed with its peg axis at O = (0, a). B lands on F3, coming from +X and rolling about the shared bottom edge P = (R/2, 0). The sense that keeps B's lowest vertex at H = 0 is the correct one (the other sinks it to H = -4.43 at 10 deg and -22.08 at 60 deg); the centre height is 22.084, 23.96, 25.11, **25.50 at 30 deg**, 25.11, 23.96, 22.084 mm.

Peg in B's frame **in time order** (roll angle from the start of the roll-in at B's other bottom vertex to docking at the face centre): roll 0: (12.750, 22.084); 10: (12.363, 17.656); 20: (11.212, 13.362); 30: (9.334, 9.334); 40: (6.784, 5.693); 50: (3.641, 2.550); 60: (0, 0). The distance to B's bottom vertex (-12.75, 22.084) is 25.5 throughout; the hex turns exactly 60 deg relative to B; the final approach is along 30 deg from the body x axis (nearly sideways). (v4 listed the same points in reverse time order under the same labels.) The mirror image serves approach from -X.

### 7.2 Align (windows at the slot and at the jaw, review items 3 and 7)

Slot unchanged (width 5.8, depth 7.0, mouths 45 deg x 1.5; SLS gives 5.5 to 6.1).

| Window AT THE SLOT | Nominal | SLS minimum slot |
| --- | --- | --- |
| clearance per side to the 4.619 mm peg | 0.59 mm | 0.44 mm |
| lateral at the mouth | +-2.09 mm | +-1.94 mm |
| height | +-0.59 mm | +-0.44 mm |
| heading (two-point jam, 6.5 mm) | 11.27 deg | 8.21 deg; 7.65 deg at AF 4.05 |
| axial | +-0.5 mm | +-0.3 to +-0.7 mm |
| roll | any multiple of 60 deg | |

| Window AT THE JAW (open jaw outer block x +-2.9, swept hex AF 4.0 / 4.05; clearance = distance) | Nominal stroke 5.582 | Size-rule min 5.088 | All +-0.1 min 5.035 | Frame + play min 4.631 |
| --- | --- | --- | --- | --- |
| jaw, height margin toward the jaw | 0.448 / 0.419 | **0.104** | 0.052 / 0.027 | **0.000** |
| tongue (closes at z 0, needs 4.20 for zero clearance) | 1.025 / 0.996 | 0.654 | 0.614 / 0.585 | 0.318 / 0.290 |

These are for a peg at nominal height. They contain **no allowance** for the peg-height offset (up to +-0.6 mm, both units' SLS +-0.3) or for the +-0.35 mm seat-to-frame stack, so the jaw's upward window is a **reduced-margin item that does not close**. The four-bar is not changed. The jaw entry chamfer 0.6 x 30 deg is a seating lead-in only; no capture of peg-height offset is claimed (force argument dropped).

**There is no axial or heading pre-alignment means, and a free approach cannot start a roll-in** (docking needs B one roll step to the side in a common lane, only reachable by rolling out of a previous dock; capture window not claimed, CPL-006).

**Tongue seating.** V-notch not a pre-alignment means (lateral fraction 0.393 at flank mu 0.15; rated closing force 1.045 N gives 0.411 N against mu W = 0.421 N: ratio 0.98, stall 2.94, below 1.5). Semicircular notch r 1.55 with 30 deg wedge is a seating feature; with the vertical free play the peg may sit low and the notch then does not wrap the groove root (7.3).

### 7.3 Vertical stack, free play, roll lash, torsion (review items 2 and 3)

**Flexure rejected.** Required: absorb +-0.35 mm (0.7 mm range) and still push the jaw with (1 + mu) W/2 = 0.42 N to lift a neighbour's head end. Energy for k = 0.5 to 5 N/mm is 0.58 to 1.53 mJ (peak force 0.76 to 3.9 N); at the 304 bending energy density sigma_y² / 18E = 0.0117 mJ/mm³ that is 49 to 131 mm³ fully stressed. The best meander that fits the yoke bar (6 legs 3.3 mm long, 1 wide, 0.15 thick, k = 3.1 N/mm) has an elastic range of 0.15 mm at yield. Not used.

**Declared design (lead decision).** The jaw closes to a fixed height set by the crank stop on the frame (no jaw-to-peg contact needed). Jaw pocket: upper half-hex AF 4.20 +-0.05 (flat 2.10 above the receiver axis), legs 2.425 to 2.9, ceiling to z 3.05. Seat top: nominal z -2.45 (seat on the puck web, NOT registered to the frame).

Vertical free play P = (seat top to jaw top flat) minus the peg across-flats:

| Quantity | Value |
| --- | --- |
| nominal | 0.55 mm |
| stack (lead: both units' SLS +-0.3 plus the PA12 chain frame/end plate/puck/seat) | +-0.35 |
| class f: jaw flat, seat top, peg AF | +-0.05 each |
| **worst case (arithmetic sum)** | **0.05 to 1.05 mm** |
| lateral clearance per flat (pocket 4.20 +-0.05, peg 4.00 +-0.05) | 0.10 nominal, 0.05 to 0.15 |

**Escape and lash** (`v5geo.py`: exact polygons for the jaw legs, ceiling and seat, peg hex AF 4.0, breadth-first search of (x, z, roll) from the seated pose on a 0.05 mm / 1 deg grid, 0.01 mm / 0.5 deg for the tight corner; "escaped" = reaching |x| or |z| > 7 mm, which is outside the jaw and its channel):

| Corner | P | Reachable z | Reachable x | Roll lash | Escape |
| --- | --- | --- | --- | --- | --- |
| tight (peg 4.05, pocket 4.15) | 0.05 | 0 to +0.05 | +-0.05 | +-0.5 deg | none |
| nominal | 0.55 | -0.45 to +0.10 | +-0.35 | +-12 deg | none |
| loose (peg 3.95, pocket 4.25) | 1.05 | -0.90 to +0.15 | +-0.65 | free over +-30 deg (hex period 60 deg) | none |

So the peg cannot leave along either arc, laterally, up or down for any gap in the range: lateral exit needs the 4.0 mm hex to pass the 2.45 mm opening between the seat top and the leg lower edge, possible only after a roll of 30 deg (P > 0.62), and then the legs and ceiling still block it. Only the jaw and seat are in this model (the cap strips and tongue would block more); the tongue blocks the pull-out in y. **At the loose corner there is no roll lock.**

**Torsion contacts with the gap** (contact scan at the lash limit): nominal: three corner contacts (both jaw inclined flats and the seat top), equal normal forces F, torque = 2.141 mm x F. Tight: top-flat corner and seat corner, pure couple, arm 2.302 mm. Loose: no torque carried.

| Case | Torque | Nominal F | Tight F | Hertz p0 at the contacts (R 0.1 mm assumed, E* 110 GPa, line load F/1.4 mm) |
| --- | --- | --- | --- | --- |
| one idle neighbour tipped | 5.36 mN m | 2.51 N | 2.33 N | 791 MPa (2.31 x the 342 MPa first-yield rule of thumb) |
| two neighbours | 10.73 mN m | 5.01 N | 4.66 N | 1 119 MPa (3.27 x) |

Cam-out on the jaw z axis = F (5.01 N for two neighbours) plus the pitch couple W/2 x 36 mm over 1.4 mm = 5.41 N (modelling assumption, not a source): **10.42 N** on the tongue/jaw axis, carried by the over-centre stop.

**Groove engagement, single value (review item 6).** The tongue plate (|x| <= 2.05, 0 <= z <= 2.55, outside the r 1.55 notch) overlaps the peg shoulder (hexagon AF 4.0 with flats at +-z minus the r 1.5 groove root): **3.04 mm²** with the peg axis on the tongue axis (grid 0.002 mm; matches the reviewer's 3.04). The v4 analysis script tested the hexagon with the second constraint 0.5|x| + 0.866|z| (a non-regular shape), giving 3.11, and quoted the half-annulus 3.39; both are superseded. Over the vertical free play the overlap is 3.41 (peg +0.15), 3.34 (+0.10), 3.04 (0), 2.01 (-0.25), 1.19 (-0.45), **0.14 (-0.90)**, 0.05 (-1.05) mm².

### 7.4 Latch, release and the keeper frame (review items 1 and 4)

The four-bar is unchanged (`fbg.py`): C = (-4.500, 12.272), Pv = (5.250, 15.322), link 10.2159, crank r 2.0, arms 3.0 / 4.5, dead centres 28.86 / 211.39 deg, stops 18.86 / 221.39 deg, travel 202.53 deg, swing 82.64 deg, nominal stroke 5.582 mm, offsets 0.422 / 0.277 mm, peak lever 2.871 mm/rad.

**What the frame fixes.** The rocker pivot (post), both crank stops (lugs on the M3 block), the M3 crank-side bearing (bore dia 2.0 +-0.05 on a shaft dia 2.0 +-0.05: radial play at most 0.05 mm beyond a class-f fit) and the thrust saddle sit on one machined 304 part on the middle triangle piece; the rod is guided by the bore of the hollow 304 yaw shaft. The frame carries class-f tolerance only (no 0.3 mm SLS terms). **Not on the frame:** the seat (PA12 puck web), the cap strips; the yaw-shaft upper bearing is the collar in the saddle (-y and about +-38 deg), with **no +y restraint** (no room for a rear ring; 7.5).

**Tolerance corners (1 024 corners over r, b, a, C, Pv, L, rocker arm angle +-1 deg, stop +-0.05 mm at crank radius = +-1.43 deg):**

| Case | margin open / closed (deg past dead centre) | offsets open / closed (mm) | rod stroke min..max (mm) |
| --- | --- | --- | --- |
| **declared basis: class f by size** (r b a +-0.05, Cx Px +-0.05, Cz Pz +-0.1, L +-0.1) | **5.64 / 6.09** | 0.245 / 0.167 | **5.088 .. 6.068** |
| every coordinate +-0.1, r b a +-0.05 | 5.19 / 5.41 | 0.225 / 0.149 | 5.035 .. 6.113 |
| frame plus bearing and pin play (C, Pv +-0.15, L +-0.2, r b a +-0.1) | 1.73 / 3.59 | 0.077 / 0.097 | 4.631 .. 6.613 |

Margin is positive and the stroke is at least 4.6 mm in all three, which meets the tongue's need (4.20 to 4.65 mm) but, as the jaw table in 7.2 shows, not the jaw's. With the frame-plus-play case the link-line offset (the lever that pushes the crank into the stop) drops to 0.077 mm.

**Lock and load reversal.** Loads: tongue z force 10.42 N; at the open stop link force 11.3 N (ratio 1.082), crank moment 4.76 mN m, stop reaction at r 2.0 2.38 N; at the closed stop 17.1 N (1.645), 4.75 mN m, 2.37 N. A load that tries to change the state pushes the crank into its stop. Reversal at the dead centre needs pin friction >= 0.141 (open) and 0.103 (closed) for an assumed 0.05 mm play (derived bound, real friction not cited, UNRESOLVED). No flexure is in the path: the stop reaction is the whole story.

**Release (review item 5).** Friction on both faces under chain tension T: the peg shoulder on the tongue (normal force T) and the stem on the guide slot wall (normal force T), each at the mu = 1 bound (provisional): force on the rod 2 mu T. Peak crank torque 2 mu T x 2.871 mm/rad.

| Case | Value |
| --- | --- |
| design tension 4 mu W | 1.683 N |
| release torque at that tension | 3.366 N x 2.871 mm/rad = **9.66 mN m = 1.07 x M3 stall (9)**, 3.2 x rated (3): **blocked** at the full mu = 1 bound (CPL-008 allows blocked release) |
| **operating rule** | release only when T <= T_rel = 3 mN m / (2 mu x 2.871) = **0.5225 N** (1.24 W, 31% of the design tension); stall covers 1.567 N |
| closing, minimum tongue force over the stroke | rated 1.045 N, stall 3.135 N |

(v4 counted only the shoulder face: 4.70 mN m, 0.64 of rated.)

### 7.5 Thrust face (review item 4)

Collar (304, convex cylinder r 3.8 +-0.05, 1.4 high, coaxial with the yaw axis) on the saddle (304, concave r 4.2 +-0.05, covers +-38 deg about -y): contact holds through +-12 deg yaw and the +-15 deg stops because both are coaxial with the yaw axis. Tension 1.683 N; line contact 1.4 mm; Hertz p0 = sqrt(F' E* / (pi R_eq)), E* = 109.9 GPa (304 on 304, nu 0.3), R_eq = r1 r2 / (r2 - r1):

| r1 / r2 | R_eq | p0 |
| --- | --- | --- |
| 3.80 / 4.20 | 39.9 mm | **32.5 MPa** |
| 3.75 / 4.25 | 31.9 mm | 36.3 MPa |
| 3.85 / 4.15 | 53.3 mm | 28.1 MPa |

0.14 to 0.18 of 304 yield (205 MPa). The saddle radius is above the collar maximum (4.10) because the collar must not interfere; the bore bottom is 0.4 mm into the end plate window. UNRESOLVED: the collar-to-puck-column joint, the moment between the stem plane and the collar plane, the PA12 end plate b middle piece behind the insert, and the +y radial restraint of the collar.

### 7.6 End plate and yaw sweep

Slot +-4.545 x +-2.6 at the centre of end plate b, as v4; the washer and the cap-strip thrust area are gone; the thrust annulus rule is moot. End plate b and the caps are cut into three pieces by the V; the frame sits on the middle piece, which hangs on the F3 wall.

### 7.7 Data and power

BLE only. Range, occlusion and latency UNRESOLVED. No power transfer.

## 8. Passive retention when unpowered (CPL-009, Q11)

`requires_power_to_hold = false`, `mechanism_kind = geometric_interlock`. Components: keeper-tongue, jaw, keeper-rod, keeper-crank, keeper-link, keeper-rocker, keeper-rocker-tip, keeper-motor, frame-m3, frame-base, frame-rocker-post, frame-saddle, puck-collar, seat, yaw-puck, head-peg. Both states are held by hard stops past dead centre with no power and no spring. Only release and closing are powered. Bounded independent release is declared true with the operating rule T <= 0.5225 N.

**Tension path** (1.683 N, mu 1 provisional): peg shoulder (3.04 mm², 0.55 MPa; 11.8 MPa at the 0.14 mm² worst position) to tongue (web shear 1.68 MPa), stem 2 x 2 (shear 0.84 MPa), PA12 guide slot (5.2 mm², 0.32 MPa), puck column, collar, saddle (Hertz 28 to 36 MPa), end plate b middle piece, F3 wall. All far below limits; stress concentrations and the undesigned joints are not evaluated.

**Bearing pressures.** Loaded bearings in 304 (frame): M3 bearing block (d 2.0 x L 2.4 = 4.8 mm²) takes up to 11.3 N / 17.1 N link force: **2.35 / 3.57 MPa** (half: 1.17 / 1.79); collar on saddle 28 to 36 MPa (above). Remaining PA12 contact pressures, **no allowable claimed (none cited)**: stem in the guide slot 0.32 MPa; seat on the PA12 puck web at the torsion contact force 5.0 N over about 6.7 mm², about 0.75 MPa; peg tip and lead-in contacts against PA12 channel walls during entry (not computed). The M3 shaft material and the gearbox radial rating are not given by the datasheet.

## 9. Pre-alignment justification (CPL-005, Q36)

Alignment is geometric and passive: the roll-in channel, the tongue seating feature (explicitly not a pre-alignment means) and the hex peg in a seat and jaw with a declared free play and a lead-in chamfer. No attractive force. **No axial or heading pre-alignment means exists, and a free approach cannot start a roll-in.** The jaw chamfer is a lead-in, not a height-capture claim. A reviewer should expect G6 to be justified on paper only.

## 10. Chain bending (Q31) resolution

Unchanged from v4 except the mass: yaw 27:1 worm, torque ratio at table mu = 1 is 36.06 / (W x 91.6) = **0.935** at rated (2.8 at stall); bending holds at rated torque only for table mu up to about 0.94. Face clearance and sweep as v4. The yaw puck now turns a 304 collar bearing on the saddle; the yaw hard stops +-15 deg and working +-12 deg are unchanged. Worm self-lock needs friction >= 0.125 (UNRESOLVED).

## 11. Risks and unknowns

1. No steering or axial locomotion; no pre-alignment means; docking needs a common lane.
2. Docking by roll-in is a paper idea; impact dynamics and landing inside the windows unresolved.
3. **Release at the mu = 1 bound is blocked** (1.07 x stall); the rule T <= 0.5225 N needs the controller to relax the chain first.
4. Load reversal needs pin friction >= 0.10 to 0.14.
5. **Free play and roll lock**: P 0.05 to 1.05 mm; roll lash +-0.5 deg to free; the roll lock is not qualified.
6. **Open-jaw clearance** 0.104 / 0.052 / 0.000 mm at the stroke corners, no peg-height allowance.
7. **Tongue overlap** 0.14 mm² when the peg sits 0.9 mm low.
8. M3 radial load up to 17.1 N with no gearbox rating; M3 body to frame alignment not designed.
9. Yaw margin 0.935 at rated.
10. Hertz stress at the peg corners 791 to 1 119 MPa against 342 MPa rule of thumb; thin jaw legs (0.475 mm wide at the lower edge).
11. Collar-to-puck joint, +y collar restraint, saddle insert window in end plate b, three-piece end plate, tension couple.
12. Rotated M1 group, tolerance assumptions, motors on PWM with a sampling specification, QT Py regulator.
13. Lumped placements and box approximations; assembly unverified; masses are upper bounds.
14. Three-unit chain only; the five-unit claim of Q31 is untested.

## 12. Response to the v4 reviews

### Retention review v4 r1, section 7 (seven items)

| # | Required | What v5 does |
| --- | --- | --- |
| 1 | Fix the positions that define the over-centre lock: one machined 304 part (or give the SLS chain 0.3 mm), close the 0.3 mm bore play | One 304 frame on the middle triangle piece carries the pivot post, both stop lugs, the M3 bearing (bore play at most 0.05, in the frame-plus-play corners) and the saddle (7.4). Margin 5.64 / 6.09 deg and stroke 5.088 to 6.068 mm (declared); 1.73 / 3.59 deg and 4.631 to 6.613 mm with play. **Closed on paper for the lock; not one part with the seat** |
| 2 | Show the vertical stack, SLS apothem tolerance, a lead-in or compliance, or state the maximum height error | Flexure found infeasible (energy); no compliance. The stack is a declared vertical free play P 0.05 to 1.05 mm with a configuration-space escape check (7.3). Chamfer is a lead-in only. **Closed as a statement, not as a function**: roll lash and the tongue overlap degrade with P |
| 3 | State alignment windows at the jaw | 7.2 table: jaw 0.448 / 0.104 / 0.052 / 0.000 mm, tongue 1.025 to 0.318 mm, with the caveats. **Not closed**: reduced margin, no peg-height allowance |
| 4 | Replace the flat washer by a thrust face that works through yaw | Cylindrical 304 collar r 3.8 on a concave 304 saddle r 4.2, coaxial with the yaw axis; p0 28 to 36 MPa (7.5). **Closed on paper**; joint and +y restraint UNRESOLVED |
| 5 | Count the stem-slot friction, cite or remove PA12 as a crank bearing, guides through the middle triangle | Both faces counted: 9.66 mN m at the bound, T_rel = 0.5225 N (7.4). Crank bearing and pivot are now 304 on 304; remaining PA12 pressures listed with no allowable. The middle triangle is where the frame stands; the jaw and tongue guide there is the frame / shaft bore (rod) and the PA12 puck column (stem): **guide of the jaw body itself not designed** |
| 6 | Correct the time labels in 7.1 and the groove area | Done (7.1, 7.3): time-ordered list; single groove value 3.04 mm² with the corrected hexagon test |
| 7 | Keep the arcs, swept check, no pre-alignment statements, honesty | Kept |

### Retention review v4 r1, section 5 (arithmetic and consistency)

1. Time labels: fixed (7.1). 2. Groove area: single value 3.04 mm² (7.3). 3. Windows at the jaw: stated (7.2) and they are small. 4. Class f on PA12-carried positions: the lock positions are now on the 304 frame (7.4). 5. Release friction: stem slot included (7.4). 6. Washer vs yaw: washer removed, coaxial cylindrical thrust face (7.5); the "ordering" statement of v4 is withdrawn. 7. The jaw/tongue guide through the V middle triangle: the rod is guided by the shaft bore and the stem by the puck column slot; a guide for the jaw block is not designed.

## 13. Author self-check against the originality corpus (NOT the official review)

This is the author's own check against `docs/originality/reference-corpus.md`. It is **not** the Q61 matrix, it is not independent (Q61 s4), and it does not count for G7 or G8. Ratings use the Q61 anchors (N, L, M, H); I also use the v3 and v4 reviewers' findings, which I did not make.

| Reference | D1 geometry | D2 coupler | D3 locomotion | D4 assembly | D5 visual | Note |
| --- | --- | --- | --- | --- | --- | --- |
| A1 BH6 microbots | N | N | N | N | N | |
| B1 Replicators | N | N | N | L | N | |
| **C6 Roombots** | N | **H** | L | L | N | Motor-driven crank mechanism into a non-reversible position, unpowered hold; the v3 high stands for v5 (same locking principle) |
| **Q64-C21 CONRO / C12 PolyBot G2** | L | **M** | N / M | L / M | L / N | Groove-on-pin hold; release is a motor-driven four-bar |
| **C7 / C8 M-Blocks** | L | L | **M** | **M** | L | Rigid body pivoting over an edge |
| **Q64-C22 HEXEL, Q64-C23 hexagon pivoting** | **M** / L | L | L / **M** | L | L | Hexagon outline |
| C4 ATRON, C13 SuperBot, C17 HyMod | N/L | M / L | N | L | N | Motor-driven hooks locked without power |
| C11, C14, C22, C16, C18/19, D1, C23, C9, X3 | L / N | L / M | N / L | L | N / L | as in v3 |

**Points to look at first.** 1. D2 against Roombots and ATRON: same principle, different form. 2. D2 against CONRO and PolyBot. 3. D3/D4 against M-Blocks and hexagonal pivoting modules. 4. v5 adds a machined frame, a cylindrical collar-and-saddle thrust bearing and a pocketed jaw; I found no new corpus element in them. Nothing here claims absolute originality.

## 14. Changes from v4

| Area | v4 | v5 | Why |
| --- | --- | --- | --- |
| Lock geometry carrier | PA12 rocker boss on M2, PA12 outrigger post (0.3 mm bore play), stops on the post | one 304 frame (base, M3 block with 2.0 bore, rocker post, saddle insert) | review 7.1 |
| Thrust | flat 304 washer on cap strips | 304 collar r 3.8 on concave 304 saddle r 4.2, collar at z 9.3 to 10.7 | review 7.4 |
| Vertical stack | 0.05 mm per side fit, unstated stack | declared free play P 0.05 to 1.05 mm; no flexure (infeasible) | review 7.2 |
| Jaw | pocket AF 4.10, seats on the peg | pocket AF 4.20, closes to a fixed height, 0.6 x 30 chamfer lead-in only | lead decision |
| Seat top | z -2.05 | z -2.45 | declared free play |
| Release | shoulder friction only, 4.70 mN m | both faces, 9.66 mN m (1.07 x stall), T_rel 0.5225 N | review 7.5 |
| Groove overlap | 3.11 and 3.39 | 3.04 (corrected hexagon) | review 7.6 |
| Peg-path labels | reversed | time order | review 7.6 |
| Stop lug (closed) | r 2.9 corner 2.71 mm from the arc centreline | lug at 249 deg, 3.29 mm | channel clearance |
| Puck column | x +-2.2, z 6.9 to 8.6 | x +-1.4, z 6.9 to 10.2 | joins the collar |
| Mass | 41.741 g | 42.905 g | frame and collar in 304 |
| Yaw ratio at mu 1 | 0.964 | 0.935 | mass |

Notes from the implementation, as stated: the tension path and the stem guide (a stem at y -9 in a guide at y > -7) are inherited from v4 and not fixed here; the contact scan for the torsion arm uses the equal-force solution at the lash limit; the BFS models the jaw and seat only; the lead's stack +-0.35 mm is taken as given.

## 15. Unresolved list (for the lead)

1. SLS tolerance holds for any printer; four-bar hole fits and thin-leaf tolerances below 0.5 mm are outside the cited table.
2. Roll-in closing dynamics, landing inside the windows, capture window (CPL-006); why mating roll 0 fails the evaluator's table check.
3. **Free play and roll lock**: lash from +-0.5 deg to none; the roll lock is not qualified; the +-0.35 mm stack is the lead's figure, not derived; a registration of the seat to the frame is not possible in this layout (the seat and the frame are on different end-plate pieces).
4. **Open-jaw clearance** 0.104 / 0.052 / 0.000 mm with no peg-height allowance; tongue overlap 0.14 mm² at 0.9 mm low.
5. Release at the mu = 1 bound blocked (1.07 x stall); mu for steel on steel provisional; crank stop wear; pin friction and the load-reversal friction bound (0.10 to 0.14); M3 radial rating, shaft material and body-to-frame alignment; M3 heat and cycle life.
6. Collar-to-puck-column joint; stem-plane to collar-plane moment; +y radial restraint of the collar; saddle insert window in end plate b; three-piece end plate; fixing of the frame to the middle triangle piece and of that piece to the F3 wall; guide of the jaw block.
7. Pin and yoke-bar envelope against r <= 20 (0.02 mm nominal, about 0.2 at corners); the 0.06 mm approach to the sector top.
8. Rotated M1 group; worm friction; yaw margin 0.935; sector tooth strength.
9. Tooth strength, backlash, contact ratio of all gears; press fits; assembly sequence; lumped placements.
10. Motor PWM constraint, PMD sampling-specification status, QT Py regulator and charging; heat.
11. BLE range, occlusion and latency; through-coupler data and power.
12. Lateral couplers, steering, axial locomotion, **five-unit chain** (Q31).
13. Independent retention-review and originality-review records for v5; the author self-check above is not the review. The Roombots D2 high is carried over unchanged.
