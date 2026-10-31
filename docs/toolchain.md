# Toolchain

Implements Q42 (BLD-001 to BLD-006).

## Pinned compiler

| Field | Value |
| --- | --- |
| Zig release | **0.17.0**, the latest tagged stable release on 2026-10-30 (released 2026-10-01; verified against `https://ziglang.org/download/index.json`) |
| Identity | SHA-256 of the official release tarball |
| `aarch64-macos` | `b607e9b9234790a008116ae5bdb71c6243b84b9fb42a53a9e70fde41c06c536a` |
| `x86_64-macos` | `4f9a1c5269aa17ebda5e6d3c2b89d6cbf36f7d2b22a0306e9ab98f25f95529c6` |
| `x86_64-linux` | `1cbe9df9f27e6b78d14ccbca43b6703a404ef79ef1c463de901d7f088d4e2026` |
| `aarch64-linux` | `9e8d11661d4ae3bd57702a3832781e23ad151dde5798e16a5ccd503f65234ff8` |
| Source tarball | `b6c7f1728f043700d6529bac980800792f824256a9d2f1839b3d62beed0b8abd` |

`tools/zig-toolchain.sh` downloads the tarball for the host into `.toolchain/` (gitignored). It verifies the SHA-256 **before** extraction, checks that `zig version` reports `0.17.0`, and records a verification stamp. `tools/zig` runs that verified compiler. Never use a system or Homebrew `zig` for recorded results: a Homebrew build is a different binary even when it reports the same version.

### Authenticity and provenance

Zig publishes a minisign signature (`<tarball>.minisig`) for every release artifact. These signatures use the `ED` algorithm: Ed25519 over a BLAKE2b-512 prehash. A signed trusted comment names the file and the signing timestamp.

| Check | Method | Result (2026-10-30) |
| --- | --- | --- |
| Signing key | Fetched from `ziglang.org/download/` and from the `ziglang/www.ziglang.org` source repository on GitHub | Both match: `RWSGOq2NVecA2UPNdBUZykf1CCb147pkmdtYxgb3Ti+JO/wCYvhbAb/U` |
| Pinned SHA-256 values | All four platform tarballs downloaded and hashed | All four match `tools/zig-toolchain.sh` |
| Official signatures | `tools/minisign.zig` (std-only verifier) on all four tarballs | All four verify. The trusted comments name the correct files (timestamps 1790965431–1790965900) |
| Tamper detection | One corrupted byte in a tarball copy | Rejected: `BadFileSignature` |
| Fetch-script rejection | Script copy with a wrong expected SHA-256 | Exits 1 before extraction; no files left behind |

The signatures are stored in `tools/zig-signatures/`. `tools/zig-verify-signature.sh` re-verifies the host's tarball.

**Limitations:**

- **Same trust anchor for the key.** Both key sources are controlled by the Zig project, so they protect against a compromised download mirror, not a compromised project.
- **Self-hosted verifier.** `tools/minisign.zig` runs under the pinned compiler, so its signature check is only as trustworthy as the SHA-256 pin that admitted that compiler. The original verification ran on 2026-10-30, before the pin was relied on. For a fully independent check, use the reference `minisign` tool (not installed on the development host).
- **No hosted check yet.** Signature verification is not yet part of the automated download path. It is a manual or scripted step.

Upgrading the pin requires a decision record, then replay verification and reruns of affected validation cases (BLD-001).

## Commands

```sh
tools/zig-toolchain.sh                 # fetch and verify; prints compiler path
tools/zig build test                   # core + tools unit tests + conformance (current optimize mode)
tools/zig build conformance            # conformance under Debug, ReleaseSafe, ReleaseFast, ReleaseSmall
tools/zig-verify-signature.sh          # verify the host tarball's official minisign signature
```

## Dependency policy in practice

| Area | Policy | Current dependencies |
| --- | --- | --- |
| Simulation core (`src/core`) | Zig standard library only | none |
| Inspector | Vetted, hash-pinned, license recorded | none yet. Library review pending (INS-002) |
| Validation tooling | Validation-only external engines after review (Q41) | none yet |

`build.zig.zon` declares no dependencies. Any future dependency is pinned by its content hash in `build.zig.zon` (direct and transitive), and its license is recorded here.

## Acceptance build profile (draft, not frozen)

| Field | Draft value | Status |
| --- | --- | --- |
| Compiler | Zig 0.17.0, tarball SHA-256 as above | fixed |
| Target triple | `aarch64-macos` (development host) | proposed |
| CPU features | `-Dcpu=baseline`, the explicit architecture baseline. Never host autodetection | proposed |
| Optimization level | **unresolved** (BLD-005). Frozen before the first validated acceptance run | unresolved |
| Float mode | Zig default (strict). No `@setFloatMode(.optimized)` in the simulation core | proposed |
| Fused-operation policy | No implicit contraction. FMA only through explicit `@mulAdd`. Verified by `tests/conformance/float_contraction_test.zig` in all optimize modes | proposed, verified on host |
| Flags | none beyond the above | proposed |
| Dependency lock | `build.zig.zon` content hash | fixed |

Results from any other profile (including host-native test runs) stay exploratory until shown to match this profile across the relevant validation suite (BLD-006).

## Test matrix (exact counts, fresh caches, 2026-10-30)

Measured with a fresh `--cache-dir` per run, so no step was served from cache.

| Command | Configuration | Test executables | Tests |
| --- | --- | --- | --- |
| `tools/zig build test` | native CPU, Debug | core 3, tools 4, conformance-debug 24 | **31** |
| `tools/zig build test -Dtarget=aarch64-macos -Dcpu=baseline` | baseline CPU, Debug | core 3, tools 4, conformance-debug 24 | **31** |
| `tools/zig build conformance` | native CPU | 24 × {Debug, ReleaseSafe, ReleaseFast, ReleaseSmall} | **96** |
| `tools/zig build conformance -Dtarget=aarch64-macos -Dcpu=baseline` | baseline CPU | 24 × 4 modes | **96** |

The core count of 3 is the two `identity` tests plus the aggregating `test {}` block in `src/core/root.zig`.

**Correction:** an earlier report gave "72/72" for the conformance step. That run had served the Debug conformance results from the build cache, so only 3 × 24 tests actually executed. The complete count is 96 per CPU configuration, 192 across both.

## Conformance findings (Zig 0.17.0)

`tests/conformance/` pins down standard-library behavior that Kinigami relies on or must override.

**Behaves as required:**

- `std.json` typed parsing rejects unknown fields, duplicate keys, missing fields, invalid enum names, out-of-range integers, trailing content, malformed documents, and non-JSON number grammar (`NaN`, `Infinity`, `0x10`, `+1`, `01`, `.5`, `1.`).
- `std.fmt.parseFloat(f64, …)` rounds correctly to nearest, ties to even, including slow-path halfway cases, subnormal boundaries, and overflow.
- `a * b + c` is not implicitly fused in any optimize mode, on either the native or the baseline CPU target.

**Lenient. Kinigami's strict JSON layer must reject these (DAT-005, DAT-007, DAT-008):**

1. Float-formatted integral numbers (`3.0`, `3e0`) are accepted into integer fields.
2. Bare integers are accepted as enum tags.
3. Numeric strings (`"3"`, `"0.5"`) are accepted into number fields.
4. Strings such as `"nan"` and `"-inf"` are accepted into float fields as non-finite values.
5. Decimal overflow (`1e400`) becomes `+inf` in float fields.
6. Integers above 2^53 are accepted into wide integer fields.
7. Integer literals are accepted into float fields. This may be acceptable. The strict-schema design decides per field.

Consequence: `std.json.parseFromSlice` with default options is **not** sufficient for criteria and configuration files. A strict layer (planned with the core infrastructure work) must enforce the schema rules on top of it.
