from drive82 import *
from itertools import combinations
from scipy.spatial import ConvexHull
from scipy.optimize import minimize
import hashlib,os,sys
def flat(m):return np.array(m.bounding_box())
def aabb(m,n):return np.all(np.minimum(m[3:],n[3:])-np.maximum(m[:3],n[:3])>1.e-7)
def common(m,n):return max(0.,(m^n).volume())
def poses():
 return [('LOCK',0)]+[(p,t) for p,tt in [('DRAW',[.5,1]),('UNLOCK',[0,.25,.5,.625,.75,.875,1]),('EJECT',[0,.15,.40,.65,1])] for t in tt]
def rounded(a):return np.round(a,7).tolist()
def collision():
 b=book();names=list(b);cache={};rows=[];records={}
 for ph,t in poses():
  v=phase(ph,t)
  for y in [-15,0,15]:
   mm=pose(b,ph,t,y,True);bb={n:flat(m) for n,m in mm.items()}
   tags={g:tuple(d) for g,d in v.items()};tags['yaw']=(y,);tags['coil']=(v['cage'][0],v['draw'][0])
   hits={}
   # Include static-static and attachments. Output raw positives for independent review,
   # NOT counts of unique unintended collisions. No clearance whitelist.
   for i,n in enumerate(names):
    a=bb[n];g=b[n][1]
    for k in names[i+1:]:
     h=b[k][1]
     if not aabb(a,bb[k]):continue
     key=(n,k) if g==h and g!='coil' else (n,k,tags[g],tags[h])
     if key not in cache:cache[key]=common(mm[n],mm[k])
     vol=cache[key]
     if vol>1.e-6:
      key2=n+' | '+k;hits[key2]=round(vol,6)
      if key2 not in records or records[key2][0]<vol:records[key2]=[vol,ph,t,y]
   rows.append(dict(phase=ph,fraction=t,yaw=y,all_positive_volumes_mm3=hits))
 dump('phase-pairs.json',dict(label='exploratory',description='Raw geometric intersections incl designed joins, thread and bearing envelopes, tooth sweeps, electronics and guest; positive overlaps are not all faults. Finite polygonal CSG; sampled clearance is not a certificate.',rows=rows))
 print('PAIR SAMPLES',len(rows),'unique',len(records))
 for key,v in sorted(records.items(),key=lambda x:-x[1][0])[:24]:print(key,rounded(v[:1]),v[1:])
def sphcheck():
 b=book()
 # All non-turning component trajectories piecewise affine. Include every branch boundary.
 pts=[];owners=[]
 def add(n,v):
  if len(v)>80:v=v[ConvexHull(v).vertices]
  pts.extend(v);owners.extend([n]*len(v))
 for name,(m,g,mt,k) in b.items():
  if g=='guest':continue
  vv=mesh(m)
  if g=='yaw':
   v=vv[ConvexHull(vv).vertices];rel=v-PIV
   for a in np.arange(-15,15.001,1):
    c=cos(radians(a));s=sin(radians(a));add(name,rel@np.array([[c,s,0],[-s,c,0],[0,0,1]])+PIV)
  else:
   for ph,t in ([('DRAW',0),('DRAW',1),('UNLOCK',.5),('UNLOCK',1),('EJECT',1)] if g!='fixed' else [('LOCK',0)]):
    d=phase(ph,t)
    if g=='coil':
     w=vv.copy();w[:,0]=-19.43+d['cage'][0]+(vv[:,0]+19.43)*(4.63+d['draw'][0]-d['cage'][0])/4.63
    else:w=vv+d[g]
    add(name,w)
 pts=np.array(pts);ii=ConvexHull(pts).vertices;V=pts[ii];nn=np.asarray(owners)[ii]
 def lower(w):
  c=w[:3];return w[3]**2-np.sum((V-c)**2,axis=1)
 def jac(w):return np.c_[2*(V-w[:3]),np.ones(len(V))*2*w[3]]
 ans=minimize(lambda w:w[3],[-20.,0.,0.,37.],jac=lambda w:np.array([0,0,0,1]),method='SLSQP',constraints=[dict(type='ineq',fun=lower,jac=jac)],options=dict(ftol=1.e-11,maxiter=180))
 c=ans.x[:3];d=np.linalg.norm(V-c,axis=1);r=max(d);active=np.where(d>r-.0001)[0];maxyaw=max(max(np.linalg.norm((mesh(m)-PIV)[:,:2],axis=1)) for m,g,mt,k in b.values() if g=='yaw')
 # Real support spheres require same pose. Choose static worst pair and minimum sphere lower from simultaneous pose by convex combination of material points.
 out=dict(label='exploratory',center_mm=rounded(c),installed_polygonal_common_diameter_mm=2*r,yaw_arc_max_debit_mm=maxyaw*(1-cos(radians(.5))),critical_support=[(nn[i],rounded(V[i])) for i in active],includes_air_and_teeth=True)
 # A separate single installed pose, excluding air and teeth. Furthest actual pair: no assumption of shared sphere center.
 from scipy.spatial.distance import pdist,squareform
 ss=pose(b,'EJECT',1,15);v=[];no=[]
 for n,m in ss.items():
  if b[n][3] in ('air','teeth'):continue
  vv=mesh(m);v.extend(vv);no.extend([n]*len(vv))
 v=np.array(v);i=ConvexHull(v).vertices;v=v[i];no=np.array(no)[i];z=squareform(pdist(v));j,k=np.unravel_index(np.argmax(z),z.shape)
 out.update(one_pose_pair_diameter_mm=z[j,k],one_pose_pair=[[no[a],rounded(v[a])] for a in [j,k]])
 # Curved primitive maximum sagitta .007 for nominal largest smooth R=21/64 segment;
 # raw catalog parts with 24-segment spheres use wider conservative support correction.
 out['uniform_surface_debit_mm']=.06
 out['common_diameter_upper_mm']=2*(r+out['yaw_arc_max_debit_mm']+.06)
 dump('sphere82.json',out);print(out)
def local():
 b=book(); rows=[];a0=-4.20
 for ph,t in poses():
  mm=pose(b,ph,t,0,True);rows.append([ph,t]+[round(common(mm[n],mm[k]),8) for n,k in [('roller cage','guest tri-flat pin'),('roller 0','sleeve'),('roller 0','guest tri-flat pin'),('sleeve','ejector spider'),('pilot','guest tri-flat pin'),('roller cage','ejector rod 60')]])
 # Separate cheek/trunnion variant with unchanged material of the sleeve.
 xc=-4.245
 def cheek(s):
  tt=tuple(sorted([2.8*s,3.25*s]));q=box((xc-.81,xc+.81),(4.25,7.10),tt)
  def end(yy):return M.cylinder(.65,.525,.525,64).translate([xc,yy,tt[0]-.10])
  return q-(end(4.89)+end(6.43)).hull()
 var=[]
 for ph,t in poses():
  mm=pose(b,ph,t,0,True);v=phase(ph,t);c=v['cage'][0]
  che=cheek(1).translate([c,0,0]);tr=M.cylinder(1.80,.50,.50,N).translate([-4.20,RK,1.5]).translate(v['r0'])
  var.append([ph,t,round(common(che,mm['sleeve']),8),round(common(tr,mm['sleeve']),8),round(common(che,mm['guest tri-flat pin']),8)])
 # Rail fault certificate for exact analytic surfaces (independent of manifold tessellation).
 x,y,z=-5.62,4.094,0.;h=3.85-(x-(-4.20-1.5/sqrt(2)))
 margins=dict(rail_x=min(x+5.71,-5.53-x),rail_y=min(y-4.03,4.71-y),rail_t=1.5,shoulder_plane=(h-y)/sqrt(2),head_blank=4.60-y)
 dump('local82.json',dict(label='exploratory',full_stock_pair_columns=['phase','fraction','cage_pin','roller0_sleeve','roller0_pin','sleeve_eject_spider','pilot_pin','cage_ejectrod60'],rows=rows,variant_columns=['phase','fraction','cheek_sleeve','trunnion_sleeve','cheek_pin'],variant=var,analytic_draw_witness=dict(center=[x,y,z],radius_mm=.061,clearances=margins)))
 print('local DRAW rail witness',margins,'variant',var[:3])
if __name__=='__main__':
 for f in sys.argv[1:] or ['local','sphere','pairs']:{'local':local,'sphere':sphcheck,'pairs':collision}[f]()
