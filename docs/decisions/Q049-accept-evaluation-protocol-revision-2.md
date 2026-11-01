# Q49 — Acceptance of evaluation protocol revision 2

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-01 |
| Supersedes | — (affirms protocol revision 2 of `docs/validation/fixture-analytic-v1-protocol.md`) |
| Provenance | **agent decision under explicit owner delegation** ("make a decision for this"). The owner may reverse it through a superseding record |

## Context

Run 1 of the analytic fixture-validation suite (`7c7581f`) gave: friction threshold `uncertain` (6/9), slide to stop `fail` (0/9), the rest `pass`. The agent then revised the evaluation protocol (revision 2) and reran (`cd59f3e`): all five cases `pass` 9/9. Revision 2 was made **after observing results**, so it needed an explicit ruling. The same agent made the revision and this ruling. That conflict is mitigated by the safeguards below, not ignored.

## Decision

**Revision 2 is accepted. Run 2 is the official result for criteria v1. Run 1 is kept as superseded evidence.**

1. **Settled initial state: accepted.** "At rest on the table" means static equilibrium of the contact model. Run 1 placed fixtures on uncompressed contacts, a state no resting body occupies. In the first 0.5 ms step the table carried 0.83·m·g, so the run 1 slip reflects that non-physical initial condition, not the friction threshold. Settling unloaded for 0.5 s before t = 0 is the physically correct reading of the case.
2. **Contact-patch stop detection: accepted.** The case measures *sliding* to a stop, and sliding is relative motion at the contact. Run 1 shows sliding ceases within one step of v0/(μk·g), with distance within 0.5 mm. The CoM speed then reflects about 3 ms of decaying rocking on the compliant contact (v_com = ω·h_com). That is real model behavior, but it is not sliding.

## Why this is not threshold tuning

- Every registered threshold, every friction pair and timestep, and every solver setting is unchanged.
- Both changes correct *what is measured* to match the case's stated physical meaning. Neither loosens a limit.
- The diagnosis is reproducible from the preserved run 1 report and the committed code at `7c7581f`.

## Safeguards

1. Run 1 stays in `results/` and in the results table. It is never deleted or relabeled.
2. The revision-1 CoM-speed stop metric stays in every report as an informational metric. It currently fails (9.2 ms vs a 4 ms limit at Δt = 2 ms), so the rocking behavior stays visible.
3. Any future change to an evaluation protocol made after observing results requires its own decision record **before** the rerun counts as official.
4. The next criteria version for these cases must state the initial-state and stop definitions in the criteria file itself, not only in the protocol, so they are covered by the registered hash.

## Consequences

- PHY-001, PHY-005, PHY-007, and BEN-010 evidence rests on run 2, labeled `fixture`, within the documented envelope.
- Nothing here qualifies the solver (PHY-011) or makes any claim about Kin candidates.
