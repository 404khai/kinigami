candidate_id: cand-d
candidate_version: 2
author: Claude Opus 5.5 (engineering lead, cand-d author)
reviewer: reviewer-d2-retention (Claude Sonnet 5.5, independent session, no authorship in cand-d)
outcome: unresolved

# Retention and pre-alignment review: cand-d v2, r1

Date: 2026-11-20.

Declaration `candidates/cand-d/declaration.json`, SHA-256 `659810c455376de8c3450d42556f266e3c37ed6260f235a3676dec22725cc0cf`. I computed it with `shasum -a 256`. It equals the hash in `dossier-v2.md` and the expected value. Figures marked "reviewer" are my own computation (python3, script kept outside the repo). I also ran the author's `coupler.py`, `joint.py` and `gen_declaration.py` (without `--write`). They reproduce the dossier numbers and `git status` stayed clean.

Files read: `AGENTS.md`; `docs/validation/gate1-v1-protocol.md` section 8; `criteria/gates/gate1-v1.json` (G6); `docs/decisions/Q062`, `Q031` (item 6), `Q085`, `Q086`, `Q087`; `Q036` (by reference only, not re-read in full); `docs/requirements/requirements.md` CPL-001..CPL-011; `candidates/cand-d/declaration.json` (retention, release, alignment, limitations, summary, chain, sites, assembly_access, stowed primitives, and every component box, with full text of head-cartridge, tail-stud, retainer-collar, both ears, coupler-motor, coupler-pinion, hinge-pin, front-wall pieces, fasteners); `candidates/cand-d/dossier-v2.md`; `candidates/cand-d/scripts/` (`README.md`, `coupler.py`, `joint.py`; `gen_declaration.py` and `declaration_text.py` run, not read line by line); `candidates/cand-d/retention-review-v1-r1.md` (section 6 and the findings it refers to). `candidates/cand-a/retention-review-v5-r1.md` was not re-read in this session. I used the v1 record for calibration of rigour.

Raw sources checked in this session (curl, then grep or pdftotext): Wikipedia Leadscrew (`action=raw`), Engineering ToolBox friction page (HTML text), Precision Microdrives 206-109 PDF (`pdftotext`), Concast C93200 page. Results are in section 2.

This is a paper judgement under protocol section 8. It is not a test of the mechanism (Gate 2/3).

## 1. Judgement in brief

v2 is a real improvement on v1. Most v1 items are closed or narrowed. The core ideas hold on paper:
- The friction wedge is self-locking with margin (2.86 dry, 1.91 oiled at the declared lead angle; 2.08 and 1.39 at the inner contact radius, reviewer).
- Tension, shear, torsion and out-of-plane bending have carriers inside the machined coupler.
- The Hirth ring does make roll independent of face friction under the declared single loads.
- The release torque and supply rule reproduce (1.62 dry, 1.70 oiled).

I do not record `pass`. Four things are unsupported, and one is a wrong lever in the author's own mount calculation:

1. **The ears have no declared load path to the housing.** The ears (x 32.8 to 34.4, radius 6.45 to 8.35 from the axis) are boxed apart from the lip (x 34.8 to 35.6, radius up to 6.45). The annulus between them (radius 3.55 to 6.3) is the rotating sleeve. The gap in radius is 0.15 mm and in x is 0.4 mm. The ears are the only axial restraint of the cartridge in the shell. "One part with the housing" is a statement, not a geometry.
2. **In-plane bending has no lever at the ears (error).** The ears lie on the vertical (z) line through the coupler axis. They resist moments about y only (out-of-plane bending). The in-plane bending (14.5 mN m, fault 52.2) is a moment about z. The ear pair gives it zero lever, yet `coupler.py` and the declaration size "worst screw load 1.59 N" with lever 7.4 for the larger of the two bendings. The real carrier is the lip in the window and the screw shanks, with a lever of about 0.8 to 1.6 mm. That gives 9 to 18 N lateral on PA12 (31 to 44 MPa line contact, reviewer), and 33 to 65 N at the fault (58 to 83 MPa). The load is carried on paper, but the number the declaration gives is wrong by a factor of 6 to 11, and the PA12 bearing is near its strength.
3. **"Zero lash and the lugs never slide" rests on an unsupported phase claim.** The Hirth tooth phase and the lug slot lash are two roll indexers on one body. The slot lash is +-0.30 deg minimum at the tube outer radius 3.5 (the author uses 0.38 at radius 2.77). The phase error between teeth and slots is given as "about +-0.2 deg (one set-up)". There are two parts. The sum is +-0.4 deg and the RSS is 0.28 deg, both at or above the lash. At that corner the lug touches the slot side before the teeth reach zero lash on both flanks. The torsion carrier still exists (slot sides). But the no-slide argument for the sleeve is then not shown.
4. **Combination and preload depend on a typical motor value.** The 4.41 N F_p_min comes from a linear stall model at 1.0 V. The datasheet gives typical values only and a max start voltage of 0.5 V. With an offset model (reviewer, illustrative) F_p_min is 2.65 N. The single-load ratios stay above 1 (torsion 1.52). The all-loads-at-once teeth ratio falls from 1.35 to 0.81. The author already says the combination gaps the faces, and retention in the combination is then carried by the lugs, so this alone is not blocking. It does matter for the "teeth stay seated" statement.
5. Smaller unsupported items: the PTFE ring needs a notch for the lugs and none is declared; the lip slots and V lead-ins remove 22 to 61 percent of the Hirth ring by radius, and the tipping lever and flank pressure use the full ring; the window and lip are both r 6.45 with a declared PA12 tolerance of +-0.3, so the nominal fit is not shown; pilot before lug has margin 0.000 at nominal.

I record `unresolved`, not `fail`. I looked for a claim that physics or the declaration's numbers defeat outright. The nearest is item 2. It is a wrong lever on a small load, and a plausible fix exists (separate the ears in y, or thicken the lip). It does not remove the carrier. Item 1 is an undeclared connection, not a proof that none can exist. A pass needs a new version.

## 2. Independent recomputation

All figures marked "reviewer" are mine.

| Item | Author | Reviewer |
| --- | --- | --- |
| Unit weight W, mass 31 109 mg | 0.3051 N | 0.3051 N |
| Cam: capture 20 deg, 1.0 mm; lock 3 deg, 0.4 mm; Rc 4.875; slot -24.7 to 139.6 deg; web 15.7 deg (1.34 mm); seat rotation 77.1 deg; stop at 122.0 deg | as left | web 15.69 deg (1.34 mm at Rc); capture arc 32.3 deg, lock arc 89.7 deg; reproduces |
| Axial stack, 7 terms, IT9 / g6 | +-0.0815; seat 3.518 to 3.681; margin 0.118 / 0.119 | 3.5185 to 3.6815; margins 0.1185 / 0.1185. Reproduces. Missing: lug-axis angular error (perpendicularity), flank form error, PTFE creep (author says not counted) |
| Self-locking at Rc, tan 3 = 0.0524 | 2.86 dry, 1.91 oil | 2.86, 1.91. At the inner contact radius 3.55 (constant-pitch flank): lead 4.12 deg, margins 2.08 dry, 1.39 oil. At 6.2: 3.64 and 2.43. All above 1 |
| Preload F_p, 1.0 V stall, linear in V | 4.41 to 9.00 N dry; 5.25 to 11.35 oil | 4.41 to 9.00. With T(V) = 9 (V - 0.5) / 2.5 (reviewer, illustrative, from the datasheet start voltage 0.5 V): motor 1.80 mN m, F_p 2.65 to 5.40 N. With torque from current (14.5 ohm, 185 mA typical start): motor 3.36 mN m, F_p 4.93 to 10.06 N |
| Release need, worst dry corner (F_p_max 9.00 + 3.27 N, flank 0.23, thrust 0.20) | 20.3 mN m | 20.31 mN m |
| Release available, 3.4 V, eta 0.9 | 32.9 (1.62 dry, 1.70 oil) | 32.89; ratio 1.62. At 3.0 V: 1.43; at 2.7 V: 1.29 (so even below the 3.5 V rule the worst corner holds on this arithmetic). The rule matters little |
| Hirth: pitch, axial separating force from torsion | 0.777 mm; 1.74 N at r_m 4.45 | 0.777 mm; 1.74 N. For flanks of constant height 0.4 (the declared "teeth +-0.2") the flank angle varies with radius, but the axial force is T x (pitch / (2 h r)) summed = 0.218 T = 1.69 N, almost independent of load distribution. Reproduces |
| Torsion ratio, alone | 2.53 | 2.53 (F_p_min / 1.74). This is the point where the trailing flanks unload (T = F_p r_m = 19.6 mN m). It is not a separation: the lugs block axial lift, so the teeth cannot lift in any case (reviewer) |
| Combined axial separating loads | 3.27 N, ratio 1.35 | 3.27 N; ratio 1.35 at F_p_min 4.41; 0.81 at 2.65 N (offset model) |
| Face tipping, alone | 27.79 mN m; 1.93 (out-of-plane), 1.92 (in-plane) | 27.79 reproduces for out-of-plane (edge at z, intact). In-plane: the lug slots (3.05 wide, V lead-ins to 4.25 at the face) open the ring at +-y. The outermost remaining contact is at y = 5.93 to 6.11: tipping 26.2 to 27.0 mN m, ratio 1.80 to 1.86 |
| Hirth ring removed by the two slots (4.25 at the face) | not stated | 61 percent of the circumference at r 2.6, 32 percent at r 4.45, 22 percent at r 6.3 |
| Residual clamp under all loads and tipping capacity | 1.14 N; 7.21 mN m vs 20.4 | 1.14 N; 7.2 mN m. Out-of-plane part 14.4 vs capacity about 7.2: the pilot couple takes about 7 mN m (lever about 5 mm, about 1.4 N) |
| Hertz p0, lug on bronze flank (E* 73.6 GPa, r 1.5, L 2.65) | 163, 209, 225, 252 MPa | 163, 209, 225, 252. Reproduces. Onset 1.67 x 138 = 230 MPa is a rule of thumb the declaration labels. 225 is 2 percent under it; 252 is over (local indentation) |
| Lug-slot roll lash | +-0.38 to 0.75 deg (r 2.77) | +-0.38 to 0.75 deg at r 2.77; +-0.30 to 0.60 deg at r 3.5, the binding radius of the tube wall |
| Phase tolerance teeth vs slots | "about +-0.2 deg" | not derived. Two parts: +-0.4 deg sum, 0.28 RSS. Exceeds or equals +-0.30 deg |
| Stop pin, 3.6 V stall at the sleeve | 7.3 N; shear 9.3 MPa; bearing 14.6 MPa | 7.30 N; 9.30; 14.60. Reproduces |
| Retainer reaction | 0.81 N; 0.02 MPa | 0.81 N plus the 0.5 N provisional term. Trivial |
| Mount, ear pair for out-of-plane bending 14.4 | 1.59 N per screw (max of both bendings, lever 7.4, plus half the tension) | 14.4 / (2 x 7.4) + 0.61 = 1.58 N. Right for out-of-plane only |
| Mount, in-plane bending 14.5 (fault 52.2) | treated with the same ear lever | **ear lever 0** (ears at y = axis, z = +-7.4). Lip-in-window and screw-shank lever 0.8 to 1.6 mm: 9.1 to 18.1 N lateral; PA12 line contact (E 1.7 GPa, assumed, not cited) p0 31 to 44 MPa. Fault: 32.6 to 65.2 N, 58 to 83 MPa |
| Window, lip, flange, PA12 tolerance | flange 6.3 < lip and window 6.45; gap 0.3 min | Nominal lip = window = 6.45. With the declared +-0.3 PA12 tolerance the lip does not fit a window at 6.15 and a flange of 6.3 overlaps the plate there. The declaration gives no window tolerance |
| Ear to lip geometry | "one part with the housing" | ear x 32.8 to 34.4, r 6.45 to 8.35; lip x 34.8 to 35.6, r to 6.45; sleeve r 3.55 to 6.3 between. Gap 0.15 in radius, 0.4 in x |
| Pilot before lug | 0.60 into the bore vs chamfer 0.60 | 5.70 - 5.10 = 0.600 vs 0.600: margin 0.000 at nominal. Lug axis tolerance +-0.015 (IT9) makes it -0.015 at one corner. Effect: the lug sees the pilot clearance plus 0.015 mm, against +-0.6 V lead-ins. Not a blocked guide |
| Roll window | +-5.5 deg at r 6.2 | 5.54 deg vs about 1.4 deg stack; reproduces |
| Pitch | +-0.73 deg | 0.731 deg |
| Yaw before the teeth meet | 1.49 deg (0.130 / 5.0) | 1.49 deg; with the 5.7 mm actual engaged length 1.31 deg. Also 0.130 is the diametral clearance, so the lateral error at the lugs is 0.065 mm radial, half of what the author uses |
| Joint outline contact | +-16.13 deg; margin 1.14 deg | 16.13; first sweep contact 16.14 deg |

Source checks (my fetches, 2026-11-20, raw text):
- **Wikipedia Leadscrew (`action=raw`).** The friction table "Coefficient of friction for leadscrew threads" has rows Steel, dry: steel nut 0.15 to 0.25, bronze nut 0.15 to 0.23; Steel, machine oil: bronze nut 0.10 to 0.16. So "steel on bronze dry 0.15 to 0.23, oil 0.10 to 0.16" is correct. The self-locking paragraph says the screw is self-locking when the coefficient of friction exceeds the tangent of the lead angle (friction angle greater than lead angle), and that the property "is not absolute" under vibration or shock, where the effective coefficient may drop to dynamic levels. It recommends a secondary holding brake in safety-critical applications. Reproduces. The page also says "Most are self-locking" in a general list. The 0.35 value is not on the page, and v2 does not use it.
- **Engineering ToolBox.** "Polytetrafluoroethylene (PTFE) Steel Clean and Dry 0.05 - 0.2" present. "Steel Steel Clean and Dry 0.5 - 0.8 0.42" (static, kinetic) present. Only bronze rows: "Bronze Steel Grease 0.16", "Bronze Cast Iron Clean and Dry 0.22", "Bronze - sintered Steel Grease 0.13". There is no dry bronze-steel row, as the author says. The steel-steel row is generic, not stainless on stainless.
- **206-109 datasheet (`pdftotext`).** Rated 3 V, rated load 3 mN m at 140 rpm, max start voltage 0.5 V, max operating voltage 3.6 V, max start current 230 mA, typical start current 185 mA, typical stall torque 9 mN m, typical terminal resistance 14.5 ohm, ratio 136:1 planetary, typical peak efficiency 26 percent, 1.2 g, body 6 x 18.7, shaft 2 x 3.6. All "typical" except where "max" is printed. No lower bound on stall torque, no stated voltage for the 9 mN m. The dossier's "start current 230 mA x 3.7 V = 851 mW" is the max start current at the cell voltage, as a peak bound.
- **Concast C93200.** Density 0.322 lb/in3 (8.91 g/cm3), yield 138 MPa (20 ksi, at 0.5 percent extension, minimum, ASTM B505), tensile minimum 241 MPa, modulus 100 000 MPa. Reproduces.
- Not re-fetched: IT grade page, KHK, 3M PTFE (the dossier itself says "not opened" for the last two; they enter only as a 0.9 to 1.0 band and a 13 mg mass), ATI 304.

## 3. Status of each v1 item (v1 section 6)

| v1 item | v2 change | Status |
| --- | --- | --- |
| 1. Mount must exist physically; axial restraint and moment path | Radial screws removed. Two housing ears with countersunk M1.6 screws through the plate. Pull-out on the ears, push-in on the heads | **Not closed.** The ears' attachment to the housing has no declared path (section 4.1 and 6.2). The moment lever is wrong for in-plane bending (ear pair on the z line) |
| 2. Flange smaller than the window; full stack; flushness | Flange 6.3, lip and window 6.45. Stack split into 7 terms. Plate flushness moved out of the stack as a PA12 gap term | **Mostly closed.** The stack reproduces. The nominal geometry is right. The window tolerance and the lip fit at the PA12 corner are not stated (section 6.3) |
| 3. Rear retainer and open stop | 304 retainer collar (r 2.05 to 4.9 x 0.4) behind the gear; stop pin dia 1 at r 5.3 in an arc groove | **Closed on paper.** Both exist as components and are sized (0.81 N; 7.3 N, 9.3 and 14.6 MPa). The collar box overlaps the gear rear face plane at x 28.0 only (touching). The pin and the groove are described but not boxed (inside the cartridge). Stop-to-notch tolerance (+-0.3 deg vs +-7.1) reproduces |
| 4. Walking: bound F_p, or a stop that does not rely on friction | Hirth face pair, zero lash under preload; pilot demoted to an entry guide | **Partly closed.** Under each single declared load the Hirth carries torsion and shear without face friction (ratio 2.53 and 14.5). It rests on a typical F_p and on a phase tolerance that is not derived (section 6.2). The mechanism is a real improvement. The argument "cannot be walked" is not shown at the tolerance corners |
| 5. Contamination treated alike | Oil cases for the flank, release, Hertz. Face friction no longer used | **Closed.** Oil cases are in, and the Hirth removes the face-friction dependence for torsion. Oil on the Hirth flanks only helps separation (friction opposes it) |
| 6. Joint angle, tilt, axial push | Windows stated; joint angles shown not to enter; the axial push is external with stroke and force | **Closed.** Each segment is rigid, so the joint angle does not move the coupler. Tilt 0.73 deg and yaw 1.49 deg are stated and the push is declared external (CPL-006 not claimed) |
| 7. Citations, roll window, mechanism kind | Friction from Wikipedia only; 0.35 withdrawn; roll at the tip radius; `friction_wedge` | **Closed.** All reproduce in raw text (section 2). `mechanism_kind` is `friction_wedge` |
| 8. Load combinations | Each load alone, then all at once | **Closed in form.** Done. The combination result depends on the typical F_p (section 6.2) |
| 9. Supply voltage for release | Release only with the cell at 3.5 V or more; 3.4 V at the motor | **Closed.** 1.62 dry, 1.70 oil. Margin stays above 1.25 down to 2.7 V (reviewer), so the rule is conservative. The DRV8835 drop figure was not checked in this session; it matters little |

## 4. Findings per means

### 4.1 Retention

Principle. The 304 stud lugs bear on the front flank of the C93200 sleeve's 3 deg lock stage. The sleeve cannot turn back under axial load while flank friction exceeds tan 3 deg. The load loop is lug, sleeve land, PTFE ring, lip, Hirth teeth, flange, stud. A 1.0 V motor stall closes it to F_p. Torsion and shear go through the Hirth teeth. Nothing needs power.

Is a friction wedge acceptable as passive retention (CPL-009, Q31 item 6)? CPL-009 says passive when unpowered and evaluated under declared loads. Q31 item 6 asks to distinguish actively maintained from passively locked states and not to assume every state locks. A friction wedge holds with no power and no stored energy, so it is passive in the CPL-009 sense. The source says it is "not absolute" under vibration or shock. The author states this in the mechanism text and in the limitations, and does not claim more. The preload is also set by a one-way stall with no spring to re-tighten, which the declaration says (limitation 3). I accept it as passive retention for the Gate 1 paper standard. Vibration walking is a Gate 2/3 matter. I record that the wedge's margin (1.39 at the inner radius in oil) is real but static.

**Tension (1.220 N, 4 mu W, mu 1).** Carrier: lugs on the self-locking stage. The load goes up the same sense as the preload. Margins 2.86, 1.91 (2.08, 1.39 at the inner radius). The lug stays in the lock stage over the stack (margin 0.118). The teeth stay loaded for tension up to F_p_min (ratio 3.61), and in any case the lugs block axial lift (the teeth can only lose contact force, not separate). Supported. The load path from the sleeve to the shell passes through the lip and then the ears, and the ear link is not shown (section 6.1). So tension is supported inside the coupler and open at the mount.

**Torsion (7.75 mN m).** Carrier: Hirth teeth with zero lash. The preload makes both flanks of each tooth carry load. Torsion adds to one flank and relieves the other. The axial component of the two flanks sums to F_p and does not change until the trailing flank unloads, at T = F_p r_m = 19.6 mN m (ratio 2.53). So the teeth do not need face friction and do not lift. Beyond that point the lugs sit in the slot sides (lash +-0.30 deg minimum) as a second carrier, 1.4 N per lug at r 2.77. The torque is carried at every corner I can find. Supported. The claim "the sleeve cannot be walked" is supported at nominal. At the tolerance corner where the lug slot lash is smaller than the phase error between teeth and slots, the teeth have a one-sided gap and the lug can slide along the 3 deg flank by the remaining lash on each torsion reversal. The author does not derive the phase tolerance (section 6.2). Transverse slip is the mechanism that defeats self-locking. So walking is excluded only if the phase tolerance holds. Unsupported at the corner, not contradicted. The same tolerance matters for whether the teeth reach zero lash at all.

**Shear (0.305 N).** Radial Hirth teeth centre the flange; the separating force is at most shear x tan 45. Ratio 14.5. Supported. Note the in-plane bending also produces coupler shear (14.5 mN m over about 34 mm is about 0.43 N, reviewer). It is still small.

**Out-of-plane bending (14.4 mN m, about y).** Face tipping 27.8 mN m (1.93). The tipping edge is at z, where the ring is intact. Beyond tipping the pilot couple bounds the tilt to 1.49 deg (1.31 with the true engaged length). The lugs lie on the y axis and add nothing for this axis, and the declaration does not say they do. Supported. At the mount the ear pair (lever 7.4) is the right carrier for this axis.

**In-plane bending (14.5 mN m, about z; fault 52.2).** Face tipping 26.2 to 27.0 mN m after the slots are accounted for (1.80 to 1.86, not 1.92). Beyond tipping, the lug pair on the self-locking stage with lever 11.2 (author) as an axial differential load. The lugs are on the y axis, so this axis does use them. Capacity is far above 14.5. Supported inside the coupler. At the mount, there is no ear lever for this axis (section 4.1 item below and 6.2). The load is carried by the lip in the window, with a lever of 0.8 to 1.6 mm. The author's mount figure is wrong for this load.

**Combined (all loads at once, an upper bound).** Axial 3.27 N against F_p_min 4.41 (ratio 1.35 at typical, 0.81 with the offset model, reviewer). Residual clamp 1.14 N, tipping capacity 7.2 mN m against a vector sum of 20.4 mN m. The faces gap at one edge. The author claims retention by the lugs on the self-locking stage and the pilot. I agree this is a valid closed path: the lugs block axial lift; the pilot couple takes the out-of-plane excess (about 7 mN m, 1.4 N at lever 5 mm); the lug pair takes the in-plane excess. The edge gap from the pilot-bounded tilt is at most 0.16 mm at radius 6.3, which is less than the tooth height there (0.4 to 0.55 mm), so the teeth stay partly engaged and roll stays indexed. Supported as retention. Stiffness and roll lash in this state are Gate 2 matters.

**Declared loads reasonable?** Tension at mu 1 (a 4 mu W bound for a chain of five), torsion 2 W x 12.7, out-of-plane W x 47.2 are generous bounds. In-plane equal to the joint drive limit is the actual maximum the unit can apply. The fault case (52.2) is stated as local indentation only. I find the declared loads reasonable and not set low to help the pass. Q31 bending adequacy at high table friction is left unresolved by the author, correctly.

**Release (CPL-008).** The head's own motor reverses the sleeve to the open stop. Need 20.3 mN m (worst), available 32.9 at 3.4 V. The ratio does not depend on the motor constant because F_p and the release torque scale together. This is true when closing and release see the same motor. Preload 9.00 N at the maximum band needs only the single motor ratio. The opposite worst-corner pairing (F_p_max at low friction with release at high friction) is conservative. Ejection reaction goes into the 304 collar (0.81 N); the stop pin takes 7.3 N at the 3.6 V fault stall. Bounded and independent: the tail unit cannot release this joint, and each head releases its own. Supported. The release does need the stop pin and the arc groove to be built into the lip and sleeve, and neither is boxed (they are inside the cartridge box, which is acceptable).

**The mount (does it exist physically?).** The ears are on the declared parts list and have boxes. The plate has a window (y -3.15 to 9.75, z -5.45 to 7.45) and the ear boxes (z 7.45 to 9.35 and -7.35 to -5.45) lie exactly behind the plate pieces `L-front-hi` and `L-front-lo`, so the bearing of the ears on the plate inner face (x 34.4) and the countersunk screws through a 1.2 mm plate are geometrically consistent. What is missing is the housing side. The ear is declared "one part with" the housing, but the housing in the declared geometry has material only at radius 2.05 to 3.5 (tube) and in the lip (radius to 6.45, x 34.8 to 35.6). The sleeve (r 3.55 to 6.3) fills the annulus around the tube from about x 28.4 to 34.5, and it rotates over 122 deg, so no arm can pass through it. The ear (x 32.8 to 34.4, r 6.45 to 8.35) is therefore joined to nothing in the declared boxes. A join would need a skirt in the 0.15 mm gap at radius 6.3 to 6.45, or a recess in the 1.2 mm plate for an arm at x 34.4 to 34.8 (the plate pieces are declared as full slabs). The author's own phrase "behind the front plate" and the assembly statement (cartridge inserted from inside, ears bearing on the inner face) do not show how the lip, 0.4 mm in front of the ears, is tied to them. This is the same class of defect as v1 item 1: a mount described in words that the geometry does not yet support. A small design change would fix it (for example a rear housing flange behind the sleeve gear carrying the ears, with the retainer collar), so I class it as unsupported and not as a contradiction.

### 4.2 Alignment means

**(a) Lateral: chamfers 0.6 on the bore mouth and 0.5 on the pilot nose into the 4.10 bore.** Principle: a 45 deg chamfer under an axial push gives a centring component (1 - mu) / (1 + mu) of the push, positive while mu below 1 (0.111 at 0.8, reproduces, with the generic steel-steel static 0.8 as the upper bound from the ToolBox page). Window: nose r 1.5 enters mouth r 2.65 by 1.15 mm lateral, against the +-0.6 mm stack of two PA12 features at +-0.3. Margin 1.9. Unpowered, geometric, in 304. Supported. The 0.130 used as lateral error at the lugs is a diametral clearance, so the true radial error is 0.065 mm, which is conservative.

**(b) Roll, pitch, yaw: round lugs in 0.6 x 45 deg V lead-ins, then the 36-tooth Hirth faces.**
- Roll window +-5.5 deg at the lug tip radius 6.2 against about +-1.4 deg from table flatness: 3.9 times. Reproduces. Supported.
- Pitch +-0.73 deg from flatness: the pilot bore (clearance 0.13 diametral over 5.7 mm engaged gives 1.31 deg) and the teeth take it. Supported.
- Yaw: bounded to 1.31 to 1.49 deg by the pilot. Joint angles do not enter (each segment is rigid). Supported.
- Pilot before lug: 0.600 deep when the lug front reaches the lip, equal to the chamfer. Margin zero at nominal and -0.015 at a lug-axis corner. The lug then sees the clearance plus 0.015 mm, small against +-0.6 mm. Not a blocked guide, but the asserted margin is not a margin.
- The guide must not be blocked at a declared corner. Two details I could not close from the declaration: (i) the PTFE ring (r 3.6 to 4.4, x depth 0.8 to 1.1) lies in the lug's path, because the lug front is at depth 0.9 at the start of the capture stage (axis 2.4, radius 1.5). A continuous ring blocks it. The ring must carry a notch at the lug azimuth, and none is declared. (ii) Lug slots in the lip and V lead-ins cut the Hirth ring (section 6.4). Neither is a contradiction. Both are missing detail in a part the declaration describes.
- Tooth phase to slot phase is the one alignment item that couples to retention (section 6.2).

**(c) Axial closing and seating.** The 20 deg capture stage draws 1.0 mm. Closing 9.68 to 10.75 mN m against 1.21 mN m needed to drag one free unit at mu 1. The 3 deg stage seats the Hirth faces. Tolerance is taken by sleeve travel to a stall: the seat spans 3.518 to 3.681 inside the lock stage 3.40 to 3.80. The author is right that the stall seats the faces wherever they meet. The stack reproduces. One aspect is not shown: the stall happens at the motor's torque limit with no sensor, so over-travel past the lock stage is stopped by the pin only at 122.0 deg, and the lock stage ends at 122.0 deg too. The lug at the end of the lock stage with no further flank is then held by the stop, not by friction. This only occurs if the faces fail to seat. It is a fault case. Supported at the declared corners.

**Axial push to reach the capture stage.** External: 2.40 mm stroke, about 0.31 N plus chamfer friction. The declaration says it comes from the Q31 start configuration or a later approach design, and claims no capture window (CPL-006). Accepted for Gate 1 (no capture claim). It is not a pre-alignment force the candidate supplies, which the author states.

### 4.3 Magnetism

No magnet component. `mechanism_kind` is `friction_wedge`. No alignment has `kind` `magnetic`. The summary says "no magnet". Not applicable. Passes.

### 4.4 Automated checks 1 to 5

1. `retention.requires_power_to_hold` is `false`. Pass. The mechanism holds with the motor off (self-locking), and I find no powered holding element.
2. `retention.release.bounded_independent_release` is `true`, `release.means` is nonempty and physical. Pass.
3. `retention.mechanism` and all three `alignment[].justification` are nonempty. `component_ids` are `head-cartridge`, `tail-stud`, `retainer-collar`, `cartridge-ear-up`, `cartridge-ear-low`, which exist. Pass.
4. No magnet. Pass (not applicable).
5. Each alignment names components that exist: (`tail-stud`, `head-cartridge`), (`tail-stud`, `head-cartridge`), (`head-cartridge`, `coupler-motor`, `coupler-pinion`, `tail-stud`). Pass.

## 5. Errors found

1. **In-plane bending routed through the ear pair.** `coupler.py` section 11 takes `M_mount = max(M_OOP, M_INPLANE)` and divides by 2 x 7.4. The ears are on the z line (axis y, z offsets +-7.4). They give lever 7.4 to a moment about y, and none to the in-plane moment about z. The declaration's "worst screw load 1.59 N, 0.26 MPa on PA12" is true for out-of-plane bending only. For in-plane bending the load is the lip-window couple, 9 to 18 N (fault 33 to 65 N) with 31 to 44 MPa line contact on PA12 (my assumed E 1.7 GPa, not a cited value). That is below PA12 yield on paper at the drive limit and above it at the fault.
2. **Lash radius.** The roll lash is quoted at r 2.77 (+-0.38 deg). The lug is a cylinder, so the slot contacts at the tube outer radius 3.5 first. Lash +-0.30 deg (reviewer). Small, but it is the binding value for the phase comparison.
3. **Tipping for in-plane bending ignores the slots.** 27.8 mN m uses the full ring edge at 6.3. The slots cut the outer teeth at +-y. Reviewer 26.2 to 27.0 mN m, ratio 1.80 to 1.86 (declared 1.92). Not blocking.
4. **Hirth flank pressure.** 0.9 MPa uses 72 flanks. The slots remove 22 to 61 percent of the ring by radius, so the real number of flanks is roughly 45 to 55. About 1.2 to 1.4 MPa (reviewer). Not blocking. The "provisional 0.05 mm band" is not sourced.
5. **Pilot clearance mixing.** 0.050 (radial nominal) and 0.130 (diametral maximum) are quoted as one band. The tilt formula uses the diametral value correctly. The lateral error at the lugs uses it as radial, which is conservative by a factor of 2.
6. **Hertz onset.** 225 MPa (oiled) is 2 percent under the 230 rule of thumb. The author states it. Not a contradiction.
7. **Dossier wording.** The dossier table says "Torsion ... separating force ... stays below F_p_min". True, and the equivalent statement is the trailing flank unloading point. The word "separation" is used for the teeth although the lugs prevent axial lift. This is a wording point.

I found no arithmetic error in the cam layout, the stack, self-locking, preload, release, Hertz, stop pin, or window numbers.

## 6. Classification of weaknesses

### 6.1 Contradiction (a claim defeated by the declaration's own numbers or by physics)

None that defeats a retention or alignment requirement. The nearest is error 1 (the in-plane lever at the ears). The load keeps a carrier (lip and screw shanks in the PA12 plate, at a lever of 0.8 to 1.6 mm), so no declared load is without a carrier. The statement of 1.59 N is wrong for that load, but the wrong number is not what retains the coupler. If a later version keeps the ears on the z line and claims the 1.59 N as the in-plane mount load, I would treat that as a contradiction.

### 6.2 Unsupported (blocks `pass`)

1. The ear to housing connection (section 4.1, mount). The ears carry every axial and moment load into the shell and have no shown connection.
2. The mount for the in-plane bending (error 1) is not sized with the right lever, and the PA12 bearing is near its strength at the drive limit.
3. The tooth phase to lug slot tolerance, "about +-0.2 deg", has no derivation. It decides whether the Hirth teeth reach zero lash with the lugs clear of the slot sides, and so whether "the lugs never slide" holds at the corners. The phase tolerance for two parts, +-0.4 deg sum or 0.28 RSS, equals or exceeds the minimum lash +-0.30 deg.
4. The preload F_p_min = 4.41 N rests on a linear stall model from a typical datasheet value. The datasheet gives no lower bound and a 0.5 V start voltage. The single-load ratios survive a 40 percent loss (torsion 1.52, tension 2.17). The combined teeth ratio does not (0.81). The author says the ratios depend on F_p, so this is stated, but no bound is given.
5. The PTFE ring has no lug notch, and the lip slots and V lead-ins are not accounted for in the Hirth face areas.
6. The window and lip are both r 6.45 and the PA12 tolerance is +-0.3. The fit of the lip in the window and the claim "flange smaller than the window" are shown at nominal only. The window tolerance is not declared.
7. Pilot before lug: margin zero.

### 6.3 Gate 2/3 matters (do not block a paper pass)

- Vibration and shock back-driving of the friction wedge ("not absolute", declared).
- PTFE ring creep and thermal change of F_p, with no re-tightening (declared).
- Galling of 304 on 304 teeth, pilot and bore (declared).
- Fine machining of a 36-tooth ring 0.39 mm high (declared). Hirth flank contact band.
- Capture sweeps and the approach locomotion (declared external, no capture window claimed).
- Stiffness loss and roll lash after faces gap under the combined case.
- Motor stall variation and temperature (the bound itself is item 6.2.4).
- Q31 bending adequacy at high table friction (declared unresolved).

## 7. What a further version would need

1. Show the ears joined to the housing: a drawn or described housing flange (for example behind the sleeve gear, with the retainer collar), or a skirt, or a plate recess, with the dimensions inside the declared boxes, and the load path from lip to ears to plate stated.
2. Separate the ears in y (or add a second bearing in x) so that in-plane bending has a lever, or size the lip-in-window couple with a stated lever, a cited PA12 bearing strength, and the fault case.
3. State the window tolerance and the lip fit, and show the flange clear of the plate at the PA12 corner.
4. Derive the tooth phase to slot tolerance (one set-up or not, by process), compare it with the lash at radius 3.5, and show the lugs clear of the slot sides when the teeth are seated, or state which carrier takes torsion in each direction and that no sliding is possible.
5. Bound F_p from below (a cited lower bound on motor torque at 1.0 V including the start voltage, or a sensed or mechanically limited closing) and re-state the combination ratio.
6. Declare the PTFE ring's lug notch, and account for the lip slots in the Hirth areas and the in-plane tipping lever.
7. Give the pilot-before-lug sequence a real margin (a longer pilot or a shorter bore chamfer).

None of these needs more volume (the stowed margin is 1.14 mm and the coupler stays inside it).

## 8. Basis of the outcome

Under protocol section 8 and Q062, `pass` needs retention under every declared load and every alignment means to be physically justified on paper. Inside the coupler it is: tension, torsion, shear and both bendings each have a closed carrier in machined metal, the friction wedge is self-locking with margin at the cited lower bounds, release is bounded and independent, and the alignment windows exceed the declared PA12 stack. The mount that ties the coupler to the shell is not shown to exist (ear connection) and is mis-sized for the in-plane moment. The no-slide argument for the sleeve rests on an underived phase tolerance. A load path that cannot be traced from the cartridge to the shell leaves tension, shear and bending without a complete carrier, so I cannot record `pass`.

`fail` needs a claim contradicted by the declaration's own numbers or by physics in a way that defeats a retention or alignment requirement. I looked for it and did not find it: no declared load is left without any carrier, no guide is shown blocked at a declared corner, and the one wrong lever (error 1) sits on a load with a plausible carrier. I would change this to `fail` if the author keeps the ears as declared and claims the in-plane mount load as 1.59 N, or if a later reading shows no way to connect the ears to the housing inside the 0.15 mm annulus and the plate thickness while keeping the sleeve, the collar and the window as declared.

The correct label is `unresolved`. This record is a paper judgement only, label `exploratory`, and says nothing about whether the mechanism works.
