# Q60 — Coupler-engagement criteria v2: energy audit, activation accounting, capture-zone consistency

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-03 |
| Supersedes | **Q57's energy-audit allowance and Q56 §6's capture-zone size, for criteria v2 only.** Q57's case list, every other tolerance, and criteria v1 stay as registered. Run 1 (v1) is kept as superseded evidence. Completes the open rulings of Q59 |
| Provenance | **agent decision under explicit owner delegation** ("I trust its judgement"). The owner may revise it through a superseding record |

## Context

Run 1 (`results/qualification/coupler-engagement-v1/run1-f4b8e0f-ReleaseSafe.json`, clean tree) passed C1–C6, C9, and C10. C7 and C8 were `uncertain` on one metric, `energy_creation_over_allowance`. Q59 recorded this and ruled nothing. Two causes have since been identified **from the step map and the declared parameters, not by fitting to the observed values**.

1. **First-order energy fluctuation (C7).** Q57 assumed the energy error of the link step is second order, (ω·Δt)²/4. A semi-implicit step conserves a shadow energy, and KE(vₙ) + V(xₙ) differs from it at **first** order: the deviation is bounded by ω·Δt/2 of the oscillation energy. Run 1 measured 0.0253 / 0.0511 / 0.1041 of E_ref at ω·Δt = 0.05 / 0.1 / 0.2, i.e. ω·Δt/2. Q57's rationale was wrong.
2. **Activation accounting and a self-inconsistent capture zone (C8).**
   - The link's stiffness and its limits both scale with e, so the stretch at which a link overloads is limit/k, **independent of e**: 0.2 mm axial, 0.1 mm shear.
   - Q56's capture zone (0.2 mm radial, ±0.2 mm axial) plus the 0.05 mm preload offset admits an activation stretch of up to about 0.25 mm. A ball entering the zone's edge therefore overloads on its first active step. This is why run 1 captured rarely.
   - The pawl work at activation (the link going from no rows to ½·e·Σk·C², with C ≠ 0) was never credited, so the energy audit counted real, actuator-supplied potential as created energy.

## Decision

**Criteria v2** (`criteria/qualification/coupler-engagement-v2.json`, registered before any code change or rerun) and **protocol revision 3** change exactly:

1. **Energy allowance.** The allowance becomes (`creation_rel_tol` + `first_order_omega_dt_coefficient` · ω_ref · Δt) · E_ref + floor. The coefficient is **1.0**: twice the first-order shadow-energy bound ω·Δt/2, matching the factor-of-two convention of the original audit. ω_ref is
   - √(k_axial,full / μ_reduced) (about 1000 rad/s) when every evaluated sample is contact-free, and
   - the larger of that and √(k_seat / μ_reduced), with k_seat = 4·k_contact·sin²α, when the final sample carries guide contact.

   The contact term is the stiffness the final-sample contact potential is stored in. The audit is then coarse for contact-bearing runs at large Δt (the allowance can approach the oscillation energy). That is a stated property of the check. For those runs the momentum, impulse-accounting, and pose audits carry the CPL-004 evidence.
2. **Pawl work at activation is credited.** When the link goes from no rows to rows, the pawl supplied ½·Σ k_i,full · C_i² · e_after (C from that step's report). The solver reports it in `pawl_work_j`, and the evaluator credits it in W. Linked to Q58: W through step n−1 pairs with sample n.
3. **Capture-zone self-consistency rule.** A capture zone must satisfy, for the preload offset δ:
   - axial: capture_axial + δ < limit_tension / k_axial,
   - radial: capture_radial < limit_shear / k_shear,
   - combined: √(capture_radial² + (capture_axial + δ)²) < limit_tension / k_axial.

   The parser enforces it for criteria version ≥ 2 only, so v1 still parses and run 1 stays reproducible. v1's zone violates it. v2's zone is **0.05 mm radial, 0.1 mm axial**: 0.15 mm, 0.05 mm, and 0.158 mm against 0.2, 0.1, and 0.2 mm. The zone is chosen as the rounded-down largest value satisfying the rule with a margin, not by reference to any sweep outcome.
4. **Sweep misalignments** become {0, 0.005, 0.15} rad. The bend limit of the latch link is M_lim/k_bend = 0.01 rad, and nothing in the fixture can rotate a ball-in-socket body toward alignment, so 0.15 rad is expected never to latch and 0.005 rad is the informative value inside the limit. This is reported, not gated (CPL-006).

Nothing else changes: all tolerances, the case list, setups, solver settings, the stand-in's physical parameters, and the C9 requirement.

## Safeguards (Q49)

- This change is **post-hoc**, made after run 1. This record and criteria v2 are committed, and v2's hash is registered, **before** any code change and before the rerun.
- Run 1 and its README are preserved. Run 2 (v2) is the reported result if produced at a clean tree. C1–C6, C9, and C10 are expected unchanged except that C8 and C9 use the new zone and misalignment list.
- The deviations are all derived from the step map or the declared parameters. None was tuned to move an outcome, and the rule in item 3 would have rejected v1's zone.
- The same agent wrote the criteria and the code. The mitigation is the C9 controls, which still must trip, and the unchanged regression gates (63 and 60 final-state hashes).
- If run 2 still fails, that is reported as found. Another ruling would need another record.

## Consequences

- `coupler_criteria.zig` parses v2 with a defaulted `first_order_omega_dt_coefficient` (0.0 for v1) and the version-gated rule.
- The suite's official criteria become v2. Run 2 is the next result.
