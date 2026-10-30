# Q36 — Coupler engagement model

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-10-30 |
| Supersedes | — |
| Provenance | condensed from owner decision |

## Context

Q35 defines how a link behaves once it exists. This decision defines how links form and dissolve without "fake cohesion", and what the "authoritative coupler state" referenced by Q33 and Q34 is.

## Decision

1. **Option C — a reduced continuous mechanism model with discrete states derived from physical state.** Docking and release emerge from modeled forces, contacts, actuators, internal latch dynamics, and evolving link constraints. Discrete states (approaching, aligning, latching, locked, releasing, jammed, failed) are classifications for controllers, logs, and inspection. They never independently create, strengthen, or remove physical connections.
2. **The capture window is measured, not declared.** Sweep relevant initial misalignments, relative velocities, approach directions, and other justified conditions. Derive the capture operating envelope from the outcomes and document its uncertainty.
3. **Validate against detailed close-up reference models.** Build representative full-mechanism models for docking, partial engagement, jamming, loaded retention, and release. Compare wherever meaningful. Use analytic or other justified references where appropriate, and document what the detailed reference itself cannot establish. Detailed models serve validation and inspection, not routine production simulation.
4. **No unmodeled docking assistance, pose correction, or velocity correction.** Every change in a Kin's pose or velocity arises from gravity, contact, friction, declared actuator forces, physically justified magnetic or guide forces, or link constraints at their current engagement state. No snapping, teleporting, or silent velocity correction. Numerical stabilization stays distinguishable from physical forces and satisfies Q35 validation.

## Constraints

- Pre-alignment uses candidate-specific, physically justified forces and the actual guide and contact geometry. Do not assume magnetic attraction unless the candidate includes it.
- Latch variables (travel, preload, actuator state, wear where supported) are continuous and respect force, torque, speed, energy, and power limits.
- Link stiffness, strength, retention, and failure derive from the current engagement state and never jump to full strength because a label changed.
- Data and power availability couple to the coupler state (Q33, Q34). Mechanical engagement alone does not guarantee data or electrical continuity.
- Release is a modeled physical process under the current load. It may take time, fail, or be blocked by load limits or obstruction.
- Distinguish partial engagement, incomplete release, jamming, damage, and permanent failure where the mechanism supports them. Do not invent unsupported failure physics.
- Record continuous mechanism state, classifications, forces and loads, transitions, and outcomes for replay and cutaway inspection.
- The mechanism, magnetic design, parameters, and numerical implementation remain open.

## Alternatives considered

- **A. Discrete "snap" transitions:** teleporting, energy artifacts, no partial or jammed states. Close to forbidden fake cohesion.
- **B. Full mechanism simulation in production:** too costly beyond close-up studies. It is retained as a validation reference.

## Rationale

Real failure modes stay possible, connection quality has a continuous physical basis, and cost stays practical.
