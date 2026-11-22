"""Exact phase responsibilities. Scalar stop loads/cut surfaces are not ratings."""
from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('flange-audit-take59.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def solid():
 f,w,d,c,t=arr();e=json.loads((D/'flange-boards-take59.json').read_text());faces=frame()
 sel=lambda ss,p:[s for s in ss if s[0].startswith(p)]
 ti=sol('true flange inner',[(C)*X+(R-.02)*U(j*360/32) for j in range(32)],RE)
 raw=[ti]+flange()[1:4]
 jopen=[s for i in range(3) for s in tooth(STATION+120*i,ST)]
 # Axial release across OPEN shoes: min radial support of a real shoe in
 # its local fixed slider direction, vs all-YZ flange outer radius.
 hmin=min(np.asarray(tooth(-90,ST)[0][1])@U(-90));print('open shoe vs whole flange unyawed any-X radial gap',hmin-(R+RE))
 print('other open-jaw hardware vs aligned swept flange',pairs(boxesweep(flange()[:4],[TR,0,0]),[s for s in jopen if not s[0].startswith('Take58 contact')]))
 print('disk swept vs fixed bore, radial expression for tapered OD, nominal',min(14.5+.28*(HOME+b)-(RD+d) for b,d in [(-1.45,-.42),(0,0)]))
 disktrue=frust('disk material',(O+HOME-1.45,O+HOME),(RD-.42,RD),inner=True)
 for q in (0,TR/2,TR):
  val=cp(shift([disktrue],q),[s for s in f if s[0].startswith(('disk gearmotor','clamp gearmotor','guide frame rear','frame spoke','clamp jackshaft','disk jackshaft','ring drive','disk thrust frame','disk bearing mount'))])
  print('disk steel vs cans/frame/jacks, X',q,val[:4])
 # Contact-neutral lift: roll-free two heads at independent hinge angles.
 # As X increases, cone poles, shoulders, jaws and fixed wall have different roles.
 # Look for actual unscheduled contact outside the six working cones/three jaw contacts.
 rest=[s for s in f if not s[0].startswith(('flared wall','slide thrust cheek','radial channel'))]+[s for s in jopen if not s[0].startswith('Take58 contact')]
 print('continuous aligned neighbour entire tail +X ray over disk motion vs other stock',pairs(boxesweep(col(flange()),[TR,0,0]),col(rest+w)))
 print('open jaw gap to disk, all phases',pairs(boxesweep(d,[TR,0,0]),jopen))
 for tag,ss in [('closed',c),('open',jopen)]:
  retained=sel(ss,('Take58 contact','rear T slide','guided draw cartridge','radial heel'))
  solids=sel(f,('slide thrust cheek','radial channel','captured shoe','jaw guide-to-wall','ring bearing anchor'))
  print(tag,'shoe material vs fixed guides/feet',cp(retained,solids)[:3])
 # Direction-dependent loading. Each axial stop is unilateral, not a tension bolt.
 a=-90.;v=U(a+90);u=U(a);xa=O+HOME-2.53;xc=O-3.61-2.5/sqrt(2)
 centers=np.vstack([9.25*U(z)[1:] for z in (-90,30,150)]).T
 A=np.vstack((np.ones(3),centers))
 def wgt(t):return np.linalg.solve(A,np.r_[1.,(8.4*u+t*v)[1:]])
 print('stop offsets at projection of one 45-degree cone force line',xc-xa,2.50/sqrt(2),2.50/sqrt(2)+(xc-xa))
 for z in (0.,2.5/sqrt(2),2.5/sqrt(2)+xc-xa):print('barycentric pad thrust fractions vs tangent offset',z,wgt(z))
 for F in (40,75):
  # If screw holds inward at its off-axis location, solve pad reactions anew.
  ws=np.linalg.solve(A,[1,4.85,0]);worst=0
  for j,a in enumerate((-90,30,150)):
   for k in (-1,1):
    off=8.4*U(a)+k*(2.5/sqrt(2)+xc-xa)*U(a+90)
    ww=np.linalg.solve(A,np.r_[1.,off[1:]])
    need=max([0.]+[-F*b/r for b,r in zip(ww,ws) if b<0 and r>0])
    worst=max(need,worst)
  print('screw inbound force sensitivity to restore three nonnegative stops, one cone, F',F,worst,'screw load bary',ws)
 # Normal deflection of yawed disk plate front edge relative bore at home.
 for dz in (0,.05,.1):print('ideal disk center transverse offset, remaining sharp-edge radial clearance',dz,14.50+.28*HOME-RD-dz)
 # Backing/cam: rigid-sliding 3-point ring can float. Flat radial keeper
 # distance b with normals 120° => triangle circumradius 2b before ring touches.
 print('ring radial float from .12 bore gap, groove clearance, total radial lost motion bound (not stiffness)',2*.12,.075,2*.12+.075)
 # Sharp-edge window at each opened sector: test at actual tangential centre.
 p=(-.27-.38)/2;rw=10.75+2.50/hypot(1,.38);xw=-2.25+2.50*.38/hypot(1,.38)
 for x in (-3.5,-2.,xw,-.38):
  roof=max(rw-.38*(x-xw),14.514+2.20*(x+.38),11.33)
  print('park shoe radial recess above cone bore on t=0',x,roof+ST-(14.5+.28*x))
 print('terminal mouth/disk annulus nominal radial gap and face overtravel',14.5-RD,END)
if __name__=='__main__':solid()
def ledge():
 # A following flange at zero yaw can stay on the -.38 ramp as s grows,
 # but only until its CONTACT POINT reaches the other facet.
 xw=J['tip_x'];rw=10.75+2.5/hypot(1,.38)
 xend=(rw+.38*xw-14.514-2.20*.38)/(2.20+.38);last=.38*(xend-xw)
 print('axial force ratio ramp ends at x/s',xend,last)
 for k in (1.5,3.5):
  ph=k*45*20/140;s=lift(ph);x=xw+s/.38
  grad=ST*.5*pi/radians(PH1-PH0)*sin(pi*(ph-PH0)/(PH1-PH0))
  q=np.array([x,rw-s,0.]);planes=np.array(J['halfspaces']);n=planes[:,:3]/np.linalg.norm(planes[:,:3],axis=1)[:,None];b=planes[:,3]/np.linalg.norm(planes[:,:3],axis=1);k0=5
  co=q-.12*n[k0];marg=b-.12-n@co;nperp=np.sqrt(np.maximum(0,1-(n@n[k0])**2));ok=nperp>1e-7;print('plane patch radius remaining after R.12 convex blend',min(marg[ok]/nperp[ok]))
  print('mid-index phi, radial travel, matching axial motion, contact X, valid first flank',ph,s,s/.38,x,x<=xend)
  for F in (40,75,113):
   tq=F/.38*grad*(20/140)*(sin(pi/8)/(1-sin(pi/8)))*(18/32)
   print('F, ideal motor and conditional demanded gearhead',F,tq,tq/(.72*.80*.75))
if __name__=='__main__':ledge()
