# Q43 — Simulated time representation and scheduling

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-10-30 |
| Supersedes | — |
| Provenance | condensed from owner decision |

## Context

Q32 requires sensor rates and latencies, message delay and queuing, and physics that continues while Kins wait. Q22 makes computation take time. Q14 and Q42 require exact replay with stable ordering. Q35 requires timestep-sensitivity studies.

## Decision

1. **Option B — integer clock, fixed physics step, deterministic event scheduler.**
   - Simulation time is an integer tick count with a declared time unit per experiment, never a floating-point accumulator.
   - The fixed physics timestep is an integer multiple of the time unit.
   - Sensor sampling, message delivery, computation completion, and controller events have their own scheduled times and periods.
   - Every run records its time unit, physics timestep, and scheduler configuration.
   - Time arithmetic detects overflow and never silently wraps.
   - The event queue uses a stable total order such as `(scheduled_tick, event_phase, source_id, sequence_number)`. The phase order is explicitly specified. Same-timestamp events are never ordered by incidental insertion order, thread completion order, or memory layout.
2. **Coarse-timestep detection: yes.** Configurations whose physics timestep is too coarse for the declared operating conditions are flagged. Two cases are distinguished:
   - **Scheduler resolution:** communication and computation events are represented at their exact integer timestamps, even when intervals are shorter than the physics step. A short latency alone never invalidates a configuration.
   - **Physics coupling resolution:** sensor observations and actuator effects interact with completed physics states and physics boundaries, so their effective resolution is limited by the timestep.

   Thresholds come from sensitivity studies and validation evidence, with no invented universal ratio. Out-of-range configurations are flagged as outside the validated envelope (Q37).
3. **Adaptive or sub-stepped physics is excluded from slices 1–2.** Any later introduction requires a new evidence-backed decision record specifying deterministic step selection, stable ordering across step changes, recording of the actual step sequence, sensitivity and convergence testing, and the effect on Q35's operating envelope. It must not appear quietly as a solver optimization.

## Event semantics between physics steps

| Event | Semantics |
| --- | --- |
| Message delivery | Occurs at its scheduled integer tick |
| Computation completion | Occurs at its scheduled tick |
| Sensor sampling | Samples the most recently completed physics state |
| Controller output | Becomes available after its declared compute latency |
| Actuator command | Takes effect at the next physics boundary |

- Sensor records include **both** the requested sample timestamp and the timestamp of the physics state actually sampled.
- Actuator records include **both** the command-ready timestamp and the effective application timestamp.

A command scheduled between physics steps cannot change an already completed integration. Its effect waits for the next boundary.

## Refinement to Q35 sensitivity studies

Changing the physics timestep leaves the **nominal** sensor, computation, and communication event times unchanged. It can change the age of the sampled state and the delay until actuator commands reach a step boundary. Those effects are measured in timestep-sensitivity studies, never hidden or described as unchanged. (This corrects the agent's original proposal, which said these timings "stay fixed".)

## Principle

> Simulated time belongs to the experiment, not to the physics solver. Changing physics resolution must not silently change the declared schedules of sensors, computation, or communication.

## Alternatives considered

- **A. Quantize everything to the physics step:** sub-step latencies can't be represented, and every rate silently depends on the timestep.
- **C. Adaptive or variable physics step:** an extra source of nondeterminism, and harder sensitivity studies.
