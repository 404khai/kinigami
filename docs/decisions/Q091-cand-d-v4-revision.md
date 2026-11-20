# Q91 — cand-d version 4: revision decisions

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-20 |
| Supersedes | — (changes no criterion, threshold or verdict; v1 to v3 and their records are preserved) |
| Provenance | **agent decision under explicit owner delegation**. Lead: Claude Opus 5.5 (cand-d author) |

## Context

The v3 retention review (`candidates/cand-d/retention-review-v3-r1.md` §7) left G6 `unresolved`, with no contradiction and six items. Q90 started v4. The cam, Hirth faces, head flange mount, body and envelope are unchanged.

## Decision (review item → v4 change)

1. **Tail stud mount.** Two countersunk ISO 7046 M1.6 A2 screws are driven from inside the tail end plate, with their heads flush with its inner face, into blind 0.6 mm tapped holes in the 304 stud flange at z ±4.6. There is no thread in PA12. The mount is sized for tension, both bendings, the fault case, torsion and shear (worst 4.76 N per screw, 0.94 MPa on the PA12 countersink).
2. **Plate joints.**
   - Each segment shell is one SLS part: bottom, sides, end plate and inner wall. The top is a separate lid that carries no declared load.
   - The front plate is checked as a clamped plate under a nut block at the fault load: 5.9 MPa against the cited 50 MPa.
   - Every other PA12 joint in the load path follows the same rule: a countersunk screw into 304 thread. This covers the hinge ears' root legs inside the head cavity, the tail upper plate's leg in the gap, and the tail lower plate on the tail floor screwed from below.
3. **Slot lash at the contact radius.** The lash is taken at r 3.5, where a rotating lug touches first. The slots widen to 3.40:
   - indexing lash 3.17 to 3.46 deg, below half a tooth pitch;
   - phase ±0.88 deg;
   - seated clearance at least 2.29 deg.
4. **Tooth seating at the lower-bound motor.** The draw needed to tilt a unit flat through the teeth is computed: 1.25 N at μ 0.8, against 0.88 N guaranteed. If the teeth seat without flattening, the residual pitch is at most 0.73 deg, the teeth stay engaged by at least 0.23 mm, and the seat stays inside the lock stage (±0.162 against ±0.20). Retention does not depend on flattening.
5. **Reference planes.**
   - The head flange front face is the head Hirth pitch plane (crest +0.2, root −0.2).
   - Both inner lands are recessed 0.25, so they never touch.
   - The bore chamfer runs 0.4 from the land.
   - The nose chamfer is 0.3, so the sequence margin is 0.15 and the lateral window ±0.75.
6. **Small items.**
   - The flange rim band is about 0.6 mm (window r 6.4).
   - The out-of-plane load label is W × 48.0.
   - `coupler-motor`, the stud mount plates and `fasteners` are added to the retention `component_ids`.

## Order

This record, then the v4 declaration, dossier and scripts (`declaration-v3.json` keeps v3), then fresh independent retention and originality reviews of v4, then an official run.
