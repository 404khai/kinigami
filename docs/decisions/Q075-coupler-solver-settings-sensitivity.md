# Q75 — Coupler-engagement solver-settings sensitivity study (preregistered)

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-07 |
| Supersedes | — (implements Q74 §3.1 and PHY-016 for the coupler slice; changes no criterion, setting or result) |
| Provenance | **agent decision under explicit owner delegation** |

## Context

R8 is qualified for the fixture coupler stand-in (run 2, `afd29a8`, criteria v2, Q60), but R8's status records "coupler solver-settings sensitivity not studied". PHY-016 requires sensitivity to solver settings for every qualified capability. Q54 did this for the compliant link. This record declares the coupler study **before it runs**.

## Decision

1. **Label:** `exploratory`. The study never changes the official settings, the outcomes or run 2, and it gives no verdict on the variants.
2. **Criteria:** `criteria/qualification/coupler-engagement-v2.json`, unchanged. Every variant runs the full C1–C10 suite with the same outcome rule.
3. **Variants:** the same nine as Q54, each one setting changed from the protocol baseline (contact as the protocol; 100 iterations; warm start on; midpoint-prediction link form, q = 1/4):
   - `baseline`
   - `iterations_10`, `iterations_25`, `iterations_50`, `iterations_200`
   - `no_warm_start`
   - `q_0`, `q_0.5`
   - `backward_euler` (link form backward Euler, q = 1)
4. **Implementation:** reuse `link_suite.sensitivity_variants` through a new `kinigami-qualify --coupler-sensitivity <dir>` mode that writes one report per variant. Non-protocol runs must be labelled exploratory, enforced as in the link suite. No solver, evaluator or criteria code changes.
5. **Reported:** per variant, the case outcomes and the worst margin of each metric, together with the baseline equality check. The baseline must reproduce run 2's outcomes and final-state hashes, or the study is invalid and is reported as such. Results go in `results/qualification/coupler-engagement-v1/sensitivity-<rev>/` with a README.
6. **Interpretation rule, fixed now:**
   - A capability is **settings-sensitive** for a case if a variant changes that case's outcome.
   - It is **settings-robust** if no variant does.
   - A change of a metric value without an outcome change is reported but does not count as sensitivity.
   - Expected failures of deliberately weak settings (for example 10 iterations) are documented, not explained away.
