"""Exploratory Take 66; local x,y,t; mm/N/Nmm. python3 lobe.py"""
from math import *
import json
B,K,KR,XB=14.54,.41,.26,-1.55
D,R0,R,C,A,L=12.42,2.45,2.5,-2.25,10.75,4.
W,WC,RI,RO=3.20,3.26,1.10,1.16
MU=.23
# Offset hull embeds the full original three-knot socket (not a thin replacement).
CORE_DISKS=[(C,7.60),(.20,7.10),(2.50,6.00),(4.40,3.50),
            (-.30,10.08-R),(2.25,9.00-R),(5.80,5.66-R)]
def b(x):return max(B+K*x,B+(K-KR)*XB+KR*x)
def w(x,t):return sqrt(b(x)**2-t*t)
M=hypot(1,K)
def dot(a,b):return sum(i*j for i,j in zip(a,b))
def add(a,b,s=1):return tuple(i+s*j for i,j in zip(a,b))
def unit(a):return tuple(i/hypot(*a) for i in a)
def axes(n,off):
    d=sqrt(1-n*n);xp=C+R*n;yp=A+R*d;h0=(yp+xp*n/d-B)/(K+n/d)
    h=h0+off*(1/M-d)/(n+K/M);v=B+K*h0+off
    return h,v,atan(K)+asin(n),xp,yp
h,v,beta,xp,yp=axes(.60,.24)
def rot(u,z,t,th):
    return (h+u*cos(th)+z*sin(th),v-u*sin(th)+z*cos(th),t)
def hertz(N,rx,rt):
    def I(k):
        x=y=0
        for j in range(385):
            c=cos(j*pi/768)**2;d=1+(k*k-1)*c
            f=(1 if j in (0,384) else 4 if j%2 else 2)*2*c/sqrt(d)
            x+=f;y+=f/d
        return x*pi/2304,y*pi/2304
    lo,hi=1.,64.
    for _ in range(48):
        k=(lo+hi)/2;x,y=I(k)
        if x/y>rt/rx:hi=k
        else:lo=k
    a=(3*N*rx*x/(2*pi*110000))**(1/3);bb=k*a
    return a,bb,3*N/(2*pi*a*bb*1000)

def geometry(n,off):
    hh,vv,be,xw,yw=axes(n,off);d=sqrt(1-n*n)
    c,s=cos(be),sin(be);u,z=xw-hh,yw-vv
    pp=hh+u*c-z*s
    length=-pp*M; rx=R;kt=d/(L+R*d)-1/(M*(B+K*pp))
    toe=vv+hh*s+(B-vv)*c
    # Eroded cone vs current jaw-facing core circle, including all attitudes
    # of the LEAF for a centered flange. Other core sections below.
    ax,az=C-hh,A-vv
    def coeff(th):
        c,s=cos(th),sin(th)
        pc=hh+ax*c-az*s;yc=vv+ax*s+az*c;J=B+K*pc-M*R
        return J-yc,J*K*s+yc*c-L
    assert min(K*ax-az,-ax-K*az)>0 and abs(coeff(be)[0])<1e-12
    df=K*abs(B+K*hh-M*R)+2*K*(1+K)*(abs(ax)+abs(az))+vv+4*(abs(ax)+abs(az))
    assert min(coeff(i*be/64)[1] for i in range(65))>df*(be/64)**2/8
    N=40/(n-MU*d)
    tau=(u*d-z*n+MU*abs(u*n+z*d))*N
    return dict(qx=n,offset=off,H=[hh,vv],beta=degrees(be),pole=[xw,yw],pole_park_p=pp,
       toe_length=length,toe_r=toe,disk_clear=toe-D,rel_k_t=kt,N40=N,torque40=tau,
       ideal_tangent_force_at_P=tau/hypot(1.03,2.70),ellipse=hertz(N,rx,1/kt))

def others(n,off):
    hh,vv,be,_,_=axes(n,off); gap=100
    # 3D convex hull of DISKS then ball offset; angularly sampled centers with
    # analytic Hausdorff debits between azimuth and phase. Signed cone distance
    # is 1-Lipschitz. Right/left lobes symmetric.
    for x,y,t,r in [(xx,0,0,rr) for xx,rr in CORE_DISKS]+[(C,-.5*(A-L),sqrt(.75)*(A-L),L)]:
        points=[(y+r*cos(i*pi/128),t+r*sin(i*pi/128)) for i in range(256)]
        minval=100
        for j in range(257):
            th=j*be/256;c,s=cos(th),sin(th)
            for yy,tt in points:
                p=hh+(x-hh)*c-(yy-vv)*s
                ry=vv+(x-hh)*s+(yy-vv)*c
                minval=min(minval,(B+K*p-hypot(ry,tt))/M-R)
        gap=min(gap,minval-r*pi/256-(hypot(x-hh,y-vv)+r)*be/512)
    assert gap>0
    return gap

def park():
    # Nominal relative tangential step at all seams <=H. Total signed normal
    # separation between a reference cone INSIDE all stock and covering stock <=e.
    H=.075;e=.020;g=B-D+.05
    angle=atan(K)-acos((sqrt(R0**2-H**2)-e)/R0)
    nx=sin(angle);ax=nx-MU*cos(angle)
    back=sin(atan(KR))-MU*cos(atan(KR))
    req=R0-sqrt(R0**2-g*g)
    # Over rear cut (u≈1.1), |w-v|<.36. Test the two extremal u bounds
    # first to localize the intersection; w increases with p, decreases in t.
    assert hypot(.99,max(abs(w(h+.99,WC)-v),abs(w(h+RO,0)-v)))<RI
    assert max(abs(w(h+.99,WC)-v),abs(w(h+RO,0)-v))<.36
    deriv=(sqrt(RI**2-.36**2)-.36*.44)/RO
    dx=(RO-RI)/(2*deriv)
    # Δphi at fixed t with changed b is < .001 rad; retain tighter bound
    # to avoid wasting the gap allowance. Side correction at constant p.
    dr=K*dx
    da=WC*dr/(13.9*sqrt(13.9**2-WC**2))
    bound=max(hypot(M*dx,14.55*da),14.55*(WC-W)/sqrt(13.9**2-WC**2))
    assert bound<H and min(ax,back,1.35-req,b(-6.95)-D)>0
    return dict(home_r=b(-6.95),home_gap=b(-6.95)-D,g_eff=g,terminal_min_lift=req,
       terminal_net=1.35-req,max_step=sqrt(R0**2-H**2)-R0*cos(atan(K)-atan(MU)),
       total_normal_step_budget=e,tangent_H=H,nearest_stock_cover=bound,
       front_nx=nx,front_X_per_N=ax,rear_X_per_N=back)

def linked():
    # Both slopes bound each finite cheek by separate concave-graph tangents.
    margins=[]
    for t,rad,ear in [(3.26,.45,False),(4.58,.55,True),(5.55,.90,True)]:
        rmin=100
        for k,bc in [(K,B),(KR,B+(K-KR)*XB)]:
            bh=bc+k*h;wc=sqrt(bh*bh-t*t);m=k*bh/wc
            ex,ez=(.10,2.70) if t<5 else (0,0)
            z=-ex*sin(beta)+ez*cos(beta)-m*(ex*cos(beta)+ez*sin(beta))
            rmin=min(rmin,v-wc+(min(0,z) if ear else z)-rad*hypot(1,m)-.20)
        margins.append(rmin)
    assert min(margins)>.17
    return margins

def obstruction():
    # Static final-approach pose in free space, not a trajectory from seated.
    # D0 points FROM exposed circular drive boss TOWARD the neighbor.
    th=.99*beta;D0=(.80,.60,0);T0=(-.60,.80,0);A0=.55
    xt=add(tuple(cos(A0)*z for z in D0),T0,sin(A0))
    rt=add(tuple(-sin(A0)*z for z in D0),T0,cos(A0))
    tt=(0,0,1)
    bp=rot(1.03,2.70,1.80,th);q=add(bp,D0,.88)
    center=add(add(q,D0,R),rt,-A)
    # Tail min-support along arbitrary axis, actual disks and their convex
    # hull, capsules mounted 60° from loaded lobe. Fork overbound uses all
    # corners in a symmetric radial rectangle.
    def tail_min(d):
        ax,ar,at=dot(d,xt),dot(d,rt),dot(d,tt); sz=hypot(ar,at)
        base=dot(d,center)-R*hypot(*d)
        H=[(x-C)*ax-r*sz for x,r in CORE_DISKS]
        H+= [(A-L)*(ar*cos(k)+at*sin(k))-L*sz for k in [0,2*pi/3,-2*pi/3]]
        caps=[(x-C)*ax+r*(ar*cos(k)+at*sin(k)) for k in [pi/3,pi,5*pi/3]
              for x,r in [(-4.31,10.30),(C,10.30),(0.,5.)]]
        fork=min(dot(d,center)+(x-C)*ax-hypot(hy,hz)*sz for x,hy,hz in
                 [(4,3.3,5.08),(6.75,2.15,6.45),(11.46,1.45,6.66)])
        return min(base+min(H+caps),fork)
    # Change meridian/clock so the R2.50 extremal center is the given lobe.
    assert abs(tail_min(D0)-dot(q,D0))<1e-9
    # Bounds on positive meridional radial projection; added amount for yz
    # rotations makes these conservative for the other two sectors.
    g=tail_min(D0)
    def radial(q):return dot(D0,q)
    # List outer solids as (name, extreme D0·q, t_low,t_high). A family
    # D0+a e_t provides exact separating certificates without discretizing
    # either convex body. Positive nominal margin is a strict certificate.
    parts=[]
    def part(name,top,lo,hi):parts.append((name,top,lo,hi))
    def P(u,z):return radial(rot(u,z,0,th))
    def pairs(name,s,lo,hi):
        part(name+'+',s,lo,hi);part(name+'-',s,-hi,-lo)
    # Cone backing, ordinary pillars, hardware at loaded station.
    # For projection over the cone choose t=0 at every p, ignoring trim.
    leafmax=max(P(p-h,B+K*p+.95-v) for p in [h+.65,0])
    part('leaf',leafmax,-W,W)
    for name,t1,t2,top in [('drive_boss',1.70,2.65,P(1.03,2.70)+.88),
                            ('pin',0,2.65,P(1.03,2.70)+.60),
                            ('pillar',1.70,2.65,max(P(u,2.85) for u in [1.22,1.74])),
                            ('outer_pillar',2.78,3.2,max(P(u,2.) for u in [1.22,1.74])),
                            ('rib',2.78,3.20,max(P(.10,2.70),P(1.44,1.85))+.45),
                            ('crossbar',3.03,4.90,P(.10,2.70)+.45),
                            ('ear',4.58,5.35,max(P(0,0),P(.10,2.70))+.55),
                            ('pin_stub',4.9,7.55,P(0,0)+.52),
                            ('bearing',5.55,6.15,P(0,0)+.90),
                            ('stop_lever',6.68,7.28,max(P(0,0),P(0,3.8))+.46),
                            ('stop_block',6.60,7.40,.8*(h-.46)+.6*(v+4.25))]:
        pairs(name,top,t1,t2)
    part('fixed_wall',.60*15.73,-16,16)
    part('fixed_rear_cap',max(.8*p+.6*(b(p)+.95) for p in [-7.2,h+RI]),-WC,WC)
    # Disk and fixed index insert envelope with x<=-5.0.
    part('disk',.8*(-5)+.6*D,-14,14)
    # Remaining stations: y_local>=~11, |t_local|<=7.55, x<=2.2, so
    # y_in_loaded_station <= -.5*11+.867*7.55. For ordinary cone use wall case.
    part('other_stations',.8*2.2+.6*(-5.5+.867*7.55),-25,25)
    mins={}
    for name,top,lo,hi in parts:
        opts=[(tail_min((.8,.6,a))-top-max(a*lo,a*hi),a) for a in [i*.01 for i in range(-200,201)]]
        mins[name]=max(opts)
    for sign in (1,-1):
        key='stop_lever'+('+' if sign==1 else '-')
        best=(mins[key][0],0,mins[key][1])
        for j in range(-32,33):
            for k in range(-32,33):
                m,a=j*.035,k*.035;dv=(.8-.6*m,.6+.8*m,a)
                eb=max(dot(dv,rot(0,z,0,th)) for z in (0,3.8))+.46*hypot(*dv[:2])
                gap=tail_min(dv)-eb-max(a*sign*6.68,a*sign*7.28)
                best=max(best,(gap,m,a))
        mins[key]=best
    f=(-.8+MU*.6,-.6-MU*.8,0)
    req=(q[0]-h)*f[1]/f[0]-(q[1]-v)
    # At the identical actuator angle: let the centered loaded neighbor
    # translate forward to the exact lobe-plane contact, not a pose snap.
    n=sin(th-atan(K));d=cos(th-atan(K))
    face=rot(0,B+K*h-v,0,th)
    newC=face[0]+(-R-d*(A-face[1]))/n
    po=(newC+R*n,A+R*d)
    ppark=h+(po[0]-h)*cos(th)-(po[1]-v)*sin(th)
    assert newC>C and ppark<0 and hypot(ppark-h,w(ppark,0)-v)>RO
    f2=(n+MU*d,d-MU*n)
    lim=(po[0]-h)*f2[1]/f2[0]-(po[1]-v)
    assert req>lim and abs(mins['drive_boss+'][0])<1e-12
    assert min(val[0] for key,val in mins.items() if key!='drive_boss+')>0
    return dict(phase=th,q=q,boss=bp,core_center=center,tail_axes=[xt,rt,tt],
                f_on_leaf=f,required_lambda=req,workface_max_lambda=lim,
                centered_C_same_phase=newC,work_pole_same_phase=po,
                supports={k:list(vv) for k,vv in mins.items()})

if __name__=='__main__':
    rows=[geometry(.6,.24),geometry(.64,.18)]
    for row in rows:row['other_section_min']=others(row['qx'],row['offset'])
    print(json.dumps(dict(label='exploratory',section=rows,park=park(),
                     cheeks=linked(),partial=obstruction()),indent=2,allow_nan=False))
