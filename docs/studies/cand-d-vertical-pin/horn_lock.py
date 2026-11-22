"""Full local reactions and one driven stub, exploratory, N and mm."""
from math import atan, cos, degrees, hypot, pi, radians, sin, sqrt, tan
import numpy as np
from scipy.optimize import linprog
from button_seats import setup, envelope, X, Y
from horn_load import hertz


def moments(L,Fx,diam=3.,ell=7.30,G=79000):
    q,c,e,ps,ns=setup(-90.,11.,6.,58.)
    J=np.column_stack([np.r_[n,np.cross(p-c,n)/11] for p,n in zip(ps,ns)])
    t=np.cross(e,Y); out=[]
    for sg in (-1,1):
        F=e+sg*.23*t; F*=Fx/F[0]
        land=np.linalg.solve(J,np.r_[F,np.cross(q-c,F)/11])
        assert min(land)>0
        T=L*F[2]; dth=T*ell/(G*pi*diam**4/32)
        out.append([min(land),T,T/6.62399,degrees(dth),L*dth,16*T/(pi*diam**3)])
    return np.array(out)


def upper(Fx,mass,case,phi=5.62,dp=.81,pitch=37.5,rad=11.,sta=6.,foot_radius=18.566):
    # Independent finite sets of vertices generate outer cones, not inscribed
    # circles. Each vertex coefficient is a possible share of total normal;
    # no independence or equal sharing postulate is needed for inclusion.
    q,c,e,ps,ns=setup(-90.,rad,sta,58.)
    nfac=16;mu=.23;delta=2*sin(radians(.60)/2)
    w=envelope(mass,case,rad,wide='take23')
    torque=.001*mass*9.80665*(3*pitch+3*foot_radius)
    w[-1]+=(torque*(1.4 if case=='fault' else 1)-(52.2 if case=='fault' else 14.5))/rad
    w[3:]+=abs(np.cross(np.eye(3),15*X-c)).T@w[:3]/rad
    W=[]; err=[]; cap=[]; df=delta*hypot(1,mu)
    for label,(n,centre) in enumerate(zip([*ns,e],[*ps,q])):
        pole=centre-4.2*n if label<6 else centre
        damp=(pole-c)/rad; u=np.cross(n,Y);u/=np.linalg.norm(u);v=np.cross(n,u)
        ratio=(mu if label<6 else tan(atan(mu)+radians(phi)))/cos(pi/nfac)
        for i in range(nfac):
            a=2*pi*i/nfac
            F=n+ratio*(cos(a)*u+sin(a)*v)
            W.append((1 if label<6 else -1)*np.r_[F,np.cross(damp,F)])
            # A rotation through <=.6 deg maps the actual flat contact cone
            # into the nominal cone. Contact anywhere inside a .30 pressure
            # patch, plus centre, ball-radius and normal-direction errors.
            dm=np.linalg.norm(damp)*df+(.19+.03+4.23*delta+.30)*hypot(1,mu)/rad
            err.append([df]*3+[dm]*3 if label<6 else [0.]*3+[dp*hypot(1,ratio)/rad]*3)
            cap.append(F[0] if label==6 else 0.)
    W=np.array(W).T;err=np.array(err).T
    A=np.vstack((W-err,-W-err,cap));b=np.r_[w,w,Fx+w[0]]
    # To convert numerical LP outputs to verifiable upper bounds, bound sum
    # of all weights first by e-force balance, then pay any dual roundoff.
    pcap=(Fx+w[0])/(e[0]-ratio*e[2])
    allcap=pcap+(pcap+abs(e)@w[:3])/(cos(radians(58.6))-mu*sin(radians(58.6)))
    def dual(obj):
        d=linprog(-obj,A_ub=A,b_ub=b,bounds=(0,None),method='highs')
        assert d.success
        y=np.maximum(0,-d.ineqlin.marginals)
        return y@b+allcap*max(0,max(obj-y@A))+1e-6
    return [dual(np.repeat(np.eye(7)[i],nfac)) for i in range(7)]


if __name__=='__main__':
    for d in (3.,5.):
        S=moments(18.,163.,d)
        print('diam, min pad force, torque, closed roller, twist, pole arc, shaft shear:')
        print(d,np.round(S,3))
    for mass,Fx in ((70.,185.),(90.,235.)):
        boxes=[upper(Fx,mass,c) for c in ('service','table','fault')]
        U=np.max(boxes,axis=0);a,b,p=hertz(max(U[:6]),4.2,4.2)
        print('mass/Fx cap, six land upper bounds / P cap',mass,Fx,np.round(U,2))
        print('most loaded land: patch radius; peak GPa',round(a,4),round(p/1000,3))
