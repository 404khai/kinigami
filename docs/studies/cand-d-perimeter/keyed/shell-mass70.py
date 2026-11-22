from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('shell-audit70.py')))
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
