# Backend qualification checklist (draft, not yet registered)

Implements Q41's requirement that a qualification checklist be **preregistered before any compliant-link code** (PHY-012). The checklist applies to every production backend equally, the custom Zig solver or any alternative (PHY-011). Capabilities qualify one at a time (PHY-015).

> **Status: draft.** The quantitative acceptance values (PHY-013) are pending an owner decision. Once decided, the machine-readable criteria file is committed and hashed in `criteria/REGISTER.md` before compliant-link implementation starts.

## Scope of this registration: compliant links between two fixture bodies (slice 2)

A **fixture link** joins two neutral fixture bodies at declared anchor points with **per-axis compliance** (Q35): axial (tension/compression), two shear axes, two bending axes, and torsion. Each axis has a declared stiffness and damping. Rigid behavior is only a declared limit (PHY-004). The link is fixture-only: it is not a Kin coupler, and it says nothing about coupler design (Q40).

## Capabilities and required evidence

| # | Capability | Reference case (closed form) | Measured quantity | Acceptance value |
| --- | --- | --- | --- | --- |
| L1 | Static axial load | Body A anchored to the world, body B hanging from the link in gravity | Solver-reported link axial force vs m·g; elongation vs m·g/k_axial | pending |
| L2 | Static shear and bending | Same anchor, with a declared horizontal validation load on B | Solver shear force and bending moment vs statics; deflection vs F/k | pending |
| L3 | Static torsion | Declared validation torque about the link axis | Solver torque vs applied torque; twist vs τ/k_torsion | pending |
| L4 | Axial dynamics | Free two-body oscillator (no contact, in free fall) | Oscillation frequency vs √(k/μ), where μ is the reduced mass | pending |
| L5 | Torsional dynamics | Free two-body torsional oscillator | Frequency vs √(k_t/I_reduced) | pending |
| L6 | Physical damping | L4 with declared damping c | Logarithmic decrement vs the analytic damped oscillator | pending |
| L7 | Numerical dissipation (PHY-006) | L4 with **c = 0** | Amplitude or energy loss per period caused by the integrator alone, reported per timestep | pending |
| L8 | Momentum | Free two-body motion with no external load except gravity | Total linear momentum drift relative to m·g·t | pending |
| L9 | Load consistency (PHY-007) | L2 resting on the tabletop instead of a world anchor | Link force consistent with contact forces under static equilibrium | pending |
| L10 | Determinism | Every case above | Replay reproduces final-state hashes exactly | exact (bit-identical) |

**Every case runs on the Q48 timestep grid** (0.5, 1, and 2 ms) and on a declared stiffness grid. It is evaluated under the Q48 outcome rule: all combinations pass → pass, all fail → fail, any mix → uncertain. Uncertainty overlapping a limit means `uncertain` (PHY-008).

## Not covered by this registration (qualified later, separately)

- Link creation, release, failure, and changing topology (PHY-003). These come with the reduced coupler mechanism (slice 3).
- Closed kinematic loops (lattice work).
- Chains of three or more bodies. These need a joint-coordinate reference (PHY-009, see below).

## Independent reference (Q41, PHY-009)

Two bodies joined by one compliant link have exact closed-form solutions for every case above, so **slice 2 needs no external engine**. The joint-coordinate reference for open chains becomes necessary when chains of three or more bodies are qualified (R12). The reference engine review for that stage is in `reference-engine-review.md`.
