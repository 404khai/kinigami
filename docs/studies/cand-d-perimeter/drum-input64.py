"""Provisional Take61 pivot data; explicit complete section and 120-degree phase."""
from pathlib import Path
from runpy import run_path
g=run_path(str(Path(__file__).with_name('drum-primitives64.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
AZ=(-90.,30.,150.);BAZ=(-30.,90.,210.);HX=-2.576717461;HR=13.778519111;AL=-degrees(atan(.28)+asin(.48))
HORN=4.40;CAM=105.;T0=0.;FINAL=8.35;LEAF_W=3.20;DR=10.68;LR=16.42;FACE=radians(65)
def ease(u):return .5-.5*cos(pi*np.clip(u,0,1))
def phase(th):
 # Positive th is OPEN. Nonzero final draw slope over -3..+10 deg.
 # Cubic Hermite reaches a zero-slope park; reversible thereafter.
 if th<=10:ang=AL+.35*th
 elif th<44:
  z=(th-10)/34;ang=(2*z**3-3*z**2+1)*(AL+3.5)+(z**3-2*z**2+z)*(.35*34)
 else:ang=0.
 h=FINAL*ease((th-48)/51)
 return radians(ang),h
def pos(a,x,r,t=0):return (O+x)*X+r*U(a)+t*U(a+90)
def sec(n,x,r,t,a):return sbox(n,tuple(O+np.array(x)),r,t,a)
def rad(n,x,r,t,a,span):return sol(n,[pos(a,x,rr,t) for rr in span],r,U(a))
def tang(n,x,r,t,a,sz):return sol(n,[pos(a,x,r,q) for q in t],sz,U(a+90))
def xcy(n,x,r,t,a,sz):return cy(n,0,tuple(O+np.array(x)),pos(a,0,r,t)[1:],sz)
def hingept(x,r,t,ang,a):
 c=cos(ang);s=sin(ang);return pos(a,HX+c*(x-HX)-s*(r-HR),HR+s*(x-HX)+c*(r-HR),t)
def horn(ang):return HX-HORN*sin(ang),HR+HORN*cos(ang)
def pole(ang):
 n=np.array([-.28,1.])/hypot(1,.28);c=cos(ang);s=sin(ang);nx,nr=np.array([[c,-s],[s,c]])@n
 if abs(nx)<1e-8:return inf,0,0,0,0
 cx=HX+(nr*(HR-R)-2.5)/nx;x=cx+2.5*nx;r=R+2.5*nr
 return cx,x,r,nx,HX+c*(x-HX)+s*(r-HR)
# Chordal bounds for fixed/moving faces; curved top spans t and x.
from functools import lru_cache
@lru_cache(None)
def rootcut(t,dy,rho):
 def rr(x):return hypot(x-HX,sqrt((14.5+.28*x)**2-t*t)+dy-HR)
 lo=HX+.65 if rho>1.1 else HX;hi=0.
 if rr(lo)>rho:return lo
 for _ in range(48):
  mid=(lo+hi)*.5
  if rr(mid)>rho:hi=mid
  else:lo=mid
 return hi
def ptile(a,i,j,ang,leaf=True):
 # Conservative chordal tile, including the curved cylindrical heel crop.
 ts=np.linspace(-3.20,3.20,9)[j:j+2];u0=i/4;u1=(i+1)/4
 vv=[]
 for t,dy,z in product(ts,np.linspace(0,.95,5),(u0,u1)):
  cut=rootcut(t,dy,1.16 if leaf else 1.10)
  x=(1-z)*cut if leaf else (1-z)*(HX-.03)+z*cut
  vv.append(hingept(x,sqrt((14.50+.28*x)**2-t*t)+dy,t,ang,a))
 return sol(('cone patch ' if leaf else 'fixed heel roof ')+str((a,i,j)),vv,.055)
def leaves(a,ang,outer=True):
 ls=[ptile(a,i,j,ang) for i in range(4) for j in range(8)]
 # Pivot is virtual at middle of wall. Only side journals/ears at t±4.
 for k in (-1,1):
  ts=np.array([2.85,3.20])*k;vv=[]
  for x,t in product((HX+1.19,HX+1.57),ts):
   for r in (sqrt((14.5+.28*x)**2-t*t),HR+2.75):vv.append(hingept(x,r,t,ang,a))
  ls +=[sol('paired dogleg boss '+str((a,k)),vv,.006)]
  ep=hingept(HX+1.35,HR+2.70,0,ang,a)
  tvec=U(a+90)
  ls +=[sol('crossbar R.22 '+str((a,k)),[ep+k*t*tvec for t in (3.03,4.96)],.22,tvec),
        sol('flat dogleg ear '+str((a,k)),[p+k*t*tvec for p,t in product((pos(a,HX,HR),ep),(4.58,5.08))],.38,tvec),
        tang('short R.37 stub '+str((a,k)),HX,HR,sorted((k*4.86,k*6.18)),a,.37)]
 o=pos(a,HX,HR,4.83);xx,rr=horn(ang);e=pos(a,xx,rr,4.83)
 # Horn is machined as an extension of the +t ear; it terminates at E
 # via the thin crossbar, not through a fictional full-width hinge axle.
 ls += [sol('outboard ear drive horn '+str(a),[p+t*U(a+90) for p,t in product((o,e),(-.25,.25))],.53,U(a+90)),
        tang('leaf horn roller '+str(a),xx,rr,(4.55,5.27),a,.77)]
 return ls
def wall():
 f=[]
 for a in AZ:
  f +=[ptile(a,i,j,0,False) for i in range(4) for j in range(8)]
  for j in range(20):
   u=a-60+6*j;v=u+6
   for x,y,cut in ((HOME-.16,HX-1.16,False),(HX-1.16,HX,False),(HX,0.,True)):
    w=washer('fixed flared wall '+str((a,j,x)),(O+x,O+y),(14.50+.28*x,14.50+.28*y),(15.70,15.70),u,v)
    if x < HX-1.17:f.append(w);continue
    for sg in (-1,1):
     f+=clipone(w,sg*U(a+90),-6.22)
    if not cut:
     for ws in clipone(w,U(a+90),3.26):f+=clipone(ws,-U(a+90),3.26)
  # Fixed liners are .20 in LOCAL radial y, not .20 normal to cone.
  for sg in (-1,1):
   for i in range(4):
    x0=HX-1.16+(0-HX+1.16)*i/4;x1=HX-1.16+(0-HX+1.16)*(i+1)/4
    for m in range(3):
     ts=sg*np.array([3.26+(6.22-3.26)*k/3 for k in (m,m+1)])
     f +=[sol('thin cheek liner '+str((a,sg,i,m)),[pos(a,x,sqrt((14.50+.28*x)**2-t*t)+dd,t) for x,t,dd in product((x0,x1),ts,(0,.20))],.015)]
   f +=[tang('bearing outer reserve '+str((a,sg)),HX,HR,sorted((sg*5.28,sg*6.00)),a,.75),
        sec('outboard cheek support '+str((a,sg)),(HX-.83,HX+.83),(HR-.25,15.62),sorted((sg*6.22,sg*7.05)),a),
        sec('bearing backing bridge '+str((a,sg)),(HX-.52,HX+.52),(HR+.58,HR+.91),sorted((sg*5.47,sg*6.59)),a)]
 return f
def disk():
 d=[frust('solid advancing disk',(O+HOME-1.60,O+HOME),(RD-.55,RD))]
 xt=-4.31-2.5*cos(FACE);t0=2.5*sin(FACE)+(HOME-xt)/tan(FACE)
 for a in BAZ:
  for k in (-1,1):
   v=[]
   for x in (HOME,-5.):
    off=(x-HOME)/tan(FACE)
    v += [pos(a,x,rr,k*t) for rr,t in product((10.3-1.35+off,10.3+1.35-off),(t0+off,3.81-off))]
   d.append(sol('65deg drafted seat '+str((a,k)),v))
  for k in (-1,1):
   d.append(sec('flank gauge bridge allocation '+str((a,k)),(HOME-1.89,HOME-1.59),(9.45,10.95),tuple(sorted((k*1.83,k*2.99))),a))
  d +=[sec('seat backer and strain bridge '+str(a),(HOME-2.56,HOME-1.45),(7.05,11.06),(-2.30,2.30),a),
       sec('axial disk post '+str(a),(-19.72,HOME-1.48),(8.15,9.49),(-1.48,1.48),a),
       rad('disk axle shoulder '+str(a),-19.03,.73,0,a,(8.30,11.68)),
       rad('disk cam roller '+str(a),-19.03,.98,0,a,(9.91,11.45)),
       sec('disk guide rib '+str(a),(-19.71,HOME-1.52),(6.98,8.26),(-1.14,1.14),a)]
 return d
def drum():
 return (ring('inner disk cam sleeve', (O-20.29,O-9.39),(9.78,9.78),(13.19,13.19))
     + ring('outer jaw cam sleeve',(O-17.94,O-12.39),(14.06,14.06),(17.01,17.01))
     + ring('annular connecting web',(O-17.90,O-16.89),(12.82,12.82),(16.91,16.91))
     + ring('120T single-start worm wheel blank',(O-10.41,O-7.81),(16.84,16.84),(18.28,18.28))
     + ring('wheel hub standoff',(O-12.00,O-9.96),(16.86,16.86),(17.33,17.33))
     + ring('front outer bearing rim',(O-12.62,O-11.68),(14.71,14.71),(17.37,17.37)))
def rods(a,ang):
 xx,rr=horn(ang);dx=xx-HX;sh=4.78
 # Moving plunger outer faces enclose *radially extended* horn-roller slot.
 z=[sec('axial leaf rod '+str(a),(HX-12.72,HX-.71),(18.67,19.81),(sh-.80,sh+.79),a),
    sec('leaf link fork root '+str(a),(HX-1.24,HX+1.24),(15.70,19.60),(4.33,5.71),a)]
 for k in (-1,1):z+=[sec('fork positive cheek '+str((a,k)),(HX+k*1.04-.21,HX+k*1.04+.21),(16.28,18.78),(4.34,5.55),a)]
 # Cam groove is on outside surface. Roller extends radially IN from outer
 # journal and has its true azimuth displaced by the circumferential offset.
 z +=[sec('outer follower lug '+str(a),(-17.49,-16.13),(16.01,19.90),(3.86,5.40),a),
       rad('outer groove axle '+str(a),-16.80,.66,0,a+degrees(atan2(4.68,16.42)),(16.11,19.63)),
       rad('outer groove roller '+str(a),-16.80,.80,0,a+degrees(atan2(4.68,16.42)),(16.19,17.16))]
 return shift(z,dx)
def tail():
 t=flange()
 # Balls are captive guided axial plungers in back-inserted boss stock.
 for a in BAZ:
  t+=[xcy('button plunger shank '+str(a),(-3.05,1.32),10.3,0,a,1.10),
      xcy('captive button foot '+str(a),(1.08,1.62),10.3,0,a,2.03),
      xcy('spring OD reserve '+str(a),(1.62,6.37),10.3,0,a,2.14),
      xcy('button inner guide stem '+str(a),(1.45,7.83),10.3,0,a,.80)]
  co=10.3*U(a)
  for name,l,h,ri,ro in [('back cap',6.37,7.10,.87,2.49),('internal travel limiter tube',1.84,6.52,.87,1.18),('front guide bush',-1.53,-.86,1.17,1.62)]:
   t +=[trans(v,co) for v in ring(name+' '+str(a),(O+l,O+h),(ri,ri),(ro,ro),12)]
  # Tube, not closed cylinder; nose retainer has an actual shank bore.
  co=10.3*U(a)
  t += [trans(s,co) for s in ring('button tube '+str(a),(O-.28,O+6.61),(2.20,2.20),(2.57,2.57),16)]
  t += [trans(s,co) for s in ring('front travel shoulder '+str(a),(O-.44,O+.68),(1.20,1.20),(2.54,2.54),16)]
  t +=[sec('button rear displacement reader '+str(a),(7.24,8.73),(9.30,11.32),(1.25,2.61),a),
       xcy('plunger target ring '+str(a),(7.26,7.72),10.30,0,a,1.14),
       sec('reaction gauge lead '+str(a),(6.67,7.31),(9.37,11.23),(-2.53,-1.55),a),
       rod('return flex harness allocation '+str(a),pos(a,7.43,9.40,1.82),pos(a,9.09,5.25,.84),.54),
       sec('cartridge root web '+str(a),(.13,6.69),(6.89,8.49),(-1.32,1.32),a)]
 return t
