# Q55 — Links in recordings: format version 3

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-02 |
| Supersedes | **Q51's payload contents, extended**: Q51's interval, its per-body and per-contact fields, and its encoding rules all stand |
| Provenance | **agent decision under explicit owner delegation** ("make the decisions") |

## Context

Fixture links are qualified (run 2, Q53, Q54), but recording format v2 (Q51) has no place for them. The compliant-link suite therefore writes no recordings, and its runs cannot be inspected (inspectability, priority 6).

## Decision

**Recording format version 3:** Q51's payload plus link sections. The writer always produces v3. Readers keep v1 and v2 (DAT-010).

- **Scene header** gains, after the bodies, `link_count u32` and per link:
  - `body_a u32 | body_b u32`
  - `axes_a 3 × (3 × f64)`: the anchor-A frame axes in body A's frame (axial, shear 1, shear 2), exactly as the solver uses them
  - `anchor_a_m 3 × f64 | anchor_b_m 3 × f64` (body frames)
  - `rest_length_m f64`
- **Body kind** gains `static_fixture = 2` (v3 only). Its `mass_kg` is written as 0 and means infinite. Non-finite values stay forbidden (DAT-008).
- **Snapshot** gains, after the contacts, `link_count u32` (must equal the header's) and per link the solver-native report (PHY-005), in anchor-A components:
  - `force_on_b_n 3 × f64 | moment_on_b_nm 3 × f64 | extension_m 3 × f64 | rotation_rad 3 × f64`
  - At t = 0 the force and moment are zero (no step has produced them), as in the evaluator's sample 0.
- **The link suite records** every official run when asked (`--recordings`), one snapshot per step, as Q51 does.
- **The inspector draws** each link as the segment between its anchors and the force on B as an arrow at anchor B. Anchor positions and the force direction are rigid transforms of recorded values by recorded poses and recorded axes. This is presentation, not physics (INS-005).

## Rationale

- Recording the axes makes the force direction a pure display transform, so the inspector never re-derives solver geometry.
- The `static_fixture` kind avoids encoding an infinite mass.

## Alternatives considered

- **World-frame link vectors.** Rejected: they duplicate data, and they would make the recording disagree with the evaluator's anchor-frame samples.
- **A separate link chunk type.** Rejected: links belong to the same instant as the bodies and contacts.

## Consequences

- Analytic-suite recordings become v3 with zero links. Their simulation hashes are unaffected, because recording never feeds back into the simulation (INS-007).
- The inspector accepts v2 and v3 recordings.
