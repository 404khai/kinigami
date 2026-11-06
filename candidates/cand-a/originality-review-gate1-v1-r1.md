# Originality review (Q61, stage gate1): cand-a v1, r1

candidate_id: cand-a
candidate_version: 1
declaration_sha256: 27656337f27029690085a4b5f8c04b8fd6a0c9ddc82cebbdf3a136d83a972f54
stage: gate1
author: Claude Sonnet 5.5 (task-4 agent)
reviewer: reviewer-a-independent
high_cells_f1_f2: 0
exclusion_cube_with_internal_flywheel: not_present
exclusion_needle_or_particle_silhouette: not_present
outcome: pass

Date: 2026-11-05. This review reduces copying risk and does not claim absolute originality.

## 1. Basis and limits

- Compared: `candidates/cand-a/dossier.md` and `declaration.json` (SHA-256 above, computed with `shasum -a 256`) against every entry of `docs/originality/reference-corpus.md` (A1, B1-B4, C1-C23, D1-D4) plus the references found in section 5.
- The reviewer did not author the candidate and did not edit the corpus, dossier or declaration.
- Corpus descriptors were written from abstracts and general knowledge (corpus "Limits"). The reviewer did not read full texts of the primary works. Source links in the matrix are the corpus entry's own citations (accessed 2026-11-04 by the corpus; re-used here without re-reading the primary works). Ratings are therefore judgements on summaries.
- D3 (locomotion) is rated on the **stated intent** of the dossier (section 2 and 6: a spring-returned kick strut pushes a hexagonal prism over a bottom edge). The dossier says this mechanism is not designed. If it is redesigned, section 5 of Q61 requires re-review.
- Search record (2026-11-05): "hexagonal prism rolling robot tumbling edge pivoting modular self-reconfigurable"; "polygonal rolling log robot tumbling locomotion polyhedral body flips over edge small robot"; "modular robot hexagonal prism module rolling lattice self-reconfiguration pivoting". Source: web search (standard mode). Only search-result summaries were read, not the papers.

## 2. Family check

Family A (Q62 s3): single rigid polyhedral body, moves by edge pivoting or rolling, couplers on faces. cand-a is a regular hexagonal prism (R 26 mm, H 28 mm), no internal joint, one coupler on each hexagonal end face. It meets the Family A constraint on the declared geometry. Locomotion is a stated intent only, not designed.

## 3. Exclusions (Q62 s3)

- Cube with internal flywheel: not present. Hexagonal prism, no flywheel or reaction wheel in the component list.
- Needle- or particle-like silhouette: not present. 52 mm across corners, 28 mm long (about 1.9:1 on the long axis), large flat faces. Not a particle swarm unit.

## 4. Similarity matrix

Ratings: N none, L low, M moderate, H high. Order of columns: D1 geometry, D2 coupler, D3 locomotion, D4 assembly, D5 visual. Source for each row is the corpus entry's citation (listed in the corpus under the same id).

| Ref | D1 | D2 | D3 | D4 | D5 | Reasons |
| --- | --- | --- | --- | --- | --- | --- |
| A1 BH6 microbots (F1) | N | N | N | N | N | D1: one 52 mm prism vs thousands of tiny near-identical units. D2: ball-lock pin/bore vs magnetic legs. D3: kick-and-tumble vs crowd surfing over neighbours. D4: end-to-end chain, no arbitrary shapes. D5: pale structural plastic hexagon, not a dark liquid-like swarm. Source: Gizmodo and AWN pages cited in corpus A1 |
| B1 Replicators (F2) | N | N | N | L | N | D4: both chain or join units, generic. Others: different shape, no scuttling, no swarm. Source: corpus B-section Wikipedia page |
| B2 Prey swarm (F2) | N | N | N | N | N | Molecule-scale cloud vs one rigid 52 mm body. Same source |
| B3 Nanites (F2) | N | N | N | N | N | Sub-visible vs a visible rigid body. Same source |
| B4 T-1000 (F2) | N | N | N | N | N | Continuous liquid vs a rigid prism. Same source |
| C1 M-TRAN I | N | L | N | L | N | D1: box halves vs a hexagonal prism. D2: both have face connectors, generic; ball-lock vs permanent magnets. D3: joint-driven vs no joint. D4: chain only generic. D5: blue/red halves vs undetermined. DOI 10.1109/TMECH.2002.806220 |
| C2 M-TRAN II | N | L | N | L | N | As C1. Record in corpus C2 |
| C3 M-TRAN III | N | L | N | L | N | As C1. DOI 10.1177/0278364907085560 |
| C4 ATRON | N | L | N | L | N | Sphere vs prism; hook connectors vs ball-lock; equatorial rotation vs tumbling. DOI 10.1109/IROS.2004.1389702 |
| C5 SMORES-EP | L | L | L | L | N | D1: both a small body with flat faces; D3: wheeled faces vs tumbling; D2 electro-permanent magnets vs ball-lock. DOI 10.1126/scirobotics.aat4983 |
| C6 Roombots | N | L | N | L | N | Peanut spheres vs prism; active connectors vs passive ball-lock. DOI 10.1016/j.robot.2013.08.011 |
| C7 M-Blocks | L | L | **M** | L | L | D1: both a faceted whole body; cube with chamfers vs hexagonal prism, only generic. D2: both put couplers on faces; magnets on faces/edges vs one ball-lock pin/bore per end, differ. D3: **shared in kind**: a rigid whole body pivots over an edge with no external limbs; differs in principle (flywheel brake vs ground kick strut) and in geometry (60 degree steps over a hexagon edge vs 90 degree cube steps). D4: M-Blocks form lattices and pivot around neighbours; cand-a declares only a straight chain, no lattice. D5: plain unadorned body, generic. DOI 10.1109/IROS.2013.6696971 |
| C8 3D M-Blocks | L | L | **M** | L | L | As C7. 3D M-Blocks pivot about several axes; cand-a one axis, one direction. DOI 10.1109/ICRA.2015.7139450 |
| C9 Kilobot | N | N | L | N | N | Legs on the ground vs a prism that tumbles; D3 low because both use ground contact. DOI 10.1109/ICRA.2012.6224638 |
| C10 Claytronics catoms | N | L | L | L | N | Catoms roll around neighbours; cand-a rolls on the table. Adhesion vs mechanical lock. DOI 10.1109/MC.2005.198 |
| C11 Molecubes | L | L | N | L | L | Cube with diagonal axis vs prism; electromagnet vs ball-lock. DOI 10.1038/435163a |
| C12 PolyBot | L | L | N | L | L | Genderless latch plates vs pin/bore ball-lock; chains in common. Record in corpus C12 |
| C13 SuperBot | N | L | N | L | N | Three-segment articulated vs a rigid single body. Record in corpus C13 |
| C14 CKBot | L | L | N | L | L | Cube chains with servo joint; cand-a has no joint. Corpus C14 page |
| C15 Soldercubes | N | N | N | N | N | Soldering connector vs ball-lock. DOI 10.1007/s10514-015-9441-4 |
| C16 FreeBOT | N | N | N | L | N | Sphere/any-point magnet vs prism with two fixed sites. PDF in corpus C16 |
| C17 HyMod | N | L | N | L | N | Spherical joint core vs rigid prism. DOI 10.1007/978-3-319-73008-0_28 |
| C18 Telecube | N | L | N | L | N | Telescoping cube vs fixed prism. Corpus C18 record |
| C19 Crystalline | N | L | L | L | N | Expanding squares vs rigid prism; D3 both use alternating contact, generic. DOI 10.1023/A:1026504804984 |
| C20 PolyPod (unverified) | N | N | N | L | N | Not used as a basis (corpus marks it unverified); chain-only generic overlap noted |
| C21 Swarm-bot | N | L | N | L | N | Gripper/ring vs ball-lock; wheeled body vs tumbler. DOI 10.1023/B:AURO.0000033972.50769.1c |
| C22 Sambot | L | L | N | L | N | Active/passive dock faces vs head pin/tail bore (a genderless-vs-gendered difference); no wheels. DOI 10.1109/TMECH.2010.2085009 |
| C23 Blinky Blocks | L | L | N | L | L | Magnetic stacking cubes, no locomotion. DOI 10.1145/1979742.1979712 |
| D1 Cubelets | L | L | N | L | L | Magnetic snap cubes, passive; no tumbling. modrobotics.com |
| D2 MOSS | L | L | N | L | L | Magnetic kit modules; no self-locomotion of a body. Parallax forum page |
| D3 UBTech Jimu | N | N | N | N | N | Servo kit vs a single-body tumbler. PCWorld page |
| D4 LEGO EV3 | N | N | N | N | N | Brick kit. lego.com page |

Totals: highs 0 (against any reference, F1, F2 or other). Moderates 2 (C7 D3, C8 D3) from the corpus, plus those in section 5.

## 5. References found during review (not in the corpus; not added to it)

Found by web search on 2026-11-05; the reviewer read only search summaries, so ratings are provisional and based on a snippet, not the paper.

| Ref | D1 | D2 | D3 | D4 | D5 | Reasons and source |
| --- | --- | --- | --- | --- | --- | --- |
| R1 HEXEL: hexagonal electrohydraulic modules, Keplinger group, Science Robotics, 18 Sep 2024 ([techbriefs summary](https://www.techbriefs.com/component/content/article/51905-hexagonal-electrohydraulic-modules-shape-shift-into-versatile-robots)) | **M** | L | **M** | L | L | Hexagonal modules with embedded magnets that combine into a rolling robot. D1: both hexagon-based; HEXEL modules are thin hexagonal pieces, cand-a is a solid prism, differs in form. D3: rolling over hexagonal edges is shared in kind, but the drive is electrohydraulic artificial muscle in HEXEL vs a mechanical ground kick strut here. D2: magnets vs ball-lock. This is the closest published hexagonal rolling body found |
| R2 Hexagonal lattice pivot reconfiguration (Demaine et al., Hinged Pixels, SoCG 2021; [paper](https://erikdemaine.org/papers/HingedPixels_SoCG2021/paper.pdf), [dagstuhl](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2021.10)) | L | N | L | L | N | Theoretical hexagon modules pivoting about shared vertices. Abstract model, not a hardware body |
| R3 Rolling cylindrical modules on a hexagonal lattice ([HAL hal-02300456](https://hal.archives-ouvertes.fr/hal-02300456)) | L | N | L | L | N | Millimetre-scale rolling cylinders; rolling on a surface of revolution, not edge tumbling |
| R4 Polyhedral rolling robots with linkage or eccentric motor (Front. Mech. Eng. 2020, [Springer](https://link.springer.com/content/pdf/10.1007/s11465-020-0585-3.pdf)) | L | N | L | N | N | Expandable linkage polyhedra roll by changing shape; cand-a is rigid |
| R5 Deformable polyhedron rolling robot, 2014 ([BUAA](https://research.buaa.edu.cn/en/publications/design-and-rolling-analysis-of-a-novel-deformable-polyhedron-robo/)) | L | N | L | N | N | As R4 |

No close hexagonal-log tumbler with a ground kick strut was found. The search did not find rolling-log or edge-pivoting hexagonal prism robots by name, and that is not proof they do not exist. The corpus should be extended by the owner/lead (reviewer did not edit it).

## 6. Differentiation notes (Q61 s3 item 3)

- **C7 D3 and C8 D3 (moderate):** shared: a whole rigid body, no external limbs in the stowed form, changes support face by pivoting over an edge. Different: (a) energy source is a braked internal flywheel in M-Blocks, a spring-returned strut pushing against the table here; (b) the polyhedron is a hexagonal prism with 60 degree steps, not a cube; (c) no magnet is used and no flywheel is declared (exclusion 1 recorded not present); (d) cand-a is not a lattice robot. To keep it different: keep the strut mechanism and do not adopt an internal reaction wheel or a magnet pivot hinge. Note the strut may never be designed; a redesign that moves to an internal momentum wheel would trigger exclusion 1 and re-review.
- **R1 HEXEL D1 and D3 (moderate):** shared: hexagon-based rolling body with edge-over-edge motion. Different: HEXEL is a thin modular hexagonal plate actuated by electrohydraulic muscles with magnet interfaces; cand-a is a solid 28 mm prism with a mechanical kick strut and a ball-lock coupler on the hexagonal faces. To keep it different: do not adopt flat-plate hexagon modules or artificial muscle actuation, and keep the end-face couplers.

## 7. Fail-rule outcome (Q61 s3)

1. Any F1 cell high: no (A1 all none).
2. Two or more highs against the same reference: no (no high cell at all).
3. Each moderate has a differentiation note: yes (section 6).
4. Each single high against non-F1 has a note: no highs.
5. Both exclusions recorded: yes (section 3).

Outcome: pass. Pass means only that no rule was triggered by the references examined. Caveats: ratings rest on corpus summaries and search snippets, and locomotion is only an intent.

## 8. Changes made as a result of the review

None required by this review.

## 9. Required changes

- None to pass this stage. Before final visuals: re-review D5 and D3 when the strut mechanism and visuals exist, and read the HEXEL paper in full to confirm R1's D1 and D3 moderates are not high.
- Dossier section 11 omitted HEXEL and the hexagonal-lattice literature; the lead should consider adding R1-R5 to the corpus.

## 10. References reviewed

Corpus A1, B1-B4, C1-C23, D1-D4 (as listed in the matrix); R1-R5 above. Standing statement: this review reduces copying risk and does not claim absolute originality.
