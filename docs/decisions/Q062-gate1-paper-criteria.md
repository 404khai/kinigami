# Q62 — Gate 1 paper-feasibility criteria and candidate-family distinctness

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-04 |
| Supersedes | — (implements Q38 Gate 1 for ENV-003..005, CPL-005, CPL-009, SEL-001..009) |
| Provenance | **agent decision under explicit owner delegation** ("I delegate all decisions"). The owner may revise it through a superseding record. Each value is evidence-based or labeled **provisional**; unresolved thresholds stay `unresolved` |

## Context

Q38 defines Gate 1 as paper feasibility: the Q12 stowed envelope, packaging and assembly access, an evidence-backed component list, preliminary mass and energy/power budgets, coupler layout, mechanical requirements, and originality. Q38 item 3 requires the criteria to be documented before evaluation, and AGENTS.md requires them to be committed and hashed first. No candidate exists yet. These criteria are written before any candidate declaration, and are not chosen to favor any geometry or mechanism.

## Decision

### 1. Items

Gate 1 has eight hard items. Each evaluates to `pass`, `fail`, or `unresolved`. Exact definitions (declaration schema, geometry computations, tolerances) are in [`docs/validation/gate1-v1-protocol.md`](../validation/gate1-v1-protocol.md), revision 1. The thresholds live in `criteria/gates/gate1-v1.json`.

| Item | Requirement | Pass condition | Unresolved when |
| --- | --- | --- | --- |
| **G1** stowed envelope (ENV-004, Q12) | Stowed enclosing-sphere diameter | The diameter, computed from the declared stowed geometry primitives, is at most **0.060 m** (Q12, exact) | The declaration has no stowed geometry, the computed diameter lies within the numerical band of the limit, or the enclosing-sphere computation does not complete |
| **G2** packaging | Layout | No pairwise interference between the declared component bounding boxes in the stowed layout, every box inside the shell cavity, and an assembly-access statement present | Component boxes, poses, or the shell cavity are undeclared, or an intersection test does not complete |
| **G3** evidence | Sources | Every component cites a source (datasheet or publication URL plus access date), and every mass, dimension, and power value is sourced or derived from a cited source | **Any** uncited component, or any value whose basis is `estimate`. This cannot pass |
| **G4** budgets | Mass, power, energy | The mass budget equals the sum of the components. Peak electrical draw is at most the declared source's rated continuous discharge. **Endurance is reported only**: its threshold stays `unresolved` | Any budget input is missing or the source declares no rated continuous discharge. The endurance value never causes a fail, and never makes G4 pass or fail on its own |
| **G5** tabletop chain | Coupler layout (ENV-001, Q31) | At least **2** coupler sites, and geometry that allows a 3-unit chain with every unit supported on the tabletop | Coupler sites, the chain declaration, or the stable-rest declaration are missing, or a geometry test does not complete |
| **G6** retention and pre-alignment (CPL-005, CPL-009, Q11, Q36) | Mechanism | Retention is passive when unpowered, the pre-alignment means are physically justified (with an independent justification record), and magnetism appears only if declared as a component | Retention or alignment statements are missing, or the justification record is missing |
| **G7** originality review (SEL-005, SEL-006, Q61) | Review | The Q61 gate1 review for this candidate version exists, is complete, is independent, and passes | The review record is missing or incomplete |
| **G8** no copying (SEL-009, Q61) | Specific checks | No cell rated **high** against any F1 or F2 reference, and both family exclusions of §3 recorded as **not present**, in the G7 review record | The review record is missing, or an exclusion check is not recorded |

Notes:

- **G1** is a threshold with an exact source (Q12). The enclosing-sphere computation is conservative by construction (protocol §3), so a pass is sound and the computed diameter may overstate the true minimum slightly for round parts.
- **G3** "unresolved" is not a pass. A candidate is carried forward with uncited components only as an `unresolved` candidate, never as `pass`.
- **G4** endurance: Q31 has not decided the task duration, so no endurance threshold exists. The report states the computed endurance and the average power it assumes. Choosing a threshold needs a task duration from Q31's benchmark specification. Until a superseding record exists, the threshold is `unresolved`, and the item neither passes nor fails on it.
- **G5** uses three units because the interior unit of a chain is the minimal case that has both coupler sites engaged. Q31's benchmark uses five. The three-unit count is **provisional**. It is a minimal necessary condition, not evidence that a five-unit chain is supported.
- **G6** automated checks cover consistency and presence. The physical justification itself is judged by an independent reviewer who records an outcome (protocol §8). Gate 2 and Gate 3 test whether the mechanism works.
- **G7/G8** both read the same Q61 review record. G7 is overall (all fail rules). G8 is the SEL-009 subset, kept separate so a copying finding is never hidden inside a general pass.

### 2. Outcome per candidate

- A candidate version is **`pass`** only if **every** item G1–G8 is `pass`.
- It is **`fail`** if any item is `fail`. (A definite failure dominates `unresolved`. The candidate is rejected and its reasons preserved, SEL-007.)
- Otherwise (no `fail`, at least one `unresolved`) it is **`unresolved`**. `unresolved` is **not** a pass. Unresolved items are listed, and the candidate cannot proceed to Gate 2 until they are resolved by a new, versioned declaration.

The result label for every Gate 1 result is **`exploratory`** (a paper gate, Q38/Q40). A Gate 1 pass never becomes `validated_acceptance`, and does not establish candidate feasibility beyond the paper checks it names.

### 3. Candidate families (distinctness constraints, not designs)

Q38 requires a small set of **structurally distinct** candidates. The lead assigns three architecture families. Each is a constraint on what a candidate in that family must be. None selects a geometry, a coupler, or a mechanism, and none is a design. Each candidate declaration carries a `family` field.

| Family | Constraint |
| --- | --- |
| **A** | A single rigid polyhedral body that moves by whole-body pivoting or rolling over edges, with couplers on faces |
| **B** | An elongated two-segment body with one internal revolute joint, so it is chain-native, with couplers at the segment ends |
| **C** | A near-spherical shell with internal mass-shift or reaction actuation, with couplers on retractable radial sites |

**Exclusions for every family** (checked in the Q61 review and recorded as present or not present, G8):

1. **No cube with an internal flywheel** (the M-Blocks lineage).
2. **No needle- or particle-like silhouette** (the forbidden direction in the charter, design-guidance §4.1).

Further:

- A family is a constraint, so a candidate that violates its family's constraint is not a member of that family. It is outside this assignment and is not scored as a member.
- Q38 forbids quota fillers. A family with no credible candidate stays empty (SEL-001). Two candidates in one family are allowed only if they differ structurally.
- Family membership is determined by the reviewer from the declaration, and recorded in the review.

## Alternatives considered

- **Weighted scoring at Gate 1:** forbidden by Q38 item 2 for gates. Rejected.
- **Declaring a numeric endurance threshold now:** would be an invented number, with no Q31 task duration to ground it. Rejected.
- **Letting `unresolved` pass with a warning:** violates the "unresolved is not a pass" rule. Rejected.

## Rationale

- Every threshold is either exact from a prior decision (G1: Q12) or a structural check with no tuned number. The only numeric values chosen by the agent are numerical tolerances and counts, each labeled provisional in the criteria file (§ Constraints).
- Hard items with no offsetting score follow Q38 item 2.
- Preregistering before any candidate exists means no threshold can favor a candidate.

## Constraints and consequences

- `criteria/gates/gate1-v1.json` is registered and hashed before any candidate declaration exists, together with protocol revision 1.
- **Provisional values** (in the criteria file, each marked `provisional`): the eroded-shape interference tolerance, the numerical band for G1, the minimum chain length of 3, the contact tolerance for tabletop support, the sampling counts for round primitives, the derived-mass tolerance, and the zero minimum clearance between component boxes. All can change only by a superseding record, and any change repeats the affected evaluations (Q38 item 3).
- **Unresolved:** the endurance threshold (no Q31 task duration), the quantitative physical meaning of "physically justified" pre-alignment beyond the independent record (Gate 2/3 evidence is needed), and the five-unit chain claim.
- **Limitations:** a pass checks declared geometry and cited sources on paper. It does not check that URLs resolve, that a cited datasheet says what the declaration claims (a reviewer verifies a sample at the gate record), that parts can physically be assembled beyond a statement, or that the mechanism functions.
- Revising criteria creates a new file (`gate1-v2.json`) plus a register entry, and a new protocol revision. Registered files are never edited in place.

## Revision notes

- None. (Drafted 2026-11-04.)
