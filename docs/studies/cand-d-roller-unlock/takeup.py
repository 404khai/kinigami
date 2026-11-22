"""Positive cage-driving load; stationary sleeve, NOT 45 N at the tail."""
from roller import *
def main():
    cols=[]; charge=[]; pull=[]; drag=[]
    def add(k,tail=None,roll=None,i=None,draw=0,s=0):
        a=np.zeros(24)
        if tail is not None:a[:6]=tail
        if roll is not None:a[6+6*i:12+6*i]=roll
        cols.append(a);charge.append(k);pull.append(draw);drag.append(s)
    p,n=b.build_contacts()
    for j in range(6):
        for f in rays(n[j]):add(j,wrench(p[j],f))
    for j in range(3):
        a=2*pi*j/3; B=np.array([X,[0,cos(a),sin(a)],[0,-sin(a),cos(a)]]).T
        cen=B@np.array([-4.22,b.R_KLOCK+.02,0])
        # Side face not needed for this moving no-spin branch.
        for k,m in [('tail',(X+Y)/sqrt(2)),('cage',-X),('sleeve',-Y)]:
            for q in supports(Z,m):
                for f in ([m+mu*X] if k=='sleeve' else rays(m)):
                    F=B@f; pos=cen+B@q
                    add(j+6 if k=='tail' else -1,wrench(pos,-F) if k=='tail' else None,
                        wrench(q,f),j,F[0] if k=='tail' else 0,mu if k=='sleeve' else 0)
    A=np.array(cols).T; P=np.array(pull); D=np.array(drag); ids=np.array(charge)
    C=np.array([-(ids==j).astype(float) for j in range(9)])
    out={}
    for k,v in b.BOXES.items():
        peak=-1
        for w in product((v[0],v[1]),*[(-h,h) for h in v[2:]]):
            R=linprog(P+D,A_eq=A,b_eq=np.r_[-np.array(w),np.zeros(18)],
                      A_ub=C,b_ub=[-.10]*9,method='highs')
            assert R.success
            if R.fun>peak:
                peak=R.fun;out[k]=dict(cage_drive=peak,draw=P@R.x,slide=D@R.x,w=w,
                    margin_to_45=45-peak,least_charge=min(-C@R.x))
    R=linprog(-(ids==6).astype(float),A_eq=np.vstack([A,P+D]),b_eq=np.r_[np.zeros(24),45],
            bounds=[(0,0 if idx==0 else None) for idx in ids],method='highs')
    assert R.success
    return dict(label='exploratory',conditional_corner_min_cage_drive=out,
        missing_face_020_at_true_45N=dict(external=[0]*6,tail_draw=P@R.x,sleeve_drag=D@R.x,
        physical_cage_pull=(P+D)@R.x,charges=[sum(R.x[ids==j]) for j in range(9)],residual=max(abs(A@R.x))))
if __name__=='__main__':print(json.dumps(main(),indent=2))
