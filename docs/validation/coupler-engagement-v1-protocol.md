# Evaluation protocol: coupler-engagement qualification criteria v1

Governs evaluation (revision 2, Q58) against `criteria/qualification/coupler-engagement-v1.json` (Q56 stand-in, Q57 criteria), from **revision 1**. Revision 1 is committed **before any coupler solver code** (no guide contact, latch, or engagement code exists at this commit).

Results are labeled **`fixture`**. They qualify only the declared envelope and say nothing about any Kin coupler or candidate (Q40).

## Frames, samples, and reported quantities

- **Coupler frame.** Axis `a` (A's frame) and the shear axes s₁, s₂ are exactly the solver's anchor-A frame for links: s₁ = normalize(a × t) with t the world axis of smallest |aᵢ|, lowest index on ties, and s₂ = a × s₁ (Q52, `rigid.perpendiculars`). Axial coordinate x is measured along `a` from A's coupler face plane.
- **Sample n** is the state after physics step n and after the coupler update that follows it, at t_n = n·Δt from exact ticks. Sample 0 is the initial state, with no forces. Each sample carries:
  - both bodies' position, orientation, velocity, and angular velocity
  - every solver contact report of step n (tabletop and guide), with point, normal, normal force, tangential force, and bodies
  - the latch-link report of step n (force and moment on B, extension, rotation, in coupler-frame components, as Q52)
  - `active_during_step` (the link had rows in step n), `e_during_step`, `active_after`, `e_after`, pawl travel u after the update
  - the command, and the validation loads applied in step n
- **Loads per axis** (solver outputs, PHY-005):
  - tension T = −F_b[0], with no limit when T ≤ 0
  - shear S = √(F_b[1]² + F_b[2]²)
  - bending M_b = √(M_b[1]² + M_b[2]²)
  - torsion M_t = |M_b[0]|
- **Seat axial force** N_ax = Σ over guide contacts on B of f_n·(n · a_world), where n is the contact normal acting on B. **Guide contact count** is the number of guide contacts on B with f_n > 0.
- Window means average components first, then take magnitudes, as in Q52.
- **Separation step:** the first step n with `active_during_step` true and `active_after` false. The time is t_n.

## Setups

All runs use the protocol solver settings of the compliant-link suite: 100 Gauss–Seidel sweeps, warm start on, link prediction q = 1/4, contact k = 1e5 N/m, c = 50 N·s/m, slip speed 1e-5 m/s. Guide contact rows are solved after tabletop contacts and before link rows, in a fixed feature order. Latch-link damping is c_full = 2·0.2·√(k_full·μ_red) (or I_red), with rows using e·c_full, unless a case overrides ζ.

| Case | Setup |
| --- | --- |
| C1, C2, C5 (hang) | Static A, centre (0, 0, 1) m, a = (0, 0, −1) in A's frame. B has identity orientation, with its ball centre exactly at the seat point (zero penetration), at rest. u = u_full at t = 0. Gravity on. Guide μ = 0. Command `hold` throughout, except C5 commands `release` from t ≥ 0.5 s. Validation force on B at its centre of mass along the world direction of `a` (away from A), constant from t = 0 |
| C2 | Total pull F = m·g + F_val = factor·F_sep, with F_sep = k_axial·δ_pre (e = 1), factor ∈ {0.9, 1.1} |
| C5 | F = m·g + F_val = factor·T_block, factor ∈ {0.9, 1.1} |
| C3, C7 (link only) | **Guide contacts disabled** for these runs. This isolates the latch link, which is permitted only in `fixture_validation`. Two free cubes, centres at z = 10 m, a = (1, 0, 0). B has identity orientation, positioned so anchor B coincides with anchor A (zero extension), at rest. u = e·u_full, command `hold` |
| C3 loads | Magnitude L(t) = L_target·min(t/0.5 s, 1), L_target = factor·limit(e). Tension: +L·a on B at anchor B and −L·a on A at anchor A. Shear: the same along s₁. Bending: torque +L·s₁ on B and −L·s₁ on A. Torsion: torque ±L·a. Directions are the world axes at t = 0. Force points are the current world anchor positions at step start. After separation the loads continue |
| C7 | B displaced +5e-5 m along `a` (axial runs) or rotated 0.002 rad about `a` (torsion run), at rest. The damping override is ζ at the tested engagement: rows use c = 2ζ·√(e·k_full·μ_red) (or I_red) |
| C4, C6, C8 (free fall with guide) | A centre at (0, 0, 10) m, a = (1, 0, 0), at rest, no tabletop contact |
| C4 | Ball centre at the seat point (or seat + 1 mm·a for `blocked`), at rest, u = 0, command `engage` throughout, μ = 0 |
| C6 | Ball at the seat point, at rest, u = u_full, `hold` until t = 0.2 s, then `release`, μ = 0 |
| C8 | B is rotated by θ₀ about A-frame axis a × d (d the unit offset direction; about s₂ for d = 0), then placed so the ball centre is at x = +3 mm with lateral offset y₀·d. Velocity −v·a, ω = 0. Command `engage` throughout. Friction pair per run. d is A-frame (0, 1, 0) for `toward_facet` and (0, 1, 1)/√2 for `toward_corner` |

## References (closed form, from criteria parameters only)

Notation: k = k_axial_full, δ = preload offset, α = atan(w/D), k_s = 4·k_contact·sin²α, m = fixture mass, g = gravity.

- **Seated statics** (C1 with F = m·g, C2 below with F = factor·F_sep): T_ref = k·(F + k_s·δ)/(k + k_s) and N_ref = k_s·(k·δ − F)/(k + k_s).
- **Open seat** (C2 above): T_ref = F and N = 0.
- **F_sep** = k·δ. **T_block** = k·u·μ_p − √((k·u·μ_p)² − 2·k·u·F_act). **P** = k·δ·k_s/(k + k_s).
- **C5 reference:** integrate the one-degree-of-freedom axial model of B on the link with the seat open, using classical RK4 at 1 µs: m·ẍ = F − e(t)·(k·x + c·ẋ). It starts at x = F/k, ẋ = 0 at t_r = 0.5 s, with e(t) = 1 − (t − t_r)·v_max/u_full and c the declared axial c_full (Q56, reduced-mass convention, exactly the value the solver rows use at e = 1). The moving mass is B's mass m, because A is static. Separation is the first instant where k·x + c·ẋ > T_full, because T = e·(k·x + c·ẋ) and the limit is e·T_full. The blocked case (factor 1.1) has no separation.
- **C6 removal** at t_r + u_full/v_max.
- **C7:** ω = √(e·k/μ_red) for axial runs, √(e·k_t/I_red) for torsion.

**Analytical expectations recorded before any run:**

| Quantity | Value |
| --- | --- |
| P | 0.476190 N |
| C1 T_ref, N_ref | 0.485530 N, 0.289397 N |
| F_sep | 0.5 N |
| T_block | 1.267949 N |
| C5 separation (factor 0.9) | about t_r + 0.043 s |
| C7 axial ω·Δt at e = 1 | 0.05, 0.1, 0.2 |
| C7 torsion at 200 µs, e = 1 | ω·Δt = 0.245: `outside_envelope` |

## Metrics

| Check | Metric | Limit |
| --- | --- | --- |
| C1 | Window means: \|T − T_ref\|/T_ref; \|N_ax − N_ref\|/N_ref; \|T − N_ax − m·g\|/(m·g); guide contact count = 4 at every window sample | 1e-3; 1e-3; 1e-3; exact |
| C2 below | As C1 with F = 0.9·F_sep, and N_ax > 0 at every window sample | 1e-3 |
| C2 above | Max over window samples of Σ guide f_n; \|T − F\|/F | ≤ 1e-9 N; 1e-3 |
| C3 below (per axis × e) | No separation in the run. Window-mean deflection (ext[0], ext[1], rot[1], rot[0] for tension, shear, bending, torsion) vs L_target/(e·k_axis) | 1e-2 |
| C3 above | Separation occurs. **Rule:** at the separation step the axis load > limit(e), and at every earlier step every axis load ≤ limit(e). **Accuracy:** \|L(t_s) − limit(e)\|/limit(e). **After:** at every later sample the link is inactive, and its reported force and moment are exactly zero | exact; 1e-2; exact |
| C4 engage | First sample with u = u_full at t vs u_full/v_max; every \|e_after − e_during\| ≤ v_max·Δt/u_full·(1 + 1e-12); window-mean T vs P | 2 steps; exact; 1e-3 |
| C4 blocked | u = 0 and the link inactive at every sample | exact |
| C5 below | \|t_s − t_ref\|; during [t_r, t_s), u decreases by v_max·Δt per step (rel 1e-12) | 2 steps; exact |
| C5 above | u = u_full at every sample; no separation; the link is active at the end | exact |
| C6 | Removal time vs t_r + u_full/v_max; max \|T_n − T_{n−1}\| over steps after t_r vs 2·k·δ·v_max·Δt/u_full; after removal the link is inactive with zero reported force | 2 steps; ≤ 1; exact |
| C7 | Q52 measures (protocol of `compliant-link-v1-protocol.md`, revision 2): mean period vs 2π/ω (axial and torsion, ζ = 0); ζ measured vs 0.05; \|ζ_num\| (ζ = 0) | 1e-2; 25 %; 0.01 |
| C8 | Per run: every audit passes. The outcome is classified, not gated | — |
| C9 | `velocity_snap` fails the impulse audit, and `pose_snap` fails the pose audit, at every Δt | exact |
| C10 | Every run's final-state SHA-256 is reproduced by an immediate in-process replay | bit-identical |

**Audits** run on every C1–C8 run, on its dynamic bodies:

- **Momentum** (runs without a static body): max over t > 0 of \|p − (p₀ + M·g⃗·t)\|/(1e-9·M·g·t + 1e-12). Validation loads in C3 are equal and opposite, so they do not enter. Limit ≤ 1.
- **Impulse accounting:** for every step and every dynamic body,
  - linear: \|m·(v_n − v_{n−1}) − Δt·(m·g⃗ + ΣF)\| ≤ 1e-9·Δt·(m·g + Σ\|F\|) + 1e-15
  - angular: \|I·(ω_n − ω_{n−1}) − Δt·Στ\| ≤ 1e-9·Δt·Σ\|τ\| + 1e-15

  ΣF sums the reported contact forces on the body (normal·n + tangential), the reported link force (on B, its negative on A; coupler components rotated to world by A's orientation **at step start**), and the applied validation loads. Στ sums r × F at the reported contact points and at the anchors (r from the body's step-start pose), the link moment (±), and validation torques. A uniform cube has isotropic inertia, so I is a scalar and no gyroscopic term exists.
- **Pose integration:** x_n is bit-identical to x_{n−1} + Δt·v_n, and q_n is bit-identical to `q_{n−1}.integrate(ω_n, Δt)`, computed with the same `math3` operations.
- **Energy** (C4, C6, C7, C8, which are free fall without validation loads), in the centre-of-mass frame:
  - E_n = Σ ½·m·\|v − v_cm\|² + ½·I·\|ω\|² + V_link + V_contact
  - V_link = ½·Σᵢ e_during·k_i,full·C_i², with C the six reported coordinates of step n
  - V_contact = 0 at samples whose step reported no guide contact. At the final sample it is Σ f_n²/(2·k_contact).
  - Energy is evaluated at contact-free samples and at the final sample. W_n is the sum of link-potential changes made by coupler updates (pawl travel and removal) **made before step n** (those of steps 1..n−1; revision 2, Q58), so that it pairs with V_link's e_during at sample n: at each update, ½·Σ k_i,full·C_i²·(e_after − e_during), counting e_after as 0 when the link is removed.
  - Metric: max over evaluated samples of (E_n − E_0 − W_n) / (0.02·E_ref + 1e-12 J) ≤ 1, with E_ref = KE_rel(0) + max V_link + max \|W\|.
  - The 2e-2 comes from the shadow-energy oscillation of the q = 1/4 link step, (ω·Δt)²/4 ≤ 1e-2 at the resolution limit, with a factor of 2. The check is one-sided: dissipation is allowed, creation is not.

**C8 validity and classification.** A run is `outside_model` (listed, not counted) if any sample has the two cubes overlapping (oriented-box separating-axis test, 15 axes) or the ball centre's lateral coordinates outside ±8 mm of the axis. The final-sample classification is:

| Class | Condition |
| --- | --- |
| `captured` | link active, e = 1, ball centre inside the capture zone |
| `partial` | link active, e < 1 |
| `separated` | link inactive after having been active |
| `latch_blocked` | link never active, ball centre at x < 0 |
| `missed` | otherwise |

**Capture window report.** For each (friction pair, direction, θ₀, v, Δt), the report lists the captured offsets and the capture radius: the largest grid offset at and below which every offset is captured. The true boundary lies within one grid step (1 mm) above it. `dt_disagreement` flags any offset whose class differs across Δt. These are measured envelope data with their resolution as uncertainty (CPL-006). They are not pass/fail.

## Outcome aggregation

As Q48 and Q52: per case, over evaluated combinations (sub-run × Δt, or sweep run), all pass → `pass`, all fail → `fail`, mixed → `uncertain`. `outside_envelope` (C7 resolution) and `outside_model` (C8 validity) are listed and not counted. If nothing is evaluated the case fails. Every metric must be finite; a non-finite value fails.

## Revision log

| Date | Change | Reason | Results affected |
| --- | --- | --- | --- |
| 2026-11-02 | Initial protocol (revision 1), before any coupler solver code | — | — |
| 2026-11-03 | **Revision 2. Pre-run clarification, made before any coupler suite run existed** (no results observed). The energy audit's W_n sums the coupler updates of steps 1..n−1, not 1..n. Nothing else changes | Revision 1's "up to sample n" was ambiguous. V_link at sample n uses e_during (the engagement the step ran at), so the matching work excludes step n's own update. Found while testing the evaluator on synthetic data | None. Ruled by Q58 |

Any change after observing results requires its own decision record before the rerun counts as official (Q49 safeguard).
