# Take 77 — Finite-Flat Connected-Component Bound (Exploratory)

**Label:** exploratory. Does not change Q12, Q85, Q100, candidate declarations, criteria, or Gate 1 results.

## Objective

Check whether the seven finite unilateral flats of the Take 74 inclined dry key (one 18° key face plus six 65° V-seat flats) geometrically confine the rigid tail inside a bounded connected neighborhood of the registered pose even when any seat has an air gap, without assuming all seven contacts carry preload simultaneously.

## Method and assumptions

`cage.py` forms the 7×6 nominal contact wrench matrix `A` about `O = (-3.20, 0, 0)` mm (rank 6, strictly positive nullspace weights). Using the exact Rodrigues split `w = sin(θ) u` so `‖(R - I) c - w × c‖ ≤ (1 - cos θ) ‖c‖`, any finite motion in the trial box `θ ≤ β = 1.95°` and ball-center displacement `‖Δc_i‖ ≤ H_i` satisfies `A v + e ≥ 0` with:

- plane-recess budget `E = [0.065, 0.025, …, 0.025]` mm (key, six seats),
- normal-tilt budget `δ = [2.0°, 0.60°, …, 0.60°]`,
- finite curvature term `(1 - cos β) ‖c_i‖`,
- trial center-displacement caps `H = [0.190, 0.460, …, 0.460]` mm.

Because the seven-inequality polytope `{v : A v + e ≥ 0}` is a bounded 6-simplex, convex norms of translation, rotation, and ball-center displacement achieve their maxima at its seven vertices.

## Reproduced results

Command:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONHASHSEED=0 python3 -B docs/studies/cand-d-single-key/cage.py
```

| Metric | Value | Notes |
| --- | --- | --- |
| Flat land radii (key / seat) | 0.849745 / 0.546197 mm | Finite flat extents from Take 74 geometry |
| Flat land reserve (key / seat) | 0.532444 / 0.020016 mm | After `H + R tan δ + 0.040` mm datum debit |
| Max connected-component translation | 0.163898 mm | Strict interior of `< 0.17` mm check |
| Max connected-component rotation | 1.799051° | Strictly below `β = 1.95°` (0.1509° slack) |
| Finite ball-center displacement (lug / registry) | 0.175919 / 0.450985 mm | Strictly below `H = [0.190, 0.460]` mm |
| Original guide cocking (0.50° tilt, X used / normal recession) | 0.017941 / 0.085118 mm | Exceeds the 0.065 mm key recess budget |
| Trial lower y=4.50 guide XY offset (lock only) | 0.041198 mm | Rear full shank starts at y=2.1785 mm (lock) to y=7.0285 mm (4.85 mm park) |

## Limitations and disposition

- **Conditional geometric bound only.** This does not prove passive retention, structural strength, contact stress, unpowered key lock, or loaded release.
- **Original Take 74 guide fails the key recess budget.** A 0.50° cock within the 0.080 mm diametral play of the original `y = 8.60..12.70` mm guide bands recedes the key face by 0.0851 mm along its normal, exceeding the 0.065 mm key recess assumed above.
- **Lower-guide caveat.** Adding a lower band near `y = 4.50` mm reduces lock-pose XY offset to 0.0412 mm, but the rear full-width shank moves to `y ≈ 7.0285` mm at the 4.85 mm park, so that band cannot be credited as a full two-shoulder guide through withdrawal.
- **Separate from release and packaging.** Loaded release from this retained neighborhood is checked in Take 78, and installed packaging in Take 79.
