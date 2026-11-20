# Originality review (Q61, stage gate1): cand-d v2, r1

candidate_id: cand-d
candidate_version: 2
declaration_sha256: 659810c455376de8c3450d42556f266e3c37ed6260f235a3676dec22725cc0cf
stage: gate1
author: Claude Opus 5.5 (engineering lead, cand-d author)
reviewer: reviewer-d2-originality (Claude Sonnet 5.5, independent session, no authorship in cand-d)
high_cells_f1_f2: 0
exclusion_cube_with_internal_flywheel: not_present
exclusion_needle_or_particle_silhouette: not_present
outcome: pass

Date: 2026-11-20. This review reduces copying risk and does not claim absolute originality.

## 0. Summary

- Result: **pass** under Q61 s3. No cell against F1 (A1) or F2 (B1-B4) is high. No reference has two high cells. There is no high cell at all. Both Q62 exclusions are not present. Every moderate cell has a differentiation note (s5).
- **High cells (Q61 s3 item 4): none.** I looked for one in the new Hirth face pair. The closest calls are Beckhoff's Hirth-plus-screw-ring arm connector (Y12) and Belke and Paik's toothed coupling (Y14, primary not obtained). Both are held at moderate for the reasons in s5.
- **Moderate cells (20):** C4 ATRON D2; C6 Roombots D2; C12 PolyBot D1, D2, D3, D4; C14 CKBot D3; C17 HyMod D2; Q64-C21 CONRO D1, D2, D3; Y1 ModLock D2; Y2 Zhang D2; Y3 RoFICoM D2; Y4 WPI poster D2; **new in this review:** Y12 Beckhoff arm module D2; Y13 Xerox PolyBot toy patent D2; Y14 Belke and Paik D2 (capped); Y15 PetLock D2; Y16 Reach Robotics patent D2.
- **What v2 changes for originality.** The 36-tooth Hirth face pair is a known machine element. It is used in a modular robot arm connector (Beckhoff, 4 teeth, hand-screwed ring, a tooth-count and drive difference) and a similar toothed face is described for a modular robot coupling (Belke and Paik, unread). A toothed face for rotational positions also appears in the PolyBot toy patent (8 teeth). None is a self-reconfigurable-module coupler that combines a Hirth pair with a motor-turned helical-slot cam sleeve, a self-locking lock stage and a stop pin. The combination is not found, but each part is known. Search results show closest art only.
- **Caps.** Belke and Paik (full text), M-TRAN I to III, CoBoLD, CKBot module paper, PolyPod, iBOSS iSSI and Shen 2001 were not obtained. See s1. Pass means only that no fail rule was triggered by the references examined.

## 1. Basis, limits and primary sources

**What was compared.** `candidates/cand-d/declaration.json` (v2) and `candidates/cand-d/dossier-v2.md`.
- SHA-256 from `shasum -a 256 candidates/cand-d/declaration.json`: `659810c455376de8c3450d42556f266e3c37ed6260f235a3676dec22725cc0cf`. It equals the expected value, so the outcome is not forced to unresolved.
- Dossier-v2 section 8 (author self-check) was read as a list of points to examine only. It says the Hirth pair may raise D2 if a reference uses face serrations on a connector. I searched for that specifically (s2). It was **not** used as a rating.
- The v1 review (`originality-review-gate1-v1-r1.md`) was used as a pointer list (Y1-Y11) and as context. Every cell here was rated afresh against v2. I re-read primary sources for every moderate cell where the source was obtainable.

**What v2 is, as declared (used for every cell).**
- Body, joint, electronics: unchanged from v1. Head segment (PA12 SLS shell, 33.8 mm long) and tail segment (8.8 mm), 25.4 x 24 mm section, 3.6 mm hinge gap, 47.2 mm site to site. One vertical revolute joint, pin dia 2 at mid-gap, spur sector driven by a 6 mm gearmotor, working range +-15 deg. Declared stowed enclosing sphere 58.862 mm (dossier; not recomputed here).
- Coupler (rigid, gendered, changed in v2): a one-piece 304 tail stud with a flange carrying a **36-tooth 90 deg Hirth ring** (r 2.6 to 6.3), an entry pilot (dia 4) and two dia 3 lugs. A head cartridge: 304 housing with a Hirth-toothed lip, axial lug slots, a **stop pin** and **two tapped mounting ears**; a C93200 bronze cam sleeve with two helical slots (20 deg capture stage, 3 deg self-locking stage) and a stop arc groove; a PTFE thrust ring; a 304 **retainer collar**. A 6 mm gearmotor turns the sleeve to a 1.0 V stall. This seats the Hirth faces under 4.41 to 9.00 N preload. Torsion and shear go through the Hirth teeth with zero lash. Hold is passive (friction self-locking, `friction_wedge`).
- No SMA, no spring, no magnet. BLE only. No power transfer.
- Declared materials: PA12 SLS shell (PA2200 white), 304, C93200, PTFE. No stated colour scheme, markings or finish beyond that.

**Primary sources read in this session (all fetched or opened 2026-11-20; PDFs converted with pdftotext and searched).**
- **Beckhoff, US 12,290,920 B2, "Arm module for a modular robot arm of an industrial robot"** (Google Patents full text, https://patents.google.com/patent/US12290920B2/en). Read: "a first face gearing 302 having four teeth, which is embodied as a Hirth joint"; "a fastening ring 401 with an internal thread"; "By twisting the fastening ring 401, the internal thread is screwed onto the external thread 301, pressing the second connection device 40 onto the first connection device 30. In the pressed-on state, the first face gearing 302 and the second face gearing 402 engage with each other in such a way that the first connection device 30 and the second connection device 40 are mechanically connected to each other in a torque-locking manner"; a centering pin and receptacle; the module has a motor unit for the arm joint.
- **Xerox, US 6,605,914 B2, "Robotic toy modular system"** (Google Patents full text, https://patents.google.com/patent/US6605914B2/en). Read: "Each connector plate includes connector teeth 30 allowing for positioning of the module relative to its adjacent module"; "eight teeth allow eight rotational positions of the module relative to its adjacent module; six teeth would allow six positions"; claim: "connector teeth having a profile suitable for locking an attaching robotic module into position". The module has "an actuator connected to a pivot mechanism".
- **PolyBot G2:** Yim et al., https://modlab.engineering.upenn.edu/publications/asme.pdf. Read: segment modules are "nominally rectangular prisms and have one rotational degree of freedom separating two connection ports"; latch plate "rotates about the center of the interface as seen in Figure 3. Its four legs reach out and around the grooves"; "150 micron shape memory alloy (SMA) wire"; "a return spring"; hermaphroditic interface plates about 50 x 50 mm.
- **CONRO:** https://robots.isi.edu/conro/proto2H.html (page text fetched). Read: "a passive connector that has pins ... a motor housing ... an active connector"; "the latch engages groves on the pins and secure them. To release the pins, a SMA wire is contracted pulling the latch back"; "a spring brings the latch back to the close position"; "10 cm long ... weighs 100 grams"; yaw and pitch motors.
- **ATRON:** Ostergaard et al., Autonomous Robots 21 (2006), https://sccn.ucsd.edu/download/robot.pdf. Read: "The three hooks are driven by a DC motor via a lead screw. The mechanism driving the arms is not backdrivable in the extended arm position".
- **Roombots:** Sprowitz et al. (2014), https://documents.epfl.ch/groups/e/ep/epflmedia/www/20140520_Roombots/roombots%20publication.pdf. Read: the crank and slider "pushes the latch into an externally non-reversible singularity position"; the connected state needs no power.
- **HiGen (HyMod):** Parrott, Dodd, Gross, https://sheffield.ac.uk/media/22956/download. Read: genderless, four radial hooks, 298:1 gearbox, holds when power is removed.
- **RoFICoM:** Mrazek and Barnat, https://rofi.fi.muni.cz/assets/files/publications/roficom.pdf. Read: "there are four hooks attached to a ring (named clip). The motor rotates the clip, which then slides out of the body using pins driven by a helical slot in the body. The hooks slide under hooks in the mating clip"; a "skirt" blocks rotation; 50 mm diameter.
- **ModLock:** Davey et al., IROS 2012, https://www.modlabupenn.org/wp-content/uploads/ModLock.pdf. Read: "The faces are twisted 12 deg to align and tighten the connection"; "a stainless steel locking dowel on a compliant lever snaps into a lock groove to prevent the faces from untwisting"; manual, no motor. (Its "five teeth" are in the end-effector guide, not on the connector face.)
- **Zhang, Zhang, Gupta, Robotics 6(2):25 (2017),** https://mdpi-res.com/d_attachment/robotics/robotics-06-00025/article_deploy/robotics-06-00025.pdf. Read: "When a male interface is pushed along Slot 2 and rotated, it will be spring-backed to the position between two teeth, and the two modules are locked".
- **MODUR:** Gu et al., https://arxiv.org/pdf/2510.13356. Read: "a screw-in hook mechanism with a resolution of 90"; a lead-screw motor moves the hook, then "the motor switches to generate rotational motion, thereby locking the hooks together"; "the motors ... continuing to provide thrust and preventing the hooks from rotating in the opposite direction through friction".
- **Tool changer:** arXiv 2603.04760, https://arxiv.org/pdf/2603.04760. Read: servo, cam and lock-pin; "the cam pulls the lock-pin inward; ... in the locked state, the cam rotates in the opposite direction and pushes the lock-pin outward".
- **PetLock:** Li et al., https://arxiv.org/pdf/2209.04307. Read: "driven by the electric push rod, Pyramid moves axially, pushes the locking pins to move radially"; "The locking mechanism and the electric push rod are both self-locking"; "So when mu > tan beta, the locking mechanism has the capability of self-locking ... beta = 5 deg".
- **Reach Robotics (Blueprint Lab), US 11,376,730 B2** (Google Patents text via fetch, https://patents.google.com/patent/US11376730B2/en). Read: "a plurality of protrusions arranged in an annular array and extending from the flange"; "A locking nut is arranged about, and threadedly engaged with, the male connector" to urge frictional engagement.
- **KIST, US 10,160,121 B2** (Google Patents text via fetch, https://patents.google.com/patent/US10160121B2/en). Read: "The fixing ring ... may be simultaneously engaged and screwed to the wing thread of the fixing wing"; genderless; couples at 0, 90, 180, 270 deg.
- **US 8,234,950 (SINGO patent)** and **US 9,616,948 (Ben-Tzvi docking)**, Google Patents text via fetch. Read: four sliding jaws on a motorized circular gear (8,234,950); a T-mech shaft with a hex neck and C-mech clamps on a non-back-drivable lead screw (9,616,948).
- Also opened (lower ratings): SINGO paper (https://robots.isi.edu/prl/shen2009SINGO.pdf), Latching X-Face (https://www.modlabupenn.org/wp-content/uploads/latching_xface_overlay.pdf), X-Face (https://www.modlabupenn.org/wp-content/uploads/X-Face.pdf; chamfered pins and grooves, no serrations), SIROM paper (https://www-live.dfki.de/fileadmin/user_upload/import/10026_SIROM-IAC.pdf; no mechanism text on the interface), UCT survey thesis (https://open.uct.ac.za/bitstreams/5dcc9290-b036-4687-b908-3ca62889beac/download).

**Not obtained (cells capped, and the cap is marked in the matrix).**
- **Belke and Paik, "Automatic Couplings with Mechanical Overload Protection for Modular Robots", IEEE/ASME Trans. Mechatronics 2019, DOI 10.1109/TMECH.2019.2907802.** The IEEE PDF returned HTTP 418, the EPFL record (https://infoscience.epfl.ch/record/265187) holds the abstract only (checked through its API: only a licence bundle, no full text). The abstract was read: "genderless coupling ... disengages two modules at a pre-defined torque threshold ... compact cylindrical space". The statement that the coupling has "radial teeth on the front face, with similarities to Hirth joint teeth but with altered design and varied face angles along the radius" came from a **search-engine summary** of the IEEE PDF, not from text I read. I cannot quote it. Y14 D2 is **capped at moderate**, and a reader with the paper should re-rate it (s9 item 2).
- M-TRAN I to III (C1-C3): no primary papers. D1 to D4 capped at low (as in v1).
- CoBoLD (Y5): primary not obtained (secondary thesis only). D2 capped at low (as in v1). Risk note in s5.
- CKBot module paper (C14), PolyPod (C20), Shen 2001 (CONRO docking): not obtained. CKBot D3 rests on the project page read in v1 (https://www.modlabupenn.org/ckbot/, search-confirmed this session, not re-read), so it is flagged "v1 read".
- iBOSS iSSI (bayonet plug-and-turn, seen in a search summary only) and the DFKI "Multifunctional interconnect" paper (fetch failed): capped low (Y17).
- Q64-C22 to Q64-C29 and the section-C rows not listed above: rated from corpus descriptors, which place them far from a two-segment inline body. Fictional entries have no engineering source and are rated from the corpus descriptors.

## 2. Search record

Date: 2026-11-20. Tool: web search (standard and one extended query) plus fetch of the sources in s1.

Terms, in order, and what each returned:
1. "modular self-reconfigurable robot connector Hirth coupling face serration toothed face docking". Returned X-Face, HiGen, SINGO patent, EP-Face, Zhang, UCT thesis. No Hirth-faced module found here.
2. "modular robot docking interface serrated teeth face dog clutch torque transmission self-reconfigurable". Returned Zhang (teeth in the female layer), Ben-Tzvi patents, tool changer (arXiv 2603.04760). Added Y2 (re-read), Y11.
3. "curvic coupling modular robot module connector radial teeth alignment". Returned the Hirth and curvic background (Wikipedia, patents), the **Xerox PolyBot toy patent (connector teeth)**, Reach Robotics, KIST. Added Y13, Y16, Y18.
4. "modular robot connector face gear OR face teeth OR toothed face OR serrated ... self-reconfiguring". Returned X-Face, HiGen, SINGO patent, MODUR. No serrated face found beyond Y13.
5. "Hirth coupling robot joint module quick-change connector toothed face preload lock robotic modular". Returned **Beckhoff US 12,290,920 and 12,285,860** (Hirth with screw ring), CN110561486A (conical surface joint flange; read, no teeth: conical fit with screws), US 12,703,109 (quick change interface, record only). Added Y12 and Y19.
6. "RoFICoM ModLock bayonet rotating collar cam sleeve connector modular robot twist lock docking 2024 2025". Returned RoFICoM, ModLock, bayonet patents, the Reach patent. Re-read RoFICoM and ModLock.
7. "self-reconfigurable modular robot genderless connector Hirth OR face spline OR radial teeth mechanical docking interface paper" (extended). Returned HiGen, SINGO, **Belke and Paik (teeth similar to Hirth, summary only)**, SMORES-EP arXiv 2104.00800 (EPM faces, not read), coupling-mechanism review papers (records only). Added Y14.
8. "modular robot module connector motor-driven rotating ring bayonet lug cam slot helical locking coupling paper (not RoFICoM)". Returned the tool changer, MODUR, a self-locking bayonet patent (US 6,226,068, record only). Re-read MODUR and tool changer.
9. "Automatic Couplings With Mechanical Overload Protection for Modular Robots" and a second query on Belke and Paik teeth. Returned EPFL records only (see s1).
10. "on-orbit modular reconfigurable robot docking interface Hirth teeth bayonet rotating ring SIROM iBOSS" . Returned iBOSS iSSI (bayonet), SIROM, PetLock, DFKI interconnect, a US androgynous coupling patent (10,279,933, record only). Added Y15, Y17.
11. "modular robot coupling serrated OR toothed face-to-face connectors zero backlash ... Hirth teeth coupling Franka OR Schunk OR Kinova". Returned Beckhoff again, serrated tooling patents (not robots), Wikipedia Hirth joint.

Findings. A Hirth or serrated face is used on connectors of **modular robot arms** (Beckhoff) and as indexing teeth on a **PolyBot-lineage toy module** (Xerox), and is reported for one self-reconfigurable coupling (Belke and Paik, unread). I found no published self-reconfigurable module whose coupler combines a fine Hirth pair (36 teeth) with a motor-turned helical-slot sleeve that draws a lugged stud to a self-locking stage and a torque-stop seat. Search results are not proof of absence.

F2 examined: Replicators (B1), Prey (B2), Borg and Star Trek nanites (B3), T-1000 (B4), from the corpus descriptors. No further fictional entries were searched.

## 3. References examined, by class

- F1: A1. F2: B1, B2, B3, B4.
- P (corpus): C1-C23 (C1-C3 M-TRAN, C4 ATRON, C5 SMORES-EP, C6 Roombots, C7-C8 M-Blocks, C9 Kilobot, C10 catoms, C11 Molecubes, C12 PolyBot, C13 SuperBot, C14 CKBot, C15 Soldercubes, C16 FreeBOT, C17 HyMod, C18 Telecube, C19 Crystalline, C20 PolyPod, C21 Swarm-bot, C22 Sambot, C23 Blinky Blocks) and Q64-C21 to Q64-C29 (Q65 identifiers).
- K: D1 Cubelets, D2 MOSS, D3 UBTech Jimu, D4 LEGO Mindstorms EV3. (No serrated or Hirth-type face found on any kit product in this search. Not product-searched beyond the corpus rows.)
- Extra references: **Y1-Y11 from v1** (ModLock, Zhang et al., RoFICoM, WPI poster, CoBoLD, RIMRES, LaMMos, Latching X-Face and DRAGON, Truss Link and VTT, MODUR, cam-shaft tool changer) and **new here:** Y12 Beckhoff arm module; Y13 Xerox PolyBot toy patent; Y14 Belke and Paik coupling; Y15 PetLock; Y16 Reach Robotics modular system patent; Y17 iBOSS iSSI and SIROM; Y18 KIST module connection system; Y19 CN110561486A modular joint quick connection.

## 4. Similarity matrix

Key: N none, L low, M moderate, H high. D1 silhouette and geometry, D2 coupler concept, D3 actuation and locomotion logic, D4 assembly and reconfiguration, D5 visual identity.

**D5 note (declared only).** No final visuals exist. D5 is rated **on what the declaration states only**: white PA12 SLS shell (PA2200 white), exposed 304 steel and bronze coupler parts including a visible toothed ring on each coupler face, no stated colour scheme, markings or finish. A D5 "none" is not a clearance of the final look. D5 must be re-rated at final visuals (Q61 s7).

**Cell convention.** A bare N or L means the reference shares nothing (N) or only generic features forced by the task or by physics (L). The reason is a short form of the corpus descriptor or of what I read. Every M cell has a full reason and the source I read (or the cap stated). Access date 2026-11-20 for pages read in this session, 2026-11-04 for corpus-only sources.

### 4.1 Forbidden and fictional

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| A1 BH6 microbots (F1) | N - one 47 mm two-segment unit vs thousands of near-identical small dark units | N - rigid steel stud, bronze cam sleeve and Hirth faces vs magnetic legs; cand-d has no magnet | N - one geared joint vs crowd-surfing | N - a chain of identical units vs arbitrary shapes | N - declared pale PA12 and bare steel vs a dark liquid-like swarm | https://gizmodo.com/how-disney-will-make-you-cry-again-with-big-hero-6-1630115219 ; https://awn.com/animationworld/don-hall-and-chris-williams-talk-disneys-big-hero-6 (corpus, secondary) |
| B1 Replicators (F2) | N - elongated two-segment body vs insect-like blocks | N | N | L - both join identical units | N | https://en.wikipedia.org/wiki/Nanotechnology_in_fiction (corpus, secondary) |
| B2 Prey (F2) | N | N | N | N | N | same |
| B3 Borg nanites (F2) | N | N | N | N | N | same |
| B4 T-1000 (F2) | N | N | N | N | N | same |

### 4.2 Published robots, section C

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| C1 M-TRAN I | L - two box halves; primary unread, capped | L - magnets vs mechanical; capped | L - two joints vs one; capped | L - capped | N | DOI 10.1109/TMECH.2002.806220 |
| C2 M-TRAN II | L - capped | L - capped | L - capped | L - capped | N | corpus record (bib-bvb) |
| C3 M-TRAN III | L - capped | L - capped. Secondary only (UCT thesis): motor, hooks, holds without power | L - capped | L - capped | N | DOI 10.1177/0278364907085560 ; UCT thesis (secondary) |
| C4 ATRON | L - two hemispheres vs boxes | **M** - read: "The three hooks are driven by a DC motor via a lead screw. The mechanism driving the arms is not backdrivable in the extended arm position". Shared in kind: motor latch held unpowered by a non-backdrivable screw. Differs: hooks on arms gripping bars vs lugs on helical slots and a Hirth seat | L - one equatorial infinite-revolute joint | L - lattice vs chain | N | https://sccn.ucsd.edu/download/robot.pdf (s4.4) |
| C5 SMORES-EP | L | L - electro-permanent magnets; paper arXiv 2104.00800 not read | L | L | N | DOI 10.1126/scirobotics.aat4983 |
| C6 Roombots | L - paired spheres | **M** - read: the crank and slider "pushes the latch into an externally non-reversible singularity position". Shared in kind: motor latch, unpowered non-reversible hold. Differs: geometric over-centre singularity vs friction self-locking helical stage and a toothed seat | L - three DOF | L - 3D reconfiguration | N | DOI 10.1016/j.robot.2013.08.011 ; EPFL PDF |
| C7 M-Blocks | N - cube | N - magnets | N - flywheel | N | N | DOI 10.1109/IROS.2013.6696971 |
| C8 3D M-Blocks | N | N | N | N | N | DOI 10.1109/ICRA.2015.7139450 |
| C9 Kilobot | N | N | N | N | N | DOI 10.1109/ICRA.2012.6224638 |
| C10 catoms | L | L | L | L | N | DOI 10.1109/MC.2005.198 |
| C11 Molecubes | L | L - electromagnets | L | L | N | DOI 10.1038/435163a |
| C12 PolyBot | **M** - read: segments "nominally rectangular prisms and have one rotational degree of freedom separating two connection ports". Shared in kind: prismatic two-port body, one joint between the ports. Differs: about 50 x 50 mm symmetric halves with hermaphroditic plates vs 47.2 x 25.4 x 24 mm, a 33.8 mm head and 8.8 mm tail, gendered ends | **M** - read: grooved pins, a latch plate that "rotates about the center of the interface" with "four legs" around the grooves, SMA and return spring, no-power hold. Shared in kind: pin-in-hole docking, rotation about the interface axis, unpowered hold. Differs: SMA, spring, four-leg plate vs lug stud, motor-turned helical sleeve, Hirth seat. (The PolyBot-lineage toy patent is rated separately as Y13) | **M** - read: one rotational DOF per segment module. Differs: +-15 deg sector joint vs full-range hinge | **M** - read: chain reconfiguration by docking. Differs: cand-d claims chain only, no reconfiguration | N | https://modlab.engineering.upenn.edu/publications/asme.pdf |
| C13 SuperBot | L - boxy segments; module paper unread | L - read SINGO (paper and patent): four sliding jaws on a motorized circular gear, genderless; no Hirth or toothed face | L | L | N | https://robots.isi.edu/prl/shen2009SINGO.pdf ; US 8,234,950 |
| C14 CKBot | L - 60 mm cube modules | L - manual M3 screws (v1 read) | **M** - v1 read of project page: a servo module with "one rotational degree of freedom" in a chain; not re-read this session (project page only; module paper not obtained). Differs: cand-d has a sector-geared +-15 deg joint inside the shell | L | N | https://www.modlabupenn.org/ckbot/ |
| C15 Soldercubes | L | L | L | L | N | DOI 10.1007/s10514-015-9441-4 |
| C16 FreeBOT | N | L | L | L | N | https://freeformrobotics.org/wp-content/uploads/2022/02/IROS20_0857_FI.pdf |
| C17 HyMod | L | **M** - read (HiGen): four radial hooks, 298:1 gearbox, holds when power is removed, genderless. Shared in kind: motor latch with an unpowered hold. Differs: translating radial hooks hook-to-hook vs gendered lugs on a helical cam and Hirth seat | L | L | N | DOI 10.1007/978-3-319-73008-0_28 ; https://sheffield.ac.uk/media/22956/download |
| C18 Telecube | N | L - switching magnets | N | L | N | https://researchr.org/publication/SuhHY02 |
| C19 Crystalline | L | L - latches | L | L | N | DOI 10.1023/A:1026504804984 |
| C20 PolyPod | L - capped | L - capped | L | L | N | https://www.mit.edu/people/manoli/polypod/polypod.html |
| C21 Swarm-bot | N | L - gripper and ring | N | L | N | DOI 10.1023/B:AURO.0000033972.50769.1c |
| C22 Sambot | L - cuboid | L - active docking face | N | L | N | DOI 10.1109/TMECH.2010.2085009 |
| C23 Blinky Blocks | N | L - magnets | N | L | N | DOI 10.1145/1979742.1979712 |

### 4.3 Commercial kits

| Ref | D1 | D2 | D3 | D4 | D5 | Source |
| --- | --- | --- | --- | --- | --- | --- |
| D1 Cubelets | L - small blocks | L - magnetic snap vs motor cam and toothed seat | N | L | N - bright plastic vs white PA12 and bare steel | https://modrobotics.com/about-us |
| D2 MOSS | L | L - magnets | L | L | N | https://forums.parallax.com/discussion/151259/moss-brand-new-robot-construction-system-from-modular-robotics |
| D3 UBTech Jimu | N | L - interlocking parts | L | L | N | https://www.pcworld.com/article/419049/ubtech-looks-to-up-its-toy-robot-game-with-the-jimu.html |
| D4 LEGO EV3 | N | L - studs and pins | L | L | N | https://www.lego.com/en-us/product/31313 |

### 4.4 Q64 additions (Q64-C21 to Q64-C29)

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| Q64-C21 CONRO | **M** - read: a module of "a passive connector that has pins ... a motor housing ... an active connector", 10 cm, 100 g. Shared in kind: an elongated inline module with a pin end and a receptacle end. Differs: cand-d's body is two shell segments with a hinge gap; its joint is inside the body, not a motor housing between connectors | **M** - read: "the latch engages groves on the pins ... a SMA wire is contracted pulling the latch back"; "a spring brings the latch back to the close position". Shared in kind: gendered pin-in-receptacle docking with an unpowered hold. Differs: no SMA, no spring, no groove on the pin; a lug stud drawn by a motor-turned helical cam; Hirth faces carry torsion | **M** - read: yaw and pitch motors in chain locomotion. Shared in kind: servo-driven revolute joints inline. Differs: one joint, +-15 deg, geared sector | L - Shen 2001 not read, capped | N | https://robots.isi.edu/conro/proto2H.html |
| Q64-C22 HEXEL | L - paper unread | L | L | L | L | DOI 10.1126/scirobotics.adl3546 (not read) |
| Q64-C23 Hinged Pixels | N | N | N | L | N | https://erikdemaine.org/papers/HingedPixels_SoCG2021/paper.pdf (not re-read) |
| Q64-C24 rolling cylinders | N | L | N | L | N | https://hal.archives-ouvertes.fr/hal-02300456 |
| Q64-C25 PenduMorph | N | L - magnetic docking | N | L | N | https://arxiv.org/pdf/2606.22491 |
| Q64-C26 Rotundus GroundBot | N | N | N | N | N | https://orionrobots.co.uk/wiki/rotundus |
| Q64-C27 Sphero / BB-8 | N | N | N | N | N | https://newatlas.com/sphero-bb-8-droid/39269/ |
| Q64-C28 MOPARAS | N | L | N | L | N | https://research.polyu.edu.hk/en/publications/moparas-a-modular-parallel-spherical-robot-with-position-adjustab/ |
| Q64-C29 pendulum-sphere literature | N | N | N | N | N | https://ar5iv.labs.arxiv.org/html/2302.08932 |

### 4.5 Extra references (Y)

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| Y1 ModLock | L - flat plates | **M** - read: "The faces are twisted 12 deg to align and tighten"; "a stainless steel locking dowel on a compliant lever snaps into a lock groove". Shared in kind: push in, twist, lock (bayonet class), passive hold. Differs: manual, whole-module twist, snap dowel; no teeth on the face | N | L | N | https://www.modlabupenn.org/wp-content/uploads/ModLock.pdf |
| Y2 Zhang, Zhang, Gupta | L | **M** - read: "pushed along Slot 2 and rotated, it will be spring-backed to the position between two teeth, and the two modules are locked". Shared in kind: insert, rotate, lock against **teeth** (a detent, not a face pair). Differs: rotation by module joints, spring-back, slotted layers; no motor cam, no Hirth face | L | L | N | https://mdpi-res.com/d_attachment/robotics/robotics-06-00025/article_deploy/robotics-06-00025.pdf |
| Y3 RoFICoM | L - 50 mm round connector | **M** - read: "The motor rotates the clip, which then slides out of the body using pins driven by a helical slot in the body. The hooks slide under hooks in the mating clip". Shared in kind: a motor-turned ring moving in a helical slot to lock. Differs: the slot extends a hook ring, genderless hook to hook; no self-locking stage, no toothed face | N | L | N | https://rofi.fi.muni.cz/assets/files/publications/roficom.pdf |
| Y4 WPI twist-lock poster | L | **M** - read (poster, thin; v1 read, re-opened): "Gendered Twist-Lock Connector ... bayonet or quarter-turn mechanism". Shared in kind: gendered quarter-turn lock. Differs: nothing more stated | L | L | N | https://users.wpi.edu/~cxu5/docs/MSEFPoster.pdf |
| Y5 CoBoLD | L | L - capped; secondary only (worm-wheel locking wheel with milled hooks on four bolts). See s5 risk note | L | L | N | DOI 10.1109/ROBIO.2011.6181589 (record only) ; UCT thesis |
| Y6 RIMRES latch | L | L - secondary only | L | L | N | UCT thesis |
| Y7 LaMMos | N | L - motorized screw into a T-nut | N | N | N | https://arxiv.org/pdf/1801.00035 (v1 read) |
| Y8 Latching X-Face / DRAGON | L | L - read: passive compliant latch, chamfered pins and grooves, no serrations | N | L | N | https://www.modlabupenn.org/wp-content/uploads/latching_xface_overlay.pdf ; https://www.modlabupenn.org/wp-content/uploads/X-Face.pdf |
| Y9 Truss Link / VTT | N | L - magnets; servo latch with rack and pinion | N | L | N | https://arxiv.org/pdf/2508.01829 (v1 read) |
| Y10 MODUR | L | L - read: a motor-rotated screw-in hook, 90 deg resolution, 33 mm; the hold needs "continuing to provide thrust ... through friction", so it is power-held. Shared only: motor-rotated hook lock. Magnets for pre-alignment | L | L | N | https://arxiv.org/pdf/2510.13356 |
| Y11 Cam-shaft tool changer | N | L - read: servo, cam, lock-pin, chamfered receptacle; a manipulator tool changer, not a module coupler | N | N | N | https://arxiv.org/pdf/2603.04760 |
| **Y12 Beckhoff arm module (US 12,290,920 B2)** | N - an industrial arm module with rotary joint, round | **M** - read: "a first face gearing 302 having four teeth, which is embodied as a Hirth joint"; "By twisting the fastening ring 401, the internal thread is screwed onto the external thread 301, pressing the second connection device 40 onto the first connection device 30 ... torque-locking manner"; centering pin. Shared in kind: **a Hirth face pair on a modular-robot connector, drawn together by a rotating ring, with a centering feature.** Differs: 4 teeth vs 36; a hand-screwed threaded ring vs a motor-turned helical-slot bronze sleeve with a 3 deg self-locking stage and stop pin; not self-reconfigurable; carries data, power and fluid lines | N | N - manual assembly, no reconfiguration | N | https://patents.google.com/patent/US12290920B2/en |
| **Y13 Xerox PolyBot toy patent (US 6,605,914 B2)** | L | **M** - read: "Each connector plate includes connector teeth 30 allowing for positioning of the module relative to its adjacent module"; "eight teeth allow eight rotational positions"; claim: "connector teeth having a profile suitable for locking an attaching robotic module into position". Shared in kind: **a ring of teeth on a modular-robot connector face that fixes relative roll.** Differs: 4 or 8 coarse teeth, a few indexed positions, vs 36 fine Hirth teeth that centre and carry zero-lash torsion; plates are latched separately. Counted with PolyBot (C12) for rule 2 | L | L | N | https://patents.google.com/patent/US6605914B2/en |
| **Y14 Belke and Paik (TMECH 2019)** | L - cylindrical genderless coupling; abstract only | **M, capped (primary not obtained).** Abstract read: "genderless coupling ... disengages two modules at a pre-defined torque threshold ... compact cylindrical space". The teeth statement comes from a search summary only: radial teeth on the front face "with similarities to Hirth joint teeth". Shared in kind (if confirmed): toothed face on a modular-robot coupling. Differs on the abstract: the teeth are meant to release at an overload torque, the opposite of zero-lash torque carrying, and the coupling is genderless | L - abstract | L - abstract: self-reconfigurable systems "enabling" | N | DOI 10.1109/TMECH.2019.2907802 ; https://infoscience.epfl.ch/record/265187 |
| **Y15 PetLock (HIT)** | N - space interface | **M** - read: pyramid pushed axially by an electric push rod moves locking pins radially; "mu > tan beta, the locking mechanism has the capability of self-locking ... beta = 5 deg". Shared in kind: **a motor-driven lock held by a friction self-locking wedge angle.** Differs: genderless, pyramid and radial pins, 5 deg, axial push rod, 3D face; no helical sleeve, no Hirth teeth | N | L | N | https://arxiv.org/pdf/2209.04307 |
| **Y16 Reach Robotics (US 11,376,730 B2)** | N | **M** - read: "a plurality of protrusions arranged in an annular array and extending from the flange"; "A locking nut is arranged about, and threadedly engaged with, the male connector". Shared in kind: bayonet-style flange and annular protrusions with a rotating collar. Differs: a hand locking nut, sealed underwater manipulator modules; no teeth, no motor cam | N | N | N | https://patents.google.com/patent/US11376730B2/en |
| Y17 iBOSS iSSI / SIROM | N | L - capped: bayonet plug-and-turn seen in a search summary only; the SIROM paper read has no mechanism text | N | L | N | https://www-live.dfki.de/fileadmin/user_upload/import/10026_SIROM-IAC.pdf |
| Y18 KIST module connection (US 10,160,121 B2) | N | L - read (summary text): a rotating fixing ring screwed to "wing thread" on a genderless connector, four orientations; thin text, capped at low | N | L | N | https://patents.google.com/patent/US10160121B2/en |
| Y19 CN110561486A joint quick connection | N | L - read: a conical fit with screws; positioning pins; no teeth | N | N | N | https://patents.google.com/patent/CN110561486A/en |
| Y20 Ben-Tzvi docking (US 9,616,948) | L | L - read: T-mech shaft, hex neck, C-mech clamps, non-back-drivable lead screw | L | L | N | https://patents.google.com/patent/US9616948B2/en |

Counts. High cells against F1 or F2 (A1, B1-B4): 0. High cells in total: 0. Moderate cells: 20 (listed in s0). The most moderate cells against one reference lineage are PolyBot: four in C12, plus Y13 D2 counted with PolyBot, so five. CONRO has three. No reference has a high.

## 5. Differentiation notes (Q61 s3 items 3 and 4)

There is no high cell, so there is no item-4 note. Each moderate cell has a note below. "Kept" means a feature forced by Family B or by the task.

**New in v2: the Hirth face pair (Y12, Y13, Y14).** This is the point the author asked me to examine. My finding: the feature is known in modular robots.
- **Y12 Beckhoff D2.** Shared: a Hirth tooth pair on the connector faces, pulled together by a rotating ring, with a centering feature. This is the nearest published combination of "Hirth plus turning collar". Differs: 4 teeth vs 36; a hand-screwed thread vs a motor-turned helical-slot cam sleeve with a capture stage (20 deg), a self-locking stage (3 deg) and a torque-stop seat; cand-d's lugs, pilot and stop pin; a rigid arm module vs a chain unit. I rated M, not H: an informed observer would not call a 4-tooth, hand-screwed industrial arm flange and a 36-tooth, motor-drawn, self-locking coupler on a chain unit "the same design". Kept: the Hirth pair itself, which is a generic machine element (dossier s8 says so, and this review agrees). **Not kept as a novelty claim:** nothing in the dossier may claim Hirth teeth on a modular-robot coupler as new.
- **Y13 Xerox D2.** Shared: teeth around a connector face fix the roll between modules. Differs: coarse indexing teeth (4 or 8), several allowed positions, latch separate; cand-d has one roll position, 36 teeth that centre and carry torque with zero lash. Counted with PolyBot for rule 2, still no high.
- **Y14 Belke and Paik D2 (capped).** If the paper confirms radial teeth that resemble a Hirth ring on the coupling face, then the shared kind is a toothed face on a self-reconfigurable-robot coupling. Differs on the abstract: the teeth let two modules disengage at a set torque (overload release), whereas cand-d's teeth hold torsion and do not slip; genderless vs gendered; no helical cam sleeve described. I could not read it, so I cannot rule out that D2 is closer than M. See s9 item 2.

**PolyBot (C12 D1, D2, D3, D4; Y13 D2).** The reference with the most moderate cells. A single high would not fail alone (rule 2 needs two highs), but a second would.
- D1. Shared: a rectangular two-port body with one joint between the ports. Kept: this is the Family B definition. Differs: aspect (about 1.9 to 1, a long head and a short 8.8 mm tail, vs a cube-like module with matching halves), gendered ends vs hermaphroditic plates, the coupler axis offset from the body axis (3.3, 1.0). I rate M, not H, because the proportions and the gendered stud-and-cartridge ends are not those of PolyBot.
- D2. Shared: a pin-like part entering a hole and locked by turning about the interface axis, no power to hold; and (Y13) teeth on the connector face. Differs: SMA wires and a spring, a four-leg plate, grooved pins vs a lug stud, a helical cam sleeve, motor close and release, a self-locking stage and a fine Hirth ring.
- D3. Shared: one revolute joint per module. Differs: +-15 deg sector gear vs a full-range hinge.
- D4. Shared: chains. Differs: chain only, no reconfiguration claim, no IR. Kept: chain-native is Family B.

**CONRO (D1, D2, D3).**
- D1. Shared: elongated, gendered ends, actuator between. Differs: two shell segments with a hinge inside the body. Kept: gendered inline ends are cand-d's own choice (flagged in v1; the author may revisit).
- D2. Shared: gendered pin-in-receptacle docking with an unpowered hold. Differs: no SMA, no spring-closed default, no groove on the pin, powered close by torque stop, and now Hirth faces carry the torque. cand-b's high against CONRO was for SMA release plus spring-closed latch; cand-d has neither.
- D3. Shared: servo revolute joints inline. Differs: one joint, small range.

**ATRON D2, HyMod D2, Roombots D2.** All three: "motor-driven latch, unpowered hold". Differs: hooks on arms with a lead screw (ATRON); four radial hooks and a 298:1 gearbox (HiGen); a crank to a geometric singularity (Roombots). cand-d uses lugs on helical cam slots and friction self-locking (2.86x dry, 1.91x oiled per the dossier), with a Hirth seat. Kept: the non-backdrivable hold class, which is how G6 passive retention can be met.

**PetLock D2 (Y15).** Shared: a motor-driven lock held by a friction self-locking wedge (mu greater than tan of the angle). Differs: 5 deg pyramid pushing radial pins on a genderless face, vs a 3 deg helical stage on a bronze sleeve. Kept: the friction wedge principle is generic and is named in the dossier as "friction wedge".

**Bayonet and rotating-collar class (ModLock D2, Zhang D2, WPI D2, RoFICoM D2, Reach D2, Beckhoff D2).** This is the class the task asked me to re-check. Shared in kind: push in, turn, lock. Differs in each case:
- ModLock: manual, whole-module twist, snap dowel.
- Zhang: the modules' own joints rotate; spring-back between teeth; slotted layers.
- WPI poster: thin; no more details.
- RoFICoM: the helical slot extends a hook ring against a mating hook ring (genderless); no self-locking lead and no toothed face. This is the nearest published "motor plus ring plus helical slot", so a later reviewer should re-read it if the coupler changes again.
- Reach: hand locking nut on a sealed underwater arm; no teeth.
- Beckhoff: see above.
cand-d: a dedicated motor, a bronze sleeve with a capture stage and a 3 deg self-locking stage, a torque-stop seat that absorbs the axial tolerance stack, and a Hirth pair. The bayonet class is generic. The dossier does not claim novelty in the class.

**CKBot D3.** Shared: a servo-class revolute joint in a chain module. Differs: sector-gear joint inside a shell, +-15 deg. Kept: Family B.

**Combination risk (not a rating).** The coupler can be described as "RoFICoM-style motor ring and helical slot" plus "Beckhoff-style Hirth pair" plus "PetLock-style friction wedge". Each part appears in a different published system. No one reference holds two of the three on a chain unit. A combination of references does not make any one cell high under Q61, and I did not raise any cell for it. I record it so an owner can see it.

**Risk notes on capped cells (not ratings).**
- CoBoLD D2 (Y5): if the primary paper confirms a motor-driven worm-gear locking wheel with milled hooks grasping four cone bolts, a reviewer could rate it M. Differentiation: four cone bolts and hooks vs a two-lug stud on helical cam slots, a Hirth pair; genderless vs gendered. It could not make a high without a second feature shared in specific form.
- M-TRAN D1 and D3: the two-box body with a joint is the Family B shape. A confirmed M would need a note: one joint vs two, gendered stud ends vs gendered hook faces, no magnets.
- Y14 Belke and Paik: see above.

## 6. Exclusion checks (Q62 s3, recorded for G8)

1. **Cube with an internal flywheel (M-Blocks lineage): not present.** The body is a 47.2 x 25.4 x 24 mm elongated two-segment prism, not a cube. The declaration's 35 components (kinds structure, energy_source, controller, actuator, coupler_mechanism, other) include no flywheel, brake or inertial actuator. Motion is by a geared joint, not impulse. The new v2 parts (Hirth ring, stop pin, retainer collar, ears) are all static or coupler parts.
2. **Needle- or particle-like silhouette: not present.** Site-to-site pitch 47.2 mm, cross-section 25.4 x 24 mm, aspect about 1.9 to 1. That is a tabletop block, not a thin needle and not a sub-visible particle. The stowed enclosing sphere is 58.862 mm (dossier). Design guidance s4.1's forbidden direction is not approached.

## 7. Family membership check (Q62 s3, Family B)

Constraint: "An elongated two-segment body with one internal revolute joint, so it is chain-native, with couplers at the segment ends." Checked against `declaration.json` (v2):
- Two segments: head (box half-extent x 16.3 at x 18.1, so x 1.8 to 34.4, plus a front plate to 35.6) and tail (half-extent x 3.8 at x -5.6, so x -9.4 to -1.8, plus an end plate to -10.6), separated by a 3.6 mm hinge gap. Yes.
- One internal revolute joint: one hinge pin (dia 2, 304) driven by one gearmotor and one toothed sector (`joint-motor`, `joint-pinion`, `joint-sector`, `hinge-pin`). Yes. The Hirth ring and sleeve turn are coupler motions, not a body joint.
- Elongated: aspect about 1.9 to 1 along the chain. Yes, modest. The tail is short (8.8 mm), which the family text allows.
- Couplers at the segment ends: `site-head` at x 35.6 (head end face, normal +x) and `site-tail` at x -11.6 (tail end face, normal -x). Yes.
- Chain-native: chain declared inline, `mating_roll_deg [0]`, head site to tail site.
- Result: **cand-d v2 is a member of Family B** (`family` field "B"). The reviewer found no violation. Not tested here: that the joint bends a chain adequately (Q31, unresolved in the dossier). Family membership is about structure, not function.

## 8. Fail-rule evaluation

- Rule 1 (any F1 cell high): none. A1 is N in every column. Not triggered.
- Rule 2 (two or more highs against one reference): there are no highs against any reference. The nearest are PolyBot (four moderates in C12, plus Y13 D2 counted with it) and CONRO (three). Not triggered.
- Item 3 (every moderate has a differentiation note): done in s5 for all 20 moderate cells.
- Item 4 (every single high has a note and is listed prominently): there are no highs.
- Item 5 (both exclusions recorded): done in s6.
- G8 (Q62): no high cell against F1 or F2, both exclusions "not present". Satisfied.
- Completeness: every cell of the matrix has a rating, a reason (short for L and N cells, per the cell convention) and a source in its row. Capped cells are marked.
- Independence: the reviewer is a different agent session with no authorship in cand-d (Q61 s4). The declaration hash matches.

## 9. Changes recommended

No change is required for this review to pass. These are advice only. Any declaration change changes the hash and needs a new review (Q61 s5).
1. **Author:** do not claim novelty for a Hirth pair, the bayonet class, or the friction wedge. Keep the claim to the combination, and state it as "no single published system found with all of these".
2. **Reviewer follow-up (r2, optional but advised):** obtain the full text of Belke and Paik (TMECH 2019, DOI 10.1109/TMECH.2019.2907802) and confirm or revise Y14 D2. If it shows a Hirth-like tooth ring with preload and torque carrying in the same coupler as a rotating cam, D2 could rise to high. A single high is allowed (it would need a note, no fail), but it would sit beside Beckhoff and RoFICoM. Also try again for M-TRAN III, CoBoLD, the CKBot module paper, Shen 2001 and iBOSS iSSI.
3. **Corpus (owner or lead, by a decision record):** add Y1 to Y4 and Y12 to Y16 (at least ModLock, Zhang, RoFICoM, the WPI poster, Beckhoff US 12,290,920, Xerox US 6,605,914, Belke and Paik, PetLock) as appended entries. This review does not edit the corpus.
4. **Final visuals (Q61 s7):** D5 is rated only on the declared materials. The exposed Hirth ring and bronze sleeve are visible features, so D5 needs a fresh look when the visuals exist.
5. **Wording:** the dossier calls Hirth a "common machine element" (s8). This review confirms that, and found it in a modular-robot arm connector. Keep that wording.

## 10. Outcome

**pass.** No F1 high, no reference with two highs, no high cell at all, every moderate noted, both exclusions "not present", Family B membership holds, the declaration hash matches the expected value. Pass means no Q61 fail rule was triggered by the references examined, with the capped cells listed in s1. It is not a claim of absolute originality. This review reduces copying risk and does not claim absolute originality.
