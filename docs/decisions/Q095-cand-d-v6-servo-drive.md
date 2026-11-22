# Q95 — cand-d v6: isolate actuator torque from seating preload

| Field | Value |
| --- | --- |
| Status | accepted design direction, not a gate result |
| Recorded | 2026-11-20 |
| Supersedes | Q93's candidate implementation only; no governing requirement or evaluation changes |
| Provenance | **agent decision under explicit owner delegation** |

The [v5 review](../../candidates/cand-d/retention-review-v5-r1.md) found one contradictory interface and three unsupported guarantees. Do not iterate the motor PWM voltage again: a higher typical stall torque supplies neither an upper preload nor a lower loaded-release limit.

1. Keep the Q85 two-segment architecture, 60 mm sphere, machined lug/cam lock, rigid face coupling and full v5 tabletop load cases. Archive the exact v5 declaration. Keep both high-similarity evidence and adverse review findings visible.
2. Retain the sleeve on its housing with a **clearance-bored, cross-pinned rear collar**, on an extended, unslotted rear tube land. Install the collar and transverse pin before the removable rear drive plate. Dimension axial end play, pin edge distances, holes, worst fits and double shear. The servo must not carry axial ejection load.
3. Replace the bonded round gearhead, spur pinion and PWM-to-stall preload with the **FEETECH SCS0002-C001** serial position servo, regulated supply and keyed mechanical case reaction. Use the manufacturer's [specification](https://www.feetech.cn/Data/feetechrc/upload/file/20260622/6391771886009025053412379.pdf), especially pp. 3, 4 and 6, over conflicting catalog rows. Use the output spline and retaining screw, not a glued joint. A series torsion spring converts bounded angle into bounded closing torque; a separate reverse dog positively drives release after unwinding. This is not a spring-closed latch: no spring closes the open port and unpowered retention must survive removal of the servo torque. Allow partial engagement and obstruction explicitly.
4. Carry the fixed external loads through the release calculation; check force at each cam stage, contact timing, standoff at the tooth ring and differential lug depth, including the interrupted bore. Distinguish a documented externally presented start from an autonomous capture claim. Provide the actual loads that correct each admitted error; reject poses that the guides or actuator cannot correct. Do not assume contact over the entire diameter of a slotted bore.
5. Repack around the actual servo/rail/converter and a sourced thinner high-rate cell if necessary. Account for hinge hardware, drive tool access, mounting, fastener types and lengths, regulator loss, and source tolerances. Preserve the existing joint mechanism. If bounds or fit do not close, document them instead of classifying the candidate by its nominal geometry.

Decision → regenerated candidate and dossier → fresh independent G6 and Q61 reviews → clean evaluation → disposition. Q12, Q31, Q36, Q61, Q62 and their registered criteria are untouched. Preregistering this revision neither qualifies a servo nor accepts cand-d.
