# Q45 — Inspector architecture

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-10-30 |
| Supersedes | — |
| Provenance | condensed from owner decision, including an agent-proposed verification rule the owner accepted |

## Context

Q42 makes the inspector read-only and Q44 makes it read recordings. Its technology and timing were still open. Contact and tipping bugs are much easier to see than to infer, but an early viewer must not become a second source of truth.

## Decision

1. **Option A — a separate native Zig inspector executable using a vetted portable graphics library,** behind the Q42 dependency policy.
   - The recording reader is reusable Zig code, separate from the rendering layer.
   - The graphics library belongs exclusively to the inspector, never to the simulation core.
   - A library such as sokol is a **candidate, not a selection**. Its license, maintenance, platform support, and technical fit are checked before adoption.
   - The inspector consumes immutable snapshots and recorded events. It cannot access mutable simulation state, issue commands to Kins, or change evaluator behavior.
2. **A minimal inspector in slice 1: yes.** Scope:
   - fixture bodies and the reference tabletop
   - body positions and orientations
   - contact points
   - recorded normal and friction force vectors
   - timeline and snapshot scrubbing
   - simulation timestamp and run-status labels

   The inspector displays solver-produced values. It never independently calculates authoritative contact forces or reconstructs missing state. Unrecorded values are shown as **unavailable**, never estimated. It is a debugging aid: its screenshots are not benchmark evidence, and its existence does not qualify the solver.
3. **Live viewing: yes, through a one-way, non-blocking boundary.**
   - a bounded, preallocated snapshot buffer
   - non-blocking publication from the simulation
   - no waiting for rendering, user input, or acknowledgement
   - dropped-frame accounting
   - no backpressure into the simulation
   - no shared mutable state

   If the inspector falls behind, it drops frames. Capture and rendering may reduce wall-clock throughput through host resource contention, but must never alter simulated time, event ordering, controller compute budgets, random inputs, or results.
4. **Interpolation: yes, presentation-only.** Optional and switchable off, with a visible label such as `INTERPOLATED DISPLAY`. Exact recorded snapshots stay accessible, and the actual timestamp of the selected snapshot stays visible. Interpolation never modifies recorded data or checkpoint hashes. Measurements, contact and force inspection, and cutaways use exact recorded states. A cutaway never shows an invented intermediate mechanism configuration.

## Verification rule (agent refinement, accepted)

- Slice 1 replay tests include a pair of otherwise identical runs, one with live capture enabled and one without. **Their checkpoint state hashes must match.**
- Snapshot publication never draws from the simulation RNG and never creates scheduled events.

## Consistency

- **Q15:** the inspector sits outside the backend.
- **Q35–Q36:** it visualizes actual solver and mechanism state.
- **Q39:** inspector output never replaces hash-linked evaluator results.
- **Q42:** rendering dependencies stay outside the core.
- **Q43:** live rendering cannot affect scheduling.
- **Q44:** recordings are the inspection source.

## Principle

> The simulator produces truth. The recording preserves truth. The inspector visualizes truth. The inspector must never manufacture, modify or influence it.

## Alternatives considered

- **B. Web inspector (TypeScript with WebGPU):** a second language, a duplicated recording reader, and a large dependency tree.
- **C. Native Zig calling Metal directly:** not portable, and a lot of code before anything is visible.
