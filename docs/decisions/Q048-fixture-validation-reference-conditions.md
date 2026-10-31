# Q48 — Reference conditions and tolerances for the analytic fixture-validation cases

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-10-31 |
| Supersedes | — |
| Provenance | **agent decision under explicit owner delegation** ("make the decisions for those questions"). The owner may revise any value through a superseding record |

## Context

Q46 fixed the five analytic cases and Q47 the friction law. Before the solver can be written, the remaining reference conditions and tolerances must be preregistered (BEN-008, BEN-014, ENV-002, TIM-012). The owner delegated these choices to the implementation agent.

## Guiding principle

These cases check the **solver against closed-form mechanics** at declared conditions. Every value below is a **solver-validation parameter**, not a claim about any real material, tabletop, or Kin candidate. Values are chosen so that each case is analytically clean, self-consistent across the whole parameter grid, and inside the Q1 30–60 mm reference scale. Consistency checks are encoded in the criteria and enforced by tests.

## Decision

1. **Friction coefficients (Option A): a preregistered grid,** Coulomb law per Q47.

   | Grid ID | μs | μk |
   | --- | --- | --- |
   | `mu_low` | 0.3 | 0.2 |
   | `mu_mid` | 0.6 | 0.45 |
   | `mu_high` | 0.9 | 0.7 |

   The grid spans the order of magnitude typical of dry contacts. Every pair has μs > μk, so starting to slide and continuing to slide are distinguishable. Every case is evaluated at all three pairs.

2. **Gravity:** standard gravity, g_n = 9.80665 m/s² (an exact defined constant), acting along world −z. The tabletop is the world plane z = 0.

3. **Fixtures:** two neutral, uniform-density, sharp-edged cuboids. These are not Kin candidates.

   | ID | Size (x × y × z) | Mass | Used by |
   | --- | --- | --- | --- |
   | `fixture_flat_block` | 40 × 40 × 20 mm | 0.040 kg | rest, free fall, friction threshold, sliding to a stop |
   | `fixture_tall_block` | 20 × 20 × 60 mm | 0.030 kg | tipping |

   Inertia follows from the uniform solid cuboid. Sharp edges make the support polygon and tipping pivot exact. Per Q46, no single fixture serves every case, and the rounded-edge block is not needed for these analytic references.

4. **Time:** a time unit of 1 µs (1/1,000,000 s). The physics step grid is **0.5 ms, 1 ms, 2 ms** (500, 1000, 2000 ticks).

5. **Outcome rule and uncertainty treatment (PHY-008):** each case is evaluated at every (friction pair × timestep) combination that applies.
   - A case **passes** only if every combination passes.
   - It **fails** if every combination fails.
   - Any mixed outcome is **uncertain**.

6. **Thresholds are never tested at equality** (Q46). Below-threshold loads are 0.9× the analytic threshold, and above-threshold loads are 1.1×.

7. **Tolerances:** fixed per case in `criteria/fixture-validation/analytic-v1.json`. Their principles:
   - **Statics** (force balance): 1e-3 relative. This is tight enough to expose force-accounting errors, and loose enough for an iterative implicit solver's convergence tolerance.
   - **Integration-order-aware kinematics:** free-fall velocity must be exact to 1e-9 relative, because any consistent integrator is exact for constant acceleration. Position error is bounded by g·Δt·t, which admits first-order integrators of either sign.
   - **Event timing** (stopping time): within 2 steps.
   - **Distances:** 1% relative plus one step of travel (v0·Δt).
   - **Rigid-limit sanity:** maximum penetration 0.1 mm. Static drift is 1e-6 m or 1e-6 rad at rest, and 1e-5 m under a sub-threshold load to allow for tangential compliance.
   - **Tipping:** at most 1e-3 rad below threshold, at least 0.1 rad within 1 s above threshold, and pivot slip of at most 0.1 mm before 0.05 rad of tilt.

## Alternatives considered

- **Friction from a named material pair:** adds a material-evidence question these solver checks don't need.
- **A single friction pair:** risks a solver that is only correct at one point.
- **A single timestep:** cannot separate solver error from step-size artifacts, and conflicts with the Q35 sensitivity requirement.
- **Rounded-edge fixtures:** fillets blur the support polygon and pivot, so the analytic reference is no longer exact.

## Consequences

- Criteria file `criteria/fixture-validation/analytic-v1.json` is preregistered and hashed before any production solver code (BEN-008).
- Contact stiffness and solver settings are solver configuration. They are recorded with each run but are not acceptance criteria. The criteria check only model-independent quantities, plus the penetration sanity bound.
- Passing these cases yields `fixture` results only (Q46). It qualifies nothing beyond these conditions.
