# Q34 — Power transfer through couplers

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-10-30 |
| Supersedes | — |
| Provenance | condensed from owner decision |

## Context

Q31 sets energy, power, and thermal limits, and Q11 distinguishes actively held shapes from passively locked ones. Both depend on whether Kins can share energy through links.

## Decision

1. **Option B — optional, explicitly modeled power transfer through couplers.** Each candidate declares whether its couplers support power transfer and specifies hardware-grounded electrical characteristics. Transfer is available only through a mechanically engaged coupler with a functioning power path. It is not a universal shared assembly bus.
2. **Limits apply per Kin as well as at the assembly level.** An acceptable aggregate never hides an individual Kin that exceeds its energy, power, or thermal limits. There is no automatic balancing. Transfers result only from controller commands through the normal interface or from explicitly declared passive circuitry.
3. **The first Q31 benchmark requires an energy-isolated baseline.** Every Kin completes it on its own onboard energy. A candidate that supports transfer may additionally run a separately reported power-sharing variant.

## Constraints

- Power-path availability and performance derive from the authoritative mechanical and electrical coupler state. Partial engagement may degrade or prevent transfer, and mechanical engagement alone does not guarantee electrical continuity.
- Where applicable, model contact or coupling resistance, voltage drop, current and power limits, conversion losses, heating, and fault protection. Do not add electrical detail beyond the model's validated fidelity.
- Record every transfer's source, destination, path, amount, losses, and heat for replay and inspection.
- Electrical faults and depleted or disconnected Kins have explicit outcomes. Sharing never bypasses individual limits.
- Cells, voltages, capacities, current limits, and other numbers remain open until supported by component evidence.

## Alternatives considered

- **A. Isolated energy only:** rules out in-assembly recharging and power-relay roles.
- **C. A shared assembly bus with automatic load sharing:** requires full network simulation and weakens per-Kin accountability.

## Rationale

Preserves per-Kin accountability while still allowing designs that share power to demonstrate that capability honestly.
