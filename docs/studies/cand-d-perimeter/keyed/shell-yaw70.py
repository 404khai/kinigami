from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('shell-sphere70.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def poly(q):
 n,v,r,d=q;v=np.array(v)
 if d is None or r==0:return v,r
 d=np.array(d);a=np.eye(3)[np.argmin(abs(d))];a=np.cross(d,a);a/=np.linalg.norm(a);b=np.cross(d,a);u=np.array([a*cos(k*pi/48)+b*sin(k*pi/48) for k in range(96)])
 return (v[:,None]+r/cos(pi/96)*u).reshape(-1,3),0
def run():
 h=head()+json.loads((D/'shell-elec70.json').read_text());c=np.array([-1.48,.52,-.38]);ss=[q for q in h if far(q,c)>28.70];pt=tailbound();v=[];rr=[];names=[]
 for q in pt:
  u,r=poly(q);v.extend(u);rr.extend([r]*len(u));names.extend([q[0]]*len(u))
 v=np.array(v)-H;r=np.array(rr);rho=np.hypot(v[:,0],v[:,1]);ang=np.arctan2(v[:,1],v[:,0])
 def yf(c):
  dx=H-c;delta=np.arctan2(dx[1],dx[0])-ang;delta=(delta+pi)%(2*pi)-pi;gap=np.maximum(0,abs(delta)-radians(15))
  return np.sqrt((v[:,2]+dx[2])**2+rho**2+dx[:2]@dx[:2]+2*rho*np.linalg.norm(dx[:2])*np.cos(gap))+r
 L=lambda c:np.r_[[far(q,c) for q in ss],yf(c).max()]
 R=minimize(lambda x:x[3],np.r_[c,30.1],method='SLSQP',constraints=[dict(type='ineq',fun=lambda x:x[3]-L(x[:3]))],options={'ftol':1e-11});cc=R.x[:3];f=yf(cc);print('one sphere, entire continuous yaw -15..+15 & full stroke, explicit reevaluated containment diameter',2*max(max(far(q,cc) for q in h),f.max()),sh(cc),names[np.argmax(f)])
if __name__=='__main__':run()
