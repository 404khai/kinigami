"""Take 46: rolling cartridge; exploratory, mm and N/N. Python stdlib only."""
from itertools import product
from math import asin, atan, atan2, cos, hypot, pi, radians, sin, sqrt, tan

XP, H, R, S = 12.389796, 7.53675, 4.20, 3.225
XA, XF, REAR, WALL, NOTCH = 7.75, 18.4, 9.649, 0.20, 2.0
A, C, SN = radians(28), cos(radians(28)), sin(radians(28))
X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
BOSSES = [(16.567077881337568, 6.735557395310443e-16, -8.648011256569864),
          (11.538278384125135, 9.526279441628827, 7.066987172218985),
          (11.538278384125135, -9.526279441628827, 7.066987172218985)]


def plus(a, b): return tuple(i+j for i, j in zip(a, b))
def sub(a, b): return tuple(i-j for i, j in zip(a, b))
def mul(a, k): return tuple(i*k for i in a)
def dot(a, b): return sum(i*j for i, j in zip(a, b))
def unit(a): return mul(a, 1/hypot(*a))
def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def out(label, *numbers): print(label, *(f"{n:.6f}" for n in numbers))
def low(x): return H+tan(A)*(x-XP)
def top(x): return 28.2-.26*(x-XP)
def side(x): return 4.935-.25*(x-XP)
def work(nx):
    a = asin(nx)-radians(1)
    return sin(a)-.23*cos(a)


def mouth():
    d = sqrt(R*R-S*S)
    h = NOTCH*C
    crit = sin(atan(.23)+radians(1))
    r_work = S/sqrt(1-(crit/SN)**2)
    r_lintel = (S*S+h*h)/(2*h)
    out("roller thresholds: axial work / hidden inner lintel", r_work, r_lintel)
    for r in (3.85, R):
        sag = r-sqrt(r*r-S*S)
        park = (12.0-low(XP+.224))*C-h-sag
        out("radius / roof lip work / lintel depth reserve / parked gap",
            r, work(SN*(r-sag)/r), h-sag, park)
        assert min(work(SN*(r-sag)/r), h-sag, park) > 0
    # Old low inner edge, solved in the tangent/normal plane normal to y.
    dn = d+.4*C
    dt = sqrt(R*R-dn*dn)
    nx = (dn*SN-dt*C)/R
    cx = XF-WALL+R*nx
    cz = low(cx)-d/C
    out("old notch: terminal ball centre x,y,z; corner n_x, work", cx, 0, cz, nx, work(nx))
    out("exterior side/top work; required n_x", work(.25/hypot(1,.25)),
        work(.26/hypot(1,.26)), crit)
    # Minimal-width straight drafted slot w(x)=a+k*(x-XP) containing the locked
    # maximum-stock ellipse; derive intercept from support in direction (-k,1).
    k = tan(atan(.23)+radians(1))
    u, c = .32*tan(A), .48+.32*(H+.4)
    a = c*(sqrt(1-u*u+k*k)-k*u)/(1-u*u)
    out("drafted slot limit: k / intercept / half width at nose / outer side",
        k, a, a+k*(XF-XP), side(XF))
    assert a+k*(XF-XP) > max(R, side(XF))


def centreline():
    eye = [(15+7.5*cos(2*pi*i/240), 7.5*sin(2*pi*i/240), 0) for i in range(240)]
    # Closed circle is contained in chord capsules with this additional sag.
    err = 7.5*(1-cos(pi/240))
    lines = [("eye", a, b, err) for a, b in zip(eye, eye[1:]+eye[:1])]
    lines += [("stem", (22.5, 0, 0), (26, 0, 0), 0)]
    for i,b in enumerate(BOSSES):
        if i == 0:
            points = [b, (22.5,0,0)]
        else:
            xe = 16.5
            points = [b, (xe,b[1],b[2]), (xe,b[1],0),
                      (xe, (1 if b[1]>0 else -1)*sqrt(7.5**2-(xe-15)**2), 0)]
        lines.extend((f"boss{i}/{j}", a, end, 0)
                     for j,(a,end) in enumerate(zip(points, points[1:])))
    return lines


def seats():
    e = unit((1,0,.32))
    w = cross(e,Y)
    result = []
    for i,(b,psi) in enumerate(zip(BOSSES,(-90,30,150))):
        a = radians(psi)
        t = cross(e, plus(mul(Y,cos(a)),mul(w,sin(a))))
        for sign in (-1,1):
            n = plus(mul(e,cos(radians(58))),mul(t,sign*sin(radians(58))))
            p = sub(b,mul(n,R))
            u = unit(cross(n,X))
            v = cross(n,u)
            result.append((i,n,p,u,v))
    return result


def nose(p,n,u,v):
    # Flat nose patch plus an aft-growing octagonal cone, cropped to one X plane.
    half = .65 if n[0] > .7 else 1.2
    corners = [plus(p,plus(mul(u,i*half),mul(v,j*half)))
               for i,j in product((-1,1),repeat=2)]
    xb = min(a[0] for a in corners)-.35
    rear = [(xb,a[1]+.28*(a[0]-xb)*cos(j*pi/4),a[2]+.28*(a[0]-xb)*sin(j*pi/4))
            for a in corners for j in range(8)]
    return corners+rear, xb


def axis_cache(points, n):
    directions = [X,n]
    for i in range(10):
        a = i*pi/18
        for j in range(36):
            directions.append((cos(a),sin(a)*cos(j*pi/18),sin(a)*sin(j*pi/18)))
    # Exactly non-negative x; force a transverse direction's x component to zero.
    directions += [Y,Z,mul(Y,-1),mul(Z,-1)]
    return [(t,max(dot(b,t) for b in points)) for t in directions]


def axial_gap(a,b,axes):
    return max(min(dot(a,t),dot(b,t))-h for t,h in axes)-R


def checks():
    lines = centreline()
    hood = min(max(min((low(p[0])-p[2])*C for p in (a,b)),
                   max(min((sign*p[1]-side(p[0]))/hypot(1,.25) for p in (a,b))
                       for sign in (-1,1)))-R-err for _,a,b,err in lines)
    out("aligned full thick tail to finite hood, ray t>=0", hood)
    assert hood > .04
    crit = sin(atan(.23)+radians(1))
    aft = [(XA,y,z) for y,z in product((-side(XA),side(XA)),(low(XA),top(XA)))]
    axes = axis_cache(aft,X)
    rear_guard = min(max(min(a[0],b[0])-XA-R*crit, axial_gap(a,b,axes))-err
                     for _,a,b,err in lines)
    out("unburied hood rear: adverse-contact margin along aligned path",rear_guard)
    assert rear_guard > 0
    rb = max(hypot(*sub(p,(15,0,0)))+R+err for _,a,b,err in lines for p in (a,b))
    out("body radius around C / all-attitude Cx threshold, local hood",rb,XF+rb)
    out("aligned +X travel to clear hood / gap at +16.8", XF-(15-7.5-R),
        15-7.5-R+16.8-XF)
    out("octagonal side normal work",work(.28*cos(pi/8)/hypot(1,.28*cos(pi/8))))
    for j,(i,n,p,u,v) in enumerate(seats()):
        pts, xb = nose(p,n,u,v)
        axes = axis_cache(pts,n)
        rear_axes = axis_cache(pts[4:],n)
        crit = sin(atan(.23)+radians(1))
        other = float("inf")
        rear_margin = float("inf")
        for name,a,b,err in lines:
            # Bound the swept capsule by separating it over each full subsegment.
            # This is not a set of sample-only point tests.
            steps = 1 if name=="eye" else 12
            seg = [plus(a,mul(sub(b,a),k/steps)) for k in range(steps+1)]
            for s,t in zip(seg,seg[1:]):
                rear_margin = min(rear_margin,
                                  max(min(s[0],t[0])-xb-R*crit,
                                      axial_gap(s,t,rear_axes))-err)
            if name == f"boss{i}/0":
                assert min(dot(sub(q,p),n)-R for q in (a,b)) >= -2e-12
                continue
            other = min(other,min(axial_gap(s,t,axes)-err for s,t in zip(seg,seg[1:])))
        assert max(dot(sub(q,p),n) for q in pts) < 2e-12
        if i == 0:
            ng = min((low(q[0]-1.5)-q[2])*C for q in pts)
        else:
            ng = min((abs(q[1])-side(q[0]-1.5))/hypot(1,.25) for q in pts)
        out(f"land {j}: n_x / work / nonpartner / nose-hood / adverse-rear margin",
            n[0], work(n[0]), other, ng, rear_margin)
        assert min(other,ng,rear_margin,work(n[0])) > 0
        if j==2:
            q = plus(p,plus(mul(n,-1.05),plus(mul(u,1.17),mul(v,-1.17))))
            intrusion = side(q[0])-q[1]
            out("old full-backing interior point/side-skin depth",*q,intrusion)
            assert XA < q[0] < XF and 0 < intrusion < WALL and low(q[0])<q[2]<top(q[0])
        if j==3:
            b=BOSSES[i]
            angle=atan2(b[1],b[0]-15)
            end=(15+7.5*cos(angle),7.5*sin(angle),0)
            c=plus(b,mul(sub(end,b),.10))
            out("straight R4.2 neck: occupied pole inside generator by", R-hypot(*sub(c,p)))
            assert hypot(*sub(c,p)) < R


if __name__ == "__main__":
    print("exploratory; lengths mm, work N/N")
    mouth()
    checks()
