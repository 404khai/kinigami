"""Exploratory dimensional screens; mm, N, MPa. No gate/solver results."""
from itertools import product
from math import acos, asin, atan, atan2, cos, degrees, dist, hypot, pi, radians, sin, sqrt, tan


def show(key, *v):
    print(key, *(round(x, 5) for x in v))


def add(a, s, b):
    return tuple(x+s*y for x, y in zip(a, b))


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def rot(a, angle):
    x, r, t = a
    return x, r*cos(angle)-t*sin(angle), r*sin(angle)+t*cos(angle)


def angle(a, b):
    return acos(max(-1, min(1, dot(a, b)/hypot(*a)/hypot(*b))))


def hertz(f, r):
    e = 213000/(2*(1-.29**2))
    w = (3*f*r/(4*e))**(1/3)
    return w, 3*f/(2*pi*w*w)/1000


# A shoulder is the p-offset of a spherical patch on the core; radius R,
# curvature centre K, central direction w, half-angle eps. No mesh sampling.
def near(pt, cap):
    K, w, R, eps = cap
    v = add(pt, -1, K)
    a = max(0, angle(v, w)-eps) if hypot(*v) else 0.
    return sqrt(max(0, dot(v, v)+R*R-2*R*hypot(*v)*cos(a)))


def support(direction, cap):
    K, w, R, eps = cap
    return dot(direction, K)+R*hypot(*direction)*cos(max(0, angle(direction, w)-eps))


def far(cap):
    K, w, R, eps = cap
    return sqrt(dot(K, K)+R*R+2*R*hypot(*K)*cos(max(0, angle(K, w)-eps)))


rad = radians
p, bs, mu = 5.8, 2.4, .23
phi, beta, gamma, alpha, eps = map(rad, (39, 23, 25, 35, 5))
D, height, br, rd = 11.65, 3.20, 2.50, 4.2
n = (sin(phi), -cos(phi), 0.)
m = tuple(-x for x in n)
P = (-.187, (D-.187*sin(phi))/cos(phi), 0.)
C = add(P, height, n)
W = (-7., 4., 0.)
v = (cos(alpha), sin(alpha), 0.)
S = add(W, -br, v)
plane = S[0]+.63
disk = 5.95
rear = (add(W, -rd, v), v, rd+p, eps)
lock = []
backs = []
for i in range(3):
    az = i*2*pi/3
    for sign in (-1, 1):
        u = (sin(beta)*cos(gamma), cos(beta)*cos(gamma), sign*sin(gamma))
        lock.append((rot(add(C, 4.2-bs, u), az), rot(tuple(-q for q in u), az), 4.2+p, eps))
    backs.append((rot(rear[0], az+pi/3), rot(v, az+pi/3), rd+p, eps))


def geometry():
    ph = rad(37)
    c = add((-.187, 12.593, 0), 2.25, (sin(ph), -cos(ph), 0))
    u = sin(beta), cos(beta), 0
    gmax = acos((dot(c,c)+(bs+p)**2-(10-p)**2)/(2*(bs+p)*dot(c,u)))
    show('supplied trial h2.25 gamma max in R10; park phi min (a2.49/p5.75)', degrees(gmax),
         degrees(asin(2.49/5.75)+atan(mu)))
    for g in (25, 28, 30):
        gg = rad(g)
        q = add(c, -(p+bs), (sin(beta)*cos(gg), cos(beta)*cos(gg), sin(gg)))
        show('gamma, necessary bounding B at centre of shoulder', g, hypot(*q)+p)
    show('revised P, C (x,r)', *P[:2], *C[:2])
    cap = lock[1]
    q = add(cap[0], cap[2], cap[1])
    a = add(cap[0], 4.2, cap[1])
    show('one lock contact A, core Q', *a, *q)
    show('back contact / equivalent axial pitch arm', *W[:2], W[1]-W[0]*tan(alpha))
    show('rear core extent R4 vs R5 (without finite patch)', hypot(*add(W,p,v))+p,
         hypot(*add((-7.,5.,0.),p,v))+p)
    show('working patch half widths lock, back', 4.2*sin(eps), rd*sin(eps))
    show('p-offset full-cap gap vs all 3 lock planes: lock, backs',
         *(D-p-max(support(m, a) for a in caps) for caps in (lock, backs)))
    sphere_bound = max(map(far, lock+backs))+p
    show('complete patches B excluding neck; largest core d', sphere_bound, sphere_bound-p)
    show('full-ball locked gap to own patches, adjacent locks, back patches',
         *(min(near(C,a)-p-bs for a in caps) for caps in (lock[:2], lock[2:], backs)))
    s = rot(S,pi/3)
    show('rear full pad ball gap to all lock shoulders/other rear shoulders/own',
         *(min(near(s,a)-p-br for a in caps) for caps in (lock,backs[1:],backs[:1])))
    # Worst rear meridian: as angle increases the point moves aft; squared
    # distance to the disk rim decreases here (relative vector to K verified).
    q = add(rear[0], rd+p, (cos(alpha+eps),sin(alpha+eps),0))
    ed = hypot(q[0]-plane, max(0.,q[1]-disk))-p
    show('x plane including buried crowns; back pad core vs front disk edge gap',plane,ed)
    # Intact sphere b and rear neck centreline (O..+X) are separate from lobes.
    show('centred b max from pad spheres; nominal b6.65 gap',hypot(*S)-br,hypot(*S)-br-6.65)
    show('button port lock/park distance and outer-lip sag',
         height+3.22,p-sqrt(p*p-2.49**2),3.22-(bs+.02)-(5.75-sqrt(5.75**2-2.49**2)))
    k = cos(phi+beta)*cos(gamma)
    for load, R in ((145.07,1/(1/bs-1/4.2)),(191.47,1/(1/br-1/rd))):
        aw,p0 = hertz(load,R)
        show('N, relative R, Hertz a/p0 (GPa)',load,R,aw,p0)
    side = 145.07*(sqrt(1-k*k)+mu*k)
    bm = side*3.8+145.07*mu*bs
    show('locked transverse demand, single-flank moment at 3.8, dia3.0 stem MPa',side,bm,bm/(pi*3**3/32))
    # Distance between actual working points; a convex hull across tangent points
    # would fill this groove, regardless of original smooth dishes.
    g = gamma
    show('lock two tangency-point span, chord penetration if bridged',2*bs*sin(g),bs*(1-cos(g)))
    # Test pitch clearance with the filled core bridges from O to every patch
    # (one radial segment per point, NOT the convex hull across a dish).
    def bridge_gap(pt, caps, radius):
        vals = [hypot(*pt)-p-radius]
        nseg = 500
        for cap in caps:
            K, w, R, ep = cap
            for j in range(nseg):
                f = (j+.5)/nseg
                cc = tuple(f*z for z in K), w, R*f, ep
                vals.append(near(pt,cc)-radius-p-far(cap)/(2*nseg))
        return min(vals)
    show('lower gap full spherical buttons vs NON-working bridges: front/back',
         bridge_gap(C,lock[2:]+backs,bs),bridge_gap(s,lock+backs[1:],br))
    show('centrally joined core max radial support, b assumed 6.65; shell is hollow',
         sphere_bound-p)
    assert 10.65<degrees(gmax)<10.67 and ed>.18 and min(near(C,a) for a in lock)>p+bs-1e-8
    return sphere_bound


def ejection(B):
    # All dimensions provisional. h and e here relative to COMPLETE hoop plane.
    b, H, xhoop, hook, r = 6.65, 20.7, 12.8, 2.05, disk
    B = B+.15
    h = B-(xhoop-hook)+.2
    e = h
    def cover(x):
        # Solid column extends to e and cannot be entered from aft.
        dx = max(0.,x-e)
        return r+sqrt(max(0., b*b-dx*dx))+sqrt(max(0., b*b-x*x))-H
    show('B/h,e,hoop H; upper coverage at 0 and h',B,h,e,H,cover(0.),cover(h))
    show('at h, gap between allowed centre radii',
         r+b,H-sqrt(b*b-h*h))
    # Stronger disproof: a gap exists even at the HOOP plane, regardless of
    # forward overtravel; not a realizable physical jam proof.
    assert r+2*b<H and h<b
    stroke = (xhoop+e)-plane
    show('piston plane, terminal absolute x, stroke; 3 stages at 6 each deficit',
         plane,xhoop+e,stroke,stroke-18.)
    # Positive virtual translations for ordinary walls versus EMPTY port.
    cur = (B-p)/(7.+p)
    cmin = sqrt(1-cur**2)
    k = .38
    req = mu*hypot(1,k)/hypot(1,mu)
    amin = phi-rad(.30)-asin(2.49/5.75)
    show('common-v margins: cylinder, plain facet, EMPTY lip (sufficient test)',
         k*cmin-req,sin(phi-rad(.30))-k*cos(phi-rad(.30))-req,
         sin(amin)-k*cos(amin)-req)
    show('min empty lip angle, no lateral perturbation margin',degrees(amin),sin(amin)-mu*cos(amin))
    # Telescoping tapered stages: as each stage extends, its thicker aft end
    # stays behind the NEXT stage lip. At collapse, that same lip must pass the
    # largest OD on the inner stage. Wall, bearing and step width are real.
    for travel in (6.,stroke/3):
        length = travel+2.5
        taper = tan(rad(18))
        dr = length*taper+.75+.12
        R = [disk+i*dr for i in range(3)]
        largest = R[-1]+length*taper
        # 3 front shoulders stepped 0.55 axially in home. Witness at the
        # OPEN outer shoulder, compare a rear tail core on its own meridian.
        outer_plane = plane-1.1
        q = add(rear[0],rd+p,(cos(alpha+eps),sin(alpha+eps),0))
        dist_to_annulus = hypot(q[0]-outer_plane,max(0.,R[-1]-q[1],q[1]-largest))
        show('telescope travel/stage, collapsed barrel length/OD, core vs outer shoulder',
             travel,length+1.1,2*(largest+.55),dist_to_annulus-p)
    return stroke


def inventory(stroke):
    # Three normal slides with floating opposing pickup cups and a hard
    # closing limit on INPUT travel. Spring never bottoms at maximum travel.
    sopen, sl = 3.22, height+3.22
    d, dm, turns, G = .80, 4.10, 5, 76000.
    K = G*d**4/(8*dm**3*turns)
    wahl = (4*dm/d-1)/(4*dm/d-4)+.615*d/dm
    dp = 30/K
    err = .8/K
    show('per coil k, compression at 30, allowed total motion error +/-',K,dp,err)
    show('coil ID/OD, nominal shear at 32, active+2 solid length',
         dm-d,dm+d,wahl*8*32*dm/(pi*d**3),(turns+2)*d)
    # Ratio screw-axis stroke to normal follower. Avoid concentric central
    # draw hardware. Slotted tracks push cups (series spring) and pull rods.
    k = .65
    ramp = k*cos(phi)/(1-k*sin(phi))
    travel = (sl+dp+.2)/k
    mtor = lambda f: f*1.75*tan(atan(.5/(pi*3.50))+atan(.18/cos(rad(30)))) + 1.8
    for loss in (.0,.25):
        f = 3*32*k/(1-loss)
        show('working drive trial loss, screw axial load, 2:1 motor torque @.8 efficiency',
             loss,f,mtor(f)/1.6)
    show('ramp dr/dx, axial ramp/stroke then piston/stroke, total nut stroke',ramp,travel,stroke,travel+stroke)
    side = 145.07*.99
    M = 632.91
    show('LWL2 linear interaction screen, LWL1 same (conservative axial allocations)',
         side/381+M/420,side/113+M/60)
    rail = 12.5+sl+1
    end = add(P,-rail,n)
    show('in-line LWL2 rail length and outer end x,r',rail,*end[:2])
    # Diametrically opposed point on complete front ring can be chosen after
    # the tail pose is fixed. This is a real p-interior ball, not a bound box.
    cup = 28.
    xt, xh, rh = -13.,cup+12.8,20.7+.7
    ax, rr, _ = add(W,p,v)
    # Rear pad at azimuth 180 (=60 + 120), along -y. Conservative axial
    # projection even after bending the existing hinge: all bends continuous.
    min_dx = xh-((xt+ax)*cos(rad(15))+rr*sin(rad(15)))
    show('two-end straight D witness; folded lower bound incl all +/-15',
         hypot(xh-(xt+ax),rh+rr)+p,hypot(min_dx,rh)+p)
    show('max straight head datum given actual rim + rear witness',sqrt((60-p)**2-(rh+rr)**2)+(xt+ax)-12.8)
    rho=.008
    shellmass=lambda rad0,t: 4*pi*(rad0**3-(rad0-t)**3)/3*rho
    show('304 hollow sphere trial grams D20/D22 /.8; six solid shoes excluded',
         shellmass(10.,.8),shellmass(11.,.8))
    show('separate mass allocations g: three b2.4 full steel balls, three coil bodies only, sleeve 3x shell',
         3*4*pi*bs**3/3*.0078,3*pi*d*d/4*pi*dm*(turns+2)*.0078,
         sum(2*pi*(disk+i*(8.5*tan(rad(18))+.87)+4.25*tan(rad(18)))*8.5*.75*.0078
             for i in range(3)))
    # Draw cage alternate, two +/-y shafts at R6, rear y-tab spans them;
    # rotate runner pair to 45deg to bypass BOTH orthogonal stacks.
    off, padR, rod, w = 6.35, 3.2, .85, 1.55
    show('twin runner/crossed tabs gap at 45deg, central disk rim minus rod outer',
         off/sqrt(2)-w-rod, disk-(off+rod))
    # Long legs stay in fixed bearings (4 mm spacing), 1 N lateral tip at
    # final free length = max travel; one pad can carry ALL ejection load.
    span = stroke+1.5
    show('runner tip lever, 8N at single rim bearing couple / per shaft Euler P pin-pin',
         span,8*disk/4,pi*pi*200000*pi*(2*rod)**4/(64*span**2))
    assert hypot(min_dx,rh)+p>60 and rail>19 and travel+stroke>35


def common_cup():
    print('\nCOMMON Ø24.96 DATUM, separate from previous branch')
    ph = rad(37)
    b = 2.41
    cc = (-.570,10.950)
    # Infer local port plane from specified foremost lip. h0 is a proposed
    # machining datum, NOT read from the other study.
    a, amin = 2.49, 2.455
    px = -.320-a*cos(ph)
    h0 = (cc[0]-px)/sin(ph)
    pr = cc[1]+h0*cos(ph)
    normal = sin(ph),-cos(ph)
    mer = cos(ph),sin(ph)
    parked = -1.928
    sh = h0-parked
    P0 = (px,pr)
    show('inferred P0 x,r, lock h, shoe stroke, parked centre/tip x',*P0,h0,sh,
         add(P0,parked,normal)[0],add(P0,parked,normal)[0]+b)
    # Maximum over every layer T and stroke s. Worst h and T largest,
    # derivative wrt phi = -(b*cos(phi)+T+h)/sin(phi)^2 <0 here.
    pm = rad(36.7); T=.60; hp=parked+.04
    sstar = (T+hp+b*cos(pm))/sin(pm)
    proj = b/sin(pm)+(T+hp)/tan(pm)
    drift = .02+.035+18*sin(rad(.13))
    show('thin moving wall critical translation, swept footprint, free drifted gap',
         sstar,proj,amin-proj-drift)
    st = 9.
    show('9mm normal shield margin after sag, drift and exposed shoe; projected hole gap',
         (st-.1)*sin(pm)-(hp+b)-(5.75-sqrt(5.75**2-2.51**2))-.10,
         (st-.1)*cos(rad(37.3))-2*2.51-.10)
    show('37deg empty aperture friction-cone shortfall (deg)',
         degrees(asin(2.51/5.75)+atan(mu))-36.7)
    # Do NOT reuse parallel-layer sweep for a 45deg local facet. Upper bound
    # only if a round coaxial tool gauge is passed through EVERY layer.
    for rr0 in (2.49,5.35):
        show('37/45deg oblique distance across facet radius',rr0,rr0*tan(rad(8)))
    # The metal cap cannot first pass through a permanently installed Ø3 guide.
    # Mount outside from behind when the split collar/guide has been removed.
    G, d, dm, na = 76000.,.8,4.1,5.
    K=G*d**4/(8*dm**3*na)
    dl=30/K; free=9.6
    solid=(na+2)*d
    cap32=32/K
    behind=4.4+free-dl+1.25
    lockpin=add(add(cc,-behind,normal),-3.6,mer)
    parkpin=add(lockpin,-(sh+dl+.2),normal)
    show('cam pin locked & parked x,r (conical face offset aft 3.60)',*lockpin,*parkpin)
    show('coil available additional compression before solid at 32, external shoe back travel',
         free-solid-cap32,sh)
    # Current continuation is a direct one-way closing pusher. If a spring
    # cannot stay below the cap to complete park, solid is a BYPASS, not safety.
    show('locked 30N additional deflection for 32N, preload max allowed displacement',
         2/K,.8/K)
    show('minimum rear-seat overrun until h=-4.15, gauge double-shear pin MPa @32N',
         h0+4.15+.25,32/(2*pi*.25**2/4))
    for e in (4.7,11.):
        lateral=145.07*1.03
        moment=lateral*e+mu*145.07*bs
        reactions=lateral+2*moment/6.2
        show('guide arm, one loaded pad reaction, summed normal, .006 dynamic / .18 dry drag',
             e,lateral+moment/6.2,reactions,.006*reactions,.18*reactions)
    # Reversible 0..108 deg, three repeat stations 120 deg apart. Budgets:
    # first lower force then pick up shoe, only then move cup.
    # Half-cosine phase; upper estimates assume peak force AND slope coincide.
    R=max(lockpin[1],parkpin[1])
    def torque(stroke,deg,force,r,nf,drag):
        v = pi/2*stroke/rad(deg)
        return nf*r*force*tan(atan(v/r)+atan(drag))
    lam=atan(.50/4.5)
    for drag in (.02,.18):
        eff=tan(lam)/tan(lam+atan(.12/cos(rad(20))))
        for title,ss,deg,F,r,nf in (('unload/close',dl+.2,26,32,R,3),
                ('withdraw',sh,44,32,R,3),('withdraw dry-guide 95N each',sh,44,95,R,3),
                ('cup',9,32,18,18.5,1)):
            t=torque(ss,deg,F,r,nf,drag)
            show(title+' drag/ring Nmm/90:1 worm motor Nmm',drag,t,(t+15)/(90*eff))
    # Cam lips as finite strips; not a solid conical annulus. Estimate plate
    # stock with both side rails and bottom web for 3x108degree cam grooves.
    path=3*R*rad(108)
    show('ring groove minimum gross strip length; steel mass (6.1 x 2.2) before grooves',
         path,path*6.1*2.2*.0078)
    # Aft yoke and two hardened rods at +/-45deg, R15.60, fixed split bushes.
    rr=15.6; rod=1.25
    show('full-stroke aft rod overlap beyond aft bush; rod to crossed tab half-width',
         -16.0-(-26.5+9.1),rr/sqrt(2)-1.55-rod)
    span=6.5
    show('8N one-rim ejection bearing couple with off-centre takeoff; friction debit @.23',
         8*(18.5+12.48)/span,.23*2*8*(18.5+12.48)/span)
    show('18 N available upper vs corrected 8N+drag; dry binding factor 2mu*driveoffset/span',
         18,8+.23*2*8*(18.5+12.48)/span,2*.23*18.5/span)
    L, ecc = 9.80, 9.20
    req=(8+2+.23*2*8*12.48/L)/(1-2*.23*ecc/L)
    show('separate cup screw corrected guide binding factor/thrust and screw torque',
         2*.23*ecc/L,req,req*1.75*tan(atan(.5/(pi*3.5))+atan(.18/cos(rad(30))))+1.8)
    # Home-load stop: three individually shimmed flats exactly behind pads;
    # bolts/rails do not absorb a designed constant preload.
    show('one seat nominal axial, lateral, pitch over .6 stock, pad3x3 bearing MPa',
         191.47*cos(rad(35)),191.47*sin(rad(35)),191.47*sin(rad(35))*.6,
         191.47*cos(rad(35))/9)
    # Nose/foot clearances & drive fits are conditional. All axes z=+1.20.
    # Sleeve outer ring R22.5 tooth pitch, axial location -21.5. A specific
    # rotating, full cylindrical fixed-stock guard is used (not a swept circle
    # substituted for permanent material when deriving an impossibility).
    hx,tx,ox=22.,-13.,4.35
    ringr=R+2.5
    def diam(x1,x2,r):
        return 2*hypot(max(abs(hx+x1-ox),abs(hx+x2-ox)),r)
    show('selected diam head button ring guard, cup rim guard, worm outer gear guard, tail sphere upper',
         diam(parkpin[0]-1.4,lockpin[0]+1.4,ringr),diam(2.,3.,18.2),
         diam(-23.2,-19.8,23.5),2*(ox-tx+12.48))
    # Physical interference of rack alternative with full unwindowed stationary
    # rear race at x=-22.3: circle ray at the proposed rod azimuth.
    # Keep two relief windows in STATIONARY cheeks; CANNOT window 360 races.
    show('rod to proposed R17.60 race bore, moving rod bosses R2.35 at R15.6',
         17.60-rr-rod,17.60-rr-2.35)
    # Complete low-table feet need clearance below new large-radius fixed guard.
    show('proposed guard radius/foot span at +.45 below guard, 60-sphere about ox',
         ringr,2*sqrt(max(0.,30**2-(ringr+.45)**2)))
    assert amin-proj-drift>0 and 0<sstar<st and free-solid-cap32<sh


def swing():
    print('\nCOMMON +t TANGENTIAL SWING; no straight-slide force credit')
    L, h0, hl = 18., 2.450, 3.020
    ph=rad(37)
    n=(sin(ph),-cos(ph),0)
    m=(cos(ph),sin(ph),0)
    qlock=asin((hl-h0)/L)
    V=(18.430-(hl-h0)*n[0],10.950-(hl-h0)*n[1],L*cos(qlock))
    O=(.514,0.,0.)
    def point(q,u,t,w=0.):
        return add(add(add(V,u*cos(q)-t*sin(q),n),w,m),u*sin(q)+t*cos(q),(0.,0.,1.))
    def cyl(centre,axis,r,l):
        v0=add(centre,-1,O)
        x=dot(v0,axis)
        return 2*hypot(abs(x)+l/2,sqrt(max(0.,dot(v0,v0)-x*x))+r)
    def tcyl(x,r,t1,t2,b):
        return cyl((x,r,(t1+t2)/2),(0,0,1),b,t2-t1)
    show('global virtual pivot x,r,t, local x',*V,V[0]-19)
    for h in (hl,-1.928,-4.10):
        q = asin((h-h0)/L)
        xi,ri,ti=point(q,-9.5,-5.)
        x,r,t=point(q,-9.5,-5.,-2.8)
        N=-9.5*cos(q)+5*sin(q)
        Tp=-9.5*sin(q)-5*cos(q)
        rp=cos(ph)*Tp
        ap=(r*N-t*rp)/(r*r+t*t)
        show('h,deg,crank global x/r/t, screw tangent F at 32.8 plus 12Nmm trial bearing drag',
             h,degrees(q),xi,ri,ti,(32.8*L+12)/abs(N))
        show('aft pin x/rho/az, hoop rad/rad, one/all3 hoop torques @32.8 before losses',
             x,hypot(r,t),degrees(atan2(t,r)),ap,32.8*L/abs(ap),3*32.8*L/abs(ap))
    for w,r,l in ((.4,5.5,4.5),(4.7,5.5,4.5),(-5.,5.5,4.5),(-17.,5.5,4.5),(-4.,4.,4.)):
        v=add(V,w,m)
        show('pivot race w, D actual stock about prescribed centre',w,cyl(v,m,r,l))
    # Witness on 11-mm race rim, NOT its centre hole. Rotate to station
    # 120 degrees then add raised z datum. Also lies inside the Cell x range.
    v=rot(add(add(V,-17.,m),-5.5,(0,0,1)),2*pi/3)
    show('rear race rim x,y,z vs cell',v[0],v[1],v[2]+1.2)
    w1,w2=-5.,-17.
    Fs,Fin=198.,65.
    mm=L*Fs+.23*192.064*2.41
    rb=(mm+abs(w1)*(Fs+Fin))/(w1-w2)
    show('robust overbound rear/front race radial (NOT simultaneous predictions)',rb,Fs+Fin+rb)
    show('MTA04-11 axial-only, radial-only C0 N',1410,282)
    # Illustrative, admissible transverse arm test, NOT a nine-face solution.
    # 100N purely along pivot axis at 18 mm remote => 150N paired couple.
    show('single 100N axial-to-pivot load, two-race couple over 12',18*100/12)
    # M2x.4, pitch diameter 1.74, opposed supported thrust pair. Spring/guide
    # friction trials add 2N and 12 Nmm at swing axis, 1 Nmm on screw.
    F=(32.8*L+12)/abs(-9.5*cos(qlock)+5*sin(qlock))+2
    tm=F*.87*tan(atan(.4/(pi*1.74))+atan(.18/cos(rad(30))))+1.
    show('working screw N/Nmm, GP6A output after motor 25:26 gear/.85, min GP efficiency',
         F,tm,tm/(26/25*.85),tm/(26/25*.85*.324*(531441/2401)))
    show('jam at 27 Nmm screw: frictionless upper axial load, crank torque at max arm',
         27*2*pi/.4,27*2*pi/.4*10.67)
    show('tangential motor, gears, cartridge envelope D at x+.514',
         tcyl(11.4,14.375,-9.,19.7,3.2),tcyl(11.4,20.75,-12.35,-11.1,3.85),
         tcyl(11.4,20.75,-4.,12.8,3.10))
    elbow=point(qlock,-6.15,-18.,-2.2)
    g0=hypot(elbow[0]-11.4,elbow[1]-14.375)-3.
    show('locked elbow corner and signed gap to actual motor',*elbow,g0)
    # A solid screw witness at deep park: nearest actual member point can
    # slide within the beam thickness and its 4.40 meridional width.
    q=asin((-4.10-h0)/L)
    pts=(point(q,-6.15+u,-18.+t,w) for u,t,w in product(
        (-1.1,0.,1.1),(0.,.5,1.),(-2.2,-1.,0.,1.,2.2)))
    gg,z=min((hypot(v[0]-11.4,v[1]-20.75)-.75,v) for v in pts if -4.<v[2]<10.)
    show('deep parked beam vs M2 root cylinder, signed gap and x,r,t',gg,*z)
    ser=degrees(asin((10.65-1.2)/21.5));cell=degrees(asin((15.325-1.2)/21.5))
    show('abandoned linear stage: guaranteed servo/cell angular sectors, overlap',
         ser,cell,ser+cell-60)
    assert g0 < -1.4 and gg<0 and -22.<v[1]<-1.3 and 1.5<v[0]<6.9

    print('\nBEVEL + BOTTOM CELL: 35 pitch, x19/-16, trial sphere centre (0,0,0)')
    show('undimpled R12.48/.8 304 shell mass; three RE6A + GP6A estimate g',
         4*pi/3*(12.48**3-11.68**3)*.008,3*(2.3+2.9))
    s0=point(0.,-5.85,0.,-4.)
    x,r=s0[:2]
    rho=15.92
    t=-sqrt(rho*rho-r*r)
    front=x-5.55
    aft=front-28.7
    clock=pi/2-atan2(t,r)
    motors=[rot((0,r,t),clock+i*2*pi/3) for i in range(3)]
    shafts=[rot(add(V,-17.,m),clock+i*2*pi/3) for i in range(3)]
    htest=-3.91013
    q=asin((htest-h0)/L)
    # Directly specified solid section; tangent screw major-root cylinder
    # includes r=.75 and runs through the point's measured t. No box contact.
    hit=point(q,-7.25,-8.)
    show('parent bevel witness h,q,beam x/r/t and signed screw-root gap',
         htest,q,*hit,hypot(hit[0]-12.2,hit[1]-19.)-.75)
    show('revised meridional and cross-section e,n,x,r,t motor, x aft/front, clock deg',
         -4.,-5.85,x,r,t,aft,front,degrees(clock))
    show('motor 3x guard D, intermotor gap, worst bottom cell vertical gap, local tail B margin',
         2*hypot(aft,rho+3.2),sqrt(3)*rho-6.4,min(k[2] for k in motors)-3.2+15,
         rho-3.2-12.48)
    cellD=2*hypot(14.,15.325,20.4)
    show('bottom cell D, original provisional front/secondary disk D, core-offset bound D',
         cellD,2*hypot(22.1,20.),2*hypot(9.5,22.),2*(hypot(22.15,6.68)+5.8))
    for i,(xx,y,z) in enumerate(shafts):
        _,ym,zm=motors[(i+1)%3]
        g=hypot(y-ym,z-zm)-3.0
        show('station index, e-17 solid axle centre global x/y/z, signed gap next bare motor',i,xx,y,z,g)
        assert aft<xx<front and g<-.71
    # Arm's x is increasing in e, and n is smallest at min q, tip end
    # (-18 t) for q<0. For positive q lower bound is -7.25 outright.
    qp=asin((-4.12-h0)/L)
    low=V[0]-2.2*m[0]+(-7.25*cos(qp)+18*sin(qp))*n[0]
    show('beam x lower bound, axially clear three motor bodies by',low,low-front)
    show('e-plane gaps screw to beam; flattened 2.90-wide crosshead to beam',
         4.-2.20-1.,4.-2.20-1.45)
    # Brake/clutch position and spring are not installed. Working target
    # tangent 32, independent flexure measurement required downstream.
    for h in (3.02,-4.10):
        qp=asin((h-h0)/18.)
        tp=point(qp,-9.5,-5.)[2]
        show('h; crank pin t, fork datum; nut datum loaded vs picked-up park',
             h,tp,tp-12.5,tp-12.5+(-2.15 if h>0 else .18))
    xx=19.+3.30+4.+.30; rf=18.39+4.30*tan(rad(14.4))+.40
    show('max straight 4mm-sleeve pitch vs rear p-ball alone',
         sqrt((60-5.8)**2-(rf+2.95+5.8*sin(rad(35)))**2)
         -(xx-19)+(-9.92+5.8*cos(rad(35))))
    # Slot/guide assumptions, not catalogue guaranteed. Rotate at full
    # exposure including h tolerance. For screw start use dry effective
    # fork and keyed guide friction, not just the previous 2-N loss.
    qh=asin((3.055-h0)/L)
    N=abs(-9.5*cos(qh)+5*sin(qh))
    dN=abs(-9.5*sin(qh)-5*cos(qh))
    for us,ug in ((.03,.03),(.18,.18),(.23,.23)):
        F=(32.8*18.+12.)/(N-us*dN)
        # guide pads straddle screw, two support planes 7.5 apart along t;
        # 5.1 normal-to-screw eccentricity incl slot width; no equal sharing.
        guide=2*5.1*F/7.5+us*F
        thrust=F+ug*guide+2.
        tm=thrust*.87*tan(atan(.4/(pi*1.74))+atan(.18/cos(rad(30))))+1.
        show('fork/guide mu, pin thrust, guide normal sum, screw force/torque, bevel eta_min vs 30 Nmm, GP eta_min @.85',
             us,F,guide,thrust,tm,tm/30.,tm/(.85*.324*(531441/2401)))
    show('jam: crank radius and roll, screw 27Nmm frictionless upper thrust; e-17..-5 reactions upper at fault',
         hypot(9.5,5.),2.55,27*2*pi/.4,
         (mm+5*198+abs(-4+5)*27*2*pi/.4)/12,
         198+27*2*pi/.4+(mm+5*198+abs(-4+5)*27*2*pi/.4)/12)
    # Take 24's fixed sleeve must remain ahead of moving rim. This is
    # physical stock, not the deployed pose imposed as a stow condition.
    xr=-16-9.920+5.8*cos(rad(35))
    rr=2.950+5.8*sin(rad(35))
    for st in (4.,9.):
        xx=19.+3.30+st+.30
        rrim=18.39+(st+.30)*tan(rad(14.4))+.40
        both=hypot(xx-xr,rrim+rr)+5.80
        show('travel, stationary guide x/R, D about zero, actual opposed tail p-ball distance, motor-guard distance',
             st,xx,rrim,2*hypot(xx,rrim),both,hypot(xx-aft,rrim+rho+3.2))
        assert both>60


if __name__ == '__main__':
    inventory(ejection(geometry()))
    common_cup()
    swing()
