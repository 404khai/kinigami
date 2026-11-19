# C8 capture boundary vs physics timestep (Q81, exploratory)

- **Preregistration:** Q81, committed at `c4a9ab3` before any code or run.
- **Code:** `9dc7b48` (clean tree), ReleaseSafe, `kinigami-qualify --coupler-capture-dt`.
- **Criteria:** C8 geometry of coupler-engagement v2, unchanged.
- **Grid:** Δt ∈ {25, 50, 100, 200} µs.
- **Search:** 36 axes, with the boundary located by bisection to 10 µm. 902 runs, about 4 minutes.
- **Reproducibility:** this report is identical to the preview run in the graft.

## Verdict: **partially converged**, so the study does not support a timestep limit

- **No boundary (12 axes):** every θ0 = 0.15 axis. Offset 0 is never captured.
- **Not analysable (8 axes):** at v = 0.3 the capture window exists at 25, 50 and 200 µs but not at 100 µs, so capture itself flips with Δt.
- **Analysable (16 axes):** 8 meet the provisional convergence test (|b25 − b50| ≤ 0.1 mm and not growing).
  - Many of these pass on a coincidentally small difference, with undefined or negative fitted order.
  - All 8 toward-corner axes fail. Their boundaries move by 0.1–1.5 mm, non-monotonically (for example 1898 / 1625 / 1484 / 664 µm).
- **Magnitudes:** the boundaries span 0.4–2.6 mm. Only 5 axes support an extrapolation, from 740 to 2551 µm, each resting on a single noisy order.

## Interpretation (Q82)

- The rule's literal candidate maximum, 50 µs, is **not adopted**: the study verdict is not "converged".
- The fixture stand-in's capture boundary is **not Δt-converged** down to 25 µs. Capture claims hold only as stated at each tested Δt, never as Δt-independent.
- Run 3's C8 pass stands, because it is evaluated per Δt under its criteria. It does not establish a converged capture envelope.
