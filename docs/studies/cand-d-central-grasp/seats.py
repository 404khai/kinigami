"""Exploratory sizing of the external six-contact face only, N, mm, N mm.

This does not bound the central gripper, certify the edge of the housing,
or substitute a frictionless equilibrium for an upper bearing load.
"""
from itertools import product
from math import cos, degrees, hypot, pi, radians, sin, sqrt, tan

import numpy as np

X, Y, Z = np.eye(3)
R, B, BERR = 6.30, 2., .015
ALPHA, ANGERR = radians(45), radians(.5)
MU = .23
V_END, ROOT, LIP = 1.84, .4, 2.
W = .05 * 9.80665
E = .060  # maximum manufactured signed contact residual at nominal pose
DC = .035  # manufactured ball-centre location error relative to tail frame
D = 2*sin(ANGERR/2)
RAD = [cos(a)*Y + sin(a)*Z for a in (pi/2, 7*pi/6, 11*pi/6)]
TAN = [np.cross(X,l) for l in RAD]


def seat_matrix():
    rows = []
    for l,t in zip(RAD,TAN):
        for s in [-1,1]:
            n = cos(ALPHA)*X+s*sin(ALPHA)*t
            rows.append(np.r_[n,np.cross(l,n)])
    return np.array(rows)


J = seat_matrix()
H = np.linalg.inv(J)


def rigid_fit(radius=.15):
    # u=(translation, R*rotation vector), Euclidean ball of given radius.
    # Actual residual is n.(translation + Q*v_i - v_i) + e at each flat.
    # Derivative of exp about any axis: ||Q-I|| <= a; operator that maps
    # delta rotation vector to angular velocity differs from I by <= a/2
    # (integrate a rotation over tau in [0,1]). Its norm is <= 1.
    a=radius/R
    de_rot=DC/R + (1+DC/R)*(1.5*a+D)
    gain=np.linalg.norm(H,2)*sqrt(6)*hypot(D,de_rot)
    offset=np.linalg.norm(H,2)*sqrt(6)*E
    assert gain<1 and offset+gain*radius<radius
    # Relative displacement of a centre: q and v correlated by ball norm.
    movement=DC+radius*hypot(1,1+DC/R)
    patch_shift=movement+BERR+(B+BERR)*D
    return gain,offset,degrees(a),movement,patch_shift


def face_geometry():
    return (ROOT*sin(ALPHA), V_END+LIP*sin(ALPHA),
            V_END*tan(ALPHA)+LIP*(1-cos(ALPHA)),
            B/cos(ALPHA), B*sin(ALPHA))


def min_normal(P,side,couple,kind):
    # About moving nominal centre of the tail triangle. Axial pull applied
    # through this origin. Every gripper eccentricity/moment, including
    # arm x lateral force, goes in 'couple' (a norm, not each component).
    radius=.15
    dn=D
    dl=DC/R+radius/R*(1+DC/R)
    dm=dl+dn  # l' x n' - l x n, with unit n'
    fx=4*W
    loads=np.r_[fx,W,W,25.4*W/R,50.8*W/R,(52.2 if kind=='fault' else 14.5)/R]
    if kind=='table':
        loads+=np.r_[W,0,0,W*(12.7+2.42)/R,W*(37.2-11.23)/R,W*hypot(50.8,25.4)/R]
    out=[]
    for d in H.T:
        # At the first zero along a continuous geometry perturbation,
        # sum N <= (P+|Fx|)/minimum axial normal, by x balance.
        margin=d[0]*P-np.abs(d)@loads
        margin-=np.linalg.norm(d[1:3])*side+np.linalg.norm(d[3:])*couple/R
        margin-=(np.linalg.norm(d[:3])*dn+np.linalg.norm(d[3:])*dm)*(P+loads[0])/cos(ALPHA+ANGERR)
        out.append(margin)
    return min(out)


def need_pull(side,couple,kind):
    f=min_normal(0,side,couple,kind)
    return -f/(min_normal(1,side,couple,kind)-f)


def sphere_flat(N,b):
    # Steel/steel, E=210 GPa, nu=.30; static Hertz, untruncated patch.
    Estar=210000/(2*(1-.3**2))
    a=(3*N*b/(4*Estar))**(1/3)
    return a,3*N/(2*pi*a*a)


def main():
    print('fit: gain, nominal residual correction, angle deg, centre/patch motion mm',rigid_fit())
    root,outer,level,xc,tc=face_geometry()
    print('root/outer t, plateau x, seated centre x, working t',root,outer,level,xc,tc)
    assert outer < 4.*sin(pi/3)
    assert xc-B > ROOT*(1/cos(ALPHA)-1)
    # Closed contact geometry: all six flat normals span wrenches. A
    # strictly positive frictionless equilibrium precludes a first-order
    # escape under these forces at this pose; not an assembly proof.
    assert np.linalg.matrix_rank(J)==6
    print('minimum axial draw for positive virtual-work test; no friction credit')
    for side,couple in [(0.,0.),(1.,4.),(2.,10.),(5.,25.)]:
        print('parasitics N/Nmm',side,couple,
              {k:round(need_pull(side,couple,k),3) for k in ['service','table','fault']})
    # ALL equilibria, any contact subset, not just positive frictionless one:
    # x component >= cos(alpha)-mu sin(alpha), independent of pose as long
    # as it is on one of the qualified ruled faces/rounded transitions.
    kx=cos(ALPHA+ANGERR)-MU*sin(ALPHA+ANGERR)
    cap=(35+5*W)/kx
    a,p=sphere_flat(cap,B-BERR)
    usable=V_END-tc-rigid_fit()[-1]
    print('axial force / normal >=',kx,'one normal upper',cap,
          'flat Hertz halfwidth, MPa',a,p,'available flat halfwidth',usable)
    assert usable>a
    print('NOTE: lip is NOT flat. Flat stress and seated equilibrium are not release bounds.')


if __name__=='__main__':
    main()
