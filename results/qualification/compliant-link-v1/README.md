# Compliant-link qualification results

Official criteria: `criteria/qualification/compliant-link-v2.json` (SHA-256 `8cfe7c42…0c6e`, Q52 + Q53). Superseded: `compliant-link-v1.json` (SHA-256 `7e147a9d…eb77f8`, Q52).
Protocol: `docs/validation/compliant-link-v1-protocol.md`. Revision 2 governs v2; revision 1 governed v1. The folder keeps the protocol's name.
Every result is labeled **`fixture`**. These results are not coupler, benchmark, or Kin-candidate evidence, and they qualify nothing beyond the declared envelope.

| Run | Code revision | Criteria | Protocol rev | Build | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 | L10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [run 1](run1-77bc3ca-ReleaseSafe.json) | `77bc3ca` (clean) | v1 | 1 | ReleaseSafe, aarch64-macos | pass 9/9 | **fail 0/9** | pass 9/9 | pass 4/4 | pass 3/3 | pass 4/4 | pass 4/4 | pass 9/9 | pass 9/9 | pass 9/9 |
| [run 2](run2-5f04229-ReleaseSafe.json) | `5f04229` (clean) | **v2** | 2 | ReleaseSafe, aarch64-macos | pass 9/9 | **pass 9/9** | pass 9/9 | pass 4/4 | pass 3/3 | pass 4/4 | pass 4/4 | pass 9/9 | pass 9/9 | pass 9/9 |

(L4–L7: evaluated combinations only; the rest are `outside_envelope`.)

**Run 2 is the official result.** Criteria v2 and protocol revision 2 were made **after observing run 1**. They were ruled by [Q53](../../../docs/decisions/Q053-compliant-link-l2-bending-reference.md) and registered before run 2 (Q49 safeguard). They change only the L2 bending moment and angle reference, from `F·h` to the exact torque balance including the tension lever. No tolerance, solver setting, grid point, timestep, or other case changed. Run 1 is kept as superseded evidence.

## Run 2

- **Solver unchanged:** all 60 run-2 final-state hashes are identical to run 1's. Only the evaluation of L2 differs.
- **Replay:** a second process run on the same binary reproduced all 60 final-state hashes and every metric value bit-exactly. Every run also replayed in-process (L10).
- **L2 under v2:** bending moment error ≤ 2.3e-14 and bending angle error ≤ 1.9e-14 at every combination, at the convergence level of L1 and L3. The informational deviation from `F·h` is 0.164 / 0.0192 / 0.00196 (soft/mid/stiff), matching the hand-solved statics of Q53 to 13 digits.

#### Run 1 margins

| Metric | Margin used | Where |
| --- | --- | --- |
| L1 tension, elongation | 1.4e-11, 6.0e-10 | |
| L2 shear force, moment, displacement, angle | 1.5e-11, 2.3e-11, 1.0e-12, 9.5e-13 | |
| L3 torque, twist | 1.8e-11, 1.8e-12 | |
| L4 period error | 0.33 (3.3e-3 of 1e-2) | soft, 2 ms (ω·Δt = 0.2) |
| L5 period error | 0.31 | mid, 0.5 ms |
| L6 ζ error | 0.041 | soft, 2 ms |
| L7 \|ζ_num\| (limit 0.01) | 1.9e-5 (1.9e-7 absolute) | soft, 2 ms |
| L8 momentum | 1.7e-5 | soft, 0.5 ms |
| L9 load sum | 1.2e-11 | |

The dynamic margins are the integrator's honest error budget. The period error grows as (ω·Δt)²/12, which is the implicit-midpoint phase error of the q = 1/4 link step. The numerical damping is at round-off level. The `outside_envelope` combinations are the same as in run 1 (table below).

## Run 1 (superseded): [`run1-77bc3ca-ReleaseSafe.json`](run1-77bc3ca-ReleaseSafe.json)

Code revision `77bc3ca` (clean tree), ReleaseSafe, aarch64-macos, Zig 0.17.0. Solver settings as fixed in the protocol (100 sweeps, contact k = 1e5 N/m and c = 50 N·s/m, link prediction q = 1/4). No solver, protocol, or criteria change was made after the run was observed.

| Case | Outcome | Evaluated | Outside envelope |
| --- | --- | --- | --- |
| L1 axial statics | **pass** | 9 | 0 |
| L2 shear and bending statics | **fail** | 9 | 0 |
| L3 torsion statics | **pass** | 9 | 0 |
| L4 axial dynamics | **pass** | 4 | 5 |
| L5 torsional dynamics | **pass** | 3 | 6 |
| L6 physical damping | **pass** | 4 | 5 |
| L7 numerical dissipation | **pass** | 4 | 5 |
| L8 momentum | **pass** | 9 | 0 |
| L9 contact–link consistency | **pass** | 9 | 0 |
| L10 determinism | **pass** | 9 | 0 |

Under v1, L2 failed at all nine combinations. The diagnosis below led to Q53.

## L2 failure and diagnosis

Shear force (≤ 1.5e-11) and shear displacement (≤ 1e-12) are exact. Only the bending moment and bending angle fail, identically at every Δt, so this is not a timestep or convergence effect:

| Grid point | Bending moment error (limit 1e-3) | Bending angle error (limit 2e-2) |
| --- | --- | --- |
| soft | 0.1641 | 0.1641 |
| mid | 0.01924 | 0.01924 (passes) |
| stiff | 0.001958 | 0.001958 (passes) |

Cause: the registered reference `F·h` ignores the vertical tension acting through the rotated anchor lever. Torque balance about B's centre of mass gives |M| = F·h/(1 + h·m·g/k_bend), where the tension (= m·g) **reduces** the moment B must transmit. This closed form predicts errors of 0.1640, 0.01924, 0.001957, against 0.1641, 0.01924, 0.001958 measured. The solver reproduces the correct statics. The registered criterion is what is incomplete. The angle check also fails at soft because the same factor applies.

**Disclosure about the protocol.** The protocol's "analytical expectations" note said the soft/mid/stiff moment errors would be about 2.4 % / 2.0 % / 0.2 % and that the lever term adds to the moment. The soft figure was a numerical slip and the sign was wrong. The corrected values are above. The protocol was not edited (Q49 safeguard). The informational metric `info_moment_rel_error_with_axial_lever` inherits the wrong sign, so it reads 28 % / 3.8 % / 0.39 % and should be ignored. `info_angle_rel_error_vs_measured_moment` (≈ 1e-14) confirms the reported moment and angle are mutually consistent.

**Options (need a new decision record; none taken here):** (a) revise L2's moment and angle references to include the lever term and issue criteria v2; (b) keep v1 and accept L2 as a documented fail with the diagnosis above.

### Run 1 margins

| Metric | Margin used | Where |
| --- | --- | --- |
| L1 tension, elongation | 1.4e-11, 6.0e-10 | |
| L2 shear force, shear displacement | 1.5e-11, 1.0e-12 | |
| L2 bending moment (fails) | 164 | soft |
| L2 bending angle (fails) | 8.2 | soft |
| L3 torque, twist | 1.8e-11, 1.8e-12 | |
| L4 period error | 0.33 (3.3e-3 of 1e-2) | soft, 2 ms (ω·Δt = 0.2) |
| L5 period error | 0.31 | mid, 0.5 ms |
| L6 ζ error | 0.041 | soft, 2 ms |
| L7 \|ζ_num\| (limit 0.01) | 1.9e-5 (1.9e-7 absolute) | soft, 2 ms |
| L8 momentum | 1.7e-5 | soft, 0.5 ms |
| L9 load sum | 1.2e-11 | |

L7 is the check the criteria were designed around: measured numerical damping is at most 1.9e-7, five orders under the bound, so the link integrator does not masquerade as physical damping (PHY-006). The signed value changes sign across combinations, consistent with round-off-scale phase error rather than dissipation.

## Solver-settings sensitivity (PHY-016, Q54): [`sensitivity-f634692/`](sensitivity-f634692/)

Exploratory study at `f634692` (clean tree, ReleaseSafe), declared in [Q54](../../../docs/decisions/Q054-compliant-link-slice-closure.md) before it ran. It is the full L1–L10 suite under criteria v2 for each variant, changing one setting at a time. Non-baseline variants are labeled **`exploratory`** and gate nothing. The baseline is the protocol configuration, and its 60 hashes and metrics equal run 2's.

Worst margin used (value ÷ limit) over evaluated combinations:

| Variant | Outcomes | L1 tension | L2 bending | L3 torque | L4 period | L5 period | L6 zeta | L7 abs | L8 momentum | L9 load |
|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` (fixture) | 10/10 pass | 1.4e-11 | 2.3e-11 | 1.8e-11 | 0.33 | 0.31 | 0.041 | 1.9e-05 | 1.7e-05 | 1.2e-11 |
| `iterations_10` (exploratory) | 10/10 pass | 1.4e-11 | 2.3e-11 | 1.8e-11 | 0.33 | 0.31 | 0.041 | 1.9e-05 | 1.7e-05 | 1.4e-11 |
| `iterations_25` (exploratory) | 10/10 pass | 1.4e-11 | 2.3e-11 | 1.8e-11 | 0.33 | 0.31 | 0.041 | 1.9e-05 | 1.7e-05 | 1.2e-11 |
| `iterations_50` (exploratory) | 10/10 pass | 1.4e-11 | 2.3e-11 | 1.8e-11 | 0.33 | 0.31 | 0.041 | 1.9e-05 | 1.7e-05 | 1.2e-11 |
| `iterations_200` (exploratory) | 10/10 pass | 1.4e-11 | 2.3e-11 | 1.8e-11 | 0.33 | 0.31 | 0.041 | 1.9e-05 | 1.7e-05 | 1.2e-11 |
| `no_warm_start` (exploratory) | 10/10 pass | 1.4e-11 | 2.3e-11 | 1.8e-11 | 0.33 | 0.31 | 0.041 | 1.9e-05 | 1.7e-05 | 1.4e-11 |
| `q_0` (exploratory) | 10/10 pass | 1.4e-11 | 2.3e-11 | 1.8e-11 | 0.17 | 0.16 | 0.021 | 3.6e-06 | 1.7e-05 | 1.2e-11 |
| `q_0.5` (exploratory) | 10/10 pass | 1.4e-11 | 2.3e-11 | 1.8e-11 | 0.83 | 0.78 | 0.06 | 1.7e-05 | 1.7e-05 | 1.2e-11 |
| `backward_euler` (exploratory) | 6/10 pass | 1.4e-11 | 2.3e-11 | 1.8e-11 | 1.3 | 1.2 | 7.9 | 9.9 | 1.7e-05 | 1.2e-11 |

Findings:

- **Sweep count and warm start do not matter** for these fixtures (10–200 sweeps, warm start on or off): margins agree to the digits shown. The six link rows are nearly decoupled in two-body fixtures, so Gauss–Seidel converges in about one sweep. **Limitation:** this says nothing about strongly coupled systems such as chains and closed loops, which must repeat the study when qualified.
- **q changes only the phase error,** as the analysis predicts. Period error at ω·Δt = 0.2 is 0.17 % (q = 0), 0.33 % (q = 1/4, protocol), and 0.83 % (q = 1/2). Numerical damping stays at round-off level for every q. q = 0 has a smaller phase error but is only conditionally stable (ω·Δt < 2), whereas q = 1/4 is unconditionally stable. The protocol value stands. Changing it would need a decision and a rerun, and none is warranted.
- **The backward-Euler control fails L6 and L7** at every resolved combination: ζ_num = 0.025, 0.050, 0.099 at ω·Δt = 0.05, 0.1, 0.2, which is ω·Δt/2 to within 1 % (Q52's prediction). Its declared ζ = 0.05 is measured up to 2–3× too high. So L7 discriminates. A conventional soft constraint would have presented numerical damping as physics, and this protocol catches it (PHY-006). Its period errors also exceed the limit at ω·Δt ≥ 0.19 (L4, L5 `uncertain`).
- **Timestep sensitivity:** under the protocol settings the period error follows (ω·Δt)²/12 (2.1e-4, 8.3e-4, 3.3e-3 at ω·Δt = 0.05, 0.1, 0.2): second order, as expected.

## `outside_envelope` combinations (runs 1 and 2) (neither pass nor fail, not counted)

| Case | Combinations (grid, Δt, ω·Δt) |
| --- | --- |
| L4, L6, L7 | mid 1 ms (0.316), mid 2 ms (0.632), stiff 0.5 ms (0.5), stiff 1 ms (1.0), stiff 2 ms (2.0) |
| L5 | soft 2 ms (0.245), mid 1 ms (0.387), mid 2 ms (0.775), stiff 0.5/1/2 ms (0.61/1.22/2.45) |

Soft-axial at 2 ms sits exactly on the limit (ω·Δt = 0.2) and is evaluated (protocol slack 1e-12 relative).

### Run 1 replay check

The binary was rerun on the same tree. All 60 sub-run final-state SHA-256 hashes and every metric value were identical (bit-exact JSON equality). Each run also replayed in-process during the suite, which is L10.

## Validated envelope (run 2: what these results cover)

Only:

- two uniform 20 mm / 0.020 kg cubes joined by one fixture link (L₀ = 10 mm, anchors at facing face centres), or one static cube and one dynamic cube
- stiffness grid soft/mid/stiff (k_axial = k_shear 1e2/1e3/1e4 N/m; k_torsion = k_bend 1e-2/1e-1/1 N·m/rad), Δt = 0.5, 1, 2 ms
- statics: axial tension and elongation, shear force and displacement, bending moment and angle under a lateral load at the centre of mass (with the tension lever), torsion (all with ζ = 1 settling)
- dynamics: axial and torsional oscillation and damping at ω·Δt ≤ 0.2 only; the **stiff** grid point is never dynamically validated
- the protocol's solver settings

Not covered:

- the stiff grid point's dynamics (outside the resolution rule)
- chains of three or more bodies, link creation, release or failure, closed loops, couplers
- large relative rotations (small-angle rotational Jacobian) and frame-rotation coupling
- link load limits and failure (deferred to the coupler slice, Q54)
- any Kin geometry

Recordings: `kinigami-qualify <report> --recordings <dir>` writes one format-v3 recording per evaluated run (Q55), with no effect on results (hashes verified identical to run 2). Recordings are reproducible from the code revision and are not committed.
