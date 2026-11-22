"""Positive rotary index + positive two-flank polar selector. mm, N, N mm."""
from geo83 import *
from scipy.optimize import minimize_scalar
D=1.60; R=13.50; lead=.5; angle=rad(55);delta=2.62;rr=.38
def r(s):return 5.44-delta*(3*s*s-2*s**3)
def dr(s):return -delta*6*s*(1-s)/angle
def cam(s):return r(s)*np.array([cos(s*angle),sin(s*angle)])
def curv(s):
    v=dr(s); acc=-6*delta*(1-2*s)/angle**2; R0=r(s)
    return (R0*R0+2*v*v-R0*acc)/(R0*R0+v*v)**1.5
def one(F):
    # No static thread-friction credit for passive axial-load backdrive.
    pitchR=(18-.649519*.50)/2;T=F*lead/(2*pi);Bt=T/R
    # Contrasting case: residual motor/gear torque equal to dry raising torque
    # can seat the dog far harder than a lossless backdriven thread does.
    alpha=atan(lead/(2*pi*pitchR));Tdry=F*pitchR*tan(alpha+atan(mu/cos(pi/6)))
    out={}
    for tag,t in [('lossless',T),('dry_raising_residual',Tdry)]:
        B=t/R
        # specify two effective pressure subbands in single guide; do not credit
        # vanishing rear overlap (or equal shear split). Overhung flange at
        # -19.90, near band -17.45, far band -16.25: conditional finite model.
        g=1+2*(19.90-17.45)/1.20
        # Dog load + front guide Coulomb drag at withdrawal; allow yaw +/-1.8°
        # of dog vs hole. No press fit/pinch/burr credit.
        k=tan(atan(mu)+rad(1.8));Q=(k+g*k)*B
        # centerline follower, friction on sliding groove and separate axial guide.
        def torque(s,m=mu):
            slope=abs(dr(s))/r(s)
            tang=(slope+m)/(1-m*slope)
            return r(s)*tang*Q
        q=minimize_scalar(lambda s:-torque(s),bounds=(0,1),method='bounded')
        out[tag]=dict(flange_torque=t,side=B,withdraw_two_support=2*k*B,withdraw_one_support=Q,
            single_support_max_normal=g*B,shaft_overhang_stress_MPa=32*B*2.45/(pi*D**3),
            edge_projected_MPa_at_5um=B/(D*.005),
            isolated_cam_torque=-q.fun,cam_worst_stroke_frac=q.x)
    return out
def study():
    s=minimize_scalar(lambda v:-abs(dr(v))/r(v),bounds=(0,1),method='bounded').x
    mid=r(.5)*np.array([cos(rad(24)),sin(rad(24))])
    def oldwall(s,sg):return (r(s)+sg*.422)*np.array([cos(rad(48)*s),sin(rad(48)*s)])
    dist=[minimize_scalar(lambda v:np.linalg.norm(oldwall(v,sg)-mid),bounds=(0,1),method='bounded').fun for sg in [-1,1]]
    rad_min=min(1/abs(curv(v)) for v in np.r_[0,1,np.linspace(0,1,1001)])
    # A swept disk avoids inner offset cusps even if centerline radius smaller
    # than cutter. Then the far pressure flank may disappear at high curvature.
    return dict(label='exploratory',engagement={'dog_axis_R':R,'nose':-20.32,'rear_bush_overlap':.37,
        'full_both_sign_hole':[-19.9,-17.9],'front_bush':[-17.65,-16.05],'withdrawn_clearance':.20,
        'diametral_dog_backlash_in_sleeve_x':(2*(.85-.80)/R)*lead/(2*pi),'residual_thread_backlash_not_included':True,
        'nut_index_holes':20,'stroke_index_pitches':(4.60/.50%1)*20,
        'grounded_skirt_key_clocks':[30,150,270],'key_radial': [8.64,9.77], 'key_x':[-15.83,-15.45],'key_side_play':.43-.39,
        'gear_root_to_dog_hole':14.925-R-.85,'crossed_roller_gap':.08,'cam_dwell_deg':12,
        'nominal_dwell_dog_play':.424-.38,'residual_engaged_overlap_with_dwell_play':.37-(.424-.38)},
        old_radial_groove_closest_to_follower_center=dist,old_intersection=rr-min(dist),
        roller_center_offset_restraint_proposed=.424,minimum_local_curvature_radius=rad_min,
        worst_slope=-dr(s)/r(s),peak_motion_ratio_mm_per_rad=abs(dr(.5)),worst_slope_at=s,
        conditional_pin_force={str(f):one(f) for f in [33.524,45,100]},
        handoff=dict(flange_hole_R=.85,pin_R=.80,pin_contact_free_if_center_error_lt=.05,
            conservative_inspection_target_radial_mm=.025,full_index_angle_play_deg=degrees(.10/13.5),
            required_T_retake_at_45N_dry=one(45)['dry_raising_residual']['flange_torque'],
            fully_clear_last_overlap_when_nose_forward_of=-17.90),
        caveat='Loads are bounds conditional on stated contact modes. Remote, off-axis selector/yoke loads NOT included in isolated_cam_torque.')
if __name__=='__main__':print(json.dumps(study(),indent=2))
