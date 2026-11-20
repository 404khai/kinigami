candidate_id: cand-d
candidate_version: 1
author: Claude Opus 5.5 (engineering lead, cand-d author)
reviewer: reviewer-d1-retention (Claude Sonnet 5.5, independent session, no authorship in cand-d)
outcome: unresolved

# Retention and pre-alignment review: cand-d v1, r1

Date: 2026-11-20.

Declaration `candidates/cand-d/declaration.json`, SHA-256 `4b6788a544f6a4226d7bcf0e8951fbf789e44b6c67cbf2ae2eb312ff31bbf64a`. I computed it with `shasum -a 256` and it equals the hash in `dossier.md`. Every figure marked "reviewer" is my own computation (python3, script kept outside the repo). I did not use the author's scripts for those figures. I did run the author's `coupler.py`, `joint.py` and `gen_declaration.py` and they reproduce the dossier numbers.

Files read: `AGENTS.md`; `docs/validation/gate1-v1-protocol.md` (all, section 8 in detail); `criteria/gates/gate1-v1.json` (item G6); `docs/decisions/Q062`, `Q031` (item 6), `Q036`, `Q085`; `docs/requirements/requirements.md` rows CPL-001..CPL-011; `candidates/cand-d/declaration.json` (summary, retention, release, alignment, limitations, assembly_access, chain, sites, geometry primitives, and the components head-cartridge, tail-stud, coupler-motor, coupler-pinion, joint-sector, hinge-plate-low, hinge-ear-low, hinge-pin, front-wall parts, fasteners, cell, driver); `candidates/cand-d/dossier.md` (all); `candidates/cand-d/scripts/` (`README.md`, `coupler.py`, `joint.py`, `gen_declaration.py`, `declaration_text.py`); `candidates/cand-a/retention-review-v5-r1.md` and `retention-review-v4-r1.md` (calibration only). Sources fetched again: Engineering ToolBox friction page, Wikipedia Leadscrew, Precision Microdrives 206-109 datasheet (PDF text), Concast C93200 page.

This is a paper judgement under protocol section 8. It is not a test of the mechanism (Gate 2/3).

## 1. Judgement in brief

The core idea is sound on paper. A 3 deg lock stage on a bronze cam sleeve holds two 304 lugs. The friction needed for self-locking (0.0524) is below every cited dry and oiled friction value (margins 2.86 and 1.91 at the cited minima). Tension (1.186 N declared) is carried geometrically by the lugs on the self-locking flank. That claim is supported. The torsion, bending and shear carriers are also named, each with a geometric fall-back (housing slot sides, pilot in bore, lug pair), and their arithmetic reproduces.

I do not record `pass`, because five things are not supported or are wrong as declared:

1. **Cartridge mount (declaration contradicts itself).** The head cartridge is "fixed by two radial M1.6 screws through the PA12 into its lip". The lip is 0.8 mm thick. An M1.6 x 0.35 thread has a minor diameter of about 1.17 mm (reviewer), which is larger than the lip. The fixing cannot be made as stated. This fixing and the 0.8 mm lip bearing in the 1.2 mm PA12 window are the only declared link from the cartridge to the head shell. Every external load on the head side runs through it.
2. **The "no slip" argument is carried by one corner.** The torsion carrier that the author says prevents a sleeve from being walked loose is dry face friction, ratio 1.30 at F_p_min. That ratio holds only for a typical-value motor, a clean dry 304 face, a uniform pressure distribution, the torsion load alone, and a full-supply voltage. It falls to 1.0 or below at several corners the author did not close (section 3.2). The author's own limitation says a greased face slips above 3.1 mN m, against a declared 7.53 mN m, and that slip can walk the sleeve. The oil case is accepted for the flank (self-locking, preload, release, Hertz) but not for the face.
3. **Seat and tolerance stack incomplete.** The stack of +-0.068 mm omits the plate-to-lip flushness. The flange (r 6.5) is larger than the lip and the window (r 6.45), so at a corner the flange bears on four PA12 slivers instead of the lip.
4. **Parts not declared that the cycle needs.** There is no rear axial stop for the sleeve (the release ejection reaction goes rearward), and no open hard stop (release drives "to the open hard stop").
5. **Pre-alignment** (lateral window, roll window and sequence) is geometrically adequate against the declared PA12 stack. But the stack leaves out the joint angle error (no joint sensor), tilt is claimed and not quantified, and the force that drives the centring (an axial push) has no declared source. Capture windows are rightly not claimed (CPL-006).

I record `unresolved`, not `fail`. The one hard numeric contradiction (item 1) sits in a fixing the declaration itself lists as unsized (limitations) and in `assembly_access`, which G2 checks for presence only. It does not contradict a retention requirement. The retention loads (tension, torsion, both bendings, shear) each keep a geometric carrier inside the declared numbers. The other items are missing or unbounded, not contradicted. I list in section 6 what would turn this into a `fail`. A pass needs a new version.

## 2. Independent recomputation

| Item | Author | Reviewer |
| --- | --- | --- |
| Capture / lock arc, slot end, web | 33.3 / 92.6 deg; end 144.1; web 10.5 deg, 0.86 mm | 33.32 / 92.55 deg; end 144.06; web 10.48 deg = 0.65 mm at r 3.55, 0.86 at Rc 4.725, 1.10 at 6.0; seat rotation 79.6 deg |
| Axial stack at seat (4 terms) | +-0.068; seat 3.532..3.668; margin 0.132 | same; margin 0.132 per side. Splitting the lumped 2.8 mm into PTFE ring (+-0.02) and sleeve front-to-flank (+-0.02) gives +-0.108 and margin 0.092. With the front plate proud of the lip by up to PA12 +-0.3, the corner is outside the lock stage (section 3.3) |
| Self-locking, tan 3 deg = 0.0524 | 2.86 dry (0.15), 1.91 oil (0.10) | 2.86, 1.91. If the flank is a constant-pitch helicoid, the lead angle at the inner contact radius 3.55 is 3.99 deg (tan 0.0697): margins 2.15 and 1.43 |
| Closing preload F_p, 1.2 V, flank 0.35/0.15, thrust 0.20/0.05, eta 0.9/1.0 | 4.24 .. 11.08 N | 4.24 .. 11.08 N. With flank <= 0.23 (the only dry values on the Wikipedia page): F_p_min 5.40 N |
| F_p_min at 0.77 x the typical motor constant | "23 percent weaker gives ratio 1.0" | 3.27 N, ratio 1.0. At 0.70 x: 2.97 N |
| Stall torque at 1.2 V | 3.60 mN m (linear in V) | 3.60 if linear. The datasheet gives max start voltage 0.5 V. A model with constant output friction (reviewer, illustrative: T = 3.6 V - 1.8 mN m) gives 2.52 mN m at 1.2 V and 11.16 at 3.6 V. F_p_min then 2.97 N |
| Release need, worst corner (F_p_max + 1.186 N, flank 0.35, thrust 0.20) | 26.8 mN m | 26.76 mN m |
| Release available, 3.6 V stall, eta 0.9 | 34.8 (ratio 1.30) | 34.83. At 3.3 V: 31.9 (1.19). At 3.0 V: 29.0 (1.08). At 2.7 V: 26.1 (0.98) |
| Release need if closing and release use the same friction state | not given | 8.1 / 10.8 / 12.9 mN m at flank 0.15 / 0.25 / 0.35. Far below the worst-corner figure |
| Torsion 2 W x 12.7 | 7.53 mN m | 7.534 mN m (W 0.2966 N) |
| Torsion no-slip, 0.5 x 4.24 x 4.62 | 9.79 (1.30) | 9.80 (1.30). With r_eff 4.4 / 4.0 / 3.6: 1.24 / 1.13 / 1.01. With tension 1.186 N present at the same time (F 3.06 N): 7.06, ratio 0.94. With face mu 0.4: 1.04. Greased 0.16: 3.14 mN m. Light oil 0.23: 4.51 mN m |
| r_eff, uniform pressure | 4.62 (r 2.0..6.45) | 4.62; 4.80 if the 0.6 mm bore chamfer is removed from the contact (r 2.6..6.45). The assumption of uniform pressure is not supported (section 3.2) |
| Face decompression start (kern) | not given | kern radius 1.87 mm: first opening at 7.95 mN m at F_p_min. Declared out-of-plane 14.0 and in-plane 14.5 exceed it. Tipping to the edge 27.36 (1.95x, 1.89x) reproduces |
| Torsion at slot side, Hertz | not given | lug on housing slot: 1.37 N per lug, p0 143 MPa (304 yield 205) |
| Hertz p0 lug on flank, F_p_max + tension | 202 / 222 (with drive-limit bending) / 268 fault; onset about 230 | 201.9 / 222.2 / 268.0. E* 73.6 GPa reproduces. Oil case (F_p 13.96 N): 224 / 243. The 222 case is 3.5 percent under the onset |
| Roll window | +-7.3 deg | 7.28 deg at the mean radius 4.7. At the lug tip r 5.9 (binding): 5.81 deg |
| Pilot-before-lug margin | 0.60 vs 0.60 (margin 0 at nominal) | 0.000 at nominal. With the lug axis at +0.028 (IT10 + g6 terms): -0.028 |
| Chamfer centring ratio (1-mu)/(1+mu), mu 0.8 | 0.11 | 0.111 |
| Joint outline contact, 2 atan(1.8/12.7) | +-16.13 deg | 16.13 deg. Working +-15 deg leaves 1.13 deg |
| M1.6 minor diameter vs lip | not compared | 1.17 mm vs lip 0.8 mm |
| Sleeve web bending at stall release (reviewer, land tangential force 2.64 N per lug, lever 3.9 mm) | not given | 34 MPa (w 0.86) .. 60 MPa (w 0.65) against C93200 yield 138 |
| Stiffness of the preload loop (reviewer; PTFE E about 0.5 GPa and alpha about 1e-4 per K are my general values, not cited in the declaration) | not given | ring 33 N per um. F_p of 11 N is 0.33 um of compression. 1 K of PTFE temperature change moves F_p by about 1 N. Order of magnitude only |

Source checks (my fetches, 2026-11-20):
- Wikipedia Leadscrew: steel on bronze dry 0.15 to 0.23, machine oil 0.10 to 0.16; the page states that self-locking is not absolute under vibration or shock. Reproduces.
- Engineering ToolBox: "Steel - Steel, clean and dry 0.5 to 0.8"; "Bronze - Steel, grease 0.16"; "PTFE - Steel 0.05 to 0.2". **It has no "bronze on steel dry static 0.35" row.** The only other bronze rows are bronze - cast iron clean and dry 0.22 and bronze, sintered - steel grease 0.13. The steel-steel row is generic, not stainless on stainless. The cited dry flank band 0.15 to 0.35 is therefore only partly sourced.
- 206-109 datasheet: rated 3 V, 3 mN m, max 3.6 V, typical stall torque 9 mN m, typical start current 185 mA, max start current 230 mA, max start voltage 0.5 V, resistance 14.5 ohm, ratio 136, peak efficiency 26 percent. All values are "typical" except as stated. There is no lower bound on torque.
- C93200: density 8.91, yield 138 MPa (minimum, 0.5 percent extension), E 100 GPa. Reproduces.

## 3. Findings per means

### 3.1 Retention against tension (declared 4 mu W = 1.186 N, mu = 1)

Principle: two 304 lugs (dia 3.0 g6, to r 5.9) bear on the front flank of the helical slots of a C93200 sleeve. The sleeve cannot rotate under lug load because flank friction exceeds tan 3 deg. The load goes lug, flank, sleeve land, PTFE ring, lip, housing.

Check: the load direction is correct. Tension pulls the stud outward. The front flank (toward the lip) stops the lug and pushes the sleeve forward onto the PTFE ring. The unwinding torque from axial load F is F Rc tan 3 deg and the friction torque is F Rc mu. At the cited minima the ratio is 2.86 dry and 1.91 oiled (reviewer: same). The lug stays on the lock stage over the stack (margin 0.132 mm per side, section 3.3). The tension is a fraction of the preload (4.24 N min), so the lug stays loaded in the same sense. Static retention against 1.186 N is **supported on paper** (this is the strongest part of the design).

Limits that are not blocking by themselves:
- Self-locking is friction-based and static. Vibration, shock and the dynamic friction drop are not covered. Gate 2/3 matter, and the author states it.
- `retention.mechanism_kind` is `geometric_interlock`. The author's own text says the lug is held only while friction prevents the sleeve from turning, which is a friction wedge. The label is wrong (protocol lists `friction_wedge`). No automated check uses it, but the record should not call this geometric.
- Preload persistence: the loop (metal, bronze, PTFE) is stiff. F_p of 4 to 11 N is below 1 um of compression (reviewer). Settling, creep of the PTFE ring or a few kelvin of PTFE temperature change can remove it, and an unpowered sleeve with no spring cannot re-tighten. So F_p_min is an initial value, not a held value. Tension retention does not depend on it. The face-friction and tipping margins in 3.2 and 3.4 do.

### 3.2 Torsion about the axis (declared 7.53 mN m)

Declared carriers: (1) no slip by dry 304 face friction (9.79 mN m, 1.30x); (2) beyond slip, the lugs on the sides of the 304 housing slots (r 2.75, lash 0.39 to 0.76 deg each way, 1.37 N per lug, p0 143 MPa). Carrier (2) is geometric, closed in 304, and its arithmetic reproduces. The torque is therefore carried in every case. This part is supported.

The open point is the author's own reason for carrier (1): if the lugs slide on the 3 deg flank under cyclic torsion, the sleeve can be walked in the release direction (the transverse-slip loosening mechanism). I agree the mechanism is real. With slip, the friction on the flank pushes the sleeve at F_p x Rc x (mu + tan 3 deg) = 0.96 to 1.90 mm x F_p, in the loosening direction. The thrust (PTFE) resistance is only 0.20 to 0.80 mm x F_p (reviewer). The gear train hold is not credited and not quantified (no back-drive torque in the datasheet). So walking is possible once the face slips. The paper must therefore show no slip, or show another stop to walking. It shows no slip at one corner only:
- **Motor constant.** F_p is set by a voltage-limited stall of a motor whose datasheet gives typical stall torque only. The author says 23 percent weaker gives 1.0. The datasheet max start voltage of 0.5 V alone allows a constant friction loss that would put T(1.2 V) near 2.5 mN m instead of 3.6 (reviewer model, illustrative). There is no lower bound from the datasheet, and temperature (winding resistance) and supply voltage are not bounded. The author describes the band "4.24 to 11.08 N" as covering "all cited corners", but the motor corner is not in it.
- **Face friction.** 0.5 comes from a generic "steel on steel clean and dry" row. At 0.4 the ratio is 1.04. At 0.3 it is 0.78. Greased or light-oil faces (0.16, 0.23) slip at 3.1 and 4.5 mN m. The same oil contamination is accepted for the flank, so it is not out of the envelope.
- **Contact radius.** The 4.62 mm assumes uniform pressure over r 2.0 to 6.45. The lip is supported at the rear only by the PTFE ring (r 3.6 to 4.4), and the lip is 0.8 mm thick. The pressure is likely concentrated near the ring. At r_eff 4.0 the ratio is 1.13. At 3.6 it is 1.01 (reviewer). The author's own value of 4.62 also ignores the 0.6 mm bore chamfer and the two lip slots.
- **Load combination.** With the declared tension acting at the same time, the clamp falls to F_p_min - 1.186 N and the ratio is 0.94. The declaration does not say the loads are exclusive. Tension 4 mu W (chain dragged) and a tipping neighbour can coexist on a tabletop chain.

Assessment: torsion retention (the load itself) has a geometric carrier. The claim that the sleeve cannot be walked loose under that torsion is **unsupported across the declared corners**, and the author's own limitation concedes slip with a greased face. It is not contradicted at the declared dry nominal corner, so I class it as unsupported, not as a contradiction.

Declared load reasonableness: 2 W x 12.7 (two neighbours each tipping on a bottom edge) is a plausible Q31 tabletop torsion bound and its arithmetic is right.

### 3.3 Axial tolerance stack and the lock stage

Principle: the sleeve turns to a motor stall, so the seat lands wherever the flange meets the lip. It must land in the lock stage (lug-axis depth 3.40 to 3.80, nominal 3.60).

Check: the four-term stack (IT10 / g6 values from Wikipedia IT Grade) reproduces: +-0.068, margin 0.132 each side. Missing terms:
- The lumped 2.8 mm "lip rear to flank" dimension contains the PTFE ring thickness, the sleeve front-to-flank dimension and the slot position. Each should be its own term (reviewer split: +-0.108, margin 0.092). That is still inside the stage.
- **The flange is r 6.5 and the lip and the front-plate window are r 6.45.** The window in the front wall is y -3.15 to 9.75, z -5.45 to 7.45 (declared wall pieces), a square of half-side 6.45 around the axis. A circle of r 6.5 stands 0.05 mm outside that square at the middle of each side. There the flange touches the PA12 plate at four small slivers. The declaration calls the cartridge face "flush" with the plate, but the cartridge position along x is set by PA12 features (screws and window), and the declaration itself quotes +-0.3 mm for PA12 outer features. If the plate stands proud of the lip by more than 0.132 mm, the flange stops on PA12 and the lugs stop in the 20 deg capture stage (not self-locking). If it stands proud by less, the PA12 slivers share the preload at a micrometre scale. Either way the claim "the preload loop is all machined metal; PA12 carries only mounting" is not true at that corner. This corner is not in the stack.
- Flange and lip flatness, perpendicularity of the lug axis and tilt are not in the stack (small, but absent).
- The sleeve is a bronze tube with two long helical slots. The land that carries the lug load hangs on the web of 10.5 deg (0.65 to 1.10 mm wide). My estimate of the web bending at stall release is 34 to 60 MPa against yield 138. It is adequate on paper but nobody analysed it.

Assessment: **unsupported** (stack incomplete, with a concrete corner the declared dimensions make possible).

### 3.4 Out-of-plane bending (declared 14.0 mN m, W x 47.2)

Principle: the flange is held on the lip by F_p. Beyond opening, the H7/g6 pilot bears against the bore as a couple (arm about 5 mm; the force is about 2.8 N and the pressure is below 1 MPa over the 4 mm bore).

Check: tipping about the edge needs F_p_min x 6.45 = 27.4 mN m (1.95x, reproduces). But the face starts to open at the kern radius 1.87 mm: 7.95 mN m (reviewer), so at the declared 14.0 the face is partly open and the friction carrier in 3.2 is reduced at the same time. The pilot couple is the real carrier above 8 mN m. It is a geometric carrier in 304 and is adequate by size. The lugs lie on the y axis, so they add nothing for this bending axis (correct, and the author does not claim it). The load is also a bound: the neighbour's CoM is about half the pitch from the coupler, so W x 47.2 is conservative.

The head-side reaction runs through the cartridge: the cartridge is held at one plane only (the 0.8 mm lip in the 1.2 mm window). The couple has a lever of about 1 mm, so the PA12 window edge sees about 14 N (reviewer), about 4 MPa on 0.8 mm x 4 mm. This is within PA12 on paper, but the dossier gives no such figure ("not sized beyond bearing pressure").

Assessment: carrier is supported; the mount (section 3.8) is not.

### 3.5 In-plane bending (declared 14.5 mN m = joint drive limit; fault 52.2)

Principle: lug pair as differential axial load on the self-locking stage, plus face edge.

Check: the arithmetic reproduces (14.5 = 3 x 58/12; 52.2 = 9 x 3.6/3 x 58/12). The lug lever is Rc + 6.45 = 11.2 mm, so 14.5 mN m is 1.3 N differential per lug and the fault case 4.67 N. All are tiny against 304. Both lugs can be loaded because the face edge reacts on the other side. The lug contact reaches Hertz 222 MPa at the drive limit (under the 230 onset by 3.5 percent) and 268 at fault (local indentation, which the author admits). The author is right that no separation occurs.

Reasonableness: the declared load is the joint's own drive limit. The dossier states the Q31 push needs 8.7 mN m at mu 0.3 and about 29 at mu 1. So the chain may need a joint torque above the declared load, and the declaration would then not cover it. This is a scope statement of Q31 adequacy, which the author marks unresolved. It does not contradict G6.

Assessment: supported at the declared load.

### 3.6 Shear (declared W = 0.297 N)

Pilot in bore (geometric) plus face friction 2.12 N. Supported, with margin 7.1. Note the joint can produce coupler shear up to about 0.43 N (reviewer: 14.5 mN m over the 34 mm lever). That is above W and still tiny for a 4 mm pilot in 304. Not blocking.

### 3.7 Release (CPL-008, bounded independent release)

The head unit's own motor turns the sleeve back. Torque balance reproduces (26.76 needed, 34.83 available at 3.6 V stall, eta 0.9, ratio 1.30). Two points:
- The worst corner joins F_p_max at the lowest friction with release at the highest friction. That is conservative. With one friction state for closing and release, the need is only 8 to 13 mN m (reviewer), far below 34.8.
- The 3.6 V is the datasheet maximum. The declared cell is 3.7 V nominal 1S, and the driver drop is not stated. At 3.0 V the margin is 1.08, and at 2.7 V it is 0.98 (reviewer, worst friction corner only). The author's "margin 1.30" holds only at the top of the discharge. It is not a retention failure (release may be slow or blocked, CPL-008), but the figure is not bounded over supply voltage.
- The release ejection (the outer flank pushes the stud out by 1.4 mm) pushes the sleeve rearward. **No rear stop for the sleeve is declared** (the cartridge is housing, sleeve, PTFE ring, and the housing volume has no rear shoulder). In the layout the motor can face (x 28.0) is adjacent to the sleeve gear ring rear face (x 28.0), but it is not declared as a stop, and a thrust there adds friction that is not in the torque budget. Without a stop, the stud is not ejected and the sleeve is not retained at assembly either. Release itself (sleeve back to open, stud free) does not need the ejection.
- The "open hard stop at the entry notch" is not declared as a part or as geometry. The controller has no position sensor (limitation), so the open position has an unbounded angular tolerance. The entry window in sleeve angle is about +-7.3 deg at Rc (notch half-width 2.1 mm vs lug 1.5 mm; reviewer). The dossier does not show the stop meets this.

Assessment: release is plausible and bounded in torque, but the stop and the rear retainer are missing parts. Unsupported.

### 3.8 Mounting of the cartridge and of the stud (load path into the shells)

- Head: "two radial M1.6 screws through the PA12 into its lip". Lip 0.8 mm; M1.6 minor diameter 1.17 mm (reviewer). This cannot be made as stated. The only other restraint is the lip as a 0.8 mm thick edge in the window (no shoulder in the declared parts), so axial retention of the cartridge against stud pull-out and against the entry push is not shown. The loads are small (tension 1.186 N, bearing about 14 N for the bending couple), so a thickened lip or a boss would very likely solve it. As declared it is a contradiction by the declaration's own numbers.
- Tail: the flange (r 6.5 x 1.0) is screwed to the 1.2 mm PA12 end plate with 2 x M1.6. The loads are small (7.5 mN m gives 0.8 N per screw at r about 4.5, reviewer). PA12 pull-out is not cited (limitation). Not blocking.

Assessment: head mount **contradicted as declared** (fixable), tail mount unsupported but benign.

### 3.9 Alignment means

**(a) Lateral and tilt: 45 deg chamfers on the pilot nose (0.5) and the bore mouth (0.6).**
- Principle: an axial push gives a centring force of (1-mu)/(1+mu) of the push (reproduces: 0.111 at mu 0.8, positive while mu < 1).
- Window: the nose tip r 1.5 enters the mouth r 2.6 up to 1.10 mm lateral. The declared stack is +-0.6 mm (two PA12 features of +-0.3 each). The window is larger than the stack. Supported.
- Not covered: (i) tilt is in the title but only lateral is computed; (ii) joint angle error: the joint has no sensor and no unpowered hold, and the coupler is 34 mm from the pin, so each 1 deg of joint error moves the coupler 0.6 mm (reviewer), which uses the 0.5 mm margin by itself; (iii) the force: the push has no declared source, since approach locomotion is not designed. The centring needs a push of about 9 x (table drag) at mu 0.8; for a 0.3 N unit at table mu 0.3 that is about 0.8 N (reviewer). This is a Gate 2/3 matter (no capture window is claimed) but the means is declared as "physically justified".
- Assessment: geometry supported against the declared stack; unsupported for tilt and joint error.

**(b) Roll: round lugs in 0.6 x 45 deg V lead-ins.**
- Principle and window: the declared +-7.3 deg is taken at the mean radius 4.7. The binding point is the lug tip (r 5.9), where the V lead-in depth 0.6 gives 5.8 deg (reviewer). The stack is about +-1.4 deg (0.6 mm over 25 mm). The window is still four times the stack. Supported at the corrected value.
- The V lead-in alone is +-0.625 mm lateral, which is not more than the +-0.6 stack, so the pilot must centre the unit first.

**(c) Pilot before lug.**
- The pilot cylinder is 0.60 mm into the bore when the lug front reaches the lip, and the bore chamfer ends at 0.60: a margin of exactly zero at nominal, and -0.028 mm if the lug axis is at +0.028 (reviewer). The physical effect of that corner is small: the lug then sees at most the pilot clearance plus 0.03 mm (about 0.05 mm), against a 0.6 mm V lead-in. So the claim "lugs meet their slots within 0.024 mm" is stated more sharply than the geometry can guarantee, but it is not a blocked guide. Supported physically; the stated assert is not a margin.

**(d) Axial closing and seating (capture stage, lock stage, flange on lip).**
- Principle: 20 deg capture stage draws 1.0 mm. The closing torque 11.6 to 12.9 mN m is far above the 1.38 mN m needed to drag a free unit at mu 1 (reproduces).
- Seat: depends on the stack in 3.3. Unsupported at the plate-proud corner.
- Entry notch alignment depends on the open stop in 3.7.

### 3.10 Magnetism and automated checks 1 to 5

1. `requires_power_to_hold` is `false`. Passes. (My reading of the mechanism agrees: unpowered, the lugs stay captured by self-locking friction and nothing needs power.)
2. `release.bounded_independent_release` is `true`, `means` is nonempty. Passes. Release is the head's own motor, independent of the tail unit.
3. `retention.mechanism` and all three `alignment[].justification` are nonempty. `component_ids` are `head-cartridge`, `tail-stud` (exist). Passes.
4. No magnet is used. `mechanism_kind` is not `permanent_magnet`, no alignment is `magnetic`, and no component has `kind` `magnet`. Passes (not applicable).
5. Each alignment names at least one component (tail-stud, head-cartridge, coupler-motor, coupler-pinion, all exist). Passes.

Item 6 (this record) is `unresolved`. G6 therefore stays `unresolved`.

## 4. Errors found

1. The cartridge is fixed by "radial M1.6 into its lip" but the lip is 0.8 mm and the M1.6 minor diameter is 1.17 mm. Impossible as stated (assembly_access, limitations).
2. Roll window quoted at +-7.3 deg (mean radius 4.7) where the binding radius is the lug tip: 5.8 deg.
3. Friction citation: "bronze on steel dry static 0.35" is not on the cited Engineering ToolBox page (bronze - steel is grease 0.16 only). The steel-steel row is generic, not stainless. The 0.35 is on the conservative side for F_p_min and for release, but it is a misattributed number, not a sourced one. The only sourced dry values are 0.15 to 0.23 (Wikipedia).
4. `mechanism_kind` is `geometric_interlock`, but the retention is friction-held (self-locking): `friction_wedge`.
5. The flange (r 6.5) is larger than the lip and window (r 6.45), against the claim that the loop is all metal.
6. `coupler.py` depth bookkeeping places the sleeve front face at the lip rear face (0.8) while the PTFE ring of 0.3 mm lies between them. The 2.8 mm term hides this.
7. "Lateral and tilt" title: tilt is not computed.
8. The pilot-before-lug "assert" is satisfied only at nominal (margin 0.000).
9. The band "4.24 to 11.08 N" is described as covering all cited corners, but the motor-constant, supply-voltage and temperature corners are not in it.
10. The oil case is accepted for the flank but not for the face; the face slip threshold 3.1 mN m is below the declared torsion and the author's own mechanism says slip can walk the sleeve.
11. The author states Hertz "onset about 230" as 1.67 x 138 (rule of thumb). It reproduces. The design case sits 3.5 percent below it, and the oil case is above it. This is a provisional rule, so not an error, but the margin is thin.

No arithmetic error in the dossier numbers I checked (cam, stack, preload, release, loads, tipping, Hertz, joint range).

## 5. Classification of weaknesses

**Contradicted by the declaration's own numbers or by physics:**
- Cartridge screw into a 0.8 mm lip (errors 1). Scope: mount detail, flagged unsized by the author, small loads. Not treated as a contradiction of a retention requirement (see section 7).
- Roll window overstated (error 2): the corrected value still exceeds the stack.
- `mechanism_kind` label (error 4).

**Unsupported (blocks a pass):**
- Torsion no-slip not shown across motor, supply, face friction, contact radius and load combination (3.2); face contamination inconsistent with the flank cases.
- Tolerance stack missing terms, and the flange-on-plate corner (3.3).
- Sleeve rear stop and open hard stop not declared (3.7).
- Head-cartridge to shell load path (3.8).
- Tilt and joint-angle error in the alignment stack; source of the axial push (3.9).
- Release torque not bounded over supply voltage (3.7).
- Friction sources partly misattributed (error 3); the dry flank band is not wholly sourced.
- Preload is an initial, not a held, value (3.1).

**Gate 2/3 matters (not counted against the paper pass):**
- Vibration and shock behaviour of the self-locking stage; dynamic friction.
- Capture window by sweep (CPL-006); approach locomotion.
- Wear, galling of 304 on 304 at the pilot, PTFE creep over time, screw pull-out in PA12 as a test.
- Line contact on the helical flank (Hertz line length 2.35 mm assumes the flank is cut to match the lug); thermal stall of the motors.
- Q31 bending adequacy at high table friction (the author marks it unresolved).

## 6. What a further version would need

1. Mount the cartridge so that it exists: a lip boss or a rear flange thick enough for the screws, or a clamp. Show the axial restraint of the cartridge (pull-out and entry push) and the moment path (14 mN m) with a stated lever.
2. Make the flange radius smaller than the window and the lip (for example 6.3 against 6.45), or recess the plate, so the flange can only bear on the lip. Add the cartridge position and plate flushness to the stack, split the 2.8 mm term, and show the lock stage with margin.
3. Declare a rear stop or retainer for the sleeve and an open hard stop (parts, geometry, stress), and show the sleeve entry window against the stop tolerance.
4. Close the walking question either by: (a) bounding F_p over motor constant (cite or measure a lower bound), supply voltage and temperature, and taking r_eff, the face friction (a stainless-on-stainless source) and the combined loads into the no-slip ratio; or (b) a mechanical stop to walking that does not rely on friction, or a credited and sourced gear-train holding torque.
5. Treat face contamination the same way as flank contamination. Do not accept the oil case for one and not the other.
6. Add to the alignment stack the joint angle error and the tilt. State where the axial push comes from, even at a model level, without claiming a capture window.
7. Correct the friction citations (state which dry values come from Wikipedia and which from where), the roll window (tip radius), and `mechanism_kind` (`friction_wedge`).
8. State whether the declared loads act together and re-run the margins for the combinations.
9. Give the supply voltage available at the motor for release.

## 7. Basis of the outcome

Under protocol section 8 and Q062, `pass` needs retention under every declared load and every alignment means to be physically justified on paper. That is not met: section 5 lists unsupported items that block it, including the torsion no-slip corners, the stack and the flange-on-plate corner, the undeclared sleeve stops, and the unreal cartridge fixing.

`fail` needs a claim contradicted by the declaration's own numbers or by physics in a way that defeats a retention or alignment requirement. I looked for that and did not find it:
- Tension, shear, out-of-plane and in-plane bending each keep a geometric carrier inside the declared numbers (self-locking lugs, pilot in bore, lug pair with face edge). Torsion keeps its housing-slot carrier. No declared load is without a carrier in the sense of cand-a v5 (where the declared torsion had none).
- Each alignment window exceeds the declared PA12 stack on paper (lateral 1.10 vs 0.6, roll 5.8 vs 1.4), and no guide is shown blocked at a declared tolerance corner. The one corner I found (flange on PA12 slivers) depends on a cartridge position tolerance the declaration does not give.
- The one hard numeric contradiction (M1.6 in a 0.8 mm lip) is in a mount the declaration itself lists as unsized, in a statement G2 checks only for presence, and carries small loads.

If the lead keeps the cartridge fixing as declared and claims it as designed, or if a later reading of the declared PA12 tolerance shows the plate proud of the lip at a stated corner, I would change this to `fail`. As it stands the correct label is `unresolved`. A pass needs a new version that closes section 6. This record is a paper judgement only, label `exploratory`, and says nothing about whether the mechanism works.
