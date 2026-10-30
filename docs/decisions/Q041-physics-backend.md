# Q41 — Production physics backend

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-10-30 |
| Supersedes | — |
| Provenance | condensed from owner decision |

## Context

Q35 chose the formulation and Q15 keeps the backend replaceable, but slice 1 needs an actual backend. The core Q35/Q36 requirements (solver-native loads, per-axis compliance, continuous latch variables, per-step topology change, exact replay, and stabilization kept separate from damping) are central, not peripheral.

## Decision

1. **Option C — a custom Zig production solver, with an external engine used only for validation.** The production backend is implemented in Zig behind the Q15 interface. This is an architectural direction, not permission to disregard evidence. The custom backend must pass the same qualification requirements as any alternative. If it cannot demonstrate the required accuracy, stability, or capabilities, it stays unqualified, and an alternative may be evaluated through the same interface.
2. **Third-party physics engines are permitted as validation-only dependencies.** They stay outside production runtime code and builds. Licensing, capabilities, numerical assumptions, and suitability per reference case are reviewed before adoption. MuJoCo is a candidate for suitable open-chain reference cases, not a mandatory choice or universal reference. External engines provide independent numerical comparisons, not ground truth, and their envelopes and limitations are documented. Analytic statics and other independent references remain necessary.
3. **A backend qualification checklist is preregistered before slice 2 begins.** It establishes the required evidence and acceptance conditions before the compliant-constraint implementation is evaluated.

## Backend qualification requirements

- Full 3D rigid-body dynamics with appropriate mass, inertia, gravity, and collision geometry.
- Contact and friction validated against suitable analytic and independent references.
- Separate rigid bodies connected through implicitly solved compliant constraints (Q35).
- Per-axis compliance, damping, limits, and load reporting for supported tension, compression, shear, bending, and torsion.
- Solver-native constraint and contact outputs with documented accuracy, suitable for retention, failure, detachment, and acceptance decisions.
- Dynamic link creation, release, failure, and changing topology, including closed loops.
- Continuous coupler engagement variables and engagement-dependent constraint properties (Q36).
- Deterministic replay for the same build and configuration, with stable event ordering and recorded inputs.
- Clear separation between numerical stabilization and physical compliance or damping.
- Documented convergence, constraint error, load accuracy, energy behavior, and sensitivity to timestep and solver settings.
- A documented operating envelope and uncertainty treatment. Results whose uncertainty could change an outcome are classified as uncertain.
- Compatibility with the replaceable interface, with no validation-engine-specific assumptions leaking into production code.

## Implementation sequence

- **Slice 1:** the minimum custom backend for full 3D neutral bodies, gravity, tabletop contact and friction, deterministic stepping, state recording, and replay. Validate suitable equilibrium and contact cases against analytic references. Do not claim this validates the complete formulation.
- **Before slice 2:** publish and preregister the qualification checklist, including the compliant-constraint reference cases and load-accuracy criteria. Thresholds come from evidence, not invention.
- **Slice 2:** fixture-only compliant connections, validating solver-native loads, compliance, and constraint behavior against the preregistered references.
- **Later slices:** extend qualification to topology change, closed loops, reduced coupler mechanisms, and other capabilities as they are implemented. An untested capability is never treated as qualified merely because the interface supports it.

## Dependency and scope constraints

- Validation engines never become hidden production dependencies.
- MuJoCo or any other library is not selected before its suitability and licensing are checked.
- Q35/Q36 requirements are not sacrificed to make the custom solver easier.
- The 10K-Kin throughput target is not a slice 1 or slice 2 acceptance requirement.
- The backend stays replaceable, and results stay exploratory until the relevant models pass validation.
- Backend implementation progress, backend qualification, and Kin candidate feasibility are kept distinct.

## Alternatives considered

- **A. Custom solver only:** a reference independent of our own code would be lost.
- **B. Wrap an established engine (for example Jolt, Bullet, Chrono):** faster contact, but per-axis compliant links, solver-native load accuracy, and in-solve coupler mechanisms would need custom C++ inside the engine. Determinism and stabilization behavior would be inherited rather than chosen.

## Rationale

The requirements a wrapped engine would struggle with are exactly the ones Kinigami exists to get right. An independent reference prevents the validation from agreeing with our own mistakes.
