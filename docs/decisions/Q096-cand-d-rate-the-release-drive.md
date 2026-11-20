# Q96 — Size the release drive against moving torque, not stall

| Field | Value |
| --- | --- |
| Status | accepted v6 design revision before candidate freeze; not a gate result |
| Recorded | 2026-11-20 |
| Supersedes | Q95's SCS0002-C001 choice only |
| Provenance | **agent decision under explicit owner delegation** |

The first Q95 packaging study fits (58.920 mm) but does **not** justify
bidirectional actuation under the declared tabletop loads. A single spring
leg/dog loads two interrupted journal bearings. With a 42 g sizing case,
the preliminary conservative dry-torque budget is **40.91 N mm to break
away**, **33.73 N mm to eject**. The SCS0002-C001 has only **15.69 N mm
rated at 4.8 V**. Its 49.03 N mm locked-rotor point and two-second
overload protection do not establish a moving torque. Do not pick a shorter
duty cycle and treat the stalled torque as a rating. These figures reject
the proposed 1:1 drive on the available evidence; they do not prove that
every physical specimen will jam, or that 60 mm is infeasible. No v6
declaration or independent review had been frozen at this point.

1. Keep the Q95 split between spring closing and positive reverse drive.
   Change to a source-rated higher-torque serial drive. First choice:
   [FEETECH SCS0037-C001, A/0, pp. 3, 4, 6](https://www.feetech.cn/Data/feetechrc/upload/file/20260622/6391771882565263995959110.pdf):
   0.50 kgf cm = **49.03 N mm rated** at 4.8 V, 6.1±0.5 g, same nominal
   28T / Ø3.9, M1.7 screw. The **23.3 mm tip-to-back** and 27.35 mm
   untrimmed tab span are not the 17.4 mm nominal case height. Use the
   dimensioned drawing, not a marketing name or length-only swap.
2. Verify the chosen alternative with the complete package, including
   the operating hinge sweep, screw/tool access, axial/radial datum
   stack, feature-limited case cradle, end plates and spline. Recompute
   mass, electrical losses, regulator capability, spring/contact and
   loaded release. Use a larger compatible servo only if the same checks
   close and its own primary datasheet supports the moving torque.
3. Limit normal closing preload mechanically. Do not let a stronger
   motor turn a blocked open or reverse stop into an unexamined axial
   force: calculate the pin, collar, journal, driver and plate reactions,
   distinguish operating from overload and decide which fault states are
   recoverable or explicitly rejected. No assumed equal lug sharing,
   no fit established by a box test, no reliance on a marketing current
   or a healthy tail for release.
4. Preserve the SCS0002 dimensional/torque study and adverse ratios in the
   dossier/report. If none of these direct drives fits and closes the load
   budget, record the conflict; a reduction stage with output sensing and
   independent stroke stops would need its own space, efficiency, fault
   and control analysis. Do not substitute an unsupported torque factor.

Q12, Q31, Q36, Q61, Q62, Q85 and the registered gate are unchanged.
Run 10 remains the latest official result. Continue with the candidate,
fresh independent reviews, clean official evaluator, then disposition.
