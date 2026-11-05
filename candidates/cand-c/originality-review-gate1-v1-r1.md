# Originality review (Q61, stage gate1): cand-c v1, r1

candidate_id: cand-c
candidate_version: 1
declaration_sha256: 33843995036c6a5eca97d9de7a47686598c5faf9eda20f4dd356ab301bddb517
stage: gate1
author: agent task-6 (cand-c dossier author)
reviewer: reviewer-c-independent
high_cells_f1_f2: 0
exclusion_cube_with_internal_flywheel: not_present
exclusion_needle_or_particle_silhouette: not_present
outcome: unresolved

Review date: 2026-11-05. The reviewer authored no file of cand-c. Standing statement: this review reduces copying risk and does not claim absolute originality.

## Summary

- **Outcome: `unresolved`, not `fail` and not `pass`.** No F1/F2 cell is high and no reference has two cells that are *established* as high, so fail rules 1 and 2 are not triggered on the evidence read. But the corpus gap named by the author is real and the closest references were only read as search summaries and abstracts, not primary sources. Rotundus GroundBot could move D1 to high (see D1 note), which would trigger rule 2. A pass cannot be given on unread geometry.
- **Prominent high cells (rule 4), both non-F1/F2, both D3 (actuation logic):** against **PenduMorph** and against **Rotundus GroundBot**. A hanging-pendulum chassis inside a rolling sphere is the same driving principle as cand-c. Differentiation notes are below.
- **Family exclusions (Q62 §3):** cube with an internal flywheel: not present (the body is a sphere and there is no flywheel). Needle- or particle-like silhouette: not present (a 59 mm sphere, with an aspect ratio of 1).
- `high_cells_f1_f2: 0`. The only fictional references touched are Big Hero 6 microbots (F1), Replicators (F2) and BB-8 (F2, the fictional droid; the toy is class K). None is high in any dimension.
- The candidate's own dossier calls itself weak and expects G5 to fail. That is not an originality matter and is not weighed here.

## Search record (references found during review)

Date 2026-11-05. The corpus file `docs/originality/reference-corpus.md` was not edited. Searches (WebSearch, standard mode), terms and the references they surfaced:

1. "PenduMorph pendulum-driven spherical robot" gave N1, and also generic pendulum-driven spherical robot literature (N6).
2. "Sphero BB-8 toy internal drive self-propelled spherical robot magnetic head" gave N2.
3. "Rotundus GroundBot spherical robot pendulum drive" gave N3.
4. "modular spherical robot self-assembling spherical shell modules docking pendulum rolling" gave N4 and N5.

Only search-result summaries and titles were read. No full text was opened. Every rating below that rests on them is flagged as such, and any close call must be checked against the primary source.

| ID | Reference | Class | Source (accessed 2026-11-05) |
| --- | --- | --- | --- |
| N1 | PenduMorph: pendulum-actuated rolling reconfigurable spherical robot with magnetic coupling; fully enclosed sphere, 2-DOF internal pendulum, magnetic docking | P (new) | https://arxiv.org/pdf/2606.22491 |
| N2 | Sphero / BB-8 toy: ball with an internal wheeled drive running on the inner shell surface, with a counterweight; BB-8's head is held on top by magnets | K (new) | https://newatlas.com/sphero-bb-8-droid/39269/ ; https://www.machinedesign.com/automation-iiot/embedded/article/21834396/whats-inside-two-different-star-wars-bb-8-droids ; https://hackaday.com/2015/04/19/bb-8-is-real-but-how-did-they-do-it |
| N3 | Rotundus GroundBot: sealed spherical security robot, pendulum drive, no external moving parts | P/K (new) | https://orionrobots.co.uk/wiki/rotundus ; https://uspto.report/patent/grant/8099189 ; https://patents.justia.com/assignee/rotundus-ab |
| N4 | SnailBot: spherical ferromagnetic shell, six-wheel rocker chassis with embedded magnets, continuous 3D dock | P (new) | https://multirobotsystems.org/?q=node/448 ; https://www.roboticgizmos.com/snailbot/amp/ |
| N5 | MOPARAS: modular parallel spherical robot with adjustable connector positions | P (new) | https://research.polyu.edu.hk/en/publications/moparas-a-modular-parallel-spherical-robot-with-position-adjustab/ |
| N6 | Pendulum-driven spherical robot literature (dynamics and MPC control, momentum-wheel variants) | P (new, generic) | https://ar5iv.labs.arxiv.org/html/2302.08932 ; https://www.scientific.net/AMM.315.192 ; https://pure.bit.edu.cn/en/publications/design-and-control-of-a-spherical-robot-using-pendulum-and-moment |

Not searched, and so still a gap: self-propelled spherical drones with a shell-only cage (flying and amphibious), spherical tensegrity rollers, and spherical modular shells outside the terms above.

## Matrix (5 dimensions)

Corpus entries below are cited from `docs/originality/reference-corpus.md` (access date 2026-11-04) by name; the author's IDs in dossier section 10 are used where given. Where the corpus descriptor is the only source, that is the stated basis. The reviewer did not re-open primary sources for the corpus entries.

| Reference | D1 geometry | D2 coupler | D3 motion | D4 assembly | D5 visual |
| --- | --- | --- | --- | --- | --- |
| A1 Big Hero 6 microbots (F1) | none | none | none | low | low |
| B1 Replicators (F2) | none | none | none | low | none |
| BB-8, fictional droid (F2) | low | none | low | none | none |
| C4 ATRON | **moderate** | low | low | low | **moderate** |
| C16 FreeBOT | **moderate** | low | **moderate** | low | low |
| C6 Roombots | low | low | low | low | low |
| C10 Claytronics catoms | low | none | **moderate** | low | low |
| C7/C8 M-Blocks | none | none | low | low | none |
| C17 HyMod | low | low | low | low | low |
| C21 Swarm-bots | low | low | low | low | low |
| N1 PenduMorph | **moderate** | low | **HIGH** | **moderate** | low |
| N2 Sphero / BB-8 toy | **moderate** | low | **moderate** | none | low |
| N3 Rotundus GroundBot | **moderate** (may be high) | none | **HIGH** | none | low |
| N4 SnailBot | **moderate** | low | low | **moderate** | low |
| N5 MOPARAS | low | low | none | low | low |
| N6 pendulum-driven spherical robot literature | **moderate** | none | **HIGH (generic)** | none | none |
| Others (C1-C3, C5, C9, C11-C15, C18-C20, C22, C23, D1-D4) | none to low | none to low | none to low | none to low | none to low |

Reasons and sources per cell (rated cells above low; low and none cells share the reason "only generic features are shared, such as a body or some means of attachment", or "no shared feature", from the corpus descriptor of that entry):

- **C4 ATRON D1 moderate:** both are spheres of two hemispheres split by a plane with connector pockets (corpus descriptor 1 and 5). Specific form differs: the split here is perpendicular to the chain axis, there are two on-axis sites against eight hook connectors. **D5 moderate:** split sphere with connector pockets reads similarly; finish and markings are undefined in cand-c.
- **C16 FreeBOT D1 moderate:** a rolling sphere (corpus descriptor 1). The dossier gives no ferromagnetic shell. **D3 moderate (author rated low; raised):** FreeBOT rolls by internal motors; cand-c rolls by an internal motor and a gravity-loaded chassis. The principle is shared in kind, the specific drive differs. Source: corpus descriptor of FreeBOT.
- **C10 catoms D3 moderate:** rolling spheres (corpus descriptor 3). Here a unit rolls on the table on its own axis, not around neighbours.
- **N1 PenduMorph D3 high:** "pendulum-actuated rolling" in a "fully enclosed" sphere with "onboard control, battery-powered operation" (arXiv abstract, via search summary). An internal pendulum whose gravity reaction rolls the shell is the same principle as cand-c. Cand-c has one degree of freedom (shell turns around a fixed axis relative to the chassis); PenduMorph has two. **D1 moderate:** an enclosed sphere in both; apertures, size and proportions not known. **D2 low:** magnetic coupling against mechanical ball-and-jaw. **D4 moderate:** both are rolling modules that dock to peers; docking here is head to tail on the roll axis.
- **N2 Sphero/BB-8 D1 moderate:** a sealed ball with an internal chassis. **D3 moderate:** internal mass and drive reacts against the shell. Sphero uses wheels pressed on the inner surface, which differs from cand-c's relative shell rotation about pole bearings.
- **N3 Rotundus D3 high:** a pendulum raised by a built-in motor moves the centre of gravity and the sphere rolls (orionrobots wiki, search summary). Same principle as cand-c. **D1 moderate, possibly high:** Rotundus is a sealed sphere with a hanging internal drive. If the primary source (patent US 8,099,189 or the product documentation) shows a shell on pole axles with the pendulum hanging from them, D1 is also high, and fail rule 2 would apply. This was not verified, hence `unresolved`.
- **N4 SnailBot D1 moderate:** a spherical shell body. **D4 moderate:** self-assembling and reconfiguring spherical modules. Differs: ferromagnetic shell and continuous docking, against fixed mechanical sites.
- **N6 generic literature D3 high (generic):** pendulum-driven spherical robots are established prior art (dynamics and control papers). Only the principle is shared. **D1 moderate:** shell form.

Disagreement with the author's self-check (dossier section 10): FreeBOT D3 raised from low to moderate. The author's "no cell is high" no longer holds once the gap is closed: the two D3 cells above are high.

## Differentiation notes

Required for every moderate cell (rule 3) and for each high cell against a non-F1 reference (rule 4). "Kept" means a feature of the declared design; the reviewer cannot confirm an intent that is not in the declaration.

- **C4 ATRON D1/D5:** kept: hemispheres split on a plane perpendicular to the chain axis, both halves turn together, no relative hemisphere motion, two ball-and-socket sites. Not changed by this review. D5 depends on finish, which is not defined at Gate 1, so it must be re-rated at final visuals.
- **C16 FreeBOT D1/D3:** kept: no magnets or ferromagnetic shell, fixed sites, one pendulum drive. D3 principle (internal motion rolls a sphere) is shared in kind and is not avoidable in this family.
- **C10 catoms D3:** kept: table rolling on own axis, no neighbour rolling.
- **N1 PenduMorph D1/D4, and D3 (high):** differences: one actuated degree of freedom, mechanical ball-and-jaw coupling on the roll axis against magnetic docking, chain-native head-to-tail sites. These differences are real but they sit in D2 and D4. In D3 the principle is the same, and the only distinguishing feature is the single-axis, fixed-pole arrangement, which Rotundus may share. The family's whole premise (rolling sphere with a pendulum chassis) is prior art; the candidate's novelty, if any, rests on the coupler and chain behaviour, not its rolling.
- **N2 Sphero/BB-8 D1/D3:** differences: no wheels on the inner shell; shell turned by a gearmotor against pole bearings; couplers on the poles. The candidate has no head or accessory, so BB-8 D5 is none.
- **N3 Rotundus D1/D3 (high):** difference: chain-native couplers on the poles with a retractable head ball and a sprung tail socket. Rotundus has no coupler (D2 none). If D1 turns out high, the required change is geometric (for example a non-spherical or flatted shell), which the dossier declined to make for G5.
- **N4 SnailBot D1/D4:** differences: wheeled rocker chassis and continuous 3D docking, against rolling with a pendulum and two fixed axial sites.
- **N6 D1/D3 (high, generic):** prior art for the principle. Differentiation lies only in the coupler arrangement.

## Fail-rule outcome

- Rule 1 (any F1 cell high): not triggered; all A1 cells are none or low.
- Rule 2 (two highs against one reference): not triggered on the evidence read (each reference has at most one established high). **Not cleared** for N3 Rotundus, where D1 may be high; see above.
- Rule 3 (moderate cells have notes): satisfied above.
- Rule 4 (non-F1 highs have notes and are prominent): satisfied above (N1, N3, N6 D3).
- Rule 5 (both exclusions checked and recorded): satisfied above.
- Completeness: ratings for N1 to N6 rest on search summaries, and D5 for every new reference is unrated from images (reasoned from descriptions only). The matrix is therefore incomplete in the Q61 §2 sense for those cells. This, together with the open Rotundus D1 question, gives **`unresolved`**.

## References reviewed

- F1: Big Hero 6 microbots. F2: Replicators; BB-8 (fictional droid). Other F2 examples (nanite swarms in film, games and comics) were not individually examined by this reviewer; the dossier's wider "none to low" claim for them is accepted only as an author statement.
- P and K from the corpus: ATRON, FreeBOT, Roombots, Claytronics catoms, M-Blocks, HyMod, Swarm-bots; the remainder as a group, by the corpus descriptors only.
- New in this review: N1 to N6 above.

## Changes made as a result

None to the design (this reviewer does not edit the dossier or declaration). The corpus file is unchanged. N1 to N6 should be added to the corpus by a new decision record.

## Required changes before a re-review (r2)

1. Open the primary sources for Rotundus (US 8,099,189) and PenduMorph (arXiv 2606.22491) and rate D1 and D5 from drawings and images. If any reference then shows two high cells, the candidate fails under rule 2 and needs a new version.
2. State in the dossier what in the shell, bearing and pole arrangement is distinct from a single-axis pendulum sphere, or accept that the claim of distinctness rests only on the couplers (D2) and chain behaviour (D4).
3. Re-rate D5 once colour, finish and markings exist; at Gate 1 they are undefined.
4. Add the six new references to the corpus through a decision record, and extend the search to spherical cage drones and tensegrity rollers.
