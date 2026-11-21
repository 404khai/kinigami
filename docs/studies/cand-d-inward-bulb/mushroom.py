"""Exploratory Take 24. mm, N, steel/steel elastic comparison. No solver or pose snap."""
from math import acos, asin, atan, cos, degrees, dist, hypot, pi, radians, sin, sqrt, tan


def show(s, *xs):
    print(s, *(round(x, 6) for x in xs))


def add(a, b, k=1.):
    return tuple(x+k*y for x, y in zip(a, b))


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def rot(v, t):
    x, y, z = v
    return x, y*cos(t)-z*sin(t), y*sin(t)+z*cos(t)


def mincone(c, t):
    return cos(min(pi, acos(min(1., max(-1., c)))+t))


p, b, rd, mu = 5.80, 2.40, 4.20, .23
f, beta, gamma, alpha, span = map(radians, [37, 23, 28, 35, 4.3])
O = (-.57, 10.95, 0.)
n = (sin(f), -cos(f), 0.)
H = 3.02
P = add(O, n, -H)
D = -dot(P, n)
# Intersection of THESE free half-spaces. Extra lower-draft facets are for
# compactness; their intercept deliberately clears the three rear pad lobes.
f2, D2 = radians(18.), 14.05
walls = [(rot(n, i*2*pi/3), D) for i in range(3)] + [
    (rot((sin(f2), -cos(f2), 0.), (1+2*i)*pi/3), D2) for i in range(3)]
Krad, Klo, Khi = 6.68, -6.15, 4.5
xr, rr = -9.92, 2.95
ax = (1., 0., 0.)
C = (xr, rr, 0.)
w = (cos(alpha), sin(alpha), 0.)
Q = add(C, w, p)
rear = [(rot(w, (2*i+1)*pi/3), rot(Q, (2*i+1)*pi/3)) for i in range(3)]


def cutters():
    result = []
    for i in range(3):
        pair = []
        for sign in (-1., 1.):
            u = rot((-sin(beta)*cos(gamma), -cos(beta)*cos(gamma), sign*sin(gamma)), i*2*pi/3)
            L = add(rot(O, i*2*pi/3), u, b-rd)
            pair.append((L, u))
        result.append(pair)
    return result


def fixed_clear(k):
    return min(dot(v, k)+d-p for v, d in walls)


def core_slack(k):
    """Untrimmed margins; sign matters. Outside at least one sphere of each lens."""
    return [Krad-hypot(*k[1:]), k[0]-Klo, Khi-k[0], fixed_clear(k)-.07,
            max(dot(j, add(k, q, -1.)) for j, q in rear),
            min(max(dist(k, l)-(rd+p) for l, _ in pair) for pair in cutters())]


def backing():
    delta = 2*(p+rd)*sin(span/2)
    for i, pair in enumerate(cutters()):
        for side, (l, u) in enumerate(pair):
            k = add(l, u, rd+p)
            y = add(l, u, rd)
            wall = min(dot(v, l)+d+(p+rd)*mincone(dot(v, u), span)-p for v, d in walls)
            back = max(dot(v, add(l, q, -1))+(p+rd)*mincone(dot(v, u), span) for v, q in rear)
            other = min(dist(k, l2)-(rd+p)-delta for j, pp in enumerate(cutters())
                        if j != i for l2, _ in pp)
            # Whole physical land inside the other empty cavity by distance.
            # Use exact max along the cap instead of a chord-distance budget.
            vdiff = add(l, pair[1-side][0], -1)
            dl = hypot(*vdiff)
            hc = -mincone(-dot(vdiff, u)/dl, span)
            opp = rd-sqrt(dl*dl+rd*rd+2*dl*rd*hc)
            m = min(Krad-hypot(*k[1:])-delta, wall-.07, back,
                    k[0]-Klo-delta, Khi-k[0]-delta, other, opp)
            if i == 0 and side == 1:
                show('V contact x,r,t; dish centre x,r,t', *y, *l)
                show('V core radial, wall free, rear, remote cutters, opposite cavity mm',
                     Krad-hypot(*k[1:])-delta, wall, back, other, opp)
            assert m > .04, m
    for j, q in rear:
        # Actual 0.40-radius plane disk on the core. Its normal is j; no
        # penalty to its own rear plane. Other cuts, not the plane, truncate it.
        a = .40
        # For a tangent disk, r^2 is quadratic in its meridional direction
        # cosine; it increases up to that cosine = 1 for this disk.
        assert hypot(*q[1:])*cos(alpha)>a*sin(alpha)**2
        radial = Krad-hypot(*q[1:])-a*cos(alpha)
        wall = min(dot(v, q)+d-p-a*sqrt(max(0., 1-dot(v, j)**2)) for v, d in walls)
        cut = min(max(dist(q, l)-(rd+p)-a for l, _ in pair) for pair in cutters())
        assert min(radial, wall-.07, cut, q[0]-Klo-a) > 0
    show('rear x,r; pad core x,r; equivalent arm', *C[:2], *Q[:2], rr-xr*tan(alpha))
    show('rear core disk radial spare, min wall free, other cut', radial, wall, cut)
    show('bulb OD; port x,r; lock centre height', 2*(Krad+p), *P[:2], H)
    # Integrated insphere. Two witnesses cover each 120-degree angular sector:
    # the rear-pole ball or the ball centred at (B-p) times query direction.
    for debit in [0., .16]:
        B = -xr-rr*tan(alpha)-debit
        qp = (-B+p*cos(alpha), p*sin(alpha), 0.)
        qp = rot(qp, pi/3)
        angle = 2*atan(.5*p*sin(alpha)/(B-p*cos(alpha)))
        rear_slack = (B-p)*(-cos(alpha)*cos(angle)+.5*sin(alpha)*sin(angle))-dot(w,Q)
        # All directions of the small core shell must clear every non-rear cut.
        rad = B-p
        regular = min(Krad-rad, -Klo-rad, Khi-rad, min(d-rad-p-.07 for _,d in walls),
                      min(hypot(*l)-(rd+p)-rad for pair in cutters() for l,_ in pair))
        sl = core_slack(qp)
        show('insphere, crossover deg, forward-core, rear-plane, pole-other margins',
             B, degrees(angle), regular, rear_slack, min(sl[:4]+sl[5:]))
        assert min(sl) > -.00000001 and min(regular,rear_slack)>.08
        assert hypot(*qp)<p
        if debit: assert min(sl)>.08
    # A neck centreline from x=0 forward: axis distance to each cutter by radial
    # component, so no new contact. No neck filling the rear apex at x=-7.854.
    show('neck: clearance from cutter lens, piston apex', min(hypot(*l[1:])-(p+rd)
         for pp in cutters() for l,_ in pp), -xr-rr*tan(alpha)-p)
    assert min(core_slack((0.,0.,0.)))>0 and min(core_slack((4.,0.,0.)))>0


bl, bh, A, W, L, drift = 2.390, 2.410, 2.510, 6.75, 5.40, .020
hlo, hp, hhi = -1.953, -1.928, H+.035


def gap(lo, hi, a, z):
    return max(0., a-lo, hi-z)


def excluded(cmax, hmax, nc=1400, nh=64):
    worst = 0.
    for i in range(nc):
        lo = -1+(1+cmax)*i/nc
        hi = -1+(1+cmax)*(i+1)/nc
        s = [sqrt(max(0.,1-x*x)) for x in (lo,hi)]
        r0 = (p+bl)*min(s)-drift
        r1 = (p+bh)*(1 if lo<=0<=hi else max(s))+drift
        zlo = min((p+bb)*lo for bb in (bl,bh))
        zhi = max((p+bb)*hi for bb in (bl,bh))
        for j in range(nh):
            z0 = zlo+hlo+(hmax-hlo)*j/nh
            z1 = zhi+hlo+(hmax-hlo)*(j+1)/nh
            worst = max(worst, min(hypot(gap(r0,r1,A,W),gap(z0,z1,0.,0.)),
                                   hypot(gap(r0,r1,A,A),gap(z0,z1,-L,0.))))
    return p-worst-1.e-9


def projection(v):
    return v-mu*sqrt(max(0.,1-v*v))


def hertz(N, R):
    patch = (3*N*R/(4*115384.615))**(1/3)
    return patch, 3*N/(2*pi*patch**2)*.001


def ports():
    c, cp = .315, .939
    m1, m2 = excluded(c,hhi), excluded(cp,hp)
    g = projection(mincone(c,radians(.5)))
    angle = f-radians(.30)-acos(cp)
    shield = p+bl-hypot(A+drift, p-hlo)
    show('guard exclusion all/park mm, lip shield, bore running clearance', m1,m2,shield,2.455-bh-drift)
    show('free retraction N/N, parked draft deg & outward N/N',g,degrees(angle),projection(sin(angle)))
    assert min(m1,m2,shield,projection(sin(angle)))>0
    # A hemispherical plunger on a full-diameter barrel, not a sphere on a stem.
    # Points at c=0 below the equator are hidden behind a continuous bore or
    # collide with the top annulus; the blind bottom is closed.
    assert hypot(p+bh+drift-W,hhi)<p and A<p+bl-drift<W+p
    f0, drag = .40, .035
    Nfree, Nlim = f0/(g-drag), (1+f0)/(g-drag)
    eps = acos(c)-f+radians(.8)
    neg = sin(eps)+mu*cos(eps)
    show('free N, 1N closure N, 5W+ k contact opposing push (k=0,1,2,3)',
         Nfree,Nlim,*[5*.070*9.80665+j*neg*Nfree for j in range(4)])
    for N in (Nfree,Nlim,145.07):
        show('one contact N, sphere/p GPa, spherical dish GPa, sphere/flat GPa',
             N,hertz(N,1/(1/bl+1/p))[1],hertz(N,1/(1/bl-1/4.22))[1],hertz(N,bl)[1])
    av=hertz(145.07,1/(1/bh-1/4.18))[0]
    usable=4.18*sin(span-asin(.040/(4.18-bh)))
    rearpatch=hertz(191.47,8.05)[0]
    show('V max patch, usable, reserve; rear max patch, peak GPa, .40 land minus .04 reg, .012 tilt and patch',
         av, usable, usable-av, rearpatch,hertz(191.47,7.95)[1],.40-.04-8.05*.012-rearpatch)
    show('guide/front sole seated force/moment N,Nmm',145.07*(sin(acos(dot(n,cutters()[0][0][1]))+.012)+mu),
         145.07*((hhi+.25)*(sin(acos(dot(n,cutters()[0][0][1]))+.012)+mu)+mu*bh))
    assert usable-av>.005 and .40-.04-8.05*.012-rearpatch>0
    show('nose x parked bound; port edges bound; disk xmax, rmax; sleeve rmax',
         P[0]+.035+hp*sin(f-radians(.30))+drift+bh,
         P[0]+.035+A*cos(f-radians(.30))+drift,
         P[0]+.035+W*cos(f-radians(.3)), P[1]+.035+W*sin(f+radians(.3)),
         P[1]+.035+L*cos(f-radians(.3))+A*sin(f+radians(.3)))
    return angle


def skirt(angle):
    # Whole bulb core under arbitrary orientation. Neck/backing NOT included.
    dc=hypot(Krad,max(abs(Klo),Khi))+.08
    for k, draft in ((.34,0.),(.055,11.5),(.0,13.5)):
        d=radians(draft)
        u=sqrt(1+k*k)
        az=sqrt(1-(dc/(6.90+p*cos(d)))**2)
        side=sin(d)+k*cos(d)*az
        fixed=sin(angle)-k*cos(angle)
        force=lambda v: v-mu*sqrt(u*u-v*v)
        show('skirt deg,k; min side and parked virtual N/N',draft,k,force(side),force(fixed))
    # Infinite front triangle apex envelope and unrelieved funnel interference.
    x7=xr+rr*tan(alpha)-7*tan(alpha)
    show('R7 nose skirt x, active unrelieved aperture, missing radius',x7,(D+x7*sin(f))/cos(f),7-(D+x7*sin(f))/cos(f))


def control():
    # Separate single-dish 50–55 N cartridge branch; no rear integrated seats.
    t=radians(4.3); v=(-sin(beta+t),-cos(beta+t),0.)
    l=add(tuple(-(10-p-.17)*x for x in n),v,-(p+rd))
    o=add(l,(-sin(beta),-cos(beta),0.),rd-b)
    h=10+.17+dot(o,n); pp=add(o,n,-h)
    show('single-dish insphere nom/conservative, port x,r,H',hypot(*l)-rd,hypot(*l)-rd-.055,*pp[:2],h)
    def cf(lam,az):
        u=hypot(1.,lam)
        return u*projection(mincone((sin(beta)+lam*cos(beta)*az)/u,radians(2.)))
    lam=.268
    assert cf(lam,-.5)>0
    one=(55+16*lam)/cf(lam,1.)
    show('single-dish 55N and <=16N lateral, one-foot cap; no lateral bound; dish GPa',
         one,55/cf(0,1),hertz(one,1/(1/bl-1/4.22))[1])


if __name__=='__main__':
    control()
    backing()
    skirt(ports())
