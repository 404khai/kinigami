# Criteria register

Append-only. One row per registered criteria file version.

| Criteria file | SHA-256 | Registered at commit | Date | Governs | Supersedes | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `fixture-validation/analytic-v1.json` | `565ef6b62aeebe92aabf6dc2a4763aef02d9e4e51579985513c2cff4f9df3e78` | `70b629a55a9c` | 2026-10-31 | Analytic fixture-validation cases (Q46–Q48): rest, free fall, friction threshold, sliding to a stop, tipping | — | Registered before any production solver code. Local Git commit only; not externally timestamped |
| `qualification/compliant-link-v1.json` | `7e147a9dda34caf73932b1734b41cccb70f0574cb3211b640624785312eb77f8` | `8fbb4ddadb2d` | 2026-11-02 | Compliant-link backend qualification L1–L10 (Q52) | — | Registered before any compliant-link code. Local Git commit only; not externally timestamped |
| `qualification/compliant-link-v2.json` | `8cfe7c42b6829f4d90694e3b35378b45abe902fc1ecc221d30076e702b7e0c6e` | `8a379d3` | 2026-11-02 | Compliant-link backend qualification L1–L10 (Q52, Q53) | `qualification/compliant-link-v1.json` | Q53: L2 bending moment and angle references include the tension lever; tolerances unchanged. Post-hoc after run 1 (`run1-77bc3ca`, preserved); registered before the evaluator change and run 2. Local Git commit only; not externally timestamped |
| `qualification/coupler-engagement-v1.json` | `1f07a24b1b3de9cd5da825b9ef5153bb8f693f0cf399484b14921f5f6e0e8bdc` | `1ea8629cee99` | 2026-11-02 | Reduced coupler engagement fixture qualification C1–C10 (Q56, Q57) | — | Registered before any guide-contact, latch, or engagement code. Local Git commit only; not externally timestamped |
