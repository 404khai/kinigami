# AGENTS.md

**Kinigami** (Kinetic Origami) is a physically grounded, deterministic, distributed swarm-agent simulation written in Zig. It models small interconnected robotic units called **Kins** that move, connect, communicate, transfer energy, form assemblies, articulate collectively, and can be inspected down to mechanical detail.

It takes high-level inspiration from programmable matter but must have its own original mechanical architecture and visual identity. Never reproduce the design of Big Hero 6 microbots or any other existing fictional or real robot. Avoid the word "microbot" in any way that implies that identity.

Priorities, in order:

1. mechanical plausibility
2. numerical and physical correctness
3. deterministic, reproducible experiments
4. explicitly validated operating envelopes
5. originality
6. inspectability
7. scalability, only after correctness is established

An attractive animation is not evidence that a mechanism works.

## Where things live

Read these before implementing or evaluating anything:

| Document | Purpose |
| --- | --- |
| [`docs/decisions/`](docs/decisions/README.md) | Append-only decision log (Q1–Q50). **Decisions govern.** Q1–Q30 are known only by reference |
| [`docs/requirements/`](docs/requirements/README.md) | Current requirements with stable IDs (`ENV-`, `PHY-`, `CPL-`, `CTL-`, `COM-`, `PWR-`, `TIM-`, `DAT-`, `INS-`, `BLD-`, `BEN-`, `SEL-`, `PRC-`) and status |
| [`criteria/`](criteria/README.md) | Machine-readable, preregistered, hash-linked criteria |
| [`docs/traceability.md`](docs/traceability.md) | What is implemented, tested, validated, and qualified, and what is not |
| [`docs/roadmap.md`](docs/roadmap.md) | Dependency-ordered phases and the owner decision gates |
| [`docs/toolchain.md`](docs/toolchain.md) | Pinned Zig, build profiles, dependency policy |
| [`docs/design-guidance.md`](docs/design-guidance.md) | Non-binding design guidance for candidate generation |

## Non-negotiable rules

- **No silent changes.** A requirement, criterion, or threshold changes only through a new decision record that names what it supersedes. Old records are never rewritten.
- **No invented numbers.** Thresholds, physical properties, and parameters come from evidence or are labeled provisional. Otherwise they stay `unresolved` until the owner decides at the roadmap gate.
- **No unfounded design selection.** Geometry, couplers, and mechanisms are chosen only through the Q38 gates. Test fixtures are never Kin candidates.
- **Full 3D only.** No production 2D mode, no planar constraints, no snapping, docking assist, or unmodeled pose or velocity correction. State labels never create physical links.
- **Information boundary.** Controllers see only modeled sensors, their own state, and modeled messages. Ground truth belongs to the evaluator. Oracle runs are labeled and never pass.
- **Solver-native loads.** Acceptance loads come from the solver's own outputs with documented accuracy. Uncertainty that overlaps a threshold makes the result `uncertain`.
- **Preregistration.** Criteria are committed and hashed before the evaluation they govern. Solver code for a slice is not written before that slice's validation criteria exist.
- **Determinism.** Integer simulation time, explicit event ordering, seeded RNG, and canonical state hashes. Same build plus same configuration means the same result.
- **Core boundary.** The simulation core uses the Zig standard library only. The inspector is read-only and can never influence results.
- **Result labels.** Every result is exactly one of `exploratory` (default), `oracle`, `fixture`, `uncertain`, or `validated_acceptance`. Planned, implemented, tested, validated, qualified, and accepted are not interchangeable.
- **Unit testing is not physical validation.** One analytic case does not qualify a solver.

## Build and test

The toolchain is pinned to one Zig release. See [`docs/toolchain.md`](docs/toolchain.md).

```sh
tools/zig-toolchain.sh          # download (if needed) and verify the pinned compiler by SHA-256
tools/zig build test            # run all tests with the pinned compiler
tools/zig-verify-signature.sh   # verify the pinned tarball's official minisign signature
tools/zig build inspector       # build the read-only inspector (needs SDL3; see docs/toolchain.md)
```

Never use a system or Homebrew `zig` for recorded results.

## Git workflow

- Branches: `<type>/<short-purpose>` (for example `feat/integer-scheduler`, `docs/q41-q45-records`). **Never put roadmap phase names or numbers in branches, commits, or PRs.**
- Commits: Conventional Commits, `type(scope): description`. Small and coherent. Never amend or rewrite history.
- PR titles use the same style. Descriptions cover what changed, why, requirement and decision IDs, tests, validation evidence, limitations, and follow-ups.
- Never push, open public PRs, pull, merge from remote, or rebase without explicit owner authorization.
- Inspect staged changes before committing. Never discard, reset, or clean existing work.

## Working method

Work in small, reviewable packages:

1. objective
2. requirement and decision IDs
3. prerequisites
4. minimal implementation
5. tests
6. diff review
7. documentation and traceability update
8. limitations recorded
9. commit

At owner decision gates (listed in the roadmap), ask one concise question at a time, with alternatives, conflicts, and a recommendation. Do not ask about questions that are not yet relevant, and continue independent work while a gate is pending.
