# Q53 — Compliant-link L2 bending reference: exact statics with the tension lever

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-02 |
| Supersedes | **Q52 §5, L2 row: the bending-moment reference `F·(cube half-size)` and the bending-angle reference `moment/k_bend` derived from it.** Every other part of Q52, including all L2 tolerances, stands |
| Provenance | **agent decision under explicit owner delegation** ("own it end to end, make the decisions and resolve it"). The owner may revise it through a superseding record |

## Context

Run 1 of the compliant-link suite (`results/qualification/compliant-link-v1/run1-77bc3ca-ReleaseSafe.json`, preserved) passed 9 of 10 checks. **L2 failed** at all nine combinations. Shear force and shear displacement were exact (≤ 1.5e-11), but the bending moment deviated from `F·h` by 16.4 % (soft), 1.92 % (mid), and 0.196 % (stiff), identically at every Δt.

`F·h` is not the static moment of the L2 setup. Body B hangs under tension T = m·g. When it rotates by φ, its centre of mass moves under the anchor, and gravity's lever about the anchor opposes the lateral load: the pendulum-stiffening effect. The exact equilibrium of B about its centre of mass is

  k_bend·φ = h·(F·cos φ − T·sin φ),  M = k_bend·φ,

with h the anchor-to-centre lever (half the cube edge) and F = 0.1·m·g. This equation is the rigid-body statics of the declared Q52 link model. It contains no solver quantity and no free parameter. Solved independently, it predicts deviations from `F·h` of 0.164078787944781 / 0.019237821095197 / 0.001957509823605, which match run 1 to 13 significant digits.

So run 1's L2 failure measured an error in the **reference**, not in the solver. Under v1, a correct solver cannot pass L2, and a solver that did pass it would be wrong.

## Decision

1. **L2 moment and angle references.** φ_ref is the root of k_bend·φ = h·(F·cos φ − T·sin φ) on [0, π/2], found by 200 bisection halvings (deterministic). It is unique there, because the left side increases and the right side decreases. M_ref = k_bend·φ_ref. T is the closed-form tension m·g, not a measured value.
2. **Tolerances are unchanged:** moment 1e-3, angle 2e-2, shear force 1e-3, shear displacement 2e-2. No other check changes.
3. **The deviation from `F·h` stays visible.** It is reported as an informational metric, so the size of the lever effect is never hidden.
4. **Criteria v2** (`criteria/qualification/compliant-link-v2.json`) carries the change as an explicit enum, `"moment_reference": "torque_balance_with_tension_lever"`, and is registered **before** the rerun. v1 stays registered and parses unchanged, with the schema default `load_times_half_size`.
5. **Protocol revision 2** of `docs/validation/compliant-link-v1-protocol.md` implements this and corrects the revision-1 "analytical expectations" note, which had the wrong sign and a wrong soft-point magnitude. It removes the wrong-sign informational metric `info_moment_rel_error_with_axial_lever`. Solver settings are unchanged.
6. **Run 2 under v2 is the official result if it is produced at a clean tree.** Run 1 is kept as superseded evidence.

## Alternatives rejected

- **Loosen the L2 tolerance.** It would hide a 16 % modeling error behind a threshold. That is tuning to pass.
- **Keep v1 and accept a documented fail.** The check would then test the wrong physics forever. A link capability would stay blocked by a criterion that no correct solver can meet.
- **Linearized reference F·h/(1 + h·T/k_bend).** It is accurate to 1.3e-4 at the soft point, but that uses 13 % of the moment tolerance on a known approximation. The exact equation costs nothing.
- **Use the measured tension in the reference.** That couples the reference to solver output. The closed form m·g is exact at equilibrium and is independently checked by L1.

## Safeguards (Q49)

- This change was made **after observing results**. This record precedes the rerun, and criteria v2 is hashed before it.
- The same agent wrote the criteria, the solver, and this ruling. The mitigation is that the new reference is a parameter-free first-principles equation that can be checked by hand. Its prediction was computed independently of the solver before run 2.
- No solver setting, tolerance, grid point, timestep, or other case changes. Run 1 and its README are preserved.

## Consequences

- An L2 pass under v2 qualifies static bending under lateral load only within the declared envelope.
- The checklist (`docs/qualification/backend-checklist.md`) references Q53 for L2.
