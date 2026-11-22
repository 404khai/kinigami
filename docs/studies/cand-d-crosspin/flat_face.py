"""Three coplanar pad centres around the vertical pin; exploratory."""
from itertools import product
from math import asin, atan, cos, degrees, hypot, radians, sin, sqrt, tan
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parent))
from registry import X,Y,Z,envelope


def triangle(front,back,span,t,u,alpha,xp,R=6.5,r=2.7,b=1.75):
    # x_front and x_back are absolute pad-centre coordinates; the rear
    # and combined front thrusts pass through the nominal pull point.
    x0=xp-b
    pts=np.array([[back,(back-x0)*t,0],[front,(front-x0)*u+span,0],
                  [front,(front-x0)*u-span,0]])
    horiz=np.array([(X+k*Y)/hypot(1,k) for k in (t,u,u)])
    N=np.array([cos(alpha)*a+sg*sin(alpha)*Z for a in horiz for sg in (-1,1)])
    # Working poles must be outside the torus and the other two root caps.
    # The separate pads may fuse with the eye away from the working poles.
    pairs=list(zip(pts.repeat(2,axis=0),N))
    ring=np.array([15.,0.,0.])
    cg=[]
    for i,(p,n) in enumerate(pairs):
        q=p-r*n
        cg.append(hypot(np.linalg.norm((q-ring)[:2])-R,q[2])-r)
        cg.extend(np.linalg.norm(q-o)-r for j,o in enumerate(pts) if j!=i//2)
        cg.append(np.linalg.norm(p[:2]-[xp,0.])-r-b)
    return pts,N,min(cg)


def loads(pts,N,mass=70.,R=6.5,r=2.7,b=1.75,zerr=.05):
    # Non-collinear centres give three distinct vertical force coordinates.
    # All perturbations below are at a physically registered, full-face pose.
    xp=15-R+r+b; x0=xp-b
    ref=15*X; scale=9.
    J=np.column_stack([np.r_[n,np.cross(p-ref,n)/scale] for p,n in
                        zip(pts.repeat(2,axis=0),N)])
    dn=2*sin(radians(.6)/2)
    dm=.19/scale+max(np.linalg.norm(pts-ref,axis=1))/scale*dn
    if np.linalg.svd(J,compute_uv=False)[-1]<=sqrt(6)*hypot(dn,dm):return None
    H=np.linalg.inv(J); f,m=H[:,:3],H[:,3:]
    loss=(np.linalg.norm(f,axis=1)*dn+np.linalg.norm(m,axis=1)*dm)/(min(N[:,0])-dn)
    a=radians(2.)
    phi=asin((zerr+(R+.025)*sin(a)**2/(2*cos(a))) /
             ((R-.025)*cos(a)-(r+.015+b+.010)))
    K=tan(phi+atan(.23))
    off=hypot((R+.025)*sin(a)+.23,zerr+(b+.010)*sin(phi)+.23)
    g=f+np.cross(m,(x0-15.)*X)/scale
    penalty=(K*np.linalg.norm(g[:,1:],axis=1)+
             ((off+.25*K)*np.linalg.norm(m[:,1:],axis=1)+off*K*abs(m[:,0]))/scale)
    slope=f[:,0]-penalty-loss
    if min(slope)<=0: return None
    return [max((abs(H)@e+loss*e[0])/slope) for case in ('service','table','fault')
            for e in [envelope(mass,case,scale,wide='take23')]]


def main():
    R,r,b=6.5,2.7,1.75; xp=15-R+r+b
    best=[]
    for xf,xb,h,t,u,angle in product((18.,20.,22.),(5.,7.,9.),(6.,8.,10.),
                                     (.6,.9,1.2),(-.5,-.8,-1.1),(38.,48.,58.)):
        pts,N,c=triangle(xf,xb,h,t,u,radians(angle),xp)
        if c<.35:continue
        P=loads(pts,N)
        if P:best.append((max(P),xf,xb,h,t,u,angle,c,P,pts))
    assert best
    for row in sorted(best,key=lambda v:v[0])[:3]:
        print('P, front/back/span/t/u/angle/gap, service/table/fault, centres',
              [round(float(v),3) for v in row[:-2]],
              [round(float(v),3) for v in row[-2]],row[-1].tolist())


if __name__=='__main__':main()
