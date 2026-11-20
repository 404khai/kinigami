# Handoff: get cand-d through Gate 1 (cloud agent instructions)

Written 2026-11-20 by the engineering lead (Claude Opus 5.5) for a cloud coding agent.
Branch: `feat/cand-d-coupler-first`, HEAD `f8c1c99` at handoff. Repository: `404khai/kinigami`.

## 1. Goal and authority

**Goal:** at least one candidate passes Gate 1. That means every item G1–G8 is `pass` in an official `zig-out/bin/kinigami-gate1` run, built from a clean tree (`working_tree_dirty: false`).

**Keep going until that result exists.** Do not stop to ask. The owner has delegated all decisions to the lead role, which you now hold. Record each decision as an append-only record in `docs/decisions/` with the provenance "agent decision under explicit owner delegation". The next free number is **Q94**.

**Never change a criterion, threshold or verdict to obtain a pass.** A criteria change needs:
1. its own superseding decision record, and
2. a newly registered criteria version (`criteria/gates/gate1-v2.json` plus `criteria/REGISTER.md`), committed **before** any evaluation it governs.

Q85 decided to keep the Q12 60 mm envelope and `gate1-v1`. Stay with that unless a recorded decision with numbers shows it is infeasible.

If you conclude, with numbers, that no candidate can pass under the kept requirements, say so in a decision record rather than forcing a pass.

Read `AGENTS.md` first and follow it strictly.

## 2. State at handoff

| Candidate | Status |
| --- | --- |
| cand-a v5 | `fail` (G6). Revisions stopped (Q84) |
| cand-b v1, cand-c v1 | `fail` (G5) |
| **cand-d** (Family B, Q85) | Versions 1 to 4 evaluated in runs 6 to 9. Each was `unresolved` on **G6 only**; G1–G5, G7 and G8 passed every time |
| **cand-d v5** | Declared at `f8c1c99` (decision Q93, sha `c6baa8dc…8897d`). **Its two independent reviews have not been done.** Both reviewer sessions died on an API rate limit before writing anything useful |

Results and dispositions are in `results/gates/gate1-v1/README.md` (runs 1–9) and Q86, Q88, Q90 and Q92.

cand-d v5 on the registered evaluator, draft (not a recorded run):
- G1 D 59.133 mm;
- G2 1081 pairs, no interference;
- G3 pass;
- G4 31.181 g, peak 3939 / 19425 mW;
- G5 supported at roll 0.

### How the G6 reviews have gone

Each review found real but narrower issues, and none was a contradiction from v2 on:

| Review | Main open items |
| --- | --- |
| v1 | mount not buildable; torsion relied on friction; missing stops |
| v2 | ears not joined; preload lower bound missing |
| v3 | tail stud threaded into PA12; slot lash at the wrong radius |
| v4 | at the guaranteed lower-bound motor torque the teeth could not roll or yaw a unit flat; no motor mount; no voltage sense |

v5 closes the v4 items, and `candidates/cand-d/dossier-v5.md` §1 maps each one.

## 3. What to do next (the loop)

Repeat until G1–G8 all pass.

1. **Independent reviews of the current version.** Both must be written by sessions that had **no authorship** in cand-d: a separate agent session or child session that did not write or edit any cand-d file. Never write these reviews yourself; you are the author from now on.
   - **Retention (G6):** `candidates/cand-d/retention-review-v<N>-r1.md`, following protocol §8 (`docs/validation/gate1-v1-protocol.md`). Model the brief on the earlier records, `retention-review-v4-r1.md` for example. Give the reviewer the brief in §5.
   - **Originality (G7, G8):** `candidates/cand-d/originality-review-gate1-v<N>-r1.md`, following Q61. The format is in `originality-review-gate1-v4-r1.md`. A changed coupler needs a full fresh review (Q61 §5).
   - Header keys (column 0, each exactly once) are parsed by the evaluator. Copy the key set from the previous record of the same kind. The `author` value must be exactly `Claude Opus 5.5 (engineering lead, cand-d author)` (the declaration's `author`), and `reviewer` must differ from it.
   - If the version 5 records are stubs left by a dead session, delete them and rerun the reviewers fresh.
2. **Commit both review records** with explicit paths (`git commit -- <paths>`), before any evaluation.
3. **Official run**, from a clean tree:
   ```sh
   tools/zig-toolchain.sh                  # once: download and verify the pinned Zig 0.17.0
   rm -rf zig-out && tools/zig build -Doptimize=ReleaseSafe
   REV=$(git rev-parse --short HEAD)
   zig-out/bin/kinigami-gate1 results/gates/gate1-v1/run<k>-$REV-ReleaseSafe.json \
       candidates/cand-a candidates/cand-b candidates/cand-c candidates/cand-d
   jq '.working_tree_dirty' results/gates/gate1-v1/run<k>-$REV-ReleaseSafe.json   # must be false
   ```
   The next run is **run 10**. Never use a system or Homebrew `zig`.
4. **Record the run** in `results/gates/gate1-v1/README.md` (same table format as runs 6–9) and in a disposition decision record. Commit the report JSON with them.
5. If G6 (or anything else) is not `pass`:
   - read the review's "what a further version would need" section;
   - write a revision decision record (Q-number) mapping each item to a change, **commit it alone first**;
   - preserve the current declaration as `candidates/cand-d/declaration-v<N>.json` (a plain copy: `git show HEAD:candidates/cand-d/declaration.json > ...`; **do not** use `git mv`, see §6);
   - edit the scripts, regenerate, write `dossier-v<N+1>.md`, check the draft with the evaluator, and commit the candidate;
   - go back to step 1.
6. When a run gives cand-d `pass` on G1–G8:
   - record it and its disposition;
   - update `docs/roadmap.md` (R9 status; R10 unblocks) and `docs/traceability.md` if affected;
   - push, and open a PR. The PR body ends with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`, or your own tool's attribution line if you are not Claude Code.

The required order is decision → candidate → reviews → evaluation, and it must be provable from `git log`.

## 4. How the candidate is built (scripts are the source of truth)

```sh
cd candidates/cand-d/scripts
python3 declaration_text.py           # prose fields -> declaration_text.json
python3 gen_declaration.py            # checks: box overlap (SAT, 1 um erosion), containment, mass, COM, power
python3 gen_declaration.py --write    # writes ../declaration.json (bump "candidate_version" in this script per version)
python3 coupler.py                    # every coupler number; ASSERTS each claimed margin (exit 1 = a claim broke)
python3 joint.py                      # joint range, sector sweep, torque
```

- Every number in the declaration prose (`declaration_text.py`) must come from `coupler.py` or `joint.py` output. After any change, re-run and update the prose. Stale numbers are what reviewers catch.
- Draft evaluator check: copy `declaration.json` into a scratch directory named `cand-d/` and run `zig-out/bin/kinigami-gate1 /tmp/r.json /tmp/x/cand-d`. G1–G5 must pass, and G6–G8 will read `review_record_missing`.
- Keep the stowed sphere (G1) under 60 mm with margin. It is 59.133 mm now. The stud tip and the head front corners set it, so do not lengthen the stud or the body.

## 5. Brief to give each retention reviewer (adapt N)

> You are an INDEPENDENT reviewer with no authorship in cand-d. Strict, honest paper judgement; a wrong pass is worse than a wrong fail. Write ONLY `candidates/cand-d/retention-review-v<N>-r1.md` (write the header early, update as you go; do not commit). Read:
> - AGENTS.md;
> - the protocol §8;
> - Q062, Q031 (item 6), Q036, Q085 and the latest revision decision;
> - CPL-001..011;
> - the declaration, the latest dossier and the scripts (run them);
> - the previous retention review, checking each of its open items.
>
> Recompute key numbers yourself, and check the cited sources in raw form (curl and grep, or pdftotext). `pass` only if every declared load and every alignment means is physically justified on paper. A contradiction is `fail`; an unsupported claim is `unresolved`. Gate 2/3 matters alone do not block. Do not raise or lower the protocol's bar.
>
> Header lines: `candidate_id`, `candidate_version`, `author: Claude Opus 5.5 (engineering lead, cand-d author)`, `reviewer: <your id>`, `outcome`. Then the SHA-256 of the declaration, files read, recomputation table, status of the prior items, findings per means, errors, classification, what a further version needs, and the basis of the outcome.

The originality brief is similar, per Q61. The header keys are `candidate_id`, `candidate_version`, `declaration_sha256`, `stage: gate1`, `author`, `reviewer`, `high_cells_f1_f2`, `exclusion_cube_with_internal_flywheel`, `exclusion_needle_or_particle_silhouette` and `outcome`. Ask for primary sources read for every moderate or high cell.

## 6. Rules learned the hard way (keep them)

- **Check every cited number in raw source text** (`curl` + `grep`, or `pdftotext`). A page-summarising fetch tool once produced a value that was not on the page (Q86).
- **Compute at the physical contact point.** Lash at the wrong radius was a lead error (Q90). So was a fallback argument that covered pitch but not roll and yaw (Q92). Check every degree of freedom.
- **Commit with explicit paths.** `git commit -- <paths>`, after `git add` for new files. A staged `git mv` once rode along in a decision commit (Q87/e4ec1cb). Never amend, rebase or force-push.
- **No thread in PA12** anywhere in a load path: use 304 nut blocks or tapped 304 parts, with countersunk screws. PA12 sees bearing only (Materialise PA12 SLS tensile strength 48 MPa).
- **Packaging rule (G2):** component boxes must not overlap after the 1 µm erosion, and each box must lie inside one cavity primitive. Meshing gears are bounded at their pitch circles, shafts in bores are boxed with the bore part, and clips are lumped boxes. Say so in the descriptions.
- **Preserve each version** as `declaration-v<N>.json`, and keep its dossier and reviews.
- **Regression gates must stay green.** Run `tools/zig build test` (exit 0; the suite prints diagnostics and "failed command" lines on stderr, but the exit code is what counts) and `tools/check-core-purity.sh`. The solver and criteria are untouched by candidate work.
- **Branches** are `feat/...` or `docs/...` with no phase names. Use Conventional Commits. You may merge your own PR once tests pass.

## 7. Current risks to watch in the v5 review

- PTFE film on the head teeth must not reach the cam flank. Self-locking needs μ > 0.0524.
- Aluminium bronze C95400 is treated as "bronze" for the cited lead-screw friction rows.
- The release margin is 1.25 at the 3.75 V cell rule. The roll-flattening margin is 1.27 at the guaranteed lower-bound motor torque.
- The motor-clip bond strength is for steel pins; the gearhead housing material is unknown.
- The tail stud screws are hex-socket countersunk M1.6, a non-standard size.
- The yaw residual (0.69 deg) is absorbed by the lock stage: seat window ±0.140 against ±0.20.

If a reviewer finds a new blocker, fix it in v6 the same way. All fixes so far stayed inside the 60 mm envelope.
