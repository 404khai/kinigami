"""Take 16, quasistatic author study. Python 3 + NumPy/SciPy; no candidate inputs edited.
mm, N, N mm; normalize all moments by R for equilibrium. Not a contact simulation.
"""
from math import sin, cos, tan, sqrt, hypot, pi, radians, degrees
from itertools import product
import numpy as np
from scipy.optimize import linprog

MU=.23
R=4.65
PLO,PHI=25.,34.       # required ACTUAL thread-axis load after carrier drag, not nominal spring specification
X,Y,Z=np.eye(3)
rad=lambda a:cos(a)*Y+sin(a)*Z
face=np.array([rad(i*2*pi/3) for i in range(3)])
key=np.array([rad(pi/3+i*2*pi/3) for i in range(3)])
KT=np.cross(X,key)
NORMAL=np.vstack(([X]*3,KT)); C=np.vstack((face,key))
B=np.c_[NORMAL,np.cross(C,NORMAL)].T
A=np.linalg.inv(B)
assert np.allclose(A[:3,3:],2*np.cross(face,X)/3)
assert np.allclose(A[3:,:3],2*KT/3)

def thread(d,p,rlo,ahi=1.):
    # Conservative usable pressure-flank radius and undamaged nominal profile.
    # One loaded flank sign only; no lower estimate for projected overlap.
    hi=d/2
    l=p/(2*pi*rlo); a=tan(pi/6); nx=1/sqrt(1+a*a+l*l)
    delta=2*sin(radians(ahi)/2)
    c=nx-delta-MU*(sqrt(1-nx*nx)+delta)
    t=l/sqrt(1+a*a)+delta
    side=sqrt(1-nx*nx)+delta
    tor=hi*(t+MU)/c
    return c,tor,(side+MU)/c, l
CAX,KQ,KS,LEAD=thread(2.5,.45,.92)
Q=PHI*KQ

def gimbals(restrained):
    # Requirements on *installed* supports, not an assumed 50/50 torque couple.
    # Single tab can take all nut torque at >=3.00 mm. Side-flexure <=1.50 N
    # throughout allowed radial motion; angular flexure <=50 N mm/rad over +/-2 deg.
    # Tabs/flexures within .25 mm axial offset from the force-reference plane.
    if restrained:
        S=1.50+Q/3.0
        return S,50*radians(2)+.25*S,.12
    # No useful flexure isolation: bound one pressure-flank sector directly.
    S=KS*PHI
    return S,.50*S,1.25+.12

def params(m,case,signed=True):
    w=m*.001*9.80665
    return 4*w,w,25.4*w,50.8*w,52.2 if case=='fault' else 14.5

def ideal_face_min(m,case,restrained):
    f,s,t,y,z=params(m,case)
    side,m0,e=gimbals(restrained)
    return (PLO-f)/3-2*(hypot(y,z)+m0+e*PLO)/(3*R)

def model(m,case,restrained,roller=.23,raw=False):
    # All axial pads compress only, any may lift. One polarity per tangent roller
    # coordinate. Radius of cap/roller pole <=1.06. Same-center direction error
    # .5 deg; true centre deviates <=.18 mm. Outer friction polygon + column error.
    f,s,t,my,mz=params(m,case)
    side,m0,e=gimbals(restrained)
    g=.18/R; ang=2*sin(radians(.5)/2)
    rotor=1.06/R; poly=12
    loads=np.r_[f,s+side,s+side,(t+Q)/R,(my+m0)/R,(mz+m0)/R]
    best=np.full(6,-np.inf); small=np.full(3,np.inf)
    v=np.r_[X,[0.,0.,0.]]
    # Actual central resultant -P*X ; its bounded eccentricity contributes moment <=eP.
    E=np.r_[np.zeros(4),e/R,e/R]
    for signs in product((-1,1),repeat=3):
        cols=[];errs=[];ids=[]
        for i in range(6):
            n=NORMAL[i]*(1 if i<3 else signs[i-3]); u=C[i]; w=np.cross(n,u)
            mu=MU if i<3 else roller
            fp=mu/cos(pi/poly)
            for j in range(poly):
                a=2*pi*j/poly
                F=n+fp*(u*cos(a)+w*sin(a))
                # Ball force is INWARD at pole. Covers both +/- tangent polarities.
                p=C[i]-rotor*n
                cols.append(np.r_[F,np.cross(p,F)])
                ef=sqrt(1+fp**2)*ang
                em=ef+g*sqrt(1+fp**2)+fp*(rotor*ang+.02/R)
                errs.append(np.r_[np.full(3,ef),np.full(3,em)])
                ids.append(i)
        M=np.array(cols).T;H=np.array(errs).T
        U=np.r_[np.c_[ M-H,-v-E],np.c_[-M-H, v-E]]
        b=np.r_[loads,loads]+1e-8
        # The primal feasible superset has certifying dual solutions from HiGHS.
        for i in range(6):
            obj=np.r_[(np.array(ids)==i).astype(float),0]
            bounds=[(0,None)]*len(ids)+[(PLO,PHI)]
            for sg in ((-1,1) if i<3 else (-1,)):
                r=linprog(sg*obj,A_ub=U,b_ub=b,bounds=bounds,method='highs')
                assert r.success, r.message
                # Recheck minor floating LP residuals using a tighter tolerance than printed rounding.
                assert max(U@r.x-b)<1e-7
                if sg==-1:best[i]=max(best[i],-r.fun)
                else:small[i]=min(small[i],r.fun)
    return min(small),max(best[:3]),max(best[3:])

def last(m,d,p,rlo,allow=1000.):
    # f = remaining fraction of last load-bearing helical circumference.
    # Single-flank surface area <= annular area * sqrt(1+tan^2 30 + lead^2);
    # allow another 2% on surface orientation/geometry. Most optimistic: whole flank
    # is loaded up to a pressure cieling everywhere, no runout/edge concentration.
    ann=pi*((d/2)**2-rlo**2)
    surface=1.02*ann*sqrt(1+tan(pi/6)**2+(p/(2*pi*rlo))**2)
    F=4*m*.001*9.80665
    return F,F/(allow*surface*sqrt(1+MU**2))

if __name__=='__main__':
    for d,p,rlo in [(2.5,.45,.92),(3.,.5,1.12)]:
        ax,kt,ks,l=thread(d,p,rlo)
        print(d,'axial cosine/friction reserve',ax,'torque/axial',kt,'side/axial',ks,
              'P34 thread torque',PHI*kt,'Nsum',PHI/ax,'max lead',l)
    for m in (46,50):
        for case in ('service','fault'):
            for bounded in (True,False):
                print(m,case,'gimballed' if bounded else 'one-sector direct',
                      'frictionless min',ideal_face_min(m,case,bounded),
                      'outer: axial min,max; tangent max',model(m,case,bounded))
        print('last finite pulling load N, min full-sector fraction at example p*=1 GPa',last(m,2.5,.45,.92))
    print('spring nominal only: 1.70/1.88 height',[(2.82-h)*28.85 for h in (1.70,1.88)])
    print('tilt debit 0.25 deg',2.5*tan(radians(.25)),'axial pitch backlash at diametral .020',.020*tan(pi/6))
