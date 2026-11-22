from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('shell-tilt70.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def run():
 e=json.loads((D/'shell-elec70.json').read_text());fixed=groups(chassis()+pads()+drum()+e);hh=groups(fixed+state(105));F=np.column_stack((X,U(30),U(120)));r=max(far(q,H) for q in hh);ax=np.array([(O-4.31),0.,0.])+5.15*U(30)
 # On the fixed terminal station translate the mated body aft-to-front by
 # 7.88 from Take72's separate locked reference -6.45. Then roll about
 # the carried t-axis: probe screening, not prescribed release physics.
 def tr(S,deg):
  a=radians(deg);R=F@np.array([[cos(a),-sin(a),0],[sin(a),cos(a),0],[0,0,1]])@F.T
  return [sol(q[0],(np.array(q[1])-ax)@R.T+ax+7.88*X,q[2],None if q[3] is None else R@np.array(q[3])) for q in S]
 # Project each true 3D solid to Z for floor. Conservative X separation to
 # powered body: negative isn't collision. Only outer body, no seat proof.
 out=[];sweep_deg=.5;yy=np.arange(-15,15.001,.5)
 for z in np.arange(0,4.001,sweep_deg):
  vals=[]
  for y in yy:
   # Exact rotation of support directions, no need to transform thousands
   # of vertices per angle; retain gauges in original unit frame.
   al=radians(y);Y=np.array([[cos(al),-sin(al),0],[sin(al),cos(al),0],[0,0,1]]);ph=radians(z);R=F@np.array([[cos(ph),-sin(ph),0],[sin(ph),cos(ph),0],[0,0,1]])@F.T
   mat=R@Y;d=np.array([[1.,0.,0.],[0.,0.,1.]])@mat;o=R@(H-Y@H+P*X-ax)+ax+7.88*X;lo=np.min([ext(q,d)[0] for q in hh],axis=0)+o[[0,2]]
   vals.append((lo[0],lo[1]))
  out.append((z,np.min(vals,0)))
 r2=max(far(q,H) for q in hh)+np.linalg.norm(H+P*X-ax);dx=2*r*sin(radians(.125))+2*r2*sin(radians(.125));bound=np.min([q[1] for q in out],axis=0)-dx;xx=max(ext(q,X[None])[1][0] for q in hh)
 print('separate Take72 carrier probe p=1.43, phi 0..4, independent yaw ±15, lower fixed-X separation of adjacent POWER HEAD (not tail interface), floor all parts incl midpoint debits',bound[0]-xx,bound[1]+23.22,dx)
 lower=1e3
 for y in yy:
  for q in move(yaw(hh,y),P):
   lo,hi=ext(q,np.array([X,U(30)]));delta=2*far(q,H+P*X)*sin(radians(.125));dx=lo[0]-ax[0]-delta;rd=hi[1]-ax@U(30)+delta
   lower=min(lower,.5*(min(dx,cos(radians(4))*dx)-max(0,sin(radians(4))*rd)))
 print('all named adjacent powered solids: lower d(world Z)/dphi from Rodrigues, mm/rad, over all independent yaw and phi; phi=0 exact floor',lower,min((ext(q,np.eye(3))[0][2]+23.22,q[0]) for q in hh))
 for deg in (0,.5,2,4):
  vals=[]
  for yy in np.arange(-15,15.1,.5):
   s=tr(move(yaw(pads(),yy),P),deg)
   vals.append(min((ext(q,np.eye(3))[0][2]+23.22,q[0]) for q in s))
  print('actual lowest foot+rail vs floor at roll for all sampled yaws',deg,min(vals),max(vals))
 print('terminal 4deg core center local',F.T@(np.array(tr([sol('C',[C*X])],4)[0][1][0])-O*X))
if __name__=='__main__':run()
