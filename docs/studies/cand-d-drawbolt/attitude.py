"""12-degree continuation: reachable hard-pair partial (no neck/obstacle credited).
mm, geometry only; independent of the Hertz or LP load at the pose."""
from math import asin,cos,degrees,hypot,pi,radians,sin,sqrt
from scipy.optimize import minimize
import numpy as np

b=1.045; H=20.; R=4.65; gap=.09; angle=radians(3.); alpha=radians(12.)
X,Y,Z=np.eye(3)
def B(u):return b-H+sqrt(H**2-u*u)
def h(x,y):
    rho=hypot(x,y)
    return rho if x>=-sin(alpha)*rho else -sin(alpha)*x+cos(alpha)*abs(y)

r=.5*Y+sqrt(3)/2*Z
t=np.cross(X,r); n=cos(angle)*X-sin(angle)*Y   # tail-frame head +X
nx,nr,nt=[n@v for v in (X,r,t)]
c=hypot(nx,nr)
x=(b-H*(1-c))*nx/c; y=(b-H*(1-c))*nr/c; z=H*nt
print('extension: minimum other-constraint slack centrally (lower bound)',
      B(b)-(sin(alpha)*b+cos(alpha)*.70))
print('flat-support tilt degrees, unconstrained K support xyz (x,r,t), clip',
      degrees(asin(nt)),(x,y,z),h(-x,z)-B(y))
d=(H-b)*(1-cos(angle)); side=1.5*R*(1-cos(angle))
assert d+side<gap/2 and h(-x,z)>B(y)
print('max pole growth, free-site transverse shift, available half gap, forward shift',
      d,side,gap/2,1.5*R*sin(angle))
# Confirm the constrained flat support, not used to prove the clearance bound.
v=np.array([nx,nr,nt])
f=lambda p:B(p[2])-h(p[0],p[1])
g=lambda p:B(p[1])-h(-p[0],p[2])
res=minimize(lambda p:-v@p,[b,0,.8],bounds=[(-b,b)]*3,
             constraints=[{'type':'ineq','fun':f},{'type':'ineq','fun':g}],
             method='SLSQP',options={'ftol':1e-13,'maxiter':300})
assert res.success and min(f(res.x),g(res.x))>-1e-8
print('both-active support',res.x,'constraint residuals',f(res.x),g(res.x))
