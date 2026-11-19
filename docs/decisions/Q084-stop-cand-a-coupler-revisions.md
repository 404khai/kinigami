# Q84 — Stop cand-a coupler revisions; scope decision to the owner

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-20 |
| Supersedes | — (changes no criterion, threshold or verdict) |
| Provenance | **agent decision under explicit owner delegation** (the owner said "do whatever"; this is the lead's announced stop rule) |

## Context

The time-boxed go/no-go for cand-a v6 = K4 + K1 (`docs/studies/coupler-k4-gonogo.md`, graft commit `883d9b6`) gave three results:
- **Self-locking: pass, dry only.** Cited μ is 0.15–0.23 dry and 0.10–0.16 oiled, against tan λ = 0.073. It is vibration-sensitive.
- **Packing: pass, conditional.** It needs five part changes, and the screw stroke is capped at 4.97 mm.
- **Jaw window: fail.** The screw top would need r 21.23 mm against the 19.97 mm allowed.

This is the eighth cand-a coupler attempt (v1–v5, the seat-frame v6, the two-pin v6, K4 + K1). Each failed for the same reason: the 40 mm cavity, holding the cell, controller, three motors and the roll-in, yaw and keeper mechanisms, leaves no room for a tolerance-robust, two-sided coupler at cited machining classes.

## Decision

1. **cand-a coupler revisions stop.** v5 is preserved (`fail`, Q73). The body, lift-lobe locomotion, corrected roll-in kinematics, four-bar lock and analysis scripts remain as reusable results.
2. **No candidate survives Gate 1, and R10 stays blocked.**
3. **The next step is a scope decision for the owner.** The lead does not take it under delegation, because the options change owner decisions or the candidate set:
   - (A) Revise cand-b or cand-c (each fails G5 and has unsized retention).
   - (B) Revisit scope, for example the Q12 60 mm envelope, or whether chain bending must be integrated in the coupler at Gate 1.
   - (C) New candidates or families that budget the coupler first.
