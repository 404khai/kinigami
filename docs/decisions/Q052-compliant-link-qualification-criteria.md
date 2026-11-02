# Q52 — Compliant-link qualification criteria (preregistration before link code)

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-02 |
| Supersedes | — (fills PHY-012 and PHY-013 for the compliant-link capability) |
| Provenance | **agent decision under explicit owner delegation** ("make the decisions"). The owner may revise it through a superseding record |

## Context

Q41 requires a backend qualification checklist preregistered before compliant-link code. The draft (`docs/qualification/backend-checklist.md`) left the acceptance values open. All values below are **solver-qualification parameters on neutral fixtures**, not coupler or Kin-candidate claims (Q40).

## Decision

### 1. Fixture link mechanics (what is being qualified)

- A **fixture link** is a 6-DOF generalized spring-damper between two **anchor frames**: anchor A on body A and anchor B on body B. Each anchor frame is the body frame translated to the anchor point.
- The link axis `a` is a declared unit vector in body A's frame.
- Let **d** be the position of anchor B relative to anchor A (world frame) minus the rest offset L₀·a. Let **θ** be the rotation vector of body B's orientation relative to body A's, measured from the rest relative orientation. Both are resolved in anchor A's frame.
- The link resists:
  - the component of **d** along `a` with **k_axial** and **c_axial**
  - the components of **d** perpendicular to `a` with **k_shear** and **c_shear** (isotropic)
  - the component of **θ** along `a` with **k_torsion** and **c_torsion**
  - the components of **θ** perpendicular to `a` with **k_bend** and **c_bend** (isotropic)
- Link force and moment act equal and opposite at the two anchors.
- It is solved as an **implicitly integrated compliant constraint** in the same solver pass as contact (Q35, PHY-007).
- Solver-reported link force and moment are solver outputs (PHY-005).
- A **static body** (infinite mass, never moves) may serve as body A. It acts as a world anchor and is permitted only in `fixture_validation` runs.

### 2. Fixtures

| ID | Shape | Mass | Notes |
| --- | --- | --- | --- |
| `fixture_link_cube` | 20 mm uniform cube | 0.020 kg | Used for both bodies |

- Rest length L₀ = 10 mm between anchors at facing face centres.
- Vertical cases hang body B below static body A. Free cases use two dynamic cubes.

### 3. Stiffness grid (every case runs at every grid point × every timestep)

| Grid point | k_axial = k_shear (N/m) | k_torsion = k_bend (N·m/rad) |
| --- | --- | --- |
| `soft` | 1e2 | 1e-2 |
| `mid` | 1e3 | 1e-1 |
| `stiff` | 1e4 | 1 |

Timesteps: 0.5, 1, and 2 ms (as in Q48).

### 4. Resolution rule (Q43, PHY-018)

- **Dynamic** checks (L4–L7) are evaluated only where ω·Δt ≤ 0.2 (at least about 31 steps per period).
- Combinations beyond that are reported `outside_envelope`. They are neither pass nor fail, and they are excluded from the outcome rule.
- **Static** checks run at every combination.

### 5. Acceptance values

| Check | Case | Acceptance |
| --- | --- | --- |
| L1 axial statics | B hangs from static A, link critically damped (ζ = 1 on body B), settled | Link tension vs m·g: relative error ≤ 1e-3. Elongation vs m·g/k_axial: relative error ≤ 1e-2 |
| L2 shear and bending statics | L1 plus a horizontal validation load F = 0.1·m·g at B's centre of mass | Link shear force vs F ≤ 1e-3 relative. Link bending moment vs F·(cube half-size) ≤ 1e-3 relative. Shear displacement vs F/k_shear and bending angle vs moment/k_bend ≤ 2e-2 relative |
| L3 torsion statics | L1 plus a validation torque τ = 1e-4 N·m about the link axis | Link torque vs τ ≤ 1e-3 relative. Twist vs τ/k_torsion ≤ 1e-2 relative |
| L4 axial dynamics | Two free cubes in free fall, 0.5 mm initial stretch, c = 0 | Mean period vs 2π/√(k/μ) ≤ 1e-2 relative (resolved combinations only) |
| L5 torsional dynamics | Two free cubes, 0.05 rad initial twist, c = 0 | Mean period vs 2π/√(k_t/I_red) ≤ 1e-2 relative (resolved) |
| L6 physical damping | L4 with declared ζ = 0.05 | Measured ζ vs 0.05 ≤ 25 % relative (resolved) |
| **L7 numerical dissipation** | L4 with **c = 0** | Equivalent numerical damping ratio ζ_num ≤ **0.01**, which is one fifth of L6's physical ζ, so numerics can't masquerade as physics (PHY-006). Reported at every resolved combination |
| L8 momentum | L4 | \|p(t) − (p₀ + M·g·t)\| ≤ 1e-9·M·g·t + 1e-12 kg·m/s |
| L9 contact–link consistency | B resting on the tabletop, a vertical link to static A above pre-tensioned to 0.5·m·g, settled | Σ normal contact force + link tension vs m·g ≤ 1e-3 relative. Both are positive |
| L10 determinism | Every case | Replay reproduces final-state hashes bit-identically |

Measurement definitions (zero-crossing periods, peak-ratio damping, settling windows) are fixed in the criteria file and protocol before code.

### 6. Outcome rule

As Q48: each case passes only if every *evaluated* combination passes, fails if all fail, and is otherwise `uncertain`. `outside_envelope` combinations are listed but not counted. Results are labeled `fixture` and qualify only the declared envelope.

## Rationale

- Statics tolerances reuse Q48's principles.
- Deflection tolerances are looser because they include small-angle nonlinearity.
- The ζ_num bound ties numerical dissipation to physically meaningful damping. A backward-Euler-style link would dissipate about ζ ≈ ω·Δt/2 (≈ 0.1 at the resolution limit) and **would fail**, which is intended: PHY-006 forbids presenting that as physics.

## Consequences

- `criteria/qualification/compliant-link-v1.json` is registered and hashed **before** any link code.
- A failure or `uncertain` result is reported as such. Revising values requires a superseding decision and a new criteria version.
