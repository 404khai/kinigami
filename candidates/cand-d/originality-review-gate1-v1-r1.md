# Originality review (Q61, stage gate1): cand-d v1, r1

candidate_id: cand-d
candidate_version: 1
declaration_sha256: 4b6788a544f6a4226d7bcf0e8951fbf789e44b6c67cbf2ae2eb312ff31bbf64a
stage: gate1
author: Claude Opus 5.5 (engineering lead, cand-d author)
reviewer: reviewer-d1-originality (Claude Sonnet 5.5, independent session, no authorship in cand-d)
high_cells_f1_f2: 0
exclusion_cube_with_internal_flywheel: not_present
exclusion_needle_or_particle_silhouette: not_present
outcome: pass

Date: 2026-11-20. This review reduces copying risk and does not claim absolute originality.

## 0. Summary

- Result: **pass** under Q61 s3. No cell against F1 (A1) or F2 (B1-B4) is high. No reference has two high cells. Both Q62 exclusions are not present. Every moderate cell has a differentiation note (s5).
- **High cells (Q61 s3 item 4): none.** I looked hard for one. The closest calls are PolyBot D1 and CONRO D1/D2. I held them at moderate for the reasons in s5.
- **Moderate cells (15):** C4 ATRON D2; C6 Roombots D2; C12 PolyBot D1, D2, D3, D4; C14 CKBot D3; C17 HyMod D2; Q64-C21 CONRO D1, D2, D3; Y1 ModLock D2; Y2 Zhang et al. docking system D2; Y3 RoFICoM D2; Y4 WPI twist-lock poster D2.
- **Where the risk is.** Body, joint and chain behaviour (D1, D3, D4) are close to PolyBot and CONRO in kind. That is forced by Family B (one joint, couplers at segment ends). The coupler (D2) is a stack of known elements: a motor-turned ring with a helical slot (RoFICoM), a bayonet-style twist-lock (ModLock, Zhang, WPI poster), a non-backdrivable motor latch (ATRON, Roombots), and an unpowered hold. It is not a copy of any one of them.
- **Caps.** Primary papers for M-TRAN (all), CKBot's module paper, PolyPod and CoBoLD were not obtained. Those cells are capped at low and listed in s1. They are the main reason the first revision (r2) should re-read sources. If a later reader confirms CoBoLD D2 or M-TRAN D1 as moderate, it needs a note, but cannot by itself cause a fail.
- Pass means only that no fail rule was triggered by the references examined. It is not a clearance of the design.

## 1. Basis, limits and primary sources

**What was compared.** `candidates/cand-d/declaration.json` and `candidates/cand-d/dossier.md`.
- SHA-256 from `shasum -a 256 candidates/cand-d/declaration.json`: `4b6788a544f6a4226d7bcf0e8951fbf789e44b6c67cbf2ae2eb312ff31bbf64a`. It equals the expected value. The `author` line above is copied from the declaration's `author` field.
- Dossier section 7 (the author's self-check) was read as a list of points to examine and was **not** used as a rating.
- The cand-a v5 and cand-b v1 reviews were read for format only. Ratings were made afresh.

**Summary of cand-d v1 as declared (used for every cell).**
- Body: two PA12 shell segments, head 33.8 mm long, tail 8.8 mm, 25.4 x 24 mm section, 3.6 mm hinge gap, 47.2 mm site to site. Stowed enclosing sphere 58.862 mm.
- Joint: one vertical revolute joint, pin at mid-gap, spur sector driven by a 6 mm gearmotor, working range plus or minus 15 degrees.
- Coupler: rigid and gendered. Tail stud (flange, 4 mm pilot, two 3 mm lugs) enters the head cartridge. The cartridge has a pilot bore, axial lug slots, and a bronze cam sleeve with two helical slots (20 degree capture stage, 3 degree self-locking lock stage). A 6 mm gearmotor turns the sleeve to a voltage-limited stall. Hold is passive (friction self-locking). Release turns the sleeve back.
- No SMA, no spring, no magnet. BLE only. No power transfer.
- Materials declared: PA12 SLS shell (EOS PA2200 white datasheet), 304 stainless steel and C93200 bronze coupler parts, PTFE ring.

**Primary sources read in this session (all fetched 2026-11-20; PDFs converted with pdftotext and searched).**
- PolyBot G2: Yim et al., https://modlab.engineering.upenn.edu/publications/asme.pdf . Read: "The segment modules are nominally rectangular prisms and have one rotational degree of freedom separating two connection ports"; "grooved pins ... A hook-like latch is engaged in the groove on the pin"; the latch plate "rotates about the center of the interface" with "four legs" reaching "around the grooves in the pins"; two "150 micron shape memory alloy (SMA) wire"; a BeCu return spring; an IR ranging system.
- CONRO: https://robots.isi.edu/conro/proto2H.html (whole page). Read: "a passive connector that has pins ... a motor housing ... an active connector"; "the latch engages groves on the pins"; "a SMA wire is contracted pulling the latch back"; "a spring brings the latch back to the close position"; yaw and pitch servos; "10 cm long ... 100 grams".
- ATRON: Ostergaard et al., Autonomous Robots 21:165-183 (2006), https://sccn.ucsd.edu/download/robot.pdf . Read: "The three hooks are driven by a DC motor via a lead screw. The mechanism driving the arms is not backdrivable in the extended arm position, hence no power is required to maintain connection"; "two half spheres joint together by an infinite revolute joint". The same paper also describes PolyBot G2, CONRO and M-TRAN I/II attachment (secondary use only).
- HiGen (HyMod): Parrott, Dodd, Gross, https://sheffield.ac.uk/media/22956/download . Read: "four hooks placed radially"; "298:1 gearbox"; "Once two connectors are joined they can maintain a connection even when power is removed"; genderless.
- SINGO (SuperBot): Shen et al., https://robots.isi.edu/prl/shen2009SINGO.pdf . Read: genderless; "four such jaws" on sliding rails driven by a circular gear; the jaws "bite" each other. I found no statement about an unpowered hold, so D2 is rated low.
- Roombots: Sprowitz et al., Robotics and Autonomous Systems 62 (2014), https://documents.epfl.ch/groups/e/ep/epflmedia/www/20140520_Roombots/roombots%20publication.pdf . Read: "Roombots' ACM requires no power in the connected state. Its crank and slider mechanism ... pushes the latch into an externally non-reversible singularity position"; latches and grooves; 150:1 geared motor.
- CKBot project page: https://www.modlabupenn.org/ckbot/ . Read: 60 x 60 x 60 mm; Hitec HSR5990TG servo; U-bar and L7 types, "one rotational degree of freedom"; modules connect with M3 screws; "chain style modular robot", manually reconfigured. No module paper obtained.
- ModLock: Davey, Sastra, Piccoli, Yim, IROS 2012, https://www.modlabupenn.org/wp-content/uploads/ModLock.pdf . Read: "The faces are twisted 12 deg to align and tighten"; four flat-head screws act as hooks in insertion holes; "a stainless steel locking dowel on a compliant lever snaps into a lock groove"; manual, no motor; failure at 2.2 kN tension.
- Zhang, Zhang, Gupta, "A Novel Docking System for Modular Self-Reconfigurable Robots", Robotics 6(2):25 (2017), https://mdpi-res.com/d_attachment/robotics/robotics-06-00025/article_deploy/robotics-06-00025.pdf . Read: "Both linear motions and rotation motions are required to connect a female interface and a male interface"; the male interface inserts along a slot and rotates into a layer; it "will be spring-backed to the position between two teeth"; rotation is driven by the modules' own locomotion actuators.
- RoFICoM: Mrazek and Barnat, https://rofi.fi.muni.cz/assets/files/publications/roficom.pdf . Read: "four hooks attached to a ring (named clip). The motor rotates the clip, which then slides out of the body using pins driven by a helical slot in the body. The hooks slide under hooks in the mating clip"; "skirt" blocks mutual rotation; 50 mm diameter, 17 mm deep; N20 motor.
- WPI poster, "Self-Assembling Modular Robots Enabled by an Articulated Multi-Axis Connector", https://users.wpi.edu/~cxu5/docs/MSEFPoster.pdf . Read: "Prototype 2: Gendered Twist-Lock Connector. A bayonet or quarter-turn mechanism inspired by androgynous fasteners ... requires rotation during engagement; can be hard to align under load." It is a poster with little detail (a student prototype comparison).
- Other reads used for lower ratings: Eckenstein and Yim, Latching X-Face (IROS 2014), https://www.modlabupenn.org/wp-content/uploads/latching_xface_overlay.pdf (passive compliant two-layer latch, no actuator); Mateos and Vincze, LaMMos, https://arxiv.org/pdf/1801.00035 (motorized-screw latch for links and exoskeleton, not a module coupler); Wyder et al., https://arxiv.org/pdf/2508.01829 (Truss Link magnet connectors; VTT servo latch with a rack and pinion); Muthui, UCT MSc thesis, https://open.uct.ac.za/bitstreams/5dcc9290-b036-4687-b908-3ca62889beac/download (a secondary survey: it describes M-TRAN III hooks, CoBoLD and RIMRES).

**Not obtained (cells capped at low, as in the cand-a reviews).**
- M-TRAN I, II and III papers (C1-C3). Only secondary descriptions were read (the ATRON paper's survey text; the UCT thesis, which says M-TRAN III uses motor, gears, linkage and hooks, gendered, "maintained without power consumption"). M-TRAN D1, D2, D3 and D4 are capped at low.
- CKBot module design paper (C14). The project page was read. D3 is moderate from the page. D2 and D4 are low.
- PolyPod (C20), SuperBot module paper (C13, only SINGO read), Sambot, Swarm-bots and the other low-rated section-C rows: corpus descriptors only.
- CoBoLD primary paper (Liedke and Woern, IEEE ROBIO 2011, DOI 10.1109/ROBIO.2011.6181589). The IEEE record was found but the text was not obtainable. The UCT thesis summary says CoBoLD has "a geared locking wheel, four cone shaped locking bolts" and the locking wheel is "a standard worm wheel where four hooks are milled out". Capped at low. See the risk note in s5.
- Shen et al. 2001 (CONRO docking paper): not read. CONRO D4 is capped at low. CONRO D3 is held by the hardware page's "yaw and pitch axes".
- Q64-C22 to Q64-C29: not fetched. Rated from the corpus descriptors, which place them far from a two-segment inline body.
- Fictional entries have no engineering source and are rated from the corpus descriptors, as the corpus states.

## 2. Search record

Date: 2026-11-20. Tool: web search (standard mode) plus fetch of the sources in s1. Terms and what they returned:

1. "bayonet twist-lock connector modular self-reconfigurable robot rotating collar docking". Returned ModLock, HiGen, the WPI posters (a bayonet/quarter-turn "twist-lock" prototype), a US patent record (US 8,234,950, a homogeneous single-side connector; not read), MDPI Robotics 6:25 (Zhang), arXiv 2508.01829. Added Y1, Y2, Y4, Y9.
2. "self-reconfigurable modular robot connector lead screw self-locking cam sleeve docking mechanism". Returned LaMMos, arXiv 2603.04760 (a cam-shaft tool changer for modular manipulators; PDF too large to fetch, summary only), MODUR (arXiv 2510.13356, hermaphrodite connector; titles and summaries only), MobiDock (arXiv 2510.27178, not read), Sage 10.5772/45709 and 10.5772/58379 (records only). Added Y7, Y10, Y11.
3. "two-segment single joint chain module self-reconfigurable robot hinge module connectors at both ends". Returned PolyBot G2 (segment with a hinge between two connection plates), Rhombot (arXiv 2601.19529, title only), US 6,084,373 (reconfigurable modular joint, record only), MODUR, the IEEE Spectrum modular-robots page. Confirms PolyBot and CKBot as the nearest published two-port, one-joint modules.
4. "CKBot Chain-based modular robot module design servo connector Yim Modlab paper". Returned the CKBot page, Latching X-Face (Eckenstein and Yim), ModLock, SMORES, a CKBot quadratic programming paper (arXiv 2104.02755, not read). Added Y8.
5. "M-TRAN III connection mechanism extendible hooks Kurokawa distributed self-reconfiguration" and a second M-TRAN III query. Returned bibliographic records only. No full text. M-TRAN stays capped.
6. "modular robot connector twist lug stud helical cam slot latching self-reconfigurable motor-driven rotating sleeve". Returned RoFICoM (motor turns a clip that moves along a helical slot), HiGen, the Roombots ACM record (EPFL infoscience 130738), US 10,326,237 (hermaphroditic connector with mating assist; record only). Added Y3.
7. "Sambot OR SINGO OR DRAGON connector OR ModLock bayonet twist docking modular robot motor-driven rotation lock lugs". Returned DRAGON (passive latch, 70 kg tension, 170 g), SINGO (spiral gear jaws), Sambot, SMORES-EP, a self-aligning EPM connector (arXiv 2508.16008, magnetic, not read).
8. "CoBoLD cone bolt locking device docking Symbrion Replicator locking wheel worm gear Liu Kernbach". Returned the CoBoLD IEEE record, arXiv 1108.5543 (multi-robot organisms, text not extractable), and a cone-hole docking paper (DOI 10.1108/IR-11-2022-0295, same as cand-a's Y6; not read). Added Y5. Thesis text about CoBoLD and RIMRES read (Y5, Y6).
9. "M-TRAN III module connection mechanism mechanical hooks half-module 65 mm" returned only patents. Nothing usable.

Findings. No source found shows a module with all of these together: a motor-turned bronze cam sleeve with a capture stage and a 3 degree self-locking lock stage, a two-lug pilot stud drawn onto a flat steel seat by torque-stop travel, in a rigid coupler on an inline two-segment body with a separate body joint. Search results are not proof of absence. They show closest art only.

F2 examined: Replicators (B1), Prey (B2), Borg and Star Trek nanites (B3), T-1000 (B4). No further fictional entries were searched in this review.

## 3. References examined, by class

- F1: A1. F2: B1, B2, B3, B4.
- P (corpus): C1-C23 (C1-C3 M-TRAN, C4 ATRON, C5 SMORES-EP, C6 Roombots, C7-C8 M-Blocks, C9 Kilobot, C10 catoms, C11 Molecubes, C12 PolyBot, C13 SuperBot, C14 CKBot, C15 Soldercubes, C16 FreeBOT, C17 HyMod, C18 Telecube, C19 Crystalline, C20 PolyPod, C21 Swarm-bots, C22 Sambot, C23 Blinky Blocks) and Q64-C21..Q64-C29 (Q65 identifiers).
- K: D1 Cubelets, D2 MOSS, D3 UBTech Jimu, D4 LEGO Mindstorms EV3.
- Added by this review: Y1 ModLock, Y2 Zhang et al. docking system, Y3 RoFICoM, Y4 WPI twist-lock poster, Y5 CoBoLD, Y6 RIMRES latch, Y7 LaMMos, Y8 Latching X-Face and DRAGON, Y9 Truss Link and VTT (Wyder et al.), Y10 MODUR, Y11 arXiv 2603.04760 cam-shaft tool changer.

## 4. Similarity matrix

Key: N none, L low, M moderate, H high. Columns: D1 silhouette and geometry, D2 coupler concept, D3 actuation and locomotion logic, D4 assembly and reconfiguration, D5 visual identity.

**D5 note.** No final visuals exist. D5 is judged only on what the declaration states: white PA12 SLS shell (EOS PA2200 white datasheet), exposed 304 steel and bronze coupler parts, no stated colour scheme, markings or finish. D5 is rated on that and must be re-rated at final visuals (Q61 s7). A D5 "none" here is not a clearance of the final look.

**Cell convention.** A bare N or L means the reference's descriptor shares nothing (N) or only generic features forced by the task or physics (L) in that dimension. The reason is the corpus descriptor of the row, shown short, and the source is the row's Sources column. Every M cell has a full reason and a source read in this session. Access date: 2026-11-20 for pages read in this session, 2026-11-04 for corpus-only sources.

### 4.1 Forbidden and fictional

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| A1 BH6 microbots (F1) | N - one 47 mm two-box unit vs thousands of small near-identical dark units | N - rigid mechanical stud and cam sleeve vs magnetic legs; cand-d has no magnet | N - single geared joint vs units crowd-surfing over each other | N - a chain of identical units vs arbitrary shapes | N - declared pale PA12 shell and bare steel vs a dark liquid-like swarm | https://gizmodo.com/how-disney-will-make-you-cry-again-with-big-hero-6-1630115219 ; https://awn.com/animationworld/don-hall-and-chris-williams-talk-disneys-big-hero-6 (corpus) |
| B1 Replicators (F2) | N - elongated two-box body vs insect-like blocks | N - no mechanism shown in the fiction | N - single hinge vs scuttling | L - both join identical units; generic | N - nothing like grey-silver bug masses | https://en.wikipedia.org/wiki/Nanotechnology_in_fiction (corpus, secondary) |
| B2 Prey (F2) | N | N | N | N | N | same |
| B3 Borg nanites (F2) | N | N | N | N | N | same |
| B4 T-1000 (F2) | N | N | N | N | N | same |

### 4.2 Published robots, section C

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| C1 M-TRAN I | L - two box halves with a link; primary not read, capped (could be M if read) | L - magnets vs mechanical | L - two joints per module vs one; capped | L - capped | N | DOI 10.1109/TMECH.2002.806220 ; Ostergaard 2006 s2.5 (secondary) |
| C2 M-TRAN II | L | L | L | L | N | corpus URL |
| C3 M-TRAN III | L - capped | L - capped. Secondary (UCT thesis): motor, gears, linkage, hooks, gendered, holds without power. Shares the class "motor latch, unpowered hold" with ATRON and HiGen, but a different mechanism (retractable hooks vs a turned cam sleeve). Would be a note, not a fail | L - capped | L - capped | N | DOI 10.1177/0278364907085560 ; https://open.uct.ac.za/bitstreams/5dcc9290-b036-4687-b908-3ca62889beac/download (secondary) |
| C4 ATRON | L - two hemispheres vs two boxes | **M** - read: "three hooks ... driven by a DC motor via a lead screw ... not backdrivable in the extended arm position, hence no power is required". Shared in kind: motor-driven latch held unpowered by a non-backdrivable screw. Differs: three hooks on pivoting arms grabbing bars vs a two-lug stud on helical cam slots; the screw lead vs a 3 degree cam stage with torque-stop seat | L - one infinite-revolute joint, equatorial; lattice moves | L - lattice vs chain | N | DOI 10.1109/IROS.2004.1389702 ; https://sccn.ucsd.edu/download/robot.pdf s4.4 |
| C5 SMORES-EP | L | L - electro-permanent magnets | L | L | N | DOI 10.1126/scirobotics.aat4983 (corpus) |
| C6 Roombots | L - paired spheres vs boxes | **M** - read: "no power in the connected state ... crank and slider ... pushes the latch into an externally non-reversible singularity position"; latches and grooves. Shared in kind: a motor-driven latch with an unpowered, non-backdrivable hold. Differs: crank to a geometric singularity vs friction self-locking helical cam (no over-centre); latch in a groove vs lugs on helical slots on a pilot stud | L - three rotational DOF | L - 3D self-reconfiguration | N | DOI 10.1016/j.robot.2013.08.011 ; EPFL PDF (Fig. 4 text, ACM description) |
| C7 M-Blocks | N - cube vs elongated two-box | N - magnets | N - flywheel pivot | N | N | DOI 10.1109/IROS.2013.6696971 (corpus) |
| C8 3D M-Blocks | N | N | N | N | N | DOI 10.1109/ICRA.2015.7139450 (corpus) |
| C9 Kilobot | N | N | N | N | N | DOI 10.1109/ICRA.2012.6224638 |
| C10 catoms | L | L | L | L | N | DOI 10.1109/MC.2005.198 |
| C11 Molecubes | L - cube with a hinge-like axis | L - electromagnets | L - one rotation axis, generic | L | N | DOI 10.1038/435163a |
| C12 PolyBot | **M** - read: segments are "nominally rectangular prisms" with "one rotational degree of freedom separating two connection ports". Shared in kind: a prismatic two-port body with one joint between the ports. Differs: about 50 mm cube-like with symmetric halves and plates at both ends vs 47.2 x 25.4 x 24 mm, a 33.8 mm head and 8.8 mm tail, gendered ends, off-axis coupler | **M** - read: grooved pins enter holes; a latch plate that "rotates about the center of the interface" with "four legs" reaches around pin grooves; unpowered hold. Shared in kind: pin-in-hole docking and a rotation about the interface axis that locks features on protruding pins. Differs: SMA release, spring return, hermaphroditic four-way pin plate vs a stud with two lugs, a helical cam draw, a motor close and release, gendered | **M** - read: one rotational DOF per segment module. Shared in kind: one revolute joint per module. Differs: cand-d plus or minus 15 degrees by sector gear, bends in the table plane only, vs a full-range joint | **M** - read: chain reconfiguration by docking with IR guidance. Shared in kind: chains. Differs: cand-d is chain only, no reconfiguration claim, no IR | N | https://modlab.engineering.upenn.edu/publications/asme.pdf ; ICRA 2000 (corpus) |
| C13 SuperBot | L - boxy segments; module paper not read | L - read SINGO: genderless chuck of four jaws; no unpowered-hold statement found. Shared: a motor-driven latch. Differs a lot | L - three DOF | L | N | https://robots.isi.edu/prl/shen2009SINGO.pdf |
| C14 CKBot | L - 60 mm cube modules, U-bar and L7, vs an elongated two-box | L - read: modules join with M3 screws by hand; no coupler shared | **M** - read: servo-driven module with "one rotational degree of freedom" in a chain. Shared in kind: one servo-like revolute joint per chain module. Differs: cand-d has a geared sector joint inside the shell with plus or minus 15 degrees; CKBot's servo turns the module at the connector | L - manual reconfiguration of chains | N | https://www.modlabupenn.org/ckbot/ |
| C15 Soldercubes | L | L | L | L | N | DOI 10.1007/s10514-015-9441-4 |
| C16 FreeBOT | N | L | L | L | N | https://freeformrobotics.org/wp-content/uploads/2022/02/IROS20_0857_FI.pdf |
| C17 HyMod | L - ball-joint cube unit | **M** - read (HiGen): "four hooks placed radially", motor with a "298:1 gearbox", "maintain a connection even when power is removed"; genderless. Shared in kind: a motor-driven latch with an unpowered hold, with gear friction. Differs: four radial hooks translating in and out, genderless hook-to-hook vs a gendered stud and cam sleeve; no helical slot | L - three DOF, in-place rotation | L - lattice, chain, mobile hybrid | N | DOI 10.1007/978-3-319-73008-0_28 ; https://sheffield.ac.uk/media/22956/download |
| C18 Telecube | N | L - switching magnets | N | L | N | https://researchr.org/publication/SuhHY02 |
| C19 Crystalline | L | L - latches | L | L | N | DOI 10.1023/A:1026504804984 |
| C20 PolyPod | L - segment and node chain; not verified, capped | L - not verified | L | L | N | https://www.mit.edu/people/manoli/polypod/polypod.html |
| C21 Swarm-bot | N | L - gripper and ring | N | L | N | DOI 10.1023/B:AURO.0000033972.50769.1c |
| C22 Sambot | L - cuboid | L - active docking face | N - wheels | L | N | DOI 10.1109/TMECH.2010.2085009 |
| C23 Blinky Blocks | N | L - magnets | N | L | N | DOI 10.1145/1979742.1979712 |

### 4.3 Commercial kits (explicit reasons)

| Ref | D1 | D2 | D3 | D4 | D5 | Source |
| --- | --- | --- | --- | --- | --- | --- |
| D1 Cubelets | L - small solid blocks; only "compact body" shared | L - magnetic snap vs a motor-turned mechanical cam; only "has an attachment" shared | N - fixed-function blocks | L - hand-assembled; generic | N - bright colour-coded plastic cubes vs declared white PA12 and bare steel | https://modrobotics.com/about-us (corpus) |
| D2 MOSS | L | L - magnets | L - motorised joint modules, generic | L | N | https://forums.parallax.com/discussion/151259/moss-brand-new-robot-construction-system-from-modular-robotics (corpus, secondary) |
| D3 UBTech Jimu | N | L - interlocking parts | L - servos | L | N | https://www.pcworld.com/article/419049/ubtech-looks-to-up-its-toy-robot-game-with-the-jimu.html (corpus, secondary) |
| D4 LEGO EV3 | N | L - studs and pins | L - motors on a brick | L | N | https://www.lego.com/en-us/product/31313 (corpus) |

### 4.4 Q64 additions (Q64-C21..C29)

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| Q64-C21 CONRO | **M** - read: a module of "a passive connector ... a motor housing ... an active connector", 10 cm, 100 g. Shared in kind: an elongated inline module with a pin end and a receptacle end (gendered ends) and an actuator body between. Differs: cand-d's body is two shell segments with a hinge gap, 47.2 mm site to site, head cartridge and tail stud, and its joint is inside the body, not a motor housing between connectors | **M** - read: "the latch engages groves on the pins"; SMA release; spring close; unpowered hold. Shared in kind: gendered pin-in-receptacle docking with an unpowered hold. Differs: no SMA, no spring-closed latch, no groove on the pin; a lug stud drawn by a motor-turned helical cam; powered close and release; torque-stop seat | **M** - read: pitch and yaw servos in chain locomotion. Shared in kind: servo-driven revolute joints inline in a chain. Differs: one joint, plus or minus 15 degrees, geared sector, no chain locomotion claim | L - capped; Shen 2001 not read; CONRO's reconfiguration is not shown by the hardware page | N | https://robots.isi.edu/conro/proto2H.html |
| Q64-C22 HEXEL | L - hexagonal exoskeleton; paper unread | L | L | L | L | DOI 10.1126/scirobotics.adl3546 (not read) |
| Q64-C23 Hinged Pixels | N - hexagon modules vs elongated boxes | N - theory | N - hexagon pivots about a shared vertex; cand-d has a hinge between its own segments | L | N | https://erikdemaine.org/papers/HingedPixels_SoCG2021/paper.pdf (not re-read) |
| Q64-C24 rolling cylinders on hex lattice | N | L | N - rolling | L | N | https://hal.archives-ouvertes.fr/hal-02300456 |
| Q64-C25 PenduMorph | N - sphere | L - magnetic docking | N - pendulum | L | N | https://arxiv.org/pdf/2606.22491 |
| Q64-C26 Rotundus GroundBot | N | N | N | N | N | https://orionrobots.co.uk/wiki/rotundus |
| Q64-C27 Sphero / BB-8 | N | N | N | N | N | https://newatlas.com/sphero-bb-8-droid/39269/ |
| Q64-C28 MOPARAS | N | L | N | L | N | https://research.polyu.edu.hk/en/publications/moparas-a-modular-parallel-spherical-robot-with-position-adjustab/ |
| Q64-C29 pendulum-sphere literature | N | N | N | N | N | https://ar5iv.labs.arxiv.org/html/2302.08932 |

### 4.5 References added by this review (Y)

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| Y1 ModLock (Davey et al., IROS 2012) | L - flat connector plates, no body | **M** - read: four hook-headed screws pass through holes, "faces are twisted 12 deg to align and tighten", a locking dowel snaps into a groove. Shared in kind: a push-in then twist lock (bayonet class) on protruding hooks with a passive hold. Differs: manual, no motor; whole-module twist of 12 degrees vs a motor-turned sleeve with helical slots and a self-locking stage; a snap dowel vs friction self-locking | N - manual | L | N | https://www.modlabupenn.org/wp-content/uploads/ModLock.pdf |
| Y2 Zhang, Zhang, Gupta (Robotics 2017) | L | **M** - read: the male interface inserts along a slot and rotates into a layer, then "spring-backed to the position between two teeth". Shared in kind: insert then rotate to lock (bayonet class). Differs: rotation comes from the module joints, lock by spring-back into teeth, slotted layers vs a dedicated motor and helical cam with a 3 degree self-locking stage | L - docking driven by locomotion actuators | L - under-actuated chains | N | https://mdpi-res.com/d_attachment/robotics/robotics-06-00025/article_deploy/robotics-06-00025.pdf |
| Y3 RoFICoM (Mrazek and Barnat) | L - 50 mm round connector body in a lattice | **M** - read: "The motor rotates the clip, which then slides out of the body using pins driven by a helical slot in the body"; hooks slide under hooks in the mating clip; a skirt blocks mutual rotation. Shared in kind: a motor-turned ring moving along a helical slot to lock. Differs: the helical slot extends a hook ring (genderless, hook-to-hook) vs cand-d's cam sleeve drawing a lugged stud onto a flat seat; no self-locking 3 degree stage or torque-stop seat is described | N | L - lattice | N | https://rofi.fi.muni.cz/assets/files/publications/roficom.pdf |
| Y4 WPI twist-lock poster | L | **M** - read (poster, thin): "Gendered Twist-Lock Connector ... bayonet or quarter-turn mechanism". Shared in kind: a gendered bayonet or quarter-turn lock. Differs: nothing more is stated on actuation or hold, so the difference is cand-d's motor-driven helical cam with a 3 degree self-locking stage, torque-stop seat and capture stage | L | L | N | https://users.wpi.edu/~cxu5/docs/MSEFPoster.pdf |
| Y5 CoBoLD (Symbrion and Replicator) | L | L - capped. Secondary read: a geared locking wheel (worm wheel) with milled hooks grasps four cone bolts after insertion. A gear-driven rotating wheel locking inserted bolts is a close kind. Primary not obtained. See s5 risk note | L | L | N | DOI 10.1109/ROBIO.2011.6181589 (record only); UCT thesis (secondary) |
| Y6 RIMRES latch (Sherpa and CREX) | L | L - secondary read: two braces driven by a spindle drive hold the modules with no energy; gendered | L | L | N | UCT thesis (secondary) |
| Y7 LaMMos | N | L - read: a motorized screw into a T-slot nut; links, not modules | N | N | N | https://arxiv.org/pdf/1801.00035 |
| Y8 Latching X-Face / DRAGON | L | L - read: a passive compliant latch with no actuator; DRAGON is a passive latch | N | L | N | https://www.modlabupenn.org/wp-content/uploads/latching_xface_overlay.pdf |
| Y9 Truss Link and VTT (Wyder et al.) | N - truss members | L - read: magnet spheres (Truss Link); a servo latch and rack and pinion (VTT) | N | L | N | https://arxiv.org/pdf/2508.01829 |
| Y10 MODUR | L | L - hermaphrodite connector; summary only | L | L | N | https://arxiv.org/html/2510.13356 (not read) |
| Y11 Cam-shaft tool changer | N | L - summary only: a servo turns a cam shaft 0 to 60 degrees to push a lock-pin; manipulator tool changer, not a module coupler | N | N | N | https://arxiv.org/pdf/2603.04760 (summary only; PDF too large) |

Counts. High cells against F1 or F2 (A1, B1-B4): 0. High cells in total: 0. Moderate cells: 15 (listed in s0).

## 5. Differentiation notes (Q61 s3 items 3 and 4)

There is no high cell, so there is no item-4 note. Each moderate cell has a note below. "Kept" means a feature that is forced by Family B or by the task.

**PolyBot (D1, D2, D3, D4).** This is the reference with the most moderate cells (four) and it needs the closest watch. A fifth moderate or a single high would not by itself fail (rule 2 needs two highs), but a second high would.
- D1. Shared: a rectangular two-port body with one joint between the ports. Kept: this is the Family B definition, not a design choice. Differs: aspect (about 1.9 to 1 and a long head against a short tail, vs a cube-like module with matching halves), gendered ends vs hermaphroditic plates, and coupler axis offset from the body axis. The segment-and-joint idea is not specific to PolyBot (CKBot, M-TRAN and CONRO share it). I rated this M, not H, because cand-d's proportions, asymmetric segment lengths and gendered stud-and-cartridge ends would not be called "the same design" by an informed observer.
- D2. Shared: a pin-like part entering a hole, locked by turning a part about the interface axis, no power to hold. Differs: SMA wires and spring, grooved pins and a four-leg latch plate vs a lug stud, helical cam sleeve, motor close and release, and a self-locking stage.
- D3. Shared: one revolute joint per module. Differs: plus or minus 15 degrees, geared sector, not a full-range hinge.
- D4. Shared: chains. Differs: no reconfiguration or IR claim; chain only. Kept: chain-native is Family B.

**CONRO (D1, D2, D3).**
- D1. Shared: elongated, gendered ends, actuator in the middle. Differs: two shell segments with an inside-the-body hinge, not connector-motor-connector housing. Kept: gendered inline ends (a stud end and a cartridge end) are a choice of cand-d. I flag this as a point the author may wish to revisit if later reviews raise it.
- D2. Shared: gendered pin-in-receptacle docking with an unpowered hold. Differs: no SMA, no spring-closed default, no groove on the pin, powered close by torque stop. This is the cell that cand-b's review rated H, for SMA release plus spring-closed latch. cand-d removes both on purpose (dossier s1 item 5), so H is not supported here.
- D3. Shared: servo-driven revolute joints inline. Differs: one joint, small range.

**ATRON D2, HyMod D2, Roombots D2.** All three are "motor-driven latch, unpowered hold". Differs: ATRON uses hooks on pivoting arms and a lead screw; HiGen uses radial hooks and a 298:1 gearbox; Roombots uses a crank to a geometric singularity. cand-d uses lugs on helical cam slots and a friction self-locking stage (2.86x dry, 1.91x oiled, not geometric). Kept: the non-backdrivable hold class (it is how G6 passive retention can be met). Not shared: the four-bar over-centre of the cand-a line (Roombots, H on cand-a), SMA and spring (PolyBot, CONRO), magnets.

**CKBot D3.** Shared: a servo-class revolute joint in a chain module. Differs: sector-gear geared joint with plus or minus 15 degrees inside a shell; the CKBot servo turns the whole module end. Kept: Family B.

**ModLock D2, Zhang D2, WPI poster D2 (bayonet class).** This is the class the task asked me to search for. Shared in kind: push in, turn, lock. Differs in each case:
- ModLock is manual with whole-module twist and a snap dowel.
- Zhang uses the modules' own joints to rotate and a spring-back into teeth.
- The WPI poster gives no further details.
- cand-d uses a dedicated motor, a bronze sleeve with a capture stage and a 3 degree lock stage, a torque-stop seat that absorbs the axial tolerance stack, and passive retention by friction self-locking.
The twist-lock class is a generic machine element (bayonet mounts). The novelty claim is not in the class, and the dossier does not claim it.

**RoFICoM D2.** Shared: motor-turned ring and a helical slot. Differs: RoFICoM's helical slot extends a hook ring against a mating hook ring (genderless); cand-d's draws a stud onto a seat. cand-d's lock stage self-locks by lead angle; RoFICoM's hold is by hooks plus skirts, and no self-locking lead is described. This is the nearest published use of "helical slot plus motor plus ring", so a later reviewer should re-read it in the full paper if the coupler changes.

**Risk notes on capped cells (not ratings).**
- CoBoLD D2 (Y5): if the primary paper confirms a motor-driven worm-gear locking wheel with milled hooks that grasp bolts on insertion, a reviewer could rate it M. The differentiation would be: four cone bolts and hooks vs a two-lug stud on helical cam slots; genderless vs gendered; the wheel locks by hook shape vs a drawn flange on a flat seat. It could not make a high without a second feature shared in specific form.
- M-TRAN D1 and D3: the two-box body with a joint is the Family B shape. A confirmed M would need a note: one joint vs two, gendered stud ends vs gendered hook faces, no magnets.

## 6. Exclusion checks (Q62 s3, recorded for G8)

1. **Cube with an internal flywheel (the M-Blocks lineage): not present.** The body is a 47.2 x 25.4 x 24 mm elongated two-segment prism, not a cube. The component list (32 entries; kinds structure, energy_source, controller, actuator, coupler_mechanism, other) has no flywheel, no brake and no inertial actuator. Motion is by a geared joint, not impulse.
2. **Needle- or particle-like silhouette: not present.** Site-to-site pitch 47.2 mm, cross-section 25.4 x 24 mm, aspect about 1.9 to 1 (elongation 1.8 to 2.0). That is a tabletop block, not a needle (high aspect ratio, thin), and not a sub-visible or dust-like particle. The stowed enclosing sphere is 58.862 mm. Design guidance s4.1's forbidden direction is not approached.

## 7. Family membership check (Q62 s3, Family B)

Constraint: "An elongated two-segment body with one internal revolute joint, so it is chain-native, with couplers at the segment ends."
- Two segments: head (33.8 mm, x 1.8 to 35.6) and tail (8.8 mm, x -10.6 to -1.8), separated by a 3.6 mm hinge gap. Yes.
- One internal revolute joint: one vertical pin at the origin, driven by a sector gear. Declaration lists one joint. Yes.
- Elongated: aspect about 1.9 to 1 along the chain. Yes, though modestly. The tail segment is short (8.8 mm), so the "two segments" are very unequal; this is allowed by the family text.
- Couplers at the segment ends: head coupler site at x 35.6 (head end face), tail coupler site at x -11.6 (tail end face). Yes. Two sites in all, one per segment end.
- Chain-native: chain geometry is declared inline with `mating_roll_deg [0]`.
- Result: cand-d is a member of Family B. The declaration's `family` field is "B". The reviewer found no violation of the family constraint.
- Not tested here: that the joint bends a chain adequately (Q31; the dossier says unresolved). Family membership is about structure, not function.

## 8. Fail-rule evaluation

- Rule 1 (any F1 cell high): none. A1 is rated N in every column. Not triggered.
- Rule 2 (two or more highs against one reference): there are no highs against any reference. Not triggered. The nearest are PolyBot (four M) and CONRO (three M).
- Item 3 (every moderate has a differentiation note): done in s5 for all 15 moderate cells.
- Item 4 (every single high has a note and is listed prominently): there are no highs.
- Item 5 (both exclusions checked and recorded): done in s6.
- G8 (Q62): no high cell against F1 or F2, both exclusions "not present". Satisfied.
- Completeness: every cell of the matrix has a rating, a reason (short for L and N cells, per the cell convention) and a source in its row. Capped cells are marked as capped.
- Independence: reviewer is a different agent session with no authorship in cand-d (Q61 s4).

## 9. Changes recommended

No change is required for this review to pass. These are advice only. Any declaration change changes the hash and needs a new review (Q61 s5).
1. Author or owner: decide whether the gendered inline-end layout (stud on the tail, cartridge on the head) is a deliberate difference from CONRO. It is the one structural feature that raises CONRO D1 to moderate. Keep it if it is needed for the coupler.
2. Reviewer follow-up (r2, optional): obtain primary papers for M-TRAN (I to III), CoBoLD (Liedke and Woern 2011), CKBot's module paper and CONRO's docking paper (Shen 2001), and confirm or revise the capped cells. If the full text of RoFICoM shows a self-locking helical lead, re-rate D2 against it.
3. Corpus (owner or lead, by a decision record): add Y1 to Y11 (at least ModLock, Zhang et al., RoFICoM, the WPI twist-lock poster and CoBoLD) as appended entries. This review does not edit the corpus.
4. Final visuals (Q61 s7): D5 is rated only on the declared materials. It must be reviewed again when geometry and visuals exist.
5. The dossier says "bayonet and breech-lock mounts: generic machine elements". Keep that wording out of any claim of novelty. The review found published modular-robot twist-locks (ModLock, Zhang et al., a WPI prototype), so the class is not new in this field.

## 10. Outcome

**pass.** No F1 high, no reference with two highs, every moderate noted, both exclusions "not present", Family B membership holds, the declaration hash matches. Pass means no Q61 fail rule was triggered by the references examined, with the capped cells listed in s1. It is not a claim of absolute originality. This review reduces copying risk and does not claim absolute originality.
