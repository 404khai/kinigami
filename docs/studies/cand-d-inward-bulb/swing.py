"""Local swing-arm screen. No arm, pivot, mounting or powertrain fit implied."""
from math import asin, cos, hypot, pi, sqrt
import numpy as np
from mushroom import p, bl, bh, drift, W, mu


def sag(h,h0,l):
    return l-np.sqrt(l*l-(h-h0)**2)


def screen(l=18.,h0=2.45,A=2.85,hp=-4.12,hhi=3.055,ds=.012):
    # In the normal/tangent plane, centre t = sag(h)-sag(0), s.t. t(0)=0.
    # e represents the provisioned transverse clearance of a matched port,
    # including radial load deflection. A is relief radius, NOT running fit.
    hs=np.linspace(hp,hhi,801); cs=np.linspace(-1.,1.,1801)
    clo,chi=cs[:-1],cs[1:]
    s0=np.sqrt(np.maximum(0.,1.-np.maximum(abs(clo),abs(chi))**2))
    s1=np.sqrt(np.maximum(0.,1.-np.where(clo*chi<=0.,0.,np.minimum(abs(clo),abs(chi)))**2))
    def dmax(rlo,rhi,zlo,zhi,rmin,rmax,zmin,zmax):
        return np.hypot(np.maximum(0.,np.maximum(rmin-rlo,rhi-rmax)),
                        np.maximum(0.,np.maximum(zmin-zlo,zhi-zmax)))
    minproj,bore=1.,0.
    # Upper radius needed for a round central passage through stock at
    # depth, not the radius of a hole in the tilted front trim.
    passage=bh+drift+sag(hp,h0,l)-sag(0.,h0,l)+.03
    for h1,h2 in zip(hs[:-1],hs[1:]):
        e=max(abs(sag(h,h0,l)-sag(0.,h0,l)) for h in (h1,h2,min(max(h1,h0),h2)))+drift
        # Bound overlap at the top *plane*. Stem/sphere also needs swept
        # internal passage, checked independently below.
        hd=0. if h1*h2<=0 else min(abs(h1),abs(h2))
        if hd<bh: bore=max(bore,e+sqrt(bh*bh-hd*hd))
        r0,r1=(bl+p)*s0-e,(bh+p)*s1+e
        z0=h1+np.minimum((p+bl)*clo,(p+bh)*clo)
        z1=h2+np.maximum((p+bl)*chi,(p+bh)*chi)
        # Ring at z=0, larger buried ring and a rear passage. No solid
        # wall filling the entire original (straight) cylindrical bore.
        main=dmax(r0,r1,z0,z1,5.35,W,0.,0.)
        tube=dmax(r0,r1,z0,z1,passage,passage,-13.0,-1.68)
        lip=dmax(r0,r1,z0,z1,A,W,-1.,-1.)
        mask=np.minimum.reduce([main,lip,tube])>=p-1e-8
        if not np.any(mask): continue
        c=float(min(clo[mask]))
        angle=max(abs(asin((h-h0)/l)) for h in (h1,h2))+ds
        ca=cos(min(pi,np.arccos(c)+angle))
        ca=max(ca,-1/hypot(1,mu))
        proj=ca-mu*(sqrt(max(0.,1.-ca*ca))+bh/l)
        minproj=min(minproj,proj)
    # If an arm crosses the tube or clips the buried annulus, this
    # remains a conditional normal certificate, not a collar design.
    return bore,minproj


if __name__=='__main__':
    for l in (15.,18.,23.):
        bore,br=screen(l)
        maxback=sag(-4.12,2.45,l)-sag(0.,2.45,l)
        print('L; top opening required R; conditional force coefficient;'
              ' maximum parked centre offset; minimum cylindrical passage R',
              *(round(v,4) for v in (l,bore,br,maxback,bh+drift+maxback)))
