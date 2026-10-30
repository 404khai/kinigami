# AGENTS.md

## Project

**Codename:** Kinigami [Kinetic Origami], A distributed programmable matter engine built in Zig.
**Type:** Distributed swarm-agent simulation in Zig
**Goal:** Build an original programmable-matter / swarm-robot simulation inspired by the _idea_ of self-organizing robotic matter, but **not copying** the design, silhouette, or mechanical language of any existing film or franchise.

The unit of the swarm is called a **Kin**.

---

## 0. Read this first

### 0.1 Document hierarchy (Q39)

Kinigami is governed by four authoritative records plus this file:

| Record | Purpose | Status |
| --- | --- | --- |
| Decision log | Ordered, append-only decision records with stable IDs, rationale, consequences, and links to superseded decisions | **Not yet created** |
| Requirements specification | Current requirements grouped by subsystem, with stable IDs, source decision IDs, status (`in_force`, `open`, `unresolved`, `superseded`), and acceptance implications | **Not yet created** |
| Machine-readable criteria | Benchmark and selection-gate definitions read directly by the evaluator, including thresholds, uncertainty treatment, and required evidence | **Not yet created** |
| Traceability map | Requirement → benchmark → validation case → recorded result. Unvalidated requirements stay visibly unvalidated | **Not yet created** |

`AGENTS.md` is the concise entry point. Once the records above exist, it links to them rather than duplicating them.

**Interim rule:** until the decision log and requirements specification exist, **§3 Governing decisions** in this file is the interim record. Where design guidance elsewhere in this file conflicts with §3, §3 governs.

### 0.2 Rules for every agent

- Read §3 (and, once they exist, the authoritative records) before implementing or evaluating anything.
- Never silently change a requirement, criterion, or threshold. Supersede it with a new decision record that preserves the original and revised versions, the reason, the date, the affected evaluations, and the required reruns.
- Do not invent numerical parameters. Derive them from documented components or justified engineering estimates, or label them explicitly as provisional. Where evidence is insufficient, mark the criterion `unresolved`.
- Do not select the final Kin geometry, coupler mechanism, articulation mechanism, or components outside the Q38 selection process.
- Always distinguish **exploratory**, **oracle/diagnostic**, and **test-fixture** results from **validated acceptance** results.
- Do not commit, push, or rewrite Git history without explicit authorization.

### 0.3 Provenance of the decision summaries

- Q31–Q40 in §3 are condensed summaries of the user's accepted decisions. They are not verbatim transcripts.
- The original text of Q1–Q30 is not available in this workspace. §3.11 lists only what later decisions state about them. Do not reconstruct, paraphrase beyond that, or present any reconstruction as original wording. Verbatim archival requires the user to supply the original thread.

---

## 1. Core mission

This project simulates a large population of autonomous Kins that:

- move independently
- communicate locally
- interlink into chains, lattices, and load-bearing structures
- detach and reconfigure dynamically
- self-repair damaged structures
- support close-up mechanical visualization
- support cutaway and cross-sectional inspection of single Kins and assemblies

The simulation must emphasize:

1. **local rules producing global behavior**
2. **physically plausible interlinking**
3. **clear visual explanation of how a Kin works internally**
4. **original industrial/mechanical design**
5. **performance and scalability in Zig**

---

## 2. Non-goals

Do **not**:

- copy the visual design of Disney / Big Hero 6 microbots
- replicate exact shape language, silhouettes, or motion signatures from copyrighted source material
- build only a particle effect with fake cohesion
- hardcode cinematic motion without believable connection logic
- optimize for aesthetics at the expense of simulation architecture

This is a **systems project first**, a visual project second.

---

## 3. Governing decisions

### 3.1 Q31 — Tabletop-supported connected-chain articulation

- The first mandatory chain-articulation benchmark: **five mechanically identical Kins** in a connected chain, all required links engaged, resting on the Q21 reference tabletop, deliberately change the chain's curvature using onboard actuators while keeping every required link connected.
- Not permitted: clamps, guide rails, prescribed body trajectories, artificial planar constraints, or external stabilization. Endpoints move only through modeled contact.
- **Full 3D physics stays active:** gravity, contact, friction and slip, joint compliance, structural loads, body rotation and tipping, out-of-plane motion, collisions, and actuator dynamics. Any lifting, rolling, twisting, or tipping must emerge from the simulation. The permissible out-of-plane deviation is defined before final acceptance testing.
- Success is measured with relative shape metrics that exclude whole-chain translation and rotation.
- **Defined before testing:** initial geometry and topology, target transformation, maximum completion time, permitted shape error, settling behavior, energy, actuator and coupler load limits, thermal limits, and uncertainty cases. No thresholds may be chosen after observing results. Q14 and Q25 validation, replay, and operating-envelope principles apply.
- Actively maintained shapes and passively locked shapes are distinct. Passive retention (Q11) is evaluated separately under declared loads. Do not assume every reachable curvature can be locked without power.
- This benchmark does **not** establish unsupported lifting, cantilever articulation, unsupported spans, gravity-loaded 3D reconfiguration, arbitrary spatial curvature, cooperative traversal, or large-scale assembly. A future base-anchored **cantilever benchmark** is planned.
- The inspector must eventually show initial, intermediate, and final configurations, articulation playback, joint and coupler loads, contact and friction, centerline and curvature overlays, out-of-plane deviation, energy and actuator timelines, and mechanism close-ups and cutaways. All of it must come from the authoritative simulated state.

### 3.2 Q32 — Controller information boundary

- **Physics engine and evaluator** may access ground truth: exact poses, joint configurations, contacts, topology, forces, actuator states, resource use, and full history.
- **Acceptance controllers** may access only: their modeled onboard sensors, their own internal state and permitted estimates, feedback from their own actuators and couplers, messages received through modeled communication, and retained information within declared memory limits. Controllers never read authoritative physics state.
- **Oracle mode** is permitted only for labeled development and diagnostic runs. It is labeled in replay metadata and results and can never qualify as a pass. Privileged trajectories must not be transferred into acceptance controllers as prescribed poses or actuator sequences.
- **Target delivery:** the target goes to one designated Kin through its normal communication interface and propagates only through modeled communication. No Kin receives a snapshot of global geometry, pose, or topology. The designated Kin has a software role only, with no extra mechanics, sensing, or compute.
- **Target semantics:** the target describes a desired collective shape, preferably as relative geometry. It does not prescribe body trajectories, actuator histories, or attachment sequences. The exact representation is still open.
- **Sensor models are mandatory** for acceptance. Each selected sensor documents its measured quantity, range, resolution, update rate, latency, noise, calibration assumptions, and failure behavior. Noise, quantization, and latency reach controllers through the sensor interface, not only through visualization. Do not assume every Kin has every sensor.
- **Communication is never instantaneous** merely because all Kins share a process. Document range, latency, bandwidth, ordering, queuing, loss, and energy as relevant to the selected hardware.
- **Determinism:** seeded randomness, deterministic sampling, delivery, queue processing, and scheduling, and simulated time only. Host wall-clock time never sets latency or timing. Physics continues while Kins wait.
- Q22 finite computation and memory apply to message processing, observations, estimates, and accumulated topology knowledge.

### 3.3 Q33 — Communication channels

- The architecture supports two separately modeled, **optional** channels: a **through-coupler** channel and a **short-range contactless** channel. Each candidate declares which channels it has, along with hardware-grounded parameters.
- Coupler-channel availability and quality derive from the authoritative coupler state: engagement, alignment, degradation, and separation. Partial engagement is never a perfect connection.
- **Reachability always derives from physical state**, never from a manually maintained logical neighbor list. Contactless reachability comes from geometry, range, occlusion, and other applicable effects.
- The articulation benchmark may use any declared channel. The evaluator records each message's route and channel. **Through-chain propagation is a separate acceptance criterion**: the target must travel along the engaged coupler chain, and contactless shortcuts do not count toward it.
- Message paths, delays, losses, and outcomes are recorded for replay. No channel bypasses the Q22 or Q32 constraints.

### 3.4 Q34 — Power transfer

- Through-coupler power transfer is an **optional, declared** capability. It is available only across a mechanically engaged coupler with a functioning power path. It is not a universal shared bus, and mechanical engagement does not guarantee electrical continuity.
- **Limits apply per Kin as well as per assembly.** An acceptable aggregate never hides an individual Kin that exceeds its energy, power, or thermal limits.
- There is **no automatic balancing**. Transfers happen only through controller commands via the normal interface or through explicitly declared passive circuitry.
- The first Q31 benchmark requires an **energy-isolated baseline**. A power-sharing variant may be reported separately.
- Model contact or coupling resistance, voltage drop, current and power limits, conversion losses, heating, and fault protection where applicable, without exceeding the model's validated fidelity.
- Record every transfer's source, destination, path, amount, losses, and heat. Faults and depleted or disconnected Kins have explicit outcomes.

### 3.5 Q35 — Physics formulation

- Each Kin is a **separate rigid body**. Links are **implicitly solved compliant constraints** with declared compliance, damping, limits, and failure behavior. The formulation must handle changing topology and closed loops. This chooses a formulation, not a library, algorithm, or integrator.
- Compliance and load limits are modeled **per axis** (tension, compression, shear, bending, torsion) as the actual coupler supports. Fully rigid behavior is only an explicitly declared limiting case.
- **Loads used for acceptance come from the solver's own constraint and contact outputs**, with documented accuracy. This covers break and detach decisions, passive retention, stress views, and Q31 limits. Post-hoc estimates are allowed only for visualization or diagnostics.
- A **reference-validation suite** is required: a joint-coordinate reference for suitable open chains and analytic statics for known cases. Gaps are documented. References are never production paths.
- Solver stabilization must never be mistaken for physical damping or compliance. Contact, friction, and links are solved consistently.
- If numerical uncertainty overlaps a failure threshold or could change a pass/fail outcome, the result is **uncertain**, not a pass.
- The physics backend stays replaceable (Q15). Simulation time stays separate from rendering time (an earlier decision). Fidelity is never sacrificed to claim 10K-Kin scale. Large-scale throughput is a separate milestone with declared fidelity limits.

### 3.6 Q36 — Coupler engagement

- Docking and release use a **reduced continuous mechanism model**. Continuous latch variables (travel, preload, actuator state, wear as supported) are driven by bounded actuators and react to loads.
- Discrete states (approaching, aligning, latching, locked, releasing, jammed, failed) are **classifications derived from physical state**. They never create, strengthen, or remove a connection.
- Link stiffness, strength, retention, data quality, and power-path quality evolve with physical engagement. Nothing jumps to full strength because a label changed.
- The **capture window is measured**, by sweeping misalignment, relative velocity, approach direction, and other justified conditions. It is never declared. Its uncertainty is documented.
- The reduced model is **validated against detailed close-up full-mechanism models** for docking, partial engagement, jamming, loaded retention, and release. Detailed models are for validation and inspection only.
- **No docking assistance:** no snapping, teleporting, or unmodeled pose or velocity correction. Every change in pose or velocity comes from gravity, contact, friction, declared actuators, physically justified magnetic or guide forces, or link constraints at their current engagement.
- Do not assume magnetic pre-alignment unless the candidate includes it. Release is a physical process under load that may take time, fail, or be blocked.
- Record continuous mechanism state, classifications, loads, and transitions for replay and cutaway inspection.

### 3.7 Q37 — Physical scale

- **Q1's 30–60 mm reference size class and Q12's 60 mm stowed enclosing sphere govern.** This is a reference scale for current benchmarks, not proof that any design in that range is feasible. Deployed geometry, swept volumes, mass, inertia, actuator reach, and clearances are evaluated independently.
- Use SI units throughout, with no hidden size-dependent constants. Physical properties derive from the candidate model and its declared components.
- Document the validated operating range of each physics model, including when gravity, contact, friction, adhesion, electrostatics, and magnetic forces may be neglected. Do not assume ordinary rigid contact is adequate for every centimeter-scale design.
- The engine **flags** candidates and experiments outside the validated envelope. Such results are exploratory, not validated feasibility passes.

### 3.8 Q38 — Candidate selection

- Evaluate approximately **two to four structurally distinct, credible candidates**. Do not add weak candidates to fill a quota.
- **Gate 1 — Paper feasibility:** Q12 envelope, packaging and assembly access, evidence-backed components, preliminary mass and energy/power budgets, coupler layout, mechanical requirements, and originality.
- **Gate 2 — Reduced-model feasibility:** locomotion, docking, articulation, retention, and load transfer using production physics and established benchmark rules.
- **Gate 3 — Detailed validation:** Q35/Q36 reference models, sensitivity and uncertainty analysis, and correct classification of inconclusive results.
- **Selection:** gates are hard pass/fail. Weighted comparison happens only among survivors, in the priority order of §15. The scoring method is documented before scoring. Publish the evidence, trade-offs, disadvantages, and risks. Preserve rejected candidates and their failure reasons.
- Criteria are **pre-registered** before evaluation. Changes record the original and revised versions, the reason, the date, and the evaluations to repeat.
- **Originality review** happens at Gate 1, before substantial modeling, and again at final visuals. Record the references reviewed, the reasoning, and the changes made. The review reduces copying risk. It does not prove absolute originality.
- Benchmark acceptance is separate from ranking. Candidates get equivalent evidence requirements and conditions. Revisions are versioned and retested against the same criteria. No parameter optimization happens until the models and benchmarks are validated.

### 3.9 Q39 — Decision records and preregistration

- Record structure is in §0.1.
- Every evaluation result records the criteria version and content hash, candidate version, simulator configuration, run ID, and Git commit. Criteria changes must not silently reinterpret earlier results.
- A local Git commit aids traceability but is not independent proof of preregistration. Where stronger evidence is needed, publish or externally timestamp the criteria hash before the run.
- Git is initialized in this workspace. Do not commit, push, or rewrite history without explicit authorization.

### 3.10 Q40 — First implementation milestone

- A **thin vertical slice on the production 3D architecture**. Physics, sensing, communication, controllers, evaluator, deterministic stepping, SI units, replay, and criteria versioning are distinct from the first commit. Models may be minimal and provisional, but the architecture must not depend on shortcuts that contradict accepted decisions.
- **Neutral test fixtures** (for example, a generic rounded block and simple coupler stand-ins) are permitted before Gate 1. They are labeled as fixtures in source, data, logs, and the inspector. They are not Kin candidates, do not enter Q38, and cannot establish candidate feasibility.
- **Every slice result is exploratory by default** until its specific models pass validation for specific conditions and claims. Passing one analytic case does not validate the engine.
- There is no production 2D mode and no artificial planar constraint. A test case may use planar geometry where analytically appropriate, but the simulation remains fully 3D.
- The slice sequence is in §14. It **supersedes** the original "2D or simplified 3D prototype" task list (preserved in §14.2).

### 3.11 Q1–Q30 — known by reference only

The original text is unavailable. Later decisions reference only the following:

| ID | Known content (as referenced by later decisions) |
| --- | --- |
| Q1 | 30–60 mm reference size class |
| Q11 | Passive structural retention requirement for locked structural states |
| Q12 | Every Kin fits within a common 60 mm diameter enclosing sphere in its mechanically achievable stowed configuration |
| Q14 | Numerical validation; configuration-scoped exact deterministic replay |
| Q15 | Replaceable physics-backend boundary |
| Q21 | Passive, unpatterned, nonmagnetic, electrically insulating reference tabletop |
| Q22 | Finite onboard computation and memory |
| Q25 | Numerical validation and operating-envelope principles |
| Q30 | Documented, mechanically stable designated starting orientations for initial tabletop locomotion |

All other Q1–Q30 content is unknown here. Treat it as unrecorded, not as nonexistent.

---

## 4. Design principles

### 4.1 Originality

The Kins must be visually and mechanically original.

Allowed inspiration:

- swarm robotics
- modular robotics
- programmable matter
- claytronics
- lattice materials
- insect swarms
- cellular structures
- self-assembling materials

Forbidden direction:

- direct imitation of the "microbot" look from Big Hero 6
- dense black needle-like particles with near-identical proportions and silhouette
- any obvious one-to-one copy of a known fictional robot

Originality is reviewed formally at Q38 Gate 1 and again at final visuals.

### 4.2 Mechanical plausibility

Every connection method needs a clear rationale for:

- how Kins align
- how they latch
- how they transmit force
- how they detach
- how power and communication work during linkage

### 4.3 Local intelligence

Each Kin operates using only:

- local sensing
- short-range communication
- local structural knowledge
- limited internal state

No Kin may require omniscient knowledge of the swarm. This is enforced by the Q32 controller information boundary.

### 4.4 Explainability

The simulation must make it easy to inspect:

- a single Kin
- a chain of Kins
- a branching assembly
- a lattice / wall / bridge section
- damaged vs repaired state

Cutaway and cross-section views are first-class features, not afterthoughts.

---

## 5. Candidate design guidance (non-binding)

> **Status:** This section is input for generating Q38 candidates. It does **not** select the final geometry, coupler mechanism, articulation mechanism, or locomotion method. Those remain open until Q38 selection. Every candidate must satisfy §3, including the Q12 60 mm stowed envelope.

### 5.1 Suggested starting direction: "Link-Cell"

One suggested starting form is the **Link-Cell**:

- **rounded polyhedral body**
- approximately palm-seed / pebble-like, not spiky
- multiple connection faces distributed around the shell
- retractable couplers on each usable face
- internal flywheel / actuator / battery / controller layout visible in cutaway

Possible geometries include:

- a **rounded truncated-octahedron-inspired shell**
- a simplified **rounded hex-prism core with 6–8 coupler zones**

These offer high packing efficiency, multiple stable attachment orientations, good branching, believable load transfer, and clear cross-sections. Candidates must be structurally distinct (Q38), so they should not all be variants of this one form.

Pure spheres are weak for deterministic alignment, chain rotation control, torque transfer, and face-based connection semantics. Cubes pack well but look blocky, move poorly in swarms, and produce awkward rotational transitions.

### 5.2 Connection requirements

Each Kin should support:

- **end-to-end linking** for chain formation
- **side linking** for lattice / sheet formation
- **branching** for trees / trusses / reinforcement
- **deterministic alignment**, so assemblies do not wobble unrealistically
- **force transfer**, so linked Kins behave like connected mechanical units

### 5.3 Suggested connection topology

- **2 primary axial couplers** for chain growth and head-tail structural continuity
- **4 to 6 secondary lateral couplers** for bracing, branching, lattice formation, and reinforcement

This is preferable to dozens of tiny uniform couplers. It simplifies logic, makes the mechanics legible, helps cutaway visualization, and produces more realistic structural behavior.

### 5.4 Coupler concepts

Candidate coupler concepts include:

- retractable hooks
- magnetic latch pads with alignment pins
- twist-lock collars
- claw-and-ring connectors
- tongue-and-groove locking tabs

One clear pattern is **passive pre-alignment followed by a mechanical lock**:

1. Kins enter docking proximity.
2. Passive alignment features (magnetic or geometric guides) rotate them into place.
3. The mechanical latch engages.
4. The connection becomes rigid or semi-rigid.

Per Q36, pre-alignment forces must be physically justified by the candidate's actual mechanism. Magnetic attraction is not assumed. Each candidate also declares whether its couplers carry data (Q33) and power (Q34).

### 5.5 Shape rules

The body should:

- avoid long spikes or hair-like rods
- avoid a perfectly smooth sphere
- avoid very thin appendages
- keep the center of mass near the geometric center
- provide flat-ish or gently recessed coupling zones
- remain readable at both distance and close-up

The body should be compact, symmetric or near-symmetric, slightly rounded for motion, and faceted enough for repeatable docking.

### 5.6 Structural realism

Every link defines its connection point, connection normal, rotational alignment, and, per axis as the coupler supports (Q35): tensile, compressive, shear, bending, and torsional stiffness and limits, damping, and detach/failure behavior.

Assemblies must not behave like welded solids. Candidate connection modes include **loose**, **hinged**, **rigid**, **temporary magnetic**, and **locked structural**. Rigid is only an explicitly declared limiting case (Q35). Locked structural states must satisfy Q11 passive retention, evaluated under declared loads.

### 5.7 Motion realism

The shape must allow believable transitions: approach, orient, dock, lock, reinforce, detach, retreat, reattach elsewhere. Each unit must be able to rotate freely in space, expose connection faces, avoid collision during docking, and maintain clearance around couplers.

Do not place couplers where adjacent bodies would interpenetrate during docking.

### 5.8 Internal anatomy

Every candidate must support close-up cutaway views and conceptually include:

- outer shell
- internal frame
- control unit
- energy cell
- locomotion / attitude system
- short-range communication module(s)
- coupler actuation system
- sensor ring / proximity sensors

One suggested layout:

- **central core:** compute + battery
- **mid ring:** stabilization / flywheel / power distribution
- **outer shell:** sensors + coupler mounts
- **connection face modules:** latch actuator + pre-alignment system

All of it must fit within the Q12 stowed envelope with a datasheet-backed component list (Q38 Gate 1).

### 5.9 Locomotion

Locomotion options to evaluate per candidate:

1. micro-thruster / reaction-control style
2. electromagnetic hopping / impulse motion
3. surface traction with internal flywheel stabilization
4. other physically modeled mechanisms

Per Q31, Q32, and Q36, acceptance runs require locomotion produced by modeled, bounded actuators acting through contact and physics. Abstracted locomotion may appear only in runs labeled exploratory or fixture. For visuals, show internal reaction wheels / micro-actuators where the candidate actually has them.

---

## 6. Visual inspection goals

### 6.1 Required visualization modes

- **macro swarm view:** thousands of Kins in motion
- **close-up cluster view:** tens of Kins linking in real time
- **single-Kin exploded view:** shell, couplers, internal core
- **cutaway cross-section:** slice through the shell to reveal internals
- **assembly cutaway:** a chain, truss, or wall section from the inside
- **connection stress view:** color-coded link loads from solver outputs (Q35)
- **signal / communication view:** messages, routes, channels, consensus, gradient fields (Q33)
- **articulation inspection:** the Q31 inspector features
- **energy view:** per-Kin energy, power, thermal state, and transfers (Q34)

Every view shows the authoritative simulated state. Test fixtures, oracle runs, and exploratory results are visibly labeled (Q40).

### 6.2 Art direction for diagrams

Use a technical, clean, engineering-oriented, slightly futuristic style that reads at a glance.

Avoid superhero / movie mimicry, over-stylized fantasy robotics, and the "black swarm needle" aesthetic.

---

## 7. Simulation architecture

### 7.1 Layers

1. **Physics layer:** authoritative state. Rigid bodies, contact, friction, compliant link constraints (Q35), reduced coupler mechanisms (Q36), actuators, energy and thermal models (Q34). Backend replaceable (Q15).
2. **Sensing layer:** modeled sensors that turn authoritative state into noisy, quantized, delayed observations (Q32).
3. **Communication layer:** through-coupler and contactless channels with reachability derived from physical state, plus modeled latency, loss, and ordering (Q33).
4. **Agent / controller layer:** per-Kin controllers with finite compute and memory (Q22). They see only sensor observations, their own state, and received messages.
5. **Docking layer:** coupler control and the derived classification of engagement state (Q36).
6. **Assembly layer:** chains, lattices, surfaces, trusses, and repair formations, built from local behavior.
7. **Evaluator:** reads ground truth and versioned criteria, and produces hash-linked results (Q39). Never exposed to controllers.
8. **Rendering / inspection layer:** debug overlays, cutaways, close-ups, and state coloring, driven from recorded authoritative state, with rendering time separate from simulation time.

Cross-cutting requirements: SI units, deterministic simulation-time stepping, stable event ordering, seeded randomness, and replay (Q14, Q32).

### 7.2 Agent state labels

Behavioral states (examples): idle, scouting, approaching, aligning, docking, locked, bracing, relaying, repairing, detaching, failed.

Coupler engagement labels (approaching, aligning, latching, locked, releasing, jammed, failed) are **derived from continuous mechanism state** and never drive physics (Q36).

---

## 8. Behavioral roadmap

The first milestone is the Q40 slice sequence (§14). Deterministic replay, the evaluator boundary, and criteria versioning exist from slice 1, not from a later phase.

- **Phase 1:** physically modeled movement, neighbor detection from physical state, local messaging, visual debugging
- **Phase 2:** two-Kin docking, small chain formation, coupler engagement model, detach / reattach
- **Phase 3:** the Q31 tabletop articulation benchmark, branching chains, simple lattices, structural constraints, local repair
- **Phase 4:** shape goals, distributed assembly strategies, role assignment, reinforcement, the cantilever benchmark (Q31)
- **Phase 5:** full cutaway rendering, inspection tooling, stress view
- **Phase 6:** distributed execution, world partitioning, message latency / failure at scale, and scalability benchmarking with declared fidelity limits (Q35)

---

## 9. Data model guidance

Prefer SoA or hybrid SoA layouts once scale increases.

Each Kin minimally tracks:

- id, candidate / fixture identity and version
- position, orientation, velocity, angular velocity
- energy, power, thermal state
- behavioral state, role
- available couplers and their continuous mechanism state
- active links
- local message inbox, within memory limits

Neighbor sets are caches **derived from physical state** (Q33), never manually maintained.

Each link tracks:

- endpoint A / B, coupler A / B
- engagement state (continuous) and derived classification
- link mode
- per-axis compliance, damping, and limits
- solver-reported current loads and their accuracy (Q35)
- data-channel and power-path state (Q33, Q34)
- break / detach thresholds

---

## 10. Rendering goals

The renderer must support:

- instanced rendering where possible
- debug overlays
- selection + inspection
- cut plane rendering
- exploded / cutaway mode for single-Kin visualization
- visible labeling of fixtures, oracle runs, and exploratory results

Rendering 10K+ Kins is a goal. Simulating 10K+ Kins is a separate milestone with declared fidelity and validation limits (Q35). Do not sacrifice mechanical fidelity to claim scale.

Cutaway rendering does not need full CAD-level realism. A clean "technical illustration" feel is enough.

---

## 11. Naming conventions

- **Kin** = one unit of the swarm (informally: unit, cell, mote)
- **Coupler** = one connection interface
- **Link** = an active connection between two Kins
- **Assembly** = a connected structure
- **Lattice** = a regular multi-Kin structure
- **Chain** = linear connected sequence
- **Node** = graph node in the logical connectivity layer
- **Cluster** = spatially local group, whether linked or not
- **Test fixture** = a neutral, non-candidate body used to exercise infrastructure (Q40)
- **Candidate** = a Kin design under Q38 evaluation

Avoid the word "microbot" in any way that implies copyrighted identity.

---

## 12. Success criteria

The project is succeeding if:

- single Kins look mechanically plausible
- docking behavior is understandable, repeatable, and emerges from modeled physics
- chains form and articulate convincingly under the Q31 rules
- branching assemblies feel structurally intentional
- close-up views clearly explain internal anatomy
- cross-sections are visually compelling
- the system is obviously original
- every acceptance claim traces to pre-registered criteria, validated models, and replayable results
- the simulation architecture scales beyond a toy demo

---

## 13. Validation status vocabulary

Every result is labeled with exactly one of:

- **exploratory:** models not yet validated for this claim and these conditions (the default)
- **oracle / diagnostic:** used privileged ground truth. Never a pass
- **fixture:** produced with test fixtures. Says nothing about candidate feasibility
- **uncertain:** numerical or model uncertainty could change the outcome
- **validated acceptance:** satisfies pre-registered criteria using validated models within their operating envelope

---

## 14. First implementation milestone (Q40)

### 14.1 Slice sequence

All slices use the production 3D architecture and test fixtures. All results are exploratory until validated.

1. **Slice 1: neutral body and tabletop contact.** A generic fixture body rests on the reference tabletop in full 3D. Compare equilibrium and contact against analytic statics. Establish SI units, deterministic stepping, state recording, replay, and evaluator separation.
2. **Slice 2: compliant connection.** Two fixture bodies are joined by a fixture-only compliant constraint. Exercise solver-output loads, compliance, and reference validation against analytic statics and separate reference dynamics (Q35).
3. **Slice 3: reduced coupler engagement.** Two fixture bodies dock through a fixture-only reduced continuous mechanism. Exercise alignment, contact, latch travel, engagement-dependent constraint strength, and physical release under load, with no snapping or assist (Q36).

Benchmark step cost is measured from slice 1 onward, before any scaling work.

### 14.2 Superseded task list (historical, do not follow)

The original first-task list is superseded by Q40, primarily because its item 3 allowed a 2D prototype. It is preserved here for history:

1. Define the base bot schema in Zig.
2. Define the coupler schema and connection state machine.
3. Build a 2D or simplified 3D prototype with movement, neighbor detection, and two-bot docking.
4. Create a debug visualization for coupler normals, docking candidates, and link states.
5. Add small chain growth from 2 → 8 → 32 bots.
6. Add a close-up inspection mode.
7. Add a single-bot cutaway mock view, even if static at first.
8. Benchmark simulation step cost before scaling up.

Items 1, 2, 4, 6, 7, and 8 remain useful work, subject to §3. Item 2's "connection state machine" is now a derived classification over a continuous mechanism (Q36). Items 3 and 5 are replaced by the slice sequence and the roadmap.

---

## 15. Final instruction to coding agents

When making design decisions, optimize in this order:

1. **originality**
2. **mechanical plausibility**
3. **clarity of connection logic**
4. **scalable simulation architecture**
5. **visual quality**

If forced to choose between "looks cool" and "is structurally believable," choose structural believability. If forced to choose between "makes the demo work" and "honors an accepted decision," honor the decision, or propose a superseding decision record.

The finished project should feel like:

- an original swarm robotics / programmable matter engine
- a research-grade systems simulation
- an inspectable mechanical ecosystem

—not a copy of a movie prop.
