# Originality review (Q61, stage gate1): cand-b v1, r1

candidate_id: cand-b
candidate_version: 1
declaration_sha256: d973b4cc57b45381b0be9b7e35bdf4508aa3ef449e5fb613c648834454f69a5a
stage: gate1
author: Claude Sonnet 5.5 (agent task-5)
reviewer: reviewer-b-independent
high_cells_f1_f2: 0
exclusion_cube_with_internal_flywheel: not_present
exclusion_needle_or_particle_silhouette: not_present
outcome: unresolved

Date: 2026-11-05. Reviewer is a different agent session from the declaration author and has no authorship in the candidate files. This review reduces copying risk and does not claim absolute originality.

## 1. Outcome in brief

Outcome is **unresolved**, not pass. No fail rule fired (no F1 high; no reference with two highs). Reasons it is not a pass:

1. **CONRO is missing from the corpus and from the author's self-check**, and is the closest published match for the coupler. Checked against its primary source (section 4), D2 against CONRO is rated **high** (one high, non-F1: allowed, but needs a prominent differentiation note, given in section 5). The author's differentiation table never addressed it, so the author has not yet stated what keeps the coupler different.
2. Only CONRO was read at source. All other cells rest on corpus descriptors, which the corpus itself says must be checked against primary sources for close calls (M-TRAN, PolyBot, CKBot, SuperBot, Sambot cells are close calls). Those cells are rated and sourced, but the source-check is incomplete (section 7).
3. D5 cannot be rated meaningfully: no visual design exists. Cells are rated "none (nothing declared)" and Q61 section 7 requires the separate final-visuals review.

Family check (Q62 section 3): declaration is an elongated two-segment body, one revolute joint, couplers at segment ends. Member of family B, with the caveat that elongation is modest (about 1.8:1 deployed; dossier R9). Exclusions: cube with internal flywheel **not present** (no cube, no flywheel, only a servo); needle- or particle-like silhouette **not present** (stowed 39 x 32 x 30 mm, deployed 57 x 32 x 30 mm).

## 2. Matrix

Ratings: none / low / moderate / high. Source for every M-TRAN, PolyBot, CKBot, SuperBot, Sambot, ATRON, SMORES, M-Blocks cell is the corpus entry cited (descriptor level, accessed 2026-11-04 in corpus) unless a primary source is named. CONRO cells use the primary pages in section 4 (accessed 2026-11-05).

### F1 / F2

| Ref | D1 | D2 | D3 | D4 | D5 |
| --- | --- | --- | --- | --- | --- |
| A1 Big Hero 6 microbots | none: dark particle masses vs one 57 mm two-box unit | none: magnetic legs vs mechanical hook, no magnets | none: crowd-surfing vs single servo hinge | low: units chain/assemble, generic | none: nothing declared |
| B1 Replicators | none: bug blocks | none: no mechanism shown | none: scuttling | low: generic assembly | none: nothing declared |
| B2 Prey | none: cloud | none | none | none | none |
| B3 Nanites | none | none | none | none | none |
| B4 T-1000 | none | none | none | none | none |

Source for all F rows: corpus A1 and B1-B4 (secondary sources listed there, accessed 2026-11-04). Fictional entries have no engineering source; primary works not re-checked.

### Published robots (relevant entries)

| Ref | D1 silhouette | D2 coupler | D3 actuation | D4 assembly | D5 visual |
| --- | --- | --- | --- | --- | --- |
| C1-C3 M-TRAN | moderate | low | moderate | moderate | none |
| C12 PolyBot | low | low | moderate | moderate | none |
| C14 CKBot | low | low | moderate | moderate | none |
| C13 SuperBot | low | low | low | moderate | none |
| C22 Sambot | low | low | low | low | none |
| **CONRO (not in corpus)** | low | **high** | moderate | moderate | none |
| C4 ATRON | none | low | low | low | none |
| C5 SMORES-EP | none | none | low | low | none |
| C6 Roombots | none | low | low | low | none |
| C7, C8 M-Blocks | none | none | none | none | none |
| C20 PolyPod | low | not verified | low | moderate | none |
| C17 HyMod, C11 Molecubes, C15 Soldercubes, C16 FreeBOT, C18 Telecube, C19 Crystalline, C21 Swarm-bots, C9 Kilobot, C10 catoms, C23 Blinky | none or low each | none or low | none or low | none or low | none |
| D1-D4 kits | none | none or low | none or low | none or low | none |

Reasons (cell by cell for the close references):

- **M-TRAN D1 moderate:** two block halves joined by a link (C1); cand-b is two boxes joined at a pivot. Shared in kind; cand-b boxes are offset by one segment width (Z-link), M-TRAN halves are cuboid plus semicylinder.
- **M-TRAN D2 low:** M-TRAN uses permanent magnets (C1, C2); cand-b has no magnets. Shared only the generic "face attachment".
- **M-TRAN D3 moderate:** rotary joints between two halves (C1); cand-b has one joint, M-TRAN two per module.
- **M-TRAN D4 moderate:** chain use and zig-zag chains (C1 visual) vs a chain that zigzags by alternating 180 degree roll (dossier section 1). Similar in kind. M-TRAN is also hybrid lattice; cand-b is chain only.
- **PolyBot D1 low, D2 low:** cube-like module with genderless plates and latching (C12); cand-b is elongated and gendered (plug/socket). **D3 moderate:** one rotational DOF per module (C12). **D4 moderate:** chain-style snake use.
- **CKBot D1 low, D2 low, D3 moderate, D4 moderate:** about 6 cm cube, hobby-servo single joint, chains (C14). Servo-driven single revolute joint is a shared distinctive feature in kind; the pivot offset and non-cubic shape differ. Corpus C14 has no module paper; descriptor is from the project page only.
- **SuperBot D4 moderate:** hybrid chain/lattice, boxy articulated (C13); cand-b chain only. D3 low: three DOF vs one.
- **Sambot all low:** hinged docking arm and mobile body (C22); cand-b has no arm, no wheels.
- **ATRON D2 low:** hook-based connectors (C4) shared generically; ATRON is spherical, lattice.

## 3. High cells (prominent)

Exactly one high cell: **CONRO D2 (coupler concept)**, non-F1, non-F2. It is not a fail under section 3 rules 1 and 2. It needs a differentiation note (rule 4) and is flagged here for the owner.

## 4. CONRO check against primary source

Sources (accessed 2026-11-05):
- [Second CONRO prototype hardware, USC/ISI](https://robots.isi.edu/conro/proto2H.html): module has a passive connector (1 inch cube with pins on three faces, with an infrared pair), motor housing, and an active connector with receptacles. Two rotational axes (pitch and yaw). "A SMA wire is contracted pulling the latch back and freeing the pins. When deactivated, a spring brings the latch back to the close position." About 10 cm, 100 g.
- [Shen et al., Docking in self-reconfigurable robots (2001)](https://robots.isi.edu/prl/shen2001docking-in-self-reconfigurable-robots.pdf) and [Khoshnevis et al., Reconnectable joints (2001)](https://robots.isi.edu/prl/b2hd-khoshnevis2001reconnectable-joints-for-self-reconfigurable-robots.html): PDF was binary and could not be read by my tool. A search result for these works described the same SMA-wire, latch and pin scheme and states the connector draws no electric power in its default state. I did not read the PDF text, so details beyond the hardware page are unverified.

Comparison with cand-b's coupler:

| Aspect | CONRO | cand-b |
| --- | --- | --- |
| Gender | gendered: passive pins vs active receptacles | gendered: plug vs socket |
| Release | SMA wire contracts, pulls latch back from pins | SMA wire contracts, pulls hook ring out of groove against spring |
| Hold | spring-closed latch, no power to hold | spring-preloaded hooks, no power to hold |
| Retained feature | cylindrical pins | circular groove on a plug neck |
| Alignment | pins into receptacles, IR pair for sensing | conical funnel, taper, two keying flats, 4 pogo pins |
| Joints per module | 2 (pitch, yaw) | 1 (mid-body pivot) |

The principle (SMA-released, spring-closed, unpowered-hold latch on a gendered connector) is the same, and that is the distinctive part of the coupler concept. Forms differ (groove-and-hook ring vs latch plate over pins). An informed observer could well call the *release principle* the same design, hence **high** on D2. The reviewer notes this is a judgement near the moderate/high boundary under the provisional anchors.

## 5. Differentiation notes

- **CONRO D2 (high):** Differences: plug neck groove with radial hook ring instead of pin-and-latch-plate; four spring-loaded pogo contacts instead of pins with IR; funnel and flats for alignment; no IR. Kept: SMA-pulled spring-return latch. Required by this review: the author must state, in a new declaration/dossier version, which of these differences is deliberate and why the shared principle is acceptable (SMA latches are also standard hobby practice; the owner may accept it). I did not change any file. No change has been made yet; the original claim in the dossier ("plain spring-hook mechanical latch") omits that release is SMA, which is the shared element.
- **M-TRAN D1:** differs by offset Z-link and plain boxes; kept two-halves-and-joint idea (forced by family B).
- **M-TRAN D3/D4:** one joint vs two; chain-only; kept hinge chain use (forced by family B).
- **PolyBot D3/D4, CKBot D3/D4:** all single-DOF chain modules; family B forces a single-joint chain. Differences: pivot offset from chain line, gendered ends, elongated shape. Kept: servo revolute joint chains. Acceptable as moderate.
- **SuperBot D4:** chain assembly only; kept generic chain behaviour.
- **CONRO D1 low, D3 moderate, D4 moderate:** one joint vs two; chains only.

## 6. Fail-rule outcome

- Rule 1 (F1 high): none.
- Rule 2 (two highs against one reference): none. CONRO has exactly one high (D2). If a later reviewer rates CONRO D4 or D3 high, the candidate fails.
- Rule 3 (moderate differentiation notes): done above.
- Rule 4 (high note): done above.
- Rule 5 (exclusions): recorded.
- No fail rule triggered, but see section 1: outcome is unresolved because of the incomplete source check and the CONRO gap.

## 7. References reviewed

F1: A1. F2: B1-B4. Published: C1-C23 (scanned), with close reading of C1-C3, C12, C13, C14, C22 at descriptor level only (primary papers not read by this reviewer). Kits D1-D4. Plus CONRO (primary hardware page read). Dossier self-check section 9 was read and not relied on.

Search record (2026-11-05, web search, standard): "CONRO self-reconfigurable robot connector SMA ...", "single-joint chain modular robot offset hinge fold plug socket latch self-reconfigurable module survey". Sources: robots.isi.edu, survey records.

## 8. Required changes

1. Add CONRO to the corpus through a decision record (owner/lead). This review does not edit the corpus.
2. Author to produce a v2 or a revised dossier addressing CONRO D2 explicitly, and consider changing the release principle or accepting it with a recorded rationale. Any declaration change changes the hash and needs re-review.
3. Reviewer follow-up (r2): read primary papers for M-TRAN, PolyBot, CKBot, SuperBot and Sambot, and the CONRO docking paper text, and confirm or revise the moderate ratings.
4. Dossier says the corpus self-check ratings are the author's; the corpus omission of CONRO is a corpus gap, not an author fault.
5. G5 note (no change made): the dossier flags a G5 artifact for the folded pose (COM computed in the stowed layout falls outside the support hull). Q63 section 3 records this as a known limitation. It is outside the originality review, noted for completeness.

## 9. References found during review

- CONRO second prototype hardware page, https://robots.isi.edu/conro/proto2H.html (read).
- Shen et al. 2001, Docking in self-reconfigurable robots, https://robots.isi.edu/prl/shen2001docking-in-self-reconfigurable-robots.pdf (listed, not text-read).
- Khoshnevis et al. 2001, Reconnectable joints for self-reconfigurable robots, https://robots.isi.edu/prl/b2hd-khoshnevis2001reconnectable-joints-for-self-reconfigurable-robots.html (listed).
- A US patent record on distributed control of reconfigurable systems (USPTO 6636781) appeared in results; not examined.
- Survey: "Module Design of Self-reconfigurable Modular Robot: A Survey" and "Survey on research and development of reconfigurable modular robots" (titles only; not read).
