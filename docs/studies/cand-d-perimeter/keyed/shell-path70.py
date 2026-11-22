from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('shell-contact70.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def run():
 f=chassis()+pads()
 # Preserve the actual collisions found before offsetting these two roots.
 aa=rod('old park bearing tie',S0+2.84*UA+.67*VA,pos(48,-6.6,15.4),.69);bb=rod('old pin guide tie',(W,WR-1.88,12.29),(W+1.72,WR-1.99,12.31),.39)
 print('rejected root variants, actual spindle and pin balls',cp([aa],subset(f,('park output spindle',)),1),cp([bb],subset(dog(16.18),('dog polished pin',)),1))
 fs=next(q for q in f if q[0]=='park cam bearing tie');ft=next(q for q in f if q[0]=='pin guide outboard tie')
 # For pin and spindle proof use analytic distance to each infinite axis:
 # bounded rods at the new clock remain outside even the extended axis.
 for b,axis,p,r in [(fs,UA,S0,.51),(ft,ZA,np.array([W,WR-1.31,12]),.215)]:
  ends=np.array(b[1])-p;xy=ends-((ends@axis)[:,None]*axis);u=xy[1]-xy[0];t=np.clip(-u@xy[0]/(u@u),0,1);print('fixed tie clearance to unbounded rotating/sliding working cylinder',b[0],np.linalg.norm(xy[0]+t*u)-r-b[2])
 for n,starts in [('park cam bearing tie',('park output spindle','park cam outboard bearing','stationary case','cam bearing to foot tie')),('draw limit frame return',('aft cantilever','draw limit rear strut')),('park limit frame return',('aft cantilever','upper yaw motor rail','park limit rear strut')),('motor rear saddle spine',('motor rear mount','clamp motor')),('pin frame bearing return',('pin guide axial return','worm independent bearing'))]:
  q=next(s for s in f if s[0]==n);print(n,'union / conflict inscribed balls, radius and neighbor',[(round(float(v[0]),5),v[2],v[3]) for v in cp([q],subset(f,starts),20) if v[0]>.04])
 unrelated=subset(f,('park geared','park motor saddle','park saddle knuckle','park output spindle','park cam bearing tie','cam bearing to foot','pin guide outboard','pin guide axial','pin frame bearing','worm thrust','clamp motor','motor rear','worm outboard'))
 for z in (16.18,16.29,17.16,18.15):
  print('true dog yoke, pin and roller vs unrelated stock, not cut star/track; z',z,cp(dog(z),unrelated,5))
 # Opposed straight pin shear faces only work if dog remains fully inserted.
 print('A bearing outer ring alone does not establish tie strength, main-drive unloading, yoke antirotation, or power-off retention.')
if __name__=='__main__':run()
