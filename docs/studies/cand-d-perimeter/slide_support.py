"""Actual seated contact wrench on a laterally floating plate (Take 71)."""
from math import atan, cos, hypot, pi, radians, sin, sqrt, tan

import numpy as np
from scipy.optimize import linprog
from fixed_face import BACK, BC, CLOCK, CX, MU, RAD, RIM, X, Y, Z, loads, setup


def contacts():
    p,n,J=setup(RAD,radians(56.),radians(CLOCK))
    xyz=list(p-BACK*n);norm=list(n)
    for j in range(3):
        t=radians(CLOCK+60+120*j);r=cos(t)*Y+sin(t)*Z;q=.60*X+.80*r
        xyz.append((CX+BACK*.60-BC)*X+(RIM+BACK*.80)*r);norm.append(q)
    return xyz,norm


def forces(mass,Slo,Shi,k,depth=-7.58,pos=.19,err=.6):
    xyz,norm=contacts()
    R=np.zeros((6,27));B=np.zeros((6,27))
    A=[];b=[];C=cos(radians(err))-MU*sin(radians(err))
    moment_error=pos*hypot(1,MU)/C
    for j,(pt,m) in enumerate(zip(xyz,norm)):
        t=np.cross(m,X);t/=np.linalg.norm(t)
        G=np.array([m,t,np.cross(m,t)]).T
        ix=slice(3*j,3*j+3)
        R[:3,ix]=G;R[3:,ix]=np.cross(pt,G.T).T/RAD
        if j>=6:R[:,ix]*=-1
        else:
            B[:3,ix]=G;B[3:,ix]=np.cross(pt+(BC-depth)*X,G.T).T
        for th in 2*pi*np.arange(24)/24:
            row=np.zeros(27);row[ix]=[-tan(radians(err)+atan(MU)),cos(th),sin(th)]
            A.append(row);b.append(0.)
    for sg,val in ((1,Shi),(-1,-Slo)):
        row=sg*B[0].copy();row[:18:3]-=k/C
        A.append(row);b.append(val+.7)
    A=np.array(A);b=np.array(b);W=loads('table')*(mass/70)
    D=np.vstack((R,-R));D[[3,4,5,9,10,11],::3]-=moment_error/RAD
    A=np.vstack((A,D));b=np.r_[b,W,W]
    bounds=[(0,None),(None,None),(None,None)]*9
    def maximize(c):
        lp=linprog(-c,A_ub=A,b_ub=b,bounds=bounds,method='highs')
        assert lp.success,lp.message
        return -lp.fun
    I=np.eye(27);peak=[max(maximize(v/C) for v in part) for part in (I[:18:3],I[18::3])]
    E=np.zeros(27);E[:18:3]=moment_error
    roll=max(maximize(s*B[3]+E) for s in (-1,1))
    fax=-maximize(-B[0]);assert fax>0
    # Charnes-Cooper: scale reactions by 1/Fx. Outer envelope of support
    # radius at the real bearing level, with position error on all poles.
    AA=np.column_stack((A,-b));cops=[]
    for angle in np.arange(36)*2*pi/36:
        c=cos(angle)*B[4]+sin(angle)*B[5]+E
        lp=linprog(-np.r_[c,0],A_ub=AA,b_ub=0*b,A_eq=np.r_[B[0],0][None],
                   b_eq=[1.],bounds=bounds+[(0,None)],method='highs')
        assert lp.success,lp.message
        cops.append(-lp.fun)
    return [*peak,roll,fax,max(cops)/cos(pi/36)]


def missing():
    # Inscribed Coulomb polygon (witness, not an upper bound). At the
    # centred pose recess ONLY seat 0 by .020 normal, keep 8 true contacts.
    # The guide is ideal, axial spring load 1 N, no external wrench.
    xyz,norm=contacts()
    A=[];forces=[]
    for j,(pt,m) in enumerate(zip(xyz,norm)):
        t=np.cross(m,X);t/=np.linalg.norm(t)
        N=np.array([m+.15*(cos(a)*t+sin(a)*np.cross(m,t)) for a in np.arange(32)*2*pi/32])
        A.extend(np.column_stack((N,np.cross(pt,N)/RAD,N if j<6 else N*0))*(1 if j<6 else -1))
        forces.append(N)
    B=np.array(A).T;w=np.r_[np.zeros(6),1.,0.,0.]
    lp=linprog(np.ones(288),A_eq=B,b_eq=w,bounds=[(0,0)]*32+[(0,None)]*256,method='highs')
    assert lp.success
    f=np.einsum('ijk,ij->ik',forces,lp.x.reshape(9,32))
    n=np.einsum('ij,ij->i',norm,f)
    shear=np.linalg.norm(f-n[:,None]*norm,axis=1)
    print('zero-charge face normals per N draw; residual; maximum shear ratio',
          np.round(n,5),round(max(abs(B@lp.x-w)),13),round(max(shear[1:]/n[1:]),6))
    assert n[0]==0 and min(n[1:])>0 and max(abs(B@lp.x-w))<1e-10 and max(shear-.15*n)<1e-10
    return f


def face():
    from floating import system
    from edge_hertz import hertz
    k=tan(radians(56));s=sin(radians(56));kt=tan(radians(64))
    h=BC-BACK*cos(radians(56))+6.95;t=BACK*s
    edge=min(h/s,(1.65-h)/s,(1.35*k-h)/hypot(k,s),(k*(3.81-t)-h)/(2*s),
             (11.66-hypot(RAD,t)-h/kt)/(1+s/kt))
    print('V land, Hertz radius & p GPa at 214.5 N, remaining edge after .19',
          np.round([edge,hertz(214.5,BACK,BACK)[0],hertz(214.5,BACK,BACK)[2]/1000,
                    edge-.19-hertz(214.5,BACK,BACK)[0]],4))
    H=np.linalg.inv(system(None)[0].T)
    motion=np.sum(abs(H),axis=1)
    print('infinitesimal x,y,z plate sensitivity per unit independent normal offset',np.round(motion[6:],4))
    # After max travel and running reserve, a common PEAK contact location
    # in each layer of the non-tilting plate must stay inside its round land.
    print('transverse offset allowance; remaining circular bed radius at R11.20; central pocket depth',
          round(sqrt(2)*.18+.025,5),round(11.20-sqrt(2)*.18-.025,5),.73)
    # Actual 2-button rocking branch. Zero net Y,Z force means pitch moment
    # does not change between parallel X stations. Construct one pressure field.
    bed=11.20-sqrt(2)*.18-.025; arm=120.59/20; patch=4.70
    print('rocking COP / reserve for circular thrust patch / uniform pressure MPa / no-lift linear limit',
          np.round([arm,bed-arm-patch,20/(pi*patch**2),bed/4],4))
    assert arm+patch<bed and arm>bed/4
    # Material stack, relative to bottomed deck x-6.95; follows disk/rim.
    # Rim front is +.50 above that deck when the full circular bed is used.
    # Relative to the original home rim the deck is -.50.
    # From deck to old post front -8.43 at full draw +.50, excluding .04
    # assembly gap. Deck .44 + two .04 films + middle .34 + base .44.
    budget=(-6.95)-(-8.43+.50)-.04
    thick=.44+2*.04+.34+.44
    print('new full-area stack depth available / required / excess over post front (mm)',
          np.round([budget,thick,thick-budget],4))
    assert thick>budget


if __name__=='__main__':
    missing()
    face()
    for m,s,h in ((70,64,80),(110,96,112),(156.07,132,148)):
        for k in (.025,.10,.20):
            print('mass, Slo:Shi, effective k / single seat,jaw, roll Nmm, Fx min, COP radius at x-7.58',
                  m,(s,h),k,np.round(forces(m,s,h,k),3))
