# Q89 — cand-d version 3: revision decisions

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-20 |
| Supersedes | — (changes no criterion, threshold or verdict; v1 and v2 and their records are preserved) |
| Provenance | **agent decision under explicit owner delegation**. Lead: Claude Opus 5.5 (cand-d author) |

## Context

The v2 retention review (`candidates/cand-d/retention-review-v2-r1.md` §7) left G6 `unresolved` with seven items. Q88 started v3. The body, joint, envelope, cam and Hirth faces are unchanged.

## Decision (review item → v3 change)

1. **Ears joined to the housing (item 1).** The mounting ears and the flush lip are removed. The 304 housing is one turned part: a tube and a **front flange** (disc r 7.0, 0.8 thick, lobes at ±z to r 9.4). The flange lies on the PA12 front plate's outer face, and its front face carries the head Hirth ring. Two countersunk M1.6 A2 screws pass through the lobes and the plate into two tapped 304 nut blocks behind it.

   The cartridge moves 0.8 mm forward. The sleeve passes the plate window, and the thrust face is the flange's rear face. The head site moves to x 36.4. All cam depths are measured from the pitch plane and do not change.
2. **In-plane lever (item 2).** In-plane bending pivots the flange on its disc edge (lever 7.0 mm), and both screws hold. Out-of-plane bending pivots on a lobe tip, with the far screw at 17.2 mm. The fault case is sized.
3. **Window and flange (item 3).** The flange bears on the plate's outer face. Plate position and flushness set only the PA12 gap (0.7 mm minimum outside r 6.3).
4. **Phase tolerance (item 4).** The lug slots widen to 3.20. With IT9 on tooth and slot positions of both parts of both units, the phase is ±1.22 deg, against 2.61 deg of slot lash at the inner radius. With the teeth seated the lugs keep at least 1.39 deg of clearance, so torsion goes only through the teeth. Before the teeth meet, the slot lash (≤ 3.12 deg) stays below half a tooth pitch.
5. **F_p lower bound (item 5).** The datasheet's guaranteed rows (rated 3 mN m at 3 V; maximum start voltage 0.5 V) give stall ≥ 1.2 (V − 0.5) mN m, so F_p ≥ 0.88 N at 1.0 V. Tooth engagement and roll are shown to be independent of F_p:
   - an axial load 20 N above the preload opens the faces by at most 1 µm against 0.39 mm teeth, while the self-locking stage holds;
   - F_p decides only face contact, and that is reported at both the typical and the lower-bound values.
6. **PTFE notch, Hirth area, tipping lever (item 6).** The PTFE ring has two lug notches and is keyed by them. The lug slots remove 33 % of the head ring, so the in-plane tipping edge is at y 5.90.
7. **Pilot margin (item 7).** The bore chamfer goes from 0.6 to 0.4, giving a 0.20 mm margin. The lateral window is ±0.95 mm against the ±0.6 mm stack.

## Order

This record, then the v3 declaration, dossier and scripts (`declaration-v2.json` keeps v2), then fresh independent retention and originality reviews of v3, then an official run.

## Alternatives considered

- **Close the coupler to a sensed current, to bound F_p tightly.** Not needed for retention once tooth engagement is shown to be independent of F_p. It is also not boundable without a cited motor-constant tolerance.
- **A spring element to set the preload by deflection.** Rejected. It is not needed, and it moves toward the spring-latch principle (Q83).
