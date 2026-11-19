# Body-contact (box-box) fixture validation

- Criteria: `criteria/fixture-validation/body-contact-v1.json`, sha256 `26b2f8dc…d883`, registered at `183b5a2` before any solver code (Q76, Q77).
- Protocol: `docs/validation/body-contact-v1-protocol.md`, revision 2 (Q78).
- Label: **`fixture`**. These results qualify nothing beyond the declared box-box envelope, and say nothing about any Kin.

| Run | Code revision | BB1 | BB2 | BB3 | BB4 | BB5 | BB6 | BB7 | BB8 | BB9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [run 1](run1-2d4dd12-ReleaseSafe.json) | `2d4dd12` (clean, ReleaseSafe) | pass 9/9 | pass 9/9 | pass 9/9 | pass 9/9 | pass 9/9 | **fail** | pass 9/9 | **uncertain** 4/9 | pass 9/9 |

**Run 1 outcome: not qualified.** No criterion or threshold was changed to obtain or alter this result.

## What did not pass

- **BB6 swap check: fail.** The face-face point set with the pair swapped differs by one penetration depth (relative error 1.25e-2 against 1e-9). The cause is a **conflict inside criteria v1**: "same point set when swapped" contradicts "points on the incident face", because swapping changes which box is incident. The ordered-pair checks for all three closed forms pass. Resolving it needs a superseding criteria version.
- **BB8 angular momentum: uncertain.** Five combinations at 1000 and 2000 µs exceed the allowance (1.6× to 73×). Linear momentum, impulse accounting, pose integration, energy and both snap controls pass.
  - Per-impulse angular-momentum conservation was verified to 1e-12.
  - The residual comes from projected Gauss–Seidel friction non-convergence at the protocol's 100 sweeps: about 1.6e-4 rad/s of off-axis spin.
  - With no gyroscopic term, that spin makes L drift after separation. At 1000 sweeps the residual drops to 1.8e-11 rad/s.
  - This is a solver-setting or modelling decision, not tuned here.

## Notes

- During implementation, a non-official preview exposed unstable SAT axis selection. That instability caused BB1 at μ_high/500 µs and the BB7 frame dependence. It was fixed and recorded in Q78 (protocol rev 2) before this run.
- The existing suites are unchanged by the opt-in body contact. Analytic 63/63 and compliant-link 60/60 final-state hashes are identical, and the coupler run-2 report is identical.
