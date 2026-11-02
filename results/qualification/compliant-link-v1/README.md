# Compliant-link qualification results (criteria v1)

Criteria: `criteria/qualification/compliant-link-v1.json` (SHA-256 `7e147a9d…eb77f8`, Q52).
Protocol: `docs/validation/compliant-link-v1-protocol.md` (revision 1, unchanged).
Every result is labeled **`fixture`**. These results are not coupler, benchmark, or Kin-candidate evidence, and they qualify nothing beyond the declared envelope.

## Run 1: [`run1-77bc3ca-ReleaseSafe.json`](run1-77bc3ca-ReleaseSafe.json)

Code revision `77bc3ca` (clean tree), ReleaseSafe, aarch64-macos, Zig 0.17.0. Solver settings as fixed in the protocol (100 sweeps, contact k = 1e5 N/m and c = 50 N·s/m, link prediction q = 1/4). No solver, protocol, or criteria change was made after the run was observed.

| Case | Outcome | Evaluated | Outside envelope |
| --- | --- | --- | --- |
| L1 axial statics | **pass** | 9 | 0 |
| L2 shear and bending statics | **fail** | 9 | 0 |
| L3 torsion statics | **pass** | 9 | 0 |
| L4 axial dynamics | **pass** | 4 | 5 |
| L5 torsional dynamics | **pass** | 3 | 6 |
| L6 physical damping | **pass** | 4 | 5 |
| L7 numerical dissipation | **pass** | 4 | 5 |
| L8 momentum | **pass** | 9 | 0 |
| L9 contact–link consistency | **pass** | 9 | 0 |
| L10 determinism | **pass** | 9 | 0 |

**The compliant-link capability is therefore not qualified.** L2 fails at all nine combinations under the registered criteria.

## L2 failure and diagnosis

Shear force (≤ 1.5e-11) and shear displacement (≤ 1e-12) are exact. Only the bending moment and bending angle fail, identically at every Δt, so this is not a timestep or convergence effect:

| Grid point | Bending moment error (limit 1e-3) | Bending angle error (limit 2e-2) |
| --- | --- | --- |
| soft | 0.1641 | 0.1641 |
| mid | 0.01924 | 0.01924 (passes) |
| stiff | 0.001958 | 0.001958 (passes) |

Cause: the registered reference `F·h` ignores the vertical tension acting through the rotated anchor lever. Torque balance about B's centre of mass gives |M| = F·h/(1 + h·m·g/k_bend), where the tension (= m·g) **reduces** the moment B must transmit. This closed form predicts errors of 0.1640, 0.01924, 0.001957, against 0.1641, 0.01924, 0.001958 measured. The solver reproduces the correct statics. The registered criterion is what is incomplete. The angle check also fails at soft because the same factor applies.

**Disclosure about the protocol.** The protocol's "analytical expectations" note said the soft/mid/stiff moment errors would be about 2.4 % / 2.0 % / 0.2 % and that the lever term adds to the moment. The soft figure was a numerical slip and the sign was wrong. The corrected values are above. The protocol was not edited (Q49 safeguard). The informational metric `info_moment_rel_error_with_axial_lever` inherits the wrong sign, so it reads 28 % / 3.8 % / 0.39 % and should be ignored. `info_angle_rel_error_vs_measured_moment` (≈ 1e-14) confirms the reported moment and angle are mutually consistent.

**Options (need a new decision record; none taken here):** (a) revise L2's moment and angle references to include the lever term and issue criteria v2; (b) keep v1 and accept L2 as a documented fail with the diagnosis above.

## Margins (worst over evaluated combinations; value ÷ limit)

| Metric | Margin used | Where |
| --- | --- | --- |
| L1 tension, elongation | 1.4e-11, 6.0e-10 | |
| L2 shear force, shear displacement | 1.5e-11, 1.0e-12 | |
| L2 bending moment (fails) | 164 | soft |
| L2 bending angle (fails) | 8.2 | soft |
| L3 torque, twist | 1.8e-11, 1.8e-12 | |
| L4 period error | 0.33 (3.3e-3 of 1e-2) | soft, 2 ms (ω·Δt = 0.2) |
| L5 period error | 0.31 | mid, 0.5 ms |
| L6 ζ error | 0.041 | soft, 2 ms |
| L7 \|ζ_num\| (limit 0.01) | 1.9e-5 (1.9e-7 absolute) | soft, 2 ms |
| L8 momentum | 1.7e-5 | soft, 0.5 ms |
| L9 load sum | 1.2e-11 | |

L7 is the check the criteria were designed around: measured numerical damping is at most 1.9e-7, five orders under the bound, so the link integrator does not masquerade as physical damping (PHY-006). The signed value changes sign across combinations, consistent with round-off-scale phase error rather than dissipation.

## `outside_envelope` combinations (neither pass nor fail, not counted)

| Case | Combinations (grid, Δt, ω·Δt) |
| --- | --- |
| L4, L6, L7 | mid 1 ms (0.316), mid 2 ms (0.632), stiff 0.5 ms (0.5), stiff 1 ms (1.0), stiff 2 ms (2.0) |
| L5 | soft 2 ms (0.245), mid 1 ms (0.387), mid 2 ms (0.775), stiff 0.5/1/2 ms (0.61/1.22/2.45) |

Soft-axial at 2 ms sits exactly on the limit (ω·Δt = 0.2) and is evaluated (protocol slack 1e-12 relative).

## Replay check

The binary was rerun on the same tree. All 60 sub-run final-state SHA-256 hashes and every metric value were identical (bit-exact JSON equality). Each run also replayed in-process during the suite, which is L10.

## Validated envelope (what these results cover)

Only:

- two uniform 20 mm / 0.020 kg cubes joined by one fixture link (L₀ = 10 mm, anchors at facing face centres), or one static cube and one dynamic cube
- stiffness grid soft/mid/stiff (k_axial = k_shear 1e2/1e3/1e4 N/m; k_torsion = k_bend 1e-2/1e-1/1 N·m/rad), Δt = 0.5, 1, 2 ms
- statics: axial tension and elongation, shear force and displacement, torsion (all with ζ = 1 settling)
- dynamics: axial and torsional oscillation and damping at ω·Δt ≤ 0.2 only; the **stiff** grid point is never dynamically validated
- the protocol's solver settings

Not covered, or failed:

- **bending moment and angle under a lateral load (L2) failed** at the soft point, and fail the moment limit at every point
- the stiff grid point's dynamics (outside the resolution rule)
- chains of three or more bodies, link creation, release or failure, closed loops, couplers
- large relative rotations (small-angle rotational Jacobian) and frame-rotation coupling
- any Kin geometry; recordings of links (the recording format has no link representation)
