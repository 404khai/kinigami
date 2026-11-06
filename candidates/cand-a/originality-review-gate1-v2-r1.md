# Originality review (Q61, stage gate1): cand-a v2, r1

candidate_id: cand-a
candidate_version: 2
declaration_sha256: b7a6e94d20b91df9e1bd27ba3af124ba66237d7fd0585594b87084e79812e54c
stage: gate1
author: Claude Opus 5.5 (engineering lead) with Claude Sonnet 5.5 (cand-a v2 implementation agent)
reviewer: reviewer-a2-originality (Claude Sonnet 5.5, independent session, no authorship in cand-a v2)
high_cells_f1_f2: 0
exclusion_cube_with_internal_flywheel: not_present
exclusion_needle_or_particle_silhouette: not_present
outcome: pass

Date: 2026-11-06. This review reduces copying risk and does not claim absolute originality.

## 0. Summary for the lead

- Result: **pass** under Q61 s3. No cell against F1 or F2 is high. No reference has two high cells. Both exclusions are not present. All differentiation notes are written.
- **High cells (Q61 s3 item 4), both against non-F1/F2 references, both on D2 (coupler concept):**
  1. **Q64-C21 CONRO, D2.** An SMA-wire-released latch that engages annular grooves on protruding pins and holds with no power.
  2. **C12 PolyBot, D2.** The PolyBot G2 interface (read in Yim et al.) has the same principle: an SMA-driven latch plate engaging grooves in pins, passive when engaged. The corpus descriptor for C12 does not mention this. It is a corpus gap that this review fills.
- **Moderate cells (12):** C7 D3, D4; C8 D3, D4; C12 D3, D4; C14 D3; Q64-C21 D3, D4; Q64-C22 D1; Q64-C23 D3; X3 D2 (an expired Toyota SMA latch patent found in this review's search).
- Counts: high 2, moderate 12. Highs against F1/F2: 0.
- The v2 coupler therefore keeps the CONRO/PolyBot **release-and-hold principle**. The pass rests on the rule structure (one high per reference) and on the differences listed in s6, not on the principle being new. The lead and owner should read that as a real residual copying-risk finding on D2, not as clearance.
- Limits are in s1. The biggest: the HEXEL paper (Science Robotics) was blocked (HTTP 403) and was read only through the institute's press release and a trade summary. Its one moderate cell (D1) rests on a geometric fact that the press release states.

## 1. Basis and limits

- Compared: `candidates/cand-a/declaration.json` (v2, SHA-256 above, computed with `shasum -a 256`) and `candidates/cand-a/dossier-v2.md` against every entry of `docs/originality/reference-corpus.md` (A1, B1-B4, C1-C23, D1-D4, and the Q64 additions cited Q64-C21..Q64-C29 per Q65), plus the added references X1-X3 (s3).
- Ratings use the declaration as the authority. Where the dossier, Q66 and the declaration disagree, the declaration is used and the disagreement is reported (s9).
- The reviewer did not author cand-a v2, did not edit any file except this record, and did not use the dossier's s12 author self-check as input to the ratings. The reviewer read s12 only after rating. It lists CONRO's coupler as "M to H" and rates PolyBot/CKBot "L" on the coupler. This review rates PolyBot D2 high, so s12 understates that.
- Fictional entries (A1, B1-B4) have no primary design document. They were rated from the corpus descriptors, as the corpus itself says.
- Corpus entries rated none or low were rated from the corpus descriptors. Q64 requires primary-source reading only for moderate and high cells.
- Sources actually read in this session (dates 2026-11-06):
  - CONRO second-prototype connector page, `https://robots.isi.edu/conro/proto2H.html`. Read in full (a short page).
  - Shen and Will, "Docking in Self-Reconfigurable Robots" (CONRO), `https://robots.isi.edu/prl/shen2001docking-in-self-reconfigurable-robots.pdf`. Full text extracted and read (s2 hardware, docking stages).
  - Yim, Zhang, Roufas, Duff, Eldershaw, "Connecting and disconnecting for chain self-reconfiguration with PolyBot" (ICRA/ASME), `https://modlab.engineering.upenn.edu/publications/asme.pdf`. Full text extracted; read the PolyBot G2 interface and latch section.
  - Romanishin, Gilpin, Claici, Rus, "3D M-Blocks", ICRA 2015, `https://people.csail.mit.edu/sclaici/pdf/romanishin20153d.pdf`. Full text extracted; read the introduction, frame, flywheel, brake and pivot sections. It also states the 2013 M-Blocks pivot-about-neighbour-edge model that C7 describes.
  - Akitaya et al., SoCG 2021 article 56, `https://erikdemaine.org/papers/HingedPixels_SoCG2021/paper.pdf`. Read the abstract and model definitions.
  - Rhombic dodecahedral modular robot, `https://arxiv.org/html/2403.01323v1`. Read (X1).
  - Truss-robot environment exploitation, `https://arxiv.org/html/2508.01829v1`. Read (X2).
  - PenduMorph, `https://arxiv.org/abs/2606.22491`. Abstract read.
  - Toyota SMA latch patent US9140243B2, `https://patents.google.com/patent/US9140243B2/en`. Read (X3).
  - CKBot module page, `https://www.modlabupenn.org/ckbot/`. Read.
  - HEXEL: `https://www.eurekalert.org/news-releases/1058118` (Max Planck Institute for Intelligent Systems press release) and `https://www.techbriefs.com/component/content/article/51905-hexagonal-electrohydraulic-modules-shape-shift-into-versatile-robots` were read. The paper (DOI 10.1126/scirobotics.adl3546 at science.org) and the institute project page (`is.mpg.de`) returned HTTP 403. **The paper itself was not read.**
  - Q64-C24: `https://hal.archives-ouvertes.fr/hal-02300456` returned an access-denied page. Only a search-result abstract was available (Naz, Piranda, Goldstein, Bourgeois, NCA 2016: rolling cylindrical Claytronics modules on a 2D vertical hexagonal lattice). Every cell against it is rated at most low, from that abstract. Any rating above low would need the paper.
  - Q64-C26..C29 were not opened. Cells against them are none or low from the corpus descriptors, which is allowed for such ratings.

## 2. Search record

Date 2026-11-06. Tool: web search (standard mode) plus page fetches. Terms:

1. "Shen Salemi Rubenstein Will Hormone-inspired CONRO docking connector SMA latch Docking in self-reconfigurable robots"
2. "hexagonal electrohydraulic modules Science Robotics 2024 Keplinger self-assembling hexagonal modules"
3. "hexagonal prism rolling robot tumbling edge pivoting modular robot"
4. "3D M-Blocks Romanishin Gilpin Claici Rus pivoting flywheel arxiv magnets cube edges"
5. "PolyBot Yim modular robot connector latch joint module actuated degrees of freedom docking genderless connector plate"
6. "rimless wheel modular robot lobe ring internal drive rolling polygon prism robot self-docking roll-in"
7. "self-reconfigurable robot SMA wire released latch bistable toggle connector unpowered holding shape memory alloy docking"
8. "polygonal prism rolling modular robot tumbling rolls hexagonal log robot lift arm eccentric internal pushes ground tips over edge"
9. "Rus Vona OR Yim OR Kutzer rolling modular robot docking roll into neighbor passive guide channel self-assembly rolling modules dock without actuators" (and three follow-up variants)
10. "Science Robotics 2024 Yoder Rumley Keplinger HEXEL hexagonal module rolling robot modules flat hexagon frame magnets abstract"
11. "tumbling robot hexagonal cylinder internal pendulum OR cam OR arm flips over edge polygonal rolling robot docking magnetic modules ICRA"
12. "hal-02300456 rolling cylindrical modules hexagonal lattice modular robot"

Findings from the search:

- **No hexagonal-prism rolling robot with a ring-mounted lobe was found.** No rimless-wheel-style modular unit was found. No "roll-in" docking in which a unit's own rolling step carries a neighbour's peg along an arc channel was found. Close results were: a hexagon rolling mechanism with a center-arranged actuator (`https://ouci.dntb.gov.ua/works/4LgMVGq7`, HTTP 403, abstract not read, not rated); a polygonal rolling robot based on composite cam regulation (patent CN 117465573 B, title only); a transformable wheel module with lobes (USPTO 12522018, title only); a 24-sided-polygon omni-wheel module (arXiv 2308.03328, summary only). None of these was opened. They are listed so a later reviewer can read them. **Search results are not proof of absence.**
- Added to the matrix: X1 (rhombic dodecahedral cells), X2 (truss robots that tumble), X3 (Toyota SMA bistable latch). The unopened items above are not rated.
- Fictional references considered (F2): Replicators, Prey, Borg/Star Trek nanites, T-1000 (corpus B1-B4). Not extended (no new fictional entries searched).

## 3. Reference list examined, by class

- F1: A1.
- F2: B1, B2, B3, B4.
- P (published): C1-C23 (section C of the corpus; plain C21 Swarm-bot, C22 Sambot, C23 Blinky Blocks), Q64-C21..Q64-C29, X1, X2, X3.
- K (commercial kits): D1-D4.

## 4. Similarity matrix

Key: N none, L low, M moderate, H high. Each cell is `rating - reason`. The **Sources** column applies to all five cells of the row. Dates: corpus citations were accessed by the corpus on 2026-11-04 and re-used for none/low corpus-descriptor ratings; sources this reviewer opened were accessed 2026-11-06 (s1). Reasons for D-columns of a row are given in the order D1 (silhouette), D2 (coupler), D3 (actuation and locomotion), D4 (assembly), D5 (visual identity).

v2 summary used for the comparison: a regular hexagonal prism (circumradius 25.5 mm, 28 mm long, about 36.6 g) that rolls over its long edges about the axis. A girdle ring with one lobe (reach 28.5 mm) driven by a 6 mm gearmotor presses on the table and tips the body past the leading edge. Axial couplers on the end faces: a fixed 304 hex peg with an annular groove on the head, and on the tail a receiver with arc roll-in channels, a yaw turntable (actuated, plus or minus 12 degrees) and a dead-centre toggle keeper whose tongue enters the peg groove, opened by a Flexinol SMA pulse. Chain is end to end. Pale PA12 body with exposed steel peg. No magnets.

### 4.1 Forbidden and fictional (A1, B1-B4)

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| A1 BH6 microbots (F1) | N - one 51 mm prism vs thousands of near-identical tiny units | N - mechanical peg and toggle vs magnetic legs | N - ring-lobe tumbling vs units crowd-surfing over each other | N - end-to-end chain, no arbitrary shapes | N - pale structural plastic, not a dark liquid-like swarm | Gizmodo and AWN pages cited in corpus A1 (https://gizmodo.com/how-disney-will-make-you-cry-again-with-big-hero-6-1630115219 ; https://awn.com/animationworld/don-hall-and-chris-williams-talk-disneys-big-hero-6), accessed 2026-11-04 |
| B1 Replicators (F2) | N - hex prism vs insect-like blocks | N - peg/toggle vs unspecified interlock | N - tumbling vs scuttling | L - both join identical units, generic | N - pale hexagon vs grey-silver bugs | https://en.wikipedia.org/wiki/Nanotechnology_in_fiction, accessed 2026-11-04 |
| B2 Prey swarm (F2) | N - one 51 mm body vs a particle cloud | N - mechanical vs none | N - rolling vs flying cloud | N - fixed chain vs shape-forming cloud | N - solid plastic vs shimmering cloud | same Wikipedia page, accessed 2026-11-04 |
| B3 Borg/Star Trek nanites (F2) | N - visible 51 mm vs sub-visible | N - mechanical vs none | N - rolling vs bloodstream-borne | N - chain vs tissue remodelling | N - visible hardware vs sub-visible | same Wikipedia page, accessed 2026-11-04 |
| B4 T-1000 (F2) | N - rigid prism vs liquid metal | N - peg/toggle vs continuous material | N - rolling vs flowing | N - chain vs mimicry | N - matte plastic vs chrome liquid | same Wikipedia page, accessed 2026-11-04 |

### 4.2 Published robots, section C (C1-C23)

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| C1 M-TRAN I | L - box-like body, both about 50-65 mm | L - generic: a magnet face vs a mechanical peg; both just attach | L - chain gaits vs rolling; both locomote | L - chain/lattice vs end-to-end chain, generic | N - blue/red cuboid halves vs pale hex prism | DOI 10.1109/TMECH.2002.806220 |
| C2 M-TRAN II | L - as C1 | L - as C1 | L - as C1 | L - as C1 | N | https://bvbvf1.bib-bvb.de/vufind/PrimoRecord/cdi_proquest_miscellaneous_28107551 |
| C3 M-TRAN III | L - as C1 | L - as C1 | L - as C1 | L - as C1 | N | DOI 10.1177/0278364907085560 |
| C4 ATRON | L - compact body vs sphere halves | L - hook connectors vs a hook-like keeper in a groove; generic mechanical latching | L - module motion needs neighbours vs self-rolling | L - lattice vs chain | N - split spheres | DOI 10.1109/IROS.2004.1389702 |
| C5 SMORES-EP | L - compact body | L - electropermanent magnets vs a mechanical peg | L - wheel faces vs rolling about edges | L - lattice-chain vs chain | N - circular wheel faces | DOI 10.1126/scirobotics.aat4983 |
| C6 Roombots | N - paired spheres | L - active mechanical connectors vs peg/toggle, generic | L - active joints vs rolling | L - 3D self-reconfiguration vs chain | N | DOI 10.1016/j.robot.2013.08.011 |
| C7 M-Blocks | L - polyhedral rigid frame, but a cube vs a hex prism | L - permanent magnets on edges/faces vs a mechanical peg | **M** - both are rigid bodies that move by pivoting over an edge on a table (read: in each step the module pivots about one of its edges). The principle differs: a braked flywheel gives an impulse vs a quasi-static lobe lift | **M** - an M-Block pivots about the shared edge of a neighbour into a docked pose; a v2 unit docks by one roll step about its own bottom edge. Lattice vs chain differ | L - plain cube with no visible actuators vs a visible peg and lobe | DOI 10.1109/IROS.2013.6696971 ; 3D M-Blocks text read: https://people.csail.mit.edu/sclaici/pdf/romanishin20153d.pdf , 2026-11-06 |
| C8 3D M-Blocks | L - as C7 | L - as C7 | **M** - flywheel torque converted to pivoting about several axes; same kind as C7 | **M** - temporary magnetic hinges let modules pivot relative to each other; same note as C7 | L - as C7 | DOI 10.1109/ICRA.2015.7139450 ; text read 2026-11-06 |
| C9 Kilobot | N - flat PCB on legs | N - no docking | N - vibration slip-stick | N - no assembly | N | DOI 10.1109/ICRA.2012.6224638 |
| C10 Claytronics catoms | L - small polyhedron vs sphere or cylinder | L - planned adhesion vs peg | L - rolling around neighbours vs rolling on a table | L - ensembles, generic | N | DOI 10.1109/MC.2005.198 |
| C11 Molecubes | L - prismatic block | L - electromagnet faces vs peg | N - one rotation axis | L - towers vs chain | N | DOI 10.1038/435163a |
| C12 PolyBot | L - small prism-like module about 50 mm | **H** - the PolyBot G2 interface (read) has a latch plate of stainless sheet whose legs go around grooves in protruding pins; two SMA wires rotate it to release; a spring returns it; the latch is passive when engaged and active only for release. v2 shares the principle: an SMA pulse withdraws a stainless latch element from a groove in a protruding peg; holding needs no power | **M** - one actuated rotational joint per module in a chain (PolyBot) vs an actuated yaw joint per coupler in a chain (v2). The joint form and the locomotion differ | **M** - chain-based reconfiguration with SMA-released latches vs v2's end-to-end chain with SMA-released keeper | L - PolyBot modules are bare cubes/prisms in chains; v2 has a hex body | Yim et al., read: https://modlab.engineering.upenn.edu/publications/asme.pdf , 2026-11-06 ; corpus C12 (researchr record, ICRA 2000) |
| C13 SuperBot | L - boxy segments | L - docking faces | L - three joints per module | L - chain/lattice | N | https://robots.isi.edu/prl/b2hd-salemi2006superbot.html |
| C14 CKBot | L - roughly cubic 60 mm module vs hex prism 51 mm | L - read: screws and a 20-pin header; no latch | **M** - read: one rotational degree of freedom per module and modules chain through it; v2 has one actuated yaw joint per unit in a chain. Joint axis, servo form and the role of the joint differ | L - clusters assembled manually | N - laser-cut cubes | https://www.modlabupenn.org/ckbot/ , read 2026-11-06 |
| C15 Soldercubes | L - cube | L - solder joint vs peg | L - joint-driven | L | N | DOI 10.1007/s10514-015-9441-4 |
| C16 FreeBOT | N - sphere | L - internal magnet vs peg | L - motors in a sphere | L - freeform vs chain | N | https://freeformrobotics.org/wp-content/uploads/2022/02/IROS20_0857_FI.pdf |
| C17 HyMod | L - lattice envelope | L - HiGen genderless connector vs peg/receiver | L - 3-DOF joints | L | N | DOI 10.1007/978-3-319-73008-0_28 |
| C18 Telecube | L - prismatic cell | L - switching magnets | N - prismatic extension | L | N | https://researchr.org/publication/SuhHY02 |
| C19 Crystalline | L - polygonal units | L - latches between units | L - expansion/contraction | L | N | DOI 10.1023/A:1026504804984 |
| C20 PolyPod | L - segment-node linkage | L - not verified | L - gait locomotion | L - chain | N | https://www.mit.edu/people/manoli/polypod/polypod.html (low confidence) |
| C21 Swarm-bot | N - round wheeled body | L - gripper and ring vs peg | N - wheels and tracks | L - connected swarm | N | DOI 10.1023/B:AURO.0000033972.50769.1c |
| C22 Sambot | L - cuboid body | L - one active, several passive docking faces; v2 has one peg end and one receiver end | N - wheels/tracks | L - self-assembly | N | DOI 10.1109/TMECH.2010.2085009 |
| C23 Blinky Blocks | N - glowing cubes | L - magnetic stacking | N - no locomotion | L | N | DOI 10.1145/1979742.1979712 |

### 4.3 Commercial kits (D1-D4)

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| D1 Cubelets | L - small blocks | L - magnetic faces | N - fixed function blocks | L - hand-built | N - bright coloured cubes | https://modrobotics.com/about-us , 2026-11-04 |
| D2 MOSS | L - simple solids | L - magnets | L - motor joints | L | N | https://forums.parallax.com/discussion/151259/moss-brand-new-robot-construction-system-from-modular-robotics |
| D3 UBTech Jimu | N | L - interlocking parts | L - servos | L | N | https://www.pcworld.com/article/419049/ubtech-looks-to-up-its-toy-robot-game-with-the-jimu.html |
| D4 LEGO Mindstorms EV3 | N | L - pins and studs | L - motors | L | N | https://www.lego.com/en-us/product/31313 |

### 4.4 Additions from Q64 (cited Q64-C21..Q64-C29)

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| Q64-C21 CONRO | L - elongated box segments of 10 cm vs a 51 mm hex prism | **H** - read: the latch engages grooves on pins; an SMA wire pulls the latch back to free the pins; a spring returns it; no energy is used in the default state. v2: a keeper tongue engages the groove of a protruding peg; an SMA pulse withdraws it; holding needs no power. Same release actuator, same groove-on-pin geometric lock, same unpowered hold | **M** - read: two actuated DOF (pitch, yaw) per module, with modules chained to locomote. v2 has an actuated yaw per coupler in a chain, but its locomotion is rolling, and the joint works only on certain faces | **M** - read: chain topologies with docking by joint movement and IR guidance. v2 chains units end to end with a yaw joint and docks by roll-in | L - bare functional plastic modules; v2's pale hex body is different | https://robots.isi.edu/conro/proto2H.html ; Shen and Will PDF https://robots.isi.edu/prl/shen2001docking-in-self-reconfigurable-robots.pdf , read 2026-11-06 |
| Q64-C22 HEXEL (Keplinger group, Science Robotics 2024) | **M** - a hexagonal exoskeleton of six rigid plates (institute press release) vs a regular hexagonal prism: a hexagon outline in common, but a flat actuated linkage vs a solid prism | L - magnets for mechanical and electrical connection vs a mechanical peg and toggle | L - HASEL muscles change the hexagon's shape; a rolling robot is assembled from modules vs one ring-lobe-driven rolling unit | L - snap-together reconfigurable arrays vs chain | L - glass-fibre plate frames vs PA12 body | https://www.eurekalert.org/news-releases/1058118 ; https://www.techbriefs.com/component/content/article/51905-hexagonal-electrohydraulic-modules-shape-shift-into-versatile-robots , read 2026-11-06. Paper (DOI 10.1126/scirobotics.adl3546) HTTP 403, not read |
| Q64-C23 hexagon pivoting modular robots (Akitaya et al., SoCG 2021) | L - hexagonal modules in a 2D grid (abstract) | N - no coupler, theory | **M** - read: a hexagonal module pivots around a vertex shared with another module. In the v2 cross-section, a roll step about the leading bottom edge is a hexagon rotating about a vertex, so the kinematic move is the same kind. Theory model only, no mechanism, and the pivot is about the ground vertex, not a neighbour | L - reconfiguration in a hex grid vs end-to-end chain | N | https://erikdemaine.org/papers/HingedPixels_SoCG2021/paper.pdf , read 2026-11-06 (DOI 10.4230/LIPIcs.SoCG.2021.56) |
| Q64-C24 rolling cylindrical modules on a hexagonal lattice | L - cylinders vs a hex prism | L - not described in the abstract | L - cylinders roll around each other in a 2D vertical lattice; v2 rolls on a table. Generic rolling | L - 2D lattice self-reconfiguration | N | https://hal.archives-ouvertes.fr/hal-02300456 (abstract through search only; page blocked, 2026-11-06) |
| Q64-C25 PenduMorph | L - sphere vs prism | L - magnetic coupling | L - internal 2-DOF pendulum drives a rolling body; internal mass shift vs a ring lobe that presses the table | L - dual-module coordination | N | https://arxiv.org/abs/2606.22491 , abstract read 2026-11-06 |
| Q64-C26 Rotundus GroundBot | N - sphere | N | L - pendulum drive | N | N | https://orionrobots.co.uk/wiki/rotundus (corpus citation, 2026-11-04) |
| Q64-C27 Sphero / BB-8 | N | N | L - internal drive | N | N | https://newatlas.com/sphero-bb-8-droid/39269/ (corpus citation) |
| Q64-C28 MOPARAS | N | N | N | L - modular parallel spherical robot | N | https://research.polyu.edu.hk/en/publications/moparas-a-modular-parallel-spherical-robot-with-position-adjustab/ (corpus citation) |
| Q64-C29 pendulum spherical robot literature | N | N | L - pendulum-in-sphere drive | N | N | https://ar5iv.labs.arxiv.org/html/2302.08932 (corpus citation) |

### 4.5 References added by this review

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| X1 Rhombic-dodecahedral cells (arXiv 2403.01323) | L - a space-filling parallelohedron, as the hex prism is one | L - passive magnets on 12 faces | L - read: they do not roll or pivot yet; vibration motors only | L - manual structures | N | https://arxiv.org/html/2403.01323v1 , read 2026-11-06 |
| X2 Truss robots VTT and Truss Link (arXiv 2508.01829) | N - truss links | L - rack-and-pinion lock, or spherical magnets | L - read: tumbling by shifting the centre of mass outside the support polygon; generic | L - truss topologies | N | https://arxiv.org/html/2508.01829v1 , read 2026-11-06 |
| X3 Toyota "Shape memory alloy latch with stable on-off position", US9140243B2 (vehicle latches, not a robot) | N | **M** - read: an SMA element toggles a latch between two positions, and both are held mechanically with no power (bistable). v2's keeper is also SMA-flipped and bistable (open stays open). The mechanism differs: crowns and ramps vs a two-link dead-centre toggle | N | N | N | https://patents.google.com/patent/US9140243B2/en , read 2026-11-06 |

## 5. Differentiation notes (Q61 s3 items 3 and 4)

### 5.1 High cells (prominent)

**H1. Q64-C21 CONRO, D2.**
- What is shared (read in the CONRO page and Shen and Will): a latch element that goes into annular grooves on the neighbour's protruding pins, released by an SMA wire, which holds with no electrical power. An informed observer would recognise the release-and-hold principle.
- What differs in v2, from the declaration:
  1. One **hexagonal** peg, not two round pins. The hex peg carries torque about the axis in a half-hex cup; the keeper only carries axial load.
  2. The latch element is a tongue on a **two-link dead-centre toggle**. The load line runs through the link pins, so axial pull cannot back-drive it. CONRO's latch is held closed by a spring and holds by friction/geometry of the latch itself.
  3. The toggle is **bistable**: after an SMA pulse it stays open unpowered, and the arriving peg trips it closed. CONRO's spring re-closes the latch when the SMA cools.
  4. Alignment and closing: a **lateral arc roll-in channel** and the unit's own lift drive; CONRO uses frontal docking with IR guidance and joint motion.
  5. The yaw turntable inside the coupler (CONRO's joints are in the module body).
- What was kept: SMA release, groove-on-pin, unpowered hold. Q66 s4 states this on purpose.
- Assessment: the shared part is **a mechanical principle that is also in PolyBot G2 and generic SMA-latch practice** (Shen and Will cite their own separate connector paper). The differences are real in form and in closing logic. This review still rates D2 high, because the release-and-hold principle is shared in specific form (SMA wire, latch tongue, annular groove on a protruding pin).
- Mitigating: no second high exists against CONRO (D3 and D4 are moderate, s5.2), so rule 2 is not triggered.

**H2. C12 PolyBot, D2.**
- What is shared (read in Yim et al.): the G2 latch plate engages grooves in the opposing module's pins, and two SMA wires rotate the plate to release; a return spring closes it; it needs no energy when engaged.
- What differs: same list as H1. In addition, PolyBot uses four chamfered pins and holes on a face-to-face square plate; v2 uses one hex peg in a half-hex cup with arc entry.
- What was kept: the SMA release and groove-on-pin hold.
- Assessment: as H1. The corpus descriptor for C12 ("a latching system on each face") hides this overlap, so a reviewer using only the corpus would have missed it.

### 5.2 Moderate cells

1. **C7 M-Blocks D3 and C8 3D M-Blocks D3** (read: 3D M-Blocks). Shared in kind: a rigid polyhedral body pivots over an edge on a table. Differs: M-Blocks use an internal braked flywheel (momentum impulse) and no external moving part; v2 has no flywheel, and a ring-mounted lobe presses the table and lifts the body quasi-statically past tipping. Rolling is on a prism's long edges about its axis, with a 60 degree step and a 1.2 g gearmotor. Kept different: no flywheel, no brake, no angular-momentum transfer (and the family exclusion is not present, s7).
2. **C7 and C8 D4.** Shared in kind: a module reaches a docked pose by pivoting over an edge. Differs: M-Blocks pivot about a neighbour's shared edge inside a cubic lattice with magnetic hinges; v2 rolls about its own bottom edge so that a peg moves along an arc into a receiver, in a one-dimensional chain, with a mechanical lock. Kept different: chain only, no lattice, no magnets.
3. **C12 PolyBot D3 and C14 CKBot D3.** Shared in kind: an actuated rotational joint between chain modules. Differs: PolyBot and CKBot are joint-per-module snake or loop robots whose locomotion comes from the joints. v2 locomotes by rolling the whole body, and its yaw joint is a coupler turntable of plus or minus 12 degrees that works only with the chain on a face with a vertical yaw axis; it is not a locomotion actuator. Kept different: no pitch joint and no joint-driven gait.
4. **C12 PolyBot D4.** Shared in kind: chain-style assembly with SMA-released latching. Differs: PolyBot reconfigures a chain by bending it to bring ends to docks (three-phase docking); v2 docks by roll-in, and there is no chain reconfiguration algorithm. Kept different: roll-in with the unit's own rolling drive as the closing force.
5. **Q64-C21 CONRO D3 and D4** (read). D3: shared in kind, an actuated yaw joint between chained units, as in note 3, with CONRO having both pitch and yaw. Differs as in note 3. D4: shared in kind, chain topologies with docking; CONRO docks by IR-guided joint motion in three stages; v2 by roll-in. Kept different: as in note 4.
6. **Q64-C22 HEXEL D1.** Shared in kind: a hexagonal outline. Differs: a flat, shape-changing six-plate linkage with HASEL muscles and magnets vs a solid regular hexagonal prism with an internal ring and a mechanical peg. The hexagon is also a generic space-filling shape. Kept different: no actuation of the hexagon's shape, no magnets.
7. **Q64-C23 D3.** Shared in kind: a hexagon rotates about a vertex. Differs: theory only, with no mechanism; the pivot is about a vertex shared with a neighbour, not the ground contact edge of a self-driven prism. Kept different: v2 has a defined physical driver.
8. **X3 SMA latch patent D2.** Shared in kind: an SMA-flipped bistable latch. Differs: vehicle-door crowns and ramps vs a two-link toggle in a robot coupler. This patent is also prior art for the "bistable SMA latch" idea alone, which narrows what v2 can claim as new in the keeper.

## 6. Family check (Q62 s3, Family A)

- Family A is a single rigid polyhedral body that moves by whole-body pivoting or rolling over edges, with couplers on faces.
- v2: a regular hexagonal prism shell. Its walls are 12 slabs (6 head, 6 tail) joined by two posts and end plates; the girdle slot cuts the walls fully; the lift ring sits in the slot. Moving parts: the ring and its lobe (which reaches beyond the hexagon, 28.5 mm vs 25.5 mm circumradius, only when active), the yaw puck and keeper in the tail receiver, and the gear train. The body itself is rigid. It moves by rolling over its long edges, one 60 degree step at a time. Couplers sit on the two hexagonal end faces. The yaw joint is in the coupler, not between two body segments, so Family B (an elongated two-segment body with one internal revolute joint) does not apply.
- Conclusion: a prism with an internal lift ring and a yaw puck is **still a single rigid polyhedral body that moves by pivoting over edges with couplers on faces**. It is a member of Family A. The note: the lobe is an external-contact actuated member, so v2 is not a "no external moving parts" tumbler like M-Blocks; that is a difference from the M-Blocks lineage, not a family violation.

## 7. Exclusion checks (Q62 s3)

- **Cube with an internal flywheel (the M-Blocks lineage): not present.** The body is a hexagonal prism (not a cube). The component list has no flywheel or reaction wheel (checked in `declaration.json`). The lift ring is a PA12 annulus (about 0.9 g) turning at about 38 rpm, driven geared; it works by lifting the body quasi-statically against the table, not by stored momentum. It would not satisfy a flywheel description.
- **Needle- or particle-like silhouette: not present.** 51.0 mm across corners, 44.2 mm across flats, 28 mm long, with a peg projecting 13 mm beyond the head. The body is a stout prism with large flat faces, about 0.55:1 axis to width. It is a single 36.6 g unit, not a particle-scale one.

## 8. Fail-rule evaluation (Q61 s3)

1. Any cell against F1 (A1) high: **no** (all N).
2. Two or more cells against the same reference high: **no**. Highs: Q64-C21 D2 only; C12 D2 only. High cells against F1 or F2: **0** (this is the `high_cells_f1_f2` count).
3. Every moderate cell has a differentiation note: **yes** (s5.2, 12 cells: C7 D3 D4, C8 D3 D4, C12 D3 D4, C14 D3, Q64-C21 D3 D4, Q64-C22 D1, Q64-C23 D3, X3 D2).
4. Every high cell against a non-F1 reference has a note and is listed in the summary: **yes** (s0, s5.1).
5. Both Q62 exclusions are explicitly checked and recorded: **yes** (s7).
6. Matrix completeness: every corpus entry (A1, B1-B4, C1-C23, D1-D4, Q64-C21..C29) and X1-X3 has five rated cells with a reason and a source: **yes**.

Q61 s3 outcome: **pass**. This means only that no rule was triggered by the references examined. G8 (no high against F1/F2, both exclusions not present) is also satisfied by this record.

## 9. Problems noticed in the inputs

1. **Corpus gap, C12 PolyBot.** The descriptor says only "a latching system on each face". The primary paper shows that PolyBot G2 has an SMA-released latch plate on grooved pins, the same release principle as CONRO. This is the second high cell. The corpus, the author self-check (dossier-v2 s12) and Q66 s4 all missed it.
2. **Corpus C23 title.** The URL in the corpus (`erikdemaine.org/papers/HingedPixels_SoCG2021/`) resolves to the paper "Characterizing Universal Reconfigurability of Modular Pivoting Robots" (SoCG 2021, article 56), not to a paper titled "Hinged Pixels". The entry name and the paper title do not match. The rating above uses the paper that was read.
3. **Description of the keeper differs between the three author documents.** The declaration says the toggle is "biased closed by a Lee LC 014A 01 S spring at 0.2 mm installed compression (0.33 N)". Q66 s4 says the keeper has "no spring holding it closed". Dossier-v2 s12 says the latch is "spring-biased" and that "the SMA only pulls it past centre and the spring completes the motion". The declaration was used here. Under the declaration, a spring biases the toggle closed, which narrows one of the differences Q66 relies on (point 2 of H1 stands, because the load path does not depend on the spring; point 3 stands, because the keeper stays open after release only if the toggle passes centre, which the declaration also states).
4. **Not read:** the HEXEL paper (HTTP 403), the HAL paper for Q64-C24 (access denied), the "hexagon rolling mechanism with a center-arranged actuator" paper (HTTP 403), and the unopened patents named in s2. HEXEL's D1 moderate rests on the institute's press release; it cannot reasonably rise above moderate, because HEXEL is a magnet-coupled, shape-changing planar linkage. Reading the paper is a recommended follow-up. Q64-C24 cells are all low and would need the paper before any could be moderate.
5. **Corpus access date.** Section C and D sources carry 2026-11-04; the Q64 table gives no access dates. This record gives its own dates in s1 and s4.

## 10. Changes made as a result of the review

None. The reviewer edits no candidate file. The changes between v1 and v2 (hex peg and toggle keeper in place of the v1 ball-lock, lift ring in place of the v1 strut reservation, yaw turntable) are the author's, recorded in Q66. This review is the first review of v2.

## 11. Required changes

None are required for the outcome. Recommended, not required:

1. A later corpus revision should add the PolyBot G2 SMA latch to C12 and fix the C23 title.
2. If cand-a is selected for the next stage, the final-visuals review (Q61 s7) should re-rate D2 against CONRO and PolyBot G2 with the final coupler geometry, and the author should decide whether to move away from SMA-released release (for example, a different release principle) so that D2 drops below high. That is a design choice for the Q38 gates, not something this review decides.
3. Read the HEXEL paper and the Q64-C24 paper in a r2 review if either cell is relied on.

## 12. Standing statement

This review reduces copying risk and does not claim absolute originality.
