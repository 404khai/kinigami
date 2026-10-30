# Kinigami documentation

| Document | Role | Authority |
| --- | --- | --- |
| [Decision log](decisions/README.md) | Append-only history of engineering decisions | **Highest.** Decisions govern |
| [Requirements](requirements/README.md) | Current requirements with stable IDs and status | Derived from decisions |
| [Criteria](../criteria/README.md) | Machine-readable benchmark and gate criteria read by the evaluator | Preregistered, hash-linked |
| [Traceability](traceability.md) | Requirement → implementation → verification → result | Evidence record |
| [Roadmap](roadmap.md) | Dependency-ordered phases and owner decision gates | Planning |
| [Toolchain](toolchain.md) | Pinned compiler, build profiles, dependency policy in practice | Implements Q42 |
| [Design guidance](design-guidance.md) | Non-binding input for candidate generation | Advisory only |

Changing a requirement, criterion, or threshold takes a new decision record. See the [decision log rules](decisions/README.md#rules).
