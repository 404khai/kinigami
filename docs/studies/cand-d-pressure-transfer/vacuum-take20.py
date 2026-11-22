"""Exploratory only. Python 3 standard library, mm, N, N mm, kPa abs or difference."""
from math import cos, dist, hypot, pi, radians, sin, sqrt
from itertools import product

R, RO, RI, E = 9.50, 13.30, 5.80, .10
B, HIDE, FLAT, LIP, L = 2.50, 1.00, 2.14, .80, 2.78
H=FLAT+LIP*(1-cos(pi/4))
WIDTH=FLAT+LIP*sin(pi/4)
P, STROKE=101.325,10.50
AMIN=pi*((RO-E)**2-(RI+E)**2)-.50
AMAX=pi*((RO+E)**2-(RI-E)**2)
APMIN=pi*(9.85**2-4.60**2)
APMAX=pi*(9.95**2-4.50**2)
VOL=APMIN*(STROKE-.05)

def norm(v):return sqrt(sum(x*x for x in v))
def inv(a):
    a=[row[:]+[float(i==j) for j in range(6)] for i,row in enumerate(a)]
    for k in range(6):
        p=max(range(k,6),key=lambda i:abs(a[i][k]));a[k],a[p]=a[p],a[k]
        t=a[k][k];assert abs(t)>.1
        a[k]=[v/t for v in a[k]]
        for i in range(6):
            if i!=k:
                t=a[i][k];a[i]=[v-t*w for v,w in zip(a[i],a[k])]
    return [r[6:] for r in a]

def seats():
    # Take 18 seats.py frictionless positive-normal test, same loads at 60g;
    # wrench origin nominal triangle centre. New R; not new requirements.
    W=.060*9.80665; c=cos(pi/4); j=[]
    for deg in (90,210,330):
        y,z=cos(radians(deg)),sin(radians(deg))
        for sign in (-1,1):
            j.append([c,-sign*z*c,sign*y*c,sign*c,z*c,-y*c])
    ht=list(zip(*inv(j)))
    dn=2*sin(radians(.5)/2);dm=.035/R+.15/R*(1+.035/R)+dn
    def mn(p,k,couple=10):
        f=[4*W,W,W,25.4*W/R,50.8*W/R,(52.2 if k=='fault' else 14.5)/R]
        if k=='table':
            h=[W,0,0,W*15.12/R,W*25.97/R,W*hypot(50.8,25.4)/R]
            f=[u+v for u,v in zip(f,h)]
        return min(d[0]*p-sum(abs(q)*v for q,v in zip(d,f))-2*norm(d[1:3])
                   -couple*norm(d[3:])/R-(norm(d[:3])*dn+norm(d[3:])*dm)
                   *(p+f[0])/cos(radians(45.5)) for d in ht)
    req=0
    for k in ('service','table','fault'):
        a=mn(0,k);r=-a/(mn(1,k)-a);req=max(r,req)
        print(k,"net draw threshold, minimum normal at dp82 after 3N seal",r,mn(.082*AMIN-3,k))
    for m in (10.,15.,20.):print("table margin vs total parasitic moment",m,mn(.082*AMIN-3,"table",m))
    for mass in (.060,.065,.070):
        W=mass*9.80665
        print("mass g, table min normal at dp82",mass*1000,mn(.082*AMIN-3,"table"))
    return req

def gas():
    # Integral under tail groove, overestimate by constant FULL radial width.
    # Use a left rectangle upper sum (depth nonincreasing in |t|).
    def d(t):
        if t<=FLAT:return H-t
        return LIP-sqrt(max(0.,LIP**2-(WIDTH-t)**2))
    n=10000; area=2*WIDTH/n*sum(d(i*WIDTH/n) for i in range(n))
    v={'gap .24':AMAX*.24,'3 blind Vs, incl +.04 profile':3*2*L*(area+.04*2*WIDTH),
       'annulus unswept .15':APMAX*.15,'sealed drillings':pi*(.40**2*50+.30**2*30),
       'three sensor wells':3*(pi*1**2*.80+2.0),'vent seat and pocket':pi*1.2**2*1.1+2,
       'seal crevices/ports allowance':24.}
    vd=sum(v.values()); print("dead volumes upper (no cap subtraction)",v,vd,"sweep min",VOL)
    assert vd<340 and VOL>2450
    for pat in (80.,90.,95.,98.,101.325):
        pe=pat*vd/(vd+VOL); warm=pe*1.06
        leak=P*(1000/60.)/VOL*(313.15/293.15)
        print("ambient, equilibrated abs, warm dp, seconds to 82 at 1 sccm",pat,pe,pat-warm,(pat-warm-82)/leak)
    print("at 1 sccm upper kPa/s; min ambient for dp82/85 warm, no leak",
          leak,82/(1-1.06*vd/(vd+VOL)),85/(1-1.06*vd/(vd+VOL)))
    Vmax=vd+APMAX*(STROKE+.05)
    Tamb=293.15; rho=98000/(287.05*Tamb)
    mdot=.60*pi*(.00065/2)**2*sqrt(2*rho*1500)
    print("vent example remaining dm / terminal flow / seconds (not valve rating)",
          .090*1e6*Vmax*1e-9/(287.05*Tamb),mdot,
          90000*Vmax*1e-9/(287.05*Tamb)/mdot)
    print("expanded pressure penalty after pump+4s at .25,.5,1 sccm",
          [q*leak*(2.794+4) for q in (.25,.5,1.)])
    return vd

def face(req):
    centre=34.5-HIDE; apex=centre+sqrt(2)*B; plane=apex-H
    print("head mask, cap centre, apex, passive plane, nominal face gap",34.5,centre,apex,plane,plane-34.5)
    n=.36;mu=.23
    print("buried cap outward resultant per N",n-mu*sqrt(1-n*n))
    print("radial end chamfer min button clearance (ideal), lip to outer/inner glands",
          L-H,(RO-.10-.30)-hypot(R+L,WIDTH),(R-L)-(RI+.10+.30))
    dp=(req+3)/AMIN*1000
    d=.045
    moment=.1*2/3*sum((r+d)**3-(r-d)**3 for r in (RO+.055,RI+.055))
    m=moment+.0003*AMAX*(RO+E)+.010*.1*AMAX+.50*.1*(RO+E)+2.6
    print("Amin/Amax, dp for net draw and 3N seal, parasitic moment budget",AMIN,AMAX,dp,m)
    print("nominal seal perimeter, allowed avg compression line force",2*pi*(RO+RI),3/(2*pi*(RO+RI)))
    print("strip req at dp 1.5, adhesion2N, body and table",.0015*AMAX+2+5*.060*9.80665)
    slope=.075 # 4deg incl plane uncertainty approximated here; see note
    for rr,h in ((12.2,36.015),(23,34.60)):
        print("measured plane 37.75, clearance incl .10 debit over radius",rr,37.75-.10-rr*slope-h)
    assert plane>34.50 and dp<82 and m<10

def outer():
    c=(11.5,.25,.70); a=(0.,1.35)
    def cyl(x,yz,r):return 2*hypot(x-c[0],dist(yz,c[1:])+r)
    def box(lo,hi):return 2*max(dist(c,p)for p in product(*zip(lo,hi)))
    rows={'head ring at 34.60':cyl(34.60,a,14.95),'tail complete plate at -11.50':cyl(-11.50,a,14.95),
          'tail rear cup backing at -6.8':cyl(-6.8,a,5.30),
          'tail internal V plate back -7.65':cyl(-7.65,a,14.95),
          'motor stock':box((3.70,10.85,-5),(30.0,21.55,7.70)),
          'shaft cap':cyl(-6.35,(16.2,1.35),1.85),
          'cell padded':box((.8,-17.,-10.55),(31.85,-11.20,10.55)),
          'waist and foot stock':box((1.8,-12.7,-13.80),(34.,12.7,12.0)),
          'tail and foot stock':box((-9.4,-12.7,-13.80),(-1.8,12.7,12.0))}
    for ang in (90,210,330):
        q=(R*cos(radians(ang)),a[1]+R*sin(radians(ang)))
        rows['full head ball %s'%ang]=2*(dist(c,(33.50,*q))+2.515)
    z=1.35+sqrt(12**2-8.1**2)
    rows['gearing/roof boss']=cyl(.65,(8.1,z),9.55)
    print("stowed selected stock diameters, common centre",c,rows,"max",max(rows.values()))
    print("min table margin ring; piston housing vs cell/motor",1.35-14.95+13.80,11.2-10.8,10.85-10.8)
    print("coaxial pump near vented chamber dead front and at full stroke",
          31.15,31.15-STROKE,31.15-STROKE-1.80-18.2)
    print("old joint x8.0 y8.10 z1.35 is inside fixed rotating barrel wall at r8.1.")

def drive():
    m=.23; radius=8.10;span=10.50; eta=.78
    k=STROKE*pi/(2*radians(95))
    for mu in (.08,.23):
        F=(.098*APMAX+4)/(1-2*m*radius/span)
        T=F*(k+mu*radius)/(1-mu*k/radius)+5
        print("mu, ramp k, carriage thrust, drum torque, motor torque",mu,k,F,T,T/(12*eta))
    print("4796 68rpm moving-point time for 330deg, pump stroke and latch sector",
          *(60*12*(th/360)/68 for th in (330,95,98)))
    print("time for e.g. 4s cutoff volume proof at 1sccm use actual measured pressure rate")
    print("sector pump-screw option effective stroke",(94.5/360)*20*2)
    print("T-cam .60 over 18deg pressure angle vs main circle",.60*pi/(2*radians(18)))
    # Qualified-direction motor option; one complete pump revolution per transition.
    c=(11.5,.25,.7)
    def cyly(x,y,z,r):return 2*hypot(y-c[1],hypot(x-c[0],z-c[2])+r)
    print("transverse motor, cap, large rear gear guarded diameters",max(cyly(13,y,15.35,4.45) for y in (-21.35,15.80)),
          cyly(13,21.70,15.35,1.20),cyly(5,18.90,15.35,6.85))
    cyc=60*16/11; tm=cyc*(246-8)/360
    print("CW 208-100 torque at .67 efficiency, break-even eta",T/(16*.67),T/(16*80))
    print("CW full turn / evacuation ramp / seal closed to end of hold",cyc,cyc*95/360,tm)
    leak=P*(1000/60.)/VOL*(313.15/293.15)
    print("leak budget 98kPa to 82kPa incl +1kPa reserve and +4 s interlock time",
          (86.0337-82-1)/(leak*(tm+4)))
    assert STROKE<11
if __name__=='__main__':
    print("EXPLORATORY, no candidate or gate")
    face(seats());gas();outer();drive()
