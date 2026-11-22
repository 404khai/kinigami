from plug75 import *
ref=json.loads((D/'reference75.json').read_text())
ref['electrical']=[trans(q,[-.60,.62,0]) if q[0].startswith(('BMD antenna','controller board')) else q for q in ref['electrical']]
def band(n,a,l,h,i,o,half,nn=10):return rg(n,l,h,i,o,nn,a-half,a+half)
def facebody():
 f=[]
 for a in AZ:
  f+=ways(a)+roof(a)
  # Full fixed annular sectors beyond the plug cheek. Overlap cheek
  # material without filling the sliding slot: wall overwritten only on
  # the three narrow accessible socket windows. Front is continuous.
  for k in (-1,1):
   for l,h in ((-8.65,-1.095),(-1.095,-.075),(-.075,0)):
    for j in range(8):
     u=a+k*(10.9+j*49.1/8);v=a+k*(10.9+(j+1)*49.1/8);w=[]
     for x,q in product((l,h),(u,v)):
      w +=[pos(q,x,bore(x)),pos(q,x,15.89/cos(radians(49.1/16)))]
     f.append(sol('fixed continuous case '+str((a,k,j,l)),w))
  f+=band('rear radial gusset',a+40,-13.18,-12.73,5.5,15.85,7)
 # Enclose the moving ring, not the entire powered body in a hollow box.
 f+=rg('bearing liner',-7.05,-5.00,21.627,21.91)+rg('cam cover sleeve',-7.62,-4.76,21.87,22.16)
 for l,h in ((-7.39,-7.05),(-5.01,-4.72)):
  f+=rg('removable thrust cap',l,h,21.24,22.11)
 for a in (22,195,260):
  f+=band('rear idler cap tie',a,-10.23,-7.33,21.86,22.15,6,4)
  f+=[rod('cover pillar '+str(a),pos(a,-7.97,22.19),pos(a,-12.88,15.72),.55),
      rod('central motor frame tie '+str(a),pos(a+54,-13.0,6.10),pos(a+54,-22.91,3.93),.61)]
 # Smooth screw-fastened rear cover cap includes pierced guide spokes;
 # actual section, not a plane recovered by support extrapolation.
 f+=sum((band('rear bush carrier',a,-13.20,-12.76,4.50,7.05,11,4) for a in BAZ),[])
 for a in BAZ:
  f +=[rod('outboard bush strut '+str(a),pos(a,-12.9,10.29),pos(a+17,-12.90,15.74),.57),
       rod('forward bush strut '+str(a),pos(a,-9.22,9.98),pos(a,-8.66,12.17),.60)]
 # Diagram stock for plated metal ring fastening ears; no adhesive credit.
 for a in (12,132,252):
  f+= [cyl('cover screw head '+str(a),pos(a,-7.94,22.12),pos(a,-7.41,22.12),.74),cyl('cover screw shank '+str(a),pos(a,-7.62,22.12),pos(a,-5.34,22.12),.29)]
 return f
def motor(n,x,y,z0,z1,r=3):return cy(n,2,(z0,z1),(O+x,y),r)
def mounts():
 f=[]
 for a in (8,172,-119):
  ends=(pos(a,-23.20,4.73),pos(a,-12.99,14.30))
  f.append(rod('rear frame rib '+str(a),*ends,.78))
 f +=[rod('hinge frame tang',[-8.13,0,0],pos(180,-23.8,2.8),.92)]
 return f
# Worm and clamp spur in tangential plane near +Y; gears never unmesh.
WX=-9.11;WY=19.90;MX=WX-4.80
def jawdrive():
 f=[motor('jaw worm shaft',WX,WY,-17.93,12.76,.88),motor('jaw worm blank',WX,WY,-3.64,3.64,1.89),
    motor('jaw 32T driven spur',WX,WY,-17.83,-16.28,3.42),motor('jaw 16T driver',MX,WY,-17.82,-16.29,1.79),
    motor('jaw geared 256',MX,WY,-14.75,18.05),motor('jaw motor spindle',MX,WY,-17.85,-14.61,.73),
    motor('parking star',WX,WY,8.20,9.66,2.75)]
 for l,h in ((-15.20,-13.84),(-8.,-6.34),(4.06,5.76),(10.32,11.88)):
  f+=tube('jaw worm fixed bearing',np.array([O+WX,WY,l]),np.array([O+WX,WY,h]),.91,1.46)
 # Machined shaft shoulder and keyed outboard nut capture the fixed
 # bushing faces; .015 axial play each way, not guaranteed under load.
 f +=[motor('jaw thrust shoulder',WX,WY,3.72,4.045,1.60),motor('jaw retained thrust collar',WX,WY,5.775,6.18,1.60),
      rod('jaw thrust bush tie',pos(0,WX,22.15,5.12),pos(0,WX,21.23,5.12),.37)]
 f +=[rod('jaw motor chassis mount',pos(0,MX,19.2,7.5),pos(0,-14.3,14.80,6.2),.89),
      rod('jaw motor cross rail',pos(0,-14.3,14.80,6.2),pos(30,-13.04,14.50),.8)]
 return [trans(q,1.02*Z) if q[0].startswith(('jaw 32T','jaw 16T','jaw motor spindle','jaw geared')) else q for q in f]
# Axial screw with 24T wheel and second, independent tangential worm.
SX=-12.62;SY=5.10;DX=SX+4.80
def origin_eject():
 f=rg('disk 24T worm gear',SX-.90,SX+.90,1.44,3.90,32)
 f+=rg('disk nut journal',SX-2.03,SX+2.03,1.44,2.55,32)
 for l,h in ((SX-2.12,SX-.94),(SX+.94,SX+2.12)):
  f+=rg('disk thrust bearing',l,h,2.57,3.33,24)
 f+=[motor('disk worm shaft',SX,SY,-13.85,8.49,.80),
    motor('disk worm blank',SX,SY,-3.24,3.24,1.80),motor('disk worm 32T',SX,SY,-13.83,-12.38,3.41),
    motor('disk drive 16T',DX,SY,-13.82,-12.39,1.79),motor('disk geared 4',DX,SY,-10.89,13.81),
    motor('disk drive spindle',DX,SY,-13.85,-10.79,.72)]
 for l,h in ((-11.89,-10.46),(4.46,5.85)):
  f+=tube('disk worm fixed bearing',np.array([O+SX,SY,l]),np.array([O+SX,SY,h]),.82,1.27)
 return f
# Straight shear pin parks the input worm at two ring positions. Spring
# closes ONLY the brake; it cannot close the jaws. 64:1 auxiliary gearmotor
# positively displaces it with a captive cam. Shaft canted in the XY plane
# well above the nose rather than an exposed tooth or guessed coil pull.
def spin(q,m,off):
 n,v,r,d=q;return sol(n,np.array(v)@m.T+off,r,None if d is None else m@d)
def ejectdrive():
 a=radians(-158.69);m=np.array([[1.,0,0],[0,cos(a),-sin(a)],[0,sin(a),cos(a)]])
 a=radians(135.62);m2=np.array([[cos(a),-sin(a),0],[sin(a),cos(a),0],[0,0,1]])
 f=[];c=np.array([O+SX,SY,0]);off=ND+.09*X
 for q in origin_eject():
  n=q[0]
  if n.startswith(('disk geared','disk drive 16','disk drive spindle','disk motor truss')):q=spin(q,m2,c-m2@c)
  if n.startswith(('disk geared','disk drive 16','disk drive spindle','disk worm 32')):q=trans(q,-2.65*Z)
  f.append(spin(q,m,off))
 # Move the aft worm journal with the shifted spur; the shaft now
 # spans both bearings and the gear face instead of ending before it.
 f=[q for q in f if q[0]!='disk worm shaft']
 f.append(spin(motor('disk worm shaft',SX,SY,-16.62,8.49,.80),m,off))
 return f
AX=np.array([cos(radians(84)),sin(radians(84)),0.]);AT=np.cross(Z,AX)
S=np.array([O+WX,WY-2.08,17.65])-2.85*AX-2.1*X;MC=S-1.60*AX+3.6*AT+4.80*Z
def park():
 f=[cyl('dog geared 64',MC-30.10*AX,MC,3.0),cyl('dog spindle',S-2.94*AX,S+3.98*AX,.52),cyl('dog driven spur',S+1.12*AX,S+2.28*AX,3.22),cyl('dog input spindle',MC-.04*AX,MC+3.96*AX,.50),cyl('dog input spur',MC+2.72*AX,MC+3.88*AX,3.22),
    cyl('dog blind cam',S-.72*AX,S+.72*AX,3.44)]
 f+=tube('dog outboard bearing',S+2.62*AX,S+3.72*AX,.54,.91)
 c=np.array([O+WX,WY-2.08,0.])
 for l,h in ((10.01,10.84),(11.98,12.91)):
  f+=tube('dog bush',c+l*Z,c+h*Z,.369,.76)
 for k in (-1,1):
  f.append(rod('dog spring cap pillar '+str(k),c+k*1.40*AT+12.37*Z,c+k*1.40*AT+18.96*Z,.235))
 f.append(cyl('dog spring cap',c+18.85*Z,c+19.15*Z,1.54))
 f.append(cyl('dog spring reserve',c+15.04*Z,c+18.85*Z,.91))
 f+=[rod('brake bearing tie',S+3.30*AX+.75*AT,pos(53,-7.41,21.91),.48),
     rod('brake motor return',MC-26.11*AX+1.60*Z,pos(90,-23.93,8.7),.71)]
 return f
def dogmove(z):
 c=S-z*Z;pc=c+2.85*AX+2.1*X
 return [motor('parking pin',WX,WY-2.08,pc[2]-6.80,pc[2]+.41,.35),cyl('dog spring foot',pc+.14*Z,pc+.42*Z,.91),
  cyl('parking cam roller',c-.69*AX,c+.69*AX,.28),cyl('parking cam axle',c-.76*AX,c+1.14*AX,.17),
  rod('parking yoke bridge',c+1.02*AX,pc,.32)]
def bushholes(a):
 # Solid end stops for disk ejection. Axially split detachable collar
 # and matching axial bore, installed from rear *after* posts enter.
 return tube('disk terminal collar '+str(a),pos(a,-21.93,8.58),pos(a,-21.35,8.58),1.085,1.59)
def tails():
 ret=[]
 for q in ref['tail']:
  if q[0].startswith(('button near-mid','plunger shank','captive foot','inner stem')):ret+=sweep([trans(q,-.4*X)],.65*X)
  else:ret+=[q]
 return ret
def allstock():
 return ref['fixed']+facebody()+mounts()+diskfixed()+jawdrive()+ejectdrive()+park()+sweep(dogmove(3.03),2.04*Z)+drive()+sum((sweep(plug(a),ST*U(a)) for a in AZ),[])+sweep(plate()+sum((bushholes(a) for a in BAZ),[]),TR*X)+ref['electrical']
if __name__=='__main__':
 data=dict(label='exploratory',reference='38 pitch; lip world 17.04',fixed=ref['fixed']+facebody()+mounts()+diskfixed()+jawdrive()+ejectdrive()+park(),disk_home=plate()+sum((bushholes(a) for a in BAZ),[]),disk_throw=TR,plugs_lock=sum((plug(a) for a in AZ),[]),plug_throw=ST,cam_blanks=drive(),tail=ref['tail'],electrical=ref['electrical'])
 (D/'installed75.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
 print('frozen finite stock',[(k,len(v)) for k,v in data.items() if isinstance(v,list)])
