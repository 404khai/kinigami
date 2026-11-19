# Q82 — Disposition of the capture-boundary timestep study (Q81)

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-19 |
| Supersedes | — (changes no criterion, threshold or official setting) |
| Provenance | **agent decision under explicit owner delegation** |

## Context

The Q81 study (`results/qualification/coupler-engagement-v1/capture-dt-9dc7b48/`, exploratory) is **partially converged**. 8 of 16 analysable axes meet the provisional test, and several of those only weakly. Every toward-corner axis moves by up to 1.5 mm, and non-monotonically. At v = 0.3, capture appears or disappears with Δt.

## Decision

1. **No maximum timestep is adopted.** The rule's printed 50 µs is not used.
2. **The R8 limitation is restated.** "The capture boundary is Δt-sensitive and not converged at 25 µs for the fixture stand-in (Q81)." Capture envelopes are reported per Δt and are never claimed to be Δt-independent.
3. **Run 3's C8 pass stands as evaluated.** C8 is evaluated per Δt under criteria v2, and nothing in it claimed convergence.
4. **Follow-ups, if a converged capture envelope is ever needed** (for example by Gate 2 for a real coupler):
   - a finer Δt (12.5 µs and below);
   - a per-axis multi-transition search, since bisection assumes a single transition;
   - a diagnosis of the v = 0.3 window flips.

   Each needs its own preregistration. It is not urgent: the stand-in is not a Kin coupler.
