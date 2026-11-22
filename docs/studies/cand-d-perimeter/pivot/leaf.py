"""Take 61; exploratory, mm and N. Run: python3 leaf.py > result.json"""
from math import sqrt,hypot,cos,sin,atan,asin,pi,degrees
import json

B,K,A,R,C,MU=14.5,.28,10.75,2.5,-2.25,.23
M=hypot(1,K)
W,WC,A0,A1,BACK=3.20,3.26,1.10,1.16,.95

def wall(p,t):
    return sqrt((B+K*p)**2-t*t)

def hertz(N,rx,rt):
    # Elliptical nonconforming half-spaces; no pressure claim at clipped edges.
    def I(k):
        x=y=0.
        for j in range(1537):
            c=cos(j*pi/3072)**2; d=1+(k*k-1)*c
            w=(1 if j in (0,1536) else 4 if j%2 else 2)*2*c/sqrt(d)
            x+=w;y+=w/d
        return pi*x/9216,pi*y/9216
    lo,hi=1.,256.
    for _ in range(54):
        k=.5*(lo+hi); x,y=I(k)
        if x/y>rt/rx: hi=k
        else: lo=k
    a=(3*N*rx*x/(2*pi*110000))**(1/3);b=k*a
    return [a,b,.001*3*N/(2*pi*a*b)]

def leaf(n):
    d=sqrt(1-n*n); beta=asin(n)+atan(K)
    xp=C+R*n; yp=A+R*d; h=(yp+xp*n/d-B)/(K+n/d); v=B+K*h
    length=-h*M; arm=(xp-h)/d; pp=h+arm/M
    def xf(p,y,t,ang=beta):
        a,b=p-h,y-v
        return h+a*cos(ang)+b*sin(ang),v-a*sin(ang)+b*cos(ang),t
    def gap(p,t):
        x,y,t=xf(p,wall(p,t),t)
        return hypot(x-C,max(0,hypot(y,t)-A))-R
    def coeff(ang):
        c,s=cos(ang),sin(ang);a,b=C-h,A-v
        pc,yc=h+a*c-b*s,v+a*s+b*c
        j=B+K*pc-M*R
        return [j-yc,j*K*s+yc*c-A]
    cur=d/yp-1/(M*(B+K*pp))
    out=dict(qx=n,qr=d,H=[h,v],pole=[xp,yp],park_pole_p=pp,
             beta_deg=degrees(beta),pole_arm=arm,toe_reserve=length-arm,
             transverse_relative_curvature=cur,lock_coeff=coeff(beta))
    # Concrete, strictly interior points of machined stock, not a min over a mesh.
    if n in (.55,.60,.72):
        p,t={.55:(-.38,3.08),.60:(-.18,3.08),.72:(-.02,2.76)}[n]
        e=.0005
        x,y,t=xf(p,wall(p,t)+e,t)
        pen=R-hypot(x-C,hypot(y,t)-A)
        assert p>h+.65 and hypot(p-h,wall(p,t)-v)>A1 and min(p-h,-p,W-t)>e
        assert pen>e and cur<0
        out['interior_overlap']={'park':[p,wall(p,t)+e,t],'locked':[x,y,t],
                                 'depth_in_flange':pen,'added_leaf_depth':e}
    if n>.5: return out
    assert cur>0 and abs(coeff(beta)[0])<1e-12 and coeff(beta)[1]>0
    # For all intermediate angles, g=j-yc>0 by concavity (positive sin/cos
    # combination or min at endpoints). Bound f=j*K*sin + yc*cos - A:
    # |f''| <= 2K(|a|+|b|)(1+K)+K(B+K*h-MR)
    #              +4(|a|+|b|)+v, or simply 80 for both datums.
    # Between two nodes the secant error <=80*step^2/8. At zero f=0,
    # so use f'(0)>0 and the same second-derivative bound on first interval.
    a,b=C-h,A-v
    secmax=K*abs(v-M*R)+2*K*(1+K)*(abs(a)+abs(b))+v+4*(abs(a)+abs(b))
    assert secmax<80
    step=beta/64; vals=[coeff(i*step)[1] for i in range(65)]
    assert min(vals[1:])>80*step**2/8 and K*(B+K*C-M*R)+a>80*step
    assert K*a-b>0 and -a-K*b>=0 and min(coeff(0)[0],coeff(beta)[0])>=-1e-12
    # Aligned pressure only, no unseen support or load-sharing credits.
    N=40/(n-MU*d);half=hertz(N,R,1/cur)
    out.update(one_work_40N=N,hertz_half_mm_peak_GPa=half,
        holding_moment_Nmm=N*arm, rear_flat_reserve=arm-A1,
        toe_x_y_locked=xf(0,B,0)[:2],phase_coeff2nd_abs_bound=secmax)
    # Whole backing (including midwidth) clears aligned socket/housing: the
    # lowest y is at the deepest stroke or at park for p near H. Use the
    # common conservative lower bound at *every* p and angle.
    ylo=v-(-h)*sin(beta)-.40
    out['aligned_socket_radial_clear_lower']=ylo-10.08
    assert ylo>10.08
    # Minimum cylindrical radius of the parked-to-locked leaf: for each t
    # the lower skin's y decreases with angle if its current x>h. At lock
    # it decreases with p. At the toe, r^2-y0^2=delta*(2*(B-c*y0)-s^2*delta)
    # for delta=B-sqrt(B²-t²), so its radial minimum is at midwidth.
    c,s=cos(beta),sin(beta)
    assert .65*c-.40*s>0 and -s+c*K*14.50/wall(0,W)<0
    toe_r=xf(0,B,0)[1]
    assert 2*(B-c*toe_r)>s*s*(B-wall(0,W))
    xlo=h+.65*c-.40*s
    out.update(disk_R12p42_aligned_gap=toe_r-12.42,
        button_R2p5_aligned_gap=hypot(xlo+4.31,toe_r-10.30)-2.5)
    assert min(out['disk_R12p42_aligned_gap'],out['button_R2p5_aligned_gap'])>0
    # End hardware: tangent to the concave w(p,t) bounds it from ABOVE for
    # all p. Liners occupy only w..w+.20 (fixed housing beyond is relieved).
    # Rigid E has offset (1.35,2.70); the worst E height above the tangent
    # occurs at the locked angle (positive cos term, negative sin term).
    def liner(t,e,ear):
        wc=wall(h,t);k=K*v/wc
        ex,ey=1.35*c+2.70*s,-1.35*s+2.70*c
        z=ey-k*ex
        return v-wc+(min(0,z) if ear else z)-e*hypot(1,k)-.20
    gaps=[liner(3.26,.22,False),liner(4.58,.38,True),liner(5.28,.75,True)]
    assert min(gaps)>0
    # For the fixed annulus the tangent test needs only the center term.
    gaps[2]=v-wall(h,5.28)-.75*hypot(1,K*v/wall(h,5.28))-.20
    Le=hypot(1.35,2.70)
    half_shear=N*arm/(2*(Le+.22))  # equivalent shear resultant at maximum arm
    out.update(cheek_stock_clear=[*gaps], locked_toe_tip_min_radius=toe_r,
        crossbar_equivalent_shear_N=half_shear,
        crossbar_peak_transverse_shear_lower_MPa=half_shear/(pi*.22**2),
        crossbar_bending_screen_GPa=.001*(half_shear*(4.58-3.20)/2)/(pi*.22**3/4))
    # finite exposed forward toe: whole flange tilted 0.38 rad in radial
    # meridian of the pole so that only its extremal generator touches plane.
    # Construct at park, then rotate the ENTIRE neighbor and patch together
    # by -theta. This is a partial-pose witness, not commanded neighbor motion.
    t=3.10; y=wall(0,t)+.060; rr=hypot(y,t); ey,et=y/rr,t/rr; alpha=.38
    xc=R+A*sin(alpha);rc=rr-A*cos(alpha)
    theta=.012;c,s=cos(theta),sin(theta)
    vx,vy=cos(alpha)*c+sin(alpha)*ey*s, -cos(alpha)*s+sin(alpha)*ey*c
    cc=xf(xc,rc*ey,rc*et,theta); xlo=cc[0]-A*sqrt(1-vx*vx)-R
    assert xlo>0
    btn=[]
    for ph in [pi/3,pi,5*pi/3]:
        # radial meridian unit (-sin(alpha), cos(alpha)*ey, cos(alpha)*et);
        # tangent (0,-et,ey); axial station rotation 60° from loaded meridian.
        xb=xc-2.06*cos(alpha)-10.30*sin(alpha)*cos(ph)
        rb=rc-2.06*sin(alpha)+10.30*cos(alpha)*cos(ph)
        pb=xf(xb,rb*ey-10.30*sin(ph)*et,rb*et+10.30*sin(ph)*ey,theta)
        btn.append(pb[0]-R)
    # x supports of solid socket frusta / fork convex hulls after same rotation.
    xt=[cc[0]+(u-C)*vx-r*sqrt(1-vx*vx) for u,r in [(-.30,10.08),(2.25,9),(5.8,5.66)]]
    xfork=[cc[0]+(u-C)*vx-hypot(hy,hz)*sqrt(1-vx*vx)
           for u,hy,hz in [(4,3.3,5.08),(6.75,2.15,6.45),(11.46,1.45,6.66)]]
    # Other two toes, heads, and button clearance: at another station every
    # inside leaf point has outer-station radius y>=ylo, |t|<=W.
    # Its projection onto THIS radial meridian is <= cos(120°-offset)*ylo+
    # sin(...)*W. Use a weakened angle bound for both; whole tilted neighbor
    # can extend that far laterally, so separate using its back tangent plane.
    # Unit face direction v, all core+r ball stock has v·(q-cc)>=-R.
    # For the other leaves bound meridian projection with tilt correction
    # via v_yz projected onto each station.
    vt=sin(alpha)*et
    # x = h+(p-h)cosθ+(y-v)sinθ; p<=0
    vx0=h*(1-c)+(B+BACK-v)*s
    other=[]
    for ph in [2*pi/3,-2*pi/3]:
        vr=vy*cos(ph)+vt*sin(ph); vv=-vy*sin(ph)+vt*cos(ph)
        assert vr<0
        other.append(cc[0]*vx+cc[1]*vy+cc[2]*vt-R-(vx*vx0+vr*ylo+abs(vv)*W))
    assert min(other)>0 and min(btn)>0 and min(xt+xfork)>0
    work=(y-v)-MU*(-h)
    assert work<0
    out['partial_toe']={'angle_from_park_rad':theta,'point_park':[0,y,t],
       'point_actual':xf(0,y,t,theta),'core_center':cc,'tail_axis':[vx,vy,vt],
       'whole_flange_min_x':xlo,'buttons_min_x':min(btn),'socket_min_x':min(xt),
       'forks_min_x':min(xfork),'other_leaf_plane_gap':min(other),
       'opening_moment_per_N':work}
    # Contact force on leaf (-1,-mu,0) in the PARK chart. Rotate it at pose.
    fx,fy,_=xf(h-1,v-MU,0,theta); f=(fx-h,fy-v,0)
    pt=out['partial_toe']['point_actual']; q=[pt[i]-cc[i] for i in range(3)]
    tau=[-q[2]*f[1],q[2]*f[0],q[0]*f[1]-q[1]*f[0]]
    out['partial_toe']['external_wrench_about_core_per_N']=[*f,*tau]
    return out

def parked():
    # Bounds on the *physical* concentric and tangential running cuts.
    slope=(sqrt(A0*A0-.40**2)-.40*.30)/A1
    assert slope>.77
    dx=(A1-A0)/(2*slope)
    # If |t| in side cut, keep x and move <=.06 in t to real cheek.
    # Else move <=dx in x at fixed t to a covered coaxial cutoff.
    da=(WC-W)/sqrt((13.60)**2-WC**2)
    # r_c, r_s are <=14.51 about openings for inner contacts (r_c<=r at projection).
    ht=14.51*da
    # dr*sinphi = change in t at fixed azimuth; converting to delta_phi
    # at fixed t along x costs < .005 mm arc displacement.
    hx=hypot(M*dx,.005)
    H=.070
    assert max(ht,hx)<H
    angle=atan(K)-asin(H/R)
    useful=sin(angle)-MU*cos(angle)
    return dict(back_dx=dx,side_tangent_distance=ht,back_tangent_distance=hx,
        cover_H=H,tail_nx_lower=sin(angle),useful_X_per_N=useful,
        normal_per_adverse_X=1/useful,max_extra_outward_normal_loss_mm=
        sqrt(R*R-H*H)-R*cos(atan(K)-atan(MU)))

if __name__=='__main__':
    rows=[leaf(n) for n in [.38/hypot(1,.38),.48,.55,.60,.72,.80]]
    p=parked()
    assert p['useful_X_per_N']>0
    print(json.dumps(dict(label='exploratory',parked=p,leaves=rows),indent=2,allow_nan=False))
