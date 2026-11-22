from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('shell-tilt70.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def run():
 F=chassis()+pads();moving=curvesweep()
 targets=subset(F,('fixed wall heel','outer axial rail','aft cantilever','cross rail','cantilever radial step','foot','worm fore','worm bearing','park geared','clamp motor','yaw motor body'))
 A=subset(moving,('crosshead','radial crosshead','axial transfer','radial slide','centre clevis','slider link pin','face roller'))
 print('continuous expanded convex swept links vs outboard heels rails feet and motors',fine(A,targets))
 # Sliding web, X-pads, and cheeks: analytic support in the way frame
 # throughout even for loaded diagonal bearing contact. Only X travel .04
 # is counted here; rotation, galling, and fit remain open.
 minrd=100.;maxrd=-100.;a0=phase(-3.295)[0];angles=np.linspace(a0,0,161)
 for an in angles:
  rd=link(an)[2];minrd=min(minrd,rd);maxrd=max(maxrd,rd)
 de=4*radians(abs(degrees(a0))/320) # |rD'| < 2.89*(1+1.42/4.43) <4
 print('continuous pad registration; radial inner / outer margin, X face gap, useful transverse contact width',minrd-de-5.34-13.05,22.44-(maxrd+de+.94),.04,2.24-1.59)
 q=subset(sweep(disk(),TR*X),('disk key','disk post','seat backer','disk axle','disk roller'))
 print('translating post assembly vs quill, inner webs, flanking stationary pads and same outer stock',fine(q,subset(F,('fixed center quill','inner key web','key positive face'))+targets))
 print('carrier response and disk clearance to all other cut surfaces are NOT established by these subsets.')
if __name__=='__main__':run()
