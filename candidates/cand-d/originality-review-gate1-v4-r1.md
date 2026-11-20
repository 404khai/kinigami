candidate_id: cand-d
candidate_version: 4
declaration_sha256: 21bebbe5812f9a4f41f43c0868634afceb6cf75972174e0f7e2924a0beccb978
stage: gate1
author: Claude Opus 5.5 (engineering lead, cand-d author)
reviewer: reviewer-d4-originality (Claude Sonnet 5.5, independent session, no authorship in cand-d)
high_cells_f1_f2: 0
exclusion_cube_with_internal_flywheel: not_present
exclusion_needle_or_particle_silhouette: not_present
outcome: pass

# Originality review (Q61, stage gate1): cand-d v4, r1

Date: 2026-11-20. This review reduces copying risk and does not claim absolute originality.

## 0. Summary

- Result: **pass** under Q61 s3. No cell against F1 (A1) or F2 (B1-B4) is high. There is **no high cell at all**, so no reference has two highs. Both Q62 exclusions are not present. Every moderate cell has a differentiation note (s5). Family B membership holds (s7).
- **High cells (Q61 s3 item 4): none.** The closest calls are Belke and Paik (Y14) and Beckhoff (Y12), both held at moderate on D2 (s5).
- **Moderate cells (21):** C4 ATRON D2; C6 Roombots D2; C12 PolyBot D1, D2, D3, D4; C14 CKBot D3; C17 HyMod D2; Q64-C21 CONRO D1, D2, D3; Y1 ModLock D2; Y2 Zhang D2; Y3 RoFICoM D2; Y4 WPI poster D2; Y12 Beckhoff D2; Y13 Xerox D2; Y14 Belke and Paik D2; Y15 PetLock D2; Y16 Reach D2; Y21 Khoshnevis D2. The list is the same as for v3, but every cell was re-rated against v4 and the primary sources were re-read in this session.
- **What v4 changes (Q91).** The cam, sleeve, PTFE ring, Hirth faces, stud and head flange are as in v3. v4 changes how parts are fastened: countersunk M1.6 screws from inside the tail end plate into the 304 stud flange; one-piece SLS shell per segment with a separate lid; countersunk-screwed root legs on the hinge ears and plates; slots widened to 3.40; recessed inner lands; chamfer and seating figures. All of these are generic fastening, tolerance and reference-plane changes. Components added: `ear-up-leg`, `ear-low-leg`, `plate-up-leg` (304 root legs). I found no published modular-robot coupler or joint with a distinctive shared form in these features. No rating changed because of v4.
- **Combination risk (not a rating).** A reader could describe the coupler as RoFICoM (motor ring in a helical slot) plus Beckhoff (Hirth pair drawn by a turning ring) plus Belke and Paik (radial toothed faces on a robot coupling with a self-locking angle) plus PetLock (friction wedge). No single reference I read holds more than one of these on a chain unit. Recorded for the owner. It raises no cell.

## 1. Basis, limits and primary sources

**Compared.** `candidates/cand-d/declaration.json` (v4) with `dossier-v4.md`, `dossier-v3.md`, `dossier-v2.md`, and Q91. The declaration hash was computed in this session: `shasum -a 256 candidates/cand-d/declaration.json` = `21bebbe5812f9a4f41f43c0868634afceb6cf75972174e0f7e2924a0beccb978`, equal to the expected value, so the outcome is not forced to `unresolved`. The dossier's self-check (s4) was used as a pointer, not as a rating. The v1 to v3 reviews were used only as pointer lists (Y1 to Y26). I rated every cell afresh and re-read the primary sources myself for every moderate cell.

**v4 as declared (basis of every cell).**
- Body: two PA12 SLS (PA2200) shell segments, head 33.8 mm and tail 8.8 mm, section 25.4 x 24 mm, 3.6 mm hinge gap, 47.2 mm site to site, one vertical revolute joint (304 pin, spur sector, 6 mm gearmotor, +-15 deg working). Stowed sphere 58.862 mm (dossier, not recomputed). Each shell is one SLS part with a separate non-load lid.
- Coupler, rigid and gendered: a one-piece 304 tail stud (flange r 6.3 with a 36-tooth 90 deg Hirth ring, dia 4 pilot, two dia 3 lugs), held by two countersunk M1.6 screws driven from inside the end plate into blind holes of the flange. A head cartridge: a one-piece 304 housing with a front flange (Hirth ring, two lobes, two countersunk M1.6 screws through the plate into nut blocks), lug slots 3.40, stop pin; a C93200 bronze sleeve with two helical slots (20 deg capture stage, 3 deg self-locking lock stage); a PTFE thrust ring; a 304 retainer collar. A 6 mm gearmotor turns the sleeve to a 1.0 V stall and seats the faces at 4.41 to 9.00 N. Torsion and shear go through the teeth. Hold is passive (`friction_wedge`).
- Declaration text: "No spring, no SMA, no magnet. BLE only, no power transfer." A grep of the declaration for colour, finish, marking, paint, anodise, logo, flywheel returns nothing. D5 is therefore rated on declared materials only.

**Primary sources read in this session (fetched 2026-11-20; PDFs by pdftotext; patents as Google Patents full text). Quotes are verbatim.**
- **Belke and Paik**, IEEE/ASME Trans. Mechatronics 24(3):1420-1428, 2019, DOI 10.1109/TMECH.2019.2907802, full text from https://ieeexplore.ieee.org/ielx7/3516/8736910/08675300.pdf (the URL gave HTTP 418 with a bare user agent and the PDF with a browser user agent). Read: "The front face of the coupling element has specially designed radial teeth ... The teeth of the coupling element engage with identical teeth on a pivot of another module and, thus, transmit rotational actuation."; "The teeth have similarities to those of a Hirth joint, a locked mechanical coupling for shafts, although with an altered design and a different purpose. The faces of each tooth span between two radial lines, resulting in a varying angle of the face along the radius, unlike a Hirth joint."; "The genderless coupling incorporates a novel safety mechanism that disengages two modules at a predefined torque threshold."; "We employ an SMA spring, providing a contractile force when heated, to retract the coupling element to an open state."; "A passive spring placed around the square pin ensures that the coupling returns to a closed state once the SMA spring cools down"; "the self-locking condition that occurs when the axial force produced by the torque acting on the angled teeth can no longer overcome the frictional forces acting on the slider."
- **Beckhoff, US 12,290,920 B2**, "Arm module for a modular robot arm of an industrial robot", https://patents.google.com/patent/US12290920B2/en: "the first connecting device 30 has a first face gearing 302 having four teeth, which is embodied as a Hirth joint"; "a fastening ring 401 with an internal thread"; "a second face gearing 402 having four teeth, which is embodied as Hirth joint and is embodied complementary"; "a centering receptacle 403 corresponding to a centering pin 303".
- **Xerox, US 6,605,914 B2** (PolyBot toy patent), https://patents.google.com/patent/US6605914B2/en: "Each connector plate includes connector teeth 30 allowing for positioning of the module relative to its adjacent module. ... any number of connector teeth may be used ... eight teeth allow eight rotational positions of the module relative to its adjacent module".
- **RoFICoM**, https://rofi.fi.muni.cz/assets/files/publications/roficom.pdf: "The motor rotates the clip, which then slides out of the body using pins driven by a helical slot in the body. The hooks slide under hooks in the mating clip and therefore, prevent the connectors from being pulled apart."; "genderless 90-degree symmetric connection mechanism".
- **ModLock**, https://www.modlabupenn.org/wp-content/uploads/ModLock.pdf: "The faces are twisted 12 deg to align and tighten the male connector plate assembly with the female pattern. A stainless steel locking dowel on a compliant lever snaps into a lock groove to prevent the faces from untwisting."
- **ATRON**, Ostergaard et al., https://sccn.ucsd.edu/download/robot.pdf: "The three hooks are driven by a DC motor via a lead screw. The mechanism driving the arms is not backdrivable in the extented arm position, hence no power is required to maintain connection."
- **Roombots**, Sprowitz et al., Robotics and Autonomous Systems 62(7), DOI 10.1016/j.robot.2013.08.011. I read a copy of the EPFL PDF already in the session scratchpad (the Elsevier front page and text are those of the DOI paper). My own re-fetch from infoscience.epfl.ch returned HTTP 429 and Zenodo returned 410, so this one copy was not fetched by me. Read: "Roombots' ACM requires no power in the connected state. Its crank and slider mechanism (Fig. 4(a)) pushes the latch into an externally non-reversible singularity position."
- **PolyBot G2**, Yim et al., https://modlab.engineering.upenn.edu/publications/asme.pdf: "Two pieces of 150 micron shape memory alloy (SMA) wire are mechanically connected to ... the plate"; legs "reach out and around the grooves in the pins of a mating module when the latch is engaged"; segment modules with one rotational DOF.
- **CONRO**, https://robots.isi.edu/conro/proto2H.html: "a passive connector that has pins to allow the module to connect to other modules, a motor housing that supports the servos of the module and, an active connector"; "the latch engages groves on the pins and secure them. To release the pins, a SMA wire is contracted pulling the latch back".
- **HiGen (HyMod)**, Parrott et al., IROS 2014, https://sheffield.ac.uk/media/22956/download: "Once two connectors are joined they can maintain a connection even when power is removed"; genderless, connections at 90 degree intervals.
- **Zhang, Zhang, Gupta**, Robotics 6(2):25, https://mdpi-res.com/d_attachment/robotics/robotics-06-00025/article_deploy/robotics-06-00025.pdf: "When a male interface is pushed along Slot 2 and rotated, it will be spring-backed to the position between two teeth, and the two modules are locked".
- **PetLock**, https://arxiv.org/pdf/2209.04307: self-locking property of the locking mechanism, driven by an electric push rod (genderless, pyramid and pins).
- **Reach Robotics, US 11,376,730 B2**, https://patents.google.com/patent/US11376730B2/en: "A plurality of protrusions 56 arranged in an annular array extend into the aperture 54"; "a locking nut threadedly engaged with the associated connector and operable to urge the male connector and female connector into engagement".
- **Khoshnevis (USC), US 7,850,388 B2**, https://patents.google.com/patent/US7850388B2/en: "a rotating drive mechanism, a hollow cylindrical body operatively connected to the rotating drive mechanism, wherein the hollow cylindrical body has at least one internal spiral channel, and at least one connector claw positioned within the hollow cylindrical body and guided by the internal spiral channel".
- **CKBot**, https://www.modlabupenn.org/ckbot/ : "a chain style modular robot"; modules "having one rotational degree of freedom". **WPI poster**, https://users.wpi.edu/~cxu5/docs/MSEFPoster.pdf: "A bayonet or quarter-turn mechanism inspired by androgynous fasteners."
- **CuBot-STT**, https://arxiv.org/html/2610.39279 (read in part): 120 mm cubic modules, "a gear transmission converts one external input into motion of four helical locking points", locked by an external tightening robot.

**Not obtained or not fully read (cells capped; low is not a clearance).**
- M-TRAN I to III (C1-C3), PolyPod (C20), CoBoLD (Y5), Shen 2001 (CONRO docking), the CKBot module paper, iBOSS iSSI, Q64-C22 to C29 primaries, the SMORES-EP hardware paper, the Parrott HiGen thesis.
- Advanced Robotics 2026, DOI 10.1080/01691864.2026.2618831 (HTTP 403 from tandfonline, content unknown). US 10,482,786 (the USPTO PDF is an image with no text layer). US 10,910,760 and core.ac.uk/download/147946969.pdf (HTTP 404 and 403).
- Fictional entries (A1, B1-B4): no engineering source; rated from corpus descriptors (secondary). Kit pages D1-D4: corpus descriptors and the 2026-11-20 search below.

## 2. Search record

Date: 2026-11-20. Tools: web search (standard and extended), direct fetch (curl with browser user agent, WebFetch), Unpaywall and Semantic Scholar APIs for open-access locations. All searches are mine; the earlier reviews' searches were used only as pointers.
1. "modular robot connector Hirth face teeth motor-driven rotating sleeve helical slot self-locking docking 2026" (extended). Returned: Advanced Robotics 2026 (unreadable), US 10,482,786 (unreadable), a 2025 RA-L continuum robot paper (record only), CuBot-STT (arXiv 2610.39279, read in part), the EPM connector arXiv 2508.16008 (magnets), SMORES-EP parallel assembly, "A Novel Docking System for Modular Self-Reconfigurable Robots". Added Y27 CuBot-STT. The summary quoted "TYCOON" (hook into a female groove on insertion and rotation); searched for it next.
2. "chain-type self-reconfigurable modular robot gendered stud lugs bayonet motorized coupler draws serrated faces preload patent". Returned the Parrott thesis, US 8,234,950 (SINGO), MODUR, ModLock, HiGen. Nothing closer than before.
3. "modular robot toy kit twist-lock connector two-segment servo module snake chain 2025 product". Returned KiwiCo snake kit, Fable, ChainFORM, ModMi, Tamiya chain-program robot, Lynxmotion, Jimu, Robosen. Added kit group Y28 (summary level, low).
4. "TYCOON modular robot connector hook female groove insertion rotation locking mechanism". Returned ModLock, Reach US 11,376,730, MODUR, US 9,917,398 (snap connector), US 10,910,760 (electrical connector, rotatable locking part), US 8,777,649. No TYCOON primary found. Added Y29 as record-only.
5. "Hirth coupling robot module docking Hirth self-reconfigurable modular robot connector 2025". Returned the UCT thesis (RIMRES), Zhang, a docking-system paper (DOAJ), arXiv 2603.04760 (tool changer), US 2007/0286674. No new Hirth-on-robot-coupler reference beyond Beckhoff, Xerox, and Belke and Paik.
6. Re-fetch and read of the primary sources listed in s1 (the 13 listed above, each by curl or pdftotext).
7. Fictional entries: no new search. F2 examined from the corpus descriptors only: Replicators (B1), Prey (B2), Borg nanites (B3), T-1000 (B4). Big Hero 6 (A1) from the corpus descriptor and the two cited secondary sources (not re-opened).

Findings. A Hirth or serrated face on a modular-robot connector appears in three published places (Beckhoff 4 teeth, Xerox 4 or 8 indexing teeth, Belke and Paik radial teeth "similarities to those of a Hirth joint"). A motor-turned member with helical channels appears in RoFICoM and Khoshnevis, and with four helical locking points in CuBot-STT (external robot, no teeth). A friction self-locking wedge appears in PetLock and in Belke and Paik's analysis. I found no system that combines a 36-tooth Hirth pair with a motor-turned bronze helical-slot sleeve that draws a gendered lugged stud to a 3 deg self-locking stage on a two-segment chain unit. Search results are not proof of absence.

## 3. References examined, by class

- F1: A1. F2: B1-B4.
- P (corpus): C1-C23 and Q64-C21 to Q64-C29 (Q65 identifiers; C21 Swarm-bot, C22 Sambot, C23 Blinky Blocks are the section-C entries).
- K: D1 Cubelets, D2 MOSS, D3 UBTech Jimu, D4 LEGO Mindstorms EV3.
- Extra (Y), carried as pointers from earlier reviews and re-rated: Y1 ModLock, Y2 Zhang et al., Y3 RoFICoM, Y4 WPI poster, Y5 CoBoLD, Y6 RIMRES, Y7 LaMMos, Y8 Latching X-Face and DRAGON, Y9 Truss Link/VTT, Y10 MODUR, Y11 tool changer, Y12 Beckhoff, Y13 Xerox, Y14 Belke and Paik, Y15 PetLock, Y16 Reach, Y17 iBOSS iSSI/SIROM, Y18 KIST, Y19 CN110561486A, Y20 Ben-Tzvi US 9,616,948, Y21 Khoshnevis, Y22 US 6,780,042, Y23 US 11,654,548, Y24 ChainFORM/Makeblock/ROBOTIS/PMR, Y25 RhoMorph, Y26 ElectroVoxels.
- **New in this review:** Y27 CuBot-STT (arXiv 2610.39279), Y28 kit and toy snake-chain group (KiwiCo snake robot, Fable, ModMi, Tamiya chain-program), Y29 TYCOON connector (search summary only), Y30 Advanced Robotics 2026 paper and US 10,482,786 (unreadable, record only).

## 4. Similarity matrix

Key: N none, L low, M moderate, H high. D1 silhouette and geometry, D2 coupler concept, D3 actuation and locomotion logic, D4 assembly and reconfiguration, D5 visual identity.

**D5 (declared only).** Rated on what the declaration states: white PA12 SLS shell, exposed 304 steel and bronze coupler parts including a visible Hirth ring, no colour scheme, markings or finish. A D5 of N is not a clearance of the final look and must be re-rated at final visuals (Q61 s7).

**Convention.** A bare N or L has a short reason. Every M cell has the full reason and the primary source I read in this session (access date 2026-11-20). Sources read only as corpus descriptors carry the corpus access date 2026-11-04.

### 4.1 Forbidden and fictional

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| A1 BH6 microbots (F1) | N - one 47 mm two-segment unit vs thousands of near-identical small units | N - steel stud, bronze cam sleeve, Hirth faces; no magnet vs magnetic legs | N - one geared joint vs crowd-surfing | N - identical chain units vs arbitrary shapes | N - pale PA12 and bare steel vs a dark liquid-like swarm | https://gizmodo.com/how-disney-will-make-you-cry-again-with-big-hero-6-1630115219 ; https://awn.com/animationworld/don-hall-and-chris-williams-talk-disneys-big-hero-6 (corpus, 2026-11-04) |
| B1 Replicators (F2) | N - elongated two-segment body vs insect-like blocks | N - no mechanism shown in the work | N | L - both join identical units | N | https://en.wikipedia.org/wiki/Nanotechnology_in_fiction (corpus, secondary) |
| B2 Prey (F2) | N - cloud | N | N | N | N | same |
| B3 Borg nanites (F2) | N - sub-visible | N | N | N | N | same |
| B4 T-1000 (F2) | N - continuous liquid metal | N | N | N | N | same |

### 4.2 Published robots, section C

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| C1 M-TRAN I | L - two box halves; primary unread, capped | L - magnets vs mechanical; capped | L - two joints vs one; capped | L - capped | N | DOI 10.1109/TMECH.2002.806220 |
| C2 M-TRAN II | L - capped | L - capped | L - capped | L - capped | N | corpus record (bib-bvb) |
| C3 M-TRAN III | L - capped | L - capped | L - capped | L - capped | N | DOI 10.1177/0278364907085560 |
| C4 ATRON | L - two hemispheres vs boxes | **M** - read: "The three hooks are driven by a DC motor via a lead screw. The mechanism driving the arms is not backdrivable in the extented arm position, hence no power is required to maintain connection." Shared in kind: motor latch held unpowered by a non-backdrivable element. Differs: three hooks on arms vs lugs on helical slots, a friction self-locking stage and a Hirth seat | L - one equatorial joint | L - lattice vs chain | N | https://sccn.ucsd.edu/download/robot.pdf ; DOI 10.1109/IROS.2004.1389702 |
| C5 SMORES-EP | L - small cube | L - electro-permanent magnets (hardware paper not read) | L | L | N | DOI 10.1126/scirobotics.aat4983 |
| C6 Roombots | L - paired spheres | **M** - read: "requires no power in the connected state. Its crank and slider mechanism ... pushes the latch into an externally non-reversible singularity position." Shared in kind: motor latch with a non-reversible unpowered hold. Differs: over-centre singularity vs friction self-locking stage and a toothed seat | L - three DOF | L | N | DOI 10.1016/j.robot.2013.08.011 (EPFL PDF; see s1 note) |
| C7 M-Blocks | N - cube | N - magnets | N - flywheel | N | N | DOI 10.1109/IROS.2013.6696971 |
| C8 3D M-Blocks | N | N | N | N | N | DOI 10.1109/ICRA.2015.7139450 |
| C9 Kilobot | N | N - no coupler | N | N | N | DOI 10.1109/ICRA.2012.6224638 |
| C10 catoms | L | L | L | L | N | DOI 10.1109/MC.2005.198 |
| C11 Molecubes | L | L - electromagnets | L | L | N | DOI 10.1038/435163a |
| C12 PolyBot | **M** - read: segment modules with one rotational DOF; interface plates about 50 mm square. Shared in kind: a prismatic two-port body with one joint between the ports. Differs: symmetric halves and hermaphroditic plates vs a 33.8 mm head, 8.8 mm tail and gendered ends | **M** - read: legs "reach out and around the grooves in the pins of a mating module when the latch is engaged", SMA wire and return spring, unpowered hold. Shared in kind: pin-in-hole docking, latch about the interface axis. Differs: SMA, spring, four-leg plate vs lug stud, motor-turned sleeve and Hirth seat | **M** - read: one rotational DOF per segment. Differs: +-15 deg sector joint vs a full-range hinge | **M** - read: chain reconfiguration by docking. Differs: cand-d claims chain only | N | https://modlab.engineering.upenn.edu/publications/asme.pdf |
| C13 SuperBot | L - boxy segments, module paper unread | L - SINGO jaws on a circular gear (US 8,234,950) | L | L | N | https://robots.isi.edu/prl/shen2009SINGO.pdf |
| C14 CKBot | L - 60 mm cube | L - read: modules "connected manually using M3 screws" | **M** - read: "chain style modular robot", one rotational DOF per module. Shared in kind: a revolute joint in a chain module. Differs: sector-geared +-15 deg joint inside a shell | L | N | https://www.modlabupenn.org/ckbot/ |
| C15 Soldercubes | L | L | L | L | N | DOI 10.1007/s10514-015-9441-4 |
| C16 FreeBOT | N | L | L | L | N | https://freeformrobotics.org/wp-content/uploads/2022/02/IROS20_0857_FI.pdf |
| C17 HyMod | L | **M** - read (HiGen): "Once two connectors are joined they can maintain a connection even when power is removed"; genderless hooks. Shared in kind: motor latch with unpowered hold. Differs: radial hooks hook-to-hook vs gendered lugs on a helical cam and a Hirth seat | L | L | N | DOI 10.1007/978-3-319-73008-0_28 ; https://sheffield.ac.uk/media/22956/download |
| C18 Telecube | N | L - magnets | N | L | N | https://researchr.org/publication/SuhHY02 |
| C19 Crystalline | L | L - latches | L | L | N | DOI 10.1023/A:1026504804984 |
| C20 PolyPod | L - capped | L - capped | L | L | N | https://www.mit.edu/people/manoli/polypod/polypod.html |
| C21 Swarm-bot | N | L - gripper and ring | N | L | N | DOI 10.1023/B:AURO.0000033972.50769.1c |
| C22 Sambot | L - cuboid | L - active docking face | N | L | N | DOI 10.1109/TMECH.2010.2085009 |
| C23 Blinky Blocks | N | L - magnets | N | L | N | DOI 10.1145/1979742.1979712 |

### 4.3 Commercial kits

| Ref | D1 | D2 | D3 | D4 | D5 | Source |
| --- | --- | --- | --- | --- | --- | --- |
| D1 Cubelets | L - small blocks | L - magnetic snap | N | L | N - bright plastic vs white PA12 and steel | https://modrobotics.com/about-us |
| D2 MOSS | L | L - magnets | L | L | N | https://forums.parallax.com/discussion/151259/moss-brand-new-robot-construction-system-from-modular-robotics |
| D3 UBTech Jimu | N | L - interlocking parts | L | L | N | https://www.pcworld.com/article/419049/ubtech-looks-to-up-its-toy-robot-game-with-the-jimu.html |
| D4 LEGO EV3 | N | L - studs and pins | L | L | N | https://www.lego.com/en-us/product/31313 |

### 4.4 Q64 additions

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| Q64-C21 CONRO | **M** - read: a module of "a passive connector that has pins ... a motor housing ... an active connector". Shared in kind: an elongated inline module with a pin end and a receptacle end. Differs: two shell segments with a hinge gap, the joint inside the body | **M** - read: "the latch engages groves on the pins and secure them. To release the pins, a SMA wire is contracted pulling the latch back". Shared in kind: gendered pin-in-receptacle docking, unpowered hold. Differs: no SMA, no latch, no groove on the pin; a lug stud drawn by a motor-turned helical cam; Hirth faces carry torque | **M** - read: yaw and pitch servos inline. Differs: one joint, +-15 deg | L - Shen 2001 not read, capped | N | https://robots.isi.edu/conro/proto2H.html |
| Q64-C22 HEXEL | L - paper unread | L | L | L | L | DOI 10.1126/scirobotics.adl3546 |
| Q64-C23 Hinged Pixels | N | N | N | L | N | https://erikdemaine.org/papers/HingedPixels_SoCG2021/paper.pdf |
| Q64-C24 rolling cylinders | N | L | N | L | N | https://hal.archives-ouvertes.fr/hal-02300456 |
| Q64-C25 PenduMorph | N | L - magnetic docking | N | L | N | https://arxiv.org/pdf/2606.22491 |
| Q64-C26 Rotundus GroundBot | N | N | N | N | N | https://orionrobots.co.uk/wiki/rotundus |
| Q64-C27 Sphero / BB-8 | N | N | N | N | N | https://newatlas.com/sphero-bb-8-droid/39269/ |
| Q64-C28 MOPARAS | N | L | N | L | N | https://research.polyu.edu.hk/en/publications/moparas-a-modular-parallel-spherical-robot-with-position-adjustab/ |
| Q64-C29 pendulum-sphere literature | N | N | N | N | N | https://ar5iv.labs.arxiv.org/html/2302.08932 |

### 4.5 Extra references (Y)

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| Y1 ModLock | L - flat plates | **M** - read: "The faces are twisted 12 deg to align and tighten ... A stainless steel locking dowel on a compliant lever snaps into a lock groove". Shared in kind: push in, twist, lock (bayonet class), passive hold. Differs: manual whole-module twist, snap dowel; no teeth on the face | N | L | N | https://www.modlabupenn.org/wp-content/uploads/ModLock.pdf |
| Y2 Zhang, Zhang, Gupta | L | **M** - read: "pushed along Slot 2 and rotated, it will be spring-backed to the position between two teeth, and the two modules are locked". Shared in kind: insert, rotate, lock against teeth (a detent). Differs: rotation by the modules' joints, spring-back, slotted layers; no motor cam, no face pair | L | L | N | https://mdpi-res.com/d_attachment/robotics/robotics-06-00025/article_deploy/robotics-06-00025.pdf |
| Y3 RoFICoM | L - 50 mm round connector | **M** - read: "The motor rotates the clip, which then slides out of the body using pins driven by a helical slot in the body. The hooks slide under hooks in the mating clip". Shared in kind: a motor-turned ring in a helical slot that locks. Differs: the slot extends a hook ring, genderless hook to hook; no self-locking stage stated, no toothed face | N | L | N | https://rofi.fi.muni.cz/assets/files/publications/roficom.pdf |
| Y4 WPI twist-lock poster | L | **M** - read (thin): "A bayonet or quarter-turn mechanism inspired by androgynous fasteners". Shared in kind: a quarter-turn lock. Differs: nothing more is stated; androgynous | L | L | N | https://users.wpi.edu/~cxu5/docs/MSEFPoster.pdf |
| Y5 CoBoLD | L | L - capped, secondary only | L | L | N | DOI 10.1109/ROBIO.2011.6181589 |
| Y6 RIMRES latch | L | L - secondary only | L | L | N | UCT thesis (https://open.uct.ac.za/bitstreams/5dcc9290-b036-4687-b908-3ca62889beac/download, search result) |
| Y7 LaMMos | N | L - motorized screw into a T-nut | N | N | N | https://arxiv.org/pdf/1801.00035 |
| Y8 Latching X-Face / DRAGON | L | L - passive compliant latch, no serrations | N | L | N | https://www.modlabupenn.org/wp-content/uploads/latching_xface_overlay.pdf |
| Y9 Truss Link / VTT | N | L - magnets, servo latch | N | L | N | https://arxiv.org/pdf/2508.01829 |
| Y10 MODUR | L | L - read: lead-screw thrust, then rotation to lock hooks; genderless | L | L | N | https://arxiv.org/pdf/2510.13356 |
| Y11 tool changer | N | L - servo, cam and lock-pin; manipulator tool changer | N | N | N | https://arxiv.org/pdf/2603.04760 |
| Y12 Beckhoff US 12,290,920 B2 | N - industrial arm module, round | **M** - read: "face gearing 302 having four teeth, which is embodied as a Hirth joint"; "fastening ring 401 with an internal thread"; "centering pin 303". Shared in kind: a Hirth face pair on a modular-robot connector, pulled together by a turning ring, with a centering feature. Differs: 4 teeth vs 36; a thread vs a motor-turned helical-slot sleeve with a self-locking stage; a robot-arm module, not a self-reconfigurable unit | N | N - manual assembly | N | https://patents.google.com/patent/US12290920B2/en |
| Y13 Xerox US 6,605,914 B2 | L | **M** - read: "Each connector plate includes connector teeth 30 allowing for positioning of the module relative to its adjacent module ... eight teeth allow eight rotational positions". Shared in kind: a ring of teeth on a modular-robot connector face that fixes roll. Differs: 4 or 8 coarse indexing teeth vs 36 Hirth teeth that centre and carry zero-lash torsion. Counted with PolyBot (C12) for rule 2 | L | L | N | https://patents.google.com/patent/US6605914B2/en |
| Y14 Belke and Paik | L - cylindrical genderless coupling in an edge hinge of an origami module | **M** - read in full (s1). Shared in kind: radial teeth on the front face of a modular-robot coupling, engaged with identical teeth, self-centering, "similarities to those of a Hirth joint", torque through angled faces, a self-locking condition from face angle and friction, a purpose of unpowered hold. Differs: genderless; planar-faced teeth "unlike a Hirth joint"; the toothed slider is moved on a square rail by an SMA spring and a return spring; the teeth are an overload release at a set torque (the coupling "disengages"), where cand-d's teeth carry torsion without slip and the lugs on a bronze helical stage hold tension; the teeth transmit joint actuation. Not H: not the same design in specific form or principle | L - the coupling also transmits a hinge rotation; cand-d's joint is inside the body | L | N | https://ieeexplore.ieee.org/ielx7/3516/8736910/08675300.pdf ; DOI 10.1109/TMECH.2019.2907802 |
| Y15 PetLock | N | **M** - read: a lock with a self-locking property, driven by an electric push rod (pyramid and pins; genderless). Shared in kind: a motor-driven lock held by friction self-locking. Differs: genderless, axial pyramid and radial pins vs a 3 deg helical stage on a sleeve; no Hirth teeth | N | L | N | https://arxiv.org/pdf/2209.04307 |
| Y16 Reach US 11,376,730 B2 | N | **M** - read: "A plurality of protrusions 56 arranged in an annular array"; "a locking nut threadedly engaged ... urge the male connector and female connector into engagement". Shared in kind: bayonet-style annular protrusions and a rotating collar on a modular connector. Differs: hand nut, sealed underwater manipulator modules; no teeth, no motor cam | N | N | N | https://patents.google.com/patent/US11376730B2/en |
| Y17 iBOSS iSSI / SIROM | N | L - capped (search summary) | N | L | N | https://www-live.dfki.de/fileadmin/user_upload/import/10026_SIROM-IAC.pdf |
| Y18 KIST US 10,160,121 / 9,853,386 | N | L - threaded fixing ring on a genderless connector; no teeth | N | L | N | https://patents.google.com/patent/US9853386B1/en |
| Y19 CN110561486A | N | L - conical fit with screws, positioning pins; no teeth | N | N | N | https://patents.google.com/patent/CN110561486A/en |
| Y20 Ben-Tzvi US 9,616,948 | L | L - T-mech shaft, C-mech clamps, non-back-drivable lead screw | L | L | N | https://patents.google.com/patent/US9616948B2/en |
| Y21 Khoshnevis US 7,850,388 B2 | L - cylindrical module coupling | **M** - read: "a rotating drive mechanism, a hollow cylindrical body ... has at least one internal spiral channel, and at least one connector claw ... guided by the internal spiral channel". Shared in kind: a motor-turned cylinder with spiral channels moves the latching elements (same lab lineage as CONRO). Differs: genderless claws extending radially vs a gendered stud with lugs drawn axially; no teeth, no stated self-locking stage | L | L | N | https://patents.google.com/patent/US7850388B2/en |
| Y22 US 6,780,042 B1 | N | L - plug with lamellae and shoulders, actuators; no teeth | N | N | N | https://patents.google.com/patent/US6780042B1/en |
| Y23 US 11,654,548 B2 | L - two rotatable housings | L - rotating ring with drive gear teeth, not a face pair | L | L | N | https://patents.google.com/patent/US11654548B2/en |
| Y24 ChainFORM / Makeblock / ROBOTIS / PMR | L - chain of servo modules | L - screws, brackets, magnets; summaries only | L | L | N | https://spectrum.ieee.org/automaton/robotics/robotics-hardware/modular-robotic-chain-is-whatever-you-want-it-to-be (search result) |
| Y25 RhoMorph | N | L - docking of rhombus modules | N | L | N | https://arxiv.org/pdf/2601.19529 |
| Y26 ElectroVoxels | N - cubes | N - electromagnets | N | L | N | https://www.hackster.io/news/a-joint-effort-in-modular-robotics-9d4984e3bc86 (search result) |
| **Y27 CuBot-STT** | N - 120 mm cubes | L - read in part: "a gear transmission converts one external input into motion of four helical locking points"; locked by an external tightening robot. Helical locking, no teeth, no onboard motor | N | L - lattice | N | https://arxiv.org/html/2610.39279 |
| **Y28 kit snake-chain group** (KiwiCo snake robot, Fable, ModMi, Tamiya chain-program) | L - chain of servo modules | L - search summaries only; ModMi "standardized mechanical and electrical interfaces" | L | L | N | search result pages, not opened |
| **Y29 TYCOON** | L | L - capped; search-summary text only: a hook engages a female groove on insertion and rotation | L | L | N | search result summary (no primary found) |
| **Y30 Adv. Robotics 2026 / US 10,482,786** | L - capped | L - capped, unreadable | L | L | N | https://www.tandfonline.com/doi/pdf/10.1080/01691864.2026.2618831 (403) ; https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10482786 (image only) |

**Counts.** High cells against F1 or F2 (A1, B1-B4): **0**. High cells in total: **0**. Moderate cells: **21** (list in s0). Most moderates against one lineage: PolyBot four in C12, plus Y13 D2 counted with it for rule 2 (five, none high). CONRO three. No reference has a high.

## 5. Differentiation notes (Q61 s3 items 3 and 4)

No high cell, so no item-4 note. "Kept" means a feature forced by Family B or by the task.

**Hirth and toothed-face class (Y12 Beckhoff, Y13 Xerox, Y14 Belke and Paik).**
- **Y14 Belke and Paik D2 (M, not H).** This is the closest reference to the face pair and the closest overall. Shared: radial teeth on a robot coupling, "similarities to those of a Hirth joint", self-centering, torque through the teeth, a self-locking condition, passive hold. Why not high: an informed observer would not call it the same design. Its teeth are planar-faced and explicitly "unlike a Hirth joint"; it is genderless; the slider is pushed by an SMA spring and a passive return spring on a square rail; the teeth are designed to disengage at a set torque, while cand-d's are designed not to (zero lash, lugs on a 3 deg bronze helical stage hold tension). cand-d keeps a true 36-tooth 90 deg Hirth pair and has no SMA, spring or magnet. Not kept as a claim: the dossier may not claim toothed faces on a modular-robot coupler as new. If a later version adds an SMA, a return spring, a planar-faced tooth or a sliding toothed slider, re-review this reference first, because D2 could then reach high.
- **Y12 Beckhoff D2.** Shared: a Hirth pair on connector faces drawn together by a turning ring, with a centering feature. Differs: 4 teeth vs 36; a hand-screwed thread vs a motor-turned helical-slot sleeve with capture and self-locking stages and a torque-stop seat; a robot-arm module vs a chain unit. M, not H: the form and the principle of drawing differ. Kept: the Hirth pair, a generic machine element.
- **Y13 Xerox D2.** Shared: a tooth ring on a connector face fixes roll. Differs: coarse, several allowed positions, latch separate; cand-d has one roll position and 36 teeth that centre and carry torque. Counted with PolyBot for rule 2. Still no high.

**Bayonet, rotating-collar and cam-sleeve class (Y1 ModLock, Y2 Zhang, Y3 RoFICoM, Y4 WPI, Y16 Reach, Y21 Khoshnevis).** Shared in kind: push in, turn, lock; in Y3 and Y21 a motor-turned member with helical slots or channels. Differs:
- ModLock: manual whole-module twist, snap dowel.
- Zhang: the modules' own joints rotate; spring-back between teeth.
- WPI: a poster with one line on a quarter-turn lock; nothing more to compare.
- RoFICoM: the helical slot extends a hook ring against a mating hook ring (genderless); no stated self-locking stage, no toothed face. The nearest published "motor plus ring plus helical slot".
- Reach: hand nut, sealed underwater manipulator modules; no teeth.
- Khoshnevis: genderless claws pushed out by spiral channels; no teeth, no stated self-locking.
- cand-d: a dedicated motor turns a bronze sleeve with a 20 deg capture stage and a 3 deg self-locking stage to a stall that seats a Hirth pair and absorbs the axial tolerance stack. The class is generic and the dossier must not claim novelty in it.

**Motor latch with unpowered hold (C4 ATRON, C6 Roombots, C17 HyMod).** Shared: a motor-driven latch held without power by a non-backdrivable element (lead screw, over-centre singularity, gearbox friction). Differs: hooks on arms (ATRON), crank to a singularity (Roombots), radial genderless hooks (HiGen) vs lugs on helical slots held by friction self-locking (2.86x dry, 1.91x oiled per the dossier). Kept: the non-backdrivable hold class, which is how G6 passive retention is met.

**PetLock D2 (Y15).** Shared: a friction self-locking wedge in a motor-driven lock. Differs: a pyramid pushing radial pins on a genderless face vs a 3 deg helical stage on a sleeve. The principle is generic and is declared as `friction_wedge`.

**PolyBot (C12 D1, D2, D3, D4; Y13 D2).**
- D1. Shared: a rectangular two-port body with one joint between the ports. Kept: this is the Family B definition. Differs: a long head and an 8.8 mm tail vs matching halves; gendered ends vs hermaphroditic plates; the coupler axis offset from the body axis (3.3, 1.0). M, not H.
- D2. Shared: a pin entering a hole and locked by a motion about the interface axis, unpowered hold. Differs: SMA wires, spring, four-leg plate vs a lug stud, helical sleeve, motor close and release, self-locking stage, Hirth ring.
- D3. Shared: one revolute joint per module. Differs: +-15 deg sector gear vs a full-range hinge.
- D4. Shared: chains. Differs: chain only, no reconfiguration claim. Kept: chain-native is Family B.

**CONRO (D1, D2, D3).**
- D1. Shared: elongated, gendered ends, actuator between. Differs: two shell segments with a hinge inside the body. Kept: gendered inline ends are cand-d's choice.
- D2. Shared: gendered pin-in-receptacle docking, unpowered hold. Differs: no SMA, no latch, no groove on the pin; Hirth faces carry the torque. Khoshnevis (Y21, same lineage) differs as above.
- D3. Shared: servo revolute joints inline. Differs: one joint, small range.

**CKBot D3.** Shared: a revolute joint in a chain module. Differs: sector-gear joint inside a shell, +-15 deg. Kept: Family B.

**v4 changes (Q91): countersunk screws, one-piece shells, root legs, slots 3.40, reference planes.** No cell changes. Screwed joints, one-piece SLS shells with a lid, and screw-fixed hinge legs are generic fastening. The closest shared items found are the screwed CKBot connection ("M3 screws") and the Reach threaded nut, neither with the same form. No v4 feature is a coupler concept.

**Risk notes on capped cells (not ratings).**
- M-TRAN D1 and D3: the two-box body with a joint is the Family B shape. A confirmed M would need a note (two joints vs one, gendered stud ends vs permanent magnet faces, no magnets). An H is not plausible: M-TRAN has two joints and magnetic faces, and cand-d has one joint and a mechanical coupler.
- CoBoLD D2: a motor-driven locking wheel with hooks would be M at most (genderless, cone bolts vs a lug stud with a Hirth pair).
- TYCOON D2 (search summary only): a hook entering a female groove on insertion and rotation would be M at most (bayonet class, as ModLock).

## 6. Exclusion checks (Q62 s3, recorded for G8)

1. **Cube with an internal flywheel (M-Blocks lineage): not present.** The body is an elongated two-segment prism, 47.2 x 25.4 x 24 mm, not a cube. The declared components (structure, energy_source, controller, actuator, coupler_mechanism, other) include no flywheel, brake or inertial actuator, and a grep of the declaration for "flywheel" returns nothing. Motion is by a geared joint, not impulse. The v4 parts (root legs, screws) are static.
2. **Needle- or particle-like silhouette: not present.** Site to site 47.2 mm, section 25.4 x 24 mm, aspect about 1.9 to 1, flange lobes to r 9.4. A tabletop block, neither a needle nor sub-visible. Stowed sphere 58.862 mm (dossier). Design guidance s4.1's forbidden direction is not approached.

## 7. Family membership check (Q62 s3, Family B)

Constraint: "An elongated two-segment body with one internal revolute joint, so it is chain-native, with couplers at the segment ends." Checked against `declaration.json` v4 (`family` "B"):
- Two segments: `head-segment` (box half-extent x 16.3 at x 18.1) and `tail-segment` (half-extent x 3.8 at x -5.6), with end plates, separated by a 3.6 mm hinge gap. Yes.
- One internal revolute joint: one hinge pin (`hinge-pin`), one gearmotor, pinion and sector (`joint-motor`, `joint-pinion`, `joint-sector`). The sleeve turn is a coupler motion, not a body joint. The v4 root legs are mounts, not joints. Yes.
- Elongated: aspect about 1.9 to 1 along the chain. Modest, and the tail is short, which the family text allows.
- Couplers at the segment ends: `site-head` at x 36.4 and `site-tail` at x -11.6. Yes.
- Chain-native: `chain` has `head_site` and `tail_site`, `mating_roll_deg [0]`.
- Result: **cand-d v4 is a member of Family B.** Whether the joint bends a chain adequately (Q31) is not tested here. Membership is structural.

## 8. Fail-rule evaluation

- Rule 1 (any F1 cell high): none. A1 is N in every column. Not triggered.
- Rule 2 (two or more highs against one reference): there is no high against any reference. Nearest: PolyBot (five moderates counting Y13) and CONRO (three). Not triggered.
- Item 3 (every moderate has a differentiation note): done in s5 for all 21.
- Item 4 (every single high has a note, listed prominently): there are none.
- Item 5 (both exclusions recorded): done in s6.
- G8 (Q62): no high against F1 or F2; both exclusions not present. Satisfied.
- Completeness: every cell has a rating, a reason (short for N and L) and a source in its row; capped cells are marked. The hash check matches the expected value.
- Independence: the reviewer is a different agent session with no authorship in cand-d (Q61 s4).
- Limits that bear on the outcome: the capped cells (M-TRAN, CoBoLD, Shen 2001, TYCOON, Advanced Robotics 2026, US 10,482,786) cannot produce a fail under rule 2 alone, because a fail needs two highs against one reference and none of those has a plausible high in two dimensions. A cap is not a clearance.

## 9. Recommended changes

No change is required for this review to pass. Advice only; any declaration change changes the hash and needs a new review (Q61 s5).
1. **Author:** do not claim novelty for a Hirth pair, toothed faces on a robot coupling, the bayonet or cam-sleeve class, or the friction wedge. If a claim is made, state it as the combination, with "no single published system found with all of these".
2. **Differentiation to keep:** a true Hirth pair that holds torsion without slip (Belke and Paik's teeth release at a threshold), a gendered lug stud, no SMA, no spring, no magnet. If a later version adds an SMA, a return spring, a planar-faced tooth or a sliding toothed slider, re-review Belke and Paik and PolyBot D2 first.
3. **Corpus (owner or lead, by a decision record):** append Y1 to Y4, Y12 to Y16, Y21 and Y27 to the corpus. This review does not edit the corpus.
4. **Reviewer follow-up (optional):** obtain M-TRAN III, CoBoLD, the CKBot module paper, Shen 2001, iBOSS iSSI, the 2026 Advanced Robotics paper and TYCOON. Re-read Roombots from a fresh fetch if the EPFL copy can be reached.
5. **Final visuals (Q61 s7):** D5 is rated only on declared materials. The exposed Hirth ring, bronze sleeve and flange lobes are visible features and need a fresh look.

## 10. Outcome

**pass.** No F1 high, no reference with two highs, no high cell at all, every moderate noted, both exclusions not present, Family B membership holds, and the declaration hash matches the expected value. Pass means only that no Q61 fail rule was triggered by the references examined, with the capped cells listed in s1. It is not a claim of absolute originality. This review reduces copying risk and does not claim absolute originality.
