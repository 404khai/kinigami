from package79 import *
rat=radians(18);c,sn=U[:2];Rlug=2.5
YC=Y0+R;KC=(Rlug+R-sn*(YC-Q[1]))/c+Q[0]
def branch(angle):
 t=radians(angle)
 d=(KC-Q[0]-(Rlug+R)*cos(t))/c
 st=Q[1]+d*sn+(Rlug+R)*sin(t)-YC
 return st,d
def reaction(st,d,ang,slip,vel,mg=.12):
 t=radians(ang);n=np.array([cos(t),sin(t)])
 fx,fy=n+slip*.23*np.array([sin(t),-cos(t)])
 x,y=(Q+d*U)[:2]+Rlug*n
 M=(x-XC)*fy-y*fx
 # Count the actual two loaded rows; no baseline squeeze from the third.
 # +q is X-normal on the aft shank; -q is X-normal on fore (full).
 # Re-evaluate face-specific pressure bands incl proximal joint debit.
 rear=keyseam(0)[1]
 variants=[]
 for i,j in ((0,1),(1,2),(0,2)):
  for si,sj in product((-1,1),repeat=2):
   def ys(k,sg):
    a,b=ROWS[k];lo=(rear if sg>0 else (Y0+R))+st
    return [y for u,v in ((lo,13.+st),(13.70+st,18.92+st)) for y in (max(a,u),min(b,v)) if min(b,v)>max(a,u)]
   for yi,yj in product(ys(i,si),ys(j,sj)):
    # moment of Coulomb drag is linear in q_i for centered shank.
    y1=yi-vel*mg*(XF-XC);y2=yj-vel*mg*(XF-XC)
    q2=(M+y1*fx)/(y2-y1);q1=-fx-q2
    if si*q1 < -1e-8 or sj*q2 < -1e-8:continue
    drag=mg*(abs(q1)+abs(q2))
    variants.append((vel*drag-fy,abs(q1)+abs(q2),(i,j),(si,sj)))
 return variants
def loads():
 v=[]
 for ang in np.linspace(18,90,361):
  st,d=branch(ang)
  for sl,vel in product((-1,1),repeat=2):
   for A in reaction(st,d,ang,sl,vel):v.append((*A,ang,sl,vel))
 for st in np.linspace(0,branch(18)[0],51):
  for sl,vel in product((-1,1),repeat=2):
   for A in reaction(st,st*sn,18,sl,vel):v.append((*A,18,sl,vel))
 print('two-row centered branch samples, per unit N (NOT a three-row upper), force sign +Y')
 for vv in (1,-1):
  l=[q for q in v if q[-1]==vv]
  print(vv,'least and greatest actuator force, max guide sum',min(l),max(l),max(l,key=lambda q:q[1]))
 for a in (18,48,84,90):
  st,d=branch(a)
  print('theta stroke pair directions feasible at mu ±',a,round(st,4),sorted(set((A[2],A[3]) for sl in (-1,1) for A in reaction(st,d,a,sl,1))))
 # carried moment from offset yoke: actual spring/driver overhang, incl
 # returning open hard lips on rear projection. Conservative conditional
 # bound for two planar moving X bands no opposing assembly squeeze.
 p=13.44-(4.06+1.03);h=1.24;e=abs(XC-(RX-.1))+.05;mg=.12
 fac=(2*e/p)/(1-2*mg*h/p)
 print('rear offset key positive load applied at pickup; guide normal per transmitted Y, added drag fraction',fac,mg*fac)
def sizes():
 k,lf,solid=springvalues()
 # intentionally independent example tolerance intervals, not production data
 # largest output park 4.88, min driver -0.05, ΔL ±.10 and free ±.10.
 Lmin=11.40-.05-4.88-.10;LmaxL=11.4+.05+.12+.1
 Fcap=2*k*1.10*(lf+.10-Lmin)
 print('conditional spring min length/solid plus .10/max force',Lmin,solid+.10,Fcap)
 print('LOCK centered worst spring min/max under ±10% rates, free ±.10, installed ±.10, seating ±.12 and stop ±.05',2*k*.90*(lf-.10-LmaxL),2*k*1.10*(lf+.10-(11.4-.05-.12-.1)))
 cf=3.35/.55;wahl=(4*cf-1)/(4*cf-4)+.615/cf
 print('spring wire peak Wahl shear under conditional cap (not a rating)',8*(Fcap/2)*3.35*wahl/(pi*.55**3))
 # Thread torque at FULL load both directions, include plain thrust ring,
 # mean radius 1.56 mm ISO 60deg included, provisional same mu=.15.
 rm=1.56;lead=.60;fmu=.15;rl=atan(lead/(2*pi*rm));rho=atan(fmu/cos(radians(30)));rc=1.90
 tplus=rm*tan(rho+rl)+rc*.10;tminus=rm*tan(rho-rl)+rc*.10
 Tupper=min(.156*256*.60,25)*2*.88
 print('thread torque coefficients driving / lowering Nmm per N',tplus,tminus,'optimistic motor continuous via gear efficiencies, Nmm',Tupper,'push max N before rails',Tupper/tplus)
 # Gearbox shaft force for actual torque at pinion pitch radius 1.8.
 # Upper capacity upstream torque does not imply permitted radial force.
 for f in (20.43,Fcap,80):
  torque=f*tplus;fg=torque/(3.6*.88*cos(radians(20)))
  print('screw thrust N / screw torque Nmm / one-ended gearhead pinion radial N vs .5 N catalog',f,torque,fg)
 # TRUNNION load: all on one side, no fictitious equal sharing.
 FN=60.;pin=1.48;span=12.485-11.55;J=pi*pin**3/32
 print('60N trunnion illustrative: bending MPa, shear MPa, projected roller contact MPa, crossbar root cantilever MPa',FN*span/J,FN/(pi*pin**2/4),FN/(pin*1.27),FN*abs(XC-RX)/(2*1.24*1.38**2/6))
 # Positive two-force latch on rolling trunnion; friction and bush load
 # adverse. Coaxial Geneva spans a nonlinear index with max Jacobian.
 v=ec(0)-PC;n=v/np.linalg.norm(v);arm=ec(0)-LC;Tn=abs(arm[0]*n[1]-arm[1]*n[0]);Tt=abs(arm@n)
 measured_J=AR/(C-AR);print('nominal zero-motion latch contact N from 60N +Y ignoring friction',60/n[1])
 # coincident current at exact index angle when roller unseats over center.
 for deg in (0,1,4,8,16):
  alpha=radians(deg-45)
  # pin angle t obeys (sin(t+alpha)=C sin(alpha)/AR).
  t=asin(np.clip(C*sin(alpha)/AR,-1,1))-alpha
  J=(AR*(C*cos(t)-AR))/(C*C+AR*AR-2*C*AR*cos(t))
  cen=ec(deg);xy=cen-PC
  # Under the stated +Y load the trunnion actually follows the finite
  # eccentric envelope; solve true circle contact at fixed trunnion X.
  st=xy[1]-sqrt((ROLL+R0)**2-xy[0]**2);pc=PC+[0,st];nn=(cen-pc)/(ROLL+R0)
  pole=cen-R0*nn;rr=pole-LC;tt=np.array([-nn[1],nn[0]])
  # Adverse seized roller / nonrotating trunnion trial; Coulomb opposes
  # relative slip at the actual pole, so sign and normal remain correlated.
  va=np.array([-(cen-LC)[1],(cen-LC)[0]])
  ds=(va@nn)/nn[1]
  vr=np.array([-rr[1],rr[0]])-[0,ds]
  f=nn-.23*np.sign(vr@tt)*tt;N=60/f[1];Ta=N*(rr[0]*f[1]-rr[1]*f[0]);req=-Ta*J
  print('angle, actual s, ds/dtheta, N, J, signed motor torque Nmm FOR seized rolling members and net 60N output; positive = drive',deg,st,ds,N,J,req)
 print('index maximum geometric Jacobian',measured_J,'catalog continuous upper relay (.90 each)',min(25,.156*256*.60)*.9**2)
 print('3 motors only (key,index,yaw); separately reserved ejector needs own drive & supply. 3V/16.2 armature nominal zero speed, converter .85, aux .28',3*(3/16.2)/.85+.28)
if __name__=='__main__':loads();sizes()
