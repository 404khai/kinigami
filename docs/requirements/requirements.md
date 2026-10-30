# Kinigami requirements

See [README](README.md) for conventions. Evidence and limitations are in the [traceability map](../traceability.md).

## ENV — Environment and scale

| ID | Requirement | Sources | Status | Verification |
| --- | --- | --- | --- | --- |
| ENV-001 | The reference environment is an ordinary, passive, unpatterned, nonmagnetic, electrically insulating tabletop under Earth gravity. | Q21 | in_force | Configuration review |
| ENV-002 | The tabletop's numerical physical properties (contact and friction parameters, gravity value used) are declared per experiment and justified. | Q21, Q37 | unresolved | Gate: slice 1 validation cases |
| ENV-003 | Kins belong to the 30–60 mm reference size class. The class is a reference scale, not proof of feasibility. | Q1, Q37 | in_force | Gate 1 paper review |
| ENV-004 | Every Kin fits within a common 60 mm diameter enclosing sphere in its mechanically achievable stowed configuration. | Q12, Q37 | in_force | Gate 1 paper review |
| ENV-005 | Deployed geometry, swept volumes, mass, inertia, actuator reach, and clearances are evaluated independently of the size class. | Q37 | in_force | Gates 1–3 |
| ENV-006 | SI units throughout. No hidden constants or geometry assumptions tied to a particular size. | Q37 | in_force | Code review; unit tests |
| ENV-007 | Physical properties derive from the candidate (or fixture) model and its declared components. | Q37 | in_force | Code review |
| ENV-008 | Each physics model documents its validated operating range, including when gravity, contact, friction, adhesion, electrostatics, and magnetic effects may be neglected. | Q37, Q25 | in_force | Envelope documents per model |
| ENV-009 | The engine flags candidates and experiments outside the validated envelope. Such results are exploratory, never validated passes. | Q37 | in_force | Automated envelope checks |
| ENV-010 | Initial tabletop locomotion may start from a documented, mechanically stable orientation. Mandatory self-righting is not required. | Q30 | in_force | Benchmark configuration review |

## PHY — Physics

| ID | Requirement | Sources | Status | Verification |
| --- | --- | --- | --- | --- |
| PHY-001 | Full 3D rigid-body dynamics with mass, inertia, gravity, and collision geometry. No production 2D mode and no artificial planar constraints. | Q31, Q35, Q40, Q41 | in_force | Slice 1 validation cases |
| PHY-002 | Each Kin (and fixture) is a separate rigid body. Links are implicitly solved compliant constraints with declared compliance, damping, limits, and failure behavior. | Q35 | in_force | Slice 2 qualification |
| PHY-003 | The formulation supports dynamic link creation, release, failure, changing topology, and closed loops. | Q35, Q41 | in_force | Later qualification cases |
| PHY-004 | Compliance and load limits are modeled per axis (tension, compression, shear, bending, torsion) where the coupler supports them. Rigid behavior is only an explicitly declared limit. | Q35 | in_force | Slice 2 qualification |
| PHY-005 | Loads used for acceptance (break/detach, retention, stress view, benchmark limits) come from solver-native constraint and contact outputs with documented accuracy. Post-hoc estimates are diagnostic only. | Q35, Q41 | in_force | Qualification checklist |
| PHY-006 | Numerical stabilization is distinguishable from, and never presented as, physical damping or compliance. | Q35, Q36, Q41 | in_force | Qualification checklist |
| PHY-007 | Contact, friction, and link constraints are solved consistently, so loads transfer coherently between tabletop, bodies, and couplers. | Q35, Q41 | in_force | Slices 1–2 validation |
| PHY-008 | If numerical uncertainty overlaps a threshold or could change pass/fail, the result is classified `uncertain`. | Q35, Q41 | in_force | Evaluator tests |
| PHY-009 | A reference-validation suite exists, with analytic statics and a joint-coordinate reference for suitable open chains. Gaps are documented. References are never production paths. | Q35, Q41 | open | Validation suite |
| PHY-010 | The production backend is custom Zig behind the replaceable, project-owned backend interface. | Q15, Q41 | in_force | Code review |
| PHY-011 | Any backend (custom or alternative) is held to the same qualification checklist and stays unqualified until it passes. | Q41 | in_force | Qualification records |
| PHY-012 | The backend qualification checklist is preregistered before slice 2 compliant constraints are implemented. | Q41 | open | Gate: before slice 2 |
| PHY-013 | Quantitative accuracy criteria for the qualification checklist are justified by evidence. | Q41 | unresolved | Gate: before slice 2 |
| PHY-014 | External physics engines are validation-only, adopted after license and technical-fit review, and never enter production builds. | Q41, Q42 | in_force | Dependency audit |
| PHY-015 | Capabilities are qualified one at a time. An untested capability is never treated as qualified because the interface supports it. | Q41 | in_force | Qualification records |
| PHY-016 | Convergence, constraint error, load accuracy, energy behavior, and sensitivity to timestep and solver settings are documented for each qualified capability. | Q35, Q41 | in_force | Qualification records |
| PHY-017 | Fixed-step physics only in slices 1–2. Adaptive or sub-stepped physics requires a new evidence-backed decision. | Q43 | in_force | Code review |
| PHY-018 | Timesteps too coarse for the relevant physical dynamics are flagged as outside the validated envelope. Thresholds come from sensitivity evidence. | Q43, Q37 | in_force | Sensitivity studies |
| PHY-019 | Mechanical fidelity is never reduced to claim throughput. Large-scale throughput is a separate milestone with declared fidelity limits. | Q35, Q41 | in_force | Review |

## CPL — Couplers

| ID | Requirement | Sources | Status | Verification |
| --- | --- | --- | --- | --- |
| CPL-001 | Docking and release use a reduced continuous mechanism model. Discrete states are classifications derived from continuous state and never create, strengthen, or remove connections. | Q36 | in_force | Slice 3 tests |
| CPL-002 | Latch variables (travel, preload, actuator state, wear where supported) are continuous and respect force, torque, speed, energy, and power limits. | Q36 | in_force | Slice 3 tests |
| CPL-003 | Link stiffness, strength, retention, failure, data quality, and power-path quality derive from current physical engagement. Nothing jumps to full strength because a label changed. | Q36, Q33, Q34 | in_force | Slice 3 tests |
| CPL-004 | No docking assistance: no snapping, teleporting, or unmodeled pose or velocity correction. | Q36 | in_force | Code review; energy audit tests |
| CPL-005 | Pre-alignment forces are physically justified by the candidate's actual mechanism. Magnetic attraction is not assumed. | Q36 | in_force | Gate 1 review |
| CPL-006 | The capture window is measured by sweeps (misalignment, relative velocity, approach direction, other justified conditions), never declared. Its uncertainty is documented. | Q36 | in_force | Capture sweeps |
| CPL-007 | The reduced model is validated against detailed close-up full-mechanism references for docking, partial engagement, jamming, loaded retention, and release. | Q36 | open | Gate 3 |
| CPL-008 | Release is a physical process under the current load. It may take time, fail, or be blocked. | Q36 | in_force | Slice 3 tests |
| CPL-009 | Structural retention is passive when unpowered. Bounded independent release remains possible. Passive retention is evaluated under declared loads. | Q11, Q31 | in_force | Retention benchmark |
| CPL-010 | Partial engagement, incomplete release, jamming, damage, and permanent failure are distinguished where the mechanism supports them. Unsupported failure physics is not invented. | Q36 | in_force | Slice 3 and later tests |
| CPL-011 | Coupler geometry and physical parameters are decided and justified. | Q36, Q38 | unresolved | Gate: reduced coupler implementation |

## CTL — Sensing and control

| ID | Requirement | Sources | Status | Verification |
| --- | --- | --- | --- | --- |
| CTL-001 | Acceptance controllers access only modeled sensors, their own internal state and estimates, their own actuator and coupler feedback, messages via modeled communication, and retained information within memory limits. Never authoritative physics state. | Q32 | in_force | Architecture tests (no ground-truth path) |
| CTL-002 | The evaluator uses ground truth without exposing it to controllers. | Q32 | in_force | Architecture tests |
| CTL-003 | Oracle runs are labeled in replay metadata and results, never qualify as a pass, and privileged trajectories are never transferred into acceptance controllers. | Q32 | in_force | Evaluator tests |
| CTL-004 | A modeled sensor interface is mandatory for acceptance. Noise, quantization, and latency reach controllers through it. | Q32 | in_force | Sensor model tests |
| CTL-005 | Each selected sensor documents its measured quantity, range, resolution, update rate, latency, noise, calibration assumptions, and failure behavior. Not every Kin is assumed to have every sensor. | Q32 | in_force | Candidate documentation |
| CTL-006 | The sensor inventory and numerical parameters are justified by candidate hardware or labeled provisional, with sensitivity analysis. | Q32 | unresolved | Gate: controller and benchmark implementation |
| CTL-007 | Finite onboard computation and memory. Physics continues while computation is pending. Outputs become available after the declared compute latency. | Q22, Q32, Q43 | in_force | Scheduler tests |
| CTL-008 | The target is delivered to one designated Kin through its normal interface and propagates only via modeled communication. The designated Kin has a software role only. | Q32 | in_force | Benchmark design |
| CTL-009 | The target describes a desired collective shape, preferably as relative geometry, never trajectories, actuator histories, or attachment sequences. | Q32 | in_force | Benchmark review |
| CTL-010 | The target-shape representation is decided. | Q32 | unresolved | Gate: shape-based control |

## COM — Communication

| ID | Requirement | Sources | Status | Verification |
| --- | --- | --- | --- | --- |
| COM-001 | Through-coupler and short-range contactless channels are separately modeled, optional capabilities. Each candidate declares its channels and their hardware-grounded parameters. | Q33 | in_force | Candidate documentation |
| COM-002 | Reachability derives from authoritative physical state, never from a manually maintained neighbor list. | Q33 | in_force | Architecture tests |
| COM-003 | Coupler-channel availability and quality derive from coupler state (engagement, alignment, degradation, separation). Partial engagement is never perfect. | Q33, Q36 | in_force | Communication tests |
| COM-004 | Contactless reachability derives from geometry, range, occlusion, and other applicable effects. | Q33 | in_force | Communication tests |
| COM-005 | Communication is never instantaneous merely because Kins share a process. Latency, bandwidth or rate limits, ordering, queuing, and loss are modeled as relevant. | Q32 | in_force | Communication tests |
| COM-006 | Message paths, channels, delays, losses, and outcomes are recorded for replay. | Q33 | in_force | Replay tests |
| COM-007 | Communication reliability, timing, and numerical parameters are justified by evidence. | Q32, Q33 | unresolved | Gate: connected-chain benchmark |
| COM-008 | The mapping from coupler mechanical state to communication performance is justified by component evidence. | Q33 | unresolved | Gate: coupler communication model |

## PWR — Energy and power

| ID | Requirement | Sources | Status | Verification |
| --- | --- | --- | --- | --- |
| PWR-001 | Power transfer is optional and declared per candidate, and only through a mechanically engaged coupler with a functioning power path. Engagement does not imply electrical continuity. | Q34 | in_force | Power model tests |
| PWR-002 | Energy, power, and thermal limits are enforced per Kin as well as at the assembly level. | Q34 | in_force | Evaluator tests |
| PWR-003 | No automatic balancing. Transfers come only from controller commands or declared passive circuitry. | Q34 | in_force | Power model tests |
| PWR-004 | Resistance, voltage drop, current and power limits, conversion losses, heating, and fault protection are modeled where applicable, within validated fidelity. | Q34 | in_force | Power model validation |
| PWR-005 | Every transfer records its source, destination, path, amount, losses, and heat. | Q34 | in_force | Replay tests |
| PWR-006 | Faults and depleted or disconnected Kins have explicit outcomes. | Q34 | in_force | Fault tests |
| PWR-007 | Power-transfer numerical parameters are justified by component evidence. | Q34 | unresolved | Gate: power-sharing experiments |
| PWR-008 | Actuator and thermal model fidelity is decided. | Q31, Q34 | unresolved | Gate: detailed Kin models |

## TIM — Time, scheduling, and replay

| ID | Requirement | Sources | Status | Verification |
| --- | --- | --- | --- | --- |
| TIM-001 | Simulation time is an integer tick count with a declared time unit per experiment, never a floating-point accumulator. | Q43 | in_force | Unit tests |
| TIM-002 | The fixed physics timestep is an integer multiple of the time unit. | Q43 | in_force | Configuration validation tests |
| TIM-003 | Time arithmetic detects overflow and never wraps silently. | Q43 | in_force | Unit tests |
| TIM-004 | Events are totally ordered by `(scheduled_tick, event_phase, source_id, sequence_number)` or an equivalent stable key with an explicitly specified phase order. | Q43 | in_force | Scheduler tests |
| TIM-005 | Event semantics: messages and compute completions occur at their scheduled tick, sensors sample the most recently completed physics state, controller outputs appear after their compute latency, and actuator commands take effect at the next physics boundary. | Q43 | in_force | Scheduler tests |
| TIM-006 | Sensor records hold both the requested and the actually-sampled state timestamps. Actuator records hold both the command-ready and the effective application timestamps. | Q43 | in_force | Recording tests |
| TIM-007 | All randomness is explicitly seeded and recorded. Host wall-clock time never sets simulated timing. | Q32, Q43 | in_force | Replay tests |
| TIM-008 | Exact replay is guaranteed for the same build and configuration. Cross-platform bitwise identity is not promised. | Q14, Q42 | in_force | Replay tests |
| TIM-009 | Deterministic parallelism partitions work independently of worker count and uses fixed-order reductions, with no unordered floating-point atomic accumulation. The core stays single-threaded until this is verified. | Q42 | in_force | Code review; replay tests |
| TIM-010 | Timestep-sensitivity studies measure changes in sensed-state age and actuator boundary delay. | Q43, Q35 | in_force | Sensitivity studies |
| TIM-011 | Each run records its time unit, physics timestep, and scheduler configuration. | Q43 | in_force | Recording tests |
| TIM-012 | The time unit and physics timestep for slice 1 validation are declared and justified. | Q43 | unresolved | Gate: slice 1 validation cases |

## DAT — Data formats

| ID | Requirement | Sources | Status | Verification |
| --- | --- | --- | --- | --- |
| DAT-001 | Criteria, run configurations, and results are JSON with an explicit schema version. | Q44 | in_force | Parser tests |
| DAT-002 | Recordings use a versioned binary format with a magic identifier, explicit little-endian encoding, and exact float bit patterns. Raw Zig structs are never serialized. | Q44 | in_force | Format tests |
| DAT-003 | File identity hash: SHA-256 over exact file bytes, without normalization. | Q44 | in_force | Hash tests |
| DAT-004 | Checkpoint state hash: SHA-256 over a canonical state encoding (defined field order, integer widths, endianness, float bits; no addresses or padding). | Q44 | in_force | Replay tests |
| DAT-005 | Strict parsing rejects unknown fields, missing required fields, duplicate keys, type mismatches, invalid enums, out-of-range values, and malformed or trailing content. | Q44 | in_force | Parser conformance tests |
| DAT-006 | Defaults exist only where the schema defines them. Resolved defaults appear in the effective configuration. | Q44 | in_force | Parser tests |
| DAT-007 | JSON integers are bounded below 2^53 or encoded as strings, as defined per field. | Q44 | in_force | Schema tests |
| DAT-008 | Non-finite floats are forbidden or explicitly encoded, never silently mapped to `null`. | Q44 | in_force | Parser tests |
| DAT-009 | Decimal-to-binary64 conversion is specified (round to nearest, ties to even) and verified against the pinned Zig version. | Q44 | in_force | Toolchain conformance tests |
| DAT-010 | Readers identify the version before interpreting content and reject unsupported versions. Migrations create new artifacts, preserve originals, and record the source version, target version, and tool version. | Q44 | in_force | Format tests |
| DAT-011 | Results identify the exact criteria, configuration, recording, code revision, acceptance build profile, candidate version, and run ID. | Q39, Q44 | in_force | Evaluator tests |

## INS — Inspector

| ID | Requirement | Sources | Status | Verification |
| --- | --- | --- | --- | --- |
| INS-001 | The inspector is a separate native Zig executable. Its graphics library belongs only to the inspector. | Q45 | in_force | Build graph review |
| INS-002 | The graphics library is selected only after a license, maintenance, platform, and technical-fit review. | Q45, Q42 | open | Library review record |
| INS-003 | The recording reader is reusable Zig code, separate from rendering. | Q45 | in_force | Code review |
| INS-004 | The inspector is read-only. It cannot access mutable simulation state, command Kins, or affect the evaluator. | Q42, Q45 | in_force | Architecture review |
| INS-005 | It displays only solver-produced or recorded values. Unrecorded values are shown as unavailable, never estimated. | Q45 | in_force | Inspector tests |
| INS-006 | Live viewing uses a one-way, non-blocking, bounded, preallocated snapshot stream with dropped-frame accounting and no backpressure. | Q45 | in_force | Stream tests |
| INS-007 | Capture isolation: otherwise identical runs with and without live capture produce matching checkpoint state hashes. Publication never draws from the simulation RNG or creates scheduled events. | Q45 | in_force | Replay test (VC-REPLAY-CAPTURE) |
| INS-008 | Interpolation is display-only, optional, and visibly labeled. Measurements, contact and force inspection, and cutaways use exact recorded states. | Q45 | in_force | Inspector tests |
| INS-009 | Fixtures, oracle runs, and exploratory results are visibly labeled. | Q40, Q45 | in_force | Inspector review |
| INS-010 | Long-term inspection views: swarm, cluster, exploded, cutaway, assembly cutaway, stress, signal, articulation, energy. | Charter, Q31 | open | Later phases |

## BLD — Build and toolchain

| ID | Requirement | Sources | Status | Verification |
| --- | --- | --- | --- | --- |
| BLD-001 | One exact tagged stable Zig release is pinned with its distribution content hash. Upgrades require a decision record plus replay and validation reruns. | Q42 | in_force | Toolchain verification script |
| BLD-002 | The simulation core uses only the Zig standard library, with no third-party runtime dependencies. | Q42 | in_force | Build graph review |
| BLD-003 | Direct and transitive dependencies are pinned by content hash, with licenses recorded. | Q42 | in_force | Dependency audit |
| BLD-004 | Validated-acceptance results require a declared acceptance build profile: compiler version and hash, target triple, explicit CPU feature baseline (no host autodetection), optimization level, float mode, fused-operation policy, flags, and dependency lock state. | Q42 | in_force | Profile record in results |
| BLD-005 | The acceptance profile's optimization level is chosen and frozen before the first validated acceptance run. | Q42 | unresolved | Gate: first validated acceptance run |
| BLD-006 | Results from non-acceptance profiles stay exploratory until shown to match the acceptance profile across the relevant validation suite. | Q42 | in_force | Evaluator labeling |

## BEN — Benchmarks and validation

| ID | Requirement | Sources | Status | Verification |
| --- | --- | --- | --- | --- |
| BEN-001 | Five-Kin tabletop articulation benchmark: identical Kins, engaged chain, documented stable start, onboard actuation, no clamps, rails, prescribed trajectories, or planar constraints, and a curvature change with all required links preserved. | Q31 | in_force | Benchmark definition |
| BEN-002 | Shape success uses relative metrics that exclude whole-chain translation and rotation. The permissible out-of-plane deviation is defined before acceptance. | Q31 | in_force | Evaluator tests |
| BEN-003 | All benchmark thresholds (completion time, shape error, settling, energy, loads, thermal, uncertainty cases) are preregistered and never chosen after results. | Q31, Q38, Q39 | in_force | Criteria hash precedes results |
| BEN-004 | Actively maintained and passively locked configurations are distinguished. Passive retention is evaluated separately under declared loads. | Q31, Q11 | in_force | Retention benchmark |
| BEN-005 | The first articulation benchmark requires an energy-isolated baseline. A power-sharing variant is reported separately. | Q34 | in_force | Benchmark definition |
| BEN-006 | Through-chain propagation is a separate criterion. Contactless shortcuts don't count toward it. | Q33 | in_force | Benchmark definition |
| BEN-007 | A future base-anchored cantilever benchmark. | Q31 | open | Later phase |
| BEN-008 | Slice 1 analytic validation cases, reference conditions, and tolerances are decided and preregistered before solver code is written. | Q40, Q41 | unresolved | Gate: slice 1 validation cases |
| BEN-009 | Benchmark acceptance is separate from candidate ranking. | Q38 | in_force | Process review |

## SEL — Candidate selection

| ID | Requirement | Sources | Status | Verification |
| --- | --- | --- | --- | --- |
| SEL-001 | About 2–4 structurally distinct, credible candidates. No quota fillers. | Q38 | in_force | Selection record |
| SEL-002 | Gate 1 (paper), Gate 2 (reduced model), Gate 3 (detailed validation), then selection among survivors. | Q38 | in_force | Gate records |
| SEL-003 | Gates are hard pass/fail. Ranking among survivors follows the priority order originality → plausibility → connection clarity → scalability → visual quality, with the scoring method documented before scoring. | Q38, Charter | in_force | Selection record |
| SEL-004 | Gate criteria are preregistered. Changes record the original and revised versions, reason, date, and reruns. Criteria without sufficient evidence are marked unresolved. | Q38, Q39 | in_force | Criteria history |
| SEL-005 | Originality is reviewed at Gate 1 and at final visuals, recording the references reviewed, the reasoning, and the changes made. No claim of absolute originality. | Q38 | in_force | Review records |
| SEL-006 | The originality-review procedure is defined. | Q38 | unresolved | Gate: candidate generation |
| SEL-007 | Rejected candidates and failure reasons are preserved. Revisions are versioned and retested against the same criteria. Candidates get equivalent conditions. | Q38 | in_force | Selection record |
| SEL-008 | No exhaustive parameter optimization until the models and benchmarks are validated. | Q38 | in_force | Process review |
| SEL-009 | No copying of Big Hero 6 microbots or any other existing fictional or real robot design. | Charter | in_force | Originality reviews |

## PRC — Process and provenance

| ID | Requirement | Sources | Status | Verification |
| --- | --- | --- | --- | --- |
| PRC-001 | The decision log is append-only, with stable IDs and supersession records. Old records are never rewritten. | Q39 | in_force | Git history |
| PRC-002 | This specification maintains stable IDs, sources, and status. | Q39 | in_force | Review |
| PRC-003 | Criteria are machine-readable and hash-linked to every result. | Q39, Q44 | in_force | Evaluator tests |
| PRC-004 | A traceability map links requirements to implementation, verification, results, and limitations. Unvalidated requirements stay visibly unvalidated. | Q39 | in_force | Review |
| PRC-005 | Every result carries exactly one status label: `exploratory` (default), `oracle`, `fixture`, `uncertain`, or `validated_acceptance`. | Q32, Q35, Q37, Q40 | in_force | Evaluator tests |
| PRC-006 | Test fixtures are labeled in source, data, logs, and the inspector. They never enter candidate selection or establish feasibility. | Q40 | in_force | Code review |
| PRC-007 | First milestone: slice 1 (body and tabletop), slice 2 (compliant connection), slice 3 (reduced coupler engagement), all on production 3D architecture. | Q40 | in_force | Roadmap |
| PRC-008 | Q1–Q30 wording is never fabricated. Reconstructions are labeled. | Q39 | in_force | Review |
| PRC-009 | No push, public PR, or history rewrite without explicit owner authorization. | Q39 | in_force | Process |
| PRC-010 | Project licensing is decided before public release. | — | unresolved | Gate: public release |
| PRC-011 | CI and validation policy is decided before automated project-wide acceptance. | — | unresolved | Gate: CI |
