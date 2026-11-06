# Q69 — Gate 1 run 3 disposition (cand-a v3)

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-06 |
| Supersedes | — (changes no criterion, threshold or verdict) |
| Provenance | **agent decision under explicit owner delegation** |

## Context

Run 3 (`results/gates/gate1-v1/run3-447dc70-ReleaseSafe.json`, clean tree, unchanged criteria) gives cand-a v3 `fail` on G6. All other items pass.

## Findings

1. **The roll-in arc is wrong, and the error is the lead's.** It originates in the lead's v2 spec (Q66 §3).
   - When B rolls toward −x onto F0, the pivot is the bottom vertex P = (+R/2, −a) in B's frame.
   - A neighbour's peg on the common axis starts at B's other bottom vertex (−R/2, −a). It travels the arc of radius R about P to the face centre, passing about (−9.3, −9.3) at mid-step.
   - The declared channels run from (±R, 0) over the top. Those are points of the same circles that rolling never reaches.
   - The lead verified this with the table-height condition. The v2 retention review accepted the wrong arc, so v2's channel has the same defect. v2's recorded verdict (`unresolved`) is not changed (append-only); this record notes the defect.
2. **What v3 established on paper** (reproduced by the independent reviewer):
   - the four-bar keeper with two geometric over-centre states and no spring, at class-f margins of about 5° or more;
   - the hex-in-hex roll lock;
   - the tension path and the puck journal.
3. **Originality:** pass. The new single high is Roombots D2. A future revision that adds a second high against Roombots would fail rule 2.

## Decision

- The verdict stands. cand-a v3 is rejected as declared and preserved (SEL-007).
- A v4 is the next cand-a revision, at the owner's call. It needs the corrected kinematics, then items 1–7 of `candidates/cand-a/retention-review-v3-r1.md` §6, which follow from them:
  1. re-cut the lower-half arcs (entry at the bottom vertices) and the end-plate and cap cuts;
  2. a cup, jaw and puck entry layout for arrival from below, with a swept-volume check;
  3. the end-plate opening against the yaw sweep, with class f applied per the cited table;
  4. the rod stroke shown with tolerances;
  5. a rating for the M3 shaft radial load, or an outrigger bearing;
  6. the V-notch closing force with flank friction, or drop the V-notch as a pre-alignment means;
  7. a statement that a free approach cannot start a roll-in.
- Corpus follow-ups (later record): the C4, C6, C13, C17 and C12 descriptors omit their motor-driven or SMA latches; the C23 URL resolves to a differently titled paper; Science Robotics (Q64-C22) and HAL (Q64-C24) were unreadable.
- No family is selected or abandoned. R10 stays blocked.
