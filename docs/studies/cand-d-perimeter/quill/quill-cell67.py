from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('quill-electrics67.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def cell():
 z=[bx('cell bulk',( -15.4,15.4),(-8.4,8.4),(-2.7,2.7))]
 r=1.55
 for t in (-3.55,3.55):
  vv=[np.array([14.5,t,0])]+[np.array([15.72+r*sin(th),t,r*(1-cos(th))]) for th in np.linspace(0,pi,9)]+[np.array([15.72-(7-1.22-pi*r),t,2*r])]
  for j,(l,h) in enumerate(zip(vv,vv[1:])):
   z.append(sol('folded tab '+str((t,j)),[p+np.array([0,w,0]) for p,w in product((l,h),(-1.15,1.15))],.155))
 z+=[bx('tab insulator',(11.01,16.81),(-5.61,5.61),(2.73,2.88)),bx('protection board',(10.40,15.91),(-5.75,5.75),(3.33,4.43)),bx('spot joint reserve',(14.23,15.83),(-5.03,5.03),(2.99,3.48))]
 return z
def run():
 z=cell();s=head();tt=tailbound();rr=max(far(q,H) for q in tt)
 for a in range(-15,16,3):s +=[sol(q[0],q[1],q[2]+2*rr*sin(radians(.75))) for q in yaw(tt,a)]
 # Restrict to a rotating tangent plane; separate each packet element
 # using world axes AND the packet's own axes. First pass packet AABB,
 # then body & groups. Cost is full OBB support to trial center (-1,0,1).
 best=None
 for angle in range(-180,180,10):
  u=U(angle);v=U(angle+90);axes=np.vstack((X,u,v));DD=np.unique(np.r_[ds,axes],axis=0);aa=extlist(s) if False else np.array([ext(q,DD) for q in s])
  radi=np.arange(17.8,28.1,1.2);zs=np.array(list(product(np.arange(-13.5,7.6,1.5),radi,np.arange(-7.5,7.6,1.5))))@axes
  for k in range(8):
   a1=(X if k%2==0 else v)*(1 if (k//2)%2==0 else -1);n=u*(1 if k<4 else -1);a2=np.cross(n,a1);mat=np.column_stack((a1,a2,n))
   pr=[sol(q[0],np.array(q[1])@mat.T,q[2]) for q in z];grp=[]
   # True convex envelope of thin tab segments; avoid charging a filled
   # extension elsewhere on the cell. Include supplementary projection dirs.
   for ii in ([0],list(range(1,11)),list(range(11,21)),[21,22,23]):
    qq=[pr[j] for j in ii];grp.append(sol('group',np.vstack([l[1] for l in qq]),max(l[2] for l in qq)))
   cost=np.maximum.reduce([np.linalg.norm(zs+v-np.array([-1.,0,1.]),axis=1)+q[2] for q in grp for v in q[1]])
   kt=np.argsort(cost);kt=kt[cost[kt]<(best[0] if best else 36)]
   for q in grp:
    lo,hi=ext(q,DD);p=zs[kt]@DD.T
    for al,ah in aa:
     good=np.any((p+hi+.27<al)|(p+lo-.27>ah),axis=1)
     if not good.all():kt=kt[good];p=p[good]
     if not len(kt):break
    if not len(kt):break
   if len(kt):
    kk=kt[0];ls=offset(pr,zs[kk])
    if min(ext(q,np.eye(3))[0][2] for q in ls)<-23.60:continue
    best=cost[kk],angle,k,sh(zs[kk]),ls
 if best:
  print('folded 7 mm tab route, all listed reservations: max from trial centre, az, clock, cell centre',best[:4]);(D/'quill-cell67.json').write_text(json.dumps(best[-1],separators=(',',':'))+'\n')
 else:
  (D/'quill-cell67.json').unlink(missing_ok=True);print('NO FOLDED-CELL PLACEMENT')
if __name__=='__main__':run()
