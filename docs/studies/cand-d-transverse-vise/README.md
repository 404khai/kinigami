# Transverse vise — successor study, not a Gate 1 run

The head presses a finite paddle onto three open V seats with one transverse platen, then withdraws the platen and drives a separate axial blade. The closed load path, each opening transition and actual neighbour travel are distinct questions. Q12, Q85, Q100, the registered criteria and the v7 candidate are unchanged.

| Study | What the numbers establish | What they do not establish |
|---|---|---|
| [Finite solids and poses](surfaces.md), [calculator](bench.py) | In the measured near-home branch, a loaded excess gap ≤.055 mm bounds tilt to 1.53°, yaw to 1.13° and planar boss excursion to .416 mm, without positive load on every face. | Initial acquisition from arbitrary pose, manufacturing at that gap under load, actual sharing, overload survival or a guaranteed escape path after the platen lifts. |
| [Drive and package](drive.md), [final installation](install.py) | At 34.5 mm pitch the enumerated stowed stock has a 59.838 mm containing diameter. Two prismatic strokes can clear the adjacent installed **heads** by .250 mm including the stated reserve, independent of tail travel. | A complete shell, mating paddle, harness, feet and powered fold clearing the sweep. The 30 mm pitch does not work. |
| [Articulation](articulate.py) | The relocated cell and controller, PMD motor about the revised pivot, paddle back and two yoke ends can be separated in the listed allocation. Earlier pivot/rack collisions are retained. | An installed shaft/sector, bearing webs, rigidity, or any of the final packaging parts omitted from this smaller trial. Use the installation calculator for the later coordinates. |

## Force checks

[vise.py](vise.py) checks whether six **frictionless lower normal reactions exist** for every wrench in the carried-over service/table/fault boxes. R7 circle, 35° normals, top height 3.50 mm. For a 70 g load screen, assumed upper tangential-force ratios 0/.05/.15/.23 give sufficient central preload **56/70/132/465 N**, respectively. These are separate idealized solutions including normal/centre error; the actual screw does not choose contact forces. They are neither a seating proof nor bounds on forces after the platen hits a hard stop.

[settle.py](settle.py) asks a different question. Its outer Coulomb cone and uncertain wrench columns allow shear on **both** lower flanks and the upper ball. A separating virtual twist can exclude a missing lower reaction above a computed preload at those contacts. At lower µ=.05, upper .04, the table case needs 104.44 N; at .23 lower even zero top drag gives no finite certificate. A failed sufficient test is not a jam witness. The inner-cone witness option in the first calculator is for nominal realisable forces, not an uncertainty bound. Do not combine the most favourable numbers from these models.

### Ejection and the table

In a lower-only contact state, choose a virtual translation with positive work on every admissible head contact. If the lower normals lie in a cone of half-angle a about +Y, choose v=(1,k,0), k≥tan(a+atan µ). A pusher with axial force F and lateral force at most bF contributes at least (1−bk)F, b=tan(.5°+atan .23). Moments do not enter a common translation; that does not constrain the physical tail to translate without rotating.

* In a **Z-up** installation a floor normal can grow with internal contact force. Use v=(1,k',h) with h≥µ_floor·hypot(1,k') and k'≥k·hypot(1,h). For the final 51° accessible falling deck and a 70 g screen this requires 18.07 N at floor µ=.30; at .50 the certificate does not exist. The earlier 36° interior calculation cannot rate the wider swept deck.
* For the alternate **Y-up** installation, if the floor normal is within 15° of +Y and µ_floor≤1, the same v works on the floor and deck without assuming floor load ≤weight. At 70 g the sufficient axial force is 11.19 N allowing the force box and gravity. This is not a floor-material qualification or proof that the head cannot tip farther. It requires no opposite/upper contact, back lip, exposed hardware or other resisting body. The separate 15 N delivered-force drive calculation is a sizing test, not proof of those conditions.
* A high-open gap excludes simultaneous jaw contact by the enumerated 25.494 mm paddle/arm set; an unloaded paddle may go around a finite blade. Neither an upper-only pinch against the floor nor a momentarily free tail is excluded by motor position. A shaped folding tongue can have a positive opening moment on its sides and tip while its back still jams. A terminal cover does not guard the swept back.

**Free chain, versus a grounded test head.** The unbounded-floor test above does not use vertical equilibrium of the entire assembly. For a separate quasistatic case on a single flat, nonadhesive tabletop with **no external hold-down**, sum vertical forces over *all* free Kins: internal reactions cancel, so the sum of nonnegative floor normals is total weight plus any net downward external load. This bounds the total floor normal on either subchain, **not** the force within a pinched cheek, on the shaft, or on one foot by that foot's Kin weight. [Calculator](free_chain.py) retains a separate 4W/W/W external force box on the tail group (balanced external loading on the assembly), debits its gravity and allows Coulomb friction against the entire floor budget. It tests a virtual translation (1,k,h), not a prescribed tail path. At h=0, k=tan(51°+atan .23), lower graph contacts do nonnegative work. In the nominal Z-up pose the maximum adverse floor work per unit normal is floor μ times hypot(1,k); the axial blade contributes at least 1−k tan(.5°+atan .23) per delivered axial N.

| Quasistatic, 70 g/Kin, floor μ=1 | Total floor normal cap | Sufficient axial push, level / at up to 15° head tilt |
|---|---:|---:|
| Two free Kins, one on the tail side | 1.373 N | >14.253 / >16.630 N |
| Five free Kins, four on the tail side | 3.432 N | >23.439 / >30.571 N |

These are sufficient-force *screens*, not measured minimums. The 15 N drive sizing case covers the first level row only among those four cases. They require actual continuous blade pickup, **only** the qualified lower graph contacting the tail, and no opposite jaw, blade-edge or casing contact. They do not relax external load criteria, certify μ, include impacts, or replace the unbounded-normal calculation for a clamped fixture. Reproduce: `python3 -B free_chain.py`.

## Reproduction

[Contact deflection and load sharing](pads.md) tests a different, integral top pad. [Straight toe](toe.md) and [its ram](oblique-drive.md) document the terminal contact and single-web failures. The [rotary toe](sector.md) can turn its central face toward ejection, but the [installed sector drive](sector-drive-take35.md) collides. None replaces the frozen v7.

Run from this directory: `for s in bench drive install articulate vise settle; do OPENBLAS_NUM_THREADS=1 python3 -B "$s.py" || exit 1; done`. The three installation/surface calculators use the standard library; the trial articulation and force screens also use NumPy and the LPs use SciPy/HiGHS. No simulator or candidate declaration reads these files. A candidate revision still needs a complete loaded restraint/release path, sensing, structure, fault response, provenance and a fresh independent review.
