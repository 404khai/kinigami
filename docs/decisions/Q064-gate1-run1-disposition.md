# Q64 — Gate 1 run 1 disposition: corpus additions, candidate fate, evaluator note

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-05 |
| Supersedes | — (amends no criteria; extends the Q61 reference corpus by appending) |
| Provenance | **agent decision under explicit owner delegation** ("make the decisions"). The owner may revise it through a superseding record |

## Context

Gate 1 run 1 (`results/gates/gate1-v1/run1-b1d0a81-ReleaseSafe.json`) produced no survivor: cand-a is `unresolved`, cand-b and cand-c `fail` G5. The independent reviews found references missing from the corpus and left several ratings provisional.

## Decision

1. **Corpus additions.** Entries C21–C29 are appended to `docs/originality/reference-corpus.md` (CONRO, hexagonal electrohydraulic modules, Hinged Pixels, rolling hexagonal-lattice modules, PenduMorph, Rotundus GroundBot, Sphero/BB-8, MOPARAS, the pendulum-sphere literature). They are flagged as sourced from search summaries and are provisional. Existing entries and review records are not changed.
2. **Run 1 stands as reported.** Its reviews are r1. Any candidate revision gets a new version and new r2 reviews against the extended corpus, reading primary sources for every moderate or high cell.
3. **Candidate disposition.** No family is abandoned and none is selected. All three stay preserved (SEL-007). **No revision is authored now:** a revision needs real engineering numbers (lock sizing, a supported-chain geometry) and inventing them to pass G5 or G6 would be unfounded design selection (Q38). Revisions are future work at the owner's call.
   - cand-a: nearest to passing. Its open items are G3 estimates, the G6 sizing, and the rigid-coupler versus Q31 chain-bending conflict.
   - cand-b: needs a supported-chain pose, retention dimensions, and a response to the CONRO high rating.
   - cand-c: needs a supported-chain geometry, retention numbers, and differentiation from Rotundus and PenduMorph.
4. **Evaluator note.** The run report prints `protocol_revision 1` although Q63 made revision 2 current. This is a labelling gap only. It is left as is (editing the evaluator after a run needs a rerun); a later version of the evaluator should print the protocol revision it implements.
5. **Next phases.** R10 (sensors, actuators, communication) is blocked until a candidate survives Gate 1. The independent R8 follow-ups (cube-cube contact, coupler solver-settings sensitivity) are the productive work meanwhile.

## Consequences

- The corpus is larger. Earlier verdicts rest on the corpus as it stood and say so.
- Nothing is promoted. The paper gate is not feasibility evidence.
