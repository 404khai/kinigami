"""Seated frictionless feasibility by separating each missing contact face.

The optimiser only proposes dual vectors. The reported sign is checked
using analytic support bounds on the full uncertainty sets.
"""
import numpy as np
from scipy.optimize import linprog
from tripod import R, integrated, matrix, envelope


def errgrad(gs,v,dn,dp,da):
    f,w=v[:3],v[3:6]/R
    res=[]
    def normgrad(a): return a/max(np.linalg.norm(a),1e-30)
    for contact,n,j,a in gs:
        p=contact-2.4*n if np.linalg.norm(a) else contact
        g=f+np.cross(w,p)+v[6+j]*a
        t=g-(g@n)*n
        dg=dn*normgrad(t)+.5*dn**2*np.sign(g@n)*n
        dw=np.cross(p,dg)+dp*(np.cross(normgrad(np.cross(n,w)),n)+dn*normgrad(w))
        ds=a@dg+da*np.linalg.norm(a)*np.sign(v[6+j])
        res.append(np.r_[dg,dw/R,ds*np.eye(3)[j]])
    return np.array(res)


def certificate(gs,missing,nom,err,dn=.012,dp=.30,da=.008):
    # v.W_i <= 0 (other contacts); v.W_j <= 1 for the reference.
    # That bounds v.b above by N_j for every nonnegative equilibrium.
    J=matrix(gs)
    target=np.eye(9)[missing]
    g=errgrad(gs,np.linalg.solve(J,target),dn,dp,da)
    rows=np.c_[J+g,np.zeros((9,9))]
    b=target.copy()
    for sg in (1.,-1.):
        rows=np.vstack((rows,np.c_[sg*np.eye(9),-np.eye(9)]))
        b=np.r_[b,np.zeros(9)]
    for _ in range(60):
        sol=linprog(np.r_[-nom,err],A_ub=rows,b_ub=b,
                    bounds=[(-100.,100.)]*9+[(0.,100.)]*9)
        if not sol.success: raise ValueError(sol.message)
        v=sol.x[:9]
        g=errgrad(gs,v,dn,dp,da)
        # Homogeneous norm supports; the error is the current subgradient.v.
        d=(J+g)@v-target
        if max(d)<2e-7: break
        i=np.flatnonzero(d>1e-7)
        rows=np.vstack((rows,np.c_[(J+g)[i],np.zeros((len(i),9))]))
        b=np.r_[b,target[i]]
    # Correct numerical feasibility by subtracting a separating force
    # whose inner product with EVERY possible contact is strictly positive.
    v0=np.r_[1.,np.zeros(5),[5.]*3]
    m=np.min((J-errgrad(gs,v0,dn,dp,da))@v0)
    assert m>.4
    v-=max(0.,max(d)+2e-9)/m*v0
    assert max((J+errgrad(gs,v,dn,dp,da))@v-target)<1e-9
    return v@nom-abs(v)@err


if __name__=='__main__':
    gs=integrated()
    for mass in (70.,90.,110.):
        for dn in (.012,.028,.04):
            f=30.
            err=np.r_[envelope(mass,'table',R,'take23'),[.8]*3]
            lo=min(certificate(gs,i,np.r_[np.zeros(6),[f]*3],err,dn) for i in range(9))
            print('g, normal chord, N/slide, table lower N',mass,dn,f,round(lo,4))
