# Q99 — Separate the six retention coordinates in cand-d v7

| Field | Value |
| --- | --- |
| Status | accepted revision direction; not a gate verdict |
| Recorded | 2026-11-20 |
| Supersedes | Q95/Q96's rotary lug cartridge for cand-d v7 only; those records and Q97's adverse result stand. Q98's captive-screw layout is not adopted. |
| Provenance | **agent decision under explicit owner delegation** |

Implement and review a clearance-set mechanical keeper, not another preload clamp. In the [v6 review](../../candidates/cand-d/retention-review-v6-r1.md) one lug could carry the entire load, pressure depended on how the joint had been tightened, and the steep release flank could self-bind. In [Q98](Q098-cand-d-internal-screw-study.md) even a nominally loose central stud and three V grooves admitted internal force with no external wrench. A stronger screw does not fix that.

1. **Retention:** place three radially supported crowned members on the tail, spaced at 120°. At each site a pair of parallel axial stops bounds one axial coordinate and a pair of parallel tangential cheeks bounds one tangential coordinate. Intentionally leave positive clearance at both opposite pairs, including elastic and machining error. These three axial plus three tangential constraints have different moment arms. Name the carriers for tension, compression, transverse load, twist, pitch and yaw. Quantify backlash and facet extents. No requirement for six simultaneous contacts or force-sharing. No screw, central draw stud, V clamp, spring-closed latch or magnet.
2. **Actuation:** the head motor moves metal keepers *transversely* across the free axial poles, not past a force-dependent axial tightening point. Provide a positively backed zero-lift closed dwell and positive reverse drive. Size the rear drive, torque reaction, radial and thrust support and removable facing plate. The tail need not be powered. Size a positively sequenced axial withdrawal **after** mechanical clearance under the load; distinguish opening a keeper from actually releasing the faces. Check the torque on the loaded slide/cam, one contact at a time, with all guide reactions.
3. **Alignment:** controlled prepositioning only; tell how the members pass the entries and what can move a body against tabletop friction. Account for finite throat edges, first/last engagement, tangential, tilt and axial offsets, backlash, full-mass service wrench and passive retention after power loss. No autonomous capture envelope. An obstruction may be rejected, but a jam is never reported as a lock or release.
4. **Fault and force:** test the six-coordinate wrench map including friction at the actual contact patches and all admissible signs; if no finite bound or rated release emerges, state that explicitly. Do not treat a cube-corner SAT pass as a fit for every moving component, a stall figure as a motor rating, or missing data as zero. Use actual output-state indicators, not motor travel alone.
5. **Sequence:** preserve v6's declaration, dossier, reviews and run 11. Regenerate the v7 declaration from scripts, integrate the actual mechanism/mass/power/chain, run the draft, get two fresh independent reviews against the immutable version, commit reviews, run the official evaluator clean and record the disposition. Q12, Q31, Q36, Q61, Q62, Q85, the criteria and all thresholds remain unchanged.

If part of this revision fails, preserve the numerical reason. Q99 does not declare a Gate 1 pass or a universal envelope no-go.
