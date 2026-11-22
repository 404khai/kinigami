from survey84 import *
def ledger():
 b=book();m=pose(b,'DRAW',1,0);parts=[];groups={};moms=np.zeros(3)
 rho={'steel':.00785,'bronze':.0088,'spring':.00785,'7075':.00281,'PA12':.00102,'wire':.00896,'electronics':.00896,'bearing':.00785}
 for n,q in m.items():
  _,g,mat,k=b[n];me=q.to_mesh64();v=me.vert_properties[:,:3];vv=v[me.tri_verts];ref=v.mean(axis=0);vv=vv-ref;w=np.einsum('ij,ij->i',vv[:,0],np.cross(vv[:,1],vv[:,2]));V=w.sum()/6;cent=ref+(w@(vv.mean(axis=1)*.75))/w.sum()
  mass=0 if k=='air' else 14.8 if n=='cross roller CRBT205A' else .84 if ' F3-8M ' in n and not n.endswith('seat') else 6.0 if mat=='catalog' else 2.90 if mat=='cell' else V*rho[mat]
  groups[mat]=groups.get(mat,0)+mass;moms+=mass*cent
  parts.append(dict(name=n,group=g,material=mat,kind=k,bbox_mm=np.round(bb(q),7).tolist(),volume_mm3=round(V,6),mass_ledger_g=round(mass,6)))
 dump('installed84.json',dict(label='exploratory',pose='DRAW end, zero yaw, no guest',parts=parts))
 dump('mass84.json',dict(label='exploratory',subtotal=sum(groups.values()),groups=groups,COM_subtotal_mm=(moms/sum(groups.values())).tolist(),partial_nominal_g=5*6.+14.8+2.90+4*.84,as_built_upper=None,note='5 motor+gearhead envelopes, IKO 14.8 g reference mass and four EZO axial bearings; other bearings, PCB, springs and teeth conservatively costed as gross solid stock. Overlapping attachments, missing drivers/wires/fasteners; neither a 70g unit nor an upper limit on real mass.'))
def ratings():
 mu=.23;eta=.88;gh=.156*256*.60;dm=17.675;lam=atan(.5/(pi*dm));rows={}
 def torque(F,d,collar):return F*(d/2*tan(atan(.5/(pi*d))+atan(mu/cos(pi/6)))+collar)
 for n,F,d,ratio,meshes,collar,rp in [('sleeve centered sensitivity',45,dm,102/14,2,0,15.3),('sleeve old breakaway sensitivity',22.06,dm,102/14,2,0,15.3),('M3 draw',54,2.68,56/16,1,mu*2,6.16),('M3 eject',35,2.68,42/18,2,mu*2,5.04)]:
  T=torque(F,d,collar);ghneed=T/(ratio*eta**meshes);rad=T/(eta*rp*cos(radians(20)));row=dict(axial_N=F,total_output_torque_Nmm=T,gearhead_required_Nmm=ghneed,gearhead_continuous_Nmm=25,gearhead_intermittent_Nmm=35,motor_rated_optimistic_output_Nmm=gh*ratio*eta**meshes,minimum_efficiency_at_rated_motor=ghneed/(.156*256),spur_total_normal_reaction_N=rad)
  if 'sleeve' in n:
   moment=4.0*rad;f=rad+2*moment/25.5;x,y=(1,.45) if F/f<=1.5 else (.67,.67);row.update(ideal_drive_offset_mm=0,guide_feedback=0,crossed_roller_moment_Nmm=moment,CRBT_dynamic_equivalent_N=x*f+y*F,CRBT_static_equivalent_N=f+.44*F,CRBT_C_N=1400,CRBT_C0_N=1290,rating_note='Ring-centered AXIAL load only; one spur mesh still supplies transverse force and a tilting moment. Form errors, preload friction and actual loading open.')
  else:
   # Bracket small pinion center, plus head-side bearing load if screw gear overhangs.
   row.update(F3_8M_axial_N=F,F3_8M_C_N=994,F3_8M_C0_N=932,L730_C_N=384,L730_C0_N=129,pinion_mesh_N_conservative=rad/eta**(meshes-1),each_centered_pinion_L415_N=rad/(2*eta**(meshes-1)),eject_idler_sum_N_upper=(rad+rad/eta) if 'eject' in n else None)
  # Ideal tooth-root comparison only: Lewis 20-deg full-depth form, nominal face.
  # No undercut/profile correction, dynamic/contact factor, tooth quality or allowable.
  module,z,width=(.30,14,2.) if 'sleeve' in n else ((.22,16,1.36) if 'draw' in n else (.24,18,1.36))
  Ft=ghneed*(eta if 'sleeve' in n else 1.)/(module*z/2)
  Y=pi*(.154-.912/z)
  row.update(pinion_tangential_N=Ft,nominal_Lewis_MPa=Ft/(width*module*Y),standard_undercut_risk=z<2/sin(pi/9)**2,
             alloy_allowable_MPa=None,gearbox_rated_speed_trial_rpm=2500,seconds_per_full_stroke_at_2500rpm=(4.6 if 'sleeve' in n else (1.29 if 'draw' in n else 8.10))/.5*ratio*256/2500*60)
  rows[n]=row
 T=torque(45,dm,0);dog={}
 for mode,P in [('lossless',45*.5/(2*pi)/13.5),('dry residual',T/13.5)]:
  xs=[]
  for u in np.linspace(0,1,2001):
   d=2.62*u*u*(3-2*u);nose=-20.32+d
   if nose>=-17.90:continue
   r=5.44-d;rr=2.62*6*u*(1-u)/radians(55);s=rr/r;K=(s+mu)/(1-mu*s)
   flank=(max(nose,-19.90)-17.90)/2;near,far=-17.65,-16.05
   # Use ONE grounded bushing once the opposite support is lost. Coulomb signed reaction magnitudes.
   xf=-17.99+d;L=far-near;k=abs((far-xf)/L)+abs((xf-near)/L)
   basic=mu*P*(1+abs((far-flank)/L)+abs((flank-near)/L))
   fb=mu*k*K
   xs.append((basic*r*K,fb,basic*r*K/(1-fb) if fb<1 else 1e30,u,xf))
  dog[mode]=dict(pin_side_N=P,max_selector_no_yoke_feedback_Nmm=max(x[0] for x in xs),max_feedback=max(x[1] for x in xs),max_same_plane_triangle_bound_Nmm=max(x[2] for x in xs),last_005mm_nominal_bearing_MPa=P/(1.60*.005),warning='Single-bushing conservative surrogate even before loss of far support; friction .23 assumed, loading plane unknown. Divergence as remaining overlap tends to zero. Not a non-galling handoff or a global upper bound.')
 # Cam curvature polar smoothstep incl endpoints. Shifted finite guide sustains follower only if adequate two-point support exists.
 u=np.linspace(0,1,10001);be=radians(55);r=5.44-2.62*(3*u*u-2*u**3);rp=-2.62*6*u*(1-u)/be;rpp=-2.62*(6-12*u)/be**2
 rho=(r*r+rp*rp)**1.5/np.abs(r*r+2*rp*rp-r*rpp)
 d=.4;D=2.14;nt=3.65;k=79000*d**4/(8*D**3*nt);lf=6.17;high=3*1.1*k*(lf+.05-(4.63-.245-.07));w=(4*D/d-1)/(4*D/d-4)+.615*d/D
 dump('rating84.json',dict(label='exploratory',drives=rows,power_off=dog,coaxial_key=dict(count=3,x=[-15.83,-15.45],r_floor=8.59,nominal_key_side_clearance=.04,guide_band_span_mm=8.65),cam=dict(radii=[5.44,2.82],ramp_deg=55,dwell_deg=12,command_deg=73,minimum_centerline_curvature_R=float(min(rho)),normal_groove_halfwidth=.424,follower_R=.38,rear_bush_tip_engagement=.37,zero_lead_dwell_hypothesis=True,rotary_torque_direct_max_cont_Nmm=25,rated_motor_times_GH_max_eff=gh,unbraked_selector_angular_disturbance_capacity=None),bearings=dict(CRBT205A=[20,31,5],L415=[1.5,4,1.2,125,38],gearhead_native_radial_axial_N=[.5,.5],ring_thread_lambda_deg=degrees(lam),ring_thread_mu_threshold_ISO=tan(lam)*cos(pi/6),m3_thread_lambda_deg=degrees(atan(.5/(pi*2.68))),m3_thread_mu_threshold_ISO=.5/(pi*2.68)*cos(pi/6)),centered_drive_friction_note='Lossless when mu=0 both threads can backdrive. M18 torque excludes unknown crossed-roller preload, seal and joint breakaway. Mesh efficiency .88 sensitivity only.',springs=dict(wire=d,mean_D=D,active_turns=nt,free=lf,nominal_k_N_mm=k,assumptions='±10% rate; free ±.05, installed ±.07, grounded cage stop and both drive stops intact; no equal roller load assumed.',nominal_DRAW=3*k*(lf-4.63),min_DRAW=3*.9*k*(lf-.05-4.63-.07),max_jammed_N=high,min_len=4.63-.245-.07,solid_height_assumed=(nt+2)*d,max_wahl_MPa=8*high/3*D*w/(pi*d**3),fatigue_qualified=False),thread_engagement=dict(sleeve_min_nominal=2.65,sleeve_full_turns_after_halfpitch_ends=(2.65-.5)/.5),power=dict(estimated_5_rated_A=5*.142,five_starts_scenario_A=(5*3/(16.2*.90)+.28)/.85,cell_continuous_A=2,thermal_proof=False)))
if __name__=='__main__':ledger();ratings()
