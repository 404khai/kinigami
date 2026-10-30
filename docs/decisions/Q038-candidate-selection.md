# Q38 — Candidate selection process

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-10-30 |
| Supersedes | — |
| Provenance | condensed from owner decision |

## Context

Many decisions defer geometry, mechanism, and parameters "until supported by evidence". This decision defines how evidence is produced and how it closes a design choice.

## Decision

1. **Option B — a small set of structurally distinct candidates through staged gates.** Aim for approximately two to four credible candidates, and do not invent weak ones to fill a quota. Reject at each progressively more expensive gate. Parameterized search and optimization wait until the benchmarks are validated and inexpensive.
2. **Hard gates for feasibility and validity, with weighted comparison only among survivors.** A packaging violation, an unsupported physical assumption, an unacceptable mechanical failure, or an invalid result cannot be offset by a high score elsewhere. Survivors are ranked by originality, then mechanical plausibility, clarity of connection logic, scalability, and visual quality. The scoring method and rationale are documented before scoring.
3. **Criteria are documented before evaluation.** Define the required evidence, acceptance conditions, uncertainty treatment, and thresholds in advance, justified by engineering evidence and not chosen to favor a candidate. A change records the original and revised versions, the reason, the date, and the evaluations to repeat. Where evidence is insufficient, mark the criterion unresolved.
4. **Originality is reviewed at the paper gate and again at the final-visual stage.** Before substantial modeling, examine the geometry, coupling concept, assembly behavior, and similarities to existing designs. Repeat once final geometry and visuals exist. Record the references reviewed, the reasoning, and the changes made. The review reduces copying risk. It does not claim absolute originality.

## Staged process

- **Gate 1 — Paper feasibility:** the Q12 stowed envelope, packaging and assembly access, an evidence-backed component list, preliminary mass and energy/power budgets, coupler layout, mechanical requirements, and originality.
- **Gate 2 — Reduced-model feasibility:** locomotion, docking, articulation, retention, and load transfer using production physics and the established benchmark rules.
- **Gate 3 — Detailed validation:** Q35/Q36 reference models, sensitivity and uncertainty analysis, and correct classification of inconclusive results.
- **Selection:** compare only candidates that pass every gate. Publish the evidence, trade-offs, disadvantages, and unresolved risks. Preserve rejected candidates and their failure reasons.

## Constraints

- Benchmark acceptance criteria are separate from ranking scores. Requirements never change to make a preferred candidate win.
- Competing candidates get equivalent evidence requirements and conditions.
- A failed candidate may be revised. The revision is versioned and retested against the same criteria.
- Keep the exploratory/validated distinction (Q37).
- No exhaustive optimization before the models and benchmarks are validated.
- This decision does not favor any geometry or coupler mechanism.

## Alternatives considered

- **A. One reference design, refined iteratively:** early lock-in, and nothing to compare feasibility against.
- **C. Parameterized design-space search:** requires cheap, validated benchmarks, and tends to exploit model gaps.
