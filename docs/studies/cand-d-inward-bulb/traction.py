"""Upper bounds on total normal reaction; full circular Coulomb cones.

A dual vector supplies rigid-body linear/angular virtual velocities and
one actuator virtual speed per site. For a unit normal reaction the
least virtual work over the friction disk is n.g - mu*|P_n g + b*Kxn|.
K contains both the virtual body rotation and the solid nose rotation.
"""
import numpy as np
from scipy.optimize import linprog
from crank import geometry, envelope, R, b, bh


def maps(gs,axes,mu,dn,dp=.30,da=.012,L=18.):
    costs=[]; J=[]
    for (p,n,i,a),axis in zip(gs,axes):
        B=b if np.linalg.norm(a) else 0.
        c=p-B*n
        def fields(v):
            f,w,s=v[:3],v[3:6]/R,v[6+i]
            g=f+np.cross(w,c)+s*a
            t=g-(g@n)*n
            K=w+s*axis/L
            dA=da*np.linalg.norm(a)
            dK=np.linalg.norm(a)*(.008/(L-.05)+.05/(L*(L-.05)))
            return g@n,[mu*(t+B*np.cross(K,n)), dn*t, .5*dn*dn*np.array([g@n]),
                        dp*np.cross(w,n), dp*(dn+mu)*w, np.array([(1.+mu)*dA*s]),
                        mu*dn*g,mu*(B*dn+.01*bool(B))*K,np.array([mu*bh*dK*s])]
        terms=[fields(v) for v in np.eye(9)]
        J.append([z[0] for z in terms])
        costs.append([np.array(a) for a in zip(*(z[1] for z in terms))])
    return np.array(J),costs


def penalty(costs,v):
    # Return a subgradient of the sum of norms; value is grad.v.
    def d(A):
        x=v@A
        return A@(x/max(np.linalg.norm(x),1e-30))
    return np.array([sum(d(A) for A in k) for k in costs])


def upper(J,costs,nom,err,target):
    lower=J-penalty(costs,np.linalg.solve(J,target))
    rows=np.c_[-lower,np.zeros((9,9))]
    rhs=-target.copy()
    for sg in (1.,-1.):
        rows=np.vstack((rows,np.c_[sg*np.eye(9),-np.eye(9)]))
        rhs=np.r_[rhs,np.zeros(9)]
    for _ in range(50):
        sol=linprog(np.r_[nom,err],A_ub=rows,b_ub=rhs,bounds=[(-200.,200.)]*9+[(0.,200.)]*9)
        if not sol.success: return float('inf')
        v=sol.x[:9].copy()
        lower=J-penalty(costs,v)
        d=target-lower@v
        if max(d)<2e-7: break
        idx=np.flatnonzero(d>1e-7)
        rows=np.vstack((rows,np.c_[-lower[idx],np.zeros((len(idx),9))]))
        rhs=np.r_[rhs,-target[idx]]
    v0=np.r_[1.,np.zeros(5),[5.]*3]
    slack=min((J-penalty(costs,v0))@v0)
    if slack<=0: return float('inf')
    v+=max(0.,max(d)+2e-9)/slack*v0
    assert min((J-penalty(costs,v))@v-target)>-1e-9
    return v@nom+err@abs(v)


if __name__=='__main__':
    gs,axes=geometry()
    for mass,dn,F in ((70.,.012,30.),(90.,.028,32.),(110.,.028,35.)):
        J,costs=maps(gs,axes,.23,dn)
        nom=np.r_[np.zeros(6),np.full(3,F)]
        for case in ('service','table','fault'):
            err=np.r_[envelope(mass,case,R,'take23'),[.8]*3]
            t=np.eye(9)
            cap=[upper(J,costs,nom,err,j) for j in list(t)+list(t[1::3]+t[2::3])]
            print('g,case,max rear,individual V,same shoe sum:',mass,case,
                  *(round(max(a),3) for a in (cap[:9:3],np.delete(cap[:9],[0,3,6]),cap[9:])))
