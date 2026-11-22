from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('shell-face70.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
# W=world X, local az about X. No inherited Take51 hinge, motor or fork.
W=O-14.24;WR=21.;JX=H[0];MOTOR_X=W-4.80;RKEY=10.68;DRUM_NORMAL=19.5
def wring(n,x,y,ri,ro,m=48,inner=False):
 return [washer(n+' '+str(j),(x,y),(ri,ri),(ro,ro),360*j/m,360*(j+1)/m,inner) for j in range(m)]
def annuli():
 return [('disk sleeve',O-20.29,O-9.07,9.78,13.19),
         ('quill bearing outer hub',-6.03,-.81,5.97,6.68),('aft rotor bridge',-4.18,-3.56,6.32,13.15),('aft rotor rim',-3.85,-3.06,11.93,13.15),
         ('face cam',O-11.69,O-9.04,12.89,20.84),('worm wheel web',W-.97,W+.97,12.91,18.77),('130T rim',W-1.29,W+1.29,18.56,19.80)]
def drum():return sum((wring(*q) for q in annuli()),[])
def joint():
 f=[];t=[];c0=lambda n,t,z,r:cy(n,2,z,((JX+2.82 if t==8.8 else JX),(-sqrt(18.90**2-2.82**2) if t==8.8 else t)),r)
 f+=tube('yaw main steel knuckle',np.array([JX,0.,-2.08]),np.array([JX,0.,2.08]),1.91,3.71)
 f += [bx('knuckle tang',(JX+2.33,-6.85),(-2.45,2.45),(-1.91,1.91)),
       xy('fixed center quill',(-7.38-O,7.65-O),0,0,0,3.44)]
 for xl,xr in ((-5.96,-4.39),(-2.53,-.96)):
  for n,ri,ro in [('quill inner race',3.43,4.05),('quill rolling row',4.06,5.48),('quill outer race',5.49,6.02)]:
   f+=wring(n+str(xl),xl,xr,ri,ro,24)
 # Outer rings seat into rotating hub; stationary INNER race stops at shaft shoulder.
 f+=wring('shaft aft thrust shoulder',-6.29,-5.96,2.18,4.11,20)+wring('shaft front thrust shoulder',-.96,-.61,3.35,4.12,20)
 t +=[c0('yaw shaft',0,(-6.52,17.28),1.82)]
 for sg in (-1,1):
  z=sorted((sg*2.23,sg*4.46))
  t+=[sol('yaw fork blade '+str(sg),[[x,y,s*sg] for x,hy,zz in [(-16.45,2.85,(1.96,4.42)),(-12.38,2.20,(2.23,4.46)),(JX-.32,1.79,(2.23,4.46))] for y in (-hy,hy) for s in zz]),
      c0('yaw fork hub '+str(sg),0,z,2.76)]
 # Keyed shaft transmits to driven sector above motor. Teeth blanks are
 # swept enclosures, not solid full wheel or interference in the mesh.
 for j in range(10):
  a,b=np.radians((-101.42+j*4,-97.42+j*4));t.append(sol('yaw 114T sector '+str(j),[(JX+r*cos(q),r*sin(q),z) for q,r,z in product((a,b),(2.1,17.40/cos((b-a)/2)),(15.98,17.28))]))
 t +=[c0('yaw keyed sector hub',0,(15.94,17.32),2.65)]
 f +=[c0('yaw motor body',8.80,(-17.50,15.30),3.0),c0('yaw pinion',8.80,(15.99,17.25),2.09),
      c0('yaw pinion shaft',8.8,(15.18,17.28),.71),
      rod('yaw motor lower saddle',(JX+2.82,-17.54,-14.70),(-7.53,-17.64,-12.15),1.38),
      rod('yaw motor upper saddle',(JX+2.82,-17.54,13.90),(-7.53,-17.64,13.90),1.38)]
 return f,t
def teeth():
 f=[]
 f += [cy('worm teeth blank',2,(-3.52,3.52),(W,WR),1.80),cy('worm shaft',2,(-18.01,9.39),(W,WR),.93),
       cy('worm 32T spur',2,(-17.91,-16.35),(W,WR),3.43),cy('motor 16T spur',2,(-17.90,-16.36),(MOTOR_X,WR),1.79),
       cy('clamp motor',2,(-14.73,18.07),(MOTOR_X,WR),3.0),cy('clamp pinion quill',2,(-17.94,-14.63),(MOTOR_X,WR),.78)]
 for lo,hi in ((-15.95,-14.51),(-9.67,-7.32),(4.43,6.28)):
  f+=tube('worm independent bearing',np.array([W,WR,lo]),np.array([W,WR,hi]),.96,2.08)
 f+=tube('clamp pinion bearing',np.array([MOTOR_X,WR,-16.19]),np.array([MOTOR_X,WR,-14.81]),.82,1.38)
 # Upper keyed index wheel stays at OD3.52 between the opposing motor and worm.
 f+=[cy('12 hole parking wheel blank',2,(9.40,10.84),(W,WR),1.76),
     bx('parking square journal',(W-.645,W+.645),(WR-.645,WR+.645),(9.38,10.92)),cy('parking staked end',2,(10.86,11.02),(W,WR),.93)]
 for l,h in ((11.00,11.66),(12.02,12.70)):
  f+=tube('dog guide',np.array([W,WR-1.31,l]),np.array([W,WR-1.31,h]),.231,.62)
 for n,l,h in [('negative',-7.305,-6.68),('positive',3.77,4.415)]:
  f+=[cy('worm thrust collar '+n,2,(l,h),(W,WR),1.62)]
 return f+parkmotor()
UA=np.array([cos(radians(30)),sin(radians(30)),0]);VA=np.cross(UA,[0,0,1]);ZA=np.array([0.,0.,1.]); M0=np.array([3.000961894323341,16.341923788646685,19.3]); S0=M0+1.50*UA
def parkmotor():
 f=[cyl('park geared 4to1',M0-24.70*UA,M0,3.),cyl('park output spindle',M0-.06*UA,S0+3.12*UA,.51),cyl('park cam blank',S0-.65*UA,S0+.65*UA,3.56)]
 f+=tube('park cam outboard bearing',S0+2.34*UA,S0+3.08*UA,.53,.88)
 f+=[rod('park motor saddle return',M0-21*UA-.9*ZA,np.array([-7.53,5.20,13.98]),.75),
     rod('park saddle knuckle return',np.array([-7.53,5.20,13.98]),np.array([-7.48,-.62,1.22]),.64),
     rod('park cam bearing tie',S0+2.84*UA+1.32*VA,pos(48,-6.6,15.4),.69)]
 f+=[rod('cam bearing to foot tie',pos(48,-6.6,15.4),pos(47,-6.63,15.25),.91)]
 return f
def dog(z):
 # Lateral offset so the return fork does not pass through the rotating cam.
 zz=S0[2]-z;axis=S0-zz*ZA;pc=np.array([W,WR-1.31,z]);out=[]
 out+=[cyl('park cam roller',axis-.58*UA,axis+.58*UA,.315),
       cyl('park roller axle',axis-.60*UA,axis+1.31*UA,.185),
       rod('park follower yoke',axis+1.19*UA,pc+1.19*UA,.44),
       rod('park offset plunger bridge',pc+1.19*UA,pc-.06*ZA,.40),
       cy('dog polished pin',2,(z-7.14,z-.21),(W,WR-1.31),.215)]
 return out
def sliders(a,an):
 px,rp,rd=link(an);out=[]
 for sg in (-1,1):
  ts=(sg*.78,sg*1.53)
  out+=[sol('centre clevis link '+str((a,sg)),[pos(a,x,r,t) for x,r in ((px,rp),(SLX,rd)) for t in ts],.91,U(a+90))]
 out+=[tg('slider link pin '+str(a),SLX,rd,(-2.49,2.49),a,.69)]
 for sg in (-1,1):
  out.append(sec('radial slide fork '+str((a,sg)),(SLX-1.21,SLX+.91),(rd-.85,rd+1.23),sorted((1.61*sg,2.50*sg)),a))
 out +=[sec('radial slide tie '+str(a),(SLX-2.19,SLX-.75),(rd+.11,rd+1.27),(-2.42,2.42),a),
       sec('axial transfer beam '+str(a),(-8.17,SLX-1.13),(rd-.39,rd+1.26),(-1.31,1.31),a),
       sec('face roller lug '+str(a),(-8.45,-7.53),(rd-2.65,rd+1.02),(-1.15,1.15),a),
       xy('face roller journal '+str(a),(-11.00,-7.61),rd-2,0,a,.71),
       xy('face roller '+str(a),(-10.83,-9.18),rd-2,0,a,.87)]
 # Crosshead backing plate with four X-reacting pads; pad separation
 # measured radially, not the axial spacing of tangential guide cheeks.
 out +=[sec('radial crosshead web '+str(a),(-7.91,-7.39),(rd-5.42,rd+.96),(-1.42,1.42),a)]
 for k in (-1,1):
  for nm,span in [('inner',(rd-5.34,rd-4.48)),('outer',(rd+.12,rd+.94))]:
   out.append(sec('crosshead X face '+str((a,k,nm)),(-7.97,-7.33),span,sorted((k*1.22,k*2.35)),a))
 return out
def chassis():
 f=joint()[0]+wall()+teeth()+sweep(dog(16.18),1.97*ZA)
 for a in BAZ:
  # Short key transverse reaction returned to quill INSIDE ribs, never an
  # aft strut crossing the moving rib. Two guides, both rib faces.
  f +=[sec('inner key web '+str(a),(5.25-O,7.72-O),(2.88,6.87),(-1.47,1.47),a)]
  for sg in (-1,1):f +=[sec('key positive face '+str((a,sg)),(5.23-O,7.70-O),(6.53,8.05),sorted((sg*1.16,sg*1.50)),a)]
 # Partial aft cantilevers at alternate clocks; rooted in fixed knuckle,
 # entirely behind rotor bridge before they turn forward along OD.
 for a in (-34.,143.,-141.):
  if a==-34:
   p0=pos(-34,-24.56,22.45);p1=pos(-42.5,-23.75,23.24);p2=pos(-42.5,-7.69,23.24)
   f += [rod('aft cantilever '+str(a),np.array([-7.52,0.,0.]),p0,.94),rod('cross rail detour',p0,p1,.65),
         rod('outer axial rail '+str(a),p1,p2,.65),rod('fixed wall heel '+str(a),p2,pos(-43,-6.55,15.20),.80)]
  else:
   p0=pos(a,-24.56,13.75);p1=pos(a,-21.80,18.55);p2=pos(a,-21.80,22.45)
   f += [rod('aft cantilever '+str(a),np.array([-7.52,0.,0.]),p0,.78),rod('aft cantilever dogleg '+str(a),p0,p1,.65),
         rod('cantilever radial step '+str(a),p1,p2,.64),rod('outer axial rail '+str(a),p2,pos(a,-7.66,22.75),.78),rod('fixed wall heel '+str(a),pos(a,-7.66,22.75),pos(a,-6.55,15.20),.92)]
   if a==143:
    del f[-2:]
    mid=pos(131,-14.92,22.90);nose=pos(129,-7.66,22.75)
    f +=[rod('outer axial rail dogleg 143',p2,mid,.70),rod('outer axial rail 143',mid,nose,.78),rod('fixed wall heel 129',nose,pos(129,-6.55,15.20),.92)]
 for a in AZ:
  for sg in (-1,1):
   # side ways on both X stations; rail flanks react transverse load.
   for x in (-6.64,-3.72):
    f +=[sec('slider guide cheek '+str((a,sg,x)),(x-.46,x+.46),(17.30,22.90),sorted((sg*1.45,sg*2.07)),a)]
   f +=[sec('way anchor '+str((a,sg)),(-6.94,-3.29),(15.07,20.84),sorted((sg*1.72,sg*2.18)),a)]
 for a in AZ:
  for sg in (-1,1):
   for i,xr in enumerate([(-8.43,-8.01),(-7.29,-6.88)]):
    f.append(sec('pitched X way '+str((a,sg,i)),xr,(13.05,22.44),sorted((sg*1.59,sg*2.24)),a))
   f.append(sec('X way outer cap '+str((a,sg)),(-8.43,-6.84),(13.08,21.80),sorted((sg*2.40,sg*2.86)),a))
   for xx in (-8.28,-7.05):
    f.append(sec('X way return '+str((a,sg,xx)),(xx-.09,xx+.09),(13.10,21.77),sorted((sg*2.13,sg*2.83)),a))
   f.append(sec('X way root '+str((a,sg)),(-7.12,-6.56),(15.06,16.48),sorted((sg*2.45,sg*3.28)),a))
 # Grounded ties from rear of hinge, not through annular working cam.
 f +=[rod('motor rear saddle spine',(-5.01,20.88,8.26),(-7.48,16.54,9.68),1.23),
      rod('motor rear mount',(-7.48,16.54,9.68),(-7.58,1.73,1.06),1.12),
      rod('worm outboard pillar',(W,WR+1.88,5.35),(W-1.75,24.38,9.62),.85),
      rod('worm fore bracket',(W+.64,24.45,-4.10),(O-6.63,20.81,-6.60),.94),
      rod('worm bearing yoke',(W,WR+1.88,-8.51),(W+.64,24.45,-4.10),.84),
      rod('worm bearing exterior rail',(W+.64,24.45,-4.10),(W-1.75,24.38,9.62),.89),
      rod('pin guide outboard tie',(W,WR-2.03,12.29),(W+1.72,WR-1.99,12.31),.39),rod('pin guide axial return',(W+1.72,WR-1.99,12.31),(W+1.72,WR-1.99,6.04),.41),rod('pin frame bearing return',(W+1.72,WR-1.99,6.04),(W+.93,WR-1.52,5.80),.45),
      rod('lower yaw motor rail',(-7.53,-17.64,-12.15),(-7.48,-.62,-1.22),.98),
      rod('upper yaw motor rail',(-7.53,-17.64,13.90),(-7.48,-.62,1.22),.98)]
 f +=[rod('worm carrier to fixed wall',(O-6.63,20.81,-6.60),pos(-17,-6.54,15.24),1.01)]
 for n,a,base in [('draw',-70.5,-34),('park',47.,143)]:
  f +=[sec(n+' ring steel limit',(-5.18-O,-4.25-O),(11.94,13.41),(-.47,.47),a),
       rod(n+' limit rear strut',pos(a,-4.85-O,12.83),pos(a,-6.93-O,13.72),.65),
       rod(n+' limit frame return',pos(a,-6.93-O,13.72),pos(base,-24.56,16.87),.75)]
 f +=[sec('ring phase sensor',(-6.44-O,-5.86-O),(11.03,12.53),(-1.49,1.49),96),
      rod('sensor frame return',pos(96,-6.20-O,11.98),pos(136,-24.56,12.62),.65)]
 return f
def lug(th):return sec('ring stop lug',(-4.92-O,-3.96-O),(12.12,13.16),(-.42,.42),-63+th)
def pads():
 f=[]
 for x,y in product((-14.8,8.3),(-7.8,7.8)):
  f +=[bx('foot '+str((x,y)),(x-1.12,x+1.12),(y-1.07,y+1.07),(-23.22,-22.12)),
       rod('foot rail '+str((x,y)),np.array([x,y,-22.17]),np.array([x+(.80 if x<0 else -1.2),y*(1.44 if x<0 and y<0 else 1.66),(-18.4 if x<0 and y<0 else -16.63)]),.93)]
  if x<0:
   f.pop()
   # Rear pads return along two actual under-cell box beams into the
   # FRONT wall ties. No rear upright through neighboring park lever.
   for z in (-22.85,-21.49):
    f.append(bx('foot cantilever skin '+str((y,z)),(x-.28,8.82),(y-1.21,y+1.21),(z,z+.28)))
   for oy in (-1.21,.90):
    f.append(bx('foot cantilever web '+str((y,oy)),(x-.28,8.82),(y+oy,y+oy+.31),(-22.60,-21.47)))
  else:
   v=np.array([x-1.2,y*1.66,-16.63])
   u=pos((-49 if y>0 else -131),-6.54,15.31)
   f.append(rod('foot forward tie '+str(y),v,u,.90))
 return f
def state(th):
 an,h=phase(th);return move(disk(),h)+[lug(th)]+sum((leaf(a,an)+sliders(a,an) for a in AZ),[])
def pack():
 return dict(label='exploratory',head_lip_world=O,pitch=P,table=-23.22,pivot=sh(H),fixed=chassis()+pads(),yaw_tail=move(tail(),-P)+joint()[1],cam_blank=annuli(),disk_home=disk(),closed=state(0),park=state(105))
if __name__=='__main__':
 q=pack();(D/'shell-model70.json').write_text(json.dumps(q,separators=(',',':'))+'\n');print([(k,len(v)) for k,v in q.items() if isinstance(v,list)])
