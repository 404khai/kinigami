# Retention review: cand-a v4, r1

candidate_id: cand-a
candidate_version: 4
author: Claude Opus 5.5 (engineering lead) with Claude Sonnet 5.5 (cand-a v4 implementation agent)
reviewer: reviewer-a4-retention (Claude Sonnet 5.5, independent session, no authorship in cand-a v4)
outcome: unresolved

Date: 2026-11-07. Declaration `candidates/cand-a/declaration.json`, SHA-256 f6c18f80dd14815538e923cdb9c1f7c3c514fc7d22d55518d0c45063ef62b05d (from `shasum -a 256`, equal to the hash in `dossier-v4.md`). Reviewed: `dossier-v4.md` (all sections), the `retention`, `alignment` and `limitations` entries and the head-peg, seat, jaw, keeper-tongue, keeper-rod, keeper-crank, keeper-rocker-tip, keeper-motor, m3-post, thrust-washer, yaw-puck and endplate-b components; protocol section 8; Q062 G6; Q063 section 1; Q036; Q031 item 6; Q047; Q069; Q070; CPL-005/006/008/009; `retention-review-v3-r1.md` (section 6). Sources re-read: the amesweb ISO 2768-1 table (class f: 0.05 for 0.5 to 6 mm, 0.1 for 6 to 30 mm; confirmed). Not re-read this time: Materialise, EOS, ATI, PMD (v3 review checked Materialise and PMD; v4 cites the same pages). This is a paper judgement under protocol section 8, not a test (Gate 2/3). Every figure marked "reviewer" was recomputed in my own Python scripts (rotation-matrix roll kinematics, 4 001-point swept hex against boxes, four-bar by circle intersection with 1 024 to 4 096 tolerance corners).

## 1. Judgement in brief

The v3 failure is repaired. The roll-in channel now lies on the arc that the peg really follows, the arrival direction is right, the flat seat and three-flat jaw are consistent with the swept peg, and the four-bar (as declared) reproduces to the last digit. Nothing I found contradicts passive retention or justifies a `fail`: the keeper holds both states geometrically and the principle is sound.

I still cannot record `pass`. Several elements of the holding and alignment path rest on tolerance or registration assumptions that the cited evidence does not support, and in one case the declared numbers are contradicted by the author's own tabulated clearances (section 3.5). Protocol section 8 makes unsupported claims `unresolved`, not `pass`. The decisive items are: (a) the over-centre margin and the 0.05 mm per side jaw/seat/tongue fit depend on positions that are carried by PA12 parts (rocker boss, outrigger post with a 0.3 mm radial bore clearance, guides) while the dossier applies the machined class f; (b) the stated alignment windows are not valid at the receiver (the jaw leaves 0.03 to 0.12 mm of upward margin at the class-f stroke corners, not 0.44 mm); (c) the flat thrust washer cannot work with yaw as declared.

## 2. Roll-in kinematics, recomputed from scratch (task point 1)

World (X right, H up). A fixed, peg axis O = (0, a), a = 22.0836. B starts with centre (R, a) on the adjacent face and rolls about the shared bottom edge P = (R/2, 0), counterclockwise in the (X, H) plane, so its centre moves on the circle of radius R about P from 60 to 120 degrees. B body (x, z) maps to world (c + Rot(120 + s degrees)(x, z)), and at s = 60 that is (-x, a - z), the declared rest map.

| Check | Result (reviewer) |
| --- | --- |
| Lowest vertex of B during the roll | H = 0 (to 1e-15) for the whole roll. Centre height 22.084, 23.962, 25.113, 25.500 at s = 30, 25.113, 23.962, 22.084 |
| The other sense (sinking) | lowest vertex H = -4.43 at 10 degrees, -22.08 at 60 degrees: impossible, confirmed |
| Peg in B frame, s = 0, 10, ..., 60 | (12.750, 22.084), (12.363, 17.656), (11.212, 13.362), (9.334, 9.334), (6.784, 5.693), (3.641, 2.550), (0, 0) |
| Distance of the peg to B's vertex (-12.75, 22.084) | 25.5 at every s |
| Hex orientation in the B frame | rotation of -s degrees, 60 degrees in total, equal to the symmetry of the hex |
| Final approach velocity at the centre | direction (-0.866, -0.5), 30 degrees from the body x axis |

This agrees with the dossier's 7.1 numbers, the declared arcs (radius 25.5, centred on the F3 bottom vertices, from the far vertex to the face centre, opening toward +z) and the V-shaped keep-out. The arc the peg follows starts at the far bottom vertex (hex corner, outside the hex outline, so the 1.5 mm flared mouth is at a corner that is open to the side faces) and meets the face centre. Entry direction at the centre matches the seat and jaw layout: the peg comes from +z, so the seat (z below -2.05) is not in the path and the jaw and tongue (closed at z 0) are open above (lower edge at the stroke). Presentational error: the dossier 7.1 coordinate table is labelled in the reverse time order of its own prose (the list gives (0, 0) at roll 0 and (12.75, 22.084) at roll 60, whereas the roll starts at the vertex). The values themselves are right.

Bonus check: along the whole roll the radial direction of the arc stays fixed relative to the rotating hex (a corner direction), so the hex half-width across the slot is exactly 2.3094 at every s. The clearance 0.591 mm per side (0.441 at the 5.5 mm SLS minimum) is therefore exact, not just a bound.

**Swept volume (4.0 AF hex rotating 60 degrees along the path, exact polygon distances).** Jaw (half-width 2.9, open lower edge = stroke): 0.449 mm at the nominal stroke 5.583, 0.087 at 5.088, 0.018 at 4.991, 0 at 4.6. Tongue (half-width 2.05): 1.025, 0.654, 0.581, 0.284 mm. The old tongue closing at -1.0 touches at the class-f corner strokes. The seat (top -2.05) keeps 0.050 mm to the peg only at the end of the roll, and the peg approaches it monotonically from above (no earlier contact). With AF 4.05: 0.420, 0.058, 0 for the jaw. All of this reproduces the dossier 7.4 table. The tongue is checked against the hex although it actually meets the groove (dia 3.0), so it is conservative. The jaw leaves 5.78 mm for a floating peg, as the dossier says.

## 3. Findings per means

### 3.1 Retention (tongue on the groove root, held by the over-centre four-bar): principle supported, dimensions partly unsupported

**Principle and unpowered state.** Tension in y bears on the shoulder of the 304 peg and the 1.0 mm 304 tongue in the 1.4 mm groove, and the tongue is held closed by two hard stops 10 degrees past the dead centres. `requires_power_to_hold` false, `geometric_interlock`, no spring or SMA. Both states are held without power as long as the crank is against its stop and the stop side is the loaded side. Supported.

**Four-bar (reproduced).** C (-4.5, 12.272), Pv (5.25, 15.322), r 2.0, b 3.0, a 4.5 at +46 degrees, L = D = 10.2159. Grashof crank-rocker. Dead centres 28.858 and 211.390 degrees (crank-link collinear), stops 18.86 and 221.39, travel 202.53. Pin at the stops (3.095, 19.272) and (1.056, 13.690); z extremes 19.311 at 28.9 degrees and 13.650 at 211.4 degrees; stroke 5.582; link-line offsets 0.4217 and 0.2770; lever at the stops 0.454 mm/rad; peak lever 2.871 at 126.8 degrees; link/tongue ratios 1.082 and 1.645; link forces 11.0 and 16.7 N at 10.17 N. All as in the dossier. **Do loads push the crank into the stop?** dz/dθ is positive at both stops (z rises toward the extreme and the stops are 10 degrees beyond it), so an upward load in the closed state and a downward load in the open state give a torque toward the stop. Those are the loads the cam-out (always +z on the jaw) and the neighbour's weight can produce. The opposite sign pulls the crank 0.04 mm back to the unstable-for-reversal dead centre: honestly stated (friction at least 0.10 to 0.14). Closing, rod weight and shock loads of either sign are not quantified. Gate 2.

**Tolerance corners (reviewer, 1 024 corners over r, b, a, arm angle, L, C and Pv coordinates, stops).**

| Convention | Margin open/closed (degrees) | Stroke min..max (mm) |
| --- | --- | --- |
| dossier v3 convention (coordinates 0.05, stops 1.43 degrees) | 6.35 / 6.46 | 5.11..6.07 |
| class f by size (coordinates 0.1) | 5.19 / 5.42 | 5.02..6.14 |
| rod stroke needed | 4.6 | passes |

My values equal the dossier's table within noise (its stroke range 5.035 to 6.113 was without stop tolerance; I get 5.039 to 6.115 on the same basis). **The cited table is applied as a general dimension tolerance on parts that the dossier says are not machined.** The rocker pivot is carried by the PA12 rocker boss, the crank axis by M3 (itself in PA12 pockets), and the stops by the PA12 outrigger post. Materialise gives 0.3 mm as the lower limit. Rerun with Pv at 0.3 and C at 0.1: margin 2.3 / 3.4 degrees, stroke down to 4.78; with both at 0.3: margin -2.3 / 1.3 degrees (not over centre at the worst corner) and stroke 4.41 (below 4.6). With the stop position at 0.3 at radius 2.0 (8.6 degrees), the 10 degrees of offset disappear altogether. The M3 shaft (dia 2.0) runs in a 2.6 mm bore (radial clearance 0.3, "the 0.6 mm rule") in the PA12 post, so the crank axis can float 0.3 mm with respect to the stops: with stops fixed on the post and the shaft shifted worst-case, the closed-stop margin becomes -0.8 degrees and the open-stop margin 2.7. Under the actual link loads the shaft is pushed along the link force and the margin rises to 7.8 to 10.3 degrees (reviewer), so the loaded state is fine; the unloaded rest position is not controlled. This is an **unsupported assumption, not a contradiction**: unresolved, and it belongs in the record because the over-centre margin is the whole of the passive lock.

**Closure depends on a 0.05 mm vertical stack.** The pin z at the closed stop is only 0.04 mm above the dead-centre minimum. Therefore if the jaw (pocket 4.10 mm) cannot descend because the peg plus tolerances is more than 0.05 mm above its nominal height relative to the seat, the crank cannot reach the stop or even the dead centre (a 0.25 mm block means about 25 degrees short of it, on the unlocked side). The vertical relation between the peg axis of unit A and the seat of unit B includes the apothem and boss tolerances of two PA12 bodies (0.3 mm each by the cited service data), and the jaw z is set by the rod through the PA12 pivot chain. The dossier lists jaw/seat registration as unresolved but not the unit-to-unit peg height, and not that a jaw blocked by more than 0.04 mm defeats the over-centre state. Unresolved.

**Tongue notch engagement.** The semicircular notch r 1.55 over the groove root r 1.5 (0.05 clearance) seats the root from above; the peg cannot leave downward (the seat is 0.05 below its flat), laterally it is held by the notch edge, the seat and the jaw. Hex shoulder overlap area for the declared tongue (x within 2.05, notch r 1.55) is **3.04 mm2** (reviewer, grid integration), not the 3.11 or 3.39 mm2 quoted in three places in the dossier and declaration (3.39 is the full half-hex minus the root half disc). The stress is trivial either way (0.54 MPa against 205), so this is an inconsistency, not an effect on the margin. Also, only 0.7 mm of hex lies tip-side of the groove (reduced by the 0.5 x 45 degree chamfer), which is enough for bearing at these loads.

**Tension path.** Peg tip-side shoulder, tongue (pushed in -y), stem in the PA12 guide slot (bearing on its -y wall), puck, web (pulled onto the washer's +y face at y -7.0), 304 washer (its -y face on the cap strips at y -7.5), cap strips, wall ring. The direction chain is consistent (it closes in compression on the cap strips). Stresses are 0.1 to 1.6 MPa against 50 to 205: strength closes by two orders of magnitude.

**Thrust washer against yaw (task point 3).** The web (x within 3.6, face at y -7.0, 1.2 mm in front of the yaw axis at (0, -8.2)) bears on a washer face fixed to the caps. Turning the puck by psi about z moves the web corner at x = -3.6 by -3.6 sin(psi) in y: with no gap it penetrates the washer by 0.19 mm at 3 degrees, 0.77 mm at 12 degrees and 0.97 mm at 15 degrees; with the 0.2 mm of axial play that the 1.0 mm tongue in the 1.4 mm groove allows, the puck can only turn about 3.2 degrees before the corner meets the washer; a gap of about 0.8 mm (12 degrees) to 1.0 mm (15 degrees) would be needed. The author's reservation is correct and understated: as declared the flat washer is incompatible with the working yaw (12 degrees) and the hard stops (15 degrees), unless the tension path is allowed a play of about 0.8 to 1.0 mm that the groove does not provide. Classification: the tension path of the retention at a bent chain is unsupported (unresolved, the dossier says so); the yaw function itself is a chain-bending (Q31) matter for Gate 2. It is not a contradiction of passive retention in the straight state.

### 3.2 Flat seat plus three-flat jaw (roll lock), task point 4

Free roll: hex AF 4.0 in 4.10: acos(2.05/2.3094) = 27.4 degrees from the 30 degree corner position, lash 2.58 degrees (reviewer; the three upper flats and the seat flat bind at the same angle). Contact arm sqrt(2.3094^2 - 2.05^2) = 1.063 mm, force per contact T/(2 x 1.063): 2.45 N (5.22 mN m) and 4.91 N (10.44 mN m). Concentrating all of the torque on the top-flat corner pair is the upper bound of cam-out (sharing with the 30 and 150 degree flats gives less), so 4.91 N is conservative. Adding the declared pitch reaction (5.26 N) gives 10.17 N; link loads 11.0 and 16.7 N, 4.64 mN m on the stop at lever 0.454; stop reaction 2.32 N at r 2.0. All reproduced. The lower slanted flats are open, so the lock is a corner couple (jaw top flat to seat), not an enclosure. Hertz 783 to 1 107 MPa with an assumed 0.1 mm corner radius is above the rule-of-thumb first yield, as declared: local indentation and lash growth, not loss of the lock; Gate 2/3. The jaw has no declared lead-in on its slanted flats, so the jaw wedge that would centre an off-position peg is not shown; and the registration (section 3.1) is the real gap. Cam-out on the crank: pushes the crank into the closed stop (correct sign), a qualified single-sign statement.

Supported in principle. Not supported: registration and the closing of the jaw onto a peg off by more than 0.05 mm (unresolved).

### 3.3 Tongue seating feature and V-notch

The V-notch is correctly dropped as a pre-alignment means: reviewer ratio (sin 30 - 0.15 cos 30)/(cos 30 + 0.15 sin 30) = 0.393; rated closing force 1.045 N gives 0.411 N against mu W = 0.409 N: ratio 1.00 (stall 3.01), as declared. The remaining seating feature is not a claimed alignment means. Accepted.

### 3.4 Release and M3 (task point 5)

W = 41.741 g x 9.80665 = 0.4093 N; 4 mu W = 1.637 N; torque 1.637 x 2.871 = 4.70 mN m: 1.57 times the PMD rated 3 mN m (0.64 coverage) and 0.52 of the typical stall 9 (1.91x). Rated covers up to 1.045 N; closing rated 1.045 N, stall 3.135 N (minimum over the stroke is at the peak lever), against 0.205 N half-weight head-end friction and 0.409 N full-weight friction. All arithmetic reproduced. Two additions: the friction counted is only the tongue/shoulder face; the stem bears on the guide slot wall with the same normal force T and slides with it, so if both interfaces are at the bound mu 1, the friction doubles to about 3.3 N and 9.4 mN m (about the typical stall); with the unquantified pin friction. The dossier already specifies release at low tension (controller relaxes it first), which is consistent with CPL-008 (release may take time, fail or be blocked) and CPL-009 (bounded independent release). `bounded_independent_release` true and a nonempty means are consistent. Gate 2 item, not a contradiction. The motor runs at a PWM-limited 3.0 V from a sampling specification; no radial rating exists, and the outrigger bushing (PA12, 2.0 shaft in a 2.6 bore, 1.3 mm long) takes the link force: 4.2 and 6.4 MPa projected (11.0 and 16.7 N over 2.0 x 1.3), no PA12 bearing allowable or PV limit cited. The load reaches the post only after the 0.3 mm of play is taken up, and the gearbox bearing shares until then. Unresolved; Gate 2.

### 3.5 Windows with the SLS tolerance and the pre-alignment limits (task point 6)

The slot width 5.8 +/- 0.3 gives 5.5 to 6.1, clearance 0.591 / 0.441 per side (exact, section 2), mouth +/- 2.09 / 1.94, and the heading by two-point jam at 6.5 mm engagement (reviewer: 6.5 sin t + 4.619 cos t = 5.8 gives 11.27 degrees, 5.5 gives 8.21 degrees; AF 4.05 gives 7.65). Axial +/- 0.5 (groove 0.2 plus slot 0.3): the tongue sits 0.2 mm each way in the groove and the peg tip stays 0.5 mm clear of the washer face, with the tip chamfer.

**These windows do not hold at the receiver.** With the peg displaced in +z (toward the jaw) by the height window, the jaw touches the swept hex at +0.617 mm at the nominal stroke, **0.122 mm at the class-f stroke 5.088 and 0.025 mm at 4.991** (reviewer). So the effective height window at the end of the roll is 0.03 to 0.12 mm upward at the stroke corners, against the stated +/- 0.44. The dossier states that the jaw "does not clear the slot wall for a floating peg" but still presents the full window figures in section 7.2 and in the alignment justification. In addition, the vertical offset of two units (apothem and boss tolerance of two PA12 bodies, up to 0.6 mm if the cited 0.3 mm applies to each) exceeds the 0.44 window by its own cited source. The capture window is explicitly not claimed (CPL-006), and the principle of the guide is intact, so I classify this as **unsupported (unresolved)**, not as a contradiction: the channel still guides the peg; the claim of the window size is what lacks support.

**No axial or heading pre-alignment, free approach.** The dossier says so in 7.2, 9, 11 and in the declaration (limitation 1 and the alignment text): no axial or heading pre-alignment means exists; docking needs a common lane (axial +/- 0.5, heading inside the window, the peg already engaged 6.5 mm); **a free approach cannot start a roll-in**; only a re-dock of a previously docked pair is served. I confirm both statements. The peg starts at the far corner of the tail face, already engaged 6.5 mm, which is not reachable from a free approach because the body has no axial motion.

### 3.6 Magnetism and process

No magnet component, no magnetic alignment kind, no attractive force. Checks 1 to 5 of section 8 hold on the declaration as I read it (retention.mechanism and each alignment justification nonempty, every alignment names components, component_ids exist).

## 4. The seven v3 section 6 items

| # | v3 required | v4 | Judgement |
| --- | --- | --- | --- |
| 1 | Re-derive roll-in kinematics with the table-height condition, re-cut slots, recompute windows, show a coordinate table | Done (7.1, 7.2, 7.5). I reproduced the path, the arc branch, the arrival direction and the clearances; the table labels are time-reversed | Met for the kinematics. The windows are not valid at the jaw (3.5) |
| 2 | Re-derive cup, jaw, tongue from the corrected arrival with a swept-volume check and a consistent insert box; state which parts locate the jaw and show the 0.05 mm fit survives | Cup replaced by a flat seat and three-flat jaw; swept check reproduced; seat box matches its description | Layout and swept-volume met. Location of the jaw relative to the seat (PA12 guide, 0.3 mm rule) and survival of the 0.05 mm fit are not shown (author says so) |
| 3 | Resolve end plate and yaw sweep, restate the tension path | Slot +/- 4.545 x +/- 2.6 (my check: 2.309/cos 15 + 1.554 + 0.6 = 4.545, correct), washer, restated path (direction chain consistent) | Met for strength and area. The flat washer against the yaw is contradicted by the declared geometry for yaw above about 3 degrees (3.1) |
| 4 | State which part carries the pivot and stops, apply class f correctly, stroke with tolerances, load reversal | Part named (PA12 boss and post), class f applied by size, stroke 5.04 to 6.11, reversal friction 0.10 to 0.14 | Stated, but class f is applied to positions carried by PA12 parts; with the cited 0.3 mm the margin and stroke are not guaranteed (3.1). Unresolved |
| 5 | Rate or avoid the M3 radial load; add the pitch couple | Outrigger post, pitch couple added (10.17 N) | Added. No PA12 allowable cited; the 0.3 mm bore play; worm shaft unprotected. Unresolved, Gate 2 |
| 6 | Re-derive or drop the V-notch claim | Dropped; ratio 1.00 reproduced | Met |
| 7 | Keep no axial/heading pre-alignment and add the free-approach statement | Both stated | Met |

## 5. Arithmetic and consistency errors found

None changes the principle. To correct:
1. Dossier 7.1 coordinate list is labelled in the reverse time order of its prose.
2. Groove overlap area is quoted as 3.39, 3.11 and (reviewer) 3.04 mm2 for the declared tongue.
3. The windows (height +/- 0.44/0.59, lateral +/- 1.94/2.09) are stated at the channel but not at the jaw, where they shrink to 0.03 to 0.12 mm upward at the class-f stroke corners.
4. Class f is used for pivot, stop and crank positions that are carried by PA12 parts (rocker boss, outrigger post, 0.3 mm radial bore clearance).
5. Release friction counts only the shoulder face; the stem slot wall carries the same normal force.
6. Washer: the 12 mm wide flat face is not compatible with yaw above about 3 degrees; the "ordering" in the author's text ("the lead's decision is that this resolves the issue") overstates it.
7. The cap/middle-triangle of the V cut has no declared guide for the jaw and tongue, which pass through that region (the dossier lists the three-piece cut as not designed).

## 6. Classification of the reported weaknesses

| Weakness | Contradicts passive retention or justified pre-alignment? | Where it belongs |
| --- | --- | --- |
| Release at the mu 1 bound needs 1.57 x rated M3 torque | No (CPL-008/009 allow release to be slow or blocked; low-tension release is specified) | Gate 2/3 |
| Load-reversal at the dead centre needs pin friction 0.10 to 0.14 | No, but the friction is not cited: unsupported | Unresolved; Gate 2 |
| Rod stroke below 5.4 mm at corners | No (5.0 mm is above the 4.6 needed) | Gate 2 |
| Jaw clearance 0.02 to 0.10 mm at corners; jaw touches slot wall for a floating peg | Not a contradiction of the principle; it makes the claimed windows unsupported | Unresolved (3.5) |
| Unrated M3 shaft, no PA12 bearing allowable, 0.3 mm bore play | Unsupported element in the holding path | Unresolved; Gate 2 |
| Class f on PA12-carried positions; 0.05 mm per side registration; unit-to-unit peg height | Unsupported; decisive for whether the lock closes | Unresolved |
| Thrust washer against yaw | Unsupported for the bent state; contradicts the declared yaw only | Unresolved (G6); chain-bending slice |
| Hertz above first yield; yaw 0.964 of rated at mu 1; worm friction; assembly sequence; dynamics | No | Gate 2/3 |

## 7. What a further version needs

1. Fix the positions that define the over-centre lock: put the rocker pivot, the stops and the crank bearing on one machined 304 part (or give the SLS-carried chain the 0.3 mm tolerance and show a margin and a stroke of at least 4.6 mm in the corners), and close the 0.3 mm bore play (a bushing or a tight bore) or include it in the corners.
2. Show the vertical stack peg axis to seat to jaw to tongue to rod, including both units' SLS apothem tolerance, and a lead-in or compliance that lets the jaw close on a peg that is off by more than 0.05 mm; otherwise state the maximum unit-to-unit height error the lock tolerates (about 0.05 mm plus 0.04 mm of dead-centre travel).
3. State alignment windows at the receiver (the jaw, not only the slot): the upward height margin 0.03 to 0.12 mm at the stroke corners, or a longer stroke / narrower jaw that restores it.
4. Replace the flat washer by a thrust face that works through yaw (spherical or conical seat, a thrust bearing on the yaw axis, or a larger y play with the tension path restated), or limit the declared yaw.
5. Count the stem slot friction in the release torque, cite or measure a PA12 bearing allowable or remove PA12 from the crank bearing, and state guides for the jaw and tongue through the middle triangle of the V cut.
6. Correct the time labels in 7.1 and the groove area.
7. Keep: the arc geometry, the swept-volume check, the statements that no axial or heading pre-alignment exists and that a free approach cannot start a roll-in, and the honesty about release and reversal.

## 8. Basis of the outcome

Protocol section 8 asks, for retention and for each alignment means, for the principle, the governing geometry and forces with declared dimensions, and the reasoning that it works unpowered. Retention: principle and strength supported; the dimensions that make the lock actually close (positions carried by PA12 parts, bore play, registration) are not supported. Roll-in guide: kinematics and clearances supported; the claimed windows are not valid at the jaw. Seat and jaw: principle supported; registration unsupported. No declared dimension contradicts the principle of an unpowered holding or guiding means, so this is `unresolved`, not `fail`. A `pass` would be a paper judgement only and would not show that the mechanism works.
