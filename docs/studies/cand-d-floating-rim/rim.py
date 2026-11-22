"""Take 72 nominal floating-plate mechanics. x from head lip toward tail."""
from math import *
import json
B,K,J,XB=14.54,.41,.26,-1.55
RI,OD,RP=12.04,12.42,11.66
RG,R,C,A,BC,BR=2.45,2.50,-2.25,10.75,-4.31,10.30
OFFSET=.18*sqrt(2)+.025
MU=.23; V=radians(56); cv,sv=cos(V),sin(V);T=tan(V);TR=tan(radians(64))
P0,P1,PM,PH=-6.95,-6.45,1.43,1.73
DECK=P1-.50;CAP=1.65
TP=R*sv;XP=BC-R*cv;T0=TP+(DECK-XP)/T
H0=(12.75-.75*.6/.8-B)/(K+.6/.8);M=hypot(1,K)
H=H0+.24*(1/M-.80)/(.60+K/M);HR=B+K*H0+.24;BE=atan(K)+asin(.60)
CORE=[(C,7.60),(.20,7.10),(2.50,6.),(4.40,3.50),(-.30,7.58),(2.25,6.50),(5.80,3.16)]
ANG=[0,2*pi/3,-2*pi/3];BUT=[pi/3,-pi/3,pi]
def wmin(g):return g-MU*sqrt(1-g*g)
def aperture():
    e=OFFSET;gap=RI-RP+e;half=gap/2;g=B-OD+.05
    z=sqrt(RG**2-half**2)-.5
    # For r>OD reaching any plate island, use 64° edge draft and
    # r_pole >= r_core-R. The crude bound changes slope at dstar.
    def edge(R):
        ds=RP+e+R-CAP/TR-OD
        a=(sqrt(R*R-ds*ds)+.50-CAP)/R
        # derivative after this breakpoint is TR-d/sqrt(R²-d²)>0 on
        # 0..g; in the interior of deck the direct cone normal is stronger.
        assert g/sqrt(R*R-g*g)<TR and 0<ds<g
        return a
    ef=edge(RG)
    # R actual 2.5 nominal throughout. For backing guarantee use tangent
    # R2.45 sub-balls, with their OWN r and x; outer bound is on those.
    ret=dict(shift=e,min_gap=RI-RP-e,max_gap=gap,inner_center_ahead=z,
       inner_min_x_work=wmin(z/RG),island_cap_check=wmin((z+.5-CAP)/RG),
       outer_trim_min_nx=ef,outer_rim_min_x_work=wmin(sqrt(RG**2-g*g)/RG),
       front_graph_min_x_work=wmin(cos(radians(64))),
       terminal_inner_back=PM+z-RG,terminal_outer_back=PM+sqrt(RG**2-g*g)-RG,
       diagonal_barrier=hypot(g,PH),max_seam_diagonal=hypot(gap,.5))
    ret['terminal_stroke_cases']=[dict(rim_plane=p,carrier_travel=p-P0,
       inner_trailing_bound=p+z-RG,outer_trailing_bound=p+sqrt(RG**2-g*g)-RG,
       rocked_tail_trailing_x=BC+p-P1-R) for p in (PM,1.58,PH)]
    assert min(ret[k] for k in ['min_gap','inner_min_x_work','island_cap_check','terminal_outer_back'])>0
    return ret
def draw():
    # δ=(.18,.18), local V station whose tangential projection is
    # (.5,.866). One exact finite-plane interference at full nominal draw.
    dt=.18*(1+sqrt(3))/2;dy=.18*(sqrt(3)-1)/2
    dist=R-dt*sv;hz=BC-dist*cv-DECK;tp=dt+dist*sv
    radial=BR+dy
    face=min(CAP-hz,(3.81-tp)*T-hz,(1.35-dy)*T-hz,
             TR*(RP-hypot(radial,tp))-hz)
    assert abs((tp-T0)*T-hz)<1e-10 and face>0
    # Boss worst lateral approach to button, polyline in (x,r). Extends to
    # edge at deck and radius 8.40; cap to R8.4-1.6/tan60.
    def seg(a,b,p):
        d=[b[i]-a[i] for i in (0,1)]
        s=max(0,min(1,sum((p[i]-a[i])*d[i] for i in (0,1))/sum(v*v for v in d)))
        return hypot(*(p[i]-a[i]-s*d[i] for i in (0,1)))
    def clear(p):
        top=p-.50+1.60;edge=8.40-1.60/tan(pi/3)
        # Rigid tail remains centered; translate plate *toward* button.
        boss=seg((p-.5,8.4),(top,edge),(BC,BR-OFFSET))-R
        lip=hypot(BC-p,RI-BR)-R
        # Also report if tail translates bodily with the plate.
        lip2=hypot(BC-p,RI-BR-OFFSET)-R
        return dict(boss_button=boss,boss_hull=C-R-top,rim_button=lip,
                    rim_if_tail_follows=lip2,cap_hull=C-R-(p-.5+CAP))
    return dict(home=clear(P0),draw=clear(P1),first_seat_early=T*dt,
                home_plane_reserve=cv*.50-sv*dt,full_face_penetration=R-dist,
                projection_t=tp,projection_h=hz,remaining_finite_faces=face,
                centered_contact=[XP,BR,TP])
def force():
    a=sqrt(.75)*sv;u=hypot(cv,a);skew=MU*cv/(a*u);eff=cv+MU*a*skew/u
    arm=R*MU*u/eff; N=20/(4*eff); res=[0.]*6; mom=0.
    for k in [pi/3,-pi/3]:
        for sg in [-1,1]:
            n=(cv,-sg*sv*sin(k),sg*sv*cos(k))
            N1=N*(1-copysign(skew,n[1]))
            f=[N1*(n[0]-MU*n[1]/u),N1*(n[1]+MU*n[0]/u),N1*n[2]]
            q0=(0.,0.,BR*sin(k));p=[q0[i]-R*n[i] for i in range(3)]
            x,y,t=p;fx,fy,ft=f
            for i,yy in enumerate([fx,fy,ft,y*ft-t*fy,t*fx-x*ft,x*fy-y*fx]):res[i]+=yy
    assert max(map(abs,(res[0]-20,*res[1:5],res[5]+20*arm)))<1e-12
    return dict(adverse_axial=20.,contact_magnitudes=[N*(1-skew),N*(1+skew)],
         support_wrench_about_button_line=res,adverse_force_line_offset=arm,
         max_stick_arm_sufficient=R*MU/(cv-MU*sv))
if __name__=='__main__':
    print(json.dumps(dict(label='exploratory',gap=aperture(),draw=draw(),rocking=force()),indent=2))
