# Q35 — Physics formulation and link representation

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-10-30 |
| Supersedes | — |
| Provenance | condensed from owner decision |

## Context

Q31 needs measured joint and coupler loads, Q11 needs retention judged under declared loads, and links must form and break continuously, including in closed loops.

## Decision

1. **Option D — separate rigid bodies with implicitly solved compliant constraints.** Each Kin is a separate rigid body. Links are constraints with explicitly declared compliance, damping, limits, and failure behavior. The formulation supports changing topology and closed loops without treating assemblies as welded solids. This selects a formulation, not a library or solver implementation.
2. **Acceptance loads come from the solver's own constraint and contact outputs, with documented accuracy.** This applies to break and detach decisions, passive-retention checks, stress visualization, Q31 load limits, and other claims of mechanical feasibility. Post-hoc estimates may be used for visualization or diagnostics, but never silently substitute in acceptance decisions.
3. **A separate reference-validation suite is required.** It includes a joint-coordinate reference for suitable open chains and analytic statics for configurations with known solutions. These are validation tools, not production paths. Where a reference cannot represent a case, document the gap and use another justified method.

## Constraints

- Model compliance and load limits per axis (tension, compression, shear, bending, torsion) where the actual coupler supports them. Couplers do not share identical degrees of freedom or stiffness.
- Fully rigid behavior is an explicitly declared limiting case, not a default.
- Model finite stiffness, damping, joint travel, actuator limits, and load-dependent failure with evidence-supported parameters. Solver stabilization must never be mistaken for physical damping or compliance.
- Solve contact, friction, and link constraints so that load transfer between tabletop contacts, bodies, and couplers is consistent.
- Validate load accuracy, constraint error, energy behavior, convergence, and sensitivity to timestep and solver settings.
- Document the operating envelope and uncertainty of every acceptance load quantity. If uncertainty overlaps a failure threshold or could change pass/fail, the result is **uncertain**, not a pass.
- Preserve deterministic replay and the separation of simulation time from rendering time.
- Keep the backend replaceable (Q15). A candidate backend must demonstrate topology, compliance, load-reporting, replay, and validation capabilities before serving as the reference implementation.
- Do not sacrifice mechanical fidelity to claim 10K-Kin scalability. Large-scale throughput is a separate milestone with declared fidelity and validation limits.
- The library, algorithm, integrator, tolerances, and numbers remain open until benchmarked against the validation suite.

## Alternatives considered

- **A. Separate bodies with hard joint constraints:** iterative drift, approximate forces, and "rigid" meaning only whatever the solver converged to.
- **B. Joint-angle (Featherstone-style) coordinates:** exact for trees, but a rebuild on every topology change and poor support for loops.
- **C. Explicit spring-damper links:** tiny timesteps, or softening that becomes invented physics.

## Rationale

Supports arbitrary changing topology and loops, keeps stiff links stable at practical timesteps, makes compliance a declared physical property, and yields solver-native loads whose accuracy can be measured.
