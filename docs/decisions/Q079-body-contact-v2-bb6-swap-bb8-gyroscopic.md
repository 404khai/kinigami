# Q79 — Body-contact criteria v2 (BB6 swap) and the gyroscopic term (BB8)

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-19 |
| Supersedes | `criteria/fixture-validation/body-contact-v1.json`, BB6 `swap_check` only. Q35 integrator: adds the gyroscopic term. Every other criterion and threshold is unchanged |
| Provenance | **agent decision under explicit owner delegation** (the owner told the lead to proceed with the lead's recommendations for BB6 and BB8) |

## Context

Body-contact run 1 (`2d4dd12`, preserved) is not qualified.
- **BB6 fails** on a conflict inside criteria v1: "same point set when swapped" against "point on the incident face".
- **BB8 is uncertain** on angular momentum. Each impulse conserves L to 1e-12. The cause is PGS friction non-convergence leaving off-axis spin of about 1.6e-4 rad/s, which the integrator turns into L drift because it **omits the gyroscopic term** −ω×(Iω). Passing by raising the sweep count, or by narrowing the audit window, was rejected as tuning.

## Decision

1. **BB6 (criteria v2).** The swapped manifold must have the negated normal, the same depth and the same point count. Each point must equal the (A, B) point translated by the depth along the (A, B) normal. This is the incident-face rule applied consistently. This post-hoc correction of a contradictory criterion is registered before run 2, following the Q53 precedent. Run 1 stays as reported.
2. **BB8 (solver: rigid-body integrator).**
   - Add the gyroscopic term to every dynamic body, implicitly. One Newton step in the body frame per step, following the standard stable form for stiff spins: solve I(ω₂ − ω₁) + h·ω₂×(Iω₂) = 0. This is a model improvement, not a tuning.
   - It applies to all worlds, so it can change final-state hashes of the existing qualified slices.
   - Those slices are therefore **re-run** under their unchanged criteria as new runs: analytic-v1 run 3, compliant-link-v2 run 3, coupler-engagement-v2 run 3. Their **outcomes must still pass**. Changed hashes are expected and recorded, not hidden.
   - If an outcome changes, the integrator change is reverted and reported.
   - The protocol's 100 sweeps and every threshold are unchanged.
3. Body-contact **run 2** uses criteria v2.
