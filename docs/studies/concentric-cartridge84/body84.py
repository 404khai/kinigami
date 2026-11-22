"""Concentric ring-nut, screw cartridges, pinned power-off selector, split enclosure."""
from head84 import *
import drive82 as old
from scipy.spatial import ConvexHull
SANG=91.55; DANG=246.; EANG=156.; CAMANG=57.; CELL=196.; PCB=303.8; GAMMA=137.
ECLK=125.85; EFACE=-34.45; SCLK=69.
EC=np.array([-4.95,2.23])
def yz(r,a):return np.asarray(at(r,a))
def shaft(b,n,x,r,yz0,gr='fixed'):b.put(n,cyl(x,r,*yz0),gr)
def sleeve_drive(b):
 put=b.put;bear=(-25.4,-20.4)
 put('cross roller CRBT205A',ring(bear,10.001,15.5),'fixed','bearing','envelope')
 h=ring((-25.82,-19.99),15.50,16.04)
 for x in [(-25.83,-25.40),(-20.40,-20.00)]:h+=ring(x,13.55,15.72)
 h-=cyl((-20.45,-19.80),1.83,*at(13.5,CAMANG))
 put('cross roller support split',h,'fixed','7075')
 # Nut housing/journals are one rotating part. The bore is minor/root
 # envelope, not an empty annular gap credited as a transmitting thread.
 nut=ring((-25.72,-17.90),9.65,9.990)+ring((-22.85,-20.0),8.74,9.82)
 nut+=ring((-25.78,-25.40),9.82,11.45)+ring((-20.40,-19.89),9.82,11.45)
 flange=ring((-19.90,-17.90),9.82,14.925)
 for a in np.arange(20)*18+CAMANG:flange-=cyl((-20.0,-17.8),.85,*at(13.50,a))
 put('rotating hollow nut',nut+flange,'nut','steel','thread')
 put('102T teeth',ring((-19.90,-17.90),14.925,15.6),'fixed','steel','teeth')
 # Remote motor, clearance tang in separately bearing-supported shaft, 1:1 rear transfer.
 relay=yz(17.40,SANG);mot=relay+yz(5.76,SANG+SCLK)
 motor(b,'sleeve',mot,-35.65)
 gears(b,'sleeve transfer',(-38.39,-37.04),[(mot,24,.24,.751),(relay,24,.24,.751)])
 shaft(b,'sleeve relay axle',(-39.84,-16.48),.749,relay)
 for i,x in enumerate([(-39.82,-38.62),(-36.90,-35.70),(-17.70,-16.50)]):bearing(b,'relay L415 '+str(i),x,relay,.751,2.0)
 gears(b,'sleeve reduction',(-19.90,-17.90),[(relay,14,.30,.751)])
 pin=yz(13.50,CAMANG)
 for i,x in enumerate([(-20.35,-19.95),(-17.65,-16.05)]):
  bearing(b,'sleeve lock bushing '+str(i),x,pin,.825,1.40,1.80)
 shaft(b,'sleeve index pin',(-20.32,-14.62),.80,pin,'spin')
def bearing(b,n,x,p,ri,ro,h=None):
 b.put(n,ring(x,ri,ro,*p),'fixed','bearing','envelope')
 b.put(n+' seat',ring(x,ro,ro+.38 if h is None else h,*p),'fixed','7075')
def motor(b,n,p,face):
 b.put(n+' 0615/06-1',cyl((face,face+32.8),3,*p),'fixed','catalog','envelope')
 b.put(n+' wire',cyl((face+32.8,face+33.7),.83,*p),'fixed','wire','reserve')
 for i,u in enumerate([.28,28.05]):b.put(n+' motor band '+str(i),ring((face+u,face+u+1.1),3.01,3.40,*p),'fixed','7075')
 shaft(b,n+' gearhead axle',(face-4.18,face),.50,p)
 q=ring((face-4.20,face-.06),.535,.750,*p)
 q-=box((face-2.56,face-2.14),(p[0]-.8,p[0]+.8),(p[1]-.22,p[1]+.22))
 b.put(n+' floating torque tube',q)
 b.put(n+' coupling key',box((face-2.53,face-2.17),(p[0]-.72,p[0]+.72),(p[1]-.185,p[1]+.185)))
 for i,x in enumerate([(face-4.09,face-2.89),(face-1.26,face-.06)]):bearing(b,n+' pinion L415 '+str(i),x,p,.752,2.)
def gears(b,n,x,centers):
 for i,(p,t,m,bore) in enumerate(centers):
  root=t*m/2-1.25*m;ro=t*m/2+m
  b.put(n+' root '+str(i),ring(x,bore,root,*p))
  b.put(n+' teeth '+str(i),ring(x,root,ro,*p),'fixed','steel','teeth')
def screws(b):
 for tag,center,ang in [('eject',EC,EANG),('draw',yz(17.70,DANG),DANG)]:
  ej=tag=='eject';c=center;p=c+yz(9.60 if ej else 7.92,ang if ej else ang+89)
  mot=p+yz(6.72,ang-61) if ej else p
  if ej:
   mot=yz(19.55,ECLK);delta=mot-c;v=delta/np.linalg.norm(delta)
   al=(9.60**2-6.72**2+delta@delta)/(2*np.linalg.norm(delta))
   p=c+al*v+sqrt(9.60**2-al**2)*np.array([-v[1],v[0]])
  mf=EFACE if ej else -35.60;gx=(mf-2.75,mf-1.39)
  motor(b,tag,mot,mf)
  if ej:
   gears(b,'eject train',gx,[(c,42,.24,1.501),(p,38,.24,.751),(mot,18,.24,.751)])
   shaft(b,'eject relay axle',(mf-4.27,mf-.04),.749,p)
   for i,x in enumerate([(mf-4.09,mf-2.89),(mf-1.26,mf-.06)]):bearing(b,'eject idle L415 '+str(i),x,p,.751,2.)
  else:gears(b,'draw train',gx,[(c,56,.22,1.501),(p,16,.22,.751)])
  front=-13.9 if ej else -7.20
  shaft(b,tag+' M3 screw',(gx[0]-3.18,front),1.496,c)
  bearing(b,tag+' rear L730',(gx[0]-3.13,gx[0]-.13),c,1.5,3.5)
  for i,x in enumerate([(-35.24,-31.74),(-31.04,-27.54)]):
   bearing(b,tag+' F3-8M '+str(i),x,c,1.50,4.0)
  b.put(tag+' thrust flange',ring((-31.74,-31.04),1.49,3.13,*c))
  for i,x in enumerate([(-35.60,-35.24),(-27.54,-27.18)]):
   b.put(tag+' thrust abutment '+str(i),ring(x,2.65,4.37,*c)-(cyl((-27.26,-27.0),10.0)-cyl((-27.29,-26.9),7.49)) if ej else ring(x,2.65,4.37,*c),'fixed','7075')
  if not ej:
   bearing(b,'draw nose L730',(-10.52,-7.52),c,1.50,3.50)
   b.put('draw nut',ring((-14.35,-11.85),1.503,2.54,*c),'draw','bronze','thread')
   # Load path from outboard nut around (not through) the rotating hollow skirt.
   runner=box((-33.38,-12.76),(17.14,18.16),(4.97,5.99))

   runner+=box((-13.44,-12.79),(17.14,18.16),(2.15,5.75))
   runner+=box((-14.15,-13.75),(17.90,19.15),(5.12,5.95))
   pts=json.load(open('routes84.json'))['draw'];b.put('draw wrap yoke',loc(runner.mirror([0,0,1]),ang)+union(strut(p,q,.65) for p,q in zip(pts,pts[1:])), 'draw')
   for i,x in enumerate([(-29.6,-28.3),(-17.05,-15.75)]):
    w=box(x,(16.73,18.58),(4.57,6.39))-box((x[0]-.1,x[1]+.1),(17.10,18.20),(4.93,6.03))
    b.put('draw runner way '+str(i),loc(w.mirror([0,0,1]),ang),'fixed','bronze')
   for i,x in enumerate([(-14.55,-14.15),(-12.46,-12.06)]):b.put('draw input stop '+str(i),loc(box(x,(18.50,19.27),(-5.96,-5.13)),ang))
  else:
   # Front cantilever from thrust cartridge, added radial steady before last thread.
   b.put('eject nose bronze bush',ring((-27.54,-26.33),1.514,1.95,*c),'fixed','bronze')
def transfer(b):
 # Dual captive plate cams on a separately supported tangential shaft.
 # Normal-offset groove around sampled polar centerline (not a command latch).
 a=CAMANG-36.;C=np.array([-12.55,14.12,0.]);ts=[14.65,17.65]
 def wrap(m):return loc(m.translate(C),a)
 def put(n,m,g='fixed',mat='steel',kind='solid'):b.put(n,wrap(m),g,mat,kind)
 def dis(th,i):
  x=max(0,min(1,((th*(1 if i==0 else -1))-12)/55))
  return (2.62 if i==0 else 2.62)*x*x*(3-2*x)
 for i,t in enumerate(ts):
  poly=[];p2=[]
  for th in np.linspace(-180,180,360,endpoint=False):
   # Each groove returns to hold on opposite unused semicircle.
   ang=min(180-abs(th),abs(th))*(1 if th>0 else -1)
   r=5.44-dis(ang,i);u=np.array([-cos(radians(th)),sin(radians(th))])
   poly.append(u*(r+.422));p2.append(u*(r-.422))
  loop=CrossSection([(np.array(poly[::-1])+np.array(p2[::-1]))/2]); cs=loop.offset(.424)-loop.offset(-.424)
  q=zpin(0,0,(t,t+1.0),6.16)-cs.extrude(1.16).translate([0,0,t-.08])
  # Continuous steel backing closes the groove axially.
  q+=zpin(0,0,(t-.44,t+.02),6.16)
  put(('sleeve' if i==0 else 'draw')+' closed cam',q,'cam')
  g='spin' if i==0 else 'dpin'
  put(g+' follower',zpin(-5.44,0,(t+.07,t+1.63),.38),g)
  end=np.array([-5.44,0.,t+1.58])+C
  if i==0:
   v=yz(13.5,CAMANG);dst=np.array([-14.74,*v])
  else:
   # Positive drawer hold remote from the sleeve; index holes in draw screw disk.
   pv=yz(17.70,DANG)+yz(5.18,DANG-45)
   dst=np.array([-34.36,*pv]);shaft(b,'draw index pin',(-38.74,-34.24),.67,pv,g)
   shaftc=yz(17.70,DANG);disk=ring((-38.35,-36.99),1.499,5.85,*shaftc)
   for deg in [DANG-45,DANG-45-(1.29/.5*360)]:disk-=cyl((-38.42,-36.90),.722,*(shaftc+yz(5.18,deg)))
   del b['draw train root 0']; b.put('draw index disc',disk,'drot')
   for j,x in enumerate([(-38.78,-38.42),(-36.89,-35.27)]):bearing(b,'draw lock bush '+str(j),x,pv,.70,1.05)
  v=np.r_[end[0],loc(M.cube([.001]*3).translate(end),a).bounding_box()[1:3]]
  # Serviceable bolted pushlink; review entire long draw linkage for physical route.
  put(g+' slider shoe',box((-8.87,-5.10),(-.44,.44),(t+1.25,t+1.98)),g)
  way=json.load(open('routes84.json'))[g];b.put(g+' return fork',union(strut(p,q,.34 if i==0 else .36) for p,q in zip(way,way[1:])),g,'steel')
  for j,x in enumerate([(-20.58,-20.08),(-18.60,-18.10)]):
   put(g+' cam follower guide '+str(j),box((x[0]+12.55,x[1]+12.55),(-.79,.79),(t+1.18,t+2.31))-box((x[0]+12.45,x[1]+12.65),(-.50,.50),(t+1.10,t+2.08)))
 # Separate commanded angular travel ±73 deg; face cam cannot be driven axially out of dwell.
 put('selector 0615/06-1',zpin(0,0,(-20.59,12.21),3),'fixed','catalog','envelope')
 put('selector motor key',zpin(0,0,(12.21,16.61),.50))
 put('cam spindle',zpin(0,0,(12.40,20.48),.75)-zpin(0,0,(12.33,16.74),.53))
 for j,t in enumerate([12.55,19.17]):
  put('cam spindle L415 '+str(j),zpin(0,0,(t,t+1.20),2)-zpin(0,0,(t-.1,t+1.3),.752),'fixed','bearing','envelope')
 return a,C
def subsy(b):
 base=Book();old.PIV=PIV;old.GAMMA=GAMMA;old.reserves(base)
 for n,(m,g,mt,k) in base.items():
  if n.startswith(('outer clamshell','tail shroud','tail fork','cell tray','pcb tray','cell service','pcb service','foot','fixed hinge spine')):continue
  if mt in ('cell','electronics') or n=='fourth H bridge':
   cell=n in [q[0] for q in json.load(open('catalog-reserves79.json'))['elec'][:24]]
   if cell:m=loc(loc(m,-old.CELL).translate([-2.88,2.47,0]),CELL)
   else:
    q=loc(m,-old.BOARD)
    if n in ['controller board incl LDO SWD','BMD antenna air reserve']:q=q.translate([19.70,-15.30,0]).translate([-29.3,18.17,.90])
    else:
     mid=(np.array(q.bounding_box()[:3])+q.bounding_box()[3:])/2
     places={'coupler H-bridge':((0,0,0),[-24.43571,21.745,-.825]),'independent cutoff':((90,0,0),[-17.05208,19.32,-3.42]),
       'yaw H-bridge':((0,0,0),[-18.15,17.245,3.76364]),'interface flex reserve':((0,90,0),[-26.15,21.62,5.33]),'parking motor bridge':((0,0,90),[-25.315,19.45,-6.825]),
       'fourth H bridge':((0,0,90),[-19.51667,18.42,-1.62857]),'bus connector':((0,0,90),[-16.925,20.365,3.75])}
     ang,trg=places[n];q=q.translate(-mid)
     if n in ('independent cutoff','interface flex reserve'):q=q.rotate([90,0,0])
     q=q.rotate(ang).translate(trg)
    m=loc(q,PCB)
  b.put(n,m,g,mt,k)
 for j in (-1,1):
  b.put('turn fork '+str(j),strut(PIV+[0,0,j*3.6],[-PITCH+2.80,0,j*5.55],.89),'yaw','7075')
  b.put('fixed hinge link '+str(j),strut(PIV+[0,1.95,j*1.5],[-25.83,8.9,j*12.7],.76),'fixed','7075')
 b.put('tail fairing',ring((-PITCH+3.12,-PITCH+5.22),9.90,10.45),'yaw','PA12')
def shell(b):
 center=[-21.0,0,0]
 outer=M.sphere(29.77,96).translate(center)^box((-41.55,-3.90),(-24,24),(-21.65,25.25))
 inner=M.sphere(29.32,96).translate(center)^box((-41.10,-4.35),(-23.55,23.55),(-21.20,24.80))
 # Bevel both ends vs tangential width. Cut returns actual cover thickness,
 # not just the shared volume at LOCK. Same analytic planes sweep all yaw pairs.
 for sign in [-1,1]:
  normal=(1,sign*.28,0);outer=outer.trim_by_plane(normal,-39.97+sign*.28*PIV[1])
  inner=inner.trim_by_plane(normal,-39.51+sign*.28*PIV[1])
 # Locally closed drive blisters. Use the convex stock envelope, never erode a
 # motor to make the cover pass. Nested outer & inner hulls connect to split shell.
 pods=[]
 for tag in ('sleeve','draw','eject'):
  group=[tag+' 0615/06-1',tag+' wire',tag+' motor band 0',tag+' motor band 1',tag+' floating torque tube',tag+' pinion L415 0 seat']
  pods.append(group)
 for ns in [['draw index disc','draw train teeth 0','draw rear L730 seat','draw lock bush 0 seat','draw lock bush 1 seat','draw train teeth 1'],
            ['eject train teeth 0','eject rear L730 seat'],['eject train teeth 1','eject idle L415 0 seat','eject idle L415 1 seat'],['eject train teeth 2'],
            ['relay L415 0 seat','sleeve transfer teeth 1','sleeve transfer teeth 0'],['selector 0615/06-1','selector motor key']]:pods.append(ns)
 # Disks are bounded irrespective of polar orientation by their full circumscribed OD.
 pods.append(['sleeve closed cam','draw closed cam','cam spindle L415 1'])
 oo=[outer];ii=[inner]
 for ns in pods:
  pts=np.vstack([mesh(b[n][0]) for n in ns if n in b]);qq=pts[ConvexHull(pts).vertices]
  for target,delta in [(oo,.35),(ii,.09)]:
   target.append(hull(np.vstack([qq+off for off in product(*[(-delta,delta)]*3)])))
 outer=union(oo)^M.sphere(29.88,120).translate([-20.97,0,0]);inner=union(ii)^M.sphere(29.805,120).translate([-20.97,0,0])
 skin=outer-inner-cyl((-43,-35.22),11.15)-cyl((-4.5,-3.7),11.10)
 # Replace a completely open service aperture by the screwed cell panel, not two nested lids.
 for tag,a,x,rr,w in [('cell',CELL,(-38.04,-3.78),(13.72,22.0),9.08),('pcb',PCB,(-37.90,-14.70),(15.72,22.90),8.70)]:
  pocket=box((x[0]+.38,x[1]-.38),(rr[0]+.38,35),(-w+.38,w-.38));tray=box(x,rr,(-w,w))-pocket
  tray-=box((-26.02,-17.70),(rr[0]-.06,16.26),(-w-.1,w+.1))
  lid=box(x,(rr[1],rr[1]+.36),(-w,w))
  if tag=='pcb':
   air=loc(b['BMD antenna air reserve'][0],-a)
   x0,y0,z0,x1,y1,z1=air.bounding_box()
   innerp=box((x0-.10,x1+.10),(rr[1]-.1,y1+.12),(z0-.10,z1+.10))
   outerp=box((x0-.45,x1+.45),(rr[1]+.02,y1+.46),(z0-.45,z1+.45))
   roof=M.sphere(29.86,120).translate([-20.97,0,0]);innerroof=M.sphere(29.74,120).translate([-20.97,0,0])
   # Close the rear blister with material BETWEEN curved, concentric roofs.
   cap=(outerp^roof)-(innerp^innerroof)
   lid=(lid-innerp)+cap
   lid=lid^roof
  skin-=loc(box((x[0]-.15,x[1]+.15),(rr[0]-.13,40),(-w-.15,w+.15)),a)
  # Screw tabs on short ends would protrude into neighbor; locate along long sides.
  for i,xx in enumerate(([-27.0,-15.2] if tag=='cell' else [-30.2,-19.9])):
   z=(w+1.32)*(1 if i==0 else -1);y=rr[1]
   lid+=box((xx-1.62,xx+1.62),(y,y+.36),(min(z-1.60,w-.06) if i==0 else z-1.60,z+1.60 if i==0 else -w+.06))
   skin-=loc(box((xx-2.09,xx+2.09),(y-3.1,40),(z-2.09,z+2.09)),a)
   hole=M.cylinder(9,1.055,1.055,N).rotate([-90,0,0]).translate([xx,y-5,z])
   lug=box((xx-1.56,xx+1.56),(y-2.82,y), (z-1.48,z+1.48))-hole
   lid-=hole;b.put(tag+' screw lug '+str(i),loc(lug,a),'fixed','7075')
   sh=M.cylinder(3.35,.985,.985,N).rotate([-90,0,0]).translate([xx,y-2.81,z])
   cap=M.cylinder(.66,1.50,1.50,N).rotate([-90,0,0]).translate([xx,y+.36,z])
   socket=M.cylinder(.69,1.30/sqrt(3),1.30/sqrt(3),6).rotate([-90,0,0]).translate([xx,y+.49,z])
   b.put(tag+' M2 screw '+str(i),loc((sh+cap)-socket,a))
  # Mold longitudinal wells around installed catalog bodies; these are open scallops,
  # not evidence of enclosure strength. Verify continuous lid/pack extraction separately.
  clear=['yaw motor body','draw 0615/06-1','selector 0615/06-1','draw motor band 0','draw motor band 1','lower yaw motor rail','fixed hinge link -1','draw pinion L415 0 seat','draw pinion L415 1 seat','BMD antenna air reserve'] if tag=='pcb' else ['draw index disc','draw train teeth 0','draw runner way 0','draw runner way 1','draw M3 screw','draw F3-8M 0 seat','draw F3-8M 1 seat']
  for name in clear:
   mm=loc(b[name][0],-a);vv=mesh(mm);vv=vv[ConvexHull(vv).vertices];hole=hull(np.vstack([vv+o for o in product(*[(-.13,.13)]*3)]));tray-=hole
   if name=='selector 0615/06-1' or name=='yaw motor body':lid-=hole
  if tag=='cell':
   for tab in [n for n in b if n.startswith('folded tab') and n.endswith(('4)','5)'))]:
    vv=mesh(loc(b[tab][0],-a));vv=vv[ConvexHull(vv).vertices]
    # Open-ended 0.13 mm clearance pockets for real folded contacts, not shaved cell parts.
    tray-=hull(np.vstack([vv+o for o in product((-.13,.13),(-.13,16.),(-.13,.13))]))
  b.put(tag+' cassette',loc(tray,a),'fixed','PA12');b.put(tag+' lid',loc(lid,a),'fixed','PA12')
 for i,(x,y) in enumerate(product([-31.,-9.6],[-6.4,6.4])):
  b.put('foot '+str(i),box((x-1.70,x+1.70),(y-1.35,y+1.35),(-25.55,-25.09)),'fixed','PA12')
 # Retain the rotating tail flange/fairing: provide a swept shroud aperture in fixed skin.
 for name in ['own flange','own eject boss','tail fairing']:
  vv=mesh(b[name][0]);vv=vv[ConvexHull(vv).vertices]
  pts=[]
  for deg in range(-15,16,3):
   th=radians(deg);w=(vv-PIV)@np.array([[cos(th),sin(th),0],[-sin(th),cos(th),0],[0,0,1]])+PIV;pts.extend(w)
  vv=np.asarray(pts);vv=vv[ConvexHull(vv).vertices];skin-=hull(np.vstack([vv+o for o in product(*[(-.13,.13)]*3)]))
 for tag,a in [('cell',CELL),('pcb',PCB)]:
  skin-=b[tag+' lid'][0].hull()
 for i,h in enumerate([(-30,-.018),(.018,30)]):b.put('clamshell '+str(i),skin^box((-44,1),h,(-25,27)),'fixed','PA12')
@lru_cache(None)
def book():
 b=Book();local(b);sleeve_drive(b);screws(b);transfer(b);subsy(b);shell(b);return b
def pose(b,p,t,yaw,guest=False,selector=None):
 v=phase(p,t);dc=v['draw'][0];ds=v['sleeve'][0]
 unlock=p=='UNLOCK' and t>1/3 and t<1
 draw=p=='DRAW' and 0<t<1 or p=='UNLOCK' and 0<t<1/3
 th=selector if selector is not None else (73 if unlock else (-73 if draw else 0));out={}
 for n,(m,g,mt,k) in b.items():
  if g=='guest' and not guest:continue
  if g=='yaw':q=m.translate(-PIV).rotate([0,0,yaw]).translate(PIV)
  elif g in ('nut','drot'):
   ctr=np.array([0,*(yz(17.70,DANG) if g=='drot' else [0,0])]);q=m.translate(-ctr).rotate([(-720*ds if g=='nut' else 720*dc),0,0]).translate(ctr)
  elif g=='cam':
   a=CAMANG-36.;C=np.array([-12.55,14.12,0.])
   q=loc(loc(m,-a).translate(-C).rotate([0,0,th]).translate(C),a)
  elif g in ('spin','dpin'):
   u=np.clip(((th if g=='spin' else -th)-12.)/55.,0,1);q=m.translate([2.62*u*u*(3-2*u),0,0])
  elif g=='coil':
   c=v['cage'][0];q=m.translate([16.16,0,0]).scale([(4.63+dc-c)/4.63,1,1]).translate([-16.16+c,0,0])
  else:q=m.translate(v[g])
  out[n]=q
 return out
