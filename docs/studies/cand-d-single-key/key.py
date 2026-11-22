"""Seven poles on three rigid balls and one tapered transverse key. mm, N."""
from math import *
import numpy as np
from scipy.optimize import linprog
from numpy.linalg import norm,solve
R=2.50;BR=10.30;BC=-3.20;QX=-5.90;ANG=radians(18);V=radians(56);MU=.23
E=np.array([1.,0.,0.]);Y=np.array([0.,1.,0.])
def model(a=ANG,v=V,phase=0.,ecc=None):
    # retaining load intersects face triangle at y=ecc (default: axis).
    qy=(0 if ecc is None else ecc)-(BC-QX)*tan(a)
    Q=np.array([QX,qy,0.]);n0=np.array([-cos(a),-sin(a),0.])
    n=[n0];p=[Q-R*n0];C=[Q]
    for i in range(3):
        k=phase+2*pi*i/3
        b=np.array([BC,BR*cos(k),BR*sin(k)])
        t=np.array([0.,-sin(k),cos(k)])
        for s in [-1,1]:
            nn=cos(v)*E+s*sin(v)*t
            n.append(nn);p.append(b-R*nn);C.append(b)
    return np.array(p),np.array(n),np.array(C)
def wrench(p,f):
    return np.r_[f,np.cross(p-np.array([BC,0.,0.]),f)/BR]
def frame(n):
    aux=Y if abs(n@Y)<.9 else E
    u=np.cross(n,aux);u/=norm(u)
    return u,np.cross(n,u)
def rays(n,mu,N,outer):
    u,v=frame(n); ang=np.arange(N)*2*pi/N
    return n+(mu/cos(pi/N) if outer else mu)*(np.cos(ang)[:,None]*u+np.sin(ang)[:,None]*v)
def basis(p,n,mu,N,outer):
    f=np.array([rays(nn,mu,N,outer) for nn in n])
    w=np.concatenate([f,np.cross(p[:,None,:]-[BC,0.,0.],f)/BR],axis=2)
    return f,w
def opt(p,n,mu=MU,idx=1,N=12,outer=True,F=None):
    f,w=basis(p,n,mu,N,outer)
    eq=np.vstack([w.reshape(-1,6).T,np.repeat([1,0,0,0,0,0,0],N)])
    obj=np.repeat(np.arange(7)==idx,N).astype(float)
    ans=linprog(obj,A_eq=eq,b_eq=np.r_[np.zeros(6) if F is None else -F,1.],bounds=(0,None),method='highs')
    assert ans.success,ans.message
    x=ans.x.reshape(7,-1);return ans.fun,x.sum(axis=1),(x[:,:,None]*f).sum(axis=1),ans.eqlin.marginals
def clean(p,n):
    w=np.array([wrench(pp,nn) for pp,nn in zip(p,n)]).T
    return w,solve(w[:,1:],-w[:,0])
if __name__=='__main__':
    for a in [0,14,16,18,20,24]:
        for v in [45,56,64,70]:
            best=(-1,None)
            for phi in [0,15,30,45,60]:
                p,n,C=model(radians(a),radians(v),radians(phi))
                g=min(opt(p,n,idx=i)[0] for i in range(1,7))
                if g>best[0]:best=(g,phi)
            print(a,v,best)
