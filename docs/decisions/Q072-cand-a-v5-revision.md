# Q72 — cand-a version 5: revision decisions

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-07 |
| Supersedes | — (revises a candidate; changes no criterion, threshold, protocol or verdict; Gate 1 under unchanged `gate1-v1`) |
| Provenance | **agent decision under explicit owner delegation** (owner chose v5 on 2026-11-07 and asked to keep the phase short). Lead Claude Opus 5.5, implementation Claude Sonnet 5.5 |

## Decision (answers retention review v4 r1 §7)

1. **One machined 304 frame (ISO 2768-1 class f, size rule)** on the end-plate middle piece. It carries:
   - the rocker pivot and both crank stops;
   - the M3 crank-side bearing;
   - the yaw-shaft bearing;
   - a 304 thrust saddle.

   Four-bar margins are 5.64° open and 6.09° closed. The stroke is 5.09–6.07 mm against 4.6 mm needed. With frame and pin play, the margins are 1.7° and 3.6° and the stroke is at least 4.63 mm.
2. **No flexure.** A 304 flexure cannot absorb 0.7 mm of stack at this size. The jaw closes to a fixed, frame-set height. The stack becomes a declared vertical free play of 0.05–1.05 mm. An exact escape check shows the peg stays captured at every corner.
3. **Thrust.** A convex 304 collar runs on a concave 304 saddle, coaxial with the yaw axis, so contact holds through ±12° yaw. Contact stress is about 33 MPa.
4. **Release rule.** Releasing at the μ = 1 bound with both friction faces needs 1.07× stall, so release is blocked there (CPL-008). Release is allowed at chain tension ≤ 0.52 N.
5. **Accepted and reported:**
   - Roll lock is **not guaranteed** at the loose corner (free play > 0.62 mm makes the lash unbounded). Torsion is then held only by the units resting on the table.
   - The jaw's open clearance is 0.10 mm at the size-rule worst corner.
   - The seat is not registered to the frame.
   - Several joints are undesigned (collar-to-column, saddle window, collar +y restraint, jaw guide).
   - Hertz stress at the peg corners is above first yield.
   - The yaw envelope is μ ≤ 0.96 at rated torque.
6. **Records.** v4 is preserved as `declaration-v4.json` (sha256 f6c18f80…). If v5 does not pass Gate 1, the lead reports to the owner and does not start v6 unasked.
