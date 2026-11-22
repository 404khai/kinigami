"""Second build: linear master input, no rotating barrel or spring cartridges."""
from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('sleeve-check62.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
AA=7.2;BB=3.60;CAP=16.;TROW=2.7;PX=-17.15;RA=18.50;RR=17.55;RK=(-24,96,216)
SCA=-169.;SN=-3.95;SC=19.00
def stepint(x):
 if x<=0:return 0.
 if x>=1:return x-.5
 return x**3-.5*x**4
def laws(p):
 h=stepint(p-5.9)-stepint(p-14.25);d=p-h
 return ST*ramp(d,.65,5.55),h,d,asin((TR*.5-h)/AA)
def ctr(a,local,r,t):return (O+local)*X+r*U(a)+t*U(a+90)
def intan(n,a,x,r,t1,t2,rad):
 u=U(a+90);return sol(n,[ctr(a,x,r,t) for t in (t1,t2)],rad,u)
def planebar(n,a,tuples,rs):
 return sol(n,[ctr(a,x,r,t) for x,t in tuples for r in rs])
def slotblank(n,a,p1,p2,rs,rr):
 # Convex 3D outer stock spanning a segment, with rectangular side margins.
 return sol(n,[ctr(a,x+i,r,t+j) for x,t in (p1,p2) for r,i,j in product(rs,(-rr,rr),(-rr,rr))])
def rocker(a,p):
 s,h,d,k=laws(p);o=ctr(a,PX,RA,0);q=ctr(a,PX+AA*sin(k),RA,AA*cos(k));v=ctr(a,PX+BB*cos(k),RA,-BB*sin(k))
 qx=PX+AA*sin(k);vx=PX+BB*cos(k)
 return [rod('fixed pivot output rocker '+str(a),o,q,.90),rod('paired input arm '+str(a),o,v,.88),
         radial('rocker output roller '+str(a),qx,.84,AA*cos(k),a,(RA+.67,RA+2.16)),
         radial('master cam roller '+str(a),vx,.84,-BB*sin(k),a,(RA-2.12,RA-.69))]
def fixed2():
 f=plate()+[sol(*s) for s in V['joint']]+pads()
 for a in RK:
  f += [radial('fixed rocker pin '+str(a),PX,.86,0,a,(RA-2.14,RA+2.68)),
        sec('fork on fixed pillar '+str(a),(PX-1.45,PX+1.45),(RA+2.30,RA+3.19),(-1.44,1.44),a),
        rod('fixed pivot reaction spine '+str(a),ctr(a,PX,RA+2.78,0),ctr(a,-27.44,RA+2.78,0),1.08),
        rod('fixed fork rear return '+str(a),ctr(a,-27.44,RA+2.78,0),ctr(a,-27.44,6.88,0),1.08),
        rod('fork inner stationary rail '+str(a),ctr(a,-27.44,6.88,0),(-3.63)*X+3.45*U(a),1.08)]
  for k in (-1,1):
   f+= [sec('axial sleeve rail '+str((a,k)),(-15.20,-2.48),(RA+1.86,RA+3.12),(k*1.71-.35,k*1.71+.35),a+16),
        rod('rail to fixed bearing fork '+str((a,k)),ctr(a+16,-13.24,RA+2.66,k*1.71),ctr(a,PX,RA+2.73,0),.91)]
 # Screw lies outside the swept wall on a meridian away from the fork tips.
 c=SC*U(SCA);y,z=c[1:];xn=O+SN;rear=xn-CAP-2;ex=xn+2.45;xb=rear-3.80;zc=z-4.43;yc=y+1.05
 f +=[cy('master screw M3',0,(rear,ex),(y,z),1.5),
      cy('front bushing reserve',0,(ex+.12,ex+1.59),(y,z),2.15),
      cy('screw rear journal',0,(xb-.39,rear+.16),(y,z),1.24),
      cy('opposed thrust races',0,(xb+1.02,rear-.08),(y,z),2.46),
      cy('8slot wheel blank',0,(xb-.50,xb+.95),(y,z),4.21),
      cy('locking sector blank',0,(xb-.55,xb+.83),(yc,zc),2.05),
      cy('index plate',0,(xb-1.52,xb-.72),(yc,zc),2.29),
      cy('driver quill bearing',0,(xb-2.71,xb-1.65),(yc,zc),1.66),
      cy('bevel 30T',0,(xb-3.89,xb-2.64),(yc,zc),3.75),
      cy('motor pinion 16T',1,(yc+.53,yc+2.21),(xb-3.28,zc),2.1),
      cy('motor quill bush',1,(yc+2.30,yc+3.50),(xb-3.28,zc),1.44),
      cy('clamp gearmotor',1,(yc+3.63,yc+36.43),(xb-3.28,zc),3.0),
      rod('screw front anchor',ctr(SCA,SN+3.75,SC,0),ctr(RK[2],PX,RA+2.78,0),1.07),
      rod('screw thrust anchor',(xb+1.60,y,z),ctr(RK[2],PX,RA+2.73,0),1.19),
      rod('motor quill return',(xb-3.32,yc+2.95,zc-.65),(xb+2.65,y,z-.86),1.07),
      bx('coupler driver',(-4.73,.92),(5.50,10.65),(-1.30,.63))]
 # Twin rails prevent nut rotation and react the external helical torque.
 for k in (-1,1):
  f+=[sec('traveller key rail '+str(k),(SN-CAP-1.42,SN+1.44),(SC-.95,SC+.95),(k*2.76-.36,k*2.76+.36),SCA)]
 return f
def shell2():
 ls=[s for s in lip() if s[0].startswith('conical lip')]
 for a in AZ:
  for k in (-1,1):
   ls+=[sec('radial shoe guide '+str((a,k)),(-3.38,-1.13),(16.62,21.15),(k*3.04-.38,k*3.04+.38),a),
       sec('slide back cheek '+str((a,k)),(-3.60,-3.33),(16.72,21.15),tuple(sorted((k*2.15,k*3.42))),a),
       sec('front cheek and stand '+str((a,k)),(-1.19,-.83),(16.72,21.15),tuple(sorted((k*2.15,k*3.42))),a),
       sec('cheek anchored outside aperture '+str((a,k)),(-3.49,-.93),(15.36,17.19),tuple(sorted((k*3.42,k*4.31))),a)]
 for a in RK:
  q=PX+TR*.5
  for k in (-1,1):
   ls+=[sec('rocker output straight slot side '+str((a,k)),(q+k*1.12-.21,q+k*1.12+.21),(RA+.65,RA+2.16),(4.78,8.48),a)]
  ls += [sec('axial extension of output fork '+str(a),(q-1.0,-4.31),(15.76,16.72),(8.50,9.19),a),
         sec('front extension foot '+str(a),(-4.89,-4.24),(12.82,16.72),(8.48,9.18),a),
         sec('rocker output fork root '+str(a),(q-1.33,q+1.33),(15.20,RA+2.18),(8.45,9.22),a),
         sec('axial bearing shoe '+str(a),(-5.32,-2.62),(18.90,21.22),(-1.29,1.29),a+16),
         sec('guide tie to cone '+str(a),(-4.69,-3.41),(15.41,20.62),(-1.24,1.24),a+16)]
 return ls
def jaw2(a):
 shoe=jaw(a)[0]
 return [shoe,sec('rigid saddle '+str(a),(-3.29,-1.25),(16.49,19.64),(-2.58,2.58),a),
         sec('steel trailing slide '+str(a),(-9.72,-1.35),(16.94,18.24),(-.84,.84),a),
         intan('roller shaft '+str(a),a,-8.73,RR,-1.86,1.86,.68),
         intan('radial drive roller '+str(a),a,-8.73,RR,1.21,2.73,.83)]
def yoke():
 ls=ring('input yoke ring',(O-8.79,O-7.29),(13.47,13.47),(15.52,15.52))
 for a in AZ:
  ls +=[sec('input bridge to rise track '+str(a),(-8.49,-7.49),(15.27,18.12),(1.45,2.83),a)]
  # The actual enclosed roller channel is profiled in master frame x=-8.73+d.
  ls +=[sec('jaw-rise track outer '+str(a),(-9.89,.16),(16.23,20.29),(1.18,2.78),a)]
 for a in RK:
  ls+= [sec('input track anchor '+str(a),(-8.39,-7.44),(15.19,16.91),(-3.51,3.51),a),
        sec('cam plate rear keel '+str(a),(PX+2.45,-7.46),(15.49,16.77),(-1.26,1.26),a)]
  pts=[]
  for p in np.arange(0,CAP+.01,1):
   _,_,_,k=laws(p);pts.append((PX+BB*cos(k)+p,-BB*sin(k)))
  # Outer blank only. Profile data exports the actual normal offsets.
  for i in range(len(pts)-1):
   ls.append(slotblank('sequencer plate '+str((a,i)),a,pts[i],pts[i+1],(RA-2.16,RA-.70),1.68))
 c=SC*U(SCA)
 ls += [lcy('nut body',(SN-1.45,SN+1.45),c,2.26),
        sec('master pull link',(SN-4.17,SN+.95),(SC-.93,SC+.90),(-2.31,2.31),SCA),
        sec('master yoke boss',(SN-4.60,SN-3.46),(14.70,SC+.82),(-1.39,1.39),SCA)]
 return ls
def shortstate(p):
 s,h,_,_=laws(p)
 return shift(shell2(),-h)+shift(yoke(),-p)+[trans(q,s*U(a)-h*X) for a in AZ for q in jaw2(a)]+[q for a in RK for q in rocker(a,p)]
def osweep():
 f=compress(fixed2());ls=[q for q in yoke() if not q[0].startswith('input yoke ring')];ls+=ring('yoke band coarse',(O-8.79,O-7.29),(13.47,13.47),(15.52,15.52),12)
 # Arc-bounded full rocker span; endpoints and a per-sample rotation debit
 # bound motion of all rockers and shaft rods.
 rs=[]
 for a in RK:
  for p in range(0,17):
   for n,v,r,d in rocker(a,p):rs.append(sol(n,v,r+.66,None))
 # Fix articular estimate conservatively using the max rocker length times
 # half the max angular step of asin(h/A), <=.62 mm at 1mm grid.
 return f+boxesweep(compress(shell2()),-TR*X)+boxesweep(ls,-CAP*X)+sum((boxesweep(jaw2(a),ST*U(a))+boxesweep([trans(q,ST*U(a)) for q in jaw2(a)],-TR*X) for a in AZ),[])+rs
def profiles():
 o={}
 for typ in ('sequence','radial'):
  curves=[]
  for p in np.linspace(-.39,CAP+.39,841):
   s,h,d,k=laws(p);curves.append((PX+BB*cos(k)+p,-BB*sin(k)) if typ=='sequence' else (-8.73+d,RR+s))
  ar=np.array(curves);ar=ar[np.r_[True,np.linalg.norm(np.diff(ar,axis=0),axis=1)>1e-9]];dd=np.gradient(ar,axis=0);no=np.c_[-dd[:,1],dd[:,0]]/np.linalg.norm(dd,axis=1)[:,None];width=.90 if typ=='sequence' else .89
  o[typ]=dict(center=ar.round(5).tolist(),sideA=(ar+width*no).round(5).tolist(),sideB=(ar-width*no).round(5).tolist())
 return o
def search():
 hd=osweep();t=compress(shift(flange(),-P));rt=max(far(s,H) for s in t)
 for a in range(-15,16,2):hd+=[sol(n,v,r+2*rt*sin(radians(.50)),None) for n,v,r,d in rotate(t,a)]
 e=elec(hd,wide=True)
 (D/'sleeve-short62.json').write_text(json.dumps(dict(fixed=fixed2(),carriage=shell2(),input=yoke(),radials=[jaw2(a) for a in AZ],rockerClosed=[rocker(a,0) for a in RK],own_tail=shift(flange(),-P),electronics=e),separators=(',',':'))+'\n')
 (D/'sleeve-profile62.json').write_text(json.dumps(profiles(),separators=(',',':'))+'\n')
if __name__=='__main__':search()
