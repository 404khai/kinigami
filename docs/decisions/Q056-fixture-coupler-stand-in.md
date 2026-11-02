# Q56 — Fixture coupler stand-in: geometry, reduced latch model, and parameters

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-02 |
| Supersedes | — (decides CPL-011 **for the fixture stand-in only**; CPL-011 stays unresolved for Kin couplers) |
| Provenance | **agent decision under explicit owner delegation** ("I trust its judgement"; every decision of the reduced coupler engagement phase delegated). The owner may revise it through a superseding record |

## Context

The roadmap gate for the reduced coupler engagement fixture asks for "fixture coupler stand-in geometry and physical parameters (CPL-011, fixture scope)". Q40 permits neutral coupler stand-ins before Gate 1. They are labeled fixtures, are not Kin candidates, and never enter Q38. Q36 fixes the model class: a reduced continuous mechanism with derived discrete states, no assistance, and release under load as a physical process. Q54 moved three items here: link load limits and failure, link release and topology change (PHY-003), and stiff-link dynamics once a coupler stiffness is declared.

The solver today has contact only between cuboids and the tabletop. It has no body-body contact.

## Decision

### 1. What the stand-in is

`fixture_coupler_probe_socket`: a **ball probe in a square-pyramid socket, held by an engagement-scaled compliant link whose engagement is the travel of a single actuated pawl coordinate**. Ball-in-socket kinematic seats and actuated detents are generic machine elements. Nothing here is derived from, or proposed as, a Kin coupler. It exists to qualify solver capabilities:

- body-body guide contact
- continuous latch state
- engagement-dependent stiffness and strength
- load limits and separation
- release under load
- capture sweeps

The fixture says nothing about the geometry, mechanism, or feasibility of any candidate (Q38, Q40).

### 2. Bodies

Both bodies are `fixture_link_cube`: a 20 mm uniform cube of 0.020 kg (Q52). The probe, stem, socket, and pawl are **massless geometric features** of the bodies. Their mass and inertia are not modeled, which is declared rather than hidden. A cube's inertia is isotropic, so the gyroscopic term the solver omits is exactly zero for these bodies. That is why the cube is kept.

### 3. Geometry (coupler frame on body A)

The coupler axis `a` is a unit vector in A's frame, normal to one of A's faces, pointing out of A. Axial coordinate x is measured along `a` from that face plane.

| Feature | Body | Definition |
| --- | --- | --- |
| Socket | A | Square-pyramid recess. Apex on the axis at x = −D, D = **4 mm**. Mouth is a square of half-width w = **4 mm** at x = 0, its edges aligned with A's two body axes perpendicular to `a`. Facet half-angle α = atan(w/D) = **45°** |
| Face | A | The rest of A's face around the mouth (half-size 10 mm), a contact surface |
| Rim | A | The four convex mouth edges and four mouth corners, as contact features |
| Probe | B | Sphere of radius ρ = **2 mm**. Its centre sits on B's face normal −`a` (facing A), at stem length s = **4 mm** outside B's face. The stem is massless and non-colliding |
| Seat point | A | Where the ball touches all four facets: x_seat = ρ/sin α − D = 2√2 − 4 mm ≈ **−1.1716 mm** |

Rationale: the socket fits a 20 mm face with a 6 mm margin and stays shallower than half the cube. With α = 45°, the wedge condition for sliding into the seat is μ < cot α = 1, which every preregistered friction pair satisfies (Q48), so alignment is possible by geometry alone. At the seat the faces are 2.83 mm apart, which leaves room for angular misalignment before the cube bodies could touch. Cube-cube contact is **not modeled**. Runs where it would occur are flagged `outside_model` and never counted (Q57).

### 4. Guide contact

The ball contacts A's socket facets, face, rim edges, and rim corners. Each is a sphere-to-feature contact that is active only in that feature's Voronoi region, so a single geometric contact is never counted twice. The normal law and the Coulomb friction law are the tabletop's (Q47, analytic protocol): k = 1e5 N/m and c = 50 N·s/m per contact, slip speed 1e-5 m/s. They are solved in the **same Gauss–Seidel pass** as the tabletop contacts and the links (PHY-007). The guide friction pair is a run parameter: frictionless for the statics references, and Q48's `mu_low` and `mu_mid` for the capture sweeps.

### 5. Latch link and engagement

- The latch link is the Q52 6-DOF link. Anchor B is the ball centre. Anchor A is the seat point moved **δ_pre = 0.05 mm** deeper along −`a`. The rest length L₀ is 0 and the rest relative orientation is identity, so a seated, engaged ball is preloaded into the socket.
- **Engagement** is e = u/u_full ∈ [0, 1], where u is the pawl travel. Every row scales linearly with e: k_i(e) = e·k_i,full, c_i(e) = e·c_i,full, and limit_i(e) = e·limit_i,full. The link exists (has rows) only while u > 0 and it has not separated. It therefore appears with zero stiffness and grows continuously. It never appears at full strength (CPL-003).
- **Full stiffness:** k_axial = k_shear = **1e4 N/m**, k_torsion = k_bend = **1 N·m/rad**. This is Q52's `stiff` grid point, whose statics are already qualified (run 2).
- **Full damping:** ζ = **0.2** on the free two-cube system: c = 2ζ√(k·m/2) for translation and 2ζ√(k·I/2) for rotation.
- **Full limits:** tension **2.0 N**, shear **1.0 N** (magnitude), bending **0.01 N·m** (magnitude), torsion **0.005 N·m** (magnitude). Compression has no link limit, because the seat contacts carry it.
- **Combined loading:** each axis is checked independently. Interaction between axes is not modeled.

### 6. Pawl (latch variable) dynamics

The pawl is massless and first order. It is updated **after** each physics step from that step's solver-native link report, so the order is explicit and deterministic:

- Command `s` ∈ {engage, hold, release}, supplied per step by the run harness. Without a command it holds.
- **Cam-out force** from the link potential V = ½·Σ e·k_i,full·C_i²: Q = −∂V/∂u = −½·Σ k_i,full·C_i²/u_full, which is always ≤ 0. C_i are the six reported extension and rotation components.
- **Pawl friction:** μ_p·N, with N = max(0, reported tension).
- **Engage:** u increases by v_max·Δt (clamped to u_full) if F_act − |Q| > μ_p·N **and**, when u = 0, the ball centre is inside the capture zone. Otherwise the pawl stalls.
- **Release:** u decreases by v_max·Δt (clamped to 0) if F_act + |Q| > μ_p·N. Otherwise the release is **blocked** (CPL-008).
- **Hold, or unpowered:** no motion. The drive is declared self-locking, so passive retention holds by construction (CPL-009).
- The change ½·Δe·Σ k_i,full·C_i² in stored link energy at each update is the work done by the pawl. It is reported, so the energy audit can account for it.

| Parameter | Value |
| --- | --- |
| Travel u_full | **1.0 mm** |
| Speed limit v_max | **10 mm/s** (full stroke in 0.1 s) |
| Actuator force limit F_act | **0.3 N** |
| Pawl friction μ_p | **0.3** |
| Capture zone, ball centre relative to the seat point | radial ≤ **0.2 mm**, axial within ±**0.2 mm** |

With these values, engagement from a seated ball succeeds: the largest μ_p·N + |Q| is about 0.155 N, below F_act. Release becomes blocked above a tension of T_block = k·u·μ_p − √((k·u·μ_p)² − 2·k·u·F_act) ≈ **1.268 N** at e = 1, which is below the tension limit. The preload is P = δ_pre·k·k_s/(k + k_s) ≈ **0.476 N** with seat stiffness k_s = 4·k_contact·sin²α = 2e5 N/m. This is above the fixture weight (0.196 N), so a hanging body stays seated.

### 7. Separation and topology change (PHY-003)

- If, after a step, any axis's solver-native load exceeds its engagement-scaled limit, the link is removed before the next step. The decision uses solver loads only (Q35 §2).
- Separation is classified `released_under_load` when the release command was active and `separated_overload` otherwise.
- The fixture has **no damage model**. After separation the pawl keeps its travel. The link can form again only after the pawl returns to u = 0 and re-engages through the capture zone. Damage, wear, and jamming physics are not invented (CPL-010).
- When u reaches 0 during release, the link is removed at zero stiffness. That is a clean release, with no force discontinuity.

### 8. Discrete states (CPL-001)

`approaching`, `aligning`, `latching`, `locked`, `releasing`, `separated`, and `latch_blocked` are **classifications computed by the evaluator** from continuous state: guide contacts present, link active, e, command, and pawl stalled. The solver never reads them.

## Alternatives considered

- **Snap or threshold engagement** (Q36 option A): forbidden.
- **A round cone socket:** at the centred seat the contact is a full circle, and a single-point contact has no defined normal there. Four planar facets make the seat well-posed.
- **Pawl as a contacting rigid body** (a detailed mechanism): that is the Gate 3 reference model of Q36 §3, not the reduced production model.
- **Stiffness gated by position:** a gate on stiffness makes the force field non-conservative. Here the geometric gate acts only on the pawl's advance, never on the force law.
- **Engagement-independent stiffness with only strength scaling:** violates CPL-003, because stiffness would jump when the link forms.

## Constraints and consequences

- Every value above is a **provisional fixture parameter** chosen for solver qualification. None is the strength, stiffness, or friction of any material or mechanism.
- Not modeled: data and power coupling (Q33, Q34; there is none in the fixture), pawl inertia, stem collision, cube-cube contact, combined-load interaction, and damage.
- The criteria governing this stand-in are preregistered in Q57 before any coupler solver code.

## Revision notes

—
