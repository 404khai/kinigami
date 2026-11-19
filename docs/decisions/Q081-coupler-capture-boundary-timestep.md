# Q81 — Coupler capture boundary vs physics timestep (preregistered study)

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-19 |
| Supersedes | — (implements the R8 follow-up "Δt-sensitive capture boundary"; changes no criterion, setting or result) |
| Provenance | **agent decision under explicit owner delegation** (lead: Claude Opus 5.5) |

## Context

R8 run 2 and run 3 report that 65 C8 offsets disagree across Δt ∈ {50, 100, 200} µs: the capture boundary is Δt-sensitive at the sweep's 1 mm offset resolution. C8 is reported and never gated (CPL-006). This record declares, **before any code**, a study of how that boundary moves with Δt and whether it converges.

## Decision

1. **Purpose.** Characterise, for each declared approach axis, how the lateral-offset capture boundary moves with the physics timestep, and whether it converges as Δt shrinks.
2. **Label:** `exploratory`, enforced in code. No criterion, threshold, protocol or official setting changes. The official `--coupler` path and run 3 are untouched.
3. **Geometry and settings.** The C8 sweep of `criteria/qualification/coupler-engagement-v2.json` (unchanged): every (friction pair, offset direction, θ0, v) combination is one **axis**, 36 in all. Protocol solver settings. The criteria's own Δt grid {50, 100, 200} µs is a subset of the study grid, so the study grid is **Δt ∈ {25, 50, 100, 200} µs**, with 25 µs added.
4. **Boundary definition.** The criteria's capture radius: the largest lateral offset at and below which every offset is `captured` (`outside_model` counts as not captured), the same rule as `captureRadius`. Per axis and Δt: run the criteria's offset grid, take the first grid offset that is not captured as the upper end and the grid offset below it as the lower end, then **bisect to a fixed resolution of 10 µm** (the final bracket is at most 10 µm wide; the reported boundary is the bracket's lower end, a captured offset). Bisection assumes one transition inside the bracket; this is an assumption, stated, not tested. Two special cases are reported and not fitted: `none` (offset 0 is not captured) and `censored` (all grid offsets captured, boundary at or above 5 mm).
5. **Fit.** With b(Δt) the boundary, using the three finest steps: r = (b(100) − b(50)) / (b(50) − b(25)); observed order p = log2(r) when r > 0, else `not_monotone`. Extrapolation b0 = b(25) − (b(50) − b(25)) / (2^p − 1) when p is defined and 0.5 ≤ p ≤ 4; fixed-order extrapolations for p = 1 and p = 2 are always reported. With only four points and a 10 µm resolution the order is an estimate, not a measurement.
6. **Outcome rule, fixed now.** An axis is **converged** if |b(25) − b(50)| ≤ 0.1 mm and |b(25) − b(50)| ≤ |b(50) − b(100)|. Otherwise it is **not converged**. The 0.1 mm bound is **provisional**, chosen as ten times the bisection resolution and one tenth of the criteria's offset step, and has no physical evidence behind it. The study is **converged** if every axis with a boundary is converged, **partially converged** if at least half are, else **not converged**.
7. **Recommendation rule, fixed now.** The study reports the largest Δt in the grid for which every converged axis satisfies |b(Δt) − b(25)| ≤ 0.1 mm, as the **candidate maximum Δt for capture claims**. If the study is not converged, no maximum is recommended and the finding is that capture claims need a finer Δt than 25 µs, or a criteria change that needs its own record. Adopting any maximum Δt, or changing the C8 grid, Δt set or C8 reporting, needs a superseding decision record. This study does not change them.
8. **Reported.** Per axis: the boundary at each Δt, the class, the fitted order, the extrapolation, and the convergence verdict; the study verdict and the candidate maximum Δt. Resource: runs are deterministic and in-process only. A preview run is not an official record. An official run, if any, needs its own record under `results/qualification/coupler-engagement-v1/`.
9. **Implementation.** `kinigami-qualify --coupler-capture-dt <dir>`, writing one JSON file. No solver or evaluator behaviour changes.

## Limits

This characterises the provisional stand-in (Q56) on neutral fixtures. It is not evidence about any Kin coupler, and it does not show that any Δt is physically correct, only whether the boundary stops moving.
