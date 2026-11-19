# Q85 — Keep the Q12 envelope; start a coupler-first Family B candidate (cand-d)

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-20 |
| Supersedes | — (changes no requirement, criterion, threshold or verdict; answers the scope question Q84 §3 left open) |
| Provenance | **agent decision under explicit owner delegation**. The owner delegated all decisions until a candidate passes Gate 1, without changing criteria to obtain a pass. Lead: Claude Opus 5.5 |

## Context

Q84 stopped cand-a coupler revisions after nine attempts and left three options: (A) revise cand-b or cand-c, (B) revisit scope, for example the Q12 60 mm envelope, (C) a new candidate that budgets the coupler first. The owner has now delegated that choice.

cand-a's coupler failures share one cause. One 40 mm cavity holds the cell, the controller, three motors, and the roll-in, yaw and keeper mechanisms. Because chain bending (the yaw turntable) and locomotion (roll-in docking) are both coupled into the coupler, every coupler part sits inside a tolerance stack that runs through PA12 parts.

## Decision

1. **Q12 and `gate1-v1` stay unchanged.** The G1 limit stays 60 mm. No new criteria version is registered.
2. **Open a new candidate, `cand-d`, in Family B** (Q62 §3: an elongated two-segment body with one internal revolute joint, couplers at the segment ends). It is designed coupler-first:
   - Chain bending lives in the internal joint, so the coupler is rigid and has no articulation duty.
   - The coupler's closed load loop is machined metal only. PA12 carries mounting loads, never the preload.
   - Axial tolerance is absorbed by drive travel to a torque-limited stop, not by a fixed stroke or free play (Q83 lesson 1).
   - Every declared load (tension, torsion, both bending axes) has a named geometric carrier at every declared tolerance corner (Q83 lesson 2).
   - No SMA release, no spring-closed latch, no magnet, and no crank driven to a singularity. These are the corpus principles behind the CONRO, PolyBot, Roombots and A1 risks (Q83 §2 item 5).
3. cand-d is a structurally different Family B member, not a revision of cand-b. cand-b's Z-link offset, plug and hook latch are not reused. cand-b v1 and cand-c v1 stay as recorded (`fail`). Q62 §3 allows two candidates in one family when they differ structurally, and the reviewer checks this.
4. Order, provable from git history: this record, then the cand-d declaration, dossier and scripts (one commit), then the independent retention and originality reviews (fresh agent sessions with no authorship), then an official `kinigami-gate1` run from a clean tree, then a disposition record.
5. Stop rule. If cand-d fails G6 on a root cause that a further version cannot remove inside 60 mm, the lead records that, with numbers, and does not force a pass.

## Alternatives considered

- **(B) Raise Q12 to about 70 mm (new G1 limit in a `gate1-v2`).** Rejected, for four reasons:
  - Q12 is a direct owner charter instruction (ENV-004), and Q37 ties the size class to it.
  - Changing it after nine coupler failures would be a threshold moved to fit a known design. That is the pattern the owner excluded.
  - It does not remove cand-a's G6 defects. Those are a tolerance stack through PA12 and torsion carried by free play, not lack of volume alone.
  - Every candidate would need re-running against criteria they were not designed for.
- **(A) Revise cand-b.** Rejected as a revision. Its Z-link offset forces 180° roll alternation, its fold sweep has zero clearance, and its plug-and-hook latch is the CONRO-high principle. Little survives.
- **(A) Revise cand-c.** Rejected. A near-spherical shell gives a one-point table contact, so G5 support needs added feet that conflict with its rolling locomotion. Its pendulum drive also carries the Rotundus and PenduMorph risks.
- **(C) A new Family A candidate.** Not now. Family A docks by rolling, so the coupler again takes a lateral entry, an open channel and an articulation duty (Q83 K2).

## Consequences

- Candidate work resumes (Q74 pause lifted for cand-d only). Solver, criteria and regression gates are untouched.
- cand-d's approach locomotion (how a free unit reaches a neighbour) is not a Gate 1 item. If cand-d does not design it, its dossier must say so, and it must claim no capture window (CPL-006).
- R10 stays blocked until a candidate passes Gate 1.

## Revision notes

- None.
