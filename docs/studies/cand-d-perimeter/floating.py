"""Take 71: one double-rocking seat plate, not three spring plungers (N, mm)."""
from itertools import combinations
from math import cos, hypot, radians, sin, sqrt

import numpy as np
from scipy.optimize import linprog
from fixed_face import BACK, BC, CLOCK, CX, MU, RAD, RIM, X, Y, Z, loads, setup


def system(xg,angle=56.,qx=.60):
    nseat=6
    p,n,J=setup(RAD,radians(angle),radians(CLOCK))
    A=np.zeros((9,9));A[:6,:6]=J
    P=list(p)
    for j in range(3):
        t=radians(CLOCK+60+120*j);r=cos(t)*Y+sin(t)*Z
        qr=sqrt(1-qx*qx);q=qx*X+qr*r;pt=(CX+BACK*qx-BC)*X+(RIM+BACK*qr)*r
        A[:6,6+j]=-np.r_[q,np.cross(pt,q)/RAD];P.append(pt)
    arms=np.array(P)/RAD;gr=arms[:nseat]+(BC-(BC if xg is None else xg))*X/RAD
    A[6,:6]=n[:,0]
    A[7:,:6]=(n if xg is None else np.cross(gr,n))[:,1:].T
    return A,arms,gr


def certificate(xg,case='table',mass=70.,angerr=.60,pos=.19,piv=.06,axerr=1.,tau=0.,angle=56.,qx=.60):
    """Largest common delivered spring S compatible with a first lost normal."""
    A,p,g=system(xg,angle,qx)
    dn=2*sin(radians(angerr)/2);dg=2*sin(radians(axerr)/2)
    # Frobenius debit over all 9 columns for motion of both contact lines
    # and of the two unit rotation axes. Translation rail axis stays X.
    dm=dn*np.linalg.norm(p,axis=1)+pos/RAD
    dm2=np.full(6,dn+dg) if xg is None else (dn+dg)*np.linalg.norm(g,axis=1)+(pos+piv)/RAD
    gap=np.linalg.svd(A,compute_uv=False)[-1]-sqrt(15*dn**2+dm@dm+2*(dm2@dm2))
    W=mass/70*loads(case)
    if gap<=0:return np.inf,gap
    E=np.linalg.inv(A)
    D=np.vstack((np.eye(9),E,*[E[i]+s*E[j] for i,j in combinations(range(9),2) for s in (-1,1)]))
    rows=[]
    for d in np.vstack((D,-D)):
        m=d[3:6];v=d[:3]+np.cross(m,p)
        a=d[7]*Y+d[8]*Z
        v[:6]+=d[6]*X+(a if xg is None else np.cross(a,g))
        er=dn*np.linalg.norm(v,axis=1)
        er[6:]+=pos/RAD*np.linalg.norm(m)
        # Both torque rows share the same displaced contact, not two
        # unrelated gaps. Axis errors remain independent and adverse.
        if xg is None:
            er[:6]+=pos*np.linalg.norm(m)/RAD+dg*sum(abs(d[7:]))
        else:
            er[:6]+=(pos*np.linalg.norm(m+a)+piv*np.linalg.norm(a))/RAD
            er[:6]+=dg*sum(abs(d[7:]))*(np.linalg.norm(g,axis=1)+(pos+piv)/RAD)
        rows.append(np.r_[d@A-er,-d])
    rows=np.array(rows);obj=np.zeros(18);obj[15]=-1
    aux=tau if xg is None else tau/RAD
    ext=np.r_[W,aux,aux]
    vals=[]
    for i in range(9):
        bounds=[(0,None)]*9+[(-w,w) for w in W]+[(0,None)]+[(-aux,aux)]*2
        bounds[i]=(0,0)
        res=linprog(obj,A_ub=rows,b_ub=np.zeros(len(rows)),bounds=bounds,method='highs')
        if res.status==3:return np.inf,gap
        assert res.success
        lm=np.maximum(0.,-res.ineqlin.marginals);c=lm@rows
        tol=1e-10*(1+lm@abs(rows));c[i]=tol[i]=0
        ws=min(0.,min((c-tol)[:6]));wj=min(0.,min((c-tol)[6:9]))
        ns=cos(radians(angle))-dn;nj=qx-dn
        scale=c[15]-tol[15]+ws/ns+wj/nj
        assert scale>0
        ix=[9,10,11,12,13,14,16,17]
        vals.append(((abs(c[ix])+tol[ix])@ext-wj*W[0]/nj)/scale)
    return max(vals),gap


if __name__=='__main__':
    for xg in (2.,0.,BC,-6.95,-8.,-10.,-18.,-22.):
        A,_,_=system(xg);E=np.linalg.inv(A)
        print('joint center / nominal clean / tolerance first-loss bound,rank reserve',
              xg,round(max(abs(E[:,:6])@loads('table')/E[:,6]),3),
              np.round(certificate(xg,tau=1.),4))
    for mass in (70.,110.,156.07):
        for aux in (0.,2.):
            print('non-tilting plate / mass / Y,Z spring or cable bias each / true axial S thresholds',
                  mass,aux,np.round([certificate(None,c,mass,tau=aux)[0]
                       for c in ('service','table','fault')],3))
