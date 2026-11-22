"""A loaded noncentral departure and guide/load budgets; limits are not hardware ratings."""
from exit import *
from saddle import saddle
def study():
    ang=atan2(s,c);L=R+RF;KY=Y0+RF;KX=Q[0]+(L-(KY-Q[1])*s)/c
    dx=KX-Q[0]; dz=.025*dx
    # theta motion on toe: center=(kx-L cos(theta),Qy,dz) with key
    # travel Qy+L sin(theta)-ky. Unit tangent gives actual slip direction
    # incl z motion. No use of pose sensing or restriction to z=0.
    tr=[]
    for ph,b in zip(PH,B):
        for j in [-1,1]:
            n=D*cos(radians(65))+j*(-T*sin(ph)+Z*cos(ph))*sin(radians(65))
            tr.append((n,b))
    # Recess one nonlimiting primary initially; keep it until the end.
    ratios=np.array([-n[2]*dz/n[0] for n,b in tr]); k=int(np.argmax(ratios))
    recessed=int(np.argmin(ratios));loss=.020
    ratios[recessed]-=loss/tr[recessed][0][0]
    lag=max(ratios);n,b=tr[k]
    # Static contact indicator at pickup is a consequence of nonpenetration,
    # not commanded tail motion: one leading face, remaining gaps measured.
    gaps=[lag*nn[0]+dz*nn[2]+(loss if i==recessed else 0.) for i,(nn,_) in enumerate(tr)]
    # Nominal mirror pair may meet simultaneously; a load witness can
    # act only at k, without assuming even a pair of equal reactions.
    ext=-.45*n;mom=np.cross(b-O-R*n,ext)
    assert max(abs(ext))<.686466 and max(abs(mom))<31.5774
    # Through dry sliding key contact before the toe end, taper N to 0.
    # |resultant|<=.45sqrt(1+mu²), moments bounded by actual lever.
    ext0=.45*hypot(1,MU);lever=norm(Q-O)+R
    # Project bearing reactions in XY and ZY individually. Need a measured
    # multiplier for antiroll and excess/opposed pressure (not provided
    # by the Take74 bore); give an explicit conditional example.
    endshift=.10; pitch=2.40; over=9.45-Y0+endshift
    Hx=1.34+.04;Hz=1.65+.04
    Kf=hypot(1,MU)
    raw=Kf*(sqrt(2)*(1+2*over/pitch)+2*(Hx+Hz)/pitch)
    gamma=2*(Hx+Hz)/pitch
    mr=.12;roll_extra=1.0
    sumR=(raw+roll_extra)/(1-mr*gamma)
    ass=sin(ang-ETA)-MU*cos(ang-ETA)
    # Distinct reaction bound for saddle rolling guide: after fixed-stock
    # AIR has been established total F,M on saddle equal external F,M
    # transported to the guide, regardless of which V face is carrying.
    have={'service':(2.745862,.686466,.686466,31.5774,34.8724,120.7836),
          'table':(3.432328,.686466,.686466,48.7391,62.3311,167.8285),
          'fault':(2.745862,.686466,.686466,31.5774,34.8724,169.0970)}
    # Provisional two radial stations on a common primary rod, plus
    # ONE opposed-Z antiroll shoe on second rod. No nominal even sharing.
    # Driver aligned on primary axis. Radial resultants pass through the
    # primary axis. Axial guide friction at contact radius feeds bending.
    ga={}; gm={}
    # The sole possible stationary contact during saddle ejection is on
    # a hub generator at the fixed guide leading X edge. When this can
    # occur there is still a rigorous lower bound on primary V/cap/deck
    # forces along D. The lug is over unbroken piston floor, so it bounds
    # saddle lead EVEN IF NO SEAT IS AT A PRIMARY POLE.
    herr=TR+K*hypot(5.8-O[0],7.6)
    gx=GX1+.025
    tguide=R-(2.5-herr-gx)
    nxx=(2.5-herr-gx)/R
    nd=c*nxx-s*sqrt(1-nxx*nxx);hg=nd-MU*sqrt(1-nd*nd)
    lag_lo=HOME-.025-Q[0]+R-e(Q)
    mg0=1.;rim=100;slot=100;sidegap=100
    for name,cc,rr,ds in entities(1025):
        ee=e(cc)+G*tguide+ds+.025
        hh=(cc-O)@D+lag_lo*c-ee
        # Stem and lug are away from towers whenever a hub can bear on
        # the fixed guide. Check all station radial projections allowing
        # the relative axial lag to move the transverse center also.
        z=cc[:,2];w=(cc-O)@T
        gd=100
        for ph in PH:
            ru=w*cos(ph)+z*sin(ph); tu=-w*sin(ph)+z*cos(ph)
            gd=min(gd,np.min(np.maximum.reduce([abs(ru-10.3)-1.35-ee,
                abs(tu)-3.81-ee,hh+.56])-rr-max(abs(lag_lo),tguide)*s))
        if gd<=0:
            mg0=min(mg0,np.min((hh+2.68)/rr))
        rim=min(rim,np.min(13.90-np.hypot(cc[:,1],cc[:,2])-ee-rr))
        slot=min(slot,np.min(np.hypot(np.maximum(3.73-cc[:,1],0),
                   np.maximum(abs(cc[:,2])-2.395,0))-ee))
    assert mg0>cos(radians(65)) and rim>0 and slot>.10
    # Hub/end disk generators: h>=3.07 before pose and relative lag;
    # if at a tower, rear deck edge lies >R below the center. No face
    # can bear on the slot side as the entire hub is globally ahead
    # of the early moving floor.
    assert (2.50-O[0])*c-7.60*s-herr+lag_lo*c-G*tguide+2.68>R
    early=dict(max_t=tguide,relative_axial_lag_lower=lag_lo,
       slot_center_clear=slot,rounded_OD_clear=rim,possible_deck_normal=mg0,
       hub_fixed_D_force=hg)
    for lab,(fx,fy,fz,mx,my,mz) in have.items():
        span=np.array([22.,6.70,5.45])
        M=np.array([mx+span[1]*fz+span[2]*fy,my+span[0]*fz+span[2]*fx,
                    mz+span[0]*fy+span[1]*fx])
        for fixed,at in [(0.,ga),((c*fx+s*fy)/hg*Kf,gm)]:
            # Fixed guide force is bounded in norm. Maximum contact arm
            # about front primary guide center: x<=11,y<=24,z<=6.5.
            mm=np.array([24+6.5,11+6.5,11+24])*fixed+M
            side=mm[0]/10.66;mg=.12; pitch=7.2;rb=1.46
            raw=fy+fz+sqrt(2)*fixed+side+2*(mm[1]+mm[2]+.82*side+
                                mg*(10.74+2*rb)*side)/pitch
            main=raw/(1-2*mg*sqrt(2)*rb/pitch)
            nr=main+side
            at[lab]=dict(ideal_axial=fx,antiroll_shoe=side,total_radial=nr,
               illustrative_pull_if_no_preload_and_mu012=fx+mg*nr)
    assert min(gaps)>-1e-12
    return dict(key_toe_axial=dx,key_toe_offaxis_z=dz,flat_end_stroke=Q[1]+L*s-KY,
        toe_end_stroke=Q[1]+L-KY,key_external_norm_max=ext0,
        key_moment_norm_bound=ext0*lever,first_saddle_pickup=dx-lag,
        relative_axial_at_pickup=lag,pickup_gaps=gaps,loaded_primary=k,recessed=recessed,
        pickup_external=ext.tolist(),pickup_moment=mom.tolist(),
        saddle_11mm_lug_rear=Q[0]+11+lag-R,peak_saddle_steady_f_x=-ext[0],
        key_guide_example=dict(excess_roll_bearing_per_normal=roll_extra,
          mu_g=mr,guide_normal_per_key=sumR,drive_per_key=mr*sumR-ass,
          if_60N_actual_cap=60*(mr*sumR-ass)),saddle_guide_example=ga,
        early_saddle_geometry=early,saddle_with_possible_guide_contact=gm)
if __name__=='__main__':print(json.dumps(study(),indent=2))
