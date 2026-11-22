"""Take 48 installation. L18/p37.5. Positive-capture grooved rotary actuator."""
from pathlib import Path
from runpy import run_path
g=run_path(str(Path(__file__).with_name('horn-core-take48.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
L=18.;k=0.;P=37.5;O48=axis(L,k);pk=pars(L)[4];C48=(-2.25,11.15);M48=(-11.0,12.0)
def tail48(p=P,k=0):
    a=[s for s in tailshift(p,k) if not s[0].startswith(('metal neck','main stem'))]
    def pt(q):return plus(q,(-p,0,k))
    for j,b in enumerate(BOSS):
        line=[b,(22.5,0.,0.)] if j==0 else [b,(16.5,b[1],b[2]),(16.5,b[1],0.),(16.5,copysign(sqrt(54),b[1]),0.)]
        for i,(a0,b0) in enumerate(zip(line,line[1:])):a.append(cap('heavy neck'+str((j,i)),pt(a0),pt(b0),4.2))
    return a+[cap('heavy stem',pt((22.5,0.,0.)),pt((26.,0.,0.)),4.2)]
def sh(n,lo,hi,c,r):return cyl(n,Y,(lo,hi),c,r)
def joint48():
    a=[]
    for s in tucked_joint():
        n=s[0]
        if n in ('gear plate return','bridge tang'):continue
        if n.startswith(('yaw ','quill nose','saddle spur','bracket return','bracket foot')):
            s=move(s,(J[0]-J2[0],J[1]-J2[1],0))
        a.append(s)
    return a+[box('compound bridge fin',(-4.65,-2.35),(14.75,18.15),(-6.95,-5.65)),
              box('compound bridge post',(-4.65,-2.35),(17.65,19.15),(-15.60,-5.65)),
              box('outboard bottom plate',(-4.85,4.9),(13.7,18.75),(-15.75,-14.55))]
def fork(phi=0,end=None):
    a=[s for s in pivot(L,k,True,phi,end) if not s[0].startswith('spoke')]
    for sg in (-1,1):
        st=[(0,7.9*sg,1.20,-1.20,1.30),(6.80,6.87*sg,.95,-1.10,1.30),
            (10.00,3.92*sg,1.05,-.85,1.65),(12.3,2.65*sg,.95,-.45,1.65),(14.25,2.65*sg,.95,-.40,1.65),
            (18.9,2.0*sg,1.2,-.55,1.40)]
        a+=sang(L,k,'spoke'+str(sg),st,phi,end)
    return a
def cheeks():
    a=house(L,k);x,_,z=O48
    for sg in (-1,1):
        def yy(lo,hi):return tuple(sorted((sg*lo,sg*hi)))
        if sg>0:a.append(box('upper bridge cheek post',(-3.15,-1.45),(13.60,15.10),(-5.85,2.40)))
        else:a.append(box('hinge cheek tie',(-3.05,-1.35),(-11.45,-3.95),(-.85,.85)))
    return a
def rise(th):
    # 25-degree closed dwell for interlocked X relief, closed groove both flanks.
    u=min(1.,max(0.,(th-radians(25))/radians(132)))
    return pk*(u-sin(2*pi*u)/(2*pi))
def polar(v,th):return (v[0]*cos(th)-v[1]*sin(th),v[0]*sin(th)+v[1]*cos(th))
def pinpt(ph):
    return O48[0]+6.85*cos(ph),O48[2]+6.85*sin(ph)
def path(th):
    x,z=pinpt(rise(th));return polar((x-C48[0],z-C48[1]),-th)
def camstock(theta=0):
    # Sample the analytic pitch path in the cam's own frame. Use both
    # normal offsets for the groove, not a radial slot of variable width.
    # Blended endcaps extend into terminal dwells; separate hard stops.
    rows=[]
    for a in np.linspace(-3.,183.,125):
        th=radians(a);q=np.array(path(th));t0=np.array(path(th+1e-5))-np.array(path(th-1e-5));t0/=np.linalg.norm(t0);n=np.array((t0[1],-t0[0]))
        if n@q<0:n=-n
        def w(h):
            u=polar(q+h*n,theta);return (C48[0]+u[0],C48[1]+u[1])
        rows.append([C48,w(-2.31),w(2.31),w(3.36)])
    out=[]
    for i,(a,b) in enumerate(zip(rows,rows[1:])):
        for name,k0,k1,y0,y1 in [('rear web',0,3,22.45,23.6),('inner flank',0,1,19.35,22.45),('outer flank',2,3,19.35,22.45)]:
            out.append(poly(name+str(i),[(r[j][0],-y,r[j][1]) for r,j,y in product((a,b),(k0,k1),(y0,y1))],.006))
    return out
def idler():
    d=hypot(*sub(C48,M48));u=unit(sub(C48,M48));h=sqrt(7.2**2-(d/2)**2)
    return tuple((x+y)/2+t*h for x,y,t in zip(M48,C48,(-u[1],u[0])))
IC=idler()
def flip(s):
    n,v,r,a=s
    return (n,tuple((x,-y,z) for x,y,z in v),r,(a[0],-a[1],a[2]) if a is not None else None)
def drive():
    S=[sh('horn gearmotor',-12.10,16.60,M48,3.),sh('horn saddle',-8.6,-6.6,M48,3.70),
       sh('horn motor quill',16.40,21.25,M48,.95),sh('horn motor 18T',16.95,18.95,M48,2.00),
       sh('motor nose bush',19.25,21.3,M48,1.6),sh('compound wheel 54T',16.95,18.95,IC,5.60),
       sh('compound axle',12.15,21.4,IC,1.20),sh('compound pinion 18T',14.40,16.40,IC,2.00),
       sh('cam gear 54T',14.40,16.40,C48,5.60),sh('cam shaft',10.30,25.30,C48,1.80),
       sh('cam near bush',10.35,12.45,C48,3.15),sh('cam far bush',23.95,25.30,C48,3.15),
       sh('compound inner bush',11.75,14.05,IC,2.20),sh('compound outer bush',19.25,21.4,IC,2.20)]
    # Cam outer enclosure; working groove void is NOT claimed to be material.
    # A full rear web carries the grooved plate. Direct inertia and cover not ignored.
    outer=max(hypot(*path(radians(i))) for i in range(181))+3.36
    S.extend([sh('cam solid rear web',22.45,23.60,C48,outer),
              sh('grooved cam envelope',19.35,22.45,C48,outer),
              sh('horn output hub',16.40,19.05,(O48[0],O48[2]),2.6),
              box('outer carrier tie',(M48[0]-1.45,M48[0]+1.45),(19.25,21.30),(M48[1]-1.,M48[1]+2.5)),
              box('motor saddle support',(M48[0]-1.7,M48[0]+.1),(-9.25,-6.45),(M48[1]-3.6,M48[1]-.4)),
              box('cam backplate',(C48[0]-1.6,C48[0]+1.6),(10.35,12.55),(5.8,12.35))])
    return [flip(s) for s in S]
def lever(phi=0,end=None):
    # Arm lies beyond drum, follower projects inward, shaft extends through cheek.
    end=phi if end is None else end;M=max(1,ceil((end-phi)/.065));out=[]
    for i in range(M):
        h=phi+(end-phi)*i/M;j=phi+(end-phi)*(i+1)/M
        pts=[point(L,k,p,r,y,dy) for p,r,y,dy in product((h,j),(0,6.85),(16.70,19.05),(-1.70,1.70))]
        out.append(poly('lever'+str(i),pts,7.2*(1-cos((j-h)/2))))
        for name,y1,y2,rad in [('follower',19.65,22.15,2.25),('follower pin',16.70,22.30,1.30)]:
            s=sh(name+str(i),y1,y2,pinpt(h),rad);v=pinpt(j);w=pinpt(h);out.append(sweep(s,(v[0]-w[0],0,v[1]-w[1])))
    return [flip(s) for s in out]
def camcalc():
    xy=[];m=[]
    for d in np.linspace(0,180,901):
        th=radians(d);dt=1e-5;ph=rise(th);p=np.array(path(th));v=(np.array(path(th+dt))-np.array(path(th-dt)))/(2*dt);a=(np.array(path(th+dt))+np.array(path(th-dt))-2*p)/dt**2
        tang=v/np.linalg.norm(v);no=np.array((-tang[1],tang[0]));nx,nz=polar(no,th);arm=6.85*abs(nz*cos(ph)-nx*sin(ph));tin=abs(p[0]*no[1]-p[1]*no[0])
        cur=abs(v[0]*a[1]-v[1]*a[0])/np.linalg.norm(v)**3
        m.append((arm,tin,1/cur if cur else inf,hypot(*p)));xy.append(p)
    ar=np.array(m);print('cam axis, motor, compound, ratio, radii, min rolling curve radius',C48,M48,IC,9.,ar[:,3].min(),ar[:,3].max(),ar[:,2].min())
    print('min output moment arm, greatest torque ratio input/output, closed arm',ar[:,0].min(),max(ar[:,1]/ar[:,0]),ar[0,0])
    for F in (76,155,163,200):
        T=F*.32*18;print('face X wedge example, torque, closed roller normal, worst resisting motor torque (.80 external eff)',F,T,T/ar[0,0],T*max(ar[:,1]/ar[:,0])/(9*.8))
def stages48():
    return [('C',horn(L,k)+fork()+lever(),[sweep(mx(s,REL),(1.5,0,0)) for s in face3()]),
            ('W',horn(L,k,0,pk)+fork(0,pk)+lever(0,pk),[mx(s,REL) for s in face3()]),
            ('E',horn(L,k,pk)+fork(pk)+lever(pk),fp(face3()))]
def run():
    camcalc();j=joint48();bh=bearingproxy(L,k)+cheeks()[72:]
    for n,h,f in stages48():
        print(n,'horn and spokes v face',fastpair(h,f)[:3],'cheek v face',fastpair(bh,f)[:2])
        print(n,'horn/joint',fastpair(h,j)[:3],'horn/tail',ytest(h,tail48(P,k),1)[:2])
    for tag,A in [('bearing carriers',cheeks()),('full drive',drive())]:
        print(tag,'joint',fastpair(A,j)[:5],'face',fastpair(A,fp(face3()))[:3],'tail',ytest(A,tail48(P,k),1)[:3])
    print('joint tail',ytest([s for s in j if s[0] not in ('hinge pin','compound output 18T')],tail48(P,k),1)[:3])
if __name__=='__main__':run()
