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

[Four-tile separator](docs/studies/cand-d-forced-section/README.md): forced separation holds inside a bounded window, not around the perimeter. The root motor axis penetrates both a cropped side and a blade even at home.

## Take 50 — drive the horn root without an overhung cam

Packaging Graft: check a pinned connecting rod to the buried horn root, driven by an always-engaged screw. Replace the Take 48 external cam and long torque-carrying stub; check the actual link, nut, motor, lock, supports and repeated Kin rather than treating an ideal slider as installed.

[Root drive](docs/studies/cand-d-vertical-pin/horn-take50.md): no crank dead centre, but four non-electronic points need ≥61.041 mm. The guide also hits the fixed horn motor, and the moving carriage hits a held neighbour. A stronger paired socket trades tower bending for an inadequately supported cross-sill.

## Take 51 — put the six seats on a drafted, backed face

Lead integration in the reciprocal-v7 Graft. Relocate the bosses and check a finite U-shaped moving face with continuous tapered backing from each tangent land. Check its underside, side towers, junctions, load targets, local release path and interaction with the actual stationary hinge.

[Backed face and relocated joint](docs/studies/cand-d-vertical-pin/registered-face.md): the four-tile stock clears the revised hinge but not the root motor. The steel eye/tail and face alone weigh about 49–55 g; the 90 g loaded-datum study needs 170.43 N axial force, not a universal 111 N.

## Take 52 — thread and withdraw a flexible positive tie

Mechanics Graft: test a finite strand driven through a passive curved return. Check force transfer at unequal end tensions, mouth interference and the last-link exit under live load; no latch opened merely by command.

[Fixture and derivation](docs/studies/cand-d-beaded-lace/README.md): the rocker absorbs a full pitch, and a single rounded lip cannot statically trap the last bead in the stated gauge. Two rounded strips leave a 2.011 mm throat around a 2.30 mm bead even at zero friction. This refutes the general single-lip argument, not reachability in a complete assembly.

## Take 53 — install the reusable lace and its receivers

Packaging Graft: check a head-side feed, supported pickup, power-off lock, take-up, recovery and actual pusher with the passive return, neighbouring body and electronics. Do not carry over the horn, high post or long X rail.

[Installed section](docs/studies/cand-d-beaded-lace/bore-take53.md): Ø59.599 mm straight stow does not make this assembly installable. The U wall crosses its own hinge and opposing magazines at 38 mm pitch have overlapping metal. At 55.5 N draw the tested drive needs 43.33 N·mm against 23.96 N·mm optimistic continuous output. Reject this arrangement, not every flexible tie.

## Take 54 — bound the two-end draw on an indexed face

Lead integration in the reciprocal-v7 Graft. Check the effect of unequal or single-end tension in a laced U return on all six indexed reactions. Separate the working draw from guide friction, working load, strength at the end fitting and actual exit.

[Finite frame](docs/studies/cand-d-lace/README.md): 55.77 N total axial draw at the 70 g table case on six R8 cropped crowns, conditional on a 1.16 tension ratio, a 6.7° line cone and the stated errors. The frame clears the preliminary rocker at zero draw offset through ±17°; full installed motion and release are not certified.

## Take 55 — discharge a spherical stud sideways

Mechanics Graft. Explore an open-ended C-track and a full-section positive displacement plug. Distinguish a closed end cross-section from a force bound through the last partial engagement; model the finite stock of the neck and the moving neighbour.

[Free-body certificate](docs/studies/cand-d-sideways/README.md): two inner lips and two rounded rear corners can hold the globe and flat shoulder against an arbitrarily scaled plug load in the rigid friction model. Increasing screw torque is not a release guarantee.

## Take 56 — install a transverse discharge slide

Packaging Graft. Budget the short track, axial take-up, one positively driven transverse plug, screw drives, battery, logic and the joint together; check the ejected neighbour as well as straight stow.

[Installed section](docs/studies/cand-d-sideways/side-take56.md): Ø58.988 straight stow, but the draw bracket crosses the transverse motor. A −25° pre-roll can bypass the straight-pose index collision and reach the Take 55 jam for the checked free-space surfaces. That path crosses a level table by 1.942 mm, so it does not demonstrate a tabletop jam.

## Take 57 — finite-time release after the last loaded support

Lead Graft. Test whether a positively retained, stored-energy **opening** stroke could bound the relative pose before the last edge clears, instead of assuming a partly released body remains aligned forever. Account separately for lost preload, guide reactions, moving mass, rebound, power interruption and the work needed to clear a neighbour.

[Opening-only captive return](docs/studies/cand-d-pressure-transfer/retreat.md): a conditional .709 ms aligned stroke spends almost all the slot margin in a free-body load screen. The carrier can recoil, the terminal stop must absorb up to .300 J, and vacuum loss **before** alignment leaves a finite interval where the bar cannot retreat. No release credit.

## Take 58 — open three captive peripheral sectors

Mechanics Graft. Replace the central stud by a broad, short tail flange. Check opening the rear-flank sectors under one-sided load including sector ends, guide reactions, neck and neighbouring stock; no spring-closed clamp or assumed band load sharing.

[Sector study](docs/studies/cand-d-perimeter/README.md): a single loaded sector can reach the rounded crest while the other two clear. Pressure assists opening only within the guide-drag budget. The parked sector leaves a 1.570 mm recess with a backward-facing fixed lip; the local sphere witness is not a whole-flange jam.

## Take 59 — package a perimeter clamp and a solid central ejector

Packaging Graft. Install the flange, radial sector drives and positively driven disk; test the metal axial take-up/disk stop, screw reactions, tail joint, electronics, neighbour and stow together.

[Installation](docs/studies/cand-d-perimeter/flange-take59.md): transverse motor clears the neighbouring head in Ø58.504 stow, but crosses its own frame, and the sectors cross their feet. One loaded seat needs a tensile reaction at a compression-only pad. Reject both studied packages.

## Take 60 — close the full bore with a solid advancing disk

Lead Graft. Bound the annular slit around the advancing disk and the loaded pole directions with real backed-surface radii; separate emptying the retaining cavity from clearing other exposed parts or certifying the sector drive.

[Disk analysis](docs/studies/cand-d-perimeter/disk.md): .072 mm terminal clearance for sphere generators inside the continuous mouth. The earlier window contact and installed eccentric drive are outside the smooth-bore force proof. No Gate result.

## Take 61 — repair the forward sector seam

Mechanics Graft. Test a whole-flange constraint at the parked lip and a positively driven wall bridge if necessary; keep side and end contacts in the release budget.

[Pivot leaf](docs/studies/cand-d-perimeter/pivot/README.md): .48 axial pole fits the whole flange; .55 and .60 intersect it. A tilted flange can oppose rotation at the finite toe. The parked seam's 1.77 µm normal-loss allowance does not establish a robust stop.

## Take 62 — retract the sleeve around a fixed seat plate

Packaging Graft. Test a rigid metal spine, six finite face inserts, three axial take-up shoes and positively sequenced radial opening then axial sleeve retreat.

[Installed sleeve](docs/studies/cand-d-perimeter/sleeve-take62.md): the fixed plate removes the tensile-pad problem. One drive hits its own yaw motor, and the lower spring seat crosses the table. In the shorter layout the translating hoop crosses the fixed spine, and two electronics corners are 62.767 mm apart. These are specific installations, not a universal lower bound.

## Take 63 — bound the axial take-up and fixed face

Lead fixed-spine Graft. Test finite drafted index faces, independent spring bands, unilateral clamping work and actual static reactions in a declared tolerance box. Do not count the spring as the radial lock.

[Fixed face](docs/studies/cand-d-perimeter/fixed_face.md): three independently delivered 33–39 N axial springs on the working jaws can resist a local seated escape in the 70 g screen, but their catalog tolerance and installed drag are not established. Moving the springs behind the tail buttons changes the wrench matrix: it needs a different jaw angle. Neither meets the full release requirement.

## Take 64 — drive three captured plate followers and pivot leaves on one fixed-axis drum

Packaging Graft. Test an axially fixed ring, three bilateral disk supports, worm and positively backed index, rigid opening leaves, and separate passive-tail button cartridges. Keep the actual last-leaf contacts distinct from a nominal force calculation.

[Captured drum](docs/studies/cand-d-perimeter/drum-take64.md): the cam core overlaps the rear spine even after cutting its grooves. The rod crosses the bearing pillar, and the Geneva releases the wheel before pin pickup. The tested cell and motor-base corners alone are 60.155 mm apart. Reject this installation, not Q12.

## Take 65 — match the full flange to three spring-guided tail buttons

Lead button-support Graft. Use the actual .48 pivot-leaf normal. Compare the 60° face with a finite 65° seat, bound the loaded contacts without equal sharing, and check button guide, stack length, exposed nose and face tolerances. No transfer from the .60 leaf that cuts the flange.

[Button support](docs/studies/cand-d-perimeter/button_support.md): 65° brings the nominal table preload down to 35.404 N per button, but the commercial plunger hides its working pole as it compresses. A loaded custom guide can have more friction than the force tolerance. A rocker changes the required force and admits only .071 mm of equivalent travel in the trial band.

## Take 66 — reshape the full flange and control the parked edge

Mechanics Graft. Test a rounded three-lobe core, higher working axial component and a finite positively supported seam with an attainable tolerance. Check local flare against both home and full ejector stroke; do not carry over the old continuous bore calculation.

[Rounded lobes](docs/studies/cand-d-perimeter/lobed/README.md): the .60 working pole and the lower inner-contact work bound survive finite stock. At the same actuator phase two distinct tail poses require axial virtual velocities ≤2.266 and ≥3.141 mm/rad. No single axial certificate for all poses; no simultaneous jam established.

## Take 67 — relocate the joint behind the drum

Packaging Graft. Try an offset yaw assembly, central quill, three-lobe flange, 56° seats, and a positively inserted worm parking bolt. Check electronics at cycled cell dimensions, mounted tabs, separate protection and antenna clearance. No ordinary worm friction as a lock.

[Offset quill](docs/studies/cand-d-perimeter/quill/quill-take67.md): a cycled-cell corner and a foot corner are 61.365 mm apart. The named steel parts and bare cell alone weigh at least 74.323 g; do not transfer the 70 g preload result. The shallow center pocket is only 0.73 mm deep. The slide's transverse cheeks cannot react its 9.465 N mm pitch couple per radial newton. Reject this installed layout.

## Take 68 — move the compliant seats into the ejector plate

Lead saddle-plate Graft. Keep the three-lobe tail solid with integral R2.50 buttons. Model independent translating V-saddles, narrow blind running gaps, finite protrusion and spring/guide stock behind the mobile disk. Check plate-rim continuity, pressurized parts, force windows and one-sided guide reactions separately from the moving-leaf proof.

[Moving V-saddles](docs/studies/cand-d-perimeter/saddle.md): the pocket retains a continuous outer rim. A clean one-sided guide moment exceeds the short block's smooth-running recommendation; its bracket crosses the disk post. The sufficient seated S=28 N certificate covers less than 73.133 g in the trial mass-scaled load box.

## Take 69 — partition the inside and outside release contacts

Mechanics Graft. Test whether a single tail configuration can load both the outer drive stock and the inner jaws. Try a configuration-specific virtual twist or a fixed convex guard. Include one-sided guide and journal losses; distinguish a missing certificate from a self-stress.

[Three pose families](docs/studies/cand-d-perimeter/twists/README.md) admit different work certificates. The near-bore family covers every leaf surface when all R2.50 generators stay inside radius 10.95; it is not an invariant of release. The fixed hoop introduces a reachable backward-facing rim. Neither a positive local margin nor adding the hoop establishes a global jam or a guaranteed release.

## Take 70 — reduce installed mass without erasing the contacts

Packaging Graft. Try a mechanically backed light core or a closed hollow tail with finite ribs, finished metal load pads and fixed pull-off keys; check the cycled cell, feet, motor mounts and enclosing sphere together. Keep the stock and force scales consistent.

[Keyed sleeve](docs/studies/cand-d-perimeter/keyed/shell-take70.md): Ø59.948 nominally including the cycled cell and articulating tail, but the front shoulder blocks insertion of the assembled axle. At the trial load the dog needs .831 N mm for extraction versus .562 N mm optimistic continuous drive. The separate spherical cup intersects the fixed quill. No buildable loaded-release installation.

## Take 71 — put the six seats on one floating plate

Lead floating-seat Graft. Remove three separate sliding carriages. Screen a single spring-loaded plate with two angular degrees of freedom, including the actual pivot offset, swept rim, six finite faces, antiroll reaction, spring travel, finite load path and one-sided contacts.

[Floating plate](docs/studies/cand-d-perimeter/floating.md): moving the pitch/yaw center aft exhausts the trial rank budget. For the XY alternative an exact dry equilibrium with one recessed seat supports the whole draw even with ideal slide guides. Force-only seating is not sufficient. A separate full uncut backing overlaps the three post tips.

## Take 72 — release across a floating face

Mechanics Graft. Test the non-tilting XY plate alternative separately from the seated force screen: finite moving V faces, displaced rim and central boss, draw with the jaws locked, then withdrawal under load without assuming continuing seat contact.

[Rocking release](docs/studies/cand-d-floating-rim/README.md): under 20 N compression one continuous path rocks the complete tail 4° and clears the lip at the minimum stroke, with four seats still in contact. The central boss penetrates a diagonal capsule at a permitted .18 mm transverse displacement. Neither continued compression nor positive stroke certifies a persistent air gap.

## Take 73 — withdraw a plug with an actual cone cap

Lead flush-plugs Graft. Replace the external pivot/link with a blind radial piston. Keep the original tension pole on an aft bevel, use a true cone on the nose, and quantify the missing cap at the bevel and side reliefs at park. Check the front end and the rear fixed cheek during opening, not only the ideal working plane.

[Blind plugs](docs/studies/cand-d-perimeter/plug.md): all bore-side cuts of the trial port have a common positive virtual-work motion on R2.45-backed stock. The proof includes the non-flush aft bevel, not a perfectly filled cone. It does not include guide loss, missing seats or the outer housing.

## Take 74 — one draw contact and six rigid seats

Mechanics Graft. Test a seven-contact load path: one positively withdrawn tapered key carrying a central rounded lug, and six rigid seat normals around its load line. Check eccentric force, Coulomb stiction, tolerance, partial contacts and real guide stock.

[Single key](docs/studies/cand-d-single-key/README.md): a 60 N key normal is compatible with one open face under a 70 g service-box load. The 4.85 mm park clears the returning lug on the centered inclined path, but guide play exceeds the assumed ±0.10° accuracy. Neither an all-seven equilibrium nor a centered release is an installed lock.

## Take 75 — enclose the radial-plug drive

Packaging Graft. Put two opposing X-bearing rows at different radii on each translating plug, drive all three with an enclosed face cam, and drive the terminal disk independently. Keep the finite front wall, check assembly access and guide loads at the actual actuator offset.

## Take 76 — compatibility of elastic seat loads

Lead elastic-seats Graft. Test the rigid disk with finite local compliance against simultaneous equilibrium, true contact poles and installation errors. Compute whether a zero-charge seat remains supportable as a function of measured draw, not just whether an arbitrary rigid contact-force vector exists.

[Compatible states](docs/studies/cand-d-perimeter/elastic.md): at the same 100 N draw and 0.029421 mm disk advance, all seats can carry load or one recessed seat can have a 0.0138 mm gap. Both obey finite unilateral compliance and Coulomb friction. A separate six-pocket spring installation intersects all three disk posts.
