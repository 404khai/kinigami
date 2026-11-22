from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('shell-audit70.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
MU=.23;STEP=360/12/130
def pole(an):
 n=np.array([-FR,1.])/hypot(1,FR);c=cos(an);s=sin(an);nx,nr=np.array([[c,-s],[s,c]])@n
 delta=(B+FR*HX-HR)/hypot(1,FR)
 cx=HX+(nr*(HR-R)+delta-2.5)/nx;x=cx+2.5*nx;r=R+2.5*nr
 return cx,x,r,nx,HX+c*(x-HX)+s*(r-HR)
def run():
 kw=79000*.70**4/(8*3.50**3*4);l0=4.85+28/kw
 print('qx=.60 mechanics pole:',pole(A0),'central link P and radial output D range',link(A0),link(0.))
 for F in (25.2,28,30.8):
  l=l0-F/kw;Cw=3.50/.70;stress=8*F*3.50/(pi*.70**3)*((4*Cw-1)/(4*Cw-4)+.615/Cw)
  print('spring F, k, L, reserve to solid, conditional Wahl stress MPa',F,kw,l,l-6*.70,stress)
 print('extension and back stops F, reachable range',28-.38*kw,28+.24*kw)
 # Actual spring scatter/guide effects are not replaced by this travel law.
 st=np.arange(-3.,10.-STEP,STEP);dw=max(pole(phase(q+STEP)[0])[0]-pole(phase(q)[0])[0] for q in st)
 print('one dog pitch ring degrees, ideal takeup mm and ΔS, nonzero final draw slope',STEP,dw,kw*dw)
 for a in (0,10,12,14,16):
  an=phase(a)[0];cx,x,r,n,p=pole(an);qt=sqrt(1-n*n);fs=28-kw*(cx+2.25);N=fs/(n-MU*qt);mt=(x-HX)*(qt+MU*n)*N-(r-HR)*fs
  slope=(phase(a+.0001)[0]-an)/radians(.0001);print('conditional closing from true extension stop: theta, S, cx, 3-pole ring torque (reject if out of stroke)',a,fs,cx,3*mt*slope)
 pp=brentq(lambda t:pole(phase(t)[0])[0]+2.25-.38,0,23)
 print('flank pickup theta from front-stop if moving tail follows, include finite p',pp,pole(phase(pp)[0]))
 # Jacobian of real P--D link: perpendicular moment leverage and pin stress.
 for N in (228.,):
  cx,x,r,n,p=pole(A0);nt=sqrt(1-n*n);v=np.array([x-HX,r-HR]);n2=np.array([n,nt]);t2=np.array([-nt,n]);cross=lambda u,v:u[0]*v[1]-u[1]*v[0]
  tq=N*(abs(cross(v,n2))+MU*abs(cross(v,t2)));px,rp,rd=link(A0);ld=np.array([SLX-px,rd-rp])/LINK;lever=abs(cross(np.array([px-HX,rp-HR]),ld));F=tq/lever
  print('one 228 N jaw + μ=.23: torque upper and effective link lever / force',tq,lever,F)
  print('P pin double-shear MPa, simple center load span 4.35 bending MPa, centre-pair bearing nominal MPa',F/(2*pi*.6**2),(F*4.35/4)/(pi*.6**3/4),F/(1.2*1.5))
 for N in (102.,):
  fx=N*cos(FACE);ft=N*sin(FACE);s0=BAZ[0];xp=-4.31-2.5*cos(FACE);r=10.3*U(s0)+(2.5*sin(FACE)+(xp-(5.23-O))*tan(FACE))*U(s0+90);A=np.vstack((np.ones(3),np.array([D0*U(b)[1:] for b in BAZ]).T));ff=fx*np.linalg.solve(A,np.r_[1.,r[1:]])
  print('one 102 N seat (clean) axial/tang, 3 bilateral rollers, key torque',fx,ft,ff,10.3*ft)
  print('with μ=.23 isolated worst axial / tangent (separate)',fx+.23*ft,ft+.23*fx)
 # Locked bolt contact and finite flank. Conservative grade-blind stresses.
 for tq in (200,500,1000,1500):
  F=tq/19.5;gamma=atan(.30/3);mu=.12;eta=tan(gamma)/tan(gamma+atan(mu/cos(radians(20))));Tw=tq/(130*eta)
  print('ring torque; worm axial N; drive worm T; required 2:1 gearhead T (ηspur=.8); conservative dog force if FULL drive worm T at parked plate',tq,F,Tw,Tw/1.6,Tw/1.31)
 hp=TR*pi/(2*radians(55));print('pure disk rise max slope, pressure angle, torque for 40/75/113 N',hp,degrees(atan(hp/D0)),[hp*f for f in (40,75,113)])
 # Jam load not an installed preload. Conservative pin load for 23.96*2 gearhead/
 # worm locked input, irrespective of backdrive efficiency.
 Tw=23.96*2;Fb=Tw/1.31;print('conservative jam Nm -> dog load, single shear, bore bearing, pin bending .2mm cantilever MPa',Tw/1000,Fb,Fb/(pi*.215**2),Fb/(.43*1.28),Fb*.2/(pi*.215**3/4))
 print('side load rubbing withdrawal, mu=.23; even lossless backdrive 500 Nmm /130 /1.31',.23*500/130/1.31,'N; do not infer unload by reversing a command.')
 per=3/(16.2*.9*(1-.00393*12));print('3 cold stalled 0615 3V + .13 logic/sensors + .15 transient, illustrative .85 converter',per, (3*per+.13+.15)/.85,'cell A at 3V; no thermal rating')
 print('0615 N 003 S at 22C: rated thermal current .142A (not .292A; that is 1.5V), rated torque .156Nmm, stall torque .221Nmm. At 3V, 16.2ohm copper stall loss',3**2/16.2,'W per winding, vs rated copper at 22C',.142**2*16.2,'W. No duty/thermal permission for release at stall.')
 print('2A continuous at 10..45C only; 6W at 3V. Hypothetical battery-side hard limits: clamp .90, yaw .42, parking .30, controls .13, transient .15 A, all +5%:',1.05*(.9+.42+.30+.13+.15),'A. 4A for 2-3ms prohibited for motor operation. Fault cutoff and voltage sag untested.')
if __name__=='__main__':run()
