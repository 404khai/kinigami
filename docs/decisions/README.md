# Decision log

Append-only record of Kinigami's engineering decisions (Q39).

## Rules

- Every decision has a stable ID (`Q<n>`). IDs are never reused or renumbered.
- Records are never rewritten to change their meaning. Typos may be fixed only if the meaning is unchanged, and the fix must be noted in the record's revision notes.
- A decision is changed only by a **new** record that names what it supersedes. The old record stays, with its status set to `superseded` and a pointer to its replacement.
- Each record states its provenance. Distinguish verbatim owner text, condensed summaries of owner text, and information known only by reference.
- Decisions set requirements. The current, consolidated requirements live in [`../requirements/`](../requirements/README.md). If a requirement and its source decision disagree, the decision governs and the requirement is fixed.

## Record template

```markdown
# Q<n> — <title>

| Field | Value |
| --- | --- |
| Status | accepted / superseded |
| Recorded | YYYY-MM-DD |
| Supersedes | — / Q<m> |
| Superseded by | — / Q<k> |
| Provenance | verbatim / condensed from owner decision / reference only |

## Context
## Decision
## Alternatives considered
## Rationale
## Constraints and consequences
## Revision notes
```

## Provenance of the current entries

- **Q1–Q30:** the original question-and-answer text is not available in this repository. [`Q001-Q030-reference-only.md`](Q001-Q030-reference-only.md) records only what later decisions state about them. Verbatim archival requires the owner to supply the original thread.
- **Q31–Q47:** condensed from the owner's accepted decision text in the design conversation, preserving every decision, constraint, and refinement. They are not verbatim transcripts. Decision dates were not captured separately. All were accepted on or before the recording date.

## Index

| ID | Title | Status |
| --- | --- | --- |
| Q1–Q30 | [Known by reference only](Q001-Q030-reference-only.md) | partially recorded |
| Q31 | [Tabletop-supported connected-chain articulation](Q031-tabletop-chain-articulation.md) | accepted |
| Q32 | [Controller information boundary](Q032-controller-information-boundary.md) | accepted |
| Q33 | [Communication channels](Q033-communication-channels.md) | accepted |
| Q34 | [Power transfer through couplers](Q034-power-transfer.md) | accepted |
| Q35 | [Physics formulation and link representation](Q035-physics-formulation.md) | accepted |
| Q36 | [Coupler engagement model](Q036-coupler-engagement.md) | accepted |
| Q37 | [Physical scale and validated envelope](Q037-physical-scale.md) | accepted |
| Q38 | [Candidate selection process](Q038-candidate-selection.md) | accepted |
| Q39 | [Decision records and preregistration](Q039-records-and-preregistration.md) | accepted |
| Q40 | [First implementation milestone](Q040-first-milestone.md) | accepted |
| Q41 | [Production physics backend](Q041-physics-backend.md) | accepted |
| Q42 | [Toolchain, dependencies, and determinism-relevant build settings](Q042-toolchain-dependencies.md) | accepted |
| Q43 | [Simulated time representation and scheduling](Q043-simulated-time.md) | accepted |
| Q44 | [Data formats and hashes](Q044-data-formats.md) | accepted |
| Q45 | [Inspector architecture](Q045-inspector.md) | accepted |
| Q46 | [Slice 1 analytic validation cases and validation-only forces](Q046-fixture-validation-cases.md) | accepted |
| Q47 | [Friction law for the first analytic validation cases](Q047-reference-friction-law.md) | accepted |
| Q48 | [Fixture-validation reference conditions and tolerances](Q048-fixture-validation-reference-conditions.md) (agent decision under owner delegation) | accepted |
| Q49 | [Acceptance of evaluation protocol revision 2](Q049-accept-evaluation-protocol-revision-2.md) (agent decision under owner delegation) | accepted |
| Q50 | [Inspector UI library and first 3D view](Q050-inspector-ui-library.md) | accepted |
