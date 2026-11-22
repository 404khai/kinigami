from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('drum-check64.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def compact(s):
 # Whole passive mechanism as a conservative convex hull of all stock
 # inflated by largest local rounding. Used only for remote cross-set gap.
 p=np.unique(np.vstack([u[1] for u in s]),axis=0);return sol('whole passive stock',p[ConvexHull(p).vertices],max(u[2] for u in s))
def run():
 e=json.loads((D/'drum-model64.json').read_text())['electronics'];hd=efgroup(sweep())+e;t=shift(shorttail(),-P)
 remote=[compact(t)];rt=max(far(s,H) for s in remote);rh=max(far(s,H) for s in hd)
 ed=[extlist(boxesweep(shift(rotate(hd,a),P),TR*X)) for a in range(-15,16)];rows=[]
 for a in range(-15,16):
  ta=rotate(remote,a);ee=extlist(ta)
  for b in range(-15,16):
   rows.append((pairs(ta,hd,ee,ed[b+15])[0],a,b))
 print('own passive vs adjacent powered, independent ±15°×±15° and disk held..following, raw and net',min(rows),min(rows)[0]-.20-2*(rt+rh)*sin(radians(.25)))
 # Mated passive (axes aligned) versus the drive. Contacting face/leaf
 # exempt here only, as this test isolates unrelated mechanism interference.
 aux=[s for s in hd if not s[0].startswith(('fixed flared wall','cone patch','fixed heel roof','bearing outer reserve','thin cheek liner','65deg drafted seat','solid advancing disk'))]
 mt=shorttail();print('aligned passive vs swept auxiliary, held or following',pairs(aux,boxesweep(mt,TR*X)))
 for th in (0,44,76,105):
  an,h=phase(th);q=fixture()+state(th);support=[s for s in q if s[0].startswith(('outboard ear drive horn','leaf horn roller','leaf link fork root','fixed lip wall mount','bearing backing bridge'))]
  print('aligned passive vs rods/horns/mount, index nominal and with following',th,pairs(support,mt),pairs(support,shift(mt,h)))
 # Flat sweeps the seated flange if a following motion is not realized;
 # present a point within actual full-core material far from ALL button bores.
 # Finite disk analytic X, taper and filled central flange cross-section.
 xl=brentq(lambda a:HOME+phase(a)[1]-(-2.25-2.50),48,99)
 print('held tail: first central disk/flat X equality ring deg',xl)
 th=70;x=HOME+phase(th)[1]-.5;ray=min(x-(HOME+phase(th)[1]-1.6),(HOME+phase(th)[1])-x,x+4.75,.25-x)
 print('held-tail all-metal central ball, theta, radius, world xyz',th,ray,(O+x,0,0))
 # Optional torque/pressure and compliance conditional on REAL stock.
 for Fr in (81.28,107.69,194.17):
  N=Fr*sqrt(1+(TR*pi/(2*radians(51))/DR)**2)
  print('isolated roller worst-rise normal; line-contact pressure MPa if E*=115 GPa, full 1.54 length',Fr,N,sqrt(115000*N/(pi*.98*1.54)))
 # Sidewalls and block, not fixed angular registration.
 print('metal stop angular clearance to datum, deg: draw stop vs theta -3, park stop vs theta 105',(8.3-3)-degrees(atan(.45/12.42)+atan(.58/12.20)),(60.15-55)-degrees(atan(.45/12.42)+atan(.58/12.20)))
 print('draw floating slope possible ideal disk end-wall normal thickness <.18; pad overhang at terminal',(-19.71+TR)-(-10.11))
from scipy.optimize import brentq
if __name__=='__main__':run()
