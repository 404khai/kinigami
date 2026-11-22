"""Exploratory dimensional/force inequalities; NOT a declaration or gate.

All lengths mm, forces N, moments N mm, angles degrees. Provisional
finished feature limits, not a claim that any manufacturing process meets them.
"""
from math import asin, cos, degrees, radians, sin, sqrt, tan


def radial_limit(stroke, dwell, throw, shallow, steep):
    # dr/tan(shallow) + (throw-dr)/tan(steep) + dwell <= stroke.
    inv_low, inv_high = (1 / tan(radians(x)) for x in (shallow, steep))
    return (stroke - dwell - throw * inv_high) / (inv_low - inv_high)


def window(radius, gap, wall_deg, form_debit_deg, friction):
    """Only for a continuous sphere supported by edges bordering a window."""
    half = gap / 2
    if not 0 <= half < radius:
        raise ValueError("sphere not supported across window")
    theta = asin(half / radius)
    effective = radians(wall_deg - form_debit_deg) - theta
    return (radius-sqrt(radius**2-half**2), degrees(theta),
            sin(effective)-friction*cos(effective))


if __name__ == "__main__":
    for dwell, a, b in ((0, 12, 35), (.15, 11, 34)):
        print(f"1.1 stroke at {a}/{b} deg, dwell {dwell:.2f}:"
              f" loaded radial budget {radial_limit(1.10, dwell, .55, a, b):.3f}")
    required = .42 / tan(radians(11)) + .13 / tan(radians(34)) + 1.04
    print(f"Required stroke {required:.3f}, before blend and independent ejection.")
    for radius, wall in ((.98,29),(.55,29),(.55,40)):
        depth, angular, axial = window(radius,.38,wall,2,.23)
        print(f"R={radius:.2f} g=.38 wall {wall}: intrusion {depth:.3f},"
              f" normal debit {angular:.2f} deg, min axial/N {axial:.3f}")
    for m in (.046,.050):
        opposed = 5*m*9.80665  # 4W compression plus W table drag
        print(f"{m*1000:g}g: 3.0 pusher allows {3.0-opposed:.3f} other drag")
    # Reproduce the limiting cases independently of a gate .json.
    assert 0 < radial_limit(1.10,.15,.55,11,34) < .04
    assert 3.38 < required < 3.40
    assert window(.98,.38,29,2,.23)[2] > 0
    assert window(.55,.38,29,2,.23)[2] < 0
