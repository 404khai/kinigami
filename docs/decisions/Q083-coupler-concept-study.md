# Q83 — Coupler concept study v1 (paper, exploratory)

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-19 |
| Supersedes | — (changes no requirement, criterion, threshold or verdict; selects no candidate, family or mechanism) |
| Provenance | **agent decision under explicit owner delegation**. Lead: Claude Opus 5.5 |

## Context

cand-a stopped at v5 with `fail` on G6 (Q73), and candidate revisions were paused (Q74). The body-body contact slice (Q76 to Q80) is done, so unit-to-unit contact can inform coupler design again. Before any new declaration, a short comparison of coupler concepts against the cand-a lessons is useful.

## Decision

1. Record `docs/studies/coupler-concepts-v1.md`. It is a paper study labelled **exploratory**. It lists the cand-a v1 to v5 failure modes, the requirements every coupler must meet (Q11, Q31, Q36, CPL-005/006/008/009, Gate 1 G6), and four concepts (K1 second pin, K2 keyed boss, K3 magnet with mechanical release, K4 load-sensed lead-screw keeper) with computed numbers or **UNRESOLVED**.
2. **It selects nothing.** Geometry, couplers and mechanisms are chosen only through the Q38 gates (CPL-011 stays `unresolved`). The study's recommendation (K4 with K1 on body a, as a possible cand-a v6 declaration) is input for the owner at a gate and starts no candidate work by itself.
3. New computed values come from `candidates/cand-a/scripts/pin2.py` plus an added swept-path check (not committed), and from the formulas shown in the study. One magnet figure (K&J D41, 5.29 N pull, case 1) is from a search snippet; the vendor page was not readable, so the force-versus-gap curve is UNRESOLVED.
4. Q74 stays in force: no candidate revision starts without the owner asking.
5. Numbering note: this checkout contains decisions up to Q80; Q83 is the number requested.

## Alternatives considered

- **Write cand-a v6 directly.** Rejected: Q74 pauses revisions, and the study shows an open packaging question (K4 drive layout) that a declaration would hide.
- **Rank the concepts with a weighted score.** Rejected: the scores would hide the decisive numbers and invent weights.

## Consequences

Docs only. No code, criteria or declarations changed. Traceability and requirements are unchanged.
