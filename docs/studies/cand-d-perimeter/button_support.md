# Take 65 — why the 65° seat does not rescue the full circular flange

**Exploratory; do not promote.** For the full flange the real working jaw has axial normal component .48. Under the Take 63 70 g wrench and ±10% independent axial spring scatter, the seated virtual-work bound needs a nominal **49.368 N/button** at 60°, **35.404 N/button** at 65°. This establishes neither seating nor safe separation under load. There is no 65° catalog cartridge installation here. In particular a 22–40 N label is not a delivered 36 N on this face.

## Correlated geometry

The [pivot study](pivot/README.md) keeps R10.75 core and R2.50 backing. Its lowest toe at .48 is **12.49413** mm at lock; 12.60194 belongs to the distinct .355218 leaf. The phase in the nine-contact model is **relative**: the jaw and button triplets differ by 60°. Relative to Take 64’s installed angles the coded triplets differ by a 180° roll and a cyclic permutation. That roll merely reverses both transverse axes; the componentwise symmetric external wrench box is unchanged. Clocking to a different frame requires transforming/enclosing that frame's load box, not just relabelling a row. No .55/.60 full circular leaf is used.

At 65° the working poles have x=−5.3665 and tangential offset ±2.2658 (button centre x=−4.31, radius 10.30). Base x=−6.95, cap −5.00, outside toe 3.81, radial half-width 1.35. The finite top is .4640 long × .8814 wide. Distance **in the slope plane** to its closest edge is .4044, not the full insert width. The nominal 8.35 mm disk stroke puts its flat +1.40 beyond the parked lip: .1106 mm ideal terminal exclusion for actual R≥2.45 generators and the .28 full bore. This is *not* clearance for an open cartridge port, an exposed shank, a moving leaf or an outer frame.

At S=36 N, ±10%, the contact-normal bounds with at most .50 N constant guide drag plus k times the actual guide's seat-pair normal sum are:

| Effective k | Worst seat normal (N) | Worst jaw normal (N) | Steel sphere/plane peak (GPa) | Unrounded seat edge reserve after .19 location and contact radius (mm) |
|---:|---:|---:|---:|---:|
| 0 | 197 | 410 | 4.33 | .067 |
| .05 | 261 | 534 | 4.76 | .053 |
| .15 | 748 | 1489 | 6.75 | −.015 |
| .21 | no finite LP bound | no finite LP bound | — | — |

Values rounded up for forces; separate single-contact bounds, not simultaneous or axial loads. Coulomb tangential force ≤.23 times each actual normal. As a check independent of numerical LP: if a seat's axial normal is at least n, its axial force per normal is at least c=n−μ√(1−n²). For a translating button, sum of its two normals ≤(S_hi+.5)/(c−k). The jaw sum follows from the whole-body axial balance. At k=.05 these give 260.99 N and 608.06 N **total on all jaws** respectively. Hitting an LP limit does not imply actual jamming. E*=115.4 GPa elastic seat half-space predictions are load screens, not allowables for a finite insert. At the actual near-conformal outer leaf even the smaller isolated 40 N axial screen consumes essentially the entire half-width. No rating for its cheeks or welds.

## Cartridge and alternate lever

[KIPP K2396.206](https://www.kipp.com/ie/en/Products/Product-Lines/Rustproof-stainless-steel/Spring-plungers-to-press-in-without-collar-stainless-steel.html): body Ø6×14, R2.50 ball, H=1.50 mm, 22/40 N approximate endpoints. A 65° pole requires 1.4435 mm of exposed spherical cap, leaving at most .0565 mm stroke *before the pole is behind the body rim plane*. At 36 N a linear interpolation would leave .333 mm projection, exposing only 29.93°. This interpolation is not a measured force curve. The jacket and face also need their own sweep; even the uncompressed continuous-cylinder envelope extends .31 mm beyond the tested insert cap in the wrong direction. The larger Ø8 plunger has a different nose radius, not a drop-in. An actual long exposed ball-ended rod requires different bearings, a spring and finite clearance at shoulder/port, not this catalog part. See Take 64's independent installed check in the Graft report.

The spring load in the retention calculation is internal conservative work, not the external force inferred by reading the motor. For one clean loaded flank at S=35.404 N, transverse force can be S tan(65°)=75.93 N. With a 7.93 mm two-bush span and 3.115 mm overhang the sum of absolute radial reactions can be 135.6 N; even a .03 coefficient allows **4.07 N** drag. This exceeds the entire ±3.54 N one-sided force allowance before manufacturing variation. Separate force/deflection measurements and real seating at all six faces are needed. Reading travel alone cannot establish that the flange is seated; forced opening, post-fault diagnosis and ejection remain separate obligations.

A rocker avoids the long axial body but changes the kinematics. Trial tangential pivot: span 5.20 mm, axial offset 1.96 mm, so unit-span angular motion moves the ball centre at X+(.3769)r. Generalized spring force is torque/span. For conjugate normal reactions the ball offset is collinear with the normal, but actual tangential forces have a moment about the centre. For the 65° pair the pole speed vector gains (R cos(65°)/span)r; ignoring this would overstate the force ceiling. The uncertainty parameter dv bounds vector error in *centre velocity* including pivot, motion angle and radius tolerance; it is not provided by an encoder. With independent .6° face, .19 mm arm and .02 velocity uncertainty the three nominal force screens are 33.95/47.65/46.41 N (service/table/fault). At dv=.03 they rise to 41.78/58.00/57.10 N.

For a 50 N nominal choice one straight Ø1.45 × 9 active steel torsion bar at a **trial** shear modulus 79.3 GPa takes 260 Nmm, 3.90° twist and 478 MPa ideal peak shear at the high limit. Only .071 mm total axial equivalent spring travel fits the ±10% band. At dv=.02 the minimum clean work term per normal before journal drag is .1343; the illustrative two-station 5 mm yoke and thrust collar leave a seat-pair ceiling of ~588 N at assumed journal μ=.02, >1600 N at .05 and no certificate at .10. No hardness, bearing, preload, torsion-end, flexure, offset-error or installed stop rating is inferred. A freely clocking sphere cannot be assumed to cancel all frictional moments. Don't substitute this rocker for a translating spring in the candidate.

## Reproduce

From this directory, with the same NumPy/SciPy tools as Take 63:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONHASHSEED=0
python3 -B button_support.py
python3 -B pivot/leaf.py | cmp - pivot/result.json
```

The modified Take 63 calculators reproduce their original default stdout; optional arguments do not revise that study. Work concerns only seated retention, stock and specified edges. It does not repair the finite toe, make the KIPP cartridge fit, establish clean exit under all supported attitudes, or give a universal 60 mm exclusion. No change to Q12/Q85/Q100 or any Gate result.
