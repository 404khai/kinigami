"""Take 48, own and adjacent package, nominal lower certificates. mm/N/Nmm."""
from pathlib import Path
from runpy import run_path
g=run_path(str(Path(__file__).with_name('horn-install-take48.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
from itertools import permutations,combinations
from scipy.spatial import ConvexHull
from scipy.optimize import minimize,nnls
def fixed48():return joint48()+xfixed()+drive()+indexdog()+che5()+hoodoutside()+duct()
def moving(n):
    phi=0 if n=='C' else pk
    return horn(L,0,phi)+fork5(phi)+lever(phi)
def packageElec():
    c=box('cell',(-19.33,11.33),(-4.75,15.95),(-22.10,-16.70))
    return [c]+[s for s in electr() if s[0].startswith('foot')]+boards()
def boards():
    return [bnew(n,c,d) for n,c,d in [
        ('MCU',(-3.5,23.,-.5),(17.8,5.7,22.)),
        ('joint+X driver',(-5.,-10.,-6.5),(9.8,8.8,1.87)),
        ('Z driver',(1.,-13.,-.5),(2.05,5.8,6.2)),
        ('power cutoff',(-9.5,-1.,-12.5),(6.2,6.85,1.95)),
        ('cell connector',(1.,5.,-2.),(2.8,3.35,2.9)),
        ('harness channel',(-3.5,6.5,-5.),(3.4,2.,3.))]]
def bnew(n,c,d):return box(n,*[(x-h/2,x+h/2) for x,h in zip(c,d)])
def boardsearch():
    """Conservative coarse placement search; every accepted hit has a SAT axis for each stock."""
    t=tail48()
    A=fixed48()+fp(face3()+xmove())+horn(L,0,0,pk)+fork5(0,pk)+lever(0,pk)+packageElec()[:5]
    A.extend(yaw(s,radians(i)) for i in range(-15,16,3) for s in t)
    A.extend(sweep(s,(END,0,0)) for s in tail48(0) if s[0].startswith(('eye','heavy','boss')))
    d=np.array([(1,0,0),(0,1,0),(0,0,1)]+[unit(v) for v in product((-1,0,1),repeat=3) if v>(0,0,0) and v.count(0)<2])
    def projA(A):
        return np.array([[proj(s,tuple(e)) for e in d] for s in A])
    proj0=projA(A)
    for old in [s for s in electr() if s[0]!='cell' and not s[0].startswith('foot')]:
        name=old[0];dims=tuple(round(b-a,4) for a,b in ab(old));trial=[]
        for dims in sorted(set(permutations(dims))):
            h=np.array(dims)*.5;pad=abs(d)@h
            grid=np.array(list(product(np.arange(-23,17,1.5),np.arange(-22,24,1.5),np.arange(-21.5,23.6,1.5))))
            radii=np.linalg.norm(np.abs(grid-[-4,-2,0])+h,axis=1)
            ix=np.argsort(radii)
            ix=ix[(radii[ix]<min(33.,trial[-1][0] if trial else 33.)) & (grid[ix,2]-h[2]>=-23.45)]
            mids=grid[ix]@d.T
            for lo,hi in zip(proj0[:,:,0],proj0[:,:,1]):
                valid=np.any((mids+pad+.75<lo)|(mids-pad-.75>hi),axis=1)
                mids=mids[valid];ix=ix[valid]
                if not len(ix):break
            if len(ix):
                i=ix[0];mid=mids[0];gap=np.maximum(proj0[:,:,0]-(mid+pad),(mid-pad)-proj0[:,:,1]).max(1)
                trial.append((radii[i],list(grid[i]),dims,gap.min()))
        if trial:
            rad,c,ds,margin=trial[-1];print(name,c,ds,margin,rad,flush=True);proj0=np.concatenate((proj0,projA([bnew(name,c,ds)])))
        else:print(name,'NO GRID PLACEMENT',flush=True)
def actualpoints(k):
    # Material interiors: not sector addendum disks, swept hulls, circumscribed
    # torus chords, uncut blanks, or envelope corners of a part with holes.
    a=[]
    for s in packageElec()+joint48()+shift(xfixed()+xmove()+drive(),k):
        n,v,r,ax=s
        if n in ('cell','MCU','X rail','X guide mounting beam') or n.startswith('foot'):
            a.extend((n,q) for q in v)
        if n in ('yaw gearmotor','horn gearmotor','X gearmotor'):
            for q in v:
                for i in range(36):
                    vv=np.roll([0,r*cos(radians(i*10)),r*sin(radians(i*10))],np.argmax(np.abs(ax)))
                    a.append((n,tuple(np.array(q)+vv)))
    for theta in np.linspace(-2.,182.,93):
        t=radians(theta);q=np.array(path(t));v=np.array(path(t+1e-7))-np.array(path(t-1e-7));n=np.array((v[1],-v[0]))/np.linalg.norm(v)
        if n@q<0:n=-n
        # Halfway through the outer flank; rear web at y=-23.5 is also solid.
        q=q+n*2.835+C48;a.append(('cam rear web',(q[0],-23.5,q[1]+k)))
    for t in np.linspace(0,2*pi,90,endpoint=False):
        q=(15-P+(R+r)*cos(t),(R+r)*sin(t),k);a.append(('true own torus',q))
    return a
def certify(points):
    # Any convex-weighted variance is a rigorous lower bound, even when the
    # numerical enclosing-ball trial centre is suboptimal.
    p=np.array([q for _,q in points]);ix=ConvexHull(p).vertices;h=p[ix]
    res=minimize(lambda x:x[3],[-4,-2,0,1100.],jac=lambda x:[0.,0.,0.,1.],constraints=[dict(type='ineq',fun=lambda x:x[3]-((h-x[:3])**2).sum(1),jac=lambda x:np.c_[2*(h-x[:3]),np.ones(len(h))])],method='SLSQP',options={'ftol':1e-9})
    o=res.x[:3];dist=np.linalg.norm(h-o,axis=1);jj=ix[dist>=dist.max()-.001];pts=p[jj]
    w,_=nnls(np.vstack((pts.T,np.ones(len(pts)))),np.r_[o,1.]);w/=w.sum()
    lb=2*sqrt(float(w@(pts**2).sum(1)-sum((w@pts)**2)))
    return lb,[(points[i][0],tuple(round(float(a),5) for a in p[i]),round(float(z),6)) for i,z in zip(jj,w) if z>1e-7]
def bounds():
    for k in (0.,-3.,-5.,-7.):
        t=tail48(P,k);e=packageElec();fixed=shift(che5()+drive()+indexdog()+xfixed()+duct()+hoodoutside(),k)
        s=fixed+shift(face3()+xmove()+moving('C'),k)+joint48()+e+t
        p=actualpoints(k);print('offset',k,'floor',min((proj(a,Z)[0]+23.65,a[0]) for a in s),'lower cert',certify(p),'enclosing proxy upper incl full round cam envelope',centre(s),flush=True)
        print('non-electronic lower cert',certify([q for q in p if q[0] not in ('cell','MCU')]))
        print('own split moving incl thick tail',ytest(shift(fork5(0,pk),k),t,1)[:1],'vs fixed hinge',fastpair(shift(fork5(0,pk),k),joint48())[:1],
              'cell/MCU v tail',ytest(e[:1]+[a for a in e if a[0]=='MCU'],t,1)[:1],
              'cell/MCU vs core',fastpair(e[:1]+[a for a in e if a[0]=='MCU'],fixed+shift(horn(L,0,0,pk)+fork5(0,pk)+fp(xmove()+face3()),k))[:2])
def near():
    D=fixed48()+packageElec();a,b=face3()+xmove(),moving('C');c=moving('E')
    # Housing and duct outer bounds are rigid throughout. Compress per-name
    # group for neighbor broad phase; negatives are *only* unresolved pairs.
    def compact(S):
        out=[];group={}
        for s in S:
            n=s[0];p=next((p for p in ('horn ','spoke','cheek','bearing A','bearing B','case5','bush A5','bush B5','lever','follower','hood','tail pivot','sector web') if n.startswith(p)),n)
            group.setdefault(p,[]).append(s)
        for p,grp in group.items():
            if len(grp)==1:out+=grp;continue
            out.append(box(p+' bound',*[(min(proj(x,v)[0] for x in grp),max(proj(x,v)[1] for x in grp)) for v in (X,Y,Z)]))
        return out
    b=compact(b);c=compact(c);D=compact(D)
    for lab,q,dep,nb in [('CC',0.,0.,0.),('CW',REL,0.,0.),('EC co-advanced',END,END,0.),('EC held',END,0.,0.),('CE held',0.,0.,END),('EE co-advanced',END,END,END)]:
        s=D+([mx(z,q) for z in a])+(b if q!=END else c);t=D+([mx(z,nb) for z in a])+(b if nb!=END else c)
        worst=(999.,);bad=0
        debit=.20+max(2*far(v,H)*sin(radians(.25)) for v in t)
        for ang in range(-15,16):
            tt=[mx(yaw(z,radians(ang),P),dep) for z in t]
            vals=fastpair(s,tt)
            worst=min(worst,(vals[0][0]-debit,*vals[0][1:],ang));bad+=sum(v[0]<=debit for v in vals)
        print(lab,'end-state bound after .2 and 1-degree angular interval, unresolved tests',worst,bad,flush=True)
def witnesses():
    for n,p in [('hinge top elbow',(0.,-4.,1.15)),('upper bridge1',(5.5,6.51,10.))]:
        s=next(s for s in joint48()+face3() if s[0]==n);x,y,z=p
        print('common hood/part point',n,p,'inside box signed depth',min(min(v-a,b-v) for (a,b),v in zip(ab(s),p)),
              'skin depth',min(z-guardfloor(x),guardfloor(x)+.4-z) if x==0 else min(8.26-.3*x-y,y-(8.06-.3*x)))
    sides=[]
    for s in fork5(0,pk):
        if not s[0].startswith('spoke'):continue
        v=clip(s,-1.15-s[2],False)
        if v:sides.append(min((8.06-.30*x-abs(y))/hypot(1,.30) for x,y,z in v[1])-s[2])
    print('spoke clipped forward of rear plane / inner hood sides conservative mm',min(sides))
    p=(-1.05,0.,6.15);print('rear bulkhead / actual upper lug annular point',p,'lug radius',hypot(p[0]-H[0],p[1]),
                      'separation of point from garage outer proxies',fastpair([ball('w',p,0)],duct())[0])
    # Hold actual next head still; straight site, not a forced co-translation.
    # Both rails are real rectangles. Give intersection length at endpoint and onset.
    a=next(s for s in xmove() if s[0]=='X rail');lo,hi=proj(a,X)
    print('two independent rails aligned, closed gap and onset',P+lo-hi,'full advance overlap',min(hi+END,hi+P)-max(lo+END,lo+P),'point',((P+lo+hi+END)*.5,AY,AZ))
    # One interior point of L18 through shaft and knuckle annulus plus
    # shortest distance from the L20 shaft centre to the solid heavy stem.
    q=(-6.25,0.,1.28);print('L18 common point',q,'r to hinge, to shaft',hypot(q[0]-H[0],q[1]),hypot(q[0]-O[0],q[2]-O[1]))
    for L0 in (18.,20.):
        xx,_,zz=axis(L0,0);print('L/p, nominal straight thick stem to axis xz distance',L0,P,hypot(xx-min(max(xx,22.5-P),26-P),zz))
    for f in (155.,163.,200.):
        print('stalk upper fibre reaction pure centered Fx, MPa',f,f/(3.2*2.8)+f*10.4/(3.2*2.8**2/6)+f*7.4/(2.8*3.2**2/6))
    print('groove half lash at pole mm, full sign reversal',18*.06/6.62399,18*.12/6.62399)
    print('references, solve gear output torque at peak if unrelieved',1742*.538233/(.80*9),'peak root spur tangential at worst cam load',1742*.538233/5.4)
    p=actualpoints(0)
    print('independent cell / closed web lower cert',certify([x for x in p if x[0] in ('cell','cam rear web')]))
    print('independent MCU / X motor material-point distance',max((hypot(*sub(a,b)),a,tuple(float(v) for v in b)) for n,a in p for m,b in p if n=='MCU' and m=='X gearmotor'))
if __name__=='__main__':witnesses();bounds();near()
