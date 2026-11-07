# Retention review: cand-a v5, r1

candidate_id: cand-a
candidate_version: 5
author: Claude Opus 5.5 (engineering lead) with Claude Sonnet 5.5 (cand-a v5 implementation agent)
reviewer: reviewer-a5-retention (Claude Sonnet 5.5, independent session, no authorship in cand-a v5)
outcome: fail

Date: 2026-11-07. Declaration `candidates/cand-a/declaration.json`, SHA-256 c1a3adceedfb3201676891c769c3e0b27667ee5c0330e7c3a5ab8a9e350ad169 (from `shasum -a 256`, equal to the hash in `dossier-v5.md`). Reviewed: `dossier-v5.md` (all sections), the `retention`, `alignment` and `limitations` entries and the jaw, seat, keeper-tongue, keeper-rod, keeper-crank, keeper-rocker-tip, frame-m3, frame-saddle, puck-collar, yaw-puck, head-peg and endplate-b components; protocol section 8; Q062 G6; Q063; Q036; Q031 item 6; Q047; Q071; Q072; CPL-005/006/008/009; `retention-review-v4-r1.md` (section 7). No source was re-read this time (the v5 source set is the v4 set). This is a paper judgement under protocol section 8, not a test (Gate 2/3). Every figure marked "reviewer" was recomputed in my own Python scripts (four-bar by circle intersection with 2 048 tolerance corners, swept hex against boxes at 1 201 roll steps, breadth-first configuration-space search of the jaw and seat, grid integration of the tongue overlap).

## 1. Judgement in brief

Most of the v4 gaps are repaired. The lock geometry now sits on one machined 304 frame, the four-bar margins and strokes reproduce, the escape check reproduces, and the thrust face works through yaw. Retention against pull-out (tension) is supported on paper.

I record `fail`, not `unresolved`, because of two results that the declaration states itself and that contradict the requirement:

1. **Torsion (decisive).** CPL-009 and Q031 item 6 evaluate passive retention under declared loads. The candidate declares torsion loads (5.36 mN m for one idle neighbour tipped, 10.73 mN m for two). Its own configuration-space result is that at the loose corner of its own tolerance stack (P above 0.62 mm, 43 percent of the declared P interval 0.05 to 1.05 mm) the peg turns freely over the whole 60 degree hex period and "carries no roll torque". At the nominal gap the peg turns about 12 degrees first. Nothing declared holds that torque (section 3.3). Q072 item 5 hands it to "the units resting on the table", which is not a retention component, has no geometry, friction value or load path in the declaration, and is not in `retention.component_ids`. The declared load is therefore not carried by the declared mechanism, which is a contradiction of the requirement, not just a missing analysis.
2. **Alignment window at the jaw smaller than the declared tolerance.** The roll-in channel is the alignment means. At the receiver its window toward the jaw is 0.087 mm at the class-f minimum stroke (the dossier says 0.104, an error), against a declared height stack of +-0.35 mm (and a stated peg-height offset of up to +-0.6 mm). With the declared offset the open jaw intersects the swept peg at the class-f stroke corners (section 3.4). The author labels this "reduced-margin ... does not close". By the candidate's own worst-case convention (arithmetic sum, used for P) the means does not work at that corner.

Separately, closure of the held state onto a laterally offset peg is unsupported (section 3.2), and several joints are undesigned. Those alone would be `unresolved`.

## 2. Independent recomputation

| Item | Dossier | Reviewer |
| --- | --- | --- |
| Dead centres, stops, travel | 28.858 / 211.39, 18.86 / 221.39, 202.53 | 28.86 / 211.38; the rocker output offset that reproduces the declared stop-tip points is 46.00 degrees |
| Margin open / closed, class f by size (11 independent signs, 2 048 corners) | 5.64 / 6.09 deg | 5.66 / 6.11 deg |
| Stroke min..max, class f by size | 5.088..6.068 mm | 5.07..6.10 mm (stop signs independent) |
| Every coordinate +-0.1 | 5.19 / 5.41; 5.035..6.113 | 5.21 / 5.41; 5.02..6.14 |
| Frame plus play | 1.73 / 3.59; 4.631..6.613 | 1.71 / 3.61; 4.62..6.65 |
| Open jaw to swept hex AF 4.0, stroke 5.582 | 0.448 | 0.448 (tongue 1.024) |
| same, stroke 5.088 | **0.104** | **0.087** (AF 4.05: 0.058) |
| same, stroke 5.035 | 0.052 / 0.027 | 0.048 / 0.019 |
| same, stroke 4.631 | 0.000 | 0.000 (tongue 0.308) |
| Open jaw, peg raised +0.35 mm | not stated | 0.193 at 5.582; interference (0) at 5.088, 5.035 and 4.631 |
| Escape search (jaw and seat, exact polygons) | no escape | tight: x +-0.05, z 0 to 0.05, roll fixed; nominal: x +-0.35, z -0.45 to +0.10, roll +-12 deg; loose: x +-0.65, z -0.90 to +0.15, roll unbounded; no escape in any case |
| Tongue / shoulder overlap, centred | 3.04 mm2 | 3.05 mm2; 0.14 mm2 at 0.9 mm low; minimum over the reachable loose set about 0.095 mm2 (never zero) |
| Release torque at 1.683 N, mu 1 | 9.66 mN m (1.07 x stall); T_rel 0.5225 N | 3.366 N x 2.871 = 9.66; 3 / (2 x 2.871) = 0.5224 N |

The four-bar numbers agree to grid noise (0.02 degree, 0.03 mm). The only real discrepancy is 0.104 against 0.087 for the open-jaw clearance at 5.088 mm: the dossier's own pair (0.052 at 5.035, 0.104 at 5.088) would need a slope of 1.0, while the true slope near 0.73 gives 0.087, and the v4 review also had 0.087. The error is on the unsafe side. My escape search equals the dossier's table in every column, so I accept the escape result.

## 3. Findings per means

### 3.1 Retention against pull-out (tongue on the groove, over-centre four-bar, collar on saddle)

Principle: tension bears on the 304 peg shoulder and the 1.0 mm 304 tongue in the 1.4 mm groove; the tongue is held closed by a hard stop 6 to 10 degrees past a dead centre on a 304 frame; no power, no spring. Supported.

- Four-bar: margins positive in all three declared tolerance bases (minimum 1.71 / 3.61 degrees with play); the rod stroke is at least 4.62 mm against the 4.6 mm the tongue needs. The frame carries class f only, which is legitimate for machined 304. The v4 point that PA12-carried positions got class f is resolved for the lock. With play the link-line offset falls to 0.077 mm and the author states load-reversal needs pin friction 0.10 to 0.14 (uncited); I do not count that against retention under single-sign loads.
- Escape: reproduced. With the jaw closed the peg cannot leave up, down or sideways at any P in 0.05 to 1.05 (the 4.0 mm hex cannot pass the 2.45 mm opening below the legs, and part of it always stays in the pocket). The tongue additionally blocks y.
- Tension overlap never reaches zero in the reachable set. Stresses are small (11.8 MPa at 0.14 mm2). I accept the overlap argument for tension. At low positions it is a sliver and its moment and bearing behaviour is not examined (Gate 2).
- Thrust: collar r 3.8 in saddle r 4.2 is coaxial with the yaw axis. In the body frame the tension direction rotates with yaw, the contact point moves on the saddle, which spans +-38 degrees (4.2 sin 38 = 2.585, matching the x +-2.6 limit). Contact holds through +-12 degrees and the +-15 degree stops. The yaw torque from the 0.7 mm lever is 0.24 mN m. The v4 washer contradiction is resolved. Hertz 28 to 36 MPa is plausible. Unresolved and not a contradiction: the collar-to-column joint, the moment between the stem plane (z near 1 to 2.5) and the collar plane (z 9.3 to 10.7), about 14 mN m at 1.683 N, the +y restraint of the collar and the 0.4 mm radial slack, and the saddle window in a PA12 plate.
- Release: both friction faces counted. CPL-008 permits blocked release, the operating rule T <= 0.5225 N is stated, `bounded_independent_release` true with a nonempty means is consistent. The rule depends on the neighbour relaxing the chain, so the release is independent only below that tension. I accept it as declared, since the mu = 1 bound is provisional and the blocked margin is 7 percent.

### 3.2 Closure of the held state (v4 item 2): not met, unresolved

The jaw and tongue close together on the same rod. The tongue notch is r 1.55 on a groove root r 1.5, so the peg must be centred to about 0.05 mm. My grid integration of the tongue plate against the root cylinder gives interference (the tongue lands on the root instead of the notch) once the resting peg is more than about 0.15 mm off laterally (0.01 mm2 at 0.2, 0.07 mm2 at 0.35 for a peg resting on the nominal seat), and interference for any upward offset above the axis (0.106 mm2 at +0.1 mm, centred). The declared reachable positions are x +-0.35 (nominal) and +-0.65 (loose), z up to +0.10 and +0.15. v5 offers no registration, no compliance (flexure dropped) and explicitly disclaims the wedge and chamfer as a pre-alignment or capture means (dossier 7.2). So whether the crank reaches its stop on a peg that has landed at an arbitrary position inside the declared play is not shown. The v4 required fix ("a lead-in or compliance that lets the jaw close on a peg that is off by more than 0.05 mm, or state the maximum error the lock tolerates") is answered by the free play statement only. I classify this as unsupported.

### 3.3 Torsion and roll lash across the free play (contradicted)

The declared lock for roll is three corner contacts (two jaw inclined flats and the seat top), torque 2.141 mm x F at nominal, a pure couple with arm 2.302 mm at the tight corner. I reproduced the lash in my own search (tight +-0.5 deg, nominal +-12 deg, loose unlimited) and the contact forces are consistent with the quoted torques (10.73 mN m / 2.141 = 5.01 N; / 2.302 = 4.66 N). I did not re-derive the 2.141 mm arm itself.

What follows for retention under the declared torsion load:

- Tight corner (P near 0.05): a roll lock exists, with Hertz stress 791 to 1 119 MPa at an assumed 0.1 mm corner radius, above first yield by the author's rule of thumb. That is local indentation and growing lash, not loss of the lock yet; Gate 2/3.
- Nominal corner: the peg rotates 12 degrees before it is stopped. The load is then carried.
- Loose corner (P above 0.62 mm, a 43 percent share of the declared P interval and above the nominal value by only 0.07 mm of stack): the peg rotates freely. The declaration says "NO roll lock" and "carries no roll torque". There is no second path. The yaw puck takes torsion "through the yaw shaft only" (yaw-puck description) but the yaw shaft is driven by a 27:1 worm whose self-lock needs a friction coefficient of at least 0.125 that is UNRESOLVED, and which is not a roll constraint about the peg axis in any case. The thrust collar bears along y. The tongue in the groove does not constrain rotation about the peg axis (the groove is axisymmetric).
- "Torsion is then held only by the units resting on the table" (Q072) is not a declared mechanism, has no component, geometry, friction coefficient or load path in the declaration, and is excluded from `retention.component_ids`. The retention mechanism must hold unpowered under the declared loads (CPL-009, Q31 item 6). The candidate's own declared load meets zero capacity at a declared corner, and the candidate's own text calls the roll lock "not a qualified function".

Verdict on this point: torsion retention is not unsupported but contradicted by the declaration's own numbers at the loose corner, and conditionally held (after a 12 degree lash) at nominal. Pull-out retention is not affected, so the connection does not separate, but the declared structural load is not passively carried. The limitation text and Q072 disclose this honestly; the protocol, however, asks whether the means works unpowered under the declared load, not whether the failure was disclosed.

### 3.4 Alignment: roll-in channel and the windows at the jaw (contradicted at the corners)

Kinematics, arcs and the V-shaped channel are unchanged from v4 and reproduced there; I re-ran the swept-volume check (clearances above). The statements that no axial or heading pre-alignment exists and that a free approach cannot start a roll-in are kept and I confirm them (CPL-006: no capture window claimed). Windows are now stated at the jaw (v4 item 3), which is the required change, and they are small.

- At the slot the clearance is 0.59 mm per side, 0.44 at the SLS minimum; unaffected.
- At the jaw the usable height margin toward the jaw is 0.448 mm (nominal stroke), 0.087 mm (class-f minimum stroke; the dossier says 0.104), 0.048 mm and zero at the frame-plus-play stroke 4.631.
- The declared stack is +-0.35 mm and the dossier itself says the peg-height offset is up to +-0.6 mm. A +0.35 mm offset leaves 0.193 mm at the nominal stroke but gives interference at the class-f minimum stroke. At those corners the open jaw blocks the roll-in, so the alignment means does not function across the candidate's own declared tolerance range. The candidate does not claim a capture window, but it does claim the guide; at the corners its own numbers show the guide is blocked.
- The 0.6 x 30 degree jaw chamfer is a seating lead-in only, as stated.

Because the candidate itself places this in "reduced margin that does not close" and the channel works at the nominal stroke, I would have recorded `unresolved` for this item alone. It is listed as a second contradiction because it compounds with 3.3: both have the same root cause, the +-0.35 mm stack of two PA12 units that the lead decided to carry as free play instead of absorbing or registering (flexure infeasible, seat not registered to the frame).

### 3.5 Tongue seating feature

Not a claimed alignment means (ratio 0.98 at rated closing force, stall 2.94, below 1.5). The notch does not wrap the root when the peg sits low. Accepted as a seating feature.

### 3.6 Magnetism and automated checks

No magnet component and no magnetic alignment kind. Checks 1 to 5 of protocol section 8 hold: `requires_power_to_hold` false, `bounded_independent_release` true with a nonempty means, mechanism and justifications nonempty, every alignment entry names components, component ids exist.

## 4. The seven v4 section 7 items

| # | v4 required | v5 | Judgement |
| --- | --- | --- | --- |
| 1 | Fix the positions that define the over-centre lock; close the bore play | One machined 304 frame carries post, stops, bearing, saddle; bore play 0.05 | Met for the lock. Margins and strokes reproduced. The frame is on the middle triangle piece of the PA12 end plate; its fixing and location to the F3 wall are not designed (unresolved) |
| 2 | Vertical stack to seat to jaw to tongue; lead-in or compliance; or state the maximum error | Stack stated as a free play 0.05 to 1.05 mm; flexure rejected on energy grounds; no registration | Stated, not closed: the stack degrades the roll lock (3.3), the open-jaw window (3.4) and the tongue closure (3.2) |
| 3 | State windows at the receiver (jaw) | Stated in 7.2 with caveats | Stated; the 0.104 value is wrong (0.087); the window is smaller than the declared offset |
| 4 | Thrust face that works through yaw | Cylindrical collar on saddle, coaxial | Met on paper (3.1). Joint, +y restraint and moment undesigned |
| 5 | Count stem friction; cite or remove PA12 as crank bearing; guides through the V middle triangle | Both faces counted (9.66 mN m, T_rel 0.5225 N); crank and pivot in 304; jaw guide not designed | Friction and bearing met. Jaw guide not designed (unresolved; the jaw runs on the rod only) |
| 6 | Time labels and groove area | Fixed; 3.04 mm2 reproduced (3.05) | Met |
| 7 | Keep the arcs, the statements and the honesty | Kept | Met |

## 5. Arithmetic and consistency errors found

1. Open-jaw clearance at the class-f minimum stroke 5.088 mm is 0.087 mm (reviewer; also the v4 reviewer's value), not 0.104. The AF 4.05 and 5.035 mm values also differ slightly (0.019 against 0.027, 0.048 against 0.052). The error is unsafe.
2. The dossier's "peg cannot leave along either arc" check models the jaw and seat only; the tongue closing interference (3.2) is not in any table.
3. The roll-lock discussion mixes the tolerance of the jaw and seat with the lash model but never states the share of the P interval above 0.62 mm (43 percent).
4. Sections 7.2 and 11 call the jaw window "reduced margin"; the resulting interference at the declared stack is not stated as a failure of the means.
5. The 14 mN m moment between the stem plane and the collar plane (about 8.5 mm x 1.683 N) is not stated anywhere, although the collar thrust path is closed on paper without it.

## 6. Classification of the reported weaknesses

| Weakness | Contradicts passive retention or justified pre-alignment? | Where |
| --- | --- | --- |
| No roll lock at the loose corner, torsion path undeclared | **Yes** (declared load 5.36 to 10.73 mN m, no declared path) | G6 fail |
| Open-jaw window below the declared offset | Yes at the class-f stroke corners (alignment means blocked) | G6 fail (compounding) |
| Tongue closure on an offset peg | No, unsupported | Unresolved |
| Hertz above first yield at the peg corners | No | Gate 2/3 |
| Release at the mu 1 bound blocked | No (CPL-008) | Gate 2/3 |
| Load reversal needing pin friction 0.10 to 0.14 | No, unsupported | Unresolved; Gate 2 |
| M3 radial load and unrated shaft | No, unsupported | Gate 2 |
| Collar joint, +y restraint, stem-collar moment, saddle window | No, unsupported | Unresolved |

## 7. What a further version needs

1. Give the declared torsion load a declared path at every corner of the declared tolerance range: register the seat to the frame so that P is bounded below the lash threshold (the roll lock is lost at P above 0.62 mm and has +-12 degrees of lash at 0.55), or provide a roll constraint that does not depend on P (for example a pocket profile that bears on the peg flats at any P, or a torsion-rated feature in the shoulder), or restate the retention claim and the loads so that torsion is explicitly not a retention load, with a modelled and declared table-contact path (geometry, friction coefficient, load) that appears in the retention component list. Quantify lash against the 5.36 and 10.73 mN m loads including the Hertz indentation growth.
2. Make the usable window at the jaw at least as large as the declared stack at the class-f minimum stroke: a longer stroke, a jaw that opens in a different direction, or a narrower leg, with the clearance recomputed (0.087 mm at 5.088 mm at present, not 0.104).
3. Show that the tongue and jaw can close onto a peg that sits anywhere in the declared play (lateral up to +-0.65 mm, up to +0.15 mm), by registration, compliance or a guided lead-in, or state the largest offset the lock tolerates and keep it inside the declared stack.
4. Design the collar-to-column joint, the +y restraint and the stem-to-collar moment path, the saddle insert window, the fixing of the frame to the middle piece and the jaw guide.
5. Correct the 0.104 value and state the interference with the declared offset, and the share of P above 0.62 mm.
6. Keep: the 304 frame, the cylindrical thrust face, the two-face release friction, the escape model, the corrected groove area and time labels, and the honest limitations.

## 8. Basis of the outcome

Protocol section 8 asks, for retention and for each alignment means, for the principle, the governing geometry and forces with declared dimensions, and the reasoning that it works unpowered; unsupported claims are `unresolved` and contradicted claims are `fail`. Pull-out retention: principle, geometry and strength supported. Torsion under the declared loads: contradicted by the candidate's own configuration-space result at the loose corner, with the nominal corner held only after a 12 degree lash. Roll-in channel: the guide works at the nominal stroke and is blocked by the declared offset at the class-f stroke corners. The record is a paper judgement and not a test of the mechanism. Under the protocol, `outcome: fail` makes G6 a fail.
