"""Material, installation restrictions and reactions omitted from outer screens."""
from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('side-audit-take56.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def capins():
 out=[];p,ns,J=cr.setup(13.,radians(60),radians(-90))
 for j,(P,n) in enumerate(zip(p,ns)):
  u=P/13;v=np.cross(n,u);q=cr.O+P-1.85*n;sag=8-sqrt(8**2-.88**2)
  rim=[q+.88*(cos(a)*u+sin(a)*v) for a in np.arange(32)*pi/16]
  out.append(sol('round backing '+str(j),[z+t*n for z in rim for t in (sag,.35)]))
 return out
def ring(s):
 _,v,r,d=s;d=np.array(d);a=np.eye(3)[np.argmin(abs(d))];b=np.cross(d,a)
 return np.vstack([w+r*(a*cos(t)+b*sin(t)) for w in v for t in np.arange(256)*pi/128])
def report():
 f,m,y,t=parts();e=stock();ff=face();eye=np.eye(3)
 for ang,cx,cy in [(-15.25,.169099,-.3893213),(-17.25,.172095,-.196669)]:
  print('finite cap (true inner circle, not box), zero-roll',ang,meshcap(mr(capins(),ang,cx,cy),ff))
 for q in (0,DX):
  print('solid supports vs actual Y can',q,meshcap([s for s in f if s[0].startswith(('X race frame','X rail bolt'))],shift([s for s in m if s[0]=='Y gearmotor'],q)))
  print('parked plug link in actual axial rear yoke',q,meshcap(shift([s for s in y if s[0]=='plug rear crossarm'],q,DY),shift([s for s in m if s[0]=='axial rear yoke'],q)))
 for L in (PL,20.):
  p=next(s for s in ytrain(CX,BACK,Y0,DY,L)[0] if s[0]=='Y outboard quill bush')
  a=ring(next(s for s in V['joint'] if s[0]=='yaw gearmotor'))
  for q in (0,DX):
   b=ring(trans(p,[q,0,0]));norm=np.linalg.norm(a[:,None,:]-b[None,:,:],axis=2);i,j=np.unravel_index(np.argmax(norm),norm.shape)
   print('L, X, diameter lower from actual end rims if bearings/motor retain ODs',L,q,norm[i,j],sh(a[i]),sh(b[j]))
 # For own rear contacts exclude joint-internal intended mating stock; check
 # new rigid tail on its proper pivot. Motors and boards included in head.
 moving=reduce([s for s in t if s[0].startswith(('ball','neck','shoulder','tail core','crown','tail fork'))])
 full=reduce(f+e)+boxesweep(reduce(m),[DX,0,0])+boxesweep(boxesweep(reduce(y),[0,DY,0]),[DX,0,0])
 g=min((*pairs(rotate(moving,a),full),a) for a in range(-15,16));r=max(far(s,H) for s in moving);print('new own tail vs complete head, ±15 yaw through independent strokes',g,'net',g[0]-.20-2*r*sin(radians(.25)))
 # Other thrust/holding sensitivities. Efficiency and forces are trial only.
 angle=27;arm=5.5*sin(radians(angle))
 for F in (42.39,75,113):
  n=ecc(F,.15,4.54,.25,.25);t=n*.50/(2*pi*.28)
  print('X F, T, one dwell flank reaction, .7 pin transverse single shear MPa, .94r socket pin double shear MPa, M3 core axial MPa',F,t,t/arm,(t/(5.5*(1-sin(pi/8))))/(pi*.35**2),n/(2*pi*.94**2),n/(pi*1.18**2))
 print('minimum average input turns and times at 80 loaded gearhead rpm (illustration only)',[(axis,d,d/.0625*32/18,d/.0625*32/18*60/80) for axis,d in [('X',DX),('Y',DY)]])
 for f in (8,30):
  # plug web 1.29 along Y x3.06 along Z bends around Z; measured section only
  print('plug arm Fy, cantilever torque and nominal rectangular-web MPa',f,f*9.17,6*f*9.17/(3.06*1.29**2))
if __name__=='__main__':report()
