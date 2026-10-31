# Q47 — Friction law for the first analytic validation cases

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-10-31 |
| Supersedes | — |
| Provenance | condensed from owner decision ("go with A") |

## Context

Q46 approved the five analytic fixture-validation cases but left the friction law open. The friction-threshold and sliding-to-stop cases cannot be specified until the law is known.

## Decision

**Option A — Coulomb friction with separate static and kinetic coefficients** (μs ≥ μk) is the reference friction law for the first analytic validation cases.

- **Static regime:** tangential contact force up to μs·N with no relative sliding.
- **Kinetic regime:** sliding resisted by μk·N, opposing the sliding velocity.

## Scope and limits

- This selects the **law only**. Coefficient values, tolerances, and uncertainty treatment remain separate open decisions.
- It is the reference for the analytic fixture-validation cases. It does not claim that Coulomb friction adequately represents any Kin candidate's real contacts. That is evaluated under Q37 and Q38.
- Q46 still applies: transition tests use loads below and above threshold, never exact equality.

## Alternatives considered

- **B. Coulomb with a single coefficient:** cannot distinguish correct handling of the start of sliding from correct sliding.
- **C. Regularized friction:** the smoothing adds a model parameter, so the transition is no longer cleanly analytic.
