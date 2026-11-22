from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('quill-audit67.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
MU=.23;STEP=360/16/130
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
  print('ring torque; worm axial N; drive worm T; required 2:1 gearhead T (ηspur=.8); conservative dog force if FULL drive worm T at parked plate',tq,F,Tw,Tw/1.6,Tw/3.56)
 hp=TR*pi/(2*radians(55));print('pure disk rise max slope, pressure angle, torque for 40/75/113 N',hp,degrees(atan(hp/D0)),[hp*f for f in (40,75,113)])
 # Jam load not an installed preload. Conservative pin load for 23.96*2 gearhead/
 # worm locked input, irrespective of backdrive efficiency.
 Tw=23.96*2;Fb=Tw/3.56;print('full drive-pin conservative jam: bolt load, shear, edge bearing',Fb,Fb/(pi*.44**2),Fb/(.88*1.13))
 print('bolt hole R.50 less pin .44 nominal ±worm angular backlash and ring angle',degrees(2*asin(.060/(2*3.56))),degrees(2*asin(.060/(2*3.56)))/130)
 print('16-hole circumferential ligament / radial outer ligament',2*3.56*sin(pi/16)-1.00,4.53-3.56-.50)
 print('0615 N 003 S cold stall both: at 22C R16.2 ohm, at 10C copper coeff .00393/K plus provisional -10% winding/brush tolerance',2*3/(16.2*(1-.00393*12)*.9),'A. Approximate both gearmotors 2*(2g + ca.4g), nominal mass; not a toleranced lower.')
 rs=.01724*888*2*pi*.00167/(pi*.04**2);ir=3/(.9*rs*(1-.00393*12));area=pi*(.00093**2);Fk=4*pi*1e-7/2*(888*ir/.00199)**2*area
 print('trial coil 12x74 turns, .08 bare/.09 OD Cu, mean r1.67, R at ~20C, cold high current, ideal simple airgap 1.99mm pull N',rs,ir,Fk)
 sk=79000*.16**4/(8*1.66**3*10);print('spring ten active turns d.16 D1.66; force at .22mm installed compression and .22+1.99mm retracted',sk*.22,sk*2.21)
 print('simultaneous 3V nominal bus (2 cold-stall + coil cold + provisional .13 logic/instrument + .15 transients), 85% efficiency', (2*3/(16.2*(1-.00393*12)*.9)+ir+.13+.15)/.85, 'A; not an as-built peak')
 print('min 3V x 2A all-in =',3*2,'W (entire unit at cell, 10..45C). Illustrative branch HARD current limits, not verified: coupler .90A, yaw .42A, parking coil .30A, logic/radio/sensors .13A, contingency .15A.')
 print('illustrative simultaneous peak at cell incl all running, 5% high-side scatter',1.05*(.90+.42+.30+.13+.15),'A / 6 W. If drivers assumed to regulate motor current rather than battery-side branch current, budget invalid. Actual worst unbounded until min cold winding resistance, shunt/loop response, converters, pack impedance, armature pull-in and all stall/start currents verified.')
 print('mass screen required equivalent S at 74.323g vs trial 28',26.8006*74.323/70,'N, holds only for mass-proportional loads and same 70g geometry/moment arms; include actual larger joint torques instead.')
if __name__=='__main__':run()
