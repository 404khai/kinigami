# Q32 — Controller information boundary

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-10-30 |
| Supersedes | — |
| Provenance | condensed from owner decision |

## Context

Q31 requires closed-loop shape change. A pass is only meaningful if the controllers could have achieved it with information a real Kin would have.

## Decision

**Option C (tiered):** acceptance benchmarks use modeled onboard sensing and actual modeled communication. Oracle access is permitted only for labeled development and diagnostic runs.

1. **Information boundary.**
   - The physics engine and evaluator may access exact poses, joint configurations, contact states, topology and mechanical states, forces and moments, deflections, actuator states, resource consumption, and full history.
   - Acceptance controllers may access only:
     - their modeled onboard sensors
     - their own internal state and permitted estimates
     - direct feedback from their own actuators and couplers
     - messages received through modeled communication links
     - retained information within declared memory limits

   Controllers never read authoritative physics state. The evaluator uses ground truth without exposing it.
2. **Oracle mode.** Permitted for reachability checks, accuracy upper bounds, constraint diagnosis, separating mechanism failures from controller failures, and reference trajectories. Every oracle run is labeled in replay metadata and results. Oracle runs never qualify as a decentralized pass. A privileged trajectory must never be silently transferred into an acceptance controller as prescribed poses or actuator commands.
3. **Target delivery.** The target goes to one designated Kin through its normal communication interface. Every subsequent transfer uses modeled communication between connected participants. No Kin receives an automatic snapshot of global geometry, pose, or topology, and no hidden channel exists. The designated Kin has a software role only, with no extra mechanics, sensing, or computation.
4. **Target semantics.** The target describes a desired collective shape, preferably as relative chain geometry. It does not prescribe body trajectories, actuator histories, or attachment-transfer sequences. The evaluator compares final geometry while discounting whole-chain translation and rotation. The exact representation remains open.
5. **Sensor models** are mandatory for acceptance. Possible categories include joint position and motion, coupler engagement and release, connection load, inertial, contact, and actuator current and temperature. The final inventory is justified by candidate hardware, and not every Kin is assumed to have every sensor. Each sensor documents:
   - measured quantity
   - range and resolution
   - update frequency and latency
   - noise characteristics
   - calibration assumptions
   - failure behavior

   Noise, quantization, and latency reach controllers through the interface, not only through visualization.
6. **Communication models.** Document range and connectivity, latency, bandwidth or message-rate limits, ordering and delivery semantics, queuing and processing delays, loss, and energy where supported. Communication is never instantaneous merely because all Kins share a process. A Kin never receives information from a physically unreachable neighbor.
7. **Deterministic replay (Q14).** Seeded randomness for noise and stochastic communication. Record seeds and configuration. Sampling, delivery, queue processing, and controller scheduling follow deterministic rules. Physics continues while Kins wait. Host wall-clock time never sets simulated latency or timing.
8. **Computation and memory (Q22).** Messages and observations are processed through the declared execution model. Propagation incurs modeled communication and processing delays, with no privileged instant broadcast. Memory limits apply to observations, estimates, and topology knowledge.
9. **Acceptance.** The five-Kin benchmark must reach its declared target with the accepted mechanical model, modeled sensing, actual links, finite compute and memory, bounded actuators, and physically constrained contact, while meeting the time, shape-error, stability, energy, and thermal criteria. Oracle performance may be reported only as a diagnostic comparison.
10. **Parameters.** No arbitrary noise levels, delays, bandwidths, or sensor inventories. Derive them from documented components or justified estimates, or label them provisional. Perform sensitivity analysis where evidence is incomplete.

## Alternatives considered

- **A. Oracle access for controllers:** rejected, because passing results would overstate capability.
- **B. Modeled sensing only, with no oracle mode:** rejected in favor of C, which keeps the diagnostic value of oracle runs.

## Rationale

It enforces the local-intelligence principle and makes acceptance claims credible. Oracle runs still help with diagnosis.

## Constraints and consequences

Requires a sensing layer and an evaluator layer that are separate from both physics and controllers. Requires deterministic scheduling (later specified by Q43).
