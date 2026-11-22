"""Take 69 analytic pose cover. Length mm, force N, torque Nmm. Nominal."""
from math import *
from stock import B,K,C,W,RO,R,v,h,b,beta,w,rot,CORE_DISKS
import json
MU=.23;KAP=hypot(1,MU);LAM=1.10;G=10.95;SLX=-.54;LINK=4.66
def vecdot(a,b):return sum(x*y for x,y in zip(a,b))
def core(axes):
    # For any d return exact min/max d·generator relative to body core center.
    ax,ar,at=axes;sz=hypot(ar,at)
    rows=[((x-C)*ax,rr*sz) for x,rr in CORE_DISKS]
    rows += [(6.75*(ar*cos(k)+at*sin(k)),4*sz) for k in [0,2*pi/3,-2*pi/3]]
    rows += [((x-C)*ax+rr*(ar*cos(k)+at*sin(k)),0.) for k in [pi/3,pi,5*pi/3]
             for x,rr in [(-4.31,10.30),(C,10.30),(0,5)]]
    return min(c-r for c,r in rows),max(c+r for c,r in rows)
def upper():
    # Any exposed pillar or leaf upper face/edge above roof+.94 is
    # contained in this 4D volume; normals need NOT follow that surface.
    roots=[(.65,-h),(0,W),(.94,3.98),(0,beta)]
    stack=[roots];minw=1e9;boxes=0
    while stack:
        box=stack.pop();mid=[(a+b)/2 for a,b in box];de=[(b-a)/2 for a,b in box]
        u,t,hh,th=mid;du,dt,dh,dth=de
        z=w(h+u,t)-v+hh;dz=.44*du+.25*dt+dh
        c,s=cos(th),sin(th);y=v-u*s+z*c;rr=hypot(y,t)
        eq=hypot(du,dz)+hypot(u,z)*dth; dr=hypot(eq,dt)
        rlo=rr-dr
        if rlo>G+R+1e-8:continue
        m=max(-1.,(rlo-G)/R)
        V=(-z-LAM*c,u-LAM*s);speed=hypot(*V)
        # radial unit in PARK chart; each direction in the box differs from
        # midpoint by <= dtheta + 2 dr/(r-dr). Tail normal on metal must
        # have radial projection >= (r-G)/R. Allow full 3D Coulomb cone.
        a=(-s*V[0]+c*V[1])*y/rr;tn=sqrt(max(0.,speed**2-a*a))
        if a< -m*speed:lowest=-speed
        else:lowest=a*m-tn*sqrt(max(0.,1-m*m))
        dvel=hypot(du,dz)+LAM*dth
        lower=lowest-speed*(dth+2*dr/rlo)-dvel-MU*(speed+dvel)-1e-7
        boxes+=1
        if lower>.36:minw=min(minw,lower);continue
        i=max(range(4),key=lambda j:de[j]*[1,.55,1,2.8][j])
        assert de[i]>1e-5 and boxes<1000000
        for half in [(box[i][0],mid[i]),(mid[i],box[i][1])]:
            stack.append(box[:i]+[half]+box[i+1:])
    return dict(tested_boxes=boxes,upper_work=minw)
def device(th):
    px,rp,_=rot(1.03,2.70,0,th);ex=(SLX-px)/LINK;ey=sqrt(1-ex*ex)
    rd=rp+LINK*ey
    a=-(rp-v)*ex+(px-h)*ey
    psidot=-(rp-v)/(LINK*ey)
    slide=a/ey
    return px,rp,rd,ex,ey,a,psidot,slide
def hardware():
    # Analytic swept lower radius to external moving parts. Pillars connected
    # below .94 to solid leaf with no side exposure there. Other solids have
    # minimum r >= this bound ignoring blade azimuth wherever conservative.
    def ry(u,z):
        return min(v+z,v-u*sin(beta)+z*cos(beta)) if z>=0 and u>=0 else 0
    P=ry(1.03,2.70);Dmin=P+sqrt(LINK**2-max(abs(device(t)[0]-SLX) for t in [0,beta])**2)
    def slab(u,z,rad,t):return hypot(ry(u,z)-rad,t)
    radial=dict(boss=slab(1.03,2.70,.88,1.70),pin=P-.60,
       rigid_clevis=hypot(min(Dmin,P)-.91,.78),slider=min(Dmin-.85,Dmin-2.65),
       rib=min(slab(.10,2.70,.45,2.78),slab(1.44,1.85,.45,2.78)),
       crossbar=slab(.10,2.70,.45,3.03),ear=hypot(min(v,ry(.10,2.70))-.55,4.58),
       trunnion=hypot(v-.90,5.55),stub=hypot(v-.52,4.9),
       lever=hypot(v-.46,6.68),block=hypot(v+3,6.60),fixed_window_start=b(h-1.18),
       vertical_trim=v-.65*sin(beta)+sqrt(RO**2-.65**2)*cos(beta))
    assert all(x>G+R for x in radial.values())
    # u=.65 and rho>=RO selects positive-z only as the roof above
    # minimum w(h+.65,W)>v-sqrt(...). Covers lower cut and its edges.
    assert w(h+.65,W)>v-sqrt(RO**2-.65**2)
    return radial
def bridge():
    # Fixed structural guard trial: full toroidal lip, smooth, ahead of drive.
    # Disprove clearance by a WHOLE centered flange translated only in X/Y
    # while jaws parked. A tilted/moving-tail universal solution is not needed
    # to find a bad fixed contact. Inner-aft quadrant, integer slopes chosen.
    xg,rg,rgauge=2.76,15.30,.80
    # local 2D (axial,radial), from ring center toward core.
    nx,ny=-.35,-sqrt(1-.35**2)
    cx,cy=xg+(R+rgauge)*nx,rg+(R+rgauge)*ny
    off=cy-10.75
    # For the full convex hull against torus at this axial position:
    # each generator disk is inside the radius 10.75+off circular cylinder
    # but positive axial generators may be further forward! Use inner-cone
    # tangent support around the FULL azimuth: at each x nonpenetration
    # follows from axial/radial signed distance to this supporting cone.
    # Tail occupies lumen below the line tangent at its chosen lobe.
    k=-nx/ny
    coremargin=min(rg+rgauge*ny-cy + k*((cx+(xx-C))-(xg+rgauge*nx))
            -((off+rr)-cy)-R*hypot(1,k) for xx,rr in CORE_DISKS)
    # Seat of lobe is axis aligned. Support on the other button stations and
    # lobes uses exact radial offset, not a central R10.75 circular core.
    margins=[]
    for xx,rr,k0,cr in [(C,6.75,ki,4.) for ki in (0,2*pi/3,-2*pi/3)]+[
        (xx,rr,ki,0.) for ki in (pi/3,pi,5*pi/3) for xx,rr in [(-4.31,10.30),(C,10.30),(0,5.)]]:
        radius=hypot(off+rr*cos(k0),rr*sin(k0))+cr
        margins.append(rg+rgauge*ny + k*(cx+xx-C-xg-rgauge*nx)-radius-R*hypot(1,k))
    # Some forward sections may cross infinite tangent cone far forward;
    # report rather than infer guard clearance if that bound fails.
    spans=[(xx,rr) for xx,rr in CORE_DISKS]
    # Bore & disk checks use each core's axial station and full-cone signed
    # distance. For the front flank, no guard supports credited in the slit.
    fd=lambda x,r:(B+.41*x-r)/hypot(1,.41)-R
    bore=min([fd(cx+x-C,off+r) for x,r in spans]+[fd(cx,cy)]+[
        fd(cx+x-C,hypot(off+r*cos(k0),r*sin(k0))) for k0 in (pi/3,pi,5*pi/3)
        for x,r in [(-4.31,10.3),(C,10.30),(0,5)]])
    assert abs(margins[0])<1e-10 and min(margins[1:])>0 and coremargin>0
    assert bore>0
    # Home disk remains behind x=-5 during jaw opening, but advancing disk
    # at +1.35 may contact tail. That is precisely the case in which guard
    # is an adverse stop, not a guarantee of axial release.
    assert max(hypot(off+8.32,0),off+6.9)<rg-rgauge
    return dict(guard=[xg,rg,rgauge],core_center=[cx,off,0],lobe_generator=[cx,cy,0],
        guard_normal_on_tail=[nx,ny],fixed_axial_worst=nx-MU*abs(ny),
        core_to_tangent_min=coremargin,button_lobe_to_tangent=margins,
        flange_bore_gap=bore,max_forward_pin=device(beta)[0]+.91,
        guard_back=xg-rgauge,guard_terminal_slab_deficit=xg+rgauge-1.35)
def front():
    # Nominal x limits from all three forward installations: local clevis,
    # radial slides, journal and loaded rotating stock. All rear gear remains
    # behind x<=0. The ejector stays at home throughout this leaf stroke.
    projected=dict(leaf=h+hypot(-h,B+.95-v),
        pillar=h+hypot(1.74,2.85),clevis=max(SLX,device(beta)[0])+.91,
        rib=h+hypot(1.44,1.85)+.45,ear=h+hypot(.10,2.7)+.55,
        lever=h+3.8*sin(beta)+.46,slider=SLX+.91,wall=0.)
    xmax=max(projected.values())+1e-6;assert xmax<1.76
    nn=(2.80-1.76)/R;factor=nn-MU*sqrt(1-nn**2)
    speed=4.26
    L=KAP*speed/factor;assert L<22
    # A real contact on the available central CLEVIS, not the boss hidden
    # in Take67. Because it is frontmost in x, *one* separating plane
    # proves nonpenetration of every full neighbor/forward drive solid.
    th=.99*beta;px,rp,rd,ex,ey,a,omega,slide=device(th);qt=(px+.91,rp,1.10)
    ax=(cos(.48),sin(.48),0);ar=(-sin(.48),cos(.48),0)
    center=tuple(qt[i]+(R if i==0 else 0)-10.75*ar[i] for i in range(3))
    xmin=center[0]+core((ax[0],ar[0],0))[0]
    assert abs(xmin-qt[0]-R)<1e-8 and xmin>2.80
    assert qt[0]>max(projected[k] for k in projected if k!='clevis')
    # Forks remain inside their exact width and height stations; project an
    # enclosing circle only as a lower bound, not as bearing stock.
    fork=min(center[0]+(x-C)*ax[0]-hypot(hy,hz)*abs(ar[0])
             for x,hy,hz in [(4,3.3,5.08),(6.75,2.15,6.45),(11.46,1.45,6.66)])
    assert fork>1.76
    return dict(max_head_x=xmax,parts=projected,min_allowed_generator_x=2.80,
        axial_force_per_N=factor,normal_per_axial=1/factor,required_lambda=L,
        witness=dict(phase=th,contact=qt,core_center=center,tail_basis=[ax,ar,(0,0,1)],
                     minimum_core_x=xmin,minimum_fork_x=fork))
def torque():
    # Measured limits WOULD be needed; no μ change at the jaw/flange.
    mu=.020;slide_loss=.030;rho=3.49;s=5.55;vp=hypot(1.03,2.70)
    Cj=KAP*hypot(1,rho/s);j=mu*(.52*Cj+.90*KAP)
    eta=mu*(.60+.69)/LINK
    worst=kw=jw=poww=0.;amin=1e9;allow=1e9
    for i in range(1024):
        de=beta/2048;th=(i+.5)*2*de
        *_,ex,ey,a,omega,vel=device(th)
        # Bounds from |d(Vp)/dθ|=|Vp| and |de_link/dθ|<=|Vp|/(L ey).
        da=(vp+vp*vp/(LINK*.95))*de
        eylo=ey-vp/(LINK*.95)*de; ah=a+da;al=a-da
        bl=ah/eylo;om=(abs(omega)*LINK*ey+vp*de)/(LINK*eylo)
        arm=al*sqrt(1-eta**2)-eta*vp
        k=(KAP*rho+j)/(arm-mu*(.52+.60))
        base=j+mu*(.52+.60*(1+om)+.69*om)*k
        dl=base+slide_loss*bl*k
        worst=max(worst,dl);kw=max(kw,k);jw=max(jw,Cj+k)
        poww=max(poww,base);amin=min(amin,arm);allow=min(allow,(.36-base)/(bl*k))
    assert worst<.36 and kw<5 and amin>.75
    return dict(trial_pin_mu=mu,trial_guide_drag_per_link=slide_loss,
      min_actual_rod_arm=amin,rod_load_per_N=kw,journal_pair_per_N=jw,
      max_one_sided_pin_work=poww,max_total_loss=worst,net_credit=.36-worst,
      max_guide_ratio_for_nonnegative_net=allow)
def captured():
    # Actual 3 jaws, 6 side faces. Fixed/preloaded annular seat facings as
    # Q68 geometry only, not claiming 67 installed saddle compliance.
    n=.60;d=.80;fc=cos(radians(56));fs=sin(radians(56))
    sj=n/(2*fc);W=[0.]*6;tau=0.
    for k in [0,2*pi/3,-2*pi/3]:
        y,z=cos(k),sin(k);rs=R*fs
        jaw=(-n,-d*y,-d*z);point=(C+R*n,(10.75+R*d)*y,(10.75+R*d)*z)
        row=[(jaw,point)]
        for sg in [-1,1]:
            q=(fc,sg*fs*(-z),sg*fs*y)
            b0=(-4.31,10.30*(-z*sin(pi/3)+y*cos(pi/3)),
                10.30*(z*cos(pi/3)+y*sin(pi/3)))
            # Seat tangents rotate together with their own button stations.
            ay,az=b0[1]/10.3,b0[2]/10.3;q=(fc,-sg*fs*az,sg*fs*ay)
            row.append((tuple(sj*qq for qq in q),tuple(b0[i]-R*q[i] for i in range(3))))
        for (fx,fy,fz),(x,y0,z0) in row:
            for j,a0 in enumerate([fx,fy,fz,y0*fz-z0*fy,z0*fx-x*fz,x*fy-y0*fx]):W[j]+=a0
        tau+=-(point[1]*y+point[2]*z-v)*n+(point[0]-h)*d
    assert max(map(abs,W))<1e-12 and tau>0
    return dict(jaw_normal_each=1.,seat_normal_each=sj,residual_wrench=W,
                three_jaw_opening_assist=tau)
def coexist():
    # Exact generator diameter: each disk's farthest transverse points
    # can oppose its counterpart along their center difference. Convex
    # hulling does not enlarge the diameter. Capsule endpoints suffice.
    rows=[(x,0.,0.,r) for x,r in CORE_DISKS]
    rows += [(C,6.75*cos(k),6.75*sin(k),4.) for k in (0,2*pi/3,-2*pi/3)]
    rows += [(x,r*cos(k),r*sin(k),0.) for k in (pi/3,pi,5*pi/3)
             for x,r in [(-4.31,10.3),(C,10.30),(0.,5.)]]
    diameter=max(hypot(x-X,hypot(y-Y,z-Z)+r+rr) for x,y,z,r in rows for X,Y,Z,rr in rows)
    # Independent of pose: centers implied by the REAL normal at a
    # particular work pole and earlier .99β adverse boss contact.
    th=.99*beta; px,rp,*_=device(th);n=sin(th-atan(K));d=cos(th-atan(K))
    fx,fy,_=rot(0,B+K*h-v,0,th)
    x1=fx+(-R-d*(10.75-fy))/n
    x2,y2,t=px+(.88+R)*.80,rp+(.88+R)*.60,1.8
    gaps=[hypot(x2-x1,y2*cos(k)-t*sin(k)-10.75,y2*sin(k)+t*cos(k))-diameter
          for k in (-2*pi/3,2*pi/3)]
    projected=n*(x2-x1)+d*(y2-10.75)
    # Every button core point is within this of a convex K generator:
    # project to the centered 7.60 disk at x=C for the first two
    # endpoints, and to x=.20's disk for x=0,r5.0. Convexity extends it.
    dh=hypot(4.31+C,10.30-7.60)
    assert min(gaps)>0 and projected>dh
    return dict(max_generator_diameter=diameter,other_jaw_excess=gaps,
                same_jaw_outside_work_support=projected,max_button_core_excess=dh)
def saddle_cell():
    # A nonempty middle cell; same-leaf twist + 1 mm/rad radial retreat.
    # All head/neighbor phase displacements and tail rigid displacements
    # below are paid as Hausdorff bounds, not an interpolation claim.
    th=.35*beta;phase=.010;eps=.080
    n,d=sin(th-atan(K)),cos(th-atan(K));p=-.40;c,s=cos(th),sin(th)
    q=rot(p-h,w(p,0)-v,0,th);cx=q[0]-R*n;off=q[1]-R*d-10.75
    assert hypot(p-h,w(p,0)-v)>RO and p<=0 and off>.20 and cx-2.06<2.80
    def coef(x,y,t):
        a=x-h;z=y-v;pc=h+a*c-z*s;yc=v+a*s+z*c
        return (B+K*pc-hypot(yc,t))/hypot(1,K)-R
    ax=cx-h;ay=off+10.75-v;pc=h+ax*c-ay*s;yc=v+ax*s+ay*c
    J=B+K*pc-R*hypot(1,K)
    assert abs(J-yc)<1e-12 and J*K*s+yc*c-4>0
    g=1e3;fixed=1e3
    rows=[(xx,off,0,rr) for xx,rr in CORE_DISKS]+[(C,off+6.75*cos(k),6.75*sin(k),4.)
         for k in [2*pi/3,-2*pi/3]]+[(x,off+r*cos(k),r*sin(k),0) for k in [pi/3,pi,5*pi/3]
         for x,r in [(-4.31,10.30),(C,10.30),(0,5.)]]
    for xx,y,t,rr in rows:
        x=cx+xx-C
        g=min(g,min(coef(x,y+rr*cos(i*pi/128),t+rr*sin(i*pi/128)) for i in range(256))-rr*pi/256)
        fixed=min(fixed,(B+K*x-hypot(y,t)-rr)/hypot(1,K)-R)
    fixed=min(fixed,(B+K*cx-(10.75+off))/hypot(1,K)-R)
    sep=[]
    for k in (2*pi/3,-2*pi/3):
        plane=vecdot((n,d,0),rot(0,B+K*h-v,0,th))-.40/hypot(1,K)
        sep.append(plane-(cx*n+off*d*cos(k)+core((n,d*cos(k),d*sin(k)))[1]+R))
    assert B+K*(h+.65)-w(h+.65,W)<.40 and min(sep)-4.26*phase>eps and fixed>eps and g>0
    # All parked rear extras or all other degree-of-freedom parts outside
    # a centered cylinder. No missed P-D connector or forward bearing.
    P=device(th)[1];end_r=min(P-.91,hypot(v-.90,5.55),
        hypot(v-.52,4.9),
        hypot(min(v,rot(.10,2.70,0,th)[1])-.55,4.58),
        min(rot(1.44,1.85,0,th)[1],rot(.10,2.70,0,th)[1])-.45,
        hypot(v-.46,6.68),device(th)[2]-2.65)
    assert end_r-4.26*phase>10.75+off+R+eps
    assert cx-2.06-R-(-5.)>eps
    # The old axis-aligned fork's first knot is x=4. Radial limit only used
    # for the ball-backed compound; no curvature assumption on the forks.
    assert cx+4-C-1.76>eps
    # Minimum y of actual potentially contacted leaf stock; its root/roof
    # by interval bounds, all outer hardware proved excluded above.
    ymin=v-(-h)*sin(th+phase)+min(0,w(h+.65,W)-v)
    gamma=(ymin-(off+10.75+eps))/R;work=gamma-MU*sqrt(1-gamma**2)
    assert work>.36
    return dict(phase=th,phase_radius=phase,hausdorff=eps,center=[cx,off,0],
        contact=q,other_leaf_separation=min(sep)-4.26*phase-eps,
        fixed_wall_separation=fixed-eps,disk_separation=cx-2.06-R+5-eps,
        noncorotating_stock_radial_separation=end_r-4.26*phase-10.75-off-R-eps,
        positive_radial_work=work,normal_per_radial_external=1/work)
if __name__=='__main__':
    print(json.dumps(dict(label='exploratory',near=upper(),hardware=hardware(),guard=bridge(),
                          forward=front(),one_sided_drive=torque(),seated=captured(),
                          coexistence=coexist(),middle=saddle_cell()),indent=2))
