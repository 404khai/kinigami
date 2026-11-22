"""Alternative positive barrier: one axially translated, nonfloating saddle."""
from exit import *

def saddle():
    # Monolithic R13.95 piston, positive X slide. Six dry primary faces
    # integral to it, all on a hard stop at lock. Keep original key and
    # full two guide lands on the fixed housing. Open one through-C slot
    # for the parked key/guide only (one piece, not a detached island).
    rp=13.95; bore=14.05; zslot=2.395; ycut=3.73
    floor=-8.15;end=2.85; thick=1.60; deb=.020
    # Enclose axis/runout, slot width uncertainty, rounding and boundary
    # position by *one-sided* .025 at each material boundary. It is the
    # section actually inside the piston, outside its front/back rounds.
    effz=zslot+.025;effR=rp-.025;Bmax=bore+.025
    # For a point in the missing strip |z|<effz, y>=0 move first to
    # z=±effz, then retreat in y as needed to meet surviving circular
    # land there. Includes the real arc/slot junction, not a 2D slit.
    snag=hypot(effz,Bmax-sqrt(effR**2-effz**2))
    # Maintain the full z window across both unaltered guide bands; only
    # the two separate axial cheeks carry on outboard. Never cross the
    # parked shank there. Two extra axial lands in the receiver rear are
    # specification changes; stress/twist remain to be tested.
    sn0=snag; cut2=12.84; z2=1.80; assert hypot(cut2+.05,effz)<effR
    snag=max(effz,hypot(z2+.025,Bmax-sqrt(effR**2-(z2+.025)**2)))
    rho=2.45
    assert snag<rho
    # Use a moving section inside a THIN plate, not 13 mm solid piston.
    # Favorable side at start; center cannot first cross x_guard with
    # r<=B. Above the bore, to reenter the lagging side requires crossing
    # r=B at x<=x_guard, excluded by the continuous thin front ring or
    # by the receiver including its narrow transverse guide port.
    guard=2.38;tol=.10;innerroot=Bmax
    assert end+tol-thick+.10<guard<rho and .10<end-tol-guard
    # Specify a full ring at x=-.070..0 after the blind slot undercut;
    # on its negative-X side the outer access window is at most
    # |z|<=2.405. At r=Bmax the nearest surviving cylinder sector,
    # including circle curvature, is at chord distance below rho.
    wz=2.405+.020
    port_cover=hypot(wz,Bmax-sqrt((bore-.025)**2-wz**2))
    assert port_cover<rho
    spare=sqrt(rho*rho-snag*snag)
    # For centers x>Rmax near the outside lip the shell no longer restricts
    # r<=Bmax. Do NOT use spare to claim unconditional clearance exterior
    # to the shell; this is a bore-side bound.
    b=B[1];bend=S[1];seg0=b-Q
    frac=np.clip((bend-Q)@seg0/(seg0@seg0),0,1)
    d_elbow=norm(bend-Q-frac*seg0)
    assert d_elbow+RS<rho
    # Lower center X of forks vs hub-body center when pitch ≤ bound
    # (yaw about global X unrestricted). Protect stud/fork independent
    # of roll with farthest y,z radius; no universal anti-flip stop.
    forkrel=[]
    for xx,wy,wz in [(4.,3.3,5.08),(6.75,2.15,6.45),(11.46,1.45,6.66)]:
        forkrel.append((xx-2.50)*cos(radians(30))-hypot(wy,wz)*sin(radians(30))+rho)
    # Fixed housing to moving saddle: original Vs above deck remain;
    # rear roots are union with floor and cropped on bore OD. At each
    # primary pole use global transverse distance to trim cylinder.
    pole=[]
    for bi,ph in zip(B,PH):
        t=-T*sin(ph)+Z*cos(ph)
        for j in [-1,1]:
            n=D*cos(radians(65))+j*t*sin(radians(65))
            pole.append(rp-.05-norm((bi-R*n)[1:]))
    # Original 74 V towers span all r>=8.95 and |t|<=3.81 in station
    # section. The ±60° sectors stay entirely outside the guide z band.
    # Negative y tower's most positive y is at h=-.56 and r=8.95.
    # Fixed hardware during deploy; overlap still impossible before park
    # at HOME because floor stays behind XB.
    return dict(piston_radius=rp,slot_min_y=ycut,slot_half_z=zslot,piston_floor_home=floor,
       piston_floor_extended=end,thickness=thick,stroke=end-floor,tail_key_floor_at_home=XB-floor,
       min_gap_slot_to_key=Y0+PARK-ycut,min_gap_slot_to_guide=zslot-ZG,
       side_tower_guide_gap=8.95*sin(pi/3)-3.81*cos(pi/3)-ZG,
       negative_tower_to_slot=ycut-(-.56*s-8.95*c),primary_land_to_od=min(pole),
       outboard_slot_change_y=cut2,outboard_half_z=z2,
       straight_slot_empty_radius=sn0,bore_side_worst_empty_radius=snag,Rmin_minus_empty_radius=rho-snag,
       extended_rear_x=end-thick,terminal_plane_rim_allowance=.10,
       home_rear_x=floor-thick,full_front_ring_x=[-.070,0.],
       side_port_cover=port_cover,guard_terminal_x=guard,
       stationary_lip_x=0,terminal_flat_bore_side_trailing=guard+spare-2.55,
       stem_elbow_chord_fraction=frac,stem_chord_distance=d_elbow,
       stem_margin_to_thick_hull=rho-RS-d_elbow,fork_margin_if_30deg=min(forkrel))
if __name__=='__main__':print(json.dumps(saddle(),indent=2))
