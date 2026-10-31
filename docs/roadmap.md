# Roadmap

Derived from the dependencies between recorded decisions and requirements. This is a living document, updated as evidence and decisions arrive. Phase names here are for planning only and never appear in branch names, commits, or PR text.

**Status vocabulary** (not interchangeable): planned → in progress → implemented → tested → validated → qualified → accepted.

## Dependency overview

```text
Records ──► Toolchain ──► Core infrastructure ───────────┐
                │                                         ▼
                ├──► Slice 1 preregistration ──► Slice 1 physics ──► Qualification checklist ──► Slice 2 compliant links ──► Slice 3 coupler fixture
                │       [gate: cases, tolerances, tick, dt]   ▲                                                                       │
                └──► Inspector library review ──► Minimal inspector ───┘ (capture-isolation test)                                     │
                                                                                                                                      ▼
Candidate generation ──► Gate 1 (paper) ─────────────────────────────────────────────────────────────────────────► Kin subsystem models ──► Gate 2 ──► Q31 benchmark ──► Gate 3 + selection
 [gate: originality procedure]                                                                                     [gates: sensors, actuators/thermal, comms]
                                                                                       ──► Inspection depth ──► Robustness ──► Extended assemblies ──► Scaling ──► Release
```

## Phases

### R0 — Repository intake and decision records

- **Objective:** preserve the existing state, establish the Q39 record structure, and make `AGENTS.md` a concise entry point.
- **Deliverables:**
  - baseline commit of the original `AGENTS.md`
  - decision log (Q1–Q45)
  - requirements specification
  - traceability map
  - this roadmap
  - refactored `AGENTS.md`
- **Depends on:** nothing.
- **Exit:** records committed locally, with every Q41–Q45 constraint represented.
- **Status:** implemented.

### R1 — Toolchain and build foundation

- **Objective:** a reproducible, pinned build with the std-only core boundary, plus verified parser and hash behavior on the pinned compiler.
- **Deliverables:**
  - Zig pin with SHA-256 and a fetch/verify script
  - `build.zig` with the std-only core module (the inspector executable is added in R5, not as an empty placeholder)
  - SHA-256 file-hash utility
  - conformance tests for `std.json` strictness (unknown fields, duplicate keys, trailing content, types), integer bounds, non-finite handling, and correctly rounded decimal parsing
  - draft acceptance build profile, with optimization level left unresolved
- **Depends on:** R0.
- **Requirements:** BLD-001–004, BLD-006, DAT-003, DAT-005, DAT-007–009.
- **Exit:** `zig build test` passes under the pinned compiler, the verify script confirms the compiler hash, and conformance results are recorded in traceability.
- **Status:** tested. Finding: `std.json` is lenient in 7 documented ways, so R3 must add a strict JSON layer (see `docs/toolchain.md`).

### R2 — Slice 1 validation preregistration

- **Objective:** preregister slice 1's analytic validation cases **before any solver code exists** (Q40, Q41).
- **Decided (Q46):** the five analytic cases, and validation-only fixture forces confined to `fixture_validation` runs.
- **Decided (Q47):** Coulomb friction with separate static and kinetic coefficients.
- **Remaining decision gates (owner), one at a time:** friction coefficients, fixture geometries and mass properties (including a separate tipping fixture if needed), gravity value, tolerances and uncertainty treatment, time unit, and physics timestep (BEN-014, ENV-002, TIM-012).
- **Deliverables:**
  - criteria JSON schema v1
  - strict criteria parser
  - slice 1 criteria file(s) committed, with SHA-256 recorded before solver work begins
- **Depends on:** R1 (hashing) and the strict JSON layer from R3. The owner's decisions can be gathered in parallel.
- **Exit:** criteria committed and hashed. Optionally externally timestamped if the owner wants stronger preregistration evidence (Q39).

### R3 — Deterministic core infrastructure (parallel with R2)

- **Objective:** the non-physics backbone every slice relies on.
- **Deliverables:**
  - integer clock with overflow checks
  - event scheduler with explicit phase order and total ordering
  - seeded, recorded RNG
  - strict JSON layer over `std.json` that rejects the 7 lenient behaviors recorded in `docs/toolchain.md`
  - run configuration JSON (strict, with resolved defaults)
  - canonical state encoding and checkpoint hash
  - binary recording format v1 (magic, version, little-endian, exact float bits) with a separate reader module
  - results JSON with full provenance
  - evaluator skeleton with the PRC-005 status labels
  - backend interface (Q15) with no solver yet
  - non-blocking snapshot publication interface
- **Depends on:** R1. **Not blocked by** the R2 gate, because none of this is solver code.
- **Requirements:** TIM-001–009, TIM-011, DAT-001–011, CTL-002, PHY-010, PRC-005, INS-006.
- **Exit:** unit tests and round-trip tests pass, and replay of a physics-free scheduled run reproduces its checkpoint hashes.
- **Status:** tested (exit criterion met with a physics-free stand-in backend). Built: integer clock, scheduler, RNG interface, strict JSON layer, core purity check, canonical encoding and checkpoint hashing, recording container v1, run configuration and results schema v1 with run classes and labels, backend interface, snapshot ring, fixed-step driver with replay and capture-isolation tests. **Carried forward:** recording payload layouts and snapshot interval (open), RNG algorithm (open), event-phase order (open), Git revision and build-profile capture for result provenance, serialized effective configuration, inspector transport (R5).

### R4 — Slice 1 physics: neutral body and tabletop contact

- **Objective:** a minimum custom Zig backend with full 3D rigid bodies, gravity, fixture collision geometry, tabletop contact and friction, and solver-native contact outputs.
- **Depends on:** R2 (criteria preregistered) and R3.
- **Exit:**
  - preregistered slice 1 cases evaluated, with results labeled `fixture` / `exploratory` or validated for those specific cases only
  - replay test passes
  - capture-isolation test passes (INS-007)
  - envelope documented for what was validated
- **Not claimed:** formulation validity in general, or compliant constraints.

### R5 — Minimal inspector (review parallel with R2–R4)

- **Objective:** a read-only native viewer (Q45 scope) over recordings and the live stream.
- **Steps:**
  - graphics library review: license, maintenance, platforms, fit; sokol is a candidate (INS-002)
  - pin the chosen library by hash
  - build the viewer
- **Depends on:** the R3 reader and stream for implementation. The review can start now.
- **Exit:** viewer shows only recorded values, unavailable values are marked, interpolation is labeled, and the capture-isolation test is green.

### R6 — Backend qualification checklist

- **Decision gate (owner):** quantitative accuracy criteria and reference cases for compliant constraints (PHY-012, PHY-013).
- **Deliverables:**
  - qualification checklist as machine-readable criteria
  - external reference-engine license and fit review (MuJoCo or another candidate, validation-only)
- **Depends on:** R4 evidence (it informs what is achievable without lowering the bar).
- **Exit:** checklist preregistered and hashed **before** R7 code.

### R7 — Slice 2: compliant connection

- **Objective:**
  - fixture-only compliant constraints with per-axis compliance, damping, limits, and solver-native loads
  - analytic statics cases plus an independent reference comparison
  - stabilization kept separate from physical damping
- **Depends on:** R6.
- **Exit:** the qualification checklist items for these capabilities are evaluated, and the envelope is documented.

### R8 — Slice 3: reduced coupler engagement (fixture)

- **Decision gate (owner):** fixture coupler stand-in geometry and physical parameters (CPL-011, fixture scope).
- **Objective:**
  - continuous latch variables, contact-driven alignment, and engagement-dependent constraint strength
  - physical release under load
  - capture-window sweeps
  - no assist
- **Depends on:** R7.
- **Exit:** sweeps and qualification items recorded, plus an energy-audit test showing no unmodeled forces.

### R9 — Candidate generation and Gate 1 (paper) — parallel track

- **Decision gate (owner):** originality-review procedure (SEL-006).
- **Objective:** 2–4 structurally distinct candidates with:
  - Q12 packaging
  - evidence-backed component lists
  - mass, energy, and power budgets
  - coupler layout
  - originality review
- **Depends on:** R0 only, so it can run alongside R1–R8.
- **Exit:** Gate 1 criteria preregistered, then evaluated, with rejected candidates preserved.

### R10 — Kin subsystem models

- **Decision gates (owner):**
  - sensor inventory and parameters (CTL-006)
  - actuator and thermal fidelity (PWR-008)
  - communication reliability and timing (COM-007, COM-008)
  - power-transfer parameters, only if any candidate declares transfer (PWR-007)
- **Objective:**
  - sensing layer, communication layer (both channel types, reachability from physical state), actuator models, energy/thermal models
  - controller runtime with finite compute and memory
- **Depends on:** R3, R8, and surviving Gate 1 candidates.

### R11 — Gate 2 (reduced-model feasibility)

- **Objective:** locomotion, docking, retention, and load transfer for the surviving candidates under production physics, against preregistered Gate 2 criteria.
- **Depends on:** R10.

### R12 — Q31 articulation benchmark

- **Decision gate (owner):** target-shape representation (CTL-010) and benchmark thresholds (BEN-003).
- **Deliverables:**
  - benchmark criteria preregistered
  - decentralized controllers
  - energy-isolated baseline
  - separate through-chain propagation criterion
  - oracle diagnostic runs, labeled
- **Depends on:** R11.

### R13 — Gate 3 and selection

- **Objective:**
  - detailed close-up mechanism references (CPL-007)
  - sensitivity and uncertainty analysis
  - weighted comparison among survivors with a pre-documented scoring method
  - second originality review
  - published selection record
- **Depends on:** R12.

### R14 — Inspection depth

- **Objective:** cutaway, exploded, assembly cutaway, stress, signal, articulation, and energy views (INS-010), all from recorded state.
- **Depends on:** R5, plus the recorded data from R10–R13. Parts can start once the relevant data is recorded.

### R15 — Robustness and faults

- **Decision gate (owner):** failure-injection and repair semantics.
- **Objective:** tolerance and uncertainty campaigns (Q25), fault injection, depletion and disconnection outcomes, local repair.
- **Depends on:** R13.

### R16 — Extended assemblies

- **Objective:** cantilever benchmark (BEN-007), branching chains, lattices, closed-loop qualification.
- **Depends on:** R13, plus PHY-003 qualification.

### R17 — Scaling and distribution

- **Decision gate (owner):** distributed execution semantics.
- **Objective:** deterministic parallelism (TIM-009), world partitioning, multi-machine execution, and 10K-Kin throughput with declared fidelity.
- **Depends on:** R16. Correctness comes before scale.

### R18 — CI and release

- **Decision gates (owner):** CI and validation policy (PRC-011, before automated project-wide acceptance) and project licensing (PRC-010, before public release).
- **Note:** local check scripts exist from R1. Hosted CI requires push authorization.

## Parallelism

| Can run concurrently | Strictly sequential |
| --- | --- |
| R2 ∥ R3 ∥ R5 (library review) ∥ R9 | R2 → R4 (no solver code before criteria) |
| R14 parts alongside R10–R13 | R6 → R7 → R8 |
| | R10 → R11 → R12 → R13 |

## Decision gates (owner)

| Gate | Requirement IDs | Blocks | Needed when | Evidence to bring |
| --- | --- | --- | --- | --- |
| Slice 1 reference conditions, tolerances, time unit, timestep (cases decided in Q46) | BEN-014, ENV-002, TIM-012 | R2 → R4 | **Next** | Analytic solutions, literature values for fixture contact and friction, sensitivity rationale |
| Qualification checklist accuracy criteria | PHY-012, PHY-013 | R7 | After R4 | R4 results, reference-engine review |
| Fixture coupler stand-in parameters | CPL-011 | R8 | After R7 | Mechanism sketch, component analogues |
| Originality-review procedure | SEL-006 | R9 Gate 1 | Before candidate evaluation | Reference corpus, review method options |
| Sensor inventory and parameters | CTL-006 | R10 | After Gate 1 | Candidate component datasheets |
| Actuator and thermal fidelity | PWR-008 | R10 | After Gate 1 | Actuator datasheets, thermal estimates |
| Communication parameters | COM-007, COM-008 | R10, R12 | After Gate 1 | Channel hardware evidence |
| Power-transfer parameters | PWR-007 | Power-sharing variant | If any candidate declares transfer | Contact and electrical data |
| Target-shape representation | CTL-010 | R12 | After R11 | Controller interface prototypes |
| Acceptance optimization level | BLD-005 | First validated acceptance run | Before first validated run | Replay and performance comparison across levels |
| Failure-injection and repair semantics | — | R15 | After R13 | Fault taxonomy |
| Distributed execution semantics | — | R17 | After R16 | Partitioning prototypes |
| CI and validation policy | PRC-011 | R18 | Before automated acceptance | — |
| Project licensing | PRC-010 | Public release | Before release | — |
