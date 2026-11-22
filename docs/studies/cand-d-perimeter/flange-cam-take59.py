"""Continuous positive radial cam and open stations; mm, radians where noted."""
from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('flange-drive-take59.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
# Take58 interface in a separate small data file for provenance.
J=json.loads((D/'flange-jaw-take59.json').read_text());STATION=J['clock'];ST=J['stroke'];FOLLOW=J['closed_pin_radius'];RO=FOLLOW+ST+2.15
NSTEP=8;CAM=NSTEP*45*20/140;PH0=4.50;PH1=CAM-4.50;GC=5.50
def lift(phi):
 a=np.clip((phi-PH0)/(PH1-PH0),0,1)
 return ST*.5*(1-cos(pi*a))
def innerlaw(theta):
 # Each tooth/integral shoe slides along one FIXED radial axis. Opening
 # doesn't radially dilate circular sectors, which would be wrong off-centre.
 return lift(theta)
def tooth(a,off=0.):
 ls=[]
 for n,coords in J['prisms'].items():
  ls.append(sol(n+str(a),[(O+x)*X+r*U(a)+z*U(a+90) for x,r,z in coords]))
 fp=FOLLOW*U(a)
 ls += [sbox('captured radial slide '+str(a),(O-3.23,O-1.93),(FOLLOW-1.64,FOLLOW+1.25),(-2.12,2.12),a),
        sbox('radial bridge '+str(a),(O-3.18,O+J['bridge_xmax']),(FOLLOW-.98,FOLLOW+.92),(-1.44,1.44),a),
        cy('cam follower pin '+str(a),0,(O-5.18,O-1.98),fp[1:],.85),
        cy('hardened roller '+str(a),0,(O-5.14,O-3.56),fp[1:],1.05)]
 if ALT==2:
  ls=[s for s in ls if not s[0].startswith(('captured radial slide','radial bridge'))]
  ls += [sbox('rear T slide '+str(a),(O-3.23,O-1.93),(FOLLOW-.22,FOLLOW+3.22),(-2.11,2.11),a),
         sbox('guided draw cartridge '+str(a),(O-3.16,O-1.84),(16.59,FOLLOW+.37),(-1.25,1.25),a),
         sbox('radial heel tie upper '+str(a),(O-3.01,O-2.04),(16.42,FOLLOW+.50),(1.27,1.88),a),
         sbox('radial heel tie lower '+str(a),(O-3.01,O-2.04),(16.42,FOLLOW+.50),(-1.88,-1.27),a)]
 return [trans(s,off*U(a)) for s in ls]
def clipone(s,n,b):
 from itertools import combinations
 from scipy.spatial import ConvexHull
 v=np.array(s[1]);h=v@n-b
 if min(h)>-1e-9:return []
 if max(h)<1e-9:return [s]
 hull=ConvexHull(v);edges=set(tuple(sorted(e)) for tri in hull.simplices for e in combinations(tri,2))
 z=[p for p,d in zip(v,h) if d<=0]
 for i,j in edges:
  if h[i]*h[j]<0:z.append(v[i]+h[i]/(h[i]-h[j])*(v[j]-v[i]))
 return [sol(s[0],z)]
def frame():
 f=[]
 for j in range(3):
  a=STATION+j*120
  # Full conical wall except the actual rectangular station (±3.31t).
  for i in range(16):
   p=a-60+120*i/16;q=p+120/16
   for k,(x1,x2) in enumerate(((HOME-.10,-3.61),(-3.61,-.27),(-.27,0))):
    x=lambda v:14.50+.28*v
    z=washer('flared wall'+str((j,i,k)),(O+x1,O+x2),(x(x1),x(x2)),(16.02,16.02),p,q)
    if k!=1:f.append(z)
    else:
     for sg in (-1,1):f+=clipone(z,sg*U(a+90),-3.31)
  guide=(18.15,22.67) if ALT==2 else (FOLLOW-1.94,FOLLOW+ST+1.52)
  for k in (-1,1):
   f += [sbox('radial channel side '+str((j,k)),(O-3.32,O-1.70),guide,tuple(sorted((k*2.19,k*3.00))),a),
         sbox('slide thrust cheek '+str((j,k)),(O-1.83,O-1.10),guide,tuple(sorted((k*1.40,k*2.94))),a),
         sbox('captured shoe rear lip '+str((j,k)),(O-3.42,O-3.28),guide,tuple(sorted((k*1.38,k*2.93))),a)]
  f += [sbox('jaw guide-to-wall foot'+str(j),(O-3.60,O-.88),(14.65,FOLLOW+1.27),(2.68,3.62),a),
        sbox('fixed ring outer bridge'+str(j),(O-7.42,O-1.22),(RO+.12,RO+1.46),(-2.75,2.75),a),
        sbox('ring thrust washer near'+str(j),(O-5.62,O-5.35),(RO-.92,RO+1.06),(-2.55,2.55),a),
        sbox('ring thrust washer far'+str(j),(O-3.49,O-3.22),(RO-.92,RO+1.06),(-2.55,2.55),a),
        sbox('ring bearing anchor'+str(j),(O-7.50,O-6.77),(16.74,RO+1.38),(-2.72,2.72),a),
        rod('frame spoke and rear tie'+str(j),(O-7.07)*X+17.55*U(a),(O+HOME-4.01)*X+13.55*U((-90,30,150)[j]),1.32)]
 # Straight rigid posts tie ring register to stationary rear frame.
 f+=anchors()+drives()+[sol(*s) for s in V['joint']]+pads()
 return f
def wheel():
 w=ring('cam wheel outer stock',(O-5.29,O-3.55),(14.75,14.75),(RO,RO))
 # separate axially staggered internal gear: full OD hub overlaps back plate.
 w+=ring('inner gear ring blank',(O-7.27,O-6.06),(17.23,17.23),(RO-.70,RO-.70))
 w+=ring('cam gear wheel shoulder',(O-6.08,O-5.23),(RO-2.20,RO-2.20),(RO-.84,RO-.84))
 return w
def grooves():
 # Edges are normal offsets from a roller-centre curve in the ring's frame,
 # not uncorrected polar offsets. Explicit end caps and complete fillets need CAD.
 records=[]
 for j in range(3):
  v=[];a=STATION+120*j;rr=1.05+.075
  for phi in np.arange(-4,ceil(CAM)+5,.25):
   t=radians(a-phi);u=np.array([cos(t),sin(t)]);b=np.array([-sin(t),cos(t)])
   r=FOLLOW+lift(phi);psi=np.clip((phi-PH0)/(PH1-PH0),0,1)
   dr=ST*.5*pi*sin(pi*psi)/radians(PH1-PH0)
   n=(r*u+dr*b)/hypot(r,dr);v.append([float(phi),list(r*u+rr*n),list(r*u-rr*n)])
  records.append(v)
 return records
def arr():
 f=frame();w=wheel();d=disk();c=[s for j in range(3) for s in tooth(STATION+120*j)];t=shift(flange(),-P)
 return f,w,d,c,t
def col(S):
 # Group concentric full ring as a (conservative) CYLINDER rather than its
 # square AABB; it deliberately fills its bore in these OUTER-only tests.
 ls=[];groups={}
 for s in S:
  k=next((n for n in ('cam wheel outer stock','inner gear ring blank','cam gear wheel shoulder','flared wall') if s[0].startswith(n)),None)
  if k:groups.setdefault(k,[]).append(s)
  else:ls.append(s)
 for k,v in groups.items():
  a=np.vstack([s[1] for s in v]);ls.append(cy(k+' outer',0,(min(a[:,0]),max(a[:,0])),(0,0),max(np.linalg.norm(a[:,1:],axis=1))))
 return reduce(ls)
def csweep():
 return [s for j in range(3) for s in boxesweep(tooth(STATION+120*j),ST*U(STATION+120*j))]
def place():
 f,w,d,c,t=arr(); ss=col(f+w+csweep()+boxesweep(d,[TR,0,0]))
 ts=col(t);rs=max(far(s,H) for s in ts);delta=2*rs*sin(radians(.5))
 for a in range(-15,16,2):ss+=[sol(n,v,r+delta,None) for n,v,r,ax in rotate(ts,a)]
 s=elec(ss);(D/'flange-boards-take59.json').write_text(json.dumps(s,separators=(',',':'))+'\n')
if __name__=='__main__':place()
