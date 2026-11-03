# Q59 — Coupler-engagement slice: interim status, findings, and open rulings

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-03 |
| Supersedes | — (amends no criteria, protocol, or threshold) |
| Provenance | **agent decision under explicit owner delegation** ("I trust its judgement"). The owner may revise it through a superseding record |

## Context

Run 1 of the coupler-engagement suite (`results/qualification/coupler-engagement-v1/run1-f4b8e0f-ReleaseSafe.json`, clean tree, criteria v1, protocol revision 2) passes C1–C6, C9, and C10. C7 and C8 are `uncertain` because of one metric, the energy audit. The momentum, impulse-accounting, and pose audits pass on every run.

## Decision

1. **The slice is not closed.** R8 status is "partially qualified": the fixture engagement mechanism, load limits and separation, release under load, and no-unmodeled-force audits are evidenced. The energy audit and the stiff-link energy behavior are open. Nothing is reported as a pass that did not pass.
2. **No criterion, tolerance, or protocol rule changes now.** The Q57 energy allowance rationale was wrong: a semi-implicit step's KE + V fluctuates at first order in ω·Δt, not second order. Fixing it after seeing run 1 requires a superseding criteria version registered before a rerun (Q49). C8's failures are larger and occur at 50 µs too, so the same fix may not cover them. A ruling made now would be tuned to the observed numbers. The recommended path is:
   - diagnose the C8 energy creation (contact fluctuation at ω·Δt up to 0.63, activation with stored potential)
   - derive the allowance from the step map for each of those, not from the observed values
   - register criteria v2 and rerun, keeping run 1 as superseded evidence
3. **Capture-window finding is recorded, not acted on.** With the Q56 provisional parameters, capture is rare in the swept range (10 of 266 evaluated runs). Changing stand-in parameters or the sweep range needs a superseding Q56/Q57 record.
4. **Carry-overs from Q54:** link load limits and failure (C3), link release and topology change (C3, C5, C6; PHY-003), and stiff-link dynamics at a finer Δt (C7 period, damping, and numerical dissipation) are evidenced for the fixture. Stiff-link energy behavior is open per item 2.
5. **CPL-011 stays unresolved for Kin couplers.** The fixture is not a candidate (Q38, Q40).

## Consequences

- Traceability and the roadmap record this status.
- The owner decides whether to rule on the energy audit and the stand-in parameters, or to delegate again.
