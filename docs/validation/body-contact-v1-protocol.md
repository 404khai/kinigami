# Evaluation protocol: body-body contact fixture-validation criteria v1

Governs evaluation against `criteria/fixture-validation/body-contact-v1.json` (SHA-256 in `criteria/REGISTER.md`). Decision: Q76. Revision 1. Committed **before** any body-body contact solver code. Label of every result: `fixture` (Q46). A pass qualifies box-box contact only, within the declared conditions (Q76 section 6).

## Conventions

- Sample n is the state after step n (t = n·Δt). Sample 0 is the initial state, taken after the settle period where the criteria declare one. Windows include their endpoints. A non-finite metric never passes. Contact forces are solver-native outputs (PHY-005).
- Metrics that are the block-on-block analogue of an analytic-v1 metric use the **same definition** as `docs/validation/fixture-analytic-v1-protocol.md`, with the support body replaced by the named bottom body. Only the differences are described below.
- Every numeric value in the criteria file is `copied` from analytic-v1 (field named) or `provisional` (basis stated). Provisional values are never described as evidence.
- Settling (BB1, BB2, BB3, BB5, BB7): bodies start exactly touching, aligned, at rest and settle 0.5 s under gravity with no validation load, as in analytic-v1 protocol revision 2. This is declared from the start; it is not a post-hoc change. BB4, BB6 and BB8 are not settled.
- The tabletop is the world plane z = 0 and is unchanged. Body-body contact never replaces it.
- Contact bodies are cuboids. A static body has no mass and no state change. Two static bodies create no contact row.

## Contact generation (Q76 section 2)

The generator is a pure function of the two body poses and sizes. It is implemented in the simulation core with the Zig standard library only.

1. **Pair order.** Bodies are ordered by body index, A < B. The contact normal points from A to B. A pair is skipped if both are static.
2. **Axes.** The SAT test uses 15 axes in this fixed order:
   - 0 to 2: A local x, y, z;
   - 3 to 5: B local x, y, z;
   - 6 to 14: A local axis i crossed with B local axis j, at index 6 + 3·i + j.
3. **Overlap.** For each axis (normalised) the overlap is the sum of the two box projection radii minus the absolute projected centre distance. An edge-pair axis whose cross product has length ≤ 1e-9 times the product of the two axis lengths (parallel edges) is skipped. **Separation:** if any axis has overlap < 0 the pair is separated and creates no row. Overlap exactly 0 also creates no row (Q76: separation of more than 0 creates no row, and touching has depth 0).
4. **Axis choice and ties.** The axis with the strictly smallest overlap wins. Ties (equal as doubles) go to the lowest axis index. Face axes (0 to 5) therefore beat edge axes on a tie. The normal is the chosen axis, signed to point from A to B (positive dot with B centre minus A centre; if that dot is exactly 0, use the positive-sign axis as constructed).
5. **Face axis (0 to 5), manifold.** The reference box owns the axis (A for 0 to 2, B for 3 to 5). The incident face is the face of the other box most anti-parallel to the normal; ties go to the lowest face index (local +x, −x, +y, −y, +z, −z). The incident face polygon (4 points, canonical vertex order) is clipped by Sutherland–Hodgman against the four side planes of the reference face, in the order +u, −u, +v, −v, where u, v are the reference box's two tangential axes in ascending axis index. Clip points with depth < 0 (above the reference face) are dropped. The kept points are the vertices of the incident face that lie inside the reference face's footprint, plus the edge crossings of the incident face with that footprint. Duplicates of the previous kept point within 1e-12 m are dropped (provisional). The reported point lies on the incident face and its depth is its penetration along the normal.
6. **Edge axis (6 to 14).** One point: the midpoint of the closest points of the two supporting edges (the edge of A and the edge of B nearest along the axis). Depth is the axis overlap.
7. **Ordering.** Rows are ordered by (body pair index, feature id). The feature id of a face-manifold point is its position in the clip output (0, 1, …). An edge point has feature id 0. Pairs are ordered by (A index, B index) ascending.
8. **Solver treatment.** Each point is one compliant row with the protocol contact stiffness and damping, Coulomb friction with static/kinetic selection on the tangential speed at step start, projected Gauss–Seidel in the order above with warm starting keyed on (body pair, feature id), impulses equal and opposite on both bodies (static bodies take none). Points are not merged.

Note on the vertex-in-box wording in Q76: the clip result contains every vertex of the incident face that is inside the reference face footprint (the vertex-in-other-box points) and, in addition, the edge crossings. It also removes the double counting that arises for equal aligned footprints, where every vertex is on the other box's boundary.

## Solver configuration (fixed before the first evaluation)

These are solver settings, not criteria (Q48). They are the analytic-v1 contact settings (`docs/validation/fixture-analytic-v1-protocol.md`, section Solver configuration) and are applied to every contact, tabletop and body-body. They are recorded with every result. Any later change needs the revision log below and its reason; results under every setting are preserved.

| Setting | Value |
| --- | --- |
| Contact stiffness k | 1.0e5 N/m per contact point |
| Contact damping c | 50 N·s/m per contact point |
| Static/kinetic switch | μs when the contact's tangential speed at step start is ≤ 1e-5 m/s, else μk. For body-body contact, the tangential relative speed of the two contact points |
| Solver iterations | 100 projected Gauss–Seidel sweeps per step, fixed count, fixed contact order |
| Warm starting | Previous step's impulses reused per (body pair, feature id) |
| Integrator | Semi-implicit Euler. Quaternion first-order update with renormalization |
| Gyroscopic term | Omitted. BB8 is built so every rotation is about a principal axis (y), which makes the omission irrelevant to the angular momentum audit |

## Metric definitions

Implemented in `src/core/fixture_eval.zig` or a successor module. Not written before this protocol and criteria are hashed.

| Case | Metric | Definition | Limit |
| --- | --- | --- | --- |
| BB1 | inter-block normal force | \|mean ΣFn over window of the bottom–top interface − m_top·g\| / (m_top·g) | `inter_block_normal_force_rel_tol` |
| | table normal force | \|mean ΣFn over window of the table–bottom interface − (m_bottom + m_top)·g\| / that weight | `table_normal_force_rel_tol` |
| | tangential force | max over window of \|ΣFt\| per interface / the weight carried by it | `tangential_force_max_rel_weight` |
| | centre of pressure | per interface, max horizontal distance from the Fn-weighted contact points to the top block (or bottom block for the table interface) CoM over window | `center_of_pressure_abs_tol_m` |
| | drift | per body, max horizontal CoM displacement and max rotation angle relative to the first window sample | `drift_*` |
| | penetration | max over the whole run, per interface | `max_penetration_m` |
| | equal and opposite | at every step, \|F_on_A + F_on_B\| / \|F_on_A\| of the bottom–top interface | `newton_third_law_rel_tol` |
| BB2 below | displacement, balance, penetration | as friction below, the push applied to the top block, friction measured on the top-block interface | below limits |
| BB2 above | acceleration | as friction above, over the shortened window | `accel_rel_tol` |
| | slab | top CoM horizontal distance from the slab centre ≤ (slab half-size − block half-size) at every sample | `stays_on_slab` |
| BB3 | stop, time, distance, post-stop drift | as slide to stop (revision 2 stop point), with the slab as support | analytic-v1 limits copied |
| BB4 | free flight | any normal force before the first sample with separation ≤ 0 fails; the first contact sample must follow the closure of the clearance | `free_flight` |
| | peak penetration | max penetration over the whole run | `peak_penetration.max_penetration_m` |
| | rest state | BB1 metrics on the top-block/slab interface over the rest window, with the reference m_top·g | `rest_state_metrics` |
| | rest penetration | max penetration in the rest window | `rest_max_penetration_m` |
| BB5 | tilt, pivot slip | as tipping, with the slab as support | analytic-v1 limits copied |
| BB6 | geometry | the generator output at the declared poses against the closed forms. Points: sorted by (x, y, z) then each coordinate error ≤ `position_depth_rel_tol` · max(\|expected\|, `position_scale_m`). Depth likewise. Normal: each component ≤ `normal_component_abs_tol`. Count exactly equal. Feature ids strictly increasing. Also the swapped pair order | BB6 tolerances |
| | axis | the chosen SAT axis index equals `expected_axis` | exact |
| BB7 | invariance | per quantity, the transformed run's value (expressed in the body-relative form) against the identity run's value: \|a − b\| ≤ `rel_tol` · max(\|b\|, scale) + `abs_floor`. Stop step index within one step (`stop_step_index_tol`, set at lead review before registration; Q76 §5 said 1e-9 relative, raised to 1e-6) | BB7 tolerances |
| BB8 | momentum | max over t > 0 of \|p − p₀\| / (1e-9·M·g_n·t + 1e-12) | ≤ 1 |
| | angular momentum | max over t > 0 of \|L − L₀\| / (1e-9·M·g_n·t·r_ref + 1e-12), about the world origin | ≤ 1 |
| | impulse accounting | per step, the change in each body's momentum vs the sum of the solver's reported contact impulses on it | `impulse_accounting` |
| | pose integration | each body's pose after each step bit-identical to the semi-implicit update from the previous state and its reported velocity | exact |
| | energy | E_final − E_0 ≤ (`creation_rel_tol` + `first_order_omega_dt_coefficient`·ω_ref·Δt)·E_0 + floor | ≤ 0 |
| | preconditions | final sample has no body pair overlap, and the peak tangential impulse in the run is at least `min_peak_tangential_impulse_n_s` | pass/fail |
| | discrimination | each control (velocity snap, angular velocity snap at first contact, applied to a copy of the trace) fails the momentum or angular momentum audit at every Δt | must fail |
| BB9 | replay | canonical final-state hash of every run equals the hash of its replay | bit-identical |

Frame and rounding conventions: lengths m, forces N, momenta kg·m/s. Double precision throughout. Quantities reported in the "slab frame" are the rigid inverse of the slab pose applied to the world quantity.

## BB7 transform

The same rigid transform is applied to every body pose, orientation, velocity, the gravity direction and the slide direction, exactly as the criteria file states:

- rotation matrix rows (37/45, −16/45, 4/9), (4/9, 8/9, −1/9), (−16/45, 13/45, 8/9);
- translation (0.3, −0.2, 5.0) m.

The rotated gravity vector is the negative third column scaled by g. Doubles are constructed from the stated fractions with one division each. The tabletop never touches the scene (4 m clearance), so the world-fixed table does not enter.

## Outcome aggregation

Same as analytic-v1 (Q48):

- A case run at one combination (friction pair × timestep) passes only if every metric passes, including both sub-runs where a case has them (BB2, BB5).
- Combining combinations: all pass → `pass`, all fail → `fail`, any mix → `uncertain`. No combinations evaluated → `fail`.
- BB6 is evaluated once (no friction pair, no timestep). BB7 is evaluated at all nine combinations. BB8 audits and discrimination, and BB9 replay, use every combination.
- Every result carries the label `fixture`.
- Uncertainty that overlaps a threshold makes the result `uncertain`, not `pass` (PHY-008). Because every threshold is a tolerance on a solver-native output, a metric is uncertain only when the evaluator reports an uncertainty interval; none is declared here.

## Limitations

- Cuboids only. No other shape, no rounded edges, no mesh.
- Contact generation uses a vertex-and-clip manifold; it is one point (edge-edge) or up to 8 (clip polygon); there is no persistent manifold beyond the warm-start key.
- Feature-id warm starting can lose the warm start when the clip output changes length between steps. The cases are not designed to measure this.
- The gyroscopic term is omitted. BB8 and the dynamic cases rotate about principal axes only; the limitation is not exercised or bounded here.
- BB7 tests invariance for two scenes under one rigid transform, not for every rotation.
- The BB8 energy audit applies to contact-free first and last samples only. It does not bound the energy during contact.
- Penetration limits are bounds for these fixtures at k = 1e5 N/m. They are not material claims.
- Nothing here validates any Kin geometry or coupler. Re-evaluating the coupler C8 sweep with body-body contact needs its own decision and a new coupler criteria version (Q76 section 6).

## Revision log

| Date | Change | Reason | Results affected |
| --- | --- | --- | --- |
| 2026-11-19 | Initial protocol (revision 1) | — | — |

Any change made after observing results requires its own decision record before the rerun counts as official (Q49).

## Revision 2 (Q78)

- **SAT axis selection:** face and edge axes are tracked separately. Overlaps within 1e-9 m keep the lower index. An edge axis wins only if its overlap is below 0.95 of the best face overlap, minus that margin. Both constants are provisional. This replaces exact-equality tie breaking.
- **BB8 angular snap control:** reset body B's angular velocity at first contact to its pre-contact value.
- The criteria JSON and every threshold are unchanged.

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-11-19 | Initial (Q76, Q77) |
| 2 | 2026-11-19 | Axis-selection hysteresis and BB8 snap definition (Q78), after a non-official preview, before official run 1 |
