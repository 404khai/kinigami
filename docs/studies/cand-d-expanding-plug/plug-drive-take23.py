"""Exploratory section, not a candidate or gate. mm, N, N mm, MPa, degrees."""
from itertools import product
from math import asin, atan, cos, degrees, dist, hypot, pi, radians, sin, sqrt, tan


def show(label, *values):
    print(label, *(round(v, 4) for v in values))


phi, beta = map(radians, (29, 21))
theta = phi + beta
mu, B, p, h, a = .23, 1.25, 5., 1.125, 1.29
n, u, t = (sin(phi), cos(phi)), (-sin(beta), cos(beta)), (cos(beta), sin(beta))
P = (32.5, 7.)


def plus(v, s, w):
    return tuple(q+s*r for q, r in zip(v, w))


C = plus(P, h, n)
K = plus(C, B+p, u)
xf = 25.806
xs = xf+p*cos(radians(57.5))
st = 2.85
tip = 37.45


def hertz(force, radius):
    e = 213000/(2*(1-.29**2))
    w = (3*force*radius/(4*e))**(1/3)
    return w, 3*force/(2*pi*w*w)/1000


def front():
    show('button centre, tail core centre (x,r)', *C, *K)
    show('nominal V centre x, halfwidth t, apex x', xs, p*sin(radians(57.5)), xs-p/cos(radians(57.5)))
    show('nominal park, maximum tail sag, dimensional residual', st-h-B,
         p-sqrt(p*p-1.30**2), (st-.03)-(h+.025)-(B+.005)-(p-sqrt(p*p-1.30**2))-.10)
    show('park lip angle, friction angle, axial normal margin', degrees(asin(1.30/p)), degrees(atan(mu)),
         sin(phi-asin(1.30/p))-mu*cos(phi-asin(1.30/p)))
    # Full contact with inner ring versus a finite width surrounding facet.
    v = mu/hypot(1,mu)
    show('unbounded plane inferred cosine; finite outer collar at positive-slide boundary',
         (sqrt(p*p-a*a)-h)/(p+B), (p+B)*sqrt(1-v*v)-sqrt(p*p-(h+(p+B)*v)**2))
    show('true planar outer-collar radii (aft break, adjacent relief plane)',
         (32.5-30.60)/cos(phi),
         (5.60-.5*7)/hypot(sin(pi/3),.36*cos(phi)-.5*sin(phi)))
    b, W, f, delta = B, 8., .22, .18
    D = W-b+delta
    z = ((W-f)**2-(b-f)**2-D*D)/(2*D)
    seam = sqrt((b-f)**2-z*z)
    show('crown usable cap radius, tilt allowance to seam (deg)', seam*W/(W-f), degrees(asin(seam/(W-f))))
    for m in (.38,.27):
        q = plus(plus(K,-delta,u),-.90,t)
        rb = 7+(32.5-30.60)*tan(phi)
        d = (q[1]-rb+m*(q[0]-30.6))/hypot(1,m)
        x = q[0]-d*m/hypot(1,m)
        show('rear facet slope, nominal separation, nearest x, axial advance .45 + radial .40',
             m,d-p,x,d-p-(.45*m+.40)/hypot(1,m))
        assert d<p and x<30.60
    show('original lock-lobe complete sphere simple 29deg plane clearance',h+(p+B)*cos(theta)-p)
    show('round original nose continuation at V sphere: signed clearance (no V-sector relief)',
         (13.5-(7+(32.5-30.60)*tan(phi))+.38*(xs-30.60))/hypot(1,.38)-p)
    show('relieved V sector plane at seat sphere', (13.50-5.60+.36*(xs-32.5))/hypot(1,.36)-p)
    j = 55/(sin(beta)-mu*cos(beta))
    for N in (j/3,150,j):
        s, f_in = sin(theta)+mu*cos(theta), cos(theta)-mu*sin(theta)
        M = N*(2.475*s+mu*B)
        L = 1.65
        guide = mu*(s+2*(2.475*s+mu*B)/L)
        show('N, sphere/p5 equal-curvature surrogate GPa, crown/flat GPa, patch, crown rim reserve at 2deg/.08',
             N,hertz(N,1/(1/B+1/p))[1],hertz(N,W)[1],hertz(N,W)[0],
             seam*W/(W-f)-W*sin(radians(2))-.08-hertz(N,W)[0])
        show('N, transverse force, stem nominal bend MPa, inward force - two-edge drag, needed return pin N',
             N,N*s,M/(pi*1.8**3/32),N*(f_in-guide),max(0.,N*(guide-f_in)))
    show('sumN 55 axial, opposed friction, no equal split upper; frictionless', j,55/sin(beta))
    show('upstream crown N, width and GPa',55.48,*hertz(55.48,8))
    slope=.48
    show('nose mandrel rearward ramp travel, locked & open heel radial coord, open 120deg pitch',
         st*(cos(phi)/slope+sin(phi)), 7-3.40*cos(phi),7-(3.40+st)*cos(phi),
         sqrt(3)*(7-(3.4+st)*cos(phi)))


def drive():
    r=2.675/2
    def factor(f):
        m=f/cos(pi/6)
        k=.5/(2*pi*r)
        return r*(k+m)/(1-m*k)
    G=79000; d=.8; D=4.; na=5.4
    kc=G*d**4/(8*D**3*na)
    show('spring pair nominal N/mm / compression at 50,55 N / single spring Wahl MPa',
         2*kc,50/(2*kc),55/(2*kc),8*27.5*D/(pi*d**3)*((4*(D/d)-1)/(4*(D/d)-4)+.615/(D/d)))
    # Kinematically paired moving transverse plates; max slope for a trapezoidal
    # derivative with 10% linear ramps at each end. Finite guide friction.
    stages=(('take-up',3.15,3.8,55.),('cone example',7.45,6.8,20.),('one-pad eject example',17.3,10.3,8.))
    for label,dx,dq,F in stages:
        k=dx/(.9*dq)
        for fc,fg in ((.05,.10),(.23,.23)):
            H=(k+fc)/(1-fc*k)
            y=H*F/(1-H*fg)
            show(label+' k, cam mu, guide mu, thrust, motor torque',k,fc,fg,y,(factor(.23)*y+3)/(2*.80))
    show('clutch example low/high motor torque, max screw thrust frictionless @ high incl ideal gear',
         34,45,2*45/factor(0))
    show('screw minimum input guide/plate cycles (turns), ideal self lock thread mu minimum',
         21.4/.5*2,.5/(2*pi*r)*cos(pi/6))
    show('17.3 eject plane margin after whole plate tilt 6deg / 9deg, .40 axial + .45 cage advance',
         *(xs-p+17.3-tip-.40-.45-2*19.8*sin(radians(v)/2) for v in (6,9)))
    # Relative to the head frame of the docked neighbour. Nominal distance
    # from V sphere centres to the most remote point is <= this triangle bound.
    show('70g weight / 4W; arms relative x28.492 to nose, aftmost stowed tail',
         .070*9.80665,4*.070*9.80665,tip-xs,xs-(xs-p-40))


def package():
    # Local z=0 is the coupler axis throughout. Outermost torus major + p.
    c=(10.,0.,-.5); pitch=40.
    def box(lo,hi):
        return 2*max(dist(c,v) for v in product(*zip(lo,hi)))
    def cyl(x,r):
        return 2*hypot(x-c[0],abs(c[2])+r)
    def yshaft(x,y,z,r):
        return 2*hypot(y-c[1],hypot(x-c[0],z-c[2])+r)
    for name,lo,hi in (
        ('transverse servo gripped case',(-1.2,-2.98,-.8),(8.2,17.90,20.4)),
        ('draw plate full sweep',(11.70,-23.,-14.05),(18.75,23.,-12.45)),
        ('jaw plate full sweep',(6.15,-23.,-7.95),(18.10,23.,-6.35)),
        ('eject plate full sweep',(4.0,-23.,-11.0),(25.50,23.,-9.4))):
        show(name+' common sphere D',box(lo,hi))
    show('guarded screw gear sphere D',yshaft(3.50,20.40,-10.,10.50))
    show('tail lock sphere, tail V sphere, tail solid floor exterior shell; common sphere D',
         2*(hypot(K[0]-pitch-c[0],K[1]+.5)+p+.18+.90),
         2*(hypot(xs-pitch-c[0],13.5+.5)+p),
         2*(hypot(44.5-pitch-c[0],13.82+.5)+p))
    show('head plate R19.80, nose end R5.00 D',cyl(25.4,19.80),cyl(tip,5.0))
    show('unsplit eject hole inradius at x25.03 / max allowed', min(5.60+.36*(32.5-25.03),7+(32.5-30.60)*tan(phi)+.38*(30.60-25.03)),p)
    show('whole unit planar clearance at 6deg, direct measured 17.3 advance / if .50 lost travel',
         *(xs-p+17.3-lost-tip-.40-.45-31*sin(radians(6)) for lost in (0.,.50)))
    W=.070*9.80665
    show('arms axial to mating pair end/own far tail; transverse component box; one W moments',
         tip+pitch-xs, xs-(xs-p-pitch), 23, 23*W, (tip+pitch-xs)*W)
    # Reverse at q=0. Eject plate covers y=0; stock between end and the
    # empty slot, excludes intentional pin hole and any undercut bridge.
    # Explicit incompatibility of passive end and actuator in this pitch.
    floor=(44.5-pitch,0.,2.)   # inside fixed p-offset floor AND the servo case
    show('positive overlap, own passive floor/servo xyz',*floor)
    # These two stock subsets do not overlap in x for the nominated backing.
    show('six full solid p5 balls + central Ø27 x10 rear disk (steel g), no joins',
         (6*4*pi*p**3/3+pi*13.5**2*10)*.0078)
    show('required positive pitch for full floor to finish ahead of x=-1.2 servo boundary',
         44.5+5+1.2)
    show('axis independent 2-end witness at that pitch, aft V sphere vs positive-x tip centre',
         hypot(tip-(xs-50.7),13.5)+p)


def terminal():
    # Exact bisectors in one 60-degree sector. Outside hoop not covered.
    mid, hoop, b = 11., 19., 3.
    between = (hoop*hoop-mid*mid)/(2*(hoop-mid*cos(pi/6)))
    D = max(mid/(2*cos(pi/6)),hoop-between)+.10
    nx = sqrt(1-(D/(p+b))**2)
    show('rounded grid D incl .10, nx, axial friction margin',D,nx,nx-mu*sqrt(1-nx*nx))
    plane = 5.6+.36*(32.5-25.03)
    overlap = b-(11*cos(pi/6)-plane)
    show('mid rod crossing into nose, x25.03',overlap)
    # Three pusher arcs at radius 16..18 +/-6deg and azimuths 30+120i.
    rho = sqrt(16**2+K[1]**2-2*16*K[1]*cos(radians(24)))
    alpha = radians(6)
    x_end = tip+.45+.20+(39.50-(xs-p))/cos(alpha)+(19.80-8.5)*tan(alpha)
    pair = hypot(39.25-(xs-40),sqrt(18**2+13.5**2-2*18*13.5*cos(radians(150))))+p
    show('split arc static flank gap / projected disk inradius after offset',
         rho-(5+.18+.90),19.5*cos(alpha)-.60)
    show('split arc terminal plane, stroke at short/long park, D witness long park',
         x_end,x_end-25.03,x_end-39.25,pair)
    assert 6.44<D<6.46 and overlap>1.7 and pair>64 and x_end-25.03>30


if __name__=='__main__':
    print('RESULT exploratory; dimensions are design trials, not source ratings.')
    front()
    drive()
    package()
    terminal()
