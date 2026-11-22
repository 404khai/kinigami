from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('sleeve-short62.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def check():
 data=json.loads((D/'sleeve-short62.json').read_text());e=data['electronics'];f=fixed2();t=shift(flange(),-P);hd=osweep()
 for p in (0,5.9,16):
  st=shortstate(p);print('p',p,'stow full, mechanical',enc(f+t+st+e),enc(f+t+st));print('min-z',min(ext(q,np.eye(3))[0][2] for q in f+t+st+e))
 continuous(hd+e,compress(t[:7]))
 print('boards v head sweeps',pairs(e,hd))
 # Inscribed occupied true yoke, not a convex hull filling its centre.
 ri=inner_ring('intact yoke hoop ',-8.79,-7.29,13.47,15.52)
 ff=[q for q in f if q[0].startswith(('yaw gearmotor','lower case','compound upper bridge','motor base','clamp gearmotor','rear spine','fixed fork rear return','hinge pin','upper hinge'))]
 m=[q for q in f if q[0]=='clamp gearmotor']
 z=shift([innerfl()]+flange()[1:4],-P)
 for p in (0,5.9,12,16):
  s,h,_,_=laws(p);print('p',p,'hoop vs actual fixed joint/frame',cp(shift(ri,-p),ff)[:3])
  # material rods and clamps, not Geneva/slot blanks.
  st=[q for a in AZ for q in jaw2(a) if q[0].startswith('steel trailing slide')]
  st=[trans(q,s*U(a)-h*X) for a,q in zip(AZ,st)]
  print('inner actual steel jaw slide, own fixed rigid struts',p,cp(st,[q for q in f if 'reaction spine' in q[0] or 'thrust anchor' in q[0] or 'clamp gearmotor' in q[0]])[:2])
  n=[q for q in f if q[0].startswith(('fixed rocker pin','fixed pivot reaction spine','front bushing','master screw M3','clamp gearmotor'))];r=[]
  for a in AZ:
   for i in range(12):
    lo=a-60+10*i;hi=lo+10
    for l,u in ((-7.12,-3.61),(-.27,0),(-3.61,-.27)):
     if l==-3.61 and a-20<=lo<a+20:continue
     r.append(washer('real sleeve wall'+str((lo,l)),(O+l,O+u),(14.50+.28*l,14.50+.28*u),(15.73,15.73),lo,hi,True))
  print('inscribed sleeve wall vs fixed force train',p,cp(shift(r,-h),n)[:2])
  print('fixed plate vs real moving rocker rods',p,cp(plate(),[q for a in RK for q in rocker(a,p) if 'arm' in q[0] or 'output rocker' in q[0]])[:2])
 for a in (-15,0,15):
  print('own tail rolled flange/buttons vs motor, yaw',a,cp(rotate(z,a),m)[:1])
 # If a power head gap is negative, test actual positive-volume stock in
 # two independent states and at the continuous-study worst yaw.
 lf=[q for q in f if q[0].startswith(('clamp gearmotor','screw thrust anchor','screw front anchor','fixed rocker pin','motor quill return'))]+e
 for p,pen in ((0,0),(16,16),(0,16),(16,0)):
  s,h,_,_=laws(p);ss,hh,_,_=laws(pen);left=lf+[trans(q,s*U(a)-h*X) for a in AZ for q in jaw2(a)[1:3]]
  for a in (-15,0,15):
   print('head-head inner samples',p,pen,a,cp(left,shift(rotate(lf+[trans(q,ss*U(aa)-hh*X) for aa in AZ for q in jaw2(aa)[1:3]],a),P))[:1])
 # The parked section has real annular gap; a pitched shoulder is not covered
 # by the zero-yaw radial ordering. No release distance from screw counts.
 for h in (0,TR):
  print('fixed disc vs translated taper at face, nominal if present',h,HOME+h,14.5+.28*(HOME+h)-RD)
def bounds():
 # AABB board reserves are actually boxes in the declared package. Pairwise
 # vertices prove a diameter lower bound for this specific *listed* stock.
 d=json.loads((D/'sleeve-short62.json').read_text());e=d['electronics'];aa=[]
 for q in e:
  for v in q[1]:aa.append((q[0],v))
 # Actual corners on retained guide and input structural lugs.
 for q in fixed2()+shell2()+yoke():
  if q[0].startswith(('fork on fixed pillar','axial sleeve rail','input bridge','cam plate rear keel','guide tie to cone')):
   for v in q[1]:aa.append((q[0],v))
 n=np.array([q[1] for q in aa]);v=np.linalg.norm(n[:,None]-n[None,:],axis=2);i,j=np.unravel_index(np.argmax(v),v.shape);print('listed-stock lower point pair',v[i,j],aa[i],aa[j])
if __name__=='__main__':check();bounds()
