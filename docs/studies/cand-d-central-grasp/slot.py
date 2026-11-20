"""Take 18 thin-blade / hex guard discriminator; stdlib, mm and N."""
from math import sin,cos,tan,atan,asin,radians,degrees,sqrt,hypot,pi
mu=.23;xv=3.436608;rv=2.065802
def out(k,*xs):print(k,*(round(x,6) for x in xs))
# Adjacent unslotted faces. g0 is the NORMALIZED-TO-RADIAL centre limit
# for the ACTUAL B, at x=0, incl its manufacturing allowance.
al,ah=cos(radians(60.5)),cos(radians(59.5))
bl=sin(radians(59.5));ml,mh=.39,.41
C=.19+mh*(xv+.015)-al*(rv-.030)-bl*.34
plo,phi=3.185,3.215;hlo,hhi=.19,.21;qlo,qhi=.585,.615
assert mh*tan(radians(35.5))<al
def Dupper(a,b):return ah*(1. if a<=pi/2<=b else max(sin(a),sin(b)))-min(ml*cos(b),mh*cos(b))
def vbound(zproj):
    # A true tangent must satisfy L v <= C + q Q + (B+h) Q sqrt(1-v²).
    # Replacing negative Q by zero relaxes the inequality.
    Q=max(0.,zproj)
    def slack(v):return C+qhi*Q+(phi+hhi)*Q*sqrt(max(0.,1-v*v))-bl*(plo+hlo)*v
    if slack(1)>=0:return 1.
    a,b=0.,1.
    for _ in range(56):
        m=(a+b)/2
        if slack(m)>=0:a=m
        else:b=m
    return b

minc=1.;maxv=0.
for i in range(1110):
    a,b=radians(34.5+.1*i),radians(34.5+.1*(i+1))
    vmax=vbound(Dupper(a,b));maxv=max(maxv,vmax)
    minc=min(minc,sqrt(1-vmax*vmax)*min(sin(a),sin(b)))
# A pure side has arbitrary core point; its supporting functional m*x-a*r
# is still maximized at the apex + q*hypot(a,m).
assert C+qhi*hypot(ah,mh)<bl*(plo+hlo)
minc-=2*sin(radians(1)/2)
proj=minc-mu*sqrt(1-minc**2)
No=.55/(proj-.12);Nc=(.55+1.08*1.2)/(proj-.12)
out('ball v max, radial normal after debit, radial force floor, free/closing normal caps',
    maxv,minc,proj,No,Nc)
alpha=atan(ml);delta=asin(.640/.980)
nx=sin(alpha)*cos(delta)-2*sin(radians(.5)/2)
out('slot minimum axial normal, axial force floor, max sagitta',
    nx,nx-mu*sqrt(1-nx*nx),.98-sqrt(.98**2-.64**2))
assert proj>.12 and nx>mu*sqrt(1-nx*nx)

def dW(x,r,s):
    dx=abs(x-xv);dr=r-rv-s;sn=sin(radians(35));cs=cos(radians(35))
    return hypot(dx,dr) if sn*dx+cs*dr<0 else max(0.,cs*dx-sn*dr)
def clearance(x,r,t,s,p):
    return hypot(max(0.,dW(x,r,s)-.60),max(0.,abs(t)-.35))-p-.20
def hexnorm(r,t):return max(abs(r),.5*abs(r)+sqrt(3)/2*abs(t))
def wall(x,r,t,p):return .16+.4*x+(3.20-p)*hypot(1.,.4)-hexnorm(r,t)

# A member of the nominal tolerance set: upright ball and a tilted neck.
# Straight neck line is along the blade side. Even the complete uncut hex
# accepts both objects. A real tail housing might exclude this pose.
x,r,t=3.60,-.35,1.53;s=1.50;e=radians(80);p=.98
def neck(l):return x+l*cos(e),r+l*sin(e),t
X,R,T=neck(4.45);E=neck(4.60)
assert abs(T-(.35+.20+p))<1e-12
out('nominal sphere / neck end radial guard slacks',wall(x,r,t,3.2),wall(*E,p))
out('sphere to blade clearance, shaft core-side interior margin, remaining stock',
    clearance(x,r,t,s,3.2),.60-dW(X,R,s),4.80+s-R)
assert min(wall(x,r,t,3.2),wall(*E,p),wall(x,r,t,p),clearance(x,r,t,s,3.2))>.09
assert dW(X,R,s)<.60 and R<4.80+s
for j in [-1,1]:
    co=-.5;si=j*sqrt(3)/2
    # Each differently oriented open jaw lies at r_j >= rv+4.4-.8.
    # Sufficient halfspace for every sphere/capsule point (capsule convex).
    assert max(co*r+si*t+3.2,co*r+si*t+p,co*E[1]+si*t+p)<rv+4.4-.80

def hz(F,p,h):
    rr=1/(1/p+1/h);a=(3*F*rr/(4*115400))**(1/3)
    return 3*F/(2*pi*a*a)/1000
out('hypothetical vertex p0 GPa ball at free/closing caps',
    hz(No,3.185,.19),hz(Nc,3.185,.19))
out('neck curvature example only (not a cap), p0 GPa at 10N',hz(10,.98,.19))
