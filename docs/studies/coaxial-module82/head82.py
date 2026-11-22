"""Take 82 local solids. Millimetres. X toward registered neighbor, clocks from +Y."""
from math import *
from itertools import product
from functools import lru_cache
import json
import numpy as np
from manifold3d import Manifold as M, OpType
N=96
PH=(0,120,240); EP=(60,180,300); VP=(-90,30,150)
RK=3.85+1.5*cos(pi/4); RL=RK+1.52; RU=7.95
def union(xs):return M.batch_boolean(list(xs),OpType.Add)
def box(x,y,z):
 return M.cube([b-a for a,b in (x,y,z)]).translate([x[0],y[0],z[0]])
def cyl(x,r,y=0,z=0,R=None):
 return M.cylinder(x[1]-x[0],r,r if R is None else R,N).rotate([0,90,0]).translate([x[0],y,z])
def ring(x,ri,ro,y=0,z=0):return cyl(x,ro,y,z)-cyl((x[0]-.1,x[1]+.1),ri,y,z)
def loc(ob,a):return ob.rotate([a,0,0])
def at(r,a):return (r*cos(radians(a)),r*sin(radians(a)))
def xyz(x,r,a):return [x,*at(r,a)]
def hull(ps):return M.hull_points(np.array(ps,dtype=float))
def mesh(ob):return np.asarray(ob.to_mesh64().vert_properties)[:,:3]
def strut(p,q,r):return union([M.sphere(r,24).translate(v) for v in (p,q)]).hull()
def dump(n,d):
 with open(n,'w') as f:json.dump(d,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
def profile(x):
 a=radians(45); rb=.25; K=RU-RL
 if x<=-3.80:return RL
 u=x+3.80; A=rb*sin(a); B=rb*(1-cos(a)); L=(K-2*B)/tan(a)
 if u<=A:return RL+rb-sqrt(max(0,rb**2-u**2))
 if u<=A+L:return RL+B+(u-A)*tan(a)
 if u<2*A+L:return RU-rb+sqrt(max(0,rb**2-(u-2*A-L)**2))
 return RU
class Book(dict):
 def put(self,name,m,group='fixed',mat='steel',kind='solid'):
  assert name not in self and not m.is_empty(),name
  self[name]=(m,group,mat,kind)
def tail(b,prefix,group,dx=0):
 def put(n,m):b.put(prefix+n,m.translate([dx,0,0]),group)
 # Strict circular R4.60 outer cap. Shoulder y = 3.85-(x+5.26066).
 xc=-4.20-1.5/sqrt(2); lo=xc-(4.60-3.85); hi=xc+(3.85-3.20)
 pin=cyl((-6.76,.73),4.60)
 for a in PH:
  # Cut constant head/neck and transition independently (slope must not be convexified).
  for u,v,h,k in [(-7,lo,4.60,4.60),(lo,hi,4.60,3.20),(hi,.9,3.20,3.20)]:
   pin-=loc(hull([(x,y,z) for x,r in [(u,h),(v,k)] for y in (r,8) for z in (-8,8)]),a)
 put(' tri-flat pin',pin)
 put(' eject boss',cyl((.70,1.70),6.65));fl=cyl((1.7,2.95),10.35)
 for a in VP:
  ball=M.sphere(1.5,N).translate(xyz(0,8.2,a));post=cyl((1.14,1.73),.87,*at(8.2,a))
  put(' ball and stem '+str(a),union([ball,post]))
 put(' flange',fl)
def front(b):
 put=b.put;bar=ring((-16.1,-.02),9.70,10.90)
 put('barrel',bar,'fixed','7075')
 for i,x in enumerate([(-14.9,-13.70),(-7.45,-6.25)]):put('sleeve guide '+str(i),ring(x,9.65,9.70),'fixed','bronze')
 # Stationary front with three slots for moving sleeve tongues; cut real V valleys
 # removing face material forward of EITHER tangent plane (remaining flanks contact ball).
 face=ring((-2.21,0),6.37,9.74)
 for a in PH:face-=loc(box((-2.4,.2),(5.90,10),(-2.29,2.29)),a)
 for a in VP:
  # The void is intersection of the halfspaces n·(P-C)>-R, clipped to radial band.
  v=box((-4,.2),(6.38,10.06),(-2.70,2.70))
  for s in [-1,1]:
   v=v.trim_by_plane((cos(radians(65)),0,s*sin(radians(65))),-1.5)
  face-=loc(v,a)
 put('V seat annulus',face)
 put('pilot',ring((-2,0),5.10,5.34))
 body=cyl((-15.15,-.03),9.60)-cyl((-16,.2),6.33)
 for a in PH:
  xs=sorted(set([-15.16,-3.8,-.02]+list(np.linspace(-3.8,-2.065,72))))
  # Constant-width locker pockets with circular arc/ramp/plain top.
  # Single planar extrusion avoids union of >70 overlapping slabs.
  from manifold3d import CrossSection
  poly=[(x,profile(x)) for x in xs]+[(xs[-1],0),(xs[0],0)]
  pocket=CrossSection([np.array(poly[::-1])]).extrude(3.38).translate([0,0,-1.69])
  body-=loc(pocket,a)
 tongue=union(loc(box((-2.31,.1),(6.0,10),(-2.20,2.20)),a) for a in PH)
 body=(body^box((-15.2,-2.30),(-11,11),(-11,11)))+(body^tongue)
 put('sleeve',body,'sleeve')
 cage=ring((-5.99,-2.41),4.65,6.23)
 # remove off-station cage stock so r5.82 pushrods and fixed guides can pass
 cage=cage^union(loc(box((-6,-2.40),(2,7),(-2.05,2.05)),a) for a in PH)
 for a in PH:
  cage-=loc(box((-5.725,-2.675),(2,7),(-1.53,1.53)),a)
  for x in [(-5.71,-5.53),(-2.87,-2.69)]:
   cage+=loc(box(x,(4.03,4.71),(-1.50,1.50)),a)
  cage+=loc(box((-18.5,-5.83),(4.69,5.52),(-.62,.62)),a)
  # Cage rear shoes and posts pull toward -X.
  put('cage return stud '+str(a),cyl((-22.60,-18.25),.54,*at(5.10,a)),'cage')
  put('roller '+str(a),loc(M.cylinder(3,1.5,1.5,N,True).translate([-4.2,RK,0]),a),'r'+str(a))
 for a in EP:
  for i,x in enumerate([(-3.,-1.50),(-10.9,-9.4)]):
   put('rod bush '+str((a,i)),ring(x,.471,.68,*at(5.82,a)),'fixed','bronze')
  put('rod bush support tube '+str(a),ring((-9.4,-2.87),.475,.605,*at(5.82,a)),'fixed','steel')
  put('bush anchor '+str(a),loc(box((-1.50,-1.16),(5.89,6.85),(-.35,.35)),a)-cyl((-1.55,-1.12),.471,*at(5.82,a)),'fixed','steel')
  put('pilot web '+str(a),loc(box((-1.47,-1.17),(5.26,6.87),(-.29,.29)),a+18),'fixed','steel')
  put('ejector rod '+str(a),cyl((-31.72,-.73),.45,*at(5.82,a)),'eject')
 put('roller cage',cage,'cage')
 put('ejector lip',ring((-.85,.10),5.40,6.32),'eject')
 put('ejector spider',ring((-32.26,-31.67),2.74,6.37),'eject')
 put('cage spring seat',cyl((-20.14,-19.43),5.85),'cage')
 for a in PH:
  # Front face of cage at hard reset = −19.23. Stop over the tab's outer rim.
  q=box((-19.23,-18.96),(5.44,7.34),(-.66,.66))-cyl((-19.3,-18.9),.58,5.10,0)
  put('cage reset stop '+str(a),loc(q,a))
  put('cage stop post '+str(a),loc(box((-26.77,-19.10),(6.72,7.34),(-.67,.67)),a))
  put('cage stop ground '+str(a),loc(box((-27.10,-26.72),(6.72,11.20),(-.72,.72)),a),'fixed','7075')
 # Driver ahead of cage pushes aft through three finite compression springs;
 # two flanges/stud shoulders provide a separate, positive retraction path.
 driver=cyl((-14.80,-14.10),5.87)
 for a in PH:driver-=loc(box((-15,-14),(4.60,5.62),(-.73,.73)),a)
 put('draw spring driver',driver,'draw')
 for a in EP:
  put('draw input rod '+str(a),cyl((-22.45,-14.5),.50,*at(4.50,a)),'draw')
 spider=ring((-22.61,-21.98),2.62,5.72)
 for a in PH:spider-=cyl((-22.7,-21.9),.57,*at(5.10,a))
 put('draw input spider',spider,'draw')
 for a in PH:
  put('draw return head '+str(a),cyl((-20.92,-20.50),.83,*at(5.10,a)),'cage')
  put('spring outside '+str(a),ring((-19.43,-14.80),1.075,1.575,*at(2.85,a)),'coil','spring','reserve')
 tail(b,'own','yaw',-40.3);tail(b,'guest','guest')
def phase(phase,t):
 # Cage +.20 at LOCK, zero at DRAW; positive-release reset before sleeve translation.
 c=.2;d=1.26
 if phase=='DRAW':c=.2*(1-t);d=1.26*(1-t)
 if phase=='UNLOCK':c=.2*min(1,2*t);d=1.26*min(1,2*t)
 u=max(0,2*t-1) if phase=='UNLOCK' else float(phase=='EJECT')
 e=8.1*t if phase=='EJECT' else 0.
 s=-3.65*u
 v={'fixed':[0,0,0],'yaw':[0,0,0],'draw':[d,0,0],'cage':[c,0,0],'sleeve':[s,0,0],'eject':[e,0,0],'guest':[max(0,e-.60),0,0]}
 for a in PH:v['r'+str(a)]=[c,*at((6.40-RK)*u,a)]
 v['coil']=[c,0,0]
 return v
