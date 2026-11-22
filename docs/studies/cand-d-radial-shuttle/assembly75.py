from covers75 import *
from scipy.spatial.distance import cdist
from scipy.optimize import linprog
def borechecks():
 f=sel(facebody(),('fixed continuous case','front wall','aft roof','tangent cheek'))
 dish=plate();metal=sel(dish,('disk shell','six-seat','disk post','moving lead'))
 for what,A,B in [
 ('disk front insertion from clear x plus30 to HOME, plugs PARK collars not yet fitted',sweep(metal,30*X),f+sum((move(plug(a),ST*U(a)) for a in AZ),[])),
 ('disk posts/stud threading in real fixed guides at assembly (no collars)',sweep(sel(metal,('disk post','moving lead')),30*X),diskfixed()),
 ('rear motor versus working posts & collars',sel(ejectdrive(),('disk geared',)),sweep(sel(dish+sum((bushholes(a) for a in BAZ),[]),('disk post','disk terminal collar')),TR*X))]:
  g,n,p=minpair(A,B);print(what,round(g,5),n)
  # Small number of near pairs with worst LP material ball.
  print('conservative inscribed finite-material/envelope overlaps',witness(A,B,2)[2])
 for a in BAZ:
  for k in (-1,1):
   probe=cyl('separate seat pocket',pos(a,-12.05,10.30,2.07*k),pos(a,-8.55,10.30,2.07*k),1.70)
   post=sel(dish,('disk post '+str(a),))[0];print('external pocket probe, post, exact interval x, transverse overlap and ball',a,k,(-12.05,-8.55),2.8-hypot(1.72,2.07),ball(probe,post)[3])
 # Local jaw cassette installs in radial line from outside with lid ON
 # vs OFF; rotor installed *after* cassette with followers already in.
 a=30;p=plug(a);front=sel(roof(a),('front wall','tangent cheek','aft roof'));dr=sweep(p,12*U(a))
 print('carrier radial install front cheek/roof vs guide rails, before top closure',minpair(dr,front+ways(a))[:2])
 print('solid lid veto if assembly order reversed',witness(dr,sel(roof(a),('outer guard top',)),1)[2])
 # Trial access to the collar cross pin: tangential driver corridor
 # before/after powered pieces. Position local x -21.65 at home.
 for a in BAZ:
  tool=cyl('retainer cross-pin punch',pos(a,-21.65,8.58,0.),pos(a,-21.65,8.58,12.),.47)
  print('HOME collar tool access; after fitting drives',a,witness([tool],sel(park()+jawdrive()+ejectdrive()+mounts(),('dog geared','disk geared','jaw geared','rear frame rib','disk worm shaft')),1))
 print('stud thread x overlap home/terminal with fixed nut journal')
 for u in (0,TR):
  lo=max(-23.46+u,SX+.09-2.03);hi=min(-8.21+u,SX+.09+2.03);print(u,lo,hi,(hi-lo)/.50)
 # Ranges of plausible rear clearance on the forward in-bore branch;
 # no assumed registration of end travel beyond nominal.
 gap=bore(0)-RD+.05;R=2.45
 p=R-sqrt(R**2-gap**2);nx=min(sqrt(1-(gap/R)**2),1-1.58/R)
 print('disk p nominal; rear min over lip and spare; sign at μ=.23 δ=.6; actual loaded lost stroke unknown',1.58,p,1.58-p,cos(acos(nx)+radians(.6))-.23*sin(acos(nx)+radians(.6)))
def lower():
 # Inner vertices of installed named purchased-component envelopes, feet,
 # tail pieces and the explicit (unrelieved) pod skin. Chebyshev sphere
 # via finite subset primal/dual; variance of any nonnegative set of
 # weights gives a lower radius independent of optimizer convergence.
 t=sel(ref['tail'],('button near-mid','blind end closure','yaw shaft','yaw keyed','cartridge outer bridge'))
 core=group(sel(allstock(),('jaw geared','disk geared','dog geared','foot (','yaw motor body','cell bulk','protection board','controller board','yaw pinion','front cover high')))
 for count,A in [('mechanical and reserved parts',core),('with actual as-drawn full cover blank',core+[o for _,o in cases()])]:
  B=A+sum((yaw(t,y) for y in np.arange(-15,15.1,2.5)),[]);qq=[(p,s[0]) for s in B for p in polyin(s)];p=np.asarray([u for u,n in qq]);c=p.mean(0)
  for _ in range(5):
   idx=np.argsort(-np.linalg.norm(p-c,axis=1))[:150];ss=p[idx]
   rr=minimize(lambda z:z[3],np.r_[c,34.],method='SLSQP',constraints=[dict(type='ineq',fun=lambda z:z[3]-np.linalg.norm(ss-z[:3],axis=1))],options={'ftol':1e-12})
   cc=rr.x[:3]
   if np.linalg.norm(c-cc)<1.e-6:break
   c=cc
  # Resolve full point set with cutting plane, not oscillating active pool.
  idx=[np.argmax(np.linalg.norm(p-c,axis=1))]
  for _ in range(120):
   ss=p[idx];rr=minimize(lambda z:z[3],np.r_[c,34.],method='SLSQP',constraints=[dict(type='ineq',fun=lambda z:z[3]-np.linalg.norm(ss-z[:3],axis=1))],options={'ftol':1e-11});c=rr.x[:3];i=np.argmax(np.linalg.norm(p-c,axis=1))
   if i in idx:break
   idx.append(i)
  ss=p[idx];opt=minimize(lambda w:-w@(ss*ss).sum(1)+np.sum((w@ss)**2),np.ones(len(idx))/len(idx),method='SLSQP',bounds=[(0,1)]*len(idx),constraints=[dict(type='eq',fun=lambda w:w.sum()-1)],options={'ftol':1e-12});w=np.maximum(0,opt.x);w/=w.sum();v=w@(ss*ss).sum(1)-np.sum((w@ss)**2)
  print('finite weighted witness diameter lower',count,2*sqrt(v),[(qq[j][1],round(z,6),p[j].round(4).tolist()) for j,z in zip(idx,w) if z>.0001])
if __name__=='__main__':borechecks();lower()
