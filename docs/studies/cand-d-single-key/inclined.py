"""Finite tilted candidate, separately instantiated from the horizontal trial."""
from stock import poly_dist
from tight import *
U=-NN[0];T=u;Z=np.array([0.,0.,1.]);Q=CC[0]+O;X,Yq,_=PP[0]
XF=X+2.0223587092621167;XB=XF-2.68;Y0=Yq-1.05;RIM=14.05
KY=Y0+FIL;KX=(R+FIL-s*(KY-Q[1]))/c+Q[0]
ST1=(R+FIL)*s+Q[1]-KY
def motion(t):
    d=(KX-Q[0]-(R+FIL)*cos(t))/c
    st=Q[1]+d*s+(R+FIL)*sin(t)-KY
    return st,d
def interface():
    return dict(reference=O,draw=U,transverse_ridge_axis=T,registry=CC[1::2]+O,
      lug=Q,stem=[Q,[-4.00,-4.65,0],[2.50,-6.,0]],stem_radius=1.40,
      flared_wing_end_x_r=[2.50,6.25],hub_core=[2.50,7.60],
      backing=R,key_contact=PP[0],shank_x=[XB,XF],z_half=1.65,
      key_tip=Y0,prox_end=13.35,park=4.85,key_fillet=FIL,
      guide_y=[[8.60,9.45],[11.85,12.70]],guide_sides=.04,
      outer_guide_x=[XB-.52,XF+.58],outer_guide_z=2.35,
      blind_pocket_end_y=18.60,blind_rear_wall_x=-9.15,
      clear_bore_radius=RIM,barrel_outside=15.05,
      seat_local=dict(origin=O,axis=U,radial_reference=T,tangent_reference=Z,
        station_deg=[60,180,300],radius=10.30,deck=-2.68,cap_height=2.12,
        angular_face_draft_deg=65.,radial_and_end_draft_deg=65.,
        half_radial_width=1.35,half_tangent_width=3.81,outer_trim_radius=12.20,
        outer_trim_deg=64.,face_start_t=R*sin(radians(65))-
              (2.68-R*cos(radians(65)))/tan(radians(65))))
def solve():
    xc=X;yc=Yq;full=yc+(xc-XB)/tan(a); end=13.35;pk=4.85
    P=np.array([[xc-tan(a)*(Y0-yc),Y0],[XF,Y0],[XF,end],[XB,end],[XB,full]])
    device=interface();anchors=np.array(device['stem']);rr=device['stem_radius']
    thick=[]
    for aa,bb in zip(anchors,anchors[1:]):
        tt=np.linspace(0,1,513)
        thick.append(aa+(bb-aa)*tt[:,None])
    stalk=np.vstack(thick)
    st2,d2=motion(pi/2)
    regions=[(np.linspace(0,ST1/c**2,65),lambda st:(st,s*st),ST1/c**2/128),
      (np.linspace(a,pi/2,129),motion,2*(R+FIL)/c*(pi/2-a)/256),
      (np.linspace(st2,pk,65),lambda st:(st,d2),(pk-st2)/128)]
    # ST1 here is the horizontal branch break; working plane tangent is
    # reached when the relative travel in station tangent equals ST1*c.
    assert abs(motion(a)[0]-ST1/c**2)<1e-10
    neck=100.
    for arr,f,dp in regions:
        g=100.
        for tt in arr:
            st,dx=f(tt)
            g=min(g,np.min(poly_dist(stalk[:,0]+dx*c,stalk[:,1]+dx*s-st,P))-rr)
        neck=min(neck,g-dp-max(norm(b-a0) for a0,b in zip(anchors,anchors[1:]))/1024)
    # The parked convex key has its smallest T projection at the rounded
    # distal/front edge, exactly. Positive T separation is independent of
    # travel along D, not just a clear gauge at a single end state.
    def gap(st):
        ctr=np.array([XF-FIL,Y0+FIL+st,0.])
        return ((ctr-Q)@T-FIL-R,(ctr-Q)@U)
    kt=min(np.array([XF-FIL,Y0+FIL+pk,0.])@T-FIL-b@T-rr for b in anchors)
    # Lower separation from a continuous cylindrical wall and circular
    # lip: distance from generator center to occupied r>=RIM, x<=0.
    # Debits extend through both swept coordinates; harder knot of a wing
    # will not in general be the leading sphere.
    dc=10.65;Dvals=np.linspace(0,dc,513)[:,None]
    wall=[];wings=[];stems=[]
    for k0,b in zip([PH,pi,5*pi/3],CC[1::2]+O):
        z=np.linspace(0.,1.,257)
        t1=np.array([2.50,6.25*cos(k0),6.25*sin(k0)])
        arr=b[None,:]+(t1-b)[None,:]*z[:,None]
        xx=arr[:,0]+c*Dvals;yy=arr[:,1]+s*Dvals;zz=arr[:,2]
        def cyl(rad):
            return np.hypot(np.maximum(xx,0.),np.maximum(rad-np.hypot(yy,zz),0.))
        debit=norm(t1-b)/512+dc/1024
        wall.append(np.min(cyl(RIM))-R-debit)
        # Inner stationary V faces and their continuous rear supports:
        # all generators go farther in front along own primary planes.
        inds=[i for i in range(1,7) if np.allclose(CC[i]+O,b)]
        wings.append(min((t1-b)@NN[i] for i in inds))
        # Other stations' entire radial slabs start at 8.95 in tilted frame.
        for ko in [PH,pi,5*pi/3]:
            if abs(ko-k0)>.01:
                er=T*cos(ko)+Z*sin(ko)
                stems.append(BR-1.35-max((b-O)@er,(t1-O)@er)-R)
    # Backing of tilted fixed tower vertical in the same D coordinate.
    # |t|<=3.81, radial 8.95..11.65; blind substrate behind the three
    # supported sectors, with no plate spanning the central-lug well.
    lugseat=BR-1.35-max((Q-O)@T,-(Q-O)@T)-R
    # As D draw is along the inclination, D-perp separation remains fixed.
    rel=stalk-O
    stemseat=min(np.maximum(np.linalg.norm(rel-(rel@U)[:,None]*U,axis=1)*-1+BR-1.35,
                 rel@U+.56))-rr-max(norm(bb-aa) for aa,bb in zip(anchors,anchors[1:]))/1024
    # A central full disk rolled hub at global x=2.50, r=7.60 is in front
    # of tilted lands x<=-.1325. Positive global x motion only helps.
    hub=(-.13254366465714895)*-1
    # Hub and forks vs cylindrical lip: for all centerlines moving along
    # D, once center x>=R+lip_x, no guide/bore is reachable. The centered
    # hub's first knot x=2.50,R=2.50. All fork material x>=4.
    # Raised angle produces a true backside contact on a 4.15-park, but
    # neither rear wall nor opposing guide cheeks are hit on corrected path.
    # Positive-z wings always have |z|>=6.25 sin60 - 2.50. Negative-y
    # wing remains away from key until it is already ahead in x.
    neg=Y0-(-6.25+R+(.0-(min(CC[3,0]+O[0],2.5)-R))/c*s)
    side=6.25*sin(PH)-R-2.35
    # Fixed guides begin at y8.60. While x<=XF+.58+R the lug and all
    # stem generators stay below their y-min using their max T projection.
    # y=(T·p + s*x)/c. T evaluated over the fixed body generators.
    guide_lug=8.60-R-((T@Q)+s*(XF+.58+R))/c
    guide_stem=8.60-rr-(max(stalk@T)+s*(XF+.58+rr))/c
    # Once the tail passes entirely ahead x=0, allow 3 deg further pitch
    # about its lug along either sense. No contact or clamp is used to
    # command this free pose.
    clearance=Q[0]+dc*c-R-22*sin(radians(3))
    assert min(neck,gap(pk)[0],kt,min(wall),min(wings),min(stems),lugseat,
       stemseat,side,neg,guide_lug,guide_stem,hub,clearance)>0
    return dict(interface=device,key_flat_end=motion(a),toe_end=[st2,d2],
       old_park_actual_collision_and_station=gap(4.15),corrected_park_gap_station=gap(pk),
       stem_to_moving_key=neck,park_key_to_stem=kt,wing_barrel_clear=min(wall),
       wing_same_seat_plane_delta=min(wings),wing_other_seats=min(stems),
       stem_to_tower=stemseat,lug_to_tower=lugseat,hub_tower_guide_min=min(hub,-XF-.58),
       side_wing_guide=side,opposite_wing_key=neg,guide_lug=guide_lug,
       guide_stem=guide_stem,free_3deg_pitch_lower_mm=clearance,
       guide_differential_at_010deg=4.10*tan(ERR),
       guide_cocking_trial_deg=.50,required_clearance_for_trial=
          4.10*tan(radians(.50))+2.68*(1/cos(radians(.50))-1),
       release_loads=power())
def power():
    mg=.12;hk=1.34;pitch=11.85-9.45;over=9.45-Yq;K=hypot(1,.23)
    raw=K*(1+2*(over+hk)/pitch);gain=2*(hk+.04)/pitch
    reaction=raw/(1-gain*mg);yr=sin(a)-.23*cos(a)
    # Any planar friction direction on the upper/lower working flat/arc.
    # At toe endpoint force on tail has n=-Y; opposed +D can no longer
    # act as a lone balancing force. After flank, no other seat is loaded.
    return dict(min_open_contact_projection=yr,guide_normal_per_contact=reaction,
       max_open_motor_per_normal=mg*reaction-yr,
       mg_before_guide_spends_assist=yr/(raw+yr*gain),preload_cap_example=60.,
       illustrative_motor_at_60N=(mg*reaction-yr)*60,
       no_friction_key_axial_capacity_last_head_X=0.,
       last_draw_axis_projection=s,
       table_one_contact_motor=(mg*reaction-yr)*norm([3.432328,.686466,.686466]))
if __name__=='__main__':print(json.dumps(solve(),default=serialize,indent=2))
