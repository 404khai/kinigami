"""Exploratory virtual work in a quasistatic free chain, not a motion solver."""
from math import atan, cos, hypot, radians, sin, sqrt, tan


def bound(grams, count, tail_count, floor_mu, tilt, h=0., down=0., accel=0.):
    """+Z up nominally; additional net downward force N; COM acceleration m/s².

    4W,W,W is a separate non-gravity service force box on the moving group.
    Opposite external forces can realize that test without net hold-down.
    `down` must cover any uncompensated applied load on the whole assembly.
    """
    assert 0 < tail_count < count and min(floor_mu, down, accel, h) >= 0
    assert 0 <= tilt < 90 and grams > 0
    w = grams * .001 * 9.80665
    k = tan(radians(51) + atan(.23)) * hypot(1., h)
    y, a = radians(tilt), hypot(1., k)
    length = hypot(a,h)
    # Extremal floor projections within a cone about nominal +Z.
    low = h*cos(y) - a*sin(y)
    high = length if a <= length*sin(y) else h*cos(y) + a*sin(y)
    # Safe tangent bound, including intervals spanning orthogonality.
    nearest = max(0., low, -high)
    tangent = sqrt(max(0., length**2 - nearest**2))
    floor_debit = max(0., floor_mu*tangent - low)
    normal_cap = count*(w + grams*.001*accel) + down
    gain = 1 - tan(radians(.5) + atan(.23))*hypot(k,h)
    if gain <= 0:
        return None
    # Static tail-group equilibrium. accel only relaxes the floor cap; it
    # does NOT make this a bounded dynamic force calculation.
    demand = w*(4.+k+h) + tail_count*w*max(0.,high) + normal_cap*floor_debit
    return demand/gain, normal_cap, gain


def main():
    for count in (2,5):
        for tilt in (0.,15.):
            for mu in (.3,.5,1.):
                # Any printed direction is individually sufficient; a scan
                # can improve an upper bound but does not prove optimality.
                choices = [(x[0], i/100, x[1]) for i in range(201)
                           if (x := bound(70.,count,count-1,mu,tilt,i/100))]
                best,h,n = min(choices)
                print(f'{count} Kins, tilt {tilt:g} deg, mu {mu:g}: '
                      f'cap {n:.4f} N, h {h:.2f}, axial force >{best:.4f} N')
    f,n,g = bound(70,5,4,1,0)
    assert abs(n - 5*.070*9.80665) < 1e-12
    assert abs(f - (.070*9.80665*(4 + tan(radians(51)+atan(.23)))
                     + n*hypot(1,tan(radians(51)+atan(.23))))/g) < 1e-12


if __name__ == '__main__':
    main()
