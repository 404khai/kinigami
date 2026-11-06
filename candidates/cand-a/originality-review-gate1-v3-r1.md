# Originality review (Q61, stage gate1): cand-a v3, r1

candidate_id: cand-a
candidate_version: 3
declaration_sha256: 0025a534f9fc2496d8010e97ad69754485b5e671de23a8261ec11237e16fa1bb
stage: gate1
author: Claude Opus 5.5 (engineering lead) with Claude Sonnet 5.5 (cand-a v3 implementation agent)
reviewer: reviewer-a3-originality (Claude Sonnet 5.5, independent session, no authorship in cand-a v3)
high_cells_f1_f2: 0
exclusion_cube_with_internal_flywheel: not_present
exclusion_needle_or_particle_silhouette: not_present
outcome: pass

Date: 2026-11-06. This review reduces copying risk and does not claim absolute originality.

## 0. Summary for the lead

- Result: **pass** under Q61 s3. No cell against F1 or F2 is high. No reference has two high cells. Both exclusions are not present. Every moderate and high cell has a differentiation note. Every moderate or high cell rests on a primary source that this reviewer read (s1), with the exceptions listed under "Not read" in s1; those cells are capped at low and are reported in s9.
- **High cell (Q61 s3 item 4), non-F1/F2 reference, one cell:**
  1. **C6 Roombots, D2 (coupler concept).** The Roombots active connection mechanism (ACM) is a motor-driven crank-and-slider that pushes a latch "into an externally non-reversible singularity position", with no power in the connected state (Spröwitz et al. 2014, read). The v3 keeper is a motor-driven over-centre crank-rocker four-bar whose two stops lie past dead centre, so tongue loads push the crank into its stop and no power or spring is needed. That is the same locking principle. The form differs completely (see s5.1). This is a **new** finding: the v2 review and the author self-check (dossier-v3 s13, which groups Roombots with ATRON and FreeBOT at D2 = L) did not look at the Roombots connector.
- **Release principle moved off the v2 highs.** v2's D2 was high against Q64-C21 CONRO and C12 PolyBot G2 for an SMA-released latch on grooved pins. v3 has no SMA and no spring-closed latch. Rated afresh, D2 against both is now **moderate** (s5.2, M1). That cell is the most borderline rating in this review, and s5.2 says what would make it high.
- **Moderate cells (15):** C4 ATRON D2; C12 PolyBot D2, D3, D4; C13 SuperBot D2; C17 HyMod D2; C14 CKBot D3; Q64-C21 CONRO D2, D3, D4; C7 M-Blocks D3, D4; C8 3D M-Blocks D3, D4; Q64-C23 hexagon pivoting (Akitaya et al.) D3.
- Counts: high 1, moderate 15. Highs against F1/F2: 0 (this is `high_cells_f1_f2`).
- **Locomotion (ring-mounted lift lobe on a hexagonal prism):** no reference was found with a lobe ring on a prism, or with roll-in docking along an arc channel. The closest are M-Blocks / 3D M-Blocks (pivoting over an edge, D3 and D4 moderate) and the Akitaya hexagon pivot model (D3 moderate). Search results are not proof of absence.
- Pass means only that no fail rule was triggered by the references examined. It does not clear the design. The coupler's D2 is a stack of known elements (peg-and-latch class, motor-driven over-centre lock, hook or jaw latches that hold unpowered) and the pass rests on the rule structure and on the form differences in s5, not on the principle being new.

## 1. Basis and limits

- Compared: `candidates/cand-a/declaration.json` (v3). SHA-256 computed with `shasum -a 256 candidates/cand-a/declaration.json`: `0025a534f9fc2496d8010e97ad69754485b5e671de23a8261ec11237e16fa1bb`. Also `candidates/cand-a/dossier-v3.md`. Both against every entry of `docs/originality/reference-corpus.md` (A1, B1-B4, C1-C23, D1-D4, and the Q64 additions cited Q64-C21..Q64-C29 per Q65), plus references Y1-Y5 added by this review's search (s2).
- The declaration is the authority. Its `author` field was copied exactly into the header. The declaration states: no flywheel or reaction wheel, no magnet, no SMA and no spring (checked by text search of the JSON: "flywheel" 0 hits, "reaction wheel" 0, "magnet" 1 hit saying "No magnet and no cone", "sma " 0; the five "spring" hits all say there is none).
- The reviewer did not author cand-a v3, edited no file except this record, and did not use dossier-v3 s13 (the author's self-check) as input. The v2 review was used only as context.
- Fictional entries (A1, B1-B4) have no primary design document and were rated from the corpus descriptors, as the corpus itself says. Cells rated none or low against corpus entries were rated from corpus descriptors, which Q64 allows. Moderate and high cells were rated only after reading the primary source below.
- **Primary sources read in full or in the relevant sections (extracted with `pdftotext`, or read as HTML), all on 2026-11-06:**
  - CONRO: connector page, https://robots.isi.edu/conro/proto2H.html (whole page); Shen and Will (and co-authors), "Docking in Self-Reconfigurable Robots", https://robots.isi.edu/prl/shen2001docking-in-self-reconfigurable-robots.pdf (hardware section 2 and the dedocking section 5). Read: female connector has two holes, a locking/releasing mechanism behind them, default state accepts and locks incoming pins "by a spring motion", release by triggering an SMA actuator, no energy in the default state; the page says "the latch engages groves on the pins", "a SMA wire is contracted pulling the latch back", "a spring brings the latch back to the close position".
  - PolyBot G2: Yim, Zhang, Roufas, Duff, Eldershaw, "Connecting and disconnecting for chain self-reconfiguration with PolyBot", https://modlab.engineering.upenn.edu/publications/asme.pdf (G2 interface, latch, docking sections). Read: latch plate whose four legs go around grooves in the pins; two 150 micron SMA wires release it; a return spring; passive when engaged; chamfered pins; the plate can be pushed aside by pins on insertion without first opening.
  - Roombots: Spröwitz et al., Robotics and Autonomous Systems 62 (2014) 1016-1033, https://documents.epfl.ch/groups/e/ep/epflmedia/www/20140520_Roombots/roombots%20publication.pdf (the ACM section and Fig. 4, 5). Read: hermaphrodite latch-and-groove connector, 65 mm diameter, 57 g, 150:1 geared motor and three spur gears, "A crank and slider mechanism pushes the latch into an externally non-reversible singularity position", "requires no power in the connected state", scooping movement, absence of pins or other extrusions.
  - ATRON: Østergaard et al., "Design of the ATRON lattice-based self-reconfigurable robot", Autonomous Robots 21:165-183 (2006), https://sccn.ucsd.edu/download/robot.pdf (section 4.4). Read: three hooks driven by a DC motor via a lead screw grab two stainless bars on the passive connector, "not backdrivable in the extended arm position, hence no power is required to maintain connection".
  - SINGO (SuperBot): Shen, Kovac, Rubenstein, "SINGO: A Single-End-Operative and Genderless Connector...", https://robots.isi.edu/prl/shen2009SINGO.pdf (design and prototype sections). Read: four jaws on cross rails like a chuck, one micro-motor with a motorized circular gear, the motor stops and the connectors stay engaged without energy.
  - HiGen (HyMod): Parrott, Dodd, Gross, IROS 2014, https://sheffield.ac.uk/media/22956/download (related work and design). Read: four hooks around a central axis, motor-rotated, genderless, hooks lock when power is removed. The same paper's related-work text describes M-TRAN III (extendible hooks), CONRO and ATRON; those statements are second-hand and used only as context.
  - Zhang, Zhang, Gupta, "A Novel Docking System for Modular Self-Reconfigurable Robots", Robotics 6(4):25 (2017), https://mdpi-res.com/d_attachment/robotics/robotics-06-00025/article_deploy/robotics-06-00025.pdf (introduction). Read: the classification "PolyBot and CONRO use peg-and-latch connection systems, a latch falls to lock, released when the SMAs are heated; ICubes key-lock; ATRON active hook".
  - 3D M-Blocks: Romanishin, Gilpin, Claici, Rus, ICRA 2015, https://people.csail.mit.edu/sclaici/pdf/romanishin20153d.pdf (introduction, frame, flywheel, pivot sections). Read: "In each step, the module pivots about one of its edges"; flywheels, motors and brakes inside; modules reconfigure by pivoting about their neighbours. The 2013 M-Blocks paper (C7) was not separately obtained; the 2015 paper describes the 2013 single-axis pivoting model.
  - Akitaya et al., "Characterizing Universal Reconfigurability of Modular Pivoting Robots", SoCG 2021, https://erikdemaine.org/papers/HingedPixels_SoCG2021/paper.pdf (abstract and move definitions). Read: a hexagonal module rotates around a vertex shared with another module; theory only.
  - CKBot: https://www.modlabupenn.org/ckbot/ (whole page). Read: chain-style, one rotational DOF per module (U-bar and L7), manual connection with screws and a 20-pin header.
  - SMORES-EP: Liu et al., https://arxiv.org/pdf/2104.00800 (introduction and system description). Read: EP-Face electro-permanent magnet connectors; four rotational DOF (pan, tilt, left and right wheels).
  - PenduMorph: https://arxiv.org/pdf/2606.22491 (abstract, figure 1). Read: pendulum-actuated rolling sphere, magnetic coupling.
- **Not read (cells against these are capped at low and listed in s9):** HEXEL / Q64-C22 (Science Robotics paper and `is.mpg.de` both HTTP 403; only the search-result abstract and the press release cited by the v2 review); Q64-C24 (HAL page denied, not re-fetched); M-TRAN III / C3 (the IJRR paper was not obtainable; an `eudl.eu` PDF returned an empty file); GENFA (search-result abstract only); the ICRA 2000 PolyBot paper itself, C12 (the G2 paper above was read instead); Q64-C26..C29 and the corpus entries rated none or low.

## 2. Search record

Date 2026-11-06. Tool: web search (standard mode) plus direct downloads of PDFs. Terms:

1. "modular robot connector motor-driven latch hook engages groove on pin docking mechanism self-reconfigurable genderless"
2. "SINGO OR GENFA genderless connector modular robot self-reconfigurable docking mechanism hooks"
3. "over-centre toggle linkage gripper dead-centre bistable connector modular robot docking no power holding"
4. "Roombots active connection mechanism ACM retractable hooks motor-driven slot pin 90 degree symmetry no energy locked"
5. "ATRON modular robot connector hooks claws motor-driven grab bar Jorgensen Østergaard Lund connection mechanism" and a follow-up with "hook claws male connector"
6. "HiGen connector HyMod Parrott Dodd Gross genderless hook motor-driven mechanism"
7. "M-TRAN III Kurokawa connection mechanism hooks ..." and "Kurokawa ... Distributed Self-Reconfiguration of M-TRAN III pdf connection mechanism"
8. "SMORES-EP electropermanent magnet docking key SMORES modular robot hardware design tilt joint pan wheels"
9. "GENFA genderless fail-safe connector modular robots self-assembly ..."
10. "Hexagonal electrohydraulic modules for rapidly reconfigurable high-speed robots Science Robotics 2024 full text"
11. "modular robot hexagonal prism rolling tumbling lobe ring internal drive polygonal cylinder docking 2025 2026"
12. "modular robot rolls into dock: unit rolls about its edge so neighbour's pin slides along arc slot, passive docking by tumbling, prismatic modules"
13. "tumbling robot external lever lobe pushes ground to flip polygonal body over edge; internal arm tumbling module reconfigurable robot rotating ring cam"

Findings:

- **Motor-driven latches that hold unpowered exist in several modular robots:** Roombots ACM (crank-slider into a non-reversible singularity), ATRON (lead-screw hooks, non-backdrivable), SINGO and HiGen (motor-driven jaws or hooks, locked without power), M-TRAN III (extendible hooks, second-hand), GENFA (genderless fail-safe, abstract only). None of those found is a gendered peg with an annular groove entered by a tongue.
- **No toggle-clamp-style over-centre latch on a grooved pin in a modular robot was found other than the Roombots crank-slider.** Over-centre toggles are a general mechanical-clamp principle (search result 3 returned grippers and clamps); this reviewer treats that as a generic mechanism class, not as prior art for the whole coupler.
- **No hexagonal-prism rolling robot with a ring-mounted lobe was found.** No rimless-wheel-style modular unit and no roll-in docking where the unit's own roll carries a neighbour's peg along an arc channel was found. Close results: Truss Link / VTT tumbling (Y5), FlipWalker (Y3), the rhombic dodecahedral cells (Y4). Search results are not proof of absence.
- Fictional references considered (F2): Replicators, Prey, Borg/Star Trek nanites, T-1000 (corpus B1-B4). No new fictional entries were searched.

## 3. Reference list examined, by class

- F1: A1.
- F2: B1, B2, B3, B4.
- P (published): C1-C23 (section C; plain C21 Swarm-bot, C22 Sambot, C23 Blinky Blocks), Q64-C21..Q64-C29, Y1-Y5.
- K (commercial kits): D1-D4.
- Added by this review: Y1 Zhang et al. 2017 docking system (Robotics 6(4):25); Y2 GENFA connector (Fu, Menciassi, Dario, IEEE ROBIO 2011, search abstract only); Y3 FlipWalker (arXiv 2508.19380, search summary only); Y4 rhombic dodecahedral cells (arXiv 2403.01323, search summary and v2 review reading); Y5 Truss Link / VTT tumbling (arXiv 2508.01829, search summary). SINGO and HiGen are part of C13 SuperBot and C17 HyMod respectively and are rated inside those rows.

## 4. Similarity matrix

Key: N none, L low, M moderate, H high. Each cell is `rating - reason`. The **Sources** column applies to all five cells of the row, with the access date stated in it. Reason order is D1 (silhouette), D2 (coupler), D3 (actuation and locomotion), D4 (assembly), D5 (visual identity).

v3 summary used: a regular hexagonal prism (circumradius 25.5 mm, 28 mm long, 51 mm across corners, 41.85 g), pale PA12 shell with exposed 304 steel parts. It rolls over its long edges, one 60 degree step at a time, driven by a PA12/304 lift ring around the girdle carrying one lobe (reach 28.5 mm) that presses on the table, turned by a 6 mm gearmotor through spur gears and a 133-tooth internal gear band. Axial couplers on the two hexagonal end faces. Head: fixed 304 hex peg (4.0 mm across flats) with an annular groove, 6.5 mm engagement. Tail: a receiver with two circular-arc roll-in channels (5.8 mm wide, 7 mm deep), a yaw turntable (worm-driven, plus or minus 12 degrees), a 304 hex-in-hex roll lock (cup insert plus jaw, 4.10 mm across flats) and a keeper tongue driven by a third gearmotor through a crank-rocker four-bar with two hard stops 10 degrees past the dead centres (offsets 0.283 and 0.407 mm). No SMA, no spring, no magnet, no cone. Docking: B rolls one step about its leading bottom edge and the neighbour's peg slides along the arc channel. Chain end to end. BLE only. Passive retention: both keeper states are held by the stops with no power.

### 4.1 Forbidden and fictional (A1, B1-B4)

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| A1 BH6 microbots (F1) | N - one 51 mm prism vs thousands of tiny near-identical units | N - mechanical peg and four-bar keeper vs magnetic legs | N - lobe-ring tumbling vs units crowd-surfing over each other | N - end-to-end chain vs arbitrary shapes on command | N - pale structural plastic and steel vs a dark liquid-like swarm | https://gizmodo.com/how-disney-will-make-you-cry-again-with-big-hero-6-1630115219 ; https://awn.com/animationworld/don-hall-and-chris-williams-talk-disneys-big-hero-6 (corpus A1, accessed 2026-11-04) |
| B1 Replicators (F2) | N - hex prism vs insect-like blocks | N - peg/keeper vs unspecified interlock | N - tumbling vs scuttling | L - both join identical units, generic | N - pale hexagon vs grey-silver bugs | https://en.wikipedia.org/wiki/Nanotechnology_in_fiction (corpus, accessed 2026-11-04) |
| B2 Prey swarm (F2) | N - one 51 mm body vs a particle cloud | N - mechanical vs none | N - rolling vs flying cloud | N - fixed chain vs shape-forming cloud | N - solid plastic vs shimmering cloud | same page |
| B3 Borg / Star Trek nanites (F2) | N - visible 51 mm vs sub-visible | N - mechanical vs none | N - rolling vs bloodstream-borne | N - chain vs tissue remodelling | N - visible hardware vs sub-visible | same page |
| B4 T-1000 (F2) | N - rigid prism vs liquid metal | N - peg/keeper vs continuous material | N - rolling vs flowing | N - chain vs mimicry | N - matte plastic vs chrome liquid | same page |

### 4.2 Published robots, section C (C1-C23)

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| C1 M-TRAN I | L - box-like body, both tens of millimetres | L - permanent-magnet faces vs a mechanical peg; both just attach | L - chain gaits vs rolling; both locomote | L - chain/lattice vs end-to-end chain, generic | N - blue/red cuboid halves vs pale hex prism | DOI 10.1109/TMECH.2002.806220 (corpus) |
| C2 M-TRAN II | L - as C1 | L - as C1 | L - as C1 | L - as C1 | N | https://bvbvf1.bib-bvb.de/vufind/PrimoRecord/cdi_proquest_miscellaneous_28107551 (corpus) |
| C3 M-TRAN III | L - as C1 | L - mechanical extendible hooks per the HiGen paper's related work (second-hand; M-TRAN III paper not obtained), surface-to-surface; v3 is a pin-and-tongue. Capped at low, see s9 | L - as C1 | L - distributed chain/lattice reconfiguration vs chain | N | DOI 10.1177/0278364907085560 ; HiGen paper https://sheffield.ac.uk/media/22956/download read 2026-11-06 |
| C4 ATRON | L - sphere halves vs prism | **M** - read: three hooks driven by a DC motor via a lead screw grab stainless bars; the drive is not back-drivable when extended, so no power holds the connection. Shared in kind: a motor-driven latch that holds unpowered because of the drive geometry. Differs: hooks grabbing bars on a point-to-point lattice connector vs a tongue entering a groove of a peg, and a four-bar stop lock vs a self-locking lead screw | L - single equatorial rotation vs rolling | L - lattice vs chain | N - split spheres | DOI 10.1109/IROS.2004.1389702 ; Østergaard et al. 2006, https://sccn.ucsd.edu/download/robot.pdf , section 4.4 read 2026-11-06 |
| C5 SMORES-EP | L - compact body | L - read: electro-permanent magnet EP-Faces vs a mechanical peg | L - read: pan, tilt and wheel DOF vs rolling about edges | L - lattice-chain, parallel self-assembly vs chain | N - circular wheel faces | https://arxiv.org/pdf/2104.00800 , read 2026-11-06 |
| C6 Roombots | N - paired spheres | **H** - read: a motor and gear train drive a crank and slider that push the latch "into an externally non-reversible singularity position"; no power in the connected state; latch-and-groove interaction. v3: a motor drives a crank-rocker four-bar into stops past dead centre; load on the tongue pushes the crank further into its stop; no power. Same locking principle (motor-driven crank mechanism to a non-reversible position, unpowered hold) and the same interaction word (latch into a groove). Form differs a great deal (see s5.1) | L - 3 rotational DOF vs rolling | L - 3D self-reconfiguration vs chain | N - rounded paired spheres | DOI 10.1016/j.robot.2013.08.011 ; https://documents.epfl.ch/groups/e/ep/epflmedia/www/20140520_Roombots/roombots%20publication.pdf , ACM section read 2026-11-06 |
| C7 M-Blocks | L - polyhedral rigid frame, but a cube vs a hex prism | L - permanent magnets on edges/faces vs a mechanical peg | **M** - rigid body that pivots about one of its edges on a table in each step (read in 3D M-Blocks, which restates the 2013 model). Differs: a braked internal flywheel gives an impulse vs a quasi-static lobe lift | **M** - a block pivots about a neighbour's edge into a docked pose; a v3 unit docks by one roll about its own bottom edge. Lattice with magnetic hinges vs chain with a mechanical lock | L - plain cube, no visible actuators vs visible steel peg and lobe | DOI 10.1109/IROS.2013.6696971 ; https://people.csail.mit.edu/sclaici/pdf/romanishin20153d.pdf , read 2026-11-06 |
| C8 3D M-Blocks | L - as C7 | L - as C7 | **M** - flywheel torque redirected into pivoting about several axes; same kind as C7 | **M** - as C7 (modules reconfigure by pivoting about their neighbours) | L - as C7 | DOI 10.1109/ICRA.2015.7139450 ; text read 2026-11-06 |
| C9 Kilobot | N - flat PCB on legs | N - no docking | N - vibration slip-stick | N - no assembly | N | DOI 10.1109/ICRA.2012.6224638 (corpus) |
| C10 Claytronics catoms | L - small polyhedron vs sphere or cylinder | L - planned adhesion vs peg | L - rolling around neighbours vs rolling on a table | L - ensembles, generic | N | DOI 10.1109/MC.2005.198 (corpus) |
| C11 Molecubes | L - prismatic block | L - electromagnet faces vs peg | N - one diagonal rotation axis | L - towers vs chain | N | DOI 10.1038/435163a (corpus) |
| C12 PolyBot | L - small prism-like module about 50 mm | **M** - read: latch plate whose legs reach around grooves in protruding chamfered pins; two SMA wires release it; a return spring closes it; passive when engaged. Shared in kind: a latch element entering annular grooves of protruding pins, holding unpowered. Differs: SMA release and spring return are not in v3; v3 has one hex peg, a tongue driven by a motor four-bar with two stops, a hex-in-hex roll lock and a roll-in arc entry (s5.2 M1) | **M** - read: one actuated rotational joint per module in a chain vs one actuated yaw joint per coupler in a chain; v3's yaw is not a locomotion actuator | **M** - chain-based reconfiguration by joint-aided docking vs end-to-end chain docked by roll-in | L - bare cubes/prisms in chains vs hex body | https://modlab.engineering.upenn.edu/publications/asme.pdf , read 2026-11-06 ; corpus C12 (ICRA 2000) |
| C13 SuperBot | L - boxy segments | **M** - read (SINGO, the SuperBot connector): four jaws on cross rails like a chuck, one micro-motor, locked without energy once engaged. Shared in kind: a motor-driven latch that holds unpowered. Differs: genderless jaws biting each other vs a gendered peg and tongue; no groove-on-pin; chuck rails vs four-bar | L - three joints per module | L - chain/lattice | N | https://robots.isi.edu/prl/shen2009SINGO.pdf , read 2026-11-06 ; https://robots.isi.edu/prl/b2hd-salemi2006superbot.html (corpus) |
| C14 CKBot | L - roughly 60 mm cube vs 51 mm hex prism | L - read: manual 3M screws and a 20-pin header; no latch | **M** - read: one rotational DOF per module, chain-style, vs an actuated yaw per coupler in a chain; axis, servo form and role differ | L - clusters assembled manually | N - laser-cut cubes | https://www.modlabupenn.org/ckbot/ , read 2026-11-06 |
| C15 Soldercubes | L - cube | L - solder joint vs peg | L - joint-driven | L | N | DOI 10.1007/s10514-015-9441-4 (corpus) |
| C16 FreeBOT | N - sphere | L - internal magnet vs peg | L - motors in a sphere | L - freeform vs chain | N | https://freeformrobotics.org/wp-content/uploads/2022/02/IROS20_0857_FI.pdf (corpus) |
| C17 HyMod | L - lattice envelope with ball joint core | **M** - read (HiGen): four hooks around a central axis rotated by a motor, hook-to-hook genderless latching, hooks lock when power is removed. Shared in kind: a motor-driven latch that holds unpowered. Differs: genderless hook ring vs gendered peg and tongue; no groove-on-pin; no four-bar | L - 3-DOF joints | L - cubic-lattice groups | N | DOI 10.1007/978-3-319-73008-0_28 ; HiGen paper https://sheffield.ac.uk/media/22956/download , read 2026-11-06 |
| C18 Telecube | L - prismatic cell | L - switching magnets | N - prismatic extension | L | N | https://researchr.org/publication/SuhHY02 (corpus) |
| C19 Crystalline | L - polygonal units | L - latches between units | L - expansion/contraction | L | N | DOI 10.1023/A:1026504804984 (corpus) |
| C20 PolyPod | L - segment-node linkage | L - not verified | L - gait locomotion | L - chain | N | https://www.mit.edu/people/manoli/polypod/polypod.html (low confidence) |
| C21 Swarm-bot | N - round wheeled body | L - gripper and ring vs peg | N - wheels and tracks | L - connected swarm | N | DOI 10.1023/B:AURO.0000033972.50769.1c (corpus) |
| C22 Sambot | L - cuboid body | L - one active, several passive docking faces; v3 has one peg end and one receiver end | N - wheels/tracks | L - self-assembly | N | DOI 10.1109/TMECH.2010.2085009 (corpus) |
| C23 Blinky Blocks | N - glowing cubes | L - magnetic stacking | N - no locomotion | L | N | DOI 10.1145/1979742.1979712 (corpus) |

### 4.3 Commercial kits (D1-D4)

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| D1 Cubelets | L - small blocks | L - magnetic faces | N - fixed-function blocks | L - hand-built | N - bright coloured cubes | https://modrobotics.com/about-us (corpus, 2026-11-04) |
| D2 MOSS | L - simple solids | L - magnets | L - motor joints | L | N | https://forums.parallax.com/discussion/151259/moss-brand-new-robot-construction-system-from-modular-robotics |
| D3 UBTech Jimu | N | L - interlocking parts | L - servos | L | N | https://www.pcworld.com/article/419049/ubtech-looks-to-up-its-toy-robot-game-with-the-jimu.html |
| D4 LEGO Mindstorms EV3 | N | L - pins and studs | L - motors | L | N | https://www.lego.com/en-us/product/31313 |

### 4.4 Additions from Q64 (cited Q64-C21..Q64-C29)

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| Q64-C21 CONRO | L - elongated box segments of about 10 cm vs 51 mm hex prism | **M** - read: latch engages grooves on pins; SMA wire pulls the latch back; spring returns it; no energy in the default state. Shared in kind: peg-and-latch with a latch element entering annular grooves of protruding pins and an unpowered hold. Differs: v3 has neither the SMA release nor the spring-closed default (the CONRO distinctive principle); one hexagonal peg, bistable stops, hex roll lock, roll-in entry (s5.2 M1). Borderline | **M** - read: two DOF (pitch, yaw) per module, chained to locomote; v3 has an actuated yaw per coupler in a chain, but locomotes by rolling | **M** - read: chain topologies docked by joint motion with IR guidance; v3 chains end to end docked by roll-in | L - bare functional modules; v3's pale hex body differs | https://robots.isi.edu/conro/proto2H.html ; https://robots.isi.edu/prl/shen2001docking-in-self-reconfigurable-robots.pdf , read 2026-11-06 |
| Q64-C22 HEXEL | L - a hexagonal exoskeleton of six rigid plates (press release) vs a solid prism; paper unread, so capped at low | L - magnets vs mechanical lock | L - HASEL muscles change the hexagon vs ring-lobe rolling | L - snap-together arrays vs chain | L - glass-fibre plate frames vs PA12 | https://www.eurekalert.org/news-releases/1058118 ; DOI 10.1126/scirobotics.adl3546 (HTTP 403, not read, 2026-11-06) |
| Q64-C23 Hexagon pivoting modules (Akitaya et al.) | L - hexagonal modules in a 2D grid | N - theory, no coupler | **M** - read: a hexagonal module rotates around a vertex shared with another module. In the v3 cross-section a roll step about the leading bottom edge is a hexagon turning about a vertex: the same kind of move. Theory only; v3's pivot is about a ground edge | L - reconfiguration in a hex grid vs chain | N | https://erikdemaine.org/papers/HingedPixels_SoCG2021/paper.pdf , read 2026-11-06 (the corpus title "Hinged Pixels" does not match; the paper read is "Characterizing Universal Reconfigurability of Modular Pivoting Robots") |
| Q64-C24 Rolling cylindrical modules on a hexagonal lattice | L - cylinders vs a hex prism | L - not described in the abstract | L - cylinders roll around each other in a 2D vertical lattice; generic rolling. Paper unread, capped at low | L - 2D lattice | N | https://hal.archives-ouvertes.fr/hal-02300456 (not read) |
| Q64-C25 PenduMorph | L - sphere (figure shows a hexagon shell label) vs prism | L - magnetic coupling | L - read: 2-DOF internal pendulum rolls a sphere; internal mass shift vs a ring lobe pressing the table | L - dual-module coordination | N | https://arxiv.org/pdf/2606.22491 , abstract and figure 1 read 2026-11-06 |
| Q64-C26 Rotundus GroundBot | N - sphere | N | L - pendulum drive | N | N | https://orionrobots.co.uk/wiki/rotundus (corpus) |
| Q64-C27 Sphero / BB-8 | N | N | L - internal drive | N | N | https://newatlas.com/sphero-bb-8-droid/39269/ (corpus) |
| Q64-C28 MOPARAS | N | N | N | L - modular parallel spherical robot | N | https://research.polyu.edu.hk/en/publications/moparas-a-modular-parallel-spherical-robot-with-position-adjustab/ (corpus) |
| Q64-C29 Pendulum spherical robot literature | N | N | L - pendulum-in-sphere drive | N | N | https://ar5iv.labs.arxiv.org/html/2302.08932 (corpus) |

### 4.5 References added by this review

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| Y1 Zhang et al. 2017 docking system | N - active and passive module types | L - read the intro: surveys peg-and-latch systems; its own docking is driven by the locomotion actuators, no separate drive. Generic class statement, not a design match | L - locomotion actuators also dock | L - active/passive modules | N | Robotics 6(4):25, https://mdpi-res.com/d_attachment/robotics/robotics-06-00025/article_deploy/robotics-06-00025.pdf , 2026-11-06 |
| Y2 GENFA (Fu, Menciassi, Dario, 2011) | N | L - genderless, fail-safe, motor-driven connector, power-efficient (search abstract only; not read) | N | L - self-assembly and self-healing | N | https://search.isc.ac/Inventory/49/1719136.htm (search result), 2026-11-06 |
| Y3 FlipWalker | N - two segments joined by cables | N | L - motor-driven legs push off the ground to flip; the principle "push the ground to flip over" is generic and loosely related to the lobe; summary only | N | N | https://arxiv.org/html/2508.19380v1 (search summary), 2026-11-06 |
| Y4 Rhombic-dodecahedral cells (arXiv 2403.01323) | L - a space-filling parallelohedron, as the hex prism is one | L - passive magnets on faces | L - vibration motors only | L - manual structures | N | https://arxiv.org/abs/2403.01323 (search result; read in the v2 review), 2026-11-06 |
| Y5 Truss Link / VTT (arXiv 2508.01829) | N - truss links | L - rack-and-pinion lock or magnets | L - tumbling by shifting the centre of mass outside the support polygon; generic | L - truss topologies | N | https://arxiv.org/pdf/2508.01829 (search summary), 2026-11-06 |

## 5. Differentiation notes (Q61 s3 items 3 and 4)

### 5.1 High cell (prominent)

**H1. C6 Roombots, D2.**
- What is shared (read in Spröwitz et al.): a gear-reduced motor in the connector drives a crank and slider that move a latch into a non-reversible singularity, so the connected state needs no power; the latch interacts with a groove; the locked state resists separating loads because the load cannot back-drive the mechanism. v3's keeper: M3 (a 6 mm 136:1 gearmotor) drives a crank-rocker four-bar over dead centre into stops 10 degrees past it; tongue loads push the crank into its stop; both states hold with no power and no spring. An informed observer comparing the locking principle alone would call these the same principle.
- What differs in form and specifics (from the declaration):
  1. Roombots' ACM is a flat, 65 mm, hermaphrodite connector plate with four hooks on a rotating clip that scoops a mating clip; "the absence of pins or other extrusions" is a stated design goal. v3 has a **gendered** protruding hex peg with an annular groove and a receiver; it has pins and a protruding peg.
  2. The thing that locks differs: Roombots hooks slide under hooks of the mating clip; v3 is a 1.0 mm tongue entering a 1.4 mm groove, and the roll is locked separately by a **hex-in-hex** insert and jaw.
  3. Kinematics differ: a crank-slider driving a rotating clip vs a crank-rocker with a rod to a tongue; v3 states explicit over-centre offsets (0.283 and 0.407 mm), two hard stops and a tolerance corner study.
  4. Alignment differs: Roombots relies on a scooping hook movement and a groove shape; v3 has a lateral **arc roll-in channel**, a tongue V-notch, and a docking move that is the whole unit rolling one step.
  5. Context differs: v3 is a rolling prism with a yaw turntable in the coupler; Roombots is a three-DOF module.
- What was kept: the motor-driven crank mechanism to an unpowered, non-reversible position.
- Assessment: **high by the anchor text** ("shared in kind and in principle"), but the shared principle is a toggle or over-centre lock, a general clamp mechanism in common use (search 3), and the visible coupler is a different design. Treat this as a residual copying-risk finding on the *lock principle*, not on the coupler as a whole. Mitigating: no other Roombots cell is above low, so rule 2 is not triggered.

### 5.2 Moderate cells

**M1. Q64-C21 CONRO D2 and C12 PolyBot D2** (read: CONRO page and Shen and Will; Yim et al. G2). Shared in kind: the **peg-and-latch class** (Zhang et al. use that wording for both): a latch element enters annular grooves of protruding pins; chamfered or lead-in pins guide entry; holding needs no power. Differs: (1) the release and hold principle. CONRO and PolyBot are held by a **spring** and released by an **SMA wire**; v3 has no SMA and no spring, and a motor drives an over-centre four-bar with two stops. (2) One hexagonal peg, not two round pins or four pins. (3) A separate 4.10 mm hex-in-hex roll lock, so the groove carries axial load only. (4) A lateral arc roll-in channel instead of frontal docking with IR guidance. (5) Both states are stable (bistable), including **open**; CONRO and PolyBot re-close when the SMA cools. Kept different since v2: the groove-on-pin latch. Changed since v2: SMA, spring, trip, toggle. **Why moderate and not high:** the elements the v2 review called the distinctive shared principle (SMA wire release plus spring-closed default) are gone. What remains is the generic peg-and-latch class. **What would make it high:** a reviewer who treats "latch tongue enters annular groove of a protruding pin, holds unpowered" as the specific form regardless of actuation. That reading is arguable. If taken, CONRO D2 and PolyBot D2 are each a second high alongside D3/D4 moderates, so no reference reaches two highs (CONRO D3, D4 and PolyBot D3, D4 stay moderate), and the outcome is unchanged. The lead should read this cell as borderline.

**M2. C4 ATRON D2, C13 SuperBot (SINGO) D2, C17 HyMod (HiGen) D2.** Shared in kind: a connector whose latch is driven by the unit's own motor and holds without power. Differs in form and in the reason it holds: ATRON by a non-back-drivable lead screw on hooks that grab bars; SINGO by a motorized circular gear and four chuck jaws (genderless, single-end-operative); HiGen by a motor-rotated four-hook ring (genderless). v3: a gendered peg, a tongue entering a groove, an over-centre four-bar. Kept different: peg and groove, four-bar stops, hex roll lock. These three share the generic "motor-driven unpowered latch" class with Roombots; none shares the crank-to-stop principle.

**M3. C12 PolyBot D3 and D4, C14 CKBot D3, Q64-C21 CONRO D3 and D4.** Shared in kind: chain modules joined by an actuated rotational joint and chain topologies docked by joint motion. Differs: in those systems the joint is the locomotion actuator and docking is by joint motion with IR guidance (CONRO, PolyBot). In v3 locomotion is rolling of the whole prism by the lift ring; the yaw turntable (plus or minus 12 degrees, vertical axis only on certain faces) exists for chain bending (Q31) and is not a locomotion actuator; docking is by the unit's own roll step. Kept different: no pitch joint, no joint-driven gait, no IR guidance.

**M4. C7 M-Blocks D3 and C8 3D M-Blocks D3** (read: 3D M-Blocks). Shared in kind: a rigid polyhedral module pivots over one of its edges on a surface. Differs: M-Blocks use an internal braked **flywheel** (momentum impulse, no external moving part); v3 has no flywheel and no brake: a **ring-mounted lobe** pushes on the table and lifts the body quasi-statically past the tipping edge, then gravity completes the step (~0.265 s of ring motion at rated load). Prism rolling is on a 60 degree step about the axis, not cube-edge pivoting in three axes. Kept different: no stored angular momentum, no magnets; Q62 exclusion 1 is not present (s7).

**M5. C7 M-Blocks D4 and C8 3D M-Blocks D4.** Shared in kind: a module reaches a docked pose by pivoting over an edge. Differs: M-Blocks pivot about a neighbour's shared edge inside a cubic lattice with magnetic hinges; v3 rolls about its own bottom edge so that a neighbour's peg slides along an arc channel into a receiver, in a chain, with a mechanical lock and no magnets.

**M6. Q64-C23 Akitaya et al. D3** (read). Shared in kind: a hexagon rotating about a vertex. Differs: theory of pivoting hexagon modules in a grid with no mechanism; v3's pivot is about a ground edge, for a 3D prism, with a defined lobe drive.

## 6. Family check (Q62 s3)

Family A: a single rigid polyhedral body that moves by whole-body pivoting or rolling over edges, with couplers on faces. The declaration states `family: A`. v3 is a hexagonal prism that rolls over its long edges, and its couplers (peg, receiver) are on its two hexagonal end faces. The lift ring, yaw puck and keeper are internal moving parts; they do not change the body's whole-body motion, which is rolling over edges. Membership: **meets Family A**. Recorded here as the reviewer's reading from the declaration.

## 7. Exclusion checks (Q62 s3)

- **Cube with an internal flywheel: not present.** The body is a hexagonal prism (51.0 mm across corners, 44.2 mm across flats, 28 mm long), not a cube. The declaration lists 66 components, none a flywheel or reaction wheel (text search of the JSON found none). The only rotating mass in locomotion is the lift ring (about 38 rpm, geared down, quasi-static lift, with the ring stopped after tipping), which does not satisfy a flywheel description. No magnet.
- **Needle- or particle-like silhouette: not present.** A stout prism with large flat faces, about 28 mm long by 51 mm wide, with a 14.5 mm peg projecting from the head face. Not a needle and not a particle-scale unit.

## 8. Fail-rule evaluation (Q61 s3)

1. Any cell against F1 (A1) high: **no** (all N).
2. Two or more cells against the same reference high: **no**. The only high is C6 D2. High cells against F1 or F2: **0**.
3. Every moderate cell has a differentiation note: **yes** (s5.2, 15 cells).
4. Every high cell against a non-F1 reference has a note and is listed in the summary: **yes** (s0, s5.1).
5. Both Q62 exclusions are explicitly checked and recorded: **yes** (s7).
6. Matrix completeness: every corpus entry (A1, B1-B4, C1-C23, D1-D4, Q64-C21..C29) and Y1-Y5 has five rated cells with a reason and a source: **yes**.
7. G8 (Q62): no cell high against any F1 or F2 reference, and both exclusions not present: **satisfied by this record**.

Q61 s3 outcome: **pass**. This means only that no rule was triggered by the references examined.

## 9. Problems noticed in the inputs and limits

1. **Author self-check understates the Roombots overlap.** Dossier-v3 s13 rates C6 Roombots D2 = L (grouped with ATRON and FreeBOT) and lists only CONRO and PolyBot as D2-sensitive. The primary paper shows the crank-and-slider non-reversible-singularity lock (s5.1). The corpus descriptor for C6 ("active mechanical connectors") also hides it. Same pattern as the C12 gap found in the v2 review.
2. **Corpus gaps to append later:** C6 Roombots ACM (crank-slider singularity lock, hermaphrodite latch-and-groove), C4 ATRON (lead-screw hooks), C13 SuperBot SINGO, C17 HiGen (all motor-driven unpowered latches), and C12 PolyBot (SMA latch plate, already noted in Q67 item 5).
3. **Cells capped at low because the primary source could not be read:** Q64-C22 HEXEL D1 (paper and institute page HTTP 403; v2 rated this moderate from a press release), Q64-C24 (HAL denied), C3 M-TRAN III D2 (IJRR paper not obtainable; hooks per the HiGen paper's related work), Y2 GENFA D2. A paper-level reading could raise any of these; the likeliest to rise are M-TRAN III D2 and GENFA D2, to moderate, which would not change the outcome (they would share only the generic motor-driven latch class).
4. **Corpus C23 URL/title** still points to a differently titled SoCG 2021 paper (see s4.4).
5. **Corpus Q64 table** gives no access dates; this record gives its own.
6. **Single-end release is a further overlap in kind.** The dossier states that release needs no help from the neighbour (the keeper is in the unit's own receiver). SINGO and HiGen advertise single-sided disconnect. This was considered inside M2 and is not separately rated.
7. **No reference was found** that combines a prism rolled by a ring-mounted lobe with a roll-in arc-channel docking move. Search results are not proof of absence.

## 10. Changes made as a result of the review

None. The reviewer edits no candidate file. The v2-to-v3 changes (SMA and spring removed, motor-driven over-centre four-bar keeper, hex-in-hex roll lock, 304 band) are the author's, recorded in Q68. This is the first review of v3.

## 11. Required changes

None are required for the outcome. Recommended, not required:

1. A later corpus revision should add the Roombots ACM, ATRON, SINGO and HiGen latch mechanisms to their descriptors (s9 item 2).
2. If cand-a is selected for the next stage, the final-visuals review (Q61 s7) should re-rate D2 against Roombots, CONRO and PolyBot G2 with the final coupler geometry. The author should consider whether to differentiate the keeper from a crank-to-singularity latch (for example, a lock whose holding principle is not an over-centre stop) if a second Roombots high ever appears. That is a design choice for the Q38 gates, not something this review decides.
3. Read the HEXEL paper, the Q64-C24 paper, the M-TRAN III paper and GENFA in an r2 review if any of those cells is relied on.

## 12. Standing statement

This review reduces copying risk and does not claim absolute originality.
