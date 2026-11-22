"""Take 48 exploratory. All coordinates mm. Positive phi rotates about -Y."""
from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('button-bounds-take44.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def pars(L):
    rc=L+.9;gg=.32*L/(rc+.9);lo=log((rc+.22)/(rc+.9))/gg
    return (rc,gg,lo,.54 if L==18 else .50,.62 if L==18 else .56)
def axis(L,k):return (11.5001814182-L,0.,1.28005805+k)
def point(L,k,t,r,y,s=0.):
    x,_,z=axis(L,k);return (x+r*cos(t)-s*sin(t),y,z+r*sin(t)+s*cos(t))
def horn(L,k,opened=0,end=None):
    rc,gg,lo,hi,ph=pars(L);out=[];stop=opened if end is None else end
    # At absolute angle a, outermost disk in union has index min(hi,a-opened).
    for h0,h1 in [(lo+opened,hi+opened),(hi+opened,hi+stop)]:
        if h0==h1:continue
        M=ceil((h1-h0)/.026)
        for j in range(M):
            t0=h0+(h1-h0)*j/M;t1=h0+(h1-h0)*(j+1)/M
            f=(rc+.9)*exp(gg*min(hi,t1-opened))-rc
            rf=f/cos(pi/32);vv=[point(L,k,t,rc+rf*cos(a*pi/16),rf*sin(a*pi/16)) for t,a in product((t0,t1),range(32))]
            out.append(poly('horn '+str(round(t0,4)),vv,(rc+rf)*(1-cos((t1-t0)/2))))
    return out
def sang(L,k,name,stations,phi=0.,end=None):
    """stations=(r, ymid, halfwidth y, s-low, s-high); join successive rectangles."""
    hi=pars(L)[3];end=phi if end is None else end;M=max(1,ceil((end-phi)/.07));out=[]
    for i,(a,b) in enumerate(zip(stations,stations[1:])):
        for j in range(M):
            p=phi+(end-phi)*j/M;q=phi+(end-phi)*(j+1)/M
            vv=[point(L,k,hi+v,r,ym+dy*wy,s) for v,(r,ym,wy,lo,up),dy in product((p,q),(a,b),(-1,1)) for s in (lo,up)]
            out.append(poly(name+str((i,j)),vv,max(hypot(r,s) for r,_,_,l,u in (a,b) for s in (l,u))*(1-cos((q-p)/2))))
    return out
def pivot(L,k,stub=True,phi=0.,end=None):
    x,_,z=axis(L,k);rc,gg,lo,hi,pk=pars(L);a=[]
    for sg in (-1,1):
        yy=lambda lo,hi:tuple(sorted((lo*sg,hi*sg)))
        if stub:a.append(cyl('stub '+str(sg),Y,yy(7.65,16.9),(x,z),1.50))
        a.append(cyl('fork hub '+str(sg),Y,yy(6.70,9.10),(x,z),2.75))
        st=[(0,7.9*sg,1.20,-1.20,1.30),(5.2,7.4*sg,1.20,-1.10,1.30),
            (10.1,6.65*sg,1.15,-.75,1.65),(14.25,3.65*sg,1.15,-.35,1.65),
            (rc,2.20*sg,1.10,-.55,1.40)]
        a.extend(sang(L,k,'spoke'+str(sg),st,phi,end))
    if not stub:a.append(cyl('integral shaft',Y,(-16.90,16.90),(x,z),1.5))
    return a
def house(L,k):
    x,_,z=axis(L,k);a=[]
    for sg in (-1,1):
        yy=lambda lo,hi:tuple(sorted((lo*sg,hi*sg)))
        # Annular bearing tracks and full fixed cheek: keep actual trunnion passage.
        for tag,lo,hi,ri,ro in [('bearing A',9.45,11.95,1.50,3.),('bearing B',13.60,16.1,1.50,3.),('cheek',9.40,16.35,3.,3.80)]:
            for s in ringpart(tag+str(sg)+'/',(x,z),ri,ro,yy(lo,hi),step=30):
                a.append(poly(s[0],[(v[0],v[2],v[1]) for v in s[1]]))
    return a
def allcore(L,k,closed=False,stub=True):
    ph=0 if closed else pars(L)[4]
    return horn(L,k,0,ph)+pivot(L,k,stub,0,ph)+house(L,k)
def bearingproxy(L,k):
    x,_,z=axis(L,k)
    return [cyl('cheek outer'+str(sg),Y,tuple(sorted((sg*9.4,sg*16.35))),(x,z),3.8) for sg in (-1,1)]
def movable(L,k,stub=True):
    return horn(L,k,0,pars(L)[4])+pivot(L,k,stub,0,pars(L)[4])
def ab(s):
    return [proj(s,k) for k in (X,Y,Z)]
def fastpair(A,B):
    # Distinct, fixed separating planes common to all solids; append best-shape axes
    # only for pairs not already separated after a stock allowance.
    ax=BASIC+tuple(unit(d) for d in product((-2,-1,0,1,2),repeat=3) if d>(0,0,0))
    ax=tuple(dict.fromkeys(ax));summary,pairs=[],[]
    def pr(S):
        out=[]
        mat=np.array(ax).T
        for _,v,r,a in S:
            q=np.array(v)@mat
            pad=r if a is None else r*np.sqrt(np.maximum(0,1-(np.array(a)@mat)**2))
            out.append([q.min(0)-pad,q.max(0)+pad])
        return np.array(out)
    pa,pb=pr(A),pr(B)
    for i,s in enumerate(A):
        lo,hi=pa[i];sep=np.maximum(lo-pb[:,1],pb[:,0]-hi).max(1)
        for j,q in enumerate(sep):
            if q<.75:q=max(q,check(s,B[j]))
            pairs.append((float(q),s[0],B[j][0]))
    return sorted(pairs)
def ytest(A,B,step=3,p=0):
    out=[]
    for deg in range(-15,16,step):
        t=[yaw(s,radians(deg),p) for s in B];mp={s[0]:s for s in B}
        for q,n,m in fastpair(A,t):
            e=.20+2*far(mp[m],H)*sin(radians(step/4))
            if q<e+.7:
                z=sep(next(s for s in A if s[0]==n),next(s for s in t if s[0]==m),Z)
                out.append((max(q-e,z-.20),n,m,deg))
    return sorted(out) or [(0.70,'all','separate',0)]
def fp(F):return [sweep(mx(s,REL),(END-REL,0,0)) for s in F]
def report():
    for L,k in product((18.,20.),(0.,-3.,-5.,-7.)):
        x,y,z=axis(L,k);stub=movable(L,k);bear=bearingproxy(L,k)
        full=cyl('integral shaft',Y,(-16.9,16.9),(x,z),1.5)
        a=stub+bear;t=tailshift(36.,k);f=shift(fp(face3()),k);j=tucked_joint()
        print('L/k',L,k,'axis',axis(L,k),'through shaft vs joint/own tail',fastpair([full],j)[:1],ytest([full],t)[:1])
        print('stub core incl housing vs joint / tail / whole face X',fastpair(a,j)[:2],ytest(a,t)[:2],fastpair(a,f)[:3])
if __name__=='__main__':report()
