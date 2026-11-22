"""Direct output latch. No input-side brake or parking pin on this layout."""
from drive79 import *
PINY=8.44;PX=RX+2.39;PY=11.65;ROLL=.74;FLANK=PINY+ROLL+.03
def out(s):
 f=platform(s)
 for k in (-1,1):
  z=k*11.60
  f +=[bx('trunnion root '+str(k),(RX-1.01,RX+1.0),(PINY-.90,PINY+.90),sorted((z-.93*k,z+.22*k))),
       ax('output catch trunnion '+str(k),2,*sorted((k*11.68,k*13.27)),(RX,PINY),ROLL)]
 return move(f[-4:],s*Y)+f[:-4]
def swing(q,a):
 x,y=PX,PY;return rot(q,a,[x,y,0])
def piece(n,v,z,k):return sol(n,[(x,y,zk*k) for x,y in v for zk in z])
def pawlm(k,ang):
 # On trunnion +Y load, force on pawl is +Y underneath flat.
 # Axial eccentricity toward -X rotates this pawl clockwise INTO stop.
 # CCW release lifts? left tip lowers with CCW; cannot swing through
 # loaded pin! use convex rotating relief or allow unloading displacement.
 z=(11.83,13.09)
 tip=[(RX-.98,FLANK),(RX+.73,FLANK),(PX+.54,PY-.65),(PX+.54,PY+.68),(PX-.60,PY+.88),(RX-1.08,FLANK+1.16)]
 f=[piece('hook forged body '+str(k),tip,z,k),
 ax('pawl pivot boss '+str(k),2,*sorted([k*z[0],k*z[1]]),(PX,PY),.83),
 piece('pawl hard stop heel '+str(k),[(PX-.5,PY-.15),(PX+.32,PY-.40),(PX+1.60,PY+.28),(PX+1.32,PY+1.09),(PX-.5,PY+.80)],z,k)]
 return [swing(q,-radians(ang)) for q in f]
def catchfixed():
 f=[]
 for k in (-1,1):
  z=12.45*k
  f.extend([bx('positive stop for hook '+str(k),(PX+1.03,PX+1.57),(PY-.41,PY+.065),sorted((z-.61,z+.61))),
    ax('pawl pivot stub '+str(k),2,*sorted((11.07*k,13.81*k)),(PX,PY),.56)])
  for z1,z2 in ((10.96,11.69),(13.23,13.93)):
   f+=ann('pawl pivot support '+str((k,z1)),[PX,PY,k*z1],[PX,PY,k*z2],.574,.99,20)
  # direct positive hard stop on output at negative-Y final position;
  # don't rely on the backdrivability of the screw.
  f.append(bx('trunnion lower register '+str(k),(RX-.96,RX+.96),(PINY-1.46,PINY-.76),sorted((k*11.83,k*13.10))))
 return f
# To open: clockwise raises the left tip, but turns into locking stop.
# Counterclockwise is the permitted direction. It initially forces the
# pin downward; compute the required retreat and compare to register.
def hooktest():
 from scipy.optimize import minimize_scalar
 p=np.array([RX,PINY])
 def sep(a):
  q=pawlm(1,-a)[0]
  hull=ConvexHull(np.array(q[1])[:,:2]);v=hull.points[hull.vertices]
  d=1e6
  for aa,bb in zip(v,np.roll(v,-1,axis=0)):
   u=bb-aa;t=np.clip((p-aa)@u/(u@u),0,1);d=min(d,np.linalg.norm(p-(aa+t*u)))
  return d-ROLL
 hit=brentq(sep,0,3)
 # Real common material witness not just negative gap of supports.
 A=pawlm(1,-6.)[0];B=next(q for q in out(0) if q[0]=='output catch trunnion 1')
 z=ball(A,B);zz=ball(A,trans(B,-.020*Y))
 print('hook nominal 0 angle gap .030; earliest forbidden CCW rotation, degrees',hit)
 print('at +6deg actual catch stock ball',np.round(z,6),'at most freely available .020 inward retreat',np.round(zz,6))
 print('seated hook closing torque sign remains hard-stop directed with load fric mu=.23, moment arm min',2.39-.23*(PY-FLANK),'mm')
 return hit
if __name__=='__main__':hooktest()
