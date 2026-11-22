"""Can pre-roll about the stud open an approach to the specified Take55 jam?"""
from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('side-audit-take56.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def roll(ls,ph):
 c=cos(radians(ph));s=sin(radians(ph));R=np.array([[1,0,0],[0,c,-s],[0,s,c]])
 return [sol(n,np.array(v)@R.T,r,None if d is None else R@d) for n,v,r,d in ls]
def explore():
 f,m,y,t=parts();e=stock()
 up=reduce(f+e+shift(m,DX)+boxesweep(shift(y,DX),[0,.32,0]))
 # For intended mechanism contacts use separate Take55 geometry. All other
 # pairs checked against that mechanism's actual outer track and plug stock.
 oth=reduce([s for s in mated() if s[0] not in ('ball','shoulder','neck')])+shift(reduce(f+e+m+y),P)
 uext=extlist(up)
 for label,yaw,cx,cy in [('sharp',-15.25,.169099,-.3893213),('rounded',-17.25,.172095,-.196669)]:
  for ph in (0,-5,5,-10,10,-15,15,-20,20,-25,25,-30,30):
   mm=mr(roll(oth,ph),yaw,cx,cy);q=pairs(mm,up,eb=uext);print(label,ph,q)
def path():
 f,m,y,t=parts();e=stock();mt=mated();nhead=shift(reduce(f+e+m+y),P)
 outer=[s for s in m if not s[0].startswith('C shell')]
 a=reduce(f+e+shift(m,DX)+boxesweep(shift(y,DX),[0,.304,0]))
 b=reduce(f+e+shift(outer,DX)+boxesweep(shift([s for s in y if s[0] not in ('plug cylindrical core','plug slit tongue')],DX),[0,.304,0]))
 tail=reduce([s for s in mt if s[0] not in ('ball','neck','shoulder')])+nhead
 stud=mt[6:9];assert [s[0] for s in stud]==['ball','neck','shoulder']
 ea,eb=extlist(a),extlist(b)
 for lab,yaw,cx,cy in [('sharp',-15.25,.169099,-.3893213),('rounded',-17.25,.172095,-.196669)]:
  # From the parallel, floor-contact lifted pose, translate ball inside local
  # cavity then roll around X and yaw about Z at constant ball centre.
  n=10;stages=[[(-.15+(cx+.15)*i/n,cy*i/n,0,0) for i in range(n+1)],
                 [(cx,cy,z,0) for z in np.linspace(0,-25,51)],
                 [(cx,cy,-25,z) for z in np.linspace(0,yaw,38)]]
  for j,states in enumerate(stages):
   vals=[];net=[];flo=[];rad=max(far(s,np.array([S,0,0])) for s in tail)
   delta=np.asarray(states[1])-states[0]
   for x,yy,r,z in states:
    t1=mr(roll(tail,r),z,x,yy);t2=mr(roll(stud,r),z,x,yy)
    v1=pairs(t1,a,eb=ea);v2=pairs(t2,b,eb=eb)
    vals.append(min(v1,v2))
    debit=lambda rad:hypot(*delta[:2])/2+2*rad*sin(radians(max(abs(delta[2:]))/4))
    # Split moving-body bounds. Sphere at pivot is invariant, but using its
    # radius and that of the entire (short-neck) stud is conservative.
    net.append(min(v1[0]-debit(rad),v2[0]-debit(max(far(s,[S,0,0]) for s in stud))))
    flo.append(min(ext(s,np.eye(3))[0][2] for s in t1))
   delta=np.asarray(states[1])-states[0];eps=hypot(*delta[:2])/2+2*rad*sin(radians(max(abs(delta[2:]))/4))
   print(lab,'path stage',j,'nominal, interpolation debit, allowance .20, cert, floor',min(vals),eps,min(net)-.20,min(flo))
if __name__=='__main__':explore();path()
