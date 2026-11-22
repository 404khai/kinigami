# Take 52 — positively driven beaded lace, supported U and real equalizer

**Exploratory, not a candidate or release certificate.** A smooth-ended lace can replace the heavy horn's seated tensile path. A real trunnioned equalizer can bound both endpoint tensions without assuming a frictionless U. Rounded, backed lips can exclude exposed connector contact and a *single-contact* last-bead jam, under explicit bead/link gauges. These are useful local improvements. They do **not** yet prove supported feed, far-latch transfer or arbitrary-attitude live unthreading: two lips on different bodies can trap the last smooth bead. The small pusher has no permission to remove that obstruction by commanded motion.

Fresh Graft `beaded-lace-study`, based on `00e17dd`; no work in another agent's checkout. The accidentally created earlier `bead-lace` Graft has no study edits and is not the deliverable. Q12/Q85/Q100, criteria, candidates and Gate 1 run 12 remain unchanged. No commit, push, v8 declaration, independent review or official run.

## Reproduce and integrate

```sh
python3 docs/studies/cand-d-beaded-lace/lace.py
python3 docs/studies/cand-d-beaded-lace/lace.py --json > take52-lace-fixture.json
git diff --check
```

Python standard library only. The JSON gives exact parametric tube/rounded-cap geometry, trunnion and mouth datums, gauge targets and the two-lip counterexample. Its omissions are intentional: it is a local mechanics fixture, **not** collision stock for an installed Kin. Dimensions below are provisional study inputs unless explicitly sourced. No compliance, dynamic impact, wear, fatigue, actual sensors or actuator capacity is inferred.

## 1. Local material geometry and load path

Mated face x=0; head in negative X, passive tail in positive X. Two tail mouths are at (0,±6,0). Straight centreline legs extend to x=3.5; a semicircle of centreline radius 6 in XY joins them, bulging to x=9.5. Bore radius **1.65**, outer radius **4.15**, leaving 2.50 mm wall. The outer tube is real stock minus an enclosed bore, **not** a zero-thickness sweep or a filled bore. The return reaches x=13.65 at its exterior; |y|≤10.15, |z|≤4.15. Its stock has to join the tail structure and six lands through metal, not float in space.

At each mouth use a full toroidal end cap of major radius 2.90, minor radius 1.25, centred at (1.25,±6,0), axis X. Join the straight tube at x=1.25, with no axial back step. The most forward cap point is x=0 and the lip opens at radius 2.90 there, reducing smoothly to bore radius 1.65. A split return is machinable in principle, but fasteners, joint preload, bore finish and loaded section strength are unresolved. Any seam accessible to the lace invalidates the smooth-stock proof unless separately buried or finished. Do not replace this lip by a chamfer and keep its result.

Three sites at R13 and 120° spacing carry six ±circumferential facets, normals n_x=.5 and tangential components ±sqrt(3)/2. Their actual backing and contact area are not sized. A direct six-by-six equilibrium calculation demonstrates one frictionless feasible load case with positive normal forces; it is **not** an all-wrench or all-friction certificate. The **39 N total axial draw** is the lead's conservative 70 g, 60°-flank, near-equal-leg study input, not rederived as an acceptance threshold here. The lead's ~184 N one-sided comparison must not be replaced by 39 N after equalizer travel bottoms.

The intended seated metal load loop is slide → trunnion → two rocker arms → permanent anchor / positive free-tip pocket → lace → U wall → tail lands → head lands → slide frame. An independent reversible latch is required on the free-tip arm; an irreversible ordinary chain connector is not a release mechanism.

## 2. A real equalizer, not capstan equality

Use a rigid rocker about Z on a translating draw slide, pivot (−10,0,0), opposite endpoint centres 6 mm from the pivot. At θ the two endpoints are (−10∓6sinθ,±6cosθ,0). Both chain legs run **directly** to the tail mouths. A fixed guide touching a loaded leg would carry some line reaction outside the rocker and invalidate this moment balance. Either withdraw each temporary feed guide fully before draw or put every loaded fairlead on the relevant rocker arm and use its actual resultant/moment.

Differential leg length is

    Δ(θ) = hypot(10+6sinθ,6(1−cosθ))
         − hypot(10−6sinθ,6(1−cosθ)).

At ±17°, Δ=±3.50722 mm. This supplies a whole **±3.40 mm** pitch mismatch, not just ±half a pitch. Place unloaded mechanical stops at ±20°, where Δ=±4.10144; a measured service bound of ±17° must include seating uncertainty, pitch variation, elastic mismatch and wear. Mere ability to turn to the stop is not a guarantee that it never bears. Draw stroke adjusts common length continuously; the rocker adjusts the differential continuously. Quantized bead pickup does not excuse a hard-ended service equalizer.

The total departure of each force direction from +X is bounded here by **3° including nominal angle and build/posture error**. At the exact datums the largest nominal angle at ±17° is 1.82109°. Retracting the slide farther into the head (D≥10) only decreases that angle and increases differential capacity slightly; no loaded service credit is given at D<10. There is no supplier or physical test establishing the remaining angular margin. Allow an independent .08 mm force-line offset at each spherical seat (packaging's observation). With trunnion drag |τ|≤.50 Nmm,

    h_min = 6cos(17°+3°) − .08 = 5.55816 mm,
    h_max = 6 + .08 = 6.08000 mm,
    |h₁ T₁ − h₂ T₂| ≤ .50 Nmm,
    T_high ≤ 1.093889 T_low + .089958 N.

This uses moment equilibrium; it does **not** assume equal capstan tension, equal friction or equal take-up. For 39 N actual total axial draw, 39≤T₁+T₂≤39/cos3°, so either leg ≤**20.4453 N** and ≥18.5827 N. No endpoint equality is required. The pivot sees both force resultants (≤39/cos3°) and bounded drag torque; the draw frame must ground those loads.

The .50 Nmm and .08 mm are **measurement/qualification targets**, not sourced bearing performance. Bearing drag with two-sided Z support, seals, contamination, harness moment and load must be measured. A stop, stationary fairlead, eccentric terminal force outside the .08 envelope or a seized bearing removes this bound. The JSON's bar is only a local rigid-stock envelope; there is no bearing, lead screw, limiter, stop-strength or attachment design.

Packaging's temporary 1.90 mm split-tine slot leaves only .20 mm unilateral lip against the minimum Ø2.30 bead. A 1.00 mm pin, 2 mm supported span, carrying the above endpoint force would screen at ~104 MPa simple beam stress; this does **not** qualify that thin lip, hollow bead seam or terminal pull-through. The arm force lines must be calculated at their real socket centres.

## 3. What rounded stock can prove in full 3D

For this **hypothetical gauged chain** require spherical external bead radius r≥1.15, r≤1.25 for clearance, adjacent centre distance p≤3.40, and *all* exposed inter-bead connector material inside the capsule of radius d≤.35 joining its two bead centres, throughout permitted articulation. Require a smooth terminal bead with **no protruding cut wire/dumbbell tail** beyond it. These limits are not supplied by the commercial catalogue.

At every reachable lip patch require a genuine solid interior ball of radius ρ=1.25 tangent to the surface, backed by real wall stock. If a connector capsule met that interior ball, one of its bead centres would be within

    sqrt((ρ+d)² + (p/2)²) = 2.334524 mm

of its centre. But collision-free beads require ≥ρ+r=2.40 mm. Reserve is **.065476 mm**, independent of 3D link direction. Equivalent minimum ρ is

    ρ > (p²/4 + d² − r²)/(2(r−d)) = 1.05625 mm.

This is a precise sufficient no-connector-catching condition. Sharp edges fail it: when a .35-radius connector touches a point, adjacent centres at ±p/2 are 1.73566 away, so both 1.15-radius beads clear and the thin connector can catch. The proof must cover every reachable seam, slot, rear shoulder, feed-pawl edge and cut terminal, not just the U's mouth.

Commercial beads are hollow and seamed, not solid bearing balls. The sphere exclusion further requires every seam and stem aperture to reject the ρ=1.25 lip stock, remain closed under load, and preserve the gauged envelope; otherwise a lip can enter a hole or crush the shell. No shell hardness/contact stress or crimp retention rating is known. A sourced *average tensile* value does not establish any of those facts.

For the **free last bead contacting one convex lip only**, its next full bead limits inward pull-direction cosine to c=p/[2(ρ+r)]≤.708333. A static friction-only lock would require c≥1/sqrt(1+μ²)=.97456 for μ=.23. Available tangential sliding drive is at least [sqrt(1−c²)−μc]T=**.54296 T** in this one-contact case. Both adjacent-bead exclusion and the single-contact restriction are essential; there is no general no-jam theorem for arbitrary multiple contacts.

## 4. Supported feed, release sequencing and the missing handoffs

The R6 return asks for 32.9185° articulation per maximum-pitch link; rod chord sag is .24587 mm, below the .40 radial bore room. R8/R10/R12 lower the required angle to about 24.54°/19.58°/16.29°. **None** is qualified because no source supplies the chain's allowed loaded articulation, rod/ball-hole sweep, compressed pitch or local fatigue limit. Checking centreline/chord fit is necessary, not sufficient.

With .10 placement error and 3° total line angle over a 3.5 mm straight leg, the nominal radial fit margin is .11657. That says nothing about acquiring this supported pose: before lacing, unilateral six-V contacts cannot hold arbitrary tensile and overturning loads. A real docking force/support and temporary enclosed guide must be identified. No credit for commanding coaxial faces.

One plausible sequence, with its unclosed physical interfaces:

1. **Thread in:** hold the unlatched face through a declared external support, bridge head/tail mouths with actual guide stock, positively feed the rounded tip through the U and into a receiver on the opposite arm. A free flexible leader cannot be assumed to transmit compression across an open gap. Do not draw until the far positive latch is physically engaged.
2. **Draw:** withdraw temporary tracks and receiver elements that would touch loaded legs outside the rocker. The trunnion has continuous differential motion; the slide supplies measured common take-up and a separately capped preload. Gauge the two leg directions and actual rocker range. A count of beads is not tension measurement.
3. **Start release:** a bilateral supported pocket drive takes the far tip's actual force *before* its keeper moves. Back the tip clear of the latch while it remains in that pocket; independently sense the load transfer and keeper clearance. Ordinary spring release or moving the keeper under tip load is not this handoff. No finished pocket/cam/actuator model is supplied.
4. **Payout/unthread:** reverse the pocket/recovery drive and pull back the permanent leg while feeding the far tip into its passage. Before releasing the pocket, account for its instantaneous force and the rocker's now unequal loading. After one endpoint lets go, the service equalizer relation no longer applies; a free rocker rotates to a stop unless deliberately transferred to another rated support. Live external tension can open/tilt the face while the lace is still threaded. It cannot be replaced by the seated 39 N or by capstan equality.
5. **Finish:** retrieve the smooth last bead, demonstrate the real chain path clear of **both** bodies and their mouths, then retract all remaining noncapturing guide projections. A positive short pusher may then supply separation from plain outward faces. It cannot prove step 4 happened or cut a trapped lace.

A fully enclosed short feed tube can react compression, but friction rises with zigzag. In a simplified fully supported guide with p=3.40, lateral centre play .50 and μ=.23, alternating contact gives per-bead ratio ~1.1523; fourteen such bends could multiply input force by **7.28**. Compressed pitch and the unsupported tip can make matters worse. The smooth-belt π-wrap comparison exp(.23π)=2.0597 is therefore not a push-force rating. Neither number bounds a caught connector, unsupported buckling, multiple-body wedge or self-locking feed pawl. A finite number of links is not by itself a finite extraction-force proof.

## 5. Real last-bead obstruction surviving the rounded-lip proof

Two disjoint *solid* radius-1.25 lip patches are enough. Put the last bead radius1.15 at O=(0,0,0); take α=20°, d=2.40 and lip-ball centres

    Q± = (−d sinα, ±d cosα, 0)
       = (−.820848, ±2.255262, 0).

The lips do not overlap. They touch the bead simultaneously and leave a **2.010525 mm** throat, smaller than Ø2.30 but larger than the Ø.70 connector. The prior bead at (−3.40,0,0) clears both lips; the connector between it and O clears them too. A pure pull −X is balanced at μ=0 by two normal reactions N=T/(2sin20°); at T=20 N each is **29.238 N**. Translation toward the head is geometrically blocked even though each lip is smooth, properly backed and individually satisfies section 3. To avoid relying on an unstable out-of-plane two-sphere saddle, the JSON also gives each lip as a finite **capsule along Z from −5 to +5**, radius1.25. The section is then unchanged over 10 mm of real edge; leaving around its ends needs extra lateral movement not supplied by the pure −X retractor. These are closed solid rounded strips, not zero-thickness normals or intersecting bodies.

The second lip can approach continuously from an open throat ≥2.50 mm to this closed throat without the two lips ever intersecting. A live partly released tail is not forbidden from supplying this transverse closure. This is an explicit local two-body counterexample to the proposed *general* implication “rounded bead + rounded mouths + capstan ⇒ unconditional last-bead withdrawal.” It is **not** a certified reachable pose of the entire current U/head assembly; those full swept solids have not been modeled. It identifies the geometric handoff that an integrated design must exclude rather than asserting all laces must fail.

To remove this class of trap, prove that a bead can never contact both bodies at the same time (for example actual lip sets stay more than maximum bead diameter apart), or positively keep a full-bore continuous path until the tip is physically inside the head. The latter needs a guide/support that survives the same live wrench and then releases without recreating its own loaded last edge. Neither is furnished by this fixture. An alignment state label or a short free pusher does not supply it.

The head/tail bore Ø3.30 excludes an R4.20 ball centre through its throat; maximum spherical cap penetration at the disk is .33771 mm. It does **not** exclude the R1.45 first fork, which fits. Access to a protected latch via the larger bellmouth, the bore, side windows or seams needs actual depth/backing checks. There is no “small aperture protects everything” claim.

## 6. Materials, terminal and alternatives

Source facts checked from the product pages on 2026-11-22:

| Source | What it actually says | What it does not establish |
|---|---|---|
| [Ball Chain Mfg #3 spool](https://www.ballchain.com/3-stainless-steel-ball-chain-spool/) | Approx Ø2.4 mm, 93 beads/ft mean (3.27742 mm), stainless | Toleranced pitch/diameter, terminal or working load |
| [Manufacturer size chart](https://www.ballchain.com/chain-sizes/) | All sizes approximate; #3 94/ft (3.24255 mm), average stainless tensile25 lbf=111.206 N; #6 69/ft, Ø3.2, average45 lbf=200.170 N | Minimum breaking, safety factor, working cycle, bent strength, allowed articulation, contact bearing |
| [Frank Ferris chain description](https://www.frankferrisco.com/product/beaded-chain/) | Seamed hollow beads joined by dumbbell connectors | Solid spheres, smooth free terminal or crimp/ball-hole strength under mouth loading |
| [Manufacturer material guidance](https://www.ballchain.com/roller-shade-chain-info/) | Generic “stainless” is insufficient; ask for grade, tested finished-chain strength, pitch and stretch data | Grade or load rating of this specific #3 study gauge |

The #3 average tensile / 20.445 endpoint ratio is about5.44. It is **not** a working safety factor. A tip pocket can crush or pull through a hollow ball far below chain average tension. Packaging's separately found Nissa SUS305 SB23 Ø2.3,p3.1, reference use39.2 N and break127.5 N is a different product and is not combined with the American #3 dimensions/rating here.

Stainless strip or flex leader removes bead/connector crevices but changes the load path. A strip of thickness t bent around radius R sees outer-fibre strain approximately t/(2R): a .10 mm strip at R6 is ~.83%, not automatically elastic or fatigue-safe in an unspecified stainless temper. A nonstructural flex leader still needs a positively supported handoff from it to the load-bearing lace. Rigid articulated micro-chain supplies defined pin geometry in principle but its plate gaps, reverse articulation stops, torsion and terminal link reintroduce finite mouth/catching checks; it is not automatically a smooth Ø2.4 envelope. No replacement material is selected without finished-part data.

A trial noncapturing pusher total5 N against compression1W and table drag μ=.5 at70 g leaves **3.9703 N** before guide loss. This illustrative force margin is not a motor/source rating, an all-wrench bound, sufficient travel or a finite-rim proof. Pushing at only one pad adds overturning moment and can close a mouth against the lace. Size and place the actual pusher only after its released contact region and path are established.

## Verdict and smallest next proof

**Useful:** true moment-based endpoint balance with full-pitch differential capacity; a real backed U/lip datum; a 3D gauge-based no-connector-contact condition; a single-contact terminal sliding bound.

**Not closed:** sourced articulation/terminal strength, supported pre-latch acquisition, loaded pocket transfer, post-latch rocker support, split-track withdrawal, two-body last-bead pinch, compact pusher clearance and Q12 fit. Thus **no bounded arbitrary-attitude live-release claim**. The smallest useful next experiment is a measured two-mouth/last-bead fixture with the actual gauged chain and moving tail, plus the rocker/receiver mounted on their real bearings—not a full Kin animation.
