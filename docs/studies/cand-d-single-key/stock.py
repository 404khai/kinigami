"""Finite stock and a load-compatible, release-side path for Take 74."""
from study import *
def poly_dist(x,y,P):
    best=np.inf;inside=True
    for (x0,y0),(x1,y1) in zip(P,np.roll(P,-1,axis=0)):
        dx,dy=x1-x0,y1-y0;u=np.clip(((x-x0)*dx+(y-y0)*dy)/(dx**2+dy**2),0.,1.)
        best=np.minimum(best,np.hypot(x-x0-u*dx,y-y0-u*dy))
        inside=inside & ((x-x0)*dy<=(y-y0)*dx)
    return np.where(inside,0.,best)
def geometry():
    deck=BC-R-.18; cap=deck+1.68; rc=12.20;draft=tan(v)
    face_h=BC-R*cos(v)-deck;t_contact=R*sin(v)
    # Minimum distance in the primary face to every other clipping plane.
    # Signed distance to 3D cutting plane underbounds distance in the face.
    fv=min(1.68-face_h,((3.81-t_contact)*draft-face_h)/hypot(1,draft),
           (1.35*draft-face_h)/hypot(1,draft),
           ((rc-hypot(BR,t_contact))*tan(radians(64))-face_h)*cos(radians(64)))
    dv=.020+R*2*sin(radians(.6)/2)
    fit_marg=fv-fit()['face_pole_shift']-dv
    key_end=12.90; full_y=yc+(xc-XB)/tan(a)
    P=np.array([[xc-tan(a)*(Y0-yc),Y0],[XF,Y0],[XF,key_end],[XB,key_end],[XB,full_y]])
    # Rectangle in the streamwise and z direction with an additional
    # sloped back plane: inscribe radius .35 at every convex intersection.
    # Above is its SHARP superset. The main plane has full sphere tangent
    # from s=0 until ST1 at the fillet. Finite centre flat in z and at
    # the tip, full shank and roof sides.
    wing=min(ST1*c, (full_y-yc)*c-FIL, (XF-xc-FIL),SH-FIL)
    LUGEND=np.array([2.50,-6.00,0.]); stemR=1.45
    z=np.linspace(0,1,513);X=q[0]+z*(LUGEND[0]-q[0]);Yy=q[1]+z*(LUGEND[1]-q[1])
    # Continuous phase cells. Parameterize rounded toe by angle so no
    # mistaken finite dx/ds near pi/2. Pure forward draw while parked
    # is separated by its y plane; can then roll 3° about global X.
    regions=[(np.linspace(0,ST1,65),lambda t:(t,t*tan(a)),ST1/cos(a)/128),
             (np.linspace(a,pi/2,129),lambda t:(q[1]+(R+FIL)*sin(t)-KY,
                   KX-(R+FIL)*cos(t)-q[0]),(R+FIL)*(pi/2-a)/256),
             (np.linspace(ST2,PARK,65),lambda t:(t,shift(ST2)),(PARK-ST2)/128)]
    g=100
    for arr,f,dphase in regions:
        tmp=100
        for t in arr:
            st,xx=f(t);tmp=min(tmp,np.min(poly_dist(X+xx,Yy-st,P))-stemR)
        g=min(g,tmp-dphase-norm(q-LUGEND)/1024)
    # Capsule lobes: at +/-60deg their entire |z| range lies outside
    # every guide and key; at 180deg entirely opposite the guide and key.
    side=6.25*sin(pi/3)-R-2.35
    side180=Y0-(-6.25+R);body_drive=0.-(-.92)
    seats_key=(BR-1.35)*sin(pi/3)-3.81*.5-SH
    # Other seats at radial angle >=120deg: nominal generator r>=6.25,
    # its projection along their radial <=-3.125. Retaining lug and stem
    # do not enter any V/tower, including the opposite third station.
    stem_tower=(BR-1.35)-max(norm(q[1:]),norm(LUGEND[1:]))-stemR
    lug_tower=BR-1.35-(q[1]+R)
    # Blind-guide bore (+.04 per side) in full-section blocks; a rounded
    # shank has flats on all 4 longitudinal faces, unlike a knife in a slit.
    guide=8.60-(full_y+FIL+PARK)
    assert min(guide,key_end-12.70,g,side,side180,body_drive,seats_key,
               stem_tower,lug_tower,fit_marg)>0
    # Worst clearances on one valid post-release 3° rolling branch with the
    # carrier held at PARK, before monotone +X. x advance has opened V caps
    # completely and roll about X does not move any axial extremum.
    roll=radians(3)
    rolled_z=6.25*sin(pi/3-roll)-R-2.35
    rolled_lug=Y0+PARK-q[1]-R
    rolled_stem=Y0+PARK-max(q[1],0)-stemR
    rolled_tower=BC+shift(ST2)-R-cap
    assert min(rolled_z,rolled_lug,rolled_stem,rolled_tower)>0
    return dict(lug_center=q,key_pole=p[0],key_tip_y=Y0,shank_start_y=full_y,
      contact_face_inscribed_margin=fv,seat_margin_after_tolerances=fit_marg,
      key_face_margin=wing,shank_engagement_allowance=guide,stem_to_key_path=g,
      wing_to_guide=side,opposite_wing_to_key=side180,hub_to_drive=body_drive,
      seat_to_key=seats_key,stem_to_seat=stem_tower,lug_to_seat=lug_tower,
      rear_wall_to_lug=q[0]-R-(-8.60),barrel_to_wings=13.35-(BR+R),
      park_lug_y_clearance=rolled_lug,park_stem_y_clearance=rolled_stem,
      postroll_wing_guide=rolled_z,postroll_caps=rolled_tower,
      arm_to_guide_end=12.90-12.70,pocket_rear_end=17.50-12.90-PARK)
def withdrawal():
    # Quasistatic path at z=0. theta in [alpha,pi/2]. Body is free, with
    # a varying external wrench balancing this ONE remaining contact,
    # not assumed centered by a fictitious guide on the neighbor.
    # On key +Y, slip of tail relative to moving key is +(sin,-cos).
    # f_on_key/N=(cos+mu*sin, sin-mu*cos); guide μ independent.
    mg=.12;H=(XF-XB)/2;xmid=(XF+XB)/2
    # Actual pressure resultants in two disjoint y intervals; unknown
    # points bounded with minimum separation; avoid assuming midpoint loads.
    pitch=11.85-9.45;over=9.45-yc
    k=hypot(1,MU)
    # Sharp stock extents bound load point x; guide friction offsets can
    # return a moment proportional to guide reactions times H+clearance.
    raw=k*(1+2*(over+H)/pitch);hf=H+.04
    sumratio=raw/(1-2*mg*hf/pitch)
    flank=s-MU*c
    # For all normal levels bounded by Ncap and no additional squeeze.
    # Normal assistance survives only if mg*sumratio(mg) < flank.
    mgmax=flank/(raw+flank*2*hf/pitch)
    # Representable loading during full toe traversal. Compute last
    # distance in travel giving 0.05 X projection in frictionless limit.
    return dict(flat_end_slide=ST1,toe_end_slide=ST2,air_after_park=PARK-ST2,
        tail_dx_at_edge=shift(ST2),last_005_x_projection_travel=
           (R+FIL)*(1-sqrt(1-.05**2)),contact_open_assist_min=flank,
        illustrative_guide_mu=mg,guide_sum_norm_per_normal=sumratio,
        max_motor_pull_per_normal=max(0.,mg*sumratio-flank),
        motor_at_20N=max(0.,mg*sumratio-flank)*20,
        guide_mu_for_assist_alone=mgmax,at_last_x_contact=0.,
        minimum_tension_capacity_without_friction=0.)
if __name__=='__main__':
    print(json.dumps(dict(label='exploratory',fit=fit(),force=forcewin(),
             stock=geometry(),release=withdrawal()),default=serialize,indent=2))
