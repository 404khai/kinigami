# Retention review: cand-a v3, r1

candidate_id: cand-a
candidate_version: 3
author: Claude Opus 5.5 (engineering lead) with Claude Sonnet 5.5 (cand-a v3 implementation agent)
reviewer: reviewer-a3-retention (Claude Sonnet 5.5, independent session, no authorship in cand-a v3)
outcome: fail

Date: 2026-11-06. Reviewed: `dossier-v3.md` (all sections), the `retention`, `alignment` and the keeper, keeper-linkage, keeper-motor, cup-insert, yaw-puck, yaw-shaft, head-peg, cap-l and endplate-b entries of `candidates/cand-a/declaration.json` (SHA-256 0025a534f9fc2496d8010e97ad69754485b5e671de23a8261ec11237e16fa1bb, from `shasum -a 256`, equal to the hash in the dossier), `retention-review-v2-r1.md` (its section 6), protocol section 8, Q062 G6, Q063, Q036, Q031 item 6, Q047, Q067, Q068, CPL-005/006/008/009. This is a paper judgement under protocol section 8, not a test (Gate 2/3). All "reviewer" figures were recomputed by my own scripts (four-bar solved by circle intersection, 720 001-point sweeps, 256 tolerance corners; roll kinematics by rotation matrices). Sources spot-checked: the Materialise PA12 page (the text "±0.3% (with a lower limit of ±0.3 mm)" and "minimum wall 1 mm" are there) and the Precision Microdrives 206-109 sheet (rated 3, typical stall 9 mN·m, typical peak-efficiency torque 4 mN·m, sintered bronze bearing, no radial load rating). EOS, ATI, ISO table, Lee and Dynalloy were not re-read (the spring and SMA are gone).

## 1. Judgement in brief

The retention mechanism (over-centre four-bar keeper) is a large improvement on v2. I reproduced every one of its stated numbers and found it supported on paper, with the reservations in section 2. The alignment means are not. The roll-in channel, the central pre-alignment means, is cut on the wrong arc of its own circle: the arc that the neighbour's peg actually follows in the receiving unit's frame is the other branch, in the lower half of the tail face, not the declared arc over the top. This contradicts the justification text ("moves in B's frame along exactly this arc") and is not a missing detail (section 3.1). The same error propagates to the cup, which as declared sits in the path of the true arc (section 3.3). Because an alignment means is declared and contradicted by its own geometry, I record `fail`, not `unresolved`. The v2 review (section 2.2 item 3) accepted this arc after a check that did not apply the table-height constraint; I disagree with that check and show why.

## 2. Retention (304 tongue in the peg groove, held by a motor-driven over-centre four-bar)

### 2.1 Principle and unpowered state: supported

A 1.0 mm tongue in a 1.4 mm annular groove (dia 3.0) is a plain geometric interlock, and tension is reacted on a groove shoulder with no power. `requires_power_to_hold` false, `mechanism_kind` geometric_interlock, and the SMA and the spring are gone. The remaining question is whether the tongue can leave the groove, and that is governed by the four-bar.

### 2.2 Four-bar: recomputed, correct

Inputs: crank r 2.0 at C (11.25, 10.25); rocker pivot Pv (1.5, 13.3); rocker arms b 3.0 and a 4.5 at -46 degrees; link L = D = |C - Pv| = 10.21592 mm.

| Quantity | Dossier | Reviewer |
| --- | --- | --- |
| Grashof (r + L = 12.216 <= D + b = 13.216, crank shortest, adjacent to ground) | crank-rocker | agree; every crank angle is feasible (no locking of the loop) |
| extended / folded dead centres (|B - C| = 12.216 / 8.216) | crank 151.14 / 328.61 degrees | 151.1415 / 328.610 degrees |
| stops 10 degrees past: open / closed | 141.14 / 338.61 | the stops lie on the outer side of the 197.47 degree working range, so the working range crosses both dead centres, as claimed |
| rocker angle at the stops | 107.46 / 24.77 degrees | 107.460 / 24.769 |
| link-line offset from the crank axis | 0.407 / 0.283 mm | 0.4069 / 0.2834 (open / closed) |
| output pin z at the stops, travel over the full cycle | 17.25 / 11.67; 11.63 to 17.29 | 17.253 / 11.670; 11.628 to 17.289 |
| rod stroke between the stops | 5.58 mm | 5.583 mm |
| link force / tongue force | 1.006 to 1.722 (1.72 at closed, 1.01 at open) | 1.006 to 1.722 |
| maximum tongue-to-crank lever dz/dθ | 3.025 mm, at 225.6 degrees | 3.0252 mm, at 225.605 degrees (tongue lower edge then at +2.27 mm, so it is still engaging the shoulders; the figure is not over-conservative for the friction phase) |
| lever at the stops | (implied) 0.488 at closed | 0.409 open, 0.488 closed; 4.92 N x 0.488 = 2.40 mN·m, as stated |
| tolerance corners (256), margin past dead centre | 6.76 / 6.12 degrees | 6.756 / 6.118 degrees, reproduced with the dossier's own tolerances |

Link buckling (Euler, 0.8 x 1.5 section, about 1.2 kN) and rod buckling (dia 0.8 over 18 mm pinned: 122 N) are right. Link, rod and pin stresses at 8.5 N are trivial.

**Do tongue loads push the crank into its stop in both states? Yes for the loads that matter, with a qualification the dossier does not state.** Virtual work gives crank torque = F_z · dz/dθ for a load F_z on the rod. At the open stop dz/dθ = +0.409 mm/rad and at the closed stop +0.488 mm/rad (z has its maximum at the extended and minimum at the folded dead centre). So:
- closed state: a +z (tongue-out) load gives a torque into the stop. A -z load drives the crank back to the folded dead centre, which for that sign is a stable equilibrium (z minimum), so the state is retained but the stop is unloaded;
- open state: a -z (tongue-in) load goes into the stop; a +z load takes the crank to the extended dead centre (stable for that sign), state retained.
So "tongue loads push the crank into its stop" is exact for one load sign per state and, for the other sign, the crank settles at the dead centre within 10 degrees of the stop and the state still holds. The consequence is that after such a load the crank sits on an unstable-for-the-opposite-sign dead centre, and a later load of the opposite sign could carry it through if it exceeds the gearbox and pin friction. For the realistic loads this does not occur: the closed-state cam-out from roll torsion always pushes the jaw outward (+z, the corner-flat normal on the upper flats), which is the into-the-stop sign. The open state carries no engaged load. Tension (y) acts on the tongue's slot walls, not the linkage, apart from friction when releasing. Judgement: the holding principle is supported. The dossier statement is incomplete for load reversal; a Gate 2 item (cyclic or alternating loads), not a contradiction.

**Tolerance.** The dossier uses ±0.05 on the crank and pivot coordinates (11.25, 10.25, 13.3, 1.5). Its own table (ISO 2768-1 f) gives ±0.1 for 6 to 30 mm, so three of the four coordinates should be ±0.1. Rerunning the 256 corners with ±0.1 on those three: margin 6.11 degrees at the open stop and 5.36 degrees at the closed stop, still positive in every corner. A pure pivot-to-crank position error as large as ±0.3 mm (SLS scale, if the pivot were carried by a PA12 part) leaves at least 5.1 degrees of margin with L unchanged. The over-centre geometry therefore survives the cited machined tolerance and is robust, but the dossier does not say which part carries the pivot and the stops. Not shown: bearing and pin clearance. A radial play of 0.05 mm at each link pin changes the effective link length by under 0.1 mm, which moves the margin by about 0.5 degree, so this does not reverse the conclusion. Rod stroke 5.58 mm (needed 5.2, derivation of 4.2 mm open edge not given) varies from 5.13 to 6.07 mm over the strict class-f corners, so the margin is not guaranteed on the low side, while the open tongue edge at 4.58 mm clears the peg corner (about 4.0 mm at x = 3.5) by about 0.6 mm on the nominal path. Minor.

### 2.3 Forces and loads: recomputed

W = 0.041849 kg x 9.80665 = 0.41039 N; 4 mu W = 1.642 N; torsion W R/2 = 5.233 mN·m (two neighbours 10.47); pitch W/2 x 36 = 7.39 N·mm; yaw design load mu W (d1 + d2) = 0.4104 x 91.6 = 37.59 mN·m against 3 x 27 x 0.446 = 36.1 (ratio 0.96); worm efficiency tan 7.13 / tan(7.13 + 8.53) = 0.446; landing energy 0.4104 x 3.416 = 1.402 mJ; hex free roll acos(2.05 / 2.3094) = 27.4 degrees from the 30 degree corner position, so lash = 2.6 degrees; torsion contact arm sqrt(2.3094² - 2.05²) = 1.063 mm and F = 5.233 / (2 x 1.063) = 2.46 N; Hertz p0 for a 0.1 mm radius against a flat, E* = E / (2(1 - nu²)) = 109.9 GPa: 785 MPa and 1 110 MPa; release crank torque 1.642 N x 3.025 mm = 4.97 mN·m, rated 3 gives 0.99 N of tongue friction. All correct.

The cited loads are the candidate's declared loads (Q31 item 6 asks for exactly that); I do not second-guess the declared mu bound or the 4 mu W form.

**Tension path.** Stresses are 0.2 to 1.1 percent of the allowables, so the path closes in strength by two orders of magnitude even with the corrections below. Two geometry statements do not hold as written, neither changes the conclusion:
- The thrust is taken on "an annulus r 2.8 to 3.8 around a dia 5.6 peg hole" of end plate b (20.7 mm²). But end plate b is cut by the two roll-in arcs (5.8 mm wide, through the 7 mm depth from the tail face), which meet at the face centre, and the v3 dossier no longer states the ±4.2 mm face-opening relief that v2 had for yaw. The ±12 to 15 degree yaw sweeps the peg 1.23 to 1.55 mm at the plate plane (dossier section 10), whereas a dia 5.6 hole leaves 0.49 mm per side to the 4.619 mm corners. The yaw and the 5.6 mm hole cannot coexist. A relieved opening leaves the puck front face (dia 7.6) bearing on roughly 6 mm² of plate (reviewer estimate), 0.27 MPa, still 0.5 percent of 50 MPa. The inconsistency is a dimension error for the yaw/chain-bending slice, not a retention defect.
- The groove contact area "2 x 0.5 x 1.5 = 1.5 mm²" is not derived from the V-notch (6.0 mm mouth, 3.1 mm root): at z = 0 the 30 degree walls are at |x| = 2.42, outside the 2.0 mm hex flats, so the tongue overlaps the shoulders only near the notch root. Even a tenth of the area is about 11 MPa against 205 MPa.

**Torsion and cam-out.** The full hex-in-hex enclosure removes the v2 half-hex problem (item 3 of the v2 list). The 4.92 N cam-out (10.47 mN·m) carried by the stop at 2.4 mN·m is right. Pitch bending is not included in the cam-out: the 7.39 N·mm couple, reacted by the jaw (1.4 mm) against the tongue and the end plate (2 to 3 mm), adds a further z force of about 3 to 5 N between parts of the same rigid keeper, so the net on the stop is smaller than the sum. It does not change anything in kind. The load on the M3 output shaft (sintered bronze bearing, 8.5 N in the dossier, up to about 17 N if pitch is added) has no rating in the PMD sheet. A radial shaft shift of 0.2 mm would remove the offset of 0.28 mm at the closed stop, so the lock depends on a bearing nobody has rated. This is the one element in the holding path with no support and it is Gate 2 work (a radial-load measurement or an outrigger bearing); the dossier states it plainly.

### 2.4 Release (CPL-008, CPL-009)

M3 rated 3 mN·m covers tongue friction up to 0.99 N; the bound tension 1.642 N needs 4.97 mN·m, 1.66x rated, 0.55 of typical stall (9), above the typical peak-efficiency torque (4). Stall 9 is "typical", the sheet is a sampling specification, and the motor is PWM-limited to 3.0 V; the 1.81x stall margin is therefore a typical, not a guaranteed, figure. CPL-008 allows release to fail or be blocked under load, and CPL-009 asks for bounded independent release, not release at the bound tension. The dossier releases after the controller has relaxed the tension (chain yaw 0). `bounded_independent_release` true is consistent. This is reported honestly. Judgement: it does not contradict passive retention; Gate 2 item.

### 2.5 Accepted weaknesses, classified

| Weakness | Contradicts passive retention or the pre-alignment justification? | Where it belongs |
| --- | --- | --- |
| Hertz stress above first yield at the hex corners at the bound torsion | No. It predicts local indentation of 0.01 to 0.02 mm (flat-bearing width at 205 MPa) and lash growth with cycles, not a loss of the interlock. The corner radius is the author's assumption | Gate 2/3 (wear, lash growth, hardness or corner radius) |
| Release near stall at the full bound tension | No (section 2.4) | Gate 2/3 release test |
| Yaw 0.96x rated at mu 1 (bending holds to table mu 0.96) | No. It is the chain-bending slice (Q31), not retention or alignment. The envelope is stated; I recomputed the figure | Gate 2/3 |
| Unrated M3 shaft radial load | Not a contradiction, but it is an unsupported element in the holding path | Gate 2 |

## 3. Pre-alignment means

### 3.1 Roll-in arc channel (`cap-l`, `cap-r`, `head-peg`, `endplate-b`): contradicted by its own geometry

Principle as stated: when B rolls 60 degrees about its leading bottom edge, a neighbour's peg on the common axis moves in B's frame along a circle of radius R about that pivot vertex, ending at the face centre. The circle is right. The declared slot occupies the wrong 60 degrees of it.

Reviewer derivation (x right, z up, B docked on F0, centre at height a = 22.084 mm, A's axis fixed at O = (0, a); the peg axis of any unit lying on a side face is at height a):
- B rolls to the right about its right bottom vertex V = (R/2, 0) (world) by β. A roll the other way about V would sink B into the table (centre height 12.75 mm at 30 degrees, 0 at 60 degrees), so it is not available.
- The B-frame position of O, computed by rotation matrices at β = 0, 15, 30, 45, 60 degrees: (0, 0), (-5.28, -4.05), (-9.33, -9.33), (-11.88, -15.48), (-12.75, -22.08) mm. So the peg starts at the other bottom vertex and travels up the lower half of the face to the centre, along the circle about V between 120 and 180 degrees (a near-straight 25.5 mm diagonal, sagitta 3.4 mm), arriving moving up and to the right at 30 degrees above horizontal.
- Cross-check by height: with B resting on F1, the horizontal line through its centre meets the face frame at s(0.5, 0.866); the only point on it at 25.5 mm from V is (-12.75, -22.08), the bottom vertex. The dossier's start point (R, 0) maps to world height 0, i.e. onto the table, where the peg cannot be.
- The declared slot (radius 25.5 about each bottom vertex, "from the mid-height vertices to the face centre", crest 3.4 mm above the mid-height line) is the 60 to 120 degree arc of the circle about V. Rolling reaches it at no point. It is mirrored into the upper half of the face from the true path. The two curves meet only at the face centre.

The v2 review verified the arc by assuming the world-fixed point sits at B-frame (R, 0) at the start; that assumption was not checked against the table-height condition, so its "the arc is correct" finding cannot be relied on. v3 inherits it ("the v2 review checked it").

Consequences: (a) the justification sentence is false for the declared geometry; (b) as declared the slots cannot guide the peg through a physical roll, so none of the window figures (0.59 mm, 0.44 mm at the SLS minimum, ±2.09/±1.94 mm mouth, heading) describe a working channel; (c) the correct slots lie in the lower half, through the bottom vertices, which also changes the end-plate cut (section 2.3), the keeper side from which the peg arrives (3.3) and the mouth position relative to the table. The window arithmetic itself is correct (clearance (5.8 - 4.619)/2 = 0.590, (5.5 - 4.619)/2 = 0.440, 0.41 with the peg at +0.05; mouth 2.09/1.94; atan(0.59/5) = 6.7 degrees and atan(0.44/5) = 5.0 degrees), except that the divisor 5 mm is the v2 engagement; the engagement is now 6.5 mm. The exact two-point jam angle for 6.5 mm engagement is about 11.3 degrees nominal and 8.2 degrees at the SLS minimum, so the quoted figures are conservative whatever the divisor.

The SLS tolerance is cited correctly and applied correctly (±0.3 mm on 5.8 mm, minimum clearance 0.44 mm; no PA12 functional clearance under 0.6 mm; 1.0 mm wall). v2 review item 6, partly: see section 4.

Principle: sound. Declared dimensions: contradict the principle. Unpowered: yes (gravity and B's lift drive). Outcome for this means: fail.

### 3.2 Tongue V-notch seating (`keeper`, `keeper-linkage`, `keeper-motor`, `yaw-puck`, `head-peg`)

The spring snap force has been replaced by the M3 closing force (rated 0.99 N, stall 2.97 N), which is the correct thing to do. The notch depth (6.0 - 3.1)/2 / tan 30 = 2.51 mm and the ±1.45 mm lateral reach are correct arithmetic. The force reasoning compares the closing force with "head-end friction mu W / 2 = 0.205 N" (ratio 4.8). That ratio ignores the wedge and flank friction (the dossier says so). With flank friction 0.15, the lateral push on a 30 degree half-angle wedge is F (sin α - mu cos α) / (cos α + mu sin α) = 0.39 F, so 0.39 N at rated closing force. A free neighbour has to be moved by the full weight friction mu W = 0.41 N at the mu 1 bound, not half of it, so the ratio at the bound is about 1, not 4.8; at table mu 0.5 it is about 1.9. With flank mu 1 the wedge cannot centre at all. The V-notch is secondary (the channel is supposed to deliver the peg to within 0.44 mm of the cup), and its force claim is flagged unresolved by the author. Judgement: supported in kind; the stated ratio is not demonstrated at the declared bound; Gate 2 (CPL-006 sweeps).

### 3.3 Hex peg in the hex-in-hex cup/jaw roll lock (`head-peg`, `cup-insert`, `keeper`, `yaw-puck`)

Principle: a six-fold keyed fit that fixes roll and carries torsion on flats; with the 4.10 mm cup and jaw the free roll is ±2.6 degrees (recomputed). Supported for the closed state. The enclosure against a peg that is already seated in the cup is fine. What is not supported is the way the peg gets there, in three respects:
- **Arrival direction.** With the declared roll-in the peg approaches the cup from the +x side moving 30 degrees below horizontal (declared geometry), or, by the correct kinematics of 3.1, from below left or right, moving 30 degrees upward. The v2 review asked for this to be shown; v3 declares an upward-opening lower half-hex cup and does not check it against either. Swept-volume check on the declared arc (reviewer, hex AF 4.0 turning 60 degrees along the path): a cup whose entry-side rim is at hex mid-height (z = 0) or anywhere above about z = -1.1 mm is crossed by the peg at about 82 percent of the arc; the rim has to be below about -1.6 mm to clear. On the true arc, from below, the cup insert block (x ±2.4, z -3.5 to -1.6) lies in the path (the true arc passes (-2.6, -1.7) and (-1.9, -1.2)). The cup has to open toward the arrival side or be inverted; neither is declared.
- **Box versus description.** The cup insert box tops out at z = -1.6, which is 0.4 mm above the peg's lower flat (-2.0): not a 2.05 mm deep lower half-hex. The declaration and the dossier give two incompatible cup shapes. The puck also needs a lateral entry window for the peg (cylinder dia 7.6, peg path crossing |x| < 3.8), which is not declared.
- **Cup/jaw registration.** Cup (pressed into a PA12 puck) and jaw (on a slider guided in a PA12 cage, 0.6 mm clearance rule) must register to within 0.05 mm for a 4.10 mm hex-in-hex fit with the peg at 4.0. If the slider is located by PA12, the two hex halves can be offset 0.3 mm, so the enclosure narrows to about 3.8 mm and the peg cannot enter; the stated 0 to 0.1 mm clearance per side (0 at the tolerance extreme: line-to-line, which also cannot enter) is not shown to be achievable. Not decisive alone; unresolved.

Tip chamfer 0.5 x 45 degrees: the lead-in exists. Judgement: roll lock principle supported; its integration with the roll-in is unresolved, and the declared cup geometry is inconsistent with itself and with the path.

### 3.4 Axial and heading pre-alignment: now correctly stated as absent

The dossier states plainly (section 7.2, section 9, declaration limitation 1, risk 1) that no axial or heading pre-alignment exists and that docking needs a common lane (axial position inside about ±0.5 mm and heading inside the windows) as a precondition. I accept the statement as honest and as bounding the claim to the in-plane roll-in (v2 item 5, first half). Two things the statement does not say. The body has no axial motion, so a pair that is not already lane-aligned and axially engaged cannot start a roll-in: the 6.5 mm axial engagement at the start of the roll is not reachable from a free approach, only by rolling out of a previous dock. The re-dock of a previously docked pair is the only case the means can serve. And the 60-degree relative roll during entry (absorbed by hex symmetry) and zero relative roll after the step (B ends on F0 with A on F0) are consistent with my kinematics.

## 4. The six v2 section 6 items

| # | Required in v2 | v3 | Judgement |
| --- | --- | --- | --- |
| 1 | Specify the toggle; closing, holding, opening and open-state force balance | Specified fully. Every dimension reproduces. Holding is geometric in both states. Closing 0.99 N rated at the worst point; opening 4.97 mN·m at the bound | Met for the retention principle. Load-reversal qualification (section 2.2) and the unrated M3 shaft remain |
| 2 | Consistent tension path with a puck-to-body bearing and stress check | Groove, 1.0 mm front wall, end plate thrust, 3.5 mm journal, hollow 304 shaft, all checked; margins 100x to 600x | Met in strength. Two geometry statements do not hold (annulus around the dia 5.6 hole against the channel and the yaw sweep; groove overlap area) with no effect on the margin |
| 3 | Torsion check for the half-hex cup; release under the design tension | Full hex-in-hex enclosure; cam-out 4.92 N; release 4.97 mN·m, 1.66x rated | Met on paper. The pitch couple is not added; Hertz above first yield; release near stall; all Gate 2 |
| 4 | Cup opening direction, clearance, tongue tip form, real axial lane | Cup opens up; 0.05 mm per side; 30 degree wedge, 0.4 mm tip face; lane ±0.5 mm | Partly met. The tongue tip and the lane are fixed. The cup direction is declared but is not compatible with the roll-in arrival (section 3.3), and the declared insert box is shallower than the described cup |
| 5 | Supply axial and heading pre-alignment or state that none exists; the 60 degree relative roll | Stated that none exists; relative roll 0 after the step | Met as a statement (section 3.4). The scope limit (no free approach) should be recorded |
| 6 | Cite an SLS tolerance; show slot clearance and over-centre offset survive it | Materialise ±0.3 mm, class f for machined parts; clearance 0.44 mm; margin >= 6.1 degrees | Met as arithmetic (I verified the citation). The slot clearance is for the wrong arc (section 3.1); class f is mis-applied by a factor of two to three coordinates, which still leaves 5.4 degrees |

## 5. Arithmetic and consistency errors found

No arithmetic error in the four-bar, force, stress or window numbers affects its conclusion. Items to correct:
1. Roll-in arc placed on the wrong branch of its circle (section 3.1). This is a kinematic error, not an arithmetic one, and it is decisive.
2. Heading window uses a 5 mm divisor, left from v2; the engagement is 6.5 mm (conservative, section 3.1).
3. ISO 2768-1 class f ±0.05 is applied to the 10.25, 11.25 and 13.3 mm coordinates, for which the cited table gives ±0.1 (margin 5.36 and 6.11 degrees instead of 6.12 and 6.76).
4. Rod stroke margin (5.58 against 5.2) is not tolerance-checked: 5.13 to 6.07 mm over the strict class-f corners; the 4.2 mm open edge is not derived.
5. End plate thrust annulus and the dia 5.6 hole are incompatible with the arc cuts and the ±12 to 15 degree yaw sweep; the v2 ±4.2 mm relief has disappeared from the v3 text.
6. The cup insert box (top at z = -1.6) does not match the described lower half-hex cup.
7. The closing ratio 4.8 uses the half-weight head-end friction and no wedge or flank friction.

## 6. What a further version needs

1. Re-derive the roll-in kinematics with the table-height constraint (the peg's B-frame path is the circle about the pivot vertex between 120 and 180 degrees, mirrored for the other direction), re-cut the two slots (and the end-plate and cap cuts) on that path, and recompute the windows from the corrected geometry. Show a drawing or a coordinate table of the slot and of the peg path against the pivot vertex.
2. Re-derive the cup, jaw and tongue layout from the corrected arrival direction (the peg arrives from below at 30 degrees above horizontal, so the cup, the puck entry window and the keeper side change), with a swept-volume clearance check of the 4.0 mm hex rotating 60 degrees along the path against the insert, puck wall, tongue and jaw, and a consistent insert box. State which parts locate the jaw relative to the cup and show that the 0.05 mm per side fit survives their tolerances.
3. Resolve the end plate and the yaw sweep (opening size, remaining thrust area) and restate the tension path on the corrected cuts.
4. State which part carries the rocker pivot and the stops and apply class f correctly; show the stroke with tolerances; state the load-reversal behaviour (dead-centre resting state) and a bound for friction needed to hold it.
5. Rate or avoid the M3 shaft radial load (outrigger bearing, or a radial load figure), and add the pitch couple to the keeper z force.
6. Re-derive the V-notch closing claim with wedge and flank friction against the full-weight friction of the neighbour, or drop it as a pre-alignment means.
7. Keep the statements that no axial or heading pre-alignment exists, and add that a free approach cannot start a roll-in.

Items the author reported (Hertz above first yield, release near stall, yaw 0.96x rated) can stay as Gate 2/3 matters; none of them is what the verdict rests on.

## 7. Basis of the outcome

Under protocol section 8 the record states for each means the principle, the governing geometry and forces with declared dimensions, and the reasoning that it works unpowered. For retention I find the principle and the dimensions sufficient on paper (the four-bar reproduces exactly, the load path closes by a wide margin), with the reservations above. For the roll-in channel the declared dimensions contradict the principle and the roll lock cannot be integrated with it as declared, so alignment is not physically justified and I record `fail`. Had the arc been correct, the remaining gaps (cup and jaw registration, V-notch force, end plate relief, unrated shaft) would have made the outcome `unresolved`. A pass is a paper judgement only and would not have shown that the mechanism works.
