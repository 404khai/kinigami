"""Rigid programmable-robot packaging trial. Positive X points to mating tail; mm."""
from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('sleeve-primitives62.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
import os
BIAS=int(os.getenv('AXIAL_SHOES','1'));AZ=(-90,30,150);TH=105.;LEAD=6.40
# The rear helical roller is turned by positive axial screw displacement;
# the ring itself translates under its external fixed cam followers.
def ramp(th,lo,hi):
 u=np.clip((th-lo)/(hi-lo),0,1);return (1-cos(pi*u))/2
def law(th):return ST*ramp(th,7,44),TR*ramp(th,49,98),LEAD*th/TH+TR*ramp(th,49,98)
def sec(n,x,r,t,a):return sbox(n,tuple(O+np.array(x)),r,t,a)
def lcy(n,x,ctr,r):return cy(n,0,tuple(O+np.array(x)),ctr[1:],r)
def radial(n,x,rr,t,a,span):
 u=U(a);p=(O+x)*X+t*U(a+90)
 return sol(n,[p+q*u for q in span],rr,u)
def plate():
 f=[frust('fixed solid beveled disk',(O+HOME-1.60,O+HOME),(RD-.55,RD)),
    frust('metal fixed central spine',(-2.25,0.5,O+HOME-1.42),(3.45,4.55,5.70))]
 for j,a in enumerate(AZ):
  b=U(a+90);u=U(a)
  for sign in (-1,1):
   # Monotone truncated ramp + top land; all heights backed to common plate.
   v=[];s0=2.50*sin(pi/3)
   # Draft all four flanks 60 degrees; at top the polygon is the
   # parallel inset of the footprint by 1.95/tan(60), not a full cone.
   tbase=s0+(HOME+5.56)/tan(pi/3)
   for xx in (HOME,-5.0):
    d=(xx-HOME)/tan(pi/3)
    for tt,rr in product((tbase+d,3.81-d),(10.3-1.35+d,10.3+1.35-d)):
     v.append((O+xx)*X+rr*u+sign*tt*b)
   f.append(sol('60deg seat insert '+str((a,sign)),v))
   f.append(sec('backing under machined seat '+str((a,sign)),(HOME-2.34,HOME-1.45),(5.0,11.05),tuple(sorted((sign*1.10,sign*3.48))),a))
  f.append(sol('spine radial gusset '+str(a),[x*X+r*u+t*b for x,rlist in [(1.35,(2.0,4.65)),(O+HOME-1.5,(3.4,11.48))] for r,t in product(rlist,(-1.03,1.03))]))
 for sign in (-1,1):
  f+=[rod('spine anchor rail '+str(sign),(-4.2,sign*3.10,0.15),(1.8,sign*3.35,0.15),1.45)]
 return f
def lip():
 ret=[]
 for j,a in enumerate(AZ):
  for i in range(16):
   p=a-60+120*i/16;q=p+120/16
   for k,(l,h) in enumerate(((-7.12,-3.61),(-3.61,-.27),(-.27,0))):
    s=washer('conical lip '+str((j,i,k)),(O+l,O+h),(14.50+.28*l,14.50+.28*h),(15.73,15.73),p,q)
    if k!=1:ret.append(s)
    else:
     for sg in (-1,1):ret+=clipone(s,sg*U(a+90),-3.31)
  for sg in (-1,1):
   ts=sorted((sg*4.72,sg*5.52));ret +=[sec('jaw guide cheek '+str((j,sg)),(-3.61,.11),(15.20,22.55),ts,a),
       sec('rear T shoulder guide '+str((j,sg)),(-3.64,-3.29),(17.31,22.55),sorted((sg*3.90,sg*5.50)),a),
       sec('front T shoulder guide '+str((j,sg)),(-.07,.37),(17.31,22.55),sorted((sg*3.90,sg*5.50)),a)]
  # Annular thrust flanges on the barrel follow the collar in both directions.
  aa=a+55
  ret += [sec('collar fork '+str(a),(-7.82,-2.48),(15.56,16.01),(-1.90,1.90),aa),
          sec('collar thrust toe aft '+str(a),(-6.48,-5.99),(15.56,16.98),(-1.86,1.86),aa),
          sec('collar thrust toe fore '+str(a),(-3.56,-3.18),(15.56,16.98),(-1.86,1.86),aa),
          sec('axial antirotation key '+str(a),(-3.05,-1.21),(21.32,23.10),(-1.23,1.23),a+16),
          sec('key shoulder to annulus '+str(a),(-2.90,-1.53),(15.38,22.62),(-1.18,1.18),a+16)]
 return ret
def jaw(a,dsx=0):
 u,b=U(a),U(a+90)
 v=next(iter(J['prisms'].values()));j=[sol('Take58 rounded shoe outer '+str(a),[(O+x+dsx)*X+r*u+t*b for x,r,t in v])]
 # Shoe is separate from its radial saddle; on version A it slides only in X.
 j += [sec('shoe broad heel '+str(a),(-2.98+dsx,-2.20+dsx),(16.48,19.75),(-2.19,2.19),a)]
 co=18.65*u
 if BIAS:
  # Four series discs: spring free 1.80; total seated compression .62,
  # hard forward reserve to .752; rear stop at total .50, not a radial spring.
  j += [lcy('front spring seat '+str(a),(-.85,-.35),co,4.17),
        lcy('moving spring seat '+str(a),(-2.43+dsx,-2.03+dsx),co,4.15),
        lcy('spring stack OD keepout '+str(a),(-2.03+dsx,-.85),co,4),
        lcy('axial pilot and keeper '+str(a),(-3.24,-.54),co,1.94)]
  for sg in (-1,1):
   j += [sec('fixed keeper cheek '+str((a,sg)),(-3.24,-.34),(17.04,20.26),sorted((sg*4.20,sg*4.63)),a),
         sec('rear stop tab '+str((a,sg)),(-2.98,-2.55),(16.65,20.45),sorted((sg*2.52,sg*4.52)),a),
         sec('solid limit toe '+str((a,sg)),(-1.896,-1.44),(17.41,19.89),sorted((sg*3.84,sg*4.50)),a)]
 else:
  j += [sec('rigid closed saddle '+str(a),(-3.04,-1.23),(16.46,20.02),(-3.01,3.01),a)]
 # Pin tied through a rear rigid slide into the captured grooves in face.
 j += [sec('rear saddle boss '+str(a),(-3.29,-2.99),(16.62,20.65),(-4.58,4.58),a),
       lcy('face follower shank '+str(a),(-5.62,-3.11),17.55*u,.83),
       lcy('face groove roller '+str(a),(-5.58,-3.73),17.55*u,1.01)]
 return j
def barrel():
 return (ring('barrel dual track blank', (O-16.95,O-5.92),(16.38,16.38),(21.68,21.68))
    +ring('face cam blank',(O-5.91,O-3.65),(16.17,16.17),(21.66,21.66))
    +ring('turned integral barrel coupler',(O-6.23,O-5.73),(19.18,19.18),(21.63,21.63)))
# fixed axial profile outer groove: land radius 20.2; fixed radial-axis
# roller pins from OD. Inner drive roller is fixed to the nut at azimuth AIN.
AIN=153.;AX0=-9.17;FX=-15.51;RSC=13.26
def fixed():
 f=plate()+[sol(*s) for s in V['joint']]+pads()
 for j,a in enumerate(AZ):
  aa=a+14
  f += [radial('fixed barrel follower '+str(a),FX,.89,0,aa,(20.31,22.65)),
        sec('outer follower boss '+str(a),(FX-1.23,FX+1.23),(21.88,23.05),(-1.43,1.43),aa),
        sec('fixed sleeve key rail '+str(a),(-12.03,-1.17),(22.25,23.62),(1.32,2.10),a+16),
        sec('fixed sleeve key rail return '+str(a),(-12.03,-1.17),(22.25,23.62),(-2.10,-1.32),a+16),
        rod('bearing pillar '+str(j),(O+FX)*X+22.56*U(aa),(-8.27)*X+17.62*U(aa),1.12),
        rod('frame truss '+str(j),(-8.27)*X+17.62*U(aa),(-2.02)*X+3.62*U(aa),1.11)]
 c=RSC*U(AIN);y,z=c[1:]
 # Rotating leadscrew, translating full engaged nut; before the drive gear
 # are opposed thrust seats, built inside bearing sleeves (blanks not solid).
 rear=O+AX0-LEAD-TR-3.28;end=O+AX0+3.23;dx=rear-4.55
 f += [lcy('M3 screw thread crest',(rear-O,end-O),c,1.5),
       cy('far screw journal',0,(end-.08,end+1.58),(y,z),1.08),
       cy('fixed far journal bush reserve',0,(end+.16,end+1.43),(y,z),2.42),
       cy('rear screw journal',0,(dx-.99,rear+.11),(y,z),1.29),
       cy('opposed thrust races',0,(dx+1.00,rear-.08),(y,z),2.72),
       cy('screw bevel 30T',0,(dx-.87,dx+1.01),(y,z),3.87),
       rod('screw thrust frame', (dx+2.65,y,z),(dx+2.65,y+3.73,z-3.38),1.35),
       rod('screw thrust tie', (dx+2.65,y+3.73,z-3.38),(-3.12,-3.75,-1.45),1.30)]
 # One transverse motor from nose toward +Y. Positive locking by common
 # groove dwells; the screw may backdrive on an active interval.
 # X-parallel indexed driver is shifted in Z off the wheel; its nose
 # carries a crank pin and blocking disc. The wheel keys to the screw.
 # Total screw travel = 14.75 / .0625 = exactly 236 45deg steps.
 z0=z;z=z+4.68
 f=[s for s in f if s[0]!='screw bevel 30T']
 f += [cy('eight slot wheel blank',0,(dx-.05,dx+1.28),(y,z0),4.37),
       cy('blocking orbit and crank reserve',0,(dx-.06,dx+1.25),(y,z),2.16),
       cy('index crank cheek',0,(dx-1.12,dx-.19),(y,z),2.44),
       cy('driver spindle and independent bush',0,(dx-4.35,dx-1.22),(y,z),1.62),
       cy('driver bevel 30T',0,(dx-3.67,dx-2.14),(y,z),3.87),
       rod('input carrier anchor',(dx-3.99,y,z),(dx+2.68,y+2.86,z0-2.65),1.12)]
 dx-=3.02
 f += [cy('clamp gearmotor',1,(y+3.35,y+36.15),(dx,z),3.0),
       cy('quill journal',1,(y+.24,y+3.46),(dx,z),.85),
       cy('bevel 16T',1,(y+.45,y+2.04),(dx,z),2.13),
       cy('quill bush',1,(y+2.19,y+3.24),(dx,z),1.56),
       rod('rear motor frame',(dx,y+4.88,z+2.62),(-5.6,y+3.92,z+2.80),1.24),
       bx('coupler driver',(-6.9,-.4),(-6.5,-1.75),(11.78,13.60))]
 for sg in (-1,1):
  f += [sec('nut guide rail '+str(sg),(AX0-LEAD-TR-1.74,AX0+1.57),(RSC-.80,RSC+1.20),sorted((sg*2.32,sg*3.13)),AIN)]
 return f
def traveller():
 u=U(AIN);bc=RSC*u
 return [lcy('travel nut reserve',(AX0-1.70,AX0+1.70),bc,2.16),
         sec('nut key lug',(AX0-1.52,AX0+1.52),(RSC,RSC+3.22),(-2.22,2.22),AIN),
         radial('inner helical track roller',AX0,.92,0,AIN,(16.29,17.78))]
def state(th,extra=0):
 s,h,n=law(th)
 return shift(lip()+barrel(),-h)+[trans(q,-h*X+s*U(a)) for a in AZ for q in jaw(a,extra)]+shift(traveller(),-n)
def compress(ls):
 out=[];d={}
 for s in ls:
  nm=next((q for q in ('barrel dual track blank','face cam blank','turned integral barrel coupler','conical lip') if s[0].startswith(q)),None)
  if nm:d.setdefault(nm,[]).append(s)
  else:out.append(s)
 for n,ss in d.items():
  pts=np.vstack([s[1] for s in ss]);out.append(cy(n+' outer cylinder',0,(min(pts[:,0]),max(pts[:,0])),(0,0),max(np.linalg.norm(pts[:,1:],axis=1))))
 return reduce(out)
def swept():
 f=compress(fixed());tmp=compress(lip()+barrel());j=[]
 for a in AZ:
  # Conservatively enclose all independent axial bias motion on every jaw
  # component, then cover radial and sleeve strokes in the right order.
  q=boxesweep(shift(jaw(a),-.12),[.252,0,0]) if BIAS else jaw(a)
  j+=boxesweep(q,ST*U(a))+boxesweep([trans(s,ST*U(a)) for s in q],-TR*X)
 return f+boxesweep(tmp,-TR*X)+j+boxesweep(traveller(),-(TR+LEAD)*X)
def board():
 hd=swept();t=compress(shift(flange(),-P));rt=max(far(s,H) for s in t)
 for a in range(-15,16,2):hd+=[sol(n,v,r+2*rt*sin(radians(.50)),None) for n,v,r,d in rotate(t,a)]
 return elec(hd)
def model():
 f=fixed();t=shift(flange(),-P);e=board();fn='biased' if BIAS else 'rigid'
 groups=dict(fixed=f,lip=lip(),barrel_blank=barrel(),jaw_stations=[jaw(a) for a in AZ],nut0=traveller(),own_tail=t,boards=e)
 (D/('sleeve-'+fn+'62.json')).write_text(json.dumps(dict(units='mm',origin=O,pitch=P,H=sh(H),home=HOME,law_deg=[7,44,49,98,TH],travel=[ST,TR,LEAD],groups=groups),separators=(',',':'))+'\n')
if __name__=='__main__':model()
