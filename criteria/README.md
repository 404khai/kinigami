# Criteria

Machine-readable benchmark, validation, qualification, and gate criteria (Q39, Q44). The evaluator reads these files directly.

## Rules

- **Format:** JSON with an explicit `schema_version`, parsed strictly. Unknown fields, missing required fields, duplicate keys, type mismatches, invalid enum values, and out-of-range values are all rejected (DAT-005).
- **Identity:** SHA-256 over the exact file bytes (DAT-003). Formatting-only edits create a new identity.
- **Rationale** goes in explicit fields, never comments. Every threshold carries its justification and source.
- **No silent defaults:** only schema-defined defaults are allowed, and resolved values appear in effective configurations (DAT-006).
- **Integers:** below 2^53, or encoded as strings where the schema says so (DAT-007).
- **Non-finite values:** forbidden unless the schema defines an explicit encoding (DAT-008).
- **Unresolved thresholds** are marked unresolved, never filled with placeholder numbers.

## Preregistration procedure

1. Write the criteria file and commit it **before** the implementation or evaluation it governs.
2. Record its SHA-256, path, commit, and date in [`REGISTER.md`](REGISTER.md).
3. Optionally, for stronger evidence, publish or externally timestamp the hash (Q39).
4. A revision is a **new file** (new version) plus a register entry giving the original, the reason, the date, and the affected evaluations and reruns. Registered files are never edited in place.

Results record the criteria path, SHA-256, and register entry they were evaluated against (DAT-011).
