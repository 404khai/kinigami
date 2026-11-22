"""Conditional quasistatic 3D section, load and positive indexing calculations."""
from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('sleeve-short62.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
mu=.23;effS=.28;effG=.72;effB=.80
def force(thrust):
 return thrust*.5/(2*pi*effS)*(sin(pi/8)/(1-sin(pi/8)))*(16/30)/(effG*effB)
def platecalc():
 c=np.array([O-4.31,10.3,0.]);v=np.array([-.5,0.,sqrt(.75)]);q=c+2.5*v
 ai=next(z for z in plate() if z[0]=='60deg seat insert (-90, 1)')
 # Same frame at lower station: radial axis=world -Z, tangent=+Y.
 qa=(O-5.56)*X+10.3*U(-90)+sqrt(.75)*2.5*U(0)
 planes=np.unique(np.round(ConvexHull(np.array(ai[1])).equations,11),axis=0);k=np.argmax(planes[:,:3]@qa+planes[:,3]);n=planes[k,:3]
 print('face trial R cone-flank rounding, nominal tangent, main normal',qa,n)
 for radius in (.12,.25,.50):
  y=qa-radius*n;ds=-(planes[:,:3]@y+planes[:,3]+radius);pr=np.sqrt(np.maximum(0,1-(planes[:,:3]@n)**2));ok=pr>1e-5
  print('exposed insert roll radius, tangent plane patch radius left',radius,min(ds[ok]/pr[ok]))
 print('crest tangential flat and radial top width',3.81-1.95/tan(pi/3)-(2.5*sin(pi/3)+.56/tan(pi/3)),2*(1.35-1.95/tan(pi/3)))
 print('disc front/back radial nominal, belly clearance, button low axial margin',14.5+.28*HOME-RD,14.5+.28*(HOME-1.60)-(RD-.55),(-2.25-2.50)-(-5),(-4.31-2.50)-HOME)
 for fx in (40,75,113):
  ff=np.array([-fx,0.,sqrt(3)*fx]);rx=q-np.array([-2.25,0,0]);M=np.cross(rx,ff);rr=3.45;Ar=pi*rr**2;I=pi*rr**4/4;Jp=2*I
  print('one flank axial N, reacted 3D moments Nmm, gross root equiv normal/shear MPa',fx,M,fx/Ar+rr*hypot(*M[1:])/I,abs(M[0])*rr/Jp)
 print('root section is fixed centreline through circular metal, no one-sided pad reaction')
def bias():
 rw=10.75+2.5/hypot(1,.38);xw=J['tip_x']
 for load in (33,36,39):
  ca=.38/hypot(1,.38);sa=1/hypot(1,.38);nn=load/(ca-mu*sa);fr=nn*(sa+mu*ca)
  print('biased jaw axial / upper normal / upper radial / moment from axial offset',load,nn,fr,load*(18.65-rw))
 print('total spring length/stops',1.80-.50,1.80-.62,1.80-.752,'3N guide friction threshold at Fr=250',3/250)
 print('window free X at endpoints',.11-.12,.11-.132)
 print('bias bottom metal z',-(18.65+ST+4.17))
 print('seated spring shoe returns from rear stop at radial s',.38*.12)
 print('residual radial reaction from unverified dry guide drag μ=.10',.10*250)
 for typ,fn,hi in [('barrel',lambda u: law(u),(7,44)),('short',lambda p:laws(p),(.65,5.55))]:
  # Valid flank at aligned service while re-compressing heel (0 <= s <= .0456).
  s=.0456*.5
  p=hi[0]+(hi[1]-hi[0])*acos(1-2*s/ST)/pi
  eps=.00001
  if typ=='barrel':
   sr=(law(p+eps)[0]-law(p-eps)[0])/(law(p+eps)[2]-law(p-eps)[2]);xnut=law(p)[2];hold=s/.38
  else:sr=(laws(p+eps)[0]-laws(p-eps)[0])/(2*eps);xnut=p;hold=s/.38
  print('early true reseat sensitivity (short is hypothetic if biased)',typ,'coord, input x, heel shift, radial ratio',p,xnut,hold,sr)
  for f in (3*33,3*39):
   for fr in (f/.38,f*(1+mu*.38)/(.38-mu)):
    thrust=sr*fr
    print('axial total, radial total, bare input thrust, conditional peak-index gearhead demand',f,fr,thrust,force(thrust))
 print('16:30 bevel + 8slot Geneva + M3x.5 optimistic thrust limit at 23.9616 Nmm',23.9616/force(1.))
def lawcheck():
 for p in (0,.65,1.50,3.1,5.55,5.90,6.9,9.0,14.25,15.25,16):
  s,h,d,k=laws(p);print('short p, jaw, retreat, relative d, angle deg',p,s,h,d,degrees(k))
 print('short axial terminal x relative plate flat',HOME+TR)
 for s in (0,.02,.0456,ST):
  print('aligned flank at radial, axial following, flange radial gap at full opening only',s,s/.38,12.97895922982139+s-13.25)
 # Positive screw is indexed from motor side; detent output has no motion
 # at entrance/exit, and cannot be opened by pushing on the registered wall.
 b=sin(pi/8);dist=hypot(1.05,4.43);pitch=.5
 for beta in (acos(b),radians(45),0):
  rate=b*(cos(beta)-b)/(1+b*b-2*b*cos(beta))
  print('Geneva entry-to-mid angle deg, angular ratio, input rev / nut advance',degrees(beta),rate,rate*(16/30)*pitch)
 print('index centers, pin radius, max slot inner radius at middle',dist,dist*b,dist*(1-b))
 print('closed-to-park counts',14.75/(pitch/8),CAP/(pitch/8))
 # At terminal lip clearance, the neighbour remains at its original pose;
 # a fixed face cannot create relative energy if sleeve never catches it.
 # Nominal single seat root circle requires pad broadening OR large torque.
 for F in (40,75,113):
  for drag in (0,25):
   print('constant-speed 1:1 sleeve retreat F, extra drag, input T',F,drag,force(F+drag))
 # short sleeve off-centre master torque; release external load need not
 # pass via the master screw at dwell, but eccentric haul can bind yoke.
 for L in (2.8,8,14):
  for mu0 in (.05,.15,.23):
   v=2*mu0*SC/L
   print('master carried load, guide span, μ, jamming ratio, screw x for 40N centre load',L,mu0,v,40/(1-v) if v<1 else inf)
 # return backlash/guide and force non-certified, even ideal core has limited release.
 print('mated held body displacement from sleeve work alone',0)
if __name__=='__main__':platecalc();bias();lawcheck()
