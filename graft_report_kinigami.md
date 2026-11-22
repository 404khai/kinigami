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

## Take 7 — independent v6 G6 retention and pre-alignment review

| Field | Record |
|---|---|
| Graft and base | Fresh `retention-v6` from `bf5af8ab2082fd6ef4c7a77e1753b78c32c42ecf`; target branch `feat/cand-d-coupler-first` |
| Reviewer | 2026-11-20, Devin 6cb7e8cd7acb4fd9b77647e4006f0b41; independent of all three v6 design sessions |
| Scope and only Graft delta | `candidates/cand-d/retention-review-v6-r1.md`, SHA-256 `44982f7fc1211042aae12084758578b9b7f6d20a8b394c230704f7babac73c2f`; external report and scratch calculations are not candidate changes |
| Input integrity | Declaration SHA-256 `620b7fafc2ec1cf4c9ebb4708eeee6e22578eed0ba4190df9c3ab6d9262c944b`; criteria `ffe135329340ca7d3f630a1f14c0dd91616d8ab91e64f0985585eeabb532ddbf` |
| Review | **Fail, exploratory.** The new cross-pinned collar fits on paper. The head's rated torque is 49.03 N·mm; one-lug dry and mixed-friction estimates are 86.19 and 99.13. On steep ejection the guide-drag feedback exceeds one. The explicit false release bound contradicts §8 check 2. This does not prove every physical unit jams. |
| Other limits | Worst combined roll/pitch/yaw draw budget −6.25 N; nominal line contact 384 MPa vs 369 MPa provisional onset. No evidence of physical damage, autonomous capture, or full correction. |
| Closeout | Complete; no pending reviewer action. Tracked files unchanged. No worktree, integration, commit, push, PR, candidate implementation changes or official gate run. |

### Commands and evidence

From the existing registered Kinigami Root (`graft init` was already completed in Take 1):
```sh
git fetch origin feat/cand-d-coupler-first
git rev-parse FETCH_HEAD
tools/zig-toolchain.sh
graft new retention-v6 --from bf5af8a --clone-ignored .toolchain
cd "$(graft path retention-v6)"
git rev-parse HEAD
tools/zig version                   # 0.17.0 from the cloned pinned toolchain
sha256sum candidates/cand-d/declaration.json criteria/gates/gate1-v1.json
p=candidates/cand-d/scripts
a=~/Documents/retention-audit-v6
# Text generator writes beside itself, so run its copy outside the Graft.
python3 "$a/declaration_text.py"
cmp "$a/declaration_text.json" "$p/declaration_text.json"
python3 "$p/gen_declaration.py"     # read-only; never --write
python3 "$p/joint.py"
python3 "$p/rear_drive.py"
python3 "$p/coupler.py"
python3 "$p/coupler.py" --q96-only
python3 "$a/recompute.py" candidates/cand-d/declaration.json
git diff --exit-code
git status --short --untracked-files=all
```

Used the same verified Graft v0.2.0 binary as Take 1. The weak GLIBC_2.39 warning did not prevent creation; ext4 lacks reflinks so Graft used its copy backend, including the pinned compiler. Both FETCH_HEAD and Graft HEAD matched the required commit. Reviewer scratch stayed outside the Graft; the two incidental Python bytecode files created by importing modules were moved there as well. The only status entry is the requested untracked review. The frozen prose regeneration matched, the scripts completed, and the generator reported 2,145 clear pairs. This is not a repeat of the gate evaluator.

For independent arithmetic, the scratch calculation reads declaration masses and box centres and imports no candidate modules. It rebuilt shallow/steep slopes, clock/seat and collar tolerance sums, pin bending/shear, fixed loads, single-lug breakaway and journal/guide feedback. For raw sources, used HTTP responses, PDF text extraction (pypdf), parsed HTML and the original FEETECH p6 figure. FEETECH and Gibbs retries succeeded: SCS0037 PDF SHA-256 `eb8cae5967c52740afd33b7f196d70d4bff2481a43ad279f2d5375098c22e822`. Fresh leadscrew/IT and Vishay requests returned 403; prior raw copies were available. Material/servo values were checked separately from their applicability to the assembly. The frozen candidate and the registered criteria were not changed to produce the result.

Take numbering is the dispatcher's merged sequence. This reviewer supplied Takes 1 and 7; other reviewers' takes are not recreated here.
## Take 8 — originality-v6

2026-11-20 · Independent paper originality review; no design authorship. Reviewer session a03633b0b82544c8a07ac3abf0a68c19. Take number assigned by lead. The previous local Take 1 above was aggregated as Take 2 in the main project report.

| Item | Record |
|---|---|
| Frozen revision | `bf5af8ab2082fd6ef4c7a77e1753b78c32c42ecf`, fetched from `origin/feat/cand-d-coupler-first` into FETCH_HEAD; root working branch and its HEAD were not switched. |
| Graft | Fresh `originality-v6`, from `bf5af8a`, with ignored pinned Zig toolchain copied. Graft v0.2.0 previously checksum-verified. |
| Input | SHA-256 `620b7fafc2ec1cf4c9ebb4708eeee6e22578eed0ba4190df9c3ab6d9262c944b` before/after; v6 lineage author preserved. |
| Scope | Q61, Q62, protocol rev. 1, handoff, registered corpus and additional primary-source search; new full five-dimensional matrix, no candidate or criteria edits. |
| Result | Q61 paper **pass**: 104 reference rows, 520 cells, three high comparisons (all D2 against distinct non-fictional designs: Beckhoff ATRO, TYCOON, US6226068B1 spring-driven bayonet). None against F1/F2; neither exclusion present. No official evaluation or G6 conclusion. |
| Graft delta | Only untracked `candidates/cand-d/originality-review-gate1-v6-r1.md`; SHA-256 `612b16014bdd6d421eb750beb2fe9e728507572a26d0a149ca51651a3a9a415a`. Root working tree clean at `2ac0a54d6615d915bd22aa85538355b3e237187a`. No worktree, graft integrate, commit, push or PR. |

Commands (graft release binary shown as `graft`; diagnostics are nonwriting):
```sh
git fetch origin feat/cand-d-coupler-first
git rev-parse FETCH_HEAD
tools/zig-toolchain.sh
graft new originality-v6 --from bf5af8a --clone-ignored .toolchain
cd "$(graft path originality-v6)"
git rev-parse HEAD
sha256sum candidates/cand-d/declaration.json
cd candidates/cand-d/scripts
python -B joint.py
python -B gen_declaration.py
python -B rear_drive.py
python -B coupler.py --q96-only
```
Verified root and graft status separately via `git status --porcelain`. Checked fixed corpus IDs, references/locators for all moderate and high cells, five linked and reasoned ratings per row, unique parser fields, input hash and lineage author. All search/assembly notes lived outside the graft.

**Problems / limits:** weak GLIBC_2.39 warning and no filesystem reflinks; Graft nevertheless completed its copy, including .toolchain. Reused primary material from the reviewer's evidence archive and added fresh retrievals/searches. Restricted publisher copies (especially TYCOON) were checked via actual indexed primary passages, author material and mirrors; specific limitations are in the review. No final visuals or prototype; no official gate run.

## Take 9 — successor load-path study (not a candidate)

Reuse the Take 4 mechanics Graft, no changes to v6. A directly mated M4×0.5 screw fails to establish a robust preload/reverse window: an example face clutch slips at 6.69–10.95 N·mm vs a required 8.27–9.42 even before one-sector bearing, yaw and failed-start cases. A direct radial scroll removes the long trapped pilot but needs 89.9 N·mm closing under adverse yaw and 49.5 opening even with an assumed 2.5 mm arm, zero trapped preload and 46 g service load. At an adverse 0.5 mm partial arm those estimates reach 333 / 144. These are conditional sizing bounds, not physical stall measurements. Study alternatives with a fixed internal screw, separated centring faces and positively retracting jaws before deciding on another revision.

**Take 9 result.** [Working-load and overload study](docs/studies/cand-d-internal-screw/mechanics.md) and [source](docs/studies/cand-d-internal-screw/take9.py). At 50 g the proposed detent has only 2.3 N between the 103.8 N working demand and 106.1 N minimum release threshold. Seizing a roller raises modeled breakout from 121.0 to 182.4 N. A real force band, positive reset and protected thread are missing. A six-contact equilibrium defeats a clearance-only proof; positive face separation remains open. No candidate edits.

## Take 10 — successor drive and access study (not a candidate)

Reuse the Take 3 package Graft. Check a supported 4:1 epicyclic versus a permanently engaged single internal screw, not a threaded mating face. Verify the actuated assembly, sensors, loaded thrust support and opening travel against the actual cell, board and end plate; do not use the 60 mm envelope alone as a fit certificate. No new candidate generated by this study.

**Take 10 result — retained section, not a freeze.** The [drive/access study](docs/studies/cand-d-internal-screw/package.md) and [script](docs/studies/cand-d-internal-screw/drive_stack.py) replace the earlier 1.10 mm stroke hypothesis. The opposed races, moving nut through the front race and +0.80 mm metal nose give 3.530 mm guaranteed stroke and 59.762 mm containing diameter for the listed parts. The simple one-jaw pin/bridge section fails its bending screens. No hidden use of the tail PCB cavity: the external cassette changes pitch to 50.8 mm. At 46 g the projected allowance for tail, ejector, bidirectional overload mechanism and sensing together is only 2.28 g, not a mass criterion. Reused the package Graft; no additional candidate declaration or gate run.

**Lead synthesis (same rear-thrust-v6 Graft):** [Q98](docs/decisions/Q098-cand-d-internal-screw-study.md) holds the design. The [six-contact witness](docs/studies/cand-d-internal-screw/clearance_witness.py) also shows why dropping preload in favour of deliberate clearance does not by itself bound the one-jaw reaction. The model balances nonzero internal forces at zero external wrench. It is not proof a physical unit jams. Full studies, sources and next discriminating measurements are [here](docs/studies/cand-d-internal-screw/README.md).

## Take 11 — six-coordinate retention and release

New independent-of-packaging design Graft for the Take 4/9 mechanics author, based on 96fcfeb. Q99 replaces the Q98 seven-normal preload clamp with six bilateral, individually clearanced pole constraints. Test the frictional wrench bound, edge transitions and partials, not just the rank of a nominal matrix. This designer cannot independently review v7.

**Take 11 result:** `graft new exact-pairs-v7 --from 96fcfeb --clone-ignored .toolchain` (weak GLIBC warning, ext4 file copies). [Follow-on edge atlas](docs/studies/cand-d-exact-pairs/mechanics.md), not frozen v7: a *longer* cheek, outward-free blade and bounded guide reactions admit a finite mixed-edge bound. With lateral travel around the rim, the resulting 50 g sufficient ejector budget exceeds 9.90 N. Neither that cheek nor the free-leading blade is established by the frozen declaration.

## Take 12 — shutter and positive stripper package

New packaging Graft from 96fcfeb, Take 3/10 design author. Size the output mechanism, captive drive, blade and stripper stroke, assembly access, package bounds and fault loads; no transfer of the Q98 screw result to this topology.

**Take 12 result:** `graft new shutter-v7 --from 96fcfeb --clone-ignored .toolchain` (copy fallback). [Final section including independent pad option](docs/studies/cand-d-shutter/shutter-take12.md). Driving each pad separately at its own lane improves the provisional rated budget from 1.20 N to 4.39 N, still not enough to credit all loaded exits. The 41.824 g subtotal omits guides, sensing and other hardware and is not v7's declared mass.

## Take 13 — integrate six-coordinate shutter and QA

Lead's fresh `reciprocal-v7` Graft from 96fcfeb with ignored pinned toolchain. Graft v0.2.0 copied 318 tracked files and 19,507 toolchain files on ext4; the GLIBC weak-version warning was nonfatal. Q99 precedes the v7 declaration. Archive v6 verbatim (SHA-256 `620b7fafc2ec1cf4c9ebb4708eeee6e22578eed0ba4190df9c3ab6d9262c944b`). No pass before a clean official run.

Take 11 bounded all flat pole normals (including partial subsets, no equal sharing) at R4.65. Residual: edges and guide drag. Take 12's initial fork sweep and common barrel stripper pass their nominal travel checks, but the opposite-pad torque budget fails. Take 13 freezes that actual section, not the *proposed* separate pickup, spring ejectors or three independently driven strippers. Full dossier and separate scripts carry the numerical assumptions and failures. The branch retains Q85: a clearance trial is a recorded deficiency, not a new rule allowing free play.

## Take 14 — frozen v7 independent retention review

Dedicated reviewer Graft from the immutable v7 candidate commit. Review only; no candidate authorship, candidate edits or evaluator changes.

**Take 14 result.** [Retention review](candidates/cand-d/retention-review-v7-r1.md), Graft `take14-retention-v7`, session `f9ea685b9da04d208a10ab16b5d387d2`. At frozen `a82f52c`, independent reproduction and hashes matched, and pinned Zig tests and purity exited 0. G6 **fail**: 1.20 N available in the adverse one-pad case versus 2.45 N needed before internal drag. No candidate edits, commit or official evaluation by the reviewer.

## Take 15 — frozen v7 independent originality review

Separate reviewer Graft from the immutable v7 candidate commit. Q61 corpus, searches and full matrix; no candidate authorship, candidate edits or evaluator changes.

**Take 15 result.** [Fresh Q61 review](candidates/cand-d/originality-review-gate1-v7-r1.md), Graft `originality-v7`, session `742431beae9f465fabd47886a57ac982`. At `a82f52c` the reviewer checked the frozen declaration hash, 126 references, the search log and full five-dimension matrix. Outcome **pass**: six non-fictional highs; no reference high on two dimensions, no F1/F2 high, neither exclusion present. No candidate edits, commit or official evaluation by the reviewer.

## Take 16 — direct drawbolt reaction study

After v7 freeze, fresh `drawbolt-load-study` Graft at a82f52c, mechanics author. Study the *mating* thread instead of the earlier internal screw and retractable jaws. Require actual preload bounds, transverse isolation, thread-end and independent final release. Not part of v7 or its reviews.

## Take 17 — blind-mate drawbolt stack

After v7 freeze, fresh `drawbolt-stack-study` Graft at a82f52c, packaging author. Study actual nut, bearing, runout, sensing, side-load and recovery envelopes. Not a candidate change or an amendment to Q99.

Take 16 direct mating draw study: [source and limits](docs/studies/cand-d-drawbolt/direct.md). Complete flanks can carry preload with rated drive; a tensile 4W remains as the last flank loses its area. Take 13 lead compared [internal screw torque, packaging and edge pressure](docs/studies/cand-d-drawbolt/README.md); no successor is declared.

**Take 16 result:** the [barrel](docs/studies/cand-d-drawbolt/barrel.md) runs off its smooth patch during ordinary partial pitch. [Larger-sphere study](docs/studies/cand-d-drawbolt/cylinders.md): removing one keeper admits 12° where the guided-coupon force budget assumes ≤3°. Neither is a free-release result.

**Take 17 result:** the [linear, rotary and swinging sections](docs/studies/cand-d-drawbolt/drawbolt-take17.md) retain separate dimensions and force budgets. The long screw exceeds the face by 4.07 mm; the short rise exceeds rated torque. A pivot removes a guide but hits the existing rim. The lead's [guard calculation](docs/studies/cand-d-drawbolt/swing.py) does not change that geometry or authorize a freeze.

## Take 18 — central gripper force and release

A fresh `central-grasp-study` Graft from e6b51f9 (mechanics author). Study one central sphere between actively opened jaws; separate capture from three outward-opening bearing seats. No frozen revision or gate result.

The [mechanics study](docs/studies/cand-d-central-grasp/grasp.md) gives a measured-draw window and a zero-tilt one-jaw contact at the open stop. The [thin slot/comb study](docs/studies/cand-d-central-grasp/grille.md) distinguishes fully parked clearance from off-axis side loads during withdrawal. Neither free lead, backed transition nor unconstrained ejection has a complete installed proof.

## Take 19 — central gripper and ejection package

A separate `central-drive-package` Graft from e6b51f9 (packaging author). Check actual drive, jaw take-up, independent push, sensing and access against 60 mm. No candidate edit or official evaluation.

The [package section](docs/studies/cand-d-central-grasp/central-drive-take19.md) keeps a rear-running ejector screw but rejects the original high shaft: the two critical features span 60.194 mm before the rest of the unit. The wider slotted hex needs 4.531 mm radial stroke before cage motion. Neither that package nor the conditional force result is a Gate 1 design.

Follow-up in the same Graft: the [revised rear drive](docs/studies/cand-d-central-grasp/central-drive-rear19.md) intersects the retained joint motor. Four points in the proposed stock alone require a containing diameter of at least 60.939 mm; this rejects that package, not Q12.

## Take 20 — local vacuum transfer package

`vacuum-pose-hold` Graft from c750e18 with the pinned toolchain. [Section and gas/drive budgets](docs/studies/cand-d-pressure-transfer/vacuum-take20.md), [calculator](docs/studies/cand-d-pressure-transfer/vacuum-take20.py). A single stroke can provide the modelled differential for a finite interval. The return shaft collides with the joint motor and the slow cycle needs a tight leak bound. No external air or unpowered structural credit.

## Take 21 — load transfer to an inverted T-bar

`vacuum-fork-study` Graft from c750e18 with the pinned toolchain. [Two-foot latch and load-transfer analysis](docs/studies/cand-d-pressure-transfer/vacuum-fork.md), [calculator](docs/studies/cand-d-pressure-transfer/vacuum-fork.py). The local six-seat calculation has positive reserve with an intact, qualified seal. After the latch aligns with the exit slot, sudden venting leaves no tensile carrier. Distinct from Take 20; the budgets do not certify a single integrated design. No candidate change, review or official run.

## Take 22 — positively retracting button and passive cup

`retracting-button-study` Graft, mechanics author. Test a p5-backed tail against a finite male-nose port, including moving and parked contacts, unilateral button draw, the cut lip and an actual working crown. Do not carry an intact vacuum seal or a nominal centred contact into this study.

## Take 23 — expanding-plug drive and blind receiver

`expanding-plug-drive` Graft from c750e18, package author. Study a mechanically metered cartridge, separate retracting shoes, six alternating V and lock sites, actual swept volume and terminal ejection. Related calculations in the lead integration Graft: [crown](docs/studies/cand-d-expanding-plug/crown.py) and [individual seat loads](docs/studies/cand-d-expanding-plug/supported.py). No replacement candidate has been authorized.

**Take 22 result:** the [finite-collar proof](docs/studies/cand-d-expanding-plug/button.md) shields the cut lip; the last moving contact is still a small-radius blend, not the seated crown. Test the individual port, do not freeze a candidate.

**Take 23 result:** the [drive section](docs/studies/cand-d-expanding-plug/plug-drive-take23.md) has a 0.271 mm lock-land interference, a shared motor/floor volume and no unobstructed grid or split-ring strip. A 66.17 mm two-feature lower bound rejects the proposed aft-floor fix, not the 60 mm class.

## Take 24 — inward buttons around a single tail bulb

Fresh mechanics Graft: reverse the radial direction of the port and replace the costly outer torus with one centrally mounted, rounded mushroom. Check its actual rolling radius, locked and moving contact stresses and finite funnel clearances; do not import Take 22's outer-nose proof.

## Take 25 — central bulb, head-side push and package

Separate packaging Graft: size the passive bulb, powered take-up and central ejector without the Take 23 blind floor. Verify stock and deployment in a mechanically achievable stowed pose; no assumption that changing the pitch solves Q12.

**Take 24 result:** [central bulb and moving bowl](docs/studies/cand-d-inward-bulb/README.md): a Ø24.96 section admits the six working flanks and three rear pads. The deep park clears the local moving wall; the 731 N guide-reaction screen makes the original short straight guide unacceptable without a start-friction bound.

**Take 25 result:** [common cam and terminal study](docs/studies/cand-d-inward-bulb/bulb-drive-take25.py): the long terminal exceeds 60 mm even folded to 15°. The shorter ring collides with the side-wall servo or cell at every clocking in the studied arrangement. Do not treat the two layouts as one.

## Take 26 — integrate the inward bulb, wrench and rocker studies

Lead integration in the `reciprocal-v7` Graft, alongside the existing Take 24/25 mechanics and drive Grafts. [Wrench and force-point certificates](docs/studies/cand-d-inward-bulb/README.md): checked a nine-contact equilibrium with one rear pad unloaded, then recomputed the R18 tangential rocker with independent uncertainties and full friction disks. At 90 g, 32±.8 N per nose, the worst table reserve is 1.800 N in the frictionless existence proof; the frictional strength screen allows a single shoe to carry 192.064 N summed normal force. No v8, review or official result follows from this screen.

**Take 26 follow-up:** [finite swing](docs/studies/cand-d-inward-bulb/mushroom.md) and [bevel package](docs/studies/cand-d-inward-bulb/bulb-drive-take25.py). The 0.02979 opening coefficient cannot bound a partly supported shoe at the light-lead force while the 32 N closure is still applied. Even moving the motors behind the arm leaves the supported axle 0.723 mm inside the next motor. At 35 mm pitch a fixed guide rim and an actual opposite tail ball span 60.268 mm at the shorter 4 mm stroke, independent of chosen sphere centre. Retire this package, not all central bulbs.

## Take 27 — transverse vise surface and paddle

Separate mechanics Graft: replace the stud's undercut, moving buttons and ports with a metal paddle between two transverse jaws. Investigate finite V-groove and paddle faces, sweep, neck, last contact and ejection, including free tilt. Exploratory, not a candidate.

## Take 28 — one platen and positive ejector

Separate packaging Graft: size one transversely driven platen, the opposite fixed jaw and an axial head pusher within the complete stowed unit, including actual structural and electrical components. No credit for the bulb's bearings or actuator positions.

## Take 29 — seated support and release force for the transverse vise

Lead integration in the reciprocal-v7 Graft: test the six V faces and upper pad as a new three-dimensional load path. Distinguish existence of equilibrium, incomplete seating and partial-release force; no universal 60 mm inference.

## Take 30 — integrate the articulated body and adjacent-unit sweep

Lead (reciprocal-v7 Graft), in parallel with the separate surface and actuator Grafts. Place the cell, controller and real joint; screen moving parts **between** units as well as within one unit. The straight 30 mm chain pitch is not itself a swept-clearance proof.

## Take 31 — oblique upper toe and guarded withdrawal

Mechanics Graft: investigate a fixed-direction tapered toe instead of folding a tongue. A flat load face may remain horizontal; side and leading surfaces must recede, and the rear surface needs shielding. Do not assume any cone/sleeve seam is inaccessible.

## Take 32 — oblique ram package

Packaging Graft: replace the wide platen bridge, not the independent ejector, with a supported oblique linear ram. Check the stowed and deployed stock including real guides, drive and neighbouring unit. Independent of whether Take 31 finds a release certificate.

## Take 33 — compatibility of clamp preload with actual contact deflection

Lead integration Graft: bound the seven-contact preload under external service using both equilibrium and relative deflection from the measured closing load. Test an integral spherical top pad separately from the free ball/bed; do not infer contact-force sharing or available torque from the motor current alone.

## Take 34 — terminal force direction rather than a terminal mask

Mechanics Graft: test an arcuate toe which turns the exposed faces into positive-work ejector surfaces as it opens. Preserve the translational toe's real parked-shoulder counterexample. Bound the work of all reachable faces throughout rotation and at the final stop; a stroke angle is not a mask.

## Take 35 — fit and power an arcuate toe

Packaging Graft: check the independent blade and a powered circular toe, including its pivot, guard and moving root, against own structure, deploy and stow. A crank exposed behind a cosmetic cover or a sector sweeping the lower cheek does not count.

## Take 36 — virtual co-motion of a loose tail and the opening upper jaw

Mechanics Graft: test a virtual twist common to the entire jaw and the free tail. Internal contact work cancels without requiring every moving rear surface to assist release. Evaluate actual fixed-deck, table, pusher, axle-friction and stop constraints; distinguish travel from verified complete separation.

[Report](docs/studies/cand-d-transverse-vise/twist.md) · [calculator](docs/studies/cand-d-transverse-vise/twist.py). The upper deck gives at least +0.913 N·mm per N at the aft pivot under the stated bearing model. The finite cheek sides and parked blade can oppose opening. In a free five-Kin chain, weight bounds total floor normal, not the internal squeeze. No independent release or candidate revision is established.

## Take 37 — support an aft-pivot lift without crossing its sweep

Packaging Graft: test an aft pivot near the lower-deck height and a supported moving arm which can nest in a guarded terminal landing. Check whether a fixed shaft, motor and gear train can coexist with its housing, own fork and both neighbours, not just the working pad.

[Package report](docs/studies/cand-d-transverse-vise/aft-drive-take37.md) · [drive](docs/studies/cand-d-transverse-vise/aft-drive-take37.py) · [checks](docs/studies/cand-d-transverse-vise/aft-gear-search-take37.py). At 10° literal co-rotation puts the crown inside the parked blade by .372 mm. Moving the park 1 mm back puts the nut .70 mm into the bevel allocation. The next motor hits the closed jaw at both pitches; the terminal roof hits a side arm. Reject this installation, not Q12.

## Take 38 — withdraw a smooth cross-pin from a passive eye

Mechanics Graft: check the toroidal eye through loaded withdrawal, including tilted-eye binding, the rounded pin end, finite flared walls and port edges. Do not transfer unloaded-stroke or single-contact estimates to uncontrolled partials.

[Mechanics](docs/studies/cand-d-transverse-eye/README.md) · [calculator](docs/studies/cand-d-transverse-eye/eye.py). The fixed flares admit simultaneous barrel and hemisphere contact at 36°. A finite bound needs the whole applied wrench. At the far-journal exit even ideal near-face fixity allows the pin to reach the port at 32.03 N. An empty port has positive axial work for the stated tube, not necessarily for a thin stem.

## Take 39 — install the eye, cross-pin and independent eject drive

Packaging Graft: place the pin in supported journals, draw and unload the eye, park the pin behind the real wall, then eject. Include the motor, passive hold, load isolation, neighbours, sensors, and both bodies within the 60 mm stowed limit.

[Installation](docs/studies/cand-d-crosspin/eye-pin-take39.md) · [material witnesses](docs/studies/cand-d-crosspin/eye-witness-take39.py). At 36 mm pitch neighbouring head stock clears in the four specified endpoint pairs, but the relieved journal cuts the fixed cheek and the parked ejector rib intersects its own motor. The 59.665 mm sphere encloses the drawn stock, not an achievable stow.

## Take 40 — couple the ring contact to an indexed face

Lead integration in the separate reciprocal-v7 Graft while Takes 38 and 39 check mechanics and package. [Face, ellipse and taper checks](docs/studies/cand-d-crosspin/README.md): two points can bear on the long barrel from 27.275° tilt, not only at the 37.814° diametric pinch. Their restoring moment bounds drag **only with a bounded external eye wrench**. The illustrative six-V registry needs 141.93 N sufficient table-case draw at .050 mm pin offset allowance. A cone steep enough to shed dry friction and a tube-shielded positive-work port do not meet the same sufficient conditions. No official result or candidate revision.

## Take 41 — fixed vertical pin and a relieved seat plate

Mechanics Graft: remove the assumption of a separately bounded pin-x reaction. Test a fixed pin with only a near cheek, including its cap, port and contacts with the table after the six-V registry retreats. A squeeze that assists withdrawal may still damage the parts.

[Near-cheek calculation](docs/studies/cand-d-vertical-pin/README.md): the pin and roof reactions are bounded in the tested pose domain, not over arbitrary poses. A 121 N central load admits a short-journal case with 293 N dry sliding drag before eye friction. The rear roof corners can oppose ejection.

## Take 42 — lift the pin instead of translating its journal

Packaging Graft: fix the upper journal and drive a folded-back rack upward; move the indexed plate axially for take-up, relief and ejection. Check the mounted cantilever variant separately from the two-journal variant, including the powered stroke, direct position flags, level table and neighbouring drive.

[Installation and physical witnesses](docs/studies/cand-d-vertical-pin/fixed-z-take42.md): the plate clears the roof and folded rack, but its thin roots need at least 1.49 GPa nominal bending stress under the 131.55 N draw. At 36 mm pitch the closed-stock sphere is 59.037 mm; it is not an achievable stow because the eye centreline enters the joint motor by 1.950 mm.

## Take 43 — guard a shorter tapered button

Mechanics Graft: test the finite slotted roof and the full parked support, including rear, outer and upper edges. A positive forward normal on an interior strip of roof is not an installed all-pose clearance guarantee.

[Guard and tail](docs/studies/cand-d-parked-button/README.md): the shortened support behind the lowered hood has .473 mm nominal all-attitude clearance from the named terminal. A thinner stem can touch a lateral slot face, and the actual drive pierces the skin.

## Take 44 — fit the larger rounded eye around the joint

Packaging Graft: relocate the hinge motor and reduction, check the eye and its three bosses through articulation, then test the protected button, indexed face and both drives within the complete stowed assembly.

[Installation](docs/studies/cand-d-vertical-pin/button-take44.md): the relocated joint clears the eye, but the Z motor intersects the upper boss by 2.77 mm at +15°. The straight stow requires at least Ø62.369; lowering by 7 mm leaves an electronics-independent Ø64.791 lower bound.

## Take 45 — guide the tapered button and relocate the electronics

Lead integration in the reciprocal-v7 Graft. Check an isostatic five-roller Z guide, the loaded seated contact and its steel supports. Search for positions of the actual cell and controller around the swept joint and release hardware rather than treating an inherited electronics position as fixed. Do not transfer a coupon load rating to a complete installation.

[Guide, register and placement](docs/studies/cand-d-vertical-pin/button-guide.md): electronics positions exist for the unshifted core, and a smaller cell can clear even the lowered drive stock. Neither repairs the drive collision or demonstrates electrical sufficiency.

## Take 46 — exclude contact inside the open slot

Mechanics Graft: test a larger-radius fairing on the actual tail connectors and a raised front opening. Check whether the six working lands remain reachable, then distinguish isolation of the parked button from positive ejection.

[Rolling cartridge](docs/studies/cand-d-rolling-cartridge/README.md): the short central lintel catches the R4.20 stem ball. Raising it to 2.00 mm and routing the thick upper necks forward hides the parked cone by .560 mm and permits six cropped, drafted seats. The remaining rear surfaces have an aligned .499 mm clearance/work certificate, not a pose constraint on the free tail.

## Take 47 — withdraw a tapered horn on a transverse axle

Lead integration in the reciprocal-v7 Graft. Replace the five translating roller tracks with a fixed revolute axis. Derive the opening moment from the exact curved surface and test the swept opening, tail and housing instead of carrying over the straight cone's release credit.

[Local geometry and wrench](docs/studies/cand-d-vertical-pin/horn.md): the curved taper clears the aligned eye during rotation but the loaded pole can apply 1742 N·mm; an opening-assisting contact is not a small holding torque.

## Take 48 — install the horn, its trunnions and a power-off lock

Packaging Graft: compare a through axle with separated stub trunnions, check the moving horn, support and opposing end of the same Kin. A favourable surface normal does not prove that a buried drive fits or can unlock under load.

[Installation and stow witnesses](docs/studies/cand-d-vertical-pin/horn-take48.md): the split trunnions clear the thick tail. The installed cam/carriage configuration needs at least Ø62.588; the hood intersects the hinge and moving seat bridge independently of this diameter.

## Take 49 — force separation through a finite material section

Mechanics Graft: test whether a drafted pusher or interleaved hood and comb can physically exclude the loose rolling tail at full stroke. Check the rear seams, first fork, drive reactions and fixed/moving stock; measured pose alone does not force exit.

## Take 50 — drive the horn root without an overhung cam

Packaging Graft: check a pinned connecting rod to the buried horn root, driven by an always-engaged screw. Replace the Take 48 external cam and long torque-carrying stub; check the actual link, nut, motor, lock, supports and repeated Kin rather than treating an ideal slider as installed.
