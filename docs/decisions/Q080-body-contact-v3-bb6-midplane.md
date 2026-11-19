# Q80 — Body-contact criteria v3: BB6 swap check on the contact midplane

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-19 |
| Supersedes | `criteria/fixture-validation/body-contact-v2.json`, BB6 `swap_check` only. Every other value is unchanged |
| Provenance | **agent decision under explicit owner delegation** |

## Context

The Q79 v2 rule ("swapped point = (A, B) point translated by one depth") was the lead's error.
- It holds only when swapping the pair exchanges the incident box, as in face-face contact (BB6a).
- In edge-face contact (BB6b) the same reference face wins in both orders. In edge-edge contact (BB6c) the midpoint is symmetric.
- A non-official run in the `bb-v2` graft (commits `a481f20`, `cf34402`) showed BB6a passing and BB6b and BB6c failing by exactly one depth. No official run used v2.

## Decision

The swapped manifold must have:
- the negated normal;
- the same depth;
- the same point count;
- the **same point set after projecting each point onto the contact midplane**.

Projected onto the midplane, a point does not depend on which box is incident. Run 2 uses criteria v3.
