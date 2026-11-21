"""Exploratory sections, not candidate geometry. mm, N, N mm. Python 3."""
from itertools import product
from math import asin, cos, degrees, dist, hypot, pi, radians, sin, sqrt, tan

def crossed_crown():
    b,H=1.045,20.
    def B(u): return b-u*u/(H+sqrt(H*H-u*u))
    a=radians(12)
    def h(x,y): return hypot(x,y) if x>=-sin(a)*hypot(x,y) else -sin(a)*x+cos(a)*abs(y)
    def residual(x,r,t): return max(h(x,r)-B(t),h(-x,t)-B(r))
    # Symmetric midplane corner, not a sphere. Exact fixed point r=B(r).
    lo,hi=0.,b
    for _ in range(60):
        m=(lo+hi)/2
        if residual(0,m,m)>0: hi=m
        else: lo=m
    # A witness in the whole rectangular neck-overlap block. By convexity in
    # x,r,t the worst residual is attained at a corner of the block.
    neck=max(residual(x,r,t) for x,r,t in product((-.40,.40),(-.93,-.82),(-.48,.48)))
    # Upper bound support of the rotated bounding cube; rotation angle includes
    # all roll/pitch/yaw, not independent per-axis .5 degree angles.
    def extent(phi): return b*(cos(phi)+sqrt(2)*sin(phi))
    print("12deg crossed crown x=0 corner, local hypot, neck overlap max residual",lo,lo*sqrt(2),neck)
    for angle in (.50,1.10,1.50):
        v=extent(radians(angle))+.015  # proposed global profile oversize
        # Support of the shear meridian for a normal tilted <=phi<12 degrees:
        # sup_u B(u)*cos(tilt)+u*sin(tilt). Actual intersected part only smaller.
        w=b+(H-b)*(1-cos(radians(angle)))+.015
        print("angle / cube half-width / open lip / fork / shear extent / unilateral cheek clearance",
              angle,v,5.96-.05-(4.65+.035+.06+v),1.60-.08-v,w,1.12-.02-.035-w)
    # Sample central meridians, debit angular/sample errors (h is 1-Lipschitz,
    # B' <= b/sqrt(H^2-b^2)); r and x vary <= b dtheta + max|B'| du.
    du=.002; da=radians(.2)
    margin=min(B(B(u)*sin(p))-h(-B(u)*cos(p),u)
               for j in range(351) for i in range(511)
               for u,p in [(j*du,i*da)])
    mB=b/sqrt(H*H-b*b)
    debit=(1+mB)*b*da/2+(1+mB+mB*mB)*du/2
    print("strip min margin (sample / debited)",margin,margin-debit)
    lim=degrees(asin((.70-.275-.04)/H))
    phi=radians(1.5); weak=sin(phi)*sqrt(3)/2
    print("patch tilt limit / chord tilt / excursion / weak-axis / patch plus guard",
          lim,degrees(phi),1.5*4.65*sin(phi),degrees(asin(weak)),H*weak+.275+.04)
    assert neck<0 and margin>debit and 1.5*4.65*sin(phi)+2*H*(1-cos(phi))<.21

def axial_breaker():
    s,dead=7.64,.12
    sn=s+2*dead; half=sn+.60+.20; x=18.25
    print("nut stroke / rail / swept rail / rear/front worst / no-window gap",
          sn,2*half,2*half+s,x-half,x+half+s,(34.4-.20)-(x+half+s))
    def factor(a,m):
        k=tan(radians(a)); return (k+m)/(1-m*k)
    print("conditional notch trips normal-low/normal-high/seized-upper",
          46.4*factor(44.5,0),56*factor(45.5,.10),56*factor(45.5,.23))
    for lead,pitch in ((.70,.35),(1.00,.50),(2.00,.50)):
        hi,lo=screw(2.5,pitch,lead,.23)
        f=55*2*pi/lead
        print("lead / dry T90 incl 5 / frictionless F55 / dry thread-only backoff",
              lead,90*hi+5,f,lo*f)

def big_sphere():
    # Sphere/convex cylinder Hertz patch, half-space normal-load comparison only.
    # Integrate with t=a*tan(theta) removing the infinite upper endpoint.
    def j(a,b):
        n=400
        return sum(2*cos((i+.5)*pi/(2*n))**2/(a*a*sqrt(
            a*a*sin((i+.5)*pi/(2*n))**2 + b*b*cos((i+.5)*pi/(2*n))**2))
                   for i in range(n))*pi/(2*n)
    for B,Rc in ((1.75,1.50),(2.,2.)):
        rx=B*Rc/(B+Rc); ry=B; lo,hi=1.,4.
        for _ in range(45):
            u=(lo+hi)/2
            if rx*j(1,u)<ry*j(u,1): lo=u
            else: hi=u
        a=(rx*3*43.1*j(1,u)/(2*pi*115000))**(1/3);b=u*a
        print("sphere/cylinder Hertz b,Rc / semiaxes / p0 GPa",B,Rc,a,b,3*43.1/(2*pi*a*b*1000))
    c=(11.841,.60,-2.019); pts=[]
    def box(x0,x1,y,z):
        pts.extend((dist(c,p),p) for p in product((x0,x1),(-y,y),(-z,z)))
    box(1.8,34.4,12.7,12);box(34.4,35.6,11.9,11.2)
    box(-9.4,-1.8,12.7,12);box(-10.6,-9.4,11.9,11.2)
    cells=[]
    for az in (90,210,330):
        a=radians(az)
        def point(x,n,t):return x,.60+n*cos(a)-t*sin(a),-3.8+n*sin(a)+t*cos(a)
        ball=point(-15.50,5.65,0)
        pts.append((dist(c,ball)+1.77,ball))
        for x0,x1,n0,n1,t0,t1 in (
            (37.1,39.46,3.9,6.80,-2.1,2.1),         # transverse keeper at home
            (37.17,39.17,1.35,10.55,-2.67,2.67),     # fixed roller-guide pack
            (35.03,37.37,4.,7.30,-3.88,3.88),        # cheek mount/end incl backing
            (-15.97,-11.60,2.25,4.12,-.65,.65)):    # radial neck + inboard stem
            for x,n,t in product((x0,x1),(n0,n1),(t0,t1)):
                p=point(x,n,t);pts.append((dist(c,p),p));cells.append(p)
    for x,axis,rad in ((-11.60,(.6,-3.8),6.30),(36.40,(.6,-4.6),6.30)):
        pts.append((hypot(x-c[0],hypot(axis[0]-c[1],axis[1]-c[2])+rad),(x,*axis)))
    for s in (-1,1):
        pts.extend((dist(c,p),p) for p in product((35.60,36.40),
            (.60+s*7.1-2.6,.60+s*7.1+2.6),(-4.60+s*4.2-1.9,-4.60+s*4.2+1.9)))
    print("large stowed D, limiting point; lowest new holder/stem z",2*max(pts)[0],max(pts)[1],min(p[2] for p in cells))
    for stroke in (4.,.2+3.60/(1.65/3.8)):
        k=3.60/(stroke-.20);G=(k+.10)/(1-.10*k);g=.10*(G+2*6.25/4.4)
        r=17/(1-g); C=screw(2.5,.50,2.,.23)[0]
        f=(G*r*(1+2*.23*8.6/5.2)+.23*r*(1+2*2.8/5.2+2*2.4/8))/(1-.23*C/4)
        S=.55+stroke+.25+4.
        print("large radial cam stroke / total S / full thread end / 2lead F,T",stroke,S,
              28.69+.02+S+.04+1.56+.02,f,5+f*C)

def track_plates():
    k=3.60/radians(65-6)
    G=max((k+.10*r)/(1-.10*k/r) for r in (2.05,5.65))
    g=.10*(G/2.05+2*6.20/4.40+2*.80/3.90)
    T=17*G/(1-g)+5
    K=4/radians(33-5); E=(K+.10*5.98)/(1-.10*K/5.98)
    print("track plates radial lead,G,guide feedback,T,min efficiency",k,G,g,T,T/(4*49.03))
    print("eject lead,G,T (8N one rod, no other breakaway)",K,E,E*8*(1+.23*2*1.3/2.8)+5)
    for ti in (49.03,200):
        ft=ti/1.62; fn=ft/cos(radians(20)); b=3.50; m=.18
        print("input T/one planet pin N/Lewis MPa/pitch pressure GPa/pin bend MPa",
              ti,2*fn,ft/(b*m*.30),sqrt(115400*fn/(pi*b*1.62*sin(radians(20))/2))/1000,
              32*(2*fn)*4.5/(4*pi*1.8**3))

def swing():
    # Sectors of the working shoe, swept before allowing any tail ejection.
    xp,rp=35.375,8.45; rc=1.50; worst=(-100.,)
    def xnr(theta,v,w):
        return xp+v*cos(theta)-w*sin(theta),rp+v*sin(theta)+w*cos(theta)
    for i in range(601):
        q=radians(i/10); x,r=xnr(q,3.60,-2.80)
        for deg,rho in product(range(-12,53),(1.15,rc)):
            a=q+radians(deg); xx=x-rho*cos(a); rr=r-rho*sin(a)
            if rr<=6.3: worst=max(worst,(xx,rr,i/10,deg,rho))
    q=radians(60);x,r=xnr(q,3.6,-2.8)
    print("swing centre 60deg dx/dr; max forward centre; sampled rim penetration",
          x-38.975,r-5.65,hypot(3.60,2.80)-3.6,worst,worst[0]-39.55)
    q=radians(27);x,r=xnr(q,3.6,-2.8);a=q+radians(52)
    print("exact 27deg shoe witness x,n,t",x-rc*cos(a),r-rc*sin(a),0)
    # Dogleg strut P->B->K; cylindrical x/n section half-thickness .32,
    # transverse ears |t| 2.00..2.35. Cheek envelopes used, not just centres.
    closest=(1e9,);mx=(-1e9,)
    for i in range(601):
        q=radians(i/10)
        for v0,w0,v1,w1 in ((0,0,1.98,-.10),(1.98,-.10,3.6,-2.8)):
            for j in range(101):
                u=j/100;x,n=xnr(q,v0+(v1-v0)*u,w0+(w1-w0)*u)
                # Cheek inner working meridian on |t|=2.35 at x35.65±sqrt(...);
                # at still larger x keep the backing outside |t|=3.0.
                d=hypot(max(0,x-(35.65+sqrt(1.5**2-(3.325-2.35)**2))),
                        max(0,n-7.30))-.32
                closest=min(closest,(d,i/10,j))
                if hypot(max(0,n-.32),2.0)<=6.30:mx=max(mx,(x+.32,i/10,j))
    print("dogleg cheek gap (sample less .026); conservative rim-region arm xmax",
          closest[0]-.026,mx)

def screw(d,p,h,mu):
    dm=d-.649519*p
    l=h/(pi*dm); f=mu/cos(pi/6)
    return dm*(l+f)/(2*(1-l*f)),dm*(f-l)/(2*(1+l*f))

def section(x,n0,n1,t0,t1,c):
    return max(dist((c,0,0),(x,.60+n*cos(a)-t*sin(a),-4.60+n*sin(a)+t*cos(a)))
               for a in map(radians,(90,210,330)) for n,t in product((n0,n1),(t0,t1)))

def run():
    print("Mating M3x.5: locked/full thread, min over independently bounded ends")
    # relative to the seating plane: screw shifts forward with draw delta.
    L=min(min(2.35+ds-.03,2.95-.03)-max(-.60+ds+.03,.55+.03) for ds in (.64,.72))
    print("engagement mm, pitches",L,L/.5,"exit gap mm",(2.72+.03)-(.18-.03))
    print("max lock tip / blind floor min / clearance",2.72+.72+.03,3.75-.03,3.75-.03-(2.72+.72+.03))
    for f in (.05,.23):
        print("M3 thread T/F raise,lower",f,screw(3,.5,.5,f))
    W=.050*9.80665; Rp=4.8; pitch=36.40+15.90
    for yaw in (14.5,52.2):
        M=hypot(pitch*W,yaw)
        print("Centered draw for all three pads compressed before pusher, service/fault",
              4*W+2*M/Rp)
    for H in (4.75,7.85):
        print("Lesjofors #1163, proposed length and 3-spring reference force",H,3*.57*(10-H))
    # Fine four-start alternative uses same permanent nut envelope, NOT an ISO screw.
    print("INTERNAL: 7.60 stroke; 0.55 bias, 4.00 jaw, .25 dwell, 2.80 eject")
    S=.55+4.00+.25+2.80; nut0=28.69; LN=1.56
    print("full screw end required with gauge debits",nut0+.02+S+.04+LN+.02)
    print("front tube/spoke x33.35 at full open; tail plate x38.45+2.80; gap",
          38.45+2.80-.04-(33.35+.03+S+.04))
    print("long cheek end / min ejected rear pole / end margin",
          35.85+1.48+.025,34.80-.02+2.80-.035-.14,
          34.80-.02+2.80-.035-.14-(35.85+1.48+.025))
    for q,p in ((.35,.35),(2,.5)):
        raise_,lower=screw(2.5,p,q,.23)
        print("lead / turns / raise / lower T per F / frictionless 34 Nmm jam / dry lower T",
              q,S/q,raise_,lower,34*2*pi/q,34*2*pi/q*lower)
    # One active base resistance at a time OR sum of nonnegative loads bounded by F0;
    # no third-of-load credit. Dry sliding cam, rolling variants or a seized journal.
    k=1.65/(4.-.20); e=37.05-32.75; L=4.4; eps=5.6; b=5.2
    for mc,mg,ms in ((.23,.23,.23),(.10,.10,.23),(.12,.12,.23),(.10,.10,.10),(.23,.10,.23)):
        G=(k+mc)/(1-mc*k); g=mg*(G+2*e/L)
        R=17/(1-g); Fx=G*R
        # Housing rails straddle axis. Added norm from an overhung side force
        # and its rolling moment; target true lever separations, not equal forces.
        for lead,p in ((.35,.35),(2,.5)):
            C=screw(2.5,p,lead,.23)[0]
            F=(Fx*(1+2*ms*eps/b)+ms*R*(1+2*2.80/b+2*2.40/8))/(1-ms*C/4.)
            print("cam,keeper,shuttle / lead / gamma / F / T(+5)",mc,mg,ms,lead,
                  round(g,3),round(F,2),round(C*F+5,2))
    # End features with low-radius leading tongue; do not extrude max radius to same xmax.
    # Remaining closed shell bounds with this centre, not an official evaluator.
    c=12.60
    body=max(hypot(x-c,hypot(y,z)) for x,y,z in (
        (34.4,12.7,12.),(35.60,11.90,11.20),(-9.40,12.70,12.),(-10.60,11.90,11.20)))
    tail=hypot(-15.30-c,6.30+hypot(.60,4.60))
    nose=section(38.1,1.35,7.90,-2.18,2.18,c)
    # Correct azimuth range on leading tongue; tip low r, plateau follows it.
    camtip=section(32.75+.40+S,1.15,3.25,1.85,2.45,c)
    high=section(32.75-.55-4+.40+S,1.15,5.00,1.85,2.45,c)
    spoke=section(33.35+S,1.2,5.0,-2.1,2.1,c)
    print("D under individual bounds, mm, body/tail/nose/cam tip/high/spokes",
          *(round(2*r,3) for r in (body,tail,nose,camtip,high,spoke)))
    print("Stowed listed shell/tail/fixed nose/retracted moving pieces D",2*max(
        body,tail,nose,section(33.35,1.2,5.,-2.1,2.1,c),
        section(33.15,1.15,5.,1.85,2.45,c)))
    print("Open sweep, not G1: xmax spoke/tongue/pad/departing face",
          33.35+S,33.15+S,34.80+2.80,38.45+2.80)
    # At an intermediate x through the radial ramp debit its entire width,
    # max first derivative; the squared generator distance is convex on the
    # linear conservative roof, hence sufficient to inspect its endpoints.
    print("Max cam mid-ramp travel bound D",max(
        2*section(32.75-.55-u+S+.40,1.15,min(5.00,3.25+1.65*u/3.80),
                  1.85,2.45,c) for u in (0,3.80,4.00)))
    # Two distinct functions at 60-deg intervals, separate from sphere case.
    jaw=5.96-3.84; kr=jaw/3.80; G=(kr+.10)/(1-.10*kr)
    F=17/(1-.10*(G+2*4.30/4.40))
    H=(G*F*(1+2*.23*5.6/5.2)+.23*F*(1+2*2.8/5.2+2*2.4/8))/(1-.23*.65834/4)
    print("Crossbar throw / F / extra stroke to preserve lead",jaw,H,(jaw-1.65)/(1.65/3.8))
    for name,n,t in (("upper edge of short shear cheek",3.65,1.52),
                     ("radial shear crown inner end",3.20,1.05)):
        print(name,"clearance to neighbour rail at |t|=2.12",n*sin(pi/3)-t*cos(pi/3)-2.12)
    crossed_crown()
    axial_breaker()
    big_sphere()
    track_plates()
    swing()
    for length in (1.40,2.80):
        # Per-pad rocker, both directions against opposing load. Series yoke
        # uses a roll-guided input at -x; pin never reaches a toggle.
        worst=(0.,)
        for i in range(10001):
            q=length*i/10000; edge=.10; v=1/(length-edge)
            if q<edge:u=.5*v*q*q/edge;s=v*q/edge
            elif q>length-edge:u=1-.5*v*(length-q)**2/edge;s=v*(length-q)/edge
            else:u=v*(q-edge/2);s=v
            y=u-.5;c0=sqrt(1-y*y);k0=.85*s/(1-.85*y*s/c0);m=.10;ms=.23
            G=(k0+m)/(1-m*k0)
            ft=2.80*(c0+m*abs(y))/(.85*(c0+G*y));fx=G*ft
            H=(fx*(1+2*ms*5.6/5.2)+ms*ft*(1+2*1.2/5.2+2*2.4/8))/(1-ms*.7/4)
            worst=max(worst,(H,q))
        print("rocker input stroke / resisting 8 N one-pad shuttle demand before pivot drag",length,8*worst[0])

if __name__=="__main__": run()
