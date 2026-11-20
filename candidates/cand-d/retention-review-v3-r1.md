candidate_id: cand-d
candidate_version: 3
author: Claude Opus 5.5 (engineering lead, cand-d author)
reviewer: reviewer-d3-retention (Claude Sonnet 5.5, independent session, no authorship in cand-d)
outcome: unresolved

# Retention and pre-alignment review: cand-d v3, r1

Date: 2026-11-20.

Declaration `candidates/cand-d/declaration.json`, SHA-256 `0f82c5062fc83c8b9eb918e728f41b357245aeda848cf5d87989a0444ae6f8e8` (computed with `shasum -a 256`; equals the expected value and the dossier-v3 hash). Figures marked "reviewer" are my own python (inline, outside the repo). I also ran `coupler.py`, `joint.py` and `gen_declaration.py` (no `--write`). They run clean and reproduce the dossier numbers. No file other than this one was written.

Files read: `AGENTS.md`; protocol section 8 and 10; `criteria/gates/gate1-v1.json` (G6); `Q031` (all, item 6 noted), `Q036`, `Q085`, `Q088`, `Q089`; `Q062` by reference (section 3 family rule); `requirements.md` CPL-001..CPL-011; `declaration.json` (retention, release, alignment, limitations, summary, assembly_access, coupler_sites, stowed primitives, every component box, full text of head-cartridge, head-flange, tail-stud, coupler-motor, fasteners, front-wall pieces); `dossier-v3.md`; `dossier-v2.md` (by grep for the unchanged parts and the stud mount); `scripts/README.md`, `coupler.py` (all), `joint.py` (run), `gen_declaration.py` and `declaration_text.py` (run, grepped); `retention-review-v2-r1.md` (all of sections 1, 4 to 8); `retention-review-v1-r1.md` (grep for the stud mount). Sources checked raw: Wikipedia Leadscrew wikitext (curl), Engineering ToolBox friction page (curl, text strip), 206-109 datasheet PDF (`pdftotext`).

## 1. Judgement in brief

v3 closes most of the v2 items and its coupler core is sound on paper. I do not record `pass`, because three claims are unsupported and one is wrong in a way that matters:

1. **The tail stud has no justified mount.** Every declared load passes through the stud flange into the PA12 tail end plate (two M1.6, positions not declared, thread in PA12). The declaration says pull-out in PA12 "is not cited" and the "sized by bearing pressure" statement has no calculation anywhere (`coupler.py` section 11 covers only the head flange). The retention text claims "every load path is closed in machined metal", but this end of the path is PA12 plate and PA12 threads. Loads are small (reviewer: about 2 to 8 N on the screws) and a carrier exists geometrically, but it is not shown. Unsupported.
2. **The lug-to-slot clearance is overstated about 2 times.** The slot lash is quoted at the inner radius 2.05 and described as "the lug touches there first". It touches first at the largest radius where the lug lies in the slot, the tube outer radius 3.5. Lash there is 1.53 to 1.83 deg, not 2.61 to 3.12. The seated clearance is about 0.65 deg (reviewer), not 1.39 deg. The conclusion survives (still positive), but the stated margin is wrong. This is the same radius error the v2 review reported (its error 2), now re-introduced.
3. **Closing and tooth meshing at the guaranteed lower bound is not shown.** "Tooth engagement does not depend on F_p" is true for loaded retention once seated. It is not shown for the act of meshing the teeth, which has to correct roll and lateral error against the table (reviewer: about 3.9 mN m, 0.87 N at r_m, to tilt one free unit; available axial draw at the lower bound 0.49 N in the capture stage and 0.88 N at the lock stage). With the typical motor it holds (2.4 N and 4.4 N). This is a capture-sweep matter for Gate 2/3 as far as no window is claimed, but the declaration does claim "the teeth align it under the draw".
4. **Plate-to-shell path.** The PA12 front plate and end plate are "screwed on" with unlocated, lumped screws. No calculation of the plate as a beam or of its screws exists. Small loads, plausible, not shown.

I looked for a contradiction that defeats retention and did not find one. Nothing here contradicts passive retention. The correct label is `unresolved`. The items are small and none needs more volume.

## 2. Independent recomputation

| Item | Declared | Reviewer | Verdict |
| --- | --- | --- | --- |
| Axial stack, seat depth (7 terms, IT9 half-bands, g6) | 3.518 to 3.681 in 3.40 to 3.80, margin 0.118 | 3.5185 to 3.6815; margins 0.1185 / 0.1185. Stage-end tolerance (about 0.0125 each) not in the stack; margin stays above 0.10 | reproduces |
| Self-locking, tan 3 deg 0.0524 | 2.86 dry, 1.91 oil | same. At the inner end of the flank line (r 3.55, tan 0.0720): 2.08, 1.39 | reproduces; holds over the whole line |
| Preload band at 1.0 V | 4.41 to 9.00 N (dry) | 4.41, 9.00 | reproduces |
| Datasheet lower bound | 0.88 N | Rated 3 mN m at 3 V, start voltage 0.5 V. Minimum over v0 in 0..0.5 of 3 (V - v0) / (3 - v0) at V = 1 is 0.6 mN m (v0 = 0.5), giving F_p 0.882 N | reproduces; model is an inference (see 4.1) |
| Elastic gap, 20 N above preload, k_loop 20 kN/mm | 0.001 mm vs 0.39 teeth | 0.001 mm; roll 0.013 deg | reproduces, k_loop is provisional |
| Tooth-to-slot phase, lash at r 2.05 | 2.61 to 3.12 deg; clearance 1.39 deg | Lash at r 2.05 is 2.61 to 3.12; at r 3.5 (first contact) 1.53 to 1.83. Phase (teeth 2 x 15 um at r_m = 0.39 deg; lug and slot offsets 30 um at 3.5 = 0.49 deg) 0.88. Clearance 0.65 deg | **declared margin wrong; conclusion holds** |
| Hirth tipping edges | out-of-plane 6.3, in-plane 5.90 | 5.903 (slot half-width 2.2); 27.8 and 26.0 mN m | reproduces |
| Combination, axial | 3.266 N vs 4.41 (1.35) | same; at 0.88 N the faces gap (stated) | reproduces |
| Mount, out-of-plane | far screw at 17.2: 1.46 N | 14.64 / 17.2 + 0.61 = 1.46 N | reproduces (label says W x 47.2, value uses 48.0) |
| Mount, in-plane | 1.65 N each; fault 4.34 N | 14.5 / 7.0 / 2 + 0.61 = 1.65; 52.2 / 7.0 / 2 + 0.61 = 4.34 | reproduces |
| Mount, torsion and shear (not stated) | none | 7.75 mN m / 7.8 / 2 = 0.50 N per screw; coupler-motor reaction at the stop 38.7 mN m: 2.5 N per screw; shear 0.15 N each | small; reviewer closes for the head flange |
| Flange rim bearing on plate | 1 mm band x 4 mm, 1.86 MPa | Window half-width 6.45, disc r 7.0: band 0.55 wide, segment area about 2.0 mm2; 7.46 N gives 3.7 MPa mean (PA2200 tensile 50) | declared band wrong ~2x; far below strength |
| Release at 3.4 V, eta 0.9 | 20.3 needed, 32.9 available, 1.62 | 1.62 | reproduces |
| Hertz, line 2.65, R 1.5 | 163 / 209 / 225 / 252 MPa vs onset 230 | same (script) | reproduces; assumes contact over the whole line |
| Pilot sequence | margin 0.20 | 5.70 - 5.10 - 0.40 = 0.20 at one reference plane. The Hirth crest is 0.2 above the pitch plane and the bore-mouth plane is not declared, so 0.20 can be 0 to 0.4 | arithmetic holds; reference unstated |
| Windows | lateral 0.95 vs 0.6; roll 5.5 vs 1.4 deg; pitch 0.73 | lateral 0.4 + 2.05 - 1.5 = 0.95; roll atan(0.6/6.2) = 5.5; pitch 0.73 | reproduce |
| Declaration fit | flange inside boxes | Flange y -3.7..10.3, z -8.4..10.4; shell inner z 10.8, y 11.5; nut blocks z 7.7..9.9 and -7.9..-5.7 lie behind plate pieces z 7.45..11.2 and -11.2..-5.45; lobes lie on those pieces; evaluator G2 pass | fits |

Sources, raw: Wikipedia Leadscrew wikitext has "Steel, dry ... bronze 0.15-0.23", "Steel, machine oil ... bronze 0.10-0.16", self-locking when mu > tan(lead angle), "not absolute" under vibration or shock. ToolBox: PTFE on steel clean and dry 0.05 - 0.2; steel on steel clean and dry 0.5 - 0.8 static, 0.42 kinetic. 206-109 PDF: rows 13 rated load 3 mN m, 14 rated speed 140 rpm, 16 max start voltage 0.5 V, 21 max start current 230 mA, 31 typical stall torque 9 mN m. All as cited. "Rated load" is a specification row, not labelled guaranteed minimum; see 4.1.

## 3. Status of each v2 item (v2 section 7)

| v2 item | v3 | Status |
| --- | --- | --- |
| 1. Ears joined to housing, load path | One-piece 304 housing with a front flange; screws through lobes and plate into 304 nut blocks. Boxes are consistent. Housing is joined as one part at x 35.6 | **Closed for the head side.** The path then continues through the PA12 plate to the shell; plate screws are not located (open, item A below) |
| 2. In-plane lever | Pivot on the disc rim at 7.0; both screws hold. Lobes on the z line, so out-of-plane lever 17.2. Recomputed | **Closed.** Rim band area misstated, harmless |
| 3. Window tolerance, lip fit, flange at the PA12 corner | Flange lies on the plate face. No lip in a window; the sleeve passes the window (r 6.3 vs half-width 6.45, 0.15 clear before SLS tolerance +-0.3, so the sleeve can touch a window edge at a corner). Gap outside r 6.3 is 0.7 | **Closed for the load path** (the sleeve is not a load carrier at the window). Sleeve-window contact at a PA12 corner is a rub, not a load path; Gate 2/3 |
| 4. Tooth phase vs slot lash | Derived, IT9 both parts. Lash taken at the wrong radius | **Narrowed, not fully closed.** Clearance 0.65 deg (reviewer) instead of 1.39. Still positive |
| 5. F_p lower bound | 0.88 N from datasheet rows. Elastic gap shows retention independent of F_p | **Closed for retention.** Open for meshing at the bound (finding 3) |
| 6. PTFE notch, Hirth area, tipping lever | Notches declared; slots remove 33 percent; edge at 5.90 | **Closed** |
| 7. Pilot-before-lug margin | Chamfer 0.4, margin 0.20 | **Closed at the stated reference.** The reference plane (pitch, crest or root) is not declared; the margin could be 0 to 0.4. Lugs have 0.7 mm of V lead-in so the alignment does not hinge on it |

## 4. Findings per means

### 4.1 Retention, per load

Principle. Two 304 lugs bear on the front (hook) flank of the 3 deg lock stage of the C93200 sleeve. The same flank carries preload and tension, so tension only raises the lug load. The wedge self-locks while mu > tan 3 deg at any load. Torsion and shear pass through the Hirth teeth. Nothing needs power.

Is a friction wedge acceptable as passive retention (CPL-009, Q31 item 6)? Yes for the Gate 1 paper standard. It holds with no power and no stored energy. Q31 item 6 asks that actively held and passively locked states be distinguished and not assumed. The declaration does this, states the vibration limit, and claims no holding of a joint curvature. Vibration walking is a Gate 2/3 matter.

**Tension 1.220 N.** Carrier: lugs on the hook flank. Self-locking 2.86 (dry), 1.91 (oil), 2.08 and 1.39 at the inner line end. Faces stay closed at typical preload (3.6 x), gap by micrometres at the lower bound. Supported inside the coupler.

**Torsion 7.75 mN m.** Hirth teeth, 2.5 x to tooth unloading at typical preload. The lugs do not take it while the teeth are seated: clearance 0.65 deg at the worst phase (reviewer), not 1.39. Even if a lug touched a slot side, the lug would then carry torque at 0.0 slip along the flank because the slot side is tangential and the flank load is axial. Supported.

**Shear 0.305 N.** Teeth, 14 x. Supported.

**Out-of-plane bending 14.6 mN m.** Face tipping 27.8 (1.90 x) at typical preload; beyond it the pilot couple, tilt 1.49 deg. At the lower bound (5.5 mN m tipping) the pilot takes about 9 mN m: 1.8 N over a 5 mm lever on a 4 mm dia 304 pilot in a 304 bore. Supported.

**In-plane bending 14.5 mN m (drive limit).** Tipping about y 5.90: 26.0 (1.80 x); beyond it the lug pair (lever 10.8). Supported. Fault 52.2: lugs at Hertz 252 MPa, above the 230 onset, local indentation (declared). Not separation.

**Combined.** Teeth ratio 1.35 at typical, below 1 at the bound; the faces gap at one edge; retention by lugs, teeth on the far side and pilot. Supported as retention.

**Closed path in the head.** Tooth, flange, housing, nut blocks, plate: reviewer checks 0.61 N pull-out each, 1.65 N in-plane, 4.34 N fault, 1.46 N out-of-plane, 0.50 N torsion, 2.5 N coupler-motor stop reaction. All small against M1.6 A2 and 304 thread (454 N strip, declared) and PA12 bearing (1.5 to 3.7 MPa vs 50). Supported.

**Open path A, plate and shell.** The load leaves the nut blocks and the flange rim into the 1.2 mm PA12 front plate (a plate with a 12.9 mm window, pieces `L-front-n/p/lo/hi`) and then into the shell walls through screws that are not located (lumped 14 x M1.6 into PA12). Order of magnitude: 2 to 8 N on a plate piece clamped on three sides, deflection about 0.01 mm. Plausible and small; not calculated, not cited. Unsupported.

**Open path B, tail stud (blocking).** The stud flange (r 6.3 x 1.0) is "screwed from outside (2x M1.6)" into the 1.2 mm PA12 end plate. Screw positions, thread engagement and thread material are not declared. Pull-out strength in PA12 is "not cited" (limitation 8). The carrier for tension, both bendings, torsion and shear on the tail side is therefore the PA12 end plate and its threads, with no figure. Reviewer order of magnitude: out-of-plane 14.6 mN m over about 6.3 to 12 mm lever gives 1.2 to 2.3 N; fault in-plane 52.2 over 6.3 gives 8 N; thread in 1.2 mm PA12 plausibly tens of N. That is a ratio of perhaps 10, but on an uncited strength. The head side used 304 nut blocks to avoid this exact problem; the tail side did not. The v1 review judged this "not blocking" when the loads were 0.8 N; v3 has the fault case at 8 N and a stated claim "every load path is closed in machined metal" that the tail side does not meet. This is an unsupported claim on a carrier of every declared load. I count it as blocking.

**Preload source (lower bound).** The bound 0.6 mN m at 1.0 V needs: rated load is a minimum, torque falls with speed, friction torque is constant and at most (Kt/R) x 0.5 V. The datasheet gives "Rated Load" and "Max. Start Voltage" as rows; it does not say the rated load is a guaranteed minimum. The inference is reasonable and the author states it as a bound. I accept it for retention, because retention is shown to be independent of F_p. I do not rely on it for closing.

### 4.2 Release

The head's own motor turns the sleeve back to the open stop. Need 20.3 (oil 19.3) mN m, available 32.9 at 3.4 V and eta 0.9: 1.62 (1.70). The ratio is independent of motor constant because closing and release use the same motor. The supply rule (cell at 3.5 V or more) is a controller rule; a modelled sensor (cell voltage) is available per the declaration. Ejection reaction 0.81 N goes to the 304 collar. Stop pin 7.3 N, shear 9.3 MPa, bronze 14.6 MPa, in the 304 flange. Release path through the flange reaction (stop torque 38.7 mN m, 2.5 N per screw) is closed in the head mount. Bounded and independent: each head releases its own joint. Supported. Release when jammed by loads beyond those declared is CPL-008 and left open by the author.

Closing logic. The motor drives for a fixed time at 1.0 V PWM average; the stop pin limits over-travel at 122.0 deg, which is also the end of the lock stage. If the faces do not seat, the lug ends held by the stop and not by friction; this is a fault case the declaration does not claim as retention. No sensor confirms the state (stated, Q32).

### 4.3 Alignment means

**(a) Lateral chamfers and pilot.** A 45 deg chamfer under an axial push gives a centring component (1 - mu) / (1 + mu), 0.11 at the 0.8 upper bound. Window +-0.95 against +-0.6. The principle is geometric and unpowered. Force sufficiency: with the declared external push of about 0.31 N the centring component is 0.034 N, while moving a free unit sideways against the table at mu 1 needs up to 0.305 N. The push is external and its magnitude is not fixed by the candidate, so this is a capture-sweep matter (CPL-006) and the author claims no window. Supported as geometry; force sufficiency Gate 2/3. Pilot-before-lug: 0.20 at one reference plane (see 3, item 7). The lugs' 0.6 V lead-ins cover +-0.7 tangentially, so the lug entry does not depend on the pilot margin at the +-0.6 stack.

**(b) Roll, pitch, yaw.** V lead-ins give +-5.5 deg at r 6.2 against about +-1.4 deg. Lug indexing "2.61 to 3.12 deg" should read 1.53 to 1.83 deg at the first contact radius; the conclusion (below half a pitch, 5 deg) is stronger, not weaker. Pitch 0.73 deg from flatness; yaw bounded by the pilot at 1.49 deg. Joint angles do not enter. The guide is not blocked at any declared corner: the lug path past the PTFE ring is notched, the flange slots 3.20 plus V lead-ins pass the lugs, and the open stop puts sleeve notches over the slots within about 0.3 deg against 7.1 deg. Supported as geometry. The statement "the teeth align it under the draw" needs a draw torque larger than the table's restoring torque (reviewer 3.9 mN m for 1.4 deg roll, or 0.87 N axial at r_m through 45 deg flanks). At typical motor torque the draw is 2.4 N (capture stage) and 4.4 N (lock stage): 2.8 x and 5 x. At the guaranteed lower bound it is 0.49 N and 0.88 N: below and at 1.0 x. Not shown at the bound; Gate 2/3 capture sweep, flagged.

**(c) Axial closing and seating.** The 20 deg capture stage draws 1.0 mm for 1.21 mN m (mu 1) against 9.68 to 10.75 typical; the stack seats inside the lock stage with 0.118 margin each side. The axial push to reach the capture stage is external and declared. Supported.

### 4.4 Magnetism

No magnet component, `mechanism_kind` is `friction_wedge`, no alignment of kind `magnetic`. Not applicable. Check 4 holds.

### 4.5 Automated checks 1 to 5 (protocol section 8)

1. `requires_power_to_hold` is `false`. Holds.
2. `bounded_independent_release` is `true`; `release.means` nonempty and physical. Holds.
3. `mechanism` and all three `alignment[].justification` are nonempty; `component_ids` (head-cartridge, head-flange, tail-stud, retainer-collar, nut-block-up, nut-block-low) all exist. Holds.
4. No magnet. Holds.
5. Each alignment names existing components (tail-stud, head-flange, head-cartridge; and head-cartridge, coupler-motor, coupler-pinion, tail-stud). Holds.

Note: `retention.component_ids` does not list `coupler-motor` or the PA12 plate pieces, which carry the release torque and the plate load; the stud-side mount has no component id of its own because the stud flange screws are lumped in `fasteners`.

## 5. Errors found

1. **Slot lash radius.** "The lug touches there first" at r 2.05 is wrong. First contact is at the largest radius where the lug is in the slot (tube outer, 3.5). Lash 1.53 to 1.83 deg, seated clearance 0.65 deg (reviewer), not 2.61 to 3.12 and 1.39. Appears in `coupler.py` section 6, the retention text, the alignment text and `dossier-v3.md`. Conclusion unchanged.
2. **Slot phase radius.** The slot position error is a linear offset (15 um); converting it at r 2.05 (0.42 deg) rather than at the contact radius 3.5 (0.25 deg) is a second inconsistency. The two errors partly cancel.
3. **Flange rim band.** "1 mm wide band 4 mm long" is wrong. Window half-width 6.45 and disc r 7.0 give a 0.55 mm band, about 2.0 mm2. Pressure about 3.7 MPa, not 1.86. Harmless.
4. **Label.** The out-of-plane line prints "W x 47.2"; the value uses 48.0; the declaration limitation says 48.0.
5. **Pilot reference plane.** The 0.20 margin assumes both planes are the pitch plane. Tooth crest is 0.2 above it.
6. **Countersink in a 0.8 flange.** ISO 7046 M1.6 head k 0.96 against a 0.8 mm lobe: the cone sits about 0.7 deep and leaves about 0.1 of web under the head, in a lobe 3.4 wide against a head dk 3.0. Loads are 1 to 4 N; this is a fine-detail point, not a load-path failure.
7. **Hertz line contact.** The 2.65 mm line contact assumes a flank that matches the lug along its radial length. A true helicoid twists the helix angle from 4.1 to 2.4 deg across the line (about 20 um of gap). If contact concentrates, p0 rises above the yield onset. Fine machining; Gate 2/3.

I found no arithmetic error in the cam layout, stack, self-locking, preload, release, Hertz, stop pin or window numbers.

## 6. Classification of weaknesses

**Contradiction (defeats a requirement):** none. Error 1 overstates a margin; the margin is still positive.

**Unsupported (blocks `pass`):**
- U1. Tail stud mount into PA12: screws unlocated, thread strength in PA12 uncited, no calculation. Carrier of every declared load.
- U2. PA12 plate and shell path: plate pieces and plate screws not calculated or located.
- U3. Lug-to-slot margin (error 1) stated wrongly, so the "never bears on the slots" margin is not shown at its stated size. The corrected margin is positive, so this alone I would take as a correction. It is listed because the author's text must change.
- U4. "The teeth align it under the draw" at the guaranteed motor lower bound.

**Gate 2/3 (do not block):** vibration back-driving of the wedge; PTFE creep and thermal change of preload (no re-tightening); galling of 304 on 304; fine machining of the 36-tooth ring and the helicoid flank; lateral centring force against table friction (external push); capture sweeps; sleeve touching a PA12 window corner; stiffness and roll lash after the faces gap; the 0.8 flange countersink detail.

## 7. What a further version would need

1. Declare the stud-flange screws (positions, thread engagement), put the thread in a 304 nut block or insert like the head side, or cite a PA12 pull-out strength; compute the stud mount for tension, both bendings (fault 52.2 mN m), torsion and shear.
2. Locate the plate screws and show the plate piece as a beam with the flange and nut-block reactions, with a cited PA12 strength.
3. Correct the lug-slot lash to the contact radius 3.5 and restate the seated clearance (about 0.65 deg) and the indexing range (1.53 to 1.83 deg).
4. Show the draw torque needed to mesh the teeth against table restoring torque at the lower-bound motor, or state a closing sequence (for example a higher closing voltage with a sensed current) that bounds it.
5. Declare the reference plane for the bore chamfer and the lug lead-in against the Hirth crest and root.
6. Fix the small figures (rim band, W x 47.2 label), and add `coupler-motor` and the stud mount to the retention `component_ids`.

None of these needs more volume (the stowed margin stays about 1.14 mm).

## 8. Basis of the outcome

Under protocol section 8 and Q062, `pass` needs retention under every declared load and every alignment means to be physically justified on paper, with no declared load missing a carrier. The coupler core is justified: tension, torsion, shear and both bendings have closed carriers in machined metal; the wedge self-locks with margin at the cited lower bounds; release is bounded and independent; the elastic argument shows that seated retention does not depend on preload; the head mount now exists and its levers and screw loads reproduce. The tail stud's mount is not shown to carry any of the declared loads, the plate-to-shell path is not calculated, and the slot clearance is stated at the wrong radius. Unsupported claims make the outcome `unresolved`.

`fail` needs a claim contradicted by the declaration's own numbers or by physics so that a retention or alignment requirement is defeated. I did not find one. The wedge is passive and acceptable, the corrected slot clearance stays positive, and every declared load has a plausible carrier. A friction wedge hold is acceptable passive retention under CPL-009 and Q31 item 6 at the Gate 1 paper level.

I would change to `pass` if the author closes U1 and U2 with calculations from declared dimensions and cited strengths, restates item 3 correctly, and either bounds or withdraws the lower-bound meshing claim. I would change to `fail` if the stud mount is shown to need a lever or area the 12.7 by 24 mm end plate cannot give.

This record is a paper judgement only, label `exploratory`. It does not show that the mechanism works.
