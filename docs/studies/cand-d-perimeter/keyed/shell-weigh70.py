from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('shell-mass70.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
g=run_path(str(Path(__file__).with_name('shell-material70.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def parallel(v,r):
 h=ConvexHull(v);m=0.;pairs={}
 for tri,eq in zip(h.simplices,h.equations):
  for i,j in zip(tri,np.roll(tri,1)):
   k=tuple(sorted((i,j)))
   if k in pairs:m+=.5*np.linalg.norm(v[i]-v[j])*acos(np.clip(eq[:3]@pairs.pop(k),-1,1))
   else:pairs[k]=eq[:3]
 return h.volume+h.area*r+m*r*r+(4*pi/3)*r**3
def port_debit(v):
 h=ConvexHull(v);ins=ConvexHull((v[:,None]+1.66*UU).reshape(-1,3)).equations;outer=h.equations
 # Certified box exclusion; all three ports related by 120 deg symmetry.
 step=.15;xyz=np.array(list(product(np.arange(-4.80,8.70,step),np.arange(7.50,13.20,step),np.arange(-2.8,2.85,step))))
 xyz=xyz[(np.linalg.norm(xyz[:,1:]-[10.3,0],axis=1)<2.67+sqrt(2)*step/2)];p=xyz@np.vstack((X,U(BAZ[0]),U(BAZ[0]+90)));de=sqrt(3)*step/2;remain=0
 for z in np.array_split(p,48):
  out=(z@outer[:,:3].T+outer[:,3]).max(1)>2.50+de
  inn=(z@ins[:,:3].T+ins[:,3]).max(1)<-de
  remain+=sum(~(out|inn))
 return 3*remain*step**3
def net_rotor_min():
 # Exact slab volume for annular stock. For each axial/radial cell,
 # discard the angular union of all possible sampled inflated cutters,
 # entire tooth tip zone, and count only material left in the complement.
 A=annuli();K=bands();cut=json.loads((D/'shell-cam70.json').read_text())
 d=cut['disk'];f=cut['leaf'];dv=np.array(d['trajectory_deg_X_or_rad']);fv=np.array(f['trajectory_deg_X_or_rad'])
 xs=np.unique(np.r_[[x for n,l,h,i,o in A for x in (l,h)],[x for l,h,i,o in K for x in (l,h)],O+np.array(f['extent']),np.arange(-6.1,8.01,.24)])
 rs=np.unique(np.r_[[x for n,l,h,i,o in A for x in (i,o)],[x for l,h,i,o in K for x in (i,o)],19.095,np.arange(5.9,21,.25)])
 m=0.
 for l,h in zip(xs[:-1],xs[1:]):
  x=(l+h)/2;da=dv[(O+dv[:,1]+d['R']>=l)&(O+dv[:,1]-d['R']<=h),0]
  for i,o in zip(rs[:-1],rs[1:]):
   r=(i+o)/2
   if not any(la<x<ha and ia<r<oa for n,la,ha,ia,oa in A):continue
   if r>19.095 and W-1.29<x<W+1.29:continue
   cuts=[]
   if len(da) and o>=d['extent'][0] and i<=hypot(d['extent'][1],d['R']):
    de=degrees(atan(d['R']/d['extent'][0]));cuts.extend([(a+da.min()-de,a+da.max()+de) for a in BAZ])
   if O+f['extent'][0]<=x<=O+f['extent'][1]:
    ff=fv[(fv[:,1]+f['R']>=i)&(fv[:,1]-f['R']<=o)]
    if len(ff):
     de=degrees(asin(f['R']/ff[:,1].min()));cuts.extend([(a+min(ff[:,0])-de,a+max(ff[:,0])+de) for a in AZ])
   ix=0.;tot=0.
   for z,t in sorted((max(0.,z+off),min(360.,t+off)) for z,t in cuts for off in (-360,0,360) if t+off>0 and z+off<360):
    tot+=max(0,t-max(ix,z));ix=max(ix,t)
   rho=7.75 if any(la<x<ha and ia<r<oa for la,ha,ia,oa in K) else 2.81
   m+=rho*.001*pi*(o*o-i*i)*(h-l)*max(0.,1-tot/360)
 return m
def run():
 e=json.loads((D/'shell-elec70.json').read_text());F=chassis()+pads();S=state(0)+move(tail(),-P)+joint()[1];RHO=7.75/1000;A=2.81/1000;arr=[];cat={};named=0.
 def add(n,w,c,lo,hi,lower=0):
  arr.append((w,np.array(c),np.array(lo),np.array(hi),lower));cat[n]=cat.get(n,0)+w
 dv,xv=rotor(False);rv=sum(pi*(o*o-i*i)*(h-l) for l,h,i,o in bands());tabv=sum(vm(q)[0] for q in lugs())
 # All cutter volumes bounded (same derivation Take67, stroke now +8.53).
 ang=radians(111);cc=1.036+.021;amin=9.47;amax=11.80;da=asin(cc/amin);cuts=3*(.5*((amax+cc**2/amin)**2-amin**2)*(2*cc*ang+2*da*TR+4*cc*da)+(pi*.935**2+2*.935*(19.30*ang+link(0)[2]-link(phase(-4.25)[0])[2]))*2.1)+pi*(19.80**2-19.095**2)*2.58
 rlo=net_rotor_min();rup=dv*A+(rv+tabv)*(RHO-A)
 # rings do not intersect (different X or radial bands). all extra tabs
 # charged steel in upper, ignored in lower. Gross first moment before cut.
 mom=xv*A+sum((RHO-A)*pi*(o**2-i**2)*(h-l)*(h+l)/2 for l,h,i,o in bands())
 add('finished mixed rotor before net cuts, with extra steel tab upper',rup,[mom/rup,0,0],[-6.03,-20.84,-20.84],[O-9.04,20.84,20.84],rlo)
 v=tailcore();outer=parallel(v,2.50);inner=parallel(v,1.66);raw=outer-inner
 debris=port_debit(v);shellmin=max(0,raw-debris)*RHO
 ribup=3*13.05*13.42*.62+pi*10.77**2*.62
 # All volumes mm^3; add all rib intersections fully (upper). Shell COM
 # constrained to the real convex outer bounding box, not an exact centroid.
 z=next(q for q in S if q[0]=='rolled three-lobe hull');lo,hi=ext(z,np.eye(3));add('0.84 steel hollow tail and 3 radial ribs + cross-diaphragm',(raw+ribup)*RHO,(lo+hi)/2,lo,hi,shellmin)
 for q in F+S+e:
  n=q[0];lo,hi=ext(q,np.eye(3));lower=0
  if n=='rolled three-lobe hull' or 'air reserve' in n:continue
  if n in ('clamp motor','yaw motor body','park geared 4to1'):w=vm(q)[0]*8.96/1000;cat0='motors copper-envelope upper (catalog typical smaller)'
  elif n=='cell bulk':w=lower=2.90;cat0='catalog bare cell'
  elif q in e:w=vm(q)[0]*8.96/1000;cat0='electronics copper-envelope upper'
  else:
   alu=n.startswith(('aft cantilever','cantilever radial','cross rail','outer axial','knuckle tang','foot','fixed wall','park motor saddle','park saddle','park cam bearing tie','cam bearing to foot','upper yaw motor rail','lower yaw motor rail','stationary case','thin liner','heel land','way anchor','motor rear mount','yaw motor lower saddle','yaw motor upper saddle'))
   rho=A if alu else RHO;w=vm(q)[0]*rho;cat0='7075 mounts, housing, feet' if alu else 'steel drives, bearings, guides, covers, sprung elements'
   if n=='broad ejector':lower=pi*1.6/3*(RD**2+RD*(RD-.53)+(RD-.53)**2)*RHO
   # Finished straight stock away from joints; debit ends deliberately,
   # and use inscribed radial slices, not outer faceting, for lower bounds.
   for pref,rin,rout,len0 in [('quill inner race',3.52,3.97,1.48),('quill outer race',5.55,5.91,1.48),
                              ('cartridge body',2.26,2.54,8.65),('front stop',1.27,2.14,1.08),('front bush',1.22,2.17,.81),('rear cap',1.17,2.17,.80),('limiter',.86,1.09,4.60)]:
    if n.startswith(pref):lower=pi*(rout**2-rin**2)*len0*RHO/(24 if pref.startswith('quill ') else 16)
   if n.startswith(('aft cantilever','outer axial rail','fixed wall heel','cross rail','foot forward tie','foot rear flange tie','park saddle knuckle','lower yaw motor rail','upper yaw motor rail')):
    if len(q[1])==2:lower=pi*max(0,q[2]-.06)**2*max(0,np.linalg.norm(np.array(q[1][1])-q[1][0])-3.4)*rho
   if n.startswith('foot cantilever'):lower=.84*w
   if n=='fixed center quill':lower=pi*3.20**2*14.40*RHO
   if n.startswith('pitched X way'):lower=.32*.57*8.31*RHO
   if n.startswith('radial crosshead web'):lower=.46*1.90*5.90*RHO
   if n.startswith('axial transfer beam'):lower=5.23*1.45*2.41*RHO
   if n.startswith('yaw 114T sector'):lower=.5*(16.67**2-2.69**2)*radians(3.98)*1.24*RHO
   if n=='worm 32T spur':lower=pi*(2.92**2-1.14**2)*1.46*RHO
   if n=='motor 16T spur':lower=pi*(1.33**2-.84**2)*1.46*RHO
   if n=='yaw pinion':lower=pi*(1.41**2-.77**2)*1.18*RHO
   if n.startswith('plunger shank'):lower=pi*1.07**2*2.34*RHO
   if n.startswith('captive foot'):lower=pi*(1.99**2-.83**2)*.45*RHO
   if n.startswith('spring package'):lower=pi*.35**2*3.48*pi*4*RHO
   if n.startswith('worm thrust collar'):lower=pi*(1.58**2-.98**2)*.56*RHO
   if n.startswith('centre clevis link'):lower=(2*.89*4.63+pi*.89**2-pi*(.63**2+.72**2))*.72*RHO
   if n.startswith('bearing pin'):lower=pi*.50**2*2.02*RHO
   if n.startswith('disk axle'):lower=pi*.72**2*3.21*RHO
   if n.startswith('rear dogleg'):lower=1.06*1.98*.66*RHO
   if n.startswith('crosshead X face'):lower=.50*.78*.61*RHO
   if n.startswith('disk key'):lower=8.69*1.30*2.06*RHO
   if n.startswith('disk post'):lower=8.69*1.20*2.70*RHO
   if n.startswith('56deg seat'):lower=w
   if n=='worm shaft':lower=pi*.89**2*27.30*RHO
   if n=='yaw shaft':lower=pi*1.52**2*22.30*RHO
   if n.startswith('blind end closure'):lower=pi*2.50**2*.30*RHO
   if n.startswith('foot ('):lower=2.05*1.97*1.05*A
   if n.startswith('central through clevis PIN'):lower=pi*.58**2*5.20*RHO
   if n.startswith('face roller ') and not n.startswith(('face roller journal','face roller lug')):lower=pi*(.855**2-.74**2)*1.62*RHO
   if n.startswith('disk roller'):lower=pi*(.96**2-.78**2)*1.49*RHO
   if n.startswith('button near-mid'):lower=4*pi/3*2.50**3*RHO
  assert lower<=w+1.e-8,(n,w,lower)
  # Only these interior parts join the strict union bound. Seats start at
  # the disk plane, cartridges and balls are outside the *debited* shell
  # ports. Moving stem shanks, rails and welded joints are omitted here.
  named+=lower
  if n=='cell bulk' or n.startswith(('broad ejector','fixed center quill','56deg seat','button near-mid','cartridge body','blind end closure','disk key','disk post','yaw shaft','pitched X way','worm shaft','yaw 114T sector','spring package','rear cap','front bush','front stop','limiter','worm 32T spur','motor 16T spur','central through clevis PIN','disk roller','worm thrust collar','quill inner race','quill outer race')):pass
  else:lower=0.
  vol,c=vm(q);add(cat0,w,c,lo,hi,lower)
 # Gross upper charges joins/clearance overlaps, moving cam dog sweep.
 print('assigned densities g/cc steel 7.75 Al 2.81 Cu 8.96. Rotor union, steel ring volume, tab positive allowance, cut upper mm3',dv,rv,tabv,cuts)
 print('rotor lower/upper g',rlo,rup,'rolled shell volume, removed upper, stiffeners upper',raw,debris,ribup)
 for k,w in cat.items():print(k,w)
 low=sum(i[4] for i in arr);up=sum(cat.values());print('selected disjoint-material minimum conditional on dimensions/densities + nominal bare catalog cell; listed gross upper (not as-built) g',low,up)
 cg=sum(w*c for w,c,l,h,low in arr)/up;print('gross model representative COM',cg)
 def bound(i,sg):
  m=sum(low for w,c,l,h,low in arr);p=sum(low*max(sg*l[i],sg*h[i]) for w,c,l,h,low in arr)
  for val,rem in sorted([(max(sg*l[i],sg*h[i]),w-low) for w,c,l,h,low in arr],reverse=True):
   if val<=p/m:break
   m+=rem;p+=rem*val
  return sg*p/m
 print('independent COM intervals listed mass & support (no actual COM)',[(bound(i,-1),bound(i,1)) for i in range(3)])
 feet=subset(pads(),('foot (',));fx=np.concatenate([q[1] for q in feet])[:,:2];h=ConvexHull(fx);eq=h.equations;gap=lambda p:min(-(eq[:,:2]@p+eq[:,2]))
 print('level coplanar 4-foot hull X/Y, area, nominal gross CoP margin',fx.min(0),fx.max(0),h.volume,gap(cg[:2]))
 gg=[]
 for k in range(4):
  h=ConvexHull(np.concatenate([q[1] for j,q in enumerate(feet) if j!=k])[:,:2]);eq=h.equations;gg.append((k,h.volume,gap(cg[:2])))
 print('all four possible tripod support hulls (missing index, area, gross-model signed mm margin)',gg,'no 3-contact robust stability')
 print('S at named lower / gross-listed upper, same 70g mass-proportional 26.8006 test ONLY',26.8006*low/70,26.8006*up/70,'max mass for S28',28*70/26.8006)
 print('broader named component subtotal + typical motors (not a disjoint lower, not guaranteed)',named+rlo+shellmin+16,'g.')
 print('Actual COM and total as-built upper unknown: loom, fasteners, closures, gearbox maxima and adhesives not a complete BOM. Catalog 0615 bare 2g ca, 06/1 256:1 ca.4g x2; 4:1 ca.2g. Not guaranteed bounds.')
if __name__=='__main__':run()
