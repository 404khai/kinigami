"""Local finite cylinder contact cones and coupled incipient sleeve breakaway."""
from itertools import product
from math import *
import json
import numpy as np
from scipy.optimize import linprog, brentq
import take80 as b

X,Y,Z=np.eye(3); mu=.23; K=12
zero=np.zeros(3)
def wrench(q,f):return np.r_[f,np.cross(q,f)]
def basis(n):
    v=np.cross(n,np.eye(3)[np.argmin(abs(n))]); v/=np.linalg.norm(v)
    return v,np.cross(n,v)
def rays(n,outer=False):
    l,h=basis(n)
    return [n+mu/(cos(pi/K) if outer else 1)*(cos(i*2*pi/K)*l+sin(i*2*pi/K)*h) for i in range(K)]
def supports(u,n,outer=False):
    """Cylinder points MINIMIZING n.p for inward normal n. Exact or inner/outer polygon on end."""
    a=u@n; q=n-a*u
    if np.linalg.norm(q)<1e-9:
        l,h=basis(u)
        return [-1.5*np.sign(a)*u+1.5/(cos(pi/8) if outer else 1)*(cos(i*pi/4)*l+sin(i*pi/4)*h) for i in range(8)]
    q=-1.5*q/np.linalg.norm(q)
    return [q+1.5*s*u for s in ((-1,1) if abs(a)<1e-9 else (-np.sign(a),))]
def orientations():
    a=brentq(lambda a:3*(cos(a)+sin(a))-3.05,0,.1)
    t=brentq(lambda a:3*(cos(a)+sin(a))-3.06,0,.1)
    for ax in (0,a/2,a,-a):
        for ang in (abs(ax),(abs(ax)+t)/2,t):
            dx=sin(ax); dt=cos(ang); dr=sqrt(max(0,1-dt*dt-dx*dx))
            for rr in set([round(dr,12),round(-dr,12)]):
                u=np.array([dx,rr,dt])
                yield u,abs(abs(ax)-a)<1e-8,abs(ang-t)<1e-8
def local(u,both_x,both_z,angle,side,outer):
    n=(X+Y)/sqrt(2)
    groups=[('tail',n),('wall',-X),('side',side*Z)]
    if both_x:groups.append(('wall',X))
    if both_z:groups.append(('side',-side*Z))
    if angle is not None:groups.append(('sleeve',sin(angle)*X-cos(angle)*Y))
    A=[]; cats=[];cost=[]
    for k,m in groups:
        for q in supports(u,m,outer):
            for f in rays(m,outer):
                A.append(wrench(q,f)); cats.append(k);cost.append(-f[0] if k=='sleeve' else 0)
    A=np.array(A).T; cats=np.array(cats)
    ret=linprog(-np.array(cost),A_eq=np.vstack([A,cats=='tail']),b_eq=[0]*6+[1],method='highs')
    if ret.status==2:return None
    assert ret.success,(ret.message,u,angle)
    return dict(f_per_N=-ret.fun,normal={k:sum(ret.x[cats==k]) for k in set(cats)},res=max(abs(A@ret.x)))
def local_sweep():
    out={}; axes=list(orientations())
    for deg in (0,8,20,45,None):
        best=None; count=0
        for u,bx,bz in axes:
            for z in ((1,) if bz else (-1,1)):
                R=local(u,bx,bz,None if deg is None else radians(deg),z,True)
                if R is not None:
                    count+=1
                    if best is None or best['f_per_N']<R['f_per_N']:
                        best=dict(**R,axis=u.tolist(),both_axial=bx,both_side=bz,side_sign=z)
        out[str(deg)]=dict(feasible=count,max_outer=best)
    return out
def assembly():
    # take outer pressure offsets at both ends of each roller generator.
    # Roller stationary, sleeve moving aft at breakaway. Side face (+t)
    # touched at each of the three stations with .030 mm clearance takeup.
    cols=[]; norms=[]; classes=[]; pull=[]; drag=[]
    side=1
    def add(k,idx,tail,roll,draw,s):
        a=np.zeros(24); a[:6]=tail
        if idx>=0:a[6+idx*6:12+idx*6]=roll
        cols.append(a); classes.append(k); pull.append(draw); drag.append(s)
    p,n=b.build_contacts()
    for j in range(6):
        for f in rays(n[j]):add('v',-1,wrench(p[j],f),None,0,np.zeros(4))
    for j in range(3):
        a=2*pi*j/3; B=np.array([X,[0,cos(a),sin(a)],[0,-sin(a),cos(a)]]).T
        cen=B@np.array([-4.22,b.R_KLOCK+.02,.030*side])
        for k,m in [('tail',(X+Y)/sqrt(2)),('cage',-X),('side',-side*Z),('sleeve',-Y)]:
            for q in supports(Z,m):
                for f in ([m-mu*X] if k=='sleeve' else rays(m)):
                    F=B@f; pos=cen+B@q
                    add(k+str(j),j,wrench(pos,-F) if k=='tail' else np.zeros(6),
                        wrench(q,f),F[0] if k=='tail' else 0,
                        np.r_[mu,B@Y] if k=='sleeve' else np.zeros(4))
    A=np.array(cols).T; D=np.array(drag).T; P=np.array(pull); C=np.array(classes); out={}
    # Wrench may range ANYWHERE inside box; no corners-only assumption.
    boxes={k:(np.r_[v[0],-np.array(v[2:])],np.r_[v[1],v[2:]]) for k,v in b.BOXES.items()}
    boxes.update({k:(np.array(w),np.array(w)) for k,w in [('plus4W',[4*b.W]+[0]*5),('minus20',[-20]+[0]*5),('Mz52',[0]*5+[52.2])]})
    for k,(lo,hi) in boxes.items():
        best=0; data=None
        for ang in np.arange(12)*pi/6:
            axis=np.array([0,cos(ang),sin(ang)])
            obj=D[0]+mu*axis@D[1:]
            R=linprog(-obj,A_ub=np.vstack([A[:6],-A[:6],P]),b_ub=np.r_[-lo,hi,45],A_eq=A[6:],b_eq=np.zeros(18),method='highs')
            if not R.success:continue
            z=R.x; s=D@z; necessary=s[0]+mu*np.linalg.norm(s[1:])
            if necessary>best:
                best=necessary
                data=dict(w=(-A[:6]@z).tolist(),draw=P@z,roller_tails=[sum(z[C=='tail'+str(j)]) for j in range(3)],
                    cage_walls=[sum(z[C=='cage'+str(j)]) for j in range(3)],side_ends=[sum(z[C=='side'+str(j)]) for j in range(3)],
                    sleeve_normals=[sum(z[C=='sleeve'+str(j)]) for j in range(3)],roller_res=max(abs(A[6:]@z)),
                    direct=s[0],guide_min=necessary-s[0],necessary_total=necessary)
        out[k]=data
    return out
if __name__=='__main__':
    print(json.dumps(dict(label='exploratory',coupled_flat=assembly(),skew_local_outer=local_sweep()),indent=2,sort_keys=True))
