"""Conditionally loaded metallic mechanism. Ideal kinematics ≠ service proof."""
from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('drum-package64.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
from scipy.optimize import brentq
IDX=.375;MUS=.23;Rb=10.30;b=sin(pi/8);rr=18.;gr=120.;Gmod=79000.;kw=Gmod*.80**4/(8*3.50**3*3.50)
def root(th):return pole(phase(th)[0])
def forces():
 print('actual section H,AL',HX,HR,AL,'pole and parked p',root(0))
 for th in (-3.,0.,.375,7.5,10.,14.,16.,20.,30.,44.):
  cx,x,r,nx,p=root(th);an=phase(th)[0];cut=rootcut(0.,0.,1.16);ok=cut<=p<=0 and nx>0
  print('ring°, leaf°, rim center X, pole in parked coords, valid finite meridian, delta cx/next step',th,degrees(an),cx,p,ok,root(th+IDX)[0]-cx)
 print('park/terminal flat',HOME,HOME+TR)
 L=6.37-1.62;lo=35.404*.9;hi=35.404*1.1
 free=L+35.404/kw;solid=(3.5+2)*.8;ratio=3.5/.8
 for f in (lo,35.404,hi,49.368):
  taus=8*f*3.5/(pi*.80**3)*((4*ratio-1)/(4*ratio-4)+.615/ratio)
  print('conditional spring F, k, L, solid gap, Wahl stress MPa',f,kw,free-f/kw,free-f/kw-solid,taus)
 print('preload at forward captive stop, force at rear stop',35.404-.40*kw,35.404+.22*kw)
 for th,ff in ((0,lo),(0,35.404),(0,hi)):
  ca=root(th)[3];sa=sqrt(1-ca**2);D=ca-MUS*sa;N=ff/D;rad=N*(sa+MUS*ca)
  x,r=root(th)[1:3];mt=(x-HX)*rad-(r-HR)*ff
  dz=3*.35*mt;ang=phase(th)[0];hornF=mt/(HORN*cos(ang));print('per shoe axial, normal bound, radial bound, leaf torque, horn force, all-three drum torque',ff,N,rad,mt,hornF,dz)
  # Crossbar nominal torsion about t due to force at the working pole. E is
  # machined in the parked frame; not the pivot H. Also report unequal split.
  e=hingept(HX+1.35,HR+2.7,0,ang,0)-O*X
  tc=(x-e[0])*rad-(r-e[1])*ff
  for share in (.5,1):
   print('bar branch, E, torque about E at branch, torsion+single shear MPa',share,sh(e),tc*share,2*abs(tc)*share/(pi*.22**3),hypot(ff,rad)*share/(pi*.22**2))
 # Limit individual last increments at physical detent, not by angular encoder.
 z=3.;thv=np.arange(-3,10+1e-6,IDX);dp=np.diff([root(th)[0] for th in thv]);print('max axial closing increment last physical range, nominal spring ΔN',max(dp),kw*max(dp))
 print('equal-stiffness three bands admissible pre-index span absent errors',hi-lo-kw*max(dp))
 # Find actual start of the certified work surface: a following flange can
 # enter from an unloaded precharged stop only if globally unblocked.
 try:
  q=brentq(lambda th:root(th)[0]-(-2.25+.40),0,14);print('pickup from extended button stop if on flank; th,flat coords,bounds',q,root(q),rootcut(0,0,1.16))
 except ValueError:pass
 for mu in (.03,.10,.18):
  F=35.404;ft=F*tan(FACE);L=6.65;e=2.85
  rr=ft*e/L;front=ft+rr;print('button one flank axial, transverse, rear/front guide reactions, possible drag',F,ft,rr,front,mu*(rr+front))
def reactions():
 RB=10.68;A=np.vstack((np.ones(3),np.array([(RB*U(a))[1:] for a in BAZ]).T))
 # Coordinates in axial plane through mean guide reaction. At home, R x F
 # from the disk key lateral reaction shifts the effective thrust line.
 for f in (35.404,75,113):
  for xg in (-19.03,-10.11,-8.69):
   u=U(BAZ[0]);t=U(BAZ[0]+90);xp=-4.31-2.5*cos(FACE);dt=2.5*sin(FACE)+(xp-xg)*tan(FACE);r=Rb*u+dt*t
   out=np.linalg.solve(A,np.r_[1.,r[1:]])*f
   print('single flank Fx, guide reaction plane, thrust per captured roller, journal equiv shear/bending MPa worst',f,xg,out,max(abs(out))/(pi*.73**2),4*max(abs(out))*(10.68-9.49)/(pi*.73**3))
  print('three home stations pure symmetric axial and worst balanced Fx couple / key torque Nmm single-flank',f,f,10.3*f*tan(FACE))
 print('disk groove lateral float (zero flex), max tilt from ±.065 independent axial gaps, R12.42 face axial skew',.065,4*.065/(3*RB),12.42*4*.065/(3*RB))
 idx=sin(pi/8)/(1-sin(pi/8))
 for M in (200,500,750,1100):
  for mu in (.05,.12,.20):
   gamma=atan(.30/(2*1.50));eta=tan(gamma)/tan(gamma+atan(mu/cos(radians(20))))
   tw=M/(120*eta);gm=tw*idx*.5/(.72*.80)
   print('drum T Nmm, μ, worm efficiency, worm axial N, worm torque, conditional gearhead torque',M,mu,eta,M/18,tw,gm)
 # A concentrated resisting 3D load can require far MORE than total Fx times
 # cam slope if large +/- internal reactions have to slide.
 hp=TR*pi/(2*radians(51));print('max disk cam slope/pressure angle; rise torque only at 40/75/113N',hp,degrees(atan(hp/DR)),[hp*x for x in (40,75,113)])
 print('speed: gearhead rev per full 105 degrees, minutes at 100 rpm',105/IDX*2,105/IDX*2/100)
def curves():
 o={}
 for key,azs,rad,roller in [('disk',BAZ,DR,1.045),('leaf',tuple(a+degrees(atan2(4.68,16.42)) for a in AZ),16.675,.86)]:
  v=[]
  for th in np.linspace(-3.75,106.5,442):
   a,h=phase(th);x=(-19.03+h) if key=='disk' else -16.8+horn(a)[0]-HX;v.append((-rad*radians(th),x))
  ar=np.array(v);dd=np.gradient(ar,axis=0);nn=np.c_[-dd[:,1],dd[:,0]]/np.linalg.norm(dd,axis=1)[:,None]
  o[key]=dict(stations=azs,radius=rad,coords='unwrapped arc in ring, local X',paths=[x.round(6).tolist() for x in (ar,ar-roller*nn,ar+roller*nn)])
  print('groove',key,'x edges',min((ar-roller*nn)[:,1].min(),(ar+roller*nn)[:,1].min()),max((ar-roller*nn)[:,1].max(),(ar+roller*nn)[:,1].max()),'repeat arc between ends minus two cap radii',rad*radians(120-110.25)-2*roller)
 (D/'drum-grooves64.json').write_text(json.dumps(o,separators=(',',':'))+'\n')
def bores():
 b={}
 for a in BAZ:
  # These are NEGATIVE stock, machined from the parent flange/socket and
  # root webs, not positive volume to add to a corridor. Rolling rim only
  # where parent stock remains; certify the jaw zone separately.
  b[str(a)]=dict(center_yz=sh((10.3*U(a))[1:]),parent_bore=[[-7.,-1.54,2.61],[-1.54,-.45,1.65],[-.45,6.66,2.59]],guide=[[-1.53,-.86,1.17],[1.84,7.1,.87]],guide_stem_R=.80,rear_cap_through_R=.87,ball_R=2.5,mid_button_X=-4.31,travel=[-.4,.22],front_stop=.68,rear_stop=1.84)
 (D/'drum-cartridges64.json').write_text(json.dumps(b,separators=(',',':'))+'\n')
 print('ball port radial annulus at original flat x=-4.75, extended/mid/rear',*[2.61-sqrt(6.25-(-4.75-c)**2) for c in (-4.71,-4.31,-4.09)])
 print('seated plane face-to-button, belly-to-wedge, nearest jaw axis to aperture at work',(-4.31-2.50)-HOME,(-2.25-2.5)-(-5),sqrt(R**2+10.3**2-2*R*10.3*cos(pi/3))-2.61)
if __name__=='__main__':forces();reactions();curves();bores()
