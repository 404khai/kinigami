"""Continuous aligned material checks, nominal horn/Take 46 generator balls."""
from math import cos, hypot, pi, radians, sin, sqrt, tan
from pathlib import Path
from runpy import run_path
import numpy as np
from horn import Horn


def aligned(h,hi,park):
    # On the nominal disk t at home, let a=rc-f, d=r-a>=0.
    # y²<=2fd-d². Thus rho²=(x-15)²+y² <= rho0²-2d(rho0 cos(t)-f)
    # for rho0=15-Ox-a cos(t). The derivative at the intended pole vanishes.
    bound= .19; m=max(abs(h.lo),bound)
    amin=h.rc-h.width(bound);amax=h.rc-h.width(h.lo)
    rho_min=15-h.ox-amax;rho_max=15-h.ox-amin*cos(m)
    radial=2*(7.5-rho_max)*(cos(m)-h.width(bound)/rho_min)-2*h.oz*sin(abs(h.lo))
    assert 0<rho_min<=rho_max<7.5 and radial>0
    # Near the inner rim Q=distance² to (7.5,0,0) = const+a²+2aC.
    # .5 Q'' = (a')² + a*a'' + (a''-a)C + 2a'C'.
    D=7.5-h.ox;E=h.oz;F=h.rate*(h.rc+h.width(bound))
    curv=-amax*h.rate*F+amin*(D*cos(m)-E*sin(m))-2*F*(D*sin(m)+E)
    assert curv>0
    r=h.rc-h.width(0)
    assert abs(h.ox+r-7.5-4.2*cos(h.beta))<1e-12
    assert abs(-h.rate*(h.rc+h.b)*cos(h.beta)+r*sin(h.beta))<1.e-12
    # Above the short neighbourhood z is increasing at home; all material
    # with world angle past hi stays above the tube even for the widest disk.
    zprime=(h.rc-h.width(hi))*cos(hi)-h.rate*(h.rc+h.width(hi))*sin(hi)
    z0=h.oz+(h.rc-h.width(bound))*sin(bound)
    newz=h.oz+(h.rc-h.width(hi))*min(sin(hi),sin(hi+park))
    assert hi+park<pi and min(z0,newz)>4.2 and zprime>0
    return radial,curv,z0-4.2,newz-4.2


def neighbors(h,hi,park,lines):
    # At each world angle the widest possible moving disk is its home disk
    # at this angle or the maximum root disk after hi.
    t=np.linspace(h.lo,hi+park,1033); f=h.width(np.minimum(hi,t))
    err=(t[1]-t[0])*(h.rc+h.width(hi))*(1+h.rate)/2
    worst=(999.,None)
    for label,a,b,_ in lines:
        if label=='eye':continue
        a,b=np.array(a),np.array(b);s=np.linspace(a,b,97)
        x,y,z=(s-np.array([h.ox,0,h.oz])).T[:,:,None]
        rr=x*np.cos(t)+z*np.sin(t);tt=z*np.cos(t)-x*np.sin(t)
        dis=np.hypot(tt,np.maximum(0,np.hypot(rr-h.rc,y)-f))
        worst=min(worst,(float(dis.min()-4.2-err-np.linalg.norm(b-a)/192),label))
    return worst


if __name__=='__main__':
    rolling=run_path(str(Path(__file__).resolve().parents[1]/'cand-d-rolling-cartridge/rolling.py'))
    for L,hi,park in ((18.,.54,.62),(20.,.50,.56)):
        h=Horn(L)
        print('L, aligned q radial coefficient, half Q curvature, upper tube gaps',
              L,np.round(aligned(h,hi,park),4))
        gap,name=neighbors(h,hi,park,rolling['centreline']())
        print('full arc + thick tail, least non-ring gap:',name,round(gap,4))
        assert gap>0
        c=h.cut(hi,park);s=c[-1]+.16;d=sqrt(4.2**2-s*s)
        depth=h.depth(h.lo,hi,park);root=h.depth(hi-1.e-6,hi,0)
        print('cut x,y, slot halfwidth, lip work, parked reserve, root at lock:',
              np.round([*c,s,rolling['work'](sin(radians(28))*d/4.2),
              depth-2*cos(radians(28))-4.2+d,root],5))
