"""Registered full-contact Maxwell face behind a one-sided tapered pin. mm/N."""
from itertools import product
from math import atan, cos, hypot, radians, sin, sqrt
from pathlib import Path
import sys
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'cand-d-crosspin'))
from registry import X,Y,Z,envelope


def setup(phase,radius,station,face_angle):
    R,r,k=7.5,4.2,.32
    beta=atan(k); e=cos(beta)*X+sin(beta)*Z; w=np.cross(e,Y)
    spine=(15-R)*X; q=spine+r*e
    c=spine+station*e; alpha=radians(face_angle)
    pts=[];dirs=[]
    for psi in (phase,phase+120,phase+240):
        u=radians(psi); l=cos(u)*Y+sin(u)*w; t=np.cross(e,l)
        for sg in (-1,1):
            pts.append(c+radius*l);dirs.append(cos(alpha)*e+sg*sin(alpha)*t)
    return q,c,e,np.array(pts),np.array(dirs)


def test(phase,rad,sta,ang,normal_error=2.,point_error=.47,mass=70.,yaw=(14.5,52.2)):
    q,c,e,ps,ns=setup(phase,rad,sta,ang)
    R,r,k=7.5,4.2,.32
    xp=15-R+.48+r*hypot(1,k)
    pole=ps-r*ns
    # Necessary free space at every pole; no ascription of a load capacity
    # to the finite heads unless the complete working patch is accessible.
    clear=min(np.hypot(np.linalg.norm((pole-15*X)[:,:2],axis=1)-R,pole[:,2])-r)
    # A ball centre outside the infinite cone by its normal offset clears
    # the full solid even though the real cone is clipped at both ends.
    cg=((np.linalg.norm((ps-xp*X)[:,:2],axis=1)-.48-k*ps[:,2])/hypot(1,k)-r)
    if min(clear,min(cg))<.35 or min(ns[:,0])<.28:return None
    J=np.column_stack([np.r_[n,np.cross(p-c,n)/rad] for p,n in zip(ps,ns)])
    dn=2*sin(radians(.6)/2);dm=dn+.19/rad
    if np.linalg.svd(J,compute_uv=False)[-1]<=sqrt(6)*hypot(dn,dm):return None
    H=np.linalg.inv(J); f,m=H[:,:3],H[:,3:]
    # Cone working normal e with arbitrary traction mu=.23 and 2 degrees
    # normal error. P is the resultant component along e, NOT a screw force.
    kap=np.tan(atan(.23)+radians(normal_error)); dp=point_error
    loss=(np.linalg.norm(f,axis=1)*dn+np.linalg.norm(m,axis=1)*dm)/(cos(radians(ang))-dn)
    v=f+np.cross(m,q-c)/rad
    slope=v@e-kap*np.linalg.norm(v-np.outer(v@e,e),axis=1)-loss
    slope-=dp*hypot(1,kap)*np.linalg.norm(m,axis=1)/rad
    if min(slope)<=0:return None
    P=[]
    for case in ('service','table','fault'):
        w=envelope(mass,case,rad,wide='take23')
        w[-1]+=(yaw[1]-52.2 if case=='fault' else yaw[0]-14.5)/rad
        # Envelope moments here must be about c. Charge shift from assumed
        # old reference at ring centre even when it worsens the old allowance.
        w[3:]+=abs(np.cross(np.eye(3),15*X-c)).T@w[:3]/rad
        P.append(max((abs(H)@w+loss*(abs(e)@w[:3]))/slope))
    return max(P),P,clear,min(cg),ps[::2]


if __name__=='__main__':
    hits=[]
    for cfg in product(range(-90,-29,5),(7.,8.,9.,10.,11.),
                       (-4.,-2.,0.,2.,4.,6.),(40.,46.,52.,58.)):
        t=test(*cfg)
        if t:hits.append((t[0],cfg,t))
    print('locally screened layouts',len(hits))
    for _,cfg,t in sorted(hits,key=lambda v:v[0])[:4]:
        print(cfg,'P',np.round(t[1],2),'pole/cone surplus',np.round(t[2:4],2),
              'points',np.round(t[4],2).tolist())
