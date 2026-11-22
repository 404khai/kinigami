"""Exploratory Take 22, finite 3D rolling-ball exclusion; N, mm, radians.

Standard library only. A box succeeds by strict penetration of a guaranteed
metal witness, not by failure to find tangency at a grid point.
"""
from math import acos, asin, atan, ceil, cos, degrees, hypot, pi, radians, sin, sqrt, tan


def out(label, *args):
    print(label, *(round(x, 6) for x in args))


p = 3.60                                  # fixed inner tangent probe
bl, bh = .894, .906
A, W, L, drift = 1., 2.65, 2.80, .015    # guaranteed stock, radius/length
hlo, hp, hhi = -.751, -.735, 1.60
mu = .23
ph = radians(31)


def interval_gap(lo, hi, a, b):
    return max(0., a-lo, hi-b)


def excluded(cmax, hmin, hmax, nc=1500, nh=72):
    """Max upper bound on distance to nearest of two complete guard rings.

    Revolve [A,W] x {0} and {A} x [-L,0]. For a rectangular range of
    centre coordinates the maximum distance to either section is at an
    endpoint in each dimension. Both witnesses are continuous in azimuth.
    """
    worst = 0.
    for i in range(nc):
        l = -1+(1+cmax)*i/nc
        r = -1+(1+cmax)*(i+1)/nc
        ss = [sqrt(max(0., 1-x*x)) for x in (l, r)]
        rlo = max(0., (p+bl)*min(ss)-drift)
        rhi = (p+bh)*(1 if l<=0<=r else max(ss))+drift
        da = interval_gap(rlo, rhi, A, W)
        dt = interval_gap(rlo, rhi, A, A)
        z0 = min((p+b)*l for b in (bl,bh))
        z1 = max((p+b)*r for b in (bl,bh))
        for j in range(nh):
            zl = z0+hmin+(hmax-hmin)*j/nh
            zh = z1+hmin+(hmax-hmin)*(j+1)/nh
            top = hypot(da, interval_gap(zl, zh, 0., 0.))
            tube = hypot(dt, interval_gap(zl, zh, -L, 0.))
            worst = max(worst, min(top, tube))
    return p-worst-1.e-9


def project(v):
    return v-mu*sqrt(1-v*v)


def hertz(n, radius):
    e = 210000/(2*(1-.30**2))
    a = (3*n*radius/(4*e))**(1/3)
    return a, 3*n/(2*pi*a*a)*.001


def main():
    free_c, park_c = .350, .957
    for name, c, hmax in [('all',free_c,hhi), ('park',park_c,hp)]:
        reserve=excluded(c,hlo,hmax)
        out(name+' strict excluded c <=, stock overlap margin mm',c,reserve)
        assert reserve>0
    g = project(cos(acos(free_c)+radians(.50)))
    ax = project(sin(radians(30.5)-acos(park_c)))
    out('button inward, parked +x, N/N',g,ax)
    assert g>.10 and ax>0
    shield = p+bl-hypot(A+drift,max(p-hlo,hhi))
    out('lip probe-to-button interference reserve mm',shield)
    assert shield>.019
    # The machined neck lies within the swept sphere; full port at its minimum.
    out('running clearance vs .950 min bore; max positive travel',.950-bh-drift,hhi-hlo)
    f0,gN,opening = .40,.065,1.0
    nfree=f0/(g-gN)
    nclose=(f0+opening)/(g-gN)
    out('conditional free/1N limited advance one button normal sums',nfree,nclose)
    w=.060*9.80665
    angle=acos(free_c)-radians(30.5)
    neg=sin(angle)+mu*cos(angle)
    out('positive push all parked, one/three unconstrained leading, N',
        5*w,5*w+neg*nfree,5*w+3*neg*nfree)
    out('one parked contact all compression / min positive projection N',5*w/ax)

    # Circular cone, three milled flats, erosion then dilation by a .40 ball.
    R0,b,H,t,qq,fillet,over = 4.0,.90,1.57,3.63,radians(49),.40,.945
    Rcore=R0-fillet*cos(ph)
    Wcut=2.69
    dc=Wcut**2/(Rcore+hypot(Rcore,Wcut*cos(ph)))
    Cx=H*sin(ph)+(b+t)*sin(ph-qq)
    Cr=R0+H*cos(ph)+(b+t)*cos(ph-qq)
    gap=H+(t+b)*cos(qq)-t-over*cos(ph)
    out('required cone excess / selected mm, margin to torus nominal',dc,over,gap)
    assert dc<over and gap>.07
    # Nearest-other-plane condition n_j.(Q-O_j) on the WHOLE eroded flat disk.
    d=sin(ph)**2+cos(ph)**2*cos(2*pi/3)
    other=1.5*Rcore*cos(ph)-Wcut*sqrt(1-d*d)
    out('other eroded facet clearance; port centreline separation at -L',
        other,sqrt(3)*(R0-L*cos(ph)))
    assert other>0
    shell=Cr+t
    out('torus centre x, radius; outer radius, rear x, deck gap to x=-4.65',
        Cx,Cr,shell,Cx-t,Cx-t+4.65)
    out('nose largest collar x-span half; face flat smooth +x projection',
        Wcut*cos(ph),project(sin(radians(30.5))))

    # True 3D nominal tangent on an axisymmetric torus, not angle availability.
    # Curvature of torus azimuth is concave on inner surface; p-ball contact
    # is a comparison screen, not its elliptic Hertz solution.
    one=36./project(sin(radians(17)))   # gauged signed axial angle 18 +/-1
    out('single backed station at gross draw <=36N and >=17deg, N',one)
    # No participation of other parallel tensile paths in this inference.
    minN=35/(3*(sin(radians(19))+mu*cos(radians(19))))
    out('some button normal >=, if net draw >=35 N',minN)
    for n in (nfree,nclose,minN,100.,one):
        out('N, comparison B/convex p: patch mm, GPa; R1.28 saddle: patch mm, GPa',
            n,*hertz(n,1/(1/bl+1/p)),*hertz(n,1/(1/bl-1/1.28)))

    # Saddle from a cap of rolling centres; all head metal lies below local facet.
    # The corresponding complete toroidal core is outside the cutter sphere.
    rf=1.27
    span=radians(11)
    guard=H+(b-rf)*cos(qq)+(t+rf)*cos(qq+span)-t
    foot=rf*sin(span)
    disp=.025
    wander=asin(disp/(1.26-bh))
    usable=1.26*sin(span-wander)
    out('saddle p-ball stock gap, half-land, wander deg, remaining half-land mm',
        guard,foot,degrees(wander),usable)
    nloc=80.
    patch,peak=hertz(nloc,1/(1/bh-1/1.26))  # largest patch for clearance
    out('example 80N max patch and edge reserve with .025mm debit',patch,usable-patch-.025)
    out('saddle transverse error to limit normal to 1deg mm',(1.26-bh)*sin(radians(1)))
    assert guard>.05 and usable>patch+.025
    neck=.65
    # Guide plane z=-.22; transverse resultant and friction moment at sphere.
    trans=sin(radians(50))+mu
    arm=(hhi+.22)*trans+bh*mu
    for n in (minN,nloc,one):
        bending=4*n*arm/(pi*neck**3)
        out('N, guide-mouth bending + compression screen MPa at solid r=.65',
            n,bending+n*(cos(radians(48))+mu)/(pi*neck*neck))
    out('80N arm allows max unsupported moment arm at 800MPa design screen, mm',
        ((800-nloc*(cos(radians(48))+mu)/(pi*neck**2))*pi*neck**3/(4*nloc)-bh*mu)/trans)
    out('hypothetical two guides, min sleeve separation / span for 2-.22 mm support',
        sqrt(3)*(R0-L*cos(ph)), L-.22)
    # Exact counterexample for a different B1.25 hex nose.
    f,q=radians(29),radians(50)
    x=1.125*sin(f)+6.25*sin(f-q)
    r=4.5+1.125*cos(f)+6.25*cos(f-q)
    slope=tan(f)/cos(pi/6)
    dist=(r-4.5/cos(pi/6)+slope*x)/hypot(1,slope)
    out('B1.25 intact hex corner signed clearance, corner x and radius',
        dist-5,x-dist*slope/hypot(1,slope),r-dist/hypot(1,slope))


if __name__ == '__main__':
    main()
