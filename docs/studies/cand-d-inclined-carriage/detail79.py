from tilt79 import *
from rating79 import *
def details():
 HAG=2*pi*.020/.60
 for n,m in ((18,36),(30,30)):
  mod=.20;p1,p2=n*mod/2,m*mod/2;al=radians(20)
  path=sqrt((p1+mod)**2-(p1*cos(al))**2)+sqrt((p2+mod)**2-(p2*cos(al))**2)-(p1+p2)*sin(al)
  print('ideal standard 20deg spur mesh Z/Z transverse contact ratio',n,m,path/(pi*mod*cos(al)),'root radius',p1-1.25*mod)
 print('face screw pitch/support spacing/eccentricity load factors, separate torque/pinion load')
 # No-switch/zero-friction key: no finite contact normal under unpowered
 # opposed squeeze. Is even the two-row centered 60N illustrative
 # opening feasible under baseline-free provisional assumptions?
 q60=60*1.2613739228994332;Q=q60*(1+.3102047677932451);print('60N two-row sample motor-opening force key/rear-yoke plus drag/screw torque/optimistic rated',q60,Q,Q*.55961169,42.172416)
 print('ideal positive-lock roller pinion from angular clearance and hole not proof of achieved preload')
 print('over three LOCK guides, example .15deg cock X differential vs .040 backlash',tan(radians(.15))*(16.6-4.5)+2.68*(1/cos(radians(.15))-1))
 # Faceted sleeve segments have inner radius slight undersize - true
 # bulkhead cut is cylindrical. Volume/mesh not proof of rubbing.
 print('78 sleeve rear-bulkhead concentric clearance before unspecified shift',5.02-4.96,'inner polygon chord clearance',5.02*cos(pi/64)-4.96)
 # Check real round shaft vs boss interference in mounting at LOCK.
 k=next(q for q in eccentric(0) if q[0]=='index shaft')
 cx=next(q for q in bridge(0) if q[0]=='bored spring cap 1 26')
 print('shaft vs cap inner-ball lower, real 3D',ball(k,cx))
 # Is the same ball inside an EXACT cylindrical annulus? Avoid relying
 # on the angular sector's circumradius.
 w=ball(k,cx);p=w[:3];r0=min(w[3],2.08-np.linalg.norm(p[[0,2]]-[RX,ZR]),np.linalg.norm(p[[0,2]]-[RX,ZR])-1.36)
 print('including true cap ID/OD analytic material margin',r0)
 # Nose guide LOCK/PARK X proof remains shape-specific. Proof on .1deg
 # requires measured installed error; no threshold replaced by angular play.
 print('straight guide core radial clearance to cap bore/coil inner diameter',(2*1.36-2*1.29)/2,(3.35-.55)/2-1.29)
 print('nominal stationary trunnion seam to near flank at PARK',pairs(sweep([next(q for q in out(0) if q[0]=='output catch trunnion 1')],S*Y),eccentric(90)))
if __name__=='__main__':details()
