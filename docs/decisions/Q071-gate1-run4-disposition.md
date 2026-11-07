# Q71 — Gate 1 run 4 disposition (cand-a v4)

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-07 |
| Supersedes | — (changes no criterion, threshold or verdict) |
| Provenance | **agent decision under explicit owner delegation** |

## Context

Run 4 (`results/gates/gate1-v1/run4-e5c6521-ReleaseSafe.json`, clean tree, unchanged criteria) gives cand-a v4 `unresolved`. G6 is unresolved. G1–G5, G7 and G8 pass.

## Findings

1. **The roll-in kinematics error of Q69 is fixed.** The independent reviewer recomputed the peg path from scratch with the table-height condition. They also reproduced the four-bar, the torsion and the release figures.
2. **What remains unsupported** (retention review v4 r1, §7):
   - class f is applied to the rocker pivot, stops and crank axis, but those are carried by PA12. At the cited ±0.3 mm, the margin past dead centre goes negative and the stroke is 4.41 mm against 4.6 mm needed.
   - the M3 bore play of 0.3 mm is not accounted for.
   - the vertical closure stack of about 0.05 mm does not include the SLS height tolerance of both units.
   - the alignment windows are stated at the slot, not at the jaw (0.03–0.12 mm upward margin).
   - the flat thrust washer allows only about 3° of yaw under tension, against ±12° declared.
   - stem-slot friction is missing from the release force; with it, release needs about stall torque at μ = 1.
   - no PA12 bearing allowable is cited.
3. **Q70's stopping rule.** The rule was worded for a v4 *fail*. v4 is `unresolved`, not `fail`, so the rule does not trigger. Even so, a further revision goes to the owner, as promised in the lead's report.

## Decision

- The verdict stands, and v4 is preserved (SEL-007). No survivor exists. R10 stays blocked.
- The owner decides the next step:
  - (a) A cand-a v5 that carries the four-bar on one machined 304 frame. This removes the PA12 tolerance from the lock and the stroke. It also needs a jaw lead-in or compliance for the vertical stack, a yaw-compatible thrust face or a reduced declared yaw, and the friction and allowables fixes. All of these are tolerance and part-engineering items, not concept errors.
  - (b) Revising cand-b or cand-c.
  - (c) Rethinking the families.
- The lead recommends (a).
