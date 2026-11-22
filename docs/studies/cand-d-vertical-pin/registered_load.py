"""Conditional mass, contact and compliance screens for Take 51, mm / N."""
from itertools import product
from math import atan,cos,hypot,pi,radians,sin,sqrt,tan
import numpy as np
from scipy.spatial import ConvexHull
from backed_face import setup,test,Y,RADIUS,STATION,ANGLE
from horn import Horn
from horn_load import pressure,stresses
from horn_lock import upper,hertz
from register_joint import geometry,shorter_tail,D


def volumes(lo,hi,field,step=.8,levels=3):
    """Bracket volume by concentric ball tests on each cube, not centre counting."""
    x,y,z=[np.arange(a+step/2,b+step,step) for a,b in zip(lo,hi)]
    octants=np.array(list(product((-1,1),repeat=3)))
    def bound(v,h,i):
        f=field(v);delta=h*sqrt(3)/2+1.e-9
        inside=np.count_nonzero(f<=-delta)*h**3
        u=v[abs(f)<delta]
        if i==0:return np.array([inside,inside+len(u)*h**3])
        extra=np.zeros(2)
        for chunk in np.array_split(u,1+len(u)//800):
            vv=(chunk[:,None,:]+octants*h/4).reshape(-1,3)
            if len(vv):extra+=bound(vv,h/2,i-1)
        return inside+extra
    return bound(np.array(np.meshgrid(x,y,z,indexing='ij')).reshape(3,-1).T,step,levels)


def mass_screen():
    g,b,face=geometry();t=shorter_tail(g,b)
    # Same p translation as the two bodies' straight assembly. Exclude fork,
    # hinge, teeth and bores: the calculation is for rolling stock only.
    neck=[(np.array(v[0]),np.array(v[1])) for n,v,r,a in t if n.startswith(('heavy neck','heavy stem'))]
    def tail_field(v):
        f=np.hypot(np.hypot(v[:,0]+22.5,v[:,1])-7.50,v[:,2])-4.2
        for p,q in neck:
            d=q-p;u=np.clip((v-p)@d/(d@d),0,1)
            f=np.minimum(f,np.linalg.norm(v-p-u[:,None]*d,axis=1)-4.2)
        return f
    hu=[ConvexHull(v).equations for n,v,r,a in face]
    def head_field(v):
        return np.minimum.reduce([np.max(v@h[:,:3].T+h[:,3],axis=1) for h in hu])
    # All faces and generator-ball extrema lie strictly inside the boxes.
    for p,q in neck:
        assert np.all(np.minimum(p,q)-4.2>[-37,-23,-23])
        assert np.all(np.maximum(p,q)+4.2<[-6,23,23])
    assert all(np.all(np.min(v,axis=0)>[-1,-21,-21]) and np.all(np.max(v,axis=0)<[19,21,21]) for _,v,_,_ in face)
    tail=volumes((-37,-23,-23),(-6,23,23),tail_field)
    head=volumes((-1,-21,-21),(19,21,21),head_field)
    return .00781*tail,.00781*head


def flexibility(h,load):
    # Straight local section constitutive law along a curved centreline.
    # Tip pole, rigid clamp at t=.51. This trial beam is NOT an error bound
    # for a short root, contact patch, mounting arms or a heat-treated part.
    E,G=200000.,77000.;n=1600
    I=np.eye(3);q,c,e,_,_=setup(-90,RADIUS,STATION,ANGLE)
    cmp=np.zeros((3,3));rot=np.zeros_like(cmp);dt=.51/n;mx=0.
    for k in range(n):
        t=(k+.5)*dt
        r=h.width(t);A=pi*r*r;J=pi*r**4/4
        er=np.array([cos(t),0,sin(t)]);et=np.array([-sin(t),0,cos(t)])
        cur=np.array([h.ox,0,h.oz])+h.rc*er
        tt=np.outer(et,et);bb=I-tt
        H=bb/(E*J)+tt/(2*G*J);P=np.cross(q-cur,I).T;ds=h.rc*dt
        cmp+=ds*(P.T@H@P+(tt/E+1.15*bb/G)/A)
        rot+=ds*H@P
        mx=max(mx,np.linalg.norm(bb@P@load)*r/J+abs(et@load)/A)
    return cmp@load,rot@load*180/pi,mx


def run():
    tail,head=mass_screen()
    print('solid 7.81 mg/mm3: rolling tail, U-face, combined g',
          np.round(np.r_[tail,head,tail+head],2))
    h=Horn(18.)
    # Only previously allocated feet, not a verified three-unit COM.
    foot=hypot(12.30+3.50+D,9.75)
    q,c,e,b,n=setup(-90.,RADIUS,STATION,ANGLE)
    for exy,ez in ((.045,.060),(.10,.10)):
        ang,pos,*_=pressure(h,.54,exy,ez)
        for m in (70.,90.,110.):
            j=.001*m*9.80665*3*(37.5+foot)
            draw=test(-90.,RADIUS,STATION,ANGLE,ang,pos+.30,m,(j,1.4*j))
            Fx=draw[0]*(e[0]+tan(radians(ang)+atan(.23))*e[2])+5*.001*m*9.80665
            print('datum, mass, pole angle/pos, yaw service, required draw/X',
                  exy,ez,m,np.round([ang,pos,j,*draw[1],Fx],2))
            # Illustrative hard force cap, not a provision for one.
            cap=10*np.ceil((Fx+10)/10)
            ub=np.max([upper(cap,m,case,ang,pos+.30,37.5,RADIUS,STATION,foot)
                       for case in ('service','table','fault')],axis=0)
            land=hertz(max(ub[:6]),4.2,4.2)
            # P is a force component, convert to upper resultant for the
            # nominal curvature screen, not an allowable contact pressure.
            horn=stresses(h,ub[6]*hypot(1,tan(atan(.23)+radians(ang))))[1]
            print('trial Fx cap, worst one land, P, nominal Hertz land/horn GPa',
                  np.round([cap,max(ub[:6]),ub[6],land[-1]/1000,horn[-1]/1000],2))
    for sign in (-1,1):
        F=e+sign*.23*np.cross(e,Y);F*=111/F[0]
        J=np.column_stack([np.r_[v,np.cross(p-c,v)/RADIUS] for v,p in zip(n,b)])
        forces=np.linalg.solve(J,np.r_[F,np.cross(q-c,F)/RADIUS])
        assert min(forces)>0
        dp,dang,stress=flexibility(h,F)
        print('111 N X witness, min land, axle torque, tip travel mm, angle deg, fibre MPa',
              np.round([min(forces),18*F[2],np.linalg.norm(dp),np.linalg.norm(dang),stress],3))


if __name__=='__main__':run()
