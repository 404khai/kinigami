"""Take 50. Root-clevis slider crank. mm, N, Nmm. No external cam/drive stub."""
from runpy import run_path
from pathlib import Path
G=run_path(str(Path(__file__).with_name('horn-package-take48.py')))
globals().update({k:v for k,v in G.items() if not k.startswith('__')})
from functools import lru_cache
PH=pars(18)[4];A0=.54;RR=18.90;SS=4.10;LL=8.;ZH=17.35;YS=0.;ZS=13.05
def pose(phi,z=ZH,ell=LL):
    a=A0+phi;Bx=O[0]+RR*cos(a)-SS*sin(a);Bz=O[1]+RR*sin(a)+SS*cos(a)
    u=Bz-z;w=sqrt(ell**2-u*u);Nx=Bx-w
    j=-(Bz-O[1])+u*(Bx-O[0])/w
    return Bx,Bz,Nx,w,u,j
NC=pose(0)[2];NO=pose(PH)[2]
def ar(n,x,z,y0,y1,r):return cyl(n,Y,(y0,y1),(x,z),r)
def swept(a,b,r,axial=None):return poly(a[0],a[1]+b[1],r+a[2],axial if axial is not None else a[3])
def rotor(phi=0,end=None):
    # Both journals idle. Direct load entry through short clevis outside solid end.
    a=[s for s in fork(phi,end) if not s[0].startswith('stub')]
    for sg in (-1,1):
        span=tuple(sorted([7.25*sg,(12.56 if sg>0 else 12.92)*sg]));a.append(cyl('idle journal '+str(sg),Y,span,O,2.))
    a.extend([sh('locating inner shoulder',8.90,9.34,O,2.86),sh('rotating thrust washer',12.56,13.28,O,3.12),
              sh('axial M2 cap head',13.28,14.38,O,1.72)])
    return horn(L,0,phi,end)+a
def rodparts(phi):
    x,z,n,wx,dz,j=pose(phi);q=(x,0.,z);d=(n,0.,ZH)
    a=[ar('buried pin',x,z,-3.70,3.70,1.30),ar('buried pin head',x,z,3.42,3.90,1.66),ar('buried pin keeper',x,z,-3.90,-3.42,1.65),
       ar('slider pin',n,ZH,-3.12,3.12,1.30),ar('slider pin head',n,ZH,3.13,3.48,1.65),ar('slider keeper',n,ZH,-3.48,-3.13,1.65)]
    # Rod is a planar 2.10-wide link: R2.35 ends and a 2.80-deep central web.
    perp=(-dz/LL,wx/LL)
    a+=[ar('rod root eye',x,z,-1.05,1.05,2.35),ar('rod slider eye',n,ZH,-1.05,1.05,2.35),
        poly('short link web',[(u+sg*perp[0]*1.40,y,v+sg*perp[1]*1.40) for (u,v),sg,y in product(((x,z),(n,ZH)),(-1,1),(-1.05,1.05))])]
    for sg in (-1,1):
        def yy(lo,hi):return tuple(sorted([lo*sg,hi*sg]))
        # Solid end face remains continuous; the pin bore is wholly beyond it.
        a.extend([ar('forged root ear'+str(sg),x,z,*yy(1.20,3.40),2.50),
                  poly('root ear foot'+str(sg),[point(18,0,A0+phi,r,y,s) for r,y,s in product((RR-1.90,RR+1.90),yy(1.20,3.40),(-.50,SS))]),
                  ar('slider ear'+str(sg),n,ZH,*yy(1.22,3.11),2.30),
                  box('slider ear arm'+str(sg),(n-5.95,n+2.95),yy(1.22,3.11),(ZH-1.2,ZH+.5))])
    a.append(cyl('travelling nut',X,(n-5.25,n-1.45),(YS,ZS),2.45))
    a.append(box('nut bridge',(n-4.76,n-3.05),(-3.35,3.35),(ZS+1.72,ZH+.5)))
    # Two slider slipper stations per side, span 7.8. Guide and slide take
    # transverse components and screw-axis eccentricity, not an unsupported nut.
    for u in (-5.4,2.40):
        for sg in (-1,1):
            yy=tuple(sorted([sg*2.90,sg*4.35]))
            a.append(box('slipper'+str((u,sg)),(n+u-.72,n+u+.72),yy,(ZH-.65,ZH+.65)))
    a.append(box('dog register block',(n-5.50,n-3.1),(5.36,10.16),(ZH+1.98,ZH+3.15)))
    a.extend([box('register near return',(n-5.50,n-3.10),(1.55,2.85),(ZH+.40,ZH+3.15)),box('register overhead tie',(n-5.50,n-3.10),(2.44,5.65),(ZH+2.02,ZH+3.15))])
    return a
def stages(lo=0.,hi=PH,num=10):
    if lo==hi:return rodparts(lo)
    # Bound interval for centreline tube movement from the midpoint. Any point
    # on the rigid horn moves <=24 mm/rad. Slider |J| < 22 mm/rad in this model;
    # link orientation |alpha'|=|Bz'|/w < 2.2, R2.35 eyes inside 3D offset.
    out=[]
    for i in range(num):
        ph=lo+(hi-lo)*(i+.5)/num
        for n,v,r,d in rodparts(ph):
            # Include isotropic movement without turning a thin disk into a ball.
            # Use two cap-face layers with segment/ball padding via poly prism.
            if d is not None:
                v=tuple((x+r/cos(pi/32)*cos(th),y,z+r/cos(pi/32)*sin(th)) if abs(d[1])>.9 else (x,y+r/cos(pi/32)*cos(th),z+r/cos(pi/32)*sin(th)) for x,y,z in v for th in (i*pi/16 for i in range(32)));r=0
            out.append(poly(n+':'+str(i),v,r+28*(hi-lo)/(2*num)))
    return out
def guides():
    a=[];x0=NO-6.72;x1=NC+3.54
    for sg in (-1,1):
        yy=lambda l,h:tuple(sorted([l*sg,h*sg]))
        a.extend([box('rail upper '+str(sg),(x0,x1),yy(3.60,5.30),(ZH+.72,ZH+1.75)),
                  box('rail lower '+str(sg),(x0,x1),yy(3.60,5.30),(ZH-1.75,ZH-.72)),
                  box('rail outer '+str(sg),(x0,x1),yy(4.42,5.35),(ZH-1.74,ZH+1.74))])
    return a
def drive50(my=-11.95,mz=18.20,ys=YS,zs=ZS):
    a=[];u=np.array([my-ys,mz-zs]);dist=float(np.linalg.norm(u));u/=dist
    # Idler-to-screw 34:22, module .22; motor-to-idler 34:38, module .24.
    b=(dist**2+6.16**2-8.64**2)/(2*dist);h=sqrt(6.16**2-b*b);i=np.array((ys,zs))+u*b+np.array((u[1],-u[0]))*h
    ix,iz=tuple(i)
    r=NO-5.25-.40 # rear edge of operating nut, then thrust pair
    t=r-2.95
    def shx(n,x1,x2,y,z,r):return cyl(n,X,(x1,x2),(y,z),r)
    a+=[shx('root screw',t-4.20,NC-1.04,ys,zs,1.50),
        shx('root thrust B',r-2.55,r-1.42,ys,zs,2.80),shx('root thrust A',r-1.34,r,ys,zs,2.80),
        shx('screw wheel 22T',t-1.50,t,ys,zs,2.64),shx('root idler pinion 34T',t-1.50,t,ix,iz,3.96),
        shx('idler wheel 38T',t-3.30,t-1.70,ix,iz,4.80),shx('root motor 34T',t-3.30,t-1.70,my,mz,4.32),
        shx('idler axle',t-4.80,r-1.36,ix,iz,1.0),shx('idler inboard bush',t+.15,r-1.45,ix,iz,1.7),
        shx('idler rear bush',t-4.8,t-3.5,ix,iz,1.7),shx('root motor quill',t-4.7,t+.30,my,mz,.90),
        shx('quill bush',t-4.75,t-3.50,my,mz,1.45),shx('horn motor X',t+.30,t+29.,my,mz,3.),
        shx('horn strap',t+3.2,t+5.0,my,mz,3.65)]
    a.append(poly('root thrust tie',[(x,y,z) for x in (r-1.32,r-.50) for y,z in [(ys-1.65,zs-1.25),(ys+1.65,zs-1.25),(-4.55,ZH+1.30),(-5.35,ZH+1.30)]]))
    a.append(poly('idler rear tie',[(x,y,z) for x in (t-4.75,t-3.50) for y,z in [(ix-1,iz-.9),(ix+1,iz+.9),(my+1,mz+.9),(my-1,mz-.9)]]))
    return a
def dog50():
    # Retractable vertical square key drops behind an aft-facing register,
    # not into the threads. Remains in compression/bearing off-power.
    x=NC-5.50-.08
    return [box('holding key sweep',(x-1.60,x),(-2.00,2.00),(ZH+1.,ZH+5.65)),
            box('key guide',(x-2.25,x+.65),(-2.65,2.65),(ZH+3.40,ZH+5.35)),
            cyl('key lifter',Y,(-9.0,-3.0),(x-.80,ZH+4.50),2.10),
            box('positive lift wedge sweep',(x-1.80,x+.20),(-3.0,2.20),(ZH+3.90,ZH+6.90))]
def kine():
    # Interval arithmetic, not a sampled dead-centre test.
    from itertools import pairwise
    rows=[]
    for l,h in pairwise(np.linspace(0,PH,125)):
        p=pose(l);q=pose(h)
        # Monotone Bx decreasing and Bz increasing for the entire interval.
        assert p[0]>q[0]>O[0] and O[1]<p[1]<q[1]
        dl=p[4];dh=q[4];wl=sqrt(LL**2-max(dl*dl,dh*dh));wh=sqrt(LL**2-(min(abs(dl),abs(dh)) if dl*dh>0 else 0.)**2)
        prod=[dz*x/w for dz,x,w in product((dl,dh),(q[0]-O[0],p[0]-O[0]),(wl,wh))]
        jl=O[1]-q[1]+min(prod);jh=O[1]-p[1]+max(prod)
        assert jh<0
        rows.append((jl,jh,wl,abs(jh)*wl/LL,max(abs(dl),abs(dh))/wl))
    ar=np.array(rows);print('B,N,J closed',pose(0),'park',pose(PH),'slider stroke',NC-NO)
    print('J interval, minimum projected horizontal link length, minimum link moment arm',ar[:,0].min(),ar[:,1].max(),ar[:,2].min(),ar[:,3].min())
    for T in (246.,1742.,1742*200/163):
        F=T/abs(ar[:,1].max());Q=T/ar[:,3].min();V=F*ar[:,4].max();M=F*(ZH-ZS)
        # Both guide transverse signs; all guide load/drag allowed on a single side.
        print('T, axial, rod, transverse, guide couple Nmm, guide normal sum bound',T,F,Q,V,M,V+2*M/7.8+2*V*1.50/7.8)
        # Dog holding is independent of thread and motor efficiency/friction.
        print('pin single-shear MPa, pin bending MPa simple span 4.6, link bearing MPa, key shear MPa',Q/(pi*1.3**2),32*(Q*4.60/4)/(pi*2.6**3),Q/(2.10*2.6),F/(1.60*4.0))
    print('link Euler pinned, 2.10x2.8x8, steel E200GPa',pi**2*200000*(2.8*2.1**3/12)/LL**2)
    print('M3 min assumed thread core d2.35, effective K2 span mm, Euler',NC-1.04-(NO-5.65),pi**2*200000*pi*2.35**4/64/(2*(NC-1.04-(NO-5.65)))**2)
if __name__=='__main__':kine()
