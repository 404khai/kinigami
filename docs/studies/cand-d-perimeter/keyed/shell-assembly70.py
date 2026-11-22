from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('shell-contact70.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def run():
 # Assembly: a disk with already installed rollers translated in +X by
 # 9.9mm from home crosses the front uncut end wall on straight insertion.
 diskend=wring('uncut disk front shoulder',O-9.42,O-9.10,9.93,12.98,48,True)
 rolls=move(subset(disk(),('disk axle',)),9.77)
 print('inserting preassembled disk/post/roller through front; solid axle vs untouched front shoulder',cp(rolls,diskend,2))
 print('disk lip R12.42 passes nominal fixed bore, but ID 9.78 < assembled roller outer station R11.49. Need install loose axle from inside or close drum around it, not credit a seated CAD stack.')
 e=json.loads((D/'shell-elec70.json').read_text());f=chassis()+pads()
 bolt=subset(f,('12 hole',))[0];path=sweep([bolt],9*np.array([0,0,1.]));print('remove bolt plate +Z 9mm vs unrelated outer parts',cp(path,subset(f,('clamp motor','coil bracket','motor rear','foot tie','aft cantilever','outer axial','way anchor','yaw motor','ring phase'))+e,2))
 # Return wall and motor pickup checks.
 for an in (A0,0.):
  px,rp,rd=link(an);print('clevis pin access: local x/r; tangential tool cylinder ±t beyond bosses must be checked after removing outboard bearing caps',px,rp)
 # Profile tolerance admitted by the actual three bores if unloaded float
 # rotates disk to worst signed roller flank. n_i axial displacement is an
 # affine field, so extrema on rim use barycenter + edge interpolation.
 g=.056+.02020;ns=np.array([D0*U(a)[1:] for a in BAZ]);M=np.c_[np.ones(3),ns];cases=[]
 for signs in product((-1,1),repeat=3):
  q=np.linalg.solve(M,g*np.array(signs));cases.append((q[0]-RD*np.linalg.norm(q[1:]),signs,q.tolist()))
 z=TR+HOME;pmin=z+min(cases)[0];pmax=2*z-pmin;gap=B-RD+.05;rt=2.45
 nx=min(sqrt(1-(gap/rt)**2),1-pmax/rt);ang=acos(nx)+radians(.6);rear=rt-sqrt(rt**2-gap**2);w=cos(ang)-.23*sin(ang)
 print('all three roller flanks X offsets ±',g,'local plane low/high on R12.42 integral rim',pmin,pmax,'worst plane',min(cases))
 print('forward/in-bore branch rear-over-lip threshold, min nominal margin, max-rim force angle debit, signed axial ratio',rear,pmin-rear,degrees(ang),w)
 print('max allowed total unmodeled forward error before friction sign reversal at upper edge',rt*(1-cos(atan(1/.23)-radians(.6)))-pmax,'mm; elastic cocking, clearance in roller bearings, rotor tilt and mounted stack not specified')
if __name__=='__main__':run()
