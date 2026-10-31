# Q33 — Communication channels

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-10-30 |
| Supersedes | — |
| Provenance | condensed from owner decision |

## Context

Q32's phrase "communication links" was ambiguous. It could mean messages through engaged couplers or over a contactless channel. Docking negotiation also needs a defined way for unlinked Kins to talk.

## Decision

1. **Option C — two separately modeled channels:** a through-coupler channel and a short-range contactless channel, both optional capabilities. Each candidate declares its available channels and their hardware-grounded parameters.
2. **Coupler-channel quality depends on mechanical state.** Availability and reliability derive from the authoritative coupler state: engagement, alignment, degradation, and separation. Partial engagement never behaves as a perfect connection. The mapping from mechanical state to communication performance remains open pending component evidence.
3. **Articulation success and through-chain communication are separate.** The Q31/Q32 benchmark may use any declared channel. The evaluator records each message's route and channel. Through-chain propagation has its own acceptance criterion: the target must propagate along the engaged coupler chain, and contactless shortcuts do not count. This can be a distinct mode or a companion benchmark. Coupler communication is not a universal hardware requirement.

## Constraints

- Reachability derives from authoritative physical state, never from a manually maintained neighbor list.
- Through-coupler reachability comes from the mechanical connection and its modeled communication state. Contactless reachability comes from the modeled channel, including geometry, range, occlusion, and other applicable effects.
- Message paths, delays, losses, and outcomes are recorded for replay.
- Channel technologies and parameters remain open until supported by evidence.
- No channel bypasses the Q22 or Q32 constraints.

## Alternatives considered

- **A. Through-coupler only:** unlinked Kins could not negotiate docking by message.
- **B. Contactless only:** reachability becomes purely geometric, and benchmarks could not demonstrate through-chain propagation.

## Rationale

Supports both free-swarm behavior and through-structure signaling, while keeping each claim honest about which path carried the information.
