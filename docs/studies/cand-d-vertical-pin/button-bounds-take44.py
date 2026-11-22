"""Take 44: physical witnesses, corrected local face and independent drive bounds."""
from runpy import run_path
from pathlib import Path
import numpy as np
g=run_path(str(Path(__file__).with_name('button-route-take44.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def face3():
    f=[]
    for s in face2():
        n=s[0]
        if n=='stripper column':
            f.append(box('stripper lower shank',(2.60,4.50),(-1.45,1.45),(-8.35,-3.75)))
            s=box(n,(1.40,3.00),(-1.45,1.45),(-4.20,1.45))
        if n=='stripper low return':s=box(n,(2.60,6.20),(-1.45,1.45),(-10.25,-7.80))
        if n.startswith('side pillar'):s=box(n,proj(s,X),proj(s,Y),(-11.90,11.55))
        if n in ('backing 1.1','backing 2.1'):s=(*s[:2],1.38,s[3])
        # Crop the two corners closest to the torus; retain the 4x4 beam.
        if n in ('pad 1.1','pad 2.1'):
            j,i=map(int,n.split()[1].split('.'));b=BOSS[j];p=POLES[j][i]
            no=unit(sub(b,p));u=unit(cross(no,X));v=cross(no,u);q=sub(b,mul(r,no))
            s=poly(n,[plus(q,plus(mul(w,u),plus(mul(t,v),mul(h,no)))) for w,t,h in product((-1.0,1.),(-1.,1.),(-1.10,0.))])
        f.append(s)
    return f
def npdist(s,pts):
    # Euclidean point distance to material; pads are rectangular oriented prisms.
    v=np.array(s[1]);p=np.array(pts);n=s[0]
    if s[3] is not None:
        axis=np.array(s[3]);u=p-v[0];h=u@axis;h0,h1=sorted((0,np.dot(v[-1]-v[0],axis)))
        dr=np.linalg.norm(u-h[:,None]*axis,axis=1)-s[2]
        return np.hypot(np.maximum(0,dr),np.maximum(0,np.maximum(h0-h,h-h1)))
    if n.startswith('pad'):
        j,i=map(int,n.split()[1].split('.'));b=BOSS[j];no=unit(sub(b,POLES[j][i]));u=unit(cross(no,X));a=np.array((u,cross(no,u),no)).T;p=p@a;v=v@a
    return np.linalg.norm(np.maximum(0,np.maximum(v.min(axis=0)-p,p-v.max(axis=0))),axis=1)
def face_eye():
    f=face3();N=3600;ang=np.linspace(0,2*pi,N,endpoint=False)
    p=np.array([15+R*np.cos(ang),R*np.sin(ang),0*ang]).T
    print('exact ring gap cert incl arc debit',sorted((float(npdist(s,p).min())-r-R*pi/N,s[0]) for s in f)[:8])
    print('exact non-contact face v boss',sorted((float(npdist(s,[b])[0])-r,s[0],i) for i,b in enumerate(BOSS) for s in f if not s[0].startswith('pad '+str(i)+'.'))[:8])
    out=[]
    for t in bf(0):
        if not t[0].startswith(('metal neck','main stem')):continue
        u,v=t[1];p=np.linspace(u,v,401)
        out+= [(float(npdist(s,p).min())-t[2]-hypot(*sub(v,u))/800,s[0],t[0]) for s in f]
    print('neck gap incl sampling debit',sorted(out)[:6])
    # Entire relative X relief, including its inverse during aligned pickup.
    # Translate the test sites oppositely and debit both curve and X cell.
    a=np.linspace(0,2*pi,1440,endpoint=False)
    refs=[('ring',np.array([15+R*np.cos(a),R*np.sin(a),0*a]).T,r+pi*R/1440)]
    for t in bf(0):
        if t[0].startswith(('metal neck','main stem')):
            u,v=t[1];refs.append((t[0],np.linspace(u,v,161),t[2]+hypot(*sub(v,u))/320))
    refs.extend((f'boss{i}',np.array([b]),r) for i,b in enumerate(BOSS))
    worst=(999.,None,None,0)
    for x in np.linspace(REL,0,61):
        for n,pts,rd in refs:
            for s in f:
                if n.startswith('boss') and s[0].startswith('pad '+n[4:]+'.'):continue
                q=float(npdist(s,pts-[x,0.,0.]).min())-rd-abs(REL)/120
                worst=min(worst,(q,s[0],n,x))
    print('all nonworking aligned surfaces through relief / inverse pickup, raw gap certificate',worst)
    for name,lo,hi,zo,zi in [('takeup',REL,0,0,0),('lift',REL,REL,0,LIFT),('push',REL,END,LIFT,LIFT)]:
        F=[sweep(mx(s,lo),(hi-lo,0,0)) for s in f]
        U=[sweep(move(s,(0,0,zo)),(0,0,zi-zo)) for s in b2()]
        print(name,'face v fixed and moving',pair(F,tucked_joint()+electr()+xd2()+zz2()+U+[dog(0 if name=='takeup' else 1)])[:4])
    for pitch in (36.,37.5):
        F=[sweep(mx(s,REL),(END-REL,0,0)) for s in f]
        print('face alone vs own tail all states',pitch,scan(F,bf(pitch),0)[0])
def nearest(p,s):
    v=np.array(s[1]);axis=np.array(s[3]);p=np.array(p);h=(p-v[0])@axis
    axial=v[0]+np.clip(h,0,np.dot(v[-1]-v[0],axis))*axis
    u=p-v[0]-h*axis;mag=np.linalg.norm(u)
    return axial+u*(min(1.,s[2]/mag) if mag else 0.)
def witnesses():
    F=face2();zm=next(s for s in zz2() if s[0]=='Z motor')
    for pitch in (36.,37.5):
        b=yaw(next(s for s in bf(pitch) if s[0]=='boss2'),radians(15))[1][0];q=nearest(b,zm)
        print('own boss2 vs Z motor pitch yaw15',pitch,'nearest solid point',q.tolist(),'inside sphere',r-hypot(*sub(q,b)))
        # Explicit adjacent cylinder against the stationary side pillar.
        best=(-99,None,None,None)
        for sg in range(-15,16):
            mot=yaw(zm,radians(sg),pitch)
            for dx in (0,REL,END):
                s=mx(next(s for s in F if s[0]=='side pillar-1'),dx)
                bounds=[proj(s,k) for k in (X,Y,Z)]
                for q in product(*(np.linspace(a+.02,b-.02,8) for a,b in bounds[:2])):
                    p=(*q,mot[1][0][2]);a=np.array(mot[3]);v=np.array(p)-np.array(mot[1][0]);h=v@a
                    m=min(h,28.70-h,3.-np.linalg.norm(v-h*a))
                    if m>best[0]:best=m,sg,dx,p
        print('neighbor motor depth, yaw, face x offset, interior pillar point',pitch,best)
    xm=next(s for s in xd2() if s[0]=='X gearmotor');q=(7.,-18.70,-1.15)
    print('closed rack inner point',q,'in X motor',xm[2]-hypot(q[1]-xm[1][0][1],q[2]-xm[1][0][2]))
    for k in (-5.,-7.):
        b=plus(BOSS[0],(-36.,0,k));q=(-17.60,0,-16.50)
        print('shifted cell vs boss',k,q,4.2-hypot(*sub(q,b)),'original/routed shoe floor gaps',(-18.8+k)-(-23.65),(-19.8+k)-(-23.65))
    x=12.;q=(x,-4.97,16.8);edge=4.935-.25*(x-XP)
    print('Take43 negative wall inward depth at bridge point',q,(edge+q[1])/sqrt(1+.25**2),'top leading lift hit outer T and .2 skin',28.2-18.1,28.2-.2-18.1)
    print('moving rail travel margins front / rear',20.90+REL-18.75,3.45-(-13.85+END))
    for t in (.40,.68):
        a=.48+.32*(7.53675+t);b=.32*tan(radians(28))
        print('slot thickness / positive lateral / aft x clearance',t,3.225-a/sqrt(1-b*b),XP-a/(1+b)-9.649)
    for k in (-5,-7):
        print('roller working wall in stationary knuckle',(-1.75,0.,8+k),'knuckle radius',abs(-1.75-H[0]),'wall thickness coordinates',.3898-3.335,.3898-2.035)
    # Take 43 signed-side and top skins; bounding whole end panels only
    # ABOVE the slotted floor. Sloped skin coordinates are conservatively
    # thickened by projecting 0.20 mm normal thickness.
    XA,XB=7.75,18.4
    def w(x):return 4.935-.25*(x-XP)
    def L(x):return 7.53675+tan(radians(28))*(x-XP)
    def T(x):return 28.2-.26*(x-XP)
    hood=[poly('side'+str(sg),[(x,sg*(w(x)-d),z) for x in (XA,XB) for d in (0,.20*hypot(1,.25)) for z in (L(x),T(x))]) for sg in (-1,1)]
    hood+=[poly('hood top',[(x,y* w(x),T(x)-d) for x,y,d in product((XA,XB),(-1,1),(0,.20*hypot(1,.26)))])]
    for name,ends in [('fore',(XB-.20,XB)),('aft',(XA,XA+.20))]:
        hood.append(poly(name,[(x,y*w(x),z) for x in ends for y in (-1,1) for z in (L(x)+.4,T(x))]))
    for a,b in [(XA,9.649),(9.649,XB)]:
        for sg in (-1,1):
            hood.append(poly('hood floor'+str((a,sg)),[(x,sg*y,L(x)+d) for x in (a,b) for y in ((0 if a==XA else 3.225),w(x)) for d in (0,.40)]))
    fh=[sweep(mx(s,REL),(END-REL,0,0)) for s in face3()]
    print('face3 vs full trial hood incl end panels',pair(fh,hood)[:6])
def rollers():
    XG=.3898;rr=[];ww=[]
    for i,(y,z,ax,sg) in enumerate(((-10,-4,Y,-1),(10,-4,Y,1),(0,8,Y,-1),(5,-4,X,-1),(5,8,X,-1))):
        c=(XG,y,z);v=lambda a:plus(c,mul(a,ax))
        rr+=[poly('roll'+str(i),(v(-.85),v(.85)),2.,ax),poly('stud'+str(i),(v(.8*sg),v(6.15*sg)),.70,ax)]
        if i==4:continue
        for sign in (-1,1):
            K=(XG if ax==Y else y);el=tuple(sorted((K+sign*2.035,K+sign*3.335)))
            zbox=(z-3.60,(8 if i==3 else z)+16.30)
            ww.append(box('slot'+str((i,sign)),el if ax==Y else (XG-.85,XG+.85),(y-.85,y+.85) if ax==Y else el,zbox))
    for k in (0,-5,-7):
        a=shift(ww,k)+shift([sweep(s,(0,0,12.70)) for s in rr],k)
        print('five-roller vs joint, electronics',k,pair(a,tucked_joint())[:2],pair(a,electr())[:2])
    print('slot vs routed face stages',pair(ww,[sweep(mx(s,REL),(END-REL,0,0)) for s in face3()])[:3])
    return rr,ww
def load():
    m=[];centres=[]
    for b,ps in zip(BOSS,POLES):
        for p in ps:
            n=unit(sub(b,p));m.append((*n,*cross(sub(b,C),n)));centres.append(sub(b,mul(r,n)))
    for F in (64.,76.):
        w=np.linalg.solve(np.array(m).T,[F,0,0,0,0,0]);stress=[]
        for a,s,p,row in zip(w,[s for s in face3() if s[0].startswith('beam')],centres,m):
            q=(5.12,*cc(s)[1:]);fx,fy,fz=mul(a,row[:3]);tx,ty,tz=cross(sub(p,q),(fx,fy,fz))
            stress.append(abs(fx)/16+(abs(ty)+abs(tz))/(4**3/6))
        print('pure centred Fx',F,'normal solution',w.tolist(),'4x4 root |normal| max for each beam MPa',stress)
        print('couple from pure screw thrust to centred face M_y,M_z Nmm',F*10.65,F*17.8,
              'stalk M_y,M_z',F*10.4,F*7.4)
    print('M3 screw torque Nmm ideal / at .28 eff',F*.5/(2*pi),F*.5/(2*pi*.28))
    print('drive toe radius/m, tangential N sector then input mesh, radial at 20 deg',9.,.25,112.373/9.,15.05/2.25,112.373/9.*tan(radians(20)),15.05/2.25*tan(radians(20)))
    print('dog flat overlap LxW, lifted gap open',9.90-6.95,4.90,6.95-(9.90-4.45))
    for F in (76.,121.):
        zc=r*K/sqrt(1+K*K);zmax=(.48+3*K*zc)/(2*K)
        print('nominal tangent cone contact z/max bending z/lateral F/nominal MPa/upward normal component',zc,zmax,F,4*F*(zmax-zc)/(pi*(.48+K*zmax)**3),F*K)
    print('stalk area/weak Z modulus, nominal axial + biaxial bending for nominal pure F76',
          3.2*2.8,3.2*2.8**2/6,76/(3.2*2.8)+76*10.4/(3.2*2.8**2/6)+76*7.4/(2.8*3.2**2/6))
    # Fixed-rail comparator: block home -9.25..6.05, travel -1.50..16.80.
    # Top-mounted block clear of buried rail is not modelled as solid overlap.
    br=box('fixed rail reaction bed',(-11.20,23.35),(-8.9,-4.9),(-17.90,-16.25))
    p=(-9.,-6.90,-17.0);print('fixed rail bed inside retained cell',p,*(proj(br,a) for a in (X,Y,Z)))
    print('fixed rail alternate min axial span',15.3+(END-REL),'chosen length',34.55,'end marg',(-9.25+REL)-(-11.2),23.35-(6.05+END))
    # Even a nominal short two-band pin journal cannot be substituted for the five rollers.
    for F in (5.,76.,121.):
        lo,hi=12.24,14.80;Q=F*lo/(hi-lo)
        print('button guide reference F at local z0, lower/upper reaction, .23 drag',F,F+Q,Q,.23*(F+2*Q))
def bound():
    # Four *material points* suffice. A convex-weighted variance lower
    # bounds max radius about every centre. Optimising the weights is not
    # required for validity; print the actual weights and lower bound.
    for k in (0.,-5.,-7.):
        S=shift(face3()+mover2()+b2()+xd2()+zz2()+[dog(0)],k)+tucked_joint()+electr()+tailshift(36.,k)
        names=['cell' if not k else 'Z motor','Z motor' if not k else 'yaw gearmotor','yaw gearmotor' if not k else 'MCU','block mounting foot']
        o=np.array(centre(S)[0]);pts=[]
        for n in names:
            s=next(s for s in S if s[0]==n);pts0=[]
            for v in s[1]:
                q=np.array(v)
                if s[2]:
                    a=np.array(s[3]);w=q-o;u=w-(w@a)*a;q=q+s[2]*u/np.linalg.norm(u)
                pts0.append(q)
            pts.append(max(pts0,key=lambda q: np.linalg.norm(q-o)))
        pts=np.array(pts);u=pts[1:]-pts[0];v=np.linalg.solve(2*u,(pts[1:]**2).sum(axis=1)-(pts[0]**2).sum());w=np.linalg.solve(np.vstack((pts.T,np.ones(4))),np.append(v,1))
        w=np.maximum(w,0);w=w/w.sum()
        print('stow lower diameter',k,2*sqrt(float(w@(pts**2).sum(axis=1)-sum((w@pts)**2))),names,'points',pts.tolist(),'weights',w.tolist())
if __name__=='__main__':
    face_eye();witnesses();rollers();load();bound()
