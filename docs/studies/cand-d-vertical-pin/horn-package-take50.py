"""Take 50 all-stock packaging / placement search, with explicit exclusions."""
from runpy import run_path
from pathlib import Path
G=run_path(str(Path(__file__).with_name('horn-integrate-take50.py')))
globals().update({k:v for k,v in G.items() if not k.startswith('__')})
from scipy.optimize import linprog
feet=[s for s in electr() if s[0].startswith('foot')]
def extra():
    # Radial thrust/overload and control hardware still allocations, not ratings.
    x=NO-5.65-2.95
    return [cyl('root output limiter',X,(x-5.32,x-3.42),(YS,ZS),2.24),
            cyl('face output limiter',X,(XS-3.32,XS-1.18),(0,ZSX),2.30),
            box('X dog hard back',(-7.98,-7.52),(-3.45,-2.44),(-23.35,-21.78)),
            box('X key end switch',(-10.50,-9.5),(8.25,9.62),(-23.13,-21.55)),
            box('X strain pickup',(3.20,4.78),(7.20,7.48),(-17.70,-17.05)),
            box('X output flag switch',(-10.1,-8.3),(-9.30,-7.85),(-20.95,-18.85)),
            box('root nut output flag',(-15.65,-13.72),(6.10,7.05),(ZH+.12,ZH+1.22)),
            box('root load readout seat',(-18.45,-17.22),(1.10,2.76),(ZS-.50,ZS+1.74))]
def filldisk(s,n=16):
    name,v,r,d=s
    if d is None:return s
    a=np.eye(3)[np.argmin(np.abs(d))];u=np.cross(d,a);u/=np.linalg.norm(u);w=np.cross(d,u)
    return poly(name,[tuple(q+r/cos(pi/n)*(cos(t)*u+sin(t)*w)) for q in map(np.array,v) for t in np.arange(n)*2*pi/n])
def shell50():
    a=[s for s in duct() if s[0].startswith('rear hub case')];xrear=1.65
    # Outer allocations for a single merged rear lumen. Don't count the
    # expanded solid interiors as manufactured walls or as solid stow witnesses.
    for s in stages(num=12)+[s for s in rotor(0,PH) if s[0].startswith(('horn ','spoke'))]+allmotor()+extra()[:1]:
        if s[0]=='horn motor X' or s[0]=='horn strap':continue # sealed can ahead/outside
        h=filldisk(s);xmin,xmax=proj(h,X)
        if xmin>xrear:continue
        if xmax>xrear:
            h=clip(h,xrear,True)
        if h:a.append(grow(h,.42,'root garage '))
    return a
def fixed50(shell=True):return joint51()+cheeks50()+lowfixed()+allmotor()+[s for s in extra() if s[0]!='X strain pickup']+hood51()+(shell50() if shell else [])
def face50():return F51+lowmoving()+[s for s in extra() if s[0]=='X strain pickup']
def slide50(phi):return rotor(phi)+rodparts(phi)
def compress(S):
    groups={};out=[]
    for s in S:
        name=s[0];key=name.split(':')[0] if ':' in name else name
        for p in ('lined radial bearing','metal bearing outer','frame thrust','root garage','spoke shell','horn ','spoke-1','spoke1','bearing A','bearing B','cheek-','cheek1','eye','tail sector hub','sector web'):
            if key.startswith(p):key=key[:len(p)+1] if p in ('spoke shell','root garage') else p;break
        groups.setdefault(key,[]).append(s)
    for n,ls in groups.items():
        out+=ls if len(ls)==1 else [box(n+' outer',*[(min(proj(s,d)[0] for s in ls),max(proj(s,d)[1] for s in ls)) for d in (X,Y,Z)])]
    return out
def dirs():
    return np.array([X,Y,Z]+[unit(u) for u in product((-1,0,1),repeat=3) if u>(0,0,0) and u.count(0)<2])
def electsearch():
    # Nominal grid candidates; reject unless a common projection axis gives
    # separation. Own tail sampled at 3 degrees with conservative motion pad.
    A=fixed50()+fp(face50())+rotor(0,PH)+stages()+feet
    T=tail51();A+=[yaw(s,radians(i)) for i in range(-15,16,3) for s in T]
    A.extend(sweep(s,(END,0,0)) for s in tail51(0) if s[0].startswith(('eye','neck','boss','heavy')))
    d=dirs();ds=list(map(tuple,d))
    al=np.array([[proj(s,e) for e in ds] for s in A]);dims=[(s[0],tuple(round(b-a,4) for a,b in ab(s))) for s in electr() if not s[0].startswith('foot')]
    dims.sort(key=lambda t:-np.prod(t[1]))
    result=[];o=np.array([-5.,0.,-.3])
    for nm,dd in dims:
        best=None
        grid=np.array(list(product(np.arange(-24.,18.1,1.5),np.arange(-25.5,25.6,1.5),np.arange(-22.,25.,1.5))))
        # Account for 1.5deg excursion of articulated stock conservatively.
        for dim in sorted(set(permutations(dd))):
            h=np.array(dim)/2;pad=np.abs(d)@h
            rad=np.linalg.norm(np.abs(grid-o)+h,axis=1)
            ix=np.argsort(rad);ix=ix[(rad[ix]<(best[0] if best else 43)) & (grid[ix,2]-h[2]>=-23.55)]
            m=grid[ix]@d.T
            # Cheap/high-rejection items go first.
            for L,H in zip(al[:,:,0],al[:,:,1]):
                valid=np.any((m+pad+.95<L)|(m-pad-.95>H),axis=1)
                if valid.all():continue
                m=m[valid];ix=ix[valid]
                if not len(ix):break
            if len(ix):best=(rad[ix[0]],tuple(grid[ix[0]]),dim)
        if best:
            rad,c,dim=best;s=bnew(nm,c,dim);result.append(s)
            al=np.concatenate((al,np.array([[[*proj(s,e)] for e in ds]])))
            print(nm,c,dim,rad,flush=True)
        else:print(nm,'no trial centre',flush=True)
    return result
def parts(label='home'):
    # Cell & board placements from retained screen.
    f=Path(__file__).with_name('horn-electronics-take50.json')
    return [shp(s) for s in json.loads(f.read_text())] if f.exists() else []
def material(e):
    out=[];xs=lowfixed()+allmotor()+extra()+feet+e
    for s in xs:
        n,v,r,d=s
        if d is None and (s in feet+e or n.startswith(('T rail head','T rail sole'))):out.extend((n,q) for q in v)
        elif n in ('face Y motor','horn motor X','face input bush','root motor quill','key lifter','key return spring envelope'):
            if not d:continue
            a=np.eye(3)[np.argmin(np.abs(d))];u=np.cross(d,a);u/=np.linalg.norm(u);w=np.cross(d,u)
            for q in v:
                for t in np.arange(72)*pi/36:out.append((n,tuple(q+r*(cos(t)*u+sin(t)*w))))
    for t in np.arange(180)*pi/90:out.append(('solid torus outer equator',(15-P+(R+r0)*cos(t),(R+r0)*sin(t),0)))
    return out
r0=4.20
def lp(a,b):
    n=ConvexHull(a[1]).equations;m=ConvexHull(b[1]).equations
    return linprog([0,0,0,0,-1],A_ub=np.r_[np.c_[n[:,:3],-n[:,0],np.ones(len(n))],np.c_[m[:,:3],np.zeros(len(m)),np.ones(len(m))]],b_ub=-np.r_[n[:,3],m[:,3]],bounds=[(None,None)]*3+[(REL,END),(None,None)],method='highs').x
def reports():
    e=parts();p=material(e);print('complete actual-point certificate',certify(p),'without relocated electronics',certify(material([])),flush=True)
    print('all stock (conservative diameter upper only)',centre(fixed50()+face50()+slide50(0)+tail51()+e+feet))
    vals=[(s[0],t[0],lp(s,t)) for s in F51 for t in roof51()];print('worst forward hood face LP',max(vals,key=lambda v:v[2][4]))
    print('hub / rib LP',lp(next(s for s in F51 if s[0]=='centre'),next(s for s in tail51() if s[0]=='tail sector hub0')))
    # Exact hood plane normals for all forward link stock. Split at rear plane.
    for lab,S in [('link',stages(num=32)),('spoke',[s for s in rotor(0,PH) if s[0].startswith('spoke')])]:
        w=[]
        for s in S:
            xlo,xhi=proj(s,X)
            if xhi<1.65:continue
            v=clip(filldisk(s),1.65-s[2],False)
            if not v:continue
            for p0 in v[1]:
                x,y,z=p0;w.append(((8.06-.30*x-abs(y))/hypot(1,.30)-v[2],(23.75-.32*x-z)/hypot(1,.32)-v[2],(z-guardfloor(x)-.4)/hypot(1,tan(radians(28)))-v[2]))
        print('clipped',lab,'side roof floor',np.min(w,axis=0))
    a=compress(fixed50()+e+feet);b=compress(face50());cc=compress(slide50(0));ee=compress(slide50(PH))
    for n,q,p,nb in [('CC',0,0,0),('RC',REL,0,0),('EC held',END,0,0),('EC follows',END,END,0),('EE follows',END,END,END)]:
        s=a+[mx(z,q) for z in b]+(ee if q==END else cc);t=a+[mx(z,nb) for z in b]+(ee if nb==END else cc)
        worst=(999.,);un=0;debit=.20+max(2*far(z,H)*sin(radians(.25)) for z in t)
        for i in range(-15,16):
            rows=fastpair(s,[mx(yaw(z,radians(i),P),p) for z in t]);un+=sum(v[0]<debit for v in rows);worst=min(worst,(rows[0][0]-debit,i,*rows[0][1:]))
        print('neighbour endpoint',n,'SAT envelope only',worst,un,flush=True)
if __name__=='__main__':
    import sys
    if 'search' in sys.argv:
        Path(__file__).with_name('horn-electronics-take50.json').write_text(json.dumps(electsearch(),indent=1)+'\n')
    else:reports()
