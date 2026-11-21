"""One captive thrust crown and a six-contact face, exploratory N/mm/radians.

No torque-free pivots, exact load sharing, permanently seated gripper
or certificate of a dry coefficient are assumed. Port/drive studies are separate.
"""
from itertools import product
from math import atan, cos, hypot, pi, radians, sin, sqrt, tan

import numpy as np

X, Y, Z = np.eye(3)
R, B = 13.50, 5.0
MU, ALPHA = .23, radians(57.5)
PAD_ANGLE = radians(2.)
NORMAL_ERR = radians(.60)
SHIFT = .19  # individual ball centre relative to the nominal triangle
CROWN_R = 8.
CROWN_PATCH = .18  # maximum centre-to-traction distance on crown, not assumed Hertz contact
LATERAL = .085 + CROWN_R*sin(PAD_ANGLE) + CROWN_PATCH
AXIAL = .25  # crown and sphere triangle axial registration after taking up play
ARM = -B*cos(ALPHA)
RET_SIDE, RET_MOM = .25, 1.0  # maximum auxiliary wrench from wiring/returns


def rows(angle, radius=R):
    cols = []
    for i in range(3):
        phase = i*2*pi/3
        l = Y*cos(phase)+Z*sin(phase)
        t = np.cross(X, l)
        for sg in (-1, 1):
            n = X*cos(angle)+sg*t*sin(angle)
            # A spherical normal passes through the actual sphere centre,
            # not the nominal plane containing the V's six contact patches.
            cols.append(np.r_[n, np.cross(l*radius, n)/radius])
    return np.array(cols)


def envelope(mass, case, radius=R, wide=True):
    w = mass*.001*9.80665
    # Old v7 references are a comparison only. Wide case grows lever arms
    # for a trial 40-wide head, site plane at most 40 from the COM, table
    # offset at most 25; one must recalculate using a frozen body.
    half, roll, pitch = (20.,25.,40.) if wide else (12.7,15.12,25.97)
    if wide=='take23':
        half, roll, pitch = 23.,25.,40.
    loads = np.array([4*w,w,w,2*half*w/radius,50.8*w/radius,
                      (52.2 if case=='fault' else 14.5)/radius])
    if case=='table':
        loads += np.array([w,0,0,w*roll/radius,w*pitch/radius,
                           w*hypot(50.8,2*half)/radius])
    return loads


def margin(mass, P, angle, case, mu=MU, arm=ARM, wide=True, radius=R):
    A = rows(angle, radius)
    dual = np.linalg.inv(A.T)
    loads = envelope(mass, case, radius, wide)
    # All elemental crown forces have axial component of one sign. If
    # their sum is P, charge the whole Coulomb cone to EVERY such element.
    # K also covers elastic slope/tilt within the stated normal-angle cap.
    K = tan(PAD_ANGLE+atan(mu))
    delta_n = 2*sin(NORMAL_ERR/2)
    # Continuity from nominal geometry: at the first zero of one
    # frictionless face normal, bound the remaining nonnegative normals
    # by x balance. Angular perturbation below must not permit rank loss.
    sn = (P+loads[0])/cos(angle+NORMAL_ERR)
    ans = []
    for d in dual:
        f,m = d[:3],d[3:]
        g = f + np.cross(m, arm*X)/radius
        # Actual point may wander in a finite disk; includes the Hertz patch.
        # In-plane uncertainty × in-plane shear acts only about x.
        dp = ((LATERAL+AXIAL*K)*np.linalg.norm(m[1:])
              +LATERAL*K*abs(m[0]))/radius
        pad = P*(K*np.linalg.norm(g[1:])+dp)
        est = d[0]*P-np.abs(d)@loads-pad
        est -= np.linalg.norm(f[1:])*RET_SIDE+np.linalg.norm(m)*RET_MOM/radius
        est -= (np.linalg.norm(f)*delta_n+np.linalg.norm(m)*(delta_n+SHIFT/radius))*sn
        ans.append(est)
    delta_row = hypot(delta_n,delta_n+SHIFT/radius)
    assert np.linalg.svd(A,compute_uv=False)[-1] > sqrt(6)*delta_row
    return min(ans)


def required(mass, angle, mu, arm, wide=True):
    req=[]
    for case in ('service','table','fault'):
        m0=margin(mass,0,angle,case,mu,arm,wide)
        slope=margin(mass,1,angle,case,mu,arm,wide)-m0
        # Each row is affine. Do not extend the row limiting at P=0
        # across a switch: bracket and bisect the minimum directly.
        assert slope>0
        lo,hi=0.,250.
        assert margin(mass,hi,angle,case,mu,arm,wide)>0
        for _ in range(45):
            mid=(lo+hi)/2
            if margin(mass,mid,angle,case,mu,arm,wide)>0: hi=mid
            else: lo=mid
        req.append(hi)
    return req


def hertz(N, curvature):
    e_star=213000/(2*(1-.29**2))
    a=(3*N*curvature/(4*e_star))**(1/3)
    return a,3*N/(2*pi*a*a)


def main():
    # Regression: pure axial force equally loaded is one *nominal* solution.
    for a in (radians(45),ALPHA):
        J=rows(a)
        assert np.allclose(J.T@np.ones(6),[6*cos(a),0,0,0,0,0])
        assert np.allclose(np.linalg.inv(J.T)@J.T,np.eye(6))
    for mass,mu in product((60,70,80),(.15,.23,.30)):
        values=required(mass,ALPHA,mu,ARM)
        print('g, friction; required actual crown P service/table/fault',mass,mu,
              *(round(v,3) for v in values))
    for angle in (45,52,57.5,60,63):
        ph=radians(angle)
        print('angle; original vs wider 70g worst required',
              angle,*(round(max(required(70,ph,.23,-B*cos(ph),wide)),3)
                      for wide in (False,True)))
    print('take 23 larger lateral arm, 70g; draw requirements:',
          *(round(v,3) for v in required(70,ALPHA,MU,ARM,'take23')))
    for P in (40.,45.,50.,55.,60.):
        print('P; 70g wide minimum frictionless contact margin',
              P,round(min(margin(70,P,ALPHA,k) for k in ('service','table','fault')),3))
        N=P/(cos(PAD_ANGLE)-MU*sin(PAD_ANGLE))
        af,pf=hertz(N,CROWN_R)
        print('crown N, Hertz a, p0 MPa',round(N,3),round(af,3),round(pf,1))
        nx=cos(ALPHA+NORMAL_ERR)-MU*sin(ALPHA+NORMAL_ERR)
        upper=(P+5*.07*9.80665)/nx
        print('one outer reaction cap N; R5/flat, R5/R10 concave p0 MPa',round(upper,3),
              *(round(hertz(upper,r)[1],1) for r in (5.,10.)))


if __name__=='__main__': main()
