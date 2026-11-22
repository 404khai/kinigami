"""Take 78, exploratory, all lengths mm. Solid distance enclosures, not a dynamics solver."""
import json
from math import *
from pathlib import Path
import numpy as np
from numpy.linalg import norm

I=json.loads(Path(__file__).with_name('take74.json').read_text())['interface']
O,D,T,Q,B,S=map(np.array,[I[k] for k in ('reference','draw','transverse_ridge_axis','lug','registry','stem')])
Z=np.array([0.,0.,1.]);X=np.array([1.,0.,0.]);PH=np.radians([60,180,300])
c,s=D[:2]; R=2.5;RS=1.4; XB,XF=I['shank_x']; Y0=I['key_tip']; RF=.35
GX0,GX1=I['outer_guide_x']; ZG=2.35; H=1.65; PARK=4.85; WALL=14.05
TH=radians(1.85); TR=.17; K=2*sin(TH/2); MU=.23;ETA=radians(.60)
G=tan(radians(5));RP=4.10;HOME=-8.15;END=1.20
P=I['key_contact'];FY=P[1]+(P[0]-XB)*c/s
SW=2.68;EB=.04
def e(b): return TR+K*norm(b-O,axis=-1)
def seg(a,b,n):return a+(b-a)*np.linspace(0,1,n)[:,None]
W=np.array([[2.50,6.25*cos(ph),6.25*sin(ph)] for ph in PH])
def entities(n):
    for k,(a,b) in enumerate(zip(B,W)):
        yield 'wing'+str(k),seg(a,b,n),R,norm(b-a)/(2*(n-1))
    for i,(a,b) in enumerate(zip(S,S[1:])):
        yield 'stem'+str(i),seg(a,b,n),RS,norm(b-a)/(2*(n-1))
    yield 'lug',Q[None,:],R,0.
def gpu(x,y,z):
    return np.hypot(np.maximum(x,0),np.maximum(WALL-np.hypot(y,z),0))
def box(x,y,z,lo,hi):
    def g(x,l,u):return np.maximum(np.maximum(x-u,l-x),0)
    return np.sqrt(g(x,lo[0],hi[0])**2+g(y,lo[1],hi[1])**2+g(z,lo[2],hi[2])**2)
def stock():
    # Relaxed cone: after axial progress t>=0, lateral displacement can be
    # ANY vector of length <=g*t in addition to the retained transform.
    # Norm distances are 1-Lipschitz in the rigidly transformed center.
    tt=np.linspace(0,9.6,385)[:,None];hh=9.6/(2*384)*(1+G)
    out={}
    for name,cc,rr,ds in entities(385):
        xx=cc[:,0]+tt;yy=cc[:,1];zz=cc[:,2];debit=e(cc)+G*tt+hh+ds
        lo=[GX0,8.60,-ZG];hi=[GX1,18.60,ZG]
        bg=box(xx,yy,zz,lo,hi)
        kp=(box(xx,yy,zz,[XB,Y0+PARK,-H],[XF,18.2,H])-debit-rr).min()
        # In the moving-key sweep, exclude all non-lug contacts; taper
        # matters near the branch where the key could run into the stem.
        # Back plane at KEY SLIDE j is translated +jY (so gets shallower
        # in fixed frame). Every translated key is subset of this j=0
        # intersection: ignore the inaccessible finite proximal end here.
        # Distance via multiple faces (projection in XY).
        poly=np.array([[P[0]-(Y0-P[1])*s/c,Y0],[XF,Y0],[XF,18.60],[XB,18.60],[XB,FY]])
        xy=np.full(xx.shape,np.inf);inside=np.full(xx.shape,True)
        for a,b in zip(poly,np.roll(poly,-1,axis=0)):
            v=b-a;u=np.clip(((xx-a[0])*v[0]+(yy-a[1])*v[1])/(v@v),0,1)
            xy=np.minimum(xy,np.hypot(xx-a[0]-u*v[0],yy-a[1]-u*v[1]))
            inside&=(xx-a[0])*v[1]<=(yy-a[1])*v[0]
        allk=np.hypot(np.where(inside,0,xy),np.maximum(abs(zz)-H,0))
        h=(xx-O[0])*c+yy*s;j=-(xx-O[0])*s+yy*c
        nd=1.;tg=float('inf')
        for phi in PH:
            vr=j*cos(phi)+zz*sin(phi);vt=-j*sin(phi)+zz*cos(phi)
            dist=np.hypot(np.maximum(h+.56,0),
                     np.hypot(np.maximum(abs(vr-10.30)-1.35,0),np.maximum(abs(vt)-3.81,0)))
            dleft=dist-debit-rr;tg=min(tg,np.min(dleft));possible=dleft<=.025
            if np.any(possible):
                nd=min(nd,np.min((h+2.68-debit-.025)[possible])/rr)
        assert nd>cos(radians(65))
        out[name]=dict(barrel=(gpu(xx,yy,zz)-debit-rr).min(),
                       guide=(bg-debit-rr).min(),parked=(kp),
                       all_key=(allk-debit-rr).min(),
                       tower_box_clear=tg,deck_edge_min_nD=nd,
                       guide_lower_trial=(box(xx,yy,zz,[GX0,4.50,-ZG],hi)-debit-rr).min())
    # Hub's union of balls: center disk front [x>=2.5,r<=7.60]; disk
    # extrudes to x5.80,R3.16. Nearest axial guide plane bounds contact
    # normals even when a radial distance alone doesn't exclude contact.
    hub_e=TR+K*hypot(5.80-O[0],7.60); hub_x=2.50-hub_e
    hnx=(hub_x-(GX1+.025))/R;hnD=c*hnx-s*sqrt(1-hnx**2)
    return dict(parts=out,hub_key_x=hub_x-XF-R,
        hub_guide_min_nx=hnx,hub_guide_min_D_force=hnD-MU*sqrt(1-hnD*hnD),
        hub_barrel_radial_while_x_reachable=WALL-7.60-R-hub_e-G*(R-hub_x),
        fork_min_x=4.-TR-K*18.)
def withdrawal():
    # Initial tube is larger than the per-pole alternative from Take 77.
    # Use body transform without additionally stacking its local bounds.
    # At first crossing x=gate, the center has to pass the actual flat
    # distal edge below, since it is still in the full z section.
    gate=XF-RF-.40; qerr=e(Q); keyerr=.10
    tx=gate-Q[0]+qerr
    # Use an independent Hausdorff .10 mm error on the moving key.
    # At the gate x there is a full lower flat around it despite this
    # debit; conservatively take the shifted plane and angular rise.
    stmin=Q[1]-qerr-G*tx+R-Y0-keyerr
    max_t=XF+R-Q[0]+qerr+keyerr
    nzstrip=H-RF-qerr-G*max_t-keyerr
    minfront=(Y0+stmin-keyerr-Q[1]-qerr-G*max_t)/R
    assert nzstrip>0 and minfront>s and FY+RF*tan(radians(9))+PARK<8.60
    # nominal key angular allowance example: debit actual reachable pole,
    # not a supposition about an exact assembled ±.10 deg.
    err=radians(.60);w=sin(radians(18)-err)-MU*cos(radians(18)-err)
    # Actual y contact on key is bounded below by Y0 and above by
    # Qy+pose+departure+R. Relative to first band's nearest usable load
    # center conservatively bound overhang by 9.45-Y0, not 9.45-Yq.
    arm=S[1]-Q; aerr=K*norm(arm)
    mx=max(D@arm+aerr+2*sin(ETA/2)*norm(arm),arm[1]+aerr,-arm[0]+aerr)
    assert mx<0
    return dict(gate_x=gate,gate_first_time_ceiling=tx,max_stem_inward_projection=mx,
        first_possible_crossing_stroke=stmin,key_z_fillet_inaccessible=nzstrip,
        min_front_contact_ny=minfront,min_key_open_force_per_N=w,
        first_trial_lower_band_partial=4.50-FY-RF*tan(radians(9)),
        first_trial_lower_band_total_loss=5.35-FY-RF*tan(radians(9)),
        original_full_shank_margin_at_park=8.60-(FY+PARK+RF*tan(radians(9))),
        max_key_shift_at_lug_from_clearance=.04+(8.60-Y0)*.08/(11.85-9.45))
def piston():
    tmax=END-Q[0]+R+e(Q)
    # Once the true R2.5 sphere encounters flat, no last-contact assumption
    # is needed. Difference of rigid body extrema eliminates translation.
    ballmin=min((b[0]-Q[0])-K*norm(b-Q) for b in B)
    tailmin=min(ballmin,0.,min((b[0]-Q[0])+R-RS-K*norm(b-Q) for b in S))
    other=100.
    for name,cc,rr,dd in entities(1025):
        if name=='lug':continue
        # For a stem generator internal to the lug sphere, count only
        # the external sphere. Tube bounds carry through all needle ends.
        axial=cc[:,0]-Q[0]+R-rr-K*norm(cc-Q,axis=1)
        rad=np.hypot(cc[:,1]-Q[1],cc[:,2])-RP-rr-e(cc)-G*tmax
        other=min(other,min(np.maximum(rad,axial))-2*dd)
    assert other>0
    beta=radians(65)+ETA
    seat=cos(beta)-MU*sin(beta); lam=1/(c-MU*s)
    boxF={'service':[2.745862,.686466,.686466],'table':[3.432328,.686466,.686466],'fault':[2.745862,.686466,.686466]}
    aa={}
    for k,(fx,fy,fz) in boxF.items():
        f=lam*(c*fx+s*fy)
        # Only tail contacts at center within this defined tube. Standard
        # 2-band circular ram guide with NO hidden opposing squeeze:
        # net transverse loads <=mu*F; moment from both transverse offset
        # of normal and friction overhang. Continuous piston may spin:
        # residual roll torque addressed separately below.
        er=e(Q)+G*tmax
        h=END-(-10.0); pitch=4.0;mg=.12
        coeff=(MU+2*(er+MU*h)/pitch)/(1-2*(RP+.04)*mg/pitch)
        aa[k]=dict(tail_axial=f,sum_ram_radial_bending_reactions_per_axial=coeff,
             pull_plus_example_guide_drag=f*(1+mg*coeff),roll_torque=f*er*MU)
    return dict(end=END,home=HOME,travel=END-HOME,radius=RP,edge=.20,
        max_t_while_lug_can_lag=tmax,flat_contact_reserve=RP-.20-e(Q)-G*tmax,
        min_trailing_material_relative_to_lug=tailmin,terminal_tail_bound=END+tailmin,
        ram_to_parked_key_y=Y0+PARK-Q[1]-RP,nonlug_ram_clear=other,work_lambda=lam,
        min_seat_forward_per_normal=seat,box_force_bounds=aa)
def main():
    return dict(label='exploratory',stock=stock(),key=withdrawal(),piston=piston())
if __name__=='__main__':print(json.dumps(main(),indent=2))
