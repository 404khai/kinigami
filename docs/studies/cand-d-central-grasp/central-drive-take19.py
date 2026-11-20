"""Take 19: mm, N, N mm; executable exploratory screens, not a gate."""
from itertools import product
from math import asin, atan, cos, degrees, dist, hypot, pi, radians, sin, sqrt, tan

Y, Z = .60, -4.60
APEX, XB, B, RC, DX = 35.60, 34.90, 2.30, 1.0, 2.50
R, BTN, TO = 6.30, 2., 1.84
CREST = APEX + TO + 2*(1-cos(pi/4))
WIDTH = TO+2*sin(pi/4)
TAIL = APEX+sqrt(2)*BTN+.80
PITCH = TAIL + 11.60
EJECT = 6.80
POST = 6.12
MU = .23


def point(x, n, t, a):
    a = radians(a)
    return x, Y+n*cos(a)-t*sin(a), Z+n*sin(a)+t*cos(a)


def jaw():
    D = B+RC
    a0, a1 = (asin(d/D) for d in (DX-.15, DX+.15))
    lo, hi = D*cos(a1), D*cos(a0)
    mn, mx = tan(a0-atan(MU)), tan(a1+atan(MU))
    print("jaw angles deg / centre n / draw-per-radial",degrees(a0),degrees(a1),lo,hi,mn,mx)
    print("neck r.85 nominal min gap; max travel to open n4",lo-RC-.85,4-lo)
    # Adverse one jaw axial load, no equal sharing; dry guide in pressure plane.
    tip = B*cos(a1)
    e, span = 3.50-tip, 2.60
    print("guide overhang / mu*normal-amplification*axial:radial",e,MU*(1+2*e/span)*mx)
    # Four actual series discs; interpolate between two catalog graph/table points only.
    def stack(F):
        return 4*.45-4*(.02+(F-27)*(.05-.02)/(53-27))
    print("D63203 series 4, reference h37,h45, acceptance height window",stack(37),stack(45),stack(37)-stack(45))
    print("37..45N centered draw; single-jaw radial demand for 45N",45/mn)
    print("single-jaw neck bending MPa for 45/mn across 4.328 mm (no fillet Kt)",32*(45/mn)*(TAIL-XB)/(pi*1.70**3))


def faces():
    # Continuous radially-extruded profile; no vertical lip. Root rounding
    # changes the toolpath at |t| near zero, below seated contact at sqrt(2).
    print("V apex/crest, halfwidth, seated button center/shoulder, pitch",APEX,CREST,WIDTH,TAIL-.80,TAIL,PITCH)
    rmin = 4
    print("r4 nearest-sector half-width at bisector minus lip",rmin*sin(pi/3)-WIDTH)
    print("post guide OD1.6, transverse distance beyond lip",POST*sin(pi/3)-.8-WIDTH)
    print("tube inner clearance to R5.20 rotor, bottom z", POST-.80-5.20,Z-POST-.8)
    a = atan(MU)+asin(1.50/(2*2.28))+radians(2)
    guard = .20+2.32/cos(a)+(CREST-XB)*tan(a)
    print("continuous window guard screen alpha, required crest r + .35 metal",degrees(a),guard,guard+.35)
    # Allowance .05 on the guard radius, .05 on centre location, .03 piston radius.
    rg, rpmin, rpmax, jawmin = guard+.05, 2.65-.03, 2.65+.03, 3.-.06
    print("piston-to-open-jaw / annular bypass gap vs min diameter",jawmin-rpmax-.05,rg+.05-rpmin,2*2.28)
    # Exactly the cylinder-equator crossing test while the disk is IN a
    # closed circular guide; not a no-escape proof for a slotted/free rim.
    assert rg+.05-rpmin < 2*2.28
    print("piston face rest/end, tip & crest clearance",32.35,32.35+EJECT,XB-B-32.35,32.35+EJECT-CREST)
    # Reconstruct target plane from 3 measured axial intersections, not pad travel.
    # +/- .05 each allows intercept error .05, gradient vector <=4e/(3r).
    # Exact max over error cube occurs at 2 signs alike and one opposite.
    eps = .05
    Dtail = TAIL-(XB-.15-2.32)
    Rbody = 23.0  # specified footprint limit in head transverse frame; must verify/monitor
    for angle in (0,2,4,8):
        s = tan(radians(angle))+4*eps/(3*POST)
        # Scalar lower bound valid for |transverse position|<=Rbody and
        # signed depth behind the sensed plane <=Dtail.
        xa = TAIL+EJECT-.15-eps
        sep = xa-Rbody*s-Dtail*sqrt(1+s*s)-max(CREST+.10,38.55)
        print("measured tilt, blanket lower bound (nose; then all fixed stock incl upper shaft)",
              angle,sep,sep-(39.35-38.55))
        # Separate depth/footprint bounds; credit only with identified tail
        # targets and verified transverse registration. No moving pad is a gap sensor.
        depth=(TAIL-XB+.15)*sqrt(1+s*s)
        stud=xa-1.10*s-depth-2.32-38.55
        buttons=xa-8.90*s-(.80+2.03+.05)*sqrt(1+s*s)-39.35
        flange=xa-Rbody*s-.10*sqrt(1+s*s)-39.35
        print(" conditional split stud/buttons/body gap",stud,buttons,flange)


def box(lo,hi):
    return list(product(*zip(lo,hi)))


def envelope():
    pts = []
    for x0,x1,y,z in ((1.8,34.4,12.7,12),(-9.4,-1.8,12.7,12),(34.4,35.6,11.9,11.2),(-10.6,-9.4,11.9,11.2)):
        pts.extend(box((x0,-y,-z),(x1,y,z)))
    for a in (90,210,330):
        pts.extend(point(x,n,t,a) for x,n,t in product((35.10,CREST+.03),(4,8.15),(-WIDTH-.05,WIDTH+.05)))
    # Roof housing, motor end guard and output journal are solid envelopes
    # for the outer test, not assumed free internally.
    pts.extend(box((-.65,-5.1,1.9),(29.55,6.3,15.3)))
    for a in (30,150,270):
        pts.extend(point(x,n,t,a) for x,n,t in product((31.7,TAIL-.10),(POST-.85,POST+.85),(-.85,.85)))
    c=(11.39744,.18568,-.29474)
    def sphere(p,r):return dist(c,p)+r
    def x_cyl(x,y,z,r):return hypot(x-c[0],hypot(y-c[1],z-c[2])+r)
    samples=[('solid box/lobe',max(dist(p,c) for p in pts)),
             ('stud',sphere(point(XB-PITCH,0,0,0),2.32)),
             ('tail plate/shoulder',x_cyl(-11.60,Y,Z,7.30)),
             ('head guard',x_cyl(38.55,Y,Z,5.55)),
             ('gearbox capped shaft',x_cyl(39.35,Y,8.60,1.95))]
    for a in (90,210,330):
        samples.append(('tail button',sphere(point(TAIL-.80-PITCH,R,0,a),2.03)))
    print("stowed diameter about",c,[(k,round(2*r,3)) for k,r in samples])
    print("same witness with .15 aft stud location tolerance",
          2*sphere(point(XB-PITCH-.15,0,0,0),2.32))
    print("post housings min z; flat table",Z-POST-.85,-12)
    print("full R8.15 ring bottom z (NOT the lobed frame)",Z-8.15)


def ramp(k,r,m):
    return (k+m*r)/(1-m*k/r)


def drive():
    for mu in (.23,.10,.05):
        k=.50/radians(32)
        # .50 rise over 40 deg less 8 deg of acceleration allowance.
        t=45*ramp(k,3.6,mu)
        k=EJECT/radians(184)
        f=8*(1+2*mu*POST/5.4)/(1-2*mu*4.95/5.4)
        print("mu, draw ramp T45, barrel F8->Fdrive,T",mu,t,f,f*ramp(k,4.95,mu))
    # Positive driven, dedicated nonrotating eject screw in a fixed rotating nut.
    # Entire nut thread retained throughout stroke, use separate full threads
    # in rear tube, not threads in rolling-element bearing races.
    n0,n1=26.45,29.45
    s0,s1=14.70,31.55
    for travel in (0,EJECT):
        print("travel, screw full-thread range / nut overlap",travel,(s0+travel,s1+travel),min(n1,s1+travel)-max(n0,s0+travel))
        assert s0+travel<=n0<n1<=s1+travel
    r,p,lead=1.50,.50,2.0
    k=lead/(2*pi*r); f=MU/cos(pi/6)
    C=r*(k+f)/(1-k*f); Cl=r*(f-k)/(1+k*f)
    F=8*(1+2*MU*POST/5.4)/(1-MU*C/4.0)
    print("centred screw raising/lowering Nmm/N, eccentric single pad F8->screw F,T+3 allowance",C,Cl,F,C*F+3)
    print("hypothetical 16..24 Nmm limiter: frictionless axial / dry lowering+3",24*2*pi/lead,24*2*pi/lead*Cl+3)
    print("3070 one point, instantaneous gearbox limit, 6.8mm time at point (not guaranteed)",
          2.2*98.0665,2.5*98.0665,60*EJECT/(lead*26))
    print("D63203 hole radial room around screw OD3.05",(.5*(3.2-3.05)))
    print("piston head/forward wheel clearance, original / move nut stack aft .55",32.35-.55-32.00,32.35-.55-31.45)
    print("dry face spring torque conditional rated deficit",45*ramp(.50/radians(32),3.6,.23)-49.03)


def inventory():
    # V7 box extents in mm, including retained motor drive PCB and structure.
    motor=((-0.10,-4.4,2.6),(29.,5.6,14.6))
    boxes={"cell":((3.025,-11.4,-10.35),(33.675,-6,10.35)),
           "boost":((23.10,-5.35,2.30),(33.70,10.15,6.55)),
           "head top":((1.80,-4.95,11.78),(22.70,6.15,12.00)),
           "joint motor":((3.08,5.35,-9.85),(9.32,11.50,8.85)),
           "hinge pin":((-1.,-1.,-8.45),(1.,1.,7.60)),
           "SCS0037":((1.70,-4.10,-9.83),(22.58,5.30,11.43))}
    for name,(lo,hi) in boxes.items():
        overlap=tuple(round(min(a,b)-max(c,d),3) for a,b,c,d in zip(hi,motor[1],lo,motor[0]))
        print("N20 vs",name,"signed xyz overlaps",overlap)
    for mass in (50,60):
        W=.001*mass*9.80665
        print("sensitivity mass g / 4W / W PITCH / 25.4W",mass,4*W,W*PITCH,25.4*W)


def larger():
    b, nose, xj, rj = 3.215,.8,XB+3.437,2.066
    min_tip=XB-.15-b
    piston=min_tip-.20
    open_inner=b+.45+.15
    stroke=open_inner+nose-rj
    print("separate B3.2: xj, rj, rear tip, piston home, full nose front, tail gap",
          xj,rj,min_tip,piston,xj+nose,TAIL-(xj+nose))
    print("radial stroke (incl drift), centred initial required radial/axial lead",stroke,3.437/rj)
    print("piston end at 6.8 / min travel beyond full nose+.20",piston+EJECT,xj+nose+.20-piston)
    c=(XB-.15-PITCH,Y,Z)
    print("sphere-to-upper-shaft cap centreline witness pair distance",
          b+dist(c,(39.35,Y,8.60)))
    print("B3.2 wheel-front max for .55 piston and .15 no-rub",piston-.55-.15)
    # Worst positive tilt contact requirement at the initial compression
    # stage depends on relative pose, not just how quickly the input turns.
    assert xj+nose < TAIL and piston+EJECT<xj+nose


def hex_guard():
    print("slotted hex supplement: separate B3.20 geometry")
    b, Bhi, w, web, neck = 3.185,3.215,1.30,1.13,.96
    D=TAIL-XB+.15
    for m in (.35,.42):
        E=hypot(1,m)
        a_req=(Bhi+.07)*E+.15*m+.20+.04
        print("slope / original seated normal clearance / needed a0 / original full-nose s",
              m,(3.55-.15*m)/E-Bhi,a_req,3.55+3.437*m+1.10*E-2.066)
        for radius in (b,neck):
            # Bounding sphere medial point behind the nearest of two straight
            # lips. Normal is perpendicular to longitudinal generator (1,m,0).
            n=sin(atan(m))*sqrt(1-(w/(2*radius))**2)
            alpha=asin(n)-radians(2)
            print("bridging radius / min axial resultant per N after 2deg debit / intrusion",
                  radius,sin(alpha)-MU*cos(alpha),radius-sqrt(radius**2-(w/2)**2))
    m,a0=.42,3.87
    A=lambda x:a0+m*(x-XB)
    E=hypot(1,m)
    print("corrected s including .04 guard profile plus .05 positioning",
          A(XB+3.437)+1.10*E-2.066+.04+.05)
    print("per-side slot clearance, nominal/worst before guide drift",(.5*(1.25-1.10)),.5*(1.20-web))
    for t,h in ((0,.40*(sqrt(2)-1)),(sqrt(2),sqrt(2)),(1.84,1.84),(WIDTH,CREST-APEX)):
        print("V t / min site radial coordinate for .50 true stock",
              t,(A(APEX+h)+.5*E-.5*t)/cos(pi/6))
    for r,clock in ((6.12,0),(6.80,20)):
        h=r*cos(radians(30-clock))-.80
        print("post R/clock/guard wall conservative/lip transverse margin/table margin",
              r,clock,(h-A(CREST))/E,r*sin(radians(60-clock))-.80-WIDTH,
              12+Z-r*cos(radians(clock))-.80)
    xp=XB-.15-Bhi-.20
    print("R1.75 piston minimum disk/hex clearance corrected / R3.45 old",
          A(xp-.55)-.04-.05-1.78,3.55+m*(xp-.55-XB)-3.45)
    for x in (CREST,39.35):
        # Equatorial section while 6 enclosing faces exist except slots.
        # For centre outside the nearest lip pair, a full face excludes it.
        eroded=(A(x)+.04-sqrt(b*b-(w/2)**2))/cos(pi/6)
        print("x / equatorial centre radial bound / disk bypass reserve",
              x,eroded,1.72+b-eroded-.05)
    for ang in (0,2,4,8):
        s=tan(radians(ang))+.20/(3*6.8); h=hypot(1,s)
        rc=.45+D*s/h
        xa=TAIL+8.002-.15-.05
        print("measured tilt / conditional whole-stud, buttons, body distances",
              ang,xa-rc*s-D*h-Bhi-(XB+3.437+.80),xa-9*s-2.88*h-39.35,xa-23*s-.10*h-39.35)
    assert A(xp-.55)>.04+.05+1.78 and A(CREST)>4.


if __name__ == "__main__":
    print("exploratory – Take 19, no acceptance or independent review")
    jaw(); faces(); envelope(); drive(); larger(); inventory(); hex_guard()
