"""Exploratory: finite six-face plate, adjustable axial shoe loads. N and mm."""
from math import acos, atan, cos, degrees, hypot, pi, radians, sin, sqrt, tan

import numpy as np
from scipy.optimize import linprog
from disk import BACK, B, CX, K, RIM, X, Y, Z, envelope, preload, seam, setup
from edge_hertz import hertz


A, HOME, END = 12.42, -6.95, 1.40
BC, RAD, ANG, CLOCK = -4.31, 10.3, 60., -90.
QX, QR = .38/hypot(1,.38), 1/hypot(1,.38)
DELTA, POS, MU = radians(.6), .19, .23


def faces():
    k, s, c = tan(radians(ANG)), sin(radians(ANG)), cos(radians(ANG))
    pole_x, pole_t = BC-BACK*c, BACK*s
    cap, rw, outer = -5., 1.35, 3.81
    toe = pole_t-(pole_x-HOME)/k
    top_t = pole_t+(cap-pole_x)/k
    top_w = rw-(cap-HOME)/k
    # Truncated positive-height pyramid: includes far flank and both drafted sides.
    def face_x(t,r):
        return max(HOME,min(cap,pole_x+k*(abs(t)-pole_t),
                               HOME+k*(outer-abs(t)),HOME+k*(rw-abs(r))))
    assert abs(face_x(pole_t,0)-pole_x)<1e-10
    assert top_w>0 and top_t<outer-(cap-HOME)/k
    # Every vertex of a pyramid lies inside the plate's limiting circle.
    assert hypot(RAD+rw,outer)<A
    # Distance IN THE TANGENT PLANE from pole to first edge (not a projected gap).
    # Unit in-slope vector increases t by cos(a), x by sin(a).
    # Side plane k*r+x<=HOME+k*rw restricted to this tangent plane.
    margin=min((pole_x-HOME)/s,(cap-pole_x)/s,
               (HOME+k*rw-pole_x)/hypot(k,s),
               (HOME+k*(outer-pole_t)-pole_x)/(s+k*c))
    nx=cos(radians(ANG)+DELTA)
    g=seam(B-A+.05,BACK-.05,END-.05,END+.05)
    vals=[pole_x,pole_t,toe,outer-(cap-HOME)/k-top_t,top_w,
          A-hypot(RAD+rw,outer), BC-BACK-HOME,CX-BACK-cap,
          (B+K*BC-RAD)/hypot(1,K)-BACK,margin]
    print('pole x,t / inner toe / top length,half-width / OD margin / button,belly,bore gaps / slope-plane margin:',np.round(vals,4))
    print('stroke / home radial gap / terminal sphere exclusion / minimum disk-edge, wall, insert axial force terms:',
          np.round([END-HOME,B+K*HOME-A,g[0],g[2],g[3],nx-MU*sqrt(1-nx*nx)],4))
    return margin


def springs(lo,hi):
    # q' is actual contact normal. S/q'_x is a virtual coefficient,
    # not the actual normal reaction when friction or a guide is loaded.
    eps=2*sin(DELTA/2)
    coeff0=lo/(QX+eps); coeff1=hi/(QX-eps)
    mid=(coeff0+coeff1)/2
    scatter=(coeff1-coeff0)/(coeff1+coeff0)
    need=QX*preload(ANG,QX,0.,scatter,0.,radius=RAD,button_x=BC)
    return [QX*mid,scatter,*need]


def loads(case):
    W=envelope(70,case,RAD,wide='take23')
    tors=.070*9.80665*3*(38+20.65)*(1.4 if case=='fault' else 1.)
    W[-1]+=(tors-(52.2 if case=='fault' else 14.5))/RAD
    return W


def reactions(mu=.23, guide=.05, d0=.5, lo=33., hi=39., order=24):
    """Outer LP for seated equilibria. No equal-sharing or frictionless-force credit."""
    pts,ns,_=setup(RAD,radians(ANG),radians(CLOCK))
    p=[r-BACK*n for r,n in zip(pts,ns)]
    ns=list(ns)
    for r in pts[::2]/RAD:
        ns.append(QX*X+QR*r)
        p.append((CX+BACK*QX-BC)*X+(RIM+BACK*QR)*r)
    # Orthonormal nominal axes; f on tail positive at seats and negative at shoes.
    mtx=np.zeros((6,27))
    aq=[];bq=[]
    C=cos(DELTA)-mu*sin(DELTA)
    for i,(r,n) in enumerate(zip(p,ns)):
        t=np.cross(n,X);t/=np.linalg.norm(t)
        F=np.column_stack((n,t,np.cross(n,t)))
        sl=slice(3*i,3*i+3)
        G=F if i<6 else -F
        mtx[:3,sl]=G
        mtx[3:,sl]=np.cross(r,G.T).T/RAD
        for angle in 2*pi*np.arange(order)/order:
            row=np.zeros(27);row[sl]=[-tan(atan(mu)+DELTA),cos(angle),sin(angle)]
            aq.append(row);bq.append(0.)
        if i>=6:
            # If |guide axial drag|<= d0+guide*N_actual then F_x lies
            # within [lo-drag,hi+drag]. Assumes no axial hard stop engaged.
            for sign,lim in ((1,hi),(-1,-lo)):
                row=np.zeros(27);row[sl]=sign*F[0];row[3*i]-=guide/C
                aq.append(row);bq.append(lim+d0)
    out=[]
    for case in ('service','table','fault'):
        W=loads(case)
        mat=np.vstack((mtx,-mtx))
        mat[[3,4,5,9,10,11],::3]-=POS*hypot(1,mu)/(RAD*C)
        AA=np.vstack((aq,mat)); bb=np.r_[bq,W,W]
        results=[]
        for k in range(9):
            obj=np.zeros(27);obj[3*k]=-1./C
            res=linprog(obj,A_ub=AA,b_ub=bb,bounds=[(0,None),(None,None),(None,None)]*9,method='highs')
            if res.status==3: results.append(np.inf);continue
            assert res.success, res.message
            results.append(-res.fun)
        out.append([max(results[:6]),max(results[6:])])
    return np.array(out)


def analytic(guide,d0=.5,S=39.):
    qx=cos(acos(QX)+DELTA); x=cos(radians(ANG)+DELTA)
    c=qx-MU*sqrt(1-qx*qx)-guide
    if c<=0:return (np.inf,np.inf)
    jaw=(S+d0)/c
    seat=(3*(S+d0+guide*jaw)+5*.070*9.80665)/(x-MU*sqrt(1-x*x))
    return seat,jaw


if __name__=='__main__':
    width=faces()
    for pair in ((33,39),(33*.90,39*1.10),(42,48)):
        print('true spring band / equivalent midpoint, scatter / axial midpoint needed (service/table/fault)',pair,np.round(springs(*pair),3))
    for k in (0.,.05,.12,.15):
        print('effective axial-guide drag/N / conservative analytic seat,jaw:',k,np.round(analytic(k),2))
        est=reactions(guide=k)
        print('LP seat,jaw service/table/fault:',np.round(est,2))
        if np.all(np.isfinite(est)):
            for F,rx,ry in ((max(est[:,0]),BACK,BACK),(max(est[:,1]),BACK,(RIM+BACK*QR)/QR)):
                a,b,P=hertz(F,rx,ry)
                print('Hertz at outer bound: N,a,b,p0 GPa',np.round([F,a,b,P/1000],4))
            a=hertz(max(est[:,0]),BACK,BACK)[0]
            print('seat tangent margin less trial pole wander and Hertz radius:',round(width-POS-a,4))
