"""Seated geometry and force targets; not an installed-load measurement."""
from math import asin, atan, cos, degrees, hypot, radians, sin, sqrt
from pathlib import Path
import sys
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from button_seats import setup, X,Y,Z, test


def incidence():
    # Until withdrawal, verify the spindle is registered to the ring (the
    # relative errors below must include loaded deflection, not just CAD).
    wmin=2.61-.13; sr=.03; a=radians(1.)
    R=7.53; r=4.23; beta=atan(.32)+radians(.20); k=np.tan(beta)
    eps=k*sin(a)+1-cos(a)
    rho=.51+r/cos(beta)+k*(.06+R*sin(a))
    az=asin((R*(1-cos(a))+rho*eps)/wmin)+atan(sr/wmin)+asin(eps)
    # q pressure-centre height error: ring centre, in-plane spine tilt and
    # tube/taper tolerance. Keep integration of finite patch AS AN EXTRA.
    dz=.06+R*sin(a)+.03*sin(beta)+r*radians(.20)
    rad=.48+.32*4.2*sin(atan(.32))
    dr=.03+(r*sin(beta)+dz)*(k-.32)+.32*dz
    dp=hypot(dz,dr+rad*az)
    print('registered normal azimuth + taper angle deg; point wander / spare in .47',
          round(degrees(az)+.20,4),round(dp,4),round(.47-dp,4))
    return degrees(az)+.20,dp


def cage(seat=.02,pin=.06):
    q,c,e,ps,ns=setup(-90,11.,6.,58.); R=7.5; r=4.2
    spine=(15.-R)*X
    # A material sphere at the rear core is enough as a seventh stop;
    # additional contacts only restrict the feasible connected set.
    pts=np.vstack((ps,spine))-c
    N=np.vstack((ns,-e)); S=11.
    J=np.column_stack((N,np.cross(pts,N)/S))
    assert min(np.linalg.solve(J[:6].T,-J[-1]))>0
    ix=[np.delete(np.arange(7),i) for i in range(7)]
    hs=[np.linalg.inv(J[j]) for j in ix]
    le=np.linalg.norm(pts,axis=1); dn=2*np.sin(np.radians([.6]*6+[2.])/2)
    def box(u,w):
        pos=np.array([.19]*6+[.55])
        err=dn*u+(le*dn+pos)*w+.5*(le+pos)*w*w
        d=u+(le[-1]+pos[-1])*w
        # At a registered material rear core the cone-normal radial distance
        # is >=4.75. Norm Hessian is <=1/(4.75-d) over the motion. Stay on
        # the finite working flank, not the extrapolated cone past its tip.
        if d>=.90: return np.inf,np.inf
        err[-1]+=.5*d*d/(4.75-d)
        lim=np.r_[[seat]*6,pin]+err
        vs=np.array([h@-lim[j] for h,j in zip(hs,ix)])
        assert np.all(vs@J.T+lim>=-1e-9)
        return max(np.linalg.norm(vs[:,:3],axis=1)),max(np.linalg.norm(vs[:,3:],axis=1))/S
    u=w=0.
    for _ in range(100):
        u,w=box(u,w)
        if not np.isfinite(u):return None
        U,W=u*1.01+.0001,w*1.01+.00001
        a,b=box(U,W)
        if a<U and b<W:return tuple(round(float(i),4) for i in (U,degrees(W),U+max(le)*W))
    return None


if __name__=='__main__':
    assert incidence()[0]<2
    print('sufficient registered table resultant along e',test(-90.,11.,6.,58.)[0])
    kappa=np.tan(atan(.23)+radians(2.)); beta=atan(.32)
    x0=cos(beta); dx=kappa*sin(beta)
    B=5*.07*9.80665
    print('trial net face axial force 64..76N -> P interval',
          (64-B)/(x0+dx),(76+B)/(x0-dx))
    for g in (.010,.020,.040):
        for s in (.030,.060,.10): print('land/pin, bounded u mm/w deg/pad motion mm',g,s,cage(g,s))
