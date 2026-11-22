"""Two closest points of a torus on a long circular pin. Exploratory, mm/N."""
from math import acos, atan, cos, degrees, hypot, pi, sin, sqrt, tan


def pair(A, r, b, B):
    d = r + b
    assert d <= B <= sqrt(d*A)
    # The projection of the core circle perpendicular to the shaft is an
    # ellipse (B cos q, A sin q). A disk of radius d inside it can touch
    # twice only on its medial axis. The offset along the major axis is e.
    sinq = sqrt(max(0., (1-(d/B)**2)/(1-(B/A)**2)))
    cosq = sqrt(max(0., 1-sinq*sinq))
    e = (A-B*B/A)*sinq
    s = sqrt(A*A-B*B)*cosq
    u, v = B*cosq/d, B*B*sinq/(A*d)
    assert abs(hypot(u,v)-1) < 1e-12
    assert abs(A*sinq-e-v*d) < 1e-12
    return e,s,u,v


def contact_bound(A,r,b,mu,F,M):
    # F, M upper-bound the major-axis components of the EXTERNAL wrench
    # about the torus centre. The axis direction varies with eye attitude.
    # Pure X/Z slip cancels by choosing omega=u/s, translation=v along Z.
    d = r+b
    umax_over_s = 1/sqrt(d*(A-d))  # at B=sqrt(A*d)
    gain = 1-mu*b*umax_over_s
    assert gain > 0
    bound = (F + M*umax_over_s)/gain
    print('pair tilt range deg, omega bound /mm, gain, sum N bound, axial drag N',
          *(round(x,5) for x in (degrees(acos(sqrt(d/A))),degrees(acos(d/A)),
                                 umax_over_s,gain,bound,mu*bound)))
    # Regression check, not the proof. A one-contact case instead has N <= F3
    # by equilibrium if F3 bounds the full external resultant.
    for i in range(1001):
        B=d+(sqrt(d*A)-d)*(i/1000); e,s,u,v=pair(A,r,b,B)
        omega=B/(d*sqrt(A*A-B*B))
        assert omega < umax_over_s+1e-12 and abs(omega*s-u)<1e-12
        assert (F*v + M*omega)/(1-mu*b*omega*u) <= bound+1e-10
    return bound


def draft_screen(mu_pin=.23, mu_wall=.23):
    # Optimistic necessary size test for two simultaneous *certificates*:
    # full exposed cone recedes more steeply than friction, circular wall
    # port shields a tube-backed probe with positive axial work everywhere.
    # Even a zero far-tip radius and zero clearance need p >= 2 H tan(beta).
    # H >= r (sec(a)+tan(a)); p/r < sin(a-delta) is the guard rule.
    # For delta=0, maximize sin(a)cos(a)/(1+sin(a)) exactly.
    z=(sqrt(5)-1)/2
    absolute=z*sqrt((1-z)/(1+z))
    print('cone optimistic one-sided max slope / pin requirement',absolute/2,mu_pin)
    delta=atan(mu_wall)+pi/180
    # A certified upper bound by intervals, sin(a-delta) increases while
    # cos(a)/(1+sin(a)) decreases. An endpoint product bounds each bin.
    N=2000
    upper=max(sin((i+1)*pi/(2*N)-delta)*cos(i*pi/(2*N))/(1+sin(i*pi/(2*N)))
              for i in range(N))
    print('two equal cones optimistic max slope including wall friction and 1 deg error',upper)
    return absolute/2,upper


if __name__=='__main__':
    assert contact_bound(5.,2.7,1.25,.23,5.,50.) < 35.
    full, split=draft_screen()
    assert full < .151 and split < .216
