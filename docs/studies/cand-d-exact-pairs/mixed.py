"""Same assumptions as take11. Independent free-leading radial blades.
Static upper bound only. Requires numpy+scipy. No assertion current=force.
"""
from itertools import product
from math import sin,cos,pi,sqrt,radians,hypot
import numpy as np
from scipy.optimize import linprog
from take11 import X,rad,tang,R,MU,BALL,DC,DA
P=12; STEP=pi/32
# Lengths x from nominal seat centre. Long straight cheeks protect each still-held
# site individually; another ball may already be on its cheek rim.
XE=1.48  # end of straight cheek before extruded round, minimum target
AXERR=.08
RF=.10
def facets(i,surf,side,kg,xrange=None,band=(0,16)):
    l=rad[i]; t=tang[i]; ans=[]; rhs=[]
    z=MU/cos(pi/P); fmax=sqrt(1+z*z)
    grid=np.arange(band[0],band[1]+1)*STEP if surf in ('K','C') else [0.]
    for a in grid:
        n= -cos(a)*X-sin(a)*l if surf=='K' else sin(a)*X+cos(a)*side*t if surf=='C' else side*t if surf=='T' else X
        u=t if surf=='K' else l
        v=np.cross(n,u)
        # Enclose lever in convex hull of interval endpoints, independently of
        # angle. Works even if pose changes across contacts.
        xs = xrange if xrange is not None else (((BALL+RF)*(1-cos(a)),) if surf=='K' else (XE+(BALL+RF)*sin(a),) if surf=='C' else (0.,))
        for xp in xs:
            ct=(-side*(BALL+RF)*(1-cos(a))) if surf=='C' else 0.
            c=l+xp/R*X+ct/R*t
            for k in range(P):
                f=n+z*(cos(2*pi*k/P)*u+sin(2*pi*k/P)*v)
                m=np.cross(c-BALL/R*n,f)
                extra=np.zeros(3)
                if surf=='K':extra[i]=-f@l-kg
                ans.append(np.r_[f,m,extra])
                rhs.append(max(0.,kg+f@l) if surf=='K' else 0.)
                if surf=='K' and a==0:
                    ans.append(np.r_[f,m,0,0,0]);rhs.append(max(0.,kg+f@l))
    q=2*sin(DA/2)+(STEP**2/8 if surf in ('K','C') else 0.)
    ef=fmax*q
    cmax=1+(XE+2*(BALL+RF))/R
    # If centre depends on a, d2(c cross f)/da2 also contains c''f+2c'f'.
    # Both |c'| and |c''| <= (BALL+RF)/R (one component for K, circular arc for C).
    em=cmax*ef+(hypot(DC,AXERR)/R)*fmax+(BALL*q+.01)/R*z
    if surf in ('K','C'): em+=3*(BALL+RF)/R*fmax*STEP**2/8
    er=np.zeros(3)
    if surf=='K': er[i]=ef
    return np.array(ans),np.r_[np.full(3,ef),np.full(3,em),er],np.array(rhs)+(ef if surf=='K' else 0.)

def cert(groups,load,focus):
    mats=[]; rhs=[]
    for j,(wr,err,drag) in enumerate(groups):
        mats.append(np.c_[-wr,np.tile(err,(len(wr),1))])
        rhs.extend((-drag-1e-6) if focus=='drive' else [-1e-6-(1. if j in focus else 0.)]*len(wr))
    mats.extend([np.c_[np.eye(9),-np.eye(9)],np.c_[-np.eye(9),-np.eye(9)]])
    rhs.extend(18*[0.])
    AA=np.vstack(mats)
    res=linprog(np.r_[np.zeros(9),load],A_ub=AA,b_ub=rhs,bounds=[(None,None)]*6+[(0,None)]*12,method='highs')
    if not res.success: return None
    assert max(AA@res.x-rhs)<1e-7
    return res.fun,res.x[:9]

def allcases(kg,g0,kind='service',mass=50,focus='sum'):
    W=mass*.001*9.80665
    load=np.array([4*W,W,W,25.4*W/R,50.8*W/R,(52.2 if kind=='fault' else 14.5)/R,g0,g0,g0])
    if kind=='correction':load[:6]+=np.array([W,0,0,W*(12.7+2.42)/R,W*(37.2-11.23)/R,W*np.hypot(50.8,25.4)/R])
    G={(i,k,s):facets(i,k,s,kg) for i in range(3) for k in 'SC' for s in [-1,1]}
    for i in range(3):
        for k,lo,hi in [('A',0,8),('B',8,16)]:
            G[i,k,1]=facets(i,'K',1,kg,band=(lo,hi))
            xx=((BALL+RF)*(1-cos(lo*STEP)),(BALL+RF)*(1-cos(hi*STEP)))
            for ss in (-1,1):G[i,'T'+k,ss]=facets(i,'T',ss,kg,xrange=xx)
        for t,xx in [('TS',(0.,)),('TF',(0.,XE))]:
            for s in (-1,1):
                G[i,t,s]=facets(i,'T',s,kg,xx)
    missing=0; worst=0; critical=None
    for ax in product(['A','B','S','C','F'],repeat=3):
        # All ball sets have radial 120 deg symmetry; use all cyclic permutations
        # for loads in x/y/z, but can cheaply use symmetric absolute body force/
        # torque disk bounds for cyclic reduction if needed.
        for signs in product((-1,1),repeat=3):
            groups=[G[i,k,1] for i,k in enumerate(ax) if k in 'ABS']
            tags=[i for i,k in enumerate(ax) if k in 'ABS']

            groups+= [G[i,'C' if k=='C' else 'T'+k,signs[i]] for i,k in enumerate(ax)]
            tags += [3+i for i in range(3)]
            if focus in ('ax','tan'):
                # maximise the upper bound for any ONE active contact, not just site zero
                indices=[j for j,k in enumerate(tags) if (k<3)==(focus=='ax')]
                results=[cert(groups,load,[j]) for j in indices]
                if not indices:continue
                rr=None if None in [None if r is None else 1 for r in results] else max(results,key=lambda r:r[0])
            else:
                rr=cert(groups,load,range(len(groups)) if focus=='sum' else focus)
            if rr is None: missing+=1
            elif rr[0]>worst:worst,critical=rr[0],(ax,signs)
    print(mass,kind,'k/g',kg,g0,'focus',focus,'missing',missing,'bound',round(worst,4),'critical',critical,flush=True)
    return missing,worst
if __name__=='__main__':
    import argparse
    arg=argparse.ArgumentParser()
    arg.add_argument('--focus',choices=['sum','drive','ax','tan'],default='sum')
    arg.add_argument('--mass',type=float,default=50.)
    arg.add_argument('--kind',choices=['service','correction','fault'],default='service')
    arg.add_argument('--kg',type=float,default=.46)
    arg.add_argument('--g0',type=float,default=.8)
    a=arg.parse_args()
    allcases(a.kg,a.g0,focus=a.focus,kind=a.kind,mass=a.mass)
