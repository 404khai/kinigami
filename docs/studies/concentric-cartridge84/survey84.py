"""Optional deterministic component clock search (not a clearance certificate)."""
from body84 import *
def bb(m):return np.array(m.bounding_box())
def cand(a,c):return np.all(np.minimum(a[3:],c[3:])-np.maximum(a[:3],c[:3])>1e-7)
def contacts(src,tar):
 ac={n:bb(v) for n,v in src.items()};bc={n:bb(v) for n,v in tar.items()};hits=[]
 for n,q in src.items():
  for k,z in tar.items():
   if n!=k and cand(ac[n],bc[k]) and (v:=(q^z).volume())>1.e-5:hits.append((round(v,6),n,k))
 return sorted(hits,reverse=True)
if __name__=='__main__':
 from scipy.spatial.distance import cdist
 b=book();mm=pose(b,'LOCK',0,0)
 ns=['selector 0615/06-1','cam spindle','sleeve closed cam','draw closed cam','spin return fork']
 for l in ['electronics']:
  tar={n:m for n,m in mm.items() if n not in ns and not any(w in n for w in ('cam','selector','spin','dpin','index','clamshell','follower','lock bush'))}
  rows=[]
  for a in range(0,360,4):
   src={n:loc(mm[n],a) for n in ns}
   hits=contacts(src,tar);rows.append((round(sum(x[0] for x in hits),2),a,hits[:3]))
  print(sorted(rows)[:8])
