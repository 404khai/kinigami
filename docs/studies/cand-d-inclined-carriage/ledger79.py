from path79 import *
from scipy.spatial import QhullError
def volume(q):
 n,v,r,d=q;v=np.asarray(v)
 if not r:
  try:return ConvexHull(v).volume
  except QhullError:return 0.
 if len(v)==2:
  L=np.linalg.norm(v[0]-v[1])
  if d is None:return L*pi*r*r+4*pi*r**3/3
  elif abs(abs((v[0]-v[1])@np.array(d))-L)<1e-8:return L*pi*r*r
 # Convex circumscribed support hull on outer offset shape (safe for a gross envelope)
 A=np.r_[ds,-ds];u=ext(q,A)[1];cc=v.mean(axis=0);verts=HalfspaceIntersection(np.c_[A,-u],cc).intersections;return ConvexHull(verts).volume
def ledger():
 f,e,t=rest();g={};pieces=[]
 def add(key, mass, ctr):
  g[key]=g.get(key,0)+mass;pieces.append((mass,np.array(ctr)))
 def blk(q,tag,rho):
  if q[0]=='BMD antenna air reserve':return
  lo,hi=ext(q,np.eye(3));add(tag,volume(q)*rho,(hi+lo)/2)
 # Assigned finished materials differ from cover/stock void, orbits,
 # swept volumes, ram drives and spring preload. Do not weigh swept parts.
 f0=fixed()+f+followers(0)+bridge(0)+keyplus()+eccentric(0)+enclosure()+t
 for q in f0:
  n=q[0]
  if any(n.startswith(i) for i in ('remote index 0615','key 0615','yaw motor body')):
   blk(q,'motor copper envelope',.00896)
  elif any(i in n for i in ('bushing','thrust bush')):blk(q,'bronze bushes',.00890)
  elif any(i in n for i in ('roof return','cover','guard','hood cheek','shelter')):blk(q,'polymer guards',.00127)
  elif any(i in n for i in ('tie','strut','tab','saddle','foot','roof','bulkhead','mount','support','pedestal','spring foot','outer cheek','barrel','stop column')):blk(q,'7075 housing/support',.00281)
  else:blk(q,'steel all other installed stock',.00775)
 for q in e:
  if q[0]=='cell bulk':add('bare catalog cell',2.9,np.array(q[1]).mean(0))
  else:blk(q,'electronics copper envelopes',.00896)
 # Coil wire volume plus two end turns; exact wire length not given:
 # finite envelope as strict upper on listed configuration only.
 for q in springs(0,0):blk(q,'spring steel envelopes',.00775)
 for q in [ax('index wheel blank',2,*ZW,LC,RO),ax('driver blocking blank',2,*ZW,GIN,BR),ax('index drive pin',2,-17.4,-15.62,GIN,PIN)]:blk(q,'steel blank debit',.00775)
 dw,v,vi,vo=covers();cover=ConvexHull(vo).volume-ConvexHull(vi).volume
 add('external polymer shell before ports',cover*.00127,(vo.max(0)+vo.min(0))/2)
 # No credit for material removed when structural overlap is unknown.
 # Ram/sleeve are interface reservations, not installed 79 drive.
 print('gross listed-category subtotal g, excludes ejector drive and ram; full density-summed blanks double count intersections',g)
 total=sum(g.values());com=sum(q*p for q,p in pieces)/total
 print('gross subtotal (not an as-built upper) g and representative extent-center COM LOCK z yaw 0',total,com)
 lb=4*4*pi*2.50**3/3*.00775+pi*7.60**2*2.50*.00775;print('selected disjoint 4 balls+hub metal and nominal three 6g catalog drives +2.9g cell, partial minimum',lb,lb+3*(4+2)+2.9)
 foot=np.array([np.mean(q[1],0)[:2] for q in f if q[0].startswith('foot (')])
 for j in range(-1,4):
  eq=ConvexHull(foot if j==-1 else np.delete(foot,j,0)).equations
  print('representative support polygon omit',j,'margin mm',min(-(eq[:,:2]@com[:2]+eq[:,2])))
 print('true as-built maximum and COM unknown; 70g not a rating')
if __name__=='__main__':ledger()
