"""Exploratory small-strain spring-pad coupon. Not qualified stiffness data."""
from itertools import product
from math import pi,tan
import numpy as np
from scipy.optimize import brentq
from compatible import hertz
from floating import gain


def pad(d,dt,L,lt,a,at,emin,emax,force,offset,shear,face_height):
    area=lambda D:pi*D**2/4
    ix=lambda D:pi*D**4/64
    kl=emin*area(d-dt)/(L+lt);kh=emax*area(d+dt)/(L-lt)
    ei=emin*ix(d-dt)
    kt=4*12*emax*ix(d+dt)/(L-lt)**3
    # Rigid crossplate; square of independently toleranced-post stiffnesses.
    # Individual axial forces equilibrate an arbitrarily eccentric resultant.
    # Axis/pitch error is not free: this screen assumes a gauged square.
    xy=np.array(list(product((-(a-at),a-at),repeat=2)))
    B=np.c_[np.ones(4),xy]
    peak=0.;moment=force*offset+shear*(face_height+L+lt)
    for k in product((kl,kh),repeat=4):
        D=np.array(k)[:,None]*B;F=D@np.linalg.inv(B.T@D)
        peak=max(peak,max(F[:,0]*force+np.linalg.norm(F[:,1:],axis=1)*moment))
    # Rigid plate + axial extension of the posts gives a minimum rotational
    # stiffness 4*kl*(a-at)^2 even if plate translation is free. Allow each
    # member its own lateral motion and apportion that restraint per member.
    # For slope v(0)=0, EI*v'(L)+kr*v(L)=0 -> x*cot x= -kr*L/EI.
    # Monotone in EI, kr; rescale to longest allowed L for a lower bound.
    kr=kl*(a-at)**2
    beta=kr*(L+lt)/ei
    root=brentq(lambda x:x/tan(x)+beta,pi/2,pi-1e-9)
    crit=ei*(root/(L+lt))**2
    return (4*kl,4*kh),kt,peak,crit


def hertz_series(ks,nrange,ball):
    return tuple(1/(1/k+2*hertz(n,ball)/(3*n)) for k,n in zip(ks,nrange))


if __name__=='__main__':
    # E brackets, probe offsets, skin thickness and load caps are TARGETS.
    lo=pad(.240,.003,3.60,.025,.65,.015,190000.,205000.,38.,.30,1.5,.6)
    hi=pad(.360,.004,5.30,.030,.95,.020,190000.,205000.,110.,.35,2.,.7)
    kl=hertz_series(lo[0],(1.,38.),3.);kh=hertz_series(hi[0],(65.,110.),8.)
    for name,v,k in [('one lower',lo,kl),('upper',hi,kh)]:
        print(name,'array axial stiffness range N/mm, transverse ceiling N/mm, max post load N, Euler N',
              np.round([*v[0],*v[1:]],3),'series normal N/mm',np.round(k,2))
    for d,L in ((.237,3.625),(.356,5.33)):
        print('if root fixed and cap rotation is free, single-post Euler N',
              round(pi**2*190000.*pi*d**4/(64*4*L**2),3))
    rho,result=gain(70.,[kl]*6+[kh],np.array([lo[1]]*6+[hi[1]]),
                    np.array([.4]*6+[.5]))
    U,dN,q,df=result
    print('feedback',round(rho,4),'individual lower max dN, top max dN',
          round(max(dN[:6]),3),round(dN[6],3),'max tangential centre motion mm',
          round(max(U),5),'max per-site shear increment N',round(max(df),3))
    assert rho<.3 and max(dN[:6])<14. and dN[6]<7.
    assert lo[2]<lo[3] and hi[2]<hi[3]
