from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('drum-install64.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def run():
 f=fixture();st=[q for q in f if 'steel stop' in q[0]]
 for q in st:
  lim=(-3.8,-3.0) if 'draw' in q[0] else (105.,106.5)
  def dep(th):return ball(q,enddog(th))[3]
  print('finite stop first material contact angle, within actual capped cut',q[0],brentq(dep,*lim),lim)
 # Real guided roller/tangent flank clearance before form error or assembly flex.
 for rr,r in ((1.045,.98),(.86,.80)):
  B=.041651 if r==.98 else .046332;print('dwell full backlash for sampled cutter mm (max)',2*(rr+B-r))
 print('disk radial home front/rear clearance',14.5+.28*HOME-RD,14.5+.28*(HOME-1.6)-(RD-.55))
 print('parked flush analytic patch, centred work radial margin per Take61, 0.10 offset result',12.494126-RD,12.494126-RD-.10)
 # Zero-credit for a power-off jam in the handoff. At beta=90 the sector
 # poses have no intersection if this angular Lipschitz upper bound is negative.
 from scipy.optimize import brentq as BQ
 d=hypot(3.58,2.81);v=lambda q:np.array([cos(radians(q)),sin(radians(q))])
 for q in (-3,0,3):
  # Distance to the circle cutter centred at the closest dwell scallop is
  # not sufficient everywhere; solve upper material depth over all sector
  # sample points, subtract sampling error in BOTH polar dimensions.
  rr=np.linspace(0,2.03,80);angs=np.linspace(-51,51,205);a,r=np.meshgrid(angs-90,rr);w=np.c_[d+r.ravel()*np.cos(np.radians(a.ravel())),r.ravel()*np.sin(np.radians(a.ravel()))]
  co=cos(radians(q));si=sin(radians(q));w=w@np.array([[co,-si],[si,co]]);dep=np.minimum(4.22-np.linalg.norm(w,axis=1),np.linalg.norm(w,axis=1)-1.02)
  for j in range(8):
   v0=v(j*45);v1=v(j*45+22.5);dep=np.minimum(dep,np.linalg.norm(w-d*v0,axis=1)-2.09);dep=np.minimum(dep,np.linalg.norm(w-np.maximum(w@v1,d-d*sin(pi/8))[:,None]*v1,axis=1)-.42)
  err=2.03/158+2*2.03*sin(radians(.125));print('beta=90, wheel°',q,'sector/material depth upper incl Lipschitz; pin-to-OD',max(dep)+err,hypot(d,d*sin(pi/8))-.37-4.22)
if __name__=='__main__':run()
