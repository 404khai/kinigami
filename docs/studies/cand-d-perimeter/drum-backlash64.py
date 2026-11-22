from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('drum-load64.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def run():
 dd=.065+.041650662;dl=.06+.046331553+.06
 sa=sin(phase(0)[0]);ar=[asin(sa+i*dl/HORN) for i in [-1,1]]
 print('reversible flank and fork free-motion transfer, leaf deg, possible true spring span under ideal contact',list(map(degrees,ar)),[(pole(a)[0]-C+O)*kw for a in ar])
 print('full machined disk axial gap/tilt and edge excursion',2*dd,4*dd/(3*DR),RD*4*dd/(3*DR))
 # Actual spring front-guide spacing: distance between bush midplanes, load
 # applied at ball centre. Taking shorter span earlier is a sensitivity only.
 x1=(-1.53-.86)/2;x2=(6.37+7.10)/2;ft=35.404*tan(FACE);rear=ft*(x1+4.31)/(x2-x1);front=ft+rear;print('bush midpoint/span/overhang and clean one-flank side reactions, μ.03 drag',x1,x2-x1,x1+4.31,rear,front,.03*(rear+front))
 # Worst of uniform single-direction shear and torsion examples, not a
 # multibody load prediction. Most favourable split still fails.
 for N in (410,534):
  q=phase(0)[0];_,x,r,_,_=pole(q);E=hingept(HX+1.35,HR+2.7,0,q,0)-O*X;T=abs((x-E[0])*N*sqrt(1-.48**2)-(r-E[1])*N*.48);s=500.
  print('illustrative gross minimum crossbar radius at shear limit 500MPa no safety factor, equal branches torsion and direct shear',N,(T/(pi*s))**(1/3),sqrt(N/(2*pi*s)))
 # Ideal output forms conditionally require distinct torque outcomes at
 # preload, button picking-up and service ejection, not one Q85 number.
 for th in (-3,0,7.5,10,12,13.35):
  ang=phase(th)[0];cx,x,r,nx,p0=pole(ang);F=35.404-kw*(cx+2.25)
  if F<0:continue
  nr=sqrt(1-nx*nx);N=F/(nx-.23*nr)
  tq=N*((x-HX)*(nr+.23*nx)-(r-HR)*(nx-.23*nr))
  deriv=degrees((phase(th+.0001)[0]-ang))/.0001
  print('conditional draw from true extended stop; ring°, F spring, Nnormal, drum torque 3 loaded',th,F,N,3*tq*deriv)
 print('symbolic roof sweep and yaw, no driven separation from motor commands')
if __name__=='__main__':run()
