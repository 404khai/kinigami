"""Three measured button forces, six rearward flanks and three forward pads.
Exploratory ideal statics; units N, mm. No outer face or axial draw cartridge.
"""
from math import cos, pi, sin
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'cand-d-expanding-plug'))
from crown import X,Y,Z,envelope
from mushroom import O, alpha, beta, f, gamma, rr, xr

R=10.


def geometry(gamma, rear, xb, rb, phi, beta, rear_angle=0., skew=0., xr=-7.):
    contacts=[]
    for i in range(3):
        theta=2*pi*i/3
        r=cos(theta)*Y+sin(theta)*Z
        t=np.cross(X,r)
        p=xr*X+rear*(r*cos(skew)+t*sin(skew))
        n=cos(rear_angle)*X-sin(rear_angle)*(r*cos(skew)+t*sin(skew))
        contacts.append((p,n, i, 0*r))
        p=xb*X+rb*r
        a=sin(phi)*X-cos(phi)*r
        for sign in (-1,1):
            n=cos(gamma)*(-sin(beta)*X-cos(beta)*r)+sign*sin(gamma)*t
            contacts.append((p+2.4*n,n,i,a))
    return contacts


def integrated():
    return geometry(gamma, rr, O[0], O[1], f, beta, -alpha, pi/3, xr)


def matrix(gs):
    return np.array([np.r_[n,np.cross(p,n)/R,(a@n)*np.eye(3)[i]]
                    for p,n,i,a in gs])


def reciprocal(gs,F,load,tol=.8,dn=.012,dp=.30,da=.008):
    J=matrix(gs)
    H=np.linalg.inv(J.T)
    C=np.zeros((9,9))
    for i,h in enumerate(H):
        v,w=h[:3],h[3:6]/R
        for j,(p,n,s,a) in enumerate(gs):
            # The flank's normal passes through the sphere centre. Its
            # tangential traction is treated separately in friction.py.
            p=p-(2.4*n if np.linalg.norm(a) else 0)
            g=v+np.cross(w,p)+h[6+s]*a
            C[i,j]=(np.linalg.norm(np.cross(n,g))*dn+abs(g@n)*dn**2/2+
                    dp*(np.linalg.norm(np.cross(w,n))+np.linalg.norm(w)*dn)+
                    abs(h[6+s])*np.linalg.norm(a)*da)
    # Spectral-radius comparison bounds absolute values, without assuming
    # positivity or simultaneous sharing; it also excludes rank loss.
    assert max(abs(np.linalg.eigvals(C)))<1
    nom=H@np.r_[np.zeros(6),np.full(3,F)]
    err=abs(H)@np.r_[load,np.full(3,tol)]
    u=np.linalg.solve(np.eye(9)-C,abs(nom)+err)
    return nom-err-C@u,u


def required(gs,load,tol=.8,hi=100.):
    lo=0.
    if min(reciprocal(gs,hi,load,tol)[0])<=0:
        return None
    for _ in range(24):
        mid=(lo+hi)/2
        if min(reciprocal(gs,mid,load,tol)[0])>0:
            hi=mid
        else:
            lo=mid
    return hi


if __name__=='__main__':
    gs=integrated()
    for mass in (60,70,80):
        for case in ('service','table','fault'):
            load=envelope(mass,case,R,'take23')
            req=required(gs,load)
            low,up=reciprocal(gs,30.,load)
            print(mass,case,'required per-slide effort N; frictionless lower/upper at 30±.8 N:',
                  round(req,3) if req is not None else '>100',
                  round(min(low),3),round(max(up),3))
