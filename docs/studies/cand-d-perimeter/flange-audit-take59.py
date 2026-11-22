"""Rigid stock only; continuous support gaps and actual material witnesses."""
from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('flange-cam-take59.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def cp(a,b):
 ea=extlist(a);eb=extlist(b);out=[]
 for i,s in enumerate(a):
  v=np.maximum(ea[i,0]-eb[:,1],eb[:,0]-ea[i,1]).max(1)
  for j in np.flatnonzero(v<-.008):
   w=ball(s,b[j])
   if w[3]>.006:out.append((round(float(w[3]),6),s[0],b[j][0],sh(w[:3])))
 return sorted(out,reverse=True)
def rim(x,rf,az):
 return x*X+rf*U(az)
def clampstat():
 print('offset and stroke X, home/park disk; groove/ring/open radial stroke angle',O,HOME,END,TR,FOLLOW,RO,ST,CAM)
 gs=grooves();q=np.array(gs[0],dtype=object)
 u=np.array([np.linalg.norm(v[k]) for v in gs[0] for k in (1,2)])
 print('radial groove edge bounds, inner/outer metal remaining',min(u),max(u),min(u)-14.75,RO-max(u))
 req=ST*.5*pi/radians(PH1-PH0)
 print('cam peak dr/dangle, pressure-angle upper bound',req,degrees(atan(req/FOLLOW)))
 theta=radians(J['normal_from_axis_deg']);mu=.23
 for total in (40,75,113):
  for share in (1/3,1):
   f=share*total
   N=f/(cos(theta)-mu*sin(theta)) if cos(theta)>mu*sin(theta) else inf
   radload=N*(sin(theta)+mu*cos(theta))
   # yoke guide bearing drag: front jaw force offset to slide centre/guides.
   e=abs(J['tip_x']+2.58);L=max(1.,2.48)
   slide=radload+2*.15*(abs(f*J['tip_to_pin_radius'])+abs(radload*e))/L
   # Full-load actuation cost pessimistically charged at max cam slope.
   # Cut-in near dwell has a smaller derivative, not a loaded-release proof.
   torque=slide*req/.75
   froll=slide*hypot(1,req/FOLLOW)
   print('total axial, routing fraction, jaw normal, radial, guide+radial, working roller N, required ring T and idealised geared input',total,round(share,3),*(round(x,3) for x in (N,radload,slide,froll,torque,torque*(20/140)*(sin(pi/8)/(1-sin(pi/8)))/(.72*.8)*((18/32)/.75 if ALT==2 else 1.))))
  ph=3.5*45*20/140;grad=req*sin(pi*(ph-PH0)/(PH1-PH0))
  t0=total*tan(theta)*grad*(20/140)*(sin(pi/8)/(1-sin(pi/8)))*((18/32) if ALT==2 else 1.)
  print('actual mid-fourth-step frictionless radial, ideal motor torque, torque with ONLY gearbox/quill efficiencies',total,total*tan(theta),t0,t0/(.72*.80*(.75 if ALT==2 else 1.)))
 for f in (8,40,75,113):
  # eccentric rotating nut and guide/dowel couple from in-plane y offset
  # and shortest contact span in each 2.75-long plain sleeve.
  for mu in (.05,.15,.23):
   F=ecc(f,mu,2.45,4.85,4.85);T=F*.50/(2*pi*.28);print('disk N, guide μ, screw thrust, screw torque, gearhead demand',f,mu,round(F,3),round(T,3),round(T*(sin(pi/8)/(1-sin(pi/8)))/(.72*.75*32/18),3))
 print('cap and shoulder',14.5+.28*HOME-RD,14.5+.28*(HOME-1.45)-(RD-.42),(14.5+.28*(-2.25)-R)/hypot(1,.28)-RE)
 print('disk motion/stations/home overtravel debit',TR,TR/.0625,120*.0625-TR)
def run():
 f,w,d,c,t=arr();e=json.loads((D/'flange-boards-take59.json').read_text())
 wp=col(w);ff=col(f);cs=csweep();dp=boxesweep(d,[TR,0,0])
 print('straight stow home/closed and parked/open enclosures',enc(f+w+d+c+t+e),enc(f+w+shift(d,TR)+[s for j in range(3) for s in tooth(STATION+120*j,ST)]+t+e))
 print('minimum z all stock',min(ext(s,np.eye(3))[0][2] for s in f+w+dp+cs+t+e))
 model=dict(units='mm',lip=O,home=HOME,end=END,H=sh(H),pitch=P,clamp_angle=CAM,radial=ST,station=STATION,groups=dict(fixed=f,cam_ring_outer=w,disk_home=d,sectors_closed=c,own_tail=t,boards=e))
 (D/'flange-model-take59.json').write_text(json.dumps(model,separators=(',',':'))+'\n')
 (D/'flange-grooves-take59.json').write_text(json.dumps(grooves(),separators=(',',':'))+'\n')
 head=ff+wp+dp+cs+e;r=max(far(s,H) for s in head)
 v=[]
 for a in range(-15,16):
  v.append((*pairs(head,boxesweep(shift(rotate(head,a),P),[TR,0,0])),a))
 print('head-head two independent full motions, yaw ±15, neighbour uniformly held..following X, raw/net gap',min(v),min(v)[0]-.20-2*r*sin(radians(.25)))
 # A legitimate alternative to an upper diameter is an occupied point pair.
 # Motor cans and intact ring rim points (never a polygon's outer corner).
 m=[s for s in f if s[0].endswith('gearmotor')]
 def rimpoints(s):
  n,v,r,z=s;z=np.array(z);u=np.eye(3)[np.argmin(abs(z))];vv=np.cross(z,u)
  return np.vstack([q+r*(u*cos(a)+vv*sin(a)) for q in v for a in np.arange(256)*pi/128])
 ap=np.vstack([rim(O+x,RO,az) for az in np.arange(360) for x in (-5.29,-3.55)])
 # A bought motor with an unspecified OD chamfer: leave any lower bound conditional.
 for s in m:
  b=rimpoints(s);dd=np.linalg.norm(ap[:,None,:]-b[None,:,:],axis=2);i,j=np.unravel_index(np.argmax(dd),dd.shape);print('rim pair OD/material if retained',s[0],dd[i,j],sh(ap[i]),sh(b[j]))
 tt=col([s for s in t if s[0].startswith(('one-piece','tail ball','broad','web fork'))])
 yv=min((*pairs(rotate(tt,a),head),a) for a in range(-15,16));rt=max(far(s,H) for s in tt)
 print('new own tail vs head, all yaws, raw/net',yv,yv[0]-.20-2*rt*sin(radians(.25)))
 # Inner samples of the rolled flange: C disk INSCRIBED, A + ball contained.
 t0=t[0];truefl=sol(t0[0]+' inner',[q*X+(R-.02)*U(j*360/32) for q in (C-P,) for j in range(32)],RE)
 for a in (-15,0,15):
  print('own tail actual flange inner vs cans',a,cp(rotate([truefl],a),m))
 for name,aa,bb in [('registered stops vs clamp can',anchors(),[s for s in m if s[0]=='clamp gearmotor']),('both drive cans',m[:1],m[1:]),
                       ('disk piston core vs fixed hinge',[sol(d[-2][0],d[-2][1],1.18,d[-2][3])],V['joint']),
                       ('disk-drive motor vs steel fixed brackets',m,[s for s in f if 'bracket' in s[0] or 'frame return' in s[0] or 'rear anchor' in s[0]])]:
  print(name,cp(aa,bb)[:4])
 print('boards vs all other swept head',pairs(e,ff+wp+dp+cs))
 for z in (0.,TR):
  for fj in (0.,ST):
   j=[s for i in range(3) for s in tooth(STATION+120*i,fj)]
   vv=cp(shift(d[:1],z),[s for s in j if 'slide' in s[0] or 'bridge' in s[0]])
   print('disk vs jaw pedestal (inner check uses inner turned disk below), proxy gap',z,fj,pairs(shift(d,z),j),vv[:1])
 # exact sphere/crown-plane held response. At X0 ball is tangent to both cone
 # flanks: an advancing cone moves THROUGH a held ball, not a translating neighbour.
 for q in (0,.05,.25):
  print('held at registry, cone penetration along normal at dq',q,q/sqrt(2))
if __name__=='__main__':run();clampstat()
