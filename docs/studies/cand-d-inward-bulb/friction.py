"""Cone upper bounds when seated, with contact subsets allowed."""
from math import cos, hypot, pi, radians, sin

import numpy as np
from scipy.optimize import linprog
from tripod import X,R,integrated,envelope


def vertices(geom,mu=.23,dp=.30,dn=.012,da=.008,nv=16):
    groups=[]
    k=mu/cos(pi/nv)
    fn=hypot(1,k)
    for p,n,i,a in geom:
        t=np.cross(X,n);t/=np.linalg.norm(t)
        v=np.cross(n,t)
        cols=[]
        for j in range(nv):
            f=n+k*(t*cos(2*pi*j/nv)+v*sin(2*pi*j/nv))
            cols.append(np.r_[f,np.cross(p,f)/R,(a@f)*np.eye(3)[i]])
        err=fn*np.r_[np.full(3,dn),np.full(3,(dp+np.linalg.norm(p)*dn)/R),
                     (dn+da)*np.linalg.norm(a)*np.eye(3)[i]]
        groups.append((np.array(cols),err))
    return groups


def dual(groups,nom,err,target):
    a=[]; b=[]
    for (ws,e),s in zip(groups,target):
        a.extend(np.c_[-ws,np.tile(e,(len(ws),1))]);b.extend([-s-1e-6]*len(ws))
    for sg in (1,-1):
        a.extend(np.c_[sg*np.eye(9),-np.eye(9)]);b.extend(np.zeros(9))
    res=linprog(np.r_[nom,err],A_ub=a,b_ub=b,bounds=[(None,None)]*9+[(0,None)]*9)
    if not res.success: return float('inf')
    v=res.x[:9]
    assert all(min(ws@v)-e@abs(v)>=s-2e-10 for (ws,e),s in zip(groups,target))
    return v@nom+abs(v)@err


def screen(geom,mu=.23,force=28.,mass=70):
    groups=vertices(geom,mu)
    nom=np.r_[np.zeros(6),np.full(3,force)]
    for case in ('service','table','fault'):
        err=np.r_[envelope(mass,case,R,'take23'),np.full(3,.8)]
        caps=np.array([dual(groups,nom,err,t) for t in np.eye(9)])
        lows=np.array([-dual(groups,nom,err,-t) for t in np.eye(9)])
        print(case,'lower',*(round(min(q),2) for q in (lows[::3],np.delete(lows,[0,3,6]))),
              'upper',*(round(max(q),2) for q in (caps[::3],np.delete(caps,[0,3,6]))))


def missing_rear_witness(gs):
    # Inscribed (not circumscribed) polygons: an admissible one-pad-unloaded
    # force state at the exact nominal geometry, ignoring no contact drag.
    nv=16
    groups=vertices(gs,.23*cos(pi/nv),dp=0.,dn=0.,da=0.,nv=nv)
    A=np.vstack([ws for ws,_ in groups[1:]]).T
    b=np.r_[np.zeros(6),np.full(3,30.)]
    result=linprog(np.ones(A.shape[1]),A_eq=A,b_eq=b)
    assert result.success and min(result.x)>=-1e-10
    assert np.linalg.norm(A@result.x-b)<1e-7
    return np.r_[0.,result.x.reshape(-1,nv).sum(axis=1)]


if __name__=='__main__':
    gs=integrated()
    screen(gs,force=32.)
    print('exact 30 N/slide nominal wrench witness with rear pad 0 unloaded:',
          *np.round(missing_rear_witness(gs),3))
