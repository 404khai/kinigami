"""Take 41: deterministic rigid geometry, Coulomb cones and elastic beam screens."""
from math import acos, asin, atan, cos, degrees, hypot, pi, radians, sin, sqrt

R,r,p,h,mu = 6.5,2.70,1.75,1.85,.23
S,xp,xb,xe,bw = r+p,12.95,4.53,9.75,3.8
zr,span = 12.55,2.55
E,I = 205000.,pi*p**4/4


def show(tag,*val):
    print(tag+':', ' '.join(f'{v:.6f}' for v in val))


def g(d,v=1.,err=1.):
    a=min(pi,acos(max(-1,min(1,d/v)))+radians(err))
    return cos(a)-mu*sin(a) if a<pi-atan(mu) else -hypot(1,mu)


def local():
    A=pi/4
    lat=A-asin(h*cos(A)/r)
    rho=h+r*sin(A)
    dz=sqrt(S*S-rho*rho)
    th=radians(5)
    pc=(dz-2*R*sin(th))/S
    show('one contact angle R5/R6.5',degrees(acos(sqrt(3.95/5))),degrees(acos(sqrt(S/R))))
    show('flat/shank or flatter cap common work',g(cos(3*pi/8)))
    show('lip rho,dz,down latitude; wall and cap down work at tilt<=5 deg',
         rho,dz,degrees(lat),g(sin(lat)),g(pc))
    show('nominal parked apex required, reserve at 10.15, total travel',
         xp-xb+p*(sqrt(2)-1)+.2*sqrt(2),10.15-(xp-xb+p*(sqrt(2)-1)+.2*sqrt(2)),16.15)
    assert pc>mu/hypot(1,mu) and g(pc)>.03


def monitored(off,tilt,vx):
    # Bounds on the actual geometry; normal error is separate from shaft tilt.
    s,c=sin(radians(3)),cos(radians(3))
    dmin,dmax=15-.20-xp-off,15+.20-xp+off
    D=hypot(dmax,.50+off)
    du=s*(s*D+R*s+S)
    a=dmin-du
    ux=c*a/hypot(a,.50+off+du)
    pinx=(R*ux-dmax)/S
    rear=xe-(15-.20-R)
    u=sqrt(r*r-rear*rear)
    cz=xe-xb-u+R*s
    down=(u-2*R*s)/r
    wall=g(down-vx*sqrt(1-down*down),hypot(1,vx))
    pin=g(vx*pinx-sin(radians(tilt)),hypot(1,vx))
    show('offset,beta,translation slope; Cz, wall down, pin aft, wall/pin work',
         off,tilt,vx,cz,down,pinx,wall,pin)
    assert wall>0 and pin>0 and .5+R*s*s/c<bw
    return min(wall,pin)


def corner():
    rho=hypot(15-xe,bw);diff=R-rho
    z=xe-xb-sqrt(r*r-diff*diff)
    nx=(xe-15)*diff/(rho*r)
    show('actual aligned first roof edge: Cz,nx, x work nominal',z,nx,g(nx,err=0))
    assert nx<0 and rho<R


def mixed():
    th,t=pi/4,radians(55)
    c,s=cos(th),sin(th)
    k=hypot(sin(t)/c,cos(t))
    x=R*c*sin(t)-S*sin(t)/(c*k)
    y=R*cos(t)-S*cos(t)/k
    z1=R*s*sin(t)
    def near(z):
        d=x*c+z*s; w=hypot(y,d)
        v=(R*c*d/w-x,R*y/w-y,R*s*d/w-z)
        der=z-R*s*d/w
        return hypot(*v)-S,tuple(i/S for i in v),der,1-R*s*s*y*y/w**3
    lo,hi=-1.54,-1.51
    assert near(lo)[0]<0<near(hi)[0]
    for _ in range(60):
        z=(hi+lo)/2
        if near(z)[0]<0:lo=z
        else:hi=z
    z2=hi
    Cx,Cy=xp-x,-y
    # Plane normal anti-parallel to eye axis: continuum of wall tangencies.
    Cz=Cx-xb-sqrt(2)*r
    qx=Cx+R*c-r/sqrt(2)
    assert xe<qx<18.60 and abs(Cy)<bw and hypot(qx-xp,Cy)>h
    n1,n2=near(z1)[1],near(z2)[1]
    assert abs(near(z1)[0])<1e-10 and abs(near(z1)[2])<1e-10 and near(z1)[3]>0 and near(z2)[2]>0
    show('mixed C,x y z; face interior point x y z',Cx,Cy,Cz,qx,Cy,qx-xb)
    show('mixed generator z1,z2, nose apex',Cz+z1,Cz+z2,Cz+z2-p)
    show('mixed pin normals',*n1,*n2)
    coeff=[g(n[1]-.65*n[2],hypot(1,.65)) for n in (n1,n2,(1/sqrt(2),0,-1/sqrt(2)))]
    show('mixed work: shank, cap, wall',*coeff)
    assert min(coeff)>.1
    return [(zr-(Cz+z1),n1[2]),(zr-(Cz+z2),n2[2])]


def stress(pts):
    F=121.
    for L in (12.,zr):
        show('L, centred 121 N bending MPa, displacement, slope deg',L,F*L*p/I,
             F*L**3/(3*E*I),degrees(F*L**2/(2*E*I)))
    def debit(L,nz,H):
        perc=sqrt(max(0,1-nz*nz))
        arm=sqrt(L*L+p*p-2*L*p*nz)
        bm=L*perc+mu*arm
        delta=((perc+mu)*L*L*(3*H-L)/6+p*mu*L*(2*H-L)/2)/(E*I)
        return bm*p/I,delta
    H=max(q[0] for q in pts)
    ds=[debit(L,nz,H) for L,nz in pts]
    for (L,nz),(stress,defl) in zip(pts,ds):
        show('mixed L,nz,one-sided stress & at far generator if total N<=121',
             L,nz,F*stress,F*defl)
    # Short pin including deepest nose centre when still loaded.
    L=zr+4.25
    show('all stroke L, rough MPa/deflection if total N<=121',
         L,F*(L*hypot(1,mu)+p*mu)*p/I,
         F*(hypot(1,mu)*L**3/3+p*mu*L**2/2)/(E*I))
    for eye_drag in (0.,mu):
        Nf=F*(zr-p*mu+p*eye_drag)/span
        J=F+2*Nf
        show('eye drag factor, far normal, near normal, journal+eye draw',
             eye_drag,Nf,F+Nf,mu*J+eye_drag*F)
    show('centre load port x+, z, free-clamp forward deflection there, N for .10',
         xp+h,xp+h-xb,(dp:=F*(zr-(xp+h-xb))**2*(3*zr-(zr-(xp+h-xb)))/(6*E*I)),F*.10/dp)


def far():
    for rr,pp,xx,base in ((5.,1.25,15.,6.03),(6.5,1.75,xp,xb)):
        rad=r+pp
        qx=xx-(rad+r)/sqrt(2);qz=base-qx
        ztip=qz+(rad+r)/sqrt(2)
        show('far-face antipode R,p; qx,qz,Cx,Cz,apex',rr,pp,qx,qz,
             xx+rr-rad/sqrt(2),ztip-rad/sqrt(2),ztip-pp)


if __name__=='__main__':
    local()
    monitored(0,0,.37)
    monitored(.08,.60,.38)
    corner()
    pts=mixed()
    stress(pts)
    far()
