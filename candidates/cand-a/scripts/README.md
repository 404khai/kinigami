# cand-a scripts (provenance for version 6)

Plain Python 3, no third-party packages. Rebuilt in the v6 work because the v5 scratchpad scripts (`gen_v5.py`, `fbg.py`, ...) were lost; they were never in the repository.

- `fourbar.py`: crank-link-rocker-output-arm solver, dead centres, 1 024-corner tolerance sweeps (`python3 fourbar.py`).
- `closed_height.py`: spread of the output-pin height at the stops over the corners and per-factor sensitivity.

## Solver rebuild and validation against `dossier-v5.md`

Margin definition used from v6 on: margin_open = (extended dead centre) - (open stop angle), margin_closed = (closed stop angle) - (folded dead centre), crank angles in degrees; nominal stops 18.86 / 221.39; the stop tolerance 0.05 mm at crank radius 2.0 (1.432 deg) is one shared sign (10 factors: Cx Cz Px Pz r b a L rocker-arm angle +-1 deg, stop); minimum over the corners.

| Quantity | v5 dossier | fourbar.py |
| --- | --- | --- |
| L, dead centres, travel, swing, nominal stroke | 10.2159, 28.86 / 211.39, 202.53, 82.64, 5.582 | 10.21592, 28.858 / 211.390, 202.53, 82.644, 5.5819 |
| Offsets open / closed (nominal) | 0.422 / 0.277 | 0.4217 / 0.2770 |
| Peak lever, release torque, T_rel | 2.871, 9.66 mN m, 0.5225 N | 2.8710, 9.664, 0.52246 |
| Link force and ratio open / closed | 11.3 N (1.082) / 17.1 N (1.645) | 11.28 (1.0823) / 17.14 (1.6453) |
| Crank moment, stop reaction | 4.76 mN m, 2.38 / 2.37 N | 4.756 / 4.749, 2.378 / 2.374 |
| Stroke, class f by size | 5.088 .. 6.068 | 5.0879 .. 6.0682 |
| Stroke, every coordinate +-0.1 | 5.035 .. 6.113 | 5.0351 .. 6.1134 |
| Stroke, frame plus play | 4.631 .. 6.613 | 4.6308 .. 6.6129 |
| Offsets, class f / 0.1 / play | 0.245/0.167, 0.225/0.149, 0.077/0.097 | 0.246/0.166, 0.227/0.148, 0.080/0.095 |
| **Margins, class f** | 5.64 / 6.09 | 5.671 / 6.054 |
| **Margins, every coordinate +-0.1** | 5.19 / 5.41 | 5.223 / 5.376 |
| **Margins, frame plus play** | 1.73 / 3.59 | 1.799 / 3.516 |

Discrepancy (accepted by the lead): the margin split differs by 0.03 to 0.07 deg (0.5 to 4 percent). Open plus closed sums agree to 5e-4 relative. The v5 retention review had 5.66 / 6.11, 5.21 / 5.41, 1.71 / 3.61, also different from the dossier. The dossier's stop model is not recoverable; the definition above is used for v6.

## pin2.py (second torsion pin, packing and roll-in path)

Roll-in path of any A-frame point d in B's body frame, same table-height method as dossier 7.1: p(phi) = V + R(phi)[(25.5, 0) + R(-60) d], V = (-12.75, 22.084), R(t) = [[cos t, sin t], [-sin t, cos t]]. At phi = 60 the point lands at d. The peg (d = 0) reproduces the dossier points ((12.75, 22.084) at roll 0, (9.334, 9.334) at 30, (0, 0) at 60). Packing checks use the declared component boxes (body frame, +z is down at rest). The module is a feasibility map only; no declaration was generated from it.

## jawwin.py and k4_gonogo.py (K4 + K1 go/no-go, `docs/studies/coupler-k4-gonogo.md`)

`jawwin.py`: distance from the swept peg (hex AF 4.0 rolling 60 deg along the arc, orientation R(phi - 60) of the docked hex) to the open jaw rectangle (x +-2.9, height 3.05) or tongue rectangle (x +-2.05, height 2.55) at open stroke S, with an optional peg height offset toward the jaw. Validated against `dossier-v5.md` 7.2 and review r1: jaw 0.448 / 0.089 (dossier 0.104, review 0.087) / 0.052 / 0.000 at S = 5.582 / 5.088 / 5.035 / 4.631; tongue 1.024 / 0.654 / 0.308 (dossier 1.025 / 0.654 / 0.318); peg +0.35 at 5.582 gives 0.193 (review 0.193).

`k4_gonogo.py`: check 1 (screw lead angle against cited mu), check 2 (AABB overlap of the declared v5 boxes, with the four-bar parts removed, against the K4 drive boxes; cavity rules; arc keep-out validated against dossier v5 for frame-base 3.31 and rocker post 4.98, the saddle and M3 boxes differ because the declared boxes are stand-ins; K1 pin search), check 3 (required stroke and screw length). Negative control: pushing the M3 box into the wheel is flagged. Ring segment AABBs are skipped (the radial rule covers them). Exploratory; selects nothing.

## k4w_gonogo.py (K4w wedge variant, `docs/studies/coupler-k4w-gonogo.md`)

Reuses `jawwin.py` (validated above) and `k4_gonogo.py` (box, keep-out and pin helpers). Prints the jaw window and travel, wedge jam limit and friction cases, screw lock margins, closing and release forces, the largest free vertical window on the yaw axis (AABB against the remaining v5 boxes, four-bar parts and rod removed, r <= 20, arc keep-out) and the K1 pin search for 2 mm and 5 mm pockets. Forces use the study K4 derived screw factor (0.346 mN m/N) and rated 3 mN m; friction values are the cited Engineering ToolBox ones. Exploratory.
