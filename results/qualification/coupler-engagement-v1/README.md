# Coupler-engagement qualification results (fixture stand-in)

**Official result: run 2, criteria v2** (`coupler-engagement-v2.json`, SHA-256 `72307066…8a02`, Q60, protocol revision 3). Run 1 below used the superseded v1.

Criteria (run 1): `criteria/qualification/coupler-engagement-v1.json` (SHA-256 `1f07a24b…e8bdc`, Q56, Q57). Protocol: `docs/validation/coupler-engagement-v1-protocol.md`, revision 2 (Q58).
Every result is labeled **`fixture`**. These results say nothing about any Kin coupler, and they qualify nothing beyond the declared envelope.

| Run | Code revision | Build | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [run 1](run1-f4b8e0f-ReleaseSafe.json) | `f4b8e0f` (clean) | ReleaseSafe, aarch64-macos | pass 3/3 | pass 6/6 | pass 48/48 | pass 6/6 | pass 6/6 | pass 3/3 | **uncertain** (7 of 17 pass, 1 outside envelope) | **uncertain** (sweep runs fail the energy audit, see below) | pass 3/3 | pass 3/3 |
| [run 2](run2-afd29a8-ReleaseSafe.json) | `afd29a8` (clean) | ReleaseSafe, aarch64-macos | pass 3/3 | pass 6/6 | pass 48/48 | pass 6/6 | pass 6/6 | pass 3/3 | **pass** (17, 1 outside envelope) | **pass** (392 evaluated, 0 audit failures) | pass 3/3 | pass 3/3 |

Run time about 2 minutes. No criteria, protocol, solver, or evaluator value was changed after observing this run. Nothing here is hidden by a ruling: the open items below stay open.

## What passed

- **C1, C2:** seated preload statics and the seat-separation threshold match closed form (tension 0.485530 N, seat force 0.289397 N, F_sep 0.5 N).
- **C3:** per-axis load limits separate the link at the engagement-scaled limit from solver-native loads, and 0.9× of the limit holds, at e = 1 and 0.5.
- **C4, C5, C6:** engagement timing and continuity, blocked engagement outside the capture zone, release under load (separates at 0.9× the block tension, blocked at 1.1×, against an independent RK4 reference), and clean unloaded release with no force jump.
- **C9:** the velocity-snap and pose-snap controls trip their named audits at every Δt, and the uncontrolled baseline passes every audit.
- **C10:** replay is bit-identical on the replayed subset.
- **Audits in the sweep:** momentum, per-step impulse accounting, and bit-exact pose integration pass on **every** evaluated C8 run. These are the CPL-004 evidence that no velocity or pose change lacks a modeled cause.
- **C7 period, damping, and numerical dissipation** pass at all resolved combinations.

## What did not pass: the energy audit (C7 and C8)

`energy_creation_over_allowance` fails on 10 of 17 evaluated C7 combinations (undamped runs only; ζ = 0.05 runs pass) and on every evaluated C8 run. It is the **only** failing metric in the suite.

- **C7 diagnosis.** The measured creation divided by E_ref is 0.0253, 0.0511, 0.1041 for the axial e = 1 runs at 50, 100, 200 µs: about ω·Δt/2. The energy KE(v_n) + V(x_n) of a semi-implicit step oscillates at **first order** in ω·Δt. Q57's 2 % allowance assumed the second-order shadow-energy term. That rationale was wrong. It is a criteria error, not evidence of a solver defect: the momentum, impulse, and pose audits pass on the same runs.
- **C8 is not explained by that alone.** Ratios up to about 24 occur, and runs fail at 50 µs as well. Contact stiffness (ω·Δt up to 0.63 at 200 µs for the seat contacts) and link activation with stored potential are plausible additional causes. **Not diagnosed yet.**
- **No fix is applied.** Changing the allowance after seeing this run needs its own decision record, new criteria version, and a rerun (Q49). See Q59.

## Capture window (reported, not gated; CPL-006)

Of 432 sweep runs, 166 are `outside_model` (cube overlap or lateral excursion; listed, not counted) and 266 are evaluated. Classes of the evaluated runs: captured 10, partial 0, separated 168, latch_blocked 26, missed 62.

**With the Q56 provisional parameters the stand-in barely captures in the swept range.** Even at zero lateral offset, capture occurs only at the highest approach speed (0.3 m/s) and a 0 to 1 mm radius. 27 offsets disagree across Δt. Why:

- Engagement starts only after the ball is inside the capture zone, and the pawl then needs 0.1 s to reach full travel.
- The link limits scale with e, so a small e cannot hold the ball against its own rebound. The link forms and then overloads (168 `separated` runs).

This is a measured property of the provisional stand-in, not a defect of the solver. It is also not evidence about any Kin coupler. Whether to change the stand-in parameters, add a slower approach range, or accept this is for a superseding Q56 record.

## Other notes

- **C3 load timing.** The load applied in step n is L(t_n). The protocol did not fix this; the difference from step-start timing is at most 4.4e-4 relative against a 1e-2 tolerance.
- **Damping mass.** Rows use the reduced-mass c_full in every run, as the protocol states, including hang runs.
- **Recordings.** 530 format-v3 recordings (1.0 GB) can be produced with `--coupler <report.json> --recordings <dir>`. They are not committed.
- **Regression gates.** The analytic suite (63/63) and compliant-link suite (60/60) final-state hashes still equal their run 2 results.

## Run 2 (official, criteria v2)

All ten cases pass. Q60 was ruled and v2 was registered **after run 1 and before any code change or rerun** (Q49). Run 1 is kept as superseded evidence.

- **C7:** the energy audit passes with the first-order allowance. Period, damping, and numerical dissipation are unchanged from run 1.
- **C8:** 648 runs. 392 are evaluated with 0 audit failures, and 256 are `outside_model` (listed, not counted). The `outside_model` runs are dominated by the 0.15 rad misalignment, where the cubes overlap. Cube-cube contact is not modeled (Q56).
- **Capture classes** of valid runs: captured 107, separated 108, latch_blocked 68, missed 109. 65 offsets disagree across Δt: the capture boundary is Δt-sensitive at this resolution.
- **C9:** both snap controls trip their audits at every Δt, and the baseline trips none.
- **Regression gates:** 63/63 analytic and 60/60 compliant-link hashes are unchanged.
