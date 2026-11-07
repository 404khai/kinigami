# Q74 — Pause candidate revisions; proceed with R8 follow-ups

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-07 |
| Supersedes | — (resolves the owner decision of Q73; changes no criterion, threshold or verdict) |
| Provenance | **agent decision under explicit owner delegation** (the owner said "do what you think is best", prefers to forge ahead and not to start a v6) |

## Decision

1. **Candidate revisions are paused.**
   - cand-a stays at v5, `fail` on G6 (Q73).
   - The v6 work list in Q73 and in `candidates/cand-a/retention-review-v5-r1.md` §7 is kept as the starting point if the owner reopens candidates.
   - cand-b and cand-c stay at v1.
   - No family is abandoned or selected.
2. **Gate 1 is not bypassed.** R10 (Kin subsystem models) stays blocked until a Gate 1 survivor exists (Q38, roadmap). A Kin model built without one would be unfounded design selection.
3. **Next work is candidate-independent R8 follow-ups,** in this order:
   1. **Coupler solver-settings sensitivity study.** Exploratory, preregistered in the style of Q54 before it runs, with no solver change.
   2. **Body-body (cube-cube) contact slice.** It closes the 256/648 sweep runs reported `outside_model` (R8 status). Its validation criteria must be committed and hashed before any solver code is written (AGENTS preregistration rule).
4. **Candidate work resumes** when the owner asks, or when the body-body contact slice is qualified. At that point unit-to-unit contact can also inform coupler design.

## Rationale

Five cand-a versions converged on coupler tolerance stacks in a 40 mm cavity, and each fix exposed the next margin. The R8 follow-ups produce durable, validated capability whatever candidate is eventually chosen. Every Kin will need body-body contact.
