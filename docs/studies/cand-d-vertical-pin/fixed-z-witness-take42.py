"""Independent material witnesses, load cases and end-state checks; no gate evidence."""
from pathlib import Path
from runpy import run_path
d=run_path(str(Path(__file__).with_name('fixed-z-stage-take42.py')))
globals().update({k:v for k,v in d.items() if not k.startswith('__')})
def ringgap(q,advance=0):
    return hypot(hypot(q[0]-C-advance,q[1])-R,q[2])-TUBE
def mean(a):return tuple(sum(x)/len(x) for x in zip(*a[1]))
def actual():
    # Screw motor is a Z cylinder; master carriage minus the cylindrical
    # guide channel about (y,z)=(-14.80,6.70). Point common to real stock.
    q=(-7.90,-15.90,7.70);dep=3-hypot(q[0]+8.75,q[1]+17.70)
    assert -6.78+REL<q[0]<1.1+REL and -16.05<q[1]<-13.55 and 5.05<q[2]<8.4
    assert hypot(q[1]+14.8,q[2]-6.7)>1. and dep>.99
    print('X motor v relieved master shell, point and depth inside motor',q,dep)
    q=(-8.75,-15.10,-17.60);dep=3-hypot(q[0]+8.75,q[1]+17.70)
    assert -18.35<q[2]<10.35 and -21.95<q[2]<-16.55 and -15.325<q[1]<15.325
    print('X motor vs cell, point and motor depth',q,dep)
    m=next(a for a in body3() if a[0]=='joint motor')
    q=mean(next(a for a in seats() if a[0]=='land0/-1'))
    for pp,u in ((35,12.15),(36,13.15),(37.5,14.65)):
        qr=plus(q,(u,0,0));p=plus(m[1][0],(pp,0,0));depth=3.-hypot(qr[0]-p[0],qr[1]-p[1])
        assert -12.7<qr[2]<7 and depth>2.93
        print('zero-yaw/zero-departure recovery, pitch/face travel/land point/next motor depth',pp,u,qr,depth)
        cen=C-pp;theta=atan2(p[1],p[0]-pp-cen)
        centerline=(cen+R*cos(theta),R*sin(theta),0)
        depth=3-hypot(centerline[0]-p[0]+pp,centerline[1]-p[1])
        assert depth>1.
        print('own passive torus centreline in own motor at stow yaw zero',pp,centerline,depth)
    # True radial distances to the torus at interior points of the lands,
    # not chord/box approximations. Crop test for just one nominal patch.
    s=next(a for a in seats() if a[0]=='land1/1');q=mean(s)
    pt=min(s[1],key=ringgap);print('home land corner vs torus',pt,ringgap(pt))
    assert ringgap(pt)<-.08
    qr=plus(q,(REL,0,0));print('fixed relieved land vs translated torus',qr,5.825,ringgap(qr,5.825));assert ringgap(qr,5.825)<-.13
    a,b,c=[sub(s[1][j],s[1][0]) for j in (4,2,1)]
    # Signed distance is 1-Lipschitz. Full continuous product of land
    # volume and relative 0..REL translation; subdivide an optional .55 crop.
    scale=.55;N=30
    small=[plus(q,plus(mul(scale*(i/N-.5),a),plus(mul(scale*(j/N-.5),b),mul(k/N-.5,c))))
           for i,j,k in product(range(N+1),repeat=3)]
    # The equivalent x interval is exact, not samples. XY squared-distance
    # range is continuous; minimize over that radial interval for each point.
    def seg(v):
        x1=v[0]+REL-C;x2=v[0]-C;y=v[1]
        lo=hypot(max(x1,-x2,0),y);hi=hypot(max(abs(x1),abs(x2)),y)
        return hypot(max(lo-R,R-hi,0),v[2])-TUBE
    lower=min(map(seg,small))-(scale*hypot(*a)+scale*hypot(*b)+hypot(*c))/(2*N)
    print('cropped .55 front pad vs intact aligned torus, continuous lower bound',lower)
    assert lower>.24
    # Eye shank still linked at seated z=0; extraction swept +Z. True
    # hemispherical nose has minimum normal distance to the forward plane.
    print('cap to inner/outer planes, nominal at top',*((PARK+PIN-8.42-t)/sqrt(2)-PIN for t in (0,.65)))
    print('closed U and raised U max z',max(proj(a,Z)[1] for a in pin()),max(proj(a,Z)[1] for a in pin(DZ)))
    print('clamp carrier -/+; pusher terminal; trailing boss xmin at maintained crown contact; spare to x18.60',REL,STROKE,5.48+STROKE,7-2.7+(STROKE-(15-6.5-2.7-5.48)),7-2.7+STROKE-.32-18.6)
def beam():
    E=205000.;I=pi*3.5**4/64;J=2*I;S=16.80-12.90
    for f,z in [((121.,0.,0.),0),((131.55,0.,0.),0),((131.55,24.,-18.),-3.),((5.,0.,0.),0)]:
        fx,fy,fz=f;fh=hypot(fx,fy);assert hypot(fy,fz)<=.23*fx+1e-9
        # Inner equator contact on the pin. Last case puts load toward tip
        # but still on cylinder (transition -4.25). No equal sharing.
        def mom(L):return L*fy, -L*fx+1.75*fz, -1.75*fy
        m=mom(JMIN-z);bm=hypot(*m[:2]);sigma=bm*PIN/I+abs(fz)/(pi*PIN**2);tau=abs(m[2])*PIN/J
        ax=12.90-z;mm=mom(ax);r2=(-mm[1]/S,mm[0]/S);r1=(-fx-r2[0],-fy-r2[1]);n1=hypot(*r1);n2=hypot(*r2)
        # Upper bound by triangle inequality for eccentric axial force's couple.
        L=JMIN-z;M0=abs(PIN*fz);clamp=(fh*L**3/3+M0*L**2/2)/(E*I)
        simple=(fh*ax**2*(ax+S)/3+M0*(ax*ax/2+S*ax/3))/(E*I)
        print('F, contact z, M_b/T, combined nominal VM MPa, deflection clamp/support mm, guide N/N, drag N, projected band pressures MPa',f,z,bm,m[2],hypot(sigma,sqrt(3)*tau),clamp,simple,n1,n2,.23*(n1+n2),n1/(3.5*.70),n2/(3.5*.70))
    print('max unloaded radial play extended from opposite band ends at z0',.05+2*.05*12.9/S)
    for znear,zfar in [(12.55,17.15),(12.90,16.80),(13.25,16.45)]:
        print('support centroid sensitivity (fixed pure 121N) bands z, estimated drag',
              znear,zfar,.23*121*(1+2*znear/(zfar-znear)))
    x=12.90-(14.80-4.53);F=121
    print('positive X forward roof rim play+elastic linearized displacement vs clearance .10',
          .05+.10*x/S+F*(12.90*S*x/3+x*x*(3*12.90-x)/6)/(E*I))
    print('dual short symmetric journal comparator z 12.55..15.10 per side, tip shank transition/far exit, lift, 131.55N deflection/stress',
          (-17.05+1.75,-15.1),PARK+17.05,131.55*27.65**3/(48*E*I),131.55*27.65/4*PIN/I)
def tines():
    # Face-only preload, no external wrench. At a section x=1.13 just
    # forward of the joined rear tie each tine alone carries its land.
    # For any possible letting N_i>=0 with sum(n_ix*N_i)=P, at least one
    # root moment M is >= P/sum(n_ix/abs(m_iy)). Allow each contact to
    # range over the entire nominal flat, choosing its most helpful arm.
    total=0.; arms=[]
    for j,(b,k) in enumerate(zip(BS,SLOPE)):
        for sg in (-1,1):
            n=plus(mul(cos(radians(58)),unit((1,k,0))),mul(sg*sin(radians(58)),Z))
            s=next(a for a in seats() if a[0]==f'land{j}/{sg}')
            v=[(q[2]+4*sg)*n[0]-(q[0]-1.13)*n[2] for q in s[1][1::2]]
            assert min(v)*max(v)>0
            arm=min(map(abs,v));total+=n[0]/arm;arms.append(arm)
    for p in (65.5,131.55):
        m=p/total; W=1.26*1.04**2/6
        print('six independent cold tines, P / min arms / minimax root moment / W / fibre stress MPa',p,arms,m,W,m/W)
def drives():
    # Not a motor rating. Guide eccentricity for one ideal rail pair: don't
    # assume reactions of two rails are equal. Show missing guide friction.
    g=7.88;e=hypot(12.,12.7);dm=2.5-.64952*.45;mu=.18
    for f in (15.,65.5,131.55):
        m=f*e;n=2*m/g;Q=f+.15*n
        torque=Q*((dm/2)*tan(atan(.45/(pi*dm))+atan(mu/cos(pi/6)))+.08*1.45)
        print('face F, screw offset/moment, guide normal sum, demand N, screw Nmm, gearmotor Nmm at worm 22:3,.65',f,e,m,n,Q,torque,torque/((22/3)*.65))
    # Input offset of screw from effective friction line needs its own bound.
    ratio=5.70/1.8*5.90/1.8;v=5670/(531441/2401)
    for F in [5.,121.]:
        drag=.23*F*(1+2*12.90/(16.80-12.90));rack=drag+.23*F
        print('rack unloaded/full transverse F, drag incl eye term, pinion/gearhead Nmm before other losses',F,rack,rack*2.4,rack*2.4/(ratio*.80))
    print('rates using previous 221:1 comparator only; full Z sec, full X min',DZ/(v/ratio*2*pi*2.4)*60,(STROKE-REL)/(.45*v/(22/3)))
if __name__=='__main__':actual();beam();tines();drives()
