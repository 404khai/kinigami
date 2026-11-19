# Coupler-engagement solver-settings sensitivity (Q75)

- **Label:** exploratory. Preregistered in Q75 (`9e200a0`) before any code or run. It gives no verdict on the variants and changes no official setting, outcome or run.
- **Code and build:** `446404c` (clean tree), ReleaseSafe. Command: `kinigami-qualify --coupler-sensitivity <dir>`.
- **Criteria:** `coupler-engagement-v2.json`, unchanged. Each variant runs the full C1–C10 suite.
- **Validity:** `baseline` reproduces official run 2 (`afd29a8`). Outcomes and every final-state hash are identical, so the study is valid.
- **Replay:** a second full process run reproduced all nine variant reports byte-for-byte.

## Results

| Variant | Changed setting | C1–C6, C9, C10 | C7 | C8 |
| --- | --- | --- | --- | --- |
| baseline | — | pass | pass | pass (392 evaluated, 256 outside_model) |
| iterations_10 | 10 iterations | pass | pass | pass, same counts |
| iterations_25 | 25 | pass | pass | pass, same counts |
| iterations_50 | 50 | pass | pass | pass, same counts |
| iterations_200 | 200 | pass | pass | pass, same counts |
| no_warm_start | warm start off | pass | pass | pass, same counts |
| q_0 | link prediction q = 0 | pass | pass | pass, same counts |
| q_0.5 | q = 0.5 | pass | pass | pass, same counts |
| backward_euler | link form backward Euler, q = 1 | pass | **uncertain** (5 pass, 12 fail, 1 outside envelope) | pass (389 evaluated, 259 outside_model) |

## Interpretation (Q75 §6 rule, fixed in advance)

- **Settings-robust** across contact-solver iterations (10–200), warm start, and the link prediction coefficient q (0, ¼, ½). No case outcome changes.
- **Settings-sensitive** to the link integration form, in C7 only.
  - Under backward Euler, the undamped axial oscillations show numerical damping |ζ_num| ≈ ω·Δt/2: 0.025, 0.050 and 0.099 at ω·Δt = 0.05, 0.1 and 0.2, against the 0.01 limit.
  - The damped runs show a ζ relative error of 0.36–1.98.
  - Torsion combinations pass.
  - This is the expected first-order dissipation of backward Euler, and C7 correctly rejects it, as L7 did for the compliant link (Q54).
  - C8 still passes; three more runs fall outside the model.
- **Status:** the official settings (midpoint prediction, q = ¼) are unchanged. The result supports keeping them. R8's "solver-settings sensitivity not studied" limitation is closed.
- **Still open in R8:** cube-cube contact (256/648 sweep runs `outside_model`) and the Δt-sensitive capture boundary.
