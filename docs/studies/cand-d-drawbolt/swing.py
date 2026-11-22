"""Pivoted keeper discriminator. Distances mm, forces N, torques N mm.
The printed bound requires a maximum outward position and front-side contact.
These are NOT properties deduced from the mating body. No candidate edits.
"""
from math import asin, atan, atan2, ceil, cos, floor, hypot, pi, radians, sin, sqrt
from scipy.optimize import brentq

D,E=3.60,2.80       # meridional vector from pivot to locked cylinder centre (D,-E)
K,B=1.50,2.00       # keeper radius, ball radius
MU=.23
def centre(q):
    return (D*(cos(q)-1)+E*sin(q), D*sin(q)+E*(1-cos(q)))

def minimum_arm(outward_max, cells=600):
    # Enclose ALL angles from 0..60 and all active front-hemisphere normals.
    # g=beta-theta; normal moment = E cos(g)+D sin(g). Normal passes through
    # cylinder centre. Friction moment at the surface is <= mu*|D cos(g)
    # -E sin(g)-K|. t component has no opening-axis moment. Positive upper
    # angle is <= pi/2, and minimum over an interval is at one of its ends
    # for each of the two sinusoids while in its positive lobe.
    least=100.
    for j in range(cells):
        q0=radians(60)*j/cells; q1=radians(60)*(j+1)/cells
        low=(centre(q0)[1]-outward_max)/(K+B)
        if low>1: continue
        lo=asin(max(-1,low))-q1; hi=pi/2-q0
        for sign in (-1,1):
            a=E+sign*MU*D; b=D-sign*MU*E; c=-sign*MU*K
            pts=[lo,hi]
            # Analytic minima; don't assume positive curvature of torque.
            m=atan2(b,a)+pi
            pts.extend(m+2*pi*i for i in range(ceil((lo-m)/(2*pi)),floor((hi-m)/(2*pi))+1))
            least=min(least,*(a*cos(p)+b*sin(p)+c for p in pts))
    # Worst dry journal drag about t incl one-sided side loading. Face
    # thrust assumed at <=1.3 mm; no flange rubbing at the working arm.
    # Centre resultants may be offset <=1.1 along the tangential axis; two
    # bearings span >=4.0. Account for friction couple on the nose, and
    # moments of transverse friction at the lever arm.
    fac=hypot(1,MU); L=hypot(D,E)+K
    journals=.23*.65*(fac*(1+2*1.1/4)+2*L*MU/4)
    axial=.23*1.30*MU
    return least,least-journals-axial

def guard(alpha,gap,b):
    # An axially extruded slot through an inclined guide. Every relevant
    # contact must be on the same rounded profile or one of the adjacent
    # finished faces. Not valid at an intersecting end, rim or open side.
    c=sqrt(1-(gap/(2*b))**2)
    nx=c*sin(radians(alpha))
    return nx, nx-MU*sqrt(1-nx**2)
if __name__=='__main__':
    print('centre travel (x,r) at 60 deg',centre(radians(60)))
    for u in (.5,1.,1.3,1.5,2.):
        print('per N face / after journal+side drag at outward max',u,minimum_arm(u))
    print('zero lower arm at outward max',brentq(lambda u:minimum_arm(u)[1],.5,2.5))
    print('example split guard nx, axial reserve',guard(22,2.,B))

def guarded_arm():
    # Fixed local plane z <= U0 + tan(alpha)*x on sphere CENTRES.
    # U0 includes the extra travel into a <=2 mm slot through a nominal plane,
    # at b=2: b(1-sqrt(1-(half gap/b)^2))/cos(alpha). The wall would
    # need to continue through the entire range where credit is taken.
    alpha=radians(22); k=sin(alpha)/cos(alpha)
    U0=.20+B*(1-sqrt(1-(1/B)**2))/cos(alpha)+.10
    L=K+B
    dq=radians(.25); db=radians(.25)
    f=hypot(1,MU)
    drag=.23*.65*(f*(1+2*1.1/4)+2*(hypot(D,E)+K)*MU/4)+.23*1.30*MU
    w=hypot(D,E)
    # Retain every contact that can oppose +x ejection. Forward assisting
    # contacts (n_x >= mu/sqrt(1+mu^2)) need separate closing/strength tests.
    best=1e4; lim=0.; front=0.
    for j in range(240):
        q=(j+.5)*dq
        x,r=centre(q); x+=L
        for i in range(-360,416):
            b=(i+.5)*db
            if -cos(b)>=MU/f+db/2: continue
            xc=x-L*cos(b); u=r-L*sin(b)
            err=(1+k)*(w*dq+L*db)/2
            if u-k*xc-U0>err:continue
            g=b-q; eg=E*cos(g)+D*sin(g)
            cost=MU*abs(D*cos(g)-E*sin(g)-K)+drag
            arm=eg-cost-(1+MU)*w*(dq+db)/2
            best=min(best,arm)
            lim=max(lim,xc+(w*dq+L*db)/2)
            front=max(front,u)
    return U0,best,lim,front

if __name__=='__main__':
    print('front guard intercept, net arm, last charged centre x, max admitted u',guarded_arm())
