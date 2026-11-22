# Can the button be guided and the boards relocated?

**Exploratory.** The [finite guard](../cand-d-parked-button/README.md) protects a short parked support, not the [installed drive](button-take44.md). Relocating the electronics alone cannot repair the latter. The five-slot coupon below has no installed moving bridge or dog. No candidate, criteria or Gate 1 result changes.

## Local load and support

The R7.5 eye carries an R4.2 tube and three equal-radius bosses. [Six tangent planes](button_seats.py) surround an inclined datum with 11 mm pitch radius and 58° flank angle. The register study asks whether nonnegative normal reactions **exist** under the 70 g service, table and fault wrench boxes; it does not prescribe their division. With .47 mm cone pressure-centre uncertainty and the stated angle errors the sufficient resultants along the datum are 32.56, 56.83, 42.41 N. A provisional measured net face output of 64–76 N axially gives 58.59–91.19 N along that datum in the [registered calculation](button_home.py). It needs loaded pose/patch bounds: .010 mm effective gaps at the lands and .030 at the button admit a small local cage bound; .020/.060 do not close this test. No physical gap or preload is inferred.

Charging **all** 295.66 N of the normal-force bound to one land gives 3.51 GPa sphere/plane Hertz pressure. A Ø2.4 × 4 backing stem at .55 eccentricity and friction .23 gives 390 MPa nominal von Mises in [the section](button_roots.py). This does not rate the land, fillet, truncated patch or root under repeated contacts. Two bases have just .405 mm nominal clearance to the seated torus. The [cone](slotted.py) gives positive lift on the sustained tapered flank after 1° and friction .23, not on an exposed shoulder. Use the **actual** hood width, nose and skin in the guard study, not a rounded-up straight-lip coefficient.

The [guide coupon](slot_guide.py) uses five one-sided-at-a-time, opposed-wall rolling constraints to bound side reactions and parasitic work; it allows arbitrary traction along the axle. For the moving-roller, 12 mm vertical span, 10 mm half-width and 12 mm aft offset case, use the five roller centres in [the stock](slot_stock.py); the lower group starts at z=−4. Dimension, positional error, side traction .23, rolling ratio .005 and no end-face rub are **assumptions**. The tracks have .815 mm nominal separation from other rollers/studs, and .615 mm from each other before installation. For comparison see the [IKO miniature follower catalogue](https://www.ikont.co.jp/eg/product/needle/), CFS1.4WV with Ø4 roller: 105 N maximum allowable load. A catalogue follower does not rate its stud mounting, the slot stiffness, breakaway, overhung bridge or lock. In fact, after lowering the interface, the central upper track occupies the fixed hinge knuckle (see Take 44).

## Electronics placement, not a whole-machine packing result

[Search](electronics.py): enclose each electronics box in a 29.8 mm trial radius, above z=−23.1. Exclude named convex stock at the joint, feet, subsidiary boards, face, guide slots, moving rollers and **entire occupied volume** of the guard (including its void); in the full model also exclude both routed drives and bridges. Use direct X sweep of the mated terminal, own articulated tail, plus both adjacent head/drive envelopes at p36 over ±15° and up to 16.8 mm relative translation. Five-degree yaw samples expanded by the maximum chord sag enclose each vertex arc. For horizontal-axis cylinders the replacement ball sweep is conservative. Boxes must separate on a specific unit axis by at least .30 mm beyond the yaw debit. Selected boxes also clear their repeated copies. These checks do not test separated free-body recontact, material-to-material feasibility of the named obstacles, or omitted harness, mount and shell design. Sphere checks apply to the tested boxes, **not** to the entire assembly.

The slice search samples XY at 1 mm and solves admissible height **intervals** for each sampled orientation. A grid miss is not an impossibility theorem.

| Input (mm, centre and alignment) | Witness against the indicated stock |
|---|---|
| Unshifted core, sphere centre (−3,0,0), original 20.70 × 30.66 × 5.40 cell | Cell at (−6,0,−19.055) with original axes and MCU at (2,−20,0), axes (+Z,−X,+Y), clear named stock by .335/.434 mm. **No drive volumes** in this core screen. |
| Full route at −7, sphere centre (−3,0,−2), original cell | No original cell position certified in this search; not a universal lower bound. |
| Same full route, smaller cell allocation 33.4 × 12.1 × 3.1 | Cell at (−14,−1,12.318), axes (+Y,+Z,+X), and MCU at (−3,0,20.963), axes (+Y,−X,+Z), clear enumerated stock by .359/.713 mm. Minimum separation in the mutual/repeated cross-pair test .550 mm. |

[Spektrum EFLB0701S](https://my.spektrumrc.com/Products/Default.aspx?ProdID=EFLB0701S) lists 33 × 11.7 × 2.54 mm, 70 mAh, 3.7 V, 1.0 A continuous. The larger search box is an allocation, **not** verified swelling, protection, connector or bending room. Its rated nominal power is only 3.7 W and nominal energy .259 Wh. No credit for serialising peaks at G4. It cannot be substituted without a cited simultaneous peak-power budget, protection circuit, connector, mounting and adequate loaded voltage. In particular, the three non-electronics material points from Take 44 still require at least **64.791 mm** for that lowered drive.

From this directory (Python 3 with NumPy and SciPy):

```sh
export OPENBLAS_NUM_THREADS=1
for s in slotted button_seats button_home button_roots slot_guide slot_stock; do python3 -B "$s.py" || exit 1; done
python3 -B electronics.py --slices --grid 1 --model core --shift 0 --origin -3 0 0
python3 -B electronics.py --slices --grid 1 --model full --shift -7 --origin -3 0 -2
python3 -B electronics.py --slices --grid 1 --model full --shift -7 --origin -3 0 -2 --cell 33.4 12.1 3.1
```
