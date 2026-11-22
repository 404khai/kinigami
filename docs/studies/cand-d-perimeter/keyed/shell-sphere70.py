from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('shell-audit70.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def solve(S):
 c=np.array([-1.5,.42,-.45]);near=[q for q in S if far(q,c)>28.20]
 F=lambda x:np.array([far(q,x[:3]) for q in near])
 r=minimize(lambda x:x[3],np.r_[c,31.],method='SLSQP',constraints=[dict(type='ineq',fun=lambda x:x[3]-F(x))],options={'ftol':1e-11,'maxiter':250})
 c=r.x[:3];return sh(c),2*max(far(q,c) for q in S),sorted([(far(q,c),q[0]) for q in S],reverse=True)[:4]
def run():
 e=json.loads((D/'shell-elec70.json').read_text());t=tailbound();h=head()+e
 for label,z in [('stow',chassis()+pads()+drum()+state(0)+t+e),('swept straight',h+t),('swept with own yaw increments .5 incl sag',h+sum(([sol(q[0],q[1],q[2]+2*far(q,H)*sin(radians(.125)),q[3]) if q[3] is None else sol(q[0],q[1],q[2]+2*far(q,H)*sin(radians(.125))) for q in yaw(t,a)] for a in np.arange(-15,15.01,.5)),[]))]:
  print(label,solve(z))
if __name__=='__main__':run()
