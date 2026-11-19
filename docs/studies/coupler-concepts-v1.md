# Coupler concept study v1 (paper, exploratory)

Label: **exploratory**. Date: 2026-11-19. Lead: Claude Opus 5.5. Decision record: Q83. This study **selects nothing**. Geometry, couplers and mechanisms are chosen only through the Q38 gates (CPL-011 stays `unresolved`). Nothing here is validated or reviewed. Numbers are cited, derived (formula shown) or marked **UNRESOLVED**. "Provisional" marks a value taken from the cand-a dossiers that has no source.

Inputs read: AGENTS.md; Q36, Q61, Q62, Q66 to Q80; `candidates/cand-a/dossier-v5.md` and its r1 reviews; `candidates/cand-b/dossier.md`, `candidates/cand-c/dossier.md` and their r1 reviews; `candidates/cand-a/scripts/` (`fourbar.py`, `closed_height.py`, `pin2.py`, README); `docs/originality/reference-corpus.md`; CPL-001 to CPL-011. The checkout used ends at Q80, so Q81 and Q82 were not read. The v6 work list is in Q73 and `retention-review-v5-r1.md` section 7. No cand-a v6 declaration exists.

## 1. Lessons from cand-a v1 to v5

| Ver | Outcome (G6 / originality) | Failure mode | Root cause |
| --- | --- | --- | --- |
| v1 | G6 unresolved; no highs | Spring ball-lock with SMA release and hex key; ball size, groove, preload, stroke and load never sized. Rigid coupler conflicts with Q31 chain bending | Mechanism declared before it was sized; estimate-basis parts (G3) |
| v2 | G6 unresolved; **two highs on D2**: CONRO, PolyBot (SMA-released latch on a grooved pin) | Spring toggle undefined, force balance incoherent; roll-in arc accepted without the table-height check | Latch principle copied from the corpus; kinematics checked without the real constraint |
| v3 | G6 **fail**; one high, Roombots D2 (motor crank into a non-reversible latch position) | Roll-in channel cut on the wrong arc (the lead's own kinematics error from Q66) | Kinematics error; the originality fix (motor over-centre) created a different single high |
| v4 | G6 unresolved; Roombots D2 high stays | Class-f tolerance assumed on PA12-carried parts (rocker boss, outrigger bore with 0.3 mm clearance); jaw window 0.03 to 0.12 mm at class-f stroke corners; flat thrust washer incompatible with yaw; keeper pin 0.02 to 0.2 mm outside the r 20 rule | **Tolerance stack through a fixed-stroke linkage** in a 40 mm cavity |
| v5 | G6 **fail**; Roombots D2 high stays (CONRO and PolyBot moderate) | Torsion declared (5.36 and 10.73 mN m) but the roll lock is lost when free play P > 0.62 mm (43 % of P = 0.05 to 1.05 mm), so the load has no carrier. Jaw window 0.087 mm (reviewer; dossier 0.104) against a stack of +-0.35 mm and a peg-height offset up to +-0.6 mm. Tongue closes only if the peg is within about 0.15 mm laterally. Release at the mu = 1 bound is 1.07 x M3 stall (blocked); rule T <= 0.5225 N. A 304 flexure to absorb the stack needs 49 to 131 mm^3 against about 30 mm^3 for the keeper | Stack of PA12 SLS +-0.3 mm per feature ([Materialise PA12 SLS](https://www.materialise.com/en/industrial/3d-printing-materials/pa12-sls), cited in the dossiers, accessed 2026-11-06) plus class f ([ISO 2768-1 table](https://amesweb.info/fits-tolerances/iso-2768-linear-dimensions-tolerances.aspx), accessed 2026-11-06) absorbed by free play, not by travel |

Packing is the common thread. The cavity is r 20 mm. The cell is 31 x 20 x 7.5 mm, the controller 17.8 x 22 x 5.7 mm, and the M3 gearmotor box is 6 x 18.7 x 6 mm (declaration boxes). Every tolerance fix had to fit in the volume left over, so each fix exposed the next margin (Q73).

Lessons carried into the concepts: (1) absorb tolerance by **travel or load-sensed closure**, not by a fixed stroke or free play; (2) every declared load needs a declared carrier at every tolerance corner; (3) a roll-in approach makes the entry side an open channel, so something must close it; (4) an originality fix that swaps one mechanism class for another moves the high, it does not remove it.

## 2. Requirements every coupler must meet

From Q11 (by reference), Q31 item 6, Q36, CPL-005/006/008/009, and Gate 1 G6 as the v2 to v5 reviewers applied it (`retention-review-v5-r1.md`):

1. **Passive retention under declared loads, unpowered**, per load path: tension, torsion, bending. Disclosing a failure is not a carrier. Declared loads from cand-a v5: W = 0.4208 N; design tension 4 mu W = 1.683 N (mu = 1, provisional); torsion 5.36 mN m (one idle neighbour tipped) and 10.73 mN m (two); pitch couple W/2 x 36 mm = 7.6 mN m (dossier modelling assumption).
2. **Bounded independent release** (CPL-009), physical and possibly blocked (CPL-008); the release torque balance must be shown at a stated tension.
3. **Justified pre-alignment and a named closing force** (CPL-005, G6). No axial, heading or capture-window claim without a sweep (CPL-006). Magnetism only if declared as a component, with force from a datasheet.
4. **Tolerance-robust at cited classes:** ISO 2768-1 class f for machined parts (+-0.05 mm for 3 to 6 mm, +-0.1 mm for 6 to 30 mm), PA12 SLS +-0.3 mm with no functional clearance below 0.6 mm and no wall below 1.0 mm (Q68). Arithmetic worst case, as the reviewers applied it.
5. **Originality (Q61/Q62 G7, G8):** no cell high against F1 or F2 (A1 Big Hero 6 is F1; its coupler descriptor is "magnetic"), no reference with two highs. Current single highs for cand-a: Roombots D2 (motor over-centre latch); CONRO and PolyBot D2 (SMA-released latch on a grooved pin) were highs in v2 and are moderate in v5 only because v5 has no SMA or spring.
6. Full 3D, no snapping or assist (CPL-004); Q31 chain bending must stay possible; data and power continuity are separate (Q33, Q34).

## 3. Concepts

Bodies: **a** = cand-a hex prism (R 25.5, 28 long, stowed sphere 58.18 mm; rolls over edges; yaw turntable gives +-12 deg bending; approach is a lateral roll-in only, no axial motion, no steering). **b** = cand-b Z-link (two 34 x 16 x 30 mm segments, servo pivot, chain bending is internal; plug 8 mm dia x 5; how a unit approaches a neighbour is **not designed**, its R2). **c** = cand-c sphere shell (59 mm, rolls about the chain axis; axial approach only, unsteered, drive force at most about 0.07 N by its own dossier; fails G5 on one-point support; no joint torque).

### K1. Offset-pin roll-in dock on cand-a (second torsion pin)

Idea: add one 1.5 mm steel pin beside the hex peg on the head face, entering a second arc channel by the same roll-in, so torsion has a carrier that does not depend on the jaw free play. Everything else is v5.

- **Packing (computed).** `pin2.py` as shipped checks only the docked position. I added a swept-path check (every roll angle 0 to 60 deg, both approach sides, pin radius 0.75 mm plus 0.3 mm clearance, against the declared receiver boxes). For engagement 5 mm (pin occupies y_B -14 to -9) the existing cell and controller layout **already** leaves free swept sectors: pin at 45 or 60 deg from the down direction, radius 8 to 10 mm, both approach sides. At r 10, 45 deg the worst clearance to any declared box is 1.12 mm (mirror side) and 1.93 mm. At 4 mm engagement (ytop -10.0) the same two angles are free. At r 12 only 45 deg is free. Re-laying out the cell and controller is **not needed** for one pin. Not checked: the A-side head-face obstacles, the end-plate slot and the hex wall for the pin channel, a symmetric second pin (315 deg fails the swept check), and assembly. 5 mm engagement is reachable for one pin on both approach sides; two pins are not shown.
- **Retention.** Tension and bending: unchanged v5 (tongue and groove, end faces). Torsion: the pin at 10 mm from the peg axis carries 10.73 mN m / 10 mm = 1.07 N (0.54 N for one neighbour), bearing 0.14 MPa on a 1.5 x 5 mm PA12 pocket.
- **Torsion lash at tolerance corners.** The pocket must clear the relative pin-to-peg spacing error: +-0.3 mm SLS per feature, two units, arithmetic +-0.6 mm, plus the 0.6 mm minimum clearance. Nominal slack 1.2 mm, range 0.6 to 1.8 mm. Lash = slack / 10 mm = **3.4, 6.9, 10.3 deg** (tight, nominal, loose). The peg's own lateral play at the loose corner (+-0.65 mm) can add up to about 7 deg. So roll lash goes from **unbounded to about 10 to 18 deg**. That is bounded, not stiff.
- **Release force balance.** Unchanged (T_rel = 0.5225 N rule). The pin adds a sliding path to be backed out along the arc; friction on it adds to the keeper release load (not quantified; UNRESOLVED).
- **Pre-alignment and closing force.** Unchanged: none axial or heading; closing by the unit's own roll. The jaw window 0.087 mm against a +-0.35 mm stack and the tongue's 0.15 mm lateral limit are **not touched**.
- **Body and budget.** a only. Mass about 0.07 g per steel pin (volume x 8 g/cm^3, density not cited here). No change to the cavity budget beyond a short channel.
- **Originality.** No change: Roombots D2 high, CONRO and PolyBot D2 moderate, ATRON D2 moderate. A pin in a slot is a generic element. Likely rating unchanged.
- **Main unknowns.** Pin channel through the end plate and hex wall; spacing stack through the PA12 end plate; effect of two engaged features on the heading window (not computed); everything in v5 that K1 does not touch.

### K2. Large keyed end-face boss with a separate axial latch

Idea: a hex (or dog-tooth) boss on one end face mates a socket on the other. Flats carry torsion, the contacting end faces carry compression and bending, a separate latch carries tension.

- **Approach motion by body.** Needs an axial approach with the keys aligned in roll, then a closing push along the chain axis. **a: cannot.** It only docks sideways; the final 10 deg of roll moves the head 25.5 mm x 0.1745 = 4.45 mm while turning 10 deg, so a socket must be open on the entry side by that sweep, and the open side must be closed by a gate (this is the v5 keeper). A pure end-face boss on a is v5 again. Also a boss that contacts the end face blocks yaw bending: rim clearance for +-12 deg is at least 25.5 mm x sin 12 deg = 5.3 mm (pivot in the face plane, upper bound; the v4 face clearance was not re-derived). **b: unresolved** (R2). Folding moves the plug on a 32.7 mm radius arc about the pivot (from the declared plug position), not along the axis. **c: only along its own axis,** with about 0.07 N of drive (cand-c dossier), unsteered, and a rigid keyed face removes the swivel that c's chain bending relied on.
- **Retention.** Tension: the separate latch (see originality). Torsion: hex flats. Bending: end-face contact plus flats; lever arms of 15 to 25 mm make the forces small (7.6 mN m / 30 mm = 0.25 N).
- **Torsion lash (computed).** Hex AF 12 mm, total across-flats clearance delta, lash = delta x sqrt(3) / AF: machined class f both parts (delta 0 to 0.4 mm) **0 to 3.3 deg**; PA12 SLS +-0.3 mm both parts with the 0.6 mm rule (delta 0 to 1.2 mm) **0 to 9.9 deg**, 5.0 deg at nominal. Contact force at 10.73 mN m with a 6 mm arm is about 1.8 N per flat.
- **Release and closing.** Latch-dependent. Closing force is the push to ride over a latch ramp or seat the keys: UNRESOLVED (no unit has a declared axial force except c at 0.07 N). Release: UNRESOLVED.
- **Budget.** b: the 16 x 30 mm end face fits an AF 12 boss. b's free end region is 7.1 mm long and already holds SMA wire, latch and pogo pins with zero spare length (cand-b dossier). a: no volume until the keeper is removed.
- **Originality.** A latch that is spring-hook plus SMA release is the v2 pair of highs (CONRO and PolyBot D2). A motor over-centre latch is the Roombots high. A motor lead-screw hook is ATRON D2 (moderate on cand-a today, would rise). The boss itself is generic. Likely: one high, depends on the latch chosen.
- **Main unknowns.** Which body produces an axial push; the latch; no body is shown to approach axially with a closing force.

### K3. Keyed face held by a declared permanent magnet, mechanical release

Idea: a keyed face (as K2) with the axial hold supplied by a declared neodymium magnet; a cam or lever (driven by the existing gearmotor) pushes the faces apart.

- **Magnet datasheet.** K&J Magnetics D41, N42, 1/4 in dia x 1/16 in (6.35 x 1.59 mm), pull force case 1 (against a thick steel plate, contact) **1.19 lb = 5.29 N** ([K&J D41](https://www.kjmagnetics.com/proddetail.asp?prod=D41), values from a search snippet, accessed 2026-11-19; the page itself returned HTTP 403 and was **not read**, so the force-versus-gap curve, magnet-to-magnet force, temperature limit and mass are **UNRESOLVED**). Volume 50.3 mm^3, so about 0.38 g at a typical NdFeB density (density not cited here).
- **Retention.** Tension: one D41 at contact gives 5.29 / 1.683 = **3.1 x** the design tension. At the real gap (key stand-off, 0.1 mm recess, SLS +-0.3 mm per face) the force is **UNRESOLVED**; it needs the vendor curve. A PA12 wall of 1.0 mm in front of the magnet is a 2 mm face-to-face gap, so the magnet would sit in a machined insert flush with the face. The counter-face must be ferromagnetic or a magnet; 304 is not a dependable choice (grade and source UNRESOLVED). Torsion and bending: same as K2 (keys and contact); the magnet adds nothing in rotation except friction (mu x 5.29 N, mu = 0.15 provisional gives 0.79 N against 0.42 N from 10.73 mN m over a 25.5 mm arm: 1.9 x, friction only, not geometric).
- **Release balance.** Faces must be pushed apart against about 5.29 N at contact, less any tension T that already pulls them apart (net 5.29 - T). The M3-class gearmotor (3 mN m rated, 9 mN m stall, v5) needs a cam lever no larger than 3 / 5.29 = **0.57 mm/rad at rated** and **1.70 mm/rad at stall** per magnet (half that for two magnets), before friction. Work check: 5.29 N x 1 mm is 5.3 mJ against 3 mN m x 1.75 rad = 5.3 mJ at rated, so it is marginal at rated and the key-tooth lift-off must also be paid. Peeling a face instead of pushing it flat would cut the force, but no peel factor is cited (UNRESOLVED).
- **Pre-alignment and closing force.** Magnet attraction can supply the closing force and some centring, but only if declared and justified from the curve (CPL-005, Q36 constraints) and the capture window is then measured (CPL-006). Values UNRESOLVED.
- **Body.** a: replaces the four-bar keeper by a cam on the same M3, freeing the frame mass (1.16 g of 304 frame parts in v5); the entry-side gate problem of K2 stays, so friction alone would have to hold the key against the roll-in direction. b: possible, approach unresolved. c: magnet replaces the spring jaws; c's other defects stay.
- **Originality (the decisive risk).** Permanent-magnet faces are the passive coupler of M-TRAN I/II (C1, C2), M-Blocks and 3D M-Blocks (C7, C8), Cubelets (D1), MOSS (D2), FreeBOT (C16) and Telecube (C18), and the descriptor of **A1 (Big Hero 6, F1) is "magnetic" for D2**. The reviewers rated cand-a against M-Blocks D3 and D4 moderate already. A permanent-magnet coupler is likely **moderate to high** on D2 against several of these, and any high against A1 fails G8. Removing the over-centre keeper would drop the Roombots high but replace it with this risk. Not reviewable here.
- **Main unknowns.** The force curve and the magnet-to-magnet value; the A1 D2 rating; ferromagnetic counter-face parts; the cam lever and stroke; magnetic effect on the BNO/IMU class sensors (not assessed).

### K4. Load-sensed lead-screw keeper (tolerance absorbed by travel), with K1 as the torsion carrier

I judge this stronger on the evidence of section 1. It replaces the fixed-stroke four-bar of v5 with a non-backdrivable lead screw driving the same tongue (a half-nut closing on the peg groove) to a **motor-current stall** (own sensing only), so the stroke tolerance disappears and the closing force rises.

- **Screw numbers (derived).** M2 coarse thread, pitch 0.4 mm (standard ISO metric coarse; not cited in this study), pitch diameter 1.740 mm, lead angle 4.18 deg. Friction angle at mu = 0.15 (provisional) 8.53 deg. Torque per axial newton 0.196 mN m/N for the thread alone, 0.346 mN m/N with a 1 mm radius collar at mu 0.15. Self-locking needs thread friction above tan(4.18 deg) = **0.073**, a margin of 2.05 x on mu = 0.15 (the real mu is UNRESOLVED, as the worm self-lock was in v5).
- **Closing force.** Rated 3 mN m gives **8.7 N** (15.3 N without collar friction), against v5's four-bar minimum of 1.045 N: about 8 x more. The v5 V-notch wedge needed a lateral force above mu W = 0.421 N and reached a ratio of 0.98 at rated; at 8.7 N and the same lateral fraction 0.393 the ratio is **8.1**. That could make the V-notch a justified centring means; it still needs the sweep (CPL-006).
- **Retention.** Tension: peg shoulder on the tongue as v5, held by the self-locking screw. Torsion: needs K1 (the screw does not touch roll). Bending: unchanged.
- **Release force balance.** At the v5 design tension 1.683 N plus a 5 N preload (preload provisional), axial load 6.68 N: back-off torque 6.68 x (0.870 x tan(8.53 - 4.18 deg) + 0.15 x 1.0) = **1.44 mN m**, 0.48 of rated, against v5's 9.66 mN m at the same tension (6.7 x less). So release is no longer blocked at the mu = 1 bound, and the T <= 0.5225 N rule would not be needed. Stroke 4.6 mm at 0.4 mm/turn is 11.5 turns; the 206-109 output speed is not in the repo, so release time is **UNRESOLVED**.
- **Body and budget.** a. The screw axis must run along the tongue's z motion, but the M3 motor (6 x 18.7 mm) lies along y at z 12.27. No layout exists. It likely needs a worm or bevel stage, which the cavity may not hold. **UNRESOLVED**; this is the first thing to test on paper. A taper-seated variant for b (taper half-angle 10 deg removes hex lash under preload; seating depth changes by delta / (2 tan alpha) = 1.13 mm machined, 3.40 mm SLS; at 5 deg for self-holding 2.29 and 6.86 mm, longer than b's 7.1 mm end region) is listed as a K4b option only; it still has no approach motion and no motor volume.
- **Originality.** Removing the four-bar drops the Roombots D2 high. A motor lead-screw actuating a hook is ATRON D2 (moderate today) and could become a single high; a screw-driven half-nut on a grooved pin shares the CONRO/PolyBot latch-on-groove class but has no SMA or spring. Likely one high or moderate; a reviewer must rate it.
- **Main unknowns.** Drive layout and mass in the cavity; real thread friction; whether lateral offset (0.15 mm notch limit) is fixed by the wedge; screw wear and dust in a SLS enclosure.

## 4. Comparison (qualitative, no weighted score)

| | K1 pin | K2 keyed boss + latch | K3 magnet + cam | K4 screw keeper (+K1) |
| --- | --- | --- | --- | --- |
| Fixes v5 torsion | yes, lash bounded to about 10 to 18 deg | yes on b, 0 to 3.3 deg machined / 0 to 9.9 deg SLS | same as K2 | needs K1 |
| Fixes v5 alignment / closure | no (jaw window 0.087 mm unchanged) | n/a | n/a | closing force about 8 x v5, stroke stack removed; lateral 0.15 mm limit unverified |
| Release at 1.683 N | unchanged, blocked at mu 1 | UNRESOLVED | 5.29 N at contact; lever <= 0.57 mm/rad rated | 1.44 mN m = 0.48 of rated |
| Approach motion needed | existing roll-in (a) | axial, no body has it | as K2 (a: roll-in) | existing roll-in (a) |
| Fits | a; pin sector free at 45 to 60 deg r 8 to 10 mm | b only, approach UNRESOLVED | a, b | a, drive layout UNRESOLVED |
| Originality | unchanged (Roombots D2 high) | one high likely, depends on latch | **moderate-high; A1 D2 magnetic risk (F1)** | one high or moderate (ATRON D2) |
| Biggest unknown | A-side and end-plate channel | axial approach and closing force | force curve; A1 rating | drive volume in the cavity |

## 5. Recommendation (not a selection)

Declare next, as the thing the owner may choose at the gate: **K4 with K1, on body a** (a cand-a v6 declaration), paper-gated like any candidate.

Reason: a is the only body with a verified approach path, and the only one whose torsion contradiction has a computed repair (K1: free swept sector, lash bounded to about 10 to 18 deg). K4 targets the cause behind v4 and v5 (stack absorbed by free play) and gives the decisive numbers: closing force 8.7 N against 1.045 N, V-notch closing ratio 8.1 against 0.98, release 1.44 mN m against 9.66 mN m at the same tension. K2, K3 and the b and c bodies all depend on an axial approach and closing force that no declared body has (b's R2, c's 0.07 N), so they cannot be evaluated further on paper until that is decided. K3 adds an F1-related originality risk.

Biggest risk: **drive packaging.** There is no layout that puts a screw axis along the tongue motion inside the cavity volume the four-bar leaves free. If it does not fit, K4 collapses to v5's problems. Second risks: thread self-lock friction is unknown, the jaw window (0.087 mm) and the jaw-to-peg height stack are untouched by K1 and K4 and still need a separate fix, and a lead-screw hook may become an ATRON D2 high.

All of this is paper, exploratory, and would have to pass Gate 1 and later gates with independent reviews. The study does not abandon or select any family or body (Q74, Q38).
