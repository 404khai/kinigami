# Q76 — Body-body (box-box) contact slice: scope, formulation and validation cases

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-19 |
| Supersedes | — (implements Q74 §3.2; closes the R8 limitation "no cube-cube contact model" once qualified; changes no existing criterion) |
| Provenance | **agent decision under explicit owner delegation** ("start body-to-body contact") |

## Context

`rigid.zig` resolves contact only against the reference tabletop and coupler guide features ("General body-body contact does not exist"). In coupler run 2, 256 of 648 C8 sweep runs are `outside_model` because the two cubes would overlap. Every Kin candidate needs unit-to-unit contact.

## Decision

1. **Scope.** Compliant contact between two convex **cuboids**, each dynamic or static. General convex shapes are out of scope.
2. **Formulation.** It uses the same law and solver as the tabletop (Q35, Q47):
   - compliant normal row with the protocol contact stiffness and damping;
   - Coulomb static and kinetic friction;
   - projected Gauss–Seidel in a fixed order, with warm start;
   - impulses applied equal and opposite to both bodies.

   Contact generation:
   - a SAT test over the 15 axes of an OBB pair, which picks the minimum-penetration axis (ties broken by fixed axis order);
   - a manifold of vertex-in-other-box points for face axes, or the closest points of the two edges for edge axes;
   - ordering by (body pair, feature id), so runs are deterministic.

   Separation of more than 0 creates no row.
3. **Preregistration.** These come before any solver code:
   - `criteria/fixture-validation/body-contact-v1.json`, hashed in `criteria/REGISTER.md`;
   - `docs/validation/body-contact-v1-protocol.md`.
4. **Validation cases** (label `fixture`; analytic-v1 fixtures, friction grid and timesteps 500/1000/2000 µs):

   | Case | What it checks |
   | --- | --- |
   | BB1 stacked rest | flat block on flat block on the table; inter-block normal force = m_top·g; drift; penetration |
   | BB2 friction threshold on a block | the bottom block is static; a horizontal force on the top block at 0.9× and 1.1× of μs·m·g holds or slides |
   | BB3 slide to stop on a block | stop distance v²/(2 μk g) |
   | BB4 drop onto a block | the top block falls 0.1 m onto a static block and settles to the BB1 rest state; no penetration beyond the limit |
   | BB5 tipping on a block | tall block on a static flat block; a push below or above the analytic tipping threshold |
   | BB6 contact geometry | static generator checks against closed form: face-face, edge-face and crossing edge-edge (contact points, normal, depth) |
   | BB7 frame invariance | BB1 and BB3 scenes rigidly rotated and translated give the same body-relative results |
   | BB8 two dynamic bodies | gravity-free collision of two dynamic blocks: linear and angular momentum conserved; no energy creation beyond the analytic-v1 allowance |
   | BB9 replay | bit-identical final-state hashes |

5. **Tolerances.**
   - Where a case is the block-on-block analogue of an analytic-v1 case (rest, friction threshold, slide to stop, tipping), its tolerances are **copied** from analytic-v1. Evidence: same law and same fixtures.
   - BB6 geometry uses 1e-9 relative, and BB7 invariance uses 1e-9 relative (double-precision margin, provisional).
   - BB8 momentum uses the coupler audits' allowance form (Q57/Q60).
   - Every non-copied value is marked provisional in the criteria file.
6. **What it does not do.**
   - It does not change the coupler criteria or the C8 verdict.
   - Re-evaluating C8 with body-body contact needs its own decision and a new coupler criteria version.
   - It qualifies box-box contact only, and only within the declared envelope.
