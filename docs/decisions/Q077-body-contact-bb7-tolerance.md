# Q77 — Body-contact BB7 invariance tolerance

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-19 |
| Supersedes | Q76 §5, the BB7 value only ("BB7 invariance uses 1e-9 relative") |
| Provenance | **agent decision under explicit owner delegation** |

BB7 frame invariance in `criteria/fixture-validation/body-contact-v1.json` (registered `183b5a2`) uses **1e-6 relative**, with the stop step index within **one step**. Both are provisional. The value was set at lead review **before registration and before any solver code**, so no result informed it.

Reason: a rigidly rotated scene is not bit-identical in IEEE 754 arithmetic. Friction stick-slip over 1000 or more steps can amplify rounding, so 1e-9 would fail a frame-independent solver. 1e-6 is still at least 100× tighter than the physics tolerances (1e-4 m penetration, 1e-3 relative force), so a real frame dependence still fails. BB6 geometry keeps 1e-9.
