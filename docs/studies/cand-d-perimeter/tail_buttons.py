"""Take 63 comparison: spring-backed axial buttons in the passive tail, not in the jaws."""
from itertools import combinations
from math import cos, radians, sin, sqrt
import numpy as np
from scipy.optimize import linprog
from fixed_face import ANG, BACK, BC, CLOCK, CX, QX, RAD, RIM, X, Y, Z, loads, setup


def bound(qx,phase,scatter,case,face_error=.6,pos=.19):
    """Relax first loss of a positive virtual reaction to a linear feasibility problem."""
    p,n,J=setup(RAD,radians(ANG),radians(CLOCK))
    qr=sqrt(1-qx*qx); A=np.zeros((9,9));A[:6,:6]=J
    ds=np.zeros((9,3)); po=[]
    for i in range(3):
        theta=radians(CLOCK+phase+120*i);r=cos(theta)*Y+sin(theta)*Z
        q=qx*X+qr*r
        cp=(CX+BACK*qx-BC)*X+(RIM+BACK*qr)*r
        po.append(cp)
        A[:6,6+i]=-np.r_[q,np.cross(cp,q)/RAD]
        A[6+i,2*i:2*i+2]=cos(radians(ANG))
        ds[2*i:2*i+2,i]=1.
    pp=np.concatenate((p,np.array(po)))
    dn=2*sin(radians(face_error)/2)
    dm=dn*np.linalg.norm(pp,axis=1)/RAD+pos/RAD
    assert np.linalg.svd(A,compute_uv=False)[-1]>sqrt(sum(dm*dm)+15*dn*dn)
    E=np.linalg.inv(A); es=np.eye(9)
    dirs=np.vstack((es,E,*[E[i]+sign*E[j] for i,j in combinations(range(9),2) for sign in (-1,1)]))
    dirs=np.vstack((dirs,-dirs))
    # Variables y[9] >=0, b = [-external wrench normalized; S_i], nominal S.
    # The virtual force n' is unit. Combine its uncertainty across BOTH
    # force balance and spring balance before taking the norm.
    arms=pp/RAD
    U=[]
    for d in dirs:
        v=d[:3]+np.cross(d[3:6],arms)
        v[:6]+=(ds@d[6:])[:6,None]*X
        er=dn*np.linalg.norm(v,axis=1)+pos/RAD*np.linalg.norm(d[3:6])
        U.append(np.r_[d@A-er,-d,0])
    for i in range(3):
        for s in (-1,1):
            v=np.zeros(19); v[15+i]=s;v[-1]=-s-scatter
            U.append(v)
    vals=[];w=loads(case)
    for i in range(9):
        bounds=[(0,None)]*9+[(-a,a) for a in w]+[(0,None)]*4
        bounds[i]=(0,0)
        rows=np.array(U)
        res=linprog(np.r_[np.zeros(18),-1.],A_ub=rows,b_ub=np.zeros(len(U)),bounds=bounds,method='highs')
        if res.status==3: vals.append(np.inf);continue
        assert res.success
        # Proof by a nonnegative combination of necessary rows. For a true
        # first-loss case, all other virtual reactions are nonnegative and
        # the axial-balance sums bound any adverse dual residual.
        lm=np.maximum(0.,-res.ineqlin.marginals)
        co=lm@rows
        tol=1e-10*(1+lm@abs(rows))
        co[i]=tol[i]=0
        ws=min(0.,min((co-tol)[:6])); wj=min(0.,min((co-tol)[6:9]))
        qs=cos(radians(ANG))-dn; qj=qx-dn
        scale=(co[-1]-tol[-1]+(1+scatter)*(np.minimum(0,(co-tol)[15:18]).sum()+3*(ws/qs+wj/qj)))
        assert scale>0
        upper=((abs(co[9:15])+tol[9:15])@w-wj*w[0]/qj)/scale
        assert upper>=-res.fun-1e-5
        vals.append(upper)
    return max(vals)


if __name__=='__main__':
    for q in (QX,.50,.55,.60,.72,.80):
        for scatter in (.05,.10):
            vals=[bound(q,60.,scatter,c) for c in ('service','table','fault')]
            print('jaw nx / button scatter / nominal axial force above (N)',round(q,5),scatter,np.round(vals,2))
