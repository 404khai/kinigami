"""Exploratory independent single-key package, not the old disk or ring."""
from stocklib79 import *
from pathlib import Path
from scipy.spatial import HalfspaceIntersection
from scipy.optimize import brentq
import json
D=Path(__file__).resolve().parent
datum=json.loads((D/'reference74.json').read_text())['interface']
O=np.array(datum['reference']);U=np.array(datum['draw']);T=np.array(datum['transverse_ridge_axis']);Z=np.eye(3)[2];X=np.eye(3)[0];Y=np.eye(3)[1];Q=np.array(datum['lug']);P=np.array(datum['key_contact']);XB,XF=datum['shank_x'];XC=(XB+XF)/2
S=4.85;R=.35;Y0=datum['key_tip'];END=13.35;H=np.array([-27.0,0,0]);PITCH=37.0;# lip x=0, COM and supports expressed in head chart
def cyl(n,p,q,r):
 p=np.array(p);q=np.array(q);return sol(n,[p,q],r,(q-p)/np.linalg.norm(q-p))
def ann(n,p,q,ri,ro,N=24):
 p=np.array(p);q=np.array(q);d=q-p;d/=np.linalg.norm(d);u=np.cross(d,np.eye(3)[np.argmin(abs(d))]);u/=np.linalg.norm(u);v=np.cross(d,u)
 return [sol(n+' '+str(j),[z+r*(cos(t)*u+sin(t)*v) for z,r,t in product((p,q),(ri,ro/cos(pi/N)),(j*2*pi/N,(j+1)*2*pi/N))]) for j in range(N)]
def ax(n,ax,lo,hi,c,r):return cy(n,ax,(lo,hi),c,r)
def drivebox(n,x0,x1,y0,y1,z0,z1):return bx(n,(x0,x1),(y0,y1),(z0,z1))
def move(A,v):return [trans(q,v) for q in A]
def sweep(A,v):return [sol(n,p+trans((n,p,r,d),v)[1],r,d) for n,p,r,d in A]
def yaw(A,t):return [rot(q,radians(t),H) for q in A]
def poly(n,eq,c,rf=0):
 v=HalfspaceIntersection(np.asarray(eq,dtype=float),np.asarray(c,dtype=float)).intersections
 return sol(n,v[ConvexHull(v).vertices],rf)
def key():
 # Round all edges by erosion of ALL halfspaces followed by Minkowski +R.
 eq=[[1,0,0,-XF],[-1,0,0,XB],[0,1,0,-END],[0,-1,0,Y0],[0,0,1,-1.65],[0,0,-1,-1.65],[*tuple(-U),2.5+U@Q]]
 e=np.array(eq);e[:,3]+=R
 return poly('inclined key 74',e,[XC,8,0],R)
def sides(n,xc,zc,xw,zw,ys,g=.020,outer=(.52,.70)):
 x=xc;t=zc;y0,y1=ys;hx=xw/2;hz=zw/2;xo,zo=outer
 return [drivebox(n+' aft',x-hx-xo,x-hx-g,y0,y1,t-hz-zo,t+hz+zo),drivebox(n+' fore',x+hx+g,x+hx+xo,y0,y1,t-hz-zo,t+hz+zo)]+[bx(n+' side '+str(k),(x-hx-g,x+hx+g),ys,sorted((t+k*(hz+g),t+k*(hz+zo)))) for k in (-1,1)]
ROWS=[(4.50,5.35),(11.85,12.70),(15.16,16.60)]
def frontguides():return [q for j,yr in enumerate(ROWS) for q in sides('nose guide '+str(j),XC,0,2.68,3.3,yr)]
def keyplus():
 return [key(),drivebox('key upper separate shoe',XB,XF,13.35,18.93,-1.65,1.65),
  cyl('shoe internal spigot', [XC,11.84,0],[XC,13.75,0],.86),
  ax('shoe flush cross pin',2,-1.62,1.62,(XC,12.22),.46),
  ax('key pickup axle',2,-3.72,3.72,(XC,17.70),.70)]
def keyseam(st):
 # Old rounded top ends in a narrower face beneath shoe. Count no
 # finished flat over .70 at joint even if parts have sharp mating edges.
 rear=P[1]+(P[0]-XB)/tan(radians(18))+.35*tan(radians(9))
 # exact flat starts on +X & Z have their own limits, not rear's.
 fr=Y0+.35
 def overlap(row,intervals):
  return sum(max(0,min(row[1],b+st)-max(row[0],a+st)) for a,b in intervals)
 def reg(q,lo):return overlap(q,[(lo,13.),(13.70,18.92)])
 return [[reg(q,rear),reg(q,fr)] for q in ROWS],rear
def keycheck():
 print('key lock/park extents',ext(key(),np.eye(3)),ext(trans(key(),S*Y),np.eye(3)))
 p=key();vs=np.array(p[1]);print('fillet core rear flat start',keyseam(0)[1])
 for s in (0,.893475,2.266,3.116,3.743475,4.85):
  print('stroke, usable (-X,+X) flat lengths by fixed row (mm)',s,np.round(keyseam(s)[0],6).tolist())
 # all changes in usable side area lie at interval endpoints crossing a
 # guide boundary; min max is piecewise-linear (include row crossings).
 knots=sorted(set([0,S]+[max(0,min(S,j-i)) for q in ROWS for j in q for i in (keyseam(0)[1],Y0+.35,13.,13.70,18.92)]))
 print('independent mid-row and extra row rear length minima over FULL stroke',*[min(keyseam(x)[0][j][0] for x in knots) for j in (1,2)])
 print('extra-to-middle adverse separation',ROWS[2][0]-ROWS[1][1],'max lost angular motion, whole-lock span, .020 each side',degrees(atan(.040/(12.70-4.50))))
 print('original roof at y18.60 obstructs extended shoe at park by',18.93+S-18.6,'must revise enclosed pocket not datum of key toe')
if __name__=='__main__':keycheck()
