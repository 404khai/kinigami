from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('quill-contact67.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def run():
 # Assembly: a disk with already installed rollers translated in +X by
 # 9.9mm from home crosses the front uncut end wall on straight insertion.
 diskend=wring('uncut disk front shoulder',O-9.57,O-9.10,9.93,12.98,48,True)
 rolls=move(subset(disk(),('disk roller',)),9.70)
 print('inserting preassembled disk/post/roller through front; inscribed volume contact',cp(rolls,diskend,2))
 print('disk lip R12.42 passes nominal fixed bore, but ID 9.78 < assembled roller outer station R11.49. Need install loose axle from inside or close drum around it, not credit a seated CAD stack.')
 e=json.loads((D/'quill-elec67.json').read_text());f=chassis()+pads()
 bolt=subset(f,('16 hole',))[0];path=sweep([bolt],9*np.array([0,0,1.]));print('remove bolt plate +Z 9mm vs unrelated outer parts',cp(path,subset(f,('clamp motor','coil bracket','motor rear','foot tie','aft cantilever','outer axial','way anchor','yaw motor','ring phase'))+e,2))
 # Return wall and motor pickup checks.
 for an in (A0,0.):
  px,rp,rd=link(an);print('clevis pin access: local x/r; tangential tool cylinder ±t beyond bosses must be checked after removing outboard bearing caps',px,rp)
 print('shaft/park plate key W+.66..1.24, width .60, height 1.55; through-bush radial .46 and pin .44. Positive drive remains meshed while spring pushes bolt into the straight section; tip-only/land-on-plate is not accepted.')
 # Profile tolerance admitted by the actual three bores if unloaded float
 # rotates disk to worst signed roller flank. n_i axial displacement is an
 # affine field, so extrema on rim use barycenter + edge interpolation.
 g=.056+.02020;ns=np.array([D0*U(a)[1:] for a in BAZ]);M=np.c_[np.ones(3),ns];cases=[]
 for signs in product((-1,1),repeat=3):
  q=np.linalg.solve(M,g*np.array(signs));cases.append((q[0]-RD*np.linalg.norm(q[1:]),signs,q.tolist()))
 print('worst disk terminal min rim X with nominal groove slack alone',1.40+min(cases)[0],min(cases),'target +1.35, independent preload/stop needed')
if __name__=='__main__':run()
