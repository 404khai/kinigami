"""Adaptive inner/outer certificates of fixed nine-pole Coulomb force peak."""
from geo83 import *
from scipy.optimize import linprog
def optimize(j):
    pts,ns,_=contacts();K=8;t=[list(np.arange(K)*2*pi/K) for _ in ns];basis=[];col=[]
    for p,n in zip(pts,ns):
        u=np.cross(n,X);u/=np.linalg.norm(u);v=np.cross(n,u)
        M=np.array([n,u,v]).T;basis.append(M);col.extend([np.r_[f,np.cross(p,f)] for f in M.T])
    A=np.array(col).T;cap=np.zeros(27);cap[18:]=-A[0,18:];b=boxes['table']
    lo=np.r_[b[0],-np.array(b[2:])];hi=np.r_[b[1],b[2:]];mx=[]
    def solve(inner):
        G=[]
        for i,angs in enumerate(t):
            a=np.unique(np.sort(np.remainder(angs,2*pi)));M=len(a)
            for k,al in enumerate(a):
                be=a[(k+1)%M]+(2*pi if k==M-1 else 0);phi=(al+be)*.5 if inner else al
                g=np.zeros(27);g[3*i:3*i+3]=[-mu*(cos((be-al)/2) if inner else 1),cos(phi),sin(phi)];G.append(g)
        c=np.zeros(27);c[3*j]=-1
        r=linprog(c,A_ub=np.vstack([A,-A,cap,G]),b_ub=np.r_[-lo,hi,45,np.zeros(len(G))],bounds=[(0,None),(None,None),(None,None)]*9,
            options=dict(primal_feasibility_tolerance=1e-9,dual_feasibility_tolerance=1e-9),method='highs');assert r.success,r.message
        return r
    for k in range(100):
        l=solve(True);h=solve(False)
        if l.fun-h.fun<1e-6:break
        for i in range(9):
            for f in (l.x,h.x):
                tx,ty=f[i*3+1:i*3+3]
                if hypot(tx,ty)>1e-6:t[i].append(atan2(ty,tx))
    assert l.fun-h.fun<1e-6
    return dict(low=-l.fun,high=-h.fun,external=(-A@l.x).tolist(),normals=l.x[::3].tolist(),iterations=k+1)
if __name__=='__main__':print(json.dumps(dict(label='exploratory',contacts={str(i):optimize(i) for i in [6,7,8]}),indent=2))
