# Q61 — Originality-review procedure

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-04 |
| Supersedes | — (resolves SEL-006; implements Q38 item 4) |
| Provenance | **agent decision under explicit owner delegation** ("I delegate all decisions"). The owner may revise it through a superseding record. Each value below is evidence-based or labeled **provisional** |

## Context

Q38 item 4 requires an originality review at the paper gate (Gate 1) and again at final visuals. It must record the references reviewed, the reasoning, and the changes made, and it must not claim absolute originality. It left the procedure undefined (SEL-006, an owner decision gate in R9). SEL-009 forbids copying Big Hero 6 microbots or any other existing fictional or real robot design. Gate 1 criteria (Q62) need an exact, checkable review outcome.

## Decision

### 1. Reference corpus

A review compares the candidate with the corpus below. The corpus is a **minimum, not an exhaustive list**. The reviewer must extend it with a documented search (search terms, sources, and date recorded) and record every addition.

| Category | Class | Minimum content |
| --- | --- | --- |
| F1 | **forbidden fictional design** | Big Hero 6 microbots |
| F2 | other fictional swarm or nanite robots | Examples a reviewer must at least consider: nanite and nanobot swarms and replicator-style or "grey goo" machines in film, television, games, and comics. The reviewer records which were examined |
| P | published modular, self-reconfigurable, and swarm robots | M-TRAN, ATRON, SMORES, Roombots, M-Blocks and 3D M-Blocks, Kilobots, Claytronics catoms, Molecubes, PolyBot, SuperBot, CKBot, Soldercubes, FreeBOT, HyMod, PolyPod, Telecube, Crystal robots, and other systems the search finds |
| K | commercial modular toys and kits | Modular and magnetic-construction robot toys and kits the search finds, recorded by product name |

F1 is the only class whose rules are stricter (§3). F2 is "forbidden" in spirit through SEL-009 ("any other existing fictional or real robot design"), but only F1 is fixed by name in the charter, so the Q61 fail rules treat F2 like any other non-F1 reference. Gate 1 item G8 (Q62) separately fails any **high** cell against an F2 reference, as a SEL-009 check.

### 2. Similarity matrix

For each candidate, the review builds a matrix. Rows are the references examined. Columns are five dimensions:

| Dimension | What is compared |
| --- | --- |
| D1 silhouette and geometry | Outer form, proportions, facet layout, size relationships |
| D2 coupler concept | How units align, latch, carry load, and release; the coupler's visible form |
| D3 actuation and locomotion logic | How a unit or assembly moves, and the principle behind it |
| D4 assembly and reconfiguration behaviour | How units form chains, lattices, and reconfigure |
| D5 visual identity | Colour scheme, surface finish, markings, styling, overall look and presentation |

Each cell is rated **none**, **low**, **moderate**, or **high**, with a written reason and a source link (a URL with its access date, or a bibliographic citation with DOI or equivalent). A cell without a reason and source is **incomplete**, and an incomplete matrix makes the review `unresolved`, not a pass. Rating anchors (**provisional**: they are judgement aids, and the first reviews should test whether they discriminate):

- **none:** no shared feature in this dimension.
- **low:** the only shared features are generic ones forced by the task or by physics (for example, "has a body" or "has some means of attachment").
- **moderate:** a distinctive feature is shared in kind, but the specific form, geometry, or principle differs.
- **high:** a distinctive feature is shared in kind **and** in specific form or principle, so an informed observer would call this the same design in this dimension.

### 3. Fail rules

A candidate version **fails** the review if any of these holds:

1. any cell against an **F1** reference is **high**;
2. two or more cells against **the same reference** (any class) are **high**.

Further requirements, which are not failures but make the review incomplete (so `unresolved`) if missed:

3. every **moderate** cell has a recorded **differentiation note** saying what differs and what was changed or kept to keep it different;
4. every single **high** cell against a non-F1 reference also has a differentiation note and is listed prominently in the review summary;
5. the two family-level exclusions of Q62 §3 (a cube with an internal flywheel; a needle- or particle-like silhouette) are explicitly checked and recorded as present or not present.

Otherwise the candidate version **passes**. Pass means only that no rule above was triggered by the references examined. It is not a claim of absolute originality (Q38).

### 4. Independence

- The reviewer must **not** be the candidate's author. For agent work, a reviewer is a different agent session with no authorship in the candidate's files, or the owner. The review states who the author and reviewer are.
- The same-agent mitigation used elsewhere in this project (controls and unchanged gates) does not substitute for independence here.

### 5. Revision and re-review

- A failed candidate may be revised. The revision is a **new candidate version** (for example `v2`), reviewed from the start with the same procedure. The earlier version's review, failure reasons, and files are preserved (Q38, SEL-007).
- A change to the candidate's geometry, coupler, actuation, assembly behaviour, or visuals after a passing review invalidates that review for the changed version. The new version is re-reviewed.
- A review that finds the corpus search was inadequate may be reopened by adding references. New ratings are added to the review record in a new revision. Earlier ratings are not edited.

### 6. Review record

Each review is a file `candidates/<candidate id>/originality-review-<stage>-v<candidate version>-r<review revision>.md` (`stage` is `gate1` or `final-visuals`) that contains:

- candidate id, candidate version, candidate declaration hash (SHA-256), stage, date;
- author and reviewer (§4);
- the search record (terms, sources, date) and the full list of references examined, by class;
- the 5-column matrix with a rating, reason, and source link in every cell;
- differentiation notes (§3 items 3 and 4);
- the exclusion checks of Q62 §3 (§3 item 5);
- the changes made as a result of the review, and which earlier version they relate to;
- the outcome: `pass`, `fail` (with the triggering rule), or `unresolved` (with what is missing);
- the standing statement: *this review reduces copying risk and does not claim absolute originality*.

### 7. Repetition at final visuals

The same procedure, with the same fail rules, is repeated when final geometry and visuals exist (Q38). D5 (visual identity) carries the most weight at that stage, but all five dimensions are rated again. The final-visuals review is a separate record and is not satisfied by the Gate 1 review. A candidate whose final-visuals review fails does not proceed to selection until revised and re-reviewed.

## Alternatives considered

- **Numeric similarity scores:** invented numbers with no evidence for what they measure. Rejected.
- **A single holistic judgement:** not auditable and cannot be preregistered. Rejected.
- **Author self-review:** conflicts with the independence needed for the review to mean anything. Rejected.

## Rationale

- A five-dimension matrix makes copying risk visible per aspect, so a candidate cannot hide a copied coupler behind a different colour.
- "High" is reserved for similarity an informed observer would recognize. Using it as an automatic fail against the forbidden reference matches SEL-009. Two highs against any one reference is a pattern of imitation even when each aspect alone is arguable.
- Requiring reasons and source links keeps the review reproducible and checkable.

## Constraints and consequences

- Resolves **SEL-006**. SEL-005 and SEL-009 are verified by these records.
- Q62's G7 and G8 consume the review outcome.
- **Provisional:** the rating anchors in §2, the treatment of a single non-F1 "high" as a differentiation-note requirement (§3 item 4), and the minimum corpus list. The owner can revise them by a superseding record. No numeric threshold is introduced.
- The review is a human or independent-agent judgement. It is not machine-computed, and the evaluator reads only the recorded outcome and its completeness.

## Revision notes

- None. (Drafted 2026-11-04.)
