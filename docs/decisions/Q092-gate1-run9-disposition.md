# Q92 — Gate 1 run 9 disposition (cand-d v4)

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-20 |
| Supersedes | — (changes no criterion, threshold or verdict) |
| Provenance | **agent decision under explicit owner delegation** |

Run 9 (`run9-dbb2dc4-ReleaseSafe.json`) gives cand-d v4 `unresolved`. G6 is unresolved with no contradiction (`retention-review-v4-r1.md` §7). G1–G5, G7 and G8 pass.

## Decision

1. The verdict stands. v4 is preserved as `declaration-v4.json` when v5 is written.
2. **cand-d v5 is started.** The decisive item is seating at the guaranteed lower-bound motor torque:
   - With dry 304-on-304 tooth friction (μ up to 0.8) the teeth cannot roll or yaw a unit flat, and the residuals can take the seat out of the 3 deg lock stage.
   - The lock stage cannot be lengthened with two lugs at 180 deg.
   - v5 therefore raises the guaranteed seating force and lowers tooth friction. Raising the closing voltage needs a sleeve material with a higher contact limit.
3. **Lead's error recorded.** v4's fallback argument treated only pitch, although roll and yaw residuals act in the same way.
4. No survivor exists, and R10 stays blocked.
