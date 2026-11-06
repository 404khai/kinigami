# Q63 — Gate 1 paper-gate protocol clarifications

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-05 |
| Supersedes | — (clarifies Q61 and Q62 and `docs/validation/gate1-v1-protocol.md`; changes no criterion, threshold, candidate, or criteria JSON) |
| Provenance | **agent decision under explicit owner delegation** ("I delegate all decisions"). The owner may revise it through a superseding record |

## Context

Writing the Gate 1 evaluator (`src/core/gate1_eval.zig`) and the first candidate declarations exposed four points the protocol leaves unclear or states wrongly. This record fixes how they are read. `criteria/gates/gate1-v1.json` is not edited and keeps its registered SHA-256.

## Decision

### 1. Review-record format (ratified)

The evaluator reads review records as Markdown files whose machine-read content is `key: value` lines with the key at column 0. The value is trimmed of spaces, tabs and CR. A key that appears twice makes the record incomplete. Other text (prose, tables, indented lines) is ignored by the evaluator.

Paths, as in the criteria file:

- originality: `candidates/<candidate_id>/originality-review-gate1-v<candidate_version>-r<n>.md`
- retention: `candidates/<candidate_id>/retention-review-v<candidate_version>-r<n>.md`

Keys:

- both records: `candidate_id`, `candidate_version`, `author`, `reviewer`, `outcome` (`pass`, `fail` or `unresolved`)
- originality only: `declaration_sha256`, `stage` (`gate1`), `high_cells_f1_f2` (count of `high` matrix cells against F1/F2 references), `exclusion_cube_with_internal_flywheel` and `exclusion_needle_or_particle_silhouette` (each `present` or `not_present`)

The reviewer must differ from the author. A record with a different `candidate_id`, a `declaration_sha256` that differs from the current declaration, or a missing key is not valid and gives `unresolved` for the dependent items.

Template, originality record:

```markdown
# Originality review (Q61, stage gate1): <candidate_id> v<candidate_version>, r<n>

candidate_id: <candidate_id>
candidate_version: <candidate_version>
declaration_sha256: <64 hex characters>
stage: gate1
author: <name of the declaration author>
reviewer: <name of the independent reviewer; not the author>
high_cells_f1_f2: <integer, 0 or more>
exclusion_cube_with_internal_flywheel: <present | not_present>
exclusion_needle_or_particle_silhouette: <present | not_present>
outcome: <pass | fail | unresolved>

Free-form findings, matrix, family check and sampled sources go here, with no
line starting at column 0 in `key:` form for the keys above.
```

Template, retention record:

```markdown
# Retention review: <candidate_id> v<candidate_version>, r<n>

candidate_id: <candidate_id>
candidate_version: <candidate_version>
author: <name of the declaration author>
reviewer: <name of the independent reviewer; not the author>
outcome: <pass | fail | unresolved>

Free-form justification that the declared retention mechanism holds the units
in the stated orientations goes here.
```

### 2. Endurance units

Protocol section 6 item 3 computes `endurance_s = energy_mj · 1000 / P_avg_mW`. That is dimensionally wrong: a millijoule divided by a milliwatt is seconds, so the correct value is `energy_mj / P_avg_mW`. Endurance is **reported only**; it never gates, never enters the outcome, and its threshold stays `unresolved` (Q62). The evaluator already prints both the correct value (`endurance_s`) and the literal protocol value (`endurance_s_protocol_literal`), and sets `endurance_enters_outcome` to false. The protocol records this as revision 2. The evaluator's gating behavior does not change.

### 3. Known limitation, recorded and not fixed: G5 pose set

G5 uses a single pose set (the stowed layout) for the support-polygon test. A body that folds or deploys (cand-b) is therefore judged in its stowed layout, not in an operating layout. Fixing this needs a superseding criteria version and a separate decision. No candidate is changed because of it, and a G5 result for a folding body must be read with this limitation.

### 4. Stowed diameter of exactly 60.000 mm

The G1 limit is exactly 0.060 m (Q12), and the numerical band is 0.001 µm. A computed diameter within that band of 60.000 mm is `unresolved`, as implemented. Exactly 60.000 mm is therefore unresolved, not a pass.

## Consequences

- No criterion, threshold, candidate or criteria file changes. The registered hash of `criteria/gates/gate1-v1.json` is unchanged.
- Reviewers have one format to follow, and the evaluator reads exactly that format.
- The protocol is at revision 2 (clarification only).
