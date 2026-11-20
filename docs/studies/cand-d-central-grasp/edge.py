"""Static support-function certificate for a Maxwell lip, not a free-exit proof.
All contact positions are on the head. No assumption of coplanar tail centres.
"""
from itertools import product
from math import cos, sin, pi, radians, hypot
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import linprog
from seats import RAD,TAN,ALPHA,ANGERR,X,Y,Z,MU,R,B,BERR,ROOT,V_END,LIP,W,face_geometry
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'cand-d-drawbolt'))
from barrel import hertz

P=12
F=MU/cos(pi/P)
FN=hypot(1,F)


def rays(i,s,beta,zone):
    l,t=RAD[i],TAN[i]
    a0,a1=beta
    betas=np.linspace(a0,a1,3)
    # These boxes enclose every point on each portion of the ruled face,
    # with .10 mm in each axis for metrology and the finite patch. They
    # are not a housing drawing. Use the actual larger stock when known.
    def point(a):
        if zone=='lip':
            return V_END+LIP*(cos(a)-cos(ALPHA)),V_END+LIP*(sin(ALPHA)-sin(a))
        if zone=='root':return ROOT*(1/cos(ALPHA)-cos(a)),ROOT*sin(a)
        return V_END,V_END
    lo,hi=np.sort([point(a0),point(a1)],axis=0)
    if zone=='flat':lo[:]=ROOT*sin(ALPHA)
    v=[]
    for a in betas:
        n=X*cos(a)-s*t*sin(a)
        u=np.cross(n,l)
        fs=np.array([n+F*(cos(k*2*pi/P)*l+sin(k*2*pi/P)*u) for k in range(P)])
        for rr,tt,xx in product((3.,8.7),(lo[1]-.10,hi[1]+.10),(lo[0]-.10,hi[0]+.10)):
            pos=(rr*l+s*tt*t+(xx-B/cos(ALPHA))*X)/R
            v.append(np.c_[fs,np.cross(pos,fs)])
    # Inscribed angular interpolation error <= step^2/8 on rotating unit
    # vectors. A common rigid rotation of a cone ray for face slope error
    # displaces it by <= chord * ray length. Sum symmetric dual debits.
    de=FN*(2*sin(ANGERR/2)+(betas[1]-betas[0])**2/8)
    return np.vstack(v),np.r_[np.full(3,de),np.full(3,1.65*de)]


def flat_plate():
    # Other front-facing flats may carry external load; enclose a full
    # +/-9.5 mm square, not just nominal sites. Includes a flat origin.
    fs=np.array([X+F*(Y*cos(k*2*pi/P)+Z*sin(k*2*pi/P)) for k in range(P)])
    v=[]
    for xx,yy,zz in product((-3.,1.),(-9.5,9.5),(-9.5,9.5)):
        v.append(np.c_[fs,np.cross(np.array([xx,yy,zz])/R,fs)])
    de=FN*2*sin(ANGERR/2)
    return np.vstack(v),np.r_[np.full(3,de),np.full(3,2.2*de)]


def groups():
    out={}
    for i,s in product(range(3),(-1,1)):
        for z in ('lip','root','flat'):
            intervals=([(ALPHA,ALPHA)] if z=='flat' else
                       list(zip(np.linspace(0,ALPHA,5)[:-1],np.linspace(0,ALPHA,5)[1:])))
            for j,interval in enumerate(intervals):out[i,s,z,j]=rays(i,s,interval,z)
    out['plate']=flat_plate()
    return out


def verify(G,focus,loads):
    aa=[]
    bb=[]
    for key,(wr,err) in G.items():
        aa.append(np.c_[-wr,np.tile(err,(len(wr),1))])
        # maximize the sum of the charged elemental bearing normals
        bb.extend([-1e-7-float(key==focus)]*len(wr))
    for sign in [-1,1]:
        aa.append(np.c_[sign*np.eye(6),-np.eye(6)]);bb.extend([0.]*6)
    aa=np.vstack(aa)
    r=linprog(np.r_[np.zeros(6),loads],A_ub=aa,b_ub=bb,
              bounds=[(None,None)]*6+[(0,None)]*6,method='highs')
    assert r.success and max(aa@r.x-bb)<1e-8
    return r.fun


def main():
    G=groups()
    # Substitute 52.2 joint-fault bend for 14.5. Use correction impulse
    # envelope as a separate load case, not both maximums simultaneously.
    # 2 N per lateral direction and 10 Nmm per moment is a deliberately
    # larger BOX than the corresponding isotropic gripper budgets.
    for draw in (35.,82.):
        extrema=[]
        for work in ('fault','table'):
            loads=np.array([draw+4*W,W+2,W+2,(25.4*W+10)/R,(50.8*W+10)/R,
                             ((52.2 if work=='fault' else 14.5)+10)/R])
            if work=='table':loads+=np.r_[W,0,0,W*(12.7+2.42)/R,W*(37.2-11.23)/R,W*hypot(50.8,25.4)/R]
            for i,s in product(range(3),(-1,1)):
                # Charge ALL strips on this lip, including patches straddling a
                # strip boundary. Also charge the adjacent straight working
                # flat; no claim that a seam halves the load per Hertz ellipse.
                keys=[k for k in G if k!='plate' and k[:2]==(i,s) and k[2] in ('lip','flat')]
                H={k:data for k,data in G.items() if k not in keys}
                H['shoe']=(np.vstack([G[k][0] for k in keys]),np.max([G[k][1] for k in keys],axis=0))
                extrema.append((verify(H,'shoe',loads),work,i,s))
        upper,*which=max(extrema)
        print('draw, one flank N (including lip), case, Hertz lip p0 MPa and halfwidths',
              draw,upper,which,hertz(upper,B-BERR,LIP-.05,B-BERR),flush=True)


if __name__=='__main__':main()
