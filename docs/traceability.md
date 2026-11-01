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
| DAT-002 | `canonical.zig`, `recording.zig` (format v2), `scene_record.zig` (Q51 payloads) | Byte-layout tests, round trip, exact `-0.0` bits, fail-closed decode | tested | 63 fixture recordings written and loaded | Snapshots cover single-cuboid fixture scenes. Payloads for links, couplers, and sensors come with those models |
| DAT-004 | `canonical.zig`; `driver.zig` hashes exactly the bytes it publishes, under domain tag `kinigami.checkpoint.v1` | Signed-zero and field-order sensitivity; hash equals hash of published bytes | tested | — | Non-finite state values are rejected (fail-closed choice, revisable by decision). No real backend state yet |
| DAT-010 | Reader accepts v1 and v2, rejects others. Version-specific chunk rules | v1 back-compatibility test; inspector rejects v1 explicitly | tested | — | No migration tool (v1 files carry no snapshots to migrate) |
| DAT-011 | `run.Result` with config, criteria, recording, revision, build-profile, and candidate fields | JSON round-trip through the strict parser | implemented | — | Provenance producers (Git revision capture, build-profile ID) are not built, so those fields are null |
| PRC-005 | `run.label` | Label tests: oracle and fixture never upgrade, uncertainty dominates, `validated_acceptance` unreachable while `acceptance_profile_frozen = false` | tested | — | Run-class set (`fixture_validation`, `benchmark`, `controller_development`, `oracle_diagnostic`, `exploratory`) is scaffolding drawn from Q31/Q32/Q40/Q46; extend by decision |
| PRC-012 | `run.RunConfig.run_class` (required) | Config tests | tested | — | — |
| PRC-013 | `run.validate` | Forces rejected in all four other run classes; only declared fixture targets; intervals within the run | tested | — | Timing semantics relative to physics boundaries await the event-phase decision. The driver does not apply forces yet |
| PHY-010 | `src/core/backend.zig`; `rigid.World` implements it | Driver tests with the real solver | implemented | — | — |
| INS-006 | `src/core/snapshot.zig` `BoundedRing` (preallocated, drop-oldest, counted drops and oversize) | Unit test | tested | — | In-process only. Transport to the separate inspector process not built |
| INS-007 | `driver.run` publisher path; suite recorder | Capture on/off identical (stand-in and real solver). Suite with recordings reproduces all 63 official run 2 final-state hashes | tested | `/tmp` comparison against `run2-cd59f3e` | Live streaming transport to the inspector not built (file playback only) |
| TIM-008 | `driver.run`; suite records the final-state hash per sub-run | Full-suite rerun: 63/63 hashes identical; real-solver replay test | tested | run 2 + replay | Same binary and host only |
| BEN-008 | `criteria/fixture-validation/analytic-v1.json` registered at `70b629a55a9c` (SHA-256 `565ef6b6…3e78`) | Build-time byte-identity check against the registered hash; strict parse | tested | Registered before any production solver commit | Local commit only, not externally timestamped |
| BEN-010 | All five cases implemented and evaluated | `results/fixture-validation/analytic-v1/run2-cd59f3e-ReleaseSafe.json` | validated (fixture scope) | pass 9/9 for every case | Protocol revision 2 was post-hoc. Accepted by Q49 |
| BEN-011 | `below_factor` 0.9 / `above_factor` 1.1, enforced by `criteria.validate` | Consistency test rejects a factor of 1.0 | tested | — | — |
| BEN-013 | Separate `fixture_tall_block` with exact pivot geometry | Consistency test: tipping precedes sliding at every friction pair | tested | — | — |
| BEN-014 | Q48 values in criteria v1 | Strict parse and self-consistency validation | tested | — | Tolerances are agent-chosen under delegation, not derived from solver-convergence evidence. Revisable by a superseding decision and a new criteria version |
| BEN-015 | `friction_law: coulomb_static_kinetic`; μs > μk enforced | Consistency test | tested | — | — |
| PHY-001 | `src/core/rigid.zig` (full 3D rigid cuboids, quaternion orientation, no planar constraint) | Analytic fixture-validation suite | validated (fixture scope only) | `results/fixture-validation/analytic-v1/run2-cd59f3e-ReleaseSafe.json`: 5/5 cases pass, 9/9 combinations | Cuboid-vs-plane only. Gyroscopic term omitted. Envelope in the results README |
| PHY-002 | `rigid.zig`: separate rigid bodies; contact as implicit spring-damper constraints | Rest and penetration metrics | implemented (contact only) | Contact-only evidence in run 2 | **Links not implemented** (later slice) |
| PHY-005 | Contact reports are solver impulses ÷ h | Rest force balance (≤1e-3), friction balance, CoP checks use solver outputs | validated (fixture scope) | `results/fixture-validation/analytic-v1/run2-cd59f3e-ReleaseSafe.json` | Accuracy documented only for the declared conditions |
| PHY-006 | Normal compliance is a declared k and c, integrated implicitly. No Baumgarte or ERP stabilization term | Code review; penetration ≈ m·g/(4k) observed | implemented | — | No independent check that numerical damping is absent |
| PHY-007 | Normal and friction impulses in one PGS loop | Friction balance and tipping no-slip metrics | validated (fixture scope) | `results/fixture-validation/analytic-v1/run2-cd59f3e-ReleaseSafe.json` | — |
| PHY-011 | `rigid.zig` labeled not qualified | — | in progress | Fixture validation passed. Qualification checklist (PHY-012) not yet written | **Not qualified** |
| PHY-016 | Timestep sensitivity: 3 steps × 3 friction pairs; worst-margin table | `results/fixture-validation/analytic-v1/run2-cd59f3e-ReleaseSafe.json` | in progress | Sensitivity across Δt reported per metric | No convergence-order study or iteration-count sensitivity yet |
| DAT-011 | `src/validate/main.zig` adds code revision, dirty flag, optimize mode, target, and Zig version to each report | Embedded-revision check before and after a commit | tested | — | Run 1 used the earlier cached mechanism (documented) |
| INS-001 | `src/inspector/` (`kinigami-inspector`), zigui and SDL3 linked only into the inspector | Build graph: core module has no zigui import; purity check passes | implemented | — | — |
| INS-002 | `docs/inspector/library-review.md`, Q50 | Review document | implemented | zigui `ad0481f` builds with Zig 0.17.0 | SDL3 unpinned (BLD-003 limitation) |
| INS-003 | `src/inspector/loader.zig` uses `core.recording` and `core.scene_record` | Loader round-trip test; 63 real recordings loaded | tested | — | — |
| INS-005 | Scene view and readout draw only recorded values. Sums are labeled aggregates of recorded solver forces | Headless tests; screenshot review of real recordings | tested | — | Camera follow and arrow scaling are presentation-only |
| INS-009 | Header shows the label implied by run class (`FIXTURE`, "not Kin evidence"), case, sub-run, friction pair, and timestep | Screenshot review | implemented | — | — |
| INS-008 | No interpolation: playback shows exact recorded frames only | Code review | implemented | — | Interpolated display not offered yet. If added, it must be labeled |
