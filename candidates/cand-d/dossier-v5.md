# Candidate D (`cand-d`), version 5: two-segment inline body, coupler-first

Family B (Q62 §3). Started by Q85. Q86, Q88, Q90 and Q92 disposed of versions 1 to 4. Q93 records the version 5 decisions.

| Field | Value |
| --- | --- |
| Result label | `exploratory` (paper gate, Q38/Q40). Nothing here is validated |
| Declaration | `candidates/cand-d/declaration.json`, SHA-256 `c6baa8dcfbd3de4c5c3ed06fbb9b9d7dfcb1a8cd90738b737816a05736b8897d`. Earlier versions are kept as `declaration-v1.json` to `declaration-v4.json`, with their dossiers and reviews |
| Author | Claude Opus 5.5 (engineering lead). Not a reviewer |
| Declared | 2026-11-20 |
| Criteria | `criteria/gates/gate1-v1.json` (sha `ffe13533…`), protocol revision 2 |
| Reproduce | `cd candidates/cand-d/scripts && python3 declaration_text.py && python3 gen_declaration.py --write && python3 coupler.py && python3 joint.py`. `coupler.py` asserts every margin it claims |

Unchanged from versions 3 and 4 (`dossier-v3.md`, `dossier-v4.md`, `dossier-v2.md`):
- the body, joint, electronics and envelope layout;
- the cam geometry (20 deg capture, 3 deg lock, flank radius 4.875, line 2.65);
- the Hirth geometry (36 teeth, 90 deg, r 2.6 to 6.3);
- the head flange mount with nut blocks;
- the tail stud mount, the hinge legs, the stop pin and the retainer.

## 1. What version 5 changes (review v4 §7, Q93)

| v4 item | v5 |
| --- | --- |
| Partial-seat fallback covered pitch only; at the guaranteed lower-bound motor torque the teeth cannot roll or yaw a unit flat, and the residuals can leave the lock stage | Bonded PTFE film on the head Hirth flanks (PTFE on steel μ 0.05 to 0.20). Closing at a **1.5 V** stall gives a guaranteed draw of **1.76 N**: roll needs 1.39 N (1.27x), pitch 0.21 N (8.3x). Yaw is bounded to **0.69 deg** by a tighter pilot (clearance 0.040 to 0.060). Seat window ±0.0815 (stack) ±0.059 (yaw) = **±0.140 against ±0.20**. Pilot radial clearance (≥ 0.020) exceeds the two-part pilot-to-Hirth coaxiality (±0.010) |
| Higher closing force against contact stress | Sleeve **C95400 aluminium bronze** (yield 221 MPa, E 107 GPa, 7.45 g/cm³). Lug Hertz: 203 typical, 244 with all loads, 265 oiled, fault 283 MPa, against an onset of about 369 |
| Release margin with the higher preload | Release only with the cell ≥ 3.75 V, giving 3.6 V at the motor (its maximum). Release needs 27.8 mN m (26.8 oiled) against 34.8 available: **1.25 / 1.30** |
| Coupler motor mount not declared | 304 clip band bonded with **LOCTITE 638** (13.5 N/mm² at 15 min on steel; 113 mm² → 1527 N, 4.7 N m), with feet screwed from below into 304 thread. Mesh force 6.0 N, 3.0 N per screw, 0.59 MPa on PA12. Motor box enlarged to ±3.35 to contain the band; the clip and bond masses are lumped boxes |
| Cell-voltage sense not declared | Divider of two **Vishay CRCW0402** 100 kΩ resistors (0.65 mg, ≤ 1 mW) into a controller ADC. It sets the 1.5 V closing duty and applies the 3.75 V release rule |
| Hinge ear crosses the wall without a notch | The head inner wall is declared as a core plus four side pieces, leaving notches at \|y\| < 1.6 for both ears. The ear boxes run through to their legs |
| Plate model, PA12 source | Fixed-fixed strips (span 23 mm) under the worst screw load: head 15.5 MPa, tail 14.2 MPa, against the **Materialise PA12 (SLS)** tensile strength of 48 MPa (3.1x, 3.4x). Shell density 0.95 g/cm³ from the same page (the EOS PDF returned HTTP 403) |
| Pilot margin at the crest plane | Pilot 6.5: when the lug fronts reach the head's crest plane, the pilot cylinder is 0.90 past the head pitch plane, **0.25** past the bore cylinder. Lateral window ±0.70 against the ±0.6 stack |
| Assembly sequence | The housing goes tube-first through the window from the front. Sleeve, PTFE ring and collar go on from inside through the open top. The tail stud screws are driven with an L key through the top before the controller goes in |

## 2. Numbers (`coupler.py`)

| Check | Result |
| --- | --- |
| Self-locking (tan 3 deg = 0.0524) | dry 2.86x, oiled 1.91x at the mean radius (2.08 / 1.39 at the inner end) |
| Preload at 1.5 V | typical 6.62 to 13.50 N dry, 7.87 to 17.03 oiled; guaranteed ≥ 1.76 N |
| Tension 1.223 N | lugs on the self-locking stage; faces closed at typical (5.41x) and lower-bound (1.44x) preload |
| Torsion 7.77 mN m | Hirth teeth, zero lash, independent of preload. Separation 3.79x typical, 1.01x at the lower bound. Seated lug clearance ≥ 2.29 deg |
| Bending: out-of-plane 14.7, in-plane 14.5 mN m | tipping 41.7 (2.84x), 38.8 (2.68x) |
| All loads at once | axial 3.27 N vs typical preload 2.02x; the residual clamp holds the combined bending (21.1 vs 20.6 mN m) |
| Release | 1.25 dry, 1.30 oiled |
| Mounts, plates, motor clip | as §1 |

## 3. Envelope and budgets (registered evaluator, draft)

| Item | Value |
| --- | --- |
| G1 | D 59.133 mm (margin 0.87) |
| G2 | 1081 pairs, no interference, every box inside a cavity primitive |
| G3 | every component cited |
| G4 | 31.181 g, peak 3939 mW against 19 425 mW |
| G5 | chain supported at roll 0 |

## 4. Sources checked in raw text for this version

| Source | Values | Check |
| --- | --- | --- |
| Concast C95400 | 221 MPa yield min, 7.45 g/cm³, E 107 GPa, uses | HTML table |
| Materialise PA12 SLS | 0.95 g/cm³, 48 MPa tensile, 1650 MPa modulus | HTML table |
| Engineering ToolBox | PTFE on steel 0.05 to 0.2; nylon on steel 0.4; steel on steel 0.5 to 0.8 | HTML rows |
| Vishay D/CRCW e3 (document 20035) | CRCW0402 0.65 mg | `pdftotext` |
| Henkel LOCTITE 638 TDS | 13.5 / 29 N/mm², specific gravity 1.1 | `pdftotext` |
| 206-109 | rated load, start voltage, stall | `pdftotext` |
| Wikipedia Leadscrew | steel on bronze 0.15 to 0.23 dry, 0.10 to 0.16 oiled | raw wikitext |

## 5. Originality self-check (author, not the Q61 review)

v4 passed (no high cell, 21 moderates). v5 adds a PTFE film, a bonded motor clip, two resistors and a material change. None of these is a distinctive coupler feature. The exclusions are not present.

## 6. Limitations

The declaration's `limitations` list is the record.
