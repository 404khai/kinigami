# Q93 — cand-d version 5: revision decisions

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-20 |
| Supersedes | — (changes no criterion, threshold or verdict; v1 to v4 and their records are preserved) |
| Provenance | **agent decision under explicit owner delegation**. Lead: Claude Opus 5.5 (cand-d author) |

## Context

The v4 retention review (`candidates/cand-d/retention-review-v4-r1.md` §7) left G6 `unresolved` with no contradiction. The decisive item is seating at the guaranteed lower-bound motor torque. Dry 304 teeth (μ up to 0.8) cannot roll a unit flat, and the roll and yaw residuals can take the seat out of the 3 deg lock stage. Q92 started v5.

## Decision

1. **Seating at the lower bound.**
   - The head Hirth flanks carry a bonded PTFE dry film. PTFE on steel is μ 0.05 to 0.20 (Engineering ToolBox, raw HTML).
   - Closing rises to a 1.5 V PWM average, so the guaranteed draw is 1.76 N:
     - roll: 1.39 N is needed to tip a unit about its far bottom edge (1.27x);
     - pitch: 0.21 N is needed (8.3x).
   - Yaw is not flattened. A tighter pilot (bore 4.010 +0.010/0, pilot 3.960 to 3.970, clearance 0.040 to 0.060) bounds it to 0.69 deg. The seat window is then stack ±0.0815 plus yaw ±0.059 = ±0.140, against the lock stage's ±0.20.
   - The pilot's radial clearance (≥ 0.020) exceeds the pilot-to-Hirth coaxiality (±0.010 for two parts).
2. **Sleeve material.** C93200 is replaced by **C95400 aluminium bronze** (Concast, raw HTML: yield 221 MPa min, 7.45 g/cm³, E 107 GPa, uses include nuts and worm gears). The higher closing force keeps the lug contact below onset: 244 MPa with all loads, 265 oiled, fault 283, against about 369. The flank friction rows (steel on bronze) are applied to aluminium bronze as a bronze, and this is a declared limitation.
3. **Release supply.** Release is allowed only with the cell at 3.75 V or more, so the motor gets its 3.6 V maximum. The margin is 1.25 dry and 1.30 oiled.
4. **Coupler motor mount.** A 304 clip band is bonded to the gearhead with LOCTITE 638 (TDS, raw PDF: 13.5 N/mm² at 15 min on steel; specific gravity 1.1). The clip is screwed from below into 304 thread. The bond resists 4.7 N m against the 10.8 mN m reaction.
5. **Cell-voltage sense.** A divider of two Vishay CRCW0402 resistors (datasheet, raw PDF: 0.65 mg) feeds a controller ADC. It sets the closing duty and applies the release rule.
6. **Hinge ear notch.** The head inner wall is declared with notches at |y| < 1.6, and the ear boxes run through it to their legs.
7. **Errors corrected.**
   - The plates are checked as fixed-fixed strips: head 15.5 MPa and tail 14.2 MPa, against the Materialise PA12 tensile strength of 48 MPa.
   - The PA12 source becomes Materialise PA12 (SLS) (raw HTML: 0.95 g/cm³, 48 MPa). The EOS PDF returned HTTP 403.
   - The pilot is lengthened to 6.5, giving a crest-plane margin of 0.25.
   - The assembly sequence is corrected: the housing goes in from the front, and the sleeve, ring and collar from inside through the open top. The tail screws are driven with an L key through the top before the controller goes in.

The stowed diameter rises to 59.133 mm (margin 0.87 mm).

## Order

This record, then the v5 declaration, dossier and scripts (`declaration-v4.json` keeps v4), then fresh independent reviews of v5, then an official run.
