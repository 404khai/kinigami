from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('shell-tilt70.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def run():
 e=json.loads((D/'shell-elec70.json').read_text());h=groups(head()+e);grid=np.arange(-15,15.001,.5)
 aa=np.array([extlist(yaw(h,a)) for a in grid]);r=np.array([far(q,H) for q in h]);d=(2*r*sin(radians(.125)))[:,None];box=np.stack((aa[:,:,0].min(0)-d,aa[:,:,1].max(0)+d),axis=1);dsx=P*ds[:,0]
 raw=np.maximum(box[:,0,None]-box[None,:,1]-dsx,box[None,:,0]+dsx-box[:,1,None]).max(2);print('broad pair count',int((raw<0).sum()))
 hits=[]
 for i,j in zip(*np.where(raw<0)):
  # Only unresolved pairs; rigid poses from exact stage states, not swept
  # hulls. Retain positive-volume intersection of actual box / capsule.
  if h[j][0]!='cell bulk' or not h[i][0].startswith(('external park lever','radial slide','slider link pin','axial transfer','centre clevis link')):continue
  for ph in (-3.2,0,8,16,25,34,42):
   z=next((q for q in state(ph) if q[0]==h[i][0]),None)
   if z is None:continue
   for y0 in (-15,-7.5,0,7.5,15):
    for y1 in (-15,-7.5,0,7.5,15):
     p=yaw([z],y0);u=move(yaw([h[j]],y1),P);gg=pairs(p,u)[0]
     if gg<0:
      b=ball(p[0],u[0]);hits.append((b[3],z[0],ph,y0,y1,b[:3].tolist()))
 print('deepest actual cell bulk / solid member ball',max(hits) if hits else None)
 if hits and max(hits)[0]>0:print('actual closed/open neighbor clearance fails with nominal package, not only an AABB.')
 else:
  # Verify pairwise interval support including per-member yaw variation.
  mm=np.inf;pair=None
  for i,j in zip(*np.where(raw<.4)):
   A=aa[:,i];B=aa[:,j];per=float(d[i,0]+d[j,0]);vmin=np.maximum(A[:,0,None]-B[None,:,1]-dsx,B[None,:,0]+dsx-A[:,1,None]).max(2);val=vmin.min()-per
   if val<mm:mm=val;pair=h[i][0],h[j][0],np.unravel_index(vmin.argmin(),vmin.shape)
  print('all registered two-yaw interval hulls lowest support margin (neg inconclusive)',mm,pair)
  # Receiver-frame support: yaw(A-B) about H; peer translation P*X
  # rotates by -yaw(B). Directions include the recipient's own box axes.
  step=.25;rr=np.arange(-30,30.001,step);yy=np.arange(-15,15.001,step)
  ix=(np.rint((yy[:,None]-yy[None,:]+30)/step)).astype(int)
  rotP=np.c_[P*np.cos(np.radians(yy)),-P*np.sin(np.radians(yy)),0*yy]
  k=np.arange(120);z=(2*k+1)/120-1;D2=np.r_[ds,np.c_[np.cos(k*2.399963)*np.sqrt(1-z*z),np.sin(k*2.399963)*np.sqrt(1-z*z),z],np.eye(3)]
  worst=10.;wp=None
  for i,j in zip(*np.where(raw<.45)):
   A=np.array([ext(yaw([h[i]],y)[0],D2) for y in rr]);B=np.array(ext(h[j],D2));dd=rotP@D2.T
   g0=1e4
   for jj in range(len(yy)):
    aa0=A[ix[:,jj]];vv=np.maximum(aa0[:,0]-B[1]-dd[jj],B[0]+dd[jj]-aa0[:,1]).max(1);g0=min(g0,vv.min())
   g0-=2*r[i]*sin(radians(step/2))+2*P*sin(radians(step/4))
   if g0<worst:worst=g0;wp=(h[i][0],h[j][0])
  print('receiver-relative independent-yaw support minimum (all other pairs at least .45)',min(.45,worst),wp)
if __name__=='__main__':run()
