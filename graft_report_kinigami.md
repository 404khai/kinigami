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

## Take 3 — v6 servo packaging

Assigned to session 25f599250d1141f7a2e9cdd1666469fb, separate `pkg-v6` graft from Q95 (`b8f389b`). Scope: servo/cell/converter layout, geometry generator, mount and fasteners. This assignment is not yet a verified result.

Generator returned. The lead incorporated it in the Take 5 graft and added the new cartridge geometry and captive 304 base nuts. On the resulting **work-in-progress** input, the registered evaluator in scratch reported 58.920 mm, no overlap in 1540 pairs, 40.244 g and 7184 / 26640 mW; G1–G5 passed. This was not an official run or a G6 review.

## Take 4 — v6 cam, preload and release calculation

Assigned to session 709fe37ba624478793647aa3272fb91b, separate `mech-v6` graft from the same Q95. Scope: seating, passive retention, bounded release, spring and load cases. This assignment is not yet a verified result.

## Take 5 — v6 thrust support and drive interface

Lead session f83105eb20a94fb3b9ce36f2d6260868: `graft init`, `graft new rear-thrust-v6 --from b8f389b --clone-ignored .toolchain`, `graft ls`, `graft path rear-thrust-v6`. CLI 0.2.0; ext4 copied instead of reflinking (480.4 MiB), and the weak GLIBC_2.39 warning did not prevent creation. The exact v5 declaration was archived from Git. No worktrees or squash integration. Design in progress; no v6 judgement.

## Take 6 — compare rated servo alternatives, before candidate freeze

Reuse the separate Take 3 packaging graft for a source/dimensional study,
not a new candidate or official run. Compare FEETECH SCS0037/SCS0043
manufacturer ratings and drawings against the revised bearing loads and
actual package. Do not credit a market listing or a stall value as a
moving torque. No new servo implementation before the revision decision.

Take 6 outcome: both alternative drives are rated 49.03 N·mm at 4.8 V. SCS0043 is deeper with no advantage at that rail. After Q96 the packaging graft placed the SCS0037 into a lowered-axis steel cassette; the lead combined its generator with the Take 4 contact analysis and Take 5 H900 cross-dowel cartridge. The final scratch input is 59.357 mm / 45.541 g. Correcting the tool-port projection and preserving all one-sided service loads gives 86.19 dry / 99.13 mixed N·mm breakaway. There is no supported bounded independent release in v6. The 176.5 N·mm catalogue stall point is a **fault diagnostic only**.

## Takes 7 and 8 — frozen v6 reviews

Independent retention and originality sessions will inspect immutable v6 in separate Grafts. They do not author candidate files and receive no requested verdict. The next official result must be from a clean tree after both review records have been committed.

Take 6 source appendix: [package study](docs/studies/cand-d-v6-package.md), including cropped-case limits, diagonal flange screws, side braces, regulator overhead and bench access. The 44.783 g trial included an 8.2 g placeholder. Only the integrated dossier's 45.541 g is the v6 Gate 1 input. After candidate freeze, the independent code review found that the clipped motor envelope was not centred on its bearing axis. The sweep now uses the sector orientation; a 4 μm witness at (0.039,7.999) in the omitted sliver is correctly detected. Frozen declaration bytes unchanged.

## Take 9 — successor load-path study (not a candidate)

Reuse the Take 4 mechanics Graft, no changes to v6. A directly mated M4×0.5 screw fails to establish a robust preload/reverse window: an example face clutch slips at 6.69–10.95 N·mm vs a required 8.27–9.42 even before one-sector bearing, yaw and failed-start cases. A direct radial scroll removes the long trapped pilot but needs 89.9 N·mm closing under adverse yaw and 49.5 opening even with an assumed 2.5 mm arm, zero trapped preload and 46 g service load. At an adverse 0.5 mm partial arm those estimates reach 333 / 144. These are conditional sizing bounds, not physical stall measurements. Study alternatives with a fixed internal screw, separated centring faces and positively retracting jaws before deciding on another revision.

## Take 10 — successor drive and access study (not a candidate)

Reuse the Take 3 package Graft. Check a supported 4:1 epicyclic versus a permanently engaged single internal screw, not a threaded mating face. Verify the actuated assembly, sensors, loaded thrust support and opening travel against the actual cell, board and end plate; do not use the 60 mm envelope alone as a fit certificate. No new candidate generated by this study.
