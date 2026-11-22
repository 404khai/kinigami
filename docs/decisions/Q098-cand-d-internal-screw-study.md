# Q98 — Do not freeze the captive-screw jaw layout

| Field | Value |
| --- | --- |
| Status | accepted study disposition; no candidate revision authorized by this record |
| Recorded | 2026-11-20 |
| Supersedes | — |
| Provenance | **agent decision under explicit owner delegation** |

**Decision:** keep Q12, Q85 and Gate 1 v1. Retain the captive M2.5×0.35 screw as a *packaging study*, not a v7 design. [Run 11](../../results/gates/gate1-v1/run11-2b8ea96-ReleaseSafe.json) remains the official result: no survivor. Do not archive or regenerate a candidate merely to repeat a known G6 failure.

| V6 review item | Successor studied | Disposition |
| --- | --- | --- |
| One loaded cam lug; steep release can bind | Positive radial jaws driven by an internal screw on 12° loaded/35° free tracks; no cross-start into a mate | The 1.10 mm layout fails the stroke requirement. A 3.530 mm layout fits a 59.762 mm *partial inventory* sphere, but only 0.050 mm clearance is available before switching to fast motion. Loaded offset, draw history and loaded breakaway are not bounded by that fit. |
| Contact load split, rocker indentation, mating tilt | Three V seats and a central, flat-backed stud. Spring-limited seating compared with a positive-clearance retainer. | Full-seat frictionless equilibrium exists for plausible draw. Partial contact is different: five V flanks plus one lip admit a zero-external-wrench self-stress at μ≤0.18 in the clearance model. A finite lash calculation is not a clamping-force limit. |
| Retainer, actuator mounting and structural reaction | Opposed complete thrust races, independently journalled rotor and bench-installed floating spline drive; metal nose extended by 0.80 mm | Retain this section as a starting point. The studied single-jaw follower and bridge see >1.2 and ~1.45 GPa nominal bending. A thicker but unswept rib does not resolve interference, root stress or single-edge bearing load. |
| Jam, power and sensing | Separate working/stall ratings, nut/sleeve/jaw indication, endpoint dogs and bidirectional trip studied | At 200 N·mm input and μthread=0.20, the no-other-loss screw screen gives 622 N against 526 N static on the small race. This is a conditional fault screen, not an impact cap. No packaged two-way release/trip or bound on trapped load after a midstroke obstruction. A stop dog only addresses travel endpoints. |
| Positive release at the mating faces | Flared well, shielded jaw windows and independent centred ejector | A rounded probe can clear; a retaining shoulder may hook an exposed window. Proving disengagement needs a full-profile swept section, actual force/travel and local indications. A head that has only turned its screw is not released. |

The [sizing studies and reproducible counterexample](../studies/cand-d-internal-screw/README.md) give specific restart conditions. The direct 4:1 planetary and parallel offset screw do not yet furnish a rated, protected alternative. No universal 60 mm infeasibility follows from these results. R10 remains blocked; no change to thresholds, protocol, previous declarations/reviews or solver. A later candidate requires a separate revision decision, archived declaration, integrated dossier, fresh reviews and clean official run in that order.
