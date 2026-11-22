"""Take 58 / exploratory. N, mm, N mm; python3 sector.py [--json]."""
from math import hypot, sqrt, pi, cos, sin
import json
import sys


CORE, R, CX, B, K = 10.75, 2.50, -2.25, 14.50, .28
M, A, SIDE, FIL = .38, 2.20, 1.05, .12
X0, X1, W, S, REAR = -3.50, -.38, 3.20, 1.45, 16.60
GAP, CHEEK, ROUND, MU = .11, .17, .04, .23
NX, NR = M/hypot(1,M),1/hypot(1,M)
XW, RW = CX+R*NX, CORE+R*NR
BW, BF = RW+M*XW,14.514-A*X1


def wall(x): return B+K*x
def roof(x,t): return max(BW-M*x, BF+A*x, 11.33+SIDE*abs(t))
def window_xz_curve(x,t): return sqrt(wall(x)**2-t*t)


def hertz(load,rx,ry,E=110000.):
    """Normalized elliptic Hertz curvature integrals, Simpson + bisection."""
    def integrals(k):
        X=Y=0.; n=192
        for i in range(n+1):
            c=cos(i*pi/(2*n))**2; d=1+(k*k-1)*c
            v=(1 if i in (0,n) else 4 if i%2 else 2)*2*c/sqrt(d)
            X+=v; Y+=v/d
        return X*pi/(6*n),Y*pi/(6*n)
    lo,hi=1.,128.
    for _ in range(52):
        k=(lo+hi)/2; X,Y=integrals(k)
        if X/Y>ry/rx: hi=k
        else: lo=k
    a=(3*load*rx*X/(2*pi*E))**(1/3); b=k*a
    return dict(N=load,half_axes=[a,b],peak_GPa=3*load/(2*pi*a*b*1000))


def seg_distance(p,a,b):
    u,v=b[0]-a[0],b[1]-a[1]
    t=max(0.,min(1.,((p[0]-a[0])*u+(p[1]-a[1])*v)/(u*u+v*v)))
    return hypot(p[0]-a[0]-t*u,p[1]-a[1]-t*v)


def study():
    # Radius on every convex roof junction: expanded intersection of inset
    # planes, then crop by the four vertical port limits, and the solid rear.
    xt=(BW-BF)/(M+A); rt=roof(xt,0)
    xc=(BW+FIL*hypot(1,M)-BF-FIL*hypot(1,A))/(M+A)
    rc=BW+FIL*hypot(1,M)-M*xc
    flat=(xc-FIL*NX-XW)/NR
    assert X0<XW<xc-FIL*NX<X1 and rt<rc-FIL
    assert 11.33+FIL*hypot(1,SIDE) < RW+FIL*NR
    lowest=rc-FIL
    # Unblended roof is a lower bound on real surface; these are global across
    # whole footprint, since roof increases with |t| and cone decreases.
    park=S+rt-wall(xt)
    assert park>.22 and rt>12.63
    # Contiguous, occupied cheek sample at q+CHEEK along each cut's outward
    # normal, retained even with .04 fillet on the fixed aperture and lip.
    walls=[roof(X0,0)-wall(X0-CHEEK),roof(X1,0)-wall(X1+CHEEK),
           11.33+SIDE*W-window_xz_curve(X1,W+CHEEK)]
    assert CHEEK-GAP>ROUND and min(walls)>ROUND*hypot(1,K)
    assert X1+CHEEK+ROUND<0 and REAR+S+ROUND<18.15
    # No wrong-sign roof facet normal near a trimmed end; blend is local.
    assert BW-M*(X1-2*FIL)<BF+A*(X1-2*FIL)
    assert BW-M*(X0+2*FIL)>BF+A*(X0+2*FIL)
    eps=2*CHEEK/(2*R)
    nd=(-A*eps+sqrt(1+A*A-eps*eps))/(1+A*A)
    work=nd-MU*sqrt(1-nd*nd)
    assert abs(hypot(nd,A*nd+eps)-1)<1e-12 and work>0
    # 2 transverse bearing resultants on central shaft; separated roll-key
    # reaction, drive side loads/eccentricity, and moment of guide drag.
    span=5.; front=18.6; ecc=hypot((X1-X0)/2,W); h=front-rt
    force=hypot(1,MU); key=2.5; drag_arm=3.; screw_offset=.12; torsion=.40
    coeff=force*(1+2*ecc/key+2*(h+ecc)/span)
    drive=2*torsion/key+2*screw_offset/span
    cd=2*drag_arm/span; ug=.015
    limit=work/(coeff+cd*work)
    def budget(u):
        den=1-u*cd
        return dict(contact_help=work-u*coeff/den,
                    drive_help=1-u*drive/den,drag0_multiplier=1/den,
                    guide_Q_per_N_at_D0_P_zero=coeff/den)
    assert budget(ug)['contact_help']>.05 and budget(.05)['contact_help']<0
    # Actual last jaw on a convex cylindrical crest (not point load at the
    # nominal work plane); the same three jaws can open by the same s.
    samples=[]
    for ax in (.25,.10,.03,.01,0.,-.25,-.5):
        rd=sqrt(1-ax*ax); stroke=.40
        gx=xc-(R+FIL)*ax; gr=rc+stroke-(R+FIL)*rd; dr=gr-CORE
        assert -A/hypot(1,A)<=ax<=NX
        other=1.5*dr*rd
        wc=(wall(gx)-gr)/hypot(1,K)-R
        # Disk core at x=gx, shifted by dr, offset by R globally. Backing
        # buttons offset from core by -1.36, at R8.40 add the same R gauge.
        button_wc=(wall(gx-1.36)-(8.4+dr))/hypot(1,K)-R
        tip=-6.446+1.48
        butt_clear=(gx-1.36-tip+2.18-dr)/sqrt(2)-R
        assert wc>.05 and other>0 and button_wc>0 and butt_clear>0
        assert gx-R>tip and gx-1.36-R>-6.446 and 8.4+dr+R<rt
        samples.append(dict(nx=ax,nd=rd,core_center_x=gx,radial_offset=dr,
            guard_clear=wc,other_two_support_plane_clear=other,
            button_to_seat_clear_lower=butt_clear,
            frictionless_normal_per_axial=(1/ax if ax>0 else None)))
    # The fixed FRONT portal edge is a real .04 cylinder-local meridian
    # round on the cone/cut, not a face normal chosen from a singular corner.
    xp=X1+GAP; bx=xp+ROUND; br=wall(bx)+ROUND*hypot(1,K)
    nx=.12; nr=sqrt(1-nx*nx)
    p=(bx-(R+ROUND)*nx,br-(R+ROUND)*nr)
    v=[(X0,roof(X0,0)+S),(xt,rt+S),(X1,roof(X1,0)+S)]
    dist=min(seg_distance(p,l,r) for l,r in zip(v,v[1:]))-R
    back=seg_distance(p,(-6.7,wall(-6.7)),(X0-GAP,wall(X0-GAP)))-R
    assert dist>0 and back>0 and W+GAP>R and nx>0
    Q=(bx-ROUND*nx,br-ROUND*nr)
    xstart=xc-(R+FIL)*NX; dstart=rc+.20-(R+FIL)*NR-CORE
    enddr=rc+.20-(R+FIL)*sqrt(1-.25**2)-CORE
    home_btn=(CX-1.36-(-6.446+1.48)+2.18)/sqrt(2)-R
    assert 0<dstart<xstart-CX and enddr>0 and home_btn>=0
    assert wall(xstart)-CORE-dstart>R*hypot(1,K)
    assert .25*1.5*samples[0]['radial_offset']>0
    # Disk at park physically intersects the specific lip-witness ball,
    # although it could not do so at home. No inference about other poses.
    assert p[1]<12.63 and abs(1.05-p[0])<R
    Fclosed=40/(NX-MU*NR)
    flat_stress=hertz(Fclosed,R,RW/NR)
    assert flat>flat_stress['half_axes'][0]
    # At body/cylinder crest Rx combines the two convex radii, Rt is
    # circumferential curvature of the outside flange, not ball/flat.
    n=.1; d=sqrt(1-n*n)
    crest=hertz(10/n,1/(1/R+1/FIL),(CORE+R*d)/d)
    requested=.72
    min_slope=(wall(0)-(CORE+R*sqrt(1-requested**2)))/(-(CX+R*requested))
    return dict(label='exploratory',units='mm,N,N mm',work_plane=dict(
        x=XW,r=RW,nx=NX,nd=NR,flat_edge_distance=flat),
        section=dict(CX=CX,core=CORE,R=R,lip_radius=B,taper=K,
            jaws_at_deg=[-90,30,150],x=[X0,X1],t_half=W,work_r_intercept=BW,
            front_r_intercept=BF,side_r_intercept=11.33,
            slopes=[-M,A,SIDE],roof_core_offsets=[FIL*hypot(1,k) for k in (M,A,SIDE)],
            roof_blend=FIL,s_range=[0,S],rear_home=REAR,gap=GAP,
            min_roof_lowerbound=rt,true_ridge_center=[xc,rc],true_rmin=lowest,
            home_disk_radial_clear=rt-12.63,park_radial_recess_min_lower=park,
            downstream_recess_center=roof(X1,0)+S-wall(X1),
            guard_face_radial_depth=walls),
        loads=dict(min_any_contact_nd=nd,contact_work=work,guide_coeff=coeff,
            drive_coeff=drive,drag_feedback=cd,guide_mu_limit=limit,
            target_guide_budget=budget(ug),dry_example_budget=budget(.23),
            one_lip_clean_40N=flat_stress,flat_patch_nominal_reserve=flat-flat_stress['half_axes'][0],
            first_flat_patch_cutoff_radial_s=(flat-flat_stress['half_axes'][0])*NR*M,
            illustrative_10N_axial_on_nx_point1_crest=crest,
            slope_min_for_qx_point72=min_slope),
        last_one_jaw_on_rounded_crest=samples,
        parked_local_ball=dict(center=p,pole=Q,normal_head_on_tail_x=-nx,
            unrounded_shoe_clear_lower=dist,other_axial_edge_clear_lower=back,
            disk_first_intersection_at_face_x=p[0]-R,
            scope='one R2.5 generator, NOT the whole flange in this pose'))


if __name__=='__main__':
    out=study()
    print(json.dumps(out,indent=2 if '--json' in sys.argv else 1,sort_keys=True))
