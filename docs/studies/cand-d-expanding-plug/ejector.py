"""Exploratory covering proof for rounded ejector columns, not a package.

Each guaranteed column = a swept ball of radius b on an x-directed line
segment ending at the common plane. The hoop is the union over its axis
circle. Units mm, N. No pose control or load sharing by the tail.
"""
from math import atan, cos, hypot, pi, radians, sin, sqrt, tan


def covering(n, rm, ro, rmax):
    # At fixed r the least favourable azimuth is midway between two
    # pin axes. Partition [0, rmax] at all pairwise equality radii.
    c=cos(pi/n)
    cuts=[0.,ro/2,ro,rmax,rm/(2*c),(ro*ro-rm*rm)/(2*(ro-rm*c))]
    def near(r):
        return min(r,abs(ro-r),hypot(r-rm*c,rm*sin(pi/n)))
    return max((near(r),r) for r in cuts if 0<=r<=rmax)


def screen(n, rm, ro, b, p, fixed_r, mu, dw=.10, dx=.10):
    # The core of a contacting p-ball may be up to p beyond a fixed edge.
    # At a strictly negative-x solution, the columns must extend past the
    # earliest possible ball centre (or entry from the rear must be excluded).
    ds,r=covering(n,rm,ro,fixed_r+p)
    d=ds+dw
    if d>=p+b:
        return None
    h=sqrt((p+b)**2-d*d)-dx
    c=(h-dx)/(p+b)
    k=c-mu*sqrt(1-c*c)
    return d,r,h,c,k,max(0.,p-h)


def guide(force,side,couple,span,nut_e,mu=.23,thread=.43,anti_r=6,drag=1.):
    # Opposed plain support pairs may be taken at their total pressure
    # minima only for a determinate, unpreloaded guide. Eccentricity acts
    # on the screw force itself. 'couple' external transverse moment.
    fb=mu*(2*nut_e/span+thread/anti_r)
    if fb>=1: return float('inf')
    return (force+mu*(side+2*couple/span)+drag)/(1-fb)


def main():
    for n,rm,ro,b,fixed_r in [(6,11,19,3,18.8),(6,10,18,2.5,18.5),
                               (12,10,18,1.8,18.0),(6,10,17,2.3,18.0)]:
        val=screen(n,rm,ro,b,5.,fixed_r,.23)
        print(n,rm,ro,b,'D, critical r, h, nx, Fx/N, extra centre advance past frontmost fixed stock:')
        print('uncovered' if val is None else tuple(round(x,4) for x in val))
    n,rm,ro,b,p,mu=6,11,19,3.,5.,.23
    k=screen(n,rm,ro,b,p,18.8,mu)[4]
    F=5*.070*9.80665
    N=F/k
    S=N*(1+mu*mu)**.5
    # Only if all load-carrying p-cores stay in the covered region. The
    # external hoop face needs its own qualified draft or an outer boundary.
    print('inner atlas only: max Fx, sum N, side enclosing box',F,N,S)
    print('12mm effective span, eccentric 7.2mm screw: guide thrust if all lands determinate',
          guide(F,S,20*F+10*S,12,7.2))
    # A real external skirt tangent to the outer torus and extending aft
    # makes the positive-normal condition independent of tail radial offset.
    slope=radians(30)
    k2=sin(slope)-mu*cos(slope)
    print('outer cone axial contribution per N, additional radial build for 8mm run',k2,8*tan(slope))
    assert covering(6,11,19,19)[0]<6.5
    assert screen(6,11,19,b,p,27.2,mu) is None
    # At least 2 opposite stock circles in a fixed free-pose sphere.
    # With coaxial same-size rings centred P apart, the diametrically
    # opposite points are separated by hypot(P,2*radius). Full spheres
    # around those points need another 2b. Not a shell tolerance allowance.
    for pitch in (38.,40.,42.,45.):
        print('two R19,b3 toroidal banks, pitch, minimum D',pitch,hypot(pitch,38.)+6.)


if __name__=='__main__':main()
