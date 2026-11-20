"""Take 18 central gripper: analytic envelopes + a free-pose counterexample.

Python 3 standard library. mm, N, N mm, MPa; exploratory, quasi-static.
No pose integration, friction-direction assumption, or strength allowable.
"""
from math import asin, atan, cos, degrees, hypot, pi, radians, sin, sqrt, tan


def show(label, *v):
    print(f"{label}: " + ", ".join(f"{x:.6f}" for x in v))


mu = .23
phi = atan(mu)
beta = radians(35)
k = 1/tan(beta)
b, rho, neck = 3.20, .80, 1.00
db, drho = .015, .020
ell, half_land = 1.40, .48
D = b+rho
dx = .16
xv, rv = D*cos(beta)+dx, D*sin(beta)-k*dx
# J = core + B_rho.  Core = {r >= rv+max(k|x-xv|, ell(|t|-a))}.
# Truncation beyond r=4.80 is NOT part of the normal cone proof.
show("core ridge axial, radial; minimum working tip radius", xv, rv, rv-rho)
assert ell <= k
lo, hi = radians(34), radians(36)
radial = sin(lo)-mu*cos(lo)
axial = cos(hi)-mu*sin(hi)
show("min jaw radial projection; min seated axial projection per N", radial, axial)
show("radial-only 3-jaw min/max draw; one normal", 3*9.5/tan(hi+phi),
     3*10.5/tan(lo-phi), 10.5/radial)
show("best possible symmetric force-window ratio at 45 degrees", ((1+mu)/(1-mu))**2)

# Actual isolated draw, including +/- .25 N parasitic/loss calibration.
Plo, Phi = 30*1.310-.25, 32*1.390+.25
Slink = (.07*45+2*.4)/7
S = Slink+.25
M = 12*Slink+.020*45+.4+.90
show("actual draw low, high; lateral, moment about Maxwell triangle", Plo, Phi, S, M)
show("same moment if lock displacement grows to .20", 12*(.20*45+.80)/7+.90+.40+.90)
assert Plo>38.20 and Phi<45 and S<2 and M<10
Nsum = Phi/axial
delta = 2*sin(radians(1)/2)
h = .5*sin(beta)+delta
c = h+mu*sqrt(1-h*h)
N1 = (S+c*Nsum)/(radial+c)
h2 = .5*sin(beta)-delta
c2 = h2-mu*sqrt(1-h2*h2)
show("total normal, one front flat; min pair bisector shear at Plo",
     Nsum, N1, c2*Plo/hypot(1,mu))
assert c2*Plo/hypot(1,mu)>S

# All-three connected branch: actual plane offsets at the actual sphere,
# after elastic approach and matched setting. Independent, not averaged.
gerr = .011
ce = hypot(1/cos(beta),4/(3*sin(beta)))
E = gerr/(1-ce*2*sin(radians(.5)/2))
ox, ot = E/cos(beta), 4*E/(3*sin(beta))
axmargin = (xv-.015-ox-(D+db+drho)*cos(radians(34.5)))/sin(radians(35.5))
neckgap = rv-.030-rho-drho-(ot+4.60*sin(radians(1))+1.02)
show("max centre axial, lateral; front flat meridional margin; neck margin",
     ox, ot, axmargin, neckgap)
assert ox<.015 and neckgap>0
# Active side blend begins where ell*(|t|-a) = k*(xv-x).
side_margin = (.48-.02-(ot+(D+db+drho)*sin(radians(.5))))/hypot(1,ell)
show("conservative side facet slack / slope",side_margin)

# Signed free-leading equilibrium. Each jaw including all simultaneous spots.
g0, gN, gD = .55,.12,.08
Nclose=(g0+(1+gD)*1.2)/(radial-gN)
Nopen=g0/(radial-gN)
W=.050*9.80665
show("weak close max normal; free lead max normal; necessary no-load pickup capacity",
     Nclose,Nopen,g0/(1-gD))
show("sufficient push while all three lead, one leads, all contacts outward",
     5*W+3*hypot(1,mu)*Nopen,5*W+hypot(1,mu)*Nopen,5*W)
show("single stopped jaw only, other lateral-free, service S=sqrt(2)W",
     5*W+sqrt(2)*W/tan(lo-phi))

def hertz(n,r):
    a=(3*n*r/(4*115400.))**(1/3)
    return 3*n/(2*pi*a*a)/1000,a

req=1/(1/(b-db)+1/(rho-drho))
for nom,n,r in [('closed front plane',N1,b-db),('free tip',Nopen,req),
                ('capped closing tip',Nclose,req),('backed tip IF same load',N1,req)]:
    show(nom+" N; Hertz GPa, halfwidth",n,*hertz(n,r))
for nom,n in [('neck on free vertex',Nopen),('neck on capped closing vertex',Nclose)]:
    show(nom+" N; Hertz GPa, halfwidth",n,*hertz(n,1/(1/.98+1/(rho-drho))))
assert axmargin>hertz(N1,b-db)[1]+.04
assert side_margin>hertz(N1,b-db)[1]+.04
# Unload BEFORE any radial backer leaves, using an INDEPENDENT rear plane.
# First-exit proof in |O_yz|<=.25, -.030<=O_x<=.030. Violating a leading
# plane puts its core projection on the actual finite flat, not beyond it.
rear=.030; tx=.030; ty=.250
de=2*sin(radians(.5)/2); Et=gerr+de*hypot(tx,ty)
ux=Et/cos(beta); uy=2*(Et+cos(beta)*rear)/sin(beta)
# If a plane were penetrated, its core-plane distance < D+.035 at contact.
assert tx+(D+db+drho)*cos(radians(34.5))<xv-.015
assert ty+(D+db+drho)*sin(radians(.5))<half_land-.02
assert ux<tx and uy<ty
tilt_neck=degrees(asin((rv-.030-rho-drho-uy-1.02)/4.60))
unload_margin=(xv-.015-ux-(D+db+drho)*cos(radians(34.5)))/sin(radians(35.5))
show("rear-plane unload sphere: x upper, lateral norm, neck tilt limit, meridional land",
     ux,uy,tilt_neck,unload_margin)
assert unload_margin>hertz(N1,b-db)[1]+.035
# Local root (one jaw); steel neck section with transmitted residual couple.
nload=N1*hypot(1,mu); w,t,L=2.3,1.8,2.4
show("one jaw nominal bend/shear MPa",6*nload*L/(w*t*t),1.5*nload/(w*t))
dia=1.96; arm=4.60
show("neck axial+bending MPa under coupled draw (pivot datum at root required)",
     Phi/(pi*dia**2/4)+32*(M+arm*S)/(pi*dia**3))

# Exact support path against one RETAINING jaw. Translation only; jaws have
# equal outward travel, not equal load. Both other meridional planes clear.
LAMBDA=.5
def path(theta):
    x=xv-D*cos(theta); y=LAMBDA*x; stroke=y-rv+D*sin(theta)
    return x,y,stroke

elo,ehi=beta,pi/2
for it in range(64):
    e=(elo+ehi)/2
    if path(e)[2]<2.45:elo=e
    else:ehi=e
e=(elo+ehi)/2
x,y,s=path(e)
show("one at open stop: x, lateral, travel, normal angle deg",x,y,s,degrees(e))
show("axial RETENTION min/max per N at that stop",cos(e)-mu*sin(e),cos(e)+mu*sin(e))
assert cos(e)>mu*sin(e) and abs(s-2.45)<1e-10
assert abs(hypot(xv-x,rv+s-y)-D)<1e-10
# For the other jaws replacing y by -y/2 increases relative radial distance;
# they are subsets of the same infinite 2D profile extruded transversely.
assert rv+s-y>0
# A fixed co-axial open trefoil is NOT needed by the witness. If installed,
# check its normals and extent; an unknown new collision is not a proof.
dsep=lambda s:2*((rv-.03+s)*sin(pi/3)-(.48+.02)*cos(pi/3)-(rho+drho))
probe=max(2*(b+db),(b+db)+4.60+1.02)
show("min facing-jaw separations at 2.45, 3.05, 4.40 effective radial stroke",
     *(dsep(v) for v in [2.45,3.05,4.40]))
show("max sphere diameter, ball+neck diameter (not tail plate)",2*(b+db),probe)
assert dsep(3.05)>2*(b+db) and dsep(4.40)>probe
sstar=(D+.5*half_land)/sin(pi/3)-rv
zstar=(rv+sstar)*.5+half_land*sin(pi/3)
assert 1/sqrt(3)<ell and abs((rv+sstar)*sin(pi/3)-half_land*.5-D)<1e-12
assert xv>zstar  # nominal 45-degree seats are separated without tilt
show("two held jaws at exact pinch: stroke, axial x, bisector shift",sstar,xv,zstar)
show("single backed jaw normal if other two free and cage remains isolated",
     (S+2*hypot(1,mu)*Nopen)/radial)
show("core-only required tangential slot at r3.50; neck diameter low",
     2*(half_land+(3.5-rv)/ell),2*.98)
show("largest slot for a rolling .98 neck in a 45-degree well with 2-degree form debit",
     2*.98*sin(radians(45-2)-phi))
for m in (.35,.55):
    ss=(b+.65+.16)*hypot(1,m)+m*xv
    rc,tc=ss*cos(pi/6),ss*sin(pi/6)
    tq=half_land+(4.50-rv)/ell+.60
    show("rail collision: slope, stroke, rail-axis distance",m,rc-4.50,abs(tc-tq))
    assert abs(tc-tq)<.65
# Conservative support of clipped working part in x; NOT the unmodelled stock.
xmax=xv+.015+(4.83-rv+.03+(rho+drho)/sin(radians(34.5)))*tan(radians(35.5))
show("working metal maximum x; sphere / probe past all working metal at x >",
     xmax,xmax+b+db,xmax+4.60+1.02)
