# Evaluation protocol: analytic fixture-validation criteria v1

Governs evaluation against `criteria/fixture-validation/analytic-v1.json` (SHA-256 `565ef6b6…3e78`). Committed **before** any production solver code, together with its implementation `src/core/fixture_eval.zig`.

## Metric definitions

Implemented in `src/core/fixture_eval.zig`, which also documents them inline.

| Case | Metric | Definition | Limit |
| --- | --- | --- | --- |
| Rest | normal force | \|mean ΣFn over window − m·g\| / (m·g) | `normal_force_rel_tol` |
| | tangential force | max \|ΣFt\| over window / (m·g) | `tangential_force_max_rel_weight` |
| | centre of pressure | max horizontal distance from the CoP (Fn-weighted contact points) to the CoM over window | `center_of_pressure_abs_tol_m` |
| | drift | max horizontal CoM displacement and max rotation angle, relative to the first window sample | `drift_*` |
| | penetration | max over the whole run | `max_penetration_m` |
| Free fall | velocity | max over 0 < t ≤ T of \|vz + g·t\| / (rel·g·t + floor) | ≤ 1 |
| | position | max over 0 < t ≤ T of \|z − (z0 − ½g·t²)\| / (factor·g·Δt·t) | ≤ 1 |
| | contact | any normal force during the window | none |
| Friction, below (0.9·μs·m·g at the CoM) | displacement | max horizontal CoM displacement from t = 0 | `below_max_displacement_m` |
| | balance | \|mean \|ΣFt\| over window − push\| / push | `below_balance_rel_tol` |
| Friction, above (1.1·μs·m·g) | acceleration | (v·d at the sample nearest window end − v·d at the sample nearest window start) / Δt, vs (F − μk·m·g)/m, relative | `above_accel_rel_tol` |
| Slide to stop | stop | **rev 2:** first sample whose bottom-face-centre horizontal speed (v + ω × r) is ≤ threshold, else fail. The rev-1 CoM-speed definition is still reported as an informational metric | — |
| | time | \|t_stop − v0/(μk·g)\| | `stop_time_tol_steps`·Δt |
| | distance | \|d − v0²/(2μk·g)\| | rel·d* + steps·v0·Δt |
| | post-stop drift | max horizontal displacement after the stop | `post_stop_drift_abs_tol_m` |
| Tipping, below | tilt | max angle between the body z axis and world z | `below_max_tilt_rad` |
| Tipping, above | tilt | max tilt over the run | ≥ `above_min_tilt_rad` |
| | pivot slip | max horizontal displacement of the +x bottom-edge midpoint while tilt < `no_slip_until_tilt_rad` | `pivot_slip_abs_tol_m` |

Sample n is the state after step n (t = n·Δt). Sample 0 is the initial state. Windows include their endpoints. A non-finite metric never passes. Contact forces are solver-native outputs (PHY-005).

**Outcome rule (Q48):**

- A case run at one combination (friction pair × timestep) passes only if every metric passes, including both sub-runs where the case has them.
- Combining combinations: all pass → `pass`, all fail → `fail`, any mix → `uncertain`.
- No combinations evaluated → `fail`.
- Every result carries the label `fixture` (Q46).

## Initial conditions

| Case | Fixture | Initial state |
| --- | --- | --- |
| Rest, friction, slide | flat block | bottom face on z = 0, axis-aligned, at rest, **then settled unloaded for 0.5 s (rev 2)**. t = 0 starts after settling. Slide: v0 along `direction_world` added at t = 0 |
| Free fall | flat block | bottom face at z = `initial_clearance_m`, at rest |
| Tipping | tall block | bottom face on z = 0, axis-aligned, at rest, then settled unloaded for 0.5 s (rev 2). Load applied in the body frame at `application_point_body_m` from t = 0 |

Validation loads act for the whole run. They are recorded as run inputs and are present only in `fixture_validation` runs (Q46, PRC-013).

## Solver configuration (fixed before the first evaluation)

These are solver settings, not criteria (Q48). They are recorded with every result. **They are fixed here before any result is observed.** Any later change must be recorded below with its reason, and results under every setting are preserved, so tuning-to-pass stays visible.

| Setting | Value | Rationale |
| --- | --- | --- |
| Contact model | Compliant point contacts at cuboid vertices against the plane z = 0. Implicit spring-damper normal constraint; Coulomb friction cone with impulse clamp | Q35: implicitly solved compliant constraints |
| Contact stiffness k | 1.0e5 N/m per contact point | Static penetration of about m·g/(4k) ≈ 1e-6 m, two orders below the 1e-4 m bound |
| Contact damping c | 50 N·s/m per contact point | About critical (2√(k·m/4)) for the lightest fixture's per-contact mass share |
| Static/kinetic switch | μs when the contact's tangential speed at step start is ≤ 1e-5 m/s, else μk | Coulomb onset vs. sliding (Q47) |
| Solver iterations | 100 projected Gauss–Seidel sweeps per step, fixed count, fixed contact order | Determinism |
| Warm starting | Previous step's impulses reused per (body, vertex) | Convergence at rest |
| Integrator | Semi-implicit Euler. Quaternion first-order update with renormalization | — |
| Gyroscopic term | Omitted | Documented limitation. Negligible for the single-axis motions in these cases |

## Revision log

| Date | Change | Reason | Results affected |
| --- | --- | --- | --- |
| 2026-10-31 | Initial protocol (revision 1) | — | — |
| 2026-10-31 | **Revision 2. Post-hoc: made after observing run 1** (`results/fixture-validation/analytic-v1/run1-7c7581f-ReleaseSafe.json`, preserved). (a) Fixtures starting on the table are settled unloaded for 0.5 s before t = 0. (b) Slide-to-stop detects the stop on the bottom-face-centre speed instead of CoM speed. Criteria thresholds are unchanged. Solver settings are unchanged | (a) Rev 1 started runs on an uncompressed contact. At Δt = 0.5 ms the first step carried only 0.83·m·g, so friction capacity fell below the 0.9·μs push and the block slipped, an artifact of the initial condition, not of the threshold. (b) Run 1 shows sliding stops within one step of v0/(μk·g) (stop distance within 0.5 mm). The CoM speed then reflects a decaying post-stop rock on the compliant contact (v_com = ω·h_com) for about 3 ms, which is not sliding. The rev-1 metric is still reported as informational | Run 1: friction `uncertain` (6/9), slide `fail` (0/9), others `pass`. Run 2 replaces it as the reported result. Both are kept. **Flagged for owner review because this was post-hoc** |
