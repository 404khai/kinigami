from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('shell-audit70.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
from itertools import permutations
# Place complete board/cartridge packets; all internal objects in same
# rigid carrier frame. Straight cell tabs routed independently into an
# insulated protection panel, not folded under the bulk cell reserve.
def packages():
 return {'cell':[
 ('cell bulk reserve',(0,0,0),(30.8,16.8,5.4)),
 ('positive tab route',(17.94,-3.54,0),(7.02,2.31,.29)),('negative tab route',(17.94,3.54,0),(7.02,2.31,.29)),
 ('tab insulator',(18.47,0.,-.55),(8.54,11.20,.56)),('protection PCB',(20.57,0.,.65),(4.17,11.06,1.19)),('tab weld clearance',(18.95,0.,1.52),(3.51,9.63,.48))],
 'computer':[('controller board incl LDO SWD',(0,0,0),(16,13,3.5)),('BMD antenna air reserve',(5.36,0,3.56),(6.30,11.40,3.61))],
 'driver':[('coupler H-bridge',(0,0,0),(9.8,8.8,1.87))], 'cutoff':[('independent cutoff',(0,0,0),(6.85,6.2,1.95))],
 'yawdriver':[('yaw H-bridge',(0,0,0),(6.2,5.8,2.05))], 'bolt':[('parking motor bridge',(0,0,0),(5.1,4.4,1.75))],
 'connector':[('bus connector',(0,0,0),(3.35,2.9,2.8))], 'flex':[('interface flex reserve',(0,0,0),(7.2,3.1,2.12))]}
def elec():
 hd=head();t=tailbound();s=hd[:];Hrad=max(far(q,H) for q in t)
 for a in np.arange(-15.,15.01,3.):
  for q in yaw(t,a):s.append(sol(q[0],q[1],q[2]+2*Hrad*sin(radians(.75))))
 dirs=np.array([d for d in ds if np.all(np.isclose(abs(d),0)|np.isclose(abs(d),1)|np.isclose(abs(d),1/sqrt(2))|np.isclose(abs(d),1/sqrt(3)))])
 extA=np.array([ext(q,dirs) for q in s]);aa=np.round(extA,8)
 # Many inner shapes behind a protecting full outer cylinder needn't be
 # kept twice for electronics options. Use a rounded bounding grid.
 grid=np.array(list(product(np.arange(-24.,15.,1.5),np.arange(-25.5,25.6,1.5),np.arange(-22.,26.,1.5))))
 cen=np.array([0,0,0]);out=[];pred={}
 if (D/'shell-cell70.json').exists():
  out=json.loads((D/'shell-cell70.json').read_text());aa=np.r_[aa,np.array([ext(q,dirs) for q in out])]
 for label,parts in packages().items():
  if label=='cell' and out:continue
  best=None;done=set()
  for perm in permutations(range(3)):
   for signs in product((-1,1),repeat=3):
    M=np.eye(3)[list(perm)]*np.array(signs)[:,None]
    if np.linalg.det(M)<0:continue
    vv=[(n,M@o,abs(M)@d*.5) for n,o,d in ((n,np.array(o),np.array(d)) for n,o,d in parts)]
    sig=tuple(tuple(v.tolist()+w.tolist()) for n,v,w in vv)
    if sig in done:continue
    done.add(sig)
    cost=np.max([np.linalg.norm(abs(grid+v-cen)+w,axis=1) for n,v,w in vv],axis=0);ii=np.argsort(cost)
    qmin=np.min([v-w for n,v,w in vv],axis=0);qmax=np.max([v+w for n,v,w in vv],axis=0)
    ii=ii[(cost[ii]<(best[0] if best else 31.5))&(grid[ii,2]+qmin[2]>-23.65)&(grid[ii,0]+qmax[0]<=16.15)]
    if not len(ii):continue
    for n,v,w in vv:
     if not len(ii):break
     p=(grid[ii]+v)@dirs.T;dd=np.abs(dirs)@w
     for lo,hi in aa:
      good=np.any((p+dd+.28<lo)|(p-dd-.28>hi),axis=1)
      if not good.all():ii=ii[good];p=p[good]
      if not len(ii):break
    if len(ii):best=(cost[ii[0]],grid[ii[0]],vv)
  if best is None:print('NO placement',label);continue
  sc,c,vv=best;ls=[bx(n,*zip(c+v-w,c+v+w)) for n,v,w in vv];aa=np.r_[aa,np.array([ext(q,dirs) for q in ls])];out.extend(ls);print(label,sh(c),round(sc,4),[(n,sh(w*2)) for n,v,w in vv])
 (D/'shell-elec70.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
if __name__=='__main__':elec()
