from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('drum-package64.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def cp(a,b):
 if not a or not b:return []
 ea=extlist(a);eb=extlist(b);out=[]
 for i,s in enumerate(a):
  w=np.maximum(ea[i,0]-eb[:,1],eb[:,0]-ea[i,1]).max(1)
  for j in np.flatnonzero(w<-.001):
   q=ball(s,b[j])
   if q is not None and q[3]>.001:out.append((round(float(q[3]),5),s[0],b[j][0],sh(q[:3])))
 return sorted(out,reverse=True)
def innring(n,x0,x1,r0,r1):
 return [washer(n+str(j),(O+x0,O+x1),(r0,r0),(r1,r1),7.5*j,7.5*(j+1),True) for j in range(48)]
def efgroup(S):
 # Faster assertions on identical-octant bounds for neighbouring moving
 # leaves: spatial hull dilation is outer only, not material.
 groups={};o=[]
 for s in S:
  k=next((q for q in ('cone patch','fixed heel roof','thin cheek liner','flat dogleg ear','crossbar','short R.37','paired dogleg','outboard ear','leaf horn roller') if s[0].startswith(q)),None)
  if k:
   vv=np.mean(s[1],axis=0);key=k,max(AZ,key=lambda a:vv@U(a));groups.setdefault(key,[]).append(s)
  else:o.append(s)
 for k,ss in groups.items():
  vp=np.unique(np.vstack([s[1] for s in ss]),axis=0);vp=vp[ConvexHull(vp).vertices] if len(vp)>4 and np.linalg.matrix_rank(vp-vp[0])==3 else vp;o.append(sol(k[0]+str(k[1]),vp,max(s[2] for s in ss)))
 return o
def audit():
 e=json.loads((D/'drum-model64.json').read_text())['electronics'];f=fixture();t=shift(turnt(tail()),-P)
 hd=efgroup(sweep())+e;ea=extlist(hd);tail0=shift(shorttail(),-P)
 for th in (0,44,105):
  w=f+state(th)+t
  print('theta full/without electronics enclosure',th,enc(w+e),enc(w));print('floor',th,min(ext(s,np.eye(3))[0][2] for s in w+e))
 print('whole-stroke common enclosure (outer, incl chord allowance)',enc(hd+t))
 tt=[s for s in tail0 if s[0].startswith(('one-piece','revised tail','web fork','broad','button','cartridge','spring','back cap','captive','inner guide','front guide','internal travel','rear closure','front travel','reaction gauge','plunger target','return flex'))]
 zz=[];oo=[];r=max(far(s,H) for s in hd);rt=max(far(s,H) for s in tt)
 for a in range(-15,16):
  zz.append((*pairs(hd,boxesweep(shift(rotate(hd,a),P),TR*X),ea),a));oo.append((*pairs(hd,rotate(tt,a),ea),a))
 print('complete power heads ±15, independent phase, axial held..following raw/net',min(zz),min(zz)[0]-.20-2*r*sin(radians(.25)))
 print('own flange incl new cartridge stock vs head raw/net',min(oo),min(oo)[0]-.20-2*rt*sin(radians(.25)))
 print('boards versus head incl full motions',pairs(e,efgroup(sweep())))
 for a in (-15,0,15):
  print('new own tail actual cap, fork, spring return vs gearmotor / spine',a,cp(rotate(shift([s for s in tail() if s[0].startswith(('web fork','cartridge root','button inner guide stem'))],-P),a),[s for s in f if s[0] in ('clamp gearmotor','yaw gearmotor','rear spine')])[:3])
 # Solids inside continuous radial middle outside all grooves. The inner
 # cylinder slot is machined from ID past R11.81; core from R11.90 survives.
 ringpart=innring('inner-drum core ',-20.21,-9.47,11.90,13.12)
 wr=innring('wheel rim/root ',-10.37,-7.85,16.94,17.58)
 c=[s for s in f if s[0].startswith(('disk key support','bearing rear return','quill bearing support','rear fork frame post','front frame outrigger','leaf pullrod guide','worm bearing pillar')) or s[0] in ('yaw gearmotor','clamp gearmotor','upper hinge elbow','rear spine')]
 print('true disk cam core vs unrelated fixed stock',cp(ringpart,c)[:4])
 print('true wheel rim below working teeth vs unrelated fixed stock',cp(wr,c)[:4])
 for th in (0,44,76,105):
  ang,h=phase(th);d=shift(disk(),h);rodset=sum((rods(a,ang) for a in AZ),[])
  print('disk post and key vs unrelated fixed stock',th,cp([s for s in d if s[0].startswith(('axial disk post','disk guide rib'))],c)[:3])
  print('wheel solid core vs positive jaw rods',th,cp(wr,[s for s in rodset if s[0].startswith('axial leaf rod')])[:3])
  print('leaf drive rod vs fixed gearmotor/support',th,cp([s for s in rodset if s[0].startswith('axial leaf rod')],[s for s in f if s[0].startswith(('clamp gearmotor','phase pickup','worm bearing pillar','thrust carrier outer'))])[:3])
 # Electronics as listed reserves, not actual die corners.
 pe=[(s[0],v) for s in e for v in s[1]]
 for s in f:
  if s[0].startswith(('front frame outrigger','motor base','fixed lip wall mount')):pe +=[(s[0],v) for v in s[1]]
 ar=np.array([q[1] for q in pe]);dd=np.linalg.norm(ar[None,:]-ar[:,None],axis=2);i,j=np.unravel_index(np.argmax(dd),dd.shape)
 print('occupied listed-stock corner pair',dd[i,j],pe[i],pe[j])
if __name__=='__main__':audit()
