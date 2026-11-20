# Q86 — Gate 1 run 6 disposition (cand-d v1)

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-20 |
| Supersedes | — (changes no criterion, threshold or verdict) |
| Provenance | **agent decision under explicit owner delegation** |

Run 6 (`run6-efe5163-ReleaseSafe.json`) gives cand-d v1 `unresolved`. It passes G1–G5, G7 and G8. G6 is `unresolved` because the retention review found nine open items (`candidates/cand-d/retention-review-v1-r1.md` §6). None is a contradiction of passive retention.

## Decision

1. The verdict stands, and v1 is preserved as `declaration-v1.json` when v2 is written (Q65 layout).
2. **cand-d v2 is started.** The root causes are fixable inside the 60 mm envelope (stowed margin 1.14 mm):
   - an unbuildable mount;
   - a friction-only torsion carrier;
   - missing stops;
   - an optimistic supply voltage;
   - a citation error.

   This differs from cand-a, whose shortfall was volume.
3. **Process correction.** A page-summarising fetch tool gave the lead a value that is not on the page ("bronze on steel dry 0.35"). From now on, every cited number in a cand-d declaration is checked against the raw source text: `curl` of the page or PDF, then `grep` or `pdftotext`. The dossier states how each was checked.
4. Originality r1 passes on v1. It must be redone for v2, because the coupler changes (Q61 §5).
5. No survivor exists, and R10 stays blocked.
