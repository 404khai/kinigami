from check82 import *
def ratings():
 ref=json.load(open('upstream80.json'))['loaded_release_and_hertz'];mu=.23;dm=2.68;lead=.50;rc=2.
 lam=atan(lead/(pi*dm));tg=lambda F,mu=mu,alpha=0:F*(dm/2*tan(lam+atan(mu/cos(radians(alpha))))+mu*rc)
 cap=min(.156*256*.60,25)*3.5*.88
 rr={}
 for n,F in [('unlock',45*(1+mu)*mu*1.5),('draw',54.),('eject',35.)]:
  T=tg(F);T30=tg(F,mu,30);pr=56*.22/2
  # 0.88 trial mesh efficiency; input force on small pinion governs.
  Ft=T30/(pr*.88);Fr=Ft/cos(radians(20))
  # Wheel center x=-36.41; radial bearing centers −39.44 / −4.47
  # F3-8M seats carry only axial force; no sharing assumption between opposed thrust bearings.
  dist=36.41;rear=39.44;fore=4.47
  rr[n]=dict(required_N=F,baseline_Nmm=T,catalogue_max_efficiency_rated_path_Nmm=cap,ISO60_with_plain_collar_Nmm=T30,
    held_back_motor_eff_required=T30/(.156*256*3.5*.88),gearhead_output_Nmm=T30/(3.5*.88),
    wheel_tangential_N=Ft,pinion_mesh_resultant_N=Fr,
    pinion_bearing_reactions_N=[Fr*(36.41-34.24)/(38.58-34.24),Fr*(38.58-36.41)/(38.58-34.24)],
    wheel_bearing_reactions_N=[Fr*(dist-fore)/(rear-fore),Fr*(rear-dist)/(rear-fore)],thrust_static_demand_ratio=F/932)
 for n,k in [('unlock','M3_unlock_torque_Nmm'),('eject','M3_eject_35N_torque_Nmm'),('draw','M3_draw_54N_torque_Nmm')]:assert abs(rr[n]['baseline_Nmm']-ref[k])<.002
 # Force window when springs intact, output reset at most +.20; tolerances are assumptions not catalogue limits.
 G=79000.;d=.50;D=2.65;na=4.20;lf=6.035;k=G*d**4/(8*D**3*na)
 lo=3*.9*k*(lf-.05-(4.63+.07));hi=3*1.1*k*(lf+.05-(4.63-.20-.07))
 wh=(4*D/d-1)/(4*D/d-4)+.615*d/D
 springs=dict(count=3,wire_mm=d,mean_D_mm=D,active_turns=na,G_Nmm2=G,k_each_N_mm=k,free_mm=lf,nominal_draw_N=3*k*(lf-4.63),nominal_LOCK_residual_N=3*k*(lf-5.69),conditional_draw_min_N=lo,conditional_jammed_reset_max_N=hi,absolute_min_length_mm=4.63-.20-.07,nominal_solid_height_mm=(na+2)*d,max_Wahl_shear_MPa=8*(hi/3)*D*wh/(pi*d**3),stop_separation_travel_mm=1.26,geometric_cage_travel_mm=.20)
 guide={}
 for f in [.06,.12,.18,.23]:
  fac=2*14.5/6.25;guide[str(f)]=dict(eccentricity_factor=fac,friction_feedback=f*fac,required_unlock_push_N=19.096/(1-f*fac) if f*fac<1 else None)
 # Euler assumes a straight pin-ended rod and E=200 GPa. Exposed root-to-first support at home.
 free=abs(-31.67-(-10.90));rod=dict(length_mm=free,stress_all_35N_MPa=35/(pi*.45**2),pinned_buckling_N=pi**2*200000*(pi*.45**4/4)/free**2)
 dump('rating82.json',dict(label='exploratory',thread_model_80=rr,force_cap=springs,guide=guide,rod=rod,thread_hold=dict(lead_deg=degrees(lam),mu_threshold_square=tan(lam),mu_threshold_ISO60=tan(lam)*cos(pi/6),friction_angle_square_deg={str(m):degrees(atan(m)) for m in [.23,.08,.05,.03]},lossless_lowering_Nmm_at_45N=45*lead/(2*pi),independent_restraint_installed=False),
 drive=dict(GH_max_continuous_Nmm=25,GH_max_intermittent_Nmm=35,rated_motor_Nmm=.156,rated_motor_A=.142,GH_radial_N=.5,GH_axial_N=.5,unverified_mesh_eff=.88,GH_max_eff=.60,ratio=3.5,if_rated_2500rpm_eject_seconds=8.1/(.50*2500/(256*3.5*60)),GH_continuous_speed_limit_rpm=8000),
 power=dict(cell_min_voltage_V=3.,cell_continuous_A=2.,four_motors_22C_rated_A=4*.142,four_motors_3V_start_reference_A=4*3/16.2,trial_logic_drivers_extras_A=.28,cell_side_at_four_starts_with_10pct_low_R_and_85pct_converter_A=(4*3/(16.2*.90)+.28)/.85,no_pack_pulse_credit=True)))
def service():
 b=book();mm=pose(b,'DRAW',1,0);results={}
 def test(n,part,obs,axis,stroke,step=.50):
  # Nominal samples and a continuous clearance lower bound for linear translation.
  # Distance is 1-Lipschitz; inflate the minimum sampled distance by half a grid.
  a=np.array(axis);f=np.linspace(0,stroke,ceil(stroke/step)+1);dt=(f[1]-f[0]) if len(f)>1 else 0.;worst=(0,0,None);minsep=100.
  for t in f:
   m=part.translate(a*t);bm=flat(m)
   for k,q in obs.items():
    bq=flat(q);dvec=np.maximum(np.maximum(bm[:3]-bq[3:],bq[:3]-bm[3:]),0);bd=np.linalg.norm(dvec)
    if bd<minsep+.001:
     sep=m.min_gap(q,min(2.,minsep+.002)) if bd<2 else bd
     minsep=min(minsep,sep)
    if aabb(bm,bq):
     v=common(m,q)
     if v>worst[0]:worst=(v,t,k)
  results[n]=dict(direction=a.tolist(),path_mm=stroke,step_mm=dt,worst_sample_intersection_mm3=round(worst[0],7),distance_at_worst_mm=round(worst[1],6),obstructing_part=worst[2],continuous_polygon_gap_lower_mm=max(0,minsep-dt/2),obstacles=list(obs))
 def only(*names):return {k:mm[k] for k in names}
 shell=only('outer clamshell 0','outer clamshell 1')
 test('rear sleeve into empty barrel',mm['sleeve'],only('barrel','sleeve guide 0','sleeve guide 1','V seat annulus'),[-1,0,0],18.,.05)
 test('sleeve after fixed eject bushes',mm['sleeve'],{n:m for n,m in mm.items() if 'rod bush' in n},[-1,0,0],18.,.25)
 test('eject ring from nose before rods attached',mm['ejector lip'],only('pilot','V seat annulus','pilot web 60','bush anchor 60'),[1,0,0],4.,.04)
 test('barrel nose insertion into populated front',mm['barrel'],shell,[1,0,0],21.,.4)
 test('uncoupled rear M3 screw WITH flange after thrust housing',mm['sleeve M3 screw']+mm['sleeve shaft thrust flange'],only('sleeve F3-8M 0','sleeve F3-8M 1','sleeve seat shoulder 0','sleeve radial bearing socket 0'),[-1,0,0],43.,.5)
 test('aft thrust bearing over screw bare end before wheel installed',mm['sleeve F3-8M 0'],only('sleeve M3 screw','sleeve shaft thrust flange'),[-1,0,0],12.,.1)
 test('sleeve nut through assembled rear radial bearing',mm['sleeve nut'],only('sleeve L730ZZ 0','sleeve F3-8M 0'),[-1,0,0],28.)
 test('rear gear onto bare screw with rear lid removed',mm['sleeve wheel root'],only('sleeve L730ZZ 0','sleeve radial bearing socket 0','sleeve tail shroud') if 'sleeve tail shroud' in mm else only('sleeve L730ZZ 0','sleeve radial bearing socket 0','tail shroud'),[-1,0,0],12.)
 test('M2 socket-driver barrel through closed rear face',cyl((-55,-39.5),1.82,14.5,0),shell|only('sleeve rear lid'),[1,0,0],0.)
 test('cell lid removal along own radial normal inside fixed cover',mm['cell service lid'],shell,[0,*at(1,CELL)],10.)
 test('split clamshell close over installed yaw motor',mm['outer clamshell 1'],only('yaw motor body','sleeve 0615 + 06/1'),[0,1,0],15.)
 # Practical engagement of translating nuts, independent of the threadless analytical solid.
 for g in TN:
  starts=[TN[g]+phase(ph,t)[g][0] for ph,t in poses()]
  overlap=min(max(0,min(q+1.75,-6.20)-max(q-1.75,-26.30)) for q in starts)
  results[g+' thread']=dict(continuous_min_nominal_mm=overlap,full_turns_after_two_half_pitch_end_chamfers=(overlap-.5)/.50)
 dump('service82.json',dict(label='exploratory',tests=results))
def ledger():
 b=book();mm=pose(b,'DRAW',1,0);groups={};pcs=[];lower=4*(4+2)+2.90+6*.84
 rho=dict(steel=.00785,bronze=.0088,bearing=.00785,thrust=.00785,PA12=.00102,spring=.00785,electronics=.00896,wire=.00896,**{'7075':.00281})
 # Nominal closed faceted part volume and exact centroid for that mesh (tetra decomposition).
 for n,m in mm.items():
  _,_,mt,k=b[n]
  if k=='air':continue
  me=m.to_mesh64();v=me.vert_properties[:,:3];tri=v[np.array(me.tri_verts,dtype=int)];ref=v.mean(axis=0);tri=tri-ref
  w=np.einsum('ij,ij->i',tri[:,0],np.cross(tri[:,1],tri[:,2]));vol=w.sum()/6.;cen=ref+(w@(tri.mean(axis=1)*.75))/w.sum()
  if mt=='catalog':mass=6.0
  elif mt=='cell':mass=2.9
  elif mt=='thrust':mass=.84
  else:mass=vol*rho[mt]
  groups[mt]=groups.get(mt,0)+mass;pcs.append((mass,cen))
  if n.startswith('own ball') or n.startswith('roller ') and n!='roller cage':lower+=vol*rho['steel']
 tot=sum(groups.values());c=sum(m*p for m,p in pcs)/tot
 dump('mass82.json',dict(label='exploratory',gross_listed_g=groups,gross_subtotal_g=tot,subtotal_COM_DRAW_zero_yaw_mm=rounded(c),selected_nominal_partial_min_g=lower,as_built_mass_upper_g=None,as_built_COM=None,nominal_all_four_foot_margin_mm=min(8-abs(c[1]),c[0]+32,-7-c[0]),notes='Gross listed material only: bearings, PCB and spring reservations billed as envelopes, overlapping joints can double count. Nominal catalog masses not tolerance bounds; missing fasteners/wires/adhesive and collision fixes not bounded.'))
def inventory():
 b=book();res=[]
 for n,(m,g,mat,k) in b.items():res.append(dict(name=n,group=g,material=mat,kind=k,volume_polygon_mm3=round(m.volume(),7),bbox_mm=rounded(flat(m))))
 dump('installed82.json',res)
 # Full editable mesh viewer written as text OpenSCAD; optional section/pose controls.
 # Use polygonal material, not pictures or inflated bounding boxes.
 with open('cutaway82.scad','w') as f:
  f.write('// Take 82 exploratory: red = independent actuation, blue = yaw, yellow = tail.\n// Inspect geometry, not evidence of loaded clearance. Base = DRAW; use section=true for half view.\nsection=true; show_cover=false; show_guest=false;\n')
  f.write('module solid82(){\n')
  for n,(m,g,mt,k) in b.items():
   if k=='air':continue
   approx=m.simplify(.002).to_mesh64();v=np.round(np.asarray(approx.vert_properties)[:,:3],4);idx=np.asarray(approx.tri_verts)[:,::-1]
   c='gold' if g=='guest' else 'royalblue' if g=='yaw' else 'tomato' if g!='fixed' else 'silver'
   s='if(show_guest)' if g=='guest' else ('if(show_cover)' if mt=='PA12' else '')
   f.write('// '+n+'\n'+s+' color("'+c+'") polyhedron(points='+json.dumps(v.tolist(),separators=(',',':'))+',faces='+json.dumps(idx.tolist(),separators=(',',':'))+');\n')
  f.write('}\nif(section) intersection(){solid82(); translate([-64,-60,-60]) cube([120,60,120]);} else solid82();\n')
if __name__=='__main__':
 for f in sys.argv[1:] or ['ratings','service','mass','stock']:{'ratings':ratings,'service':service,'mass':ledger,'stock':inventory}[f]()
