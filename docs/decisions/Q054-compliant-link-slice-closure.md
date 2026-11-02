# Q54 — Closing the compliant-link slice: solver-settings sensitivity, limits, reference, envelope

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-02 |
| Supersedes | — (scopes the R7 objective; amends no criteria) |
| Provenance | **agent decision under explicit owner delegation** ("what's left to finish this up? work on it and make the decisions"). The owner may revise it through a superseding record |

## Context

Run 2 (`5f04229`, criteria v2, Q53) passes L1–L10. Four items still stand between that result and closing R7:

- PHY-016 (in force) requires sensitivity to solver settings for every qualified capability. Only timestep sensitivity exists.
- The R7 objective lists "limits", and PHY-002/PHY-004 mention limits and failure behavior.
- R7 asks for "an independent reference comparison".
- The stiff grid point is never dynamically resolved.

## Decision

### 1. Solver-settings sensitivity study (PHY-016), declared before it runs

- **Label:** `exploratory`. It never changes the official settings, outcomes, or run 2.
- **Criteria:** v2 unchanged, with the full L1–L10 suite per variant and the same outcome rule.
- **Variants,** each changing one setting from the protocol baseline (100 sweeps, warm start on, q = 1/4, midpoint-prediction link form):

  | Variant | Change |
  | --- | --- |
  | `iterations_10`, `_25`, `_50`, `_200` | Gauss–Seidel sweeps |
  | `no_warm_start` | Warm start off |
  | `q_0`, `q_0.5` | Prediction coefficient (q = 0 is an explicit spring with implicit damping) |
  | `backward_euler` | Link rows use C̃ = C_n + h·Jv′ with no step-start compensation: the conventional soft constraint |

- **`backward_euler` is a control.** Q52's rationale predicts ζ_num ≈ ω·Δt/2 for it. Its expected L7 failure shows that the L7 check discriminates (PHY-006). It is never a candidate setting.
- **Reported:** per-variant case outcomes and worst margins, in `results/qualification/compliant-link-v1/sensitivity/`.
- **No verdict on the variants.** The study documents behavior. Changing official settings would need its own decision and a rerun.

### 2. Link load limits and failure: deferred to the coupler slice (R8)

The Q52 fixture link is declared **unlimited**: no force or moment limit, and no failure. Limits and failure are properties of a coupler mechanism (CPL requirements, Q40), and they depend on link release and topology change (PHY-003), which Q52 explicitly left to slice 3. The "limits" item of the R7 objective moves to R8. PHY-002 and PHY-004 stay in force, with limits and failure to be verified there.

### 3. Independent reference

For the two-body slice, the closed-form references of Q52 and Q53 are exact and solver-independent. They satisfy R7's "independent reference comparison", as `docs/qualification/backend-checklist.md` already states. The joint-coordinate reference (PHY-009) is required when chains of three or more bodies are qualified. PHY-009 stays open.

### 4. Envelope

The stiff grid point's dynamics stay `outside_envelope` (ω·Δt ≥ 0.5 at every grid timestep). Using a stiff link dynamically requires a new criteria version with a finer timestep. That is not needed until a coupler stiffness is declared (R8, CPL-011).

### 5. Recordings

Links in recordings are decided separately in Q55.

### 6. R7 status

R7 closes as **qualified for fixture links within the declared envelope** once item 1's results are recorded.
