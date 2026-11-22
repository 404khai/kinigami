"""Finite geometry, support and center-law offsets (mm). Run standalone for sweep."""
from math import *
import numpy as np
import json
from scipy.optimize import brentq
X,Y,Z=np.eye(3); rad=radians; mu=.23; W=.070*9.81; c45=1/sqrt(2)
r0=3.85+1.5*c45+.020; r1=7.04; u0=-3.70; A=pi/4; toe=3; heel=1.2
line=(r1-r0-(toe+heel)*(1-cos(A)))/sin(A)
knots=[u0,u0+toe*sin(A),u0+toe*sin(A)+line*cos(A),u0+(toe+heel)*sin(A)+line*cos(A)]
def params(x):
    if x<=knots[0]:return r0,0.
    if x<knots[1]:
        a=asin((x-u0)/toe);return r0+toe*(1-cos(a)),a
    if x<knots[2]:return r0+toe*(1-cos(A))+(x-knots[1])*tan(A),A
    if x<knots[3]:
        a=asin((knots[3]-x)/heel);return r1-heel*(1-cos(a)),a
    return r1,0.
def surf(x,h):
    y,a=params(x);return x-h*sin(a),y+h*cos(a)
def height(x,h):
    k=brentq(lambda q:surf(q,h)[0]-x,x-2,x+2)
    return surf(k,h)[1]
def contacts():
    ns=[];cs=[];ps=[]
    for a in np.radians([60,180,300]):
        c=8.2*np.array([0,cos(a),sin(a)]);e=np.array([0,-sin(a),cos(a)])
        for s in [-1,1]:
            n=X*cos(rad(65))+s*e*sin(rad(65));ns.append(n);cs.append(c);ps.append(c-1.5*n)
    for a in np.radians([0,120,240]):
        e=np.array([0,cos(a),sin(a)]);n=-c45*(X+e);c=-4.22*X+r0*e
        ns.append(n);cs.append(c);ps.append(c+1.5*n)
    return tuple(map(np.array,(ps,ns,cs)))
boxes={'service':(-4*W,4*W,W,W,46*W,50.8*W,52.2),'table':(-20,W,25*W,40*W,46*W,50.8*W,hypot(50.8,46)*W),'fault':(-4*W,4*W,4*W,4*W,46*W,50.8*W,52.2)}
def geom():
    # Body radial maxima incl tilt/offset of Take83 tube; surfaces use cuts
    # 1.48<|t|<4.25 all u=-6.0..1.48, under roof y=8.05.
    rc=hypot(4.25,2.90); spine=hypot(3.80,3.48)
    # worst relative center x (±.025 pin play); changing y follows the normal offset.
    xlo=-4.245-.025; xhi=-4.0+.025
    umin=xlo; umax=xhi+4.60
    park=min(params(-4.02-.025+4.60)[0],r1)-.060
    # Shoulder of Take82 strict pin less than .139+6.761sin(.95deg) additional radius.
    out=dict(label='exploratory',g_start=r0,g_end=r1,knots=knots,straight_length=line,
      sleeve_profile_toe_R=toe-1.50,exit_R=heel+1.50,positive_lift_toe_R=toe+.56,lift_exit_R=heel-.56,
      double_cam_min_normal_play=.56-.5,through_sleeve_slot=dict(u=[-6,1.48],abs_t=[1.48,4.25],y_top=8.05),
      slot_roof_min_ligament=9.60-hypot(8.05,4.25),roller_roof_min_ligament=9.60-hypot(8.54,1.48),
      cheek_side_clearance=8.05-7.84,strap_top_clearance=8.05-7.91,
      cheek_axial_slot_play=.525-.50,endcap_clearance=3.90-3.84,
      pin_tip_to_endplate=3.90-3.84,max_pin_rtop=r1+.5,top_strap_above_pin=7.72-(r1+.5),
      blade_side_to_cheek=3.48-3.28,blade_side_to_endplate=3.90-3.78,strap_above_cam=7.72-(r1-.56),
      front_bridge_x_gap=1.26-(umax+.5),slot_back_to_cheek=(umin-.95)-(-6),old_closed_slot_front_remaining=1.48-(umax+.95),nominal_forward_cheek_overhang=umax+.95-1.48,
      cheek_min_rad=rc,cam_min_rad=spine,cheek_to_pin_full_OD=rc-4.60,blade_to_pin_full_OD=spine-4.60,
      shaft_to_bulk_shoulder_while_draw=hypot(r0-.50,1.50)-4.60,minimum_park_center=park,
      guaranteed_park_inner=park-1.5,loaded_upper_park_inner=r1-1.5,rod_bush_to_scallop=.80-.68,
      ball_to_widest_sector_side=8.2*sin(pi/3)-1.50-4.32)
    # Actual integral journal, through the sleeve-core boundary: for 1.48<|t|≤1.5 there is EXTRA relief,
    # not a lip. Cheek x extent escapes the cut in front at park; extend the side cut past sleeve nose.
    out['slot_front_is_open']=True
    # Open slot goes THROUGH front at u=+1.48. No solid endwall in the
    # |t| cheek/endwall lanes. Bridge only in each lower cam's own lane.
    out.update(edge_relief=dict(abs_t=[1.48,1.64],y_top=8.65),edge_side_margin=1.64-1.50-.060,
        edge_roof_margin=8.65-(r1+1.50),edge_roof_ligament=9.60-hypot(8.65,1.64),
        blade_clear_cage_toe_aft='not included; Take84 scalloped plate',
        body_to_cheek=2.90-(1.50+.060),fixed_seat_slot_to_outer_sector=4.32-4.25,
        continuous_nominal=['upper surface and lower pin cam are signed normal offsets of the convex/concave center curve, maximum offset positive 1.5 < convex curvature radius 3, negative 0.56 < concave radius 1.2',
        'circle at any u on center path cannot cross either offset: graph is monotone with slopes 0..1 and all normals are nonintersecting over offset interval',
        'roof checks use largest radial height (PARK); slot and blade-side checks use absolute t and extremal u incl cage travel, not selected states'])
    # The min-radius trunnion estimate using full R4.60 is insufficient for an
    # offset head at DRAW. Actual retained 45 degree plane cut at this clock:
    # y <= max(3.2,3.85+x_shoulder-x). Rotation+translation inflate both X,Y.
    b=rad(1.08);infl=.144+2*sin(b/2)*hypot(6.761,4.60)
    ztail=max(3.20,3.85-5.26066017-(xlo-.50-infl))+infl
    out.update(shoulder_cut_inflation=infl,shaft_to_retained_shoulder=r0-.060-.50-ztail,
        centered_low_path_trunnion_r=hypot(r0-.06-.50,1.50)-4.60)
    # Conditional tilt/roll budget from TWO full circumference bands, bore & key
    # clearances only (no credit for the nut). Include .001 for cross terms.
    slope=.10/8.65;roll=.041/8.64
    def drift(x,r):return .050+max(0,x+6.25)*slope+r*(sqrt(1+slope**2)-1)+r*roll+.001
    dn=drift(.20,9.60);dc=drift(-3.10,9.60)
    out['hardened_sweep_proposal']=dict(guide_slope=slope,key_roll_rad=roll,nose_drift=dn,cheek_lane_drift=dc,
        V_window_half=4.46,minimum_V_land_to_new_cut=8.2*sin(pi/3)-1.5*sin(rad(65))*cos(pi/3)-.45-4.46,
        new_window_reserve=4.46-4.25-dn,old_window_reserve=.070-dn,
        side_cut=4.40,edge_relief=1.78,blade_t=[3.48,3.72],side_roof_ligament=9.60-hypot(8.05,4.40),
        endwall_side_margin=4.40-4.15-dc,blade_endwall_side_margin=3.90-3.72-dc,
        edge_side_margin=1.78-1.5-.060-dc,edge_roof_ligament=9.6-hypot(8.65,1.78),
        blade_cheek_margin=3.48-3.28-dc)
    return out
if __name__=='__main__':print(json.dumps(geom(),indent=2))
