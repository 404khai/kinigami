"""Take 36; exploratory common rigid virtual velocity. mm, N, N.mm."""
from itertools import product
from math import acos, asin, atan, atan2, ceil, cos, degrees, exp, hypot, pi, radians, sin, sqrt, tan

K=1.20
MU=.23
RAD=10.75
F=-1.75
M=tan(radians(35))
VAL=-3/cos(radians(35))
RAMP=8.04
EPS=.06
BALL=.45
SITES=[(7*cos(a),7*sin(a),cos(a),sin(a)) for a in map(radians,(180,60,-60))]


def show(msg,*vals): print(msg,*(round(x,5) for x in vals))


def dishes(x,z):
    for a,b,c,s in SITES:
        u,w=x-a,z-b
        yield hypot(max(0.,abs(u*c+w*s)-.70),-s*u+c*w)


def raw(x,z):
    r=hypot(x,z)
    return min(F-K*max(0.,r-RAMP),-3.86+M*max(0.,r-1.75),
               VAL+M*min(dishes(x,z)))


def cone(d,speed,mu,err=0.):
    # Worst projection within the normal-angle and closed friction disks.
    # Do not apply the increasing branch for normal angles near pi.
    if speed==0: return 0.
    a=min(pi,acos(max(-1.,min(1.,d/speed)))+err)
    return speed*(cos(a)-mu*sin(a)) if a<pi-atan(mu) else -speed*hypot(1,mu)


def loss(r,z,mu):
    # Illustrative TWO-journal and opposed-thrust loss lengths only.
    # L=24, effective Coulomb lengths .12 radial, .16 thrust.
    return hypot(1.,mu)*(.12*(1+2*hypot(r,z)/24)+.16)


def cells(step=.25):
    half=step/2; h=hypot(half,half)
    nb=ceil(RAD/step)
    for i,j in product(range(-nb,nb+1),repeat=2):
        x,z=step*i,step*j
        r=hypot(x,z)
        if r>RAD+h: continue
        extend=2*BALL+EPS+h
        groove=(min(dishes(x,z)) <= (F-VAL)/M+extend or r<1.75+(F+3.86)/M+extend)
        ny=cos(radians(35)) if groove else 1.
        nx=sin(radians(35)) if groove else 0.
        cones=[(ny,-nx,nx)]
        if r+extend>=RAMP:
            phi=atan2(abs(z),x)
            a=asin(min(1.,extend/r))
            low=cos(min(pi,phi+a)); high=cos(max(0.,phi-a))
            nn=hypot(1,K)
            cones.append((1/nn,K*low/nn,K*high/nn))
        # Infinite upper graph only: opening by a ball loses <= b*(sec(a)-1).
        # Position debits on top of compactly supported symmetric smoothing.
        roof=raw(x,z)
        lo=roof-K*(EPS+h)-BALL*(hypot(1,K)-1)-.06
        hi=min(F,roof+K*(EPS+h))+.06
        yield (15+x-half-.06,15+x+half+.06,lo,hi,abs(z)+half+.06,cones)


def graph(px,py,boxes):
    best=net=1e6
    for l,h,b,t,z,cones in boxes:
        # Each conic inequality is concave in velocity. Test rectangle
        # vertices. Generating raw gradients suffice by convexity of the
        # permissible-normal cone at fixed velocity, incl 1deg mismatch.
        for x,y in product((l,h),(b,t)):
            dx,dy=x-px,y-py
            assert dx>=0
            r=hypot(dx,dy)
            for ny,nlo,nhi in cones:
                d=dx*ny-dy*(nhi if dy>0 else nlo)
                g=cone(d,r,MU,radians(1))
                best=min(best,g)
                net=min(net,g-loss(r,z,MU))
    return best,net


def map_pivots():
    data=list(cells())
    print('upper graph lower bounds after example bearing losses; columns xp = -5,-2,0,1,2,3')
    for yp in (-8.,-6.,-4.,-2.,0.,2.):
        show('yp',yp,*(graph(xp,yp,data)[1] for xp in (-5.,-2.,0.,1.,2.,3.)))
    a,b=graph(-2.,-4.,data)
    show('(-2,-4) graph gross/net; cells',a,b,len(data))
    assert b>0
    fine=list(cells(.125))
    show('fine (-2,-4) gross/net',*graph(-2.,-4.,fine))
    for x,z,c,s in SITES:
        for sign in (-1,1):
            nx=-sign*sin(radians(35))*s; ny=cos(radians(35))
            X=15+x-3*nx; Y=-3*ny
            show('actual V tangent x/y/z and nominal-work lower incl angle',
                 X,Y,z-3*sign*sin(radians(35))*c,
                 cone((X+2)*ny-(Y+4)*nx,hypot(X+2,Y+4),MU,radians(1)))


def cheek():
    # Centre of a backing ball under BOTH actual tangent side points and
    # proof start. Symmetric smoothing can move raw roof by at most K EPS.
    for x,z in ((15.,RAD-BALL),(15.-RAD+BALL,0.),(25.,0.)):
        y=-5.65; margin=min(raw(x-15,z)-K*EPS-y-BALL*hypot(1,K),y+6.5-BALL)
        assert margin>.3 and hypot(x-15,z)+BALL<=RAD+1e-9
    px,py=-2.,-4.; x,y=15.,-5.65
    show('vertical side / aft wall / bottom worst work at sample real points',
         cone(0,hypot(x-px,y-py),MU),cone(y-py,hypot(4.25-px,y-py),MU),
         cone(-(15-px),hypot(15-px,-6.5-py),MU))
    # A continuation of the falling deck: .46 substrate thickness. Real
    # lower housing must protect this entire termination, not just a hub.
    ro=13.; y=F-K*(ro-RAMP); fx=15+ro
    radius=hypot(hypot(15.2,.15)+ro,y-.46)
    show('skirt r / height / max assembled radius / gap below to level floor',
         ro,y,radius,y-.46+23.)
    for cz in (11.4,12.6):
        show('skirt y at rack/side outrigger radial slice',cz,F-K*(cz-RAMP))
    for ro in (11.50,13.):
        net=1e6
        for dx,dy in product((17-ro-.06,17+ro+.06),
                             (F-K*(ro-RAMP)+4-.06,F-K*(RAD-RAMP)+4+.06)):
            r=hypot(dx,dy)
            g=cone((dx-K*abs(dy))/hypot(1,K),r,MU,radians(1))
            net=min(net,g-loss(r,ro+.06,MU))
        dx=17-ro; dy=F-K*(ro-RAMP)+4
        show('perimeter r, whole added graph net, actual aft nominal per N',
             ro,net,cone((dx+K*dy)/hypot(1,K),hypot(dx,dy),MU))
        if ro==11.50: assert net>0
    # Inverse Coulomb-cone flow. A probe centre's velocity vector differs
    # from the actual point direction by <=asin(p/r). Starting in expanded
    # solid, positive work everywhere requires the field to point inward.
    p=.45; r=hypot(25-px,-5.65-py); th=atan2(-5.65-py,25-px)
    assert atan(.20)+asin(p/r)<atan(MU)
    a=radians(30); rr=r*exp(.20*a)
    x=px+rr*cos(th-a); y=py+rr*sin(th-a)
    d=hypot(x+.20,y,.15)
    show('backward spiral at 30deg x/y / outside expanded sphere / clear of floor',x,y,d-30-p,y-p+23)
    assert d>30+p and y-p>-23
    # Same obstruction for forward-leaning translation and any tilt up to
    # 20deg: a downward ray tilted no more than 8deg aft is inside its
    # reverse cone if the tilt is 8..20deg. For smaller tilt use vertical.
    y=-21.8; x=25.-(-5.65-y)*tan(radians(8))
    show('hybrid reverse-ray x/y / excess over expanded sphere',x,y,hypot(x+.20,y,.15)-30-p)
    assert hypot(x+.20,y,.15)>30+p and y-p>-23


def sided():
    c=.27; a=radians(12)
    # (name, horizontal/vertical marker norm about chosen body anchor,
    # maximum kernel reach from marker, Minkowski backing radius).
    rows=[
        ('boss',7+c,1.8,1.2),('web',c,7.,1.2),('rear stub',7+c,1.7,1.2),
        ('butt',hypot(3.45+6.55*cos(a)+c,.48),6.55*sin(a),.45),
        ('arm root',hypot(3.50-c,6.063),hypot(3.50,1.438),1.2),
        ('round arm',hypot(7-c,7.50),5.,1.2),
        ('upper hardware',.0,5.,0.)]
    # Last row means the entire SMALL upper kit fits within radius 5 of
    # anchor, not that an annular retainer is convex. Use distance from
    # contact itself instead; projection onto radial direction >=RAD-5.
    # Cap angular range by exact arccos bound of radius-5 offset from RAD.
    ds=atan(1/MU)-radians(2.)  # explicit angular work surplus
    lng=100.
    for name,r,l,b in rows[:-1]:
        m=(RAD+b)*sin(ds)-l*cos(ds)-r
        print('radial force hemisphere signed margin',name,round(m,6))
        lng=min(lng,m)
    assert asin(5/RAD)<ds and lng>0
    show('all vertical walls: worst unit radial force/N, min length reserve',
         cos(ds)-MU*sin(ds),lng)
    return cos(ds)-MU*sin(ds)


def floor_blade():
    px,py=-2.,-4.; mu=1.; y=-23.
    for x in (-2.,15.,18.,32.):
        r=hypot(x-px,y-py)
        show('floor x / level / any 15deg / bearing-net tilted',
             x,cone(x-px,r,mu),cone(x-px,r,mu,radians(15)),
             cone(x-px,r,mu,radians(15))-loss(r,10.,mu))
    w=5*.070*9.80665
    show('five 70g aggregate N / adverse torque for -2 per N / generic R60 worst',w,2*w,60*hypot(1,mu)*w)
    for x,y in ((4.15,.48),(4.15,4.7),(19.15,.48)):
        g=py-y-MU*abs(x-px)
        show('actual +x blade x/y torque per N / net incl bearings',x,y,g,g-loss(hypot(x-px,y-py),10.65,MU))
    q=radians(10); a,b=4.60-px,.48-py
    x,y=px+a*cos(q)-b*sin(q),py+a*sin(q)+b*cos(q)
    show('literal co-rotation: known interior butt point x/y / inside blade',
         x,y,min(x-3.35,4.15-x,y+1.5,3.30-y))
    assert 3.35<x<4.15 and -1.50<y<3.30
    # Two opposed bearing groups example, actuator pinion torque reaction:
    # transverse mesh force including pressure angle, offset z, no axial force.
    g=cos(radians(20)); rr=12.; zz=14.
    feedback=.12*(1+2*abs(zz)/24)/(rr*g)
    show('example mesh torque feedback / delivered fraction',feedback,1-feedback)


def lift():
    a=radians(17)
    for name,angle,mu in [('floor at 15deg',a+radians(15),1.),
                          ('upper graph 51deg',a+radians(51),MU),
                          ('measured +x pusher, 1deg',radians(91)-a,MU),
                          ('vertical z side',pi/2,MU)]:
        show('translation unit work '+name,cone(cos(angle),1.,mu))
    show('15mm lift: actual forward displacement / slide travel',15*tan(a),15/cos(a))
    show('90deg package: site x needed beyond xmax1.05, arbitrary finite paddle',
         1.05+hypot(12,8.7,1.2)+.20)


if __name__=='__main__':
    map_pivots()
    cheek()
    sided()
    floor_blade()
    lift()
