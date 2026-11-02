# Evaluation protocol: compliant-link qualification criteria v1

Governs evaluation against `criteria/qualification/compliant-link-v2.json` (SHA-256 `8cfe7c42…0c6e`, Q52 and Q53) from **revision 2**. Revision 1 governed `compliant-link-v1.json` (SHA-256 `7e147a9d…eb77f8`). Revision 1 was committed **before any link solver code**, together with its implementation `src/core/link_eval.zig` and the strict parser `src/core/link_criteria.zig`.

Results are labeled **`fixture`**. They qualify only the declared envelope and say nothing about couplers or Kin candidates (Q40).

## Sample timing and windows

- Sample n is the state after physics step n, at t_n = n·Δt computed from exact tick counts. Sample 0 is the initial state. Its link forces and moments are zero (no step has produced them); its extension and rotation are the initial geometry.
- A window [a, b] includes every sample with a ≤ t ≤ b. Static windows are `[window_start_s, duration_s]` from the criteria.
- Sample times: Δt ∈ {0.5, 1, 2} ms (`physics_step_ticks`, 1 tick = 1 µs).

## Reading link quantities (solver outputs, PHY-005)

All come from the solver's link report. The evaluator never estimates a load from positions.

| Quantity | Definition |
| --- | --- |
| Force on B | Solver impulse accumulated in the step ÷ Δt, on body B at anchor B. Components `[axial, shear 1, shear 2]` along anchor A's frame axes (axis `a`, then two deterministic perpendicular unit vectors) |
| Moment on B | Same, `[torsion, bend 1, bend 2]` |
| Tension | −(force on B)[0]. Positive when the link pulls the bodies together |
| Elongation | Extension [0]: anchor B relative to anchor A, minus L₀·a, after the step |
| Shear displacement | √(ext[1]² + ext[2]²) |
| Twist | Rotation vector [0] of B relative to A, from the rest relative orientation, in anchor A's frame, after the step |
| Bending angle | √(rot[1]² + rot[2]²) |
| Contact normal sum | Sum of the solver's contact normal forces on body B |
| Momentum | Σ m·v over dynamic bodies, from the solver's body state |

Static metrics average each component over the window first, then take magnitudes of the two perpendicular components.

## Metrics

| Check | Metric | Reference | Limit (criteria) |
| --- | --- | --- | --- |
| L1 | \|tension − m·g\| / m·g; \|elongation − m·g/k_axial\| / (m·g/k_axial) | closed form | 1e-3; 1e-2 |
| L2 | shear force vs F; shear displacement vs F/k_shear; bending angle vs φ_ref; bending moment vs k_bend·φ_ref. F = 0.1·m·g, h = half the cube edge. **Rev 2 (Q53, criteria v2):** φ_ref is the root on [0, π/2] of k_bend·φ = h·(F·cos φ − m·g·sin φ), the exact torque balance of B including the tension lever, by 200 bisection halvings. Rev 1 (v1): φ_ref = F·h/k_bend | closed form | 1e-3; 2e-2; 2e-2; 1e-3 |
| L3 | −moment[0] vs τ; twist vs τ/k_torsion (both signed) | closed form | 1e-3; 1e-2 |
| L4 | Mean period vs 2π/√(k_axial/μ), μ = m/2 | see below | 1e-2 |
| L5 | Mean period of twist vs 2π/√(k_torsion/I_red), I_red = I/2, I = m·a²/6 | see below | 1e-2 |
| L6 | ζ measured vs 0.05 | see below | 25 % |
| L7 | \|ζ_num\| for c = 0 | see below | 0.01 |
| L8 | max over t > 0 of \|p − (p₀ + M·g⃗·t)\| / (1e-9·M·g·t + 1e-12) | closed form | ≤ 1 |
| L9 | \|Σ normal + tension − m·g\| / m·g (window mean); every window sample has normal > 0 and tension > 0 | closed form | 1e-3 |
| L10 | Replay reproduces every run's final-state SHA-256 | bit-identical | exact |

**Informational metrics** (prefix `info_`) are reported but never gate. **Rev 2:** `info_moment_rel_deviation_from_load_times_half_size` reports the moment's deviation from F·h (the size of the lever effect), and `info_angle_rel_error_vs_measured_moment` checks the solver's moment and angle against each other. Rev 1's `info_moment_rel_error_with_axial_lever` had the wrong sign (the tension lever **reduces** the moment, like a pendulum) and is removed. Rev 1's text here, written before run 1, said the lever term adds about 2.4 % / 2.0 % / 0.2 %. The correct deviations are −16.4 % / −1.92 % / −0.196 % (Q53).

### Zero-crossing period

A crossing lies between samples n and n+1 when (x_n > 0) ≠ (x_{n+1} > 0), so an exact zero counts as not positive. Its time is t_n + Δt·x_n/(x_n − x_{n+1}). With crossings t_1..t_m, the full periods are t_{i+2} − t_i for i = 1..m−2 and the measure is their mean. Fewer than three crossings means the check fails (fail closed). x is the axial extension (L4) or the twist (L5).

### Peak-ratio damping

A peak is an interior sample n (1 ≤ n ≤ N−1) with x_n > 0, x_n > x_{n−1}, x_n ≥ x_{n+1}, valued by the three-point parabola through n−1, n, n+1. Sample 0 is never a peak. With p peaks, n = p−1 full periods separate the first and last, and ζ = ln(first/last) / (2π·n). Fewer than two peaks means fail. L7 gates |ζ|, so numerical energy *injection* can't pass as low dissipation. The signed value is reported.

### Resolution rule (Q43, Q52 §4)

ω·Δt ≤ 0.2·(1 + 1e-12) means resolved. The slack covers floating-point representation only: soft-axial at 2 ms is designed to sit exactly on the limit. ω = √(k_axial/μ) for L4, L6, L7; √(k_torsion/I_red) for L5. L4–L7 are evaluated only at resolved combinations; others are `outside_envelope`. L1–L3, L8, L9, and L10 run at every combination. (Q52 §4 lists L4–L7 as the dynamic checks, so L8 is evaluated everywhere.)

### Outcome aggregation (Q48, Q52 §6)

Per case, over the evaluated combinations only: all pass → `pass`; all fail → `fail`; mixed → `uncertain`. `outside_envelope` combinations are listed and not counted. If nothing was evaluated the case fails (fail closed). L10 is evaluated per (grid point × Δt): it passes when every run at that combination reproduces its final-state hash on an immediate in-process replay.

### Consistency check

Every metric must be finite. Any non-finite value fails.

## Initial conditions and run geometry

Fixture: `fixture_link_cube`, 20 mm cube, 0.020 kg, inertia m·a²/6 about any centre axis. L₀ = 10 mm; anchors at facing face centres (0.01 m from each centre along the link axis). Body B's rest relative orientation is identity.

| Case | Setup |
| --- | --- |
| L1–L3 | Static body A, centre at (0, 0, 1) m. Link axis a = (0, 0, −1) in A's frame. B hangs below, anchors separated by exactly L₀ at t = 0 (zero extension), at rest. Gravity on. ζ = 1 on body B: c = 2·ζ·√(k·m_B) (axial, shear), 2·ζ·√(k·I_B) (torsion, bend). L2 adds a world-+x force of 0.1·m·g at B's centre of mass every step. L3 adds a world torque of τ along a every step |
| L4, L6, L7, L8 | Two dynamic cubes with centres at z = 10 m, A at x = 0, B at x = 0.03 + stretch. a = (1, 0, 0). Both at rest at t = 0 and free-falling for 1 s with no contact. c = 2·ζ·√(k·μ) for translation, 2·ζ·√(k·I_red) for rotation, ζ = 0 (L4, L7, L8) or 0.05 (L6) |
| L5 | As above with no stretch, and B rotated 0.05 rad about a at t = 0 |
| L9 | Static A above B. B's bottom face on z = 0, at rest. a = (0, 0, −1). A's anchor is placed so the extension is 0.5·m·g/k_axial. Friction 0.6/0.45. ζ = 1 on B. No preroll |

The validation load and torque are fixture-validation inputs (Q46) and are recorded in the run configuration.

## Solver configuration (fixed before the first evaluation)

| Setting | Value | Rationale |
| --- | --- | --- |
| Contact model, stiffness, damping, slip speed | As the analytic protocol: k = 1e5 N/m, c = 50 N·s/m per contact point, 1e-5 m/s | Reuses the validated contact settings; L9 is the only case with contact |
| Solver iterations | 100 projected Gauss–Seidel sweeps per step, contacts then link rows, fixed order | Determinism; same pass as contact (Q52 §1) |
| Warm starting | On for contacts and link impulses (the link impulses are hashed state) | Convergence at rest |
| Link rows | Per link, in order: axial, shear 1, shear 2, torsion, bend 1, bend 2 | Determinism |
| Link integration | Implicit compliant row, velocity form. Spring term evaluated at C̃ = C_n + q·h·(J·v′ − J·v₀) with **q = 1/4**; damping term fully implicit (c·J·v′). v₀ is the relative velocity at step start, before external loads | See below |
| Rotational Jacobian | Small-angle: θ̇ ≈ ω_B − ω_A, rows along anchor A's axes at step start. Axis rotation terms neglected | Documented envelope: small relative rotation and small frame rotation rates |
| Gyroscopic term | Omitted, as in the analytic protocol | Documented limitation |
| Free-fall start height | 10 m centre height, 1 s run (falls 4.9 m) | No contact |

**Why q = 1/4.** A backward-Euler compliant row dissipates about ζ ≈ ω·Δt/2 (Q52 rationale). For a single oscillator in the solver's semi-implicit position update, any force evaluated as k·(x + q·h·(v′ − v₀)) gives a step map with determinant exactly 1 when c = 0: **zero numerical damping by construction**, unconditionally stable, and its phase advance satisfies tan(φ/2) = ωh/2 for q = 1/4, which is the implicit-midpoint frequency. At rest (v′ = v₀) the spring term is exactly k·C, so statics are unaffected. Physical damping comes only from the declared c. The residual stabilization is a frequency error (about 0.33 % at ωΔt = 0.2) and the implicit treatment of the damping term (about 2 % low in the effective ζ at ωΔt = 0.2); both are measured by L4–L6 rather than assumed.

## Analytical expectations recorded before the run

- L4/L5 period error ≈ 0.33 % at ωΔt = 0.2 (limit 1 %).
- L7: |ζ_num| near zero (finite-sweep convergence is the only other source).
- (Rev 1, kept as written) L2 moment and bending-angle checks are expected to **fail** at all grid points because of the neglected lever term above, unless the registered criteria are revised by a new decision record.
- (Rev 2, before run 2) Under criteria v2 the L2 references are the model's exact statics, so the errors should be at the convergence level of L1 and L3 (≤ 1e-9).

## Revision log

| Date | Change | Reason | Results affected |
| --- | --- | --- | --- |
| 2026-11-02 | Initial protocol (revision 1) | — | — |
| 2026-11-02 | **Revision 2. Post-hoc: made after observing run 1** (`results/qualification/compliant-link-v1/run1-77bc3ca-ReleaseSafe.json`, preserved). Governs criteria v2. The L2 bending angle and moment references become the exact torque balance with the tension lever. The wrong-sign informational metric is replaced by the deviation from F·h. Solver settings, tolerances, and every other definition are unchanged | Run 1: L2 failed 9/9 because `F·h` is not the statics of the setup. The reference was wrong, not the solver (Q53) | Run 1: 9 of 10 checks pass, L2 fail. Run 2 replaces it as the reported result. Both are kept. **Ruled by Q53 before the rerun** |

Any change after observing results requires its own decision record before the rerun counts as official (Q49 safeguard).
