"""Upper LP: full fixed-axis parallel, non-pinched flat-land breakaway model."""
from pull83 import *
def ceiling():
    # Actual aligned crowned poles, unknown tangential center (+/-.060) and
    # sleeve offset up to .05. Tail/cage contact normals remain nominal in this
    # branch. Allow full plane availability, opposing thrusts (relaxation) BUT
    # cannot include both ends in opposition at any one station: finite endplay.
    # Branches with no endcaps: correct for a common offset of tail/sleeve AND
    # rollers as used in pull83; max common .050 < .060. Omit no reactions
    # from this model. Do not claim this covers diagonal/other cage states.
    C=[];P=[];A=[];U=[]
    def add(v,c=0,p=0,u=None):A.append(v);C.append(c);P.append(p);U.append(np.zeros(3) if u is None else u)
    ps,ns,cs=contacts()
    for j in range(6):
        for f in rays(ns[j],True):
            v=np.zeros(24);v[:6]=wrench(ps[j],f);add(v)
    for i,a in enumerate(np.arange(3)*2*pi/3):
        B=np.array([X,[0,cos(a),sin(a)],[0,-sin(a),cos(a)]]).T
        cen=(-4.22*X+r0*B[:,1])
        for k,m,qs in [('t',(X+Y)*c45,[-1.5*(X+Y)*c45]),('s',-Y,[1.5*Y]),('w',-X,[.5*X+j*Z for j in [-3.34,3.34]])]:
            for q in qs:
                for f in ([-Y-mu*X] if k=='s' else rays(m,True)):
                    v=np.zeros(24);v[6+i*6:12+i*6]=wrench(q,f);F=B@f
                    if k=='t':v[:6]=wrench(cen+B@q,-F)
                    add(v,c=-F[0] if k=='w' else 0,p=F[0] if k=='t' else 0,u=np.eye(3)[i] if k=='s' else None)
    A=np.array(A).T;U=np.array(U).T;K=24
    E=np.c_[np.cos(np.arange(3)*2*pi/3),np.sin(np.arange(3)*2*pi/3)]
    out={}
    for cap in ['tail45','cage45']:
        for k,box in boxes.items():
            lo=np.r_[box[0],-np.array(box[2:])];hi=np.r_[box[1],box[2:]]
            best=0
            for a in np.arange(K)*2*pi/K:
                vel=(1+E@np.array([cos(a),sin(a)])/cos(pi/K))@U
                lp=linprog(-mu*vel,A_eq=A[6:],b_eq=np.zeros(18),A_ub=np.vstack([A[:6],-A[:6],P if cap=='tail45' else C]),
                    b_ub=np.r_[-lo,hi,45],method='highs')
                assert lp.success
                best=max(best,-lp.fun)
            out[cap+'_'+k]=best
    return dict(label='exploratory',parallel_common_offset_flat_land_upper_N=out,polygon_sides=12,norm_facets=K)
if __name__=='__main__':print(json.dumps(ceiling(),indent=2))
