from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('sleeve-stock62.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
O=17.04;P=38.;HOME=-6.95;RD=12.42;TR=8.35;C=O-2.25;R=10.75;RE=2.50
X=np.eye(3)[0];U=lambda a:np.array([0.,cos(radians(a)),sin(radians(a))])
J=json.loads((D/'flange-jaw-take59.json').read_text());ST=J['stroke'];STATION=-90
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
  t.append(sol('revised tail button '+str(j),[(O-4.31)*X+10.3*U(a)],2.50))
 # Starts at full broad footprint; no thin neck in the head. Continues
 # directly into two rear gusset forks and the articulated joint's lugs.
 t += [frust('broad tail socket',(C+1.95,C+4.50,C+8.05),(10.08,9.,5.66))]
 for k in (-1,1):
  t += [sol('web fork '+str(k),[[x,y,k*z] for x,hy,ranges in [(C+6.25,3.3,(1.7,5.08)),(C+9.0,2.15,(3.,6.45)),(P-9.5,1.45,(4.31,6.66))] for y in (-hy,hy) for z in ranges])]
 t+=shift([s for s in V['own_tail_straight'] if s[0].startswith(('tail pivot lug','sector web','tail sector hub','fork tip'))],P)
 return t
def clipone(s,n,b):
 from itertools import combinations
 from scipy.spatial import ConvexHull
 v=np.array(s[1]);h=v@n-b
 if min(h)>-1e-9:return []
 if max(h)<1e-9:return [s]
 hull=ConvexHull(v);edges=set(tuple(sorted(e)) for tri in hull.simplices for e in combinations(tri,2))
 z=[p for p,d in zip(v,h) if d<=0]
 for i,j in edges:
  if h[i]*h[j]<0:z.append(v[i]+h[i]/(h[i]-h[j])*(v[j]-v[i]))
 return [sol(s[0],z)]
