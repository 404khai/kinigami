from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('shell-contact70.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
pitch=pi*.30;root=1.145;outer=1.80;pres=radians(20)
def signed(x,y,z,angle,oversize):
 # Positive is separated, negative means inside. All terms in mm.
 r=np.hypot(y-WR,x-W);a=np.arctan2(y-WR,x-W);dist=np.abs((z-pitch*(a-angle)/(2*pi)+pitch/2)%pitch-pitch/2)
 hw=pitch/4+(1.5-r)*tan(pres);return np.maximum.reduce((abs(z)-3.52-oversize,r-outer-oversize,np.minimum(r-root-oversize,dist-hw-oversize)))
def run():
 # Remove expanded hob sweep from annular blank. Prove one small ball
 # remains in a tooth and collides with a blocked worm at each load sign.
 # Full +/-16deg around pitch for small orbit points covers tool length;
 # near the opposite pole Y<0 and the radial separation is enormous.
 a=np.radians(np.arange(-16,16.001,.008));rv=.007
 debit=(2*19.81+2.5+1)*radians(.004)+2*rv
 for sign in (-1,1):
  be=None
  for rotat in np.arange(.01,.55,.01):
   rotat*=sign;t0=radians(rotat)
   for r in (19.27,19.44,19.60,19.70):
    for b in np.arange(-1.39,1.39,.021):
     z0=radians(b);xx=W+0*a;y=r*np.cos(z0+a);z=r*np.sin(z0+a);mn=min(signed(xx,y,z,-130*a,.016))
     if mn<=debit:continue
     z1=r*sin(z0+t0);y1=r*cos(z0+t0);sw=signed(W,y1,z1,0.,0.)
     if sw< -2*rv:
      be=rotat,r,b,mn,sw;break
    if be:break
   if be:break
  print('locked worm, sign, wheel delta deg to guaranteed overlap with R.007 ball, r/az, source excess/depth',sign,be)
 # All 12 dog detents modulo one-wheel-tooth cycle. Same certificate
 # on the retained wheel; permit ±3.20deg total dog/key angular float
 # and ±.015mm axial shoulder float in the fixed worm before contact.
 # Diameter play at the two guide ends is .032; extend worst tilt to
 # z=10.68 where straight parking hole and shank both exist. Add the
 # square journal's .008 nominal edge clearance at its .645 half-width.
 pin=.030+.016+.032*(11.00-10.68)/(12.70-11.00)
 sq=degrees(asin(.653/(sqrt(2)*.645))-pi/4)
 required=degrees(2*asin(pin/(2*1.31)))+sq
 assert required<3.20
 print('centered worm star/dog total nominal shaft-angle play one side deg, permitted computational debit',required,3.20,'radial bearing shift, elastic bending & failed seating NOT included')
 pts=[]
 for r in (19.26,19.44,19.60,19.70):
  for b in np.arange(-3.60,2.61,.024):
   l=radians(b)+a
   if min(signed(W+0*a,r*np.cos(l),r*np.sin(l),-130*a,.016))>debit:pts.append((r,radians(b)))
 pts=np.array(pts);rr=pts[:,0];b=pts[:,1]
 for sgn in (-1,1):
  ok=[]
  for i in range(12):
   phase0=radians(i*360/(12*130));res=None
   for d in np.arange(.10,.71,.01):
    l=b+phase0+sgn*radians(d)
    # Bound signed component gradient wrt pure axial drift and shaft angle;
    # a held pin does not change wheel angle while the test deflects it.
    val=signed(np.full(len(l),W),rr*np.cos(l),rr*np.sin(l),-130*phase0,0.)
    if min(val)<-(2*rv+.015+pitch*3.20/360):
     res=d;break
   ok.append(None if res is None else round(res,3))
  print('12 detents, sign, wheel deviation deg to safe ball intersection (nominal centered worm, axial/key/bolt float as listed)',sgn,ok)
 # Finite spur pair: 20deg involute, choose 16T and 32T pinion root
 # profiles suitably relieved. Pinion axial overlap and transverse contact
 # ratio are NOT torque/rating of a given catalog transmission.
 a20=radians(20);p=.20*pi*cos(a20);rp=1.60;rg=3.20;base=.20*pi;terms=[sqrt((x+.20)**2-(x*cos(a20))**2) for x in (rp,rg)];print('spur ratio, transverse contact ratio nominal',2,(sum(terms)-4.8*sin(a20))/p,'z overlap',1.54)
 print('kinematic hobbing: positive wheel turns -> -130 worm math angle at +Y (positive axial progression); larger R stock cut over one entire rotation. Backdrive torque 500 / 130 = 3.846 Nmm lossless reverse. Do not credit ordinary worm friction.')
if __name__=='__main__':run()
