"""Construct a 4-degree loaded rocking branch; verify finite stock along it."""
from rim import *
import numpy as np
TA=radians(4);Y=BR/2; steps=256
def sec(x,y,t,alpha,shift=0):
    a=x-BC;z=y-Y
    return (BC+shift+a*cos(alpha)-z*sin(alpha),Y+a*sin(alpha)+z*cos(alpha),t)
def circles():
    phi=np.arange(1024)*2*pi/1024;v=[]
    def disk(x,y,t,r):
        v.append(np.broadcast_arrays(x*np.ones_like(phi),y+r*np.cos(phi),t+r*np.sin(phi)) if r else
                 [np.array([xx]) for xx in (x,y,t)])
    for x,r in CORE:disk(x,0,0,r)
    for k in ANG:disk(C,6.75*cos(k),6.75*sin(k),4)
    for k in BUT:
        for x,r in [(BC,BR),(C,BR),(0,5.)]:disk(x,r*cos(k),r*sin(k),0)
    return [np.concatenate([z[i] for z in v]) for i in range(3)]
def cone(xx,yy,tt,th):
    u=xx-H;z=yy-HR;p=H+u*cos(th)-z*sin(th);y=HR+u*sin(th)+z*cos(th)
    return max(float(np.min((i+k*p-np.hypot(y,tt))/hypot(1,k)-R))
               for k,i in [(J,B+(K-J)*XB),(K,B)])
def sweep():
    xyz=circles();xx,yy,tt=xyz;az=7.60*pi/1024
    # Signed cone distance is 1-Lipschitz; one common cone per entire
    # solid and phase, both lie in the two-slope bore. Endpoint circle arcs
    # and angular phase are debited, extending by convexity to the 3D hull.
    g=min(cone(xx-.50,yy,tt,th) for th in np.linspace(0,BE,513))
    g-=az+28.*BE/1024
    # At full draw, the centered smooth lobe touches the lock face; its
    # own eroded-cone quadratic minimum is exactly on-axis. Other disks
    # have strictly positive centered lock margin.
    off=len(CORE)*1024;idx=np.r_[0:off,off+1024:len(xx)]
    m=cone(xx[idx],yy[idx],tt[idx],BE)-az
    ax,ay=C-H,10.75-HR
    pc=H+ax*cos(BE)-ay*sin(BE);yc=HR+ax*sin(BE)+ay*cos(BE)
    A0=B+K*pc-R*M
    assert abs(A0-yc)<1e-10 and A0*K*sin(BE)+yc*cos(BE)-4>0
    # Locked approach/return: both ends contained in the SAME front
    # eroded cone; convexity interpolates pure axial translations.
    def front(xx,yy,tt):
        p=H+(xx-H)*cos(BE)-(yy-HR)*sin(BE)
        y=HR+(xx-H)*sin(BE)+(yy-HR)*cos(BE)
        return float(np.min((B+K*p-np.hypot(y,tt))/M-R))
    assert front(xx[idx],yy[idx],tt[idx])-az>0 and front(xx-.50,yy,tt)-az>0
    # Before roll, first advance .50 to full-draw relative x in the PARKED
    # barrel. Monotone in +X. Over .90 more carrier travel rock around
    # the two button centers. Then pure translation out of the flared bore.
    gg=min(cone(*sec(*xyz,a,.9*a/TA),0) for a in np.linspace(0,TA,129))
    gg-=az+(.90+19*TA)/256
    rmax=.20+10.75;assert (C-BC)*sin(TA)+Y*(1-cos(TA))<.20 and 10.3+2.06*sin(TA)<10.75
    frk=min(xx0-.50-abs(xx0-BC)*(1-cos(TA))-(hypot(hy,hz)+Y)*sin(TA)
           for xx0,hy,hz in [(4,3.3,5.08),(6.75,2.15,6.45),(11.46,1.45,6.66)])
    assert min(g,gg,m,frk-1.76)>0
    return dict(home_jaw_opening_cone_clearance=g,other_closed_sections=m,
       rotating_parked_bore_clearance=gg,fork_min_x=frk,generator_radial_bound=rmax)
def point_segment(x,r,x0,r0,x1,r1):
    u=x1-x0;z=r1-r0
    s=np.clip(((x-x0)*u+(r-r0)*z)/(u*u+z*z),0,1)
    return np.hypot(x-x0-s*u,r-r0-s*z)
def boss(x,r,rad=8.40):
    h=1.60;re=rad-h/tan(pi/3)
    return np.minimum(point_segment(x,r,DECK+h,0,DECK+h,re),
                      point_segment(x,r,DECK+h,re,DECK,rad))-R
def trig_min(f):
    c=(f(0)+f(pi))/2;a=f(0)-c;b=f(pi/2)-c
    return min(f(t) for t in [0,TA]+[atan2(b,a)+pi+2*pi*j for j in (-1,0,1)
             if 0<=atan2(b,a)+pi+2*pi*j<=TA])
def face():
    # Relative to the moving disk, whole neighbor rocks only. Leading
    # four button poles stay on the same finite R2.50 spheres, 5th/6th
    # (third button) detach. Own drafted facets bounded by their exact
    # primary planes; do NOT project a distant capsule onto an infinite V.
    Vgap=100; rim=100; bg=100;other=100;dmin=100;hull=100
    def lineface(k,sg,x,r,th):
        X,y,t=sec(x,r*cos(k),r*sin(k),th)
        return (X-BC)*cv+sg*sv*(-y*sin(k)+t*cos(k))
    for k in BUT:
        for x,r in [(BC,BR),(C,BR),(0.,5.)]:
            for sg in (-1,1):Vgap=min(Vgap,trig_min(lambda th:lineface(k,sg,x,r,th)))
            dmin=min(dmin,trig_min(lambda th:sec(x,r*cos(k),r*sin(k),th)[0])-R-DECK)
            for j in BUT:
                if j==k:continue
                def rad(th):
                    _,y,t=sec(x,r*cos(k),r*sin(k),th);return -(y*cos(j)+t*sin(j))
                other=min(other,BR-1.35+trig_min(rad)-R)
        z=np.linspace(0,1,513)
        for xend,rend in [(C,BR),(0,5.)]:
            for th in np.linspace(0,TA,129):
                x,y,t=sec(BC+z*(xend-BC),(BR+z*(rend-BR))*cos(k),
                          (BR+z*(rend-BR))*sin(k),th)
                r=np.hypot(y,t)
                rim=min(rim,float(np.min(np.hypot(x-P1,np.maximum(RI-r,0.))-R)))
                bg=min(bg,float(np.min(boss(x,r))))
    for x,y,r in [(xx,0,rr) for xx,rr in CORE]+[(C,6.75*cos(k),4.) for k in ANG]:
        hull=min(hull,trig_min(lambda th:sec(x,y+r,0,th)[0])-R-(DECK+CAP))
    # Centerline length ≤6.84 mm, rotation radius about button line <17.
    debit=6.84/1024+17*TA/256
    assert min(hull,bg-debit,rim-debit,other,dmin)>0 and Vgap>-1e-11
    def cap_line(rad,sh,h):
        # Signed perpendicular distance to sloped generator segment.
        u,z=4.31,-5.30;L=hypot(u,z)
        q=(DECK+h,rad+sh-h/tan(pi/3))
        t=((q[0]-BC)*u+(q[1]-BR)*z)/(L*L)
        assert 0<t<1
        return ((BC-q[0])*(-z)+(BR-q[1])*u)/L-R
    return dict(inner_hull_to_highest_cap=hull,loaded_button_rim=rim-debit,capsule_to_boss=bg-debit,
       other_V_slabs=other,button_deck=dmin,own_V_min_gap=Vgap,
       boss_cap_capsule_centered=cap_line(8.40,0.,1.60),
       boss_cap_capsule_at_018=cap_line(8.40,.18,1.60),
       boss_cap_capsule_at_budget=cap_line(8.40,OFFSET,1.60),
       alternate_R795_at_budget=cap_line(7.95,OFFSET,1.60),
       terminal_trailing_ball=BC+PM-P1-R)
def detach():
    # Sufficient acceleration, not evidence a worm/cam delivered it. SI
    # units here only. The previous path ends STATIONARY at full 4° tilt.
    # Initial x separation of EVERY center from the foremost carrier point.
    n=(BC-(DECK+CAP))/R
    A=.6867;m=.070;I=1.0e-5;e=.010;arm=.035
    a=100.;t=.003
    da=A/m;aa=A*e/I;relative=.5*(a-da)*t*t
    angular=.5*aa*t*t
    gap=n*relative-arm*angular
    back=(.5*da*t*t+arm*angular)
    assert gap>0 and 1000*back<.70
    return dict(leading_x_factor=n,trial_mass_kg=m,min_inertia_kg_m2=I,
       external_lever_m=e,max_generator_arm_m=arm,load_N=A,
       sufficient_acceleration_m_s2=da+arm*aa/n,
       at_20N_m_s2=20*(1/m+arm*e/(I*n)),trial_acceleration_m_s2=a,
       pulse_seconds=t,retraction_mm=1000*.5*a*t*t,
       terminal_speed_mm_s=1000*a*t,guaranteed_material_gap_mm=1000*gap,
       stationary_hardware_gap_mm=.70-1000*back)
if __name__=='__main__':
    print(json.dumps(dict(label='exploratory',carrier=aperture(),draw=draw(),sweep=sweep(),
                     faces=face(),force=force(),conditional_clear=detach()),indent=2))
