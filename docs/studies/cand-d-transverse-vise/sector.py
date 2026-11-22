"""Take 34, exploratory rigid sector and fixed landing. mm, N, radians."""
from itertools import combinations, product
from math import acos, atan, atan2, cos, degrees, hypot, radians, sin, sqrt

MU=.23
K=.62
# Coordinates (u,w,z), u along D=(.8,-.6), w radially along W=(.6,.8).
ACTIVE=[((.6,-.8,0),0.),((.8,.6,0),2.85),((K,1.,0),3.20),
        ((K,0,1.),3.00),((K,0,-1.),3.00)]
CENTER=(-.20,0.,.15)
H=(-6.50,-7.80,0.)


def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm(a): return hypot(*a)
def scale(a,k): return tuple(x*k for x in a)
def add(a,b,k=1.): return tuple(x+k*y for x,y in zip(a,b))
def unit(a): return scale(a,1/norm(a))
def show(s,*v): print(s, *(round(x,6) for x in v))


def vertices(pl):
    vs=[]
    for (a,j),(b,k),(c,l) in combinations(pl,3):
        den=dot(a,cross(b,c))
        if abs(den)<1e-9: continue
        p=scale(add(add(scale(cross(b,c),j),cross(c,a),k),cross(a,b),l),1/den)
        if all(dot(n,p)<h+1e-8 for n,h in pl): vs.append(p)
    return vs


def rot(q,v):
    x,y,z=v
    return (cos(q)*x-sin(q)*y,sin(q)*x+cos(q)*y,z)


def loc(r,q,p):
    u,w,z=p
    return add((15.-.6*r,3.5-.8*r,0),rot(q,(.8*u+.6*(r+w),-.6*u+.8*(r+w),z)))


def forces(md,error=radians(1.)):
    # Normal makes angle acos(md) to desired direction. Includes one
    # degree total mode-dependent angle mismatch, then full Coulomb disk.
    a=acos(max(-1.,min(1.,md)))+error
    return cos(a)-MU*sin(a)


def work(r,Q,P,rho):
    vs=vertices(P)
    e=unit((1.,2.05,0.))
    gmin=100.
    for n,h in P:
        x,y=.8*n[0]+.6*n[1],-.6*n[0]+.8*n[1]
        slack=h-2.5*hypot(x,n[2])-rho*(norm(n)+y)
        assert slack>=-1e-9   # ball centred rho above every point on Ø5
        if n==(-1.,0.,0.): continue
        # The whole contact face is a polygon. Use the minimum over the
        # entire solid (also bounds all points of its offset fillets).
        # A circular cone test at all vertices implies the same interior
        # because its inverse image under the linear velocity is convex.
        m=unit(n)
        md=min(dot(m,unit((r+w,-u,0))) for u,w,z in vs)
        g=forces(md)
        rr=min(r+w for u,w,z in vs)
        nm=rot(Q,(.8*m[0]+.6*m[1],-.6*m[0]+.8*m[1],m[2]))
        ework=forces(dot(nm,e))
        show('R, face n(u,w,z), opening Nmm/N, terminal unit-v F/N',
             r,*m,g*rr,ework)
        gmin=min(gmin,g)
        assert ework>.18
    return gmin


def sweep(r,Q,P,ROUND,blade,alpha,gap):
    BACK=P[-1][1]
    vs=vertices(P)
    # The centre of a blend involving the rear is at u=-BACK+ROUND.
    # If m.u > .53, the blend assists opening everywhere regardless of
    # access. Exclude the closed slab containing ALL remaining normals.
    turn=max(abs(atan2(u,r+w)) for u,w,z in vs)
    show('rear blends above .53: sweep force/N',forces(.53,turn+radians(1.)))
    assert forces(.53,turn+radians(1.))>.025
    band=vertices(P+[((1.,0.,0.),-BACK+1.53*ROUND)])
    tau=radians(3.)
    aa=radians(12.)
    rc=6.55
    cr=.45+hypot(rc*sin(aa),rc*(1-cos(aa))/2)
    cx=-3.45-rc*(1+cos(aa))/2
    # Measured before push: centre x>=14.95, dy<=.25, tilt<=3deg and
    # home yaw±3deg. Components other than working cap/loose ball.
    low=.25+max(2.56+4*sin(tau),.48+abs(cx)*sin(tau)+cr,
                 1.2+14.83*sin(tau),1.2+8.8*sin(tau))
    xmin=14.95-7.-3.45-.48*sin(tau)
    # Integral R8 cap with a real p=.45 backing sphere, NOT an R8 probe.
    a=radians(19.)
    sep=[]
    for degree in range(91):
        phi=radians(degree); c,s=cos(phi),sin(phi)
        # Inclination of separator in actual cap frame. Rotationally
        # symmetric parts: yaw is immaterial. Extremize each harmonic.
        lo,hi=phi-tau,min(radians(90),phi+tau)
        edge=atan2(7.55*cos(a)-4.5,7.55*sin(a))
        pts=[lo,hi]+[p for p in (0.,radians(90)-a,edge,atan2(2.68,1.95)) if lo<p<hi]
        extreme=100.
        for p in pts:
            cp,sp=cos(p),sin(p)
            cap=(4.5*sp-7.55 if sp>=cos(a) else
                 -7.55*sin(a)*cp+(4.5-7.55*cos(a))*sp)-.45
            stem=-1.95*cp-max(0.,2.68*sp)-.45
            extreme=min(extreme,cap,stem)
        lim=14.95*c-.25*s+extreme
        ball=c*(14.95-.38-.96*sin(tau))-s*(.25+.96+.38*sin(tau))-3.005
        sep.append((c,s,lim,ball))
    worst1=worst2=worst3=1e4
    n=808
    for i in range(n):
        q=(i+.5)*Q/n
        # Enclose complete continuous interval using chord bound; max XY
        # radius over each polygon occurs at a vertex.
        poly=[loc(r,q,p) for p in band]
        debit=2*max(hypot(u,r+w) for u,w,z in band)*sin(Q/(4*n))
        worst1=min(worst1,max(xmin-max(v[0] for v in poly),
                              min(v[1] for v in poly)-low)-debit)
        pairs=[]
        for c,s,cap,ball in sep:
            ext=max(c*x-s*y for x,y,z in poly)+debit
            pairs.append((cap-ext,ball-ext))
        worst2=min(worst2,max(t[0] for t in pairs))
        worst3=min(worst3,max(t[1] for t in pairs))
    # dot(E, p(q)-pivot) = u*cos(Q-q) + (r+w)*sin(Q-q).
    # Its minimum during the stroke is an endpoint: with r+w positive
    # and 0<=Q-q<=101 degrees any interior stationary point is a maximum.
    clear=min(min(u,u*cos(Q)+(r+w)*sin(Q)) for u,w,z in vs)+BACK
    assert clear>=-1e-9
    show('R, rear band sweep clear low/R8/R3 after .10 stack',
         r,worst1-.10,worst2-.10,worst3-.10)
    # No stationary plug can occupy the central rear contact: already at
    # +7deg a .45 tangent probe there fits INSIDE the next toe position.
    delta=radians(7)
    u,w,z=-BACK-.45,1.40,0.
    probe=(u*cos(delta)+(r+w)*sin(delta),(r+w)*cos(delta)-u*sin(delta)-r,0)
    raw=min((h-dot(a,probe))/norm(a) for a,h in P)
    show('R, future-sweep obstruction: clearance around centre minus probe+round',
         r,raw-.45-ROUND)
    assert raw>.45+ROUND
    # On the terminal rear face and its offset fillets a p=.45 ball tangent
    # at normal m has centre no deeper than ROUND+(ROUND+p)*dot(m,E).
    # Actual local metal-to-land gap incl tilt/form at STOP <=.110.
    p=.45
    mis=abs(Q-atan2(2.05,1)-atan2(.6,.8))
    overlap=p-ROUND-(ROUND+p)*alpha-gap
    g=forces(alpha,mis+radians(1.))
    show('tail p, weak-normal overlap, land fringe reserve, surviving force per N',
         p,overlap,.70-(ROUND+p),g)
    assert overlap>.005 and g>.035
    # Blade crossing: entire toe radius >= min xy corner distance; here the
    # closest raw XY corner has smallest x and y and both exceed pivot.
    pivot=loc(r,0,(0,-r,0))
    rob=hypot(min(loc(r,0,p)[0] for p in vs)-pivot[0],3.5-pivot[1])
    rb=max(hypot(x-pivot[0],y-pivot[1]) for x,y in
           product((3.35,4.15),(-1.50,blade)))
    show('core/parked blade radial margin after .20',r,rob-rb-.20)
    assert rob-rb>.20
    show('terminal core x/y min/max',*(f(loc(r,Q,p)[j] for p in vs)
         for j in (0,1) for f in (min,max)))
    aft=[p for p in vs if abs(p[0]+BACK)<1e-7]
    return min(worst1,worst2,worst3)-.10, aft


def previous(p,angle):
    return add((28.,-7.8,0.),rot(angle,add(p,H,-1)))


def package(r,Q,P,aft,viable):
    back=P[-1][1]
    vs=vertices(P)
    amin,amax=min(p[1] for p in aft),max(p[1] for p in aft)
    z=max(p[2] for p in aft)
    # Proposed fixed landing positive-E face width and 0.71 thickness.
    seat=list(product((-back-.80,-back-.09),(amin-.70,amax+.70),(-z-.70,z+.70)))
    show('end seat face opposite corners xyz',*loc(r,Q,seat[4]),*loc(r,Q,seat[-1]))
    show('core closed max distance about common Q12 centre',
         max(norm(add(loc(r,0,p),CENTER,-1)) for p in vs))
    show('fixed seat max distance about same Q12 centre',
         max(norm(add(loc(r,Q,p),CENTER,-1)) for p in seat))
    # Actual falling deck below supporting plane, including any sharper
    # deep grooves. Symmetric smoothing preserves an affine upper bound
    # and opening by a ball is anti-extensive.
    n=unit((1.,1/1.20,0)); plane=(23.04-1.75/1.20)*n[0]
    # At a fixed articulation angle, projected core vertex during the arc
    # has sinusoidal offset from the pivot. Here projections are positive
    # or modestly negative with swept angle in (0,101deg); check interval
    # endpoints and BOTH stationary directions, rather than relying on it.
    core=land=1e4
    speed=norm(add(loc(r,0,(0,-r,0)),H,-1))+max(hypot(u,r+w) for u,w,z in vs)
    taper=.45 if r==12. else .65
    flared=[(u,w+dw,z+dz) for u,w,z in seat for dw,dz in
            product((-.71*taper,.71*taper),repeat=2)]
    xmax=max(loc(r,Q,p)[0] for p in vs+flared)
    show('terminal core + flared seat xmax / arbitrary-attitude finite paddle site xmin',
         xmax,xmax+hypot(12,8.7,1.2)+.20)
    hs=max(norm(add(loc(r,Q,p),H,-1)) for p in flared)
    flare=1e4
    step=radians(.25)
    for j in range(-60,61):
        yaw=j*step
        for p in vs:
            v=add(loc(r,0,p),loc(r,0,(0,-r,0)),-1)
            phi=atan2(n[1],n[0])-yaw-atan2(v[1],v[0])
            qs=[0.,Q]+[phi+k*radians(180) for k in range(-3,4) if 0<phi+k*radians(180)<Q]
            core=min(core,*(dot(n,previous(loc(r,q,p),yaw))-plane for q in qs))
        land=min(land,*(dot(n,previous(loc(r,Q,p),yaw))-plane for p in seat))
        flare=min(flare,*(dot(n,previous(loc(r,Q,p),yaw))-plane for p in flared))
    # Allow .06 each in smoothing radius and vertical deck stock on top
    # of the collision stack, even though ideal symmetric blur alone does
    # not increase the affine upper bound.
    guard=.20+n[0]*.06+n[1]*.06
    core-=guard+2*speed*sin(step/4)
    land-=guard+2*hs*sin(step/4)
    flare-=guard+2*hs*sin(step/4)
    show('previous cheek separator: swept core / seat / bounding flared seat',core,land,flare)
    mis=abs(Q-atan2(2.05,1)-atan2(.6,.8))
    side=forces(taper/hypot(1.,taper),mis+radians(1.))
    show('flared fixed seat side work / bare rear work (no friction)',side,-cos(mis))
    if viable: assert min(core,land,flare)>0
    return seat


def fingers():
    # Possible 1mm-wide strips z±[6.10,7.10], x[14.6,15.2].
    # Nearest rounded web edge, its line from (-7,0) to (3.5,6.062).
    m=1/sqrt(3)
    web=(6.10-m*(.20+7.))/hypot(1,m)-1.2
    boss=18.5-15.2-3.
    show('home strip clear main web / forward bosses / swept toe z',
         web,boss,6.10-4.891)
    d=hypot(15.10-(10.656867+3.50),12.00-13.508178,6.30-6.062178)
    show('strip point inside Take31 displaced forward R3 boss by',3.-d)
    assert 3.-d>1.1
    # At q=atan(.6/.8), the rear becomes a constant-x plane. Put the
    # 180deg-yawed butt's extreme +x tip tangent there at y9.50.
    q=atan2(.6,.8); r=13.; p=loc(r,q,(-3.05,3.40,0))
    sx,sy=p[0]-10.45,p[1]-.48
    show('reverse-paddle tip xyz, site xy, gap to fingers x/blade y, Nmm/N',
         *p,sx,sy,14.6-p[0],sy-3.50-4.70,-(r+3.40))
    assert abs(p[0]-4.15)<1e-9 and sy-3.5>4.70
    # The aligned triangular web recedes from the strips on +X ejection.


def common():
    for k in (2.05,2.10):
        b=radians(51.)
        d=k*cos(b)-sin(b)
        show('k, unnormalized Fx+kFy per N: lower / floor / pusher',
             k,d-MU*sqrt(1+k*k-d*d),k-MU,1-MU*k)


def failed_core():
    r=13.; P=ACTIVE+[((-1.,0.,0.),3.05)]
    p=(-2.85,4.70,0.)
    x,y,z=previous(loc(r,radians(101.),p),radians(15))
    R=hypot(x-15,z)
    # A radius-.45 ball about this point is inside raw hypograph after
    # allowing .06 smoothing. Include neighbour-groove and central cuts.
    b=.45; eps=.06; k=1.2; m=.700208
    Rj=min(hypot(x-c,z-d) for c,d in ((8,0),(18.5,6.06218),(18.5,-6.06218)))
    # local deck is min of flat and falling cone; cusp at R8.04.
    margin=min(10.75-R-b,y+6.50-b,-1.75-y-b,
               -1.75-k*(R-8.04)-y-b*hypot(1,k)-k*eps,
               -3.86+m*(R-1.75)-y-b*hypot(1,m)-m*eps,
               -3/cos(radians(35))+m*(Rj-.70)-y-b*hypot(1,m)-m*eps)
    inward=min((h-dot(n,p))/norm(n) for n,h in P)
    show('real collision previous-frame xyz, cheek ball spare, toe inward distance',
         x,y,z,margin,inward)
    assert margin>.26 and inward>.15


def main():
    # Full-size and compact alternative. The sharp nose in the latter is
    # rounded by the same ball-opening construction; no extra end plate.
    compact=[ACTIVE[0],((.50,1.,0),2.772705098312484),*ACTIVE[3:]]
    for r,deg,active,back,rho,blade,alpha,gap,viable in (
            (13.,101.,ACTIVE,3.05,.15,3.30,.28,.110,False),
            (13.,89.,ACTIVE,3.05,.08,3.30,.49,.100,True),
            (12.,101.,compact,2.40,.15,3.10,.28,.110,True)):
        print('exploratory sector R, stop degrees',r,deg)
        Q=radians(deg); P=active+[((-1.,0.,0.),back)]
        for p in vertices(P): show('vertex local/global',*p,*loc(r,0,p))
        assert work(r,Q,P,rho)>0
        margin,aft=sweep(r,Q,P,rho,blade,alpha,gap)
        assert margin>0
        package(r,Q,P,aft,viable)
    failed_core()
    fingers()
    common()


if __name__=='__main__': main()
