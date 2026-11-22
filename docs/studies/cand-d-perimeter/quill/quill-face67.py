from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('quill-basics67.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
import json
from functools import lru_cache
from scipy.optimize import brentq
D=Path(__file__).parent;H=np.array([-11.70,0.,0.]);AZ=(-90.,30.,150.);BAZ=(-30.,90.,210.)
HX=-1.99732305;HR=13.94851293;B=14.54;FR=.41;BK=.26;A0=-radians(59.1635268);FACE=radians(56);STOP=105.;D0=10.68
def bore(x):return B+FR*max(x,-1.55)+BK*min(x+1.55,0)
def pos(a,x,r,t=0):return (O+x)*X+r*U(a)+t*U(a+90)
def sec(n,x,r,t,a):return sbox(n,tuple(O+np.array(x)),r,t,a)
def xy(n,x,r,t,a,rr):return cy(n,0,tuple(O+np.array(x)),pos(a,0,r,t)[1:],rr)
def cyl(n,p,q,r):
 d=q-p;return sol(n,[p,q],r,d/np.linalg.norm(d))
def tube(n,p,q,ri,ro,m=16,inner=False):
 d=q-p;d/=np.linalg.norm(d);e=np.eye(3)[np.argmin(abs(d))];u=np.cross(d,e);u/=np.linalg.norm(u);v=np.cross(d,u)
 return [sol(n+' '+str(j),[c+r*(u*cos(t)+v*sin(t)) for c,r,t in product((p,q),(ri/cos(pi/m) if inner else ri,ro if inner else ro/cos(pi/m)),(j*2*pi/m,(j+1)*2*pi/m))]) for j in range(m)]
def tg(n,x,r,t,a,rr):return cyl(n,pos(a,x,r,t[0]),pos(a,x,r,t[1]),rr)
def offset(S,v):return [trans(s,v) for s in S]
def move(S,dx):return offset(S,dx*X)
def yaw(S,deg):return [rot(s,radians(deg),H) for s in S]
def sweep(S,v):return [sol(s[0],s[1]+trans(s,v)[1],s[2],s[3]) for s in S]
def phase(th):
 al=degrees(A0)
 if th<=10:ang=al+.32*th
 elif th<42:
  z=(th-10)/32;ang=(2*z**3-3*z*z+1)*(al+3.2)+(z**3-2*z*z+z)*(.32*32)
 else:ang=0
 return radians(ang),TR*(1-cos(pi*np.clip((th-45)/55,0,1)))/2
def point(a,u,v,t,an):return pos(a,HX+u*cos(an)-v*sin(an),HR+u*sin(an)+v*cos(an),t)
def localp(u,v,an):return HX+u*cos(an)-v*sin(an),HR+u*sin(an)+v*cos(an)
SLX=-.54;LINK=4.66
def link(an):
 xp,rp=localp(1.03,2.7,an);return xp,rp,rp+sqrt(LINK**2-(xp-SLX)**2)
def heel(x,t,up):return hypot(x-HX,sqrt(bore(x)**2-t*t)+up-HR)
@lru_cache(None)
def cut(t,up,rr):
 lo=HX+.61 if rr>1.11 else HX
 return lo if heel(lo,t,up)>=rr else brentq(lambda x:heel(x,t,up)-rr,lo,0)
def tile(a,an,j,i,leaf):
 ts=np.linspace(-3.20,3.20,9)[j:j+2];v=[]
 for t,w,k in product(ts,np.linspace(0,.95,5),(i/4,(i+1)/4)):
  c=cut(t,w,1.16 if leaf else 1.10);x=(1-k)*c if leaf else (1-k)*HX+k*c
  v.append(point(a,x-HX,sqrt(bore(x)**2-t*t)+w-HR,t,an))
 return sol(('cone leaf ' if leaf else 'heel land ')+str((a,i,j)),v,.070)
def leaf(a,an):
 l=[tile(a,an,j,i,True) for j in range(8) for i in range(4)]
 def plates(n,ts,uv,rr):
  return sol(n+' '+str((a,ts[0])),[point(a,u,v,t,an) for (u,v),t in product(uv,ts)],rr,U(a+90))
 for k in (-1,1):
  for part,ts,hi in [('drive boss pillar',(1.70,2.65),2.85),('rear rib pillar',(2.78,3.20),2.00)]:
   l.append(sol(part+' '+str((a,k)),[point(a,u,v,t*k,an) for u,t in product((1.22,1.74),ts) for v in (sqrt(bore(HX+u)**2-t*t)-HR,hi)],.004))
  for n,ts,uv,rr in [('drive pin boss',(1.70,2.65),[(1.03,2.70)],.88),('rib capsule',(2.78,3.20),[(.10,2.70),(1.44,1.85)],.45),('outboard crossbar',(3.03,4.90),[(.10,2.70)],.45),('rear dogleg',(4.58,5.35),[(0,0),(.10,2.70)],.55),('bearing pin',(4.9,7.55),[(0,0)],.52),('external park lever',(6.68,7.28),[(0,0),(0,3.8)],.46)]:
   l.append(plates(n,tuple(k*t for t in ts),uv,rr))
 l.append(plates('central through clevis PIN',(-2.65,2.65),[(1.03,2.70)],.60))
 return l
def wall():
 s=[]
 for a in AZ:
  s +=[tile(a,0,j,i,False) for j in range(8) for i in range(4)]
  for i in range(16):
   u=a-60+7.5*i;v=u+7.5
   for x,z in ((HOME-.12,HX-1.18),(HX-1.18,HX),(HX,-1.55),(-1.55,0.)):
    w=washer('stationary case '+str((a,i,x)),(O+x,O+z),(bore(x),bore(z)),(15.7,15.7),u,v)
    if x<HX-1.19:s+=[w];continue
    for sg in (-1,1):s+=clipone(w,sg*U(a+90),-6.60)
    if z<=HX:
     for q in clipone(w,U(a+90),3.26):s+=clipone(q,-U(a+90),3.26)
  for sg in (-1,1):
   for x,z in ((HX-1.18,HX),(HX,-1.55),(-1.55,0)):
    for j in range(4):
     ts=[sg*(3.26+(6.60-3.26)*k/4) for k in (j,j+1)]
     s.append(sol('thin liner '+str((a,sg,x,j)),[pos(a,p,sqrt(bore(p)**2-t*t)+w,t) for p,t,w in product((x,z),ts,(0,.20))],.018))
   s+=tube('leaf bearing '+str((a,sg)),pos(a,HX,HR,sg*5.55),pos(a,HX,HR,sg*6.15),.54,.90)
   s+=[sec('park stop block '+str((a,sg)),(HX-1.46,HX-.46),(HR+3,HR+4.25),sorted((sg*6.60,sg*7.40)),a),sec('park stop outer support '+str((a,sg)),(HX-1.50,HX-.68),(HR+.70,HR+4.10),sorted((sg*7.30,sg*7.92)),a),sec('leaf bearing cap '+str((a,sg)),(HX-1.43,HX-.69),(HR-.26,HR+.26),sorted((sg*5.65,sg*6.06)),a),sec('bearing aft tie '+str((a,sg)),(HX-1.43,HX-1.12),(HR-.22,HR+.22),sorted((sg*5.65,sg*7.93)),a),
       sec('leaf mount '+str((a,sg)),(HX-1.43,HX-.98),(HR-.22,HR+4.10),sorted((sg*7.59,sg*7.93)),a)]
 return s
def disk():
 d=[frust('broad ejector',(O+HOME-1.60,O+HOME),(RD-.53,RD))]
 xc=-4.31-2.5*cos(FACE);t0=2.5*sin(FACE)+(HOME-xc)/tan(FACE)
 for a in BAZ:
  for k in (-1,1):
   v=[]
   for x in (HOME,-5.30):
    w=(x-HOME)/tan(FACE);v +=[pos(a,x,r,k*t) for r,t in product((10.3-1.35+w,10.3+1.35-w),(t0+w,3.81-w))]
   d+=[sol('56deg seat '+str((a,k)),v),sec('pole strain allocation '+str((a,k)),(HOME-1.88,HOME-1.59),(9.8,11.30),sorted((k*1.41,k*2.86)),a)]
  d +=[sec('seat backer '+str(a),(HOME-2.33,HOME-1.56),(7.8,11.50),(-2.35,2.35),a),
       sec('disk post '+str(a),(-19.74,HOME-1.48),(8.18,9.56),(-1.39,1.39),a),
       sec('disk key '+str(a),(-20.31,HOME-1.49),(6.99,8.29),(-1.05,1.05),a),
       cyl('disk axle '+str(a),pos(a,-19.03,8.38),pos(a,-19.03,11.68),.75),
       cyl('disk roller '+str(a),pos(a,-19.03,9.95),pos(a,-19.03,11.49),.98)]
 return d
def tail():
 # Construct rolled 3D core hull using outer polygon approximations for
 # all circular centres. Port corrections: stationary outer sleeve instead
 # of fusing the leading moving R2.50 ball to the flange.
 v=[]
 for a in AZ:v.extend([pos(a,-2.25,6.75)+4/cos(pi/48)*U(j*7.5) for j in range(48)])
 for x,r in ((-2.25,7.60),(.20,7.10),(2.50,6.00),(4.40,3.50),(-.30,7.58),(2.25,6.50),(5.80,3.16)):v.extend([pos(0,x,0)+r/cos(pi/48)*U(j*7.5) for j in range(48)])
 vv=np.array(v);t=[sol('rolled three-lobe hull',vv[ConvexHull(vv).vertices],2.50)]
 for a in BAZ:
  t +=[sol('button near-mid sphere '+str(a),[pos(a,-4.31,10.3)],2.50),
       xy('plunger shank '+str(a),(-3.10,1.18),10.3,0,a,1.10),
       xy('captive foot '+str(a),(.91,1.41),10.3,0,a,2.04),
       xy('spring package '+str(a),(1.41,6.26),10.3,0,a,2.16),xy('inner stem '+str(a),(1.16,7.76),10.3,0,a,.78)]
  for n,x,y,ri,ro in [('cartridge body',-2.25,6.62,2.21,2.61),('front stop',-.63,.53,1.22,2.55),('front bush',-1.95,-1.06,1.17,2.27),('rear cap',6.26,7.16,.83,2.55),('limiter',1.65,6.30,.83,1.13)]:
   t+=tube(n+' '+str(a),pos(a,x,10.30),pos(a,y,10.30),ri,ro)
  t += [sec('cartridge outer bridge '+str(a),(.20,6.61),(6.28,8.62),(-1.49,1.49),a),sec('plunger readout '+str(a),(7.17,8.32),(9.12,11.35),(1.14,2.45),a)]
 return t
