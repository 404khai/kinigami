"""Take 31. Deterministic exploratory dimensions (mm); no acceptance claims."""
from itertools import combinations, product
from math import atan, cos, degrees, hypot, pi, radians, sin, sqrt, tan


O = (15., 3.50, 0.)
CENTER = (-.20, 0., .15)
D, V, Z = (.8, -.6, 0.), (.6, .8, 0.), (0., 0., 1.)
X, Y = (1., 0., 0.), (0., 1., 0.)
K, MU, RHO = .32, .23, .20
REAR, FRONT, TRAVEL = 1.65, 17.85, 20.50


def dot(a,b): return sum(x*y for x,y in zip(a,b))
def add(a,b,k=1.): return tuple(x+k*y for x,y in zip(a,b))
def mul(a,k): return tuple(x*k for x in a)
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def show(label,*v): print(label, *(round(x,6) for x in v))


# Relative coordinates. Deliberately do not include the aft face in the
# successful normal check: it needs physical exclusion, not a sign change.
ACTIVE = [(mul(Y,-1),0.),(X,FRONT-O[0]),(add(V,D,K),2.60),
          (add(mul(V,-1),D,K),1.05),(add(Z,D,K),2.85),(add(mul(Z,-1),D,K),2.85)]
PLANES = ACTIVE+[(mul(X,-1),O[0]-REAR)]


def vertices(planes):
    pts=[]
    for (a,j),(b,k),(c,l) in combinations(planes,3):
        det=dot(a,cross(b,c))
        if abs(det)<1.e-10: continue
        p=mul(add(add(mul(cross(b,c),j),cross(c,a),k),cross(a,b),l),1/det)
        if all(dot(n,p)<=h+1.e-8 for n,h in planes): pts.append(add(O,p))
    return pts


def section(x):
    X0=x-O[0]
    return [(x,y,z) for _,y,z in vertices(ACTIVE+[(X,X0),(mul(X,-1),-X0)])]


def radius(pts):
    return max(hypot(*add(p,CENTER,-1)) for p in pts)


def toe():
    home=vertices(PLANES)
    print('exploratory: forward surfaces only; constant slide/back not credited')
    for n,h in ACTIVE:
        l=hypot(*n)
        md=dot(n,D)/l
        ma=md*cos(radians(1))-sqrt(max(0.,1-md*md))*sin(radians(1))
        force=ma-MU*sqrt(1-ma*ma)
        # tangent backing ball proves the whole R2.5 disk is still flat
        # after convex edge rounding, not merely the centre of the flat.
        slack=h-2.5*hypot(n[0],n[2])-RHO*(n[1]+l)
        show('face n; normal dot d / worst release per N at 1 deg / flat slack',
             *mul(n,1/l),md,force,slack)
        assert force>.065 and slack>=-1.e-9
    show('home toe radius about common centre, high-open xmax',radius(home),
         FRONT-D[0]*TRAVEL)
    assert radius(home)+.20<30.
    for x in (1.65,2.9,4.15,15.,17.85):
        vs=section(x)
        show('section x,ymin,ymax,max|z|',x,min(p[1] for p in vs),
             max(p[1] for p in vs),max(abs(p[2]) for p in vs))
    # Every forward inequality tightens monotonically on withdrawal at a
    # fixed world point. For x>=REAR the aft clip never intrudes. Therefore
    # all swept sections there are subsets of the original.
    lo=min(q[1] for q in section(4.15))
    show('old tall blade interference, low blade clearance after .20',9.25-lo,lo-4.70-.20)
    assert lo<9.25 and lo-4.70>.20
    # Front tongue before push; blade wings can extend to x>=2.90 at home
    # but none of their near-tip parts rises past y2.05. Wings are not the
    # working blade surface. Eject travel starts only after real upper park.
    show('home wing y clearance, lower cheek clearance',3.50-2.05,3.50+1.70)
    assert FRONT-.8*20.30+.12<2.9  # actual, not commanded, min travel
    return home


def guard():
    # Fixed vertical throat at x=1.65. For a 2D normal s in yz use the
    # support function of the convex rear polygon K0. Aperture is its
    # Euclidean .15 offset: a true rounded perimeter, not an enclosing box.
    rear=section(REAR)
    m=.46
    # Each halfplane of toe yz section translates at its own signed speed
    # per mm of x. A universal Hausdorff bound is not the max of individual
    # halfplane speeds at corners. Test shifted rear polygon's Euclidean
    # distance at every forward corner and breakpoint. Equivalently, in 3D,
    # the swept aperture (a flare of a convex set) is convex: all vertices
    # of the complete clipped solid inside imply the whole solid is inside.
    poly=sorted({(round(y,10),round(z,10)) for _,y,z in rear})
    def turn(a,b,c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    def chain(q):
        hull=[]
        for p in q:
            while len(hull)>=2 and turn(hull[-2],hull[-1],p)<=0: hull.pop()
            hull.append(p)
        return hull
    rim=chain(poly)[:-1]+chain(list(reversed(poly)))[:-1]
    def distk(y,z):
        if all(turn(a,b,(y,z))>=-1.e-10 for a,b in zip(rim,rim[1:]+rim[:1])): return 0.
        best=1.e6
        for a,b in zip(rim,rim[1:]+rim[:1]):
            e=(b[0]-a[0],b[1]-a[1])
            t=max(0.,min(1.,dot((y-a[0],z-a[1]),e)/dot(e,e)))
            best=min(best,hypot(y-a[0]-t*e[0],z-a[1]-t*e[1]))
        return best
    mouth=2.32
    clip=vertices(PLANES+[(X,mouth-O[0]),(mul(X,-1),O[0]-1.95)])
    pinch=min(.15+m*(x-REAR)-distk(y,z) for x,y,z in clip)
    # Flare expands with x at any normal in the transverse plane. At
    # planar sides or curved corners the fixed material normal has +x.
    fixed=(m-MU)/hypot(1,m)
    show('stationary entry flare: minimum radial clearance, forward F/N',pinch,fixed)
    assert pinch>.10 and fixed>.20
    # Complete shell bounded by a Minkowski expansion of K0. Extend beyond
    # hole edge .45 normal to yz; front skin normal +x. No back side credit.
    rg=max(hypot(x-CENTER[0],hypot(y-CENTER[1],z-CENTER[2])+.15+
                 m*(x-REAR)+.45) for x in (1.95,mouth) for _,y,z in rear)
    extended=[add(p,D,-TRAVEL) for p in rear]
    show('fixed cuff closed radius; rear rim max y/radius at full opening',
         rg,max(q[1] for q in extended),radius(extended))
    assert rg+.20<30 and radius(extended)>30
    # Thin running gap at HOME does not remain a narrow port. A .45 probe
    # tangent to the parked horizontal flat can reach it through this
    # atmosphere-connected mouth along +x, without intersecting its front
    # or flared wall. This is not a complete second-Kin collision witness.
    a=.45
    p=add(O,D,-TRAVEL)
    y=p[1]-a
    # Explicit straight path at y,z constant starts to the right of entire
    # toe; sphere only touches the flat at and close to its endpoint. Disk
    # guard aperture contains a full a-neighbourhood of this line.
    assert all(turn(a0,b,(y+dy,z))>=0 for a0,b in zip(rim,rim[1:]+rim[:1])
               for dy,z in product((-a,a),repeat=2))
    show('unblocked .45 terminal probe endpoint xyz',p[0],y,0.)
    return rg


def terminal():
    yball=3.5+.6*TRAVEL-3.50
    # Aligned R8 summit under the terminal flat, site at x1.00. Test true
    # rear/side parts through +12. At each x on the cuff, an approaching
    # front boss has local x<=x-1, strictly aft of its centre x=3.50.
    # Its lateral support against z-.192*y is computed over the whole
    # spherical slice. Pure lateral padding stays inside the true rounded
    # aperture because all these heights remain strictly between its y lips.
    q0=2.85+.32*(.8*(15-REAR)+.6*(yball-3.5))
    least=100.
    for i in range(100):
        xl=1.95+.37*i/100; xr=xl+.37/100
        sr=sqrt(max(0.,9.-(3.50-(xr-1.))**2))
        a=q0+.15+.46*(xl-REAR)-(7*sin(pi/3)+sr*hypot(1,.192))
        least=min(least,a)
    assert least>.20
    assert min(p[1] for p in section(REAR))<yball-4 and max(p[1] for p in section(REAR))>yball+4
    assert q0-.192*1.20>7*sin(pi/3)+1.2
    assert 2.32-1.<3.50-1.20  # side root straps cannot reach the mask
    show('finite paddle actual summit contact x/y/site x, cuff boss reserve',1.,15.8,1.,least)

    # Stronger: after stow, at fixed yaw/tilt zero, the *rear butt* alone
    # can reach the same flat while its top ball is over 9mm forward. All
    # eligible paddle material that ANY stationary mast x<=3 could hit is
    # inside the actual toe sweep. Not just a pass through this cuff design.
    sx,sy,rr,aa=-3.45,.48,6.55,radians(12)
    px=sx-rr*cos(aa)
    py=sy+rr*sin(aa)+.45
    tx,ty=.80-px,15.80-py
    xmin=tx-10.45
    assert 3-tx < -7. and ty+1.20 < 15.80
    # For tail x>=tx right through touchdown, x<=3 clips it to the aft
    # R3 boss, cropped R7 cap and web/stub. All are in this coordinate box.
    # The side boss centres are x+3.50; the bed/cage has |x_local|<4.2.
    # For each x select a preceding jaw station putting that cross-section
    # inside its material. The stroke and all face margins are affine on
    # each x interval, so the corners certify the continuous prism.
    reserve=100.
    for x,y,z in product((xmin,REAR,3.),(ty-3.,15.80),(-3.,3.)):
        stroke=max(0.,(REAR-x)/.8)+.40
        assert 0.<stroke<TRAVEL
        p=add(add((x,y,z),O,-1),D,stroke)
        reserve=min(reserve,*( (h-dot(n,p))/hypot(*n) for n,h in PLANES ))
    show('rear butt counterpose site x/y, aft tip x, prism raw/rounded-core reserve',
         tx,ty,xmin,reserve,reserve-RHO)
    assert reserve>RHO+.11
    # V-dam counterexample & a restricted summit-only comparison. Solid
    # floor in v=.6x+.8y at 6.39; worst rear lower boss already dominates
    # full butt conservatively at this pose via its cropped enclosing ball.
    cr=.45+hypot(rr*sin(aa),rr*(1-cos(aa))/2)
    cx=sx-rr*(1+cos(aa))/2
    minv=.6*tx+.8*ty+min(-.6*7-3,.6*cx+.8*sy-cr,
                           -.6*8.70-1.2,-4.3)
    assert minv>6.39+.20
    show('entire butt counterpose minimum v; optional sill margin',minv,minv-6.39)
    tilt=radians(6)
    top=.8*cos(tilt)+.6*sin(tilt)
    vspan=6.4-4.5*top+3.50*sqrt(1-top*top)+3.
    vhigh=.6*FRONT+.8*3.50  # invariant under translation by t
    margin=6.39-(vhigh-vspan)
    show('R8 summit ONLY: tilt<=6, arbitrary yaw, boss below v6.39 by',margin)
    show('collar intersects proposed sill v: min/max',
         .6*(-.90)+.8*7.30,.6*1.68+.8*9.75)
    assert margin>.15 and .6*(-.90)+.8*7.30<6.39<.6*1.68+.8*9.75
    # Sufficient *observed* separation regions. Point data through x+12,
    # not a proof that other links and feet may take all free rotations.
    r=hypot(12.,8.7,1.2)
    assert r>max(7.+3.,hypot(8.7,0)+1.2,hypot(cx,sy)+cr,4.3+2.20)
    xmin=14.95-3.45-.48*sin(tilt)-7.
    show('monitored branch actual x minimum after .20; free-angle site x threshold',
         xmin-.20,3.+.20+r)


def crown():
    tilt=radians(6.)
    # Test a genuinely spherical R8 working CAP; don't assume an inscribed
    # R8 ball in a thin cropped steel part. Its actual centre is y=-4.5.
    r=8.
    for n in (50.,100.,200.):
        a=(3*n*r/(4*115380.))**(1/3)
        show('R8/flat: actual N/patch radius/GPa',n,a,3*n/(2*pi*a*a)/1000)
    wander=4.5*sin(tilt)
    flat=2.5-.80-wander-.05-a
    cap=2.5-8*sin(tilt)-a-.05
    show('R8 at 6deg: summit height gain, top flat reserve, cap reserve',
         4.5*(1-cos(tilt)),flat,cap)
    assert min(flat,cap)>0.
    # At partial oblique opening the flat moves laterally .8*s as well as
    # lifting .6*s. Never continue a horizontal platen solve beyond its rim.
    show('max uncovered travel at 6deg/±.8 offset, 200N patch',flat/.8)


if __name__=='__main__':
    toe()
    guard()
    terminal()
    crown()
