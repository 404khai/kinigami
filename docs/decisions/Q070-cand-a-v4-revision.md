# Q70 — cand-a version 4: revision decisions

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-07 |
| Supersedes | — (revises a candidate; changes no criterion, threshold, protocol or verdict; Gate 1 under unchanged `gate1-v1`) |
| Provenance | **agent decision under explicit owner delegation**. The owner approved v4 with the five fixes on 2026-11-07. Lead: Claude Opus 5.5. Implementation: Claude Sonnet 5.5 |

## Context

cand-a v3 failed G6 (Q69). Its roll-in channel was cut on the mirror-image arc, which is the lead's error from Q66. A layout re-solve found a second lead error: the peg arrives at the centre about 30° from the body x axis, not from above. It also found five items that did not close as specified.

## Decision

1. **Docking face.** Docking is on F3 (the body +z face). The rest orientation is 180° about y, and the lift lobe parks at body −z. The arcs are corrected: they are centred on a landing-face vertex, run from the other landing-face vertex to the centre, and are verified with the table-height condition. The channel is 5.8 mm wide and 7.0 mm deep. The end-plate slot is ±4.545 × ±2.6 mm.
2. **Five fixes approved by the owner:**
   - **Lift-drive layout.** The lift-motor group is rotated 60° about the ring axis. M3 moves into the freed slot with an outrigger bushing, and M2 and the sector are re-placed.
   - **Roll lock.** A flat seat plus the jaw's three upper flats, which keeps ±2.6° of free roll.
   - **Tongue.** It closes at z = 0 with a semicircular notch, so it needs 4.6 mm of stroke. Clearance at the class-f stroke corners is 0.58–0.65 mm for the tongue and 0.02–0.10 mm for the jaw.
   - **Thrust.** A 304 thrust washer.
   - **V-notch.** No longer a declared pre-alignment means, because its closing ratio is only 1.0 at rated torque at μ = 1.
3. **Evaluator roll convention (recorded, not changed).** G5 mates each unit from the shortest-arc rotation, ignoring the predecessor's roll (`gate1_eval.zig` `evalRoll`). With rest orientation 180° about y, ψ = 180° reproduces unit 1's orientation, which is a physical relative roll of 0 (both units on F3). ψ = 0° flips the neighbour. v4's G5 pass at ψ = 180° is therefore the intended docked pose. A later evaluator version should state that ψ is absolute about the shortest-arc mate. Changing it now would need a new criteria and protocol revision.
4. **Accepted and reported, not hidden:**
   - The rod stroke at the class-f corners (5.04–6.11 mm) is below the 5.4 mm floor, though above the 4.6 mm now needed.
   - The thrust washer's compatibility with ±15° yaw is unresolved.
   - Load-reversal holding needs joint friction of at least 0.10–0.14, which is an assumed bound.
   - The keeper-pin envelope exceeds the r ≤ 20 rule by about 0.02 mm nominal and about 0.2 mm at the tolerance corners.
   - The M2 worm shaft has no outrigger.
   - The yaw envelope is μ ≤ 0.96 at rated torque.
   - The Roombots D2 originality high remains.
5. **Stopping rule.** If v4 fails Gate 1, cand-a revisions stop. The owner then chooses between revising cand-b or cand-c and rethinking the families.

## Consequences

v4 goes to new independent r1 reviews and Gate 1 run 4. v3 stays preserved as `declaration-v3.json` (sha256 0025a534…).
