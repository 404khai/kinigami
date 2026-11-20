# Candidate D (`cand-d`), version 2: two-segment inline body, coupler-first

Family B (Q62 §3). Q85 started this candidate. Q86 disposed of version 1, and Q87 records the version 2 decisions.

| Field | Value |
| --- | --- |
| Result label | `exploratory` (paper gate, Q38/Q40). Nothing here is validated |
| Declaration | `candidates/cand-d/declaration.json`, SHA-256 `659810c455376de8c3450d42556f266e3c37ed6260f235a3676dec22725cc0cf`. Version 1 is preserved as `declaration-v1.json` with its dossier `dossier.md` and reviews |
| Author | Claude Opus 5.5 (engineering lead). Not a reviewer |
| Declared | 2026-11-20 |
| Criteria | `criteria/gates/gate1-v1.json` (sha `ffe13533…`), protocol revision 2 |
| Reproduce | `cd candidates/cand-d/scripts && python3 declaration_text.py && python3 gen_declaration.py --write && python3 coupler.py && python3 joint.py` |

The body, shell, joint, electronics and layout are unchanged from version 1 (`dossier.md` §2 and §2.1, `scripts/joint.py`), apart from the coupler parts below. Lengths are in mm. Axes: x along the chain (head +x), z up, origin on the joint axis.

## 1. What version 2 changes, and why (review items, Q87)

| v1 review item (§6) | v2 |
| --- | --- |
| 1. Cartridge mount not buildable (M1.6 in a 0.8 mm lip) | Two tapped 304 ears of the housing (M1.6, 1.6 thick) behind the front plate, with countersunk A2 M1.6 screws through the plate. Pull-out bears on the plate's inner face, push-in on the screw heads. Worst screw load 1.59 N, 0.26 MPa on PA12 |
| 2. Flange r 6.5 larger than the window; stack incomplete | Flange r 6.3, smaller than the lip and window (r 6.45). The stack is split into every term at IT9. Cartridge position and plate flushness set only the PA12 gap (0.3 mm minimum) |
| 3. No sleeve rear retainer, no open stop | 304 retainer collar pressed on the housing tube (ejection reaction ≤ 0.81 N). 304 stop pin dia 1 at r 5.3 in an arc groove of the sleeve face, which is the open stop and the over-travel stop (7.3 N worst, shear 9.3 MPa, bronze bearing 14.6 MPa) |
| 4. Torsion no-slip held at one corner; walking possible | **Hirth face pair**: 36 teeth, 90 deg, r 2.6 to 6.3, on the stud flange and the housing lip. Torsion and shear are carried with zero lash. Roll cannot change without axial separation, so the lugs never slide along the cam flank. No face friction is relied on |
| 5. Contamination treated unevenly | Oil cases are computed for preload, release and contact stress. The face-friction dependence is gone |
| 6. Alignment stack: tilt, joint angle, axial push | Pitch ±0.73 deg, roll ±5.5 deg (at the tip radius), yaw ≤ 1.49 deg before the teeth meet. Joint angles do not enter the coupler pose. The axial push is external (stroke 2.40 mm, about 0.31 N) |
| 7. Citations, roll window, mechanism kind | Flank friction is from Wikipedia Leadscrew only (0.35 withdrawn). Each cited number is checked in raw source text (§7). `mechanism_kind` is `friction_wedge` |
| 8. Load combinations | Each load alone, then all declared loads at once (§4) |
| 9. Supply for release | Release only with the cell at ≥ 3.5 V (3.4 V at the motor). Closing at 1.0 V |

The sleeve is now OD 6.3 with the lug tip at r 6.2 (flank line 2.65 mm). Mass is 31.109 g.

## 2. Coupler parts

- **Tail stud, one machined 304 part:**
  - flange r 6.3 × 1.0, screwed to the tail end plate, with a 36-tooth 90 deg Hirth ring on its face (pitch plane at x -11.6, teeth ±0.2);
  - pilot dia 4.0 g6, 6.2 long beyond the pitch plane, with a 0.5 × 45 deg nose. It is an entry guide only;
  - two lugs dia 3.0 g6, axis 3.6 behind the pitch plane, reaching r 6.2.
- **Head cartridge (one subassembly):**
  - **304 housing.** Tube r 2.05 to 3.5 with a 4.10 entry bore and two lug slots 3.05 wide (IT9). Front lip 0.8 thick behind the Hirth pitch plane, flush with the front plate at x 35.6. The lip has a 0.6 × 45 deg bore chamfer, 0.6 × 45 deg V lead-ins on the slots, and a stop pin. Two tapped ears are boxed separately.
  - **PTFE thrust ring**, r 3.6 to 4.4 × 0.3.
  - **C93200 sleeve.** r 3.55 to 6.3 with two helical through-slots, each an entry notch, a 20 deg capture stage (1.0 mm) and a 3 deg lock stage (0.4 mm). It has a stop arc groove in its front face and a gear ring m 0.3 z 43 at the rear.
  - **304 retainer collar.**
- **Drive.** 206-109 with a z12 pinion (ratio 3.58). Close at a 1.0 V stall, release at ≥ 3.4 V.

Cycle:
1. Presented pose, then an external axial push of 2.40 mm.
2. The pilot passes the chamfer. The lugs pass the V lead-ins and stand at the sleeve's entry notches.
3. Capture. The sleeve turns, and the 20 deg stage draws 1.0 mm. Drawing one free unit at μ = 1 needs 1.21 mN m, against 9.68 mN m available.
4. Lock. The 3 deg stage seats the Hirth faces. The sleeve turns 77.1 deg to the nominal seat, then stalls at a preload of 4.41 to 9.00 N.
5. Hold, unpowered.
6. Release at ≥ 3.4 V to the open stop. The outer flank pushes the stud out 1.4 mm, and the reaction goes into the retainer collar.

Slot extent is -24.7 to 139.6 deg, with a 15.7 deg web (1.34 mm). The over-travel stop is at 122.0 deg.

## 3. Numbers (`coupler.py`; it asserts every margin it claims)

| Check | Result |
| --- | --- |
| Axial stack (IT9 / g6: pitch plane to lug axis, lug radius, Hirth teeth on both parts, lip, PTFE ring, sleeve face to flank) | ±0.0815 → seat 3.518 to 3.681 inside the lock stage 3.40 to 3.80, **margin 0.118 each side** |
| Self-locking, tan 3 deg = 0.0524 | dry 0.15 to 0.23: **2.86x**; machine oil 0.10 to 0.16: **1.91x** (PTFE thrust holding not credited) |
| Preload (1.0 V stall) | dry 4.41 to 9.00 N; oil 5.25 to 11.35 N |
| Release (≥ 3.4 V, η 0.9 → 32.9 mN m) | worst dry 20.3 mN m (**1.62**), oil 19.3 mN m (**1.70**). The ratio does not depend on motor-to-motor variation |
| Lug on bronze flank, Hertz p0 (onset about 230) | 163 MPa at F_p_max; 209 MPa with all loads at once; 225 MPa all loads oiled; fault 252 |
| Lug root, PTFE ring, Hirth flanks | 8.1 MPa; 0.74 MPa; 0.9 MPa (provisional 0.05 mm band) |
| Stop pin; retainer; mount | 7.3 N, 9.3 / 14.6 MPa; 0.81 N, 0.02 MPa; 1.59 N per screw, 0.26 MPa on PA12 |

## 4. Declared loads and carriers

Loads are provisional modelling assumptions for the Q31 tabletop chain of five, with W = 0.3051 N.

| Load | Value | Carrier | Ratio |
| --- | --- | --- | --- |
| Tension | 4 μ W, μ = 1: 1.220 N | lugs on the self-locking lock stage (friction wedge); faces stay closed | 3.61 (F_p_min / load) |
| Torsion | 2 W × 12.7: 7.75 mN m | Hirth teeth, zero lash. The separating force ≤ 1.74 N (45 deg flanks, no flank friction) stays below F_p_min. Beyond separation, the lugs on the 304 slot sides | 2.53 |
| Shear | W: 0.305 N | Hirth teeth (radial) | 14.5 |
| Out-of-plane bending | W × 47.2: 14.4 mN m | face tipping at F_p_min × 6.3 = 27.8 mN m. Beyond it, the pilot couple (tilt ≤ 1.49 deg) | 1.93 |
| In-plane bending | joint drive limit 14.5 mN m | face tipping 27.8 mN m. Beyond it, the lug pair (lever 11.18) on the self-locking stage | 1.92 |
| **All at once** | axial 3.27 N, bending vector 20.3 mN m | teeth stay seated (1.35). The faces gap at one edge, but the units do not separate: the lugs stay locked and the pilot bounds the tilt | n/a |
| Fault | joint stall at 3.6 V: 52.2 mN m | as in-plane bending. Hertz 252 MPa means local indentation, not separation | n/a |

## 5. Pre-alignment

| Means | Window | Against |
| --- | --- | --- |
| Chamfers 0.6 / 0.5 into the 4.10 bore | lateral ±1.15 | ±0.6 mm two-unit PA12 stack. No wedging while μ < 1 (0.11 of the push at μ 0.8) |
| Pilot before lugs | lugs see ≤ 0.130 mm | ±0.6 mm V lead-ins |
| Round lugs in 0.6 × 45 deg V lead-ins | roll ±5.5 deg (tip radius) | about ±1.4 deg |
| Slot lash vs Hirth pitch | 0.38 to 0.75 deg vs half pitch 5 deg | the teeth always meet their own gaps |
| Table flatness | pitch ±0.73 deg | taken by the pilot and teeth |
| Pilot engagement | yaw ≤ 1.49 deg before the teeth | the teeth align it under the draw |
| Capture stage, then the Hirth seat | axial: travel to a stall | stack ±0.0815 |

**No capture window is claimed (CPL-006).** The approach and the 2.40 mm push are external.

## 6. Components

All are in the declaration with sources and descriptions.

| id | kind | mass mg | basis | peak mW |
| --- | --- | ---: | --- | ---: |
| L-top | structure | 924 | derived | 0 |
| L-bottom | structure | 924 | derived | 0 |
| L-side-p | structure | 786 | derived | 0 |
| L-side-n | structure | 786 | derived | 0 |
| L-inner | structure | 508 | derived | 0 |
| L-front-n | structure | 219 | derived | 0 |
| L-front-p | structure | 54 | derived | 0 |
| L-front-lo | structure | 83 | derived | 0 |
| L-front-hi | structure | 54 | derived | 0 |
| S-top | structure | 215 | derived | 0 |
| S-bottom | structure | 215 | derived | 0 |
| S-side-p | structure | 183 | derived | 0 |
| S-side-n | structure | 183 | derived | 0 |
| S-inner | structure | 554 | derived | 0 |
| S-end | structure | 595 | derived | 0 |
| cell | energy_source | 8000 | source | 0 |
| controller | controller | 2100 | source | 2220 |
| driver | other | 500 | source | 15 |
| coupler-motor | actuator | 1200 | source | 851 |
| coupler-pinion | actuator | 83 | derived | 0 |
| head-cartridge | coupler_mechanism | 5380 | derived | 0 |
| cartridge-ear-up | coupler_mechanism | 58 | derived | 0 |
| cartridge-ear-low | coupler_mechanism | 58 | derived | 0 |
| retainer-collar | coupler_mechanism | 197 | derived | 0 |
| tail-stud | coupler_mechanism | 2070 | derived | 0 |
| joint-motor | actuator | 1200 | source | 851 |
| joint-pinion | actuator | 83 | derived | 0 |
| joint-sector | structure | 241 | derived | 0 |
| hinge-plate-low | structure | 139 | derived | 0 |
| hinge-plate-up | structure | 139 | derived | 0 |
| hinge-ear-low | structure | 139 | derived | 0 |
| hinge-ear-up | structure | 139 | derived | 0 |
| hinge-pin | structure | 534 | derived | 0 |
| fasteners | structure | 2046 | derived | 0 |
| harness | other | 520 | derived | 0 |
| **total** | | **31 109** | | **3 937** |

## 7. How each cited number was checked (Q86 item 3)

| Value | Source | Check |
| --- | --- | --- |
| Steel on bronze, dry 0.15 to 0.23, oil 0.10 to 0.16; self-locking condition and "not absolute" | Wikipedia Leadscrew | raw wikitext (`index.php?title=Leadscrew&action=raw`), friction table and the self-locking paragraph |
| PTFE on steel 0.05 to 0.2; steel on steel dry 0.5 to 0.8 static, 0.42 kinetic; no dry bronze-steel row | Engineering ToolBox friction page | raw HTML table rows |
| 206-109: 1.2 g, body 6 × 18.7, shaft 2 × 3.6, rated 3 mN m, stall 9 mN m, 3 V, max 3.6 V | Precision Microdrives datasheet PDF | `pdftotext` of the PDF |
| C93200: 8.91 g/cm³, yield 138 MPa, E 100 GPa | Concast C93200 page | page text (fetch) |
| IT9: 1 to 3 mm 25 µm, 3 to 6 mm 30 µm | Wikipedia IT Grade | page table (fetch) |
| Spur gear efficiency 98 to 99.5 percent | KHK ABCs of Gearing | search-result text of the PDF (not opened). Only the 0.9 to 1.0 band, wider than the source, is used |
| PTFE specific gravity 2.15 | 3M Dyneon TF 1620 data sheet | search-result text (not opened). It enters only the 13 mg PTFE ring through the effective density |
| Cell, controller, driver, 304, PA2200, screws, wire | as cand-a v5 (G3 passed there) | not re-checked in this version |

## 8. Originality self-check (author, not the Q61 review)

The v1 review passed: no high cell and 15 moderates. v2 adds a Hirth face pair, a common machine element (crankshafts, turbine discs, indexing heads). If any corpus or search reference uses face serrations on a connector, D2 may rise to moderate against it; the reviewer decides. Nothing else visible changes. The exclusions are not present.

## 9. Expected Gate 1 outcomes (author's checks)

- **G1–G5:** pass. Registered evaluator on this declaration (draft): D 58.862 mm, 595 pairs with no interference, every component cited, 3937 ≤ 19 425 mW, chain supported at roll 0.
- **G6, G7, G8:** each needs a fresh independent review of v2.

## 10. Limitations

The declaration's `limitations` list is the record. In short:
- approach locomotion and the axial push are external;
- the friction wedge is not absolute under vibration;
- no engagement or joint sensor;
- handbook friction values;
- PA12 screw pull-out not cited for the stud flange;
- the Hirth ring is fine machining;
- possible 304-on-304 galling;
- Q31 bending adequacy at high table friction is unresolved;
- the stowed margin is 1.1 mm.
