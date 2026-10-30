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
| BLD-001 | `tools/zig-toolchain.sh`, `tools/zig`, `docs/toolchain.md` | Script verifies tarball SHA-256 and reported version | tested | Zig 0.17.0, `aarch64-macos` SHA-256 `b607e9b9…c536a` verified on download | Minisign signature not verified. Mismatch path not exercised by an automated test |
| BLD-002 | `build.zig`, `build.zig.zon` (no dependencies) | Build graph review | implemented | — | No automated dependency audit yet |
| BLD-004 | `docs/toolchain.md` draft profile | `tests/conformance/float_contraction_test.zig` | in progress | No implicit FMA in all four optimize modes, native and `-Dcpu=baseline` | Profile not frozen. Optimization level unresolved (BLD-005). Verified on one host only |
| DAT-003 | `src/core/identity.zig` | FIPS 180-2 vectors; no-normalization test | tested | `tools/zig build test` | No register tooling yet |
| DAT-005 | — (strict layer not built) | `tests/conformance/std_json_test.zig` | in progress | std rejects unknown, duplicate, missing, invalid-enum, out-of-range, and trailing input | **std is lenient** on numeric strings, float-formatted ints, integer enum tags, and non-finite strings. The strict layer must reject these |
| DAT-007 | — | Conformance test documents std acceptance above 2^53 | in progress | — | Enforcement belongs to the strict layer |
| DAT-008 | — | Conformance tests document `1e400` → `+inf` and `"nan"` acceptance | in progress | — | Enforcement belongs to the strict layer |
| DAT-009 | Relies on `std.fmt.parseFloat` | `tests/conformance/float_parse_test.zig` | tested | Bit-exact ties-to-even, subnormal, and overflow cases pass in all optimize modes, native and baseline CPU | Verified for Zig 0.17.0 only. Rerun on upgrade |
