from carrier75 import *
from scipy.optimize import minimize
from functools import lru_cache
def unit(a):return a/np.linalg.norm(a)
DD=np.unique(np.round(np.r_[ds,np.eye(3),[U(t) for t in np.arange(0,360,2.5)],[AX,AT]],12),axis=0);DD/=np.linalg.norm(DD,axis=1)[:,None]
def minpair(A,B):
 A=list(A);B=list(B);a=np.array([ext(s,DD) for s in A]);b=np.array([ext(s,DD) for s in B]);val=np.inf;name=None;hits=[]
 for i,(lo,hi) in enumerate(a):
  d=np.maximum(lo-b[:,1],b[:,0]-hi).max(1);j=d.argmin()
  if d[j]<val:val=d[j];name=A[i][0],B[j][0]
  hits.extend((A[i],B[j]) for j in np.where(d<-1e-6)[0])
 return val,name,hits
def witness(A,B,count=6):
 g,n,hits=minpair(A,B);balls=[]
 for p,q in hits:
  v=ball(p,q)
  if v[3]>1e-6:balls.append((round(v[3],5),p[0],q[0],v[:3].round(4).tolist()))
 return round(g,5),n,sorted(balls,reverse=True)[:count]
def sel(A,n):return [x for x in A if x[0].startswith(n)]
def group(S):
 out=[];g={}
 for s in S:
  n=s[0]
  if n[-1:].isdigit() and (' ' in n):n=n.rsplit(' ',1)[0]
  g.setdefault(n,[]).append(s)
 for n,ss in g.items():
  out.extend(ss if len(ss)==1 else [convex_union(n,ss)])
 return out
def check():
 F=facebody()+mounts()+diskfixed()+jawdrive()+ejectdrive()+park()+ref['fixed'];e=ref['electrical'];pt=plate()+sum((bushholes(a) for a in BAZ),[])
 for a in AZ:
  p=plug(a);g,n,h=minpair(sweep(p[1:],ST*U(a)),ways(a)+roof(a))
  print('full continuous bridge, both rows, roller vs fixed local case',a,g,n)
 for n,A,B in [
 ('drivetrains vs cell and radio etc',jawdrive()+ejectdrive()+park(),e),
 ('motors against each other',sel(ejectdrive(),('disk geared','disk worm shaft','disk drive 16')),sel(jawdrive()+park()+ref['fixed'],('jaw geared','dog geared','yaw motor body','dog spindle'))),
 ('jaw and disk motors vs static housing and hinge',sel(jawdrive()+ejectdrive()+park(),('jaw geared','dog geared','disk geared')),facebody()+mounts()+ref['fixed']),
 ('actual translating disk inner hardware vs motors',sweep(sel(pt,('disk post','moving lead stud','disk nut','disk terminal collar')),TR*X),sel(jawdrive()+ejectdrive()+park(),('jaw geared','dog geared','disk geared','disk motor truss','disk drive 16T','disk worm blank','jaw worm blank'))),
 ('ring core at untouched working radius vs stationary solids',rg('steel untouched ring',-7.02,-5.04,21.16,21.60,48),sel(F,('rear frame','disk motor truss','cover pillar','fixed guard side','jaw worm shaft','jaw worm blank','jaw geared','dog geared','disk geared','foot ','cover screw shank','rear radial gusset'))),
 ('disk screw shaft and wheel vs unrelated chassis',sel(ejectdrive(),('disk nut journal','disk 24T')),ref['fixed']+sel(F,('rear frame rib','central motor frame tie','hinge frame','disk motor truss'))),
 ('dog stroke vs motor + guide supports',sweep(dogmove(3.03),2.04*Z),sel(F,('jaw geared','dog geared','brake bearing tie','dog spindle','dog spring cap pillar','disk geared','fixed guard side','jaw motor chassis'))),
 ('loaded disk nut and post sweep vs fixed inner guide supports',sweep(sel(pt,('disk post','moving lead stud','disk nut')),TR*X),sel(F,('rear radial gusset','outboard bush strut','front bush strut','central motor frame tie','hinge frame','disk motor truss','rear bush carrier','rear frame rib')))]:
  print(n,witness(A,B))
 for y in (-15,0,15):
  t=yaw(ref['tail'],y);print('own tail and fork vs drive (sample) yaw',y,witness(t,sel(F,('jaw geared','disk geared','dog geared','disk thrust bearing','disk 24T worm','disk screw journal','rear frame rib','brake motor return')),3))
 print('holds require independent swept tooth-land/slot tests; empty witnesses alone not an all-stock certificate')
def sphere():
 h=group(allstock());t=group(tails());c=np.array([-1.5,.4,-.42]);a=[]
 for q in t:
  n,v,r,d=q;v=np.array(v)
  if d is not None:
   u=unit(np.cross(d,np.eye(3)[np.argmin(np.abs(d))]));b=np.cross(d,u);dd=np.array([u*cos(j*pi/64)+b*sin(j*pi/64) for j in range(128)]);v=(v[:,None]+r/cos(pi/128)*dd).reshape(-1,3);r=0
  a+= [(v-H,r,n)]
 v=np.concatenate([q[0] for q in a]);rs=np.concatenate([np.full(len(q[0]),q[1]) for q in a]);rho=np.hypot(v[:,0],v[:,1]);ang=np.arctan2(v[:,1],v[:,0])
 def yf(c):
  d=H-c;delta=(np.arctan2(d[1],d[0])-ang+pi)%(2*pi)-pi;return np.max(np.sqrt((v[:,2]+d[2])**2+rho**2+d[:2]@d[:2]+2*rho*np.linalg.norm(d[:2])*np.cos(np.maximum(0,abs(delta)-radians(15))))+rs)
 near=[q for q in h if far(q,c)>26];f=lambda x:np.r_[[far(q,x) for q in near],yf(x)]
 r=minimize(lambda x:x[3],np.r_[c,31.],method='SLSQP',constraints=[dict(type='ineq',fun=lambda x:x[3]-f(x[:3]))],options={'ftol':1e-11});cc=r.x[:3]
 print('full stroke and analytic yaw incl cylinder circumscription one sphere',2*max(max(far(q,cc) for q in h),yf(cc)),cc,'active',sorted([(far(q,cc),q[0]) for q in h],reverse=True)[:5],yf(cc))
 e=ref['electrical'];solids=sel(h,('jaw geared','dog geared','disk geared','yaw motor body','controller board','cell bulk','foot (','outer guard top'));pp=[(q[0],u) for q in solids for u in polyin(q)];p=np.array([z[1] for z in pp]);dist=np.linalg.norm(p[:,None]-p,axis=2);i,j=np.unravel_index(dist.argmax(),dist.shape);print('actual two-point reservation diameter lower',dist[i,j],pp[i],pp[j])
def peer():
 h=group(allstock());yy=np.arange(-15,15.01,1.);r=np.array([far(q,H) for q in h]);de=2*r*sin(radians(.25));d=P*ds[:,0];aa=np.array([extlist(yaw(h,a)) for a in yy]);lo=aa[:,:,0].min(0)-de[:,None];hi=aa[:,:,1].max(0)+de[:,None]
 raw=np.array([np.maximum(l-hi-d,lo+d-u).max(1) for l,u in zip(lo,hi)]);i,j=np.unravel_index(raw.argmin(),raw.shape);print('independent powered neighbors continuous ±15 broad',raw[i,j],h[i][0],h[j][0])
 # Exact relative-frame support for screened pairs; otherwise interval supports suffice.
 grid=np.arange(-15,15.001,.25);rel=np.arange(-30,30.001,.25);iz=np.rint((grid[:,None]-grid[None,:]+30)/.25).astype(int);tv=np.c_[P*np.cos(np.radians(grid)),-P*np.sin(np.radians(grid)),0*grid]@DD.T;worst=(1e3,None)
 for i,j in zip(*np.where(raw<.20)):
  a=np.array([ext(yaw([h[i]],z)[0],DD) for z in rel]);b=ext(h[j],DD);v=np.inf
  for jj in range(len(grid)):
   s=a[iz[:,jj]];v=min(v,np.maximum(s[:,0]-b[1]-tv[jj],b[0]+tv[jj]-s[:,1]).max(1).min())
  v-=2*r[i]*sin(radians(.125))+2*P*sin(radians(.0625))
  if v<worst[0]:worst=v,(h[i][0],h[j][0])
 print('continuous pair clearance of powered housings',min(.20,worst[0]),worst,'host-to-tail mating contacts not included')
if __name__=='__main__':check();sphere();peer()
