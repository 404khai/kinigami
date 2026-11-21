#!/usr/bin/env python3
"""Decision study only: service wrench on three radial 90-degree grooves.

Units mm, N, N.mm, MPa. A sufficient frictionless full-seat equilibrium
is not proof it is reached, nor an upper bound on frictional self-stress.
"""
import math
from itertools import product
cos,sin,pi=math.cos,math.sin,math.pi

def inputs(m=.046,arm=50.8):
    w=m*9.80665
    return 4*w,w,2*w*12.7,math.hypot(w*arm,14.5)

def face(m,R,e,dx):
    pull,side,twist,bend=inputs(m)
    # Origin in nominal ball-centre plane. Account for external transverse
    # load applied dx away from that plane, even for the frictionless test.
    bend+=dx*side
    pmin=(pull+2*bend/R+twist/R+2*side)/(1-2*e/R)
    return pmin

def verify(P,R,e,dx,m):
    # Equilibrium check on actual directions, resisting positive external loads.
    # u radial; t=J u. mj uses pitch/yaw moment after -J convention.
    pull,side,tx,M=inputs(m); M+=dx*side+e*P
    u=[(cos(i*2*pi/3),sin(i*2*pi/3)) for i in range(3)]
    t=[(-b,a) for a,b in u]
    min_n=float('inf')
    for ai,bi in product(range(36),repeat=2):
        B=(cos(ai*pi/18)*M,sin(ai*pi/18)*M)
        S=(cos(bi*pi/18)*side,sin(bi*pi/18)*side)
        ps=[(P-pull)/3 + 2*sum(a*b for a,b in zip(v,B))/(3*R) for v in u]
        qs=[tx/(3*R)+2*sum(a*b for a,b in zip(v,S))/3 for v in t]
        for j in range(2):
            assert abs(sum(R*p*v[j] for p,v in zip(ps,u))-B[j])<1e-8
            assert abs(sum(q*v[j] for q,v in zip(qs,t))-S[j])<1e-8
        assert abs(sum(ps)+pull-P)<1e-8 and abs(R*sum(qs)-tx)<1e-8
        min_n=min(min_n,min((p-abs(q))/math.sqrt(2) for p,q in zip(ps,qs)))
    return min_n

def partial(mu,Rcap,rc=5.35,tol=.15,e=1.1,dx=.15,psi=45):
    # Entire projected axial-reaction convex segment (incl one-site endpoints)
    # stays clear of origin if the sites are a strict subset of the triangle.
    # e bounds actual loaded jaw's axial-force eccentricity, not pitch radius.
    # Face friction also acts at an offset from each cap centre.
    # dx bounds height difference *in the partial configuration*.
    th=math.radians(psi)
    nj=cos(th)-mu*sin(th)
    if nj<=0:return None
    sj=(sin(th)+mu*cos(th))/nj
    nf=(1-mu)/math.sqrt(2)
    if nf<=0:return None
    ef=Rcap*mu/nf
    # |C_x|<=P+pull; max(C_x)*(rc/2-tol) <= M+P*e+ ...
    arm=rc/2-tol-e-ef-dx*sj
    if arm<=0:return arm,None
    pull,side,tx,M=inputs()
    P=(M+pull*(rc/2-tol+ef)+dx*side)/arm
    return arm,P

if __name__=='__main__':
    for m,e in product((.046,.050),(0,.8,1.1,1.4)):
        P=face(m,5.2,e,3.0)
        print(f'full seat {1000*m:.0f} g e={e:.2f}, sufficient P > {P:.3f}; min contact at P+2N {verify(P+2,5.2,e,3.0,m):.3f}')
    for mu,dx in product((.1,.2,.23,.4,.5,.8),(.15,.4,.8)):
        print('partial',mu,dx,partial(mu,1.4,dx=dx))
    print('Hertz smooth interior only: R=1.4 mm, E*=110GPa (steel/steel provisional)')
    for load in (10,20,40,80):
        a=(3*load*1.4/(4*110000))**(1/3)
        print(load,a,3*load/(2*pi*a*a))
