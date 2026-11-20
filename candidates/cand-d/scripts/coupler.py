#!/usr/bin/env python3
"""cand-d v6 design arithmetic, NOT a gate run or capture simulation.
mm, N, N mm, degrees where stated; Python stdlib only. Run beside the candidate
or pass --declaration PATH. No geometry, state, or evidence files are written.
"""
import argparse
import json
import math
from pathlib import Path

PI, rad, deg = math.pi, math.radians, math.degrees
hypot, sqrt, atan = math.hypot, math.sqrt, math.atan
def show(title, **values):
    print(title + ": " + "; ".join(f"{k}={v:.4f}" for k, v in values.items()))

# HX = head pitch plane; s increases into head. s is the APPROACH-LOADED
# pin centre locus at zero partner roll, not the centre of a symmetric cut.
HX = 36.4
S0, S1, S2 = 2.72, 3.18, 3.765
Q1, Q2 = 2.00, 0.331  # dz/d(theta) [mm/rad], constant across radius
DQ1, DQ2 = .010, .003  # drawing/slope inspection limits, not IT grades
R0, R1 = 3.505, 5.25  # conservative contact(inner) and lug tip radii
CROWN, BAR, SLOT = 1.25, 1.60, 1.70
A1, A2 = (S1-S0)/Q1, (S2-S1)/Q2
SHELF = 31.5  # rotate across both half-mouths before applying axial lead
STOP = SHELF+deg(A1+A2)
SEAT, STACK = 3.60, .015 + .004 + 5*.0125
# STACK: seat axis position; crown; forms of two teeth; flange, thrust ring,
# sleeve track axial position. No moulding dimension in the preload loop.
# Machine each flank by enveloping the actual crowned/flattened follower.
# Opposite (ejection) centre locus is 0.160 +/-0.015 mm deeper, not zero lash.
LOST = .175
PLAY = .127
RF, RR = 4.4, 4.89  # outer thrust radii; keep forward and rear faces distinct
TILT_PIVOT = rad(1.8)
# All bores measured finished, including dry bonded PTFE on pilot OD and
# stationary slot side flats (masked from cam). Edges of both slotted lands
# have a <=.03 break. Full land begins 5.57 below HX; floor 6.70 +/-.015.
P_MIN, P_MAX = 3.986/2, 3.990/2
B_MIN, B_MAX = 4.000/2, 4.008/2
PILOT = 6.50
NOSE, FRONT = .30, .73  # front station beyond land, entry chamfer, edge breaks
COAX = .003  # combined radial true position of pitch ring wrt bore/pilot
C0 = B_MIN - P_MAX
# Worst displacement toward a missing sector: circles at the last surviving
# edge of the slot, NOT full diameter contact through an empty axial channel.
BAND = (SLOT+.010)/2 + .03
C_SPLIT = sqrt(B_MAX**2-BAND**2)-sqrt(P_MIN**2-BAND**2)
C_FULL = B_MAX-P_MIN
COS_GUIDE = sqrt(1-(BAND/P_MIN)**2)
# Bolt/key drawing limits; include phase/position of BOTH mating parts.
R_GUIDE = 3.45
HALF_LASH = math.asin(((SLOT+.010)-(BAR-.010))/(2*R_GUIDE))
PHASE = rad(.20)  # two indexed machining setups, +/-0.10 deg EACH
# Teeth have a constant axial tooth advance per radian, not a constant flank
# angle at every radius. Root and crest truncated by <=.010 each.
N_TEETH, RI, RO, QT = 72, 4.25, 6.30, 8.80
QT_LO, QT_HI = 8.70, 8.90
H_MIN, H_MAX = QT_LO*PI/N_TEETH-.020, QT_HI*PI/N_TEETH
ROLL = HALF_LASH + PHASE + math.asin((C_SPLIT+COAX)/RI)
DRY, OIL = (.15,.23), (.10,.16)
MU_CF, MU_P, MU_R, MU_SS = .20, .20, .23, .80
MU_Z_LO = .05
# Room-temperature paper properties: ATI 304 sheet (E=200 GPa, yield 205
# MPa); Concast C95400 (107 GPa, minimum yield 221 MPa); Materialise PA12
# (48 MPa tensile only). Poisson ratios and contact models PROVISIONAL.
E_STAR = 1/((1-.29**2)/200000+(1-.33**2)/107000)
# Servo: FEETECH SCS0037-C001 pp3-5. Use the 4.8 V column on the accepted
# 4.8..5.2 V AT SERVO supply. Rating is NOT a specimen lower tolerance or
# a guaranteed torque-speed curve. No operating torque is taken from 6 V.
RATED, STALL = .50*98.0665, 1.50*98.0665

def span(s):
    # Earliest pilot front end at this lug-pivot depth incl tail dimensional
    # tolerance, tip tolerance, nose break. Rear effective station .05 before
    # full cylindrical tip; if not on unslotted land, use a second split arc.
    back = PILOT-.015 - (.30+.015) - ((SEAT+.015)-s) - .050
    full = back >= 5.57
    return back-FRONT, (C_SPLIT+(C_FULL if full else C_SPLIT))/(back-FRONT), full

def angle(s, late):
    a, b = (Q1-DQ1,Q2-DQ2) if late else (Q1+DQ1,Q2+DQ2)
    return SHELF+deg(min(s-S0,S1-S0)/a + max(s-S1,0.)/b)

def hp(q,r,mu):
    return (mu+q/r)/(1-mu*q/r)  # tangential/axial force, raising
def hm(q,r,mu):
    return (mu-q/r)/(1+mu*q/r)  # lowering; negative can overhaul

# Rectangular z flats (reaction in roll) on a cylindrical rocker crown. Metal
# rocking joint has a separate central C95400 pin retained by two fork ears.
# From pivot bearing friction at r=.50 plus position error, not assumed 50:50.
# Cross-pin axial load F; bound the residual bearing moment incl nonaxial
# resultant: <= mu*rp*1.4F plus .03F small machining eccentricity.
ECC = .23*.505*1.4+.03  # C95400 pivot pin against 304 rocker (fork cheeks unloaded)
IMBALANCE = (R1-R0+2*ECC)/(R1+R0)
def asym_force(hlo,hhi):
    return .5*((hhi-hlo)+IMBALANCE*(hhi+hlo))
B_MIN_SPAN, TAN_TILT, _ = span(S0-.12)
# Slightly enlarge for clearance of a tilted, eccentric pilot nose.
TAN_TILT += .0003
FACE_DROP = RO*TAN_TILT
LUG_DROP = R1*TAN_TILT
TOOTH_DROP = QT_HI*ROLL
# Two loaded opposed rocker tips cancel the first-order differential depth
# (interpolating at the pivot), but cannot cancel translation of a cocked
# thrust datum. When forward-loaded its centre moves into the head; rearward
# ejection moves it OUT of the head vs the parallel rear-stop extreme.
REAR, FWD = (27.16,27.61), (35.05,35.30)
JSPAN = FWD[0]-REAR[1]
JR = 5.045/math.cos(math.asin(1.365/5.04))
JF = 3.51/math.cos(2*math.asin(.86/3.49))
TAN_SLEEVE=(.020*JR/5.045+.0175*JF/3.51+.005)/JSPAN
C_CAM=.0175*JF/3.51+.005+C_SPLIT
CAM_PHASE=ROLL+math.asin(C_CAM/R0)
DATUM_DROP=RF*TAN_SLEEVE+.004  # extra projection at off-centre pivot; face flatness in STACK
FIRST=SEAT-STACK-FACE_DROP-DATUM_DROP-TOOTH_DROP
SEAT_LOW, SEAT_HIGH=FIRST+TOOTH_DROP, SEAT+STACK+.004
# Angle uncertainty includes partner roll, rocker sweep & 0.6 deg cam start
# datum; operating feedback may report only the input member, not the sleeve.
EARLY = angle(SEAT_LOW,False)-deg(CAM_PHASE)-.6
LATE = angle(SEAT_HIGH,True)+deg(CAM_PHASE)+.6
# Spring. Diameter acceptance is a screened subset of .016" +/-.0003" stock.
# Mandrel-free elastic energy U=M² L/(2 E I); N_eff includes straight leg
# angular compliance. 0.94 lower multiplier covers the common 10.8 (vs
# 64/(2*pi) = 10.186) turn-rate convention. E range is a DESIGN
# allowance about 30 Mpsi, not an A228 modulus tolerance. Inspect lot rate.
WIRE, DW, D, DD, N, DN = .4064, .0026, 9.20, .04, 3.75, .03
LEGS = (2.60,1.36)  # nominal extra wire, straight/radiused radial pickups
DLO,DHI,NLO,NHI = D-DD,D+DD,N-DN,N+DN
WLO,WHI = WIRE-DW,WIRE+DW
EFF_HI = NHI+sum(LEGS)/(PI*DLO)  # upper: end moments over whole legs
def spring_rate(E,d,mean,n):
    return E*d**4/(64*mean*n) * PI/180
KLO = .94*spring_rate(199000,WLO,DHI,EFF_HI)
KHI = spring_rate(215000,WHI,DLO,NLO)
HOME,CMD = 14.,245.  # absolute input at theta_sleeve=0 datum; relative close increment
ERR = .5+.30+1.5+.7+.5  # backlash, conservative quantisation, accepted loaded tracking, calibration, cradle
FREE_ERR = 1.0  # spring free leg pickup relative to assembled pair
# Soft unloaded pickup, not a bilateral spring forced past neutral. Reverse
# dog touches at input=HOME + actual sleeve angle - 6 (+/-1) deg.
DOG,DOG_ERR = -6.,1.
WIND_MAX = CMD+ERR+FREE_ERR+.6  # obstruction at open stop incl stop error
WIND_MIN = CMD-ERR-FREE_ERR-LATE
WIND_SEAT_MAX = CMD+ERR+FREE_ERR-EARLY
TS_JAM, TS_MIN, TS_MAX = KHI*WIND_MAX, KLO*WIND_MIN, KHI*WIND_SEAT_MAX
# Rate model excludes rubbing. Forward losses are estimated separately; bound
# +/- .25 N mm in the spring cartridge as a bench acceptance limit, not data.
CARTRIDGE_DRAG = .25
VP = PI*WIRE**2/4
PITCH = 1.900/N
V_WIRE = VP*(N*hypot(PI*D,PITCH)+sum(LEGS))
# Geometry: fixed plane spacing 1.900 +/-.008, allowing increased turns to share
# the pitch rather than collide; optically inspect the minimum live gap.
BODY = 1.908+WHI
GAP = 1.892/(NHI+WIND_MAX/360)-WHI
ID_WOUND = DLO*NLO/(NLO+WIND_MAX/360)-WHI
C_INDEX = (ID_WOUND+WHI)/WHI
KB = (4*C_INDEX**2-C_INDEX-1)/(4*C_INDEX*(C_INDEX-1))
STRESS = KB*32*TS_JAM/(PI*WLO**3)
# Body swept solids. No double-subtracting notch/skirt or claiming exact mass
# for swept overlaps. Lower bound on removed slot area: core contained in the
# cutter at every centre angle, integrate actual radial shell; leave overlap
# of the open mouth out of the cut deduction.
SLEEVE_X0,SLEEVE_X1=30.35,35.30
SKIRT_X0=24.35
def volume_results():
    barrel = PI*(6.30**2-3.5075**2)*(SLEEVE_X1-SLEEVE_X0)
    skirt = PI*(6.30**2-5.035**2)*(SLEEVE_X0-SKIRT_X0)
    # Through-cuts at both stations of radius, irrespective of lug tip depth.
    # One angular ray across the two opposing helices cuts >=2*(CROWN-.005) axially.
    # Even at ends, the crown has full axial diameter on its z=0 centreline.
    cut = 2*(A1+A2+rad(SHELF))*(6.30**2-3.5125**2)/2*(2*(CROWN-.005))
    bar_section = 2*(.8*sqrt(CROWN**2-.8**2)+CROWN**2*math.asin(.8/CROWN))
    # 2.74 mm long through pocket, 1.64 wide, running across y in the pilot.
    # Bound volume from below with an inscribed prism across the cylinder.
    pocket = 2.74*1.64*2*sqrt(P_MIN**2-.82**2)
    show("CAD volume mm3", sleeve_blank=barrel, two_cam_cuts_min=cut,
         barrel_upper=barrel-cut, skirt_blank=skirt, spring=V_WIRE,
         rocker=bar_section*2*R1-PI*.505**2*BAR,
         fork_pocket_min=pocket, crosspin_upper=PI*.5**2*3.98)
    show("spring chamber mm", body=BODY,min_interturn_gap=GAP,
         wound_ID=ID_WOUND,free_OD=DHI+WHI,mandrel_OD=6.75)
    assert 0 < cut < barrel and BODY<2.4 and GAP>.01 and ID_WOUND>6.8

def layout():
    print("v6 exploratory static design; not a measurement, evaluator or capture window")
    show("cam", start=S0,transition=S1,end=S2,q1=Q1,q2=Q2,
         dead_shelf_deg=SHELF,capture_deg=deg(A1),lock_deg=deg(A2),total_deg=STOP,
         dry_lock_factor=DRY[0]*R0/(Q2+DQ2),oil_lock_factor=OIL[0]*R0/(Q2+DQ2))
    # Tangential flats project <=.805, entry slot includes 0.5 V lead; allow
    # 1 degree for datum. At front face a chamfer leads the radial channel.
    # V entry on stationary flange ONLY, straight 1.70 sleeve mouth with
    # ≤.010 all-in profile allowance. No flare in the deep end's web.
    half_mouth=math.asin(.855/R0)+math.asin(.805/R0)
    bridge=SHELF-deg(half_mouth+CAM_PHASE)-.6
    web=180-STOP-1-deg(half_mouth)
    rear=HX-SLEEVE_X0-(S2+CROWN*sqrt(1+((Q2+DQ2)/R0)**2)+LOST+.020)
    show("metal",web_deg=web,web_mm=rad(web)*R0,rear_web=rear,fully_bridged_before_rise_deg=bridge,
         minimum_pivot_travel_deg=deg(TILT_PIVOT),pivot_ecc_limit=ECC)
    for s in (S0-.12,FIRST,SEAT_LOW,SEAT_HIGH):
        l,t,f=span(s);show("pilot "+("rear full" if f else "rear split"),
                            depth=s,span=l,rock_deg=deg(atan(t)))
    show("tooth/min-max locus",phase_bound_deg=deg(ROLL),tooth_height=H_MIN,
         crest=H_MAX/2,ring_standoff=FACE_DROP,each_lug_skew=LUG_DROP,
         first_tooth_min=FIRST,early_seat=SEAT_LOW,late_seat=SEAT_HIGH,
         earliest_full_deg=EARLY,latest_full_deg=LATE)
    err=2*.0125+(.015+.015)*rad(1) # opposing track depth mismatch (mm)
    req_tilt=atan(TAN_TILT+TAN_SLEEVE+err/(2*R0))
    show("fork",rocker_need_deg=deg(req_tilt),min_throat_side_clearance=(2.74-2.51)/2-2*math.tan(TILT_PIVOT))
    # Finite crescent contact at mouth: not 5 mm engagement at first V touch.
    lead=PILOT-.015-.315-(SEAT+.015+CROWN+.005+H_MAX/2)-FRONT
    # Centre-offset limit at the nose, present roll +/-1.4 deg on the table.
    show("external presentation",nose_chamfer_capacity=(.40+.30+C0),
         axial_pilot_lead_at_lug_crest=lead,
         V_allowance=.50-R1*math.sin(rad(1.4))-C_SPLIT-.04)
    assert FIRST>S1+.0125 and SEAT_LOW>S1 and SEAT_HIGH<S2 and web>5 and rear>.30 and bridge>0
    show("two-journal cocking",max_deg=deg(atan(TAN_SLEEVE)),front_datum_debit=DATUM_DROP,
         lateral_phase_debit_deg=deg(CAM_PHASE-ROLL))
    assert COAX<C0 and req_tilt<TILT_PIVOT and lead>.10 and ROLL<PI/N_TEETH
    assert DRY[0]>(Q2+DQ2)/R0 and OIL[0]>(Q2+DQ2)/R0
    show("servo",rated_4v8=RATED,stall_4v8=STALL,absolute_close_min=HOME+CMD-ERR,
         absolute_close_max=HOME+CMD+ERR,absolute_dog_at_open_min=HOME+DOG-DOG_ERR-.6,
         absolute_dog_at_open_max=HOME+DOG+DOG_ERR+.6)
    show("spring",k_lo_Nmm_deg=KLO,k_hi=KHI,wind_min_deg=WIND_MIN,
         wind_seat_max=WIND_SEAT_MAX,wind_jam_max=WIND_MAX,T_min=TS_MIN,
         T_seat_max=TS_MAX,T_jam_max=TS_JAM,body_jam_MPa=STRESS)
    assert HOME+CMD+ERR<270 and HOME+DOG-DOG_ERR-.6>2+ERR
    assert DOG+DOG_ERR < -FREE_ERR and TS_JAM+CARTRIDGE_DRAG < RATED
    assert STRESS < .8*362000*.00689476 # M&R static body screen, not fatigue or leg proof
    volume_results()

# Fixed lands; station resultants may lie anywhere in the actual supported bands.
# Front: rotating mouth plus fixed channel can adjoin; use their SUM of full
# angular widths as a missing sector, not the width of either alone.
JM=.23
def arm(x,a,b):
    return (JR*abs(b-x)+JF*abs(x-a))/(b-a)
def drive_loss(xs,r,imbalance=1):
    return imbalance*JM*max(arm(x,a,b) for x in xs for a in REAR for b in FWD)/r
SPRING_LOSS=drive_loss((26.84,27.10),5.05)
DOG_LOSS=drive_loss((29.35-.127,30.00+.127),5.64)

def cam_path(q,mu,raising,thrust):
    func=hp if raising else hm
    hs=[func(q,r,m) for r in (R0,R1) for m in mu]
    diff=asym_force(min(hs),max(hs))
    # Resultant cam side load from friction variation and potential unequal
    # lug radii. Eccentricity of axial resultant adds a journal couple.
    # Absolute projection for the open arcs throughout. A negative descending
    # cam torque isn't credited as a motor or as helping other reactions.
    # All working axial cam reaction centres lie between the fixed lands.
    # Journal torque/axial force from net side force and a residual couple.
    fj=diff*max(JR,JF)+ECC*(JR+JF)/JSPAN
    lever=max(0.,max(r*func(q,r,m) for r in (R0,R1) for m in mu))
    return lever+thrust+JM*fj,lever,diff

def efficiency_guides(q,mu):
    k,h,side=cam_path(q,mu,True,0)
    # Sliding axial drag from torque reaction on both fixed slots, adverse
    # net cam side force and residual eccentric moment reacted by pilot pair.
    # Use positive feedback, solve F_pilot = F_fixed/(1-gamma), not an
    # assumed constant allowance. No second binding with loose original bore.
    gamma=MU_P*(h/R_GUIDE+(side+2*ECC/B_MIN_SPAN)/COS_GUIDE)
    assert gamma<1
    return 1-gamma

def torque_after_spring(angle_late):
    ts=KLO*(CMD-ERR-FREE_ERR-angle_late)
    return max(0.,ts*(1-SPRING_LOSS)-CARTRIDGE_DRAG)

def assert_open_and_overlap():
    # At open the ejection flank takes up its width + all collar end play;
    # both teeth and opposing crowns must clear. The pilot and stationary
    # key slots STILL guide the body at open; no claim of powered withdrawal
    # of a full 6.5-mm pilot or separation against arbitrary lateral jamming.
    open_depth=S0+LOST+PLAY+.0125+LUG_DROP
    separation=(SEAT-STACK)-open_depth-FACE_DROP
    overlap=H_MIN-TOOTH_DROP-2*FACE_DROP  # axial flank overlap opposite a first-touch edge
    # 2 kN/mm is a provisional minimum differential axial stiffness (steel
    # pin, bar and flange), not Young's modulus or a Gate 2 measurement.
    slack=20/2000
    locked_drop=RO*(span(FIRST-.03)[1]+.0003)
    loaded_overlap=H_MIN-TOOTH_DROP-2*locked_drop-DATUM_DROP-2*(Q2+DQ2)*CAM_PHASE-slack
    show("passive geometric reserve at limiting tilt/phase",teeth_open_clearance=separation-H_MAX,
         overlap_unloaded=overlap,overlap_after_cocking_roll_20N=loaded_overlap,
         first_contact_stroke_into_lock=FIRST-S1,
         after_single_roll_reversal=FIRST-S1-(Q2+DQ2)*2*ROLL)
    assert separation>H_MAX and loaded_overlap>0 and FIRST-S1>(Q2+DQ2)*2*CAM_PHASE
    show("spring interface",spring_side_loss_fraction=SPRING_LOSS,
         dog_side_loss_fraction=DOG_LOSS,
         free_release_at_open_absolute_command=2.,close_absolute_command=HOME+CMD,
         extra_endplay=PLAY,opposite_flank_takeup=LOST)

def loads(mass_g,com,verbose=False):
    W=mass_g*.001*9.80665
    tension,twist,shear,oop,ip=4*W,2*W*12.7,W,48.0*W,14.5
    fault=10.8*58/12
    M=hypot(oop,ip)
    # Face wedge may wedge harder than ideal T/QT. Keep adverse tooth
    # friction at both radii; assume the pilot can carry all radial shear.
    hirth=min((QT_LO-.20*r)/(1+.20*QT_LO/r) for r in (RI,RO))
    sep=tension+twist/hirth+shear*max(1,RO/hirth)
    edge=sqrt(RO**2-((SLOT+.01+1.0)/2)**2)
    # finite pitch: usable compression patch may be another half pitch from
    # the cut. Pilot may carry some of this bending; no credit at breakaway.
    edge*=math.cos(PI/N_TEETH)
    bending=M/edge
    t_roll=W*(12.7+abs(com[1]))
    pitch_v=W*(35.6-com[0])/(35.6+11.6)
    yaw_drag=W*hypot(47.2,25.4)
    # At first hard tooth contact, don't call the minimum spring torque at a
    # nominal mid-stage stall. Calculate the available draw at the latest
    # end of each interval. Spring winds up quasi-statically if sleeve lags.
    phases=[("shelf",0.,SHELF+deg(CAM_PHASE)+.6),
            ("capture",Q1+DQ1,SHELF+deg((S1-S0)/(Q1-DQ1))+deg(CAM_PHASE)+.6),
            ("lock",Q2+DQ2,LATE)]
    previous={}
    for name,q,ang in phases:
        k,ht,_=cam_path(q,DRY,True,RF*MU_CF)
        cam=torque_after_spring(ang)/k
        eff=efficiency_guides(q,DRY)
        useful=cam*eff-W
        previous[name]=useful
        if verbose:
            show(name+(" reaction capacity ONLY; no axial advance" if not q else " draw; net after one free unit"),angle_deg=ang,
                 sleeve_T=torque_after_spring(ang),cam_F=cam,guide_eff=eff,
                 net_F=useful)
        assert useful>0, (name,mass_g,useful)
    # Real corrective torque: adverse parasitic cam torque on mating stud and
    # ground load retained. Do NOT claim that individual scalar margins prove
    # simultaneous resolution of roll, yaw and pitch.
    kl,ht,_=cam_path(Q2+DQ2,DRY,True,RF*MU_CF)
    fcam=torque_after_spring(LATE)/kl
    roll_cap=hirth*previous['lock']-ht*fcam
    if verbose:
        show("attitude demand (no hidden levelling)",roll_needed=t_roll,
             adverse_roll_supplied=roll_cap,pitch_vertical_needed=pitch_v,
             yaw_floor_friction_torque_upper=yaw_drag)
        # Simultaneous virtual-work limit; moment spent at a tilted rim
        # cannot also be spent indexing teeth/translating on the table.
        fnet=previous['lock']
        show("upper service screening certificate (negative reserve rejects corner)",
             draw_available=fnet,draw_for_roll=(t_roll+ht*fcam)/hirth,
             draw_for_pitch=pitch_v*(35.6+11.6)/edge,draw_for_yaw=yaw_drag/edge,
             residual_draw=fnet-(t_roll+ht*fcam)/hirth-(pitch_v*47.2+yaw_drag)/edge)
    # Extremes when spring stalls at earliest permitted solid tooth contact,
    # not just the nominal parallel seat. Trapped static preload survives
    # unwinding. Do not subtract initial preload from external fixed loads.
    first_angle=angle(FIRST,False)-deg(CAM_PHASE)-.6
    ts_partial=KHI*(CMD+ERR+FREE_ERR-first_angle)
    by_condition={}
    for cond,cl,mu in (("dry",DRY,DRY),("oil",OIL,OIL),("oil-to-dry",OIL,DRY)):
        fmax=(ts_partial+CARTRIDGE_DRAG)/(R0*hp(Q2-DQ2,R0,cl[0])+3.6*MU_Z_LO)
        # Lowering a clamped or outward-pulled stud: front thrust ring remains
        # loaded. During pullout after unclamping, fixed tension ASSISTS: do
        # not both charge its descent friction and treat it as a compression.
        k_down,_,_=cam_path(Q2-DQ2,mu,False,RF*MU_CF)
        tax=fmax+sep+bending
        unload=(k_down*tax+CARTRIDGE_DRAG)/(1-DOG_LOSS)
        stage_opens=[]
        for name,q,_ in phases:
            # Evaluate BOTH flank signs and both thrust faces throughout.
            k_ej,_,_=cam_path(q,mu,True,RR*MU_R)
            eff=efficiency_guides(q,mu)
            # After teeth disengage: the pilot pair can carry ALL bending;
            # tapered/tooth flank unloading assistance is not credited.
            # Fixed slot sides take all torsion while the lugs remain in them.
            external=W+MU_P*((shear+2*M/B_MIN_SPAN)/COS_GUIDE+twist/R_GUIDE)
            # Include a separate, adverse case of an inward load equal to the
            # declared chain tension, though not a v5 service case.
            eject=(external/eff*k_ej+CARTRIDGE_DRAG)/(1-DOG_LOSS)
            compressed=((external+tension)/eff*k_ej+CARTRIDGE_DRAG)/(1-DOG_LOSS)
            # Released after first relaxation: no initial preload unless teeth
            # still in contact; use the worst aiding fixed axial load.
            kd,_,_=cam_path(q,mu,False,RF*MU_CF)
            descend=((sep+bending)*kd+CARTRIDGE_DRAG)/(1-DOG_LOSS)
            stage_opens.append((name,eject,descend,compressed))
        demand=max([unload]+[max(row[1:3]) for row in stage_opens])
        if verbose:
            # Alternate front bearing: take ZERO thrust resistance on closure
            # when finding preload; solve its allowable drag at breakaway.
            f0=(ts_partial+CARTRIDGE_DRAG)/(R0*hp(Q2-DQ2,R0,cl[0]))
            k0=cam_path(Q2-DQ2,mu,False,0)[0]
            show(cond+" positive-drive breakaway",trapped_preload_max=fmax,external_sep=sep,
                 additional_bend=bending,T_break=unload,imbalance_max_at_35Nmm=
                 (1-(k_down*tax+CARTRIDGE_DRAG)/35)/DOG_LOSS,
                 alternative_front_mu_max_at_35_zero_floor=
                 ((35*(1-DOG_LOSS)-CARTRIDGE_DRAG)/(f0+sep+bending)-k0)/RF)
            for name,eject,descend,compressed in stage_opens:
                show(cond+" reverse "+name,eject_against_drag=eject,assisted_descent=descend,
                     sensitivity_if_compression=compressed)
        by_condition[cond]=(demand,fmax)
    demand=max(v[0] for v in by_condition.values())
    # Lower bounds on usable quiescent preload only after F settles. At
    # first-contact the draw may be consumed in aligning; do not assume all
    # of it enters clamp compression or that the faces never gap.
    if verbose:
        show("fixed service loads",pull=tension,shear=shear,twist=twist,
             outplane=oop,inplane=ip,inplane_fault=fault)
        show("guide withdrawal after geometric unlatch (external, not a powered stroke)",
             axial_force=external)
        structural(W,tension,twist,oop,ip,fault,max(x[1] for x in by_condition.values())+sep+bending)
    show("load summary",mass_g=mass_g,lock_draw_net=previous['lock'],
         release_dry=by_condition['dry'][0],release_oil=by_condition['oil'][0],
         oil_then_dry=by_condition['oil-to-dry'][0],
         rated_ratio=RATED/demand,locked_rotor_ratio=STALL/demand)
    print("  rated-envelope release: "+("within nominal rating" if demand<=RATED else "NOT demonstrated")+
          "; static locked-rotor screen: "+("below catalogue stall" if demand<STALL else "EXCEEDS catalogue stall"))
    return demand

def structural(W,pull,twist,oop,ip,fault,axial):
    high_fraction=(1+IMBALANCE)/2
    Fn=axial*high_fraction*sqrt(1+hp(Q2+DQ2,R0,DRY[1])**2)
    line=R1-R0
    p0=sqrt(Fn*E_STAR/(PI*CROWN*line))
    # Rectangular *inscribed* section on each side of the central pin.
    chord=2*sqrt(CROWN**2-(BAR/2)**2)
    Z=BAR*chord**2/6
    b=Fn*(R1-.50)/Z
    show("rocker conditional nominal line; no edge-load guarantee",F_lug=Fn,
         Hertz_MPa=p0,onset_model=1.67*221,root_bend_MPa=b,
         pin_double_shear=axial/(2*PI*.495**2),rocker_pin_bearing=axial/(.99*BAR))
    # Head/tail mount and originally declared hinge working/fault paths.
    P=fault/7/2+pull/2
    Pt=fault/RO/2+pull/2
    show("structural loads (PA12 tensile coupon 48 MPa, NOT bearing)",head_screw_fault=P,
         tail_screw_fault=Pt,head_nut_bearing=P/(2.2**2-PI*.8**2),
         tail_cone_bearing=Pt/(PI/4*(3**2-1.6**2)),
         head_strip_MPa=6*P*23/(8*3.35*1.2**2),
         tail_strip_MPa=6*Pt*23/(8*4.0*1.2**2),
         hinge_ear_F=oop/18.3+pull/2,hinge_pin_bearing=(oop/18.3+pull/2)/(2*1.5),
         hinge_twist_F=twist/18.3)
    # Forward closure uses a compliant drive. Reverse fault torque is not
    # limited by the spring; use a structural design load, not a guaranteed limit.
    torque=176.5  # 6 V catalogue fault screen, not a measured upper limit
    force=torque/5.75
    show("stops & reaction screening",stop_torque=torque,stop_pin_F=force,
         stop_pin_shear=force/(PI*.65**2),bronze_bearing=force/(1.30*.5))
    print("  Rear collar, cross-rivet, tang/shoe and keyed ABS case cradle: see separate v6 assembly checks.")

def partial_lock_screen(mass_g,journal_mu=.23,front_mu=.20,clamp_thrust_floor=0.,
                        fixed_key=False,com=(15.70,-.18,-.64)):
    """Q96 investigation ONLY; no assumed levelling or opposing-contact rescue."""
    W=mass_g*.001*9.80665
    twist=2*W*12.7
    M=hypot(48*W,14.5)
    edge=sqrt(RO**2-((SLOT+.01+1.)/2)**2)*math.cos(PI/N_TEETH)
    a=min((QT_LO-.2*r)/(1+.2*QT_LO/r) for r in (RI,RO))
    sep=4*W+twist/a+W*max(1,RO/a)
    slot=twist/R_GUIDE  # FULL external twist on just one side, either sign
    pilot=(W+slot+2*M/B_MIN_SPAN)/COS_GUIDE
    external=W+MU_P*(slot+pilot)
    # New, longer journal spacing. Do not assume zero loss at the port.
    rear=REAR
    jspan=FWD[0]-rear[1]
    dog=journal_mu*max(arm(x,aa,b) for x in (29.35-.127,30.00+.127) for aa in rear for b in FWD)/5.64
    leg=journal_mu*max(arm(x,aa,b) for x in (26.84,27.10) for aa in rear for b in FWD)/5.05
    show("Q96 assumptions",front_mu=front_mu,clamp_thrust_floor=clamp_thrust_floor,
         journal_mu=journal_mu,fixed_separate_key=float(fixed_key),
         roll_required=W*(12.7+abs(com[1])),pitch_tail_force=W*(35.6-com[0])/47.2)
    show("Q96 partial; fixed service, no tooth torsion required",mass_g=mass_g,slot_force=slot,
         paired_pilot_normal_sum=pilot,withdraw_force=external,slot_reverse_lash_deg=deg(2*HALF_LASH),
         spring_side_loss=leg,dog_side_loss=dog,minimum_journal_spacing=jspan)
    ts=KHI*(CMD+ERR+FREE_ERR-angle(FIRST,False)+deg(CAM_PHASE)+.6)
    for label,closing in (("dry",DRY),("oil-to-dry",OIL)):
        fp=(ts+CARTRIDGE_DRAG)/(R0*hp(Q2-DQ2,R0,closing[0])+3.6*clamp_thrust_floor)
        A=fp+sep+M/edge
        # One contact at either radius: eccentric axial force r*A as well
        # as transverse h*A. The eccentric couple needs opposite journals.
        def one_path(q,fn,thrust):
            return max(max(0.,r*fn(q,r,u))+thrust+journal_mu*(abs(fn(q,r,u))*max(JR,JF)
                       +r*(JR+JF)/jspan) for r in (R0,R1) for u in DRY)
        kd=one_path(Q2-DQ2,hm,RF*front_mu)
        T=(kd*A+CARTRIDGE_DRAG)/(1-dog)
        Nlug=A*hypot(1,hp(Q2+DQ2,R0,DRY[1]))
        L_req=Nlug*E_STAR/(PI*CROWN*(1.67*221)**2)
        show("Q96 one-lug "+label+" breaking against fixed loads",A=A,T=T,
             ratio_rated=RATED/T,effective_Hertz_line_needed_mm=L_req)
    for name,q in (("shelf",0.),("steep",Q1+DQ1),("shallow",Q2+DQ2)):
        # One cam side PLUS one guide-flat side can load the pilot. Worst
        # signs treated independently: nonpositive denominator disproves
        # THIS certificate, not proof that every build self-jams.
        h=max(hp(q,r,DRY[1]) for r in (R0,R1))
        lever=max(r*hp(q,r,DRY[1]) for r in (R0,R1))
        gamma=MU_P*(lever/R_GUIDE+(h+lever/R_GUIDE+2*R1/B_MIN_SPAN)/COS_GUIDE)
        show("Q96 one-lug eject "+name,feedback=gamma)
        if gamma<1:
            show("  positive-flank (upper sizing estimate)",T=(external/(1-gamma)
                 *one_path(q,hp,RR*MU_R)+CARTRIDGE_DRAG)/(1-dog))
        else:
            print("  no finite upper torque certified by this Coulomb envelope")
    # Conditional free-rocker case. Unlike the one-tip screen, the
    # resistance to rocking is a MOMENT with a load-independent intercept.
    # These bearing dimensions/restraints are proposals, not v6 properties.
    for name,q,fn in (("break",Q2-DQ2,hm),("eject lock",Q2+DQ2,hp),
                      ("eject steep",Q1+DQ1,hp),("shelf",0.,hp)):
        hs=[fn(q,r,u) for r in (R0,R1) for u in DRY]
        hh=max(map(abs,hs))
        lever=max(abs(r*fn(q,r,u)) for r in (R0,R1) for u in DRY)
        def resist(A,small_pad):
            G=(twist+lever*A)/R_GUIDE
            H=hh*A+(0 if fixed_key else G)
            # Face friction at slot; cam may have a bounded lateral
            # in-plane component .30A. Opposed radial bearing bands span
            # >=1.10 along pivot axis. Charge BOTH orthogonal moments to
            # their reaction sum, not only the net force at a central pin.
            Fxy=1.30*A+(0 if fixed_key else .20*G)
            RP=Fxy+2*((lever*A if fixed_key else twist)+1.26*H+.805*Fxy)/1.10
            cheek=.23*.85 if small_pad else .80*2.40
            return .23*.505*RP+cheek*H+(0 if fixed_key else .20*3.75*G)+(.03+1.26*.30)*A
        for small in (False,True):
            m0=resist(0,small)
            b=resist(1,small)-m0
            print(f"  {name}, {'small' if small else 'broad'} cheek: "
                  f"M <= {m0:.3f} + {b:.3f} A; "
                  + ("one-tip static possible at any load in this bound"
                     if b>=R0 else f"one-tip crossover A*={m0/(R0-b):.3f} N"))
        for target in (False,True):
            net_guide=.25 if target else 1.
            def calc(A):
                Mcap=(.50+.30*A) if target else resist(A,True)
                E=min(R1*A,Mcap)
                imbalance=min(A,((R1-R0)*A+2*E)/(R1+R0))
                side=.5*((max(hs)-min(hs))*A+abs(max(hs)+min(hs))*imbalance)
                J=journal_mu*(max(JR,JF)*side+(JR+JF)*E/jspan)
                G=(twist+lever*A)/R_GUIDE
                N=(W+2*M/B_MIN_SPAN+net_guide*G+side+2*E/B_MIN_SPAN)/COS_GUIDE
                return W+MU_P*(G+N),J
            if name=="break":
                # Both low and high external torque present; keep maximum
                # trapped oil preload and dry reverse lever in one case.
                F=(ts+CARTRIDGE_DRAG)/(R0*hp(Q2-DQ2,R0,OIL[0])+3.6*clamp_thrust_floor)+sep+M/edge
                thrust=RF*front_mu
            else:
                # Piecewise-affine monotone envelope: Freq(0)>0, slopes
                # nonincreasing as moment and imbalance saturate.
                lo,hi=0.,1000.
                assert calc(hi)[0]<hi
                for _ in range(60):
                    mid=(lo+hi)/2
                    if calc(mid)[0]>mid:
                        lo=mid
                    else:
                        hi=mid
                F=hi
                thrust=RR*MU_R
            T=((lever+thrust)*F+calc(F)[1]+CARTRIDGE_DRAG)/(1-dog)
            show("Q96 "+name+(" redesign TARGET, not achieved" if target else " proposed small free cheeks"),
                 axial_contact=F,T=T,ratio_rated=RATED/T)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--declaration',type=Path,
                        default=Path(__file__).resolve().parents[1]/'declaration.json')
    parser.add_argument('--q96-only',action='store_true',help="run only the separate SCS0037 investigation")
    parser.add_argument('--journal-mu',type=float,default=.23,help="Q96 journal sensitivity, not cam friction")
    parser.add_argument('--front-mu',type=float,default=.20,help="Q96 breakout thrust friction; closure floor always zero")
    parser.add_argument('--fixed-key',action='store_true',help="Q96 separate stud torque guide at r≥3.45, no twist transfer via rocker")
    args=parser.parse_args()
    with args.declaration.open() as f:
        declaration=json.load(f)
    masses=declaration["components"]
    mg=sum(c["mass_mg"] for c in masses)
    assert mg==declaration["mass_budget"]["total_mass_mg"] and mg>0
    if not (0<=args.journal_mu<=.35 and 0<=args.front_mu<=.35):
        parser.error("sensitivity inputs must be in [0,0.35]")
    com=[sum(c["mass_mg"]*c["box"]["pose"]["position_um"][i]
             for c in masses)/mg/1000 for i in range(3)]
    def q96():
        for m in sorted({mg/1000,46.}):
            partial_lock_screen(m,args.journal_mu,args.front_mu,0.,args.fixed_key,com)
    if args.q96_only:
        q96()
        return
    layout()
    assert_open_and_overlap()
    show("actual input declaration",version=declaration['candidate_version'],mg=mg,x=com[0],y=com[1],z=com[2])
    print("Conditional two-contact path only; not a release certificate. See partial and one-tip cases below.")
    loads(mg/1000,com,verbose=True)
    for q in (0., Q2-DQ2, Q1-DQ1):
        show("176.5 Nmm catalogue fault screen; own drive only (no drag credit)",q=q,
             positive_flank_F=176.5/(R0*hp(q,R0,OIL[0])))
    q96()

if __name__=='__main__':
    main()
