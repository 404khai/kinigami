# Reference engine review (Q41, PHY-009, PHY-014)

Q41 permits external physics engines **only for validation**, after license and technical-fit review, and never in production builds. MuJoCo was named as a candidate, not a selection.

## When a reference engine is needed

| Stage | Reference needed | Reason |
| --- | --- | --- |
| Slice 2: two bodies, one compliant link | **No** | Every qualification case has an exact closed form (statics, oscillator frequency, damping, momentum) |
| Chains of three or more bodies (the Q31 chain) | **Yes** | No closed form for general multi-body dynamics. Q35 requires a joint-coordinate reference for open chains |
| Closed loops and contact-rich assemblies | Case by case | Joint-coordinate references don't represent loops natively. Q35 requires gaps to be documented |

## Candidate: MuJoCo

| Criterion | Finding | Assessment |
| --- | --- | --- |
| License | Apache License 2.0 (open-sourced by Google DeepMind) | Compatible with validation-only use. To be re-verified against the exact release before adoption |
| Formulation | Generalized (joint) coordinates, recursive dynamics | Matches Q35's "joint-coordinate reference for open chains" |
| Contact and compliance model | Soft, convex-optimization-based constraints with solver parameters | Not equivalent to Kinigami's contact model. **Use only for link and chain dynamics without contact**, where formulations can be compared fairly |
| Integration | C library, normally built with CMake, prebuilt releases available | Must stay a separate validation tool, hash-pinned, outside `src/core` and the inspector |
| Determinism | Deterministic for a fixed build and configuration | Adequate for reference comparisons. Cross-checking tolerances must allow for formulation differences |

## Alternative: an in-repo joint-coordinate reference

A small Featherstone-style articulated-body solver in Zig, used only for open-chain reference cases.

- **For:** no external dependency, and exactly the frictionless, contact-free chain dynamics needed.
- **Against:** same author as the production solver, so less independent. It also needs its own validation against closed forms.

## Recommendation

- **Slice 2:** adopt no reference engine. Use closed forms only.
- **Before the chain stage:** decide between MuJoCo, validation-only and hash-pinned, and an in-repo joint-coordinate reference. That's a separate decision gate when it becomes relevant.
