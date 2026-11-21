"""Take 22, larger 70 g/50--55 N alternative. Exploratory; no repo input."""
from math import acos, cos, degrees, hypot, pi, radians, sin, sqrt
from button import hertz, interval_gap, out, project

p=4.80
bl,bh=1.244,1.256
A,W,L,d=1.345,4.30,3.75,.018
low,park,high=-1.052,-1.032,2.48
mu=.23


def upper_distance(cmax,hmax,changed):
    worst=0.
    # Conservative CONTINUOUS interval enclosure, including all azimuths.
    for i in range(1800):
        a=-1+(1+cmax)*i/1800
        b=-1+(1+cmax)*(i+1)/1800
        ss=[sqrt(max(0.,1-c*c)) for c in (a,b)]
        slo=min(ss)
        shi=1 if a<=0<=b else max(ss)
        if changed:
            # Changed cap normals lie <=35deg from the keyed crown axis.
            if b<cos(radians(55.5+35)) or a>cos(radians(54.5-35)):
                continue
            # The intersection contains the concentric ball B-cut (also
            # after erosion/dilation). Tangential support deviation bounded.
            inner=bl-.156
            r0=max(0.,(p+inner)*slo-max(abs(a),abs(b))*sqrt(bh*bh-inner*inner)-d)
            r1=p*shi+bh+d
            z0=p*a-bh
            z1=p*b+bh
            # Support q = alpha*u - gamma*v, alpha,gamma >= 0;
            # q.u<=B. Thus q.n<=(B*c) for 0<=c<=v.n.
            if b<=cos(radians(55.5)):
                z1=p*b+bh*max(0.,b)
        else:
            r0,r1=max(0.,(p+bl)*slo-d),(p+bh)*shi+d
            z0,z1=min((p+v)*a for v in (bl,bh)),max((p+v)*b for v in (bl,bh))
        rw=interval_gap(r0,r1,A,W)
        rt=interval_gap(r0,r1,A,A)
        for j in range(75):
            zl=z0+low+(hmax-low)*j/75
            zh=z1+low+(hmax-low)*(j+1)/75
            dp=hypot(rw,interval_gap(zl,zh,0,0))
            dt=hypot(rt,interval_gap(zl,zh,-L,0))
            # At park only: conserved top sphere R=.65, fixed +.594*n
            # from shoe centre. May exclude probes touching a CUT region
            # only if strict overlap with this retained sphere is proved.
            ds=hypot(r1+d,max(abs(z0-.594),abs(z1-.594)))-.65
            worst=max(worst,min(dp,dt,ds if changed else 1.e5))
    return p-worst-1.e-9


def main():
    # Interval arithmetic for an entire uncertain lens, not just corner samples.
    # Plane coordinate on sphere-1 core: z=( (Rw-bf)^2-(B-bf)^2-D^2)/(2D)
    # Use a numerically stable equivalent from the radical-plane identity:
    # 1-cos(alphaS) = cut*(2*(Rw-bf)+cut)/(2*D*(B-bf)).
    # D=Rw-B+cut, so D+(B-bf)=(Rw-bf)+cut.
    cut0,cut1=.144,.156
    k=.156*(2*(8.05-.195)+.156)/(2*(7.95-bh+.144)*(bl-.205))
    aS=degrees(acos(1-k))
    kl=.144*(2*(7.95-.205)+.144)/(2*(8.05-bl+.156)*(bh-.195))
    width=(bl-.205)*sqrt(1-(1-kl)**2)  # core radius; actual crown larger
    out('crown max changed angle / guaranteed working transverse halfwidth',aS,width)
    assert aS<35
    # R=.65, centre offset .594 from O, gives inner core sphere r=.65-bf.
    # Fit to the second core requires |.594*n+D*v|+.65 <= Rw.
    # Subtract Rw algebraically: |z*n+D*v| <= D+z*cos(theta)+z²/(2D).
    marker=.65
    inside=bl-cut1-marker-.594*cos(radians(54.5))-.594**2/(2*(7.95-bh+cut0))
    shield=p+marker-hypot(A+d,max(p-low-.594,high+.594))
    out('marker fits sphere/crown, lip shielding reserve',
        bl-(marker+.594),inside,shield)
    assert inside>0 and shield>.01
    for cmax,hmax,name in [(.320,high,'all'),(.960,park,'park')]:
        a,b=(upper_distance(cmax,hmax,x) for x in (False,True))
        out(name+' excluded c<=, intact/changed stock intersection reserves',cmax,a,b)
        assert min(a,b)>0
    g=project(cos(acos(.320)+radians(.50)))
    qp=project(sin(radians(29.75)-acos(.960)))
    Wt=.070*9.80665
    nfree=.40/(g-.055)
    nclose=1.40/(g-.055)
    neg=-project(sin(radians(29.75)-acos(.320)))
    out('inward/parked signed N/N, free and 1N-spring normals',g,qp,nfree,nclose)
    out('push > N parked/one leading/three leading; parked normal sum cap',
        5*Wt,5*Wt+nfree*neg,5*Wt+3*nfree*neg,5*Wt/qp)
    assert qp>0 and g>.055
    f,q=radians(30),radians(55)
    R,H,t,s0=5.8,2.45,4.83,1.10
    base=R-.40*cos(f)
    dc=4.34**2/(base+hypot(base,4.34*cos(f)))
    over=1.62
    Cx=H*sin(f)+(s0+t)*sin(f-q)
    Cr=R+H*cos(f)+(s0+t)*cos(f-q)
    lift=.78
    gap=H+(s0+t)*cos(q)-t-(over-lift)*cos(f)
    disk=.82
    rear=Cx-t-disk*cos(q-f)
    floor=rear+7.20
    local=H+(s0+t)*cos(q)-t-disk*sin(q)
    other=sqrt(3)*(R-L*cos(f))
    out('cone oversize min / selected, full ring gap; local flat core-disk margin',dc,over,gap,local)
    out('torus x, radius, exposed ring outer R; rear deck gap; tube axis spacing',Cx,Cr+lift,Cr+lift+t,floor,other)
    assert over>dc and min(gap,local,floor)>.1
    # Other pads never intersect the shoe/Rw work patch near this station:
    # tangential distance 120deg interstation, or supporting local halfspace.
    # Limit connecting core disks to radial extrusion length lift+disk.
    out('conservative radius of ALL pad/radial-web p-balls',Cr+disk+lift+t)
    wall_margin=Cr+lift-(R+H*cos(f))-t-bh
    out('cylinder-wall to entire B sphere margin; aligned terminal travel >',wall_margin,4.40-rear)
    assert wall_margin>.06
    # Finite internal collar, including actual head front cap and other cuts.
    cross=sin(f)**2+cos(f)**2*cos(2*pi/3)
    out('other core plane / eroded cap clearance to guaranteed top disk',
        1.5*base*cos(f)-4.34*sqrt(1-cross**2),4.4-.40-(4.34*cos(f)-.40*sin(f)))
    # Dual certificate for normals in 2deg full circular cones, not just in plane.
    def coeff(l,eta):
        norm=hypot(1,l)
        co=(sin(radians(25))+l*cos(radians(25))*eta)/norm
        return norm*project(cos(acos(min(1.,co))+radians(2)))
    lam=.330
    one=(55+lam*16)/coeff(lam,1)
    total=55/coeff(0,1)
    out('sum N, directional single-foot cap S<=16, off-station coefficient',total,one,coeff(lam,-.5))
    assert coeff(lam,-.5)>0
    for n in [nfree,nclose,one,total]:
        ac,peak=hertz(n,7.95)
        out('N, crown-flat halfwidth,GPa; convex R.195/p lip halfwidth,GPa',n,ac,peak,*hertz(n,1/(1/.195+1/p)))
    patch=hertz(one,8.05)[0]
    out('crown width reserve at 2deg relative tilt, .04 edge',
        width-8.05*sin(radians(2))-patch-.040)
    out('flat land reserve at .13 transverse datum+2deg tilt+.04 edge',
        disk-.13-8.05*sin(radians(2))-patch-.04)
    assert width-8.05*sin(radians(2))-patch-.04>0
    # Root section screening; full force, worst contact offset with no couple assumption.
    # Relative to carrier O all button metal lies inside B. In closed CROWN
    # contact use |q x u| <= (Rw-B+cut)*sin(2deg+0.5deg); friction <= mu*B.
    rstem=1.03
    barm=(8.05-bl+cut1)*sin(radians(2.5))+mu*bh
    gmouth=high+.18
    tf=sin(radians(57.5))+mu
    af=cos(radians(52.5))+mu
    for n in [one,total]:
        out('single N, guide-mouth gross bending + compression MPa',n,
            4*n*(gmouth*tf+barm)/(pi*rstem**3)+n*af/(pi*rstem**2))
    out('loaded slide approximate dry two-bearing drag ceiling per N, before baseline',
        .23*((1+2*gmouth/(L-.18))*tf+2*barm/(L-.18)))
    out('travel max mm; bore clearance vs 1.300 min',high-low,1.300-bh-d)
    out('conservative radial space to 40mm diameter before other stock',
        20-(Cr+disk+lift+t))
    axial_factor=cos(radians(52.5))+mu*sin(radians(52.5))
    out('max total button n-axis compression; same incl guide, 3 offsets, loaded shelf drag',
        total*axial_factor,total*(axial_factor+.055)+3*.4,
        .23*(total*(axial_factor+.055)+3*.4))
    out('transition normal cap if real back <=2N vs 100N before trip',
        (2+.4)/(g-.055),(100+.4)/(g-.055))
    for n in (nfree,nclose,one):
        out('rounded blend R.195x1.244 against rolling p N, half-axes, GPa',n,
            *ellipse(n,1/(1/.195+1/p),1/(1/bl+1/p)))
    pfree=ellipse(nfree,1/(1/.195+1/p),1/(1/bl+1/p))[-1]
    n3=nfree*(3/pfree)**3
    out('illustrative 3GPa fillet-screen N, maximum residual actuator+guide N',
        n3,(g-.055)*n3)
    edgecap=5*Wt/project(sin(radians(29.75)))
    out('parked fixed cone contact cap, illustrative R.40/p isotropic GPa',
        edgecap,hertz(edgecap,1/(1/.4+1/p))[1])
    out('parked one button cap; sphere/p comparison GPa',
        5*Wt/qp,hertz(5*Wt/qp,1/(1/bl+1/p))[1])


def ellipse(n,rx,ry,steps=256):
    """Elastic half-space integrals as in edge_hertz.py, t=tan(y)^2."""
    def integrals(k):
        ia=ib=0.
        for j in range(steps+1):
            a=pi*j/(2*steps)
            w=(1 if j in (0,steps) else (4 if j%2 else 2))
            u=cos(a)**2
            z=1+(k*k-1)*u
            v=w*2*u/sqrt(z)
            ia+=v; ib+=v/z
        f=pi/(6*steps)
        return ia*f,ib*f
    lo,hi=1.,30.
    for _ in range(46):
        k=(lo+hi)/2
        ia,ib=integrals(k)
        if ia/ib<ry/rx: lo=k
        else: hi=k
    ia,_=integrals(k)
    a=(3*n*rx*ia/(2*pi*115384.615))**(1/3)
    return a,k*a,3*n/(2*pi*k*a*a)*.001


if __name__=='__main__':
    main()
