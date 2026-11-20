candidate_id: cand-d
candidate_version: 4
author: Claude Opus 5.5 (engineering lead, cand-d author)
reviewer: reviewer-d4-retention (Claude Sonnet 5.5, independent session, no authorship in cand-d)
outcome: unresolved

# Retention and pre-alignment review: cand-d v4, r1

Date: 2026-11-20.

Declaration `candidates/cand-d/declaration.json`, SHA-256 `21bebbe5812f9a4f41f43c0868634afceb6cf75972174e0f7e2924a0beccb978` (from `shasum -a 256`). It equals the expected value and the `dossier-v4.md` hash. No other file was written. My own python lives outside the repo. I ran `coupler.py`, `joint.py` and `gen_declaration.py` (no `--write`). They run clean and reproduce the dossier numbers (741 pairs, none overlapping, 31 222 mg).

Files read: `AGENTS.md`; protocol section 8 and 10; `criteria/gates/gate1-v1.json` (G6); `Q031` (item 6), `Q036`, `Q062`, `Q085`, `Q090`, `Q091`; `requirements.md` CPL-001..CPL-011; `declaration.json` (retention, release, alignment, limitations, summary, assembly_access, coupler_sites, stowed primitives, all 39 component boxes, and the full text of head-cartridge, head-flange, tail-stud, coupler-motor, coupler-pinion, nut blocks, retainer-collar, fasteners, S-end, front-plate pieces, inner walls, every hinge part and leg); `dossier-v4.md`, `dossier-v3.md` and `dossier-v2.md` (unchanged parts); `scripts/README.md`, `coupler.py` (all), `joint.py`, `gen_declaration.py`, `declaration_text.py` (run, grepped); `retention-review-v3-r1.md` (all).

Sources checked in raw form:
- Wikipedia Leadscrew, `action=raw` wikitext, by curl.
- Engineering ToolBox friction page, raw HTML, text-stripped.
- 206-109 datasheet, `pdftotext -layout`.
- EOS PA 2200 data sheet: **not verified.** The 3dprinting.com URL returns HTTP 403 to curl (plain, browser user agent, referer). The Wayback Machine has no snapshot. See section 2.

## 1. Judgement in brief

The fully seated coupler is justified on paper. Every declared load has a closed carrier, and the v3 stud and plate gaps are closed. I do not record `pass`, because three claims are unsupported. Two new weaknesses appeared in v4 itself.

1. **The partial-seat fallback is incomplete (the main item).** v4 admits that the lower-bound motor (0.88 N) cannot flatten a unit through the teeth. It then bounds only the pitch residual (0.73 deg, 0.080 mm) and concludes that the seat stays in the lock stage (±0.162 against ±0.20). The same table force problem applies to roll and yaw, and the declared presented pose includes both (roll ±1.4 deg, yaw 1.49 deg). Reviewer numbers:
   - Rolling a unit flat needs about 3.7 mN m (0.306 N × 12.04 mm).
   - The tooth ramps give at most 3.9 mN m at 0.88 N with **no** tooth friction, and 0.44 mN m at the author's own dry bound μ 0.8.
   - Even the typical minimum 4.41 N gives only 2.2 mN m at μ 0.8.
   - An unrolled error leaves the faces held off by r·ε: 0.154 mm at r 6.3 for 1.4 deg. Yaw 1.49 deg moves one lug by 0.127 mm.
   - After the stack and the pitch residual only **0.038 mm** of margin remains to the 3 deg stage edge. A roll of 0.35 deg already uses it.
   - Outside the stage the lug sits on the 20 deg flank, which is not self-locking.
   - So "retention does not need flattening" is shown for pitch only. The claim "the teeth fix roll with zero lash" and "align yaw under the draw" is unsupported at the lower bound. With μ 0.8 it is unsupported at typical preload too.
2. **The coupler motor has no declared mount.** Release and closing push 6.3 mN m (3.4 V release) to 10.8 mN m (3.6 V stall) of reaction torque into the motor case. The gear mesh adds 3.15 N. No fastener, saddle or adhesive is declared. The lumped fasteners box (z 4 to 9) does not reach the motor (z −10.25 to −4.25). The cell-voltage measurement that sets the closing duty and the 3.5 V release rule is also not a declared component.
3. **The hinge ears are "one 304 part" with their legs, but the wall lies between them.** The ear is on the gap face of the inner wall (x −1.6 to 1.8) and the leg is behind it (x 3.0 to 3.8). The wall box (x 1.8 to 3.0) has no declared notch. A neck through it is implied and undeclared.

I looked for a contradiction that defeats retention of the seated joint and found none. The remaining defects are errors in the declaration's arithmetic or text (section 5). I judge each one's effect on the conclusion. Outcome: `unresolved`.

## 2. Independent recomputation

Figures are from my own python (`rc.py`, `rc2.py` in the scratchpad), not from the repo scripts.

| Item | Declared | Reviewer | Verdict |
| --- | --- | --- | --- |
| Mass, W | 31 222 mg, 0.3062 N | 31 222 mg, 0.30618 N | reproduces |
| Axial stack (7 terms, IT9 half-bands, g6), lock stage 3.40 to 3.80 | 3.518 to 3.681, margin 0.118 each side | 3.5185 to 3.6815, 0.1185 / 0.1185 | reproduces |
| Self-locking, tan 3 deg 0.0524 at Rc 4.875 | 2.86 dry, 1.91 oil | same. At r 3.55 (4.12 deg): 2.08 / 1.39. At r 6.2: 3.64 / 2.43 | reproduces. Holds over the whole flank line |
| Preload at 1.0 V, dry | 4.41 to 9.00 N | 4.41, 9.00 (sleeve 9.68 to 10.75 mN m) | reproduces |
| Datasheet lower bound | 0.88 N | Minimum of k − f over k ≥ (3 + f)/3, f ≤ 0.5k gives 0.60 mN m at 1 V (k 1.2, f 0.6). With η 0.9 and flank μ 0.23, thrust 0.2: 0.882 N | reproduces. The model is an inference (4.1) |
| Elastic gap, 20 N, k_loop 20 kN/mm | 0.001 mm vs 0.39 teeth | 0.001 mm. Two lugs 193.8 kN/mm. PTFE ring (area 14.7 mm² after notches, E 500 MPa, 0.3 thick) 24.4 kN/mm. Series 21.7 kN/mm | reproduces. 20 kN/mm is near nominal, not a lower bound. Even 1 kN/mm gives 0.02 mm, so the argument is insensitive |
| Slot lash at the contact radius 3.5 | 3.17 to 3.46 deg | 3.168 to 3.462 deg | reproduces. The tube slot ends at r 3.5, so 3.5 is right for the seated state (4.3) |
| Phase, IT9 both parts | ±0.88 deg | 0.877 | reproduces |
| Seated clearance | ≥ 2.29 deg | 3.168 − 0.877 = 2.29 | reproduces |
| Seating force (tilt about the far bottom edge) | 0.139 N at the stud, 1.25 N through teeth at μ 0.8, 0.88 N guaranteed | F_v 0.1391 N. 0.1391 × 9 = 1.252 N. With a 2/π projection of ramp forces onto the vertical: 1.97 N | reproduces. The 1.25 N is optimistic by about 1.6× |
| Partial seat, pitch | ≤ 0.73 deg, ±0.080 mm, engaged ≥ 0.23, ±0.162 | atan(0.6/47) = 0.731 deg, 0.0804, 0.229, 0.1619 | reproduces. **Pitch only (4.4)** |
| Partial seat, roll and yaw | not computed | roll 1.4 deg: 0.154 mm at r 6.3 (0.109 at r_m). Yaw 1.49 deg at the lugs: 0.127 mm. Spare margin after pitch 0.0381 mm, used by roll 0.35 deg | **adverse, see 4.4** |
| Roll torque to flatten a unit | not computed | W × 12.04 = 3.69 mN m (4.09 on the other edge). Ramp torque at 0.88 N: 3.92 (μ 0), 2.11 (0.3), 1.31 (0.5), 0.44 (0.8). At 4.41 N: 19.6, 10.6, 6.5, 2.2. Axial draw needed at μ 0.8: 7.5 N | **adverse** |
| Hirth ring and tipping edges | out-of-plane 27.8 (1.89×), in-plane 25.9 (1.78×), edge y 5.87, 35 % removed | 27.79, 25.87, 5.865, ring remaining 65.4 %. Ring area 103.5 mm², 67.7 with slots | reproduces |
| Combined axial | 3.279 N vs 4.41 (1.35) | 3.2786, 1.345 | reproduces |
| Head mount | 1.47 / 1.65 / 4.34 N per screw (out-of-plane, in-plane, fault) | 14.697/17.2 + 0.612 = 1.467. 14.5/7/2 + 0.612 = 1.648. 52.2/7/2 + 0.612 = 4.341 | reproduces |
| Tail mount | 1.96 / 1.76 / 4.76 N, torsion 0.85, cone 0.94 MPa, strip 341 N | 1.961 / 1.763 / 4.755; 0.845; 0.940; 340.7 | reproduces |
| Head plate bending | 5.9 MPa, clamped circular plate r 10 (Roark) | Roark formula reproduces 5.89. The model does not fit the geometry. The load sits on a strip 3.75 wide (z 7.45 to 11.2) spanning 12.9 mm beside the window. Clamped-clamped beam: 7.8 MPa. Simply supported: 15.6 MPa. Deflection 0.053 mm | arithmetic right, model wrong, conclusion holds (3.2 to 6.4× on 50 MPa) |
| Tail plate bending | not computed | Plate clamped on three sides, loads 8.29 N at the pivot edge and two 4.14 N pulls at the heads (fault). Rough beam estimate 6 to 15 MPa. At the drive limit 2 to 4 MPa | not declared. Closed by my estimate (3 to 8×) |
| Release | need 20.3, available 32.9, 1.62 (oil 1.70) | 20.325; 32.895; 1.618; oil 19.316, 1.703. At 2.5 V at the motor 1.19, at 2.0 V 0.95 | reproduces |
| Hertz, line 2.65, R 1.5, onset 230 | 163 / 209 / 225 / 252 MPa | 162.8 / 209.3 / (oil 225) / 252.4. If one lug carries the whole load: 283 (dry), 297 (oil). If contact is 0.5 mm long: 375 to 581 | reproduces, but see 4.1 on line contact |
| Pilot sequence | pilot 0.80 past the head pitch plane, bore cylinder 0.65, margin 0.15 | 0.80, 0.65, 0.15 at the pitch plane. **At the tooth crest plane (+0.2, where the lug V lead-ins start, `coupler.py` §12): −0.05** | arithmetic right at the stated plane, wrong plane (5) |
| Windows | lateral ±0.75; roll ±5.5; pitch ±0.73 | (2.05 + 0.4) − (2.0 − 0.3) = 0.75; atan(0.6/6.2) = 5.54; 0.731 | reproduce |
| Stop groove | 122.0 deg of travel | Free front-face arc between entry notches at r 5.3: 134.6 deg. Needed 122 + pin 10.8 = 132.8 deg. Slack 1.8 deg (0.17 mm) | fits barely, no tolerance allowance |
| Declaration fit | G2 clean | 741 pairs none, nut blocks behind plate pieces, lobes on strips z 7.45 to 11.2 and −11.2 to −5.45 | fits. Exceptions: 3 and 5.3 below |

Sources, raw:
- **Wikipedia Leadscrew wikitext.** The table "Coefficient of friction for leadscrew threads" has "Steel, dry" on bronze 0.15–0.23 and "Steel, machine oil" on bronze 0.10–0.16. Self-locking when μ is greater than tan(lead angle), "not absolute" under vibration or shock loading. All as cited. Note: the table is for screw threads, not for a 304 lug on C93200 flank under a few newtons. It is an analogy, labelled provisional.
- **Engineering ToolBox.** Steel on steel clean and dry 0.5–0.8 static, kinetic 0.42. PTFE on steel clean and dry 0.05–0.2. All as cited.
- **206-109 PDF.** Row 13 rated load 3 mN m (unlabelled, not marked min or typical). Row 12 rated voltage 3 V. Row 14 rated speed 140 rpm. Row 16 max start voltage 0.5 V. Row 18 max operating voltage 3.6 V. Row 21 max start current 230 mA. Row 31 typical stall torque 9 mN m. Row 38 typical resistance 14.5 ohm. Body 6 × 18.7, shaft 2 × 3.6. As cited. There is no guaranteed minimum stall torque, so 0.88 N is derived, not stated.
- **EOS PA 2200.** The cited tensile strength 50 MPa could not be read at the cited URL. From memory, public EOS sheets quote about 48 MPa in XY and about 42 MPa in Z. That is unverified memory. If it holds, the plate margins fall by 4 to 16 percent and stay above 2.5×. G3 should have a human re-read of this source.

## 3. Status of each v3 item (v3 section 7)

| v3 item | v4 | Status |
| --- | --- | --- |
| 1. Tail stud mount (PA12 thread, unsized) | Two countersunk M1.6 A2 screws from inside the end plate into blind 0.6 mm holes in the 304 flange at z ±4.6. All loads sized, all reproduce. No PA12 thread | **Closed for the load path.** Open sub-items: plate bending not calculated (my estimate 6 to 15 MPa, closes it), the 0.2 mm web below the hole (6), screw access (5.7) |
| 2. Plate joints, plate as beam | One-piece SLS shell. Head plate checked with a circular-plate model. Hinge legs added | **Closed for head and tail plates by my beam estimates.** The declared model is wrong (5.3). The hinge ear-to-leg connection is not declared (4.1, 5.5) |
| 3. Slot lash at wrong radius | Lash 3.17 to 3.46 at r 3.5, phase 0.88, clearance 2.29 | **Closed.** The tube slot ends at r 3.5, and at the seat the lug is behind the flange slots (lug trailing edge at depth 2.1 against flange 0.8) |
| 4. Teeth meshing at the lower-bound motor | Pitch fallback: 1.25 N needed, 0.88 N available, partial seat 0.73 deg, ±0.162 | **Narrowed, not closed.** Pitch is shown. Roll and yaw are omitted and are adverse (4.4) |
| 5. Reference planes | Pitch plane = head flange face. Lands recessed 0.25. Bore chamfer 0.4. Sequence margin 0.15 | **Closed for the planes**, which are now declared. The margin is stated at the pitch plane, not the crest plane (5.4). The lateral conclusion holds (4.4a) |
| 6. Small figures | Rim band 0.6 in the dossier. W × 48.0 in the declaration. `coupler-motor`, S-end, front plates and fasteners added to `component_ids` | **Mostly closed.** `coupler.py` still prints "1 mm band, 1.86 MPa" and "W x 47.2". The hinge parts are not in `component_ids` although the text claims them |

## 4. Findings per means

### 4.1 Retention, per load

**Principle.** Two 304 lugs bear on the hook flank of the 3 deg lock stage of the C93200 sleeve. The wedge self-locks while μ is greater than tan 3 deg at any load and needs no power. The Hirth teeth carry torsion and shear. The lugs in the tube slots (r 2.05 to 3.5) are the backup path for torsion. A friction wedge is acceptable passive retention at the Gate 1 paper level (CPL-009, Q31 item 6): no power, no stored energy, and the declaration states the vibration limit and claims no curvature hold.

**Tension 1.225 N.**
- Path: lug → hook flank → sleeve → PTFE ring (r 3.6 to 4.4, 14.7 mm² after notches) → flange rear face → two screws → nut blocks → plate.
- Ratio 3.60 to preload at typical F_p. At 0.88 N the faces gap by about a micrometre; the lugs hold.
- Screws 0.61 N each against 454 N (head) and 341 N (tail) strip.
- Supported.

**Torsion 7.78 mN m.**
- Teeth: tangential 1.748 N at r_m, axial separating at most 1.748 N, ratio 2.52 at 4.41 N.
- Below that ratio the faces ride up elastically by at most 0.001 mm, which is 0.013 deg. That is far below the 2.29 deg lug clearance.
- If the stud sits off the tooth centre, the lugs take torsion on the tube slot sides (r ≤ 3.5, about 1.4 N per lug). The slot side is tangential, and the lug slides along the 3 deg flank, which moves the stud axially by under 10 µm.
- So torsion has a closed carrier in both the meshed and the unmeshed state.
- Tail: screws in shear 0.85 N each, PA12 hole bearing 0.44 MPa.
- Supported.

**Shear 0.306 N.** Teeth, ratio 14. Tail screws 0.15 N each. Supported.

**Out-of-plane bending 14.7 mN m.**
- Tipping edge z ±6.3: 27.8 mN m at 4.41 N (1.89×).
- Beyond tipping, the lug flank force rises with the tilt. Self-locking holds that force, k_loop 20 kN/mm, so about 2.3 N is reached in under 0.1 µm.
- The pilot couple (tilt ≤ 1.49 deg) is a second backup.
- The lugs sit on the y axis, so they add no moment about y. They add the axial force that the tipping edge needs.
- Head mount 1.47 N, tail mount 1.96 N per screw.
- Supported.

**In-plane bending 14.5 mN m (drive limit).**
- Tipping edge y 5.87 (slots remove 35 % of the head ring): 25.9 mN m (1.78×).
- Beyond tipping, the lug pair (lever 10.74 mm) acts as axial load on the self-locking stage.
- Fault 52.2: Hertz 252 MPa, above the 230 onset. This is local indentation of bronze, not separation, and the declaration says so.
- Supported.

**Line contact (Gate 2/3, noted).** The Hertz figures assume a 2.65 mm line along the flank. A radial lug on a helicoid meets it where the local slope matches. Slope falls from 4.12 deg at r 3.55 to 2.36 deg at r 6.2, so contact is short. At 0.5 mm length p0 is 375 to 581 MPa. The two slots are also statically indeterminate: 15 µm of slot position error against about 190 kN/mm stiffness means one lug can carry nearly all of the preload (283 to 297 MPa). Bronze beds in by yielding, as the declaration admits for the fault case. The 163 / 209 / 225 MPa figures are therefore not a retention margin, and retention does not rest on them. Fine machining and wear are Gate 2/3. The self-locking margin at the inner flank end (1.39 oiled) is the figure that matters, and it is positive.

**Mounts.**
- Head: flange on the plate's outer face, two screws at z ±7.8 into 304 nut blocks. Pivot on the lobe tip (17.2 mm), on the disc rim (7.0 mm). The disc is r 7.0, the window half-width is 6.45, so the rim band is 0.55 mm and about 2.0 mm². Rim reaction 7.46 N gives about 3.7 MPa, which is fine.
- Tail: flange on the plate's outer face, two screws at z ±4.6 from inside, pivot on the flange edge at 6.3 mm. All reproduce.
- Plate bending: head 7.8 to 15.6 MPa (my beam, declared 5.9 from the wrong model), tail 6 to 15 MPa at the fault (not declared, my estimate). Against 50 MPa (unverified, 4.0) this is 3 to 6× in the worst case.

**Hinge.**
- Ear force 14.7/18.3 + 0.61 = 1.41 N. Torsion couple 0.42 N. Pin bearing 0.47 MPa. Pin bending under the stacked loads is about 2 MPa.
- The pin passes four bearings (tail plate-low, head ear-low, tail plate-up, head ear-up), alternating, so the path is determinate.
- Not closed as declared: ear and leg are "one 304 part" but the 1.2 mm inner wall (box x 1.8 to 3.0, no declared notch at the ears) lies between them. The leg bears on the wall in pull-off and the screw holds it in push. This works with a neck through an undeclared notch (up to the top edge for the upper ear, to the sector slot for the lower ear), and fails as two separate parts. Load is 1.4 N and the fix is trivial, but it is undeclared (U3).
- The lower plate sits 0.1 mm off the floor in its box (z −10.7 against −10.8). That is a box offset only.

**Preload source.** The 0.88 N bound is a reasonable inference (stall at 3 V is at least the rated 3 mN m, and friction is at most 0.5 V of the winding). The rated-load row is not labelled as a guaranteed minimum. I accept it for retention because the seated retention does not depend on F_p. I do not rely on it for closing (4.4).

### 4.2 Retention, combined

All loads at once: axial separating 3.279 N against 4.41 N typical, so the teeth stay seated (1.35×). Residual clamp 1.13 N gives a tipping capacity of 7.13 mN m against a vector sum of 20.65 mN m, so the faces gap at one edge. Gapping is not separation (the elastic argument), because the lug stays on the self-locking stage and the far-side teeth stay meshed. Supported **for the fully seated state**.

### 4.3 Release and closing logic

- **Release.** The head's own motor turns the sleeve to the open stop. Need 20.3 mN m (19.3 oiled), available 32.9 at 3.4 V and η 0.9: 1.62 (1.70). The ratio does not depend on the motor constant, because closing and release use one motor. With the supply rule (cell at or above 3.5 V) the margin is at least 1.19 down to 2.5 V at the motor. Ejection (capture stage outer flank pushes the stud out 1.4 mm; load 0.81 N) needs about 4 mN m at the 20 deg flank (my estimate), far below 32.9. The reaction goes into the 304 collar, 0.02 MPa. Release is bounded and independent: each head releases its own joint.
- **Stop.** Pin dia 1 (304), 38.7 mN m at 3.6 V stall, 7.30 N, shear 9.3 MPa, bearing 14.6 MPa; reaction through the flange screws 2.5 N each. Closed. The groove fits with 1.8 deg slack (table, section 2).
- **Closing.** A fixed-time drive at 1.0 V PWM average stalls on the teeth. The stop at 122.0 deg is the end of the lock stage, beyond the deepest full seat (3.681 against 3.80). At the lower bound the capture stage needs 1.21 mN m against 1.94 mN m, a margin of 1.6.
- **Not declared (U2).** The coupler motor mount, with the reaction torque 6.30 mN m at release and 10.8 mN m at stall, and a 3.15 N radial mesh force on the 2 mm shaft. The cell-voltage measurement that sets the duty for 1.0 V (a 3.0 to 4.2 V cell at a fixed duty gives 0.81 to 1.14 V, so F_p ×0.81 to ×1.14) and the 3.5 V release rule. The controller declaration has no divider or sense component. At F_p ×0.81 the typical minimum is 3.6 N against 3.28 N separating (1.09×), so this does not by itself defeat the argument.
- **No state sensor.** Stated by the declaration (Q32).

### 4.4 Alignment means

**(a) Lateral: chamfers and pilot.**
- Principle: 45 deg chamfers (nose 0.3, bore 0.4 from the land recessed 0.25) lead into the 4.10 bore. Centring force (1 − μ)/(1 + μ) of the push is 0.11 at μ 0.8, with no wedging while μ is below 1.
- Window ±0.75 against ±0.6 stack. The lug V lead-ins accept ±0.8 on their own (0.2 slot clearance plus 0.6 V).
- Pilot-before-lug: margin 0.15 at the pitch plane, but −0.05 at the crest plane where the lead-ins start. The lateral error at the lugs is then at most about 0.12 to 0.2 mm, still far inside 0.8. So the guide works whichever plane is taken. The stated arithmetic is wrong (5.4).
- Over-constraint: pilot radial clearance 0.052 to 0.065 (diametral 0.104 to 0.130) against a Hirth centring error well under 0.05, so the pilot does not fight the teeth. The declaration's "0.130" is diametral but is used as radial; conservative.
- Force sufficiency against table friction needs the external push (0.31 N), which the candidate does not supply. This is a capture sweep (CPL-006), and the declaration claims no window. Gate 2/3.
- Supported as geometry.

**(b) Roll, pitch, yaw.**
- Geometry is supported:
  - V lead-ins give ±5.5 deg at r 6.2 against ±1.4 deg incoming.
  - The tube slots hold roll to ±3.17 deg at the teeth meeting, which is under half a pitch (5 deg). The teeth therefore find their own gap.
  - Pitch ±0.73 deg. Yaw 1.49 deg by the pilot.
  - No guide is blocked at a declared corner (checked: PTFE and flange notches, the open stop within ±0.3 deg against ±7.1 deg).
- **Unsupported (U1):** the statements "the teeth fix roll with zero lash" and "the teeth align yaw under the draw". They need a draw that rolls or yaws a unit against the table. Computed above: roll needs 3.69 mN m, and the ramps give 0.44 mN m at 0.88 N and 2.2 mN m at 4.41 N at the author's own μ 0.8. At lower μ the typical motor can do it (μ 0.5: 6.5 mN m), the lower bound cannot (at most 3.92 mN m with no friction). Yaw friction torque on the table is about 4 to 6 mN m against a lug moment of 4.3 mN m at 0.88 N.
- **Consequence (U1).** A partial seat sits shallower by r·ε. Spare margin is 0.118 mm after the stack and 0.038 mm after the pitch residual. Roll 1.4 deg gives 0.154 mm, yaw 1.49 deg gives 0.127 mm at the lugs. Either one leaves the lug in the 20 deg capture stage. That stage is not self-locking (tan 20 deg = 0.364 against μ at most 0.23), so power-off releases the preload and tension can back-drive the sleeve. The author's fallback (retention without flattening) is therefore not shown for roll or yaw, and by the author's own method it fails by 0.04 to 0.1 mm in the combined corner.
- This corner is: lower-bound motor, presented pose at its declared extremes, μ 0.8 at the teeth, stack at the shallow end. It is a closing and capture matter (CPL-006, CPL-010) that the author could withdraw or bound. I did not rate it a contradiction of retention of the seated joint. I rate it an unsupported claim in the declaration, because the declaration makes the claim.

**(c) Axial closing and seating.**
- The 20 deg capture stage draws 1.0 mm for 1.21 mN m at μ 1 (9.68 to 10.75 typical, 1.94 at the lower bound). The 3 deg stage then seats the faces. The stack seats inside the lock stage with 0.118 mm each side, for the fully meshed state.
- The external axial push of 2.40 mm (0.31 N at μ 1) is not supplied by the candidate and is declared so. Tolerance is taken by sleeve travel to a stall.
- Supported for the fully meshed state. For partial meshes see (b).

### 4.5 Magnetism

No magnet component. `mechanism_kind` is `friction_wedge`. No alignment of kind `magnetic`. Not applicable. Check 4 holds. Nothing in the text assumes magnetic attraction.

### 4.6 Automated checks 1 to 5 (protocol section 8)

I checked each programmatically against `declaration.json`.
1. `requires_power_to_hold` is `false`. Holds.
2. `bounded_independent_release` is `true`. `release.means` is nonempty and physical. Holds.
3. `mechanism` and all three `alignment[].justification` are nonempty. All 13 `component_ids` (head-cartridge, head-flange, tail-stud, retainer-collar, nut-block-up, nut-block-low, coupler-motor, S-end, L-front-n, L-front-p, L-front-lo, L-front-hi, fasteners) exist. Holds.
4. No `magnet` component, no `permanent_magnet`, no `magnetic` alignment. Holds.
5. Each alignment names existing components (tail-stud, head-flange, head-cartridge; and head-cartridge, coupler-motor, coupler-pinion, tail-stud). Holds.

Note: `component_ids` omits the hinge parts, the legs and the pin although the retention text claims the hinge path.

## 5. Errors found

1. **Partial-seat fallback covers pitch only.** See 4.4(b). Roll and yaw are omitted.
2. **Seating force.** The 1.25 N for pitch assumes every ramp is perpendicular to the vertical. With the 2/π projection it is about 1.97 N. The direction (above 0.88 N) is unchanged.
3. **Head plate model.** The plate is a 3.75 mm strip beside a 12.9 mm window, not a clamped disc r 10. Real stress is 7.8 to 15.6 MPa, not 5.9. The tail end plate bending is not computed at all. Both are within strength by my estimates.
4. **Pilot reference plane.** The 0.15 margin is taken at the head pitch plane. The lug V lead-ins start at the crest plane (`coupler.py` §12), where the margin is −0.05. The conclusion (lateral error at the lugs is far inside 0.8) holds.
5. **Hinge ear and leg.** "One 304 part" crosses the 1.2 mm wall with no declared notch. The wall box is a full slab.
6. **Stud flange blind hole.** The M1.6 hole is 0.6 deep in a 1.0 flange, with teeth roots 0.2 below the front face. The web below the hole is 0.2 mm. The M1.6 × 4 lumped screws are longer than the 1.8 mm of hole plus plate. Strength is fine (341 N). It is a fine-machining detail.
7. **Assembly statement against the declared geometry (G2 text, not a G6 load path).**
   - The gear ring is m 0.3 z 43, so tip diameter 13.5 and pitch diameter 12.9. The plate window is 12.9 square. The statement "cartridge assembled outside, pushed through the window from the front" cannot work. A gear ring of 13.5 does not pass a 12.9 window.
   - The tail stud screws are driven "from inside" along x in a 6.4 mm deep cavity (x −9.4 to −3.0) closed by the inner wall. A driver clear of the wall must be tilted 39 deg (z 5.6) or 66 deg (z −3.6). The same holds for the plate-up-leg screw. Straight drivers need under about 15 deg.
   - The protocol checks only that an assembly statement exists, so this does not break check 5 or G2. The statement needs correcting.
8. **Stale script prints.** `coupler.py` §5 prints "W x 47.2". §11 still prints the 1 mm band and 1.86 MPa. The declaration text is correct.
9. **Seat margin uses a nominal loop stiffness.** The 20 kN/mm "lower bound" is the series value (21.7). It is labelled provisional. The argument is insensitive by more than 15×.
10. **Zero tooth clearance.** Crest +0.2 and root −0.2 on both rings put tip and root at the same plane. Real Hirth teeth need root relief, or the tips bottom before the flanks seat. This is not in the stack (Gate 2/3 tooth form).
11. **EOS strength not re-verified** (section 2).

I found no arithmetic error in the cam layout, stack, self-locking, preload, release, stop pin, mount loads or windows. All other declared figures reproduce.

## 6. Classification of weaknesses

**Contradiction (defeats a requirement):** none of the seated joint. The partial-seat corner (4.4b) is adverse by my numbers but depends on stacked extremes at a motor bound that is itself inferred, and the author can withdraw or bound it. I treat it as unsupported, not as a contradiction.

**Unsupported (blocks `pass`):**
- **U1.** The teeth cannot be shown to fix roll and yaw at the lower-bound motor, and the retention-without-flattening fallback omits both. By the author's own numbers the spare margin after pitch is 0.038 mm.
- **U2.** The coupler motor mount (release and closing reaction 6.3 to 10.8 mN m, 3.15 N mesh force) and the cell-voltage measurement are not declared.
- **U3.** The ear-to-leg connection through the inner wall is not declared (a notch and neck), and the hinge parts are not in `retention.component_ids`.

**Closed by reviewer calculation (declaration needs correcting, no longer blocks):**
- Head plate bending (7.8 to 15.6 MPa) and tail plate bending (6 to 15 MPa at the fault), both against 50 MPa (unverified).
- The pilot sequence (−0.05 at the crest plane, still within the 0.8 lug acceptance).
- The hinge ear force numbers and pin bearing.

**Gate 2/3 (do not block):**
- Vibration back-driving of the wedge.
- Wear, galling of 304 on 304, PTFE creep, and thermal drift of preload.
- Fine machining of the 36-tooth rings (tip and root relief) and the helicoid flank. Line contact versus short contact. Two-lug load sharing and bronze bedding-in.
- Capture sweeps, lateral centring against table friction, and the push-in force.
- The assembly statement (7 above), the 0.1 mm plate-to-floor box offset, the stop groove slack of 1.8 deg, the stud-flange web, the countersink detail in the 0.8 mm lobe (cone 0.7 deep, web 0.1, punch-through about 250 N, so strength is fine), and rubbing of the sleeve on a PA12 window corner (0.15 mm clear against ±0.3 SLS).

## 7. What a further version would need

1. Bound or withdraw the lower-bound seating claim for roll and yaw. Add the roll residual (up to 1.4 deg: 0.154 mm) and the yaw residual (0.127 mm at the lugs) to the pitch residual, and show the lug stays inside 3.40 to 3.80. Options: widen the lock stage (D2) or shift the nominal seat so the shallow side has at least 0.35 mm, state a closing sequence that supplies more draw (a higher closing voltage with a current-sense stop), or restate retention as holding only for a fully meshed seat and call partial seat a CPL-010 state. Also correct the 1.25 N seating force.
2. Declare the coupler motor mount (clamp or saddle) and size it for 10.8 mN m reaction and 3.15 N mesh force. Declare the cell-voltage sense component, or drop the supply rule.
3. Declare the ear and leg neck through the inner wall (a notch), or make the ear and leg two parts with a fastener that carries the pull-off. Add the hinge parts to `component_ids`.
4. Recompute the head plate as the strip (not the circular plate). Compute the tail end plate.
5. Restate the pilot margin at the crest plane, or move the lug lead-in start to the pitch plane.
6. Correct the assembly statement: the gear ring against the 12.9 window, and tool access for the tail stud and plate-up-leg screws.
7. Clean up: the stale prints in `coupler.py`; screw lengths against the 0.6 mm hole.
8. Re-read the EOS PA 2200 tensile strength from a source that can be fetched.

None of this needs more volume (the stowed margin stays about 1.14 mm).

## 8. Basis of the outcome

Under protocol section 8 and Q062, `pass` needs retention under every declared load and every alignment means to be physically justified on paper, with no declared load missing a carrier. The seated joint now meets that for tension, torsion, shear, both bendings and the combination, at the tail as well as the head. The v3 tail stud and plate gaps are closed. The slot lash is now taken at the correct radius and reproduces.

The record still has unsupported claims:
- The claim that the teeth fix roll and yaw, and that retention does not need flattening, is shown for pitch only. For roll and yaw the declared numbers show about 0.04 mm of spare margin against shortfalls of 0.13 to 0.15 mm.
- The motor that carries release and closing has no declared mount.
- The hinge ear-to-leg connection is not declared.

Unsupported claims make the outcome `unresolved`.

`fail` needs a claim contradicted by the declaration's own numbers or by physics so that a retention or alignment requirement is defeated. The seated joint has a closed carrier for every declared load, the self-locking margin is positive (1.39 at the worst flank end), and release has a bounded 1.62 margin. The adverse corner needs a lower-bound motor that is only inferred from the datasheet, an uncorrected presented pose at its declared extremes, the author's own dry tooth friction bound, and the shallow end of the stack, all together. I did not rate that a contradiction. I did not give `pass` because a wrong pass is the worse error. The author can close the items by calculation or by narrowing the claim.

I would change to `pass` if U1 to U3 are closed with numbers from declared dimensions, and the errors in 5 (3, 4, 5, 7) are corrected in the declaration text.

This record is a paper judgement only, label `exploratory`. It does not show that the mechanism works.
