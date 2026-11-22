"""Take 28 installation revision; stdlib, dimensions mm, no gate metrics."""
from itertools import product
from math import atan, cos, degrees, hypot, pi, radians, sin, sqrt, tan


def cub(name,x,y,z):
    return (name,tuple((a+b)/2 for a,b in (x,y,z)),tuple((b-a)/2 for a,b in (x,y,z)),-1,0.)


def cyl(name,axis,span,c1,c2,r):
    c=[c1,c2]; c.insert(axis,sum(span)/2)
    t=[0.]*3; t[axis]=(span[1]-span[0])/2
    return name,tuple(c),tuple(t),axis,r


def far(s,o):
    _,c,b,i,r=s
    a=[abs(x-y) for x,y in zip(c,o)]
    if i==-1: return hypot(*(x+y for x,y in zip(a,b)))
    return hypot(a[i]+b[i],hypot(*(u for j,u in enumerate(a) if j!=i))+r)


def hs(s,n):
    _,_,b,i,r=s
    if i==-1:return sum(u*abs(v) for u,v in zip(b,n))
    return b[i]*abs(n[i])+r*sqrt(max(0.,1.-n[i]**2))


def rc(q,a):
    return (q[0]*cos(a)-q[1]*sin(a),q[0]*sin(a)+q[1]*cos(a),q[2])


H=(-6.5,-7.8)


def tr(c,p,a):
    x,y,z=rc((c[0]-H[0],c[1]-H[1],c[2]),a)
    return (x+p+H[0],y+H[1],z)


def inv(n,a):
    return rc(n,-a)


def unit(q):
    h=hypot(*q)
    return tuple(u/h for u in q)


BASE=[unit(q) for q in product((-1,0,1),repeat=3) if q!=(0,0,0) and next(x for x in q if x)>0]


def gap(s,t,p,a):
    # Any tested separating axis suffices; overlap on all is inconclusive.
    b=tr(t[1],p,a); v=tuple(y-x for x,y in zip(s[1],b))
    def test(n):
        return abs(sum(x*y for x,y in zip(n,v)))-hs(s,n)-hs(t,inv(n,a))
    normals=[(1.,0.,0.),(0.,1.,0.),(0.,0.,1.),rc((1.,0.,0.),a),rc((0.,1.,0.),a)]
    best=max(test(n) for n in normals)
    if best>1.:return best
    if hypot(*v):normals.append(unit(v))
    normals.extend(BASE)
    normals.extend(rc(n,a) for n in BASE)
    return max(test(n) for n in normals)


def drift(u,angle):
    # Upper radius to the hinge's z axis. Including half-height is safe.
    radius=far(u,(H[0],H[1],u[1][2]))
    return 2*radius*sin(radians(angle)/2)


def skip(s,u,p):
    n=(1.,0.,0.)
    return p+u[1][0]-hs(u,n)-s[1][0]-hs(s,n)-drift(u,15.)-.20>2.


def stock():
    t=[
        cyl('V-cheek',1,(-6.5,-1.70),15,0,10.75),
        cub('guide frame',(-2.10,2.90),(-3.5,28.85),(-7.05,7.05)),
        cub('tongue',(-2.10,19.),(3.50,10.50),(-7.05,7.05)),
        cyl('clamp spindle',1,(-16.80,-6.10),.55,0,4.75),
        cyl('clamp motor',1,(-8.95,19.75),-10,16,3.2),
        cyl('clamp saddle',1,(-5.50,-3.00),-10,16,3.65),
        cub('clamp mount ear',(-8.2,-5.2),(-5.5,-3.0),(17.,18.8)),
        cyl('eject motor',2,(-17.9,10.8),12.6,-15.37,3.2),
        cyl('eject saddle',2,(-4.,-1.50),12.6,-15.37,3.65),
        cub('eject ear',(13.5,16.8),(-16.9,-14.6),(-4.0,-1.5)),
        cyl('eject nut slotted cover',0,(2.05,19.50),-11.5,16.9,2.20),
        cyl('eject front guard',0,(19.50,20.00),-11.5,16.9,1.35),
        cyl('eject opposed races',0,(-6.50,.05),-11.5,16.9,3.35),
        cyl('eject nut',0,(2.20,4.45),-11.5,16.9,1.90),
        cyl('eject bevel front',0,(.1,1.90),-11.5,16.9,2.45),
        cyl('eject quill',2,(13.35,19.55),-.7,-11.5,2.20),
        cub('master guide',(-9.85,19.05),(-17.30,-15.40),(13.65,15.15)),
        cub('roll guide',(-9.85,19.05),(-8.80,-7.80),(-11.15,-10.05)),
        cub('blade',(3.35,4.15),(-1.5,9.25),(-10.65,10.65)),
        cub('blade positive wing',(1.90,2.70),(.65,2.05),(10.40,17.70)),
        cub('blade dogleg joint',(2.30,4.15),(.65,2.05),(10.40,11.10)),
        cub('blade negative wing',(3.35,4.15),(.65,2.05),(-12.6,-10.4)),
        cub('blade +upright',(1.90,2.70),(-11.5,2.05),(16.05,17.70)),
        cub('blade -upright',(3.35,4.15),(-8.8,2.05),(-12.60,-11.40)),
        cub('blade roll shoe',(2.3,4.1),(-8.8,-7.8),(-12.60,-10.00)),
        cub('blade master arm',(2.30,4.15),(-17.30,-10.25),(13.65,17.90)),
        cub('blade master carriage',(-9.70,3.90),(-17.45,-15.25),(13.50,15.30)),
        cub('cell',(-12.35,8.35),(-14.3,16.35),(-20.4,-15.0)),
        cub('MCU',(-11.,11.),(-8.9,8.9),(19.85,25.55)),
        cyl('joint motor',2,(-11.70,7.),-7.9613,-18.1978,3.2),
        cyl('joint pin',2,(-8.7,8.7),*H,1.50),
    ]
    # Outer wheel cheeks are quarter-mm beyond blank in xz. Bolts outside
    # moving wheel pitch/disc bodies, distinct from concentric radial hubs.
    for n,x,z,r in [('wheel',.55,0,11.8),('idler',-10.60309,10.03039,4.),('pinion',-10.,16.,2.8)]:
        t.append(cyl('clamp '+n+' cover',1,(-11.60,-9.50),x,z,r+.25))
    for j,(x,z) in enumerate(((9.5,-9.80),(-12.,-5.),(-15.85,12.),(-9.6,20.5))):
        t.append(cyl('clamp cover bolt '+str(j),1,(-12.35,-9.05),x,z,1.15))
    for n,x,y,r in [('driver',12.6,-15.37,2.4),('idler',7.96084,-10.67551,4.8),('wheel',-.70,-11.5,4.5)]:
        t.append(cyl('eject '+n,2,(12.25,13.40),x,y,r))
    return t


def tail(o,p):
    tx=15.-p
    sites=[(7*cos(radians(a)),7*sin(radians(a))) for a in (180,60,-60)]
    parts=[('boss',hypot(tx+x-o[0],o[1],z-o[2])+3) for x,z in sites]
    parts.extend(('strap',hypot(tx+x-o[0],o[1],z-o[2])+1.2)
                 for x,z in sites+[(7.,7.50),(7.,-7.50),(-8.7,0.)])
    parts.append(('cage',hypot(tx-o[0],2.20-o[1],o[2])+4.15))
    # AABB of .45-offset cropped butt; includes off-axis corners even where
    # outside cap. Do not substitute a full R7 sphere.
    c=6.55*cos(radians(12)); r=6.55*sin(radians(12))+.45
    parts.append(('butt',far(cub('butt',(tx-10.45,tx-3.45-c+.45),(.48-r,.48+r),(-r,r)),o)))
    # Twin Ø2.4 round spines from tail x+7 to +12, transition to clevis at
    # H, z±7.5. Radius bounds convex hull of loaded outer sections.
    for s in (-1,1):
        parts.append(('fork',far(cub('fork',(tx+7,-4.9),(-9.3,1.20),
                                     (s*7.5-1.2,s*7.5+1.2)),o)))
    return max((r,n) for n,r in parts)


def drive():
    mu=.23; f=15.; fy=mu*f; L=12.; y=-16.35; z=14.4
    span=hypot(25.,8.05)
    ey=9.25-y; ez=10.65+z
    tors=2*fy*hypot(ey,ez)/span
    k=2*mu*(abs(-11.5-y)+abs(16.9-z))/L
    base=f+2+mu*(2*f*(ey+ez)/L+fy+2*fy*1.6/L+tors)
    d=base/(1-k)
    ts=d*.87*tan(atan(.4/(pi*1.74))+atan(.18/cos(pi/6)))+1.5
    print('offset master + floating antiroll: sum roll N/feedback/thrust/screw torque/GP',
          *(round(i,4) for i in (tors,k,d,ts,(ts/.82+1)/(2*.85))))


def install():
    t=stock()+[]
    for p in (30.,34.5):
        opt=min((max(max(far(s,o) for s in t),tail(o,p)[0]),o) for o in
                product([-.05*i for i in range(11)],[-.05,.0,.05,.10,.15],[-.05,.0,.05,.10,.15]))
        rad,o=opt
        print('pitch, trial sphere centre, D incl cropped crown/fasteners, leading items:',
              p,o,round(2*rad,4),sorted([(round(2*far(s,o),3),s[0]) for s in t]+
                                         [(round(2*tail(o,p)[0],3),tail(o,p)[1])],reverse=True)[:5])
        # Neighbour articulation: next head rotates about H+p, while its tail
        # stays mated to this head. Test all +/-15 integrally, including theta=0.
        # Sample separation minus .20 mm stock and half-step angular drift.
        pairs=[]
        reserve=999.
        culprit=None
        for s in t:
            for u in t:
                if skip(s,u,p):continue
                lowest=999.
                swing=drift(u,.25)+.20
                for j in range(-30,31):
                    g=gap(s,u,p,radians(j/2))-swing
                    lowest=min(lowest,g)
                if lowest<reserve:
                    reserve=lowest
                    culprit=(s[0],u[0])
                if lowest<0:pairs.append((round(lowest,3),s[0],u[0]))
        print('unseparated parked head/head pairs:',len(pairs),sorted(pairs)[:20])
        print('minimum certified sampled-separator surplus with reserve:',round(reserve,4),culprit)
        # Second neighbour proof using x only, independent angles: bound
        # by both head-to-head rotations and rotated pitch x-component.
        # Origin of second head = H + pX + R(a)pX - R(a+b)H.
        left=min(tr((s[1][0]-s[2][0]-s[4],s[1][1]+k*(s[2][1]+s[4]),0),
                    0,radians(a))[0] for s in t for a in range(-30,31) for k in (-1,1))
        right=max(s[1][0]+s[2][0]+s[4] for s in t)
        print('three-unit non-neighbour conservative x clearance (debit .20 and exact half-step)',
              round(p*(1+cos(radians(15)))+left-right-.20-max(drift(s,.5) for s in t),3))
    # Continuous x envelope of the eject stage and y envelope of open
    # tongue; combine motions conservatively even across interlocked phases.
    def swept(s):
        n,c,b,i,r=s
        axis,stroke=(1,21.5) if n=='tongue' else (0,15.) if n.startswith('blade') or n=='eject nut' else (0,0.)
        if not stroke:return s
        if i not in (-1,axis):raise ValueError(n)
        c=list(c);b=list(b);c[axis]+=stroke/2;b[axis]+=stroke/2
        return n,tuple(c),tuple(b),i,r
    moving=[swept(s) for s in t if swept(s)!=s]
    unresolved=[];minmove=(2.,'broad','broad')
    for s,u in [(s,u) for s in moving for u in map(swept,t)]+[(s,u) for s in t if swept(s)==s for u in moving]:
        if skip(s,u,34.5):continue
        debit=.20+drift(u,.25)
        score=min(gap(s,u,34.5,radians(j/2))-debit for j in range(-30,31))
        if score<0:unresolved.append((round(score,3),s[0],u[0]))
        minmove=min(minmove,(score,s[0],u[0]))
    print('full moving envelope vs neighbour (both may move):',sorted(unresolved)[:20])
    print('moving separation surplus/pair',round(minmove[0],4),*minmove[1:])
    print('Actual mating tail contacts, folded tongue, shell, interconnect and foot contact are NOT certified by SAT.')
    drive()


if __name__=='__main__':install()
