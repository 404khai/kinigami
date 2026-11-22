"""Integrated Take 48 horn/shaft, grooved cam, shrouds and two-band X slide."""
from pathlib import Path
from runpy import run_path
g=run_path(str(Path(__file__).with_name('horn-layout-take48.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
O=(O48[0],O48[2]);AY=-9.60;AZ=-15.65;SY=-17.80;SZ=-11.40;S0=-4.50;S1=8.60
def fork5(phi=0,end=None):
    s=[v for v in fork(phi,end) if v[0] not in ('stub -1','fork hub -1')]
    return s+[sh('driven 5 stub',-19.05,-7.05,O,2.50),sh('driven 6.10 collar',-11.00,-8.55,O,3.05)]
def che5():
    a=[s for s in cheeks() if not s[0].startswith(('bearing A-1','bearing B-1','cheek-1','hinge cheek tie'))]
    for nm,lo,hi,ri,ro in [('bush A5',11.25,13.55,2.50,4.),('bush B5',14.05,16.35,2.50,4.),('case5',11.18,16.4,4.,4.7)]:
        for s in ringpart(nm,(O[0],O[1]),ri,ro,(-hi,-lo),step=15):a.append(poly(s[0],[(x,y,z) for x,z,y in s[1]]))
    # Follows the OD; stays off both inner races. Bolted to stationary hinge frame.
    a.append(box('hinge cheek return',(-2.35,-.80),(-13.0,-3.96),(-.55,1.70)))
    return a
def guardfloor(x):return 7.53675+tan(radians(28))*(x-12.3898)
def roof48():
    # Lead's rear-open Take 46 interface: front relief through L+2.0.
    s=[];xa=-1.15;xb=15.4;cutL=8.77;w=3.065
    def edge(x):return 8.26-.30*x
    def top(x):return 23.95-.32*x
    for x0,x1 in ((xa,cutL),(cutL,xb)):
        for sg in (-1,1):
            s.append(poly('slot floor'+str((x0,sg)),[(x,sg*y,guardfloor(x)+z) for x in (x0,x1) for y in ((w if x0==cutL else 0.),edge(x)) for z in (0.,.40)]))
    for sg in (-1,1):
        s.append(poly('front hood side'+str(sg),[(x,sg*(edge(x)-d),z) for x in (xa,xb) for d in (0,.20) for z in (guardfloor(x),top(x))]))
    s.append(poly('hood top',[(x,y*edge(x),top(x)-z) for x,y,z in product((xa,xb),(-1,1),(0,.20))]))
    s.append(poly('fore end',[(x,y*edge(x),z) for x in (xb-.2,xb) for y in (-1,1) for z in (guardfloor(x)+2.,top(x))]))
    return s
def grow(s,d,n):return (n+s[0],s[1],s[2]+d,None) if s[3] is None else poly(n+s[0],s[1],s[2]+d)
def clip(s,bound,left):
    # Clip convex polytope by X plane, using all true hull edges via SciPy.
    from scipy.spatial import ConvexHull
    V=np.array(s[1]);dx=(V[:,0]-bound)*(1 if left else -1);v=[tuple(q) for q,t in zip(V,dx) if t<=1e-9]
    if not v:return None
    if len(v)==len(V):return s
    h=ConvexHull(V);edges={tuple(sorted((a,b))) for tri in h.simplices for a,b in zip(tri,np.roll(tri,1))}
    for i,j in edges:
        if dx[i]*dx[j]<0:v.append(tuple(V[i]+(V[j]-V[i])*dx[i]/(dx[i]-dx[j])))
    return poly(s[0],v,s[2],s[3])
def duct():
    # Conservative outer chamber allocation. Skin = boundary of union, not
    # solid material filling the lumen. Join to pocket with a sealed bulkhead.
    # Ball offsets: .22 inner running clearance and .30 skin stock.
    a=[]
    for s in [s for s in fork5(0,pk) if s[0].startswith('spoke')]+horn(L,k,0,pk):
        v=clip(s,-.90,True)
        if v is not None:a.append(grow(v,.52,'spoke shell '))
    # Rear closure at x5.1 outside internal channel openings, not a side slot.
    # End caps surround the rotating root/hub to the stationary bearing
    # carriers. These are OUTER envelopes; the union lumen is not stock.
    a.extend([sh('rear hub case +',6.36,9.52,O,3.32),
              sh('rear hub case -',-11.28,-6.36,O,3.62)])
    return a
def hoodoutside():
    # Rectangle outside the rear tunnel-to-pocket transition. The rear plate
    # minus the duct lumen seals the remaining area; bore is not free to outside.
    return roof48()+[poly('rear bulkhead blank',[(x,y*(8.26-.30*x),z) for x in (-1.15,-.95) for y in (-1,1) for z in (guardfloor(x),23.95-.32*x)])]
def xmove():
    a=[box('X rail',(S0-18.20,S1+2.95),(AY-2.85,AY+2.85),(AZ-1.8,AZ+1.80)),
       box('X neck',(-1.7,3.20),(AY-.98,AY+.98),(AZ+1.75,-10.15)),
       box('stalk root',(.35,3.15),(AY-.98,-5.6),(-11.70,-9.50))]
    # Draw nut, rack upstream of load stack. Movable stack seats straddle
    # Belleville allocation on separate pillar line, not through screw.
    a.extend([cyl('X nut OD',X,(-8.80,-5.95),(SY,SZ),2.85),
              box('nut pickoff',(-8.65,-6.0),(SY-.95,AY-1.25),(SZ-.85,SZ+1.05)),
              box('spring pack',(-5.9,-.95),(-14.00,-10.45),(-12.30,-8.90)),
              box('series heel',(-1.1,.85),(-14.00,AY+.85),(-12.30,-9.25)),
              box('nut tooth rail',(-8.80,-4.05),(SY-4.25,SY-2.40),(SZ-1.8,SZ+.45))])
    return a
def xfixed():
    x=-13.20;ym=SY-4.5;zm=SZ+sqrt(7.20**2-4.50**2)
    a=[cyl('X screw',X,(-16.1,13.5),(SY,SZ),1.5),
       cyl('X rear thrust pair',X,(-12.2,-10.60),(SY,SZ),2.7),cyl('X forward bush',X,(11.8,13.5),(SY,SZ),2.55),
       cyl('X reduction wheel 54T',X,(x-.9,x+.9),(SY,SZ),5.60),cyl('X motor 18T',X,(x-.9,x+.9),(ym,zm),2.0),
       cyl('X gearmotor',X,(-11.8,16.90),(ym,zm),3.),cyl('X saddle',X,(-10.0,-8.35),(ym,zm),3.65),
       cyl('X torque limiter',X,(-16.00,-14.35),(SY,SZ),3.0),
       cyl('X plunger body',Z,(-21.0,-14.5),(-6.7,-21.75),2.15),
       cyl('X plunger guide',Z,(-15.4,-13.75),(-6.7,-21.75),1.45),
       box('X plunger sweep',(-7.25,-6.15),(-22.30,-21.20),(-15.10,-12.25)),
       box('X rear bearing foot',(-12.2,-10.60),(SY-1.00,SY+1.35),(SZ-5.65,SZ-.55)),
       box('X screw front tie',(11.8,13.5),(SY-1.0,SY+1.35),(SZ-5.65,SZ-.55))]
    # Two wraparound guides with a longitudinal stem SLOT. Each band can
    # transfer either transverse sign; spacing/individual reactions explicit.
    for j,x in enumerate((S0,S1)):
        xx=(x-1.2,x+1.2)
        a.append(box('X shoe base'+str(j),xx,(AY-3.85,AY+3.85),(AZ-3.05,AZ-1.86)))
        for sg in (-1,1):
            yy=lambda l,h:tuple(sorted((AY+sg*l,AY+sg*h)))
            a.append(box('X shoe side'+str((j,sg)),xx,yy(2.91,3.85),(AZ-2.0,AZ+2.85)))
            a.append(box('X shoe lip'+str((j,sg)),xx,yy(1.18,3.85),(AZ+1.86,AZ+2.85)))
    a.append(box('X guide mounting beam',(S0-1.2,S1+1.2),(AY-3.85,AY-2.75),(AZ-3.85,AZ-2.80)))
    return a
def indexdog():
    # Full wheel allocation. Actual local CSG at closed: disk LESS a parallel-
    # flank keyseat |x-Cx|<=.62, z>=Cz+3.00 through the disk thickness. Tooth
    # occupies .95..1.25 mm depth, with .07 mm nominal flank clearance.
    return [sh('notched index flange blank',-14.07,-12.63,C48,4.25),
            cyl('cam dog solenoid',Z,(17.05,23.35),(C48[0],-13.35),1.44),
            cyl('cam dog tip guide',Z,(15.85,17.55),(C48[0],-13.35),.89),
            box('cam dog tongue sweep',(C48[0]-.55,C48[0]+.55),(-13.98,-12.72),(14.22,17.55)),
            box('cam dog saddle',(C48[0]+1.30,C48[0]+2.32),(-14.35,-12.35),(16.60,20.10))]
def forcecalc():
    D=S1-S0;ds=abs(SY)+abs(SZ);dg=abs(SY-AY)+abs(SZ-AZ)
    for f in (155,163,200):
        for mu in (.10,.23):
            drag=(2*mu*f*ds/D)/(1-2*mu*dg/D)
            force=f+drag
            print('X F,mu,drag,thrust,guide reaction scalar per band,required gearhead at .28 screw/.80 gears',
                  f,mu,drag,force,drag/(2*mu),force*.5/(2*pi*.28)/(3*.8))
    for T in (246.,1742.):
        G=79e3;d=5.;length=16.7-11.
        print('stub T twist deg, contact arc, shaft shear, dwell normal',T,degrees(32*T*length/(pi*G*d**4)),18*32*T*length/(pi*G*d**4),16*T/(pi*d**3),T/6.62399)
        n=T/6.62399;over=20.90-15.20;span=15.20-12.40;print('rollers reference outer/inner N, stub M, bending MPa, .05 dwell eccentric Nmm',n*(1+over/span),n*over/span,n*over,32*n*over/(pi*d**3),n*.05)
        twist=T*32/(pi*G)*(length/d**4+1.90/6.10**4)
        print('added collar, total twist deg, pole mm + one half groove lash, .05 eccentric dog flank at R3.55 N',
              degrees(twist),18*(twist+.06/6.62399),n*.05/3.55)
        print('single spoke, pure couple sensitivity / narrow section modulus, MPa',1.90*2.4**2/6,T/(1.90*2.4**2/6))
def fixedmetal():return joint48()+che5()+xfixed()+drive()
def stages5():
    return [('C',horn(L,k)+fork5()+lever(),[sweep(mx(s,REL),(-REL,0,0)) for s in face3()+xmove()]),
            ('W',horn(L,k,0,pk)+fork5(0,pk)+lever(0,pk),[mx(s,REL) for s in face3()+xmove()]),
            ('E',horn(L,k,pk)+fork5(pk)+lever(pk),fp(face3()+xmove()))]
def checks():
    forcecalc();t=tail48();u=duct();j=joint48();f=fp(face3())
    for a,b,n in [(u,j,'duct/joint'),(u,f,'duct / face independent envelope'),(hoodoutside(),f,'hood/face'),(xfixed(),drive(),'X vs horn drive'),(xfixed(),j,'X vs joint'),(xfixed(),f,'X fixed vs face')]:
        print(n,fastpair(a,b)[:5])
    for name,s in [('5mm modified trunnion',fork5(0,pk)+che5()),('X fixed',xfixed()),('X moving',fp(xmove())),('shell',u+hoodoutside())]:
        print(name,'own tail',ytest(s,t,1)[:4])
    for n,h,m in stages5():
        print(n,'H / X moving',fastpair(h,m)[:2],'X moving / horn drive',fastpair(m,drive())[:2])
    print('X moving vs joint',fastpair(fp(xmove()),j)[:4])
    print('X shoe caps vs face stalk',fastpair([s for s in xfixed() if s[0].startswith('X shoe')],f)[:3])
    print('cam index dog moving tongue / body vs full X sweep',fastpair(indexdog(),fp(face3()+xmove()))[:3])
    print('cam index dog vs hood/duct',fastpair(indexdog(),hoodoutside()+duct())[:3])
if __name__=='__main__':checks()
