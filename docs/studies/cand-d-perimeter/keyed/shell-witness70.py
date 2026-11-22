from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('shell-sphere70.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def run():
 e=json.loads((D/'shell-elec70.json').read_text());f=subset(chassis(),('clamp motor','yaw motor body','park geared 4to1','worm shaft','park cam blank'))+subset(pads(),('foot (',))
 # Gear root witnesses, deliberately no tip in meshing tooth spaces.
 f +=[cy('worm star gear ROOT',2,(-17.91,-16.35),(W,WR),2.93),cy('pinion ROOT',2,(15.99,17.25),(JX+2.82,-sqrt(18.90**2-2.82**2)),1.43)]
 for a in AZ:
  for q in sliders(a,0):
   if q[0].startswith(('radial slide tie','radial slide fork')):f +=[q]
 pts=[]
 for q in f+e:pts.extend((q[0],p) for p in polyin(q))
 ss=[sol('yaw sector inner root land',[(JX+16.68*cos(radians(k)),16.68*sin(radians(k)),z) for k in np.arange(-101.34,-61.421,.25) for z in (16.0,17.26)])]
 for y in (-15,0,15):
  p0=pts+[(q[0],v) for q in yaw(ss,y) for v in q[1]];v=np.array([b for a,b in p0]);h=ConvexHull(v);ii=h.vertices;v0=v[ii]
  r=minimize(lambda x:x[3],[-1.4,.5,-.42,30.],method='SLSQP',constraints=[dict(type='ineq',fun=lambda x:x[3]-np.linalg.norm(v0-x[:3],axis=1))],options={'ftol':1e-12});d=np.linalg.norm(v0-r.x[:3],axis=1);vi=ii[d>d.max()-.00005]
  # Exact dual lower, no reliance on optimizer success: any convex weights
  # yield max distance >= weighted RMS about their barycenter.
  ww=minimize(lambda w:np.sum((w@v[vi]-r.x[:3])**2),np.full(len(vi),1/len(vi)),bounds=[(0,1)]*len(vi),constraints=[dict(type='eq',fun=lambda w:w.sum()-1)],options={'ftol':1e-14});ww=np.abs(ww.x);ww/=ww.sum();c=ww@v[vi];radius=np.sqrt(ww@np.square(np.linalg.norm(v[vi]-c,axis=1)))
  print('yaw',y,'finite MATERIAL/RESERVATION lower diameter',2*radius,'points',[(round(float(w),6),p0[i][0],np.round(v[i],4).tolist()) for w,i in zip(ww,vi) if w>1e-5])
if __name__=='__main__':run()
