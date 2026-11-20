# Kinigami Graft report

## Take 1 — independent v5 retention review

| Field | Record |
|---|---|
| Graft | `retention-v5`, 404khai/kinigami, no worktrees |
| Base | `2ac0a54d6615d915bd22aa85538355b3e237187a` |
| Date / reviewer | 2026-11-20, Devin session 6cb7e8cd7acb4fd9b77647e4006f0b41 (no cand-d authorship) |
| Assignment | Paper review of G6 under Gate 1 protocol §8; no official run or candidate changes |
| Only Graft delta | `candidates/cand-d/retention-review-v5-r1.md` (untracked by design) |
| Verdict | **fail**. The 4.10 mm bore of the ejection collar cannot fit the declared 7.00 mm tube. Neither a mounting land nor another axial support is defined. |
| Open independently of the fail | Adverse-pose seating through the cam transition, tilted-ring seat depth, motor variation under fixed external release load, and applicability of the gearhead-bond data. |
| Final state | Review complete; clean tracked declaration, criteria and scripts. Nothing committed, pushed, integrated or proposed as a PR. No official evaluation. |

### Setup and checks

Commands below use the release binary's directory on PATH. The report, source downloads, source-text regeneration and independent Python arithmetic stayed outside the Graft.

```sh
# From the Root checkout at the stated commit
tools/zig-toolchain.sh
# GitHub release: 404khai/graft v0.2.0, verified local Linux x86_64 archive
# From the archive download directory:
sha256sum -c graft-0.2.0-x86_64-unknown-linux-gnu.tar.gz.sha256
gh attestation verify graft-0.2.0-x86_64-unknown-linux-gnu.tar.gz --repo 404khai/graft

# From the Root
graft init
graft new retention-v5 --from 2ac0a54 --clone-ignored .toolchain
cd "$(graft path retention-v5)"
git rev-parse HEAD
sha256sum candidates/cand-d/declaration.json criteria/gates/gate1-v1.json
p=candidates/cand-d/scripts
# Run the text generator on a scratch copy (it writes beside itself).
python3 ~/Documents/retention-sources/textgen/declaration_text.py
cmp ~/Documents/retention-sources/textgen/declaration_text.json "$p/declaration_text.json"
python3 "$p/gen_declaration.py"     # no --write
python3 "$p/coupler.py"
python3 "$p/joint.py"
python3 ~/Documents/retention-sources/rc.py candidates/cand-d/declaration.json
git diff --exit-code
git status --short --untracked-files=all
```

Pinned Zig 0.17.0; Graft archive SHA-256 `d8450bb807db14cdb8e2b0ad925f78c143c84accf4605a4d17526004cfcc7c86`, with release provenance verified. The binary warned about weak GLIBC_2.39 but both Graft operations succeeded. ext4 lacked reflinks: Graft used copies for the 294 base files and 19,507 toolchain files. No fallback to worktrees.

Declaration SHA-256 `c6baa8dcfbd3de4c5c3ed06fbb9b9d7dfcb1a8cd90738b737816a05736b8897d`; criteria SHA-256 `ffe135329340ca7d3f630a1f14c0dd91616d8ab91e64f0985585eeabb532ddbf`. Scratch text regeneration matched. Generator indicated no box interference across 1,081 pairs; the coupler and joint scripts completed. These are author checks, not an official gate verdict. The review distinguishes reproduced calculations from assumptions and the release fit contradiction.

Raw source checks used HTTP downloads and text extraction/grep; Python pypdf substituted for unavailable pdftotext. Original 3M PDF returned 403; an alternate copy of the manufacturer's TF 1620 sheet confirmed its specific gravity. KHK's web table provided the gear-efficiency range when PDF extraction was incomplete. No further review work is pending in this Graft.


## Take 2 — originality-v5

**Purpose:** independent Gate 1 paper review of cand-d version 5 (G7/G8), 2026-11-20. Reviewer session a03633b0b82544c8a07ac3abf0a68c19. Single reviewer graft; no worktrees or candidate changes. This is a separate take for the lead to combine, not a repository file.

| Field | Record |
|---|---|
| Base | `2ac0a54d6615d915bd22aa85538355b3e237187a` in 404khai/kinigami |
| Graft | `originality-v5`; new from the base, with the ignored verified Zig toolchain copied |
| CLI | [Graft v0.2.0 Linux x86_64 GNU release](https://github.com/404khai/graft/releases/tag/v0.2.0). Compared archive SHA-256 against the release checksum: `d8450bb807db14cdb8e2b0ad925f78c143c84accf4605a4d17526004cfcc7c86`. No independent attestation verification claimed. |
| Root vs graft | Both HEADs equal the base. Root clean; only untracked file in graft: `candidates/cand-d/originality-review-gate1-v5-r1.md`. No commit, push, integration or PR. |
| Result | Q61 paper **pass**, 91 references/rows, 455 dimension assessments, 54 moderate, one high (Beckhoff D2), zero F1/F2 high. Exclusions absent. No G6 finding or official run. |
| Declaration SHA-256 | `c6baa8dcfbd3de4c5c3ed06fbb9b9d7dfcb1a8cd90738b737816a05736b8897d` (unchanged) |
| Review file SHA-256 | `6a4b62490a40fea3cdf0d0c9c21c02e8f57b89d141e26d96df86a703d3c317fd` |

**Commands** (locations simplified; release binary directory on PATH for the Graft calls):

```sh
# In the release download directory
sha256sum -c graft-0.2.0-x86_64-unknown-linux-gnu.tar.gz.sha256
graft --version

# In the existing kinigami checkout
tools/zig-toolchain.sh
git rev-parse HEAD
graft init
graft new originality-v5 --from 2ac0a54 --clone-ignored .toolchain
graft ls
cd "$(graft path originality-v5)"
git rev-parse HEAD
sha256sum candidates/cand-d/declaration.json
cd candidates/cand-d/scripts
python -B coupler.py
python -B joint.py
python -B gen_declaration.py              # diagnostics only; no --write
```

**Review and verification.** Compared declaration/dossier, v4 records, decisions, registered criteria/protocol/corpus and primary reference material. The three diagnostic scripts completed; they locate features, not an official evaluation. Constructed the Q61 record from reviewer notes stored outside the graft. Audited five reasoned and linked cells per row, coverage of every fixed ID, high-cell counts and the unique evaluator keys against the declaration hash/author/version; checked `git status --porcelain` separately in the root and graft.

**Problems:** the release CLI printed a missing weak GLIBC_2.39 version warning but completed init, new, path and list. No toolchain change or build workaround needed. Several publisher downloads failed or timed out; used author-hosted copies, dissertations, DFKI’s live host, indexed primary passages, and the TYCOON authors’ supplemental footage as detailed in the review. No claim of fresh full-text reading for all non-close corpus entries. Official clean-tree evaluation and any landing are for the lead, not this reviewer.
