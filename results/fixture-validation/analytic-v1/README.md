# Analytic fixture-validation results (criteria v1)

Criteria: `criteria/fixture-validation/analytic-v1.json` (SHA-256 `565ef6b6…3e78`).
Protocol: `docs/validation/fixture-analytic-v1-protocol.md`.
Every result here is labeled **`fixture`** (Q46). These results are not benchmark or Kin-candidate evidence, and they qualify nothing beyond the declared conditions.

| Run | Code revision | Protocol rev | Build | Rest | Free fall | Friction threshold | Slide to stop | Tipping |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [run 1](run1-7c7581f-ReleaseSafe.json) | `7c7581f` (clean) | 1 | ReleaseSafe, aarch64-macos | pass 9/9 | pass 9/9 | **uncertain 6/9** | **fail 0/9** | pass 9/9 |
| [run 2](run2-cd59f3e-ReleaseSafe.json) | `cd59f3e` (clean) | 2 | ReleaseSafe, aarch64-macos | pass 9/9 | pass 9/9 | pass 9/9 | pass 9/9 | pass 9/9 |

**Revision 2 was made after observing run 1.** The protocol revision log gives the reasons (an uncompressed initial contact, and centre-of-mass rocking counted as sliding) and flags the change for owner review. Criteria thresholds and solver settings are identical across both runs.

**Run 1 provenance caveat:** at the time of run 1, the code revision was read from the cached build configuration, a defect fixed in `cd59f3e`. Run 1's recorded revision matches the session's commit sequence, but it was not captured by the corrected mechanism. A later report from the old mechanism carried a stale revision and was discarded, not kept.

## Run 2: replay and margins

- **Replay:** rerunning the same binary reproduced all 63 sub-run final-state SHA-256 hashes and every metric value exactly.
- **Largest margin used** (value ÷ limit, worst over all combinations):

  | Metric | Margin used |
  | --- | --- |
  | Free-fall position | 0.50 (the expected ½·g·Δt·t error of semi-implicit Euler) |
  | Stop distance | 0.42 |
  | Stop time | 0.35 |
  | Post-stop drift | 0.15 |
  | Sub-threshold tipping tilt | 0.11 |
  | Everything else | ≤ 0.02 |

- **Above-threshold tipping:** the tall fixture falls over (minimum tilt 1.58 rad across combinations).
- **Informational:** the revision-1 CoM-speed stop metric would still fail. Its worst stop-time error is 9.2 ms, against a 4 ms limit at Δt = 2 ms.

## Validated envelope (what these results cover)

Only:

- a single uniform sharp-edged cuboid on the z = 0 plane
- standard gravity
- Coulomb friction pairs 0.3/0.2, 0.6/0.45, 0.9/0.7
- Δt = 0.5, 1, 2 ms
- the protocol's solver settings (k = 1e5 N/m and c = 50 N·s/m per contact, 100 PGS sweeps, warm start)
- the declared loads and speeds

Not covered:

- body-body contact
- links
- rotation about more than one axis (the gyroscopic term is omitted)
- other stiffnesses
- any Kin geometry
