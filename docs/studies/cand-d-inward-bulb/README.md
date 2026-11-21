# Central bulb, three inward buttons and translating bowl

**Exploratory, not a candidate or a Gate result.** Q12, Q85, Q100 and
`gate1-v1` are unchanged. The only official cand-d result for v7 is run 12.
These are competing dimensional sections; they cannot be assembled by
choosing the best line from each calculator.

## What fits locally

The six R4.20 dish surfaces on the tail and three rear flats give a single
bulb, Ø24.96 nominal. It admits a centred R7.694 backing sphere after
the stated .16 debit; its exterior has a rolling inner-ball radius of 5.8
where constructed by that offset. Neither number says the tail is a
sphere. In [the section](mushroom.py), coordinates are mm relative to the
bulb datum, +x toward the mouth: button centre (−.57,10.95,0), two working
poles at (−1.398,8.999,±1.127), three stations at 120°. Rear centres are
at x−9.92, r2.95 and clocked 60° from the buttons. The equivalent rear
pitch arm is 9.896. Neck, shell ribs and attachment are not rated by an
insphere. A 0.0033 mm remaining isotropic core bound at the rear land is
particularly sensitive to making that land larger.

| Section | Finding | Limit |
|---|---|---|
| Straight hemispherical button, fixed port | 0.0593 mm exclusion of adverse normals over travel; the parked port still has an adverse cone against a straight external sleeve | A port-clearance proof is not a bound on guide breakaway |
| [Moving bowl](translating_bowl.py), straight button | Local 45° trim gives empty port ≥0.0868 N/N outward at μ=.23; a park depth 4.10±.02 puts the tip behind the 1.55 mm back face even at zero yoke travel | Actual whole-head release, seams and fixed hardware not certified |
| [Drive and package](bulb-drive-take25.py) | With 7.175 mm shoe travel, a 2.2 mm row separation can generate 731 N summed guide reaction; a start ratio ≤.00695 would be needed for the chosen .035 N/N drag budget | A catalogue *dynamic* friction coefficient is not a starting limit. Spring solid height is not overload protection |
| Common ring, side-wall packaging at head x+19 | At x5.972/R21.5 the three pins are 120° apart. The +y servo excludes ±26.07° and −y cell ±41.07°, 60° apart modulo 120°: combined half-widths exceed the separation in both directions | No clocking fits these particular boxes. Not a limit for other drives |
| Terminal hoop versus bowl | The former straight package requires ≥68.78 mm, ≥63.54 mm even over its ±15° hinge stroke; the bowl is a **different**, shorter option | A local failure does not exclude a 60 mm Kin |

## The same seated wrench, without equal load sharing

[Straight slides](tripod.py) and the [outer polygonal cones](friction.py)
use three independently bounded effort coordinates. At 30±.8 N/slide and
70 g the frictionless interval solve gives a worst 0.918 N compressive
reserve. At the *exact* nominal geometry a distinct Coulomb equilibrium
has **zero load on one rear pad**, with the other groups between 13.915
and 26.919 N. This is an admissible wrench witness, not evidence that an
elastic assembly necessarily reaches that equilibrium. A different, 32 N
straight-slide run gives upper reaction bounds 191.47/145.07 N (rear/V).
Do not transfer its numbers to a rocker.

The alternative moves each nose along an R18 arc. At h=2.45 the tangent
is the old guide direction; its pivot lies along local +t, at
(−.913,11.405,17.991). [Crank geometry](crank.py) includes the rigid nose's
spin and the **actual contact point's velocity** in the actuator wrench.
For each missing contact [the separator](face_margin.py) bounds its virtual
work above by 0 on every other unit-normal column and 1 on its own
column; a positive minimum virtual work of the applied wrench forces a
positive reaction there in any nonnegative frictionless equilibrium.
Start at the exact positive nominal solve and vary inputs continuously:
a strictly positive virtual test on every uncertain column bounds the
sum of positive reactions (no divergence). At a first singular matrix a
bounded limiting equilibrium exists; shifting along its null vector to
the first zero would contradict a separator. Thus the result establishes
**existence** of an all-compressive seated solution, not equal sharing,
partial-pose capture, or unique reactions in a frictional assembly.

[Traction bounds](traction.py) optimise full circular friction disks.
The LP only proposes dual vectors: the script then checks the norm
support over the actual continuous uncertainty sets (and corrects
roundoff along a strict separating direction). Contacts may have zero
force. `dp=.30` mm, `da=.012` centre-tangent chord, μ≤.23; at 90 and
110 g the normal chord error is .028. The body load box is from Take 23
(23 mm half-width, 25/40 mm roll/pitch lever); resize for actual feet,
mass, joint and pitch before any declaration. Force is N/actuator measured
at the nose **along the tangent**, not motor-current-based thrust.

| Trial mass, effort | Table frictionless worst reserve (N) | Max rear (N) | Max single flank (N) | Max two flanks of one shoe, summed (N) |
|---|---:|---:|---:|---:|
| 70 g, 30±.8 N, .012 normal chord | 8.001 | 174.790 | 122.309 | 161.909 |
| 90 g, 32±.8 N | 1.800 | 213.731 | 147.301 | 192.064 |
| 110 g, 35±.8 N | .848 | 234.608 | 161.899 | 209.962 |

These bounds are conditional on **seated** contacts. For example the
straight 70 g fit's .40 rear land with .04 registration and .012 tilt
cannot simply be reused at .028 tilt (R8.05 × .028 alone costs .225 mm).
The 90 g curved design needs strength for about 198 N shoe resultant,
214 N rear and its actual root moments, not a new claim based on the
earlier ~2 GPa centred Hertz comparisons. [SKF's 4.2 GPa static
reference](https://www.skf.com/us/products/rolling-bearings/principles-of-rolling-bearing-selection/bearing-selection-process/bearing-size/size-selection-based-on-static-load)
concerns ball bearings, not a rating for these custom dishes or edges.

## Why this is not v8

[Arc withdrawal](swing.py) gives ≥.0222 N/N free-lead coefficient for
the R18 branch **if** the specified annular and back-tube stock is present,
with a ≥R3.504 cylindrical passage for the parked nose. The arm and
offset bore must pass through that stock: a shaft or shank that removes a
witness invalidates the conclusion. The existing 37° straight bore is
not that passage. No bounded opening torque, drive/return and overload
isolation, measured force/position tolerance, home-stop load path,
collision-free whole assembly or G1/G2 budget is yet demonstrated.

Reproduce from the repository root (Python 3, NumPy and SciPy, **not**
runtime dependencies of the Zig simulation):

```sh
for script in mushroom translating_bowl bulb-drive-take25 tripod friction swing face_margin crank traction check; do
  OPENBLAS_NUM_THREADS=1 python3 -B "docs/studies/cand-d-inward-bulb/$script.py" || exit 1
done
```

**Subsequent Take 24–26 checks.** [Complete swing study and limits](mushroom.md). The constant light closing bias is not guaranteed during removal of the loaded saddle: even with no saddle or bearing drag, 32.8/0.029789 = 1,101 N is the loose normal-sum bound, **not** a predicted load. The [axial motor and bevel check](bulb-drive-take25.py) reproduces a solid shaft–motor collision and a 60.268 mm centre-independent span for the shorter fixed sleeve at 35 mm straight pitch. Neither the 59.632 mm motor-only guard nor the free-lead contact estimate authorizes a successor.
