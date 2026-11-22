from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('shell-tilt70.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def enc2(S):
 # Upper of enclosing ball direct support; distance between two actual
 # vertices in cell/foot stock gives independent rotation-invariant lower.
 f=lambda c:max(far(q,c) for q in S)
 x=minimize(f,[0,0,.5],method='Powell',options={'maxiter':80,'xtol':.003,'ftol':1e-6});r=minimize(f,x.x,method='Nelder-Mead');return r.x,2*f(r.x)
def run():
 f=chassis()+pads();e=json.loads((D/'shell-elec70.json').read_text());t=tailbound()
 h=head();gt=groups(t);fh=groups(h+e)
 print('pitch, lip and table world',P,O,-23.22)
 f1=f+drum()+state(0)+move(tail(),-P)+joint()[1];print('straight stow mech only / also electronics upper OD',enc2(f1),enc2(f1+e))
 print('stroke union, straight and all parts including electronic reserves OD upper',enc2(h+e+t))
 cell=next(q for q in e if q[0]=='cell bulk')
 for q in [cell]:
  targets=subset(f,('foot (','worm 32T spur'));v=np.array(q[1]);rows=[]
  for k in targets:
   w=polyin(k);dd=np.linalg.norm(v[:,None]-w[None,:],axis=2);i,j=np.unravel_index(dd.argmax(),dd.shape);rows.append((dd[i,j],k[0],v[i],w[j]))
  print('true reserved corner distance, pair witnesses',max(rows,key=lambda q:q[0]),'actual foot alone',max((q for q in rows if q[1].startswith('foot')),key=lambda q:q[0]))
 print('own static non-foot min floor',min((ext(q,np.eye(3))[0][2],q[0]) for q in h+e+t if not q[0].startswith('foot')))
 # Continuous independent neighboring yaws around their chain joint. Test
 # head to powered head only, not head to its mated flange. Express both
 # in passive-tail datum; add chord bound per independent joint.
 grid=np.arange(-15,15.001,.25);ea=extlist(fh);ar=max(far(q,H) for q in fh);gh=2*ar*sin(radians(.0625))
 # All heads individually articulated against collinear tail frames.
 # Since head costs are independent, minimum over every pair via their
 # direction-support interval union per piece per yaw; conservative.
 blocks=[]
 for side in (0,1):
  l=[]
  for a in grid:l.append(extlist(move(yaw(fh,a),P*side)))
  m=np.array(l);blocks.append(np.stack((m[:,:,0].min(0)-gh,m[:,:,1].max(0)+gh),axis=1))
 z=pairs(fh,fh,*blocks);print('combined yaw hulls, neighbor gap lower; debit per head',z,gh)
 # With mutually independent full yaw a single aggregate hull may lose
 # separations along different axes. Sample all pairs iff inconclusive.
 if z[0]<0:
  def split(S,ls):
   ar=np.array([extlist(move(yaw(S,a),ls)) for a in grid]);return np.stack((ar[:,:,0].min(0)-gh,ar[:,:,1].max(0)+gh),axis=1)
  # exact world-X cuts on the two facing corners; optimize separations
  # by interval blocking rather than a common distance to coarse hull.
  ah=[extlist(yaw(fh,float(a))) for a in np.arange(-15,16,3)];bh=[extlist(move(yaw(fh,float(a)),P)) for a in np.arange(-15,16,3)]
  q=min((pairs(fh,fh,i,j),ia,ib) for ia,i in enumerate(ah) for ib,j in enumerate(bh));print('3deg independent grid raw, net',q,q[0][0]-4*ar*sin(radians(.75)))
 print('yawless body/foot separations do not prove tail clearance against own joint; limits checked separately')
 # Selected inherently hyperplanar sideway gap. Negative world projection
 # at skew az=30 is not material overlap; use true station tangent.
 for a in AZ:
  q=next(q for q in f if q[0]==f'slider guide cheek {(a,1,-6.64)}')
  u=U(a+90)[None];val=[]
  for an in (phase(-3.29421)[0],A0,0.):
   ss=next(q for q in sliders(a,an) if q[0].startswith('axial transfer beam'));val.append((ext(q,u)[0]-ext(ss,u)[1])[0])
  print('beam vs positive guide tangent true fixed-coordinate flank separation',a,min(val),'identical negative guide')
 # Follower face and axial/radial tolerances, more than allowable parking
 # differential. Conservative axial dry skew bound for triangle supports.
 print('park stub ID radial play, total across two supports; allowed profile difference',.54-.52,2*(.54-.52),.020)
 print('single positive 0.030 mm OD stop position error -> angle/normal toe error at meridian',degrees(asin(.030/3.8)),abs(HX)*.030/3.8)
 print('For spring/cup envelope see separate central-space test. Release under external load not certified.')
if __name__=='__main__':run()
