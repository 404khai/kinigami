"""Take 27, exploratory rigid geometry. mm, N, radians. No solver/acceptance claim."""
from itertools import combinations_with_replacement, product
from math import asin, atan2, cos, degrees, dist, hypot, pi, radians, sin, sqrt, tan

F, R, B = radians(35), 7., 3.
C, S, M = cos(F), sin(F), tan(F)
MU, EPS, HALF, FLAT = .23, .060, .70, -1.75
RAMP, K, ROLL = 8.04, 1.20, .45
VALLEY = -B/C
SY=.48  # rear push-crown centre height, not upper ball centre height
ANGLES = tuple(map(radians,(180,60,-60)))
SITES = [(R*cos(a),R*sin(a)) for a in ANGLES]
def out(name,*v): print(name,*(round(x,6) for x in v))


def raw(x,z):
    """As-cut nominal before a compact, symmetric .060 mm planar smoothing."""
    r=hypot(x,z)
    y=min(FLAT-K*max(0.,r-RAMP),-3.86+M*max(0.,r-1.75))
    for (cx,cz),th in zip(SITES,ANGLES):
        a,b=x-cx,z-cz
        d=hypot(max(0.,abs(a*cos(th)+b*sin(th))-HALF),-a*sin(th)+b*cos(th))
        y=min(y,VALLEY+M*d)
    return y


def geometry():
    d=(FLAT-VALLEY)/M
    # Each valley's support lies within a capsule; smoothing adds at most EPS.
    out('contact tangent, y; max groove footprint R, plateau margin to rim fillet',
        B*S,-B*C,R+HALF+d+EPS,10.55-R-HALF-d-EPS)
    # Tighter radial enclosure: far end of a finite segment + radius is exact.
    assert R+HALF+d+EPS<10.55
    out('opening per N on intact 35deg lands incl 1deg ground slope',
        cos(radians(36))-MU*sin(radians(36)))
    # Central R4 outer bed centred .5 above origin; otherwise lower web -1.20.
    # Upper-bound each entire radial interval of 5 microns; include near-home
    # offset + tilt and .06 mm height budget. No sample-based minimum.
    spare=10.
    for j in range(800):
        lo,hi=4*j/800,4*(j+1)/800
        low=.5*cos(radians(2))-.020/C-sqrt(max(0.,16-lo*lo))
        roof=min(FLAT,-3.86+M*max(0.,hi+.30+.5*sin(radians(2))+EPS-1.75))
        spare=min(spare,low-roof-.06)
    out('rear of R4 central ball bed to lower relief, mm',spare)
    assert spare>.15
    for (x,z),a in zip(SITES,ANGLES):
        for s in [-1,1]:
            nx,nz=-s*S*sin(a),s*S*cos(a)
            X,Z=x-B*nx,z-B*nz
            assert abs(raw(X,Z)+B*C)<1e-12
            out('contact global xyz, head-on-tail normal',15+X,-B*C,Z,nx,C,nz)


def cage(dh,verbose=True):
    # dh = gauged excess platen displacement over nominal closed plane,
    # including relative centre/skin/upper ball radius error at the actual load.
    # Plane equation violation at a lower centre is at most en (units mm).
    en=.020
    tau=radians(2)
    # Retainer: centre local y >= .490 from solid floor and aperture gage.
    wander=2.530-sqrt(2.995**2-(2.560-.490)**2)
    assert wander<.38
    # Re-entry/remote poses are NOT established by continuation. Trial branch
    # bounds tau<=2deg, centre planar displacement <=.53, |ty|<=.10 mm,
    # |yaw|<=2deg, and every boss planar displacement <=.55.
    ty=dh+.50*(1-cos(tau))+.38*sin(tau)
    # y bound for each lower centre in the trial neighbourhood.
    yi=.10+R*sin(tau)
    proj_t=.55*C*C+yi*S*C
    assert .55+EPS<HALF and B*S+proj_t+EPS<(FLAT-VALLEY)/M
    assert B*S-proj_t>EPS
    # Erode+dilate smoothed hypograph with ROLL to bound convex curvature.
    # Certify a whole ROLL ball below each projected finite tangent plus
    # convolution shifts. The plane of this V is a global minorant of its
    # own distance field; other features can only remove that witness.
    t=B*S+proj_t
    yc=VALLEY+M*t-ROLL*C
    rc=hypot(R+.55,t+ROLL*S)
    assert yc+ROLL+M*EPS < FLAT
    assert yc+K*(rc-RAMP)+ROLL*hypot(1,K)+K*EPS<FLAT
    assert R-.55-ROLL-EPS>1.75+(FLAT+3.86)/M
    assert sqrt(3)*R-hypot(.55,t+ROLL*S)-ROLL-EPS>HALF+(FLAT-VALLEY)/M
    # Other grooves and central basin are absent under either tangent foot,
    # including the entire trial disk of projected points.
    rshift=hypot(.55,proj_t)+EPS
    assert hypot(R,B*S)-rshift>1.75+(FLAT+3.86)/M
    assert sqrt(3)*R-B*S-rshift>HALF+(FLAT-VALLEY)/M
    assert .53+.38+.5*sin(tau)+.05<2.50  # true upper flat covers the sphere
    xi=R*(1-cos(tau))
    a=(en+C*ty)/S
    yaw=asin((a+xi)/R); d=2*(a+xi)
    boss=d+2*R*sin(yaw/2)+xi
    tilt=asin(2*(ty+en/C)/R)
    success=(tilt<tau and yaw<radians(2) and d<.53 and boss<.55 and ty<.10)
    if verbose:
        out('upper excess, |centre xz|, upper ty, tilt/yaw deg, boss xz, passes',
            dh,d,ty,degrees(tilt),degrees(yaw),boss,int(success))
    if success:
        radial_margin=HALF-EPS-boss-.02
        out('straight radial land left for pressure patch',radial_margin) if verbose else None
    return success


def hertz(n,r):
    a=(3*n*r/(4*115380.))**(1/3)
    return a,3*n/(2*pi*a*a)/1000.


def pressure_land():
    # Structural .055 cage, conservative outward rounding. Use a physical
    # patch disk in its own plane, with .020 extra registration, at 200 N.
    shift=.416
    yi=.069+R*sin(radians(1.53))
    patch=hertz(200,B)[0]+.020
    margins=[10.]*5
    for i in range(90):
        # Independent support bounds over a closed one-degree sector of the
        # planar boss-offset disk. Absolute component maxima over all signs.
        r0=shift*cos(radians(i))
        t0=shift*sin(radians(i+1))*C*C+yi*S*C
        for j in range(90):
            r1=r0+patch*cos(radians(j))
            t=B*S+t0+patch*C*sin(radians(j+1))
            yc=VALLEY+M*t-ROLL*C
            rc=hypot(R+r1,t+ROLL*S)
            margins=[min(a,b) for a,b in zip(margins,(
                HALF-EPS-r1, B*S-t0-patch*C-EPS,
                FLAT-yc-ROLL-M*EPS,
                FLAT-yc-K*(rc-RAMP)-ROLL*hypot(1,K)-K*EPS,
                sqrt(3)*R-hypot(r1,t+ROLL*S)-ROLL-EPS-HALF-(FLAT-VALLEY)/M))]
    assert R-shift-patch-ROLL-EPS>1.75+(FLAT+3.86)/M
    out('200N patch reserve: radial, inner tangent, plateau, fall, neighbour',*margins)
    assert min(margins)>0


def approach():
    # Quasistatic corridor, NOT a passive convergence calculation.
    # Bed floor near working point R6; an R3 ball on it roams on radius 3.
    slope=radians(.5)
    low=min(.50*cos(slope)-4,-7*sin(slope)-3,
            -1.2-14.83*sin(slope),SY-1.82-10*sin(slope))
    out('open axial insertion lower clearance at y>=2.15 and .50deg tilt',
        2.15+low-FLAT-.06)
    assert 2.15+low>FLAT+.06
    for a,offset in [(.05,.012),(.5,.12),(1.,.25)]:
        ang=radians(a)
        dxz=offset+2*R*sin(ang/2)+R*(1-cos(ang))
        # Largest height at which any real lower contact could begin on
        # these three bosses. The other parts have separate clearance.
        dy=.020/C+M*dxz+R*sin(ang)
        climb=3-sqrt(9-.38**2)
        start=dy+climb+.38*sin(ang)+.010
        out('tilt/yaw deg, centre offset, worst first lower bearing upper excess',
            a,offset,start)
        if a==.05: assert start<.080
    # Interference-free cap assembly: ball/bed working point is within r=.76.
    # Beyond r=1.10, enforce >=.30 steel skin on R4 lower outer bed, lower
    # surface enters the web where it rises above y=-1.2. Compare with all
    # possible displaced R3 balls from r=1.10 to the radius of their union.
    spare=10.
    for j in range(500):
        lo=1.10+2.30*j/500; hi=lo+2.30/500
        shell=min(-1.2,.5-sqrt(max(0.,16-hi*hi)))+.30
        ball=.49-sqrt(max(0.,3.005**2-max(0.,lo-.38)**2))
        spare=min(spare,ball-shell)
    assert spare>.35
    out('outside working bed: ball clearance to minimum .30 substrate',spare)


def bounds():
    # Balls at each vertex enclose the convex hull (diameter maximized at
    # vertices). Tail portion only, truncated at x=+12. Body is a separate test.
    parts=[('boss',(x,0,z),B) for x,z in SITES]
    parts += [('web',(x,0,z),1.2) for x,z in SITES]
    parts += [('strap',(x,0,z),1.2) for x,z in [(7,7.5),(7,-7.5),(-8.7,0)]]
    for s in [-1,1]:
        parts += [('arm',(x,y,s*z),0.) for x,y,z in product([7.,12.],[-1.2,1.2],[6.3,8.7])]
    parts += [('bed',(0,.5,0),4),('retainer',(0,2.2,0),4.15)]
    # The latter loose sphere encloses a radius-4 annular cage of thickness
    # .70 about its mid-height. The bed's R4 sphere above also encloses the
    # loose ball: the throat bounds its height and horizontal wander.
    hmax=2.560-sqrt(2.995**2-2.530**2)
    assert hypot(.38,max(hmax-.5,.010))+3.005<4.
    rc,p,ang=7.,.45,radians(12)
    rc0=rc-p; xx=rc0*(1+cos(ang))/2
    cr=p+hypot(rc0*sin(ang),rc0-xx)
    parts.append(('butt',(-3.45-xx,SY,0),cr))
    diam=max((dist(q,k)+b+r,n,m) for (n,q,b),(m,k,r) in combinations_with_replacement(parts,2))
    out('diameter any orientation incl arms to +12; open gap spare incl .20 total',
        diam[0],25-FLAT-.20-diam[0])
    print('diameter limiting primitives:',diam[1:])
    assert diam[0]<25-FLAT-.20
    # Comparison ONLY (flat-top outer rim): front fillet is meridional, with normal between +y
    # and +radial. Exterior radius >=10.55; full vertical rim below it.
    # Bounded ejection poses, axial progression >=-.05 from home; |z|<=.16,
    # tilt<=6deg, yaw<=3deg. Decompose yaw about Y, then least tilt.
    tilt,yaw=radians(6),radians(3)
    # A tilted in-plane vector's planar block after yaw differs by <=1-cos.
    zmax=max(abs(q[2])+abs(q[0])*sin(yaw)+hypot(q[0],q[2])*(1-cos(tilt))+
             abs(q[1])*sin(tilt)+r for n,q,r in parts if n not in ['arm','butt'])
    zarm=8.7+12*sin(yaw)+hypot(12,8.7)*(1-cos(tilt))+1.2*sin(tilt)
    zm=max(zarm,zmax,4.)+.16+.05
    # Work with the actual x of a point, not just the tail centre. For
    # rear-half points any positive axial translation can only shrink planar
    # radius. Positive-x arms outside the disk stay positive under this tilt.
    # Only the part of the R7 butt BELOW the (toleranced) plateau can hit
    # a perimeter fillet. Its horizontal slice shrinks at that depth.
    ylo=-.65+SY*cos(tilt)-3.45*sin(tilt)
    zs=3.45*(sin(yaw)+1-cos(tilt))+SY*sin(tilt)+.16
    butt_rear=hypot(3.45+SY*sin(tilt)+.05,zs)+sqrt(49-(ylo-FLAT-.06)**2)+.03
    rear=max(7+B,8.7+1.2)+hypot(.05,.16)+.05
    # 3.5..7 angled neck roots interpolate between endpoints; the first
    # endpoint is inside the circle and the far endpoint and its skin have
    # strictly positive x. The whole segment here stays in positive x.
    assert 3.50*cos(tilt+yaw)-7.50*sin(tilt+yaw)-1.20-.05>0
    out('aft lower rim reserve, compact solids / actual butt horizontal slice',
        10.55-rear,10.55-butt_rear)
    assert max(rear,butt_rear)<10.55
    edgex=sqrt(max(0.,1-(zm/10.55)**2))
    # Half-degree rim-normal error, all 3D. Interior already includes 1 deg.
    rim=edgex-hypot(1,1.2)*2*sin(radians(.5)/2)
    out('max |z|, lower forward rim min nx; v=(1,1.2,0) g_36deg / g_rim_tol',
        zm,edgex,*[g-MU*sqrt(1+1.2**2-g*g) for g in
                  [1.2*cos(radians(36))-sin(radians(36)),rim]])
    assert zm<10.55
    # Crown's separating plane at all admissible ejection rotations:
    # compares actual R3 rear boss and the R7 exterior sphere at butt.
    lead=4-hypot(3.55,SY)
    yhi=3.5+SY+3.45*sin(tilt)
    out('butt over aft sphere, pickup y range, flat blade side room ±2.50',
        lead,ylo,yhi,2.50-(.16+3.45*sin(tilt+yaw)+SY*sin(tilt)))
    assert lead>.34 and ylo>-.80 and yhi<5.
    # Nose protrusion to a flat pusher. Support is not a hinge or socket:
    # actual pickup force may be zero at the terminal separating condition.
    upper_tip=-3.45*cos(tilt+yaw)+SY*sin(tilt+yaw)-7.
    out('min actual tail-centre advance when blade reaches 19.10',19.1-upper_tip-15)
    # The neck starts outside the closed R10.75 footprint, not outside its
    # supporting infinite plane. Test the inverse image of the FINITE head.
    az=sin(yaw)+1-cos(tilt)
    # 10 sin + R cos increases throughout this small tilt range.
    jaw=10.75*cos(tilt)+10*sin(tilt)+.05+.16*az+.06
    out('inverse-plane clearance to x>=+12 housing: complete finite jaw',12-jaw)
    assert jaw<12
    for name,xg,yy,zz in [('guide',2.9,32.5,7.1),('screw',5.3,20.3,4.75),
                           ('bridge',19.,32.65,7.1),('wheel',13.9,20.65,19.4),
                           ('motor',15.8,22.07,18.),('rack incl travel',23.,11.55,12.9)]:
        # For components completely aft of x=15 use 0 instead of their
        # negative x: multiplying a negative x by 1 is not conservative.
        bound=max(0.,xg-15+.05)+yy*sin(tilt)+(zz+.16)*az+.06
        out(name+' housing margin',12-bound)
        assert bound<12
    # Before pushing, watch centre xz until plane is physically high. One
    # dose of tilt is enough to bound every carrier's upper y against ball.
    ball_low=.490*cos(tilt)-.38*sin(tilt)+2.995
    butt_top=SY+(3.45+xx)*sin(tilt)+cr
    other=max(1.2+14.83*sin(tilt),2.56+4*sin(tilt),
              1.2+(7+1.8)*sin(tilt),butt_top)
    out('upper ball above every other tail surface before push, incl .060 debit',
        ball_low-other-.06)
    assert ball_low-other>.06
    # Solid/body can only meet a lower backside below -6.50; conservative
    # lower support for each part bounding ball. AABB corners have r=0.
    ymin=min(-.65+min(q[1],q[1]*cos(tilt))-hypot(q[0],q[2])*sin(tilt)-r
             for _,q,r in parts)
    out('min tail y inc .06 error, margin to lower backside and motor top',
        ymin-.06,ymin-.06+6.50,ymin-.06+12.17)
    assert ymin-.06> -6.10
    # Integrated falling deck, including edge region after smoothing. Offset
    # opening only REMOVES material from the smoothed graph. Cut terminal
    # fillet/bore/backside only below this y, not through a separate thin rim.
    edge=FLAT-K*(10.55-RAMP-EPS)+.060
    alpha=radians(51)
    out('highest terminal edge, gap below entire tail, lower Fy/N, max adverse Fx/Fy',
        edge,ymin-.06-edge,cos(alpha)-MU*sin(alpha),tan(alpha+atan2(MU,1)))
    assert ymin-.06-edge>.15
    # When genuinely on the R7 working cap, pusher normal in tail coordinates
    # is within 12deg of tail X. Arbitrary roll about X is now admissible.
    # Bound vertical reach from the R7 sphere centre, which is exactly at the
    # contact height on a flat +X pusher. Half a degree for blade normal adds
    # R7*sin(.5deg) to centre height and to the direction cone.
    ang=radians(12.5)
    reach=max(abs(q[0]+3.45)*sin(ang)+hypot(q[1]-SY,q[2])+r for _,q,r in parts)
    out('arbitrary roll: reach from working cap, spare to high upper at blade top y9.25',
        reach,25-(9.25+7*sin(radians(.5))+reach+.2))
    out('fold starting y17.50: spare above actual crown contact at blade y<=4.70',
        17.5-(4.7+7*sin(radians(.5))+reach+.2))
    assert 9.25+7*sin(radians(.5))+reach+.2<25.
    assert 4.70+7*sin(radians(.5))+reach+.2<17.5
    for N in [50,100,200]:
        out('contact N, R3/flat patch+GPa, R7/flat patch+GPa',N,*hertz(N,3),*hertz(N,7))
    for rr in [.20,ROLL]:
        req=1/(1/rr+1/.45)
        out('two-convex comparison head R, GPa at 5N, load for 2.5GPa',rr,
            hertz(5,req)[1],5*(2.5/hertz(5,req)[1])**3)


def fold():
    # u is along tongue, v through thickness, (−v,u,0) per radian.
    out('bare tongue: side/tip min opening Nmm per N at u18 v-1.1',
        -MU*hypot(18,1.1),-1.1-MU*18)
    # Side z=+/-(2.65 + .58*(v+1.1)). Opening per N grows with u for
    # u>=3.50: slope dominates friction's u derivative for every v here.
    k=.58
    a=3.5*k/hypot(1,k)
    side=a-MU*sqrt(3.5**2+5.90**2-a*a)
    # Tip u(−1.1)=17.10, du/dv=max(0,.30-v/18). Bound (v+u k)
    # - mu |u-v k| by whole intervals in v, not point samples.
    worst=100.
    for i in range(2000):
        lo=-1.1+7*i/2000; hi=lo+7/2000
        kl,kh=max(0.,.30-hi/18),max(0.,.30-lo/18)
        u0,u1=17.10,17.10+(5.4+1.1)**2/36
        assert u0-max(hi*kh,hi*kl)>0
        torque=(lo+u0*kl-MU*(u1-min(lo*kl,lo*kh)))/hypot(1,kh)
        worst=min(worst,torque)
    out('shaped side/tip Nmm per N; frontmost global x and max halfwidth',
        side,worst,.55+u1,2.65+.58*7)
    assert min(side,worst)>0. and .55+u1<19 and 2.65+.58*7<7.1
    # Terminal closed strip, coplanar bands and outer branch: NOT
    # an upper bound for an unfilled tongue-size opening or uncovered slot.
    ang=radians(35)+asin(.10/.45)
    out('terminal fairing ramp width, .20 seam sag and +x force fraction',
        1.45/tan(radians(35)),.45-sqrt(.45**2-.10**2),cos(ang)-MU*sin(ang))


if __name__=='__main__':
    geometry()
    approach()
    for h in [.015,.035,.055,.080,.100]:
        ok=cage(h)
        assert ok==(h<=.080)
    bounds()
    pressure_land()
    fold()
