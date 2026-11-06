# Q65 — Candidate revision records: file layout and corpus identifiers

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-06 |
| Supersedes | — (implements Q38/SEL-007 preservation and Q61 §5 for the first candidate revision; changes no criterion, threshold, protocol text or criteria JSON) |
| Provenance | **agent decision under explicit owner delegation** ("The owner delegates the decisions for this work"). The owner may revise it through a superseding record |

## Context

cand-a is being revised to version 2 (Q64 §3 left revisions to the owner, who has now asked for one). Two record-keeping questions come up before any v2 file exists.

1. **Where the v2 declaration lives.** The registered criteria (`criteria/gates/gate1-v1.json`, `declaration.path_pattern`) and the evaluator fix the path `candidates/<candidate_id>/declaration.json`, and the declaration's `candidate_id` must equal the directory name. Q61 §5 and SEL-007 require the v1 files to be preserved. Review records are already keyed by version (`-v<version>-r<n>.md`), but the declaration is not.
2. **Duplicate corpus identifiers.** Q64 appended entries numbered C21–C29 to `docs/originality/reference-corpus.md`, but C21 (Swarm-bot), C22 (Sambot) and C23 (Blinky Blocks) already existed. "C22", for example, now names two different systems.

## Decision

### 1. Declaration of a revised candidate version

- `candidates/<id>/declaration.json` always holds the **current** version, because the registered path pattern requires that path. No criteria or evaluator change is made.
- Before a new version replaces it, the previous declaration is copied **byte for byte** to `candidates/<id>/declaration-v<old version>.json`. The copy's SHA-256 must equal the `declaration_sha256` recorded in that version's originality review. The commit that adds the copy states the hash.
- The previous version's dossier and review records are **not edited, renamed or moved**. Its dossier keeps the name `dossier.md`. Where that dossier says `declaration.json`, it means the file now kept as `declaration-v<old version>.json`.
- The new version's dossier is `dossier-v<new version>.md`. Its reviews follow the existing patterns (`originality-review-gate1-v<new version>-r<n>.md`, `retention-review-v<new version>-r<n>.md`). The evaluator reads only top-level files that match the current version, so earlier records are kept but not counted.
- Earlier run reports remain reproducible from their recorded code revision. At that revision, `declaration.json` is the earlier version.

### 2. Corpus identifiers

- The entries in the corpus table headed "Additions from the Gate 1 independent reviews (Q64)" are cited as **Q64-C21 … Q64-C29**. The older section-C entries keep their plain identifiers (C21 Swarm-bot, C22 Sambot, C23 Blinky Blocks).
- A note saying this is appended to the corpus. Existing text and earlier review records are not edited. In earlier records, "C21–C23" next to Swarm-bot, Sambot or Blinky Blocks means the section-C entries.
- New reviews use the qualified identifiers.

## Alternatives considered

- **Move v1 into `candidates/cand-a/v1/`:** this moves (touches) v1 files and breaks the paths that run 1's README and v1's reviews cite. Rejected.
- **Give v2 its own directory (`candidates/cand-a2/`):** this changes the candidate identity, and the evaluator would treat it as a different candidate, not a new version. It conflicts with Q61 §5 ("a new candidate version"). Rejected.
- **Change the evaluator to read `declaration-v<n>.json`:** this conflicts with the registered `path_pattern` and needs a new criteria version. Rejected.
- **Renumber the Q64 additions:** this edits existing corpus text. Rejected (append-only).

## Consequences

- The v1 bytes stay available at a stable path, and a hash links them to the v1 reviews.
- The corpus becomes unambiguous without rewriting it.
