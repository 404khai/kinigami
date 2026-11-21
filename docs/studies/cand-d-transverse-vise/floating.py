"""Small-displacement coupon: tangentially compliant contacts, not a declaration.

Fixed normals and poles, quasistatic loading, known *individual* initial
normal/shear bands at a measured seated reference. No beneficial friction.
"""
from itertools import product
from math import cos, pi, radians, sqrt
import numpy as np
from vise import seats,wrench,envelope,X,Y

R=7.
DIR=np.array(list(product((-1.,1.),repeat=6))).T


def basis():
    normal=[];tangent=[]
    for i,(p,n) in enumerate([*seats(R,radians(35),pi),(-4.5*Y,-Y)]):
        p=p-(3 if i<6 else 8)*n
        a=np.cross(n,X);a/=np.linalg.norm(a)
        normal.append(wrench(p,n,R))
        tangent.append([wrench(p,a,R),wrench(p,np.cross(n,a),R)])
    return np.array(normal),np.array(tangent)


def gain(mass,kn,kt,initial_shear):
    J,G=basis()
    loads=np.hstack([envelope(mass,mode,R,'take23')[:,None]*DIR
                     for mode in ('service','table','fault')])
    g=np.zeros((7,7));g0=np.zeros(7)
    m=g.copy();m0=g0.copy()
    qg=np.zeros((6,7));q0=np.zeros(6)
    for k in product(*kn):
        D=np.array(k)[:,None]*J
        H=np.linalg.inv(J.T@D)
        # Each scalar output with all but one stiffness fixed is affine /
        # affine with positive denominator (rank-one matrix update). This
        # also holds for k_i J_i H. Norms of these interpolants attain a
        # maximum at an endpoint, so the 128 corners enclose all secants.
        GH=G@H
        g0=np.maximum(g0,np.max(np.linalg.norm(GH@loads,axis=1),axis=1))
        g=np.maximum(g,np.linalg.norm(np.einsum('aik,bjk->abij',GH,G),
                                      ord=2,axis=(2,3)))
        m0=np.maximum(m0,abs(D@H@loads).max(axis=1))
        m=np.maximum(m,np.linalg.norm(np.einsum('ak,bik->abi',D@H,G),axis=2))
        q0=np.maximum(q0,abs(H@loads).max(axis=1))
        qg=np.maximum(qg,np.linalg.norm(np.einsum('ak,bik->abi',H,G),axis=2))
    # Linear, isotropic series tangential spring and Coulomb slider.
    # e=u-s, ds=lambda*e dt, lambda>=0. s(t) lies in the convex hull of
    # s(0) and all past u. For |u|<=U, |de|<=2U+|e0|, including changing
    # friction or slip direction. Reference forces are subtracted once.
    A=g*(2*kt)
    rho=max(abs(np.linalg.eigvals(A)))
    if rho>=1:return rho,None
    U=np.linalg.solve(np.eye(7)-A,g0+g@initial_shear)
    shear=2*kt*U+initial_shear
    assert min(U)>=0 and np.max(abs(g0+g@shear-U))<1e-10
    return rho,(U,m0+m@shear,q0+qg@shear,shear)


def trial(ktl,ktt,mass=70):
    kn=[(2800.,7800.)]*6+[(3200.,7800.)]
    rho,result=gain(mass,kn,np.array([ktl]*6+[ktt]),
                     np.array([.4]*6+[.5]))
    print('lower/top tangential stiffness N/mm, feedback',ktl,ktt,round(rho,4))
    if result is not None:
        U,dN,q,df=result
        print('  max lower/top relative tangent motion mm',round(max(U[:6]),5),
              round(U[6],5),'lower/top normal change N',round(max(dN[:6]),2),
              round(dN[6],2),'centre components mm; R*rotation components mm',q.round(5))
    return rho,result


if __name__=='__main__':
    for lk,tk in [(0.,0.),(20.,40.),(60.,80.),(120.,140.),(350.,350.)]:
        trial(lk,tk)
