"""Vertex enclosure and jointly optimized noncorner 6D wrench."""
from geo83 import *
from itertools import combinations
from scipy.optimize import linprog
def closure(extra):
    p,n,c=contacts();r=np.linalg.norm(c,axis=1);A=np.c_[n,np.cross(c,n)/8.2];B=rad(1.4);H=.27
    E=np.array([.025]*6+[.040]*3);E[0]+=extra
    # crowned ends; central full-radius tangent to a 1.5 insphere (see Hertz script)
    e=E+2*np.sin(np.radians([.6]*6+[1]*3)/2)*H+(1-cos(B))*r
    e[6:]+=2*sin(B/2)*H
    pos=linprog(np.ones(9),A_eq=A.T,b_eq=np.zeros(6),bounds=(1,None),method='highs')
    assert pos.success and np.linalg.matrix_rank(A)==6 and max(abs(A.T@pos.x))<1e-10
    v=[]
    for j in combinations(range(9),6):
        a=A[list(j)]
        if abs(np.linalg.det(a))<1e-9:continue
        z=np.linalg.solve(a,-e[list(j)])
        if min(A@z+e)>-1.e-9:v.append(z)
    angle=asin(max(np.linalg.norm(z[3:]) for z in v)/8.2)
    u=np.max([np.linalg.norm(z[:3]+np.cross(z[3:]/8.2,c),axis=1) for z in v],axis=0)+(1-cos(angle))*r
    assert max(u)<H and angle<B
    return dict(positive_spanning=pos.x.tolist(),vertices=len(v),travel=max(np.linalg.norm(z[:3]) for z in v),angle=degrees(angle),station_disp=u.tolist(),
        V_reserve=.45-.06-max(u[:6])-1.5*sin(rad(.6))-.025,
        shoulder_normal_section_reserve=.65*sqrt(2)-max(u[6:])-.025-1.5*sin(angle+rad(2.2))-.06,
        shoulder_lateral_reserve=sqrt(4.60**2-(3.85+(max(u[6:])+.15)/sqrt(2))**2)-1.5-max(u[6:])-.15)
def pole(mu,drop=-1):
    p,n,c=contacts(); cols=[];draw=[];ids=[]
    for i,N in enumerate(n):
        l=np.cross(N,X);l/=np.linalg.norm(l)
        for a in np.arange(24 if mu else 1)*2*pi/24:
            f=N+mu*(cos(a)*l+sin(a)*np.cross(N,l))
            cols.append(np.r_[f,np.cross(p[i],f)]);ids.append(i);draw.append(-f[0] if i>=6 else 0)
    A=np.array(cols).T; ids=np.array(ids); P=np.array(draw)
    out={}
    for k,v in dict(boxes,zero=(0,)*7).items():
        lo=np.r_[v[0],-np.array(v[2:])];hi=np.r_[v[1],v[2:]]
        best=None
        for j in (6,7,8):
            R=linprog(-(ids==j).astype(float),A_ub=np.vstack((A,-A,P)),b_ub=np.r_[-lo,hi,45],
                bounds=[(0,0 if i==drop else None) for i in ids],method='highs')
            if R.success and (best is None or -R.fun>best['peak']):
                best=dict(peak=-R.fun,draw=P@R.x,w=(-A@R.x).tolist(),normals=[sum(R.x[ids==q]) for q in range(9)])
        out[k]=best
    return out
if __name__=='__main__':
    print(json.dumps(dict(label='exploratory',closure=closure(0),extra_020=closure(.020),normal=pole(0),dry_inner=pole(.23),dry_outer=pole(.23/cos(pi/24)),missing=pole(0,0)),indent=2))
