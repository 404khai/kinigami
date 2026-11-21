"""Exploratory Take 37: positive-drive aft hinge, independent ejector. mm, degrees."""
from runpy import run_path
from pathlib import Path
from itertools import product, combinations
from math import radians, degrees, cos, sin, hypot, atan, atan2, tan, pi
D=run_path(str(Path(__file__).with_name('oblique-drive.py')))
globals().update({k:D[k] for k in ('X','Y','Z','O','H','P','BASIC','poly','box','proj','dot','mul','plus','sub','rot','far','sweep','move','yaw','sep','unit','tail','check_pair','setscan','retained')})
def zc(n,p,z,r):return poly(n,[(p[0],p[1],c) for c in z],r,Z)
def flat(n,xy,z):return poly(n,[(x,y,h) for x,y in xy for h in z])
def shaft(n,p,q,r):return poly(n,[p,q],r,unit(sub(q,p)))
def arc(s,c,a):
    return poly(s[0],[plus(c,rot(sub(p,c),radians(a))) for p in s[1]],s[2],
                rot(s[3],radians(a)) if s[3] else None)
def sh(s,dx):return move(s,mul(dx,X))
def link(n,p,q,w,z):
    vv=(p[1]-q[1],q[0]-p[0],0.);no=unit(vv)
    return flat(n,[(t[0]+i*w*no[0],t[1]+i*w*no[1]) for t in [p,q] for i in (-1,1)],z)
U=(.8,-.6,0.);W=(.6,.8,0.);tip=(15.,3.5,0.)
def uvw(u,w,z):
    return plus(tip,plus(mul(u,U),plus(mul(w,W),mul(z,Z))))
def wide():
    # Compact Take36 triangular profile, widened as the actual transverse
    # metal beam. Both lateral ends drafted along U, not bare +/-z end faces.
    planes=[((-1.,0.,0.),2.40),((.6,-.8,0.),0.),((.50,1.,0.),2.772705),
            ((.62,0,1.),14.25),((.62,0,-1.),14.40)]
    pts=[]
    for (a,h),(b,k),(c,l) in combinations(planes,3):
        den=dot(a,D['cross'](b,c))
        if abs(den)<1e-10:continue
        v=mul(1/den,plus(plus(mul(h,D['cross'](b,c)),mul(k,D['cross'](c,a))),mul(l,D['cross'](a,b))))
        if all(dot(n,v)<=m+1e-7 for n,m in planes):pts.append(uvw(*v))
    return poly('wide drafted jaw',pts)
def stowed(c):
    x,y,_=c;ap=(x+.2,6.35);front=(15.,6.35)
    # Separate arms are joined only at the working crossbar.
    # Negative arm outside roll shoe; positive arm doglegs over wide +wing.
    neg=(-15.55,-12.95);pos=(12.1,14.70)
    return [link('left spoke',c,front,1.32,neg),
            link('right riser',c,ap,1.25,pos),link('right rail',ap,front,1.32,pos),
            zc('left hub',c,neg,2.7),zc('right hub',c,pos,2.7),
            wide()]
def inventory(dx):
    es=[]
    for s in retained():
        if s[0] in ('blade','V-cheek'):s=sh(s,dx)
        if s[0] in ('blade negative wing','blade dogleg joint'):s=sweep(s,mul(dx,X))
        es.append(s)
    return es
def eject(e):
    return [sweep(s,mul(15,X)) if s[0].startswith('blade') or s[0]=='eject nut' else s for s in e]
def working(c,end):
    # Tentative terminal backing for full crossbar rear surface; home in
    # +y, .09 gap at stop. Not a guard on arm roots or terminal slit.
    return arc(poly('roof',[uvw(*k) for k in product((-3.20,-2.49),(-2.50,4.672705),(-16.60,16.45))]),c,end)
def score(s,t,axes=BASIC):return check_pair(s,t,axes)
def nominal(c,end=90,dx=0):
    e=inventory(dx);es=eject(e);mo=stowed(c);f=support(c)+[working(c,end)];m=[sh(s,dx) for s in mo];f=[sh(s,dx) for s in f]
    ts=[(yaw(s,radians(j)),j) for s in tail(15-P) for j in range(-15,16,2)]
    d={};mins={}
    def tally(n,s,t,q,j,skip=False):
        if skip:return
        ax=BASIC+tuple(rot(k,radians(q)) for k in (X,Y));g=max(score(s,t,ax)-.20,sep(s,t,Z)-.20)
        mins[n]=min(mins.get(n,99.),g)
        if g<0:
            p=n,s[0],t[0];v=(round(g,3),q,j)
            if v<d.get(p,(99.,0,0)):d[p]=v
    for s in f:
        for t in es:tally('fixed',s,t,0,0)
        for t,j in ts:tally('fixed tail',s,t,0,j)
    for s in mo:
        for q in list(range(0,end,3))+[end]:
            a=sh(arc(s,c,q),dx)
            for t in es if q==end else e:tally('moving',a,t,q,0)
            for t,j in ts:tally('moving tail',a,t,q,j)
            for t in tail(15+dx):tally('docked',a,t,q,0,s[0]=='wide drafted jaw' and t[0]=='upper ball')
    print('pivot/dx',c,dx,'full D',round(2*max(far(x,O) for x in e+m+f+tail(15-P)),3))
    for n in mins:
        vals=sorted((v,s,t) for (g,s,t),v in d.items() if g==n)
        print(n,len(vals),round(mins[n],3),vals[:6])

def support(c):
    # Axially inserted half-stubs; the fixed annuli are represented by their
    # ODs. No centre shaft or implicit material bridge between the arms.
    return [zc('left stub',c,(-15.75,-9.35),1.8),zc('right stub',c,(9.,14.90),1.8),
            zc('left journal',c,(-12.70,-9.55),3.05),zc('right journal',c,(9.,11.80),3.05)]
def frame(c):
    v=(15.,-6.05,0.)
    f=[]
    for name,z in [('L',(-10.0,-9.40)),('R',(9.05,9.65))]:
        f+=[link(name+' bearing web',c,v,2.85,z),box(name+' cheek foot',(13.0,17.0),(-8.8,-5.85),z)]
    return f
def core():
    return poly('compact core',[(x,y,s*z) for x,y,z in
         [(17.772705,3.50,1.624738),(12.,3.50,4.488),(15.463623,8.118164,4.488)] for s in [-1,1]])
def seat(c,end):
    return arc(poly('compact seat',[uvw(*k) for k in product((-3.20,-2.49),(-2.50,4.672705),(-5.188,5.188))]),c,end)
def pol(c,r,a,z):
    return (c[0]+r*cos(radians(a)),c[1]+r*sin(radians(a)),z)
def gear(c):
    # Trial compound spur train, 4:1 x 4:1 x 4.8:1. Two compound
    # shafts span their actual face separation, not a disconnected gear stack.
    j=pol(c,11.6,184,0.);i=pol(j,8.25,84,0.);m=pol(i,8.25,120,0.)
    f=[zc('G motor',m,(-18.65,10.05),3.20),zc('G motor foot',m,(5.,7.),3.55),
       zc('G pinion',m,(10.45,11.55),2.),zc('G first',i,(10.45,11.55),7.),
       zc('I axle',i,(-14.15,12.95),1.05),zc('G second',i,(-13.15,-12.05),2.),
       zc('G third',j,(-13.15,-12.05),7.),zc('J axle',j,(-16.15,-10.55),1.05),
       zc('G output pinion',j,(-15.55,-13.65),2.40)]
    for n,p,zs in [('I',i,((-14.75,-13.40),(11.85,13.50))),('J',j,((-16.24,-15.75),(-11.85,-10.15)))]:
        f.extend(zc(n+' gear support '+str(k),p,z,1.80) for k,z in enumerate(zs))
    # Circumscribed sectors cover the whole material and teeth through
    # each 8-degree cell; full disk/box are not hard-contact witnesses.
    msec=[poly('sector '+str(a),[pol(c,r,t,z) for r,t,z in product((8.35,10./cos(radians(4))),
                         (a,min(186,a+8)),(-15.55,-13.65))]) for a in range(92,186,8)]
    for a in [95,182]:
        msec.append(link('sector spoke '+str(a),c,pol(c,9.1,a,0),1.55,(-15.55,-13.65)))
    return f,msec,(j,i,m)
def clear(l,r):
    return min((score(s,t)-.2,s[0],t[0]) for s in l for t in r)
def recovery(c,dx):
    pitch=P+dx;e=inventory(dx);ee=eject(e);base=stowed(c);ss=[sh(s,dx) for s in support(c)+frame(c)]
    gf,sector,axes=gear(c);gf=[sh(s,dx) for s in gf];se=sh(seat(c,90),dx)
    ends=[[sh(arc(s,c,a),dx) for s in base+sector] for a in [0,90]]
    ang=list(range(-15,16));f=ss+gf+[se];t=tail(15-P)
    print('pitch',pitch,'gear centres J,I,M (head-local)',axes)
    print('stow diameter with bearing webs/gears/seat',max((2*far(s,O),s[0]) for s in f+e+ends[0]+t))
    for name,l,r in [('fixed drive vs retained',gf,ee),('bearing webs vs retained',ss[4:],ee),
                       ('gear vs home',gf,ends[0][:6]),('gear vs terminal',gf,ends[1][:6])]:
        print(name,tuple(round(x,3) if isinstance(x,float) else x for x in clear(l,r)))
    for name,l,r in [('gear vs own yawing tail',gf,t),('split journals and frame vs own yawing tail',ss,t)]:
        bad,mn=setscan(l,r,ang,0,.20)
        print(name,len(bad),bad[:6])
    for a,b in product([0,1],repeat=2):
        l,r=ends[a],ends[b]
        bad,mn=setscan(l[:6],r[:6],ang,pitch,.20,travel=15.)
        print('jaw/arm vs next jaw/arm q=(%i,%i)'%(90*a,90*b),len(bad),mn,bad[:3])
        # Every other endpoint pairing, including previous or next retained equipment
        # and both yaw and separating translation. Negative projection is unresolved.
        h0=l+f+(ee if a else e);h1=r+f+(ee if b else e)
        bad,mn=setscan(h0,h1,ang,pitch,.20,travel=15.)
        print('complete named endpoint inventory',len(bad),bad[:5])
    allparts=e+ee+f+ends[0]+ends[1]
    rmin=min(proj(yaw(k,radians(a)),X)[0]-2*far(k,H)*sin(radians(.25))
             for a in range(-30,31) for k in allparts)
    print('third head endpoint lower x gap',round(pitch*(1+cos(radians(15)))+rmin-max(proj(k,X)[1] for k in allparts)-.20,3))
    # prefix rear-plane check (positive u,w -- concave over delta in [0,90]).
    off=sub(tip,c);u0=dot(off,U);w0=dot(off,W)
    worst=min(min(dot(sub(p,c),U),dot(sub(p,c),W)) for p in core()[1])
    print('prefix minimum seat-front gap, u/w offset',round(worst-(u0-2.49),6),u0,w0)
    for a in (0,60,90):
        print('terminal x comparison q',a,round(max(proj(sh(arc(s,c,a),dx),X)[1] for s in base),3))
def theta(p,c,a):
    return plus(c,rot(sub(p,c),radians(a)))
def jaw_depth(p):
    d=sub(p,tip);u=dot(U,d);w=dot(W,d);z=d[2]
    return min(u+2.4,d[1],(2.772705-.5*u-w)/hypot(1,.5),(14.25-.62*u-z)/hypot(1,.62),(14.40-.62*u+z)/hypot(1,.62))
def witnesses(c):
    for dx in [0.,3.]:
        p=theta((8.,7.6,12.4),c,90);p=plus(plus(H,(P+dx,0,0)),rot(sub(plus(p,(dx,0.,0)),H),radians(15)))
        print('pitch, next rail witness, depth in previous parked jaw',
              P+dx,tuple(round(v,4) for v in p),round(jaw_depth(sub(p,(dx,0,0))),4))
    lo=[]
    for k in range(901):
        a=k*.1;p=theta((4.6,.48,0.),c,a);x,y,z=p
        g=min(x-3.35,4.15-x,y+1.5,4.7-y)
        if g>0:lo.append((a,g))
        if k==100:print('R7 crown witness q10, depth inside blade',p,g)
    print('sampled crown point inside blade angle',lo[0][0],lo[-1][0])
    # park-to-end co-motion mapped over fixed structures, no prescribed tail path.
    for q in range(0,91,5):
        l=[arc(s,c,q) for s in tail(15.)]
        e=[s for s in inventory(0) if s[0] not in ('V-cheek',)]
        g=clear(l,e);print('virtual co-rotation (NOT trajectory) q/other-stock/floor',q,g,
              round(min(proj(s,Y)[0] for s in l)+23.,3))
    # Finite-thickness fixed seat vs solid arm: points strictly inside both.
    hits=[]
    for q in range(0,91):
        for s in stowed(c)[:3]:
            for p in s[1]:
                centroid=tuple(sum(a[i] for a in s[1])/len(s[1]) for i in range(3))
                for t in [.15,.35,.55,.75,.95]:
                    k=plus(centroid,mul(t,sub(p,centroid)));v=sub(theta(theta(k,c,q),c,-90),tip)
                    u,w,z=dot(v,U),dot(v,W),v[2]
                    g=min(u+3.20,-2.49-u,w+2.50,4.672705-w,z+16.60,16.45-z)
                    hits.append((g,s[0],q,k))
    print('full roof positive interior arm witness',max(hits))
    print('terminal core seat plus arm roots/gear cannot certify all exposed faces')
def force(c):
    def g(p,n):
        rx,ry=p[0]-c[0],p[1]-c[1];d=-ry*n[0]+rx*n[1]
        return d-max(0.,rx*rx+ry*ry-d*d)**.5
    for p,n in [((15,-23),Y),((15,-5.65),Z),((4.15,.48),X),((15,-1.75),Y)]:
        print('point,nominal force direction,g at mu1',p,n,round(g(p,n),4))
    T=85*(15-c[0]);fr=T/9.6;Fmesh=fr/cos(radians(20));shaft=3.6
    print('home static Nmm, tangential output N, resultant mesh N',T,fr,Fmesh)
    print('shaft torsional tau, arm bending MPa (no sharing)',16*T/(pi*shaft**3),6*T/(2.60*2.64**2))
    print('worst mesh+load journal N + projected stress MPa',Fmesh+85,(Fmesh+85)/(shaft*2.80))
    print('bearing webs edge bend MPa no sharing',6*T/(.60*5.70**2))
    print('hold torque at motor ideal/backdrivable incl .70 forward efficiency mNm',T/76.8,T/(76.8*.70))
    print('sufficient measured site x for arbitrary orientation, jaws/journals only',1.05+14.871+.20)
if __name__=='__main__':
    print('EXPLORATORY geometry: dimensions mm, forces N, moments N mm; no qualification')
    c=(-2.,-4.,0.)
    for p in [(-5.,-6.,0.),(-3.5,-4.5,0.),c,(-.5,-4.,0.),(.75,-2.5,0.)]:nominal(p)
    for dx in (0.,3.):recovery(c,dx)
    witnesses(c);force(c)
