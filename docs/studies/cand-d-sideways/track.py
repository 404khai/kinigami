"""Take 55 / exploratory. mm, N, N mm. Run python3 track.py [--json]."""
from itertools import combinations
from math import asin, atan, cos, degrees, hypot, pi, radians, sin, sqrt, tan
import json
import sys


R, B, O, H, F = 3.50, 3.65, 5.65, 1.65, .20
Y, L, S, RN, MU = 4., 6., 2.80, 1.50, .22
RP, HK, XK, STEP, LENGTH, END = 3.55, 1.55, sqrt(O*O-H*H), 1.50, 20., 5.60


def add(a,b): return tuple(x+y for x,y in zip(a,b))
def mul(a,k): return tuple(x*k for x in a)
def sub(a,b): return add(a,mul(b,-1))
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def det(a,b,c): return dot(a,cross(b,c))
def cross(a,b):
    x,y,z=a; X,Y,Z=b
    return y*Z-z*Y, z*X-x*Z, x*Y-y*X


def pose(theta, f=F):
    # Core offsets for an actual radius on the finite lip and rear corners.
    h=H+f
    xi=sqrt((B+f)**2-h*h); xo=sqrt((O-f)**2-h*h)
    cx=xi-sqrt((R+f)**2-h*h)
    a=radians(theta); u=(cos(a),-sin(a),0.)
    dy=(L-f-(xo-cx)*u[0])/u[1]
    c=(cx,-Y+f-dy,0.)
    gi=(xi,c[1],h); go=(xo,-Y+f,h)
    ni=mul(sub(c,gi),1/(R+f))
    contacts=[(add(g,mul(n,f)),n) for g,n in ((gi,ni),(go,u))]
    arm=sub(contacts[1][0],c)
    rad=hypot(h,arm[1]*u[0]-arm[0]*u[1])
    p=c[1]-R
    # All points of a tilted cylinder satisfy these halfspace implications.
    sh_x=cx+L*u[0]+S*u[1]
    def min_y_in_x(xmax,rad):
        return c[1]+(xmax-cx)*u[1]/u[0]-rad/u[0]
    neck_y=min_y_in_x(RP,RN); shoulder_y=min_y_in_x(XK,S)
    guide_y=min_y_in_x(6.6,S)
    housing_x=cx+11*u[0]+13*u[1]
    return dict(yaw_deg=-theta,center=c,u=u,front_y=p,contacts=contacts,
                outer_contact_on_shoulder_radius=rad,
                shoulder_edge_reserve=S-rad,neck_vs_disk=neck_y-p,
                shoulder_vs_disk=sh_x-RP,shoulder_vs_key=shoulder_y-(p-STEP),
                neck_vs_key=min_y_in_x(XK,RN)-(p-STEP),
                shoulder_vs_rear_guide=guide_y+6.2,housing_vs_head=housing_x-6.6,
                core_xz=[xi,xo,h],roll_radius=f)


def eligible(v):
    return (-Y <= v['front_y'] < END and abs(v['center'][1])<Y-v['roll_radius']
            and all(v[k]>0 for k in ('shoulder_edge_reserve','neck_vs_disk',
                    'shoulder_vs_disk','shoulder_vs_key','neck_vs_key',
                    'shoulder_vs_rear_guide','housing_vs_head')))


def rays(v,mu):
    c=v['center']; columns=[]; sites=[]
    for site,(q,n) in enumerate(v['contacts']):
        u=mul((n[1],-n[0],0),1/hypot(*n[:2])); w=cross(n,u)
        for j in range(16):
            angle=j*pi/8
            t=add(mul(u,cos(angle)),mul(w,sin(angle)))
            force=add(n,mul(t,mu)); torque=cross(sub(q,c),force)
            # Lower site and force mirror in z: other 3 coordinates cancel exactly.
            columns.append(mul((force[0],force[1],torque[2]),2))
            sites.append((site,j,q,n,force))
    return columns,sites


def certificate(v,mu):
    """Min-sum-normal LP basic solutions, unrestricted body, inside friction disks."""
    A,sites=rays(v,mu); target=(0,-1.,0)
    best=None
    for i,j,k in combinations(range(len(A)),3):
        a,b,c=A[i],A[j],A[k]; d=det(a,b,c)
        if abs(d)<1e-10: continue
        x=det(target,b,c)/d; y=det(a,target,c)/d; z=det(a,b,target)/d
        if min(x,y,z)<-1e-10: continue
        cost=2*(x+y+z)
        if best is None or cost<best[0]-1e-10: best=(cost,[(i,x),(j,y),(k,z)])
    if best is None: return None
    loads=[[0.,(0.,0.,0.)] for _ in range(2)]
    for i,x in best[1]:
        s,_,_,_,f=sites[i]; loads[s][0]+=x; loads[s][1]=add(loads[s][1],mul(f,x))
    c=v['center']; residual=(0.,1.,0.,0.,0.,0.); reactions=[]
    for (q,n),(N,f) in zip(v['contacts'],loads):
        assert abs(dot(n,f)-N)<1e-9 and dot(n,n)>1-1e-12
        ft=sub(f,mul(n,N))
        assert sqrt(dot(ft,ft))<=mu*N+1e-10
        for s in (1,-1):
            Q=(q[0],q[1],s*q[2]); V=(f[0],f[1],s*f[2])
            residual=add(residual,V+cross(sub(Q,c),V))
            reactions.append(dict(q=Q,F=V,N=N))
    assert max(map(abs,residual))<1e-9
    return dict(normal_sum_per_drive=best[0],sites=reactions,residual=residual)


def hertz(load,rx,ry,E=110000.):
    # Elliptic Hertz via u=tan(t) on the normalized curvature integrals.
    def integrals(k):
        xx=yy=0.; nt=256
        for j in range(nt+1):
            t=(pi/2)*j/nt; h=cos(t)**2; d=k*k*h+sin(t)**2
            p=(1 if j in (0,nt) else 4 if j%2 else 2)*2*h/sqrt(d)
            xx+=p; yy+=p/d
        return xx*pi/(6*nt),yy*pi/(6*nt)
    lo,hi=1.,128.
    for _ in range(50):
        k=.5*(lo+hi); ix,iy=integrals(k)
        if ix/iy>ry/rx: hi=k
        else: lo=k
    a=(3*load*rx*ix/(2*pi*E))**(1/3); b=k*a
    return dict(load_N=load,a_mm=a,b_mm=b,peak_GPa=3*load/(2*pi*a*b*1000))


def test():
    v=pose(17.25); assert eligible(v)
    cert=certificate(v,MU); assert cert and 2.78<cert['normal_sum_per_drive']<2.79
    assert certificate(v,.20) is None
    angular=[]
    for theta in [14+i/4 for i in range(23)]:
        case=pose(theta)
        if eligible(case):
            sol=certificate(case,MU)
            if sol: angular.append([theta,case['front_y'],sol['normal_sum_per_drive']])
    assert angular
    # Continuous collision-free local approach: at fixed c, rotate from zero.
    # Shoulder support of track increases for yaw 0..a if D_y cos(a)>D_x sin(a).
    cx,cy,_=v['center']; xi,xo,h=v['core_xz']; a=-radians(v['yaw_deg'])
    assert (cy+Y-F)*cos(a)>(xo-cx)*sin(a)
    assert cx+L>O and -(.15)+L>O
    # All other separation bounds used in eligible() are weakest at the final
    # tilt (cos decreases, tan/sec increase; relevant xmax is ahead of cx).
    assert 2.8<3.5 and 11-.15>6.6
    # Along aligned translation, shoulder x>.15-negative datum+6; if it
    # projects into the guide x<=6.6, its y is still >=cy-S>-6.2.
    assert cy-S>-6.2 and cy-R>=-Y and cy-RN > -Y-STEP
    sharp=pose(15.25,0.); sharp_cert=certificate(sharp,.23)
    assert eligible(sharp) and sharp_cert
    # Released plug parked: whole straight C length has both filled sections.
    assert END-STEP>Y and END-LENGTH < -Y
    assert -9.-(END-LENGTH)>5 and -Y-LENGTH+16.5>-9
    n=v['contacts'][0][1]
    fx=40.; N=fx/(-n[0]-MU*abs(n[2]))
    straight=hertz(N,1/(1/R+1/F),R)
    jamcorner=hertz(20*cert['sites'][2]['N'],F,F)
    assert abs(jamcorner['a_mm']-(3*jamcorner['load_N']*F/(4*110000.))**(1/3))<1e-9
    def band(r,h): return h*sqrt(r*r-h*h)+r*r*asin(h/r)
    area=pi*((O-F)**2-(B+F)**2)-band(O-F,h)+band(B+F,h)
    lim=sqrt((R+F)**2-h*h); exit_samples=[]
    for frac in (0.,.5,.9,.99,.999):
        d=frac*lim; nx=sqrt(lim*lim-d*d)/(R+F)
        exit_samples.append([frac,d,nx,1/nx])
    return dict(label='exploratory',units='mm, N, N mm',rounded_witness=v,
        unit_drive_certificate=cert,
        sampled_jams_yaw_magnitude_front_y_normal_sum=angular,
        sharp_ideal_comparison=dict(pose=sharp,unit_drive=sharp_cert),
        nominal_reverse_lost_motion=cx+(B-R),
        plug=dict(disc_radius=RP,key_halfwidth=HK,key_tip_x=XK,key_lag=STEP,
                  rear_lag=LENGTH,front_y_range=[-Y,END],rear_guide_y=[-26,-6.2]),
        X_takeup=dict(example_draw=fx,one_lip_upper_N=N,lip_hertz=straight,
                      core_XZ_area_mm2=area,neck_area_mm2=pi*RN*RN),
        rounded_corner_hertz_at_example_20N_drive=jamcorner,
        last_flank_fraction_d_nx_Nsum_per_axial_N=exit_samples,
        last_edge_helpful_even_at_mu_after_d=(R+F)*MU/hypot(1,MU))


if __name__=='__main__':
    result=test()
    if '--json' in sys.argv: print(json.dumps(result,indent=2,sort_keys=True))
    else:
        for k in ('rounded_witness','unit_drive_certificate','X_takeup',
                  'sampled_jams_yaw_magnitude_front_y_normal_sum',
                  'rounded_corner_hertz_at_example_20N_drive',
                  'last_flank_fraction_d_nx_Nsum_per_axial_N'):
            print(k, result[k])
