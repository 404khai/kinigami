"""Convex material/outer stock records; world mm. No lace mechanism."""
from math import *
from itertools import product
import numpy as np
from scipy.optimize import minimize,linprog
from scipy.spatial import ConvexHull
sh=lambda v:tuple(map(float,v))
def sol(n,v,r=0.,d=None):return n,[sh(q) for q in v],float(r),None if d is None else sh(d)
def bx(n,x,y,z):return sol(n,product(x,y,z))
def cy(n,ax,span,cen,r):
    v=[]
    for t in span:
        a=list(cen);a.insert(ax,t);v.append(a)
    return sol(n,v,r,np.eye(3)[ax])
def rod(n,a,b,r):return sol(n,[a,b],r)
def yz(name,r0,r1,x0,x1,y,z,step=16):
    a=[]
    for i in range(step):
        ts=[2*pi*j/step for j in (i,i+1)]
        a.append(sol(name+str(i),[(x,y+rr*cos(t),z+rr*sin(t)) for t,x,rr in product(ts,(x0,x1),(r0,r1/cos(pi/step)))]))
    return a
def trans(s,v):
    return sol(s[0],np.array(s[1])+v,s[2],s[3])
def rot(s,t,o):
    c=cos(t);v=sin(t);m=np.array([[c,-v,0],[v,c,0],[0,0,1]])
    return sol(s[0],(np.array(s[1])-o)@m.T+o,s[2],None if s[3] is None else m@s[3])
def ext(s,d):
    a=np.array(s[1])@d.T;r=s[2]*(1 if s[3] is None else np.sqrt(np.maximum(0,1-(np.array(s[3])@d.T)**2)))
    return a.min(0)-r,a.max(0)+r
ds=np.array([u for u in product(range(-2,3),repeat=3) if u>(0,0,0) and gcd(gcd(abs(u[0]),abs(u[1])),abs(u[2]))==1],float);ds/=np.linalg.norm(ds,axis=1)[:,None]
def extlist(S):return np.array([ext(s,ds) for s in S])
def pairs(a,b,ea=None,eb=None):
    aa=extlist(a) if ea is None else ea;bb=extlist(b) if eb is None else eb
    gap=np.maximum(aa[:,0,None,:]-bb[None,:,1,:],bb[None,:,0,:]-aa[:,1,None,:]).max(2)
    i,j=np.unravel_index(np.argmin(gap),gap.shape);return float(gap[i,j]),a[i][0],b[j][0]
def far(s,c):
    v=np.array(s[1])-c;r=s[2];n=np.linalg.norm(v,axis=1)
    if s[3] is None:return max(n)+r
    v1=v@np.array(s[3]);return max(np.sqrt(v1**2+(np.sqrt(np.maximum(0,n**2-v1**2))+r)**2))
def enc(S):
    # Enclose solid sets by using exact vertex/ball or disk support at fixed
    # centre (optimizer only improves the upper bound, no lower claim).
    def f(x):return max(far(s,x) for s in S)
    q=minimize(f,[-2.,.2,-.6],method='Nelder-Mead',options={'maxiter':170,'xatol':.005,'fatol':.005})
    return sh(q.x),2*f(q.x),sorted([(far(s,q.x),s[0]) for s in S],reverse=True)[:3]
def polyin(s):
    n,v,r,d=s;v=np.asarray(v)
    if r==0:return v
    if d is None:
        # inscribed balls, hence hull of inner support for capsules
        u=ds
    else:
        d=np.array(d);a=np.eye(3)[np.argmin(abs(d))];aa=np.cross(d,a);aa/=np.linalg.norm(aa);bb=np.cross(d,aa);u=np.array([cos(t)*aa+sin(t)*bb for t in np.arange(32)*pi/16])
    return (v[:,None,:]+r*np.concatenate((u,-u))[None,:,:]).reshape(-1,3)
def ball(s,t):
    m=np.r_[ConvexHull(polyin(s)).equations,ConvexHull(polyin(t)).equations]
    w=linprog([0,0,0,-1],np.c_[m[:,:3],np.ones(len(m))],-m[:,3],bounds=[(None,None)]*4,method='highs').x
    return w
