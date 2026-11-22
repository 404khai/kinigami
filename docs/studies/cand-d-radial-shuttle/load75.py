from carrier75 import *
def beam():
 # Conditional unilateral, zero installed preload, two effective guide rows
 # per normal plane, concentrated resultants at their adverse bearing edges.
 # This is a demand screen, not a stiffness or manufacturing guarantee.
 # Use the follower center x to eliminate actuator radial force from X moment.
 pause=3.30;exd=6.04;contact_axial=exd-.125;exg=exd-2.037;dy=16.70-12.20
 norm=sqrt(1+.23**2);g=.05
 J=ST*pi/(2*radians(64));tanp=J/18.35
 kx=2*exg*g/pause
 # X and t guide resultants Qx,Qt. Full 3D moment about cam pin:
 # t-force causes X-axis pitch, pin/contacts have finite t eccentricity;
 # 2.67 t lever arm bounds drag moments. Qt contains cambearing side
 # thrust from positive groove and the face friction in either direction.
 # Slot derivative dr/(r*dtheta); adverse Coulomb tan(phi+atan(mu)).
 c=(tanp+.06)/(1-.06*tanp)
 # moment of external F_y about each guide axis, no common seat sharing.
 # For t-plane at t=0 drive line, external q_t<=2.25, residual radial
 # separation <= max(|18.35-yL|) affects cam tangent force.
 A=(1+2*dy/pause)*norm+2*contact_axial*norm/pause
 B=(1+2*dy/pause)*norm+2*2.25*norm/pause+(1+2*(18.35-16.05)/pause)*c*norm
 # sum of guide drags ≤g(Qx+Qt). All opposing guide drag centers bounded
 # relative to roller in x by exg and t by 2.67. Coupled feedback follows.
 C=2*(exg+2.67)*g/pause+(1+2*(18.35-16.05)/pause)*c*g
 # Add the pure twist about y taken by opposite X-pad wings (2.06
 # minimum t pitch). Count residual t reactions at either axial edge.
 wing=2/2.06;BE=(1+2*(18.35-16.05)/pause)*c+2*2.67/pause
 T0=wing*((2.25+3.15)*norm+3.63*c*norm+1.24*B)
 Tc=wing*(3.63*c+1.24*BE)
 C+=Tc*g
 q=(A+B+T0)/(1-C);f=norm+g*q
 print('conditional per unit externally applied contact NORMAL; Qx+Qt, radial axial-drive F, tangential F; feedback',q,f,c*f,C)
 print('under one contact only; torque upper on drive ring Nmm per N (μslot=.06; independent max pressure angle)',(20.19*c)*f, 'max |dr/dtheta|',J,'max pressure angle deg',degrees(atan(tanp)))
 print('conditional effective .05 guide assumptions; no equal sharing, no indeterminate preload or squeeze')
 # Resolve opposite signs and an explicit 100-N pure radial toe load.
 for ng in (0,.05,.10,.18,.23):
  aa=1-2*(exg+2.67)*ng/pause-(1+2*(18.35-16.05)/pause)*c*ng-Tc*ng
  print('guide mu and allowable feedback denom (negative = no bound)',ng,aa)
 Q=100*q;F=100*norm+g*Q
 print('illustrative one contact 100 N: total guide normal; radial drive N, single-row full load on one pad MPa, roller pin cantilever bend MPa',Q,F,Q/(.65*1.17),F*(6.04-4.5)/(pi*.60**3/4))
 print('smallest X pitch, ±clearance, angular cock, x displacement at worst toe; max two-opposed pair twice this BEFORE normal projection',pause,.003,degrees(atan(.006/pause)),.003+.006/pause*dy)
 print('nominal cutter/roller radial gap and one-side radial play max mm',.0042,.0042*sqrt(1+tanp**2))
 # Check actual sweep of tool cutters with certified grid inflation for
 # 0.125 deg steps; line-segment interpolation error ~.00002 mm, no
 # promoting sample-only contact. Output 3D bottom and rim stock.
 d2=ST*pi*pi/(2*radians(64)**2);delta=radians(.125);err=(20.19+2*J+d2)*delta**2/8
 print('face continuous centerline chordal deviation upper',err,'radial margins inside/outside cutter, axial floor',18.35-.9042-16.75,21.61-20.1891-.9042,-6.97-(-7.03))
def mechanism():
 for ratio,stages,eff in ((256,4,.60),(4,1,.90),(64,3,.70)):
  print('0615N003S + 06/1 ratio, optimistic rated / stall via catalog MAX efficiency, and lossless nominal stall',ratio,.156*ratio*eff,.221*ratio*eff,.221*ratio)
 # Nominal single-start worm 122T, m=.30. Never count self-lock.
 for ratio,wr in ((122,1.60),(24,1.50)):
  lead=atan(.30/(2*wr));ew=tan(lead)/tan(lead+atan(.10/cos(radians(20))))
  eta=.80*ew;torque= .156*(256 if ratio==122 else 4)*(.60 if ratio==122 else .90)*2*ratio*eta
  print('trial single-start',ratio,'hypothetical μ=.10 ηworm, rated output Nmm (not guaranteed)',ew,torque)
  if ratio==122:
   print('one-100N worst drive requirement below/above must use conditional screened torque, no equal split')
  else: print('disk 0.50 lead, assumed thread μ=.15, mean R1.58 thrust from rated incl collar eff=.8',torque*.8/(1.58*tan(atan(.50/(2*pi*1.58))+atan(.15/cos(radians(30))))))
 T=.221*4*2*24
 print('disk lossless 3V nominal stall-generated thrust only; NOT an upper bound on static seating, inertia, overvoltage, stiffness or assembly',T*2*pi/.50)
 print('jam, lossless jaw star torque via gearhead 35 intermittent LIMIT vs nominal motor stall; input no guaranteed fault limiter',35*2,.221*256*2)
 for T in (2*25.,2*35.,2*.221*256):
  p=T/2.08;print('star shaft torque, side reaction, pin single shear & bending (centred reaction overhang), extraction µ=.23 N',T,p,p/(pi*.35**2),p*(10.01-8.93)/(pi*.35**3/4),p*.23)
 # Brake spring free envelope: ID guided ground wire provisional design.
 k=79000*.19**4/(8*1.39**3*6);l=18.85-(14.62+.42);free=l+.13/k
 print('park spring k, Llocked, Lreleased, wire solid assumed 8 coils, preload, max',k,l,l-2.04,8*.19,.13,.13+2.04*k)
 # spring solid during withdrawal? Negative is actual blocked travel.
 print('spring compression reserve at full unlock',l-2.04-8*.19)
 J=2.04*pi/(2*radians(116));rated=.156*64*.70
 print('brake cam max axial lead, optimistic continuous torque; peak side-loaded extraction incl spring before spur loss at 70Nmm input torque',J,rated,J*(.23*70/2.08+.13+2.04*k))
 print('drift if drive spring or actuator starts between holes unresolved. No finite radial jam bound from motor torque: dr/dtheta→0 near dwell')
 print('four stalled cold 3V/16.2ohm drives on .85 converter, +.13/.15 cell-side allowances A',4*3/16.2/.85+.28,'not a guaranteed sag/thermal or cutoff limit')
 # Positive anti-rotation with offset stud and 3 post bushes; even axial
 # forces on local rim generate pitch about guide rows as well.
 span=(-9.58)-(-10.98); # nearest adverse bearing edges, not the spacing of screw turns
 for F in (100,2*pi*(.221*4*2*24)/.50):
  print('illustrative disk thrust, guide X spacing, nominal radial reaction/row if loaded opposite rim uses full rim-to-stud lever',F,span,F*(12.42+NR)/span)
if __name__=='__main__':beam();mechanism()
