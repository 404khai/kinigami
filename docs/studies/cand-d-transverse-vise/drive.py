"""Exploratory bench/paddle layout. Dimensions mm, force N, torque N mm."""
from itertools import product
from math import acos, asin, atan, cos, degrees, hypot, pi, radians, sin, sqrt, tan


def show(what, *xs):
    print(what, *(round(x, 5) for x in xs))


def box(x, y, z):
    return 2*hypot(*(max(abs(lo),abs(hi)) for lo,hi in (x,y,z)))


def cylinder(a, b, u, v, r):
    """Diameter about the origin; shaft from a..b, perpendicular centre (u,v)."""
    return 2*hypot(max(abs(a),abs(b)),hypot(u,v)+r)


def section():
    # Identical units at x0, +30; fixed hinge off the plug, pin along z.
    for a in (180,60,-60):
        show('boss centre x,y,z',15+7*cos(radians(a)),0,7*sin(radians(a)))
    show('closed/fully open y face; spine thickness behind it',3.50,9.50,7.)
    show('six mm open; blade y lower/upper nominal clearances',-.0-1.5+1.70,9.50-9.25)
    show('flat R2.5 / full cassette R4 front x, blade at 15stroke x',17.50,19.00,19.15)
    show('plug retracted/extended x back/front, minimum upper disk overlaps at terminal',
         -4.50,4.15,10.5,19.15,11.-10.50,19.15-19.,4.8-4.)
    show('original hinge penetrates full-height plug; relocated pin-to-plug y gap',
         min(4.5,4.15,1.5,9.25,4.8),-1.5-(-6+1.))
    # Exact finite pin-clearing solid. An unstepped 2.2-thick full-width
    # platen WOULD foul the visor if it also ran through the open gap.
    show('upper jaw clearance if guide land protrudes .30 below flat at open',9.5-.30-9.25)
    # Foot coordinates in nominal straight stow. Covers must be convexly
    # clipped/joined inside the sphere, not all corners of one enclosing box.
    stocks={
        'head and tail disk R10.75, y up to 3.5':cylinder(-3.,3.5,15,0,10.75),
        'stationary cheek blank, radius10.80 in xz':cylinder(-6.5,-1.70,15,0,10.80),
        'ball cassette closed':cylinder(3.5,10.5,15,0,4.),
        'nut-and-thrust roof incl housing':cylinder(16.70,23.55,13.5,0,4.75),
        'y-guide frame outer stanchion (mirrored z)':box((11.8,15.2),(-6.5,19.7),(13.45,15.0)),
        'axial clamp motor guarded':cylinder(-19.,7.1,18.05,5.60,3.2),
        'clamp worm and outboard bearing block':box((10.1,19.0),(15.95,20.15),(3.5,7.7)),
        'bottom cell':box((-14.,6.70),(-15.325,15.325),(-20.40,-15.0)),
        'controller (QT Py actual box)':box((-18.,4.),(-8.90,8.90),(14.4,20.1)),
        'joint bridge driver':box((-11.8,6.0),(-20.6,-10.4),(12.6,14.4)),
        'two actuator channels driver':box((-11.,6.8),(5.5,15.7),(-13.7,-11.9)),
        'ejector motor incl mount':cylinder(-17.9,10.8,12.6,-9.25-sqrt(81-6.6**2),3.2),
        '5:1 positive eject spur and bearing':cylinder(16.0,18.0,6.,-9.25,7.90),
        'bottom cross shaft between pinions':cylinder(-13.1,13.1,6.,-9.25,1.30),
        'side rack home incl stock':box((-17.5,8.0),(-8.05,-6.25),(11.40,12.90)),
        'side guide lands':box((-.5,10.0),(-8.70,-5.6),(11.,13.2)),
        'full solid eject plug, home':box((-4.50,4.15),(-1.50,9.25),(-4.80,4.80)),
        'front blade, home':box((3.35,4.15),(-1.50,9.25),(-10.65,10.65)),
        'independent joint gearmotor incl mount':cylinder(-9.85,8.85,-4.0,-6.-sqrt(10.5**2-4.0**2),3.3),
        'tail feet incl soles':box((-19.,-17.95),(-5.70,5.70),(-21.95,-21.2)),
        'head feet incl soles':box((15.5,16.9),(-9.0,9.0),(-21.95,-21.2)),
    }
    for name,diam in stocks.items():
        show(name+': stowed D',diam)
    show('max of THESE stock diameters only', max(stocks.values()))
    assert max(stocks.values())<60
    # Moving screw translates rather than sticking through an open platen.
    # Top protrudes during opening; cap follows on non-rotating stem.
    show('moving screw cap D stowed/open (not a stationary cap)',
         cylinder(19.4,21.2,13.5,0,1.6),cylinder(26.8,28.6,13.5,0,1.6))
    # A second real failure: the independent ejector cross-shaft passes
    # directly under the bench, not THROUGH a negative-y foot of the cheek.
    show('cheek-to-cross-shaft vertical gap; pinion ends to cheek z edge',
         -6.50-(-9.25+1.30),12.15-.70-10.8)
    show('eject motor lower z against cell but separated in x',
         12.6-3.2-6.7)
    # Slender arms at |z|6.3..8.7 do not traverse stowed centre plug z±4.8.
    # Sweep exterior for left foot/strut about pivot y=-6, +/-15 degrees.
    maxx=max(x*cos(a)-(y+6)*sin(a) for x,y,a in product(
        (-19.,-17.95),(-5.7,5.7),(-pi/12,0.,pi/12)))
    show('tail-foot x max at +/-15 vs battery rear edge x=-14',maxx,-14-maxx)
    # Ejector rails remain outside z±10.75 of paddle, yaw about z unchanged.
    show('rack to tail disk z gap; tail root fork to plug z gap',11.4-10.75,6.3-4.8)
    # For x<=0 and positive y offset from hinge, x' is convex near the
    # maximum toward the blade. Fork stock behind the pivot limited to x<=0
    # while y<=+1.20; pivot metal within R1.6 around (0,-6).
    far=max(1.6,(1.20+6)*sin(pi/12))
    show('forwardmost yawed fork x bound, to blade rear at 3.35',far,3.35-far)
    show('narrowed tail foot to cell in straight stow',-14.-(-17.95))


def torque():
    # 85N actual clamp, not 85N axial effort inferred from motor torque.
    L=6.6
    lead,pd=.35,2.273
    def screw(f,mu):
        return f*(pd/2)*tan(atan(lead/(pi*pd))+atan(mu/cos(pi/6)))+2.
    # 1-start module .40 worm on 20 teeth, q=8, 20deg normal pressure angle.
    for u in (.08,.18,.23):
        # Worst input/load offset 1.5, actual support centroid within .5;
        # .05P shear with 6.0 offset. Shaft guide plane spacing L.
        guide=2*(85*(1.5+.50)+.05*85*6.)/L+.05*85
        f=85.+u*guide+3.
        tq=screw(f,.18)
        eta=tan(atan(1/8))/tan(atan(1/8)+atan(u/cos(radians(20))))
        req=(tq+1.5)/(20*eta)+.3
        show('mu, guide N, screw thrust/torque, worm eta, GP torque Nmm, GP eta min at 57:1',
             u,guide,f,tq,eta,req,req/(.324*(19683/343)))
    show('moving clamp at 70 g alternate 250N screw torque even before guide losses',
         screw(250.,.18))
    show('full worm at 10Nmm without losses, max theoretical screw thrust',
         20*10,2*pi*(20*10)/lead)
    # Symmetric racks advance one crosshead. No equal rack traction assumed.
    for mu in (.03,.18,.23):
        fx=10.; fy=.23*fx; ey=9.25+7.15; ez=10.65
        # Includes unilateral tilted touch. If only one rack pushes, rack
        # thrust D generates ADDITIONAL yaw versus centroid at z=0.
        base=fx+2.+mu*(2*fx*(ey+ez)/10.5+fy+2*fy*1.6/10.5)
        bind=2*mu*12.15/10.5
        drive=base/(1-bind)
        balanced=2.1*base+1.5
        need=(2.1*drive+1.5)/(29/12*.85)
        out=2.1*drive+1.5
        show('mu, balanced total N, one-rack binding coeff/N, GP 2.417:1/revised 5:1 at .80, min spur eta',
             mu,base,bind,drive,need,out/(5*.80),out/(5*30.))
    show('5:1/.80 GP221 capacity N; requested crossshaft jam limit125 Nmm -> rack force',
         (30.*5*.80-1.5)/2.1,125./2.1)
    show('85N central loading 28-span steel beam b4,h2.8: sigma MPa/delta mm',
         (85*28/4)/(4*2.8**2/6),85*28**3/(48*200000*(4*2.8**3/12)))


def spur_idler(a, b, ra, rb, hand):
    dx,dy=b[0]-a[0],b[1]-a[1]
    d=hypot(dx,dy)
    k=(ra*ra-rb*rb+d*d)/(2*d)
    h=hand*sqrt(ra*ra-k*k)
    return a[0]+(k*dx-h*dy)/d,a[1]+(k*dy+h*dx)/d


def wide():
    print('\nWIDE LIFT; replaces prior roof/worm/racks, not their union')
    # Bounding pairs: disk-disk, arm-arm, arm-disk (distance to disk centre
    # plus disk radius). Y differences depend on pair.
    widths=(hypot(21.5,6.5),hypot(12-3.5,17.4,2.4),
            hypot(hypot(12,8.7)+10.75,4.7))
    show('body pair widths, gap, surplus',*widths,26.70,26.70-max(widths))
    ci=spur_idler((.55,0),(-10.,16.),15.,6.,+1)
    # At m.30: input 14T, output 28T, idler 30T.
    ei=spur_idler((-.70,-11.50),(12.60,-15.37),8.7,6.6,+1)
    show('clamp idler x,z; eject idler x,y',*ci,*ei)
    stocks={
        'cheek cylinder':cylinder(-6.5,-1.70,15,0,10.75),
        'own passive disk':cylinder(-3.,3.5,-15,0,10.75),
        'twin upper rails and shell':box((-2.10,2.90),(-3.5,29.0),(-7.05,7.05)),
        'upper tongue closed incl cassette allowance':box((-2.10,19.),(3.50,10.50),(-7.05,7.05)),
        'clamp gearmotor':cylinder(-9.75,18.95,-10,16,3.20),
        'clamp screw thrust housing':cylinder(-16.80,-6.10,.55,0,4.75),
        'clamp 57T wheel teeth':cylinder(-11.95,-10.75,.55,0,11.80),
        'clamp idler teeth':cylinder(-11.95,-10.75,*ci,4.00),
        'eject gearmotor':cylinder(-17.9,10.8,12.6,-15.37,3.20),
        'eject independent 14T, idler and 28T output max D':max(
            cylinder(12.05,13.30,x,y,r) for x,y,r in
            [(12.6,-15.37,2.4),(*ei,4.8),(-.7,-11.5,4.5)]),
        'eject thrust housing':cylinder(-6.5,.05,-11.5,16.9,3.35),
        'eject screw nose':cylinder(19.95,20.45,-11.5,16.9,1.35),
        'eject rail outer boxes':box((-8.,19.5),(-8.05,-5.65),(-12.9,12.9)),
        'eject rod quill rear bearing':cylinder(18.90,19.55,-.7,-11.50,2.20),
        'pusher with side return ears HOME':box((3.35,4.15),(-1.50,9.25),(-12.9,12.9)),
        'bottom cell shifted':box((-12.35,8.35),(-14.30,16.35),(-20.4,-15.0)),
        'QT Py top box':box((-11.,11.),(-8.9,8.9),(19.85,25.55)),
        'parent joint-motor housing':cylinder(-11.70,7.00,-7.9613,-18.1978,3.2)
    }
    for name,d in stocks.items(): show(name+': D',d)
    # Exact interaction rather than clipping a complete cylindrical bearing
    # at z=19.6 regardless of y. QTPy begins at y=-8.9.
    show('bearing highest z within controller y-window; gap to board',
         16.90+sqrt(3.35**2-2.60**2),19.85-(16.90+sqrt(3.35**2-2.60**2)))
    show('gear plane gaps to clamp wheel and eject thrust barrel',
         12.05-11.80,(16.90-3.35)-13.30)
    show('eject thrust barrel aft x gap to primary motor end in x',
         -6.50-(-10.+3.20))
    show('adjacent blocked rack at full travel: interference length',
         min(8+15,30+8)-max(-17.5+15,30-17.5))
    # Adjacent eject screw's nose cannot enter the aft race just from x
    # translation; yaw, side arms and unmodelled tips are separate.
    show('straight, identical fixed screw axial separation',
         30.-6.50-20.45)
    show('largest modelled present stock D (not complete install)',max(stocks.values()))
    # Collisions in an explicitly BAD design are not margins to zero away.
    # Supplemental two-driver reservations from discarded short package.
    # Box for tail/foot, driver mounts, flex harness etc. is NOT frozen.
    show('AABB widest guide corners vs D60 (clip cap if negative)',
         60.-stocks['twin upper rails and shell'])
    show('MCU box stow margin',60.-stocks['QT Py top box'])

    P=85.
    M=P*(15.-.55)+.05*P*5.
    guide=2*M/5.60+.05*P
    axial=P+3+.23*guide
    def thread(f,l,d):
        return f*d/2*tan(atan(l/(pi*d))+atan(.18/cos(pi/6)))
    tq=thread(axial,.35,2.273)+2
    gp=(tq+1.)/(4.75*.85)
    show('wide clamp moment /sum guide reactions/axial/screw torque/GP/min gearbox eff',
         M,guide,axial,tq,gp,gp/(.324*531441/2401))
    # Gauged force must stop independently of jam hardware and screw torque.
    for lead,limit in [(.35,67.),(.40,43.)]:
        show('lead, trial shaft torque limiter, zero-loss upper thrust',lead,limit,2*pi*limit/lead)
    # Single positive-z screw; no second rack assumed to help; measure µ.
    # z moment from screw traction; conservatively separate x/y-plane racking.
    for mu in (.12,.18,.23):
        for f in (10.,15.):
            fy=.23*f
            L=10.5
            ey=9.25+11.5
            # Includes full screw-to-rail y offset as self-excitation.
            guide_y=-6.85
            rho=2*mu*(16.90+abs(-11.50-guide_y))/L
            base=f+2+mu*(2*f*((9.25-guide_y)+10.65)/L+fy+2*fy*1.6/L)
            drive=base/(1-rho) if rho<1 else float('inf')
            ts=thread(drive,.4,1.74)+1.5
            gp=(ts/.82+1.)/(2*.85)
            show('mu, blade force, single-drive feedback, required thrust, screw torque, GP',
                 mu,f,rho,drive,ts,gp)
    # Unilateral moving 10.5-spaced journals can instead be centred in the
    # screw's own y-plane, only if a supported negative-z rail misses cell.
    for L,yg in [(10.5,-11.5),(14.,-11.5),(14.,-6.85)]:
        mu=.23; f=15.; fy=.23*f
        rho=2*mu*(16.90+abs(-11.50-yg))/L
        base=f+2+mu*(2*f*((9.25-yg)+10.65)/L+fy+2*fy*1.6/L)
        d=base/(1-rho)
        ts=thread(d,.4,1.74)+1.5
        show('comparison guide L/y, feedback, thrust, GP torque',L,yg,rho,d,(ts/.82+1)/(2*.85))
    I=pi*1.51**4/64
    show('Euler K2, root 1.51, unsupported 21mm N',pi*pi*200000*I/(2*21)**2)
    show('screw turns clamp/eject, minutes at RE6 nominal rpm GP221 spur',
         21.5/.35,15/.4,21.5/.35*4.75*(531441/2401)/5670,15/.4*2*(531441/2401)/5670)
    R=4.; dth=pi/(2*7.5)
    show('90deg fold pivot y, largest positive x of tongue, ymax bound',
         26.10,.55+1.1,26.10+hypot(19.-.55,7.-1.1))
    show('follower minimum normal moment arm; track D bound; force if carrying lock moment',
         R/sqrt(2)/(1+R*dth),box((-4.,4.60),(14.,25.0),(7.1,9.3)),
         M/(R/sqrt(2)/(1+R*dth)))
    assert 26.70>max(widths) and max(stocks.values())<60.


if __name__=='__main__':
    print('HISTORICAL compact branch (not high-lift stocks or current force targets)')
    section()
    torque()
    wide()
