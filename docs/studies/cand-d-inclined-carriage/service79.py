from containment79 import *
def assembly():
 # Independent nominal bench subassembly, separate roof removed. Slide
 # original key downward BEFORE attaching pickup axle or high shoe.
 key0=[key()]
 way=frontguides()
 for nm,sweepy,A in [('bare key insertion',18.60,way),('pickup axle left in key',18.60,way),('key with lid on',12.,[q for q in lip() if q[0]=='removable high roof'])]:
  if nm.startswith('pickup'):piece0=keyplus()
  else:piece0=key0
  m=sweep(piece0,sweepy*Y)
  print(nm,bpair(m,A,1))
 # Axial operations perpendicular to the guide: insert the solid pickup
 # axle through cage at LOCK after lowering; reserve actual tool OD2.30
 # from z up to +18, not an ideal center ray.
 tool=ax('pickup pin punch OD2.30',2,3.21,18.00,(XC,17.70),1.15)
 print('pickup punch with removable cheek still present',bpair([tool],lip(),1))
 print('pickup punch with cheek removed, excludes tool target',bpair([tool],[q for q in lip() if not q[0].startswith('hood cheek')],1))
 # Long motor assembly and screw access from radial top, guards removed.
 m=next(q for q in production() if q[0]=='key 0615 256')
 block=indexdrive()+waystock()+rest()[1]+rearways()+blocks()
 print('key motor straight Y insertion from above',bpair(sweep([m],34*Y),block,2))
 p=next(q for q in indexdrive() if q[0]=='remote index 0615 256')
 print('aux motor axial insertion −Z from below',bpair(sweep([p],-33*Z),rest()[1]+rest()[0]+waystock(),1))
 _,v,vi,vo=covers()
 print('service cover split y=13 before motor/pin insertion; no cap or removable seam grants tool access to buried cross sections')
 # Thread nominal axial overlap, real intervals at both endpoints.
 for c in (0.,CMAX):
  ov=min(22.35,13.85+c)-max(7.04,11.15+c)
  print('thread engagement before chamfers',c,ov,ov/.60,'turns')
 print('capture retained until PARK? min y catch to input shoulder at LOCK, maximum obtainable closure at travel stop',16.07-12.85,CMAX-(16.07-12.85))
 # Exact -X,+X and Z load-bearing face extents of lower row at park.
 core=np.array(key()[1]);face=core[np.isclose(core[:,2],core[:,2].max())]
 for yy in (4.50,5.35):
  y=yy-S
  h=ConvexHull(face[:,:2]);ls=[];hs=[]
  for a,b,k in h.equations:
   if a>1e-12:hs.append((-k-b*y)/a)
   elif a< -1e-12:ls.append((-k-b*y)/a)
  print('lower Z-face flat width at park, row y',yy,min(hs)-max(ls),'mm')
def updatedcapacity():
 k=(20.61+22.22)/2;j=(24.13+25.75)/2;x=(22.57+23.84)/2
 for f in (20.43,56.3813,80):
  tooth=f*.55961169/(3.60*.88*cos(radians(20)))
  a=tooth*(j-x)/(j-k);b=tooth-a
  print('independent pinion shaft: thrust tooth rear/front bush loads projections MPa and shaft bending, catalog motor bearing load NOT substituted',f,tooth,a,b,a/(1.6*1.61),b/(1.6*1.62),a*(x-k)/(pi*1.6**3/32))
 # One-sided pickup load at front fork: user's force limit is on OUTPUT Y.
 # Worst single branch for threaded output / elastic & bending demands.
 F=60.;tq=F*.55961169;G=79000.;d=1.60
 print('independent shaft stress torsion MPa at input, net tooth couple',16*(tq/(2*.88))/(pi*d**3))
 print('rolling output normalised stop drift: .72deg stable dwell play, smax opening with slot lash')
 vals=[]
 sq=degrees(brentq(lambda t:.634*(cos(t)+sin(t))-.646,0,pi/8));print('additional square-tenon angular play deg',sq)
 for a in np.linspace(-.724-sq,.724+sq,101):
  d=ec(a)-PC;vals.append(d[1]-sqrt((R0+ROLL)**2-d[0]**2))
 print('actual moving-axle center potential mm (key + slot lash .016, excludes deformation/guide cocking)',max(vals)+.016)
if __name__=='__main__':assembly();updatedcapacity()
