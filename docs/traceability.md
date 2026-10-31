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
| DAT-006 | `strict_json` schema defaults; recordings store exact effective-config bytes | Unit tests | implemented | — | Serializing resolved defaults back into an effective configuration file is not built yet |
| TIM-001 | `src/core/time.zig` | Unit tests | tested | — | Time unit value unresolved (TIM-012) |
| TIM-002 | `time.PhysicsStep` (positive tick count) | Unit tests | tested | — | Step value unresolved |
| TIM-003 | Checked arithmetic in `time.zig` | Overflow unit tests | tested | — | — |
| TIM-004 | `src/core/scheduler.zig`, generic over the phase enum | Ordering, shuffle-invariance, and cursor tests | tested | — | Concrete phase list and order still open |
| TIM-007 | `src/core/rng.zig` interface; `tools/check-core-purity.sh` | Determinism harness; purity check in the test step | implemented | — | RNG algorithm, seed width, and stream semantics unresolved. Only a test-only counter exists. The purity check is textual |
| DAT-002 | `src/core/canonical.zig`, `src/core/recording.zig` | Encoding byte-layout tests; container round-trip | tested | — | Snapshot, event, sensor, and actuator payload layouts and the snapshot interval are open. Only the container and the effective-config chunk exist |
| DAT-004 | `canonical.zig`; `driver.zig` hashes exactly the bytes it publishes, under domain tag `kinigami.checkpoint.v1` | Signed-zero and field-order sensitivity; hash equals hash of published bytes | tested | — | Non-finite state values are rejected (fail-closed choice, revisable by decision). No real backend state yet |
| DAT-010 | `recording.zig` format v1 | Rejects bad magic, unsupported version, nonzero flags, unknown chunk types, duplicate config, non-empty end, trailing bytes, and every truncated prefix | tested | — | No migration tooling (only v1 exists) |
| DAT-011 | `run.Result` with config, criteria, recording, revision, build-profile, and candidate fields | JSON round-trip through the strict parser | implemented | — | Provenance producers (Git revision capture, build-profile ID) are not built, so those fields are null |
| PRC-005 | `run.label` | Label tests: oracle and fixture never upgrade, uncertainty dominates, `validated_acceptance` unreachable while `acceptance_profile_frozen = false` | tested | — | Run-class set (`fixture_validation`, `benchmark`, `controller_development`, `oracle_diagnostic`, `exploratory`) is scaffolding drawn from Q31/Q32/Q40/Q46; extend by decision |
| PRC-012 | `run.RunConfig.run_class` (required) | Config tests | tested | — | — |
| PRC-013 | `run.validate` | Forces rejected in all four other run classes; only declared fixture targets; intervals within the run | tested | — | Timing semantics relative to physics boundaries await the event-phase decision. The driver does not apply forces yet |
| PHY-010 | `src/core/backend.zig` interface | vtable wiring via test-only stand-in | implemented | — | **No production solver** (blocked until slice validation criteria are preregistered) |
| INS-006 | `src/core/snapshot.zig` `BoundedRing` (preallocated, drop-oldest, counted drops and oversize) | Unit test | tested | — | In-process only. Transport to the separate inspector process not built |
| INS-007 | `driver.run` publisher path | Capture-on vs capture-off checkpoint hashes identical over 64 steps; publisher has no RNG or scheduler access | tested | — | Demonstrated with a test-only stand-in backend, not real physics |
| TIM-008 | `driver.run` | Two runs reproduce all 64 checkpoint hashes; perturbed initial state diverges | tested | — | Physics-free stand-in only. Same-process replay, not from a recording file yet |
