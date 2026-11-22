"""Shared rigid-body x-cell tightening for regular cylindrical-face study.
Fixture envelope is explicit, never an attitude or release proof.
"""
from itertools import product
from math import acos,asin,ceil,floor,cos,sin,pi,radians,sqrt,hypot
from functools import lru_cache
import numpy as np
from scipy.optimize import linprog
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'cand-d-exact-pairs'))
from mixed import cert

R=6.; B=2.; K=3.50; C=4.; MU=.23
X,Y,Z=np.eye(3); P=12; STEP=pi/48
def solve(kind,focus,g0,angle,stage,xy,guide):
    rad=2*R*sin(radians(angle)/2); xt=R*sin(radians(angle))
    W=.05*9.80665
    load=np.r_[[4*W,W,W,25.4*W/R,50.8*W/R,(52.2 if kind=='fault' else 14.5)/R],np.full(3,g0)]
    if kind=='correction':load[:6]+=[W,0,0,W*15.12/R,W*25.97/R,W*hypot(50.8,25.4)/R]
    elif stage=='exit':load[0]+=W
    @lru_cache(None)
    def section(i,k,s,j0,j1):
        phi=radians(90+120*i); r=cos(phi)*Y+sin(phi)*Z;t=np.cross(X,r)
        rows=[];rhs=[];u=t if k=='K' else r
        for j in range(j0,j1+1):
            a=STEP*j
            n=(-cos(a)*X-sin(a)*r if k=='K' else X if k=='G' else sin(a)*X+s*cos(a)*t)
            v=np.cross(n,u)
            for l in range(P):
                f=n+MU/cos(pi/P)*(cos(2*pi*l/P)*u+sin(2*pi*l/P)*v)
                row=np.r_[f,np.cross(r-B/R*n,f),0.,0.,0.];drag=0.
                if k=='K':
                    # Moment of meridional NORMAL vanishes on cylinder axis;
                    # friction force still incurs Rk*mu*N free couple.
                    gb=guide*(1.63*abs(f@X)+1.15*abs(f@t)+.58*abs(f@r)+
                              2*sqrt(3)/4*1.52*MU/cos(pi/P))
                    row[6+i]=-f@r-gb;drag=max(0.,gb+f@r)
                rows.append(row);rhs.append(drag)
                if k=='K' and abs(j)<=4:
                    rows.append(np.r_[row[:6],0.,0.,0.]);rhs.append(drag)
        delta=2*sin(radians(.5)/2)+(STEP**2/8 if k!='G' else 0)
        fac=hypot(1,MU/cos(pi/P)); ef=fac*delta
        em=ef+fac*(.08+.12+rad)/R+MU/cos(pi/P)*(.015+B*delta)/R
        err=np.r_[np.ones(3)*ef,np.ones(3)*em,np.zeros(3)]
        if k=='K':err[6+i]=ef*(1+guide*sqrt(1.63**2+1.15**2+.58**2))+guide*.02
        return np.array(rows),err,np.array(rhs)+(err[6+i] if k=='K' else 0)
    if stage=='charged':
        def lift(i,k,s,lo,hi,soft):
            wr,e,_=section(i%3,k,s,lo,hi); nr=len(wr); extra=np.zeros((nr,6))
            if soft:extra[:,i]=1.
            W=np.c_[wr[:,:6],extra]; E=np.r_[e[:6],np.zeros(6)]
            return np.c_[-W,np.tile(E,(nr,1))]
        # From a CLOSED radial dwell with centre at R +/-.06, XY<=.50,
        # plus .08 centre error, |beta|<11.0deg. Rear plane gap and
        # |x datum difference| <=.18 => |chi|<3.8deg if hard K or G
        # present at that ball. When both axial hard contacts absent, the
        # unbroken corridor still confines its centre between those planes.
        A={}
        for i in range(6):
            for s in (-1,1):
                k=('G' if s>0 else 'K') if i<3 else 'C'
                lo,hi={'G':(0,0),'K':(-3,3),'C':(-2,2)}[k]
                for soft in (False,True):
                    A[i,s,soft]=lift(i,k,s,lo,hi,soft)
        mx=[0.,0.];miss=0
        for sg in product((-1,1),repeat=6):
            gs=[A[i,s,False] for i,s in enumerate(sg)]+[A[i,1,True] for i in range(6)]
            M=np.vstack(gs+[np.c_[np.eye(12),-np.eye(12)],np.c_[-np.eye(12),-np.eye(12)]])
            for i in range(6):
                rhs=np.r_[np.concatenate([np.full(len(g),-1e-6-float(j%6==i)) for j,g in enumerate(gs)]),np.zeros(24)]
                z=linprog(np.r_[np.zeros(12),load[:6],3*[9.84],3*[5.90]],A_ub=M,b_ub=rhs,bounds=[(None,None)]*6+[(0,None)]*18,method='highs')
                if not z.success:miss+=1;continue
                assert max(M@z.x-rhs)<1e-7
                mx[i//3]=max(mx[i//3],z.fun)
        print('charged',kind,'missing',miss,'a/t site upper',mx,flush=True);return
    # At each x choose an active axis per station or none, sign per C.
    # x datum uncertainty per K or C (centre error .08, track .06).
    err=xt+.14
    clamp=lambda v:max(-1,min(1,v))
    neg=max(-24,floor(asin(clamp(-(xy+.08+.06)/(K-.03)))/STEP))
    maxc=ceil(acos(clamp(1-(xy+rad+.14)/(C-.03)))/STEP)
    mx=0.;missing=0;ncase=0;critical=None;cache={}
    for xc in np.arange(-err-.15,4.40+err,.12):
        lo=xc-err;hi=xc+.12+err
        def domains():
            if stage=='exit':return ['G']
            a=[]
            if lo<=.02 and hi>=-.12:a+=['G']
            if hi>=0 and lo<=K+.03:
                klo=max(0,floor(acos(clamp(1-max(0,lo)/(K+.03)))/STEP))
                khi=min(24,ceil(acos(clamp(1-max(0,hi)/(K-.03)))/STEP))
                if klo<=khi:
                    if -klo>=neg and klo>0:a+=[(max(neg,-khi),-klo)]
                    a += [(max(neg,-khi) if klo==0 else klo,khi)]
            return a if a else ['none']
        aks=domains()
        cl=max(-24,floor(asin(clamp(lo/(C+.03 if lo>=0 else C-.03)))/STEP))
        ch=min(24,ceil(asin(clamp(hi/(C-.03 if hi>=0 else C+.03)))/STEP),maxc)
        # An active C need not exist. Cannot access its backside in this fixture:
        # lateral displacement at any centre < C (including centre errors).
        # On a regular captured approach the installed back seat bounds
        # negative travel: specify x_centre >= -.18 relative to cheek axis.
        cl=max(cl,-1)
        exists=cl<=ch and hi>=-.18 and lo<=C+.03
        for ks in product(aks,repeat=3):
            for ss in product((-1,1) if exists else (1,),repeat=3):
                key=(ks,ss,cl,ch,exists)
                if key in cache:continue
                cache[key]=1
                gg=[];ids=[]
                for i,k in enumerate(ks):
                    if k=='G':gg.append(section(i,'G',1,0,0));ids.append('G')
                    elif k!='none':gg.append(section(i,'K',1,*k));ids.append('K')
                    if exists:gg.append(section(i,'C',ss[i],cl,ch));ids.append('C')
                if not gg:continue
                ncase+=1
                fs=([[j] for j in range(len(gg))] if focus=='single' else
                    [[j for j,k in enumerate(ids) if k=='G']] if focus=='push' else ['drive'])
                for f in fs:
                    if not f:continue
                    o=cert(gg,load,f)
                    if o is None:
                        if missing==0:print('first missing',xc,ks,ss,cl,ch,flush=True)
                        missing+=1
                    elif o[0]>mx:mx=o[0];critical=(xc,ks,ss,cl,ch)
    print(kind,focus,'stage',stage,'angle',angle,'xy',xy,'g0',g0,'guide',guide,'modes',ncase,
          'missing',missing,'max certified ONLY',mx,'critical',critical,flush=True)

if __name__=='__main__':
    import argparse
    a=argparse.ArgumentParser()
    for n,default in [('kind','fault'),('focus','single'),('stage','edge')]:a.add_argument('--'+n,default=default)
    for n,default in [('angle',3.),('xy',.5),('g0',8.96),('guide',.23)]:a.add_argument('--'+n,default=default,type=float)
    p=a.parse_args();solve(p.kind,p.focus,p.g0,p.angle,p.stage,p.xy,p.guide)
