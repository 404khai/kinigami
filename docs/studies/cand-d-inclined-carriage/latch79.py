"""Direct output-side rolling latch with a four-slot index and blocking arc.
Prior undercut fixed-axis hook is kept in hold79.py, NOT installed."""
from sweep79 import *
LX=RX+2.17;LY=PINY+3.55
LC=np.array([LX,LY]);PC=np.array([RX,PINY]);DR=np.linalg.norm(PC-LC);R0=1.10;DEL=radians(4.0);E0=DR*cos(DEL)-sqrt((ROLL+R0+.030)**2-(DR*sin(DEL))**2)
C=5.50;GZ=-12.50;DZ=-11.45;MID=np.array([LX,LY-C])
def rot2(a):return np.array([[cos(a),-sin(a)],[sin(a),cos(a)]])
def ec(a):return LC+rot2(radians(a)-DEL)@(PC-LC)/DR*E0
def eccentric(a):
 f=[]
 for k in (-1,1):
  cen=ec(a)
  # roller turns independently on peripheral pin; parallel side strap
  # is on OUTER side beyond trunnion tips, not a plate filling swept slot.
  f+=[ax('output locking roller '+str(k),2,*sorted((11.85*k,13.12*k)),cen,R0),
      ax('small roller axle '+str(k),2,*sorted((11.49*k,13.88*k)),cen,.57),
      sol('index arm outer strap '+str(k),[(xx+r*cos(t),yy+r*sin(t),z*k) for (xx,yy),r in ((LC,.98),(cen,.84)) for t in np.arange(20)*2*pi/20 for z in (13.34,14.04)])]
 f+=[ax('index shaft',2,-15.49,14.06,LC,.87),bx('square index drive tenon',(LX-.634,LX+.634),(LY-.634,LY+.634),(-16.91,-14.66))]
 return f
def blocks():
 f=[]
 for k in (-1,1):
  for z1,z2 in ((10.08,11.32),(14.25,14.92)):
   f+=ann('index support '+str((k,z1)),[LX,LY,k*z1],[LX,LY,k*z2],.888,1.51,24)
   f.append(rod('index pedestal '+str((k,z1)),[LX+.98,LY,k*(z1+z2)/2],[-9.70,LY-2.9,k*(z1+z2)/2],.55))
  f.append(bx('trunnion lower register '+str(k),(RX-.96,RX+.96),(PINY-1.46,PINY-.76),sorted((k*11.83,k*13.10))))
 return f
AR=C/sqrt(2);RO=4.62;BR=2.72;PIN=.42;GSLOT=.44;ZW=(-16.72,-15.56)
def stockwheel(x,y):
 r=hypot(x,y)
 if r>RO or max(abs(x),abs(y))<.646:return False
 for j in range(4):
  q=rot2(-j*pi/2)@np.array([x,y]);u,v=q
  # blocking arcs on 4 quadrants, slots midway between arcs
  if hypot(u,v+C)<BR+.028:return False
  if abs((u+v)/sqrt(2))<GSLOT and (u-v)/sqrt(2)>C-AR-.45:return False
 return True
def phased(a):
 p=ec(a)-PC
 return np.linalg.norm(p)-R0-ROLL
def latcheck():
 print('index center',LC,'analytic driver-center template before 270deg installation clock',MID,'4-slot radius/pin/bush',AR,PIN,BR)
 print('latch at LOCK pos/normal clearance',ec(0),phased(0),'peak cam approach vs pin, min radial clearance',phased(0)-phased(4),phased(4))
 pk=eccentric(90);keypin=ax('trunnion',2,11.68,13.27,(RX,PINY),ROLL)
 g=[]
 for q in pk:
  b=sweep([keypin],S*Y);g.append(pairs([q],b))
 print('PARK swept trunnion vs retracted latch',min(g))
 # +Y and -Y free travel to hard geometry: no current/stall dependency.
 cen=ec(0)-PC; free=cen[1]-sqrt((ROLL+R0)**2-cen[0]**2)
 print('max free out / in on TRUNNION, excluding twist, flex and slotted pin lash',free,.020)
 # True blocking points on actual wheel (within outer rim, slot relieved)
 # and full uncut ±20deg center of driver's blocking land, ± sign dwell.
 best=[]
 for sg in (-1,1):
  hit=[]
  for u in np.arange(-1.95,1.951,.025):
   v=-C+sqrt((BR+.040)**2-u*u)
   if not stockwheel(u,v):continue
   ang=degrees(atan2(u,v+C))
   if abs(ang)>36:continue
   def overlap(a):return np.linalg.norm(LC+rot2(radians(sg*a))@np.array([u,v])-MID)-BR
   if overlap(4)<0:hit.append((brentq(overlap,0,4),u,v))
  best.append(min(hit))
 print('two actual wheel interior points enter solid registered disk at degrees (x,y relative)',best)
 print('conditional nut/carriage spring stroke bounds and fit');show()
if __name__=='__main__':latcheck()
