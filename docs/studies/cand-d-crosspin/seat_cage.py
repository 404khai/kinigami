"""Local hard confinement after take-up; no claim that the stop is reached."""
from itertools import combinations
from math import cos, degrees, radians, sin, sqrt
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parent))
from flat_face import X, triangle, loads


def cage(gap, slack, verbose=False):
    # Both in mm: maximum signed normal lost motion at each service-loaded
    # land, and excess x permitted by the pin, relative to a witnessed pose.
    # Include bending, servo backdrive and the ENTIRE moving plate stroke
    # under changing load; unloaded part tolerance alone cannot supply them.
    R=6.5; S=9.; xp=12.95
    pts,N,_=triangle(18.,7.,8.,1.2,-.8,radians(58.),xp)
    pts=pts.repeat(2,axis=0)-15*X
    J=np.r_[np.column_stack((N,np.cross(pts,N)/S)),[[-1.,0.,0.,0.,0.,0.]]]
    # Six linearly independent seats + one tensile constraint -> simplex.
    # Strictly positive self-stress excludes unbounded recession directions.
    positive=np.linalg.solve(J[:6].T,-J[-1]);assert min(positive)>0.
    omit=[np.delete(np.arange(7),i) for i in range(7)]
    inv=[np.linalg.inv(J[ii]) for ii in omit]
    dn=2*sin(radians(.6)/2); dp=.19
    def update(tr,th):
        dist=np.linalg.norm(pts,axis=1)
        e=gap+dn*tr+(dist*dn+dp)*th+.5*(dist+dp)*th**2
        lim=np.r_[e,slack]
        vs=np.array([h@-lim[ii] for ii,h in zip(omit,inv)])
        assert np.all(vs@J.T+lim>=-1e-10)
        return max(np.linalg.norm(vs[:,:3],axis=1)),max(np.linalg.norm(vs[:,3:],axis=1))/S
    tr=th=0.
    for _ in range(150):
        tr,th=update(tr,th)
        if tr>2. or th>.15:return None
        a,b=tr*1.01+.0001,th*1.01+.00001
        c,d=update(a,b)
        if c<a and d<b:
            # The entire core circle fits between the shank ends throughout
            # this trial box. Its projected ellipse thus excludes a radius
            # r+b disk at the axis. Since the ellipse lies inside a radius R
            # disk about C, linked topology gives Cx-pin_x <= R-r-b.
            assert a+(R+.025)*sin(b)+.19<4.25
            if verbose:
                print('centre translation / angle / max pad travel',a,degrees(b),
                      a+max(np.linalg.norm(pts,axis=1))*b)
            return a,degrees(b),a+max(np.linalg.norm(pts,axis=1))*b
    return None


if __name__=='__main__':
    for gap in (.01,.02,.04,.06,.10):
        for slack in (.03,.06,.10,.20):
            x=cage(gap,slack)
            print(f'land / pin {gap:.2f}/{slack:.2f}:',None if x is None
                  else tuple(round(i,4) for i in x))
