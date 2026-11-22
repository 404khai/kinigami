from pathlib import Path
from runpy import run_path
g=run_path(str(Path(__file__).with_name('drum-input64.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def interpolate(s0,s1,extra=0):
 return sol(s0[0], s0[1]+s1[1],s0[2]+extra,s0[3])
def geartrain():
 xw=O-9.11;zw=-19.50;gx=xw-3.58;gz=zw+2.81;mx=gx-4.8;mz=gz
 f=[cy('case hardened worm blank',1,(-3.29,3.29),(xw,zw),1.80),
    cy('worm throughshaft',1,(-9.00,6.61),(xw,zw),.94),
    cy('indexed worm wheel 8 slots',1,(-8.75,-7.24),(xw,zw),4.22),
    cy('driver blocking sector',1,(-8.71,-7.27),(gx,gz),2.03),
    cy('driver crank cheek',1,(-9.79,-8.91),(gx,gz),2.40),
    cy('driver return quill',1,(-17.88,-9.24),(gx,gz),.88),
    cy('driver back bush',1,(-17.48,-16.53),(gx,gz),1.43),
    cy('driver front bush',1,(-11.37,-10.08),(gx,gz),1.47),
    cy('quill 32T',1,(-16.22,-14.89),(gx,gz),3.42),
    cy('gearmotor 16T',1,(-16.20,-14.91),(mx,mz),1.79),
    cy('motor independent pinion journal',1,(-16.36,-13.43),(mx,mz),.87),
    cy('motor pinion bush',1,(-14.71,-13.61),(mx,mz),1.43),
    cy('clamp gearmotor',1,(-13.37,19.43),(mx,mz),3.)]
 for d in (-1,1):
  z=sorted((d*3.47,d*6.31))
  f += [cy('worm thrust radial race '+str(d),1,z,(xw,zw),2.40),
        rod('worm bearing pillar '+str(d),(xw,d*5.12,zw),(xw-3.63,d*5.58,zw+2.10),1.07),
        rod('worm radial rail '+str(d),(xw-3.63,d*5.58,zw+2.10),(-1.62,d*5.20,-15.52),1.12)]
 f +=[rod('motor saddle spine',(mx,7.4,mz+2.32),(-2.61,6.10,-13.21),1.12),
      rod('quill bearing support',(gx,-10.57,gz),(xw,-5.21,zw),1.17),
      bx('cam drive cutoff board',(-4.01,2.14),(-6.21,-1.67),(7.18,8.97))]
 return f
def fixture():
 f=wall()+[sol(*s) for s in V['joint']]+pads()+geartrain()
 for a in AZ:
  # Opposed axial thrust faces at R~16 and radial guide pads on bearing rim.
  aa=a+44
  f +=[sec('frame axial race aft '+str(a),(-13.13,-12.69),(15.84,17.72),(-2.73,2.73),aa),
       sec('frame axial race fore '+str(a),(-11.57,-11.07),(15.83,16.73),(-2.72,2.72),aa),
       sec('frame OD race '+str(a),(-12.74,-11.56),(17.47,18.46),(-2.70,2.70),aa),
       sec('thrust carrier outer '+str(a),(-13.55,-10.80),(17.83,18.69),(-2.41,2.41),aa),
       sec('front bearing spoke '+str(a),(-11.46,-10.85),(16.40,18.49),(-1.66,1.66),aa),
       rod('bearing axial frame rail '+str(a),pos(aa,-13.21,18.17,0),pos(aa,-21.54,18.17,0),1.13),
       rod('bearing rear return '+str(a),pos(aa,-21.54,18.17,0),pos(aa,-21.54,5.45,0),1.08),
       rod('rear fork frame post '+str(a),pos(aa,-21.54,5.45,0),(-2.97)*X+3.60*U(aa),1.05),
       sec('fixed lip wall mount '+str(a),(-7.55,-6.75),(14.85,18.78),(-1.59,1.59),aa),
       sec('front frame outrigger '+str(a),(-13.11,-7.03),(18.57,19.57),(-1.53,1.53),aa)]
  for sg in (-1,1):
   f +=[sec('leaf pullrod guide '+str((a,sg)),(-12.30,-7.01),(18.46,20.04),(4.78+sg*1.14-.26,4.78+sg*1.14+.26),a)]
  f +=[sec('guide mounting claw '+str(a),(-7.03,-6.55),(15.28,19.91),(5.60,6.18),a),
       sec('phase pickup reserve '+str(a),(-11.08,-10.50),(14.62,16.40),(-1.16,1.16),aa)]
 for a in BAZ:
  for sg in (-1,1):
   f +=[sec('disk key pad '+str((a,sg)),(-10.11,-8.69),(6.83,8.26),(sg*1.44-.20,sg*1.44+.20),a)]
  f +=[sec('disk key ground body '+str(a),(-14.58,-8.69),(6.29,6.89),(-1.70,1.70),a),
       rod('disk key support '+str(a),pos(a,-14.09,6.65,0),pos(a,-20.62,4.37,0),.96)]
 f += [sec('park steel stop',(-20.98,-20.22),(12.20,14.25),(-.58,.58),60.15),
       sec('draw steel stop',(-20.98,-20.22),(12.20,14.25),(-.58,.58),-58.3)]
 for a in (60.15,-58.3):f.append(rod('stop to rear bridge '+str(a),pos(a,-20.71,13.71),pos(a,-21.62,17.76),.79))
 return f
def enddog(th):return sec('ring stop lug',(-20.91,-19.86),(12.42,13.83),(-.45,.45),-50+th)
def state(th):
 ang,h=phase(th)
 return shift(disk(),h)+drum()+[enddog(th)]+sum((leaves(a,ang)+rods(a,ang) for a in AZ),[])
def turnt(T):
 # Closed passive buttons referenced to midpoint. Include .40 extension
 # and .32 compression in sweep even where steel stops limit the interval.
 return [boxesweep([trans(s,-.40*X)],.72*X)[0] if s[0].startswith(('revised tail button','button plunger','captive button foot','button inner guide stem','plunger target ring')) else s for s in T]
def coarse(S):
 out=[];groups={}
 for s in S:
  k=next((n for n in ('inner disk cam sleeve','outer jaw cam sleeve','annular connecting web','120T single','front outer bearing rim','wheel hub standoff','fixed flared wall') if s[0].startswith(n)),None)
  if k:groups.setdefault(k,[]).append(s)
  else:out.append(s)
 for n,v in groups.items():
  p=np.vstack([s[1] for s in v]);out.append(cy(n+' cylinder',0,(min(p[:,0]),max(p[:,0])),(0,0),max(np.linalg.norm(p[:,1:],axis=1))))
 return reduce(out)
def sweep():
 f=coarse(fixture()+drum());s=f+boxesweep(disk(),TR*X)
 a0=phase(-3.75)[0]
 for az in AZ:
  r=rods(az,0);dx=horn(a0)[0]-HX;s+=boxesweep(r,dx*X)
  # Chords enclose the curve with sagitta <= .01 at 2.6 deg even at R10.
  pv=leaves(az,a0)
  for an in np.linspace(a0,0,17)[1:]:
   nv=leaves(az,an);s.extend(interpolate(u,v,.004) for u,v in zip(pv,nv));pv=nv
 # Full ring swept lug exterior, no clearance proved using a narrow included phase.
 s+=ring('ring stop orbit',(O-20.91,O-19.86),(12.40,12.40),(13.86,13.86),24)
 return s
def shorttail():
 t=turnt(tail());ls=[];ss={}
 for s in t:
  kk=next((n+str(a) for a in BAZ for n in ('button tube ','front travel shoulder ') if s[0].startswith(n+str(a))),None)
  if kk:ss.setdefault(kk,[]).append(s)
  else:ls.append(s)
 for k,v in ss.items():
  a=float(k.split()[-1]);p=np.vstack([s[1] for s in v]);co=10.3*U(a);ls.append(cy(k+' outer',0,(min(p[:,0]),max(p[:,0])),co[1:],max(np.linalg.norm(p[:,1:]-co[1:],axis=1))))
 return reduce(ls)
def board():
 s=sweep();t=shift(shorttail(),-P);r=max(far(q,H) for q in t)
 for a in range(-15,16,2):s +=[sol(n,v,rr+2*r*sin(radians(.5)),None) for n,v,rr,d in rotate(t,a)]
 return elec(s,wide=True)
def run():
 e=board();data=dict(label='exploratory',O=O,H=sh(H),pitch=P,home=HOME,stroke=TR,button_stations=BAZ,pivots=[HX,HR,AL],fixed=fixture(),disk=disk(),cam_blank=drum(),leaf0=[leaves(a,0) for a in AZ],pullrods0=[rods(a,0) for a in AZ],own_tail_mid=shift(tail(),-P),electronics=e)
 (D/'drum-model64.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
if __name__=='__main__':run()
