# Retention review: cand-a v1, r1

candidate_id: cand-a
candidate_version: 1
author: Claude Sonnet 5.5 (task-4 agent)
reviewer: reviewer-a-independent
outcome: unresolved

Date: 2026-11-05. Reviewed: `dossier.md` sections 7-9 and the `retention` and `alignment` entries of `declaration.json` (SHA-256 27656337f27029690085a4b5f8c04b8fd6a0c9ddc82cebbdf3a136d83a972f54). This is a paper judgement, not a test (Gate 2/3). The reviewer did not author the candidate and added no evidence in its favour.

## 1. Retention (spring-preloaded ball-lock plus hex key)

Protocol s8 item 6 needs, for retention, the physical principle, the governing geometry or forces with the declared dimensions, and the reasoning that it works unpowered.

- **Principle: supported in kind.** A sprung sleeve holding balls in a groove is a standard passive detent, and the SMA wire acts only to release. Nothing in the dossier needs power to hold, and `requires_power_to_hold` is false. The reviewer accepts that this class of mechanism can hold unpowered.
- **Governing geometry and forces: not supported.** The dossier states that ball size, groove geometry, spring preload, sleeve travel and load limits are "not designed or computed" (section 7) and that "what holds under declared loads is not shown" (section 8). The only declared dimensions are the pin radius 3 mm / 1 mm half-height in the stowed model, a 3.2 mm bore 4 mm deep, and a 4 mm pin extension. No ball diameter, groove depth, preload force, sleeve stroke, nor required holding load is given, so the reasoning cannot be checked.
- **Unpowered reasoning: incomplete.** The release SMA wire (Flexinol 0.004 in, max pull 150 g, from the cited sheet) has an unresolved stroke and force against the sleeve spring. Whether the spring preload exceeds the release-wire pull when unheated, or whether the wire can overcome the spring at all, is not shown. So even the claim of bounded independent release has no force balance.
- **Hex key:** the claim that it bears compression, bending and torsion is plausible geometry, but its flat-to-flat engagement depth is not declared, and the 2 mm PA12 end plate strength is "not assessed" (risk 7).
- **Consistency issue:** dossier risk 3 says the ball-lock plus hex key is rigid by design while the Q31 benchmark needs chain bending. That does not contradict passive retention, but it means the retention geometry may change, which would invalidate any review of this version.

Retention verdict: unresolved. The principle is credible, but the required forces and dimensions are missing. The dossier itself admits they are unsized, so this cannot be passed.

## 2. Pre-alignment (conical lead-in plus hexagonal key)

- **Principle: supported in kind.** Sliding contact on a cone centres a pin in a bore, and a hexagonal key fixes roll to six positions. The 60 degree key positions match the 60 degree roll of one tumbling step, which is consistent on paper. No magnet is declared, and the dossier does not claim one (magnetism rule satisfied).
- **Dimensions: not supported.** Cone angle, lead-in depth, key chamfer, pin-to-bore clearance (radius 3 versus 3.2 mm gives 0.2 mm radial) and tolerances are not chosen. The capture range is "not claimed" by the author. The dossier states a reviewer "should expect to find G6 justified only in principle". A 0.2 mm radial clearance with unspecified tolerances could mean a very small capture window, which the dossier does not examine.
- **No active centring, and no motion source:** the dossier says there is no attractive force and a unit "does not self-dock" unless pushed. The pushing agent (the kick strut) has no designed mechanism (dossier section 6), so what supplies the closing force that makes the lead-in work is unsupported. Friction on the table and in the lead-in is not quantified (Q47 not applied).
- **Tumbling axis not stated:** the dossier says the unit lies on a side face and tumbles over a bottom edge. A prism does that about an axis parallel to the prism axis y, which is also the coupler axis, so end-to-end alignment would be preserved and each step changes roll by 60 degrees, matching the key positions. The dossier does not state this, nor show how a chain of units stays straight while each tumbles. Unsupported.

Pre-alignment verdict: unresolved.

## 3. Outcome

Overall: unresolved. Neither claim is contradicted, but both are justified only in principle. Per protocol s8, unsupported claims are unresolved, never pass.

## 4. Required to reach pass in a new version

1. Declare ball diameter and count, groove depth and profile, spring rate and preload, sleeve stroke, and the design holding load (tension, bending, torsion), with a force balance showing retention holds unpowered with margin and that the SMA wire pull (150 g max per sheet, unresolved stroke) exceeds the spring when heated.
2. Declare cone angle, lead-in depth, key chamfer, clearances and tolerances, with a geometric capture-window estimate, and name the source of the closing force.
3. State the tumbling axis and show chain alignment through a step.
4. Resolve how the rigid key and lock allow the chain bending of Q31, or change the coupler (a new version needing new review).
