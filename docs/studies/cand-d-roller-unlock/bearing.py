"""Explicit eccentric sleeve guide contacts (no empirical drag multiplier)."""
from roller import *
def aligned():
    A=[]; ids=[]; pull=[]; xshift=.0015; d=xshift*X+.050*Y
    def add(k,tail=None,roll=None,i=None,sleeve=None,draw=0):
        col=np.zeros(30)
        if tail is not None:col[:6]=tail
        if roll is not None:col[6+6*i:12+6*i]=roll
        if sleeve is not None:col[-6:]=sleeve
        ids.append(k); A.append(col);pull.append(draw)
    p,n=b.build_contacts(); gaps=n[:6]@d
    for j in range(6):
        if gaps[j]>.025:continue
        assert gaps[j]>=-(.045 if j==0 else .025)
        for f in rays(n[j]):add('v'+str(j),tail=wrench(p[j],f))
    for j in range(3):
        a=2*pi*j/3; B=np.array([X,[0,cos(a),sin(a)],[0,-sin(a),cos(a)]]).T
        cen=B@np.array([-4.22+xshift,b.R_KLOCK+.02+.05*cos(a),0.030])
        for k,m in [('tail',(X+Y)/sqrt(2)),('cage',-X),('side',-Z),('sleeve',-Y)]:
            for q in supports(Z,m):
                for f in ([m-mu*X] if k=='sleeve' else rays(m)):
                    F=B@f; pos=cen+B@q
                    add(k+str(j),tail=wrench(pos-d,-F) if k=='tail' else None,
                        roll=wrench(q,f),i=j,sleeve=wrench(pos,-F) if k=='sleeve' else None,
                        draw=F[0] if k=='tail' else 0)
    for g in [-14.3,-6.85]:
        add('guide'+str(g),sleeve=wrench(g*X+9.65*Y,-Y+mu*X))
    add('drive',sleeve=wrench(.05*Y,-X))
    A=np.array(A).T; ids=np.array(ids); pull=np.array(pull)
    out={}
    boxes={k:(np.r_[v[0],-np.array(v[2:])],np.r_[v[1],v[2:]]) for k,v in b.BOXES.items()}
    boxes.update({k:(np.array(w),np.array(w)) for k,w in [('plus4W',[4*b.W]+[0]*5),('minus20',[-20]+[0]*5),('Mz52',[0]*5+[52.2])]})
    for single in (False,True):
      for k,(lo,hi) in boxes.items():
        k+=("_one_roller" if single else "")
        R=linprog(-(ids=='drive').astype(float),A_ub=np.vstack([A[:6],-A[:6],pull]),b_ub=np.r_[-lo,hi,45],
            A_eq=A[6:],b_eq=np.zeros(24),bounds=[(0,0 if single and tag in ('tail1','tail2','sleeve1','sleeve2') else None) for tag in ids],method='highs')
        if R.success:
            z=R.x;out[k]={'external':(-A[:6]@z).tolist(),'sleeve_puller_N':-R.fun,'normal':{tag:sum(z[ids==tag]) for tag in sorted(set(ids))},'tail_draw':pull@z,'roller_and_sleeve_residual':max(abs(A[6:]@z))}
        else:out[k]=None
    return {'label':'exploratory','cases':out,'seat_signed_plane_adjustment':gaps.tolist()}
if __name__=='__main__':print(json.dumps(aligned(),indent=2))
