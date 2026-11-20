"""Take 11: exploratory, quasi-static; dimensions mm,N,N mm. Python 3 + NumPy.
Intervals algebraically inflated; not a sweep of nominal poses. No candidate inputs changed.
"""
from math import cos, sin, pi, radians, hypot, sqrt, atan, degrees
from itertools import combinations
import numpy as np

R, BALL, MU = 4.65, 1.055, .23
# All center positions relative to a common translating, nonrotating origin.
# Includes manufacturing error, deflection and attitude departure while confined.
DC = .18
DA = radians(.5)
X,Y,Z = np.eye(3)
rad = np.array([cos(i*2*pi/3)*Y+sin(i*2*pi/3)*Z for i in range(3)])
tang = np.cross(X,rad)
centres = np.tile(rad,(2,1))
normals = np.vstack(([X]*3,tang))
B = np.concatenate((normals,np.cross(centres,normals)),axis=1).T
A = np.linalg.inv(B)
assert np.allclose(A[:3,:3],np.tile(X/3,(3,1)))
assert np.allclose(A[:3,3:],2*np.cross(rad,X)/3)
assert np.allclose(A[3:,:3],2*tang/3)
assert np.allclose(A[3:,3:],np.tile(X/3,(3,1)))

def matrix(angles=(DA,)*6,dc=DC):
    H = np.zeros((6,6))
    m = BALL/R
    for i,(u,v) in enumerate(zip(A[:,:3],A[:,3:])):
        vn=np.linalg.norm(v)
        for j,(c,n,angle) in enumerate(zip(centres,normals,angles)):
            g=u+np.cross(v,c); gn=np.linalg.norm(g); delta=2*sin(angle/2)
            # nominal-B preconditioning incl both signs and all sphere radii <= BALL.
            # Center-to-contact normal lever is parallel to n: zero normal couple.
            normal_err=gn*delta+vn*dc/R
            # Projection perturbation norm <= sin(angle); lever perturbation at
            # pole and projection of that lever each <= |v|*m*delta.
            slope=max(np.linalg.norm(np.cross(g+np.cross(v,s*m*n),n)) for s in (-1,1))
            H[i,j]=normal_err+MU*(slope+vn*dc/R+(gn+2*m*vn)*delta)+1e-12
    return H

def const_load(mass,kind,external=0.):
    W=mass*.001*9.80665
    F=4*W+external; S=W
    Tx=2*W*12.7; My=50.8*W; Mz=52.2 if kind=='fault' else 14.5
    if kind=='correction':   # optional adverse work to move body, not a mandatory snap
        Tx+=W*(12.7+2.42); Mz+=W*hypot(50.8,25.4); My+=W*(37.2-11.23)
        F+=W
    # Headed moments taken at mating ball-ring centre. Add origin transfer if loads specified elsewhere.
    return np.array(3*[F/3+2*hypot(My,Mz)/(3*R)]+3*[2*S/3+Tx/(3*R)])

def cert(H,b,mask):
    hh=H[np.ix_(mask,mask)]; eye=np.eye(len(mask))
    v=np.linalg.solve(eye-hh,np.ones(len(mask)))
    assert min(v)>0
    q=max((hh@v)/v)+1e-10  # positive Collatz-Wielandt upper bound, not just eigenvalues
    assert q<1
    x=np.linalg.solve(eye-hh,b[mask]+1e-9)
    assert min(x-hh@x-b[mask])>0
    return q,x

def exit_bound(mass):
    # Flared cheek or round end extruded radially: n=s*t*cos(beta)+X*sin(beta).
    # Each site may touch at most ONE tangential cheek, stage-wide. All keepers gone.
    # T=sum cos(beta) N, P=sum sin(beta) N + rear-seat normal sum.
    # Radial end corners NOT admitted. Real normals <= DA from these meridians.
    beta=2*sin(DA/2); d=DC/R
    # Sum over t-reciprocal rows at one centre: 1+2/sqrt(3).
    gsum=1+2/sqrt(3)
    kt=d
    # Meridional contact on a rounded exit can displace a centre in t by
    # (ball+edge radius), in addition to 0.18 mm local error. This shift
    # parallel to t makes no Mx from the nominal t normal, but does affect friction.
    shifted=d+(BALL+.10)/R
    k=(gsum+shifted)*beta+MU*(gsum+shifted+BALL/R)
    load=const_load(mass,'service')
    Dt=3*load[-1]
    F=5*mass*.001*9.80665  # 4W compression plus W table drag
    # T <= Dt + kt*T + k*(T+P); P <= F+mu*T+(1+mu)*beta*(T+P)
    a=(1+MU)*beta
    P0=F/(1-a); PT=(MU+a)/(1-a)
    q=kt+k*(1+PT)
    assert q<1
    T=(Dt+k*P0)/(1-q)
    P=P0+PT*T
    return q,T,P

if __name__=='__main__':
    np.set_printoptions(precision=4,suppress=True)
    H=matrix(); print('B direct reciprocal H =\n',H)
    print('H rho (nominal only)',max(abs(np.linalg.eigvals(matrix((0.,)*6,0)))))
    for mass in (46,50):
        for kind in ('service','correction','fault'):
            b=const_load(mass,kind); q,x=cert(H,b,list(range(6)))
            print(mass,kind,'component upper axial/tangent',x[0],x[3],'rho upper',q)
            for n in range(1,7):
                for ix in combinations(range(6),n):
                    _,sub=cert(H,b,list(ix))
                    assert np.all(sub<=x[list(ix)]+1e-8)
        print('cheek exit q,T,P',mass,exit_bound(mass))
    for a in (1,2,3,4,5,6,10,15):
        print('keeper normal tilt extra deg',a,'rho envelope',max(abs(np.linalg.eigvals(matrix((DA+radians(a),)*3+(DA,)*3)))))
