# Q37 — Physical scale and validated envelope

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-10-30 |
| Supersedes | — |
| Provenance | condensed from owner decision |

## Context

Size determines which forces dominate and which components can serve as evidence. The agent's initial proposal (a 1–5 cm band) conflicted with Q1 and Q12. The owner corrected it.

## Decision

1. **Option A — centimeter-scale Kins, preserving the existing size decisions.** Q1's 30–60 mm reference size class and Q12's 60 mm stowed enclosing sphere govern. Exact dimensions and geometry remain open pending component and mechanism evidence.
2. **The reference class is not proof of feasibility.** Deployed geometry, swept volumes, mass, inertia, actuator reach, and clearances are evaluated independently.
3. **The engine flags candidates and experiments outside the validated physics operating envelope.** Such results do not count as validated feasibility passes until the relevant models are extended and validated.

## Constraints

- SI units throughout. No hidden constants or geometry assumptions tied to a particular size.
- Mass, inertia, contact geometry, actuator capability, coupler behavior, and other properties derive from the candidate model and its declared components.
- Document validated operating ranges, including when gravity, contact, friction, adhesion, electrostatics, magnetic forces, and other effects may be neglected.
- Do not assume ordinary rigid-body contact and friction adequately represent every centimeter-scale design. Where additional effects become significant, model and validate them before acceptance use.
- Flag missing parameters, unsupported effects, and extrapolation. Distinguish exploratory results from validated benchmark results.

## Alternatives considered

- **B. Millimeter class:** surface forces dominate, and component evidence is thin.
- **C. Scale-agnostic with no fixed class:** leaves the validated envelope undefined.
