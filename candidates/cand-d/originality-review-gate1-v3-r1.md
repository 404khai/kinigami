candidate_id: cand-d
candidate_version: 3
declaration_sha256: 0f82c5062fc83c8b9eb918e728f41b357245aeda848cf5d87989a0444ae6f8e8
stage: gate1
author: Claude Opus 5.5 (engineering lead, cand-d author)
reviewer: reviewer-d3-originality (Claude Sonnet 5.5, independent session, no authorship in cand-d)
high_cells_f1_f2: 0
exclusion_cube_with_internal_flywheel: not_present
exclusion_needle_or_particle_silhouette: not_present
outcome: pass

# Originality review (Q61, stage gate1): cand-d v3, r1

Date: 2026-11-20. This review reduces copying risk and does not claim absolute originality.

## 0. Summary

- Result: **pass** under Q61 s3. No cell against F1 (A1) or F2 (B1-B4) is high. There is **no high cell at all**, so no reference has two highs. Both Q62 exclusions are not present. Every moderate cell has a differentiation note (s5). Family B membership holds (s7).
- **High cells (Q61 s3 item 4): none.** The closest calls are Belke and Paik (Y14, now read in full) and Beckhoff (Y12). Both are held at moderate (s5).
- **Moderate cells (21):** C4 ATRON D2; C6 Roombots D2; C12 PolyBot D1, D2, D3, D4; C14 CKBot D3; C17 HyMod D2; Q64-C21 CONRO D1, D2, D3; Y1 ModLock D2; Y2 Zhang D2; Y3 RoFICoM D2; Y4 WPI poster D2; Y12 Beckhoff D2; Y13 Xerox PolyBot toy patent D2; Y14 Belke and Paik D2 (cap lifted: full text read); Y15 PetLock D2; Y16 Reach Robotics D2; **new Y21 Khoshnevis US 7,850,388 D2**.
- **What v3 changes.** The coupler action, cam, Hirth faces and stud are as in v2. v3 makes the housing one 304 part with a front flange (disc r 7.0, lobes to r 9.4) screwed through the PA12 plate into nut blocks, and widens the lug slots to 3.20. These are generic fastening and tolerance changes. I found no published modular-robot coupler with a lobed front flange screwed through a shell plate that bears on the Hirth/cam features. No v2 rating rose because of them. Two things differ from the v2 review: I read Belke and Paik in full (it was capped before), and I added one reference (Y21).
- **Combination risk (not a rating).** A reader could describe the coupler as RoFICoM (motor ring, helical slot) plus Beckhoff (Hirth pair drawn by a turning ring) plus Belke and Paik (radial toothed faces on a robot coupling, with a self-locking angle) plus PetLock (friction wedge). No single reference holds more than one of these on a chain unit. Recorded for the owner. It raises no cell.

## 1. Basis, limits and primary sources

**Compared.** `candidates/cand-d/declaration.json` (v3) and `dossier-v3.md`, with `dossier-v2.md` for the unchanged parts. `shasum -a 256 candidates/cand-d/declaration.json` gives `0f82c5062fc83c8b9eb918e728f41b357245aeda848cf5d87989a0444ae6f8e8`, equal to the expected value, so the outcome is not forced to unresolved. Dossier s6 (author self-check) was used as a pointer only, not as a rating. The v1 and v2 reviews were used as pointer lists (Y1-Y16). Every cell was rated afresh against v3.

**v3 as declared (basis of every cell).**
- Body: two PA12 SLS (PA2200 white) shell segments, head 33.8 mm and tail 8.8 mm, section 25.4 x 24 mm, 3.6 mm hinge gap, 47.2 mm site to site, one vertical revolute joint (304 pin, spur sector, 6 mm gearmotor, +-15 deg). Stowed sphere 58.862 mm (dossier, not recomputed).
- Coupler, rigid and gendered: a one-piece 304 tail stud (flange with a 36-tooth 90 deg Hirth ring r 2.6 to 6.3, dia 4 pilot, two dia 3 lugs). A head cartridge: a one-piece 304 housing with a front flange (Hirth ring on its front face, lobes, two countersunk M1.6 screws through the plate into two nut blocks), lug slots 3.20 wide, a stop pin; a C93200 bronze sleeve with two helical slots (20 deg capture stage, 3 deg self-locking lock stage); a PTFE thrust ring; a 304 retainer collar. A 6 mm gearmotor turns the sleeve to a 1.0 V stall, seating the faces under 4.41 to 9.00 N. Torsion and shear go through the teeth. Hold is passive (`friction_wedge`).
- No SMA, no spring, no magnet. BLE only. No power transfer. No stated colour, markings or finish.

**Primary sources read in this session (fetched 2026-11-20; PDFs by pdftotext; patents as Google Patents full text).** Quotes are verbatim.
- **Beckhoff, US 12,290,920 B2**, https://patents.google.com/patent/US12290920B2/en: "the first connecting device 30 has a first face gearing 302 having four teeth, which is embodied as a Hirth joint"; "a fastening ring 401 with an internal thread"; "a second face gearing 402 having four teeth, which is embodied as Hirth joint and is embodied complementary"; "a centering receptacle 403 corresponding to a centering pin 303".
- **Xerox, US 6,605,914 B2**, https://patents.google.com/patent/US6605914B2/en: "Each connector plate includes connector teeth 30 allowing for positioning of the module relative to its adjacent module. ... any number of connector teeth may be used ... eight teeth allow eight rotational positions".
- **Belke and Paik, IEEE/ASME Trans. Mechatronics 24(3) 2019, DOI 10.1109/TMECH.2019.2907802**, full text obtained from https://ieeexplore.ieee.org/ielx7/3516/8736910/08675300.pdf (the open-access URL given by the Semantic Scholar and Unpaywall APIs; the `iel7` URL and WebFetch returned HTTP 418 and 403). Read: "The front face of the coupling element has specially designed radial teeth ... The teeth of the coupling element engage with identical teeth on a pivot of another module and, thus, transmit rotational actuation. A radial design ... makes the coupling elements self-centering"; "The teeth have similarities to those of a Hirth joint, a locked mechanical coupling for shafts, although with an altered design and a different purpose. The faces of each tooth span between two radial lines, resulting in a varying angle of the face along the radius, unlike a Hirth joint. This allows for a planar, rather than a conical, design of the coupling mesh"; "We employ an SMA spring ... to retract the coupling element"; "A passive spring placed around the square pin ensures that the coupling returns to a closed state"; "The coupling element, or slider, runs on a rail of square cross section"; the teeth's angled faces produce an axial force so that at a torque threshold "the slider retracts and causes the coupling to disengage"; "the self-locking condition that occurs when the axial force produced by the torque acting on the angled teeth can no longer overcome the frictional forces acting on the slider"; the couplings are genderless, 3-D printed and machined, in a modular origami robot (Mori).
- **PolyBot G2**, Yim et al., https://modlab.engineering.upenn.edu/publications/asme.pdf: segment modules "nominally rectangular prisms and have one rotational degree of freedom"; a latch plate with SMA wire "150 micron shape memory alloy (SMA) wire", a return spring; interface plates about 50 x 50 mm.
- **CONRO**, https://robots.isi.edu/conro/proto2H.html: "a passive connector that has pins to allow the module to connect to other modules, a motor housing ... and, an active connector that contains the connection/disconnection mechanism"; yaw and pitch servos.
- **ATRON**, Ostergaard et al., https://sccn.ucsd.edu/download/robot.pdf: "The three hooks are driven by a DC motor via a lead screw. The mechanism driving the arms is not backdrivable in the extended arm position".
- **Roombots**, Sprowitz et al., EPFL PDF: crank and slider "pushes the latch into an externally non-reversible singularity position".
- **HiGen (HyMod)**, Parrott et al., https://sheffield.ac.uk/media/22956/download: genderless, hooks extended, holds with power removed.
- **RoFICoM**, https://rofi.fi.muni.cz/assets/files/publications/roficom.pdf: "The motor rotates the clip, which then slides out of the body using pins driven by a helical slot in the body. The hooks slide under hooks in the mating clip"; a skirt blocked from rotation by a slot.
- **ModLock**, https://www.modlabupenn.org/wp-content/uploads/ModLock.pdf: "The faces are twisted 12 deg to align and tighten the connection"; "stainless steel locking dowel on a compliant lever snaps into a lock groove".
- **Zhang, Zhang, Gupta**, Robotics 6(2):25, https://mdpi-res.com/d_attachment/robotics/robotics-06-00025/article_deploy/robotics-06-00025.pdf: "When a male interface is pushed along Slot 2 and rotated, it will be spring-backed to the position between two teeth, and the two modules are locked".
- **PetLock**, https://arxiv.org/pdf/2209.04307: "So when mu > tan beta, the locking mechanism has the capability of self-locking" (push rod, pyramid, radial pins).
- **Reach Robotics, US 11,376,730 B2**, https://patents.google.com/patent/US11376730B2/en: "A plurality of protrusions 56 arranged in an annular array extend into the aperture"; a "locking nut threadedly engaged with the associated connector".
- **MODUR**, https://arxiv.org/pdf/2510.13356: lead-screw thrust then rotation "thereby locking the hooks together"; hold by "continuing to provide thrust ... through friction".
- **Khoshnevis (USC), US 7,850,388 B2**, https://patents.google.com/patent/US7850388B2/en: "a rotating drive mechanism, a hollow cylindrical body ... has at least one internal spiral channel, and at least one connector claw ... guided by the internal spiral channel ... configured to extend outwardly ... to engage the mating coupling module"; genderless. No teeth, no self-locking text.
- **KIST US 9,853,386 B1** and **US 6,780,042 B1** (Google Patents text): a threaded fixing ring on a genderless connector; a lamella plug with shoulders and actuators. No teeth.
- **CKBot**, https://www.modlabupenn.org/ckbot/ (read this session): "a chain style modular robot", "one rotational degree of freedom", "Modules can be connected manually using M3 screws", 60 mm cube, 138 g. WPI poster, https://users.wpi.edu/~cxu5/docs/MSEFPoster.pdf (thin): "A bayonet or quarter-turn mechanism".
- Also checked in search results only (records): RhoMorph arXiv 2601.19529 (read: no coupler of relevance, rhombus planar modules), US 11,654,548 B2 (Google Patents text; rotating ring with gear teeth driven by a bevel gear, subunit module with two rotatable housings; teeth are drive gear teeth, not a face pair).

**Not obtained (cells capped).**
- M-TRAN I to III (C1-C3), PolyPod (C20), CoBoLD (Y5), Shen 2001 (CONRO docking), the CKBot module paper, iBOSS iSSI, Q64-C22 to C29 papers. Rated from corpus descriptors and capped at low where marked. A rating of low is not a clearance.
- Fictional entries (A1, B1-B4): no engineering source. Rated from corpus descriptors (secondary).
- Kit pages D1-D4: corpus descriptors, plus a 2026-11-20 search for kits (s2).

## 2. Search record

Date: 2026-11-20. Tools: web search (standard and extended) and direct fetch (curl, WebFetch). Terms and what each returned:
1. "Belke Paik Automatic Couplings with Mechanical Overload Protection for Modular Robots radial teeth Hirth", then an extended query on the teeth. Returned the EPFL record, IEEE page, Semantic Scholar, ResearchGate (HTTP 403), the Mori3 GitHub. The Semantic Scholar and Unpaywall APIs gave an open-access `ielx7` URL, which gave the full PDF.
2. "modular self-reconfigurable robot connector Hirth teeth motor-driven cam sleeve bayonet self-locking genderless OR gendered 2025 2026". Returned HiGen, SINGO, MODUR, ModLock, MODUR HTML. Nothing new.
3. "Hirth coupling modular robot module docking connector face teeth patent twist lock motor". Returned US 7,850,388 (Khoshnevis, spiral channels), US 9,853,386, US 6,780,042, Beckhoff 12,290,920 and 12,285,860, US 11,654,548, KIST US 10,160,121, the arXiv survey 2310.09743. Added Y21; read US 7,850,388, 9,853,386, 6,780,042, 11,654,548.
4. "modular robot docking bayonet motor rotating collar helical slot lugs self-locking lead angle connector paper". Returned Reach 11,376,730, RoFICoM, Zhang, a Sheffield thesis, MODUR, LaMMos, US 11,128,082 (androgynous connection device, record only).
5. "self-reconfigurable modular robot two-segment chain module one revolute joint gendered stud docking lugs". Returned ATRON, Zhang, a SAGE 2014 record (10.5772/58379, record only), RhoMorph. Nothing closer to a two-segment gendered-stud chain unit.
6. "modular robot module connector serrated face teeth lugs bayonet motor rotates sleeve to draw stud tight preload docking mechanism". Returned Reach, HiGen, arXiv 1712.02299 (record only), Beckhoff, Xerox, MODUR, an EPM connector (arXiv 2508.16008, magnetic, not a toothed face), machine-automation patents (records only). Nothing new beyond the above.
7. "modular robot toy kit servo module magnetic OR twist-lock connector snake chain elongated modules product". Returned MOSS, ChainFORM (MIT, servo chain modules), Makeblock Motionblock, ROBOTIS Bioloid, PMR (Hamburg printable modular robot), Cubelets context. Added Y22 to Y25 as kit and toy references (low).
8. "fictional nanite swarm modular robots cubes film game Big Hero 6 microbots ...". Returned the Big Hero 6 wiki ("a central sphere with two legs connected using magnetics"), ElectroVoxels (cubes, electromagnets), a hobbyist microbot-style joint. F1 and F2 descriptors were confirmed against the corpus. ElectroVoxels added as Y26 (low).

Findings. A Hirth or serrated face appears on modular-robot connectors in three published places: Beckhoff (4 teeth, hand-screwed ring), Xerox (4 or 8 indexing teeth), Belke and Paik (radial teeth, "similarities to a Hirth joint"). A motor-turned member with helical channels appears in RoFICoM and Khoshnevis. A friction self-locking wedge appears in PetLock and in Belke and Paik's analysis. I found no system that combines a 36-tooth Hirth pair with a motor-turned bronze helical-slot sleeve that draws a gendered lugged stud to a 3 deg self-locking stage on a two-segment chain unit. Search results are not proof of absence.

F2 examined: Replicators (B1), Prey (B2), Borg and Star Trek nanites (B3), T-1000 (B4). No further fictional works were searched beyond Big Hero 6 context and ElectroVoxels.

## 3. References examined, by class

- F1: A1. F2: B1-B4.
- P (corpus): C1-C23 and Q64-C21 to Q64-C29 (Q65 identifiers). C21 Swarm-bot, C22 Sambot and C23 Blinky Blocks are the section-C entries.
- K: D1 Cubelets, D2 MOSS, D3 UBTech Jimu, D4 LEGO Mindstorms EV3.
- Extra (Y): Y1 ModLock, Y2 Zhang et al., Y3 RoFICoM, Y4 WPI poster, Y5 CoBoLD, Y6 RIMRES, Y7 LaMMos, Y8 Latching X-Face and DRAGON, Y9 Truss Link/VTT, Y10 MODUR, Y11 cam-shaft tool changer, Y12 Beckhoff US 12,290,920, Y13 Xerox US 6,605,914, Y14 Belke and Paik, Y15 PetLock, Y16 Reach US 11,376,730, Y17 iBOSS iSSI/SIROM, Y18 KIST US 10,160,121 and 9,853,386, Y19 CN110561486A, Y20 Ben-Tzvi US 9,616,948, **Y21 Khoshnevis US 7,850,388**, **Y22 US 6,780,042 lamella connector**, **Y23 US 11,654,548 subunit module**, **Y24 ChainFORM / Makeblock Motionblock / ROBOTIS Bioloid / PMR (kit and chain-module group)**, **Y25 RhoMorph**, **Y26 ElectroVoxels**.

## 4. Similarity matrix

Key: N none, L low, M moderate, H high. D1 silhouette and geometry, D2 coupler concept, D3 actuation and locomotion logic, D4 assembly and reconfiguration, D5 visual identity.

**D5 note (declared only).** D5 is rated on what the declaration states: white PA12 SLS shell, exposed 304 and bronze coupler parts including a visible Hirth ring, no colour scheme, markings or finish stated. A D5 of none is not a clearance of the final look. D5 must be re-rated at final visuals (Q61 s7).

**Cell convention.** A bare N or L means no shared feature (N) or only generic features forced by the task or physics (L), with a short reason. Every M cell has a full reason and the source I read. Access date 2026-11-20 for sources read this session, 2026-11-04 for corpus-only sources.

### 4.1 Forbidden and fictional

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| A1 BH6 microbots (F1) | N - one 47 mm two-segment unit vs thousands of small near-identical units (a sphere with legs per the BH6 wiki) | N - steel stud, bronze cam sleeve, Hirth faces vs magnetic legs; no magnet | N - one geared joint vs crowd-surfing | N - identical chain units vs arbitrary shapes | N - pale PA12 and bare steel vs a dark liquid-like swarm | https://gizmodo.com/how-disney-will-make-you-cry-again-with-big-hero-6-1630115219 ; https://awn.com/animationworld/don-hall-and-chris-williams-talk-disneys-big-hero-6 ; https://bighero6.fandom.com/wiki/Microbots (search result, not opened) |
| B1 Replicators (F2) | N - elongated two-segment body vs insect-like blocks | N | N | L - both join identical units | N | https://en.wikipedia.org/wiki/Nanotechnology_in_fiction (corpus, secondary) |
| B2 Prey (F2) | N | N | N | N | N | same |
| B3 Borg nanites (F2) | N | N | N | N | N | same |
| B4 T-1000 (F2) | N | N | N | N | N | same |

### 4.2 Published robots, section C

| Ref | D1 | D2 | D3 | D4 | D5 | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| C1 M-TRAN I | L - two box halves; primary unread, capped | L - magnets vs mechanical; capped | L - capped | L - capped | N | DOI 10.1109/TMECH.2002.806220 |
| C2 M-TRAN II | L - capped | L - capped | L - capped | L - capped | N | corpus record (bib-bvb) |
| C3 M-TRAN III | L - capped | L - capped (secondary only) | L - capped | L - capped | N | DOI 10.1177/0278364907085560 |
| C4 ATRON | L - two hemispheres vs boxes | **M** - read: "The three hooks are driven by a DC motor via a lead screw. The mechanism driving the arms is not backdrivable in the extended arm position". Shared in kind: motor latch held unpowered by a non-backdrivable screw. Differs: hooks on arms gripping bars vs lugs on helical slots and a Hirth seat | L - one equatorial joint | L - lattice vs chain | N | https://sccn.ucsd.edu/download/robot.pdf |
| C5 SMORES-EP | L | L - electro-permanent magnets (paper not read) | L | L | N | DOI 10.1126/scirobotics.aat4983 |
| C6 Roombots | L - paired spheres | **M** - read: the crank and slider "pushes the latch into an externally non-reversible singularity position". Shared in kind: motor latch with a non-reversible unpowered hold. Differs: over-centre singularity vs friction self-locking helical stage and a toothed seat | L - three DOF | L | N | DOI 10.1016/j.robot.2013.08.011 ; EPFL PDF |
| C7 M-Blocks | N - cube | N - magnets | N - flywheel | N | N | DOI 10.1109/IROS.2013.6696971 |
| C8 3D M-Blocks | N | N | N | N | N | DOI 10.1109/ICRA.2015.7139450 |
| C9 Kilobot | N | N | N | N | N | DOI 10.1109/ICRA.2012.6224638 |
| C10 catoms | L | L | L | L | N | DOI 10.1109/MC.2005.198 |
| C11 Molecubes | L | L - electromagnets | L | L | N | DOI 10.1038/435163a |
| C12 PolyBot | **M** - read: segments "nominally rectangular prisms and have one rotational degree of freedom". Shared in kind: prismatic two-port body, one joint between the ports. Differs: about 50 x 50 mm symmetric halves, hermaphroditic plates vs 33.8 mm head and 8.8 mm tail, gendered ends | **M** - read: grooved pins, a latch plate rotating about the interface centre, SMA wire and return spring, no-power hold. Shared in kind: pin-in-hole docking and rotation about the interface axis, unpowered hold. Differs: SMA, spring, four-leg plate vs lug stud, motor-turned sleeve, Hirth seat | **M** - read: one rotational DOF per segment. Differs: +-15 deg sector joint vs full-range hinge | **M** - read: chain reconfiguration by docking. Differs: cand-d claims chain only | N | https://modlab.engineering.upenn.edu/publications/asme.pdf |
| C13 SuperBot | L - boxy segments, module paper unread | L - SINGO jaws on a circular gear (patent 8,234,950, v2 read) | L | L | N | https://robots.isi.edu/prl/shen2009SINGO.pdf |
| C14 CKBot | L - 60 mm cube | L - read: modules "connected manually using M3 screws" | **M** - read: "chain style modular robot", "one rotational degree of freedom". Shared in kind: servo-class revolute joint in a chain module. Differs: sector-geared +-15 deg joint inside a shell | L | N | https://www.modlabupenn.org/ckbot/ |
| C15 Soldercubes | L | L | L | L | N | DOI 10.1007/s10514-015-9441-4 |
| C16 FreeBOT | N | L | L | L | N | https://freeformrobotics.org/wp-content/uploads/2022/02/IROS20_0857_FI.pdf |
| C17 HyMod | L | **M** - read (HiGen): genderless, hooks extended by a motor, holds with power removed. Shared in kind: motor latch with unpowered hold. Differs: radial hooks hook-to-hook vs gendered lugs on a helical cam and a Hirth seat | L | L | N | DOI 10.1007/978-3-319-73008-0_28 ; https://sheffield.ac.uk/media/22956/download |
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
| Q64-C21 CONRO | **M** - read: a module of "a passive connector that has pins ... a motor housing ... an active connector". Shared in kind: elongated inline module with a pin end and a receptacle end. Differs: two shell segments with a hinge gap, the joint inside the body | **M** - read: "the latch engages groves on the pins and secure them. To release the pins, a SMA wire is contracted pulling the latch back"; "a spring brings the latch back to the close position". Gendered pin-in-receptacle docking, unpowered hold. Shared in kind: gendered docking with pins. Differs: no SMA, no spring-closed latch, no groove on the pin; a lug stud drawn by a motor-turned helical cam; Hirth faces carry torque | **M** - read: yaw and pitch servos inline. Differs: one joint, +-15 deg | L - Shen 2001 not read, capped | N | https://robots.isi.edu/conro/proto2H.html |
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
| Y1 ModLock | L - flat plates | **M** - read: "The faces are twisted 12 deg to align and tighten the connection"; "locking dowel ... snaps into a lock groove". Shared in kind: push in, twist, lock (bayonet class), passive hold. Differs: manual whole-module twist, snap dowel; no teeth on the face | N | L | N | https://www.modlabupenn.org/wp-content/uploads/ModLock.pdf |
| Y2 Zhang, Zhang, Gupta | L | **M** - read: "pushed along Slot 2 and rotated, it will be spring-backed to the position between two teeth, and the two modules are locked". Shared in kind: insert, rotate, lock against teeth (a detent). Differs: rotation by module joints, spring-back, slotted layers; no motor cam, no face pair | L | L | N | https://mdpi-res.com/d_attachment/robotics/robotics-06-00025/article_deploy/robotics-06-00025.pdf |
| Y3 RoFICoM | L - 50 mm round connector | **M** - read: "The motor rotates the clip, which then slides out of the body using pins driven by a helical slot in the body. The hooks slide under hooks in the mating clip". Shared in kind: a motor-turned ring moving in a helical slot to lock. Differs: the slot extends a hook ring, genderless hook to hook; no self-locking stage, no toothed face | N | L | N | https://rofi.fi.muni.cz/assets/files/publications/roficom.pdf |
| Y4 WPI twist-lock poster | L | **M** - read (thin): "A bayonet or quarter-turn mechanism". Shared in kind: a quarter-turn lock. Differs: nothing more is stated | L | L | N | https://users.wpi.edu/~cxu5/docs/MSEFPoster.pdf |
| Y5 CoBoLD | L | L - capped; secondary only | L | L | N | DOI 10.1109/ROBIO.2011.6181589 |
| Y6 RIMRES latch | L | L - secondary only | L | L | N | UCT thesis |
| Y7 LaMMos | N | L - motorized screw into a T-nut | N | N | N | https://arxiv.org/pdf/1801.00035 |
| Y8 Latching X-Face / DRAGON | L | L - passive compliant latch, chamfered pins and grooves, no serrations | N | L | N | https://www.modlabupenn.org/wp-content/uploads/latching_xface_overlay.pdf |
| Y9 Truss Link / VTT | N | L - magnets, servo latch | N | L | N | https://arxiv.org/pdf/2508.01829 |
| Y10 MODUR | L | L - read: lead-screw thrust then rotation to lock hooks; "continuing to provide thrust ... through friction", so power-held | L | L | N | https://arxiv.org/pdf/2510.13356 |
| Y11 tool changer | N | L - servo, cam and lock-pin; manipulator tool changer | N | N | N | https://arxiv.org/pdf/2603.04760 |
| Y12 Beckhoff arm module (US 12,290,920 B2) | N - industrial arm module, round | **M** - read: "face gearing 302 having four teeth, which is embodied as a Hirth joint"; "fastening ring 401 with an internal thread"; "centering pin 303". Shared in kind: a Hirth face pair on a modular-robot connector, pulled together by a turning ring, with a centering feature. Differs: 4 teeth vs 36; hand-screwed thread vs a motor-turned helical-slot bronze sleeve with a 3 deg self-locking stage; not self-reconfigurable | N | N - manual assembly | N | https://patents.google.com/patent/US12290920B2/en |
| Y13 Xerox PolyBot toy patent (US 6,605,914 B2) | L | **M** - read: "Each connector plate includes connector teeth 30 allowing for positioning of the module relative to its adjacent module ... eight teeth allow eight rotational positions". Shared in kind: a ring of teeth on a modular-robot connector face that fixes roll. Differs: 4 or 8 coarse indexing teeth vs 36 Hirth teeth that centre and carry zero-lash torsion. Counted with PolyBot (C12) for rule 2 | L | L | N | https://patents.google.com/patent/US6605914B2/en |
| Y14 Belke and Paik (TMECH 2019) | L - cylindrical genderless coupling inside an edge hinge of an origami module | **M** - read in full (cap lifted). Quotes in s1. Shared in kind: radial teeth on the front face of a modular-robot coupling, engaged with identical teeth, self-centering, "similarities to those of a Hirth joint", carrying torque with angled faces, and a self-locking condition from face angle and friction. Differs: genderless; planar-faced teeth "unlike a Hirth joint"; the slider is moved axially by an SMA spring and a passive spring on a square rail, not drawn by a motor-turned helical sleeve; the teeth are an overload release at a set torque (coupling disengages) whereas cand-d's teeth hold torsion without slip and the lugs on a bronze helical stage hold tension; the teeth transmit joint actuation. Not H: I do not find the same design in specific form | L - the coupling also transmits a hinge rotation (a joint through the coupling); cand-d's joint is inside the body | L - Mori origami modules | N | https://ieeexplore.ieee.org/ielx7/3516/8736910/08675300.pdf ; DOI 10.1109/TMECH.2019.2907802 |
| Y15 PetLock (HIT) | N | **M** - read: "So when mu > tan beta, the locking mechanism has the capability of self-locking" (push rod, pyramid, radial pins, beta 5 deg). Shared in kind: motor-driven lock held by a friction self-locking wedge angle. Differs: genderless, axial pyramid and radial pins, 5 deg; no helical sleeve, no Hirth teeth | N | L | N | https://arxiv.org/pdf/2209.04307 |
| Y16 Reach Robotics (US 11,376,730 B2) | N | **M** - read: "A plurality of protrusions 56 arranged in an annular array"; "a locking nut threadedly engaged". Shared in kind: bayonet-style annular protrusions and a rotating collar on a flanged modular connector. Differs: hand nut, sealed underwater manipulator modules; no teeth, no motor cam. Its flange is not screwed to a plate through lobes | N | N | N | https://patents.google.com/patent/US11376730B2/en |
| Y17 iBOSS iSSI / SIROM | N | L - capped (search summary only) | N | L | N | https://www-live.dfki.de/fileadmin/user_upload/import/10026_SIROM-IAC.pdf |
| Y18 KIST (US 10,160,121 and 9,853,386 B1) | N | L - read: a threaded fixing ring on a "fixing wing" of a genderless connector; no teeth | N | L | N | https://patents.google.com/patent/US9853386B1/en |
| Y19 CN110561486A | N | L - conical fit with screws, positioning pins; no teeth | N | N | N | https://patents.google.com/patent/CN110561486A/en |
| Y20 Ben-Tzvi (US 9,616,948) | L | L - T-mech shaft, C-mech clamps, non-back-drivable lead screw | L | L | N | https://patents.google.com/patent/US9616948B2/en |
| **Y21 Khoshnevis (USC) US 7,850,388 B2** | L - cylindrical module coupling | **M** - read: "a rotating drive mechanism, a hollow cylindrical body ... has at least one internal spiral channel, and at least one connector claw ... guided by the internal spiral channel"; the claws extend outward to engage a mating module. Shared in kind: a motor-turned cylinder with helical (spiral) channels moves the latching elements; same laboratory lineage as CONRO. Differs: genderless claws extending radially vs a gendered stud with lugs drawn axially; no teeth, no self-locking stage stated | L | L | N | https://patents.google.com/patent/US7850388B2/en |
| Y22 US 6,780,042 B1 | N | L - read: plug with lamellae and shoulders, actuators; no teeth | N | N | N | https://patents.google.com/patent/US6780042B1/en |
| Y23 US 11,654,548 B2 | L - two rotatable housings | L - read: a rotating ring with gear teeth driven by a bevel gear (drive teeth, not a face pair) | L | L | N | https://patents.google.com/patent/US11654548B2/en |
| Y24 ChainFORM, Makeblock Motionblock, ROBOTIS Bioloid, PMR | L - chain of servo modules | L - screws, brackets, magnets; summaries only | L | L | N | https://spectrum.ieee.org/automaton/robotics/robotics-hardware/modular-robotic-chain-is-whatever-you-want-it-to-be ; https://tams.informatik.uni-hamburg.de/research/3d-printing/pmr (search results only, not opened) |
| Y25 RhoMorph | N | L - docking of rhombus modules | N | L | N | https://arxiv.org/pdf/2601.19529 |
| Y26 ElectroVoxels | N - cubes | N - electromagnets | N | L | N | search result (https://www.hackster.io/news/a-joint-effort-in-modular-robotics-9d4984e3bc86), not opened |

Counts. High cells against F1 or F2 (A1, B1-B4): **0**. High cells in total: **0**. Moderate cells: **21** (listed in s0). Most moderates against one reference lineage: PolyBot four in C12 plus Y13 D2 counted with it, five. CONRO three. Belke and Paik one. No reference has a high.

## 5. Differentiation notes (Q61 s3 items 3 and 4)

No high cell, so no item-4 note. "Kept" means a feature forced by Family B or by the task.

**Hirth and toothed-face class (Y12 Beckhoff, Y13 Xerox, Y14 Belke and Paik).** The v2 review flagged this class. I re-read all three, with Belke and Paik in full.
- **Y14 Belke and Paik D2 (M, not H).** This is the closest reference to the coupler's face pair: radial teeth on a robot coupling, "similarities to those of a Hirth joint", self-centering, torque through the teeth, a self-locking condition, and the same research purpose (passive hold without power). Why not high: an informed observer would not call it the same design. Its teeth are planar-faced and explicitly "unlike a Hirth joint"; it is genderless; the toothed slider is pushed by an SMA spring and a return spring on a square rail; the teeth are designed to disengage at a set torque, and cand-d's are designed not to (zero lash, no slip, the lugs on a 3 deg bronze helical stage hold tension). cand-d keeps a true 36-tooth 90 deg Hirth pair with no SMA, spring or magnet. Not kept as a claim: nothing in the dossier may claim toothed faces on a modular-robot coupler as new.
- **Y12 Beckhoff D2.** Shared: a Hirth pair on connector faces, drawn together by a turning ring, with a centering feature. This is the nearest published "Hirth plus turning collar". Differs: 4 teeth vs 36; a hand-screwed thread vs a motor-turned helical-slot sleeve with capture and self-locking stages and a torque-stop seat; a rigid arm module vs a chain unit. M, not H, because the form and the principle of drawing differ. Kept: the Hirth pair, a generic machine element.
- **Y13 Xerox D2.** Shared: teeth ring on a connector face fixes roll. Differs: coarse, several allowed positions, latch separate; cand-d has one roll position and 36 teeth that carry torque. Counted with PolyBot for rule 2. Still no high.

**Bayonet, rotating-collar and cam-sleeve class (Y1 ModLock, Y2 Zhang, Y3 RoFICoM, Y4 WPI, Y16 Reach, Y21 Khoshnevis, Y12).** Shared in kind: push in, turn, lock; in Y3 and Y21 a motor-turned member with helical slots or channels. Differs:
- ModLock: manual whole-module twist, snap dowel.
- Zhang: the modules' own joints rotate; spring-back between teeth.
- WPI: poster, one line; nothing more to compare.
- RoFICoM: the helical slot extends a hook ring against a mating hook ring (genderless); no self-locking stage, no toothed face. It is the nearest published "motor plus ring plus helical slot".
- Reach: hand nut, sealed underwater manipulator; no teeth. v3's flange is a different feature (a lobed flange screwed through a plate).
- Khoshnevis: genderless claws pushed out by spiral channels; no teeth, no stated self-locking.
- cand-d: a dedicated motor turns a bronze sleeve with a 20 deg capture stage and a 3 deg self-locking stage, to a stall that seats a Hirth pair and absorbs the axial tolerance stack. The class is generic and the dossier does not claim novelty in it.

**Motor latch with unpowered hold (C4 ATRON, C6 Roombots, C17 HyMod).** Shared: motor-driven latch, held without power by a non-backdrivable element (lead screw, over-centre singularity, gearbox). Differs: hooks on arms (ATRON), crank to a singularity (Roombots), radial hooks (HiGen) vs lugs on helical slots held by friction self-locking (2.86x dry, 1.91x oiled, dossier). Kept: the non-backdrivable hold class, which is how G6 passive retention can be met.

**PetLock D2 (Y15).** Shared: a friction self-locking wedge in a motor-driven lock (mu greater than tan of the angle). Differs: a 5 deg pyramid pushing radial pins on a genderless face vs a 3 deg helical stage on a sleeve. The principle is generic and is named as `friction_wedge`.

**PolyBot (C12 D1, D2, D3, D4; Y13 D2).**
- D1. Shared: a rectangular two-port body with one joint between the ports. Kept: this is the Family B definition. Differs: aspect (a long head and an 8.8 mm tail vs matching halves), gendered ends vs hermaphroditic plates, the coupler axis offset from the body axis (3.3, 1.0). M, not H.
- D2. Shared: a pin entering a hole and locked by turning about the interface axis, no power to hold. Differs: SMA wires, spring, four-leg plate vs lug stud, helical sleeve, motor close and release, self-locking stage, fine Hirth ring.
- D3. Shared: one revolute joint per module. Differs: +-15 deg sector gear vs full-range hinge.
- D4. Shared: chains. Differs: chain only, no reconfiguration claim. Kept: chain-native is Family B.

**CONRO (D1, D2, D3).**
- D1. Shared: elongated, gendered ends, actuator between. Differs: two shell segments with a hinge inside the body. Kept: gendered inline ends are cand-d's choice (flagged in v1).
- D2. Shared: gendered pin-in-receptacle docking, unpowered hold. Differs: no SMA, no spring-closed latch, no groove on the pin; Hirth faces carry the torque. Khoshnevis (Y21, same lineage) differs as above.
- D3. Shared: servo revolute joints inline. Differs: one joint, small range.

**CKBot D3.** Shared: a servo revolute joint in a chain module. Differs: sector-gear joint inside a shell, +-15 deg. Kept: Family B.

**v3 changes (flange, nut blocks, wider slots).** No cell changes with them. A flange screwed to a plate is generic. I found no reference with the same form (Reach has a flange and annular protrusions with a hand nut; Beckhoff has a ring).

**Risk notes on capped cells (not ratings).** M-TRAN D1 and D3: the two-box body with a joint is the Family B shape, and a confirmed M would need a note (one joint vs two, gendered stud ends vs hook faces, no magnets). CoBoLD D2: a motor-driven worm-gear locking wheel with hooks would be M at most; four cone bolts and genderless vs a two-lug stud and a Hirth pair.

## 6. Exclusion checks (Q62 s3, recorded for G8)

1. **Cube with an internal flywheel (M-Blocks lineage): not present.** The body is an elongated two-segment prism, 47.2 x 25.4 x 24 mm, not a cube. The declaration's components (structure, energy_source, controller, actuator, coupler_mechanism, other) include no flywheel, brake or inertial actuator. Motion is by a geared joint, not impulse. The v3 parts (flange, nut blocks) are static.
2. **Needle- or particle-like silhouette: not present.** Site-to-site 47.2 mm, section 25.4 x 24 mm, aspect about 1.9 to 1, flange lobes to r 9.4. A tabletop block, not a needle and not sub-visible. Stowed sphere 58.862 mm (dossier). Design guidance s4.1's forbidden direction is not approached.

## 7. Family membership check (Q62 s3, Family B)

Constraint: "An elongated two-segment body with one internal revolute joint, so it is chain-native, with couplers at the segment ends." Checked against `declaration.json` v3 (`family` "B"):
- Two segments: `head-segment` (box half-extent x 16.3 at x 18.1) and `tail-segment` (half-extent x 3.8 at x -5.6), with end plates, separated by a 3.6 mm hinge gap. Yes.
- One internal revolute joint: one hinge pin (`hinge-pin`, dia 2), one gearmotor, pinion and sector (`joint-motor`, `joint-pinion`, `joint-sector`). The sleeve turn and Hirth seat are coupler motions, not a body joint. Yes.
- Elongated: aspect about 1.9 to 1 along the chain. Modest, and the tail is short, which the family text allows.
- Couplers at the segment ends: `site-head` at the head end (x 36.4, flange face) and `site-tail` at the tail end (x -11.6). Yes. The head flange and teeth protrude beyond the front plate but stay at the end.
- Chain-native: `chain` inline, `mating_roll_deg [0]`.
- Result: **cand-d v3 is a member of Family B.** Whether the joint bends a chain adequately (Q31) is not tested here. Membership is structural.

## 8. Fail-rule evaluation

- Rule 1 (any F1 cell high): none. A1 is N in every column. Not triggered.
- Rule 2 (two or more highs against one reference): there is no high against any reference. Nearest: PolyBot (five moderates counting Y13) and CONRO (three). Not triggered.
- Item 3 (every moderate has a differentiation note): done in s5 for all 21.
- Item 4 (every single high has a note, listed prominently): there are none.
- Item 5 (both exclusions recorded): done in s6.
- G8 (Q62): no high against F1 or F2, both exclusions not present. Satisfied.
- Completeness: every cell has a rating, a reason (short for N and L) and a source in its row. Capped cells are marked.
- Independence: the reviewer is a different agent session with no authorship in cand-d (Q61 s4). The declaration hash matches the expected value.

## 9. Recommended changes

No change is required for this review to pass. Advice only; any declaration change changes the hash and needs a new review (Q61 s5).
1. **Author:** do not claim novelty for a Hirth pair, toothed faces on a robot coupling, the bayonet or cam-sleeve class, or the friction wedge. If a claim is made, state it as the combination, with "no single published system found with all of these".
2. **Differentiation to keep in the dossier:** a true Hirth pair that holds torsion without slip (Belke and Paik's teeth release at a threshold), gendered lug stud, no SMA, no spring, no magnet. If a later version adds an SMA, a return spring, a planar-faced tooth, or a sliding toothed slider, re-review Belke and Paik and PolyBot D2 first.
3. **Corpus (owner or lead, by a decision record):** append Y1 to Y4, Y12 to Y16 and Y21 (ModLock, Zhang, RoFICoM, WPI poster, Beckhoff, Xerox, Belke and Paik, PetLock, Reach, Khoshnevis) to the corpus. This review does not edit the corpus.
4. **Reviewer follow-up (optional):** obtain M-TRAN III, CoBoLD, the CKBot module paper, Shen 2001 and iBOSS iSSI.
5. **Final visuals (Q61 s7):** D5 is rated only on declared materials. The exposed Hirth ring, bronze sleeve and flange lobes are visible features and need a fresh look.

## 10. Outcome

**pass.** No F1 high, no reference with two highs, no high cell at all, every moderate noted, both exclusions not present, Family B membership holds, the declaration hash matches. Pass means no Q61 fail rule was triggered by the references examined, with the capped cells listed in s1. It is not a claim of absolute originality. This review reduces copying risk and does not claim absolute originality.
