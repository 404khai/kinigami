"""Exploratory fixed low X rails and transverse motor; exact external Take 51 v3 face, hood, tail and pivot."""
from runpy import run_path
from pathlib import Path
G=run_path(str(Path(__file__).with_name('horn-link-take50.py')))
globals().update({k:v for k,v in G.items() if not k.startswith('__')})
import json
inp=json.loads((Path(__file__).resolve().parents[1]/'cand-d-forced-section/take51-interface-v3.json').read_text())
def shp(s):return s[0],tuple(map(tuple,s[1])),s[2],tuple(s[3]) if s[3] else None
F51=list(map(shp,inp['face_home']))
def joint51():return list(map(shp,inp['joint']))
def hood51():return list(map(shp,inp['hood_blank']))
def roof51():return hood51()[:-1]
H=tuple(inp['H']);assert H==(-5.9,0.,0.)
def yaw(s,a,p=0):
    return s[0],tuple(plus(plus(H,(p,0,0)),rot(sub(v,H),a)) for v in s[1]),s[2],rot(s[3],a) if s[3] else None
def ytest(A,B,step=1,p=0):
    out=[];by={s[0]:s for s in B}
    for ang in range(-15,16,step):
        for g,n,m in fastpair(A,[yaw(s,radians(ang),p) for s in B]):
            debit=.20+2*far(by[m],H)*sin(radians(step/4))
            if g<debit+.70:out.append((g-debit,n,m,ang))
    return sorted(out) or [(.70,'all','separate',0)]
def tail51(p=P):
    return [mx(shp(s),P-p) for s in inp['own_tail_straight']]
def cheeks50():
    a=[]
    for sg in (-1,1):
        for n,y0,y1,ri,ro in [('lined radial bearing',9.42,12.40,2.03,3.25),('metal bearing outer',9.40,12.42,3.25,4.05)]+([('frame thrust inner',9.39,9.50,2.06,3.32),('frame thrust outer',12.40,12.50,2.06,3.32)] if sg>0 else []):
            for q in ringpart(n+str(sg)+'/',O,ri,ro,tuple(sorted((sg*y0,sg*y1))),step=12):
                a.append(poly(q[0],[(x,y,z) for x,z,y in q[1]]))
    a.append(box('v3 cheek mounting return',(-8.09,-3.08),(12.10,12.75),(-6.60,-5.72)))
    a.append(box('positive idle post',(-4.05,-3.08),(11.70,12.65),(-5.82,19.67)))
    a.extend([box('top rail saddle',(-2.06,-1.21),(4.65,12.68),(ZH+1.40,ZH+2.34)),box('outside rail lintel',(-14.45,-1.38),(11.75,12.68),(ZH+1.44,ZH+2.33)),box('key guide lug',(-6.66,-5.52),(9.65,12.65),(ZH+4.0,ZH+4.85)),box('key bracket back',(-6.70,-5.66),(11.75,12.72),(ZH+1.72,ZH+4.88))])
    a.append(box('negative idle tie',(-3.58,-2.56),(-11.35,-4.12),(-.50,1.25)))
    return a
def keyparts(u):
    # Outboard forked linear cam with a straight captive slot. Upper/lower
    # strips below are stock, not a solid plate falsely filling the slot.
    assert 0<=u<=4.70
    x=NC-5.50-.08-.80; z=ZH+4.50; lift=.50*u; a=[]
    a.extend([box('holding key',(x-.80,x+.80),(6.00,10.00),(ZH+1.+lift,ZH+3.36+lift)),
              box('guided key stem',(x-.75,x+.75),(7.40,8.60),(ZH+3.25+lift,ZH+5.25+lift)),
              ar('key follower crosspin',x,z+lift,6.42,9.58,.49)])
    for sg in (-1,1):
        yy=tuple(sorted((8+sg*.81,8+sg*1.50)))
        for j,(l,h) in enumerate(((-1.39,-.56),(.56,1.39))):
            a.append(poly('lifter slot flank'+str((sg,j)),[(x+t+u,y,z-.50*t+off) for t,y,off in product((-5.48,.78),yy,(l,h))]))
    a.extend([box('wedge crosshead',(x-5.48+u,x-4.73+u),(6.45,12.95),(z+2.38,z+3.63)),
              box('lift actuator finger',(x-5.48+u,x-4.73+u),(12.22,12.95),(20.39,z+3.40)),
              cyl('lifter positive pushrod',X,(-13.65+u,x-4.90+u),(12.60,20.80),.55)])
    return a
def grip50():
    x=NC-3.10+.04; key=keyparts(0);other=keyparts(4.70)
    a=[poly(s[0]+' allocated motion',s[1]+t[1],s[2],s[3]) for s,t in zip(key,other)]
    a.extend([cyl('key lifter',X,(-18.40,-12.40),(12.60,20.80),2.10),
              box('key rear guide land',(NC-7.82,NC-7.24),(7.54,8.46),(ZH+3.42,ZH+5.62)),
              box('key front guide land',(NC-5.52,NC-4.93),(7.54,8.46),(ZH+3.42,ZH+5.62)),
              box('key left guide',(NC-7.19,NC-5.73),(5.41,5.93),(ZH+2.82,ZH+5.62)),
              box('key right guide',(NC-7.19,NC-5.73),(10.07,10.59),(ZH+2.82,ZH+5.62)),
              box('forward closed stop',(x,x+1.10),(5.80,10.20),(ZH+1.60,ZH+2.95)),
              box('stop anchor',(x+.80,x+2.10),(5.80,12.85),(ZH+2.30,ZH+3.35)),
              cyl('key spring X envelope',X,(-17.25,-11.75),(10.90,22.45),.80),
              box('key seat switch',(x-4.85,x-4.15),(10.25,11.10),(ZH+2.65,ZH+4.75))])
    return a
ZSX=-20.30;XS=-15.16;YSX=0.;YRAIL=5.60;XR0=-11.0;XR1=-4.10
def lowfixed():
    a=[];mn=XR0+REL-1.08;mx0=XR1+END+1.09
    for sg in (-1,1):
        y=sg*YRAIL
        a.extend([box('T rail head '+str(sg),(mn,mx0),(y-.98,y+.98),(-20.25,-18.95)),
                  box('T rail web '+str(sg),(mn,mx0),(y-.48,y+.48),(-21.72,-20.23)),
                  box('T rail sole '+str(sg),(mn,mx0),(y-1.40,y+1.40),(-22.52,-21.65))])
    def ry(n,lo,hi,x,z,r):return cyl(n,Y,(lo,hi),(x,z),r)
    def rx(n,lo,hi,y,z,r):return cyl(n,X,(lo,hi),(y,z),r)
    zm=ZSX+.63;xm=XS-sqrt(5.**2-.63**2)
    a.extend([rx('face screw',XS-3.15,10.85,0,ZSX,1.50),
              rx('face paired thrust bush',-11.85,-10.40,0,ZSX,2.50),
              rx('face bevel X 22T',XS+1.62,XS+2.26,0,ZSX,2.42),
              ry('face bevel Y 22T',-2.26,-1.62,XS,ZSX,2.42),
              ry('90 degree bevel cross shaft',-18.85,-1.68,XS,ZSX,.95),
              ry('bevel inner bush',-4.15,-2.50,XS,ZSX,1.52),ry('bevel outer bush',-18.85,-17.65,XS,ZSX,1.55),
              ry('bevel spur 28T',-17.40,-16.20,XS,ZSX,3.00),
              ry('face 22T input',-17.40,-16.20,xm,zm,2.40),ry('face quill',-18.8,-15.7,xm,zm,.90),
              ry('face input bush',-18.82,-17.60,xm,zm,1.50),
              ry('face Y motor',-15.65,13.05,xm,zm,3.),ry('face clamp',-11.7,-10.40,xm,zm,3.45),
              box('face gear cover back',(xm-1.50,XS+1.50),(-19.10,-18.75),(ZSX-.98,zm+.95)),
              box('bevel frame bridge',(XS-1.2,XS+1.0),(-15.0,-2.75),(ZSX-2.95,ZSX-1.78)),
              box('thrust tie',(-11.84,-10.4),(-5.9,.95),(-22.50,-21.60)),
              box('torque strap',(-11.84,-10.4),(-2.9,1.5),(-22.58,-21.60))])
    # Retractable shouldered plunger on the unloaded nut rack, not the series path.
    a.extend([cyl('X rack lifter',X,(-1.55,4.85),(9.,-21.62),1.18),
              box('key pull rod',(-7.00,-1.26),(8.76,9.28),(-22.75,-22.30)),
              ry('X key rocker axle',-3.32,9.24,-6.90,-23.18,.28),
              box('X key tongue range',(-7.56,-6.31),(-3.25,-2.62),(-23.26,-20.84)),
              box('X key return spring',(-9.46,-7.30),(8.40,9.52),(-23.15,-22.14))])
    return a
def lowmoving():
    a=[]
    for sg in (-1,1):
        y=sg*YRAIL
        for i,x in enumerate((XR0,XR1)):
            xx=(x-1.,x+1.)
            a.append(box('shoe roof '+str((sg,i)),xx,(y-1.78,y+1.78),(-18.88,-17.89)))
            for j in (-1,1):
                yy=lambda aa,bb:tuple(sorted((y+j*aa,y+j*bb)))
                a.extend([box('shoe side '+str((sg,i,j)),xx,yy(1.05,1.78),(-21.18,-18.0)),
                          box('shoe lip '+str((sg,i,j)),xx,yy(.56,1.78),(-21.18,-20.32))])
        a.append(box('moving keel '+str(sg),(XR0-1.,5.58),(y-1.45,y-.27),(-18.71,-17.80)))
    a.extend([cyl('face nut',X,(-8.55,-6.55),(0,ZSX),2.47),
              box('face nut rack',(-8.50,-4.20),(-3.32,-2.10),(ZSX-1.05,ZSX+.65)),
              box('nut top takeoff',(-8.45,-6.65),(-2.48,1.55),(-18.68,-17.95)),
              box('series pack',(-6.72,-2.80),(-3.38,-1.64),(-20.70,-17.95)),
              box('series thrust heel',(-2.90,-1.85),(-4.26,-1.80),(-18.77,-17.86)),
              box('axial crosshead',(-2.5,-1.0),(-6.87,5.60),(-18.68,-17.80)),
              box('strain bridge',(2.48,5.65),(-7.20,7.20),(-18.68,-17.78)),
              box('gauged neck',(2.62,4.98),(-7.2,7.2),(-17.91,-16.13)),box('U bottom backing',(2.62,4.98),(-7.2,7.2),(-16.72,-8.72))])
    return a
def allmotor():return drive50()+guides()+grip50()
def inter():
    f=fp(F51);t=tail51();h=allmotor();xf=lowfixed();xm=lowmoving();sm=stages()
    for n,a,b in [('root fixed / face',h,f),('root swept / face',sm,f),('X fixed vs face',xf,f),('X new vs root fixed',xf+fp(xm),h),('X vs joint',xf+fp(xm),joint51()),
                  ('v3 face vs v3 joint',f,joint51()),('new face vs hood',f,roof51()),('parked link/guide vs fixed',rodparts(PH),drive50())]:
        print(n,fastpair(a,b)[:4],flush=True)
    for n,a in [('root fixed',h),('short root link',sm),('fixed X',xf),('moving X',fp(xm)),('face51',f)]:
        print(n,'own Take51 tail',ytest(a,t,1)[:4],flush=True)
    print('X fixed rails x span',ab(xf[0])[0],'next rail gap',P+ab(xf[0])[0][0]-ab(xf[0])[0][1])
    for f in (111,155,163,170.43,200,208.30):
        for mu in (.10,.23):
            # Two transverse directions bound; no equal bearing sharing credited.
            pitch=abs(ZSX)+abs(YSX);ecc=abs(ZSX+18.95)+YRAIL+.98
            d=XR1-XR0;drag=2*mu*f*pitch/(d-2*mu*ecc);fr=f+drag
            print('Fx mu aligned guide drag, axial, motor Nmm (0.28,0.72)',f,mu,drag,fr,(fr*.5/(2*pi*.28))/(28/22*.72))
if __name__=='__main__':inter()
