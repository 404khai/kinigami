from hold79 import *
from scipy.spatial import cKDTree
def bpair(a,b,maxw=6):
 ea,eb=extlist(a),extlist(b)
 g=np.maximum(ea[:,0,None,:]-eb[None,:,1,:],eb[None,:,0,:]-ea[:,1,None,:]).max(2)
 i,j=np.unravel_index(g.argmin(),g.shape)
 ij=np.transpose(np.nonzero(g<1e-9));w=[]
 for i1,j1 in ij:
  try:
   q=ball(a[i1],b[j1])
   if q[3]>1e-7:w.append((q[3],a[i1][0],b[j1][0],q[:3].round(5).tolist()))
  except Exception:continue
 return round(float(g[i,j]),6),a[i][0],b[j][0],sorted(w,reverse=True)[:maxw]
