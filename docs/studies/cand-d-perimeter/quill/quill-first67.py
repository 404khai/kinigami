from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('quill-face67.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
# W=world X, local az about X. No inherited Take51 hinge, motor or fork.
W=O-14.24;WR=21.;H=np.array([-10.20,0.,0.]);JX=H[0];MOTOR_X=W-4.80;RKEY=10.68;DRUM_NORMAL=19.5
def wring(n,x,y,ri,ro,m=48,inner=False):
 return [washer(n+' '+str(j),(x,y),(ri,ri),(ro,ro),360*j/m,360*(j+1)/m,inner) for j in range(m)]
def annuli():
 return [('disk sleeve',O-20.29,O-9.07,9.78,13.19),
         ('quill bearing outer hub',-7.65,-.81,5.97,6.68),('aft rotor bridge',-4.18,-3.56,6.32,13.15),('aft rotor rim',-3.85,-3.06,11.93,13.15),
         ('face cam',O-11.69,O-9.04,12.89,20.84),('worm wheel web',W-.97,W+.97,12.91,18.77),('130T rim',W-1.29,W+1.29,18.56,19.80)]
def drum():return sum((wring(*q) for q in annuli()),[])
def joint():
 f=[];t=[];c0=lambda n,t,z,r:cy(n,2,z,(JX,t),r)
 f+=tube('yaw main steel knuckle',np.array([JX,0.,-2.08]),np.array([JX,0.,2.08]),1.91,3.71)
 f += [bx('knuckle tang',(JX+2.33,-6.85),(-2.45,2.45),(-1.91,1.91)),
       xy('fixed center quill',(-7.38-O,7.65-O),0,0,0,3.44)]
 for xl,xr in ((-7.45,-5.77),(-2.53,-.96)):
  for n,ri,ro in [('quill inner race',3.43,4.05),('quill rolling row',4.06,5.48),('quill outer race',5.49,6.02)]:
   f+=wring(n+str(xl),xl,xr,ri,ro,24)
 # Outer rings seat into rotating hub; stationary INNER race stops at shaft shoulder.
 f+=wring('shaft aft thrust shoulder',-7.78,-7.45,2.18,4.11,20)+wring('shaft front thrust shoulder',-.96,-.61,3.35,4.12,20)
 t +=[c0('yaw shaft',0,(-6.52,18.28),1.82)]
 for sg in (-1,1):
  z=sorted((sg*2.23,sg*4.46))
  t+=[sol('yaw fork blade '+str(sg),[[x,y,s*sg] for x,hy,zz in [(-16.45,2.85,(1.96,4.42)),(-12.38,2.20,(2.23,4.46)),(-10.52,1.79,(2.23,4.46))] for y in (-hy,hy) for s in zz]),
      c0('yaw fork hub '+str(sg),0,z,2.76)]
 # Keyed shaft transmits to driven sector above motor. Teeth blanks are
 # swept enclosures, not solid full wheel or interference in the mesh.
 for j in range(12):
  a,b=np.radians((42+j*8,50+j*8));t.append(sol('yaw 70T sector '+str(j),[(JX+r*cos(q),r*sin(q),z) for q,r,z in product((a,b),(2.1,7.25/cos((b-a)/2)),(16.98,18.28))]))
 t +=[c0('yaw keyed sector hub',0,(16.94,18.32),2.65)]
 f +=[c0('yaw motor body',8.80,(-16.50,16.30),3.0),c0('yaw pinion',8.80,(16.99,18.25),1.99),
      c0('yaw pinion shaft',8.8,(16.18,18.28),.71),
      rod('yaw motor lower saddle',(JX+1.27,7.13,-14.70),(-7.08,6.43,-14.70),1.38),
      rod('yaw motor upper saddle',(JX+1.27,7.13,13.90),(-7.08,6.43,13.90),1.38)]
 return f,t
def teeth():
 f=[]
 f += [cy('worm teeth blank',2,(-3.52,3.52),(W,WR),1.80),cy('worm shaft',2,(-18.01,10.15),(W,WR),.93),
       cy('worm 32T spur',2,(-17.91,-16.35),(W,WR),3.43),cy('motor 16T spur',2,(-17.90,-16.36),(MOTOR_X,WR),1.79),
       cy('clamp motor',2,(-14.73,18.07),(MOTOR_X,WR),3.0),cy('clamp pinion quill',2,(-17.94,-14.63),(MOTOR_X,WR),.78)]
 for lo,hi in ((-15.95,-14.51),(-6.34,-3.71),(3.72,6.34)):
  f+=tube('worm independent bearing',np.array([W,WR,lo]),np.array([W,WR,hi]),.96,2.08)
 f+=tube('clamp pinion bearing',np.array([MOTOR_X,WR,-16.19]),np.array([MOTOR_X,WR,-14.81]),.82,1.38)
 # Spring-return pin parked along worm shaft (+Z); straight sidewalls hold
 # with no axial wedging once strictly past entry chamfer into index plate.
 sx=W+3.56;sy=WR
 f +=[cy('16 hole parking plate blank',2,(7.15,8.70),(W,WR),4.53),
      cy('parking pin swept',2,(6.93,14.90),(sx,sy),.44),
      cy('parking armature swept',2,(10.46,16.03),(sx,sy),.93),
      cy('parking spring reserve',2,(14.02,19.13),(sx,sy),1.41)]
 for n,z0,z1,ri,ro in [('bolt bush',8.81,10.37,.46,1.12),('retract coil',10.45,17.95,1.11,2.26),('spring cup',16.0,19.61,1.46,1.86)]:
  f+=tube(n,np.array([sx,sy,z0]),np.array([sx,sy,z1]),ri,ro)
 f +=[cy('parking spring cap',2,(19.13,19.65),(sx,sy),1.83),bx('parking read switch',(sx-1.38,sx+1.38),(sy+1.40,sy+2.32),(14.0,16.69))]
 return f
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
 return out
def chassis():
 f=joint()[0]+wall()+teeth()
 for a in BAZ:
  # Short key transverse reaction returned to quill INSIDE ribs, never an
  # aft strut crossing the moving rib. Two guides, both rib faces.
  f +=[sec('inner key web '+str(a),(5.25-O,7.72-O),(2.88,6.87),(-1.47,1.47),a)]
  for sg in (-1,1):f +=[sec('key positive face '+str((a,sg)),(5.23-O,7.70-O),(6.53,8.05),sorted((sg*1.16,sg*1.50)),a)]
 # Partial aft cantilevers at alternate clocks; rooted in fixed knuckle,
 # entirely behind rotor bridge before they turn forward along OD.
 for a in (-41.,83.,-157.):
  f +=[rod('aft cantilever '+str(a),np.array([JX+1.95,0.,0.]),pos(a,-23.31,20.22),1.06),
       rod('outer axial rail '+str(a),pos(a,-23.31,20.22),pos(a,-7.66,21.92),.96),
       rod('fixed wall heel '+str(a),pos(a,-7.66,21.92),pos(a,-6.55,15.20),1.02)]
 for a in AZ:
  for sg in (-1,1):
   # side ways on both X stations; rail flanks react transverse load.
   for x in (-6.90,-3.72):
    f +=[sec('slider guide cheek '+str((a,sg,x)),(x-.62,x+.62),(17.30,22.90),sorted((sg*1.45,sg*2.07)),a)]
   f +=[sec('way anchor '+str((a,sg)),(-6.94,-3.29),(15.07,20.84),sorted((sg*1.72,sg*2.18)),a)]
 # Grounded ties from rear of hinge, not through annular working cam.
 f +=[rod('motor rear saddle spine',(-5.01,20.88,8.26),(-6.56,16.54,9.68),1.23),
      rod('motor rear mount',(-6.56,16.54,9.68),(-8.28,2.13,1.06),1.12),
      rod('worm outboard pillar',(W,WR+1.65,5.26),(W+1.02,23.22,10.03),.85),
      rod('worm fore bracket',(W+1.02,23.22,10.03),(O-7.23,19.64,8.92),.94),
      rod('worm bearing yoke',(W,WR+1.63,-5.01),(W+.64,23.54,-3.04),.84),
      rod('worm bearing exterior rail',(W+.64,23.54,-3.04),(W+1.02,23.22,10.03),.89),
      rod('coil bracket',(W+5.07,21.78,12.61),(W+1.02,23.22,10.03),.80),
      rod('lower yaw motor rail',(-7.08,6.43,-14.70),(-7.46,2.22,-1.22),.98),
      rod('upper yaw motor rail',(-7.08,6.43,13.90),(-7.46,2.22,1.22),.98)]
 return f
def pads():
 f=[]
 for x,y in product((-10.1,10.65),(-8.7,8.7)):
  f +=[bx('foot '+str((x,y)),(x-1.12,x+1.12),(y-1.07,y+1.07),(-23.9,-22.49)),
       rod('foot rail '+str((x,y)),np.array([x,y,-22.69]),np.array([x+(.80 if x<0 else -1.2),y*1.66,-16.63]),.93)]
 return f
def state(th):
 an,h=phase(th);return move(disk(),h)+sum((leaf(a,an)+sliders(a,an) for a in AZ),[])
def pack():
 return dict(label='exploratory',head_lip_world=O,pitch=P,table=-23.9,pivot=sh(H),fixed=chassis()+pads(),yaw_tail=move(tail(),-P)+joint()[1],cam_blank=annuli(),disk_home=disk(),closed=state(0),park=state(105))
if __name__=='__main__':
 q=pack();(D/'quill-model67.json').write_text(json.dumps(q,separators=(',',':'))+'\n');print([(k,len(v)) for k,v in q.items() if isinstance(v,list)])
