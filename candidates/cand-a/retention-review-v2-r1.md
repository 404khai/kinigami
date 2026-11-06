# Retention review: cand-a v2, r1

candidate_id: cand-a
candidate_version: 2
author: Claude Opus 5.5 (engineering lead) with Claude Sonnet 5.5 (cand-a v2 implementation agent)
reviewer: reviewer-a2-retention (Claude Sonnet 5.5, independent session, no authorship in cand-a v2)
outcome: unresolved

Date: 2026-11-06. Reviewed: `dossier-v2.md` (sections 3, 6 to 11, 14), the `retention`, `alignment` and coupler component entries of `declaration.json` (SHA-256 b7a6e94d20b91df9e1bd27ba3af124ba66237d7fd0585594b87084e79812e54c, from `shasum -a 256`), the v1 review `retention-review-v1-r1.md`, protocol section 8, Q036, Q062 G6, Q063, Q066, Q031 item 6, CPL-005/006/008/009, Q047. This is a paper judgement under protocol section 8, not a test (Gate 2/3). Pass would mean "judged physically justified on paper", not "works". The reviewer did not author v2 and added no evidence in its favour. Figures marked "reviewer" are my own estimates and are labelled as such.

## 1. Summary of the judgement

v2 is a large improvement over v1. The alignment means are now physically described with declared dimensions, the roll-in arc is geometrically correct (checked below), a closing force is named, and the loads on the coupler are small and honestly derived. But the central retention element, the dead-centre toggle keeper, is not defined well enough on paper to support the claim that it holds unpowered under the declared loads. Three specific defects (section 2.3) prevent a pass. None of them is a contradiction of physics, so the outcome is `unresolved`, not `fail`.

## 2. Retention (304 tongue in the peg groove, held by a dead-centre toggle)

### 2.1 What is supported

- **Principle for the tension path: supported.** A 0.8 mm tongue in a 1.6 mm annular groove is a plain geometric interlock. Axial tension reaches the tongue on a groove shoulder, and no power is involved. The declared loads follow from W = m g = 0.3584 N (rechecked: 0.03655 kg x 9.80665) and mu <= 1: 4 mu W = 1.434 N (rechecked), torsion W R/2 = 0.3584 x 12.75 = 4.57 mN·m (rechecked), pitch bending W/2 x 36 = 6.45 mN·m (rechecked). Bearing stresses of 0.07 to 0.96 MPa against 50 MPa (PA12) and 205 MPa (304) are of the order the dossier says; the margins are about 100x, so no realistic correction to the areas changes the strength conclusion.
- **Over-centre locking, as a principle, is supported.** A load acting along a two-link toggle line, with the knee past centre against a stop, presses the knee further onto the stop, so a load of any size is held without power. The dossier's statement that the peg loads "cannot back-drive" the toggle is correct if, and only if, the knee is past centre against a stop. The 5 mm x 0.8 x 1.5 mm 304 links would carry the loads easily (Euler load of one link is about 4.9 kN, reviewer, E = 193 GPa).
- **Unpowered: yes.** `requires_power_to_hold` is false. The SMA wire only releases. Release is declared as bounded and independent.
- **Spring data: verified.** Lee LC 014A 01 S page read on 2026-11-06 (rate 9.4 lb/in = 1.646 N/mm, free 6.35 mm, solid 2.24 mm, 6.29 total and 4.29 active coils, wire 0.36 mm, OD 3.05 mm). Reviewer cross-check from wire mechanics (G = 69 GPa, D = 2.69 mm, 4.29 active coils) gives 1.65 N/mm. Preload 1.646 x 0.2 = 0.329 N and 1.646 x 0.5 = 0.823 N are correct arithmetic. Spring wire volume 53.2 mm x 0.0993 mm^2 = 5.28 mm^3 is correct.
- **SMA data: verified.** Dynalloy TCF1140 (SparkFun copy) row 0.004 in: 3.2 ohm/in, 143 g, 200 mA, cooling 1.1 s (LT) and 0.9 s (HT). 143 g = 1.402 N and 1.402 N / 0.008107 mm^2 = 173 MPa (rechecked). Stroke at 4 percent of 22 mm = 0.88 mm (rechecked; margin 2.93 over 0.3 mm). Wire twist from +-15 degrees yaw about its own axis is a shear strain of about 0.06 percent (reviewer), negligible, so the claim that yaw does not load the wire holds.

### 2.2 Per-item answer to the four items the v1 review required

1. **Sized retention with force balance.** Partly met. Holding loads, areas and stresses are declared and arithmetically correct (tension, torsion, bending). Spring rate and preload are declared. The SMA pull versus the spring is declared. But the force balance of the toggle itself is not coherent (section 2.3 item A). Retention in tension is sized; retention of the toggle in the closed state is not.
2. **Alignment dimensions with capture estimate and a named closing force.** Met at paper level (section 3), with the caveats listed there. The closing force is named: the arriving unit's own lift drive plus gravity. Reviewer estimate of the authority at the start of the final roll: at rated ring torque 9.01 mN·m the lobe normal force is 9.01/18.02 mm = 0.50 N, moment about the pivot 0.50 x 30.77 = 15.4 mN·m, less the weight moment 4.57, so about 10.8 mN·m, or about 0.42 N tangentially at the peg radius R = 25.5 mm. That is above the head-end friction 0.179 N the dossier uses (mu = 1) and about 1.2x the full-weight friction 0.358 N. Stated as my estimate, not a dossier figure.
3. **Tumbling axis and chain alignment through a step.** Met at paper level. The axis is the bottom hexagon edge, parallel to the prism axis y. Rolling about it is a rotation in the x-z plane, so end faces stay in their y planes, and a chain whose units step together pivots about one common edge line and stays straight. I checked the roll-in arc: with the unit resting on F0, the leading bottom vertex is (R/2, -a) and its distance to the face centre and to the vertex (R,0) is exactly R (sqrt(R^2/4 + a^2) = R). A world-fixed point at B-frame (R,0) therefore moves, as B rolls 60 degrees, along a circle of radius R about that vertex to (0,0). The arc peak is a - R sin 90 degrees offset = 3.4 mm above the mid-height line. This matches the declared slot (radius 25.5, centred on the bottom vertices, from (+-R,0) to the face centre). The arc is correct. Not discussed: the 60-degree relative roll that results (B ends on F1 or F5, so its yaw axis is not vertical until the chain is rolled back as a log). It does not defeat the principle; it matters for sequencing at Gate 2.
4. **Rigid coupler versus Q31 bending.** Resolved on paper by a powered yaw turntable (worm 7.13 degrees lead, 27:1 sector, +-12 degrees working, +-15 degrees stops). Checks: lead angle atan(0.3/2.4) = 7.125 degrees; worm efficiency tan(7.125)/tan(7.125 + 8.53) = 0.446; puck torque 3 x 27 x 0.446 = 36.1 mN·m; design load 32.8 mN·m at mu = 1 (ratio 1.10, thin, as the dossier says); tooth force 8.1, 8.9 and 26.7 N; face clearance g >= (p + R sin b)/cos b - p = 5.55 mm at 12 degrees and 7.04 mm at 15 degrees, so the 8 mm gap leaves 0.96 mm. All recomputed and correct. Holding a bend is correctly classified as actively maintained unless friction >= 0.125 (Q31 item 6 asks exactly for this distinction). The 27-tooth sector spans only about 3.2 teeth over +-21.5 degrees (reviewer), so tooth load goes to one or two teeth, which the crude Lewis flag already treats as unresolved. Not a G6 blocker.

### 2.3 Why retention is not passed (the decisive points)

**A. The toggle force balance is not coherent, and the sources disagree.**
- Q066 item 4 says the v2 keeper has "no spring holding it closed" and is bistable. The declaration and dossier say the toggle is "biased closed by a Lee spring at 0.2 mm compression (0.33 N)", that the SMA pulls the knee 0.3 mm past centre and "the spring then snaps it open and it stays open unpowered", and that the arriving peg re-closes it. A spring that biases the knee closed cannot also hold it open unpowered. Bistability needs the spring to act across the link line, not along the knee travel.
- If the spring acts along the knee travel (the reading behind the numbers 0.329 N, 0.823 N and the 1.70 SMA margin), the toggle is monostable closed. The tongue would then re-extend as soon as the SMA cools, and in the open state it would block the arriving peg. The docking and release sequence would not work.
- If the spring acts along the link line (bistable), the knee force it produces is small: for a 0.329 N axial preload, 5 mm links and a 0.3 mm knee offset, the lateral force is about 2 x 0.329 x 0.3 / 5 = 0.04 N (reviewer). The figures 0.33 to 0.82 N and the ratio 1.84 against head-end friction would not be available, and the V-notch seating argument loses its force basis.
- Either reading leaves the numbers in the dossier underived. The geometry from which they would follow (link pin positions, over-centre offset, stop) is declared UNRESOLVED by the dossier itself (sections 7, 8, 14). Dead-centre geometry is the governing geometry of the retention claim.

**B. The only unpowered holding force in the closed state is the spring unless over-centre is shown, and the spring is too weak.** Loads acting along the tongue's retract axis (z) are real: pitch bending gives about 1.29 N at the tongue (dossier), and torsion about y has to cam the peg out of the half-hex cup against the tongue. For a 4.57 mN·m torque and a hex lifting 1.155 mm/rad about its lower corner, the cam-out force is about 4.0 N (reviewer; the dossier's 1.52 N "flat bearing" model assumes a full hex socket, which the half-hex cup with a round-neck tongue is not). Both exceed the 0.329 N spring by 4x to 12x, so retention under the declared loads rests wholly on the knee being past centre against a stop by a margin larger than the SLS tolerance. The dossier says as much (section 8: "if the toggle is not actually past centre the lock holds only by the spring"). The principle is sound but its governing dimension is absent.

**C. The tension load path does not close on the declared dimensions.** In the body frame of the receiving unit the peg groove is centred 2.5 mm inside the tail face (y = -11.5), so the 0.8 mm tongue spans y = -11.9 to -11.1. The yaw puck cylinder (r 3.8 about (0, -8.2)) spans y = -12.0 to -4.4. The wall in front of the tongue's loaded face is therefore at most 0.1 mm, not the 21 mm^2 of PA12 the dossier uses. The end plate back face is also at y = -12.0 and the face opening is relieved to +-4.2 mm in x, so it cannot take that load either. Further, the path from puck to body is not declared at all: the puck sits in cap halves (declared as boxes at |x| >= 3.9 against a puck radius 3.8) and turns on a 2 mm dia PA12 shaft. Tension, pitch moment and roll torque all end up there. A reviewer estimate with a solid 2 mm shaft carrying 8.6 to 9.1 N·mm in bending gives about 11 MPa, roughly a fifth of PA12 tensile strength before creep, stress concentration and the hollow bore. That is not a failure, but it is not covered by any stated bearing check. The dossier assesses only the peg-to-puck-wall step.

None of A to C says the mechanism cannot work. Together they leave the key claim ("holds unpowered with the toggle past centre, loads carried to the body") without governing dimensions.

## 3. Pre-alignment means

### 3.1 Roll-in arc channel (geometric_guide, `cap-l`, `cap-r`, `head-peg`, `endplate-b`)

- **Principle: supported and checked** (section 2.2 item 3). Constrained path, no attraction, no magnet. Magnetism rule not triggered.
- **Dimensions: declared** (radius 25.5, width 5.4, depth 5.5, flare 45 x 1.5, peg 4.0 across flats / 4.619 across corners). Per-side clearance (5.4 - 4.619)/2 = 0.39 mm and lateral mouth 0.39 + 1.5 = 1.89 mm are correct. Peg engagement 5 mm in a 5.5 mm slot is consistent with the declared gap (22 - 14 = 8 mm, tip at y = 27). A hex rotating through 60 degrees in the slot has width between 4.0 and 4.619 mm, always below 5.4.
- **Heading window:** the dossier gives atan(0.39/5) = 4.46 degrees. My exact two-point jam condition (5 sin e + 4.619 cos e = 5.4) gives about 9.8 degrees, so the dossier figure is conservative.
- **Axial lane +-0.8 mm** depends on the 0.4 x 45 degree chamfers on a 0.8 mm tongue in a 1.6 mm groove. Two 0.4 mm chamfers on a 0.8 mm tongue leave no flat (knife-edge tip). The play without chamfers is +-0.4 mm. The +-0.8 mm is therefore a lead-in figure, and a zero-width tongue edge is not a practical feature. Noted, not decisive.
- **Preconditions without a mechanism.** Axial position (+-0.8 mm) and heading before the final roll are not supplied by any declared means. The unit has no steering and no axial motion (dossier risk 1). The dossier states this honestly as a precondition and does not claim a self-aligning capture range. I accept it for G6 because the claim is explicitly conditional, but it sharply limits what "pre-alignment" means here.
- **Closing force: named** (section 2.2 item 2). The final-pose accuracy against slot clearance 0.39 mm and the unquantified roll-edge radius is a Gate 2 issue.
- **Unpowered:** gravity and the arriving unit's own drive do the work; the stationary unit needs no power.
- Judgement: **supported on paper**, with the above conditions.

### 3.2 Tongue V-notch seating (`keeper`, `yaw-puck`, `head-peg`)

- Principle (wedge centring) is credible. Dimensions are declared (notch 3.1 mm, mouth 6.0 mm, 30 degree half angle, so notch depth is (6.0 - 3.1)/2 / tan 30 = 2.5 mm; seating +-1.45 mm is correct arithmetic).
- Force reasoning is **not supported**: it compares the toggle snap force (0.33 to 0.82 N) directly with head-end friction 0.179 N, ratio 1.84. That ignores the wedge factor and tongue friction (reviewer: 1/tan 30 = 1.73 frictionless, about 0.94 with mu 0.3 on the flank) and, more importantly, rests on a snap force that section 2.3 A shows is not derivable. After the roll-in the peg is already within +-0.39 mm, so this means is secondary. Judgement: **unresolved** as a stand-alone means.

### 3.3 Hex peg in half-hex cup with tip chamfer (`head-peg`, `yaw-puck`)

- Principle: a hex key fixes roll in six positions, and both units rest on flats, so roll error arrives near zero from gravity. Supported in kind. The cup opening direction relative to the arc end tangent (30 degrees below horizontal at arrival, my derivation) and the peg-to-cup clearance are not declared. The chamfer 0.5 x 45 degrees is the only lead-in stated. Torsion path: see section 2.3 B. Judgement: **supported in kind, dimensions incomplete**; it is not the deciding item.

## 4. Things that are only asserted

- Toggle over-centre offset, stop, pin positions; whether the spring is bistable or monostable.
- Trip energy fraction. Work needed 0.82 N x 0.3 mm = 0.247 mJ against 1.225 mJ landing energy is arithmetically right (0.3584 N x 3.416 mm = 1.224 mJ), but how much reaches the trip is dynamic.
- Release under load: the 0.82 N release force excludes tongue friction under tension. With 1.43 N tension and mu 0.3 the shoulder friction adds about 0.43 N, giving about 1.25 N against 1.40 N available (reviewer). CPL-008 allows release to fail under load, so this is not a G6 blocker, but the margin 1.70 is not valid under load.
- Worm self-locking (needs friction >= 0.125), SLS tolerances (not cited; slot clearance 0.39 mm and tongue lane are of the order of typical SLS tolerance), tooth strength (assumed Lewis factor), ring bearing friction (reviewer rough upper estimate with mu 0.3 gives up to about 1.8 mN·m, still under the 9.01 mN·m margin), wall strength, heat.

At the paper level required by protocol section 8, the alignment principle and sizing (roll-in) are sufficient. For retention, the principle is sufficient but the declared dimensions and force reasoning for the toggle are not, and the tension path has a dimensional inconsistency. Under section 8, unsupported claims are unresolved, never pass.

## 5. Arithmetic errors found in the dossier

No arithmetic error changes a conclusion. Items checked and correct: spring preload and rate, SMA pull, stress and stroke, W and the derived loads, G1 sphere (sqrt(25.5^2 + 14^2) = 29.09 mm), a = 22.0836, lobe contact angle 39.21 degrees, ring sweep 140.8 degrees, tipping sqrt(L^2 - R^2) = 12.73 mm, 42.7 degree push, peak torque 7.47 W·mm and the friction table, available torque 9.01 and 27.0 mN·m, tooth forces, worm lead and efficiency, face clearance 5.55 and 7.04 mm, peg sweep 1.23 and 1.55 mm, tension, torsion and bending stresses. Inconsistencies (not arithmetic): (a) Q066 "no spring holding it closed" versus the declaration's spring-biased closed keeper; (b) the 0.1 mm wall implied by the declared puck and groove positions; (c) the "+-0.8 mm" axial lane quoted as a nominal window though the tongue play is +-0.4 mm; (d) the torsion check treats the half-hex cup as a full socket.

## 6. Required to reach pass in a v3

1. Specify the toggle: link pin coordinates, over-centre offset and its tolerance, the stop, the spring position and direction, and state whether it is bistable. Resolve the conflict with Q066 item 4. Give a force balance for closing, holding, opening and open-state holding that follows from that geometry, with the SMA force and stroke against it.
2. Fix the tension path: make the dimensions consistent (groove and tongue position versus puck wall), and declare how the puck is carried to the body (bearing, retention against -y, shaft section) with a stress check for tension, pitch and roll loads.
3. Re-do the torsion check for a half-hex cup (cam-out against the tongue) and the release force under the design tension.
4. Declare the cup opening direction, cup-to-peg clearance, and the tongue tip form (no zero-width edge). Restate the axial lane from the real play.
5. Either supply a means of axial and heading pre-alignment or state clearly that none exists and that pre-alignment covers only the in-plane roll-in. Say how the 60-degree relative roll after docking is handled.
6. Cite an SLS tolerance and show the slot clearance and over-centre offset survive it.

Spot checks recorded: Lee Spring product page (read), Dynalloy TCF1140 SparkFun PDF (text extracted, 0.004 in row), plus the arithmetic above recomputed by script. EOS PA 2200 data sheet and ATI 304 sheet were not re-read.
