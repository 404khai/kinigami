# Traceability map

Links requirements to implementation, verification, recorded results, and known limitations (Q39, PRC-004).

**Any requirement not listed here is not implemented and not verified.**

Evidence status follows the roadmap vocabulary: planned, in progress, implemented, tested, validated, qualified, accepted.

| Requirement | Implementation | Verification | Evidence status | Result / commit | Limitations |
| --- | --- | --- | --- | --- | --- |
| PRC-001 | `docs/decisions/` | Git history | implemented | Decision log commits | Q1–Q30 known by reference only |
| PRC-002 | `docs/requirements/` | Review | implemented | — | — |
| PRC-004 | this file | Review | implemented | — | — |
| PRC-008 | `docs/decisions/Q001-Q030-reference-only.md` | Review | implemented | — | Original Q1–Q30 text unavailable |
| BLD-001 | `tools/zig-toolchain.sh`, `tools/zig`, `tools/minisign.zig`, `tools/zig-verify-signature.sh`, `tools/zig-signatures/`, `docs/toolchain.md` | SHA-256 before extraction; version check; official minisign signatures; tamper and mismatch tests | tested | All four pinned platform hashes match. All four official signatures verify. Corrupted tarball rejected. Wrong-hash script exits before extraction | Key sources share one trust anchor (the Zig project). The verifier runs under the pinned compiler. Signature check is not in the automatic fetch path |
| BLD-002 | `build.zig`, `build.zig.zon` (no dependencies) | Build graph review | implemented | — | No automated dependency audit yet |
| BLD-004 | `docs/toolchain.md` draft profile | `tests/conformance/float_contraction_test.zig` | in progress | No implicit FMA in all four optimize modes, native and `-Dcpu=baseline` | Profile not frozen. Optimization level unresolved (BLD-005). Verified on one host only |
| DAT-003 | `src/core/identity.zig` | FIPS 180-2 vectors; no-normalization test | tested | `tools/zig build test` | No register tooling yet |
| DAT-005 | `src/core/strict_json.zig` | Unit tests reject every lenient std behavior plus unknown, duplicate, missing, null, trailing, and length errors | tested | `tools/zig build test` | Out-of-range checks for non-integer types are limited to finiteness. No schema-version helper yet |
| DAT-007 | `strict_json`: numbers limited to \|n\| ≤ 2^53−1; `StringU64` for wider values | Unit tests at 2^53−1, 2^53, and canonical-string cases | tested | — | Which fields use `StringU64` is decided per schema |
| DAT-008 | `strict_json` rejects decimal overflow and non-finite strings | Unit tests | tested | — | No explicit non-finite encoding defined (none needed yet) |
| DAT-009 | Relies on `std.fmt.parseFloat` | `tests/conformance/float_parse_test.zig` | tested | Bit-exact ties-to-even, subnormal, and overflow cases pass in all optimize modes, native and baseline CPU | Verified for Zig 0.17.0 only. Rerun on upgrade |
| DAT-006 | `strict_json`: Zig field defaults are schema defaults, used only for absent keys; optionals need explicit `null` | Unit test | implemented | — | Writing resolved defaults into the effective configuration is not built yet |
| TIM-001 | `src/core/time.zig` | Unit tests | tested | — | Time unit value unresolved (TIM-012) |
| TIM-002 | `time.PhysicsStep` (positive tick count) | Unit tests | tested | — | Step value unresolved |
| TIM-003 | Checked arithmetic in `time.zig` | Overflow unit tests | tested | — | — |
| TIM-004 | `src/core/scheduler.zig`, generic over the phase enum | Ordering, shuffle-invariance, and cursor tests | tested | — | Concrete phase list and order still open |
| TIM-007 | `src/core/rng.zig` interface; `tools/check-core-purity.sh` | Determinism harness; purity check in the test step | implemented | — | RNG algorithm, seed width, and stream semantics unresolved. Only a test-only counter exists. The purity check is textual |
