"""Bound individual loads while all reachable fixed supports are the six V lands.

Dual inequalities, N and mm. Not a release model; check every inequality on
the returned certificate. No positive minimum force or equal sharing assumed.
"""
from itertools import product
from math import atan, cos, pi, sin, tan

import numpy as np
from scipy.optimize import linprog

from crown import (ALPHA, ARM, AXIAL, B, LATERAL, MU, NORMAL_ERR,
                   PAD_ANGLE, R, RET_MOM, RET_SIDE, SHIFT, X, Y, Z, envelope, hertz)


def contacts(mu=MU, nphi=16, radius=R):
    groups=[]
    # Each true Coulomb disk is contained in the circumscribed polygon.
    for i,sign in product(range(3),(-1,1)):
        phase=2*pi*i/3
        l=Y*cos(phase)+Z*sin(phase)
        t=np.cross(X,l)
        n=X*cos(ALPHA)+sign*t*sin(ALPHA)
        v=np.cross(n,l)
        k=mu/cos(pi/nphi)
        forces=[n+k*(l*cos(p*2*pi/nphi)+v*sin(p*2*pi/nphi)) for p in range(nphi)]
        pos=l-B/radius*n
        groups.append(np.array([np.r_[f,np.cross(pos,f)] for f in forces]))
    # Nominal centre sphere radius, normal-angle error, centre uncertainty
    # and a finite outer contact patch. All are installed qualification inputs.
    dn=2*sin(NORMAL_ERR/2)
    fn=(1+k*k)**.5
    dp=(SHIFT+.015+(B+.015)*dn+.22)/radius
    err=fn*np.r_[np.full(3,dn),np.full(3,dp+(1+B/radius)*dn)]
    return groups,err


def draw_loads(pmin,pmax,mu=MU,nphi=12,radius=R):
    # Return wrench acting AGAINST the fixed face supports. Crown gets
    # its own P in each vertex. No independent huge side/couple boxes.
    k=tan(PAD_ANGLE+atan(mu))/cos(pi/nphi)
    w=[]
    for P,ax,y,z in product((pmin,pmax),(ARM-AXIAL,ARM+AXIAL),
                            (-LATERAL,LATERAL),(-LATERAL,LATERAL)):
        pos=np.array([ax,y,z])/radius
        for i in range(nphi):
            F=P*(X+k*(Y*cos(i*2*pi/nphi)+Z*sin(i*2*pi/nphi)))
            w.append(np.r_[F,np.cross(pos,F)])
    return np.array(w)


def certificate(focus,loads,draw,groups,err):
    # v, |v|, maximum of v dot the draw wrench.
    a=[];b=[]
    for i,ws in enumerate(groups):
        a.extend(np.c_[-ws,np.tile(err,(len(ws),1)),np.zeros(len(ws))])
        b.extend([-float(i==focus)-1e-6]*len(ws))
    for sign in (-1,1):
        a.extend(np.c_[sign*np.eye(6),-np.eye(6),np.zeros(6)]);b.extend([0]*6)
    a.extend(np.c_[draw,np.zeros_like(draw),-np.ones(len(draw))])
    b.extend([0]*len(draw))
    a,b=np.array(a),np.array(b)
    c=np.r_[np.zeros(6),loads,1.]
    opt=linprog(c,A_ub=a,b_ub=b,bounds=[(None,None)]*6+[(0,None)]*6+[(None,None)],
                method='highs')
    assert opt.success
    # Recheck the actual support bound, not just the solver status.
    v=opt.x[:6]
    assert all(min(ws@v)-err@abs(v)>=float(i==focus) for i,ws in enumerate(groups))
    return max(draw@v)+loads@abs(v)


def main():
    G,e=contacts()
    for Plo,Phi in [(50.,55.),(45.,50.)]:
        D=draw_loads(Plo,Phi)
        for case in ('service','table','fault'):
            ext=envelope(70,case,wide='take23')+np.r_[0.,RET_SIDE,RET_SIDE,np.full(3,RET_MOM/R)]
            bound=max(certificate(i,ext,D,G,e) for i in range(6))
            print(Plo,Phi,case,'largest one face N, R5/flat and R5/R10 a,p0',
                  round(bound,3),*(tuple(round(x,4) for x in hertz(bound,r)) for r in (5,10)))


if __name__=='__main__':main()
