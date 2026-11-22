from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('quill-audit67.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def rotor(lower):
 # Union of disjoint radial intervals in each axial slab; no double count
 # from intersecting hub, sleeve, wheel web and closure. For the lower bound
 # completely discard the radial reach of each cut + tooth dedendum reserve.
 v=[]
 for n,l,h,i,o in annuli():
  if lower and n=='disk sleeve':i=11.89
  if lower and n=='face cam':
   v +=[(l,O-11.19,i,o),(O-11.19,h,i,15.65),(O-11.19,h,20.31,o)];continue
  if lower and n=='130T rim':o=19.095
  v.append((l,h,i,o))
 xs=sorted({p for s in v for p in s[:2]});vol=0.;mom=0.
 for lo,hi in zip(xs,xs[1:]):
  mx=(lo+hi)/2;rs=sorted((ri,ro) for l,h,ri,ro in v if l<mx<h);prior=0;area=0
  for ri,ro in rs:
   if ro>max(prior,ri):area+=pi*(ro**2-max(prior,ri)**2)
   prior=max(prior,ro)
  vol+=area*(hi-lo);mom+=area*(hi-lo)*mx
 return vol,mom
def polyvol(v):
 # volume & centroid of a convex polytope by positively oriented tets.
 a=np.array(v);h=ConvexHull(a);ref=a.mean(0);p=a[h.simplices];dv=abs(np.einsum('ij,ij->i',p[:,0]-ref,np.cross(p[:,1]-ref,p[:,2]-ref)))/6;return dv.sum(),((p.sum(1)+ref)*dv[:,None]).sum(0)/(4*dv.sum())
UU=np.r_[ds,-ds];Rscale=1/min(-ConvexHull(UU).equations[:,3])
def vm(q):
 n,v,r,d=q;v=np.array(v)
 if not r:return polyvol(v)
 if len(v)==2 and d is not None and abs(np.linalg.norm(v[1]-v[0])-abs((v[1]-v[0])@d))<1e-6:
  return pi*r*r*np.linalg.norm(v[1]-v[0]),v.mean(0)
 if len(v)==2 and d is None:return pi*r*r*np.linalg.norm(v[1]-v[0])+4*pi*r**3/3,v.mean(0)
 if len(v)==1:return 4*pi*r**3/3,v[0]
 if d is None:u=UU*Rscale # guaranteed ball outer polytope, not inscribed
 else:
  d=np.array(d);a=np.eye(3)[np.argmin(abs(d))];a=np.cross(a,d);a/=np.linalg.norm(a);b=np.cross(d,a);u=np.array([(cos(t)*a+sin(t)*b)/cos(pi/24) for t in np.arange(24)*pi/12])
 return polyvol((v[:,None]+r*u[None,:]).reshape(-1,3))
def run():
 # Explicit MOVING components only at midpoint. Do not use the swept hull
 # as mass. A few scalar envelopes (solenoid, PCB, motor) are metal/FR4
 # allowances, not declarations that their real mass is their box volume.
 e=json.loads((D/'quill-elec67.json').read_text());F=chassis()+pads();S=state(0)+move(tail(),-P)+joint()[1]
 tot={};arr=[]
 def add(q,cat,rho,override=None):
  vol,c=vm(q);mass=rho*vol/1000 if override is None else override
  tot[cat]=tot.get(cat,0)+mass;arr.append((mass,c,*ext(q,np.eye(3))))
 for q in F+S:
  n=q[0]
  if n.startswith(('yaw motor body','clamp motor','retract coil','parking armature','parking spring reserve')):cat,rho='motors and parking cartridge (solid copper upper)',8.96
  elif n.startswith(('broad ejector','56deg seat','disk post','disk key','disk axle','disk roller','seat backer','pole strain')):cat,rho='disk/posts/inserts steel',7.75
  elif n.startswith(('rolled three-lobe','button near-mid','plunger shank','cartridge body','inner stem','captive foot','front stop','front bush','rear cap','spring package','limiter')):cat,rho='tail/port stock incl spring reserves steel',7.75
  elif n.startswith(('cone leaf','drive pin','drive boss','rear rib','rib capsule','outboard crossbar','rear dogleg','bearing pin','external park','central through','leaf bearing','park stop block','centre clevis','slider link pin','face roller','radial slide','axial transfer')):cat,rho='leaf/slots/bearings/transmission steel',7.75
  elif n.startswith(('quill inner','quill rolling','quill outer','shaft aft','shaft front','fixed center','worm','yaw shaft','yaw pinion','yaw keyed','yaw 102','16 hole','parking pin','bolt bush','clamp pinion','motor 16T','clamp pinion','spring cup','coil shell','ring stop lug')):cat,rho='shafts/gear blanks/races steel',7.75
  else:cat,rho='mounts, wall, body, feet aluminum-upper trial',2.81
  add(q,cat,rho)
 for q in e:
  if q[0]=='cell bulk':add(q,'bare cell catalog mass',1,2.9)
  elif 'air reserve' not in q[0]:add(q,'boards, protection, tab/flex (copper upper)',8.96)
 val,px=rotor(False);w=val*7.75/1000;c=np.array([px/val,0.,0.]);tot['rotor 17-4PH net union BEFORE groove cuts']=w
 arr.append((w,c,np.array([-6.03,-20.84,-20.84]),np.array([8.,20.84,20.84])))
 low,lp=rotor(True);rlo=low*7.75/1000
 print('assigned density g/cc steel17-4PH 7.75, Al7075 2.81, Cu 8.96, steel density not motor part specification')
 for k,v in sorted(tot.items()):print(k,round(v,3),'g')
 m=sum(tot.values());com=sum(w*c for w,c,l,h in arr)/m;print('all listed mass upper g (overlaps, blanks, uncut ports, empty motor & electronics envelope charged)',m,'gross upper-model COM (NOT upper actual COM)',com)
 frustum=pi*1.6/3*(12.42**2+12.42*11.89+11.89**2)
 print('certain installed steel rotor core + disk + 2.9g cell mass lower (this steel assignment)',rlo,frustum*7.75/1000,rlo+frustum*7.75/1000+2.9)
 # Much tighter disjoint mass lower: subtract an UPPER BOUND on each
 # cutter volume, even where three swept tools cut air outside the blank.
 angle=radians(111.0);hcut=1.036+.021;amin=9.47;amax=11.80;da=asin(hcut/amin);diskcut=.5*((amax+hcut**2/amin)**2-amin**2)*(2*hcut*angle+2*da*TR+4*hcut*da)
 # Face cam R(D) monotone up to park (r' positive), so planar curve
 # length bounded by rmax times angular span plus radial total variation.
 dr=link(0)[2]-link(phase(-4.25)[0])[2];Rmax=link(0)[2]-2;rc=.935
 facecut=(pi*rc**2+2*rc*(Rmax*angle+dr))*(11.10+.025-9.04)
 teethV=pi*(19.80**2-19.095**2)*2.58
 rl=(val-3*(diskcut+facecut)-teethV)*7.75/1000
 # Genuinely INSCRIBED rolled lobe (48-sided circles, then convex hull
 # of disjoint spheres' inscribed points). Debit full 3 oversized ports.
 cc=[]
 for a in AZ:cc.extend([pos(a,-2.25,6.75)+4*U(i*7.5) for i in range(48)])
 for x,r in ((-2.25,7.60),(.20,7.10),(2.50,6.),(4.40,3.5),(-.30,7.58),(2.25,6.50),(5.80,3.16)):cc.extend([pos(0,x,0)+r*U(i*7.5) for i in range(48)])
 cc=np.array(cc);cc=cc[ConvexHull(cc).vertices];ll=ConvexHull((cc[:,None,:]+2.50*UU).reshape(-1,3)).volume
 boring=3*pi*2.66**2*(8.3+4.75);lm=(ll-boring)*7.75/1000;bm=3*4*pi/3*2.50**3*7.75/1000
 print('lower steel rotor (bounded swept cuts), bored lobe, 3 actual balls, disk steel and catalog cell, total lower (named parts only)',rl,lm,bm,frustum*7.75/1000,rl+lm+bm+frustum*7.75/1000+2.9)
 # Rigorous coordinate intervals of listed COM: known rotor/disk/cell core
 # scaled by actual mass; all residual listed residual weights bounded by
 # 0..m_i and each individual centroid by its support bbox.
 b0=next(q for q in e if q[0]=='cell bulk');# catalog cell COM inside its envelope
 lo0,hi0=ext(b0,np.eye(3));diskc=np.array([O+HOME-.8,0,0]);m0=frustum*7.75/1000
 # Include residual double held bboxes conservatively; do not give exact
 # orientation of unknown cut mass or allocate missing shell/loom.
 fixed=[(rlo,np.array([lp/low,0,0]),np.array([lp/low,0,0])),(m0,diskc-[.8,0,0],diskc+[.8,0,0]),(2.9,lo0,hi0)]
 ar=[(w,l,h) for w,c,l,h in arr if w!=2.9]
 def extreme(k,sg):
  w0=sum(w for w,l,h in fixed);s0=sum(w*(max(sg*l[k],sg*h[k])) for w,l,h in fixed)
  tmp=sorted([(max(sg*l[k],sg*h[k]),w) for w,l,h in ar],reverse=True);a=w0;b=s0
  for x,w in tmp:
   if x<=b/a:break
   a+=w;b+=w*x
  return sg*b/a
 print('conservative COM intervals mm, independent listed mass/position uncertainty',[(extreme(k,-1),extreme(k,1)) for k in range(3)])
if __name__=='__main__':run()
