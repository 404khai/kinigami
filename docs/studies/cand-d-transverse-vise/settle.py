"""Sufficient no-rest test for a missing flank near the six design faces."""
from math import atan, cos, pi, radians, sin, sqrt
import numpy as np
from scipy.optimize import linprog
from vise import X,Y,Z,seats,wrench,envelope


def support(faces,R,ball,mu,dn,dp,db,sides=24):
    groups=[]
    k=mu/cos(pi/sides)
    for c,n in faces:
        a=np.cross(n,X);a/=np.linalg.norm(a)
        b=np.cross(n,a)
        fs=[n+k*(a*cos(th)+b*sin(th)) for th in np.arange(sides)*2*pi/sides]
        W=np.array([wrench(c-ball*n,f,R) for f in fs])
        e=np.r_[np.full(3,dn*sqrt(1+k*k)),
                [((dp+dn*np.linalg.norm(np.cross(c,i)))*sqrt(1+k*k)+
                 k*(ball*dn+db))/R for i in np.eye(3)]]
        groups.append((W,e))
    return groups


def limit(groups,R,h,mu,offset,load,missing):
    # Find a virtual twist that has no positive work on the remaining
    # faces. Require unit external-load work budget and maximise net
    # preload work. Its reciprocal is a sufficient preload at this pose.
    rows=[];rhs=[]
    for i,(W,e) in enumerate(groups):
        if i!=missing:
            rows.extend(np.c_[W,np.tile(e,(len(W),1)),np.zeros(len(W))])
            rhs.extend([0.]*len(W))
    for s in (-1,1):
        rows.extend(np.c_[s*np.eye(6),-np.eye(6),np.zeros(6)]);rhs.extend([0.]*6)
    rows.append(np.r_[np.zeros(6),load,0]);rhs.append(1.)
    k=mu/cos(pi/24)
    err=np.r_[np.zeros(3),np.full(3,offset*sqrt(1+k*k)/R)]
    for j in range(24):
        f=Y+k*(cos(j*2*pi/24)*X+sin(j*2*pi/24)*Z)
        rows.append(np.r_[-wrench(h*Y,f,R),err,1]);rhs.append(0.)
    rows=np.array(rows);rhs=np.array(rhs)
    ans=linprog(np.r_[np.zeros(12),-1.],A_ub=rows,b_ub=rhs,
                bounds=[(None,None)]*6+[(0,None)]*6+[(None,None)])
    if not ans.success or ans.x[-1]<1e-9: return float('inf')
    # Move toward an interior twist to cover LP roundoff on the faces.
    v=ans.x[:6].copy()
    bad=max(max(W@v)+e@abs(v) for i,(W,e) in enumerate(groups) if i!=missing)
    v0=np.r_[Y,np.zeros(3)]
    reserve=min(min(W@v0)-e@abs(v0) for W,e in groups)
    assert reserve>0
    v-=v0*max(0,bad+1e-9)/reserve
    assert max(max(W@v)+e@abs(v) for i,(W,e) in enumerate(groups) if i!=missing)<=0
    g=v[:3]+np.cross(v[3:]/R,h*Y)
    residual=g@Y-mu*np.linalg.norm(np.cross(Y,g))-err@abs(v)
    return abs(v)@load/residual if residual>0 else float('inf')


if __name__=='__main__':
    R=7.;faces=seats(R,radians(35),pi);h=3.5
    for mu in (.05,.1,.15,.18,.23):
        groups=support(faces,R,3.,mu,.012,.12,.015)
        for top in (0.,.04):
            corners=[max(limit(groups,R,h,top,.12,envelope(70,c,R,'take23'),i)
                         for i in range(6)) for c in ('service','table','fault')]
            print('lower/top friction, N above which every face must carry force:',mu,top,
                  *(round(x,3) for x in corners))
