"""Take59 exploration: both output reactions. No other coupler in this model."""
from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('flange-stock-take59.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
import os
ALT=int(os.getenv('FLANGE_LAYOUT','2'))
O=17.04;P=38.;HOME=-3.61-(2.50/sin(pi/4)-2.18+1.48);END=1.05;TR=END-HOME
C=O-2.25;R=10.75;RE=2.50;RD=12.63
U=lambda a:np.array([0.,cos(radians(a)),sin(radians(a))])
X=np.eye(3)[0];H=np.array([-5.9,0.,0.])
def sbox(n,xs,rs,ts,a):
 u=U(a);v=U(a+90)
 return sol(n,[x*X+r*u+t*v for x,r,t in product(xs,rs,ts)])
def washer(n,xs,ris,ros,a,b,inner=False):
 # Circular sector chordal OUTER/INNER material certificate for linear RI/RO.
 u=cos(radians(b-a)/2);v=[]
 for x,ri,ro in zip(xs,ris,ros):
  for r in ((ri/u,ro) if inner else (ri,ro/u)):
   v.extend([x*X+r*U(t) for t in (a,b)])
 return sol(n,v)
def ring(n,xs,ris,ros,nb=48):
 return [washer(n+str(j),xs,ris,ros,360*j/nb,360*(j+1)/nb) for j in range(nb)]
def frust(n,xs,rs,off=(0,0),inner=False):
 d=cos(pi/48) if not inner else 1
 return sol(n,[[x,off[0]+r*cos(t)/d,off[1]+r*sin(t)/d] for x,r in zip(xs,rs) for t in np.arange(48)*pi/24])
def flange():
 t=[sol('one-piece rolled flange and solid core',[C*X+(R/cos(pi/64))*U(j*360/64) for j in range(64)],RE)]
 for j,a in enumerate((-90,30,150)):
  t.append(sol('tail ball index '+str(j),[(O-3.61)*X+8.4*U(a)],2.50))
 # Starts at full broad footprint; no thin neck in the head. Continues
 # directly into two rear gusset forks and the articulated joint's lugs.
 t += [frust('broad tail socket',(C+1.95,C+4.50,C+8.05),(10.08,9.,5.66))]
 for k in (-1,1):
  t += [sol('web fork '+str(k),[[x,y,k*z] for x,hy,ranges in [(C+6.25,3.3,(1.7,5.08)),(C+9.0,2.15,(3.,6.45)),(P-9.5,1.45,(4.31,6.66))] for y in (-hy,hy) for z in ranges])]
 t+=shift([s for s in V['own_tail_straight'] if s[0].startswith(('tail pivot lug','sector web','tail sector hub','fork tip'))],P)
 return t
def disk():
 g=[frust('solid metal ejector plate',(O+HOME-1.45,O+HOME),(RD-.42,RD))]
 for j,a in enumerate((-90,30,150)):
  u=U(a);v=U(a+90)
  for k in (-1,1):
   c=8.4*u+k*2.18*v
   g.append(frust('cone seat '+str((j,k)),(O+HOME,O+HOME+1.48),(1.48,0.),c[1:]))
  g.append(sbox('disk rear rib '+str(j),(O+HOME-2.23,O+HOME-1.38),(1.85,9.95),(-1.05,1.05),a))
 for a in (-90,30,150):
  p=9.25*U(a)
  g.append(cy('disk seat shoe '+str(a),0,(O+HOME-2.53,O+HOME-1.44),p[1:],1.45))
 for j,a in enumerate((60,210)):
  p=6.85*U(a)
  g.append(cy('guided disk dowel '+str(j),0,(O+HOME-TR-5.2,O+HOME-1.38),p[1:],1.16))
 p=np.array([0.,4.85,0])
 g += [cy('disk translating M3 threaded piston',0,(-5.52,O+HOME-1.39),p[1:],1.50),
       bx('keyed screw-to-disk block',(O+HOME-2.36,O+HOME-1.32),(3.12,6.65),(-1.74,1.74))]
 return g
def gearpin(n,x,a,r,rr,l=1.25):
 p=r*U(a);return cy(n,0,(x,x+l),p[1:],rr)
def anchors():
 f=[]
 for j,a in enumerate((-90,30,150)):
  q=9.25*U(a)
  f+=[cy('hard disk home button '+str(j),0,(O+HOME-3.68,O+HOME-2.53),q[1:],1.45),
      sbox('stop spider leg '+str(j),(O+HOME-4.46,O+HOME-3.56),(7.55,17.95),(-1.20,1.20),a)]
 for j,a in enumerate((60,210)):
  q=6.85*U(a)
  f.append(cy('disk post bush OD '+str(j),0,(O+HOME-5.27,O+HOME-2.52),q[1:],2.18))
  f.append(rod('post support '+str(j),(O+HOME-4.10)*X+q,(O+HOME-4.10)*X+11.2*U(a-23),1.00))
 return f
def drives():
 # Ring internal gear and Geneva on adjacent concentric shaft; no assumption
 # that the gearhead can react output-shaft radial or axial loads.
 a=205.;rr=17.50;rs=rr-2.5;g0=O-7.24;ci=g0-1.92;gc=5.50
 c=rs*U(a);dc=(rs-gc)*U(a);stroke=TR;f=[]
 f += [cy('clamp pinion 20T',0,(g0,g0+1.13),c[1:],2.76),cy('clamp pinion shaft',0,(ci-2.50,g0+1.35),c[1:],1.0),
       cy('clamp pinion bearing',0,(ci-2.48,ci-1.30),c[1:],2.03),cy('clamp pinion shoulder',0,(ci+.88,g0-.12),c[1:],1.82),
       cy('clamp eight slot wheel blank',0,(ci-.74,ci+.56),c[1:],5.34),cy('clamp blocking disk and pin swept',0,(ci-.74,ci+.56),dc[1:],2.46),
       cy('clamp crank plate',0,(ci-1.64,ci-.86),dc[1:],2.77),cy('clamp crank quill',0,(ci-4.55,ci+.80),dc[1:],.91),
       cy('clamp carrier bush',0,(ci-3.54,ci-2.18),dc[1:],1.80),cy('clamp gearmotor',0,(ci-4.10-32.80,ci-4.10),dc[1:],3.00)]
 if ALT==2:
  f=[s for s in f if s[0]!='clamp gearmotor']
  y,z=dc[1:];x=ci-3.68;mx=x+1.58-3.75;mz=z-5
  f += [cy('clamp crank bevel',0,(x-.3,x+.62),(y,z),2.37),
        cy('clamp driven bevel mate',1,(y-2.40,y-1.48),(x+1.58,z),2.38),
        cy('clamp jackshaft',1,(-18.72,y-1.45),(x+1.58,z),.84),
        cy('clamp jack bearing',1,(-16.44,-15.27),(x+1.58,z),1.76),
        cy('clamp 32T input',1,(-18.64,-17.59),(x+1.58,z),4.24),
        cy('clamp motor pinion',1,(-18.64,-17.59),(mx,mz),2.46),
        cy('clamp pinion quill',1,(-20.60,-15.08),(mx,mz),.78),
        cy('clamp outer quill bush',1,(-20.52,-19.31),(mx,mz),1.71),
        cy('clamp inner quill bush',1,(-17.0,-15.55),(mx,mz),1.76),
        cy('clamp gearmotor',1,(-14.9,17.90),(mx,mz),3.)]
 # Disk: fixed rotating M3 nut directly indexed. Centreline 4.85 off axis.
 # Motor at +Z / +Y offset; flex and races, not the motor, take screw thrust.
 ix=3.98;sc=np.array([0,4.85,0]);ic=sc+5.50*U(115)
 f += [cy('disk rotary M3 nut',0,(2.05,6.90),sc[1:],2.44),
       cy('disk doublet rear race OD',0,(1.95,3.12),sc[1:],3.48),cy('disk doublet front race OD',0,(5.35,6.90),sc[1:],3.48),
       cy('disk index wheel OD',0,(ix-.68,ix+.65),sc[1:],5.34),cy('disk index locking sector sweep',0,(ix-.68,ix+.65),ic[1:],2.46),
       cy('disk index crank plate',0,(ix+.81,ix+1.52),ic[1:],2.78),cy('disk crank quill',0,(ix-3.00,ix+1.52),ic[1:],.94),
       cy('disk input bearing',0,(ix-2.45,ix-1.12),ic[1:],1.81),cy('disk quill bevel gear',0,(ix-3.54,ix-2.49),ic[1:],2.47)]
 # transverse motor and 1:1 bevel: motor displacement below axis is via gears
 x=ix-2.85;yy=ic[1];z=ic[2];mx=x-3.75;mz=z+5
 f += [cy('disk bevel jack',1,(yy-2.47,yy-1.52),(x+1.55,z),2.47),
       cy('disk jackshaft',1,(-16.88,yy-1.40),(x+1.55,z),.86),cy('disk jack bearing',1,(-14.22,-12.65),(x+1.55,z),1.80),
       cy('disk 32T',1,(-16.75,-15.64),(x+1.55,z),4.24),cy('disk 18T pinion',1,(-16.75,-15.64),(mx+1.55,mz),2.45),
       cy('disk pinion quill',1,(-18.60,-13.38),(mx+1.55,mz),.77),cy('disk pinion outrigger',1,(-18.50,-17.15),(mx+1.55,mz),1.70),
       cy('disk motor inner bush',1,(-15.30,-13.96),(mx+1.55,mz),1.72),cy('disk gearmotor',1,(-13.15,19.65),(mx+1.55,mz),3.)]
 f += [rod('ring drive-to-frame bracket',(ci-2.55)*X+dc,(O+HOME-4.0)*X+12.0*U(150),1.29),
       rod('disk bearing mount',(3.10,7.30,-1.50),(O+HOME-4.0)*X+10.*U(30),1.1),
       rod('disk thrust frame return',(4.55,6.8,-1.68),(O+HOME-4.0)*X+11.*U(-90),1.12),
       rod('guide frame rear anchor',(O+HOME-4.0)*X+12.*U(-90),(-2.42,-4.25,-12.38),1.28),
       bx('motor driver shutoff reserve',(-3.50,-.05),(6.32,8.05),(-7.1,-2.6))]
 return f
