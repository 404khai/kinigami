from covers75 import *
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
 st=.00775;al=.00281;cu=.00896
 f=ref['fixed']+facebody()+mounts()+diskfixed()+jawdrive()+ejectdrive()+park()+dogmove(3.03)+drive()+sum((plug(a) for a in AZ),[])+plate()+sum((bushholes(a) for a in BAZ),[])+ref['electrical']+ref['tail']
 cats={};categories={};arr=[]
 def add(k,v,c,l,h,minv=0,cat='named'):
  cats[k]=cats.get(k,0)+v;categories[cat]=categories.get(cat,0)+minv;arr.append((v,c,l,h,minv))
 for q in f:
  n=q[0];lo,hi=ext(q,np.eye(3));lower=0.
  if n=='rolled three-lobe hull':
   # Bound imported from frozen unchanged registered geometry: 0.84 shell
   # around +2.50, interior +1.66; three port-volume debit, round OUT.
   add('steel tail pierced shell + rib blanks',11.965,(lo+hi)/2,lo,hi,(992.13-176.79)*st,'hollow lobe');continue
  if 'air reserve' in n:continue
  v,c=vm(q);k='steel';rho=st
  if n=='cell bulk':add('bare catalog cell',2.9,c,lo,hi,2.9,'cell');continue
  if q in ref['electrical']:k='electronics copper-envelope';rho=cu
  if 'geared ' in n or n=='yaw motor body':k='four motor envelope (Cu)';rho=cu
  if n.startswith(('foot ','upper yaw motor rail','lower yaw motor rail','knuckle tang','rear frame rib','outboard bush strut','forward bush strut','rear bush carrier','fixed continuous case','rear radial gusset','cover pillar','cam cover sleeve','rear idler cap tie','rear frame','hinge frame','jaw motor chassis','jaw motor cross rail','brake motor return','central motor frame tie','fixed guard side','front cover high','outer guard top')):k='7075 mounts/covers';rho=al
  cat='other named'
  if n.startswith('button near-mid sphere'):lower=4*pi/3*2.5**3*st;cat='tail cartridges, balls'
  for p,ri,ro,L in [('cartridge body',2.26,2.54,8.65),('front stop',1.27,2.14,1.08),('front bush',1.22,2.17,.81),('rear cap',1.17,2.17,.80),('limiter',.86,1.09,4.60)]:
   if n.startswith(p):lower=pi*(ro*ro-ri*ri)*L*st/16;cat='tail cartridges, balls'
  if n=='disk shell metal blank':lower=pi*1.6/3*(12.42**2+12.42*11.89+11.89**2)*st;cat='rigid disk, posts, stud'
  if n.startswith('disk post '):lower=pi*1.03**2*12.36*st;cat='rigid disk, posts, stud'
  if n=='moving lead stud':lower=pi*1.44**2*14.47*st;cat='rigid disk, posts, stud'
  if n.startswith('six-seat reservation'):lower=0 # stock allocation only
  if n.startswith('steel face cam'):
   # full axial untouched continuous ring both sides of ALL three tracks
   lower=pi*((17.40**2-16.80**2)+(21.55**2-21.15**2))*1.95*st/48;cat='face cam/wheel'
  if n.startswith('122T metal'):lower=pi*(17.85**2-16.00**2)*1.62*st/48;cat='face cam/wheel'
  if n.startswith('drive flange'):lower=pi*(20.90**2-18.74**2)*1.20*st/48;cat='face cam/wheel'
  if n.startswith('plug toe'):lower=.90*4.48*(17.89-13.30)*st;cat='plugs/ways'
  if n.startswith('X pad'):lower=2.39*.62*1.15*st;cat='plugs/ways'
  if n.startswith('fixed X way'):lower=.32*1.18*6.78*st;cat='plugs/ways'
  if n=='yaw shaft':lower=pi*1.52**2*22.30*st
  if n.startswith('spring package'):lower=pi*.35**2*3.48*pi*4*st
  if n.startswith('jaw worm shaft'):lower=pi*.79**2*25.1*st
  if n.startswith('yaw 114T sector'):lower=.5*(16.67**2-2.69**2)*radians(3.98)*1.24*st
  if n.startswith('fixed continuous case'):lower=.78*v*rho;cat='housing sectors'
  if lower>v*rho+1.e-7:raise ValueError((n,lower,v*rho))
  add(k,v*rho,c,lo,hi,lower,cat)
 for i,o in cases():
  vo,co=vm(o);vi,ci=vm(i);v=(vo-vi)*.00127;lo,hi=ext(o,np.eye(3));add('uncut fixed polymer pods',v,(vo*co-vi*ci)/(vo-vi),lo,hi)
 m=sum(cats.values());mn=sum(categories.values());cg=sum(v*c for v,c,l,h,m in arr)/m
 print('assigned nominal g/mm3 17-4 PH .00775, 7075 .00281, polycarbonate .00127, Cu envelope .00896; not manufacturing bounds')
 print('listed stock gross sums g',cats);print('separately counted selected finished-stock minimums g',categories)
 print('partial lower including nominal bare catalog cell, gross-listed subtotal upper, representative bookkeeping COM home world',mn,m,cg)
 def bound(i,g):
  den=mn;num=sum(m*max(g*l[i],g*h[i]) for v,c,l,h,m in arr)
  for p,r in sorted([(max(g*l[i],g*h[i]),v-m) for v,c,l,h,m in arr],reverse=True):
   if p<=num/den:break
   num+=p*r;den+=r
  return g*num/den
 print('listed COM intervals only home yaw0',[(bound(i,-1),bound(i,1)) for i in range(3)])
 feet=sel(ref['fixed'],('foot (',));print('level table foot and gross COM projection, all feet and four tripods')
 for k in [-1,0,1,2,3]:
  pts=np.vstack([s[1] for j,s in enumerate(feet) if j!=k])[:,:2];h=ConvexHull(pts);eq=h.equations;print(k,h.volume,min(-eq[:,:2]@cg[:2]-eq[:,2]))
 print('Catalog typical 0615 ~2 g + 06/1 gears 4,4,3.4,2 g = nominal 21.4 g not guaranteed lower/upper. Actual as-built total, CG, preload, torque/hard maxima unknown.')
if __name__=='__main__':run()
