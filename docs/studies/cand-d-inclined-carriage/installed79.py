from key79 import *
ref=json.loads((D/'catalog-reserves79.json').read_text())
PITCH=38.; H=np.array([-27.,0.,0])
JR=H-np.array([-11.7,0.,0]);SH=np.array([-15.20,-.70,-.1])
def clamp(x,l,h):return max(l,min(h,x))
def by(n,xy,z,r):return cyl(n,(xy[0],xy[1],z[0]),(xy[0],xy[1],z[1]),r)
def lip():
 # Actual tube x from bulkhead to lip. Separate an angular/axial
 # slot for the registry shoe and bridge. All other barrel remains.
 f=[]
 for lo,hi in ((-9.15,-6.85),(-6.85,-.18),(-.18,0.)):
  for j in range(96):
   u=(j+.5)*2*pi/96
   if abs(sin(u))<.30 and cos(u)>0 and hi<0:continue
   w=sol('barrel '+str((lo,j)),[(x,r*cos(k*2*pi/96),r*sin(k*2*pi/96)) for x,r,k in product((lo,hi),(14.05,15.05/cos(pi/96)),(j,j+1))])
   f.append(w)
 f+=frontguides()
 # Removable four-way cage around all three bands. Keep original rows
 # physically supported by ribs away from the working flats.
 for z in (-1,1):
  f+=[bx('guide tie '+str(z),(XB-.48,XB-.08),(4.50,16.60),sorted((z*1.82,z*2.31))),
      bx('outer guide tie '+str(z),(XF+.08,XF+.50),(4.50,16.60),sorted((z*1.82,z*2.31)))]
  for y in (5.04,12.32,15.92):
   f.append(cyl('guide bulkhead strut '+str((y,z)),(XB-.32,y,2.02*z),(-9.55,y+1.2,4.92*z),.42))
 # rear bulkhead four sectors and clear R5.00 around y=-.618 ram.
 f+=ann('rear bore bulkhead',[-9.65,-.618,0],[-9.15,-.618,0],5.02,14.50,64)
 # fixed blind roof and side walls over forward key shoe. Taper the
 # forward lower roof at the lip; do not stretch over central socket.
 f+=[bx('removable high roof',(-12.9,-.25),(24.14,24.49),(-4.25,4.25)), bx('forward roof return',(-.53,-.18),(14.21,24.42),(-4.22,4.22))]
 for k in (-1,1):f.append(bx('hood cheek '+str(k),(-12.9,-.18),(13.96,24.40),sorted((k*3.96,k*4.29))))
 return f
def seatstock():
 f=[]
 for a in (60,180,300):
  r=cos(radians(a))*T+sin(radians(a))*Z;t=-sin(radians(a))*T+cos(radians(a))*Z
  # rear tower supports: extruded along D until global x=-9.15
  def pt(h,y,z):return O+h*U+y*r+z*t
  def back(y,z):return (-9.15-pt(0,y,z)[0])/U[0]
  f.append(sol('inclined tower '+str(a),[pt(h,y,z) for y,z in product((8.95,11.65),(-3.81,3.81)) for h in (back(y,z),-2.68)]))
  for k in (-1,1):
   t0=datum['seat_local']['face_start_t'];v=tan(radians(65));eq=[[1,0,0,-2.12],[-1,0,0,0],[1,v,0,-v*11.65],[1,-v,0,v*8.95],[1,0,-k*v,t0*v],[1,0,k*v,-3.81*v]]
   # tangent support outer approximation to the radial crest trim.
   for ang in np.arange(0,360,6):
    eq.append([1,tan(radians(64))*cos(radians(ang)),tan(radians(64))*sin(radians(ang)),-12.2*tan(radians(64))])
   q=poly('inclined V metal '+str((a,k)),eq,[.08,10.3,k*2.6])
   f.append(sol(q[0],[pt(h-2.68,y,z) for h,y,z in q[1]]))
 return f
def tail():
 G=np.asarray(datum['registry']);c=np.asarray(datum['stem']);s=[rod('integral lug',Q,Q,2.50)]
 for i in range(2):s.append(rod('lug neck '+str(i),c[i],c[i+1],1.40))
 for a,p in zip((60,180,300),G):s.append(rod('solid wing '+str(a),p,[2.50,6.25*cos(radians(a)),6.25*sin(radians(a))],2.50))
 v=[(x,r*cos(2*pi*j/48)/cos(pi/48),r*sin(2*pi*j/48)/cos(pi/48)) for x,r in ((2.5,7.6),(5.8,3.16)) for j in range(48)]
 s.append(sol('rolled fork hub',v,2.5))
 for k in (-1,1):s.append(sol('socket fork '+str(k),[(x,y*sg,k*z) for x,y,l,h in ((4,3.3,1.70,5.08),(6.75,2.15,3,6.45),(11.46,1.45,4.31,6.66)) for sg,z in product((-1,1),(l,h))]))
 return s
def ejection():
 return [ax('78 moving ram face reserve',0,-9.15,-8.15,(-.618,0),4.10),ax('78 ram sleeve allowed reserve',0,-21.25,-9.15,(-.618,0),4.96)]
# Rear cage transmits only Y at front crowned axle; floating X slots.
RX=-12.30; ZR=7.65; CMAX=8.07; PLAY=3.22; SX=-15.9
def platform(s):
 f=[]
 for k in (-1,1):
  z=k*ZR;t=abs(z)
  f+=[bx('output shoe upright '+str(k),(RX-1.15,RX+.95),(1.16,18.88),sorted((z+k*2.31,z+k*3.29))),
      bx('output spring foot '+str(k),(RX-2.14,RX+2.14),(-.19,.80),sorted((z-k*2.12,z+k*2.95))),
      bx('pullback receiver '+str(k),(RX-1.15,RX+.95),(16.07,17.29),sorted((z+k*.1,z+k*2.51)))]
  for y in (4.06,13.44):f.append(bx('rear runner land '+str((k,y)),(RX-1.22,RX+1.02),(y,y+1.03),sorted((z+k*2.16,z+k*3.36))))
  f.append(rod('offset yoke arm '+str(k),np.array([RX+.36,17.70,z+k*2.72]),np.array([RX+.36,17.70,3.07*k]),.77))
  for sy in (-1,1):f.append(bx('pickup slot lip '+str((k,sy)),(XC-1.15,XC+1.16),sorted((17.70+sy*.716,17.70+sy*1.16)),sorted((k*2.04,k*3.66))))
  f +=[bx('pickup slot aft bridge '+str(k),(XC-1.56,XC-1.14),(16.54,18.86),sorted((k*2.04,k*3.66))),
       bx('pickup slot front closure '+str(k),(XC+1.16,XC+1.58),(16.54,18.86),sorted((k*2.04,k*3.66))),
       bx('long pull fork '+str(k),(RX+.08,XC-1.26),(17.01,18.39),sorted((k*2.40,k*3.64)))]
 return move(f,s*Y)
def rearways():
 f=[]
 for k in (-1,1):
  z=k*(ZR+2.76)
  # stationary ways continuous in Y so two MOVING bearing bands stay
  # fully captured. Spur, coils and cup are inboard of the side rails.
  for lo,hi in ((RX-1.64,RX-1.236),(RX+1.036,RX+1.45)):
   f.append(bx('rear X-way '+str((k,lo)),(lo,hi),(3.89,19.56),sorted((z-k*.48,z+k*.48))))
  f.append(bx('rear outer cheek '+str(k),(RX-1.63,RX+1.44),(3.91,19.52),sorted((z+k*.616,z+k*1.05))))
  for y in (4.29,14.13):
   f +=[rod('rear way support '+str((k,y)),[RX-1.58,y,z+k*.71],[-18.7,y-.60,z+k*.9],.68)]
 return f
def driver(c):
 f=[]
 for k in (-1,1):
  z=k*ZR
  f+=[bx('moving spring roof '+str(k),(RX-2.00,RX+2.00),(12.20,12.84),sorted((z-k*1.94,z+k*1.94))),
      bx('driver pickup ledge '+str(k),(RX-1.02,RX+.85),(12.74,12.85),sorted((z+k*.21,z+k*1.89))),
      rod('driver roof tie '+str(k),[SX,12.54,2.15*k],[RX,12.54,z],.76)]
 f+=ann('antirotating input nut',[SX,11.15,0],[SX,13.85,0],1.44,2.20,24)
 return move(f,c*Y)
def springs(s,c):
 return [ax('compression coil reserve '+str(k),1,.80+s,12.20+c,(RX,k*ZR),1.99) for k in (-1,1)]
def ramfixed():return [ejection()[1]]
def safeties():
 f=[]
 for k in (-1,1):
  z=k*ZR
  # Stops are between driver and fixed chassis, not in the key path.
  f += [bx('driver close end stop '+str(k),(RX-2.05,RX-1.32),(11.55,12.20),sorted((z-k*1.86,z-k*.94))),
        bx('driver park end stop '+str(k),(RX-2.05,RX-1.32),(12.84+CMAX,13.56+CMAX),sorted((z-k*1.86,z-k*.94))),
        rod('fixed stroke stop column '+str(k),[RX-2.43,11.87,z-1.25*k],[RX-2.43,21.32,z-1.25*k],.55)]
 return f
if __name__=='__main__':
 print('counts, key/seat/tail, head/ways, output and driver',len(keyplus()),len(seatstock()),len(tail()),len(lip()+rearways()),len(platform(0)),len(driver(0)))
