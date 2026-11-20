"""Exploratory design arithmetic; mm, N, N mm. Run: python3 take9.py
Requires numpy and scipy (linprog HiGHS). No Kinigami code or gate changes.
"""
from math import asin, atan, cos, degrees, pi, radians, sin, sqrt, tan
import numpy as np
from scipy.optimize import linprog

mu = .23
# Preserved intermediate results of the earlier one/two-site working-load screen;
# inputs, NOT six-dimensional reaction upper bounds for three sites or a new e.
# Each tuple: mass g, case, lip N, nut force on radial section N, nut force on dwell N.
screens = [(46, 'service', 36.92, 46.37, 90.61), (46, 'adverse', 76.81, 96.47, 96.51),
           (46, 'fault', 73.56, 92.39, 95.01), (50, 'service', 39.31, 49.38, 91.17),
           (50, 'adverse', 82.67, 103.83, 97.58), (50, 'fault', 74.94, 94.13, 95.44)]
r = 1.25
lead = .35 / (2*pi*r)
thread_mu = mu / cos(pi/6)
k_raise = r*(thread_mu + lead)/(1 - thread_mu*lead)
k_lower = r*(thread_mu - lead)/(1 + thread_mu*lead)
for m, case, lip, radial, dwell in screens:
    print(m, case, 'max nut N', max(radial, dwell), 'thread Nmm', round(k_raise*max(radial,dwell), 2))
print('sleeve stroke mm', .42/tan(radians(11))+.13/tan(radians(34))+.57+.35+.12)

def ramp(angle, drag):
    t = tan(radians(angle))
    return (t+drag)/(1-drag*t)

# Sum of two measured radial plunger contact forces throughout rise (targets).
lo = 108*ramp(44.5, 0)
for friction in (.03, .23):
    hi = 112*ramp(45.5, friction)
    print('breaker', friction, 'min/max N', lo,hi, 'thread trip / backed off Nmm', k_raise*hi,k_lower*hi)
for m in (46, 50):
    print('eject N, 4W+W', m, 5*m*.001*9.80665)
for wall, sphere in [(29,.98),(39,.55)]:
    a = radians(wall-2)-asin(.38/(2*sphere))
    print('window', wall, sphere, 'sag mm', sphere-sqrt(sphere*sphere-.19**2), 'axial reserve',sin(a)-mu*cos(a))
for radius in (.72,.95):
    print('shoulder min outward angle deg',degrees(asin(1-(1-radius)/.55)))

def lash(gap, e):
    R = 5.35
    # 0.03 mm Euclidean location perturbation per vertex. For ideal equilateral
    # triangle altitude = 1.5*R; using altitude +.06 conservatively.
    lam = (R/2-.03-e)/(1.5*R+.06)
    zsum = gap/lam
    hsum = zsum/tan(radians(44))
    # Equilateral interpolation with centered origin. Correct translation/tip/
    # rotation for actual placement by perturbation of the interpolation matrix.
    # For tangential h_i=t_i.u+R*theta_roll, |delta h_i|<=.03*|theta_roll|
    # assuming tangential directions indexed at nominal axes. Similar for tilt.
    tip = (2*zsum/(3*R))/(1-2*.03/R)
    roll = hsum/(3*(R-.03))
    lateral = 2*hsum/3+2*.03*roll
    return lam,zsum,hsum,lateral,degrees(tip),degrees(roll)
for gap in (.04, .06):
    print('gap,e; lambda, axial/tangent/translation mm, tilt/roll deg',gap,1.35,lash(gap,1.35))

def selfstress(e):
    # Forces on tail in x-outward coordinates. Head spheres contact at C+rho*n.
    # Four inscribed polygonal friction rays per contact: not an outer bound.
    X,Y,Z = np.eye(3)
    cols, ids = [], []
    def contact(label, p, n, u, v):
        for a in (0, pi/2,pi,3*pi/2):
            f=n+mu*(cos(a)*u+sin(a)*v)
            cols.append(np.r_[f,np.cross(p,f),float(label=='lip')])
            ids.append(label)
    for i in range(3):
        a=2*pi*i/3
        radial=cos(a)*Y+sin(a)*Z
        t=np.cross(X,radial)
        for s in ((1,) if i == 0 else (-1,1)):
            n=(X+s*t)/sqrt(2)
            contact(f'{i}:{s}',5.35*radial+1.4*n,n,radial,(s*X-t)/sqrt(2))
    contact('lip',-e*Y,-X,Y,Z)
    A=np.array(cols).T
    b=np.array([0.]*6+[1.])
    sol=linprog(np.zeros(len(cols)), A_eq=A,b_eq=b, bounds=(0,None),method='highs')
    assert sol.success and np.max(abs(A@sol.x-b))<1e-7 and min(sol.x)>=-1e-10
    print('zero-wrench ray e', e, 'normal N per 1 N lip:',
          {key:round(sum(v for v,k in zip(sol.x,ids) if k==key),4) for key in dict.fromkeys(ids)})
    print('ray weights (site order above, four per site)',np.round(sol.x,6).tolist())
for e in (.8,1.10,1.35):
    selfstress(e)
