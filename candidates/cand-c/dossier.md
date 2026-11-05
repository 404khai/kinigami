# cand-c: internally actuated spherical shell (Family C), version 1

Status: Gate 1 paper dossier, label `exploratory`. Declaration: `declaration.json` (schema_version 1). Decisions: Q11, Q12, Q31, Q36, Q37, Q38, Q61, Q62. Requirements: ENV-003..005, CPL-005, CPL-009, SEL-001, SEL-005, SEL-009.

**Headline.** This is a coherent but weak candidate. On paper it is expected to **fail G5** (a sphere rests on one point, the static-support test needs three) and to be `unresolved` on G3, G6, G7 and G8. I did not add flats or feet to pass G5, since that would change the design to suit the gate. It can hold a chain, but it has no actuator that applies torque at a joint, and it has no steering. Details are in sections 1 to 9.

Conventions: every number is **[S]** sourced, **[D]** derived (formula given), **[P]** provisional design choice, or **[U]** unresolved. Access date for every URL is 2026-11-04.

## 1. Concept

A near-spherical PA 2200 shell rolls about its own chain axis (x). Inside, a **chassis hangs from the shell like a pendulum** (the shell turns on pole bearings around it). A gearmotor turns the shell relative to the chassis, and gravity on the offset chassis centre of mass supplies the reaction torque. The couplers sit on the roll axis at the two poles, on the chassis, so they do not turn with the shell:

- **Head site (+x):** a 6 mm steel ball on a ram. Stowed, it sits inside the shell. Deployed, it is 1.5 mm beyond the shell surface.
- **Tail site (-x):** a socket with a lead-in funnel and two spring-preloaded jaws.
- Units join head to tail. The joint is a ball-and-socket with three rotational degrees of freedom, held against separation by the jaw springs.

Family C deviation: the tail socket is a fixed recess, not a retractable site. Only the head is retractable.

## 2. Geometry

| Quantity | Value | Basis |
| --- | --- | --- |
| Shell outside diameter (stowed and deployed) | 59.000 mm | [P], 0.5 mm margin per side |
| Shell inside diameter (cavity) | 56.000 mm | [P], 1.5 mm wall |
| Pole aperture radius | 5 mm | [P] |
| Stowed envelope (G1) | diameter 59.000 mm, so < 60 mm | [D], the stowed ball (to x = 25 mm) and tail socket (to x = -28.4 mm at its rim) lie inside the shell sphere |
| Head ball centre, deployed | +31.0 mm from the unit centre | [P] |
| Tail seat centre | -29.0 mm | [P] |
| Centre spacing in a chain | 60.0 mm (1.0 mm gap between shells) | [D], 31 + 29 |
| Ram stroke | 9 mm (ball centre 22 to 31 mm) | [P]; no declared mechanism produces it |
| Max joint angle before shells touch | about 21 degrees | [D], law of cosines with 31 mm and 29 mm arms and 59 mm contact distance |
| Deployed length of a 5-unit chain | 4 x 60 + 59 = 299 mm | [D] |

The stowed state is the rolling state. The deployed state only differs by the head ball being out.

## 3. Q12 packaging

Stowed envelope: 59.000 mm, so G1 passes with 1.0 mm of margin on the diameter (computed exactly, since the shell is one sphere centred on the origin).

Layout (centres in mm, x along the chain, z up, dimensions as boxes in the declaration). Containment in the 28 mm cavity radius and pairwise non-overlap were checked by my own script, using the protocol's 1 µm erosion rule. All 12 non-placeholder boxes pass, with the tightest at 27.8 mm. The packing was found by a greedy grid search, so it is one feasible layout, not an optimised one.

- Battery low and central (z = -12); motor at z = -4; microcontroller upright at x = -9; IMU at z = -20; chassis floor plate at z = -23.
- Servo above the axis at z = +10, so mass stays low and the ram axis stays free.
- Ram cartridge and ball on the head side; socket cartridge on the tail side; pole hardware at |x| = 26.6.

**Assembly access (statement, not a design).** Two halves split on the plane perpendicular to the chain axis; the chassis is built first and each half is slid over its pole cartridge; the halves join at the rim by screws. No fixture, screw count or rim geometry exists. [U]

**Packaging is very tight.** Two servos did not fit alongside the other parts in my search, which is why the tail socket has no actuator. The servo-to-ram linkage and the 9 mm stroke have no volume allocated beyond the cartridge box. Treat G2 as passing on declared boxes only.

## 4. Component list

Purchased parts were opened by web fetch or search on 2026-11-04. Where the fetch failed or only a search summary supported a value, this is said.

| Component | Part | Mass | Dimensions (mm) | Source (accessed 2026-11-04) | Notes |
| --- | --- | --- | --- | --- | --- |
| battery | Turnigy Nano-Tech 300 mAh 1S, 45C/90C | 8 g [S] | 43 x 17 x 6 [S] | https://speedyfpv.com/products/turnigy-nano-tech-300mah-1s-lipo-battery-pack-3-7v-45c-90c-nine-eagles-solo-pro | Retailer listing. The HobbyKing page (https://hobbyking.com/en_us/turnigy-nano-tech-300mah-1s-45-90c-lipo-pack-fits-nine-eagles-solo-pro-100.html) returned 403, so it was not read. Other listings of the same name give different sizes. No manufacturer datasheet found. |
| controller | Adafruit ItsyBitsy nRF52840 Express | 3.0 g [S] | 36.0 x 17.6 x 5.3 [S] | https://www.adafruit.com/product/4481 | Page gives no current figures. |
| IMU | Adafruit BNO055 breakout | 3 g [S] | 20 x 27 x 4 [S] | https://www.adafruit.com/product/2472; Bosch datasheet https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bno055-ds000.pdf | Datasheet states 12.3 mA typical, normal mode, VDD 3 V (read from the PDF). |
| drive motor | Pololu 75:1 micro metal gearmotor HPCB 6V | 9.5 g [S] | 10 x 12 x 25 [S] | https://www.pololu.com/product/3074/specs | 6 V, no-load 430 rpm / 0.15 A, stall 1.1 kg-cm / 1.5 A. Run at 3.7 V (see risks). |
| motor driver | Pololu DRV8833 carrier | 1.0 g [S] | 12.7 x 20.3 [S], thickness 3 [U] | https://www.pololu.com/product/2130/specs | 2.7 to 10.8 V, 1.2 A continuous, 2 A peak per channel. |
| ram servo | TowerPro SG92R micro servo | 9 g [S] | 23 x 11 x 29 [S] | https://www.adafruit.com/product/169 | Page gives no stall current. Secondary sources conflict (560 to 750 mA). |
| ball | 6 mm chrome steel ball, grade 25 | 0.882 g [S] | 6 [S] | https://m.reach.dog/shop/pgn-bearings/products/6mm-chrome-steel-grinding-media-balls-1kg-g25-precision | From a search summary; page not opened. |
| shell halves (x2) | PA 2200 laser sintered | 7.137 g each [D] | see 2 | https://www.shapeways.com/wp-content/uploads/sites/3/2021/10/Material-Data-sheet-Nylon-12-PA2200.pdf | Density 930 kg/m3 from a search summary of EOS datasheets; this PDF link was not opened. Volume 7674 mm3 [D] = (2/3) pi (29.5^3 - 28^3) - pi x 5^2 x 1.5. |
| chassis frame | custom PA 2200 | 4 g [U] | plate 20 x 20 x 2 [U] | n/a | Allowance. |
| head cartridge | custom | 2.5 g [U] | 6.5 x 9 x 9 [U] | n/a | Allowance. |
| tail cartridge | custom | 2.5 g [U] | 13 x 9 x 9 [U] | n/a | Allowance. |
| pole hardware (x2) | bearing, ring gear, fasteners | 1.5 g each [U] | 2 x 6 x 6 [U] | n/a | Bearing part not selected. |

The declaration cites a single `source` per component. Where the power or mass basis rests on a second document, it is named in that component's description.

## 5. Mass and power budgets

**Mass.** Sum of components: **60.656 g** (declared total 60656 mg, equal to the sum). The shell halves are 14.274 g of it. The rotating shell is 23.5% of the total mass; the chassis is 46.4 g with its centre of mass 4.5 mm below the roll axis [D, from box centres].

**Pendulum torque.** Maximum gravity torque at a 90 degree swing is 0.0464 kg x 9.81 m/s2 x 0.0045 m = **2.05 mN m** [D]. The motor's stall torque scaled linearly to 3.7 V is about 66 mN m [D, assumes torque proportional to voltage], so the drive is limited by the pendulum, not the motor. The tractive force at the contact is at most 2.05 mN m / 29.5 mm = **0.07 N** [D]. That bounds how hard a unit can push a neighbour.

**Peak power** (G4 rule, worst case, all at once): 54 (controller) + 46 (IMU) + 3423 (motor) + 2775 (servo) = **6298 mW**. The source limit is 3.7 V x 13.5 A (45C x 0.3 Ah) = **49950 mW**. Margin is large, but the controller and servo figures are [U] (see section 9).

**Energy and endurance (reported only).** Nominal energy 3.7 V x 0.3 Ah = 3996 J [D]. The assumed average draw is 436 mW (controller CPU 11, IMU 46, motor no-load 342, servo idle 37), giving 9.2 x 10^6 s. **This figure is not meaningful**: it assumes nominal rather than usable energy and a motor that runs at no-load current, not under load. The endurance threshold stays unresolved (Q62).

## 6. Coupler layout (design guidance 4.2)

| Question | Answer |
| --- | --- |
| Align | Closing is by rolling, along the chain axis. The funnel on the tail socket corrects lateral and angular offset by contact with the ball. Funnel half angle and depth: [U]. The ball sits 1.5 mm beyond the head shell, so a closing unit reaches it before the shells touch. |
| Latch | The ball pushes past the throat, opening the two jaws against their springs, then they close behind it. No actuator is needed to latch. |
| Transmit force | Tension and compression through the ball and jaws, then into the chassis (not the shell). Shear is carried by the ball in the seat. Joint stiffness and strength: [U]. Bending and torsion are not transmitted: the joint is free to swivel (friction only). |
| Detach | The head servo retracts the ram, pulling the ball out against the jaw spring force (bounded by the spring preload). A unit cannot release its own tail socket. Jam and partial-release behaviour: [U]. |
| Power and data | **None through the coupler in this version.** Data goes by the controller's 2.4 GHz radio, which is not short-range by nature (range limiting is a Gate 2 modelling matter, Q33). Power transfer is not offered (Q34). |

Docking pushes: the head ram's thrust pushes the two free-rolling units apart. The design therefore closes by rolling, with the ball already deployed, so capture depends on approach speed. The approach is only possible along the unit's own axis, which the unit cannot steer (section 8).

## 7. Passive retention and pre-alignment

**Retention when unpowered:** the two spring jaws hold the ball with no power (kind `spring_preload`). Retention force depends on spring rate, preload and jaw geometry, none of which is designed [U]. Passive retention of *shape* is not claimed: the ball joint swivels, so a bent chain is held only by joint friction and ground contact.

**Pre-alignment:** geometric funnel only, acting through contact while the units close. **No magnet is declared or assumed.** The funnel's ability to capture across a measured offset window is for Gate 2 to measure (Q36 item 2); it is not claimed here. An independent review record for G6 does not exist yet.

## 8. Q31: holding and articulating a three- to five-unit chain

**Holding the chain.** A unit rests on its shell at one table point, with the pendulum chassis keeping it upright. Adjacent chassis are joined by the ball joints, so the chain can sit straight on the table with every joint engaged. It is stable against rolling over because each chassis hangs below its axis. It has **no static support polygon** per unit, and no yaw stiffness at the joints. The 3-unit chain geometry has centres 60 mm apart and no shell contact when straight.

**Articulating the chain (what can work).** Each unit rolls about its own axis, which is the chain line, so it moves sideways. A middle unit that rolls sideways while its neighbours' drives hold their shells still would push the chain into a bend: each ball joint turns up to about 21 degrees before shells touch, so a 5-unit chain has about 84 degrees of total joint travel. Holding the end units requires their gearmotors to resist rolling, which means power (the gearbox is not stated to be non-backdrivable).

**Why this probably does not reach the Q31 benchmark.**

1. No actuator exerts a torque *at a joint*. Bending only happens through table friction on one unit, at most about 0.07 N (section 5), against free-rolling neighbours with near-zero friction.
2. Curvature cannot be held without power. The chain is neutrally stable when bent, and any disturbance moves it. There is no brake or lock on the joint.
3. There is **no steering**. A shell rolling about the chain axis can only move perpendicular to it. Joining separate units end to end needs a yaw actuator. I tried a vertical reaction wheel, but its motor did not fit in the cavity. Q31 starts from an already engaged chain, so assembly is outside Q31, but it limits what units can do on their own.
4. Whole-chain translation does not count, and most motions that this drive produces are whole-chain translation.

**Conclusion (reported as asked).** The units can **hold** a chain (engaged, passively retained, gravity-stabilised) but, with the declared parts, **cannot be shown to articulate it** on paper. The only candidate mechanism is the sideways-rolling bend described above; whether it produces a controlled curvature change is a Gate 2 question and I rate it unlikely. I recommend the owner treat articulation as the main weakness of this family.

## 9. Risks and unknowns

1. **G5 will fail.** One shell contact point per unit gives no support polygon. Flats or feet would fix the test but would remove free rolling or move the design toward Family A. I did not add them.
2. Joint torque, steering and docking by rolling are the weaknesses of section 8.
3. Servo stall current, controller radio current and motor-driver thickness are not read from their cited pages. The power figures rest on search summaries. Peak margin is 7x, so the pass is not sensitive.
4. The 6 V motor runs at 3.7 V. Stall torque and speed are scaled linearly [D]; real values are lower after the driver's drop.
5. A Li-ion supply sagging below about 3.3 V may stop the BNO055 breakout's regulator (checked against nothing here).
6. The servo is hobby-grade, with no life rating on the cited page; the ram linkage and 9 mm stroke have no mechanism.
7. PA 2200 shell at 1.5 mm wall: strength, stiffness and rolling-contact wear are unchecked. Surface friction and rolling resistance with the tabletop (Q21) are unknown, and for a point contact are dominated by effects the Q37 envelope may not cover.
8. Bearings and ring gear (mass 3 g allowance) are undesigned. If the real bearing is heavier, it lowers the margin but does not affect G1.
9. Wires: all electronics sit on the chassis, so no slip ring is needed. This holds only while no actuator sits on the shell. The pole bearing must pass the ball stem.
10. Statics: when the chain bends beyond about 21 degrees the shells touch and become a rigid obstacle.
11. The 3-unit gate test uses nominal positions and cannot see the dynamics above.

**Expected Gate 1 outcome (my reading of the protocol; the evaluator was not run).** G1 pass (59.000 mm). G2 pass. G3 unresolved (estimate bases on several components). G4 pass (mass sums exactly, peak 6298 mW < 49950 mW, endurance reported only). G5 fail. G6 unresolved (no independent record). G7 and G8 unresolved (no review). Candidate outcome would be **fail** because of G5. `src/core/gate1_eval.zig` exists untracked in the checkout and may be used to confirm; I did not run it.

## 10. Author self-check against the corpus

This is the author's preliminary view for the reviewer. It is not the Q61 review and has no independence. Ratings: none / low / moderate / high (Q61 anchors). Sources are the corpus entries in `docs/originality/reference-corpus.md`.

| Reference | D1 geometry | D2 coupler | D3 motion | D4 assembly | D5 visual | Note |
| --- | --- | --- | --- | --- | --- | --- |
| A1 Big Hero 6 microbots (F1) | none | none | none | low | low | Single large round units, mechanical ball joint, no swarm flow or needle form. |
| B1 Replicators | none | none | none | low | none | |
| C4 ATRON | **moderate** | low | low | low | moderate | Also a sphere of two hemispheres with connector pockets. Differences: the split is perpendicular to the chain axis, both halves rotate together, no relative hemisphere motion; two ball-and-socket sites on the axis instead of eight hooks; no lattice. |
| C16 FreeBOT | moderate | low | low | low | low | Also a sphere that rolls. Differences: no magnets or ferromagnetic shell; sites are fixed points; two motors are replaced by one pendulum drive. |
| C6 Roombots | low | low | low | low | low | Peanut-shaped spheres, three joint motors. |
| C10 Claytronics catoms | low | none | moderate | low | low | Rolling spheres; but here rolling is a table roller on its own axis, with no neighbour-rolling. |
| C7 / C8 M-Blocks | none | none | low | low | none | Internal mass acts on a shell, but gravity pendulum on a sphere, not a braked flywheel on a cube. The Q62 exclusion "cube with an internal flywheel" is **not present**. |
| C17 HyMod | low | low | low | low | low | Spherical joint core inside a cube lattice. |
| C21 Swarm-bots | low | low | low | low | low | Round body, gripper. |
| others (C1 to C3, C5, C9, C11 to C15, C18 to C20, C22, C23, D1 to D4) | none to low | none to low | none to low | none to low | none to low | Cubes, chains, kits; shared features are generic. |

**No cell is rated high.** The needle- or particle-like silhouette exclusion is **not present**.

**Corpus gap the reviewer must close.** The corpus lacks rolling spherical robots with an internal drive (for example commercial spherical toy robots and the pendulum-driven spherical robot literature). They are the closest references for D1 and D3 of this candidate. I did not search for them. The reviewer should add them and rate D1 and D3, and should check whether any rate high. The shell, internal pendulum drive and roll axis are likely shared in kind with them; what I believe is different is the chain-native couplers on the roll axis, which I could not confirm against a reference.

## 11. Unresolved items

- G3: estimate-basis masses and sizes (chassis, both cartridges, pole hardware, driver thickness, shell placeholders) and estimate-basis power (controller, servo, driver).
- G4: endurance threshold (Q31 duration); usable (not nominal) energy.
- G5: expected fail.
- G6: independent retention review; funnel, spring and jaw numbers.
- G7 and G8: independent Q61 review, corpus extension for spherical robots.
- Servo-to-ram linkage and stroke; jaw and funnel geometry; bearings and gear; assembly fixture and fasteners.
- Joint strength, stiffness and release behaviour; yaw/steering actuator.
- Coupler data and power paths: none declared.
