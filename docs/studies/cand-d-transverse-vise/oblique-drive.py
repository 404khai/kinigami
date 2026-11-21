"""Take 32 geometry/drive screen, exploratory; dimensions mm unless noted."""
from functools import lru_cache
from itertools import combinations, product
from math import atan, cos, degrees, hypot, pi, radians, sin, sqrt, tan
from pathlib import Path
from runpy import run_path

prior=run_path(str(Path(__file__).with_name('install.py')))
T=(-.8,.6,0.); N=(.6,.8,0.); Z=(0.,0.,1.); X=(1.,0.,0.); Y=(0.,1.,0.)
A=(-2.15,1.02,0.); O=(-.2,0.,.15); H=(-6.5,-7.8,0.); P=34.5
L=20.5

def dot(a,b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(k,v):return tuple(k*x for x in v)
def point(q,g,z):return plus(A,plus(mul(q,T),plus(mul(g,N),(0.,0.,z))))
def rot(v,a):
    c,s=cos(a),sin(a)
    return (v[0]*c-v[1]*s,v[0]*s+v[1]*c,v[2])
def unit(v):
    return mul(1/hypot(*v),v)

# Each convex solid is a vertex hull Minkowski-summed with a disk
# normal to axis (or a ball for axis=None). Sweeps extend all hull vertices.
def poly(name,verts,r=0.,axis=None):return (name,tuple(verts),r,axis)
def box(name,x,y,z):return poly(name,product(x,y,z))
def qc(name,q,g,z,r):return poly(name,(point(v,g,z) for v in q),r,T)
def qb(name,q,g,z):return poly(name,(point(*v) for v in product(q,g,z)))
def xyprofile(name,profile,z):return poly(name,((x,y,k) for x,y in profile for k in z))
def sweep(s,v):
    return (*s[:1],s[1]+tuple(plus(p,v) for p in s[1]),*s[2:])
def move(s,v):return (s[0],tuple(plus(p,v) for p in s[1]),*s[2:])
def yaw(s,a,p=0.):
    return (s[0],tuple(plus((H[0]+p,H[1],0.),rot(sub(u,H),a)) for u in s[1]),
            s[2],rot(s[3],a) if s[3] else None)
def far(s,o):
    def f(p):
        d=sub(p,o); u=s[3]
        if u is None:return hypot(*d)+s[2]
        h=dot(d,u);return hypot(h,sqrt(max(0.,dot(d,d)-h*h))+s[2])
    return max(map(f,s[1]))
@lru_cache(maxsize=100000)
def proj(s,n):
    a=[dot(p,n) for p in s[1]];w=s[2]
    if w and s[3]:w*=sqrt(max(0.,1-dot(n,s[3])**2))
    return min(a)-w,max(a)+w
def sep(s,t,n):
    a,b=proj(s,n);c,d=proj(t,n)
    return max(c-b,a-d)
BASIC=(X,Y,Z,T,N)+tuple(unit(plus(mul(-.32,T),k)) for k in [N,mul(-1,N),Z,mul(-1,Z)])+tuple(prior['BASE'])
def check_pair(s,t,axes):
    best=-1e9
    for n in axes:
        best=max(best,sep(s,t,n))
        if best>2.:break
    return best

def retained():
    out=[]
    for n,c,b,i,r in prior['stock']():
        if n.startswith('clamp') or n in ('tongue','guide frame'):continue
        if n=='cell':
            out.append(box(n,(-12.35,8.35),(-14.30,16.35),(-21.75,-16.35)));continue
        if n=='blade':
            out.append(box(n,(3.35,4.15),(-1.50,4.70),(-10.65,10.65)));continue
        if i<0:
            out.append(box(n,*[(x-y,x+y) for x,y in zip(c,b)]))
        else:
            u=(X,Y,Z)[i]
            out.append(poly(n,[plus(c,mul(v*b[i],u)) for v in (-1,1)],r,u))
    return out
def tail(tx):
    sites=[(tx+7*cos(radians(a)),0.,7*sin(radians(a))) for a in (180,60,-60)]
    out=[poly('web',sites,1.2)]
    for i,p in enumerate(sites):out.append(poly('boss '+str(i),[p],3.))
    out += [poly('lower bed',[(tx,-3.50,0.),(tx,1.20,0.)],4.,Y),
            poly('upper retainer',[(tx,y,0.) for y in (1.2,2.56)],4.,Y),
            poly('upper ball',[(tx,.5,0.)],3.),
            poly('aft spine',[sites[0],(tx-8.7,0.,0.)],1.2)]
    a=6.55*cos(radians(12)); r=6.55*sin(radians(12))+.45
    out.append(box('rear cap',(tx-10.45,tx-3.45-a+.45),(.48-r,.48+r),(-r,r)))
    for sign,i in [(1,1),(-1,2)]:
        z=7.5*sign
        out.extend([poly('root'+str(i),[sites[i],(tx+7,0.,z)],1.2),
                    box('arm'+str(i),(tx+7,tx+12),(-1.2,1.2),(z-1.2,z+1.2)),
                    xyprofile('fork'+str(i),[(tx+12,1.2),(tx+12,-1.2),(tx+13-1.50,-7.80),
                                             (tx+13,-9.30),(tx+13+1.5,-7.8)],
                              (z-1.2,z+1.2))])
    return out

def cross(p,q):
    return (p[1]*q[2]-p[2]*q[1],p[2]*q[0]-p[0]*q[2],p[0]*q[1]-p[1]*q[0])
def toe():
    # Coordinates u,v,z about (15,3.5,0); u=-T, v=N.
    planes=[((.6,-.8,0.),0.),((.8,.6,0.),2.85),((.32,1.,0.),2.60),
            ((.32,-1.,0.),1.05),((.32,0.,1.),2.85),((.32,0.,-1.),2.85),
            ((-.8,-.6,0.),13.35)]
    pts=[]
    for (a,h),(b,k),(c,l) in combinations(planes,3):
        den=dot(a,cross(b,c))
        if abs(den)<1e-9:continue
        v=mul(1/den,plus(plus(mul(h,cross(b,c)),mul(k,cross(c,a))),mul(l,cross(a,b))))
        if all(dot(n,v)<t+1e-8 for n,t in planes):
            pts.append(plus((15.,3.50,v[2]),plus(mul(-v[0],T),mul(v[1],N))))
    return poly('toe cone',pts)
def ram():
    qz=-12.75
    def zc(name,x,y,span,r):
        return poly(name,[(x,y,z) for z in span],r,Z)
    q=-2.3; apex=point(q,-4.45,qz)
    mot=(-.75,-19.1)
    du,dv=apex[0]-mot[0],apex[1]-mot[1];ell=hypot(du,dv)
    along=(7.2**2-9.0**2+ell**2)/(2*ell);side=sqrt(7.2**2-along**2)
    idler=(mot[0]+(du*along-dv*side)/ell,mot[1]+(dv*along+du*side)/ell)
    u=[qc('spindle',(-4.25,22.95),0,qz,1.25),
       qc('thrust drum',(-3.95,-.15),0,qz,3.25),
       qc('wheel blank',(-3.4,-1.25),0,qz,3.20),
       zc('worm',*apex[:2],(qz-2.15,qz+2.15),1.75),
       zc('worm quill',*apex[:2],(qz+2.15,14.20),.95),
       zc('quill gear',*apex[:2],(10.85,11.85),4.20),
       zc('motor',*mot,(-18.50,10.20),3.20),
       zc('motor saddle',*mot,(6.5,8.2),3.50),
       zc('driver',*mot,(10.85,11.85),2.40),
       zc('idler',*idler,(10.85,11.85),5.40),
       qc('nose',(22.95,23.95),0,qz,1.6),
       qb('master rail',(-4.3,22.58),(3.80,5.65),(-15.75,-14.30)),
       qb('roll rail',(-4.10,22.75),(6.70,8.20),(-13.15,-11.50))]
    u += [zc('worm lower journal',*apex[:2],(-16.05,-15.05),1.8),
          zc('worm upper journal',*apex[:2],(-10.45,-8.10),1.65),
          zc('worm outboard journal',*apex[:2],(8.75,10.15),1.65),
          zc('driver hub',*mot,(10.20,11.90),1.25),
          zc('idler pin',*idler,(9.60,12.00),1.30),
          qb('rail back at root',(-3.62,4.40),(3.55,8.55),(-16.03,-15.70)),
          qb('rail back at mid',(4.40,16.25),(3.55,8.55),(-16.03,-15.70)),
          qb('master support rib',(16.25,22.35),(3.80,5.65),(-15.91,-15.70)),
          qb('roll shoe bed',(-3.95,17.50),(6.7,8.2),(-15.68,-13.13)),
          qb('roll rear backing',(17.50,22.60),(6.7,8.2),(-14.55,-13.13)),
          box('frame side root',(-.55,1.40),(-10.55,7.5),(-16.03,-15.73)),
          box('frame edge beam',(-.55,13.7),(-10.55,-9.15),(-16.03,-14.10)),
          box('frame lower tie',(10.10,13.70),(-10.55,-9.15),(-15.95,-6.60)),
          box('frame cheek foot',(10.10,13.70),(-10.55,-6.30),(-8.20,-6.60))]
    moving=[qc('ram nut',(.10,2.10),0,qz,1.85),
            qb('master gib',(-3.85,1.85),(3.55,5.98),(-15.40,-13.90)),
            qb('roll gib',(-3.65,2.0),(6.38,8.52),(-12.9,-11.10)),
            qb('nut tab',(.4,1.75),(-.8,.8),(-11.15,-9.85)),
            qb('master tab',(.25,1.40),(4.1,5.15),(-14.00,-9.85)),
            qb('roll tab',(.25,1.40),(7.0,7.9),(-11.20,-9.85)),
            qb('inboard web',(.25,1.75),(-.8,8.15),(-10.45,-9.70)),
            xyprofile('upright',[(-4.2,1.8),(-1.8,1.8),(1.45,7.3),(1.45,9.75),(-1.0,9.75)],(-10.45,-9.30)),
            box('collar',(-.90,1.68),(7.30,9.75),(-10.45,3.)),toe()]
    return u,moving
def setscan(first,second,angles,p,margin,ignore=(),travel=0.):
    ans={}; minimum=(2.,'','')
    for deg in angles:
        a=radians(deg);norm=BASIC if not a else BASIC+tuple(rot(n,a) for n in BASIC)
        for t in second:
            b=yaw(t,a,p);debit=margin
            if travel:b=sweep(b,mul(travel,X))
            if len(angles)>1:
                debit+=2*far(t,H)*sin(radians((angles[1]-angles[0])/4))
            for s in first:
                if (s[0],t[0]) in ignore:continue
                g=max(check_pair(s,b,norm)-debit,sep(s,b,Z)-margin)
                if g<0:
                    key=s[0],t[0]
                    if g<ans.get(key,(1.,0))[0]:ans[key]=(round(g,4),deg)
                minimum=min(minimum,(g,s[0],t[0]))
    return sorted((score,n,m,a) for (n,m),(score,a) in ans.items()),minimum

def install():
    f,m=ram(); e=retained(); t=tail(15.-P); angles=[j*.5 for j in range(-30,31)]
    mv=[sweep(s,mul(L,T)) for s in m];op=[move(s,mul(L,T)) for s in m]
    es=[sweep(s,mul(15.,X)) if s[0].startswith('blade') or s[0]=='eject nut' else s for s in e]
    tests=[('ram vs own fixed, ejector parked',mv+f,e,[0.],0.),
           ('open ram vs own full eject',op+f,es,[0.],0.),
           ('ram vs own articulated tail',f+mv,t,angles,0.),
           ('previous head vs ram',es,f+mv,angles,P),
           ('ram vs next head',f+mv,es+f+mv,angles,P),
           ('retained vs next retained, shifted battery',es,es,angles,P),
           ('ram vs fixed mating tail during relief',f+mv,tail(15.),[0.],0.),
           ('open ram vs departing aligned tail',f+op,[sweep(s,mul(15.,X)) for s in tail(15.)],[0.],0.),
           ('internal ram',mv,f,[0.],0.)]
    print('D stow',sorted([(round(2*far(s,O),3),s[0]) for s in f+m+t+e],reverse=True)[:8])
    for n,u,v,a,p in tests:
        intended={('frame cheek foot','V-cheek')} if p==0 and 'own' in n else set()
        if n.startswith('ram vs fixed mating'):intended.add(('toe cone','upper ball'))
        if n=='internal ram':intended.update([('ram nut','spindle'),('master gib','master rail'),('roll gib','roll rail')])
        bad,bnd=setscan(u,v,a,p,.20,intended,15. if p else 0.)
        print(n,'unseparated',len(bad),bad[:18], 'minimum',bnd)
        assert not bad, (n,bad)

    h=f+mv+es
    # First-to-third head: p*X + R(a)*p*X + H - R(a+b)*H,
    # with relative angle a+b within 30deg, translations nonnegative in x.
    left=min(proj(yaw(s,radians(a)),X)[0]-2*far(s,H)*sin(radians(.25))
             for a in range(-30,31) for s in h)
    print('third-head independent-angle conservative x gap',
          round(P*(1+cos(radians(15)))+left-max(proj(s,X)[1] for s in h)-.20,4))
    # Joint/load case uses a full, clipped solid toe; positive values mean
    # the screw centre in the rejected low-layout is strictly inside all planes.
    inside=[]
    for q in range(23):
        p=plus((P+H[0],H[1],0.),rot(sub(plus((-4.5,4.,0.),mul(q,T)),H),radians(15)))
        d=sub(p,(15,3.5,0));u=-dot(T,d);v=dot(N,d)
        g=min(d[1],2.85-d[0],(2.6-v-.32*u)/hypot(1,.32),
              (1.05+v-.32*u)/hypot(1,.32),(2.85-abs(d[2])-.32*u)/hypot(1,.32),d[0]+13.35)
        inside.append((g,q,p))
    print('rejected low screw buried normal margin, q, point:',max(inside))
    print('toe home, deployed xmax; collar and sill projection',
           proj(toe(),X),proj(op[-1],X),proj(m[-2],N),(6.39-.45,6.39))
    # A trial 2nd load path must be dimensioned, not credited.
    Pn=85.;w=1.95;b=.30
    print('single web Mx / section modulus / nominal bending MPa:',
          Pn*15.88,w*b*b/6,Pn*15.88/(w*b*b/6))
    assert 2*max(far(s,O) for s in f+m+t+e)<60
    assert proj(op[-1],X)[1]<1.451 and max(inside)[0]>4

def loads():
    # Centre of front/rear master reaction planes is at q=-1; station
    # spacing 4.7 in a 5.70 long gib. Entire flat contact box allowed.
    G=point(-1.,4.73,-14.7)
    pads=[sub(p,G) for p in product((11.95,17.85),(3.50,),(-3.64,3.64))]
    a,n,z=[max(abs(dot(p,k)) for p in pads) for k in (T,N,Z)]
    en,ez=4.73,abs(-12.75+14.70);span=4.70;roll=7.45-4.73
    for Pn in (65.,85.,120.):
        # F applied to the toe. Component bounds can act adversely together.
        Fq,Fn,Fz=(.6+.8*.23)*Pn,(.8+.6*.23)*Pn,.23*Pn
        Mz=a*Fn+n*Fq; Mn=a*Fz+z*Fq; Mq=n*Fz+z*Fn
        base=Fn+Fz+2*(Mz+Mn)/span+2*Mq/roll
        for mu in (.04,.08,.12,.23):
            rho=2*mu*(en+ez)/span
            D=(Fq+3+mu*base)/(1-rho)
            dm=2.273;lead=.35
            Tthread=D*dm/2*tan(atan(lead/(pi*dm))+atan(.18/cos(pi/6)))
            Ttotal=Tthread+.10*D*2.50+1.5   # one plain thrust face; not rolling
            gear=12*26/14; GP=Ttotal/(gear*.85*.55)
            print('P / mu_g / feedback / T thrust / Tshaft / TGP',
                  *(round(x,3) for x in (Pn,mu,rho,D,Ttotal,GP)))
        print('P/Mq/one antiroll reaction',Pn,round(Mq,1),round(Mq/roll,1))
    lead=.35;dm=2.273;lam=atan(lead/(pi*dm))
    print('lead angle deg; thread mu threshold for self lock',degrees(lam),cos(pi/6)*tan(lam))
    print('shaft torque holding per 100N if friction vanishes',100*lead/(2*pi))
    print('stowed stroke/L screw turns and minutes at nominal comparator',
          L/lead,L/lead*(12*26/14)*(531441/2401)/5670)
    # Screw estimated tensile/root diameter per ISO metric external profile.
    root=2.5-1.22687*.35;I=pi*root**4/64
    print('Euler thrust at 25mm, K=1/K=2',*[round(pi*pi*200000*I/(K*25.)**2,2) for K in (1.,2.)])
    print('frictionless force at 200Nmm applied screw torque',2*pi*200/.35)

if __name__=='__main__':
    install()
    loads()
