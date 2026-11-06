# Retention review: cand-b v1, r1

candidate_id: cand-b
candidate_version: 1
author: Claude Sonnet 5.5 (agent task-5)
reviewer: reviewer-b-independent
outcome: unresolved

Date: 2026-11-05. Reviewed against declaration SHA-256 d973b4cc57b45381b0be9b7e35bdf4508aa3ef449e5fb613c648834454f69a5a. Reviewer is not the author. This is a paper judgement, not a test of the mechanism. Under G6 an unsupported claim is `unresolved`.

## Retention (spring-preloaded hooks in a plug-neck groove)

Principle: geometric interlock plus spring preload. The hook shoulder is square to the pull direction, so tension is carried by contact between shoulder and groove wall. Nothing in the holding path needs power (`requires_power_to_hold` is false). The principle is credible and standard.

What is **not** supported:
- Declared dimensions: only the plug radius (4 mm) and length (5 mm) exist. No groove depth, hook engagement depth, hook geometry, spring rate or preload are declared. Hook and latch are 600 mg placeholders with uncited size, so the interlock cannot be checked against any geometry.
- No force path is argued: shear/bending of 1.5 mm PA12 walls and the groove under tension is not estimated even in order of magnitude. Dossier section 7 says no holding force is claimed.
- Hook retention against vibration and gravity in each orientation is not stated. Retention in "the stated orientations" is only claimed for tension along the chain axis. Compression and torsion are carried by shoulders and flats, but not reasoned with dimensions.
- Release: SMA wire pulls the hook ring against the spring; stroke bounded by a ring stop (dossier). Stroke is undeclared. Independent release is stated; "bounded" is not quantified.
- The hinge is explicitly not passively locked (dossier section 7). Retention of the folded or deployed pose is not claimed and not accepted here.

## Alignment (funnel, taper, flats; no magnets)

Principle: contact reaction on a conical funnel centres the plug under the approach push; flats allow only 0 or 180 degree roll. Plausible in kind. Not supported: funnel half-angle, mouth radius and friction coefficient are undeclared, so jamming versus centring cannot be judged (dossier section 8 admits this). Capture window is unmeasured. The flats give two roll positions but no roll-centring force. The component list for the alignment names shell-a, shell-b and pogo-block; the funnel dimensions are not in the geometry. No unpowered-working argument beyond "passive geometry" is given for the pogo contacts.

## Verdict

unresolved. The mechanism is physically plausible, but the justification lacks the declared dimensions and force reasoning that protocol section 8 check 6 requires. Not a fail: no statement contradicts the requirement.

## Required changes

1. Declare groove depth, hook engagement, funnel half-angle and mouth radius, with cited or labelled-provisional values.
2. Provide an order-of-magnitude tension capacity estimate for hook and groove in PA12 with the stated 1.5 mm wall.
3. State the friction coefficient basis for the centring-versus-jamming check.
4. Any change to the declaration changes its hash; originality needs re-review too.

## Note

The dossier flags a G5 artifact for the folded pose (centre of mass computed in the stowed layout lies outside the support hull). It was not changed here. See Q63 section 3. It does not affect this retention judgement.
