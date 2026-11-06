# Q68 — cand-a version 3: revision decisions

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-06 |
| Supersedes | — (revises a candidate; changes no criterion, threshold, protocol or verdict; Gate 1 under unchanged `gate1-v1`) |
| Provenance | **agent decision under explicit owner delegation** (owner approved v3 on 2026-11-06). Lead Claude Opus 5.5, implementation Claude Sonnet 5.5 |

## Context

cand-a v2 is `unresolved` on G6 (Q67). v3 answers the six items of the v2 retention review and the originality residual risk. It is a candidate proposal under Q38, not a design selection.

## Decision

1. **Tolerance rules.**
   - SLS PA12 accuracy is ±0.3% with a lower limit of ±0.3 mm (Materialise PA12 SLS page), with a minimum wall of 1 mm.
   - No functional PA12 clearance is below 0.6 mm, and no PA12 wall below 1.0 mm.
   - PA12 carries no gear teeth: the lift-ring teeth move to a 304 band.
   - All precision coupler parts are machined 304 to ISO 2768-1 class f.
2. **Keeper.** The SMA wire, spring and trip are removed. A third PMD 206-109 (M3) drives the tongue through a crank-rocker four-bar:
   - crank r 2.0, link L 10.22, rocker arms 3.0 and 4.5, pivot at (1.5, 13.3);
   - two hard stops 10° past the folded and extended dead centres;
   - at either stop, tongue loads push the crank into its stop, so both states hold with no power and no spring;
   - the lock offsets are 0.28 mm and 0.41 mm, with at least 6.1° of margin at the class-f tolerance corners.

   Rationale: the v2 review found the spring toggle undefined and its force balance incoherent, and Q67 §4 preferred a release principle other than an SMA latch.
3. **Roll lock.** A full hex-in-hex fit (304 cup insert plus a jaw on the keeper, 4.10 A/F against the 4.0 A/F peg) replaces the PA12 half-hex cup. Free roll drops from about ±25° to ±2.6°.
4. **Tension path.** Engagement goes to 6.5 mm, with the groove 5.1 mm inside the neighbour's face. The puck front wall is 1.0 mm. Tension thrusts the puck onto end plate b. The puck is journalled in a bore in the cap halves. The yaw shaft becomes 304 and hollow.
5. **Windows.** The channel is 5.8 mm wide, leaving at least 0.44 mm clearance per side at the SLS minimum. No axial or heading pre-alignment exists, and the dossier says so: docking needs a common lane.
6. **Accepted costs, reported, not hidden:**
   - mass 41.85 g;
   - yaw torque at the μ = 1 bound is 0.96× rated, so bending at rated torque holds only for table μ up to 0.96;
   - release under the full μ = 1 bound tension needs near-stall torque (0.60× rated, 1.81× stall);
   - Hertz stress at the hex corners is above first yield at the bound torsion.

## Alternatives considered

- **Keep the spring toggle and define its geometry:** this keeps the SMA latch principle rated high twice. Rejected.
- **Release by yaw overtravel:** already rejected in Q66 §4.
- **The 699:1 206-10C for M3, for more torque:** at 24.4 mm it does not fit the 24 mm cavity. Rejected.

## Consequences

v3 is evaluated under the unchanged criteria after new independent r1 reviews. v1 and v2 stay preserved: `declaration-v1.json`, and `declaration-v2.json` (sha256 b7a6e94d…, equal to its reviews).
