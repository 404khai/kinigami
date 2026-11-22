from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('shell-install70.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def cp(A,B,cap=20):
 out=[];be=extlist(B);ae=extlist(A)
 for i,q in enumerate(A):
  z=np.maximum(ae[i,0]-be[:,1],be[:,0]-ae[i,1]).max(1)
  for j in np.flatnonzero(z<-.009):
   bb=ball(q,B[j])
   if bb is not None and bb[3]>.001:out.append((round(bb[3],4),q[0],B[j][0],np.round(bb[:3],4).tolist()))
 return sorted(out,reverse=True)[:cap]
def core():
 c=[]
 for n,l,h,ri,ro in annuli():
  if n=='disk sleeve':ri=11.89
  if n=='face cam':h=O-11.19
  if n=='130T rim':ro=19.095
  c+=wring(n,l+.015,h-.015,ri+.014,ro-.014,48,True)
 return c
pfx=('yaw main steel','quill inner','quill outer','quill rolling','shaft aft','shaft front','leaf bearing','heel land','thin liner','stationary case','park stop block','park stop outer','worm independent bearing','clamp pinion bearing','bolt bush','retract coil','spring cup')
def subset(S,starts):return [q for q in S if q[0].startswith(starts)]
def groups(S):
 # Hull of union with uniform spherical padding; only outside clearance.
 z={}
 for q in S:
  k=next((p for p in pfx+('cone leaf','cartridge body','front stop','front bush','rear cap','limiter','yaw 70T') if q[0].startswith(p)),None)
  if k and k in ('stationary case','cone leaf','heel land','thin liner','park stop block','park stop outer','leaf bearing','cartridge body','front stop','front bush','rear cap','limiter'):
   v=np.mean(q[1],axis=0);k=(k,max(AZ if k not in ('cartridge body','front stop','front bush','rear cap','limiter') else BAZ,key=lambda a:v@U(a)))
  z.setdefault(k or q[0],[]).append(q)
 res=[]
 for k,v in z.items():
  if len(v)==1:res+=v;continue
  vv=np.unique(np.concatenate([q[1] for q in v]),axis=0)
  if len(vv)>4 and np.linalg.matrix_rank(vv-vv[0])==3:vv=vv[ConvexHull(vv).vertices]
  res.append(sol(str(k),vv,max(q[2] for q in v)))
 return res
def curvesweep():
 c0=phase(-3.295)[0];out=[]
 for a in AZ:
  sets=[leaf(a,an)+sliders(a,an) for an in np.linspace(c0,0,25)]
  # leaf radius to H under 5 and slider dead-center avoided. No geometries
  # from different stations coalesced. .007 covers chord sag and link curve.
  for k in range(len(sets[0])):
   ss=[p[k] for p in sets];v=np.unique(np.concatenate([q[1] for q in ss]),axis=0)
   if len(v)>4 and np.linalg.matrix_rank(v-v[0])==3:v=v[ConvexHull(v).vertices]
   out.append(sol(ss[0][0],v,ss[0][2]+.007))
 return groups(out)
def head():
 return groups(chassis()+pads())+[cy('full stop lug orbit',0,(-4.92,-3.96),(0,0),13.18)]+curvesweep()+sweep(disk(),TR*X)+[cy(n+' outer',0,(x,y),(0,0),ro/cos(pi/48)) for n,x,y,ri,ro in annuli()]
def tailbound():
 t=tail();p=('button near-mid','plunger shank','captive foot','inner stem')
 return move(groups([sweep([trans(q,-.40*X)],.65*X)[0] if q[0].startswith(p) else q for q in t]),-P)+groups(joint()[1])
def audit():
 cs=core();f=chassis()+pads()
 si=[s for s in f if not s[0].startswith(pfx) and s[0] not in ('worm teeth blank','16 hole parking plate blank')];print('rotor structural core vs fixed, excluding intended bearings',cp(cs,si))
 for th in (0,13,42,75,105):
  an,h=phase(th);r=sum((sliders(a,an) for a in AZ),[]);d=move(disk(),h)
  print('at theta',th,'rotor core vs sliders/pins',cp(cs,r+d,3),'disk post and key vs fixed support',cp(subset(d,('disk key','disk post','disk axle')),si,3))
  print('at theta',th,'slider vs nonbearing unrelated fixed incl wall',cp(subset(r,('axial transfer','face roller lug','radial slide tie','centre clevis link')),subset(f,('fixed wall heel','outer axial rail','worm','clamp motor','slider guide cheek','way anchor','park stop outer','leaf mount','foot rail')),4))
 f2=subset(f,('aft cantilever','fixed center quill','knuckle tang','lower yaw motor','upper yaw motor','clamp motor','yaw motor body','way anchor','foot rail','motor rear','worm','coil bracket'))
 # Do not treat filled holes/outer hulls as material vetoes against mated parts.
 for a in (-15,0,15):
  t=yaw(joint()[1]+move(subset(tail(),('cartridge outer bridge','inner stem','plunger readout')),-P),a)
  print('new tail steel vs unrelated chassis',a,cp(t,f2,4))
 drive=subset(f,('clamp motor','worm shaft','worm teeth blank','clamp pinion quill'));other=subset(f,('motor rear mount','worm outboard pillar','worm fore bracket','worm bearing yoke','worm bearing exterior rail','coil bracket','yaw motor body','lower yaw motor rail','upper yaw motor rail','aft cantilever','outer axial rail','way anchor','foot rail'))
 print('drive vs unrelated rails',cp(drive,other,7))
if __name__=='__main__':audit()
