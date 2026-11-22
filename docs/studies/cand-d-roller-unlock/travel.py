"""Finite pin, annulus, pilot, contact reach and take-up dimensions (mm)."""
from math import *
from scipy.optimize import brentq
import json
import take80 as b
from lands import closure
mu=b.MU; xc=-4.20; h=4.60
shoulder=xc-1.50/sqrt(2)
back=shoulder-(h-3.85)-.75
boss=.70; Ro=6.32; Ri=5.4; pilot=5.10
def rail():
    x=-5.62; y=4.094; a=3.85+shoulder-x
    return dict(x=x,y=y,ball_inside_both=min((a-y)/sqrt(2),x-(-5.71),-5.53-x,y-4.03,4.71-y,1.50,h-y),
      head_radius=h,rail_outer_at_y4p12=hypot(4.12,1.5))
def exit_path():
    # Ring stays at p=.70+1.75; tail rotates about rim tangent x=p,y=-Ro.
    # Fixed guide/support/roller obstructions independently evaluated in README.
    d=1.75; P=boss+d
    def vals(a):
        X=P+Ro*tan(a)
        # local O is at center of boss rear face; body X below is nominal lip coord
        return (boss+cos(a)*(xc-X)-6.4*sin(a), sin(a)*(xc-X)+6.4*cos(a),X)
    ang=brentq(lambda a:vals(a)[1]-h-1.5,0,.12)
    x,y,X=vals(ang)
    assert back<x<back+.75
    # For increasing angle, body's right support flat y_body=h, infinite plane bounds
    # all pin stock; until first contact cylinder distance >0. At tangent x is on crown.
    # For any z on pilot, pin radial envelope by projected infinite cylinder.
    C=closure(.020); beta=radians(C['angle_deg']); t=C['translation']
    # For a disk perpendicular to body axis, transverse projection <= R, centers
    # drift <= |x|sin(beta). Thus this holds everywhere, not just at one x.
    head_envelope=h+t+abs(back)*sin(beta)
    boss_overlap=6.65*cos(beta)-Ro-(t+boss*sin(beta))
    bearing=abs(back-boss)*cos(beta)+h*sin(beta)
    # Independent whole-model terminal gap only in bounded orientation / flange coverage.
    return dict(ring_home=.10,ring_max=8.20,full_stroke=8.1,head_back=back,
      parked_tilt_contact_deg=degrees(ang), ring_position=P,catch_body_x=x,head_full_crown=[back,back+.75],
      roller_center_x=xc, max_radius_at_pilot_during_tilt=h/cos(ang)+(X+2)*tan(ang),
      max_extent_at_other_rollers=h/cos(ang),min_other_roller_gap_lower=4.90-h/cos(ang),
      min_registry_x_after_straight=d-1.5-8.20*sin(ang)+Ro*tan(ang),
      boss_min_edge_left=6.65-Ro/cos(ang),
      strict_parked_roller_reserve_if_tube=4.90-head_envelope,pilot_reserve_if_tube=pilot-head_envelope,
      boss_full_annulus_overlap_if_tube=boss_overlap,nose_needed_if_tube=bearing,
      min_actual_travel_if_tube=bearing-.10,terminal_pin_clear_if_tube=8.20-bearing,
      lip_contact=dict(d=4.90,side=.50,crown_x=[back+4.90,back+.75+4.90],edge_of_rearmost_roller=xc+1.5),
      apothem_variant_corner=hypot(h,1.90),flat_clock_roll_deg=degrees(atan2(1.90,h)),
      symmetric_free_return_under_20N=True)
def drive():
    e=.02+.025; reserve=.025/cos(radians(65))+.040/sin(pi/4)
    return dict(nominal_cage_midpoint=xc-e,reset_to_nominal_contact=.20+e,
        illustrative_independent_gap_budget=reserve,illustrative_series_k=150,
        illustrative_45N_compliance_travel=45/150,trial_driven_stroke=.20+e+reserve+45/150,
        axial_force_in_tail_per_normal_min=(1-mu)/sqrt(2),
        one_wall_each_release_outward_per_tail_N=(1-mu)/sqrt(2)-mu/(1-mu)*((1+mu)/sqrt(2)+mu),
        sleeve_drag_if_driving_cage_conditional_muN=mu,
        max_table_side=hypot(25*b.W,40*b.W),rim_only_side_at_20N=20*mu,
        ring_cop_20N_M52=52.2/20,rod_triangle_inradius=5.82/2,
        annulus_mean_radius=(5.4+6.32)/2,
        rod_max_two_dim=20*(1+2*(52.2/20)/5.82)/3,
        no_other_drag_straight_push=20)
if __name__=='__main__':print(json.dumps(dict(label='exploratory',rail=rail(),exit=exit_path(),drive=drive()),indent=2))
