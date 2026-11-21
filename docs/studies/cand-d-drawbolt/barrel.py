"""Exploratory six DISTINCT stations, not the three-sphere v7 results.
Loads evaluated at the tail's translating, nonrotating ball-ring reference.
"""
from math import cos,sin,pi,sqrt,tan,atan,hypot,radians,acos,ceil,floor
from itertools import product
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq,linprog
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'cand-d-exact-pairs'))
from mixed import cert

X,Y,Z=np.eye(3); R=4.65; B=1.055; C=20.; RF=.60; mu=.23; DA=radians(.5)
P=12; STEP=pi/32
COLOCATED=False
def hertz(F,rt,rf=.6,meridian=1.045):
    kx=1/meridian+1/rf; ky=1/rt
    def ints(t):
        def integ(v):
            return quad(lambda u:2/(hypot(t,u)*hypot(1,u)*(v+u*u)),0,np.inf,
                        epsabs=1e-13)[0]
        return integ(1),integ(t*t)
    t=brentq(lambda t:ints(t)[0]/ints(t)[1]-kx/ky,1,1000)
    b=(3*F*ints(t)[0]/(2*pi*115400*kx))**(1/3); a=t*b
    return 3*F/(2*pi*a*b),a,b

def groups(i,k,side,band,patch,kg):
    phi=(90+i*120+(60 if k in 'TC' and not COLOCATED else 0))*pi/180
    r=Y*cos(phi)+Z*sin(phi); t=np.cross(X,r); u=t if k in 'KSA' else r
    if COLOCATED and (k=='S' or (k=='A' and side>0)):u=r
    rows=[]; objective=[]
    trans=(C-1.045)*2*sin(DA/2)+patch
    for j in range(band[0],band[1]+1):
        a=j*STEP
        n=(-cos(a)*X-sin(a)*r if k=='K' else X if k=='S' else side*X if k=='A'
           else cos(a)*side*t+sin(a)*X)
        v=np.cross(n,u)
        for l in range(P):
            f=n+(mu/cos(pi/P))*(cos(l*2*pi/P)*u+sin(l*2*pi/P)*v)
            extra=np.zeros(3); drag=0.
            if k=='K':
                dragbound=mu*(1.645*abs(f@X)+1.5575*abs(f@t)+1.027*abs(f@r))
                extra[i]=-f@r-dragbound; drag=max(0.,dragbound+f@r)
            for offset in (-trans,trans):
                row=np.r_[f,np.cross(r+offset*u/R-B/R*n,f),extra]
                rows.append(row); objective.append(drag)
                if k=='K' and j==0:
                    rows.append(np.r_[row[:6],0,0,0]);objective.append(drag)
    # Enclose EVERY elemental ray, not only a centred Hertz resultant. Nominal
    # contact normals must stay within DA of meridian at its actual angle.
    # A fractional angular interpolation error applies to f AND pole cross f.
    fac=hypot(1,mu/cos(pi/P)); angle=2*sin(radians(1.5)/2)+(STEP**2/8 if k in 'KC' else 0.)
    ef=fac*angle
    # Distribute patch centre error along u and meridian separately. Give
    # full unknown spatial shift (.18), plus meridional patch radius .05;
    # transverse contact wander plus patch width chiefly along nominal u.
    # delta .5deg between actual barrel axis and nominal extrusion (all errors).
    em=(1+trans/R)*ef + (fac*(.18+.065+trans*2*sin(DA))+
             (B*angle+.01)*mu/cos(pi/P))/R
    err=np.r_[np.full(3,ef),np.full(3,em),np.zeros(3)]
    # Absolute guide terms are bounded by the interpolated endpoint absolutes
    # plus the same norm interpolation/angle error (triangle inequality).
    if k=='K':err[6+i]=ef*(1+mu*sqrt(1.645**2+1.5575**2+1.027**2))
    return np.array(rows),err,np.array(objective)+(err[6+i] if k=='K' else 0.)

def charged(load,patch):
    # Six signed hard rows as usual; six independent positive multipliers for
    # the certified soft pad limits. Maximize individual hard+soft scalar sum.
    signs=(1,1,1,1,1,1); b=[9.8]*3+[5.6]*3
    G={}
    for i in range(6):
        for s in (-1,1):
            wr,err,_=groups(i%3,'A' if i<3 else 'T',s,(0,0),patch,0.)
            extra=np.zeros((len(wr),6))
            for soft in (False,True):
                if soft:extra[:,i]=1
                w=np.c_[wr[:,:6],extra]; e=np.r_[err[:6],np.zeros(6)]
                G[i,s,soft]=np.c_[-w,np.tile(e,(len(w),1))]
    mx=[0.]*6; misses=0
    for sg in product((-1,1),repeat=6):
        gs=[G[i,s,False] for i,s in enumerate(sg)]+[G[i,s,True] for i,s in enumerate(signs)]
        M=np.vstack(gs+[np.c_[np.eye(12),-np.eye(12)],np.c_[-np.eye(12),-np.eye(12)]])
        for site in range(6):
            rhs=np.r_[np.concatenate([np.full(len(g),-1e-6-float(i%6==site)) for i,g in enumerate(gs)]),np.zeros(24)]
            res=linprog(np.r_[np.zeros(12),load[:6],b],A_ub=M,b_ub=rhs,bounds=[(None,None)]*6+[(0,None)]*18,method='highs')
            if not res.success:misses+=1;continue
            assert max(M@res.x-rhs)<1e-7
            mx[site]=max(mx[site],res.fun)
    print('charged',load[:6], 'patch',patch,'missing',misses,'site axial/tangent',max(mx[:3]),max(mx[3:]),flush=True)

def run(kind,focus,g0,patch,stage):
    w=.05*9.80665; kg=.60; R0=R
    load=np.array([4*w,w,w,25.4*w/R0,50.8*w/R0,(52.2 if kind=='fault' else 14.5)/R0,g0,g0,g0])
    if kind=='correction':load[:6]+=[w,0,0,w*15.12/R0,w*25.97/R0,w*hypot(50.8,25.4)/R0]
    elif stage=='exit':load[0]+=w
    if stage=='charged':return charged(load,patch)
    G={}
    for i in range(3):
        G[i,'S',1]=groups(i,'S',1,(0,0),patch,kg)
        for s in [-1,1]:
            G[i,'T',s]=groups(i,'T' if stage=='keeper' else 'C',s,
                              (0,0) if stage=='keeper' else (0,16),patch,kg)
    mx=0.; fail=0
    # Common tail ring advance x. Both keeper angles and admissibility of a
    # rear flat depend on the SAME x; a missing contact has zero force.
    cases=[]
    if stage=='exit':cases=[('S',)*3]
    else:
        ell=B+RF
        for low in np.arange(-.30,2.01,.12):
            def al(x):return acos(1-min(ell,max(0.,x))/ell)/STEP
            band=(max(0,floor(al(low-.26))-2),min(16,ceil(al(low+.12+.26))+2))
            ks=[band]+(['S'] if low<=.26 else [])
            for i in range(3):
                if (i,band,1) not in G:G[i,band,1]=groups(i,'K',1,band,patch,kg)
            cases.extend(product(ks,repeat=3))
    for cs in dict.fromkeys(cases):
        for ss in product([-1,1],repeat=3):
            gg=[G[i,c,1] for i,c in enumerate(cs)]+[G[i,'T',s] for i,s in enumerate(ss)]
            sets=[[i] for i in range(6)] if focus=='single' else [[0,1,2]] if focus=='push' else ['drive']
            for sel in sets:
                rr=cert(gg,load,sel)
                if rr is None:fail+=1
                else:mx=max(mx,rr[0])
    print(kind,focus,'g0',g0,'patch',patch,stage,'missing',fail,'max certified',mx,flush=True)
    return fail,mx

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument('--kind',default='fault',choices=['fault','correction','service'])
    ap.add_argument('--focus',default='single',choices=['single','drive','push'])
    ap.add_argument('--g0',type=float,default=8.96)
    ap.add_argument('--patch',type=float,default=.45)
    ap.add_argument('--stage',default='keeper',choices=['keeper','exit','charged'])
    ap.add_argument('--colocated',action='store_true')
    a=ap.parse_args()
    COLOCATED=a.colocated
    for F in (43.1,60,90,120):
        print(F,'edge MPa and half axes mm',hertz(F,20.),'flat',hertz(F,20.,np.inf),flush=True)
    for p0 in (3500,4200):
        c=brentq(lambda c:hertz(43.1,c)[0]-p0,2.,100.)
        print('43.1N example p0',p0,'R_trans',c,flush=True)
    run(a.kind,a.focus,a.g0,a.patch,a.stage)
