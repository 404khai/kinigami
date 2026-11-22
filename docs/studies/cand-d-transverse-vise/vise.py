"""Transverse vise study. x=docking, y=platen stroke, z=up. N and mm."""
from itertools import product
from math import atan, cos, floor, hypot, pi, radians, sin, sqrt, tan
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import linprog

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'cand-d-expanding-plug'))
from crown import envelope

X,Y,Z=np.eye(3)


def seats(R, angle, clock):
    faces=[]
    for i in range(3):
        th=clock+2*pi*i/3
        r=cos(th)*X+sin(th)*Z
        t=np.cross(Y,r)
        for side in (-1,1):
            n=cos(angle)*Y+side*sin(angle)*t
            faces.append((R*r,n))
    return faces


def wrench(p,f,R):
    return np.r_[f, np.cross(p,f)/R]


def closure(faces,R,P,e,mu,h,dth=.012,dp=.12,pad_offset=.12,tol=.8):
    # A sphere's normal passes through its centre. Use centre uncertainty,
    # not the arc distance to its surface, for normal-only support.
    J=np.array([wrench(p,n,R) for p,n in faces])
    H=np.linalg.inv(J.T)
    nom=H@wrench(h*Y,(P-tol)*Y,R)
    err=abs(H)@e
    C=np.empty((6,6))
    for k,row in enumerate(H):
        v,w=row[:3],row[3:]/R
        g=v+np.cross(w,h*Y)
        err[k]+=(P+tol)*(mu*np.linalg.norm(np.cross(g,Y))+
                        pad_offset*sqrt(1+mu**2)*np.linalg.norm(w))
        for j,(p,n) in enumerate(faces):
            u=v+np.cross(w,p)
            C[k,j]=(dth*np.linalg.norm(np.cross(n,u))+.5*dth**2*abs(u@n)+
                    dp*(np.linalg.norm(np.cross(w,n))+dth*np.linalg.norm(w)))
    assert max(abs(np.linalg.eigvals(C)))<1
    # Use the upper preload for the perturbation term. The nominal P column
    # is positive; the two endpoints bound its effect before perturbation.
    up=np.linalg.solve(np.eye(6)-C,abs(H@wrench(h*Y,(P+tol)*Y,R))+err)
    return nom-err-C@up,up


def missing(faces,R,ball,h,mu,top_mu,index,sides=24):
    # INSCRIBED polygon: feasible coefficients give an actual friction
    # witness in the nominal pose. Not a claim that the mechanism chooses it.
    cols=[]; forces=[]
    for j,(p,n) in enumerate([*faces,(h*Y,-Y)]):
        if j==index: continue
        if j<6: p=p-ball*n
        a=np.cross(n,X); a/=np.linalg.norm(a)
        b=np.cross(n,a)
        for k in range(sides):
            ang=2*pi*k/sides
            f=n+(mu if j<6 else top_mu)*(cos(ang)*a+sin(ang)*b)
            cols.append(np.r_[wrench(p,f,R),float(j==6)])
            forces.append(j)
    M=np.array(cols).T
    rhs=np.r_[np.zeros(6),1.]
    sol=linprog(np.ones(M.shape[1]),A_eq=M,b_eq=rhs,bounds=(0,None))
    if not sol.success: return None
    assert max(abs(M@sol.x-rhs))<1e-8 and min(sol.x)>-1e-8
    return np.bincount(forces,weights=sol.x,minlength=7)


def push(mass,R,angle,mu,pusher_mu,dx=0.):
    # One stationary slope in the xz plane; one non-graph opposing contact
    # invalidates this proof. Angle is a global normal-direction bound.
    # Fx/Fy <= tan(angle+atan(mu)) (projection of the full Coulomb cone).
    k=tan(angle+atan(mu))
    ky=tan(dx+atan(pusher_mu))  # |transverse force|/delivered axial push
    l=envelope(mass,'table',R,'take23')
    assert k*ky<1
    return (l[0]+k*l[1])/(1-k*ky),k*ky


def table_push(mass,angle,mu,table_mu,pusher_mu,dx):
    # A common translation tests *all* unknown contact forces, including
    # floor normal induced by the pusher. It is not a tail trajectory.
    k=tan(angle+atan(mu))
    if k*table_mu>=1: return None
    y=k*sqrt((1+table_mu**2)/(1-(k*table_mu)**2))
    z=table_mu*hypot(1.,y)
    vy=cos(angle+atan(mu))*y-sin(angle+atan(mu))*hypot(1.,z)
    assert abs(vy)<1e-10 and abs(z-table_mu*hypot(1.,y))<1e-10
    gain=1-tan(dx+atan(pusher_mu))*hypot(y,z)
    if gain<=0: return None
    w=mass*.001*9.80665
    # Allow the service 4W, W, W force box plus gravity W in z.
    return y,z,gain,w*(4+y+2*z)/gain


def vertical(mass,angle,mu,floor_mu,head_tilt,pusher_mu,dx):
    # +Y up at zero tilt. Certify a single local virtual translation
    # even when the opposing floor can develop an unknown normal load.
    k=max(tan(angle+atan(mu)),tan(head_tilt+atan(floor_mu)))
    gain=1-k*tan(dx+atan(pusher_mu))
    if gain<=0: return None
    # Weight may rotate relative to the head by head_tilt.
    grav=min(hypot(1,k),sin(head_tilt)+k)
    return mass*.001*9.80665*(4+k+grav)/gain


if __name__=='__main__':
    R=7.;angle=radians(35.);faces=seats(R,angle,pi)
    for mass in (50,70,90):
        for mu in (0.,.05,.15,.23):
            e=[envelope(mass,c,R,'take23') for c in ('service','table','fault')]
            # The threshold bound is affine for P>.8 with normal preload
            # at a fixed point. Verify the rounded-up sufficient value.
            a=np.hstack([closure(faces,R,2.,load,mu,3.5)[0] for load in e])
            b=np.hstack([closure(faces,R,3.,load,mu,3.5)[0] for load in e])-a
            ok=max(2,floor(2.+max(-a/b))+1) if min(b)>0 else None
            if ok is not None:
                assert min(min(closure(faces,R,ok,load,mu,3.5)[0]) for load in e)>0
            print('g / top shear ratio / sufficient preload (whole N)',mass,mu,ok)
        print('one-cheek fixed external wrench; N and feedback at 36 deg:',
              *push(mass,R,radians(36),.23,.23,radians(.5)))
        for deg in (36,51):
            for table_mu in (.3,.5,.6,.7,1.):
                a=table_push(mass,radians(deg),.23,table_mu,.23,radians(.5))
                print('angle, floor mu, z-up push N',deg,table_mu,
                      round(a[-1],3) if a else 'no certificate')
        print('51 deg lower-only, Y-up/15 deg attitude, table mu=1, push N',
              vertical(mass,radians(51),.23,1.,radians(15),.23,radians(.5)))
    for mu,top in product((.12,.18,.23,.30),(.0,.12,.23)):
        wit=missing(faces,R,3.,3.5,mu,top,0)
        print('zero external load; friction / top friction / missing-face witness:',
              mu,top, None if wit is None else np.round(wit,4))
