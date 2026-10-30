# Q31 — Tabletop-supported connected-chain articulation

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-10-30 |
| Supersedes | — |
| Provenance | condensed from owner decision |

## Context

Kinigami needed a first mandatory benchmark for deliberate shape change by a connected assembly. It had to be demanding enough to exercise actuation, linkage, and contact, without yet requiring unsupported (cantilevered) lifting.

## Decision

Tabletop-supported bending is the first mandatory connected-chain articulation benchmark.

1. **Configuration.** Five mechanically identical Kins form a connected chain with all required connections mechanically engaged. The chain starts in a documented, physically stable configuration on the Q21 reference tabletop. Ordinary onboard actuators drive the transformation. No external clamps, guide rails, prescribed body trajectories, or artificial planar constraints. Endpoints may move through physically modeled contact. The initial geometry and connection topology are documented before testing.
2. **Required transformation.** The chain executes a predefined change in curvature while preserving its chain connections. Success requires:
   - a measurable change in relative geometry
   - actuator-driven movement within documented mechanical limits
   - no disconnection of required links
   - physically valid contact and collision behavior
   - compliance with joint motion, force, torque, power, energy, and thermal limits
   - a final configuration within predefined shape and stability tolerances

   Whole-chain translation or rotation does not count.
3. **3D physics.** The task is nominally planar, but the simulation stays fully 3D: gravity, contact, friction and slip, joint compliance, structural loads, rotation and tipping, out-of-plane motion, collisions, and actuator dynamics. No 2D constraint. Lifting, rolling, twisting, and tipping must emerge from the physics. The permissible out-of-plane deviation is defined before final acceptance testing.
4. **Shape measurement.** Use relative geometric measures that distinguish deformation from rigid motion. Candidates include relative poses, joint angles, centerline geometry, discrete turning angles, shape difference, and maximum out-of-plane deviation. The curvature target and tolerances remain open until justified during benchmark specification.
5. **Timing and resources.** The benchmark defines the target, maximum completion time, permitted shape error, settling, energy, actuator and coupler load limits, thermal constraints, and uncertainty and tolerance cases. No thresholds may be chosen after observing results. Q14 and Q25 apply.
6. **Structural locking.** Preserve Q11. Distinguish actively maintained configurations from those that can enter a passively locked state. Do not assume every reachable curvature can be locked without power. Evaluate passive retention separately under declared loads.
7. **Not established by this benchmark:** unsupported lifting, cantilever articulation, unsupported spans, gravity-loaded 3D transformation, arbitrary spatial curvature, cooperative traversal, or large-scale assembly. A future base-anchored **cantilever benchmark** is planned.
8. **Inspection.** The inspector must eventually support:
   - initial, intermediate, and final configurations
   - articulation playback
   - joint and coupler loads
   - contact and friction
   - centerline and curvature overlays
   - out-of-plane deviation
   - energy and actuator timelines
   - close-ups and cutaways of the moving mechanisms

   All of these come from the authoritative simulated state.

The final Kin geometry and articulation mechanism are **not** selected by this decision.

## Alternatives considered

Earlier alternatives (for example, unsupported or cantilevered articulation as the first benchmark) were weighed in the Q30-era discussion. Their text is not available.

## Rationale

Tabletop support isolates articulation, linkage integrity, and contact behavior from self-weight cantilever loads. Full 3D physics prevents the benchmark from hiding tipping and out-of-plane failure.

## Constraints and consequences

- Requires sensing and communication rules (resolved in Q32 and Q33), energy rules (Q34), a physics formulation (Q35), and a coupler model (Q36).
- Target representation, thresholds, and tolerances must be preregistered before testing (Q38, Q39).
