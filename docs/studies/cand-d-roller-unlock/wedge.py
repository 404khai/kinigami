"""Outer LP interval cover of the small-skew component for a free roller."""
from roller import *
def cub(lo,hi):
    return [np.array(q) for q in product(*[(a,b) if a!=b else (a,) for a,b in zip(lo,hi)])]
def check(psi,rad,sgn,zero_x=False):
    # n=+X exact support has x in [-1.526,-1.5], |y|<=.0315, t opposes u_x.
    # n=+Z support projected into xy is 1.5(cos(theta)-sin(theta))*(cos psi,sin psi).
    # Hence each component stays within .032+1.5*rad of midpoint direction.
    T=radians(1.2); err=.032+1.5*rad
    xy=1.5*np.array([cos(psi),sin(psi)])
    sx=cub([-1.526,-.033,-1.5 if zero_x else -1.501],[-1.499,.033,1.5 if zero_x else -1.44])
    if not zero_x and sgn<0:sx=[v*np.array([1,1,-1]) for v in sx]
    sz=cub([*(xy-err),-1.531],[*(xy+err),-1.499])
    # any single contact or distribution on actual end/edges; independent
    # tail application point in containing box; relative normal error 2 deg.
    sets=[('tail',(X+Y)/sqrt(2),cub([-1.526,-1.54,-1.531],[1.526,1.54,1.531])),
          ('s+',Z,sz),('s-',-Z,[-v for v in sz])]
    ax=[('x+',X,sx),('x-',-X,[-v for v in sx])]
    margins=[]
    for axset in ([ax] if not zero_x else [[ax[0]],[ax[1]]]):
        A=[]; fid=[]
        for k,n,points in sets+axset:
            D=rays(n,True)
            if k=='tail':
                D=[n+(v-n)*tan(atan(mu)+radians(2))/mu for v in D]
            for q in points:
                for f in D:
                    A.append(wrench(q,f)); fid.append(k=='tail')
        A=np.array(A)
        R=linprog([0]*6+[-1],A_ub=np.c_[-A,np.ones(len(A))],b_ub=np.zeros(len(A)),bounds=[(-1,1)]*6+[(None,None)],method='highs')
        assert R.success
        margins.append(float(np.min(A@R.x[:6])))
    return min(margins)
def cover():
    m=64
    ok=[]; bad=[]
    for k in range(m):
        psi=2*pi*(k+.5)/m; good=check(psi,pi/m,1 if cos(psi)>0 else -1)
        (ok if good>1.e-7 else bad).append((k,good))
    for psi in (pi/2,3*pi/2):
        good=check(psi,0,1,True);(ok if good>1.e-7 else bad).append((degrees(psi),good))
    return dict(label='exploratory',azimuth_cells=m,strictly_separated=len(ok),min_dual_margin=min(x[1] for x in ok),inconclusive_cells=bad)
if __name__=='__main__': print(json.dumps(cover(),indent=2))
