# Q78 — Body-contact protocol revision 2: axis-selection hysteresis and the angular snap control

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-19 |
| Supersedes | — (revises `docs/validation/body-contact-v1-protocol.md` to revision 2; the criteria JSON and every threshold are unchanged) |
| Provenance | **agent decision under explicit owner delegation** |

## Context

A **non-official preview** of the BB1–BB9 suite, run during implementation, found two defects. Neither is a criteria value, but both depart from the literal wording of protocol rev 1. They are recorded here before the official run 1, which uses the unchanged registered criteria `body-contact-v1` (sha256 `26b2f8dc…`). Disclosure: the motivation came from the preview.

## Decision

1. **SAT axis selection (protocol §contact generation).** Rev 1 broke ties "by fixed axis order" with exact double equality. In near-parallel stacks, rounding made an edge axis win by about 1e-9 m. The whole weight then sat on one row, the row count flapped, warm start was lost, and the stack rocked. That caused BB1 `mu_high`/500 µs and the BB7 frame dependence.

   Rev 2 rules:
   - face and edge axes are tracked separately;
   - overlaps within 1e-9 m keep the lower index;
   - an edge axis is chosen only if its overlap is below 0.95 of the best face overlap, minus that margin.

   Both constants are **provisional**. The rule uses no world axis, and the BB6 closed forms are unchanged.
2. **BB8 angular-velocity snap control (protocol §BB8 controls).** Rev 1 did not define the snap. The preview's choice ("B's ω := A's ω at first contact") was a null change, because both were equal at that instant. Rev 2 defines it as resetting B's angular velocity at first contact to its pre-contact value. That is a real velocity change, which the audits must detect.
3. **Recorded and left open:**
   - **BB6 swap.** Rev 1 says the swapped pair gives "the same point set", and also that points lie on the incident face. These conflict by one depth (5e-4 m) for face-face contact. This is a criteria-level conflict, left for a superseding criteria version.
   - **BB8 angular momentum.** At the protocol's 100 PGS sweeps, the friction rows leave an off-axis spin of about 1.6e-4 rad/s. With no gyroscopic term, that makes L drift after separation. At 1000 sweeps the residual is 1.8e-11 rad/s. This is a solver-setting or modelling question, decided after run 1 by a separate record. It is not tuned here.
