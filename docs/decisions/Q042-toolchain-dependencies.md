# Q42 — Toolchain, dependencies, and determinism-relevant build settings

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-10-30 |
| Supersedes | — |
| Provenance | condensed from owner decision |

## Context

Exact replay is guaranteed only for "the same build and configuration" (Q14), so "the same build" must be well defined. The Zig version, target CPU features, float mode, optimization level, threading, and third-party code can all change floating-point results.

## Decision

1. **A2 — pin one exact tagged stable Zig release,** not `master` or nightly. Record the compiler distribution's content hash. Upgrades require an explicit decision record, followed by replay verification and rerunning every validation case whose results could be affected. The current stable version is verified when toolchain setup is authorized rather than guessed in advance.
2. **B2 — tiered dependency policy:**

   | Area | Policy |
   | --- | --- |
   | Simulation core | Zig standard library only. No third-party runtime dependencies |
   | Inspector and rendering | Vetted dependencies allowed behind a read-only boundary |
   | Validation tooling | External engines permitted under Q41, after license and technical-fit review |
   | All dependencies | Direct and transitive dependencies pinned by content hash, with licenses recorded |

   The inspector consumes snapshots or recorded events. It never mutates authoritative simulation state or influences simulation timing.
3. **A declared acceptance build profile is required for validated-acceptance results.** The profile specifies:
   - Zig version and compiler hash
   - target triple and explicit CPU feature baseline
   - optimization level
   - floating-point mode and fused-operation policy
   - relevant compiler and linker flags
   - dependency lock state and hashes

   Host-native CPU autodetection is not used for acceptance builds. Other profiles (Debug, local performance experiments) may be used, but their results stay exploratory until shown to match the acceptance profile across the relevant validation suite. **Open:** the exact optimization level for the acceptance profile. It is chosen and frozen before the first validated acceptance run and does not vary between experiments.
4. **Deterministic threading semantics.** Logical work partitioning never depends on the number of worker threads:
   - divide work into stable logical chunks, which any worker may execute
   - combine results in a fixed order
   - never let task completion order determine event order or floating-point reduction order
   - avoid unordered floating-point atomic accumulation

   Changing the worker count changes scheduling, not results. Until this is implemented and verified, the core stays single-threaded (consistent with Q41: throughput is not a slice 1 or 2 gate).

## Consistency

- **Q14:** makes same-build/configuration replay concrete without promising cross-platform bitwise identity.
- **Q15:** the backend boundary stays intact.
- **Q39:** result records include the acceptance profile identifier and hash.
- **Q41:** external engines stay validation-only.

Pinning the toolchain makes results reproducible, not correct. The solver still earns qualification through Q41's staged validation.

## Alternatives considered

- **A1. Track master/nightly:** frequent breakage, and results can't be reproduced over time.
- **B1. Zig-only everywhere:** windowing and GPU access become impractical.
- **B3. Libraries allowed anywhere:** exposes the core to external numerical behavior.
