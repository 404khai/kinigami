# Q40 — First implementation milestone

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-10-30 |
| Supersedes | The original AGENTS.md §14 task list (pre-decision baseline, commit `a89d304`), in particular its "2D or simplified 3D prototype" item |
| Provenance | condensed from owner decision |

## Context

The acceptance bar from Q31–Q39 is high. The original task list permitted a 2D prototype, which Q31 forbids. Infrastructure also needs bodies to simulate before Gate 1 has produced candidates.

## Decision

1. **Option C — a thin vertical slice on the production 3D architecture.** Physics, sensing, communication, controllers, evaluator, deterministic stepping, SI units, replay, and criteria versioning are distinct from the beginning. Models may be minimal, provisional, and marked exploratory, but the architecture must not depend on shortcuts that contradict accepted decisions.
2. **Neutral test-fixture bodies are permitted before Gate 1.** Generic bodies (for example, a rounded block) and simple coupler stand-ins may exercise the infrastructure. They are labeled as fixtures in source, data, logs, and the inspector. They are not Kin candidates, do not enter Q38, and cannot establish candidate feasibility.
3. **Every initial slice result defaults to exploratory until its relevant models pass validation.** Validation applies to specific models, conditions, and claims. One analytic case does not validate the engine, and a validated fixture does not establish candidate feasibility.

## Slice sequence

- **Slice 1 — Neutral body and tabletop contact:** a generic body on the reference tabletop in full 3D. Compare equilibrium and contact against analytic statics. Establish SI units, deterministic stepping, state recording, replay, and evaluator separation.
- **Slice 2 — Compliant connection:** two fixture bodies with a fixture-only compliant constraint. Exercise Q35 solver outputs, load reporting, compliance, and reference validation against analytic statics and separate reference dynamics.
- **Slice 3 — Reduced coupler engagement:** two fixture bodies dock through a fixture-only reduced continuous mechanism. Exercise alignment, contact, latch travel, engagement-dependent constraint strength, and physical release under load. Follow Q36: no snapping, assistance, or unmodeled correction.

## Constraints

- Full 3D rigid-body physics from the first slice. No production 2D mode and no artificial planar constraint. A test may use planar geometry where analytically appropriate, but the simulation stays 3D.
- Physics, sensing, communication, controller, and evaluator stay separate, and controllers never receive ground truth.
- Oracle access is restricted to labeled development and diagnostic runs.
- Deterministic simulation-time stepping, stable event ordering, replayable inputs, and criteria versioning and hashing (Q14, Q39).
- Fixtures never silently become candidates. Any reference Kin enters Q38 independently.
- Fixtures are visibly distinct in the inspector, along with their exploratory or validation status.
- Convincing movement or visuals never establish feasibility, fidelity, or benchmark success.
- Prototype convenience never bypasses Q31–Q36.
- Preserve the replaceable backend (Q15).
- The superseded 2D task list is recorded here, not silently rewritten.

## Alternatives considered

- **A. Infrastructure before anything moves:** slow feedback, with interfaces designed without ever being run.
- **B. A throwaway 2D/oracle prototype:** risks becoming the real codebase, and 2D says little about 3D tipping and contact.
