"""Rear drives, guides, body, battery and moving distal joint segment."""
from head82 import *
PIV=np.array([-30.0,4.30,0.]); GAMMA=137.
CELL=191.2; BOARD=314.; AXES=list(zip(PH,['sleeve','draw','eject']))
TN={'sleeve':-18.0,'draw':-19.85,'eject':-21.45}
XH={'sleeve':-16.95,'draw':-22.32,'eject':-31.96}
def drives(b):
 for a,g in AXES:
  def put(n,m,gr='fixed',mat='steel',kind='solid'):
   b.put(g+' '+n,loc(m,a),gr,mat,kind)
  sy=14.5;mz=7.92;tx=TN[g]
  put('0615 + 06/1',cyl((-31.85,.95),3.,sy,mz),'fixed','catalog','envelope')
  put('motor lead exit',box((.95,2.35),(sy-1,sy+1),(mz-.50,mz+.50)),'fixed','wire','reserve')
  put('motor shaft',cyl((-36.55,-31.85),.50,sy,mz))
  # Sliding opposed drive ears on independent torque tube; no side force rating transfer.
  hollow=ring((-39.77,-32.02),.535,.75,sy,mz)
  hollow-=box((-35.84,-35.14),(sy-.90,sy+.90),(mz-.20,mz+.20))
  put('hollow pinion shaft',hollow)
  put('coupling tang',box((-35.80,-35.18),(sy-.66,sy+.66),(mz-.18,mz+.18)))
  for k,x in enumerate([(-39.18,-37.98),(-34.84,-33.64)]):
   put('L415 '+str(k),ring(x,.752,2,sy,mz),'fixed','bearing','envelope')
   put('pinion bearing socket '+str(k),ring(x,2.0,2.50,sy,mz),'fixed','7075')
  # Actual root material and swept tooth volume tracked separately. Entire gear blank NOT billed as solid conflict with mating teeth.
  for tag,y,z,T,ri in [('pinion',sy,mz,16,.751),('wheel',sy,0.,56,1.501)]:
   pitch=T*.22/2; x=(-37.46,-35.36)
   put(tag+' root',ring(x,ri,pitch-.275,y,z))
   put(tag+' addendum sweep',ring(x,pitch-.275,pitch+.22,y,z),'fixed','steel','teeth')
  put('M3 screw',cyl((-41.4,-2.5),1.497,sy,0.),'fixed','steel','thread')
  # Back bearing and front steady separated; axial races face both directions.
  for k,x in enumerate([(-40.94,-37.94),(-5.97,-2.97)]):
   put('L730ZZ '+str(k),ring(x,1.50,3.50,sy,0),'fixed','bearing','envelope')
   put('radial bearing socket '+str(k),ring(x,3.5,4.00,sy,0),'fixed','7075')
  for k,x in enumerate([(-34.90,-31.40),(-30.60,-27.10)]):
   put('F3-8M '+str(k),ring(x,1.5,4.,sy,0),'fixed','thrust','envelope')
   put('thrust socket '+str(k),ring(x,4.,4.55,sy,0),'fixed','7075')
  for k,x in enumerate([(-35.32,-34.90),(-27.10,-26.65)]):
   put('seat shoulder '+str(k),ring(x,2.50,4.55,sy,0),'fixed','7075')
  put('shaft thrust flange',ring((-31.40,-30.60),1.49,3.06,sy,0))
  put('nut',ring((tx-1.75,tx+1.75),1.503,2.6,sy,0),g,'bronze','thread')
  put('offset nut web',box((min(tx,XH[g])-.20,max(tx,XH[g])+.20),(sy-2.49,sy-1.85),(-.90,.90)),g)
  inner={'sleeve':8.92,'draw':4.75,'eject':5.94}[g]
  put('output yoke',box((XH[g]-.36,XH[g]+.36),(inner,sy-1.88),(-.85,.85)),g)
  if g=='sleeve':put('aft tongue',box((-17.04,-15.08),(8.90,9.45),(-.85,.85)),g)
  # Forked axial guide runner outboard of nut; two fixed ways with finite span.
  put('runner',box((tx-5.35,tx+5.35),(16.95,18.15),(-1.,1.)),g)
  for k,(x0,x1) in enumerate([(tx-3.9,tx-2.9),(tx+2.9,tx+3.9)]):
   way=box((x0,x1),(16.80,18.58),(-1.44,1.44))-box((x0-.05,x1+.05),(16.70,18.18),(-1.03,1.03))
   put('way '+str(k),way,'fixed','bronze')
  # Motor bands and three-spoke bolted bearing deck.
  for k,x in enumerate([(-30.7,-29.6),(-3.55,-2.45)]):put('motor saddle '+str(k),ring(x,3.01,3.45,sy,mz),'fixed','7075')
  for k,x in enumerate([(-40.81,-40.17),(-34.46,-33.85),(-5.72,-5.04)]):
   # web deliberately relieved for bearings, tubes, mounting holes.
   w=box(x,(sy-4.28,sy+2.10),(-3.5,9.28))
   w-=cyl((x[0]-.1,x[1]+.1),4.57,sy,0)
   w-=cyl((x[0]-.1,x[1]+.1),3.50 if k==2 else 2.53,sy,mz)
   put('bearing deck '+str(k),w,'fixed','7075')
  put('gear dome',ring((-41.50,-35.33),6.47,6.87,sy,0),'fixed','PA12')
  # Open only mating sector of dome, not for protection of touching stock.
  nm=g+' gear dome';m,gr,mt,kind=b[nm];b[nm]=(m-loc(box((-42.,-35.),(sy-2.54,sy+2.54),(5.75,7.10)),a),gr,mt,kind)
  put('rear lid',ring((-41.94,-41.51),1.68,6.87,sy,0),'fixed','PA12')
  # Frame ground for driver travel limits; direct load must not bypass springs into cage.
  if g=='draw':
   put('input aft stop',box((tx-5.85,tx-5.35),(16.96,18.19),(-.97,.97)),'fixed','steel')
   put('input fore stop',box((tx+6.61,tx+7.00),(16.96,18.19),(-.97,.97)),'fixed','steel')
def raw(q):
 n,p,r,d=q;p=np.asarray(p)
 if r==0:return hull(p)
 if d is None:return union(M.sphere(r,24).translate(v) for v in p).hull()
 d=np.asarray(d);u=np.cross(d,np.eye(3)[np.argmin(abs(d))]);u=u/np.linalg.norm(u);v=np.cross(d,u)
 return hull([c+r*(cos(a)*u+sin(a)*v) for a in np.arange(64)*2*pi/64 for c in p])
def reserves(b):
 cat=json.load(open('catalog-reserves79.json'));put=b.put
 for k in ['yaw_fixed','yaw_turn']:
  for q in cat[k]:
   n=q[0];m=raw(q).translate([11.7,0,0]).rotate([0,0,GAMMA]).translate(PIV)
   put(n,m,'fixed' if k=='yaw_fixed' else 'yaw','catalog' if n=='yaw motor body' else 'steel','envelope' if 'motor body' in n or 'sector' in n else 'solid')
 # Explicit paired rigid paths housing to fixed knuckle, turning hub to own tail.
 for j in [-1,1]:
  u=PIV+np.array([-sin(radians(GAMMA)),cos(radians(GAMMA)),0])*2.35*j
  put('fixed hinge spine '+str(j),strut(u,[-15.7,9.98*j,0],1.14),'fixed','7075')
  put('tail fork link '+str(j),strut(PIV+[0,0,j*3.6],[-37.60,0,j*5.55],1.05),'yaw','7075')
 for i,(x,y) in enumerate(product((-32.,-7.),(-8.,8.))):
  put('foot '+str(i),box((x-1.7,x+1.7),(y-1.35,y+1.35),(-20.15,-19.4)),'fixed','PA12')
  put('foot post '+str(i),strut([x,y,-19.47],[x,y*.88,-13.8],.86),'fixed','7075')
 # Rotate entire cell incl tabs/insulators/protection as ONE assembly.
 o=np.mean(cat['elec'][0][1],axis=0)
 for q in cat['elec'][:24]:
  n=q[0];m=raw(q).translate(-o).transform([[0,1,0,0],[0,0,1,16.50],[1,0,0,0]]).translate([-18.6,0,0])
  put(n,loc(m,CELL),'fixed','cell' if n=='cell bulk' else 'electronics','reserve')
 # Re-layout controller and all non-cell boards; no eroding antenna reserve.
 ctr=[-19.70,15.30,0]
 for j,q in enumerate(cat['elec'][24:]):
  n=q[0];m=raw(q);ori=np.mean(q[1],axis=0)
  if j<2:
   ori=np.mean(cat['elec'][24][1],axis=0)
   m=m.translate(-ori).translate(ctr)
  else:
   sz=[(-6.64,15,1),(-16.5,20.50,1.),(-31.2,16.,1.2),(-32.7,15.,-5.55),(-8.5,18.0,-6.2),(-32.4,15.9,6.8)][j-2]
   m=m.translate(-ori).translate(sz)
  put(n,loc(m,BOARD),'fixed','electronics','air' if 'antenna' in n else 'reserve')
 put('fourth H bridge',loc(box((-11.15,-6.75),(13.4,15.3),(-8.0,-4.0)),BOARD),'fixed','electronics','reserve')
 # Removable formed U-shaped cell and PCB trays + side lids.
 for tag,ang,x,r,z in [('cell',CELL,(-35.10,-.91),(11.57,19.80),9.10),('pcb',BOARD,(-36.,-1.12),(11.78,19.65),8.65)]:
  shell=box(x,r,(-z,z))-box((x[0]+.42,x[1]-.42),(r[0]+.42,r[1]+.15),(-z+.42,z-.42))
  lid=box(x,(r[1],r[1]+.42),(-z,z))
  if tag=='pcb':
   for a0,a1,w,hi in [(-29.,-21.55,6.08,21.24),(-17.92,-15.05,3.89,24.16)]:
    lid-=box((a0+.40,a1-.40),(19.62,20.15),(-w+.4,w-.4))
    lid+=box((a0,a1),(19.68,hi),(-w,w))-box((a0+.40,a1-.40),(19.35,hi-.40),(-w+.40,w-.40))
  put(tag+' tray',loc(shell,ang),'fixed','PA12');put(tag+' service lid',loc(lid,ang),'fixed','PA12')
 # Distal cap on moving part, not a head-fixed box surrounding moving fork.
 put('tail shroud',ring((-37.04,-34.40),9.95,10.45),'yaw','PA12')
 # Split external clamshell, cropped at the feet; no invisible carveouts for clashes.
 center=[-21.02571,0,0]
 outer=M.sphere(29.90,96).translate(center)^box((-41.98,2.06),(-23.9,23.9),(-19.96,23.65))
 inner=M.sphere(29.44,96).translate(center)^box((-41.52,1.60),(-23.44,23.44),(-19.50,23.19))
 skin=outer-inner-cyl((1.50,2.2),11.03)-cyl((-42.2,-41.35),13.68)
 for a in PH:skin-=cyl((-42.3,-35.32),6.90,*at(14.5,a))
 for i,half in enumerate([(-31,-.02),(.02,31)]):
  put('outer clamshell '+str(i),skin^box((-43,3),half,(-21,26)),'fixed','PA12')
@lru_cache(None)
def book():
 b=Book();front(b);drives(b);reserves(b);return b
def pose(b,ph,t,yaw,guest=False):
 v=phase(ph,t);out={}
 for n,(m,g,mt,k) in b.items():
  if g=='guest' and not guest:continue
  if g=='coil':
   c,d=v['cage'][0],v['draw'][0];out[n]=m.translate([19.43,0,0]).scale([(4.63+d-c)/4.63,1,1]).translate([-19.43+c,0,0])
  else:out[n]=m.translate(-PIV).rotate([0,0,yaw]).translate(PIV) if g=='yaw' else m.translate(v[g])
 return out
