# Design guidance

> **Status: non-binding.** This guidance comes from the original project charter (commit `a89d304`) and its Q31–Q40 revision (commit `f003d70`). It informs **candidate generation** under Q38. It does not select the Kin geometry, coupler mechanism, articulation mechanism, or locomotion method. Where it conflicts with the [decision log](decisions/README.md) or the [requirements](requirements/requirements.md), those govern.
>
> Section numbers below are retained from the revision this text was moved from.

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

Every view shows the authoritative simulated state. Test fixtures, oracle runs, and exploratory results are visibly labeled (Q40, Q45).

### 6.2 Art direction for diagrams

Use a technical, clean, engineering-oriented, slightly futuristic style that reads at a glance.

Avoid superhero / movie mimicry, over-stylized fantasy robotics, and the "black swarm needle" aesthetic.
