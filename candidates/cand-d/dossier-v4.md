# Candidate D (`cand-d`), version 4: two-segment inline body, coupler-first

Family B (Q62 §3). Started by Q85. Q86, Q88 and Q90 disposed of versions 1 to 3. Q91 records the version 4 decisions.

| Field | Value |
| --- | --- |
| Result label | `exploratory` (paper gate, Q38/Q40). Nothing here is validated |
| Declaration | `candidates/cand-d/declaration.json`, SHA-256 `21bebbe5812f9a4f41f43c0868634afceb6cf75972174e0f7e2924a0beccb978`. Earlier versions are kept as `declaration-v1.json` to `declaration-v3.json`, with their dossiers and reviews |
| Author | Claude Opus 5.5 (engineering lead). Not a reviewer |
| Declared | 2026-11-20 |
| Criteria | `criteria/gates/gate1-v1.json` (sha `ffe13533…`), protocol revision 2 |
| Reproduce | `cd candidates/cand-d/scripts && python3 declaration_text.py && python3 gen_declaration.py --write && python3 coupler.py && python3 joint.py` |

Unchanged from version 3 (`dossier-v3.md`, `dossier-v2.md`):
- the body, joint, electronics and envelope;
- the cam, sleeve, PTFE ring, Hirth faces and stud;
- the head flange mount, retainer and stop pin;
- the drive and the supply rules.

## 1. What version 4 changes (review v3 §7, Q91)

| v3 item | v4 |
| --- | --- |
| 1. Tail stud mount in PA12 thread, unsized | Countersunk ISO 7046 M1.6 A2 screws are driven from inside the tail end plate (heads flush) into blind 0.6 mm holes of the 304 stud flange at z ±4.6. There is no PA12 thread. Per screw: tension 0.61 N, in-plane 1.76 N (fault 4.76), out-of-plane 1.96 N. Torsion 0.85 N in shear (0.44 MPa on PA12). Worst countersink bearing 0.94 MPa. Thread stripping about 341 N |
| 2. Plate joints, plate as a beam | Each segment shell is **one SLS part** (bottom, sides, end plate, inner wall). The top lid is separate and carries no declared load. Front plate under a nut block at the fault load (clamped plate, Roark): 5.9 MPa against the EOS PA 2200 tensile strength of 50 MPa. Hinge ears and plates are 304 with root legs (two inside the head cavity, one in the gap, and the lower plate on the tail floor), each fixed by a countersunk screw into 304 thread. Worst ear force 1.42 N, pin bearing 0.47 MPa |
| 3. Slot lash at the wrong radius (the lead's error, Q90) | Lash is taken at the contact radius 3.5, with slots 3.40. Indexing 3.17 to 3.46 deg (< 5 deg half pitch). Phase ±0.88 deg. **Seated clearance ≥ 2.29 deg** |
| 4. Teeth meshing at the lower-bound motor | To tilt a unit flat through the teeth needs 1.25 N (μ 0.8), against 0.88 N guaranteed (4.41 N typical). **Fallback:** the teeth seat with ≤ 0.73 deg residual pitch, stay engaged by ≥ 0.23 mm, and the seat stays in the lock stage (±0.162 against ±0.20). Retention does not need flattening |
| 5. Reference planes | The head flange face is the head pitch plane (crest +0.2, root −0.2). The inner lands of both parts are recessed 0.25 and never touch. The bore chamfer is 0.4 from the land, the nose chamfer 0.3. Sequence: the pilot cylinder is 0.80 past the head pitch plane, 0.15 past the bore cylinder (0.65), when the lugs arrive. Lateral window ±0.75 (stack ±0.6) |
| 6. Small figures | Rim band about 0.6 mm (window r 6.4). Out-of-plane load W × 48.0 (pitch). Retention `component_ids` add `coupler-motor`, the stud and front plates, and `fasteners` |

## 2. Numbers (`coupler.py`, which asserts each claimed margin)

| Check | Result |
| --- | --- |
| Axial stack | seat 3.518 to 3.681 in the lock stage 3.40 to 3.80 (0.118 each side) |
| Self-locking | 2.86x dry, 1.91x oiled (at the mean flank radius; the reviewer gives 2.08 / 1.39 at the inner end of the flank line) |
| Preload at 1.0 V | typical 4.41 to 9.00 N; guaranteed ≥ 0.88 N. Tooth engagement is independent of preload (a 20 N excess opens ≤ 0.001 mm against 0.39 mm teeth) |
| Tension 1.225 N, torsion 7.75 mN m, shear 0.306 N | lugs on the self-locking stage; Hirth teeth; Hirth teeth |
| Bending: out-of-plane 14.7, in-plane 14.5 mN m | tipping 27.8 (1.89x) and 25.9 (1.78x, edge y 5.87, slots remove 35 % of the head ring) |
| All loads at once | teeth stay seated at typical preload (1.35x); faces gap at one edge; no separation |
| Release (cell ≥ 3.5 V) | 1.62 dry, 1.70 oiled |
| Hertz, lug on bronze (onset about 230) | 163 / 209 / 225 oiled / fault 252 MPa |

## 3. Envelope and budgets (registered evaluator, draft)

| Item | Value |
| --- | --- |
| G1 | D 58.862 mm |
| G2 | 741 pairs, no interference, every box inside a cavity primitive |
| G3 | every component cited |
| G4 | 31.222 g, peak 3937 mW against 19 425 mW |
| G5 | chain supported at roll 0 |

## 4. Originality self-check (author, not the Q61 review)

v3 passed (no high cell, 21 moderates). v4 adds generic fasteners, root legs and a wider slot. The exclusions are not present.

## 5. Limitations

The declaration's `limitations` list is the record.
