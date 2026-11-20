# Candidate D (`cand-d`), version 3: two-segment inline body, coupler-first

Family B (Q62 §3). Started by Q85. Q86 and Q88 disposed of versions 1 and 2. Q89 records the version 3 decisions.

| Field | Value |
| --- | --- |
| Result label | `exploratory` (paper gate, Q38/Q40). Nothing here is validated |
| Declaration | `candidates/cand-d/declaration.json`, SHA-256 `0f82c5062fc83c8b9eb918e728f41b357245aeda848cf5d87989a0444ae6f8e8`. Earlier versions are kept as `declaration-v1.json` and `declaration-v2.json`, with their dossiers and reviews |
| Author | Claude Opus 5.5 (engineering lead). Not a reviewer |
| Declared | 2026-11-20 |
| Criteria | `criteria/gates/gate1-v1.json` (sha `ffe13533…`), protocol revision 2 |
| Reproduce | `cd candidates/cand-d/scripts && python3 declaration_text.py && python3 gen_declaration.py --write && python3 coupler.py && python3 joint.py` |

Unchanged from version 2 (`dossier-v2.md`):
- the body, shell, joint and electronics;
- the cam (capture stage 20 deg × 1.0 mm, lock stage 3 deg × 0.4 mm, flank radius 4.875, flank line 2.65);
- the C93200 sleeve and PTFE thrust ring;
- the Hirth faces (36 teeth, 90 deg, r 2.6 to 6.3);
- the stud, retainer collar, stop pin and drive.

All coupler depths are measured from the Hirth pitch plane. Lengths are in mm.

## 1. What version 3 changes (review v2 §7, Q89)

| v2 item | v3 |
| --- | --- |
| 1. Ears not joined to the housing | **One-piece 304 housing**: a tube plus a **front flange** (disc r 7.0 × 0.8, lobes at ±z to r 9.4) that lies on the PA12 front plate's outer face. Two countersunk ISO 7046 M1.6 A2 screws pass through the lobes and the plate into tapped 304 nut blocks (2.2 × 2.2 × 0.8). The cartridge moves 0.8 forward. The sleeve passes the plate window, and the thrust face is the flange's rear face. Head site x 36.4 |
| 2. In-plane lever at the mount | In-plane: the flange pivots on its disc edge at 7.0, and both screws hold, 1.65 N each (fault 4.34 N). Out-of-plane: pivot on a lobe tip, far screw at 17.2, 1.46 N. Pull-out 0.61 N per screw. Nut-block bearing on PA12 ≤ 1.53 MPa; thread stripping about 454 N |
| 3. Window, lip fit, flange at the PA12 corner | The flange bears on the plate face. The stud flange (r 6.3) can bear only on the head's teeth. PA12 gap outside r 6.3 ≥ 0.7 |
| 4. Tooth-to-slot phase | Slots 3.20. Phase ±1.22 deg (IT9 on tooth and slot positions, both parts) against 2.61 deg of slot lash at r 2.05. **With the teeth seated, the lugs keep ≥ 1.39 deg of clearance**, so torsion goes only through the teeth. Before the teeth meet, the lash (≤ 3.12 deg) is below half a pitch (5 deg) |
| 5. F_p lower bound | Datasheet guaranteed rows (rated 3 mN m at 3 V; max start voltage 0.5 V): stall ≥ 1.2 (V − 0.5) mN m, so **F_p ≥ 0.88 N** at 1.0 V. **Tooth engagement does not depend on F_p.** While self-locked, an axial load 20 N above the preload opens the faces by ≤ 0.001 mm (loop stiffness lower bound 20 kN/mm; the lugs alone 194 kN/mm), against 0.39 mm teeth, so roll stays within 0.013 deg. F_p decides face contact only |
| 6. PTFE notch, Hirth area, tipping lever | The PTFE ring has two lug notches and is keyed by them. The slots remove 33 % of the head ring; the in-plane tipping edge is at y 5.90 |
| 7. Pilot margin | Bore chamfer 0.4: the pilot is 0.20 past the chamfer when the lugs arrive. Lateral window ±0.95 (stack ±0.6) |

## 2. Numbers (`coupler.py`, which asserts each claimed margin)

| Check | Result |
| --- | --- |
| Axial stack (IT9 / g6, every term split) | seat 3.518 to 3.681 in the lock stage 3.40 to 3.80, margin 0.118 each side |
| Self-locking (tan 3 deg = 0.0524) | dry 0.15 to 0.23: 2.86x; oil 0.10 to 0.16: 1.91x |
| Preload at 1.0 V | typical 4.41 to 9.00 N dry (5.25 to 11.35 oiled); guaranteed ≥ 0.88 N |
| Tension 1.220 N | lugs on the self-locking stage; faces closed at typical F_p (3.61x), micrometre gap possible at the lower bound (0.72x) |
| Torsion 7.75 mN m | Hirth teeth, zero lash; separation ratio 2.53 at typical F_p; engagement independent of F_p |
| Shear 0.305 N | Hirth teeth |
| Out-of-plane bending 14.6 mN m | tipping 27.8 (1.90x); then the pilot couple (tilt ≤ 1.49 deg) |
| In-plane bending 14.5 mN m | tipping about y 5.90: 26.0 (1.80x); then the lug pair on the self-locking stage |
| All loads at once | axial 3.27 N < typical F_p (1.35x); faces gap at one edge under the combined bending; no separation |
| Release (cell ≥ 3.5 V, 3.4 V at the motor) | 20.3 mN m needed (19.3 oiled), 32.9 available: 1.62 (1.70) |
| Hertz, lug on bronze (onset about 230) | 163 / 209 / 225 oiled / fault 252 MPa |
| Stop pin; retainer | 7.3 N, 9.3 / 14.6 MPa; 0.81 N |

## 3. Pre-alignment

The windows are unchanged from v2 except as listed below. **No capture window is claimed (CPL-006).**

| Window | Value | Against |
| --- | --- | --- |
| Lateral | ±0.95 | stack ±0.6 |
| Pilot-before-lug | margin 0.20 | n/a |
| Roll | ±5.5 deg (tip radius) | about ±1.4 deg |
| Lug indexing | 2.61 to 3.12 deg | below half a tooth pitch |
| Pitch | ±0.73 deg | n/a |
| Yaw | ≤ 1.49 deg before the teeth meet | n/a |

The axial push (2.40 mm, about 0.31 N plus chamfer friction) is external: the Q31 start configuration or a later approach design.

## 4. Envelope and budgets (registered evaluator, draft)

| Item | Value |
| --- | --- |
| G1 | D 58.862 mm. The flange protrusion does not set the sphere |
| G2 | 630 pairs, no interference, every box inside a cavity primitive (`head-flange-envelope` added for the flange) |
| G3 | every component cited |
| G4 | 31.103 g, peak 3937 mW against 19 425 mW |
| G5 | three-unit chain supported at roll 0 |

## 5. Sources

Each was checked as in `dossier-v2.md` §7. New in v3:
- the 206-109 rated load and maximum start voltage, from `pdftotext` of the datasheet (rows 13 and 16);
- the ISO 7046 countersunk M1.6 head (dk 3.0, k 0.96), quoted as a standard dimension. It enters only the head clearance; the screws are in the lumped fastener mass.

## 6. Originality self-check (author, not the Q61 review)

v2 passed with no high cell; its review found Hirth faces in modular robots (Beckhoff, a Xerox patent) and rated them moderate. v3 adds a screwed front flange to the housing, a generic element. The exclusions are not present. The reviewer decides.

## 7. Limitations

The declaration's `limitations` list is the record.
