from finish79 import *
def minimize_points(p,w0=None):
 # Center upper via SOCP-equivalent small SLSQP, add farthest physical
 # point every iteration. Lower via maximizing a simplex variance.
 p=np.asarray(p)
 ix=[0,int(np.argmax(np.linalg.norm(p-p[0],axis=1)))];ix.append(int(np.argmax(np.linalg.norm(p-p[ix[1]],axis=1))))
 for _ in range(40):
  a=p[ix];cen=np.mean(a,axis=0);y=a-cen;n=len(ix)
  mat=(y*y).sum(1)
  obj=lambda w:np.sum((w@y)**2)-w@mat
  r=minimize(obj,np.full(n,1/n),jac=lambda w:2*y@(w@y)-mat,method='SLSQP',bounds=[(0,1)]*n,constraints=[dict(type='eq',fun=lambda w:w.sum()-1,jac=lambda w:np.ones(n))],options={'ftol':1e-12})
  w=np.maximum(0,r.x);w/=w.sum();cc=w@a;i=int(np.argmax(np.linalg.norm(p-cc,axis=1)))
  if i in ix:break
  ix.append(i)
 return 2*sqrt(-obj(w)),w,cc,ix[:len(w)]
def rerun():
 r=regions();dw,v,vi,vo=covers();p=[];lab=[]
 def add(n,a):
  p.extend(a);lab.extend([n]*len(a))
 add('surviving cover exterior',[z for z in vo if zone(z)])
 for n in ('body','elec','front','coil'):
  for q in r[n]:
   if q[0].startswith(('foot (','cell bulk','protection board','controller board','yaw motor body','key pickup axle')):add(q[0],polyin(q))
 for a in (-15,0,15):
  for q in yaw(r['tail'],a):
   if q[0].startswith(('solid wing','integral lug','socket fork','yaw shaft')):add(q[0]+' yaw '+str(a),polyin(q))
 p=np.array(p);diam,w,c,ix=minimize_points(p)
 print('physical/required stock finite-support Ø lower; center',diam,c,[(lab[i],np.round(p[i],5).tolist(),round(wa,7)) for i,wa in zip(ix,w) if wa>.0001])
 # Optimize conservative stroke+continuous yaw upper as exact cylinder
 # supports about candidate centers. Give sphere inflation between sample yaw.
 flat=[a for k,g in r.items() if k!='tail' for a in g]+[sol('drive skin',vo)]
 # At yaw extremal radial points function max + head, possible extra
 # sampled arc error is bounded by chord sagitta, not full arc length:
 # sweep of each material point lies within sagitta of its chord.
 step=2.5;debit=max(far(q,H) for q in r['tail'])*(1-cos(radians(step/2)))
 tailset=[q for a in np.arange(-15,15.01,step) for q in yaw(r['tail'],a)];forms=flat+tailset
 pp=[];rr=[];di=[];er=[]
 for i,(n,a,rad,d) in enumerate(forms):
  pp.extend(a);rr.extend([rad]*len(a));di.extend([(0.,0.,0.) if d is None else d]*len(a));er.extend([debit if i>=len(flat) else 0.]*len(a))
 pp=np.array(pp);rr=np.array(rr);di=np.array(di);er=np.array(er)
 def fun(x):
  z=pp-x[:3];t=np.sum(z*di,axis=1);return np.sqrt(t*t+(np.sqrt(np.maximum(0,np.sum(z*z,axis=1)-t*t))+rr)**2)+er
 ids=[];v0=np.r_[c,max(fun(c))]
 for it in range(40):
  d=fun(v0);j=int(np.argmax(d))
  if j in ids:break
  ids.append(j)
  r0=minimize(lambda y:y[3],v0,jac=lambda y:[0,0,0,1],method='SLSQP',constraints=[{'type':'ineq','fun':lambda y:y[3]-fun(y)[ids]}],options={'ftol':1e-11})
  v0=r0.x
 print('sufficient all listed continuous yaw and stroke Ø, center, angle interpolation error',2*max(fun(v0)),v0[:3],debit)
if __name__=='__main__':rerun()
