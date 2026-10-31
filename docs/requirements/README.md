# Requirements specification

The current governing requirements, derived from the [decision log](../decisions/README.md) (Q39).

## Conventions

- **ID:** `<AREA>-<NNN>`. IDs are stable and never reused. A retired requirement keeps its ID with status `superseded`.
- **Sources:** the decision IDs a requirement derives from. `Charter` means the original project instructions (commit `a89d304`). If a requirement and its source disagree, the source governs and the requirement is corrected.
- **Status:**
  - `in_force`: governing now.
  - `open`: required, but its content (a checklist, case list, or schema) has not been written yet. Writing it is scheduled work and needs no owner decision.
  - `unresolved`: needs an owner decision or evidence first. The roadmap names the decision gate.
  - `superseded`: retired, with a pointer to its replacement.
- **Verification:** the planned verification method or case IDs. Evidence status, implementation links, results, and known limitations live in the [traceability map](../traceability.md). A requirement with no traceability entry is **not implemented and not verified**.
- Numerical parameters are never invented here. Where a requirement needs a number that has not been decided, the number is a separate `unresolved` requirement.

## Areas

| Area | File section | Scope |
| --- | --- | --- |
| ENV | [Environment and scale](requirements.md#env--environment-and-scale) | Tabletop, size class, units, validity envelope |
| PHY | [Physics](requirements.md#phy--physics) | Formulation, backend, loads, validation, stepping |
| CPL | [Couplers](requirements.md#cpl--couplers) | Engagement mechanism, docking, retention, release |
| CTL | [Sensing and control](requirements.md#ctl--sensing-and-control) | Information boundary, oracle mode, sensors, compute, targets |
| COM | [Communication](requirements.md#com--communication) | Channels, reachability, timing, routing |
| PWR | [Energy and power](requirements.md#pwr--energy-and-power) | Transfer, limits, faults |
| TIM | [Time, scheduling, replay](requirements.md#tim--time-scheduling-and-replay) | Clock, events, determinism |
| DAT | [Data formats](requirements.md#dat--data-formats) | JSON, binary recordings, hashing, parsing |
| INS | [Inspector](requirements.md#ins--inspector) | Viewer architecture and integrity |
| BLD | [Build and toolchain](requirements.md#bld--build-and-toolchain) | Zig pin, dependencies, build profiles |
| BEN | [Benchmarks and validation](requirements.md#ben--benchmarks-and-validation) | Benchmark definitions and validation cases |
| SEL | [Candidate selection](requirements.md#sel--candidate-selection) | Gates, ranking, originality |
| PRC | [Process and provenance](requirements.md#prc--process-and-provenance) | Records, labels, fixtures, Git |
