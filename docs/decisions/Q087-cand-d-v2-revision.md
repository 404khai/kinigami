# Q87 — cand-d version 2: revision decisions

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-20 |
| Supersedes | — (changes no criterion, threshold or verdict; v1 and its records are preserved) |
| Provenance | **agent decision under explicit owner delegation**. Lead: Claude Opus 5.5 (cand-d author) |

## Context

The v1 retention review (`candidates/cand-d/retention-review-v1-r1.md`) left G6 `unresolved` and listed nine items (§6). Q86 started v2. The family, body, joint and envelope are unchanged. Only the coupler and its records change.

## Decision (review item → v2 change)

1. **Cartridge mount (item 1).** The radial screws into the 0.8 mm lip are removed. The 304 housing gets two tapped ears (M1.6, 1.6 thick) behind the front plate. Countersunk A2 M1.6 screws pass through the plate into the ears:
   - Pull-out bears the ears on the plate's inner face.
   - Push-in bears the screw heads on the plate.
   - The moment goes through the ear pair (lever 7.4 mm).
2. **Flange against the window (item 2).**
   - Flange r 6.3, smaller than the lip and window (r 6.45).
   - The stack is split into every term (Hirth teeth on both parts, lip, PTFE ring, sleeve) at ISO 286 IT9 for the critical axial sizes.
   - The cartridge position and plate flushness are shown to set only the PA12 gap (0.3 mm minimum).
3. **Stops and retainer (item 3).**
   - A 304 rear retainer collar is pressed on the housing tube and takes the ejection reaction.
   - A 304 stop pin (dia 1) in the lip runs in an arc groove of the sleeve face. It is the open stop and the over-travel stop.
4. **Walking (item 4).** Option (b) of the review, a stop to walking that does not rely on friction. Torsion and shear are carried by a 36-tooth 90 deg Hirth face pair on the stud flange and the housing lip, with zero lash under preload. Roll cannot change without axial separation, so the lugs never slide along the cam flank, and face friction is not relied on. The pilot becomes an entry guide (bore 4.10), and the teeth centre the seat.
5. **Contamination treated alike (item 5).** Oil cases are computed for the flank, the release and the contact stress. The Hirth carrier removes the face-friction dependence.
6. **Alignment stack (item 6).**
   - Pitch, roll and yaw windows are stated.
   - Joint angles are shown not to enter the coupler pose, because each segment is rigid.
   - The axial push is stated as external (Q31 start configuration, or a later approach design), with stroke and force.
7. **Citations (item 7).**
   - Flank friction is Wikipedia Leadscrew only (dry 0.15 to 0.23). The 0.35 value is withdrawn.
   - Every cited number is checked in the raw source.
   - The roll window is quoted at the lug tip radius.
   - `mechanism_kind` is `friction_wedge`.
8. **Load combinations (item 8).** Each load is evaluated alone, then all declared loads at once (an upper bound). Under the combination the faces may gap at one edge, but the units do not separate.
9. **Release supply (item 9).** Release is allowed only with the cell at 3.5 V or more (3.4 V at the motor). Closing is at 1.0 V.

Consequential geometry changes:
- Sleeve OD 6.0 → 6.3 and lug tip r 5.9 → 6.2, for a longer flank line (2.65 mm) and a lower Hertz pressure.
- Mass 30.247 → 31.109 g.

## Order

This record, then the v2 declaration, dossier and scripts (`declaration-v1.json` keeps v1), then fresh independent retention and originality reviews of v2 (new sessions, no authorship), then an official run.

## Alternatives considered

- **Raise the preload so face friction holds torsion at every corner** (review item 4 (a)). Rejected. It needs a cited lower bound on the motor constant, which the datasheet does not give, and it raises lug contact stress above the bronze onset.
- **A spring detent on the sleeve.** Rejected. A spring-held latch element moves toward the CONRO / PolyBot D2 principle (Q83 §2 item 5).
