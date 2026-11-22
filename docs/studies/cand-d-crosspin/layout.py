"""Exploratory indexed triangle search. mm, N. Not the complete Kin package."""
from itertools import product
from math import atan2, cos, hypot, radians, sin, sqrt, tan
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parent))
from registry import X,Y,Z,site,A,r,b,envelope,pin_data


def layout(x,half,span,up,angle,swivel=0):
    # Apex has positive z; two base pads on the same lower z line. Fix the
    # groove tangents in the plane, not at 120 degrees by construction.
    pts=np.array([[x,0.,up],[x,half,-span],[x,-half,-span]])
    N=[]
    for _,y,z in pts:
        a=atan2(z,y)+radians(swivel)
        t=-sin(a)*Y+cos(a)*Z
        for sg in (-1,1):
            N.append(cos(radians(angle))*X+sg*sin(radians(angle))*t)
    return pts,np.array(N)


def eval_layout(pts,N,angle,mass=70.,zerr=.05):
    a,K,off=pin_data(zerr)
    x=pts[0,0]; origin=x*X
    J=np.column_stack([np.r_[n,np.cross(p-origin,n)/site]
                       for p,n in zip(pts.repeat(2,axis=0),N)])
    maxdist=max(np.linalg.norm(pts-origin,axis=1))/site
    dn=2*sin(radians(.6)/2); dp=.19/site
    dm=maxdist*dn+dp
    if np.linalg.svd(J,compute_uv=False)[-1]<=sqrt(6)*hypot(dn,dm):
        return None
    H=np.linalg.inv(J)
    f=H[:,:3];m=H[:,3:]
    loss=(np.linalg.norm(f,axis=1)*dn+np.linalg.norm(m,axis=1)*dm)/cos(radians(angle+.6))
    g=f+np.cross(m,(12.7-x)*X)/site
    pad=K*np.linalg.norm(g[:,1:],axis=1)+((off+.25*K)*np.linalg.norm(m[:,1:],axis=1)
                                           +off*K*abs(m[:,0]))/site
    slope=f[:,0]-loss-pad
    if min(slope)<=0: return None
    return [max((abs(H)@e+loss*e[0])/slope)
            for case in ('service','table','fault')
            for e in [envelope(mass,case,site,wide='take23')]]


def clearance(p,n,others):
    # ≥.35 mm local separation from *other* spheres/tube at contact pole;
    # not a seat-patch envelope. Pin sweeps between drawn/take-up-relieved.
    q=p-r*n; delx=np.clip(p[0],13.95,15.)-p[0]
    to_pin=hypot(delx,p[2])-b-r
    to_wall=(7.91838+(p[0]-13.95)-abs(p[1]))/sqrt(2)-r
    to_ring=hypot(hypot(q[0]-15.,q[2])-A,q[1])-r
    to_peers=min(np.linalg.norm(o-q)-r for o in others)
    return min(to_pin,to_wall,to_ring,to_peers)


def main():
    best=[]; rejected=0
    for x,h,lo,hi,angle in product((12.7,13.5,14.5,15.5,16.5,18.),
                                   (2.8,3.4,4.,5.,6.,7.2),
                                   (5.5,7.,8.5,10.),(8.,10.,12.),(50.,56.,62.,66.)):
        pts,ns=layout(x,h,lo,hi,angle)
        gap=min(clearance(pts[i],n,np.delete(pts,i,axis=0))
                for i in range(3) for n in ns[2*i:2*i+2])
        if gap<.35: continue
        fs=eval_layout(pts,ns,angle)
        if not fs:rejected+=1;continue
        best.append((max(fs),x,h,lo,hi,angle,gap,fs))
    assert best
    print('qualified test geometries (local clearances/force screen only), no finite bound:',
          len(best),rejected)
    for v in sorted(best)[:5]:
        print('P, x/±y/base-z/apex-z/angle, pole surplus, service/table/fault',
              *[round(i,3) for i in v[:-1]],[round(i,3) for i in v[-1]])


if __name__=='__main__': main()
