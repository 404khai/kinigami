"""Perturbed quasistatic seven-pad coupon. N, mm, wrenches scaled at R7."""
from itertools import product
import numpy as np
from columns import pad,hertz_series
from floating import basis,R,DIR
from vise import envelope


def gains(J,G,kn,W):
    out=[]
    # Bounds on q components, normal-force increments, and 2D tangent motion.
    for size in (6,7,7):
        out.append([np.zeros(size),np.zeros((size,6)),np.zeros((size,7)),np.zeros((size,7))])
    for k in product(*kn):
        k=np.array(k);D=k[:,None]*J;H=np.linalg.inv(J.T@D)
        for j,S in enumerate((H,D@H,G@H)):
            E=S@D.T
            if j==1:E-=np.diag(k)
            if j==2:
                T=np.linalg.norm(np.einsum('aik,bjk->abij',S,G),ord=2,axis=(2,3))
                values=[np.linalg.norm(S@W,axis=1).max(axis=1),np.linalg.norm(S,axis=1),
                        T,np.linalg.norm(E,axis=1)]
            else:
                values=[abs(S@W).max(axis=1),abs(S),
                        np.linalg.norm(np.einsum('ik,jlk->ijl',S,G),axis=2),abs(E)]
            out[j]=[np.maximum(a,b) for a,b in zip(out[j],values)]
    return out


def run(mass=70.,P=91.,dn=.007,dp=.060,migration=.00015,frame=.00022,nt=.000045,path_factor=1.5,stack=False):
    """Componentwise, deliberately absolute bounds. Fixed parameter trials:
    dn = row-triad orientation error (rotation chord);
    dp = reference pole error; migration = additional normal-direction change
    during service; frame = mm per-face MAX uncaptured differential seat motion;
    nt = mm/N normal motion under change of tangential traction.
    """
    J,G=basis()
    lo=pad(.240,.003,3.6,.025,.65,.015,190000.,205000.,38.,.30,1.5,.6)
    hi=pad(.360,.004,5.3,.030,.95,.020,190000.,205000.,110.,.35,2.,.7)
    # Deliberately enlarge compliance, including rotational indentation.
    ks=[hertz_series((v[0][0]/1.35,v[0][1]),n,r) for v,n,r in
        ((lo,(1.,38.),3.),(hi,(65.,110.),8.))]
    if stack:ks[-1]=tuple(1/(1/a+1/b) for a,b in zip(ks[-1],(70.,210.)))
    kt=np.array([lo[1]]*6+[hi[1]])
    t0=np.array([.4]*6+[.5])
    N0=np.array([22.]*6+[P])
    lens=np.array([np.hypot(7,3)]*6+[3.5])
    rad=np.array([3.]*6+[8.])
    # Delta in EXTERNAL wrench from a monitored unloaded reference. 70 g
    # box comes from the earlier study, not a measured body or floor load.
    W=np.hstack([envelope(mass,mode,R,'take23')[:,None]*DIR
                 for mode in ('table','service','fault')])
    mats=gains(J,G,[ks[0]]*6+[ks[1]],W)
    q=np.zeros(6);n=np.zeros(7);u=np.zeros(7)
    def advance(q,n,u):
        trans=np.linalg.norm(q[:3]);rot=np.linalg.norm(q[3:])/R
        # Error of the wrench triad: nominal pole error plus rotation/
        # movement of the sphere centre and the real contact pole.
        move=trans+(lens+rad+dp)*rot+rad*migration
        shift=dp+move
        shear=2*kt*(u+path_factor*((dn+migration)*trans+(shift+lens*(dn+migration))*rot))+t0
        force=(dn+migration)*(n+shear)+migration*(N0+t0)
        torque=(lens*force+shift*(n+shear)+move*(N0+t0))/R
        eW=np.r_[np.full(3,sum(force)),np.full(3,sum(torque))]
        # Normal gap differs from nominal Jq by row error, finite rotation
        # remainder, measured support change and residual cross-compliance.
        e=(dn+migration)*trans+(dp+(lens+rad)*dn)*rot+(lens+rad+dp)*rot*rot/2+frame+nt*shear
        return [a+b@eW+c@shear+d@e for a,b,c,d in mats]
    for _ in range(300):
        newest=advance(q,n,u)
        err=max(np.max(abs(x-y)) for x,y in zip(newest,(q,n,u)))
        q,n,u=newest
        if max(n)>150:return None
        if err<1e-8:break
    # A strict supersolution, not convergence from below as a certificate.
    # Re-evaluate at an inflated point to cover numerical residual.
    box=[x*1.002 for x in (q,n,u)]
    if not all(np.all(test<x) for test,x in zip(advance(*box),box)):return None
    return (*box,ks,err)


if __name__=='__main__':
    for dn,dp,f in [(0.,0.,0.),(.003,.030,.00010),(.007,.060,.00022),(.012,.12,.00050)]:
        v=run(dn=dn,dp=dp,frame=f)
        print('triad chord, pole error mm, differential seat shift mm:',dn,dp,f,
              'no enclosure' if v is None else (v[1].round(3),v[0].round(5)))
    for fl,ft in ((.0001,.0005),(.0005,.003),(.001,.010)):
        v=run(frame=np.array([fl]*6+[ft]),stack=True)
        print('trial softer top support; uncaptured lower/upper shift mm',fl,ft,
              'no enclosure' if v is None else v[1].round(3))
