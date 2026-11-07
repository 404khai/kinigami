# Gate 1 paper-gate run 1

- Report: `run1-b1d0a81-ReleaseSafe.json` (code revision `b1d0a81`, `working_tree_dirty: false`, ReleaseSafe, Zig 0.17.0, aarch64-macos)
- Criteria: `criteria/gates/gate1-v1.json`, sha256 `ffe135329340…ddbf` (matches `criteria/REGISTER.md`)
- Label: **exploratory**. The paper gate is **not feasibility evidence**. It screens declarations on paper; it validates no mechanism, solver or physical behaviour.
- Note: the report prints `protocol_revision 1`. Q63 (rev. 2) clarifies the protocol; the evaluator output was not changed.

## Outcome

| Candidate | Overall | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cand-a v1 | **unresolved** | pass | pass | unresolved | pass | pass | unresolved | pass | pass |
| cand-b v1 | **fail** | pass | pass | unresolved | pass | **fail** | unresolved | unresolved | unresolved |
| cand-c v1 | **fail** | pass | pass | unresolved | pass | **fail** | unresolved | unresolved | unresolved |

**Survivors: none.** A candidate proceeds only if every item passes. Unresolved is not a pass.

## Values

| | cand-a | cand-b | cand-c |
| --- | --- | --- | --- |
| G1 stowed diameter (limit 60 mm) | 59.060 mm | 55.498 mm | 59.000 mm |
| G4 declared mass | 39.814 g | 34.559 g | 60.656 g |
| G4 peak power / limit | 2861 / 19425 mW | 9594 / 13875 mW | 6298 / 49950 mW |
| G4 average power | 160 mW | 195 mW | 436 mW |
| Endurance (reported only, no threshold) | 29137.5 s | 17076.9 s | 9165.1 s |
| G2 pairs tested | 153 | 66 | 91 |
| G5 | supported at roll 0° | no supported chain (rolls 0°, 180°) | no supported chain (rolls 0°, 90°, 180°, 270°) |

Power margin = limit minus peak: cand-a 16564 mW, cand-b 4281 mW, cand-c 43652 mW. Endurance is `mJ / mW` (seconds) per Q63; it does not enter the outcome.
cand-a's stowed diameter has only 0.94 mm of margin to the limit.

## Unresolved items

- **G3 (all three):** the mass, dimension or power basis of many components is flagged as estimate. Per-component reasons are in the JSON. cand-a: controller, kick-driver, release SMA wires, unresolved-bucket. cand-b: latch-mech, sma-wire, pogo-block, controller, boost, shells, wiring. cand-c: shell halves, controller, motor-driver, head-servo, head-ram and tail-socket cartridges, chassis-frame, pole hardware.
- **G6 (all three):** independent retention review is `unresolved`; the dossiers do not size the retention and alignment features.
- **G7 (cand-b, cand-c):** originality review `unresolved`. **G8** is `review_incomplete` for the same candidates.

## Candidates and reasons (kept per SEL-007)

### cand-a (family A, hexagonal tumbler): unresolved
No failed item. Blocked by G3 estimates and G6. G7/G8 pass, with moderate cells against M-Blocks and 3D M-Blocks, and a newly found hexagonal electrohydraulic module reference rated provisionally.
Revision would need: (1) replace the estimate bases in G3 with evidence; (2) size the ball-lock, spring preload, release-wire force balance, cone angle, chamfer and tolerances, and estimate the capture window; (3) state the tumbling axis and show chain alignment through a step; (4) resolve the rigid key-and-lock versus chain-bending conflict (Q31); (5) re-review locomotion and visual ratings once designed. A coupler change needs a new version and a fresh review.

### cand-b (family B): fail
G5 fails: no mating roll gives a supported chain, in the dossier's own stowed pose. Also unresolved on G3, G6, G7, G8.
Revision would need: (1) a geometry or pose where a chain is statically supported at some roll; (2) the missing groove, hook, spring, funnel and friction dimensions and a capacity estimate for the 1.5 mm PA12 walls; (3) address CONRO D2 (rated high, SMA-released spring latch) by changing the release principle or recording a rationale; add CONRO to the corpus by decision record; (4) G3 estimates; (5) an r2 originality review reading the primary papers for M-TRAN, PolyBot, CKBot, SuperBot, Sambot and CONRO.

### cand-c (family C, pendulum sphere): fail
G5 fails at all four rolls tested. Also unresolved on G3, G6, G7, G8.
Revision would need: (1) a geometry where a chain is supported at some roll; (2) jaw, throat, spring rate, preload, retention force, funnel angle and capture window; servo retraction force and a mechanism for the 9 mm ram stroke; (3) differentiate from pendulum spheres (PenduMorph, Rotundus, Sphero/BB-8, SnailBot, MOPARAS), reading the Rotundus patent and PenduMorph paper, since D1 vs Rotundus could reach high and fail rule 2; (4) re-rate visual identity once finish exists; (5) add the new references to the corpus by decision record; (6) G3 estimates.

## Problems found

- The report states protocol revision 1 although Q63 made revision 2 current.
- Reviews for cand-a use corpus summaries and search results for some references; primary sources were not all read, so some ratings are provisional.

# Gate 1 paper-gate run 2

- Report: `run2-3e3d63b-ReleaseSafe.json` (code revision `3e3d63b`, `working_tree_dirty: false`, ReleaseSafe, Zig 0.17.0, aarch64-macos)
- Criteria: unchanged `criteria/gates/gate1-v1.json`, sha256 `ffe135329340…ddbf`. Protocol rev. 2 (Q63); the report still prints `protocol_revision 1` (Q64 §4).
- Candidates: cand-a **v2** (Q66; v1 kept as `declaration-v1.json`, Q65). cand-b v1 and cand-c v1 are re-evaluated unchanged.
- Order: candidate `5624161` → reviews `3e3d63b` → this evaluation. Label: **exploratory**. This is not feasibility evidence.

| Candidate | Overall | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cand-a v2 | **unresolved** | pass | pass | pass | pass | pass | unresolved | pass | pass |
| cand-b v1 | **fail** | pass | pass | unresolved | pass | **fail** | unresolved | unresolved | unresolved |
| cand-c v1 | **fail** | pass | pass | unresolved | pass | **fail** | unresolved | unresolved | unresolved |

**Survivors: none.**

cand-a v2 values:

| Item | Value |
| --- | --- |
| G1 | D = 58.181 mm against the 60 mm limit, margin 1.819 mm (v1: 0.94 mm). The sphere is set by the hexagon corners |
| G2 | 1326 pairs tested, no interference |
| G3 | every component cited, no estimate basis (v1: 13 flags) |
| G4 | mass 36.550 g. Peak 8899 mW against a 19 425 mW limit, margin 10 526 mW. Average 2684 mW. Endurance 1737 s, reported only |
| G5 | supported at roll 0° |
| G7, G8 | originality pass with two single highs, both D2: CONRO (Q64-C21) and PolyBot (C12), for SMA-released latches on grooved pins |
| G6 | retention review **unresolved**. The toggle's over-centre geometry and spring direction are not defined, and whether it is bistable or monostable is not settled. The tension path leaves about 0.1 mm of PA12 wall. The puck bearing is not declared |

cand-b and cand-c results are identical to run 1.

Revision needs for a v3 of cand-a are listed in `candidates/cand-a/retention-review-v2-r1.md` §6 and in Q67.

# Gate 1 paper-gate run 3

- Report: `run3-447dc70-ReleaseSafe.json` (code revision `447dc70`, `working_tree_dirty: false`, ReleaseSafe).
- Criteria: unchanged `gate1-v1`, sha256 `ffe135329340…ddbf`.
- Candidates: cand-a **v3** (Q68). v2 is preserved as `declaration-v2.json`. cand-b v1 and cand-c v1 are unchanged.
- Order: candidate `6fc276b` → reviews `447dc70` → this evaluation.
- Label: **exploratory**.

| Candidate | Overall | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cand-a v3 | **fail** | pass | pass | pass | pass | pass | **fail** | pass | pass |
| cand-b v1 | **fail** | pass | pass | unresolved | pass | **fail** | unresolved | unresolved | unresolved |
| cand-c v1 | **fail** | pass | pass | unresolved | pass | **fail** | unresolved | unresolved | unresolved |

**Survivors: none.**

cand-a v3 values:
- **G1:** D 58.181 mm, margin 1.819 mm.
- **G2:** 2145 pairs tested, no interference.
- **G4:** 41.849 g. Peak 4807 mW against a 19 425 mW limit. Average 2899 mW.
- **G7, G8:** pass. The only high cell is Roombots D2 (over-centre lock principle). CONRO and PolyBot D2 dropped to moderate.
- **G6:** the retention review **fails**. The roll-in channel is cut on the mirror-image arc. A peg on the common axis enters at B's opposite bottom vertex and travels the lower arc about the pivot vertex. The declared slots, from the mid-height vertices over the top, are never on that path. The same error is in v2 (its review missed it).
- **Retention mechanism:** the keeper four-bar, the tension path and the stops are reproduced by the reviewer and supported on paper.

# Gate 1 paper-gate run 4

- Report: `run4-e5c6521-ReleaseSafe.json` (code revision `e5c6521`, `working_tree_dirty: false`, ReleaseSafe).
- Criteria: unchanged `gate1-v1`, sha256 `ffe135329340…ddbf`.
- Candidates: cand-a **v4** (Q70). v3 is preserved as `declaration-v3.json`. cand-b and cand-c are unchanged.
- Order: candidate `b03ffbd` → reviews `e5c6521` → this evaluation.
- Label: **exploratory**.

| Candidate | Overall | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cand-a v4 | **unresolved** | pass | pass | pass | pass | pass | unresolved | pass | pass |
| cand-b v1 | **fail** | pass | pass | unresolved | pass | **fail** | unresolved | unresolved | unresolved |
| cand-c v1 | **fail** | pass | pass | unresolved | pass | **fail** | unresolved | unresolved | unresolved |

**Survivors: none.**

cand-a v4 values:
- **G1:** D 58.181 mm, margin 1.819 mm.
- **G2:** 2775 pairs tested, no interference.
- **G4:** 41.741 g. Peak 4807 mW against a 19 425 mW limit.
- **G5:** supported at evaluator roll 180°, which is a physical relative roll of 0 under the shortest-arc mating convention (Q70 §3).
- **G7, G8:** pass. The single high is Roombots D2.
- **G6:** the retention review is **unresolved**, not fail.
  - **Corrected and reproduced:** the roll-in kinematics are correct, and the four-bar, torsion and release figures were reproduced by the reviewer.
  - **Unsupported:** class f is applied to a pivot, stops and crank axis that sit in PA12; at ±0.3 mm the stroke falls to 4.41 mm against 4.6 mm needed.
  - **Unsupported:** closure depends on a 0.05 mm vertical stack that ignores the SLS height tolerance of both units.
  - **Unsupported:** the windows are stated at the slot, not at the jaw.
  - **Unsupported:** the flat thrust washer allows only about 3° of yaw under tension.

# Gate 1 paper-gate run 5

- Report: `run5-93b3aa3-ReleaseSafe.json` (clean tree `93b3aa3`, ReleaseSafe).
- Criteria: unchanged `gate1-v1`, sha256 `ffe135329340…ddbf`.
- Candidates: cand-a **v5** (Q72). v4 is preserved as `declaration-v4.json`. cand-b and cand-c are unchanged.
- Order: candidate `f13f8b8` → reviews `93b3aa3` → this evaluation.
- Label: **exploratory**.

| Candidate | Overall | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cand-a v5 | **fail** | pass | pass | pass | pass | pass | **fail** | pass | pass |
| cand-b v1 | **fail** | pass | pass | unresolved | pass | **fail** | unresolved | unresolved | unresolved |
| cand-c v1 | **fail** | pass | pass | unresolved | pass | **fail** | unresolved | unresolved | unresolved |

**Survivors: none.**

cand-a v5 values:
- **G1:** D 58.181 mm.
- **G2:** 2926 pairs tested, no interference.
- **G4:** 42.905 g. Peak 4807 mW against a 19 425 mW limit.
- **G7, G8:** pass, with the single high Roombots D2.
- **G6:** the retention review **fails**.
  - **Torsion has no carrier:** once the vertical free play exceeds 0.62 mm (43% of the declared 0.05–1.05 mm), the declared torsion load is carried by nothing.
  - **Jaw window too small:** the open-jaw window at the class-f minimum stroke is 0.087 mm (the dossier said 0.104), below the declared ±0.35 mm stack.
  - **What still holds:** tension retention, the machined frame, the four-bar margins and the cylindrical thrust are supported.
