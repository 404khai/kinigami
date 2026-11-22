"""Take 74 — force closure, finite fit and release of one transverse key."""
import json
from itertools import product
from pathlib import Path
from key import *
PH=pi/3; ECC=1.65; a=ANG; c,s=cos(a),sin(a);v=V
p,n,C=model(phase=PH,ecc=ECC)
q=C[0]; xc,yc,_=p[0]; u=np.array([-s,c,0.])
FIL=.35;Y0=yc-1.05;XB=-4.18;XF=-1.50;SH=1.65
# Sphere offset of convex core: cut inner polygon by these offset planes,
# then dilate by FIL. No extrapolated intersection through the fillet.
KY=Y0+FIL; KX=(R+FIL-s*(KY-q[1]))/c+q[0]
ST1=(R+FIL)*s+q[1]-KY;ST2=R+FIL+q[1]-KY;PARK=4.15
def shift(st):
    if st<=ST1:return tan(a)*st
    b=min(1.,(KY+st-q[1])/(R+FIL))
    return KX-sqrt(max(0.,1-b*b))*(R+FIL)-q[0]
def serialize(v):
    if isinstance(v,np.ndarray):return v.tolist()
    if isinstance(v,np.generic):return v.item()
    raise TypeError(type(v))
def fit():
    # Unknown body pose (translation t, exponential rotation w about X=BC),
    # seventh unknown key stroke. Face offsets ±.020, local normal ±.6 deg,
    # about the nominal pole. Smooth sphere radii and centers as drawn.
    D=np.linalg.inv(clean(p,n)[0][:,1:].T)
    verts=np.array(list(product([-1,1],repeat=6)))
    Kt=max(norm(y[:3]) for y in verts@D.T)
    Kr=max(norm(y[3:]) for y in verts@D.T)
    en=2*sin(radians(.6)/2);delta=.020+R*en**2/2
    M=.023
    # A fixed-point map on [-M,M]^6 in plane-error coordinates:
    # t,BR*w=Dg. Rotation Taylor remainder norm <= BR*|w|²/2.
    bound=delta+en*(Kt+Kr)*M+(Kr*M)**2/(2*BR)
    assert bound<M
    T=Kt*M;W=Kr*M/BR
    eface=T+Kr*M+R*en
    ekey=T+norm(q-[BC,0,0])*W+R*en
    stroke=(.020+R*en**2/2+ekey-R*en)/(s-en)
    assert stroke<.30
    return dict(offset=.020,normal_degrees=.60,box_radius=M,map_bound=bound,
        translation=T,rotation_deg=degrees(W),face_pole_shift=eface,
        key_pole_shift=ekey,key_seventh_stroke=stroke,
        rank_seven=np.linalg.matrix_rank(np.block([[clean(p,n)[0].T,
             np.array([[-n[0]@Y]]+[[0.]]*6)]])))
def forcewin():
    w,N=clean(p,n);F=fit();N0=np.r_[1.,N]
    assert min(N)>0 and F['rank_seven']==7
    # Rigid normal-force only first-loss under unit scaled wrench ||(F,M/BR)||.
    S=np.linalg.inv(w[:,1:]);threshold=N/np.linalg.norm(S,axis=1)
    j=np.argmin(threshold);ext=S[j]*N[j]/(S[j]@S[j])
    assert abs((N-S@ext)[j])<1e-12
    def robust(mu):
        m=tan(atan(mu)+radians(.6));k=hypot(1,m)
        E=F['face_pole_shift'];summ=(c+m*s)/(cos(V)-m*sin(V))
        assert E>=F['key_pole_shift']
        # For an additional applied wrench |(F,M/BR)|<=H per nominal
        # key normal projection, total nominal projections <=1+summ+H/d.
        lower=[];loss=[]
        for i in range(1,7):
            val,_,_,l=opt(p,n,m,i,48,True)
            mom=norm(l[3:6])*E*k/BR
            lower.append(val-mom*(1+summ)-1e-8)
            loss.append(norm(l[:6])+mom/(cos(V)-m*sin(V)))
        return dict(mu=mu,min_nominal_projection_per_key=min(lower),
           sufficient_external_wrench_radius=min(x/y for x,y in zip(lower,loss)),
           independent_face_debit=E,nominal_normal_cone_mu=m)
    # Critical stationary friction for at least one missing seat, bracket
    # with outer and inner polygons. This is a feasibility transition,
    # not the coefficient of any actual installation.
    def crit(outer):
        lo,hi=.10,.21
        for _ in range(14):
            h=(lo+hi)/2
            if min(opt(p,n,h,i,32,outer)[0] for i in range(1,7))>1e-8:lo=h
            else:hi=h
        return lo if outer else hi
    # Actual bad-gap equilibrium: pole 2 physically recessed along -n2.
    # Use exactly the kinetic direction of key friction on closing, smaller
    # than the static max; close every wrench with five physical seat faces.
    m=.19;f,b=basis(p,n,m,24,False);f[0]=n[0]-m*u
    b[0]=wrench(p[0],f[0,0])
    eq=np.vstack([b.reshape(-1,6).T,np.repeat([1,0,0,0,0,0,0],24)])
    lp=linprog(np.repeat(np.arange(7)==2,24),A_eq=eq,b_eq=[0]*6+[1],
               bounds=(0,None),method='highs');assert lp.success
    x=lp.x.reshape(7,-1);forces=(x[:,:,None]*f).sum(axis=1)
    normals=(forces*n).sum(axis=1)
    resid=sum(wrench(pp,ff) for pp,ff in zip(p,forces))
    assert normals[2]<1e-10 and norm(resid)<1e-9 and np.min(np.delete(normals,2))>.01
    assert min(m*nn+1e-9-norm(ff-nn*vv) for nn,ff,vv in zip(normals,forces,n))>=0
    trial=robust(.08);assert trial['sufficient_external_wrench_radius']>0
    return dict(key_force_line_y=ECC,triangle_side_clearance=min(BR/2-ECC*cos(k)
        for k in (0,2*pi/3,-2*pi/3)),clean_normal_forces=N0,clean_axial_seat_shares=
        cos(V)*N.reshape(3,2).sum(axis=1)/c,clean_first_loss_radius=min(threshold),
        clean_first_loss_pole=int(j+1),clean_adverse_wrench=ext,
        nominal_stationary_first_loss_mu=[crit(True),crit(False)],
        illustrative_robust=trial,
        bad_gap=dict(recessed_pole=2,recess=.020,mu=m,normal_forces=normals,
           contact_forces=forces,residual=norm(resid),key_drive_force=-forces[0,1],
           key_tension_per_normal=-forces[0,0]),shallow_trial=shallow())
def shallow():
    pp,nn,_=model(radians(3),radians(65),PH,.30)
    g=min(opt(pp,nn,.23,i,32,False)[0] for i in range(1,7))
    return dict(taper_deg=3.,seat_deg=65.,minimum_seat_normal=g,
        open_flank_assist=sin(radians(3))-.23*cos(radians(3)))
