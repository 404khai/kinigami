"""Take 81 finite contact patches, local containment and statics (mm, N, N mm)."""
from itertools import combinations
import json
from math import *
import numpy as np
from scipy.optimize import linprog
import take80 as b

ex=np.eye(3)[0]
p,n=b.build_contacts()
c=p.copy()
c[:6]+=1.5*n[:6]; c[6:]-=1.5*n[6:]
r=np.linalg.norm(c,axis=1)
def closure(extra):
    beta=radians(1.2); H=.25
    delta=np.radians([.6]*6+[1]*3)
    E=np.array([.025]*6+[.040]*3); E[0]+=extra
    A=np.c_[n,np.cross(c,n)/8.2]
    # The last three faces rotate with tail: scalar gap uses R^T d where
    # d=t+(R-I)c. Its difference from d is <= 2sin(beta/2)H.
    e=E+2*np.sin(delta/2)*H+(1-cos(beta))*r
    e[6:]+=2*sin(beta/2)*H
    v=[]
    for ix in combinations(range(9),6):
        a=A[list(ix)]
        if abs(np.linalg.det(a))<1e-8:continue
        u=np.linalg.solve(a,-e[list(ix)])
        if min(A@u+e)>-1.e-9:v.append(u)
    t=max(np.linalg.norm(z[:3]) for z in v)
    th=asin(max(np.linalg.norm(z[3:]) for z in v)/8.2)
    disp=np.max([np.linalg.norm(z[:3]+np.cross(z[3:]/8.2,c),axis=1) for z in v],axis=0)+(1-cos(th))*r
    assert th<beta and max(disp)<H
    # End of tilted cylindrical generator relative to footprint center.
    # Tilt is for tail vs head; possible roller fixture angular errors extra.
    S=max(disp[:6])+1.5*sin(radians(.6))+.025 # station/flat registration allocation
    J=max(disp[6:])+2*1.5*sin((th+radians(1))/2)+.025
    # sphere secant center witness vs finite cylinder contact; endpoint shift
    # in slope direction from tilt/skew. Jammed axis can skew additionally.
    skew=radians(1.20)
    J+=1.5*sin(th+radians(1)+skew)
    da=J/sqrt(2)
    return dict(vertices=len(v),translation=t,angle_deg=degrees(th),center_disp=disp.tolist(),
                V_usable_edge_reserve=.45-.06-S,
                V_radial_reserve=.58-.06-S,roller_slope_reserve=(3.85-3.20)*sqrt(2)-J-.06,
                roller_transverse_reserve=min(1.90,sqrt(4.60**2-(3.85+da)**2))-1.50-J-.06,
                center_H_reserve=H-max(disp),S=S,J=J)
def reactions():
    # Fully seated realization with .02 sleeve clearance taken up.
    pts=p.copy()
    for j in range(6,9):
        er=-(n[j]+ex/sqrt(2))*sqrt(2)
        pts[j]+=.02*(er-ex)
    out={}
    for mode,mu in [('normal',0),('dry_inner',.23),('dry_outer',.23/cos(pi/16))]:
        D=[]; F=[]; T=[]; ids=[]
        for i,(q,N) in enumerate(zip(pts,n)):
            h=np.cross(N,ex); h/=np.linalg.norm(h); k=np.cross(N,h)
            for a in np.arange(16 if mu else 1)*2*pi/16:
                f=N+mu*(h*cos(a)+k*sin(a))
                D.append(np.r_[f,np.cross(q,f)]); ids.append(i); T.append(-f[0] if i>=6 else 0)
                F.append(f)
        A=np.array(D).T; T=np.array(T); ids=np.array(ids); F=np.array(F)
        def lp(bounds,drop,obj,exact=False):
            lo,hi=bounds
            R=linprog(obj,A_ub=np.vstack((A,-A,T)),b_ub=np.r_[-lo,hi,45.],
                A_eq=[T] if exact else None,b_eq=[45] if exact else None,
                bounds=[(0,0 if i==drop else None) for i in ids],method='highs')
            return R
        cases={k:(np.r_[v[0],-np.array(v[2:])],np.r_[v[1],v[2:]]) for k,v in b.BOXES.items()}
        cases.update({k:(np.array(w),np.array(w)) for k,w in [('zero',[0]*6),('tension',[4*b.W]+[0]*5),('compression',[-20]+[0]*5),('moment',[0]*5+[52.2])]})
        out[mode]={}
        for name,box in cases.items():
            for drop in (-1,0):
                peaks=[]
                for j in (6,7,8):
                    R=lp(box,drop,-(ids==j).astype(float))
                    if R.success:peaks.append(-R.fun)
                out[mode][name+('_recess_face0' if drop==0 else '_all_available')]=max(peaks,default=None)
        R=lp(cases['zero'],0,-(ids==6).astype(float),True)
        if R.success:
            out[mode]['zero_recess_45N_witness']={'normal':[sum(R.x[ids==j]) for j in range(9)],'contact_forces':[(F[ids==j].T@R.x[ids==j]).tolist() for j in range(9)],'residual':max(abs(A@R.x))}
    return out
def frozen_box():
    A=np.r_[n.T,np.cross(p,n).T]; v=b.BOXES['table']
    lo=np.r_[v[0],-np.array(v[2:])];hi=np.r_[v[1],v[2:]]
    R=linprog(-np.eye(9)[6],A_ub=np.vstack([A,-A,np.r_[[0]*6,[2**-.5]*3]]),
       b_ub=np.r_[-lo,hi,45],method='highs')
    return dict(max_single_N=-R.fun,w=(-A@R.x).tolist(),normals=R.x.tolist())
if __name__=='__main__': print(json.dumps({'label':'exploratory','closure_nominal':closure(0),'extra_recess_020':closure(.020),'retention':reactions(),'frozen_table_noncorner':frozen_box()},indent=2))
