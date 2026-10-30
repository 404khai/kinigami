# AGENTS.md

## Project

**Codename:** Kinigami [Kinetic Origami], A distributed programmable matter engine built in Zig.
**Type:** Distributed swarm-agent simulation in Zig  
**Goal:** Build an original programmable-matter / swarm-microbot simulation inspired by the _idea_ of self-organizing robotic matter, but **not copying** the microbot design, silhouette, or mechanical language from any existing film or franchise.

---

## 1. Core mission

This project simulates a large population of autonomous microbots that:

- move independently
- communicate locally
- interlink into chains, lattices, and load-bearing structures
- detach and reconfigure dynamically
- self-repair damaged structures
- support close-up mechanical visualization
- support cutaway and cross-sectional inspection of single bots and assemblies

The simulation must emphasize:

1. **local rules producing global behavior**
2. **physically plausible interlinking**
3. **clear visual explanation of how a bot works internally**
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

## 3. Design principles

### 3.1 Originality

The bots must be visually and mechanically original.

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

- direct imitation of the “microbot” look from Big Hero 6
- dense black needle-like particles with near-identical proportions and silhouette
- any obvious one-to-one copy of a known fictional robot

### 3.2 Mechanical plausibility

Every connection method should have a clear rationale:

- how bots align
- how they latch
- how they transmit force
- how they detach
- how power / communication works during linkage

### 3.3 Local intelligence

Each bot should operate using only:

- local sensing
- short-range communication
- local structural knowledge
- limited internal state

No bot should require omniscient knowledge of the entire swarm.

### 3.4 Explainability

The simulation should make it easy to inspect:

- a single bot
- a chain of bots
- a branching assembly
- a lattice / wall / bridge section
- damaged vs repaired state

Cutaway and cross-section views are first-class features, not afterthoughts.

---

## 4. Recommended bot concept

## 4.1 Chosen direction

Use an **original “Link-Cell” microbot** design.

Suggested form:

- **rounded polyhedral body**
- approximately palm-seed / pebble-like, not spiky
- multiple connection faces distributed around the shell
- retractable couplers on each usable face
- internal flywheel / actuator / battery / controller layout visible in cutaway

### Preferred geometry

Primary recommendation:

- **rounded truncated-octahedron-inspired shell**
- or simplified **rounded hex-prism core with 6–8 coupler zones**

This gives:

- high packing efficiency
- multiple stable attachment orientations
- good branching capability
- believable load transfer
- easier chain and lattice construction
- clear mechanical cross-sections

### Why not a sphere?

Pure spheres are weak for:

- deterministic alignment
- stable chain rotation control
- torque transfer
- face-based connection semantics

### Why not a cube?

Cubes pack well but:

- look too blocky
- move poorly in swarms
- produce awkward rotational transitions
- feel less like micro-scale adaptive matter

---

## 5. Shape constraints for optimal and realistic chain-linking

This section is critical. All bot design work must follow these constraints.

## 5.1 Connection requirements

Each bot must support:

- **end-to-end linking** for chain formation
- **side linking** for lattice / sheet formation
- **branching** for trees / trusses / reinforcement
- **deterministic alignment** so assemblies do not wobble unrealistically
- **force transfer** so linked bots behave like connected mechanical units

## 5.2 Recommended connection topology

Each bot should expose:

- **2 primary axial couplers**
  - used for chain growth / directional linking
  - ideal for “head-tail” structural continuity

- **4 to 6 secondary lateral couplers**
  - used for bracing, branching, lattice formation, and reinforcement

This is superior to having dozens of tiny uniform couplers because:

- it simplifies simulation logic
- makes the mechanics more legible
- helps with cutaway visualization
- produces more realistic structural behavior

## 5.3 Coupler design constraints

Couplers should be modeled conceptually as one of:

- retractable hooks
- magnetic latch pads with alignment pins
- twist-lock collars
- claw-and-ring connectors
- tongue-and-groove locking tabs

Best option for clarity:
**magnetic pre-alignment + mechanical lock**

1. bots enter docking proximity
2. passive alignment features rotate them into place
3. mechanical latch engages
4. connection becomes rigid or semi-rigid

This gives a believable combination of:

- easy docking
- positional correction
- secure structure

## 5.4 Shape rules

The bot body should:

- avoid long spikes or hair-like rods
- avoid a perfectly smooth sphere
- avoid very thin appendages
- keep center of mass near the geometric center
- provide flat-ish or gently recessed coupling zones
- support visual readability at both distance and close-up

The body should be:

- compact
- symmetric or near-symmetric
- slightly rounded for motion
- faceted enough for repeatable docking

## 5.5 Structural realism

A valid link should define:

- connection point
- connection normal
- rotational alignment
- max tensile force
- max compressive force
- shear tolerance
- torsional tolerance
- detach threshold

Assemblies should not behave like welded solids unless explicitly modeled as rigid.

Connection modes:

- **loose** (flexible)
- **hinged**
- **rigid**
- **temporary magnetic**
- **locked structural**

## 5.6 Motion realism

The bot shape must allow believable motion between link states:

- approach
- orient
- dock
- lock
- reinforce
- detach
- retreat
- reattach elsewhere

This means each unit must be able to:

- rotate freely in space
- expose connection faces
- avoid collision during docking
- maintain clearance around couplers

So do not place couplers where adjacent bot bodies would interpenetrate during docking.

---

## 6. Internal bot anatomy requirements

Every bot concept must support close-up cutaway views.

Each bot should conceptually include:

- outer shell
- internal frame
- control unit
- energy cell
- locomotion / attitude system
- short-range communication module
- coupler actuation system
- sensor ring / proximity sensors

### Suggested internal layout

- **central core:** compute + battery
- **mid ring:** stabilization / flywheel / power distribution
- **outer shell:** sensors + coupler mounts
- **connection face modules:** latch actuator + magnetic pre-align system

### Locomotion options

Choose one main locomotion model for the simulation abstraction:

1. **micro-thruster / reaction-control style**
   - visually cool
   - good for free-space movement
   - less realistic for tiny physical robots

2. **electromagnetic hopping / impulse motion**
   - interesting and stylized
   - harder to explain simply

3. **surface traction / internal flywheel stabilization**
   - more grounded
   - good for near-contact motion

4. **abstracted swarm locomotion**
   - acceptable for early simulation
   - must later evolve into a clearer physical model

Recommended for v1:
**abstracted free movement + explicit docking physics**
Recommended for visuals:
show internal reaction wheels / micro-actuators for orientation control.

---

## 7. Visual inspection goals

The engine must support views beyond the default scene.

## 7.1 Required visualization modes

Implement or plan for:

- **macro swarm view**
  - thousands of bots in motion

- **close-up cluster view**
  - tens of bots linking in real time

- **single-bot exploded view**
  - shell, couplers, internal core

- **cutaway cross-section**
  - slice through the shell to reveal internals

- **assembly cutaway**
  - show a chain, truss, or wall section from the inside

- **connection stress view**
  - color-code stressed links

- **signal / communication view**
  - show local messages, consensus, or gradient fields

## 7.2 Art direction for diagrams

Use:

- technical
- clean
- engineering-oriented
- slightly futuristic
- readable at a glance

Avoid:

- superhero / movie mimicry
- over-stylized fantasy robotics
- “black swarm needle” aesthetic too close to existing media

---

## 8. Simulation architecture

## 8.1 Simulation layers

The simulation should be decomposed into:

1. **Agent layer**
   - bot identity
   - local state
   - role
   - neighbor awareness

2. **Communication layer**
   - local broadcasts
   - direct peer messages
   - gradient / beacon propagation

3. **Docking layer**
   - detection
   - alignment
   - latch negotiation
   - connection state machine

4. **Physics layer**
   - movement
   - collision
   - attachment constraints
   - structural forces

5. **Assembly layer**
   - chains
   - lattices
   - surfaces
   - trusses
   - repair formations

6. **Rendering / inspection layer**
   - debug overlays
   - cutaways
   - closeups
   - state coloring

## 8.2 Agent state suggestions

Example states:

- idle
- scouting
- approaching
- aligning
- docking
- locked
- bracing
- relaying
- repairing
- detaching
- failed

---

## 9. Behavioral priorities

Start with the simplest believable behaviors.

## Phase 1

- free movement
- neighbor detection
- local messaging
- visual debugging

## Phase 2

- docking between two bots
- small chain formation
- connection state machine
- detach / reattach

## Phase 3

- branching chains
- simple lattices
- structural constraints
- local repair

## Phase 4

- shape goals
- distributed assembly strategies
- role assignment
- reinforcement

## Phase 5

- cutaway rendering
- inspection tooling
- stress view
- deterministic replay

## Phase 6

- distributed execution
- world partitioning
- message latency / failure
- scalability benchmarking

---

## 10. Data model guidance

Prefer SoA or hybrid SoA layouts once scale increases.

Each bot should minimally track:

- id
- position
- orientation
- velocity
- energy
- state
- role
- neighbor list
- available couplers
- active links
- local message inbox

Each link should track:

- endpoint A
- endpoint B
- coupler A
- coupler B
- link mode
- stiffness
- break threshold
- current stress / load

---

## 11. Rendering goals

The renderer must support:

- 10K+ agents comfortably in early versions
- instanced rendering where possible
- debug overlays
- selection + inspection
- cut plane rendering
- exploded / cutaway mode for single bot visualization

Cutaway rendering does not need full CAD-level realism.
A clean “technical illustration” feel is enough.

---

## 12. Naming conventions

Use clear terminology:

- **Bot** = one micro-unit
- **Coupler** = one connection interface
- **Link** = an active connection between two bots
- **Assembly** = a connected structure
- **Lattice** = a regular multi-bot structure
- **Chain** = linear connected sequence
- **Node** = graph node in the logical connectivity layer
- **Cluster** = spatially local group, whether linked or not

Avoid using the word “microbot” in a way that implies copyrighted identity. Prefer:

- bot
- mote
- link-cell
- unit
- cell

---

## 13. Success criteria

The project is succeeding if:

- single bots look mechanically plausible
- docking behavior is understandable and repeatable
- chains form convincingly
- branching assemblies feel structurally intentional
- closeup views clearly explain internal anatomy
- cross-sections are visually compelling
- the system is obviously original
- the simulation architecture scales beyond a toy demo

---

## 14. First concrete implementation tasks

1. Define the base bot schema in Zig.
2. Define the coupler schema and connection state machine.
3. Build a 2D or simplified 3D prototype with:
   - movement
   - neighbor detection
   - two-bot docking
4. Create a debug visualization for:
   - coupler normals
   - docking candidates
   - link states
5. Add small chain growth from 2 -> 8 -> 32 bots.
6. Add a close-up inspection mode.
7. Add a single-bot cutaway mock view, even if static at first.
8. Benchmark simulation step cost before scaling up.

---

## 15. Final instruction to coding agents

When making design decisions, optimize for the following order:

1. **originality**
2. **mechanical plausibility**
3. **clarity of connection logic**
4. **scalable simulation architecture**
5. **visual quality**

If forced to choose between “looks cool” and “is structurally believable,” choose structural believability.

The finished project should feel like:

- an original swarm robotics / programmable matter engine
- a research-grade systems simulation
- an inspectable mechanical ecosystem

—not a copy of a movie prop.
