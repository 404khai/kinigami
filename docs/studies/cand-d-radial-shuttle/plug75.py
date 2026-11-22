"""Exploratory / Take 75. World mm, X=17.04 at lip, straight stow P=38.
All actuation is new. The registered tail chart and external support reserves
use the frozen earlier dimensions; seal/strain mechanics do not transfer."""
from space75 import *
from pathlib import Path
from scipy.optimize import brentq
import json
D=Path(__file__).resolve().parent
O=17.04;P=38.;H=np.array([-11.7,0,0]);X=np.eye(3)[0];Z=np.eye(3)[2]
AZ=(-90,30,150);BAZ=(-30,90,210);ST=1.8391;RD=12.42;HOME=-6.95;TR=8.53
U=lambda a:np.array([0.,cos(radians(a)),sin(radians(a))])
def pos(a,x,r,t=0):return (O+x)*X+r*U(a)+t*U(a+90)
def box(n,a,x,r,t):return sol(n,[pos(a,p,q,z) for p,q,z in product(x,r,t)])
def cyl(n,p,q,r):
 p=np.array(p);q=np.array(q);return sol(n,[p,q],r,(q-p)/np.linalg.norm(q-p))
def ax(n,xs,rr,off=(0.,0.)):return cy(n,0,(xs[0]+O,xs[1]+O),off,rr)
def rg(n,l,h,i,o,N=48,start=0,end=360):
 s=[]
 for j in range(N):
  a=start+(end-start)*j/N;b=start+(end-start)*(j+1)/N
  s.append(sol(n+' '+str(j),[pos(z,x,r) for z,x,r in product((a,b),(l,h),(i,o/cos(radians((b-a)/2))))]))
 return s
def tube(n,p,q,ri,ro,N=16):
 p=np.array(p);q=np.array(q);d=q-p;d=d/np.linalg.norm(d);u=np.cross(d,np.eye(3)[np.argmin(abs(d))]);u/=np.linalg.norm(u);v=np.cross(d,u)
 return [sol(n+' '+str(j),[z+r*(u*cos(t)+v*sin(t)) for z,r,t in product((p,q),(ri,ro/cos(pi/N)),(j*2*pi/N,(j+1)*2*pi/N))]) for j in range(N)]
def move(S,v):return [trans(q,v) for q in S]
def sweep(S,v):return [sol(n,p+trans((n,p,r,d),v)[1],r,d) for n,p,r,d in S]
def yaw(S,y):return [rot(q,radians(y),H) for q in S]
def bore(x):return max(14.56+.52*x,14.56-(.52-.25)*1.095+.25*x)
def skin(x,t):return sqrt(bore(x)**2-t*t)
def bottom(x,t):
 # Take73 installed surface at LOCK; PARK is its rigid translation.
 return max(skin(x,t)-ST,12.75-.75*(x+.75))
def plug(a):
 p=[sol('plug toe '+str(a),[pos(a,x,y,t) for x,t in product((-1.04,-.93,-.75,-.40,-.125),np.linspace(-2.25,2.25,13)) for y in (bottom(x,t)-.025,17.90)])]
 p+=[box('plug bridge '+str(a),a,(-4.50,-.70),(15.72,16.55),(-.89,.89)),box('plug stiff spine '+str(a),a,(-4.50,-2.04),(15.72,20.72),(-.89,.89))]
 for j,(l,h) in enumerate(((16.05,16.70),(20.0,20.70))):
  for k in (-1,1):
   p +=[box('X pad '+str((a,j,k)),a,(-4.50,-2.04),(l,h),tuple(sorted((k*.75,k*2.20))))]
 p+=[cyl('plug follow pin '+str(a),pos(a,-6.95,18.35),pos(a,-3.8,18.35),.60),
     cyl('plug roller '+str(a),pos(a,-6.89,18.35),pos(a,-5.19,18.35),.90)]
 return p
def ways(a):
 f=[]
 for sg in (-1,1):
  def ts(l,h):return tuple(sorted((sg*l,sg*h)))
  for j,(xl,xh) in enumerate(((-4.86,-4.503),(-2.037,-1.69))):
   f.append(box('fixed X way '+str((a,sg,j)),a,(xl,xh),(15.76,22.64),ts(1.03,2.61)))
  f+=[box('guide side '+str((a,sg)),a,(-4.86,-1.69),(15.68,22.64),ts(2.203,2.67)),box('guide roof root '+str((a,sg)),a,(-4.84,-1.69),(15.18,15.78),ts(2.24,2.64))]
 return f
def jawstroke(deg):
 # Cylindrical lands on both sides of a finite sinusoidal-lead section.
 t=np.clip((deg-4.)/64.,0.,1.)
 return ST*(1-cos(pi*t))*.5
def tracks():
 a=np.linspace(-4,76,641)
 return [[float(v),18.35+jawstroke(v)] for v in a]
def changed(s,n):return sol(n,s[1],s[2],s[3])
def convex_union(name,objs):
 p=np.concatenate([s[1] for s in objs]);p=np.unique(p,axis=0);return sol(name,p[ConvexHull(p).vertices] if len(p)>4 and np.linalg.matrix_rank(p-p[0])==3 else p,max(s[2] for s in objs))
NA=30.64; NR=7.80; ND=NR*U(NA)
def plate():
 # R12.42 rigid ejection rim; six 56deg flats held fixed as a
 # conservative stock reservation. No assertion of final seal identity.
 v=[];g=[]
 for x,r in ((HOME-1.60,RD-.53),(HOME,RD)):v.extend([pos(t,x,r/cos(pi/64)) for t in np.arange(64)*360/64])
 g.append(sol('disk shell metal blank',v))
 N=2.50;angle=radians(56);t0=N*sin(angle)+(HOME-(-4.31-N*cos(angle)))/tan(angle)
 for a in BAZ:
  for k in (-1,1):
   v=[]
   for x in (HOME,-5.30):
    w=(x-HOME)/tan(angle);v +=[pos(a,x,r,k*t) for r,t in product((10.3-1.35+w,10.3+1.35-w),(t0+w,3.81-w))]
   g+=[sol('six-seat reservation '+str((a,k)),v)]
  # Ground guide rods fixed to dished disk; butt length .50 available
  # for a shoulder and independent cross fastener (not weld inference).
  g +=[cyl('disk post '+str(a),pos(a,-22.16,8.58),pos(a,-8.20,8.58),1.10)]
 # Long hollow moving cup lets fixed screw enter plate rear, never
 # project from front lip at HOME. Integral nut toward far aft end.
 g +=[trans(ax('moving lead stud',(-23.46,-8.21),1.75),ND)]
 return g
def roof(a):
 f=[]
 # On each side of 4.50-wide plug leave .05 per tangential side.
 # Actual fixed front cheek across whole aperture at x=-.075..0;
 # aft (.05 clearance) roof rises from the bore to y=15.46; neither
 # is an imaginary plane. Chordal envelope split across t & X.
 def face(n,xs,ts,top):
  for j in range(len(ts)-1):
   for i in range(len(xs)-1):
    v=[pos(a,x,y,t) for x,t in product(xs[i:i+2],ts[j:j+2]) for y in (skin(x,t),top)]
    f.append(sol(n+' '+str((a,i,j)),v,.004))
 face('front wall',[-.075,0.],np.linspace(-3.15,3.15,13),17.9)
 face('aft roof',[-7.0,-4.85,-1.095,-1.09],np.linspace(-3.15,3.15,13),15.46)
 for k in (-1,1):face('tangent cheek '+str(k),[-1.09,-.075],np.linspace(k*2.30,k*3.15,3),17.90)
 # Axial side cheeks of guard lie out of swept t; close the exposed
 # side outside the aperture with solid skirt and top, never a moving cap.
 for k in (-1,1):
  f.append(sol('fixed guard side '+str((a,k)),[pos(a,x,y,t*k) for x,h in ((-4.88,22.90),(-1.61,22.90),(0.,20.05)) for y,t in product((15.30,h),(2.84,3.19))]))
 for l,h,yl,yh in ((-5.08,-1.61,22.95,22.95),(-1.61,0.,22.95,20.09)):
  f.append(sol('outer guard top '+str((a,l)),[pos(a,x,y+t,b) for (x,y),t,b in product(((l,yl),(h,yh)),(-.24,0),(-3.18,3.18))]))
 f.append(box('front cover high '+str(a),a,(-.075,0.),(17.89,20.02),(-3.15,3.15)))
 return f
def drive():
 return rg('steel face cam',-7.03,-5.03,16.75,21.61)+rg('drive flange',-8.28,-7.02,18.68,20.99)+rg('connecting annular web',-8.62,-8.26,16.4,19.63)+rg('122T metal blank',-9.99,-8.23,15.91,18.61)
def diskfixed():
 f=[]
 for a in BAZ:
  for l,h in ((-12.82,-10.98),(-9.58,-8.84)):
   f+=tube('disk slide bush',pos(a,l,8.58),pos(a,h,8.58),1.118,1.73)
 return f
def facecheck():
 print('world lip, stroke, y pads, crosshead X, rear roof Y, front wall X',O,ST,(16.05,16.70,20,20.70),(-4.50,-2.04),15.46,(-.075,0))
 for sg in AZ:
  p=sweep(plug(sg),ST*U(sg));f=ways(sg)+roof(sg)
  xx=np.vstack((ds,X,U(sg),U(sg+90)));b=np.array([ext(s,xx) for s in f]);v=min(np.maximum(ext(s,xx)[0]-b[:,1],b[:,0]-ext(s,xx)[1]).max(1).min() for s in p[1:]);print('swept bridge/spine/pads/roller vs fixed local stock; station and world axes',sg,v)
 print('conservative fixed row coverage at both ends',16.05-15.76,22.64-20.70-ST,'X gap and min intrinsic pitch',.003,20-16.7)
 print('uninterrupted front wall, toe-to-guide bridge roof clearance full stroke',-.075-(-.125),15.72-15.46)
if __name__=='__main__':facecheck()
