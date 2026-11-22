"""Installed exploratory Take 44 head/joint check. Geometry dimensions mm."""
from pathlib import Path
from runpy import run_path
d=run_path(str(Path(__file__).with_name('button-joint-take44.py')))
globals().update({k:v for k,v in d.items() if not k.startswith('__')})
XP=12.3898; K=.32; TIP=-.8; LIFT=12.80; REL=-1.5; END=16.8
YRAIL=-6.9;YS=-13.4;ZS=-12.; ROOT=.48+.32*11.84
POLES=[[(14.45,3.56,-9.33),(14.45,-3.56,-9.33)],[(8.48,7.75,9.33),(10.36,11.31,3.45)],[(8.48,-7.75,9.33),(10.36,-11.31,3.45)]]
def rod(n,ax,span,a,b,r):return cyl(n,ax,span,(a,b),r)
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def lands():
    s=[]
    for j,(b,ps) in enumerate(zip(BOSS,POLES)):
        for i,p in enumerate(ps):
            n=unit(sub(b,p));q=sub(b,mul(r,n));u=unit(cross(n,X));v=cross(n,u);name=f'{j}.{i}'
            # Tangent pad centred on the exact sphere. Rounding of supplied
            # pole is not an imposed penetration.
            s.append(poly('pad '+name,[plus(q,plus(mul(w,u),plus(mul(t,v),mul(h,n)))) for w,t,h in product((-1.20,1.20),(-1.20,1.20),(-1.10,0.))]))
            h=sub(q,mul(2.85,n));q1=sub(q,mul(.9,n))
            s.append(poly('backing '+name,(q1,h),1.45,n))
            s.append(box('beam '+name,(.95,h[0]+.55),(h[1]-2.,h[1]+2.),(h[2]-2.,h[2]+2.)))
    return s
def face():
    s=lands()
    s.extend([box('lower bridge',(.65,3.85),(-15.40,15.40),(-12.70,-9.20)),
       box('stripper column',(.40,2.85),(-1.45,1.45),(-10.5,1.45)),
       box('crown pusher',(2.30,3.05),(-1.45,1.45),(-1.45,1.45)),
       box('force stalk',(-.5,1.2),(-9.4,-5.75),(-12.7,-9.2))])
    for sign in (-1,1):
        yy=lambda lo,hi:tuple(sorted((lo*sign,hi*sign)))
        s.extend([box('side pillar'+str(sign),(.65,3.85),yy(12.10,15.40),(-12.70,11.55)),
            box('upper bridge'+str(sign),(.65,3.85),yy(5.25,15.40),(9.00,12.35)),
            box('middle bridge'+str(sign),(.65,3.85),yy(11.20,15.40),(-.3,3.25))])
    return s
def mover():
    # Inverted fixed carriage; moving rail covers full carriage and load is
    # fed into a broad backing spar, then the independently sensed stalk.
    return [box('moving 3 rail',(-13.85,20.90),(YRAIL-1.5,YRAIL+1.5),(-15.15,-13.50)),
            box('rail backing spar',(-13.85,20.90),(-8.60,-5.20),(-13.50,-10.00)),
            box('series bridge',(-3.8,-.35),(-13.85,-7.5),(-12.75,-10.10)),
            rod('moving M3 nut',X,(-7.40,-4.60),YS,ZS,2.4),
            box('spring cassette',(-4.60,-.40),(-15.70,-11.60),(-13.65,-10.20)),
            box('X tooth rail on nut',(-8.35,10.75),(-16.90,-15.35),(-13.8,-11.55))]
def xdrive():
    x=-11.70;y=YS;z=ZS;ym=y-.90;zm=z+sqrt(8.10**2-.9**2)
    return [box('MGN3H fixed block',(3.45,18.75),(YRAIL-4.,YRAIL+4.),(-17.50,-13.50)),
            box('block mounting foot',(3.45,18.75),(-11.25,-2.55),(-18.80,-17.50)),
            box('foot return',(1.6,4.90),(-4.80,-2.65),(-17.90,-14.55)),
            rod('M3x.5 X screw',X,(-13.35,14.10),y,z,1.50),
            rod('rear thrust bearing',X,(-10.35,-9.15),y,z,2.65),
            rod('front bearing',X,(12.55,14.10),y,z,2.65),
            rod('X drive wheel',X,(x-1,x+1),y,z,5.70),
            rod('X quill pinion',X,(x-1,x+1),ym,zm,3.00),
            rod('X gearmotor',X,(-10.5,18.20),ym,zm,3.0),
            rod('X motor strap',X,(-7.60,-6.20),ym,zm,3.65),
            rod('X torque limiter',X,(-15.10,-13.15),y,z,3.20),
            box('nut holding pawl',(-7.72,-6.10),(-18.65,-16.55),(-14.0,-11.5)),
            box('pawl lift arm',(-8.0,-6.05),(-19.2,-17.95),(-12.75,-7.25)),
            box('X load pickup',(-1.65,.05),(-10.70,-9.65),(-11.95,-9.65)),
            box('X travel switch',(12.55,14.7),(-17.25,-15.55),(-10.15,-8.35))]
def button():
    a=poly('cone',[ (XP+rr/cos(pi/48)*cos(j*pi/24),rr/cos(pi/48)*sin(j*pi/24),z)
                     for z in (TIP,11.84) for j in range(48) for rr in [.48+K*z]])
    return [a,cyl('button root',Z,(11.84,16.38),(XP,0),ROOT),
            box('top bridge',(10.0,14.72),(-4.35,3.48),(15.50,18.10)),
            poly('folded bridge',[(x,y,z) for x,y in ((10,-3.85),(14.72,-3.85),(12.55,-17.45),(8.35,-17.45)) for z in (15.65,18.10)]),
            box('rack',(8.35,12.55),(-17.45,-14.7),(-3.72,17.85)),
            box('backing lug',(6.95,11.10),(-2.55,2.55),(15.60,17.65))]
def zfixed():
    s=ringpart('root sleeve',(XP,0),ROOT+.06,5.10,(11.94,15.1),step=10)
    # Solid support bridge outside the rising cone and lug footprint.
    s.extend([box('dog support',(2.55,6.65),(-3.85,3.85),(17.72,21.55)),
              box('dog back plate',(2.55,6.65),(-3.85,3.85),(20.10,22.10)),
              box('Z support heel',(2.55,5.25),(-4.15,-2.8),(10.75,18.65)),
              box('sleeve root tie',(4.2,11.1),(-4.2,-2.75),(12.9,14.85)),
              rod('rack pinion',X,(8.35,12.55),-19.55,11.4,2.70),
              rod('rack axle',X,(4.4,13.70),-19.55,11.4,1.15),
              rod('Z final wheel',X,(4.45,6.05),-19.55,11.4,4.80),
              rod('Z motor pinion',X,(4.45,6.05),-16.85,11.4-sqrt(7.20**2-2.70**2),3.00),
              rod('Z motor',X,(-24.45,4.25),-16.85,11.4-sqrt(7.20**2-2.70**2),3.0),
              rod('Z saddle',X,(-16,-14.35),-16.85,11.4-sqrt(7.20**2-2.70**2),3.60),
              rod('Z torque clutch',X,(6.15,7.8),-19.55,11.4,3.4),
              box('rack back shoe',(8.15,12.85),(-14.55,-13.60),(8.8,14.35)),
              box('rack side gib',(7.15,8.15),(-17.85,-14.3),(8.8,14.35)),
              box('rack side gib2',(12.75,13.75),(-17.85,-14.3),(8.8,14.35)),
              box('rack rest',(8.25,12.55),(-17.50,-14.55),(-4.30,-3.85)),
              box('Z end witness',(6.25,7.15),(-17.95,-15.),(9.1,11.65)),
              box('direct root down flag',(7.05,8.50),(3.35,4.75),(13.35,15.20))])
    return s
def dog(opened):
    # Lateral slide in X; flat underside bears on moving lug's flat top.
    # Retract completely before raising either lug or button.
    return mx(box('Z backing bolt',(3.85,9.90),(-2.45,2.45),(17.72,20.02)),-4.45*opened)
def roofs():
    def z(x):return 7.53675+(x-XP)*tan(radians(28))
    out=[]
    for xa,xb,ya,yb in [(8.8,9.649,-4.55,4.55),(9.649,18.80,-4.55,-3.225),(9.649,18.80,3.225,4.55)]:
        out.append(poly('trial open-slot roof '+str((xa,ya)),[(x,y,z(x)+t) for x,y,t in product((xa,xb),(ya,yb),(0,.68))]))
    return out
def stages():
    plate=face()+mover();u=button();z=zfixed()+roofs();x=xdrive();j=tucked_joint()+electr()
    rest=j+z+x
    def dx(q0,q1):return [sweep(mx(a,q0),(q1-q0,0,0)) for a in plate]
    return [('C',dx(REL,0),u,[dog(0)],rest),('W',dx(REL,REL),[sweep(a,(0,0,LIFT)) for a in u],[dog(1)],rest),
            ('E',dx(REL,END),[move(a,(0,0,LIFT)) for a in u],[dog(1)],rest)]
def run():
    zz=zfixed()+roofs();xx=xdrive();jj=tucked_joint()+electr()
    for n,p,z,d,e in stages():
        for label,ss,tt in [('face-button',p[:len(face())],z+d+zz),('face-joint',p[:len(face())],jj),('moving stage-fixed drive',p,xx),('U-joint',z,jj),('U-X',z,xx)]:
            res=pair(ss,tt);print(n,label,sum(v[0]<0 for v in res),res[:5])
    for label,ss,tt in [('X-stationary vs Z',xx,zz),('X vs joint',xx,jj),('Z vs joint',zz,jj),
                        ('face vs passive except intended bosses',face(),[a for a in tail(0) if a[0].startswith(('eye','metal neck','main stem'))])]:
        res=pair(ss,tt);print(label,sum(v[0]<0 for v in res),res[:6])
    for p in (36.,37.5):
        S=face()+mover()+button()+[dog(0)]+xx+zz+jj
        print('stow',p,centre(S+tucked_tail(p)))
        names=('C','E')
        for n,a,u,d,f in stages():
            if n not in names:continue
            for m,b,v,e,g in stages():
                if m not in names:continue
                mm,bad=scan(a+u+d+f,b+v+e+g,p,3,END);print('adjacent',p,n+m,len(bad),mm,bad[:4])
        m,g=scan(face()+mover()+button()+xx+zz,tucked_tail(p),0);print('own deployed hardware closed vs articulated tail',p,len(g),m,g[:5])
if __name__=='__main__':run()
