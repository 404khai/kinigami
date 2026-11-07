# Originality review (Q61, stage gate1): cand-a v4, r1

candidate_id: cand-a
candidate_version: 4
declaration_sha256: f6c18f80dd14815538e923cdb9c1f7c3c514fc7d22d55518d0c45063ef62b05d
stage: gate1
author: Claude Opus 5.5 (engineering lead) with Claude Sonnet 5.5 (cand-a v4 implementation agent)
reviewer: reviewer-a4-originality (Claude Sonnet 5.5, independent session, no authorship in cand-a v4)
high_cells_f1_f2: 0
exclusion_cube_with_internal_flywheel: not_present
exclusion_needle_or_particle_silhouette: not_present
outcome: pass

Date: 2026-11-07. This review reduces copying risk and does not claim absolute originality.

## 0. Summary

- Result: **pass** under Q61 s3. No cell against F1 or F2 is high. No reference has two high cells. Both exclusions are not present. Every moderate and high cell has a differentiation note (s5) and rests on a primary source read in this session (s1).
- **High cell (Q61 s3 item 4), non-F1/F2, one cell:** C6 Roombots D2 (coupler concept). Same locking principle as in v3: a motor-driven crank mechanism drives a latch element into an unpowered, non-reversible end position. v4 did not remove it (Q70 s4 says so). Details in s5.1.
- **Moderate cells (14; v3 had 15, the difference is CKBot D3, capped at low here because its page was not re-read):** C4 ATRON D2; C12 PolyBot D2, D3, D4; C13 SuperBot D2; C17 HyMod D2; Q64-C21 CONRO D2, D3, D4; C7 M-Blocks D3, D4; C8 3D M-Blocks D3, D4; Q64-C23 pivoting hexagons D3.
- **What v4 changed did not move any rating.** The top-face (F3) docking with arc channels, the flat seat plus three-flat jaw, the semicircular-notch tongue and the 304 thrust washer are mechanical details. No reference with them was found. None of them is distinctive enough in the corpus to raise or lower a cell. The Roombots high is the pattern to watch: a second high against Roombots (for example in D1 or D4) would fail rule 2.
- Pass means only that no fail rule was triggered by the references examined (Q61 s3). It is not a clearance of the design. The coupler is a stack of known elements (peg-in-groove latch class, motor-driven over-centre lock, unpowered hold). The pass rests on the rule structure and on the form differences in s5.

## 1. Basis, limits and primary sources

- Compared: `candidates/cand-a/declaration.json` (v4) and `candidates/cand-a/dossier-v4.md`. SHA-256 from `shasum -a 256 candidates/cand-a/declaration.json`: `f6c18f80dd14815538e923cdb9c1f7c3c514fc7d22d55518d0c45063ef62b05d`. The `author` header is copied exactly from the declaration's `author` field.
- Compared against every corpus entry: A1, B1-B4, C1-C23, D1-D4, Q64-C21..Q64-C29 (Q65 identifiers), plus Y1-Y7 from s2. Dossier s13 (the author's self-check) was read as a list of points to examine and was not used as a rating. The v3 review was read as context only. All ratings below were made afresh.
- The declaration is the authority. The dossier summary and the declaration summary agree (hexagonal prism, circumradius 25.5 mm, 28 mm long, 41.741 g, F3 rest orientation, lobe ring, peg and receiver, motor-driven four-bar keeper, no SMA, no spring, no magnet).
- Fictional entries have no primary design document. They are rated from corpus descriptors, as the corpus states. Cells rated none or low against corpus entries use corpus descriptors, which Q64 allows.
- **Primary sources read for moderate and high cells (all 2026-11-07, text extracted from the fetched documents; passages cited are those found):**
  - Roombots: Sprowitz et al., Robotics and Autonomous Systems 62 (2014) 1016-1033, https://documents.epfl.ch/groups/e/ep/epflmedia/www/20140520_Roombots/roombots%20publication.pdf . ACM section read: latch-and-groove hermaphrodite design; "no power in the connected state"; "Its crank and slider mechanism pushes the latch into an externally non-reversible singularity position"; flat connectors with no pins or extrusions; Fig. 5 lists four latch principles (pin-and-socket, rotary hook, AMAS, other).
  - CONRO: https://robots.isi.edu/conro/proto2H.html (whole page). Read: "the latch engages grooves on the pins and secure them"; "a SMA wire is contracted pulling the latch back"; "a spring brings the latch back to the close position".
  - PolyBot G2: Yim et al., "Connecting and disconnecting for chain self-reconfiguration with PolyBot", https://modlab.engineering.upenn.edu/publications/asme.pdf . Read: electromechanical latches that "latch onto the pins protruding from the opposite face"; latch plate whose four legs reach around the grooves in the pins; two 150 micron SMA wires; IR ranging for closed-loop docking; modules are prisms with one rotational DOF.
  - SINGO (SuperBot connector): Shen, Kovac, Rubenstein, https://robots.isi.edu/prl/shen2009SINGO.pdf . Read: four jaws on sliding rails like a chuck, genderless, the jaws "bite" each other, compliance from the jaw shape.
  - HiGen (HyMod): Parrott, Dodd, Gross, IROS 2014, https://sheffield.ac.uk/media/22956/download . Read: hooks that translate in and out from a central point; genderless; DC geared motor with a 298:1 gearbox; related-work text on M-TRAN III extendible hooks is second-hand and used only as context.
  - ATRON: Ostergaard et al., Autonomous Robots 21:165-183 (2006), https://sccn.ucsd.edu/download/robot.pdf , section 4.4. Read: "three hooks emerge" from the female connector; "driven by a DC motor via a lead screw"; the mechanism "is not backdrivable in the extended arm position".
  - 3D M-Blocks: Romanishin et al., ICRA 2015, https://people.csail.mit.edu/sclaici/pdf/romanishin20153d.pdf . Read: "In each step, the module pivots about one of its edges"; magnetic bonding; modules reconfigure by pivoting about their neighbours; flywheel torque is turned into pivoting. The 2013 M-Blocks paper (C7) was not obtained separately; the 2015 paper restates the single-axis model, so the C7 cells rest on it.
  - Akitaya et al., "Characterizing Universal Reconfigurability of Modular Pivoting Robots", SoCG 2021, https://erikdemaine.org/papers/HingedPixels_SoCG2021/paper.pdf . Read: "pivots, where a hexagonal module rotates around a vertex shared with another module"; theory only.
  - CKBot: the D3 moderate relies on the corpus descriptor and the v3 reading of https://www.modlabupenn.org/ckbot/ ; this session did not re-open that page. Because the Q61 rule requires a primary-source reading for a moderate cell and the page was not re-read, **the CKBot D3 cell is capped at low** in the matrix below.
- **Not read (cells capped at low):** Q64-C22 HEXEL (Science Robotics, HTTP 403 in earlier reviews; not re-attempted), Q64-C24 (HAL page denied in earlier reviews), M-TRAN III (C3; paper not obtained), CKBot page (above), Y4 to Y7 (search summaries only).

## 2. Search record

Date 2026-11-07. Tool: web search (standard mode), plus WebFetch of the primary sources in s1. The first-pass terms below were used in addition to the corpus.

1. "modular robot polygonal prism rolls edge to edge docking peg slides arc channel over-centre toggle latch connector"
2. "tumbling modular robot internal rotating ring lobe flips body over edge self-reconfigurable"

Findings:

- No modular robot was found that rolls a prism over its edge so that a neighbour's peg runs along an arc channel into a receiver. No ring-mounted lobe on a prism was found. Search results are not proof of absence.
- Motor-driven latches that hold unpowered exist (Roombots, ATRON, SINGO, HiGen). The one found that uses a crank-and-slider into a singularity is Roombots.
- Y4 (rhombic dodecahedral cells, https://arxiv.org/abs/2403.01323): rotation of one cell about the edge of another and genderless passive docking for radially symmetric polyhedra. Search summary only. It shares edge pivoting and passive docking in kind, so it is a near neighbour of M-Blocks in D3 and D4.
- Y6 (cone-hole docking for a modular reconfigurable mobile robot, https://doi.org/10.1108/IR-11-2022-0295): arc-shaped cone head with a spring and arc connecting rods forming a ring hole; passive locking. Search summary only. An arc-shaped passive docking guide appears, but with a cone, a spring and a mobile robot. Low.
- Y7 (polygon-based modular robot with arced t-slots on the edges, search summary only): low.
- Y1-Y3 and Y5 from the v3 search (Zhang et al. 2017 docking classification; GENFA; FlipWalker; Truss Link) were re-listed. They were not re-read this session and are rated low from their summaries.
- F2 examined: Replicators (B1), Prey (B2), Borg/Star Trek nanites (B3), T-1000 (B4). No further fictional entries were searched.

## 3. References examined, by class

- F1: A1. F2: B1, B2, B3, B4.
- P: C1-C23, Q64-C21..Q64-C29, Y1-Y7. K: D1-D4.

## 4. Similarity matrix

Key: N none, L low, M moderate, H high. Reason order D1 silhouette, D2 coupler, D3 actuation and locomotion, D4 assembly, D5 visual identity. The Sources column applies to the whole row (access date 2026-11-07 for pages read this session; corpus dates 2026-11-04 for corpus-only rows).

v4 summary used: regular hexagonal prism (R 25.5 mm, 28 mm long, 41.741 g), pale PA12 with exposed 304 steel parts, rolling over long edges via a lobe ring (lobe reach 28.5 mm, parked at body -z), peg on the head end, and a receiver on the tail end. The receiver has two circular-arc roll-in channels on the F3 landing face (a V opening toward +z), a yaw turntable, a flat seat plus a three-flat jaw as roll lock, a thrust washer, and a motor-driven over-centre four-bar keeper tongue with a semicircular notch that closes on the peg groove. BLE only.

### 4.1 Forbidden and fictional

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| A1 BH6 (F1) | N - one 51 mm prism vs thousands of small near-identical dark units | N - mechanical peg and keeper vs magnetic legs | N - lobe-ring tumbling of a single unit vs units crowd-surfing | N - end-to-end chain vs arbitrary shapes | N - pale plastic and steel vs a dark liquid swarm | https://gizmodo.com/how-disney-will-make-you-cry-again-with-big-hero-6-1630115219 ; https://awn.com/animationworld/don-hall-and-chris-williams-talk-disneys-big-hero-6 (corpus) |
| B1 Replicators (F2) | N - hex prism vs insect-like blocks | N - peg/keeper vs unspecified interlock | N - tumbling vs scuttling | L - both join identical units, generic | N | https://en.wikipedia.org/wiki/Nanotechnology_in_fiction (corpus) |
| B2 Prey (F2) | N | N | N | N | N | same |
| B3 Borg nanites (F2) | N | N | N | N | N | same |
| B4 T-1000 (F2) | N | N | N | N | N | same |

### 4.2 Published robots, section C

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| C1 M-TRAN I | L - box-like body | L - magnets vs mechanical peg | L - chain gaits vs rolling | L - generic | N | DOI 10.1109/TMECH.2002.806220 |
| C2 M-TRAN II | L | L | L | L | N | corpus URL |
| C3 M-TRAN III | L | L - extendible hooks, second-hand only (HiGen related work); capped at low | L | L | N | DOI 10.1177/0278364907085560 ; HiGen paper |
| C4 ATRON | L - spherical halves | **M** - read: three hooks driven by a DC motor via a lead screw; the drive "is not backdrivable in the extended arm position". Shared in kind: motor-driven latch that holds unpowered through the drive geometry. Differs: hooks on bars of a point lattice connector vs a tongue in a groove of a peg; self-locking screw vs a four-bar with stops | L - equatorial rotation | L - lattice vs chain | N | DOI 10.1109/IROS.2004.1389702 ; https://sccn.ucsd.edu/download/robot.pdf s4.4 |
| C5 SMORES-EP | L | L - electro-permanent magnets vs mechanical | L | L | N | DOI 10.1126/scirobotics.aat4983 (corpus) |
| C6 Roombots | N - paired spheres | **H** - read: motor and gears drive a crank and slider that push the latch "into an externally non-reversible singularity position", "no power in the connected state", latch-and-groove interaction. v4: a motor drives a crank-rocker four-bar into hard stops 10 degrees past both dead centres, tongue loads push the crank into its stop, tongue closes on a groove. Same principle (motor-driven crank mechanism to a non-reversible position with an unpowered hold, acting on a groove). Form differs a great deal (s5.1) | L - 3 rotational DOF | L - 3D self-reconfiguration | N | DOI 10.1016/j.robot.2013.08.011 ; EPFL PDF, ACM section |
| C7 M-Blocks | L - cube vs hex prism | L - magnets vs mechanical | **M** - read (3D M-Blocks restating the model): rigid body pivoting about one of its edges per step. Differs: braked flywheel impulse vs quasi-static ring lobe | **M** - pivoting about a neighbour's edge into a docked pose; v4 docks by rolling one step about its own bottom edge. Differs: magnetic lattice vs a mechanical chain lock | L - plain cube vs visible peg and lobe | DOI 10.1109/IROS.2013.6696971 ; https://people.csail.mit.edu/sclaici/pdf/romanishin20153d.pdf |
| C8 3D M-Blocks | L | L | **M** - flywheel torque redirected into pivoting about several axes; same kind as C7 | **M** - reconfigure by pivoting about neighbours | L | DOI 10.1109/ICRA.2015.7139450 ; same PDF |
| C9 Kilobot | N | N | N | N | N | DOI 10.1109/ICRA.2012.6224638 |
| C10 catoms | L | L | L | L | N | DOI 10.1109/MC.2005.198 |
| C11 Molecubes | L | L | N | L | N | DOI 10.1038/435163a |
| C12 PolyBot | L - small prism-like module | **M** - read: latch plate with four legs reaching around grooves in protruding pins; SMA release; engaged hold passive. Shared in kind: a latch element entering annular grooves of protruding pins with an unpowered hold. Differs: SMA release and spring return are absent; v4 has one hex peg, a motor four-bar tongue, a roll lock and a roll-in channel | **M** - read: prisms with one rotational DOF in chains vs v4's yaw per coupler in a chain; v4 locomotes by rolling | **M** - chain reconfiguration by joint-aided docking with IR vs end-to-end chain docked by roll-in | L | https://modlab.engineering.upenn.edu/publications/asme.pdf ; ICRA 2000 record (corpus) |
| C13 SuperBot | L | **M** - read (SINGO): four chuck-like jaws on rails, genderless, jaws bite each other. Shared in kind: motor-driven latch holding without drive. Differs: genderless jaws vs gendered peg and tongue; no groove-on-pin; no four-bar | L | L | N | https://robots.isi.edu/prl/shen2009SINGO.pdf |
| C14 CKBot | L | L | L - one rotational DOF per module in chains (corpus; page not re-read, capped at low) | L | N | https://www.modlabupenn.org/ckbot/ |
| C15 Soldercubes | L | L | L | L | N | DOI 10.1007/s10514-015-9441-4 |
| C16 FreeBOT | N | L | L | L | N | https://freeformrobotics.org/wp-content/uploads/2022/02/IROS20_0857_FI.pdf |
| C17 HyMod | L | **M** - read (HiGen): hooks translating in and out from a central point, motor with 298:1 gearbox, genderless. Shared in kind: motor-driven latch with an unpowered hold. Differs: genderless hook ring vs gendered peg; no groove-on-pin; no four-bar | L | L | N | DOI 10.1007/978-3-319-73008-0_28 ; https://sheffield.ac.uk/media/22956/download |
| C18 Telecube | L | L | N | L | N | https://researchr.org/publication/SuhHY02 |
| C19 Crystalline | L | L | L | L | N | DOI 10.1023/A:1026504804984 |
| C20 PolyPod | L | L | L | L | N | https://www.mit.edu/people/manoli/polypod/polypod.html |
| C21 Swarm-bot | N | L - gripper vs peg | N | L | N | DOI 10.1023/B:AURO.0000033972.50769.1c |
| C22 Sambot | L | L - one active docking face vs v4's peg end and receiver end | N | L | N | DOI 10.1109/TMECH.2010.2085009 |
| C23 Blinky Blocks | N | L | N | L | N | DOI 10.1145/1979742.1979712 |

### 4.3 Commercial kits

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| D1 Cubelets | L | L - magnets | N | L | N | https://modrobotics.com/about-us |
| D2 MOSS | L | L | L | L | N | https://forums.parallax.com/discussion/151259/moss-brand-new-robot-construction-system-from-modular-robotics |
| D3 UBTech Jimu | N | L | L | L | N | https://www.pcworld.com/article/419049/ubtech-looks-to-up-its-toy-robot-game-with-the-jimu.html |
| D4 LEGO EV3 | N | L | L | L | N | https://www.lego.com/en-us/product/31313 |

### 4.4 Q64 additions (Q64-C21..C29) and this review's additions (Y)

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| Q64-C21 CONRO | L - elongated box segments vs hex prism | **M** - read: latch engages grooves on pins; SMA pulls the latch back; a spring closes it. Shared in kind: a latch element entering grooves of protruding pins, unpowered hold. Differs: no SMA, no spring-closed default; v4 has a motor four-bar tongue, one hex peg, flat seat plus jaw roll lock, roll-in channel. Borderline (s5.2) | **M** - two DOF modules chained to locomote vs v4's yaw per coupler (primary source: the CONRO connector page; the DOF statement relies on the v3 reading of Shen 2001, not re-read, so this cell is held at moderate only by the corpus descriptor; see s9) | **M** - chains docked by joint motion with IR guidance vs end-to-end chain docked by roll-in | L | https://robots.isi.edu/conro/proto2H.html |
| Q64-C22 HEXEL | L - hexagonal exoskeleton of plates vs solid prism; paper unread, capped at low | L | L | L | L | https://www.eurekalert.org/news-releases/1058118 ; DOI 10.1126/scirobotics.adl3546 (not read) |
| Q64-C23 Hinged Pixels (Akitaya et al.) | L | N - theory | **M** - read: "a hexagonal module rotates around a vertex shared with another module". In cross-section a v4 roll step is a hexagon turning about a vertex: the same kind of move. Theory only; the pivot here is about a ground edge | L | N | https://erikdemaine.org/papers/HingedPixels_SoCG2021/paper.pdf |
| Q64-C24 rolling cylinders on hex lattice | L | L | L | L | N | https://hal.archives-ouvertes.fr/hal-02300456 (not read; capped at low) |
| Q64-C25 PenduMorph | N | L - magnetic | N - pendulum sphere | L | N | https://arxiv.org/pdf/2606.22491 (corpus) |
| Q64-C26 Rotundus | N | N | N | N | N | https://orionrobots.co.uk/wiki/rotundus |
| Q64-C27 Sphero/BB-8 | N | N | N | N | N | https://newatlas.com/sphero-bb-8-droid/39269/ |
| Q64-C28 MOPARAS | N | L | N | L | N | https://research.polyu.edu.hk/en/publications/moparas-a-modular-parallel-spherical-robot-with-position-adjustab/ |
| Q64-C29 pendulum sphere literature | N | N | N | N | N | https://ar5iv.labs.arxiv.org/html/2302.08932 |
| Y1 Zhang et al. 2017 docking | L | L - classification of connector types, summary | L | L | N | https://mdpi-res.com/d_attachment/robotics/robotics-06-00025/article_deploy/robotics-06-00025.pdf |
| Y2 GENFA | L | L - genderless fail-safe connector, abstract only | N | L | N | IEEE ROBIO 2011 (search abstract) |
| Y3 FlipWalker | L | L | L - flipping locomotion, summary only | L | N | arXiv 2508.19380 |
| Y4 Rhombic dodecahedral cells | L - polyhedral cell vs prism | L - genderless passive docking | L - rotation about neighbour's edge (summary only, capped) | L | N | https://arxiv.org/abs/2403.01323 |
| Y5 Truss Link tumbling | L | L | L - tumbling, summary only | L | N | arXiv 2508.01829 |
| Y6 Cone-hole docking | N | L - arc-shaped docking head and ring hole, spring; passive locking; summary only | N | L | N | https://doi.org/10.1108/IR-11-2022-0295 |
| Y7 Polygon modular robot with arced t-slots | L | L | N | L | N | search summary |

## 5. Differentiation notes

### 5.1 Roombots D2 (high)

Shared: a motor-driven crank mechanism that moves a latch into an unpowered, non-reversible position; latch acting on a groove; connected state needs no power. Different, and kept different in v4:
- Roombots: hermaphrodite flat surface connector with no pins; a crank-slider drives a latch against a groove on the other module's surface; the module is two fused spheres.
- cand-a v4: gendered, a protruding hex peg on one end and a receiver on the other; a crank-rocker four-bar with stops 10 degrees past both dead centres; the tongue (semicircular notch) closes at the groove of the peg; a flat seat plus three-flat jaw carry roll; arc channels and a yaw turntable guide entry.
- v4 does not claim a non-reversible lock in all load cases: load reversal at the dead centre needs friction of at least 0.10 to 0.14 (assumed, Q70 s4). Roombots describes the singularity as externally non-reversible.
- Kept: no unified connector, no hermaphrodite face. Changed relative to Roombots: the roll-in arc entry, the roll lock and the thrust washer have no counterpart in the Roombots ACM as read.

The high stays. It is allowed under Q61 (a single non-F1/F2 high needs a note and a prominent listing). A change that makes the keeper a spring or an SMA design would drop the high but move CONRO and PolyBot D2 toward high.

### 5.2 Moderate cells

- **CONRO D2 and PolyBot D2 (borderline).** What is shared is a latch element that enters grooves on a protruding pin. What differs: CONRO and PolyBot use SMA release and spring return; v4 has neither. v4 has one hex peg (CONRO and PolyBot use two or more pins), a tongue with a semicircular notch, a motor four-bar, a roll lock, and a roll-in channel. It would become high if a spring-closed, SMA-released latch were added, or if the connector grew to a multi-pin latch plate. v4 did not adopt any of these.
- **CONRO D3, D4 and PolyBot D3, D4.** Chain-style systems with one or two DOF per module. v4's yaw turntable is a coupler alignment actuator, not a locomotion joint; v4 locomotes by rolling and docks by rolling, not by joint-aided IR docking.
- **ATRON D2, SuperBot D2, HyMod D2.** Motor-driven latches with unpowered holds. v4 differs in form: gendered peg and tongue vs hooks or jaws; four-bar vs lead screw or chuck.
- **CKBot D3.** Capped at low this round (page not re-read), so it carries no moderate note; the v3 note stands as context only.
- **M-Blocks D3, D4; 3D M-Blocks D3, D4.** Shared: a rigid body pivoting about an edge to reconfigure. Differs: no flywheel (kept, so exclusion 1 stays not present), quasi-static lobe ring, hex prism, mechanical chain lock vs magnetic lattice. This is the reason the lobe ring and the absence of an inertial actuator are retained.
- **Q64-C23 Hinged Pixels D3.** Shared: hexagon turning about a vertex. Differs: theory in a planar grid vs a physical 3D unit with a ground edge pivot.

## 6. Family and exclusion checks

- Family A (Q62 s3): a single rigid polyhedral body (hexagonal prism) moving by rolling over edges, couplers on faces (the two end faces). The ring, yaw puck and keeper are internal moving parts. Member.
- Exclusion 1, cube with an internal flywheel: **not present.** The body is a hexagonal prism, not a cube. Declaration text search found no flywheel or reaction wheel; the actuator is a lobe ring driven by a gearmotor.
- Exclusion 2, needle- or particle-like silhouette: **not present.** The body is 51 mm across corners and 28 mm long; the aspect ratio is about 1.8:1 across corners.

## 7. Fail rules

1. Any F1 cell high: no (A1 is N in all five).
2. Two or more highs against one reference: no (Roombots has one high, D2).
3. Every moderate cell has a note: yes (s5.2).
4. Every non-F1/F2 high has a note and is listed prominently: yes (s0, s5.1).
5. Both exclusions recorded: yes (s6).
`high_cells_f1_f2` = 0.

## 8. Changes from v3 and effect on ratings

| v4 change | Effect |
| --- | --- |
| Docking on the F3 face; arc channels corrected (V toward +z) | No new reference found. D2 and D4 unchanged. Y6 shares an arc guide in kind (low) |
| Flat seat plus three-flat jaw (v3 hex-in-hex cup removed) | Generic anti-rotation; D2 unchanged |
| Semicircular-notch tongue closing at the groove | Same peg-in-groove class as CONRO and PolyBot; D2 moderate unchanged |
| 304 thrust washer | No counterpart in the corpus; no cell affected |
| Motor four-bar keeper kept | Roombots D2 high unchanged; CONRO and PolyBot D2 stay moderate |

## 9. Limits and what was not read

- Cells capped at low for lack of a primary source: C3 (M-TRAN III), C14 CKBot D3 (page not re-opened), Q64-C22 HEXEL, Q64-C24, Y2-Y7. A reader of these could raise a cell. HEXEL is hexagonal, so its D1 is the one most worth checking.
- The CONRO D3 and D4 moderates rely on the earlier reading of Shen et al. 2001 (docking paper), which this session did not fetch; the CONRO connector page was read. Treat those two cells as moderate by the corpus descriptor and the v3 reading, and as at risk of dropping to low, not of rising to high.
- The Roombots and PolyBot papers were read through text extraction; figures were not inspected.
- No searched source shows a hexagonal prism with a lobe ring and a roll-in dock. That is a search result and not proof of novelty.

## 10. Required changes

None for a pass. Recommendations, not conditions:
1. Keep a second Roombots-type high from appearing (do not adopt a hermaphrodite flat connector face).
2. Do not add SMA release or spring-closed latch logic, which would push CONRO and PolyBot D2 to high.
3. At final visuals, rate D5 afresh. The pale PA12 and bare 304 look is not compared with any reference in this review beyond the corpus descriptors.

## 11. Outcome

**pass.** No fail rule triggered. One high (Roombots D2), fourteen moderates, both exclusions not present.

This review reduces copying risk and does not claim absolute originality.
