# Q58 — Coupler protocol revision 2: indexing of the energy audit's pawl work

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-03 |
| Supersedes | **Protocol revision 1's wording of W_n only** ("up to sample n", `docs/validation/coupler-engagement-v1-protocol.md`). Criteria `coupler-engagement-v1.json` is unchanged and stays registered |
| Provenance | **agent decision under explicit owner delegation** ("I trust its judgement"). The owner may revise it through a superseding record |

## Context

Protocol revision 1 defines the energy audit as E_n − E_0 − W_n, with V_link taken at the engagement e_during of step n and W_n "the sum of link-potential changes made by coupler updates up to sample n". Written literally, W_n includes the update that follows step n, whose effect on e only appears in step n+1's e_during. The audit would then charge work against a potential that has not yet changed. A synthetic test (frozen stretch, declared pawl drop of e from 1 to 0.5) showed a spurious energy creation of ½·V_full.

## Decision

W_n is the sum of the pawl-update work of steps 1..n−1. The pawl work of step n pairs with sample n+1. Nothing else changes: the tolerance (2 %), the reference energy, the sample selection, and the criteria file stay as registered.

## Safeguards (Q49)

- No coupler suite run exists yet, so no result has been observed. This is a pre-run clarification, not a post-hoc change.
- The corrected form is the only one in which a declared pawl action is neutral to the audit. A real energy creation still fails: the audit remains one-sided and the C9 controls must still be caught.
- Revision 2 is logged in the protocol's revision log.

## Consequences

- `coupler_eval.zig` implements revision 2. Governing criteria hash is unchanged.
