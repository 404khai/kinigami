from survey84 import *
from scipy.optimize import minimize
from scipy.spatial.distance import pdist
def fit(points,names):
 h=ConvexHull(points).vertices;v=points[h];owners=np.asarray(names)[h]
 def f(w):return w[3]**2-np.sum((v-w[:3])**2,axis=1)
 def j(w):return np.c_[2*(v-w[:3]),np.ones(len(v))*2*w[3]]
 w=minimize(lambda w:w[3],[-21,0,0,32],jac=lambda w:[0,0,0,1],method='SLSQP',constraints=[dict(type='ineq',fun=f,jac=j)],options={'ftol':1e-10,'maxiter':100}).x
 c=w[:3];norm=np.linalg.norm(v-c,axis=1);r=max(norm);i=np.where(norm>r-1e-5)[0]
 return c,r,[(owners[j],v[j].tolist()) for j in i]
def sphere():
 b=book();pts=[];ns=[];kin={};samp=[('LOCK',0),('DRAW',.5),('DRAW',1),('UNLOCK',.75),('PARK',1),('EJECT',1)]
 for ph,t in samp:kin[(ph,t)]=pose(b,ph,t,0)
 for n,(m,g,mt,k) in b.items():
  if g=='guest':continue
  if g=='yaw':cs=[m.translate(-PIV).rotate([0,0,a]).translate(PIV) for a in np.arange(-15.,15.01,1)]
  elif g=='fixed':cs=[m]
  else:cs=[d[n] for d in kin.values()]
  # Selector and two screws rotate about fixed axes: use circumscribed continuous cylinders.
  if g=='cam':
   a=CAMANG-36.;C=np.array([-12.55,14.12,0.]);q=loc(m,-a).translate(-C);v=mesh(q);r=max(np.linalg.norm(v[:,:2],axis=1))/cos(pi/N);cs=[loc(zpin(0,0,(min(v[:,2]),max(v[:,2])),r).translate(C),a)]
  if g in ('nut','drot'):
   c=yz(17.7,DANG) if g=='drot' else np.zeros(2);v=mesh(m);r=max(np.linalg.norm(v[:,1:]-c,axis=1))/cos(pi/N);cs=[cyl((min(v[:,0]),max(v[:,0])),r,*c)]
  # Roller axial and radial extrema need not coincide: include enclosing translation box.
  if g.startswith('r') and g[1:].isdigit():
   cs=[m.translate([x,*at(d,int(g[1:]))]) for x,d in product([0,.22],[0,G1-G0])]
  for q in cs:
   v=mesh(q);v=v[ConvexHull(v).vertices];pts.extend(v);ns.extend([n]*len(v))
 pts=np.array(pts);c,r,act=fit(pts,ns);d=np.linalg.norm(pts-c,axis=1)
 # Explicit real-stock lower bound (same pose); do not transfer envelope supports.
 one=[];nn=[]
 for n,q in kin[('EJECT',1)].items():
  if b[n][3] in ('air','teeth'):continue
  v=mesh(q);h=ConvexHull(v).vertices;one.extend(v[h]);nn.extend([n]*len(h))
 oc,orr,oa=fit(np.array(one),nn);w=np.array([x[1] for x in oa]);weights=np.linalg.lstsq(np.vstack([w.T,np.ones(len(w))]),np.r_[oc,1.],rcond=None)[0]
 weights=np.maximum(0,weights);weights/=sum(weights);bary=weights@w
 lower=sqrt(weights@np.sum((w-bary)**2,axis=1))
 # Yaw circular arc sagitta of sampled vertices; surface debit for inscribed primitives not catalogue tolerances.
 rho=max(np.max(np.linalg.norm((mesh(m)-PIV)[:,:2],axis=1)) for m,g,_,_ in b.values() if g=='yaw')
 out=dict(label='exploratory',center=c.tolist(),radius=r,nominal_upper_diameter=2*(r+rho*(1-cos(radians(.5)))+.06),yaw_sagitta=rho*(1-cos(radians(.5))),trial_surface_debit=.06,active=act,simultaneous_lower_diameter=2*lower,simultaneous_support=oa,barycentric_weights=weights.tolist(),note='Common sphere, all listed stock and air reservations; conservative orthogonal translation endpoints. Lower via weighted squared distance of simultaneously installed material vertices at zero yaw. Curved-surface debit conditional, no build tolerances.')
 dump('sphere84.json',out);print('diameters',out['nominal_upper_diameter'],out['simultaneous_lower_diameter']);print(sorted([(max(d[np.array(ns)==n]),n) for n in set(ns)],reverse=True)[:22])
if __name__=='__main__':sphere()
