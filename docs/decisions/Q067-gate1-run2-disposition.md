# Q67 — Gate 1 run 2 disposition (cand-a v2)

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-06 |
| Supersedes | — (clarifies Q66 §4 wording; changes no criterion, threshold or verdict) |
| Provenance | **agent decision under explicit owner delegation** |

## Context

Run 2 (`results/gates/gate1-v1/run2-3e3d63b-ReleaseSafe.json`, clean tree, unchanged criteria) gives cand-a v2 `unresolved`. G1–G5, G7 and G8 pass. G6 is `unresolved` because the independent retention review is unresolved.

## Decision

1. **The verdict stands.** v2 is not edited after review. Any change is a v3 with new r1 reviews (Q61 §5).
2. **Clarification of Q66 §4.** Q66 says "no spring holding it closed". That wording is wrong. The declaration has a 0.33 N bias spring. The intent was that the lock is meant to come from dead-centre geometry and not from spring force. The reviewer correctly found that the declared spring direction does not make the toggle bistable. The declaration governs, and the gap is a v3 item.
3. **Work items for v3** (from retention review §6):
   - toggle pin coordinates, over-centre offset with its tolerance, stop, and spring position and direction;
   - a closing, holding, opening and holding-open force balance;
   - a consistent tension path, with the puck wall and the puck-to-body bearing declared and checked;
   - a torsion check for the half-hex cup, not a full socket;
   - the cup opening direction and the tongue tip form;
   - an axial and heading pre-alignment means, or an explicit statement that none exists;
   - a cited SLS tolerance.
4. **Originality residual risk.** v2's D2 is rated high against both CONRO and PolyBot G2, for SMA-released latches on grooved pins. A second high against either reference would fail rule 2. A v3 should prefer a release principle other than an SMA-released latch.
5. **Corpus follow-ups** (append-only, later record):
   - The C12 PolyBot descriptor omits its SMA latch.
   - The C23/Q64-C23 URL resolves to a different SoCG 2021 paper.
   - The Science Robotics paper behind Q64-C22 and the HAL paper behind Q64-C24 were not readable.
6. **No family is selected or abandoned.** R10 stays blocked (no survivor).
