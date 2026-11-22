from latch79 import *
# Turn the Geneva input axis 270 degrees around Z to clear the ram
# reservation. Relay its input to a separately supported geared motor.
GIN=LC+np.array([-C,0.]); IDL=GIN+np.array([-6.0,0]); MOT=IDL+np.array([-6.0,0])
def wheelphase(v,a):return np.asarray(v)@rot2(radians(270+a)).T+LC
def cutcells():
 # conservative inscribed material voxels in the lobes, not a mass upper.
 # For wider support and continuous motions use the surrounding clean disk.
 l=[];h=.22
 for x in np.arange(-RO,RO,h):
  for y in np.arange(-RO,RO,h):
   r=hypot(x+h/2,y+h/2);delta=h/sqrt(2)
   if r+delta>RO or max(abs(x+h/2),abs(y+h/2))-delta<.646:continue
   good=True
   for j in range(4):
    u,v=rot2(-j*pi/2)@np.array([x+h/2,y+h/2])
    if hypot(u,v+C)<BR+.028+delta or (abs((u+v)/sqrt(2))<GSLOT+delta and (u-v)/sqrt(2)>C-AR-.45-delta):good=False;break
   if good:l.append((x,y,h))
 return l
def indexdrive():
 f=[ax('remote index 0615 256',2,-13.58,19.22,MOT,3.00)]
 for n,c,r in (('motor',MOT,.68),('idler',IDL,.74),('index',GIN,.82)):
  lo=-19.40 if n=='index' else -16.29
  f.extend([ax(n+' relay shaft',2,lo,-13.51,c,r),ax(n+' 30T relay',2,-15.20,-14.02,c,3.19)])
  for z in ((-18.7,-18.20),(-13.26,-12.69)) if n!='motor' else ((-15.97,-15.42),):
   f+=ann(n+' relay outrigger '+str(z[0]),[*c,z[0]],[*c,z[1]],r+.025,r+.57,20)
 f.append(ax('index shaft carrier wheel',2,-18.11,-17.31,GIN,4.49))
 return f
def regmat(angle=0):
 # Base angle at lock: pin outside, pointing AWAY from wheel. Sector
 # opposite it is uncut on ±73 degrees; side relief admits wheel on index.
 p=GIN-AR*X[:2];f=[ax('drive pin at rear dwell',2,-17.40,-15.62,p,PIN)]
 for j in range(36):
  a,b=np.radians((-74+148*j/36,-74+148*(j+1)/36));f.append(sol('driver blocking material '+str(j),[(GIN[0]+r*cos(t),GIN[1]+r*sin(t),z) for t,r,z in product((a,b),(.83,BR),ZW)]))
 return f
def production():
 f=[q for q in screwdriver() if q[0] not in ('shaft crown 18 teeth','screw lower journal','motor fuse spindle','key 0615 256')]+[ax('screw supported journal',1,4.24,7.18,(SX,SZ),1.24)]
 f +=[ax('key 0615 256',1,-15.93,16.87,(MX,MZ),3.0),ax('motor drive tang',1,16.77,19.36,(MX,MZ),.48),
      ax('separate pinion axle',1,19.53,26.15,(MX,MZ),.80)]
 # Loose square-ended coupling approximated by fin/ears on separate shafts;
 # imposes torque and is NOT credited as a radial bearing.
 f += [bx('drive external tang',(MX-.73,MX+.73),(18.83,19.97),(MZ-.29,MZ+.29))]
 for k in (-1,1):f.append(bx('drive ear '+str(k),(MX-.75,MX+.75),(19.00,20.14),sorted((MZ+k*.34,MZ+k*.73))))
 f += [ax('pinion coupling foot',1,19.98,20.35,(MX,MZ),1.19)]
 for lo,hi in ((20.61,22.22),(24.13,25.75)):
  f+=ann('pinion bronze bushing '+str(lo),[MX,lo,MZ],[MX,hi,MZ],.817,1.53,24)
  f.append(cyl('pinion bushing tab '+str(lo),[MX-1.31,(lo+hi)/2,MZ],[MX-3.44,(lo+hi)/2,MZ+.55],.60))
 return f
def waystock():
 # Leave the outer rail open through the trunnion route. End wraps only.
 f=[]
 for q in rearways():
  if q[0].startswith('rear outer cheek'):
   lo,hi=ext(q,np.eye(3));a,b=lo[1],hi[1]
   for c,d in ((a,7.25),(14.45,b)):
    f.append(bx(q[0],(lo[0],hi[0]),(c,d),(lo[2],hi[2])))
  else:f.append(q)
 return f
def bridge(c):
 f=[]
 for q in car(0):
  if q[0].startswith(('moving spring roof','catch ledge','spring roof root')):
   continue
  if q[0]=='spring input crossmember':
   f.append(bx(q[0],(SX+1.79,SX+2.40),(12.19,12.89),(-ZR-.66,SZ+.48)))
  else:f.append(q)
 for k in (-1,1):
  z=k*ZR
  f+=ann('bored spring cap '+str(k),[RX,12.20,z],[RX,12.84,z],1.36,2.08,32)
  f+=[bx('spring cap rear root '+str(k),(SX+.65,RX-1.39),(12.19,12.89),(z-.64,z+.64)),
      bx('catch ledge '+str(k),(RX-1.02,RX+.85),(12.20,12.85),sorted((z+k*1.42,z+k*1.89)))]
 return move(f,c*Y)
def followers(s):
 return out(s)+[ax('spring core guide '+str(k),1,.50+s,15.22+s,(RX,k*ZR),1.29) for k in (-1,1)]
def fixed():
 return lip()+seatstock()+waystock()+safeties()+fixedguide()+production()+blocks()+indexdrive()+regmat()
def enclosure():
 # Smooth fixed *external* pod blanks; do not remove intersections or
 # claim arbitrary holes are inaccessible. Motor service side is split.
 f=[bx('rear cover roof',(-29.90,-12.70),(24.16,24.50),(-14.,14.0)),
    bx('rear cover back',(-31.00,-30.61),(4.1,18.05),(-17.0,18.95)),
    bx('rear bearing cover front',(-6.90,-6.56),(9.85,18.90),(4.35,17.30)),
    bx('index relay base guard',(-31.0,-12.49),(8.31,15.63),(-19.96,-19.52)),
    bx('index rotor lower guard',(-16.68,-4.89),(7.04,16.99),(-19.95,-19.51)),
    bx('drive gear outer guard',(-24.94,-11.93),(26.40,26.78),(6.00,13.94))]
 for k in (-1,1):f.append(bx('latch side shelter '+str(k),(-16.56,-5.26),(7.12,16.99),sorted((k*15.20,k*15.57))))
 return f
def regions():
 f,e,t=rest()
 return dict(head=fixed(), shell=enclosure(), body=f, elec=e, tail=t,ram=ramfixed()+sweep(ejection()[:1],9.35*X),front=sweep(keyplus(),S*Y),rear=sweep(followers(0),S*Y),input=sweep(bridge(0),CMAX*Y),coil=springs(0,CMAX),index=[ax('index lock wheel profile reserve',2,*ZW,LC,RO),ax('index pin orbit reserve',2,-17.40,-15.62,GIN,AR+PIN)]+eccentric(0)+eccentric(90))
def boxbounds(A):return np.array([ext(a,np.eye(3)) for a in A])
def reportpair(name,a,b):
 p=bpair(a,b,2);print(name,repr(p))
def tests():
 r=regions()
 for n,m in [('front','elec'),('front','shell'),('input','shell'),('front','ram'),('rear','ram'),('index','ram'),('head','ram'),('index','elec'),('rear','head'),('input','head'),('front','head'),('head','elec'),('shell','elec')]:reportpair(n+'/'+m,r[n],r[m])
 print('shaft / spring cap lock physical witness',bpair([q for q in eccentric(0) if q[0]=='index shaft'],bridge(0),2))
 for n,m in [('tail','elec'),('tail','head')]:
  for a in (-15,0,15):print(n,m,a,pairs(yaw(r[n],a),r[m]))
 # Real stroke seating at body heel on +Y / -Y. These sweeps do NOT
 # certify functioning if obstructed by another installed part.
 for st in (0,S):
  kp=move(keyplus(),st*Y);print('key vs guide boxes',st,pairs(kp,[q for q in lip() if 'nose guide' in q[0]]))
 rpo=move(keyplus(),S*Y);rp=sweep(ejection()[:1],9.35*X)
 print('park key vs entire tentative ram face stroke',pairs(rpo,rp))
if __name__=='__main__':tests()
