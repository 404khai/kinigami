"""cand-d v6 rear cartridge, in mm, N and N mm. Not a gate evaluator.

Dimensions are design callouts; ATI 304 and C95400 properties are from the
declaration's material sources. The press tool and spacer are assembly tools,
not onboard actuators. Nothing is pressed over an oversize tube.
"""
from math import asin, degrees, hypot, pi, sqrt

REAR_FACE = 30.35          # sleeve rear thrust shoulder when loaded forward
SKIRT_START = 24.35
SKIRT_RI, SKIRT_RO = 5.035, 6.30
JOURNAL_R = 3.50
LAND_START = 27.16        # solid tail of the one-piece housing, annular tip recess
BORE_FLOOR = 29.80        # flat-bottomed from front; not a drill point
COLLAR_FRONT = REAR_FACE - 0.09
COLLAR_RI, COLLAR_RO = 3.5175, 5.02125
PIN_X, PIN_D = 28.65, 2.20
TOOL_D, HEAD_D = 2.70, 2.50
YIELD_PH = 1170.  # certified AMS 5643 H900 bar; do not upset this part
TIP_X, BOSS_X, WEB_X = 25.35, 22.72, 25.95
PLATE_X, PLATE_END = 23.35, 24.15
DOG_RI, DOG_RO = 5.64, 6.24
DOG_X0, DOG_X1 = 29.35, 30.00  # broadened tip; only the pad, not the shank, bears


def fit():
    shaft_od = (6.980, 7.000)
    collar_id = (7.025, 7.045)
    collar_od = (10.040, 10.045)
    sleeve_id = (7.015, 7.025)
    skirt_id = (10.070, 10.080)
    clearance = (collar_id[0] - shaft_od[1], collar_id[1] - shaft_od[0])
    # Rear collar OD is a second journal. Acceptance applies to the
    # pinned assembly, not just its loose components. Sweep at BOTH ends
    # of each land (coaxiality, tilt, form combined); worst radial error.
    offset = (.005 + .005)/2
    skirt_gap = (skirt_id[0] - collar_od[1]) / 2 - offset
    # Relieved front face, radial float at both stations, and TIR.
    thrust_overlap = (collar_od[0] - sleeve_id[1]) / 2 - .10 - .025 - .070 - offset
    # The head and collar are match-reamed with a removable feeler between
    # the *actual* thrust faces. Two radial hole clearances add to one
    # diametral clearance. Allow another 10 um total axial face/runout error.
    play = (2.212 - 2.190) + .010
    end_play = (.085 - play, .095 + play)
    tip = 36.4 - 6.5 - .050  # length, tooth form and datum allowance
    bottom = max(BORE_FLOOR + .015, PIN_X + .015 + 2.212/2)
    assert BORE_FLOOR - .015 > PIN_X + .015 + 2.212/2
    assert clearance[0] > 0 and skirt_gap > 0 and thrust_overlap > 0
    assert end_play[0] > 0 and tip > bottom
    return clearance, skirt_gap, thrust_overlap, end_play, tip - bottom


def stresses(thrust, single_side):
    """Pin shear, pin root von Mises, collar/front edge shear, bearing (MPa).

    One lip carrying everything bounds asymmetric running contact. For the
    severe blocked-drive diagnostic also show symmetric reactions separately;
    neither resultant proves equal dynamic load sharing.
    """
    d, bore = 2.190, 1.05
    wall_min = (10.040-7.045)/2 - .10 - .32
    edge = COLLAR_FRONT - .05 - (PIN_X + .015 + 2.212/2)
    sides = 1 if single_side else 2
    load = thrust / sides
    tau = load / (pi*(d*d-bore*bore)/4)
    # Resultant at outermost lip, not at the centroid of its bearing strip.
    lever = (10.045-6.98)/2 + (7.045-6.98)/2
    bend = load*lever / (pi*(d**4-bore**4)/(32*d))
    return tau, hypot(bend, sqrt(3)*tau), load/(2*edge*wall_min), load/(d*wall_min)


def part_volumes():
    # The sleeve shoulder is one piece with the integral skirt. The pin passes
    # through solid steel at the rear of the blind guide. The small upset
    # replaces material removed by the two countersinks (ignored in net mass).
    hole = pi*(PIN_D/2)**2
    # Book the draw-rivet inside the tube as solid pin material; also add
    # both washer/head counterbores as solid 304 without deducting their seats.
    pin = pi*(PIN_D/2)**2 * 2*COLLAR_RO
    collar = (pi*(COLLAR_RO**2-COLLAR_RI**2)*(COLLAR_FRONT-LAND_START)
              - 2*(COLLAR_RO-COLLAR_RI)*hole)
    skirt = (pi*(SKIRT_RO**2-SKIRT_RI**2)*(REAR_FACE-SKIRT_START)
             - 2*(SKIRT_RO-SKIRT_RI)*pi*(TOOL_D/2)**2)
    return collar, pin, skirt


def strip(r, h):
    """Area inside a circle between two chords a distance 2h apart."""
    return 2*(h*sqrt(r*r-h*h) + r*r*asin(h/r))


def cartridge_volumes(slot_end, guide_width, spring_volume, spring_density,
                      cam_stages, lug_tip, lug_half_height):
    """Per-material upper volume/mass, including intentionally nested parts.

    Small chamfers, tooth/profile relief, spring slots and dog-sector pockets
    are charged as stock, not negative masses. Spring volume includes legs.
    Intersecting a component AABB is not a check of these internal fits.
    """
    collar, pin, skirt = part_volumes()
    head_rear, tube_front, sleeve_front = LAND_START, 35.60, 35.30
    bore = 2.005
    tube = pi*JOURNAL_R**2*(tube_front-head_rear) - pi*bore**2*(tube_front-BORE_FLOOR)
    tube -= (strip(JOURNAL_R, guide_width/2)-strip(bore, guide_width/2))*(tube_front-slot_end)
    # Cross-bore volume lower bound, inscribed prismatic length. Its
    # possible intersection with the flat-bottom guide is not subtracted twice.
    tube -= pi*(PIN_D/2)**2*2*sqrt(JOURNAL_R**2-(PIN_D/2)**2)
    bronze = skirt + pi*(SKIRT_RO**2-3.5075**2)*(sleeve_front-REAR_FACE)
    # Debit only the swept lug material known to be in the sleeve: at the
    # angular centreline of each lug, at every r in [3.55, lug_tip] its crown
    # occupies this axial interval. Clip at the sleeve faces. Ignore enlarged
    # clearances and radiused ends. Two diametrically opposed tracks do not
    # overlap. The minimum at the stage endpoints bounds all interior depths.
    def inside_height(depth):
        centre = 36.40 - depth
        return max(0., min(sleeve_front, centre+lug_half_height) -
                   max(REAR_FACE, centre-lug_half_height))
    for start, finish, lead in cam_stages:
        arc = (finish-start)/lead
        bronze -= (lug_tip**2-3.5125**2)*arc*min(inside_height(start), inside_height(finish))
    ring = pi*(4.4**2-3.6**2)*.30
    # Hub boss is boxed separately between its rear end and x24; count the
    # remaining stock here. The rocker screw is charged in the screw BOM.
    # Charge solid outer stock for the web and finger, less through-socket;
    # include the M1.7 screw by solid upper shank and head cylinders.
    boss = pi*2.85**2*(WEB_X-PLATE_X) - pi*1.70**2*(TIP_X-PLATE_X)
    plate = pi*(6.24**2-2.85**2)*(PLATE_END-PLATE_X)
    finger = (DOG_RO-DOG_RI)*3.6*(DOG_X1-PLATE_END)
    lengths = {"17-4 H900": tube+collar+boss+plate+finger,
               "pin/keeper upper at 304 density": pin + 2*pi*(HEAD_D/2)**2*.32,
               "C95400": bronze, "PTFE": ring, "spring": spring_volume}
    densities = {"17-4 H900": 7810., "pin/keeper upper at 304 density": 7900.,
                 "C95400": 7450., "PTFE": 2150., "spring": spring_density}
    return lengths, sum(lengths.values()), sum(lengths[k]*densities[k] for k in lengths)


def drive_checks(torque):
    # Radially shallow arc groove leaves a continuous inner skirt rim.
    # The 3.60-wide tip engages; the shank is relieved to 3.20 across.
    # Size for load on the farthest corner (not at the pad centroid).
    force = torque/DOG_RI
    z = .55*3.10**2/6
    dog_bend = force*(DOG_X1-PLATE_END)/z
    # Axial stop face runs the full groove depth (x24.35..30.25);
    # throughout end play the entire pad lies within that long stop face.
    assert DOG_X1 + .127 + .05 < 30.25
    contact = (DOG_X1-DOG_X0-.05)*.50
    bearing = force/contact
    # 28T spline: captured with a one-piece duplicate female form, qualified
    # against the actual mating part. The male spline is part of the rated
    # servo, not separately credited an invented yield strength.
    hub_to_case = BOSS_X-.015 - 22.575
    hub_to_skirt = SKIRT_START-PLATE_END - .127 - .025 - .015
    assert min(hub_to_case, hub_to_skirt) > 0 and dog_bend < YIELD_PH and bearing < 221.
    assert 298 > 257.1 + 2*degrees(asin(3.65/(2*DOG_RI))) + 2
    return dog_bend, bearing, hub_to_case, hub_to_skirt


def report():
    clr, radial, overlap, play, bottom = fit()
    print("collar diametral slip %.3f..%.3f mm; centered skirt clearance >=%.4f; thrust overlap >=%.3f" %
          (*clr, radial, overlap))
    print("forward/rear thrust endplay %.3f..%.3f mm, pilot-to-bottom >=%.3f mm" %
          (*play, bottom))
    # Size for a 30 N service reaction, exceeding the full externally
    # applied load combination calculated by coupler.py. This is a design
    # capacity, not a new candidate load, current limit or measured value.
    for thrust in (30., 530.):
        reaction = stresses(thrust, True)
        print(("%.0f N all on one side: pin mean shear %.1f, combined stress %.1f, "
               "collar edge shear %.1f, bearing %.1f MPa") % (thrust, *reaction))
        assert reaction[1] < YIELD_PH and reaction[2] < YIELD_PH/sqrt(3) and reaction[3] < YIELD_PH
    # Housing free-edge shear toward the back of the pin hole; count two
    # planes only through the outer 2 mm of the tube on the more loaded side.
    # The central r2.15 screw recess ends by x27.48. Only count the
    # unaffected stock at radii 2.20..3.20 along the pin, plus the deeper
    # ligament from x27.48 along the next 1 mm inward. Both shear planes.
    ligament = PIN_X-.015-2.212/2-(LAND_START+.015)
    inner = PIN_X-.015-2.212/2-27.48
    tau_tube = 530./(2*(ligament + inner))
    print("housing rear shear-out, 530 N: %.1f MPa vs %.1f; fault recoverability not established"
          % (tau_tube,YIELD_PH/sqrt(3)))
    for torque in (49.03,176.5):
        print(("%.1f N mm dog: bend %.1f MPa, bearing %.1f MPa; "
               "min hub-case %.3f and plate-skirt %.3f mm") % (torque,*drive_checks(torque)))
    print("collar, rivet and skirt gross-minus-tool-port volumes (mm3): %.1f %.1f %.1f" % part_volumes())


if __name__ == "__main__":
    report()
