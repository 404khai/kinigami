"""Exploratory opening-only spring on the *aligned* Take 21 fork, SI internally."""
from math import acos, atan, cos, degrees, radians, sin, sqrt


def retreat(d, side=0.0):
    # Captive single axis sleeve: two guide lands actually span 4 mm.
    # Self-induced normal is bounded by transverse spring component plus moment pair.
    mu, span, offset, tilt = .23, .004, .00025, radians(1)
    K = .90 * 28600 * (cos(tilt) - mu * (sin(tilt) + 2 * offset / span))
    drag = .7 + mu * side
    amplitude = .00415 - drag / K
    mass = .006
    if amplitude <= 0 or d >= 2 * amplitude:
        return None
    t = acos(1 - d / amplitude) * sqrt(mass / K)
    v = sqrt(K / mass * d * (2 * amplitude - d))
    return t, v, K * (amplitude - d), .5 * mass * v**2


def free_recoil(s, e, a=.010, M=.054, m=.006, gyration=.010):
    # Two bodies in the plane, no external wrench, initially at rest.
    # x = a-s, slider COM at (x,e) in carrier coordinates, not bellows pressure.
    # H = [I + reduced_mass*(x*x+e*e)]*theta' + reduced_mass*e*s' = 0.
    red = m*M/(M+m)
    u = sqrt(red / (M*gyration**2 + red*e*e))
    theta = -e*u*(atan(a*u)-atan((a-s)*u))
    c = m / (M+m)
    def delta(point):
        px, py = point
        x, y = px-c*(a-s), py-c*e
        return (c*a+x*cos(theta)-y*sin(theta), c*e+x*sin(theta)+y*cos(theta))
    # Front pole on fork, representative point at the outside seat.
    tip0 = (.01390, e)
    p = delta((tip0[0]-s,tip0[1]))
    return theta, p[0]-tip0[0], p[1]-tip0[1]


def budget(t, extent=.012):
    # Both bodies free of contact, with proposed *lower* inertias, and externally
    # bounded force/couple on EACH about its own COM. Not a housing-contact bound.
    M, I = .054, .054*.010**2
    total_inv = 2/M + 2*extent**2/I
    F, T = 5*.060*9.80665, .060
    a = 2*(F/M + extent*T/I)
    gap = .000111
    drift = .5*a*t*t
    emax = max(0., gap-drift)**2 / (2*total_inv*t*t)
    return drift, emax


if __name__ == '__main__':
    # Verify fixed-frame ODE against its work integral; do not silently use a
    # positive exit velocity when the stage cannot actually start or reach it.
    for side in (0., 62., 140., 500.):
        v = retreat(.00360, side)
        if v is None:
            print('guide side N / cannot traverse:', side)
            continue
        t, speed, end, energy = v
        drift, emax = budget(t)
        print('guide side N / ms / m/s / end net N / capture mJ / '
              'free drift mm / residual mJ:', side,
              *(round(a,5) for a in (1e3*t,speed,end,1e3*energy,1e3*drift,1e3*emax)))
    assert retreat(.00360, 500.) is None
    for e in (0., .001, .002, .004):
        print('COM offset mm; (stroke mm, rotation deg, tip retreat mm, side mm):',e*1000)
        for s in (.00150,.00300,.00320,.00360):
            q,x,y=free_recoil(s,e)
            print(tuple(round(z,5) for z in (1000*s,degrees(q),-1000*x,1000*y)))
    assert abs(free_recoil(.00360, 0.)[1]+.00324) < 1e-12
    print('max nominal clocking error before slot hits using reduced half-width '
          '(.95-.20) mm, bar half-section 2.55 x .55:')
    from scipy.optimize import brentq
    print(round(degrees(brentq(lambda q: 2.55*sin(q)+.55*cos(q)-.75,0,radians(10))),5))
