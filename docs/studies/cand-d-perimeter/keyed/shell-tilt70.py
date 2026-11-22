from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('shell-audit70.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
from scipy.optimize import minimize
def better(q,t):
 # Optimize a unit separating direction. Positive support gap is valid even
 # if optimizer misses a better axis. Negative value alone is no collision.
 def gap(d):
  d=d/max(np.linalg.norm(d),1.e-20);lo,h=ext(q,d[None]);l,hi=ext(t,d[None]);return l[0]-h[0]
 vv=np.r_[ds,-ds];k=np.argmax([gap(d) for d in vv]);y=minimize(lambda d:-gap(d),vv[k],method='Nelder-Mead',options={'maxiter':180,'xatol':1e-8});return max(-y.fun,gap(vv[k]))
def fine(A,B):
 aa=extlist(A);bb=extlist(B);raw=np.maximum(aa[:,0,None]-bb[None,:,1],bb[None,:,0]-aa[:,1,None]).max(2)
 v=sorted((raw[i,j],i,j) for i,j in zip(*np.indices(raw.shape).reshape(2,-1)));mi=np.inf;pair=None
 for val,i,j in v:
  if val>mi:break
  b=better(A[i],B[j])
  if b<mi:mi=b;pair=(A[i][0],B[j][0])
 return mi,pair
def run(az=-90.):
 F=np.column_stack((X,U(az),U(az+90)));u=.36840728;v=.92966450;u,v=np.array([u,v])/hypot(u,v);A=np.array([[u,-v,0],[v,u,0],[0,0,1]])
 if az==30:
  u,v=.8869949228,.4617791755;A=np.array([[u,-v,0],[v,u,0],[0,0,1]])
 dst=O*X+F@np.array([13.5415382,12.5450972,1.80] if az==-90 else [9.2177710014,4.9422799964,1.1]);M=F@A@F.T
 def tr(S):return [sol(s[0],dst+(np.array(s[1])-C*X)@M.T,s[2],None if s[3] is None else M@np.array(s[3])) for s in S]
 an=-1.02227235645;th=brentq(lambda t:phase(t)[0]-an,0,10);print('probe ring °, center and known boss touch world',th,dst,O*X+F@np.array([1.54764486,15.0054754,1.80] if az==-90 else [1.7536448644,14.4774754163,1.1]))
 t=tr(tail()+move(joint()[1],P));f=chassis()+pads();e=json.loads((D/'shell-elec70.json').read_text());sl=sum((sliders(a,an) for a in AZ),[]);hh=groups(f+state(th))+drum()+e
 # Individual fixed stock, not grouping separated annuli into filled hubs.
 for tag,u in [('installed links',subset(sl,('centre clevis link','radial slide','slider link','axial transfer','face roller'))),('fixed hood and stop supports',subset(f,('park stop','leaf mount','leaf bearing','stationary case','thin liner','way anchor','slider guide','fixed wall heel','outer axial','worm fore'))),('power/rear housing',subset(f,('worm shaft','clamp motor','yaw motor','foot','aft cantilever'))+e)]:
  print(tag,'separating-plane max/closest (negative inconclusive)',fine(u,t))
  if tag=='installed links' and az==-90:
   # Inscribed cross-section circles; omit hull excess, and prove the
   # core witness survives both clevis pin bores and the three talon ports.
   stock=tail()[0];vv=[]
   for aa in AZ:vv.extend([pos(aa,-2.25,6.75)+4*U(j*7.5) for j in range(48)])
   for xx,rr in ((-2.25,7.60),(.20,7.10),(2.50,6.),(4.40,3.5),(-.30,7.58),(2.25,6.50),(5.80,3.16)):vv.extend([pos(0,xx,0)+rr*U(j*7.5) for j in range(48)])
   vv=np.array(vv);fl=tr([sol('inner lobe',vv[ConvexHull(vv).vertices],2.50)])[0];cl=next(q for q in u if q[0]=='centre clevis link (-90.0, 1)')
   b=ball(cl,fl);xx,rr,tan=F.T@(b[:3]-O*X);px,rp,rd=link(an);local=(b[:3]-dst)@M+C*X
   inner=tr([sol('cavity',tail()[0][1],1.66)])[0];pt=sol('ball center',[b[:3]],0);print('shell inner void separation to probe center / witness radius',better(inner,pt),b[3]);print('outer material ball [world X,Y,Z,R]; outside clevis bores by',b,min(hypot(xx-px,rr-rp)-.626,hypot(xx-SLX,rr-rd)-.716)-b[3],'outside tail port R2.66 by',min(np.linalg.norm((local-pos(k,-2.25,10.3))[1:])-2.66-b[3] for k in BAZ))
 for a in (-15.,0.,15.):
  n=tr(move(yaw(hh,a),P));foot=tr(move(yaw(pads(),a),P));fl=min((ext(s,np.eye(3))[0][2],s[0]) for s in foot);print('adjacent yaw, broad powered gap, actual lowest foot, penetration',a,pairs(groups(hh),groups(n)),fl,-23.22-fl[0])
 rr=max(far(q,H) for q in pads());zz=[min(ext(q,np.eye(3))[0][2] for q in tr(move(yaw(pads(),a),P))) for a in np.arange(-15,15.001,.5)]
 mesh=np.arange(-15.,15.001,.5);lo=1e4;low=1e4;wg=None;hg=groups(hh)
 for y in mesh:
  ng=tr(move(yaw(hg,y),P));q0=min((ext(k,np.eye(3))[0][2],k[0]) for k in ng);lo=min(lo,q0[0])
  g0=pairs(hg,ng)
  if g0[0]<low:low=g0[0];wg=(y,g0)
 rad=max(far(q,H) for q in hg);debit=2*rad*sin(radians(.125));print('ALL powered hull & electronics vs floor continuous lower (+clear), nonmating head gap lower in fixed approach incl yaw debit',lo+23.22-debit,low-debit,wg)
 print('floor penetration lower across ALL independent adjacent yaws',-23.22-max(zz)-2*rr*sin(radians(.125)))
if __name__=='__main__':
 for k in (-90,30):print('station',k);run(k)
