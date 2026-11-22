"""Exploratory. Fixed frame mm,N,Nmm. Positive X from head into mate."""
from math import *
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import minimize
D=Path(__file__).parent;F=16.5;P=38.;H=np.array([-5.90,0.,0.])
R=6.;B=1.65;W=2.50;LEG=3.50;DB=2.40;p=304.8/93
N=10;Rp=p/(2*sin(pi/N));A=np.array([F-10.,0,0]);ST=2.4
TMAX=3.40;YMAX=radians(17);sh=lambda s:tuple(map(float,s))
def sol(n,v,r=0.,d=None):return n,[sh(q) for q in v],float(r),None if d is None else sh(d)
def bx(n,x,y,z):return sol(n,product(x,y,z))
def cy(n,ax,span,cen,r):
    v=[]
    for t in span:
        a=list(cen);a.insert(ax,t);v.append(a)
    return sol(n,v,r,np.eye(3)[ax])
def rod(n,a,b,r):return sol(n,[a,b],r)
def yz(name,r0,r1,x0,x1,y,z,step=16):
    a=[]
    for i in range(step):
        ts=[2*pi*j/step for j in (i,i+1)]
        a.append(sol(name+str(i),[(x,y+rr*cos(t),z+rr*sin(t)) for t,x,rr in product(ts,(x0,x1),(r0,r1/cos(pi/step)))]))
    return a
def trans(s,v):
    return sol(s[0],np.array(s[1])+v,s[2],s[3])
def rot(s,t,o):
    c=cos(t);v=sin(t);m=np.array([[c,-v,0],[v,c,0],[0,0,1]])
    return sol(s[0],(np.array(s[1])-o)@m.T+o,s[2],None if s[3] is None else m@s[3])
def ext(s,d):
    a=np.array(s[1])@d.T;r=s[2]*(1 if s[3] is None else np.sqrt(np.maximum(0,1-(np.array(s[3])@d.T)**2)))
    return a.min(0)-r,a.max(0)+r
ds=np.array([u for u in product(range(-2,3),repeat=3) if u>(0,0,0) and gcd(gcd(abs(u[0]),abs(u[1])),abs(u[2]))==1],float);ds/=np.linalg.norm(ds,axis=1)[:,None]
def extlist(S):return np.array([ext(s,ds) for s in S])
def pairs(a,b,ea=None,eb=None):
    aa=extlist(a) if ea is None else ea;bb=extlist(b) if eb is None else eb
    gap=np.maximum(aa[:,0,None,:]-bb[None,:,1,:],bb[None,:,0,:]-aa[:,1,None,:]).max(2)
    i,j=np.unravel_index(np.argmin(gap),gap.shape);return float(gap[i,j]),a[i][0],b[j][0]
def far(s,c):
    v=np.array(s[1])-c;r=s[2];n=np.linalg.norm(v,axis=1)
    if s[3] is None:return max(n)+r
    v1=v@np.array(s[3]);return max(np.sqrt(v1**2+(np.sqrt(np.maximum(0,n**2-v1**2))+r)**2))
def seatpoint(i):return 13*cos(-pi/2+i*2*pi/3),13*sin(-pi/2+i*2*pi/3)
def tail():
    # Analytic passage in accompanying report. Outer bounding capsules, not solid
    # bore plugs. Straight entry lips are countersunk, see radial profile.
    x=F-P;out=[]
    for sg in (-1,1):
        out.append(cy('return leg OD'+str(sg),0,(x,x+LEG),(sg*R,0),B+W))
        # Larger face bell/blend outer radius: 1.25 edge roll plus wall.
        out.append(cy('return mouth roll reserve'+str(sg),0,(x,x+1.25),(sg*R,0),B+W+1.25))
    v=[(x+LEG+R*sin(t),R*cos(t),0) for t in np.linspace(0,pi,33)]
    for i,(a,b) in enumerate(zip(v,v[1:])):out.append(rod('U tube OD '+str(i),a,b,B+W+R*(1-cos(pi/64))))
    for i in range(3):
        y,z=seatpoint(i);u=(x+1.25,y,z);out.append(rod('seat landing'+str(i),(x+.54,y,z),(x+2.0,y,z),1.85))
        for sg in (-1,1):
            dest=(x+2.00,sg*6.,0.);out.append(rod('tripod stay'+str((i,sg)),u,dest,1.12))
    old=json.loads((D.parent/'cand-d-forced-section'/'take51-interface-v3.json').read_text())
    out+=list(filter(lambda s:s[0].startswith(('tail pivot lug','sector web','tail sector hub','fork tip')),old['own_tail_straight']))
    for sg in (-1,1):
        # Tangential rail along wall, fork to real yawing lug (not central plug).
        out.append(rod('return lug stay'+str(sg),(x+LEG+R,0,sg*3.08),(-10.99,0,sg*6.15),1.37))
    return out
def fixed():
    j=json.loads((D.parent/'cand-d-forced-section'/'take51-interface-v3.json').read_text())['joint'];a=j[:]
    # Three-site trial locations only; final contact surfaces supplied by Take52.
    for i in range(3):
        y,z=seatpoint(i);t=np.array([-z,y])/13.
        for sg in (-1,1):
            v=np.array((y,z))+.93*sg*t
            a.append(cy('fixed face facet reserve'+str((i,sg)),0,(F-1.40,F+.54),v,1.10))
        if i:
            a.append(rod('outer land column'+str(i),(F-.88,y,z),(F-.88,y,-13.7),1.25))
            a.append(rod('outer sill diagonal'+str(i),(F-.88,y,-13.7),(11.65,copysign(8.1,y),-15.1),1.20))
        else:
            a.append(rod('lower land backer',(F-.88,y,z),(11.65,0,-14.80),1.20))
    for sg in (-1,1):
        a.append(bx('sill to front'+str(sg),(-3.5,15.40),(sg*8.1-.68,sg*8.1+.68),(-15.9,-14.4)))
        a.append(rod('sill post'+str(sg),(14.9,sg*8.1,-15.25),(14.5,sg*9.6,-1.8),.72))
        a.append(bx('draw slide guide'+str(sg),(1.95,8.66),(sg*3.8-.6,sg*3.8+.6),(2.64,4.12)))
    # Draw screw is BELOW the trunnion and its coaxial feed shaft. Separate
    # against torque without relying on thread friction: 24-slot screw key.
    z=-10.25;x=A[0];xm=.6;zm=z-sqrt(6.25**2-(xm-.65)**2)
    a.extend([cy('draw screw M3',0,(-2.9,10.8),(0,z),1.50),cy('draw thrust pair',0,(-1.65,.22),(0,z),2.65),
        cy('draw screw bevel 20T',0,(-2.0,-1.1),(0,z),2.25),cy('draw cross bevel',1,(-2.30,-1.38),(.65,z),2.25),
        cy('draw cross shaft',1,(-14.16,-1.32),(.65,z),.93),cy('draw driven spur32',1,(-13.98,-13.02),(.65,z),4.20),
        cy('draw input spur18',1,(-13.98,-13.02),(xm,zm),2.43),cy('draw motor',1,(-12.45,20.35),(xm,zm),3.),
        cy('draw screw index24',0,(-3.80,-2.95),(0,z),3.48),bx('index24 guide',(-4.1,-2.68),(-4.62,-3.59),(z-.95,z+.95)),
        bx('fixed thrust tie',(-1.68,.05),(-3.80,2.35),(z-.95,z+.2))])
    return a
def rocker():
    x=A[0];z=-Rp;out=[]
    out.extend([cy('hollow trunnion OD',2,(-2.82,3.08),(x,0),1.92),
                bx('equalizer under web',(x-1.02,x+.94),(-6.78,6.92),(-2.86,-1.42)),
                cy('tip hard bottom',0,(x-1.93,x-1.17),(6.,0),1.72),
                cy('pocket sprocket blank',1,(-7.43,-4.57),(x,z),Rp+1.02),
                cy('pocket axle',1,(-9.85,-1.54),(x,z),1.15),
                cy('lower feed bevel Y',1,(-2.38,-1.48),(x,z),2.2),
                cy('lower feed bevel Z',2,(z+1.45,z+2.26),(x,0),2.2),
                cy('internal coaxial feed shaft',2,(z+1.42,5.77),(x,0),.77),
                cy('wheel positive backing drum',1,(-9.78,-8.48),(x,z),3.86)])
    for sg in (-1,1):
        y=6*sg
        # At closed no post beyond the retained bead except a two-tine collar
        # with an open throat and a radial edge chamfer. No straight fairlead.
        out.append(cy('arm split bead seat backing'+str(sg),0,(x-1.40,x-.81),(y,0),1.72))
        for sy in (-1,1):
            yy=tuple(sorted((y+sy*.95,y+sy*2.12)))
            out.append(bx('closed collar tine'+str((sg,sy)),(x+.84,x+1.34),yy,(-1.54,1.54)))
        out.append(bx('collar crosshead'+str(sg),(x-.98,x+1.32),(y-2.15,y+2.15),(-2.85,-1.53)))
        out.append(bx('collar fixed cheek'+str(sg),(x-.98,x+.8),(y+1.44,y+2.18),(-2.7,1.2)))
    for sg in (-1,1):
        span=(-8.32,-7.52) if sg<0 else (-4.47,-3.55)
        out.append(cy('wheel bearing cheek'+str(sg),1,span,(x,z),2.81))
        out.append(bx('cheek mounting web'+str(sg),(x-1.05,x+1.05),span,(z,-1.86)))
        for i in range(24):
            out.append(sol('wheel side cover'+str((sg,i)),[(x-rr*sin(t),y,z+rr*cos(t)) for t,y,rr in product((i*pi/24,(i+1)*pi/24),span,(Rp-1.35,(Rp+2.08)/cos(pi/48)))]))
    out.append(cy('rocker stop peg',2,(3.64,4.54),(x+4.,0),.40))
    out.append(bx('rocker peg branch',(x+1,x+4.32),(-.48,.48),(3.58,4.1)))
    # 180-degree covered wrap; use separate outer-sector stock. Inside flank
    # and pocket profiles are not inferred from the cylindrical gear blank.
    for i in range(24):
        out.append(sol('sealed wheel keeper'+str(i),[(x-rr*sin(t),y,z+rr*cos(t)) for t,y,rr in product((i*pi/24,(i+1)*pi/24),(-7.53,-4.47),(Rp+1.40,(Rp+2.08)/cos(pi/48)))]))
    # Stock magazine after the wheel's lower tangent: axial run, U-turn to
    # negative Y, return aft. Permanently crimped larger terminal shoe captured
    # in this track against the entrance shoulder. Cartridge stays on ONE arm.
    z=-2*Rp;mx=8.60;rm=5.48
    v=[(x,-6.,z),(mx,-6.,z)]+[(mx+rm*sin(t),-6.-rm*(1-cos(t)),z) for t in np.linspace(pi/24,pi,24)]+[(-16.0,-6.-2*rm,z)]
    for i,(a,b) in enumerate(zip(v,v[1:])):out.append(rod('shoe magazine OD '+str(i),a,b,2.24+rm*(1-cos(pi/48))))
    out.append(cy('permanent source post stop',0,(x+.28,x+1.48),(-6.,z),2.28))
    out.append(cy('magazine closed rear endcap',0,(-16.62,-16.),(-6.-2*rm,z),2.24))
    # Both fold-outs are on the arm. Two halves per port leave the string
    # once parked. No fixed face post credited as a tension guide.
    return out
def trunk():
    x=A[0]
    shoes=[]
    for side in (-1,1):
        y=side*3.8
        for k in (-1,1):
            xc=x+k*1.75
            for h in (2.05,4.18):
                shoes.append(bx('draw bearing shoe'+str((side,k,h)),(xc-.30,xc+.30),(y-.73,y+.73),(h,h+.53)))
            shoes.append(bx('draw bearing outer strap'+str((side,k)),(xc-.30,xc+.30),tuple(sorted((y+side*.68,y+side*1.25))),(2.05,4.71)))
    return shoes+[cy('draw nut',0,(x-1.62,x+1.52),(0,-10.25),2.40),
            bx('draw nut tab',(x-.88,x+1.17),(-.95,2.05),(-9.20,-7.58)),
            bx('trunnion carriage lower return',(x-.95,x+1.52),(.94,2.28),(-7.94,-2.46)),
            cy('trunnion bearing top',2,(1.41,2.94),(x,0),2.70),cy('short trunnion lower bush',2,(-2.84,-1.49),(x,0),2.68),
            bx('trunnion yoke', (x-.9,x+1.35),(2.20,2.98),(-2.83,2.98)),
            *[cy('roller stop '+str(sg),2,(3.64,4.54),(x+4*cos(radians(20))-.8*sin(radians(20)),sg*(4*sin(radians(20))+.8*cos(radians(20)))),.40) for sg in (-1,1)],
            bx('draw carriage connection',(x-.86,x+1.48),(2.36,4.24),(2.58,3.62))]
def feedmotor():
    # Motors/upper cross axle are on the DRAW SLIDE, not the rocker. A fully
    # disengaged concentric face clutch isolates stator torque in hold.
    x=A[0];z=9.58;xx=x+6.25
    return [cy('feed input spur',1,(-14.65,-13.7),(xx,z),2.46),cy('feed output32',1,(-14.65,-13.70),(x,z),4.20),
            cy('feed gearmotor',1,(-13.08,19.72),(xx,z),3.),cy('feed cross axle',1,(-15.10,-1.6),(x,z),.88),
            cy('top feed Y bevel',1,(-2.4,-1.50),(x,z),2.20),cy('top feed Z bevel',2,(z-2.4,z-1.50),(x,0),2.20),
            cy('feed clutch sleeve retracted',2,(6.12,8.36),(x,0),1.36),cy('feed clutch lower dogs',2,(5.34,5.83),(x,0),1.38),
            bx('feed support and clutch fork',(x-1.26,x+.94),(1.76,2.70),(2.78,8.12))]
def shutter(q):
    H=[]
    for sg in (-1,1):
        H+=yz('eject hoop'+str(sg)+'/',2.92,4.15,F-1.28+q,F+q,6*sg,0)
        H.append(rod('eject spine'+str(sg),(F-1.42+q,sg*6.,-3.46),(F-1.42+q,0.,-10.50),.87))
    H.append(cy('third flush ejector',0,(F-1.86+q,F+q),(0.,-10.42),1.48))
    return H
def outriggers():
    return [bx('stripper slide', (8.20,16.40),(-1.,1.),(-11.68,-9.96)),
            cy('stripper cam and disc key',1,(-2.76,1.56),(8.45,-13.82),3.2),
            cy('sequencer motor',1,(-13.85,18.95),(8.45,-18.72),3.),
            cy('sequencer 18T',1,(-16.43,-15.66),(8.45,-18.72),1.99),
            cy('sequencer 31T',1,(-16.43,-15.66),(8.45,-13.82),3.29),
            cy('sequencer output shaft',1,(-16.88,1.92),(8.45,-13.82),.90)]
def runs():
    print('constants F,P,H,A, bead pitch, sprocket Rp',F,P,H,A,p,Rp)
    bend=lambda r,p:degrees(2*asin(p/(2*r)))
    print('angles at R6 and 10-pocket, nominal/max pitch',bend(R,p),bend(R,TMAX),360/N,bend(Rp,TMAX))
    print('R1.45 base / R1.65 option radial travel for R1.25..1.15', [(b-1.25,b-1.15) for b in (1.45,1.65)])
    print('R6/Rp/R5.48 and articulation nominal/max pitch; no supplier limit',[(r,bend(r,p),bend(r,TMAX)) for r in (R,Rp,5.48)])
    print('max R6 chord sagitta',R-sqrt(R*R-(TMAX/2)**2))
    for h in (.50,.95):
        print('fork halfslot, touching R1.25 space for tine / minimum pitched centres for .50 tine',h,2.50-2*sqrt(1.25**2-h*h),.50+2*sqrt(1.25**2-h*h))
    loop=2*LEG+pi*R;deploy=3.42+loop+F-A[0]
    mag=(8.6-A[0])+pi*5.48+(8.6+16.)
    print('U length, travel from parked tip centre 3.42 back to seated, pitches/turn, magazine route/spare',loop,deploy,deploy/p,360*deploy/(p*N),mag,mag-deploy)
    # Shoe nose locates its last bead at the lower tangent. Five
    # pockets are traversed on chords, not the semicircular pitch-circle arc.
    print('nominal 20-interval cut diagnostic: required path in draw=0, cut, common u to tighten',5*p+2*(F-A[0])+loop,20*p,(20*p-(5*p+2*(F-A[0])+loop))/2)
    print('93 vs 94 per foot over 5 pockets and deployment',(p-304.8/94)*5,(p-304.8/94)*deploy/p)
    print('rocker differential exact for ±17° at D10, projected per arm, single-arm projected ±3.40 yaw',hypot(10+R*sin(YMAX),R*(1-cos(YMAX)))-hypot(10-R*sin(YMAX),R*(1-cos(YMAX))),R*sin(YMAX),degrees(asin(TMAX/R)))
    dx=F-A[0]+.60-R*sin(YMAX)-.20
    for b in (1.45,1.65):
        dr=R*(1-cos(YMAX))+(b-1.15)+.10+.08
        print('angular bound B/minX/max transverse/radians converted deg',b,dx,dr,degrees(atan(dr/dx)))
    print('3 deg entry radius needed using .10 datums and .08 end margin',1.25+.10+LEG*tan(radians(3))+.08)
    for be in (3.,6.7):
        c=cos(radians(be));a=R*cos(YMAX+radians(be))-.08;b=R+.08
        for m in (.5,5.):
            for f in (39.,55.5,113.,184.):
                q=(b*f/c+m)/(a+b);other=f-q
                print('beta/external Nmm/Faxial/arm min,max/Tmax/ratio bound',be,m,f,round(a,4),b,round(q,3),round((b+m/other)/a,4))
    # Worst angular radius on 4 mm peg, tangent at +/-20, fence and peg R.4
    sg=np.array((4*cos(radians(20))-.8*sin(radians(20)),4*sin(radians(20))+.8*cos(radians(20))))
    print('peg hard-stop nominal at 17, debit .10',np.linalg.norm(sg-[4*cos(YMAX),4*sin(YMAX)])-.8)
    for f in (39.,55.5,113.,184.):
        t=(6.08*f/cos(radians(6.7))+5)/(6.08+R*cos(YMAX+radians(6.7))-.08)
        sc=f*.5/(2*pi*.28);rg=32/18
        print('axial, peak leg, stale wheel/key F, screw torque, geared input torque .75 total mesh eff, frictionless index key tangential R3, trunnion shear double and projected bearing 3.8x2.8',f,round(t,2),round(t*Rp/3.8,2),round(sc,2),round(sc/(rg*.75),2),round(f*.5/(2*pi*3.),2),round(f/(2*pi*(1.9**2-1.04**2)),2),round(f/(3.8*2.8),2))
    for t in (2.,4.,8.):
        print('feed line thrust/wheel torque/required gearhead torque incl two bevels and spur at .75 / positive key R3.8',t,t*Rp,t*Rp/((32/18)*.75),t*Rp/3.8)
    for q in (3.,6.):
        print('strip F/cam torque over 1.55 rise 70deg cycloid at .65/required geared torque',q,2*q*1.55/radians(70)/.65,2*q*1.55/radians(70)/.65/(31/18*.8))
    print('M3 .5 and 24-index lock: maximum forward-only advance to lock, paired path change',.5/24,2*.5/24)
    print('1.90 slot remaining overlap at R1.15, projected shear area per side .50 thick x chord height, nominal per-side stress at T30,60.62 all on one',1.15-.95,.5*2*sqrt(1.15**2-.95**2),30/(.5*2*sqrt(1.15**2-.95**2)),60.62/(.5*2*sqrt(1.15**2-.95**2)))
    print('average roll/tube rest friction NOT credited; cut length, fatigue, terminal, source shoe and all caps unverified')
if __name__=='__main__':runs()
