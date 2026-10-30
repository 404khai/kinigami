# Q46 — Slice 1 analytic validation cases and validation-only forces

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-10-30 |
| Supersedes | — |
| Provenance | condensed from owner decision (approval of Option A with refinements) |

## Context

Q40 and Q41 require slice 1's analytic validation cases to be preregistered before any production solver code exists. Several useful cases need a known external load on a fixture. Q31 forbids external stabilization in benchmarks, and Q36 forbids unmodeled forces in docking, but neither covered validation runs on neutral fixtures.

## Decision

**Option A is approved, with refinements.** Slice 1 includes all five analytic validation cases:

1. Rest and equilibrium.
2. Free fall before contact.
3. Static friction threshold and transition to sliding.
4. Sliding to a stop.
5. Tipping threshold.

**Validation-only external forces** are permitted on neutral fixture bodies. Every such input is explicit and recorded:

- force and torque
- application point
- coordinate frame
- timing

They are never available in benchmark or controller runs, and the evaluator rejects validation-only force inputs in those run types.

**Run class.** These runs carry the explicit run class `fixture_validation`. They cannot be used as benchmark evidence or Kin-candidate evidence.

## Refinements and constraints

- This approval does **not** freeze the friction law, friction coefficients, time unit, physics timestep, or numerical tolerances. Each remains a separate open decision.
- Friction transition tests use cases below and above the threshold. They never rely on exact equality at the transition.
- Sliding-to-stop expectations are derived from the friction model selected later.
- The tipping fixture's support geometry, center of mass, and force application point are defined explicitly. If rounded-edge geometry prevents a clean analytic reference, a separate fixture with analytically defined support geometry is used.
- One fixture geometry is not assumed to serve all five cases.

## Alternatives considered

- **B. Only the cases that need no applied force (rest, free fall, sliding to a stop):** would leave the friction threshold and tipping unvalidated before chain work.
- **C. Option A plus a tilted-gravity variant:** conflicts with Q21's level tabletop under Earth gravity.

## Consequences

- The production physics solver is still not implemented until the **complete** slice 1 criteria, reference conditions, and tolerances are preregistered and hashed.
- The evaluator needs a run-class concept, and must reject validation-force inputs outside `fixture_validation`.
