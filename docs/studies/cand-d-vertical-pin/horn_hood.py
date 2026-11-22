"""Clipped forward nose, Take 47. Missing rear bay/closure is intentional."""
from itertools import product
from math import cos, hypot, pi, radians, sin, sqrt, tan
from pathlib import Path
from runpy import run_path
import numpy as np
from horn import Horn


def support(h,hi,park,n):
    t=np.linspace(h.lo,hi+park,4097)
    f=h.width(np.minimum(hi,t));a=n[0]*np.cos(t)+n[2]*np.sin(t)
    cut=np.max(h.rc*a+f*np.hypot(a,n[1]))
    return h.ox*n[0]+h.oz*n[2]+cut+(t[1]-t[0])/2*(h.rc+h.width(hi))*(1+h.rate)*hypot(*n)


def nose():
    h=Horn(18.);hi,park=.54,.62; rear,front=-1.15,15.4
    k,b=.30,8.26;k_top,t0=.32,23.95;s=3.065
    low=lambda x:7.53675+tan(radians(28))*(x-12.389796)
    side=lambda x:b-k*x
    top=lambda x:t0-k_top*x
    out=run_path(str(Path(__file__).resolve().parents[1]/'cand-d-rolling-cartridge/rolling.py'))
    R=4.2
    vertices=[(x,y,z) for x in (rear,front) for y,z in product((-side(x),side(x)),(low(x),top(x)))]
    diam=2*max(hypot(x+4.5,y,z+.97) for x,y,z in vertices)
    print('clipped forward sleeve, diameter about trial sphere centre',round(diam,4))
    sl=side(front)-s-.20
    gap=(t0-.20-support(h,hi,park,(k_top,0,1)))/hypot(1,k_top)
    sg=(b-.20-support(h,hi,park,(k,1,0)))/hypot(1,k)
    rel=[front-.20-support(h,hi,park,(1,0,0)),-support(h,hi,park,(-1,0,0))-rear-.20]
    print('front lip stock outside side skin, roof, side, front, rear horn clearances',
          np.round([sl,gap,sg,*rel],4))
    # Below the floor or outside one actual side plane for each full generator
    # segment; positive +X relative tail travel only increases these bounds.
    lower=cos(radians(28));g=999.
    for name,p,q,err in out['centreline']():
        ax=max(min((sign*a[1]-side(a[0]))/hypot(1,k) for a in (p,q)) for sign in (-1,1))
        z=min((low(a[0])-a[2])*lower for a in (p,q))
        g=min(g,max(z,ax)-R-err)
    gaps=[]
    for i,n,p,u,v in out['seats']():
        pts,_=out['nose'](p,n,u,v)
        gaps.append(min((low(q[0]-1.5)-q[2])*lower if i==0 else
                        (abs(q[1])-side(q[0]-1.5))/hypot(1,k) for q in pts))
    print('entire aligned tail to sleeve; all six local seats on swept face',
          round(g,4),np.round(gaps,4))
    print('rear opening dimensions (width, height), not a closed housing',
          2*side(rear),top(rear)-low(rear))
    assert min(sl,gap,sg,*rel,g,*gaps)>0 and diam<60


if __name__=='__main__':nose()
