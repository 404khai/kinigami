"""Continuous direction/band pressure cover: full two-band reactions, 30 balances."""
from pull83 import *
def upper(reset=0.,key_sign=0):
    K=48;D=pi/K;p,n,c=contacts();A=[];C=[];P=[];face=[]
    def add(tag,v,c=0,p=0):A.append(v);C.append(c);P.append(p);face.append(tag)
    for j in range(6):
        for f in rays(n[j],True):
            v=np.zeros(30);v[:6]=wrench(p[j],f);add(j,v)
    for j,a in enumerate(np.arange(3)*2*pi/3):
        B=np.array([X,[0,cos(a),sin(a)],[0,-sin(a),cos(a)]]).T; cen=-4.22*X+r0*B[:,1]
        for k,m,qs in [('t',(X+Y)*c45,[-1.5*(X+Y)*c45]),('s',-Y,[1.5*Y]),('w',-X,[.5*X+j*Z for j in [-3.34,3.34]])]:
            for q in qs:
                for f in ([-Y-mu*X] if k=='s' else rays(m,True)):
                    F=B@f; v=np.zeros(30);v[6+j*6:12+j*6]=wrench(q,f)
                    if k=='t':v[:6]=wrench(cen+B@q,-F)
                    if k=='s':v[-6:]=wrench(cen+(.0015+reset)*X+B@q,-F)
                    add(-1,v,-F[0] if k=='w' else 0,F[0] if k=='t' else 0)
    F=np.zeros(30);F[-6]=-1
    rho=(18-.649519*.5)/2;F[-3]=key_sign*rho*tan(atan(.5/(2*pi*rho))+atan(mu/cos(pi/6)))
    index=len(A);add(-1,F)
    if key_sign:
        # All leading torque flanks available; no equal sharing. Independent
        # extrema in relative seat position include the .05 offset of sleeve.
        # This branch assumes no opposing/key-root preload. Nominal flat
        # roller/tail normals are conditional; no roll-error allowance here.
        for s in np.radians([30,150,270]):
            er=cos(s)*Y+sin(s)*Z;et=np.cross(X,er)
            f=-key_sign*et+mu*X
            for x,r,t in product([-15.83,-15.45],[8.64-.05,9.77+.05],[-.39-.05,.39+.05]):
                v=np.zeros(30);v[-6:]=wrench(x*X+r*er+t*et,f);add(-1,v)
    out={}; cells=0
    for i in range(-1,K):
        # -1: coaxial or offset <.050, no loaded band. All Vs allowed.
        a=i*2*D;d=Y*cos(a)+Z*sin(a);z=np.cross(X,d);As=A.copy();Cs=C.copy();Ps=P.copy()
        lim=[(0,None)]*len(As)
        if reset and i<0:
            for j,tag in enumerate(face):
                if tag>=0:lim[j]=(0,0) # even at worst .05 transverse shift, all gaps >.025
        if i>=0:
            gap=n[:6]@(.05*d+(.0015+reset)*X);delta=2*.05*sin(D/2)*np.linalg.norm(n[:6,1:],axis=1)
            if min(gap+delta)<-.045 or sum(gap+delta<-.025)>1:continue
            for j,tag in enumerate(face):
                if tag>=0 and (gap-delta)[tag]>.025:lim[j]=(0,0)
            cells+=1
            for x,b,e in product([-14.90,-13.70,-7.45,-6.25],[cos(D),1],[-sin(D),sin(D)]):
                # convex box encloses all unit radial directions in this cell.
                t=d*b+z*e;v=np.zeros(30);v[-6:-3]=-t+mu*X
                v[-3:]=-(x+9.60*mu)*np.cross(X,t)
                As.append(v);Cs.append(0);Ps.append(0);lim.append((0,None))
        M=np.array(As).T
        obj=np.zeros(len(As));obj[index]=-1
        for cap,caprow in [('tail45',Ps),('cage45',Cs)]:
            for k,v in boxes.items():
                lo=np.r_[v[0],-np.array(v[2:])];hi=np.r_[v[1],v[2:]]
                R=linprog(obj,A_eq=M[6:],b_eq=np.zeros(24),A_ub=np.vstack([M[:6],-M[:6],caprow]),
                    b_ub=np.r_[-lo,hi,45],bounds=lim,method='highs');assert R.success
                name=cap+'_'+k;out[name]=max(out.get(name,0),-R.fun)
    return dict(label='exploratory',eligible_azimuth_cells=cells,K=K,continuous_parallel_flat_upper=out)
if __name__=='__main__':print(json.dumps(dict(loaded=upper(),reset=upper(.20),keyed_positive=upper(0,1),keyed_negative=upper(0,-1),keyed_reset_positive=upper(.20,1),keyed_reset_negative=upper(.20,-1)),indent=2))
