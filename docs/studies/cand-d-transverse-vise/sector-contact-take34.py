"""Take 34, exploratory rigid sector and fixed landing. mm, N, radians."""
from itertools import combinations, product
from math import acos, asin, atan, atan2, cos, degrees, hypot, pi, radians, sin, sqrt

MU=.23
Q=radians(101.)
K,BACK,ROUND=.62,3.05,.15
# Coordinates (u,w,z), u along D=(.8,-.6), w radially along W=(.6,.8).
ACTIVE=[((.6,-.8,0),0.),((.8,.6,0),2.85),((K,1.,0),3.20),
        ((K,-1.,0),.44),((K,0,1.),3.00),((K,0,-1.),3.00)]
REAR=((-1.,0.,0.),BACK)
P=ACTIVE+[REAR]
CENTER=(-.20,0.,.15)


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


def forces(md):
    # Normal makes angle acos(md) to desired direction. Includes one
    # degree total mode-dependent angle mismatch, then full Coulomb disk.
    a=acos(max(-1.,min(1.,md)))+radians(1.)
    return cos(a)-MU*sin(a)


def work(r):
    vs=vertices(P)
    e=unit((1.,2.05,0.))
    gmin=100.
    for n,h in ACTIVE:
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
        # Back R.15 under the full 5 mm flat in actual world Y direction.
        x,y=.8*n[0]+.6*n[1],-.6*n[0]+.8*n[1]
        slack=h-2.5*hypot(x,n[2])-ROUND*(norm(n)+y)
        assert slack>=-1e-9 and ework>.23
    return gmin


def main():
    vs=vertices(P)
    print('exploratory sector; nominal closed vertices (u,w,z and global x,y,z)')
    for p in vs: show('vertex',*p,*loc(13,0,p))
    for r in (12.,13.,18.): show('worst force per N',r,work(r))


if __name__=='__main__': main()
