# Post-freeze design discriminator — no Gate result

[Take 16](direct.md) separates the useful full-thread work from the fading load path at final extraction. Neither the [direct-thread study](drawbolt.py) nor the additional [force window](preload_window.py) is an implementation or a change to the frozen v7 shutter. The alternatives have different geometries and assumptions. Do not combine their favourable numbers.

## Preload is not an inferred motor current

A [Smalley CMS08-M1](https://www.smalley.com/wave-spring/cms08-m1) fits an 8 mm bore around a 5 mm shaft and is listed at **30 N at 1.78 mm**. Free height 2.82 mm and rate 28.85 N/mm are explicitly reference values. At the sensitivity settings ±12% force, ±15% slope and ±0.08 mm true working height, the model spans 23.75–36.25 N. Those tolerances are *not* on the manufacturer page; gauge actual incoming load at installed heights and verify that the physical load path sees the spring, without a hard bypass. Merely specifying a switch and motor angle would not establish preload. The equilateral-pad axial-only full-seat screen at radius 4.65 mm and 50 g requires >14.36 N. Side forces, eccentric pitch, incomplete contact and thread torque make that lower requirement insufficient by itself.

[Glenair AN0021 rev B](https://www.glenair.com/test-reports-and-technical-information/pdf/application-note/an0021.pdf) illustrates how even a purpose-designed connector can bind or damage contacts if walked apart asymmetrically. Its application-specific prescribed mating sequence is **not** an available second actuator, fixture or allowable release force for a Kin. Primary spring data and application note were retrieved directly. The 4.8 V servo rating stays 49.03 N·mm.

## Changing the lead changes midstroke recovery

For a *permanently engaged internal* V thread, let the actual symmetric rotary overload limiter transmit 30–37 N·mm at the screw. These are hypothetical component bounds, not a delivered limiter. Reserve 5 N·mm for loaded supports, also not yet proved. Use 1.5 mm effective radius for this comparison, no friction credit at the low extreme and μ=0.23 for adverse dry; replace it with the real min/max pressure radius, misalignment and bearing losses before a design decision. With an obstruction removed and the same trapped axial force assisting reverse, the lowering coefficient rather than the raising coefficient applies. It does not apply to a second obstructing force that resists reversal.

| Screw lead (mm/rev) | Dry working force (N) | Max tightening-induced force (N) | Reverse incl. allowance (N·mm) |
| --- | ---: | ---: | ---: |
| 0.50 | 51.6 | 465.0 | 151.2 |
| 1.50 | 37.6 | 155.0 | 28.7 |
| 2.00 | 32.9 | 116.2 | 13.8 |

The fine screw can supply more working force but can defeat its own reverse limit after low-friction tightening. The 2 mm lead remains interesting only if **all** moving demands fit, the weak/strong clutch bounds exist in both directions, supports do not seize, the independently limited fault force is structurally safe, and the powered-off lock is not dependent on a backdrivable thread. Combined live load plus residual trapped preload may cost more than the tabulated reversal. A torque cap is not a cap on eccentric internal contact force. Rotor inertia, overrun and rebound are omitted here.

## Direct-thread endpoint

For a conventional male thread leaving a passive nut, there is no positive lower bound on remaining flank area during the last fractional turn. Even the generous fictitious shear area πdℓ at d=3 mm with 1 GPa allowable would support <1.961 N (4W at 50 g) for ℓ<0.000209 mm. At this scale a physical contact will deform, lose equilibrium or roll off; continuum numbers are not a prediction of breakage. The result instead exposes the missing handoff in a *uniformly static* release proof: the three axially open keys cannot take guaranteed tension, a forward pusher does not relieve it, and no actual rounded elastic exit or alternate tensile support has been analysed. This rules out crediting that direct-thread argument, **not** all threaded joints or the 60 mm envelope.

[Separate envelope witness](envelope.py): extruding the existing v7 nose primitives by 2.70 mm has a 59.754 mm containing sphere about (12.731,0,0) mm. At +3.00 mm the computed witness is 60.028 mm (not a proof that no better shape fits). No new internal holder, pad or lead-out is counted until actually drawn.

## What a smooth flat-pole calculation misses

[Elliptical Hertz screen](edge_hertz.py) solves the two principal normal-curvature integrals for an elastic half space; it reproduces the closed-form circular sphere–plane solution. See [NASA TN D-8166, elliptical-contact solution](https://ntrs.nasa.gov/api/citations/19760019429/downloads/19760019429.pdf). An illustrative 43.1 N on a 1.045 mm spherical crown and a 0.10 mm convex extruded nose gives **12.15 GPa**, not 4.67 GPa (flat face). Elastic pressure here is a sizing warning, not a dent-depth prediction. A shaped barrel with a 1.045 mm travel radius, 20 mm transverse radius and 0.60 mm nose instead gives 3.38 GPa, semi-axes 0.022 and 0.275 mm, *only while* the patch remains on both full rolled profiles. This is not a form that can simply replace a ball: a separate axial-keeper barrel would have a tangential axis, a distinct shear-cheek barrel a radial axis. Their shifted lines of action, free-end clearances, web strength, phase and all mixed-contact force bounds must be recomputed before adopting such stations. A larger radius adds stroke. Neither result rates a custom material section. The 43.1 N is a study case, not a v7 certified upper load.

A [KSS FBS01800.5A](https://www.kssballscrew.com/us/pdf/catalog/PBS_Single_Nut_with_Flange.pdf) recirculating nut is a real alternative to a sliding power screw: Ø1.8 shaft, 0.5 lead, Ø6 nut, 14 mm flange and **8.5 mm nut length**, catalogue dynamic/static 110/130 N. The nut plus 7.60 mm travel takes at least **16.10 mm** before journal, travel runouts, bearing, driver and end stops. It is not a drop-in for a ~1.56 mm engaged sliding nut, and the supplier's basic load ratings are not a recovery claim.

## Comparison after run 12 (not a new declaration)

* [Internal drive](shuttle.md): permanently engaged four-start threads remove the direct last-flank problem, but not the load/position proof for the downstream jaws.
* [Crossed crown](barrel.md): the [12° added curvature](crown.py) removes the straight-side seam. The [partial pose](attitude.py) still puts contact on a sharp intersection even before a finite pressure patch is considered.
* [Larger spheres](cylinders.md): permissible in the closed geometry is not the same as permissible throughout withdrawal. Releasing one keeper admits 12° about a chord, beyond the 3° fixture assumption.
* [Physical stack and moving rim](drawbolt-take17.md): the shallow linear drive is 4.07 mm too long; the short rise needs 56.4 N mm against 49.03 rated. The 4:1 rotary alternative needs 86.7% loaded efficiency for the studied sliding guide. The partial shoe of the pivot alternative intersects the tail rim by 0.112 mm.
* [Pivot discriminator](swing.py): another section uses R2 spheres, not the stack's R1.75. Allowing just 1.5 mm outward drift defeats a uniform positive opening-moment bound. A *hypothetical* 22° guard with 2 mm longitudinal slot can give 0.936 N mm/N net opening moment on its modelled adverse meridian. It requires coverage out to x=5.258 mm from locked centre, an actual guard attachment, accessible pivot and a release under load of the structural backstop. The section omits the ends and shell; the interval only spans front-side contacts and slightly past the positive equator, not backside contact or motion through the slot. No assembled guard, strength, or reverse claim.

All these are component studies, not official results. In particular the different sizes, friction bounds and fixture postures cannot be combined into a v8.
