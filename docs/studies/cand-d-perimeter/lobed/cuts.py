"""Nominal LOWER contact cover. numpy/scipy only accelerate exact occupied-point queries.
Cells use analytic radius bounds, not a grid pass rate. python3 cuts.py
"""
from lobe import h,v,beta,B,K,KR,XB,M,W,WC,RI,RO,MU,R0
import numpy as np
from scipy.spatial import cKDTree
import json
from math import hypot

lam=1.10
def wall(p,t):return np.sqrt(np.maximum(B+K*p,B+(K-KR)*XB+KR*p)**2-t*t)
def shape(a):return np.column_stack(a)
def size(a):return np.linalg.norm(a,axis=1)
def rot(p,th):
    a,z,t=p.T;a=a-h;z=z-v;c=np.cos(th);s=np.sin(th)
    return shape([h+a*c+z*s,v-a*s+z*c,t])
def cloud():
    # Pairs are actual occupied material, no inflated collision surrogate.
    x,t=np.meshgrid(np.linspace(-5.,0,101),np.linspace(-7.,7.,281))
    x=x.ravel();t=t.ravel();base=wall(x,t)
    f=[];leaf=[]
    for dh in (0,.04,.1,.19,.36,.58,.76,.94):
        y=base+dh;rho=np.hypot(x-h,y-v)
        fix=((abs(t)>=WC)&(abs(t)<=6.60)&(dh<=.20)) | ((abs(t)<WC)&((x<=h)|(rho<=RI)))
        mov=(abs(t)<=W)&(x>h+.65)&(rho>=RO)
        f.append(shape([x[fix],y[fix],t[fix]]));leaf.append(shape([x[mov],y[mov],t[mov]]))
    return cKDTree(np.concatenate(f)),cKDTree(np.concatenate(leaf))
def root(t,zadd=0):
    lo=np.full_like(t,.68);hi=np.full_like(t,1.48)
    for _ in range(24):
        u=(lo+hi)/2;p=h+u
        outside=np.hypot(u,wall(p,t)+zadd-v)>=RO
        lo=np.where(outside,lo,u);hi=np.where(outside,u,hi)
    return h+(lo+hi)/2

def blend(a,b,ea,eb,s,es):
    y=a*(1-s[:,None])+b*s[:,None];l=size(y);n=y/l[:,None]
    er=(1-s)*ea+s*eb+es*(size(a-b)+ea+eb)
    ratio=np.minimum(1,er/l)
    en=np.where(er>=l,2.,np.sqrt(2*ratio**2/(1+np.sqrt(1-ratio**2))))
    return n,en

def check(kind,F,J):
    # Uniform [0,1] coordinates: phase, feature parameter, first blend,
    # second blend. Zero-span coordinates encode pure faces or exact corner.
    fixed=kind.startswith('fixed_')
    if fixed:kind=kind[6:]
    both=kind.startswith('corner')
    pure=kind in ('sideface','roofface','toeface','rear_side')
    active=[1,1,0 if pure else 1,1 if both or kind=='rear_side' or kind in ('sideface','roofface','toeface') else 0]
    if both:active[1]=0
    # Boxes (center, halfwidth); coarse starts avoid worst root conditioning
    # only for mixed side/concave arc. Box proof collects no sample witnesses.
    lo=np.zeros((1,4));hi=np.array([active],float)
    boxes=power=blocked=0;depth=0;lowest=1e9
    for depth in range(65):
        if not len(lo):break
        cc=(lo+hi)/2;dh=(hi-lo)/2;T,s,a,bb=cc.T;et,es,ea,eb=dh.T
        th=T*beta;eth=et*beta; zero=0*s;ones=np.ones_like(s)
        t=(WC if fixed else W)*ones;dt=zero;p=zero;dp=zero;zz=zero;dz=zero
        if kind in ('back','toe','roofface','toeface'):
            t=W*s;dt=W*es
        if kind in ('back','corner_back'):
            p=root(t);dp=.18*dt+1e-7
        if kind in ('side','sideface','roofface'):
            # Plane extension to p=-1.02 conservatively includes every
            # actual lower roof/root intersection; entire side may go
            # farther back at its highest backing, so use h+.65 there.
            xmin=(-1.4 if fixed else h+.65) if kind=='sideface' else -1.02
            p=xmin*(1-(bb if kind=='roofface' else s))
            dp=-xmin*(eb if kind=='roofface' else es)
        if kind in ('sideface','toeface','toe_side'):
            thick=.20 if fixed else .95
            zz=thick*(s if kind=='toe_side' else bb)
            dz=thick*(es if kind=='toe_side' else eb)
        if kind=='rear_side':
            # Full cylindrical-side/flat-side edge at fixed t: polar angle
            # in park frame [-.32,1.0] includes all u>.65, w<=y<=w+.95.
            pol=-.32+1.32*s;ep=1.32*es
            p=h+RO*np.cos(pol);dp=RO*ep
            y=v+RO*np.sin(pol);dy=RO*ep
        else:
            y=wall(p,t)+zz;dy=.44*dp+.25*dt+dz
        q=shape([p,y,t]);eq=np.sqrt(dp*dp+dy*dy+dt*dt)
        rr=B+K*p;nf=shape([-K*ones,wall(p,t)/rr,t/rr])/M
        ef=(.079*dt+.010*dp)
        nr=shape([p-h,y-v,zero])/RO
        er=np.hypot(dp,dy)/RO
        nt=shape([-ones,zero,zero]);ns=shape([zero,zero,-ones])
        if kind in ('back','corner_back'): n,en=blend(nf,nr,ef,er,a,ea)
        elif kind in ('toe','corner_toe'): n,en=blend(nf,nt,ef,zero,a,ea)
        elif kind=='side':n,en=blend(nf,ns,ef,zero,a,ea)
        elif kind=='toe_side':n,en=blend(nt,ns,zero,zero,a,ea)
        elif kind=='rear_side':
            # A sphere contact on the interior of this concave arc requires
            # n_rho <= RO/R by nonnegative second variation along the arc.
            ar=bb*np.arcsin(RO/R0); eang=eb*np.arcsin(RO/R0)
            n=nr*np.sin(ar[:,None])+ns*np.cos(ar[:,None]);en=er+eang
        else:
            n,en={'roofface':(nf,ef),'toeface':(nt,zero),'sideface':(ns,zero)}[kind]
        # On the POSITIVE-t cheek the force on metal points in +t,
        # opposite to the leaf-side trim used just above.
        if fixed:
            if kind=='side':n,en=blend(nf,-ns,ef,zero,a,ea)
            if kind=='sideface':n,en=-ns,zero
            if kind=='toe_side':n,en=blend(nt,-ns,zero,zero,a,ea)
        if both:n,en=blend(n,-ns if fixed else ns,en,zero,bb,eb)
        V=shape([v-y-lam*np.cos(th),p-h-lam*np.sin(th),zero])
        if fixed:V=shape([-ones,zero,zero])
        nominal=(n*V).sum(axis=1)-MU*size(np.cross(n,V))
        lower=nominal-(1+MU)*(size(V)*en+(0 if fixed else eq+lam*eth))-2e-6
        okay=lower>0
        if np.any(okay):lowest=min(lowest,float(np.min(lower[okay])))
        boxes+=len(lo);power+=int(sum(okay)); idx=np.flatnonzero(~okay)
        if len(idx):
            ctr=q[idx]-R0*n[idx];e=eq[idx]+R0*en[idx]+2e-6
            dd=(F if fixed else J).query(ctr)[0]
            dd2=(J if fixed else F).query(rot(ctr,-th[idx] if fixed else th[idx]))[0]
            rr=np.hypot(ctr[:,0]-h,ctr[:,1]-v)
            bad=(dd+e<R0)|(dd2+e+rr*eth[idx]<R0)
            blocked+=int(sum(bad));idx=idx[~bad]
        if len(idx)==0:lo=lo[:0];break
        if depth>=49 or len(idx)>250000:
            return dict(certified=False,remaining=len(idx),depth=depth,example=cc[idx[0]].tolist())
        lo=lo[idx];hi=hi[idx]
        # split the longest weighted dimension per box
        dim=np.argmax((hi-lo)*np.array([1.25,1.40,2.,2.]),axis=1)
        ii=np.arange(len(lo));mid=(lo[ii,dim]+hi[ii,dim])/2
        right=lo.copy();right[ii,dim]=mid;left=hi.copy();left[ii,dim]=mid
        lo=np.vstack((lo,right));hi=np.vstack((left,hi))
    return dict(certified=True,boxes=boxes,power=power,penetrating=blocked,depth=depth)
if __name__=='__main__':
    F,J=cloud()
    kinds=('roofface','toeface','sideface','back','toe','side','corner_back','corner_toe','toe_side','rear_side',
           'fixed_side','fixed_sideface','fixed_corner_toe','fixed_toe_side')
    out=dict(label='exploratory',lambda_mm_per_rad=lam,features={k:check(k,F,J) for k in kinds})
    print(json.dumps(out,indent=2))
