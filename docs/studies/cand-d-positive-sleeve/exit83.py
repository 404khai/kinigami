"""Exact 0-clock finite polygon distance and independent global clearance bounds."""
from geo83 import *
from retention83 import closure
from scipy.optimize import minimize_scalar
xb=-6.76066017177982;xc=-4.02
xv=np.array([xb,xb+.75,-4.61066017177982,.70])
v=np.c_[xv,np.array([4.6,4.6,3.2,3.2])]
def distance(a,d,r,side=0):
    # receiver ring tangent at fixed rim y=-6.32; permitted body shift 'side'.
    C=np.array([d+.7+(6.32+side)*tan(a),side])
    U=np.array([cos(a),-sin(a)]);V=np.array([sin(a),cos(a)])
    l=np.array([.7+(np.array([xc,r])-C)@U,(np.array([xc,r])-C)@V])
    test=[]
    for p,q in zip(v[:-1],v[1:]):
        s=q-p;t=np.clip((l-p)@s/(s@s),0,1);test.append(np.linalg.norm(l-(p+t*s)))
    # Closing vertical rear face covers the region below the rear corner.
    test.append(np.linalg.norm(l-np.array([xb,np.clip(l[1],-4.6,4.6)])))
    return min(test)-1.5
def cheek():
    # Rear rim of exact circle, |t|=2.90, striking the cheek's LOWER inner
    # corner. At the lowest slot point y=4.365 there is still solid below.
    d=1.75;R=4.6;t=2.90;Y0=sqrt(R**2-t**2);L=.7-xb
    a=brentq(lambda a:L*sin(a)+Y0*cos(a)-4.25,0,rad(6)); U=X*cos(a)-Y*sin(a)
    C=(.7+d+6.32*tan(a))*X;O=C-.7*U;qX=C[0]-L*cos(a)+Y0*sin(a)
    # At tail's rear sharp corner, mix the lateral cylinder normal with
    # -U to obtain a common YZ-plane normal of the stationary cheek.
    W0=np.zeros(6)
    def add(q,f):return np.r_[f,np.cross(q-O,f)]
    W0+=add((d+.7)*X-6.32*Y,1.8*U)
    for sign in [-1,1]:
        n=(Y0/cos(a))*Y+sign*t*Z;n/=np.linalg.norm(n)
        W0+=add(qX*X+4.25*Y+sign*t*Z,-.20*n)
    assert max(abs(W0)-np.r_[4*W,W,W,46*W,50.8*W,52.2])<0
    # Material ball at 6 degrees, not an acceptance tolerance. Rear crown
    # body interval [xb, xb+.75]; conservative distance to every bounding face.
    b=rad(6);x=-3.90;y=4.27;z=2.92;xx=.7+(x-(.7+d+6.32*tan(b)))*cos(b)-y*sin(b)
    yy=(x-(.7+d+6.32*tan(b)))*sin(b)+y*cos(b)
    return dict(angle=degrees(a),point=[qX,4.25,t],tail_body_x=xb,
        pilot_clearance=5.10-(4.60/cos(a)+(C[0]+2)*tan(a)),
        registry_front_gap=d+6.32*tan(a)-8.2*sin(a)-1.5,roller_gap=distance(a,d,6.98),
        blade_shadow=hypot(3.80-L*sin(a),3.48)-4.60,
        endwall_shadow=hypot(4.40-L*sin(a),3.90)-4.60,
        other_station_y_bound=-(4.25)/2+sqrt(3)*4.15/2,
        rod_bush_shadow=hypot(2.91-L*sin(a),5.82*sin(pi/3))-.68-4.60,
        external_service=(-W0).tolist(),ring_normal=1.8,each_cheek_normal=.2,
        local_common_ball=dict(center=[x,y,z],angle=6,radius=min(xx-xb,xb+.75-xx,4.60-hypot(yy,z),
                   x+4.90,-3.10-x,y-4.25,4.89-.525-y,z-2.90,3.28-z)))
def alternate():
    # Optional material removal only, not the strict-round frozen/84 park test.
    # Six planes in body coordinates at roller clocks +/-40. All x on pin,
    # constrained strict circle AND three original shoulder flats remain.
    c=cos(rad(40));s=sin(rad(40));a=(4.30-2.90*s)/c;d=.7-xb
    angle=brentq(lambda b:d*sin(b)+a*cos(b)-4.25,0,rad(15))
    u=max(closure(.020)['station_disp'][6:]); y=3.85+(u+.15)/sqrt(2)
    return dict(apothem=4.30,clock_offset_deg=40,at_t_ge_2p90_body_y_max=a,
        lower_cheek_0clock_clear_through_deg=degrees(angle),gap_at_8=4.25-(d*sin(rad(8))+a*cos(rad(8))),
        shoulder_footprint_box_plane_margin=4.30-(c*y+s*(1.50+u+.15)),
        axial_chamfer_only_deg=degrees(brentq(lambda b:(.7-(xb+.75))*sin(b)+sqrt(4.6**2-2.9**2)*cos(b)-4.25,0,.2)),
        note='0-clock rim-pivot geometry only, no cross-clock/global release claim')
def result():
    CL=closure(.02); b=rad(CL['angle']);t=CL['travel'];w=6.760661
    tube=4.6+t+w*sin(b); out={}
    for d in [1.20,1.50,1.75,1.90,2.20]:
        name=str(d);ang=np.linspace(0,rad(22),441);g=np.array([distance(a,d,6.98) for a in ang]);idx=np.where(g<0)[0]
        m=minimize_scalar(lambda a:distance(a,d,6.98),bounds=(0,rad(22)),method='bounded')
        out[name]=dict(first_contact=None if len(idx)==0 else degrees(brentq(lambda a:distance(a,d,6.98),ang[idx[0]-1],ang[idx[0]])),
            min_gap=m.fun,angle_at_min=degrees(m.x))
    # Lateral translation of parked tail (level) at d placing full crown over axle
    # would meet pin pilot/flange/lower cam; distinguish tested geometry from straight clearance.
    return dict(label='exploratory',nose_max=8.2,stroke_needed=(.7+w)*cos(b)+4.6*sin(b)-.1,
        park_if_supports_engaged_and_axis_within_2deg=5.48-geom()['hardened_sweep_proposal']['cheek_lane_drift']-1.50*sin(rad(2)),
        alternate_relief=alternate(),parked_cheek=cheek(),no_roller_if_boss_shift_0p17_deg=degrees(asin((5.48-4.60-.17)/(w+.7))),tube_radius=tube,roller_reserve=5.48-tube,pilot_reserve=5.10-tube,cheek_reserve=hypot(4.25,2.90)-tube,
        blade_reserve=hypot(3.80,3.48)-tube,boss_overlap=6.65*cos(b)-6.32-(t+.7*sin(b)),rock_probe=out,
        old_2p437_gap=distance(rad(2.437),1.75,6.98),old_2p818_gap=distance(rad(2.818),1.75,6.98))
if __name__=='__main__':print(json.dumps(result(),indent=2))
