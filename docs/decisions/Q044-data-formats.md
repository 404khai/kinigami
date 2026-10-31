# Q44 — Data formats and hashes

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-10-30 |
| Supersedes | — |
| Provenance | condensed from owner decision, including agent-proposed refinements the owner accepted |

## Context

Slice 1 establishes recording, replay, and evaluator separation. Q39 requires evaluator-readable criteria linked to results by hash, and under Q42 the evaluator may use only the Zig standard library.

## Decision

1. **Option B — JSON text plus versioned binary recordings.**

   | Artifact | Format |
   | --- | --- |
   | Benchmark criteria | JSON |
   | Run configuration | JSON |
   | Results | JSON |
   | Recordings | Versioned binary |

   JSON is chosen over ZON so external analysis, CI, and publication tooling can read criteria and results. Rationale goes in explicit JSON fields, not comments. Binary recordings use explicit little-endian encoding and preserve floats as exact bit patterns. Raw Zig structs are never serialized, because memory layout, padding, and alignment are not a stable format. Field order and encoding are defined explicitly.
2. **SHA-256 over exact file bytes, without normalization.** Whitespace changes, key reordering, or any edit produce a new identity. Every artifact records its schema version and SHA-256 digest. Two kinds of hash are distinct:
   - **File identity hash:** SHA-256 over the exact bytes of a JSON or binary file.
   - **Checkpoint state hash:** SHA-256 over a canonical encoding of authoritative simulation state. That encoding defines field order, integer widths, endianness, and float bit representation, and excludes memory addresses, padding, and incidental runtime data.
3. **Strict parsing that fails closed.** Criteria and configuration parsers reject unknown fields, missing required fields, duplicate keys, incorrect types, invalid enum values, out-of-range values, and malformed JSON or trailing content.
   - Defaults are permitted only where the schema defines them, and resolved defaults appear in the effective run configuration.
   - The conversion from a JSON decimal to an IEEE-754 binary value is specified, including rounding, and resolved values are recorded where they affect acceptance.
   - A misspelled acceptance threshold must never produce a successful benchmark.
4. **Schema evolution.** Every format has an explicit schema version, and readers identify it before interpreting content. Old recordings stay readable through version-specific readers where supported, and unsupported versions are rejected. Migrations create new artifacts with new hashes and preserve the originals. No file is silently reinterpreted under a newer schema. A migration records its source version, target version, and migration tool version.

## Additional requirements

1. JSON criteria, configurations, and results require a schema version.
2. Binary recordings require a magic identifier, a format version, and explicit encoding rules.
3. Checkpoint hashes use canonical state encoding, not raw memory.
4. The inspector reads recorded state and events and never independently reconstructs authoritative state.
5. Results identify the exact criteria, configuration, recording, code revision, and acceptance build profile.
6. Hashes establish artifact identity, not physical or numerical correctness. Q41 qualification remains the authority for correctness.
7. **Large integers:** JSON integers are bounded below 2^53 or encoded as strings, as defined per field (agent refinement, accepted).
8. **Non-finite values:** JSON has no NaN or ±Infinity. Schemas forbid them or encode them explicitly, and never map them silently to `null` (agent refinement, accepted).
9. **Parser verification:** `std.json` rejection behavior and nearest-even decimal-to-float parsing are verified against the pinned Zig version with tests, not assumed (agent refinement, accepted).

## Alternatives considered

- **A. JSON everywhere, including JSON-lines recordings:** huge, slow, and authoritative floats would round-trip through decimal text.
- **C. A third-party serialization framework (Protobuf, FlatBuffers, Cap'n Proto):** violates Q42's standard-library-only core.
- **ZON for text:** no external tooling can read it.
