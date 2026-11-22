"""Take 42. Fixed vertical cantilever pin + translating indexed face. Exploratory, mm/N."""
from runpy import run_path
from pathlib import Path
from itertools import product
from math import *
g=run_path(str(Path(__file__).resolve().parents[1]/'cand-d-transverse-vise'/'oblique-drive.py'))
globals().update({k:g[k] for k in ('X','Y','Z','H','poly','box','dot','plus','sub','mul','unit','rot','far','proj','sweep','move','yaw','sep','BASIC','setscan','check_pair')})
XP=12.95; C=15.; R=6.50; TUBE=2.70; PIN=1.75; JMIN=12.55; JMAX=17.15
TIP=-6.; PARK=10.15; DZ=PARK-TIP
O=(-2.80,-.40,.70); REL=-1.35; END=13.80
BS=[(7.,-5.04,0.),(18.,2.56,0.),(18.,-13.44,0.)]; SLOPE=[1.2,-.8,-.8]
def cyl(n,i,span,a,b,r):
    j=(X,Y,Z).index(i)
    def pt(h):p=[a,b];p.insert(j,h);return tuple(p)
    return poly(n,[pt(h) for h in span],r,i)
def ball(n,p,r):return poly(n,[p],r)
def cap(n,p,q,r):return poly(n,[p,q],r)
def mx(s,x):return move(s,(x,0.,0.))
def span(s,n):return tuple(round(v,3) for v in proj(s,n))
def ann(n,i,h,a,b,ri,ro,step=30):
    u,v=(X,Y) if i==Z else (Y,Z) if i==X else (X,Z)
    # Circumscribed outer polygon, tangent hole polygon (hole is no bigger
    # than true bore). Useful for non-fit pairs; fits checked analytically.
    return [poly(n+str(k),[plus(mul(y,i),plus(mul(a+l*cos(t),u),mul(b+l*sin(t),v))) for t,l,y in product(
        [radians(k),radians(k+step)],[ri,ro/cos(radians(step/2))],h)]) for k in range(0,360,step)]
def tail(p=0,art=True):
    o=C-p;s=[]
    def ring(t):return (o+R*cos(radians(t)),R*sin(radians(t)),0.)
    for k in range(0,360,15):s.append(cap('torus'+str(k),ring(k),ring(k+15),TUBE+R*(1-cos(radians(7.5)))))
    for j,b in enumerate(BS):
        b=plus(b,(-p,0,0));s.append(ball('boss'+str(j),b,TUBE))
        a=atan2(b[1],b[0]-o)
        s.append(cap('boss neck'+str(j),ring(degrees(a)),b,1.65))
    s.append(cap('main neck',(o+R,0,0),(o+11.,0,0),2.70))
    if art:
        for sg in (-1,1):
            tip=(H[0] if p else -6.5+36,H[1],7.8*sg)
            s.append(cap('fork '+str(sg),(o+10.1,0.,1.1*sg),tip,1.30))
    return s
def seats():
    s=[];A=radians(58.)
    for j,(b,k) in enumerate(zip(BS,SLOPE)):
        f=unit((1.,k,0.));h=(-f[1],f[0],0.)
        for sign in (-1,1):
            n=plus(mul(cos(A),f),mul(sign*sin(A),Z))
            v=plus(mul(-sin(A),f),mul(sign*cos(A),Z))
            q=sub(b,mul(TUBE,n))
            s.append(poly('land%d/%d'%(j,sign),[plus(q,plus(mul(t,h),plus(mul(w,v),mul(e,n))))
                for t,w,e in product((-.67,.67),(-.70,.70),(-.66,0.))]))
            aq=sub(q,mul(.60,n));back=sub(aq,mul(.65,f)); top=(back[0],back[1],-sign*4.00)
            s.append(cap('land stem%d/%d'%(j,sign),aq,top,.48))
            # Paired metal tines at z +/-4.0; extend to the REAR of each land.
            z=-sign*4.
            s.append(box('tine%d/%d'%(j,sign),(.30,top[0]+.42),(top[1]-.63,top[1]+.63),(z-.52,z+.52)))
    return s
def slide():
    s=seats()
    # A split upper/lower H face; no sheet at z=0 across the fixed pin.
    for z in (-4.,4.):
        s.append(box('face cross-tie'+str(z),(-.65,1.12),(-14.65,5.48),(z-.62,z+.62)))
    s+=[box('outer tie',(-.65,1.12),(-14.65,-12.9),(-4.45,7.6)),
        box('face centre column',(-.65,1.12),(-1.26,1.26),(-4.45,4.45)),
        box('central stripper',(.65,5.48),(-1.2,1.2),(-1.25,1.25)),
        box('thrust bridge',(-.45,1.65),(-14.65,-7.60),(5.7,8.10)),
        box('roll link',(-.65,1.12),(4.15,6.05),(3.48,7.95))]
    # Master and roll bars translate; fixed short gibs behind the head.
    for y,z,dy in [(-14.,6.65,1.),(5.45,7.15,.85)]:
        s.append(box('slide bar '+str(y),(-23.1,.82),(y-dy,y+dy),(z-.85,z+.85)))
    s.append(cyl('translating screw',X,(-23.95,1.4),-9.15,6.95,1.25))
    return s
def shortdrive():
    s=[]
    y,z=-9.15,6.95
    for a,b,r,n in [(-6.45,-4.65,2.9,'rear nut race'),(-4.65,-2.30,5.25,'nut gear'),
                     (-2.30,-.80,2.85,'nose nut race')]:s.append(cyl(n,X,(a,b),y,z,r))
    ym,zm=-15.6,6.95  # pitch radii 4.80/1.65
    s += [cyl('X motor pinion',X,(-4.6,-2.35),ym,zm,1.94),
          cyl('X gearmotor',X,(-2.0,20.30),ym,zm,3.0),
          cyl('X gearmotor saddle',X,(.25,2.15),ym,zm,3.45),
          cyl('X clutch OD',X,(-7.65,-6.4),y,z,3.75),
          cyl('X brake drum OD',X,(-8.9,-7.65),y,z,3.85),
          box('X ratchet pawl',(-8.9,-7.5),(-14.10,-11.60),(7.0,9.65)),
          box('X dog lifter',(-9.7,-6.7),(-15.65,-13.65),(8.5,10.85))]
    for j,(yy,zz,dy) in enumerate([(-14.,6.65,1.),(5.45,7.15,.85)]):
        # Real side/back faces rather than a solid through the bar.
        for k in (-1,1):
            for name,c,d in [('y',yy,dy),('z',zz,.85)]:
                if name=='y':s.append(box('gibY'+str((j,k)),(-7.95,-1.70),(yy+k*(dy+.62)-.50,yy+k*(dy+.62)+.50),(zz-1.9,zz+1.9)))
                else:s.append(box('gibZ'+str((j,k)),(-7.95,-1.70),(yy-dy-.10,yy+dy+.10),(zz+k*1.43-.46,zz+k*1.43+.46)))
    return s
def roof2():
    # Decompose x/y plane minus round bore into cells. A regular 24-gon HOLE
    # is inscribed in the true bore: conservative occupied over-bound.
    out=[];r=1.85;zl=lambda x:x-4.53
    for j in range(12):
        xa=XP-r*cos(j*pi/12);xb=XP-r*cos((j+1)*pi/12);ya=r*sin(j*pi/12);yb=r*sin((j+1)*pi/12)
        for sg in (-1,1):
            pts=[(xa,sg*ya),(xa,sg*3.8),(xb,sg*3.8),(xb,sg*yb)]
            out.append(poly('roof bore '+str((j,sg)),[(x,y,zl(x)+t) for x,y in pts for t in (0.,.65)]))
    for a,b in [(9.75,XP-r),(XP+r,18.60)]:
        out.append(poly('roof end '+str(a),[(x,y,zl(x)+t) for x,y,t in product((a,b),(-3.8,3.8),(0.,.65))]))
    return out
def pin(z=0.):
    s=[cyl('pin shank',Z,(TIP+PIN,17.95),XP,0.,PIN),ball('pin tip', (XP,0.,TIP+PIN),PIN),
       box('U pin crossbar',(11.02,14.88),(-1.90,13.15),(17.55,19.85)),
       box('moving rack stock',(11.1,14.80),(10.40,13.40),(-7.05,18.75))]
    return [move(v,(0,0,z)) for v in s]
def zdrive():
    s=roof2()+ann('sleeve',Z,(JMIN,JMAX),XP,0,1.80,3.15,15)
    # Top bridge in two arms into body bulkhead, with bypass around bore.
    for y in [-2.75,2.75]:
        s.append(box('root rail '+str(y),(-1.25,13.75),(y-.70,y+.70),(13.0,16.70)))
    s.append(box('root rear cross',(-1.45,.20),(-3.60,3.60),(12.85,16.70)))
    s+=[box('root rear web',(-2.25,-1.10),(-3.65,3.65),(7.25,16.70)),
        box('main bulkhead',(-2.95,-1.75),(-13.40,3.65),(7.85,10.35))]
    y,z=15.50,11.70;b=(8.15,10.2075)
    y2=b[0]+4.6;z2=b[1]-sqrt(7.7**2-4.6**2)
    for n,ax,yy,zz,r in [('rack pinion',(11.15,14.70),y,z,2.70),('A wheel',(8.4,9.85),y,z,6.00),
         ('B pinion',(8.4,9.85),*b,2.10),('B wheel',(5.9,7.4),*b,6.20),('Z motor pinion',(5.9,7.4),y2,z2,2.10),
         ('Z gearmotor',(-22.85,5.85),y2,z2,3.00),('Z motor saddle',(-15.5,-13.5),y2,z2,3.50),
         ('A axle',(7.8,15.65),y,z,1.20),('B axle',(5.0,10.5),*b,1.15),
         ('A inner bush',(7.60,8.35),y,z,2.00),('A outer bush',(14.78,15.7),y,z,2.00),
         ('Z torque clutch',(9.9,11.05),y,z,3.60),('Z brake drum',(7.,7.75),y,z,3.10)]:
        s.append(cyl(n,X,ax,yy,zz,r))
    s+= [box('Z dog',(6.95,7.95),(17.8,20.05),(10.3,12.35)),
         box('Z dog lifter',(5.8,8.3),(18.35,20.65),(12.35,14.45)),
         box('rack guide near',(10.10,10.95),(10.10,13.85),(9.00,15.25)),
         box('rack guide far',(14.94,15.80),(10.10,13.85),(9.,15.25)),
         box('rack back shoe',(10.96,14.94),(9.25,10.27),(9.,15.25)),
         box('rack lower guard',(10.15,15.7),(8.96,9.55),(-7.55,9.15)),
         box('rack lower stop',(10.8,15.15),(10.3,13.6),(-7.75,-7.15)),
         box('direct pin sensor',(9.65,10.93),(-1.0,1.),(16.,17.2)),
         box('retract witness switch',(10.,11.),(9.4,11.15),(8.25,9.4)),
         box('Z gear cover',(5.6,5.85),(4.2,12.3),(7.2,15.5))]
    return s
def body():
    s=[box('cell',(-11.65,9.05),(-15.325,15.325),(-21.95,-16.55)),
       box('MCU',(-13.75,8.25),(-8.9,8.9),(19.2,24.9)),
       cyl('joint motor',Z,(-12.7,7.),-7.9613,-18.1978,3.20),
       cyl('hinge pin',Z,(-8.65,8.65),*H[:2],1.5),
       cyl('joint pinion',Z,(-14.38,-12.80),-7.9613,-18.1978,2.10),
       box('driver pair',(-11.,.50),(-5.5,4.),(-14.15,-11.9)),
       box('power cutoff',(2.,8.8),(-7.,2.4),(-13.85,-11.6)),
       box('power connector',(-13.1,-9.4),(-7.8,-4.5),(-15.7,-12.2)),
       box('routed control channel',(-11.0,-8.8),(-13.35,-5.2),(-11.35,-9.10)),
       box('slide actual switch',(1.65,3.7),(-15.9,-14.8),(8.15,9.90)),
       box('series load pickup',(-7.4,-5.3),(-10.9,-7.2),(9.95,11.60))]
    for z in [(-9.35,-7.55),(7.55,9.35)]:s+=ann('hinge ear',Z,z,*H[:2],1.55,2.3,45)
    for x,y in product((-11.,10.5),(-8.9,8.9)):
        s.append(box('foot'+str((x,y)),(x-1.45,x+1.45),(y-1.30,y+1.30),(-23.65,-22.25)))
    return s
def sector():
    return [poly('yaw sector '+str(a),[(H[0]+r*cos(radians(v)),H[1]+r*sin(radians(v)),z)
          for v,r,z in product((a,a+3),(4.5,9./cos(radians(1.5))),(-14.38,-12.80))]) for a in range(-119,-77,3)]
def chk(s,t):
    cc=lambda p:tuple(sum(v)/len(v) for v in zip(*p[1]))
    n=sub(cc(s),cc(t));axes=BASIC+((unit(n),) if hypot(*n) else ())
    return check_pair(s,t,axes)-.20
def pair(n,A,B):
    w=sorted((round(chk(s,t),3),s[0],t[0]) for s in A for t in B)
    print(n,'unseparated',sum(d<0 for d,a,b in w),'lowest',w[:7])
def coarse():
    S=slide();Zf=zdrive();Xf=shortdrive();B=body();p=pin()
    for n,a,b in [('slide vs rack and roof (locked)',S,Zf+p),
       ('slide rel->ejected vs open pin and roof',[sweep(mx(s,REL),(END-REL,0.,0.)) for s in S],Zf+pin(DZ)),
       ('X drive vs Z drive',Xf,Zf),('X drive vs cell/controller/joint',Xf,B),
       ('Z drive vs cell/controller/joint',Zf,B),('slide vs electronics',S,B),
       ('U over continuous Z vs X drive and electronics',[sweep(s,(0,0,DZ)) for s in p],Xf+B),
       ('U vs fixed Z drive over stroke',[sweep(s,(0,0,DZ)) for s in p],Zf),
       ('slide vs seated torus',S,[s for s in tail() if s[0].startswith('torus')])]:
        pair(n,a,b)
    for pp in (33.,35.,36.,37.5):
        solids=S+Zf+Xf+B+p+tail(pp)+sector()
        print('stow',pp,O,sorted([(round(2*far(s,O),3),s[0]) for s in solids],reverse=True)[:5])
if __name__=='__main__':coarse()
