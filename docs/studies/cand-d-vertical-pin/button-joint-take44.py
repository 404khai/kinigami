"""Take 44, mm/N/Nmm; own Family B revolute, body and full attached tail."""
from runpy import run_path
from pathlib import Path
from math import *
from itertools import product
g=run_path(str(Path(__file__).resolve().parents[1]/'cand-d-transverse-vise'/'oblique-drive.py'))
globals().update({k:g[k] for k in ('X','Y','Z','box','poly','dot','unit','plus','sub','mul','far','rot','sep','proj','move','sweep','check_pair','BASIC')})
H=(-3.5,0.,0.); I=(-3.5,11.25); J=(3.70,13.35); P=36.;O=(-3.5,0.,0.)
C=(15.,0.,0.);R=7.5;r=4.2
BOSS=[(16.57,0.,-8.65),(11.54,9.526,7.07),(11.54,-9.526,7.07)]
def cap(n,a,b,r):return poly(n,(a,b),r)
def ball(n,a,r):return poly(n,(a,),r)
def cyl(n,i,sec,uv,r):
    j=(X,Y,Z).index(i)
    def q(z):v=list(uv);v.insert(j,z);return tuple(v)
    return poly(n,[q(z) for z in sec],r,i)
def mx(s,x):return move(s,(x,0.,0.))
def ringpart(n,c,ri,ro,z,lo=0,hi=360,step=10):
    # Outer polygon circumscribed; hole inscribed, conservative.
    return [poly(n+str(i),[(c[0]+rr*cos(t),c[1]+rr*sin(t),h) for rr,t,h in product((ri,ro/cos(radians(step/2))),map(radians,(i,i+step)),z)]) for i in range(lo,hi,step)]
def yaw(s,a,p=0):
    return (s[0],tuple(plus(plus(H,(p,0,0)),rot(sub(v,H),a)) for v in s[1]),s[2],rot(s[3],a) if s[3] else None)
def tail(p=P):
    x=15-p
    def pt(t):return (x+R*cos(radians(t)),R*sin(radians(t)),0.)
    a=[cap('eye'+str(t),pt(t),pt(t+10),r+R*(1-cos(radians(5)))) for t in range(0,360,10)]
    for j,b in enumerate(BOSS):
        b=plus(b,(-p,0,0));a.append(ball('boss'+str(j),b,r))
        t=atan2(b[1],b[0]-x)
        a.append(cap('metal neck'+str(j),pt(degrees(t)),b,2.0))
    a.append(cap('main stem',(x+R,0,0),(x+11.0,0,0),2.20))
    for sg in (-1,1):
        z=6.15*sg
        a.append(cap('fork'+str(sg),(x+10.25,0,sg*.85),(H[0]-5.10,0,z),1.45))
        a.append(cap('fork tip'+str(sg),(H[0]-5.10,0,z),(H[0]-3.35,0,z),1.45))
        a+=ringpart('tail pivot lug'+str(sg),H[:2],1.57,3.65,(z-1.25,z+1.25),step=30)
    a+=ringpart('tail lower spacer',H[:2],1.57,2.95,(-12.35,-7.35),step=30)
    a+=ringpart('tail sector hub',H[:2],1.57,4.10,(-12.85,-10.65),step=30)
    a+=ringpart('sector web',H[:2],3.2,9.25,(-12.85,-10.65),lo=63,hi=117,step=3)
    return a
def joint():
    a=[cyl('hinge pin',Z,(-13.45,7.80),H[:2],1.50),
       cyl('stationary central knuckle',Z,(-4.30,4.30),H[:2],3.10),
       box('fixed hinge foot',(H[0],2.55),(-1.65,1.65),(-3.80,3.80)),
       box('frame pillar',(1.35,3.25),(-.90,1.30),(-15.75,3.8)),
       box('gear plate spine',(1.10,3.30),(-.75,14.80),(-15.75,-14.55)),
       box('gear plate wing',(-4.85,5.10),(10.40,14.80),(-15.75,-14.55)),
       cyl('compound lower bearing',Z,(-14.8,-13.10),I,1.75),
       cyl('compound output 18T',Z,(-12.85,-10.65),I,2.5),
       cyl('compound shaft',Z,(-15.45,-5.65),I,.95),
       cyl('compound input 42T',Z,(-9.55,-7.35),I,5.5),
       cyl('compound upper bush',Z,(-7.15,-5.65),I,1.8),
       box('axle top bridge',(-4.85,.22),(10.15,13.75),(-6.95,-5.65)),
       box('bridge clamp tang',(-.35,.43),(12.65,13.9),(-6.05,-3.95)),
       cyl('yaw gearmotor',Z,(-6.8,21.9),J,3.0),
       cyl('yaw motor quill',Z,(-12.45,-6.55),J,.95),
       cyl('yaw pinion 18T',Z,(-9.55,-7.35),J,2.5),
       cyl('quill outboard bush',Z,(-12.40,-10.30),J,1.80),
       cyl('bush standoff',Z,(-14.9,-12.3),J,1.60),
       cyl('yaw saddle',Z,(-5.65,-3.65),J,3.65),
       box('motor strap heel',(3.35,5.15),(15.65,17.55),(-5.45,-3.65)),
       box('outer bracket',(3.35,5.15),(16.95,18.55),(-15.75,-3.65)),
       box('bracket heel',(3.35,5.15),(14.1,18.55),(-15.75,-14.55))]
    return a
def electr():
    a=[box('cell',(-17.8,2.90),(-15.33,15.33),(-21.70,-16.30)),
       box('MCU',(-13.10,8.90),(-8.9,8.9),(18.35,24.05)),
       box('joint+X driver',(-15.2,-5.4),(-3.70,5.1),(-16.02,-14.15)),
       box('Z driver',(1.2,7.0),(-11.6,-5.4),(-14.8,-12.75)),
       box('power cutoff',(-11.3,-5.1),(-13.95,-7.10),(-15.65,-13.70)),
       box('cell connector',(-13.2,-9.85),(-7.4,-4.6),(-15.7,-12.8)),
       box('harness channel',(-7.8,-4.8),(-1.0,2.4),(10.45,12.45))]
    for x,y in product((-12.,11.),(-8.5,8.5)):
        a.append(box('foot'+str((x,y)),(x-1.3,x+1.3),(y-1.25,y+1.25),(-23.50,-22.15)))
    return a
def tucked_tail(p=P):
    a=[]
    for s in tail(p):
        if s[0].startswith(('sector web','tail sector hub')):s=move(s,(0,0,3.30))
        if s[0].startswith('tail lower spacer'):continue
        a.append(s)
    return a
J2=(I[0],18.75)
def tucked_joint():
    a=[]
    for s in joint():
        n=s[0]
        if n.startswith(('motor strap','outer bracket','bracket heel','axle top bridge','bridge clamp tang','quill outboard','bush standoff')):continue
        if n in ('yaw gearmotor','yaw saddle','yaw motor quill','yaw pinion 18T'):
            s=move(s,(*sub(J2,J),-3.30))
        if n=='compound input 42T':s=move(s,(0,0,-3.30))
        if n=='compound output 18T':s=move(s,(0,0,3.30))
        if n=='compound upper bush':s=move(s,(0,0,.15))
        if n=='fixed hinge foot':s=box(n,(-4.95,-1.60),(-4.80,0),(-3.80,3.80))
        if n=='frame pillar':s=box(n,(1.10,3.1),(-4.90,-3.20),(-15.75,2.3))
        a.append(s)
    a+=[box('gear plate return',(-5.15,-1.85),(13.9,21.10),(-15.75,-14.55)),
        cyl('quill nose bush',Z,(-15.60,-13.05),J2,1.75),
        box('bearing bridge',(-4.85,-2.15),(10.15,15.15),(-6.95,-5.65)),
        box('bridge tang',(-4.65,-2.35),(14.9,15.55),(-7.65,-5.80)),
        box('saddle spur',(-4.8,-2.2),(21.1,22.9),(-8.75,-7.1)),
        box('bracket return',(-4.8,-2.2),(22.35,23.45),(-15.75,-7.1)),
        box('bracket foot',(-4.8,-2.2),(20.6,23.45),(-15.75,-14.55)),
        box('hinge plate elbow',(1.10,3.1),(-4.90,-.10),(-15.75,-14.55)),
        box('hinge top elbow',(-3.95,2.95),(-4.85,-3.25),(-2.20,2.20))]
    return a
def cc(s):return tuple(sum(v)/len(v) for v in zip(*s[1]))
def check(A,B):
    n=sub(cc(A),cc(B));axes=BASIC+tuple(unit(v) for v in (n,(n[0],n[1],0)) if hypot(*v))
    return check_pair(A,B,axes)
def mated(n,m):
    # A circular hinge pin in the co-axial lug/spacer holes. Other solid
    # stocks remain in the scan, including actual non-toothed support webs.
    return (n=='hinge pin' and m.startswith(('tail pivot lug','tail lower spacer','tail sector hub'))) or (n=='compound output 18T' and m.startswith('sector web'))
def scan(A,B,p,step=1,depart=0,ex=lambda n,m:False):
    bad={};best=(999.,'','',0)
    for deg in range(-15,16,step):
        for s0 in B:
            t=yaw(s0,radians(deg),p)
            t=sweep(t,(depart,0,0)) if depart else t
            debit=.20+2*far(s0,H)*sin(radians(step/4))
            for s in A:
                if ex(s[0],t[0]):continue
                q=max(check(s,t)-debit,sep(s,t,Z)-.20)
                best=min(best,(q,s[0],t[0],deg))
                if q<0:
                    k=s[0],t[0];bad[k]=min(bad.get(k,(999,0)),(q,deg))
    return best,sorted((round(v[0],3),n,m,v[1]) for (n,m),v in bad.items())
def centre(S):
    o=O
    for h in (1.,.4,.2,.1,.05,.02,.01,.005):
        for _ in range(30):
            M=max(far(s,o) for s in S);A=[s for s in S if far(s,o)>M-2*h*sqrt(3)-1e-8]
            v=min((max(far(s,d) for s in A),d) for d in [plus(o,(a*h,b*h,c*h)) for a,b,c in product((-1,0,1),repeat=3)])
            if v[1]==o:break
            o=v[1]
    return o,sorted((round(2*far(s,o),4),s[0]) for s in S)[-4:]
def pair(A,B):
    return sorted((round(check(s,t)-.20,4),s[0],t[0]) for s in A for t in B)
def run():
    for p in (35.,36.,37.5):
        a=tail(p);b=joint();e=electr()
        m,g=scan(b,a,0,ex=mated);print('joint v whole tail',p,m,len(g),g[:18])
        print('joint v eye bosses necks alone',p,scan(b,[s for s in a if s[0].startswith(('eye','boss','metal neck'))],0)[0])
        print('electronics v own tail',p,scan(e,a,0)[0]);print('stock enclosing diameter',p,centre(a+b+e))
    print('stationary joint v electronics',pair(b,e)[:6])
    for p in (35.,36.,37.5):
        # Both full units plus own entire mass at worst foot, no equal
        # normal sharing. Gravity-only, not a multibody Q31 bound.
        reach=max(hypot(x-H[0],y) for x,y in product((-13.3,12.3),(-9.75,9.75)))
        T=.070*9.80665*(3*p+3*reach)
        ratio=42/18*72/18;gh=T/(ratio*.80)
        print('2 followers plus own, mu1, Rfeet, Nmm, gearhead Nmm, min motor/GP efficiency',p,reach,T,gh,gh/(.324*531441/2401))
    print('shaft spacings / ratio',hypot(I[0]-J[0],I[1]-J[1]),hypot(I[0]-H[0],I[1]-H[1]),42/18*72/18)
    for p in (36.,37.5):
        a,b=tucked_tail(p),tucked_joint()
        m,g=scan(b,a,0,ex=mated);print('final stacked joint v whole tail',p,m,len(g),g[:8])
        print('final stacked joint v electronics',pair(b,electr())[:3])
        print('final electronics v own tail',p,scan(electr(),a,0)[0])
        print('final tail and joint subtotal',p,centre(a+b+electr()))
if __name__=='__main__':run()
