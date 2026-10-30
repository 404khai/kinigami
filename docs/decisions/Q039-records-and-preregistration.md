# Q39 — Decision records and preregistration

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-10-30 |
| Supersedes | — |
| Provenance | condensed from owner decision |

## Context

No durable record of Q1–Q38 existed in the workspace, which had already caused a conflicting proposal (Q37). Q38 preregistration requires auditable, dated records.

## Decision

1. **Option B — a decision log plus a requirements specification with stable IDs and traceability.** Separate records for historical decisions, current requirements, and benchmark-to-validation traceability. `AGENTS.md` stays a concise entry point that links to them.
2. **Benchmark and gate criteria are machine-readable and hash-linked to results.** They are stored in structured, version-controlled files read directly by the evaluator. Every result identifies:
   - the criteria version and content hash
   - the candidate version
   - the simulator configuration
   - the run identifier
   - the code revision

   Criteria changes must not silently alter the interpretation of earlier results.
3. **Q1–Q30 wording is unavailable.** Reconstructions are labeled as summaries, never presented as verbatim, and missing wording is never fabricated. Verbatim archival requires the owner to supply the original thread.
4. **Git is initialized when file work is authorized,** before substantive document edits. No automatic commits, pushes, or history rewrites without explicit authorization.

## Record structure

- **Decision log:** ordered, append-only, stable IDs, with rationale, consequences, and supersession links.
- **Requirements specification:** grouped by subsystem, with stable IDs, source decisions, status (`in_force`, `open`, `unresolved`, `superseded`), and acceptance implications.
- **Machine-readable criteria:** consumed by the evaluator, with thresholds, uncertainty treatment, and required evidence.
- **Traceability map:** requirement → benchmark → validation case → result. Unvalidated requirements stay visibly unvalidated.
- **`AGENTS.md`:** the document hierarchy, the no-silent-change rule, and where to look before implementing or evaluating.

## Preregistration and auditability

- Criteria are established before the relevant evaluation begins.
- Results record the criteria content hash and Git commit.
- Revisions preserve the original and revised versions, the reason, the date, the affected evaluations, and the required reruns.
- A local commit aids traceability but is not independent proof of preregistration. Where stronger evidence is needed, publish or externally timestamp the criteria hash before the run.

## Alternatives considered

- **A. Decision log only:** what is currently in force would be hard to determine.
- **C. Everything in AGENTS.md:** unwieldy, with no supersession mechanism.
