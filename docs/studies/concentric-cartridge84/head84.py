"""Take 83 interface in local x/radial/tangential coordinates; all dimensions mm."""
from head82 import *
from manifold3d import CrossSection
import head82
from scipy.optimize import brentq
PITCH=42.72; VP84=EP; U0=-3.70; G0=4.93066017178; G1=7.04
PIV=np.array([-30.,3.05,0])
def law(lo=0.):
 # Offset points are normal offsets of center path, NOT vertical clearance.
 a=pi/4; X=U0; Y=G0; out=[(-32,Y+lo),(X,Y+lo)]
 for b in np.linspace(0,a,65)[1:]:
  out.append((X+(3-lo)*sin(b),Y+3-(3-lo)*cos(b)))
 X+=3*sin(a);Y+=3*(1-cos(a));d=G1-G0-4.2*(1-cos(a))
 X+=d;Y+=d;out.append((X-lo*sin(a),Y+lo*cos(a)))
 for b in np.linspace(a,0,65)[1:]:
  out.append((X+1.2*sin(a)-(1.2+lo)*sin(b),Y-1.2*cos(a)+(1.2+lo)*cos(b)))
 out.append((4,G1+lo));return np.array(out)
def shape(poly,t):
 p=np.asarray(poly)
 if np.sum(p[:,0]*np.roll(p[:,1],-1)-p[:,1]*np.roll(p[:,0],-1))<0:p=p[::-1]
 return CrossSection([p]).extrude(t[1]-t[0]).translate([0,0,t[0]])
def subprofile(off,t,base):return shape([*law(off),(4,base),(-32,base)],t)
def zpin(x,y,t,r):return M.cylinder(t[1]-t[0],r,r,N).translate([x,y,t[0]])
def trim(z,mask):return z^mask
def local(b):
 put=b.put;put('barrel',ring((-16.10,-.02),9.70,10.90),'fixed','7075')
 for i,x in enumerate([(-14.9,-13.7),(-7.45,-6.25)]):put('sleeve band '+str(i),ring(x,9.65,9.70),'fixed','bronze')
 face=ring((-2.21,0),6.37,9.74)
 for a in PH:face-=loc(box((-2.4,.2),(2.6,10.1),(-4.46,4.46)),a)
 for a in VP84:
  v=box((-4,.2),(6.38,10.06),(-2.70,2.70))
  for s in (-1,1):v=v.trim_by_plane((cos(radians(65)),0,s*sin(radians(65))),-1.50)
  face-=loc(v,a)
 put('V plate',face);put('pilot',ring((-2,0),5.10,5.34))
 # Front sector ground and 3 disconnected seat islands have bolted barrel backing.
 cylout=cyl((-15.15,1.48),9.60);core=cylout-cyl((-15.3,1.55),6.33)
 nose=union(loc(box((-2.31,1.49),(3.25,10),(-4.25,4.25)),a) for a in PH)
 body=core^(nose+box((-15.16,-2.30),(-11,11),(-11,11)))
 cutter=subprofile(1.5,(-1.4801,1.4801),0)
 for a in PH:
  body-=loc(cutter,a)
  for side in [-1,1]:
   def T(i,j):return sorted([side*i,side*j])
   # Only beside (not inside) the working roller generator.
   body-=loc(box((-6.20,1.51),(7.99,8.66),T(1.48,1.78)),a)
   body-=loc(box((-6.20,1.51),(1,8.05),T(1.48,4.40)),a)
   pr=law(-.56);xs=np.unique(np.r_[[-5.65,1.26],pr[(pr[:,0]>-5.65)&(pr[:,0]<1.26),0]])
   ys=np.interp(xs,pr[:,0],pr[:,1])
   blade=shape(list(zip(xs,ys))+list(zip(xs[::-1],np.maximum(3.80,ys-.48)[::-1])),T(3.48,3.72))
   bridge=box((1.255,1.48),(G1-.56-.48,9.6),T(3.48,3.72))^cylout
   body+=loc(blade+bridge,a)
 for a in EP:body-=cyl((-16,1.1),.80,*at(5.82,a))
 # Sleeve tail skirt engages ring nut: pitch cylinder & two 60° flank reserves.
 skirt=ring((-22.65,-14.98),7.53,8.99)
 body-=cyl((-15.33,-11.53),7.55)
 body-=cyl((-15.34,-9.05),1.63,-4.95,2.23)
 put('slotted sleeve and skirt',body+skirt,'sleeve','steel','thread')
 # Ground antirotation spline lies between working sectors; stops tangential sleeve rotation.
 for a in (30,150,270):
  groove=loc(box((-24.98,-10.4),(8.59,11),(-.43,.43)),a)
  n='slotted sleeve and skirt';m,g,mt,k=b[n];b[n]=(m-groove,g,mt,k)
  put('spline '+str(a),loc(box((-15.83,-15.45),(8.64,9.77),(-.39,.39)),a))
 cage=ring((-9.10,-8.45),1.24,6.32)
 for a in EP:cage-=cyl((-9.2,-8.4),.80,*at(5.82,a))
 for a in PH:
  for s in [-1,1]:
   cage-=loc(box((-9.2,-8.4),(3.52,7),sorted([s*3.40,s*3.86])),a)
   t=sorted([2.90*s,3.28*s])
   q=box((-5.145,-3.345),(4.25,7.84),t)
   sl=union(zpin(-4.245,r,(t[0]-.1,t[1]+.1),.525) for r in (4.89,7.10)).hull()
   # cheek support at inner corner extends to the aft crossplate.
   arm=box((-8.76,-4.97),(4.25,4.48),t)
   wall=box((-5.095,-3.395),(4.40,7.82),sorted([3.90*s,4.15*s]))
   cross=box((-5.185,-4.965),(7.72,7.91),sorted([3.13*s,4.04*s]))
   cage+=loc((q-sl)+arm+wall+cross,a)
  pin=zpin(-4.220,G0,(-3.84,3.84),.50)+zpin(-4.220,G0,(-1.50,1.50),1.50)
  put('roller '+str(a),loc(pin,a),'r'+str(a))
 put('rail-free cage',cage,'cage')
 for a in EP:
  y,z=at(5.82,a)
  for i,x in enumerate([(-3.,-1.50),(-10.9,-9.4)]):put('eject bush '+str((a,i)),ring(x,.471,.68,y,z),'fixed','bronze')
  put('cage reset abutment '+str(a),loc(box((-8.205,-7.83),(4.65,6.15),(-.50,.50)),a)-cyl((-8.26,-7.75),.476,y,z))
  put('bush spine '+str(a),ring((-9.43,-2.94),.475,.60,y,z))
  put('bush bridge '+str(a),loc(box((-1.5,-1.18),(5.8,7.27),(-.36,.36)),a)-cyl((-1.6,-1.1),.472,y,z))
  put('pilot web '+str(a),loc(box((-1.45,-1.17),(5.25,6.95),(-.29,.29)),a+16))
  put('pushrod '+str(a),cyl((-25.53,-.73),.45,y,z),'eject')
 put('annular ejector',ring((-.85,.10),5.4,6.32),'eject')
 ec=(-4.95,2.23);q=ring((-25.70,-25.0),4.05,6.48)
 q+=cyl((-26.24,-24.46),1.94,*ec);q-=cyl((-26.34,-24.36),1.503,*ec)
 put('eject crosshead',q,'eject','bronze','thread')
 # Centered draw cartridge. Rear cage flange moves with cage; three compression
 # elements do not push the sleeve. Front disk follows a positive input shaft.
 collar=ring((-16.75,-16.16),1.24,3.72)
 for a in PH:collar+=cyl((-16.50,-8.85),.34,*at(3.64,a))
 collar-=cyl((-16.95,-8.42),2.00,-4.95,2.23)
 put('cage return bell',collar,'cage')
 put('draw driver',cyl((-11.53,-10.96),3.48)+cyl((-34.52,-11.42),1.12),'draw')
 put('return shoulder',ring((-18.28,-17.795),1.08,1.78),'draw')
 for a in EP:put('series spring '+str(a),ring((-16.16,-11.53),.870,1.270,*at(2.27,a)),'coil','spring','reserve')
 head82.VP=VP84
 tail(b,'own','yaw',-PITCH);tail(b,'guest','guest')
def phase(p,t):
 # c=0 at DRAW, .245 at reset; d=0 at DRAW, 1.29 at powered reset.
 c=.245;d=1.29;s=e=0.
 if p=='DRAW':c*=1-t;d*=1-t
 if p=='UNLOCK':c*=min(1,3*t);d*=min(1,3*t);s=-4.60*max(0,(3*t-1)/2)
 if p in ('PARK','EJECT'):s=-4.60;e=8.10*t if p=='EJECT' else 0
 l=law();r=np.interp(-4.220+c*(.220/.245)-s,l[:,0],l[:,1]);dr=r-G0
 v={'fixed':[0,0,0],'yaw':[0,0,0],'sleeve':[s,0,0],'draw':[d,0,0],'cage':[c,0,0],'eject':[e,0,0],'guest':[max(0,e-.60),0,0],'coil':[c,0,0]}
 for a in PH:v['r'+str(a)]=[c*(.220/.245),*at(dr,a)]
 return v
