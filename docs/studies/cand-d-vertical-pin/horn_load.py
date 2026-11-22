"""Registered-pressure and loaded bearing screens for the curved horn."""
from math import acos, atan, cos, degrees, hypot, pi, radians, sin, sqrt, tan
import numpy as np
from horn import Horn,ring
from button_seats import test
from slotted import hertz


def pressure(h,hi,exy=.045,ez=.060,eye_angle_deg=1.):
    """Enclose every smooth contact of the torus with the polar-disk surface.

    Coordinates on grid cells only; debit the full unsampled range in
    both directions. Tolerance inputs are targets for a loaded assembly.
    """
    # Uniform position/normal profile errors, not dimensional tolerances
    # assigned independently and then silently assumed to give these errors.
    form=.030; da=radians(.40); angle=radians(eye_angle_deg)
    ring_error=.030; tube_error=.030
    # Actual eye datum relative to horn frame, not an externally held fixture.
    m,n=681,1441
    ts=np.linspace(h.lo,hi,m);vs=np.linspace(-pi,pi,n)[None,:]
    dt=(ts[1]-ts[0])/2; dv=pi/(n-1)
    fmax=h.width(hi); rmax=h.rc+fmax; rmin=h.rc-fmax
    fp=h.rate*rmax
    pos=dt*hypot(rmax,fp)+dv*fmax+form
    # Outward normal = (cos(v)e_r+sin(v)e_y - k*e_theta)/hypot(1,k).
    # Normalisation has operator norm <=1 on this family. Rotating the
    # local frame costs <= |dt|. Bound derivatives of k=f'/r separately.
    kt=h.rate*fp/rmin+(fp/rmin)**2
    kv=fp*fmax/rmin**2
    dn=dt*(1+kt)+dv*(1+kv)+2*sin(da/2)
    pcerr=pos+(4.2+tube_error)*dn+tube_error
    max_ang=max_disp=0.; low=hi; upper=h.lo
    e=np.array([cos(h.beta),0.,sin(h.beta)])
    q=np.array([7.5+4.2*e[0],0.,h.oz])
    for t in np.array_split(ts,24):
        t=t[:,None];f=h.width(t);r=h.rc+f*np.cos(vs)
        k=h.rate*(h.rc+f)/r;w=np.hypot(1,k)
        A=(np.cos(vs)*np.cos(t)+k*np.sin(t))/w
        B=np.sin(vs)/w
        D=(np.cos(vs)*np.sin(t)-k*np.cos(t))/w
        x=h.ox+r*np.cos(t);y=f*np.sin(vs);z=h.oz+r*np.sin(t)
        gx=x+4.2*A-15;gy=y+4.2*B;gz=z+4.2*D
        rad=np.hypot(np.hypot(gx,gy),gz)
        ok=(abs(rad-7.5)<=pcerr+hypot(exy,ez)+ring_error)
        ok&=abs(gz)<=pcerr+ez+(7.5+ring_error)*sin(angle)
        # n·(a cross u)=0 for a smooth contact of a generated torus ball;
        # use u=surface point-eye datum: the r*n offset cancels exactly.
        vx=x-15;vy=y;vz=z
        Hz=vx*B-vy*A;Hxy=np.hypot(vy*D-vz*B,vz*A-vx*D)
        err=pos+hypot(exy,ez)+(np.sqrt(vx*vx+vy*vy+vz*vz)+pos+hypot(exy,ez))*dn
        ok&=abs(Hz)*cos(angle)<=Hxy*sin(angle)+err
        if not np.any(ok):continue
        at=np.broadcast_to(t,ok.shape)[ok]
        low=min(low,min(at)-dt);upper=max(upper,max(at)+dt)
        max_ang=max(max_ang,degrees(np.arccos(np.clip((-A*e[0]-D*e[2])[ok],-1,1)).max()+2*np.arcsin(dn/2)))
        max_disp=max(max_disp,np.hypot(np.hypot(x-q[0],y),z-q[2])[ok].max()+pos)
    angles=np.linspace(0,2*pi,4097)
    endgap=min(np.min(h.dist(ring,angles,t)) for t in (h.lo,hi))-4.2
    endgap-=pi*7.5/(len(angles)-1)+form+tube_error+ring_error+hypot(exy,ez)+2*7.53*sin(angle/2)
    assert endgap>0
    return max_ang,max_disp,low,upper


def stresses(h,load):
    b=h.b;L=h.L;fp=h.rate*(h.rc+b);fpp=h.rate*fp;e=h.beta
    # Principal curvatures at theta=0,v=pi: meridian concave on horn,
    # across Y convex on horn and concave on torus. Reflection symmetry
    # in Y makes mixed curvature zero here.
    kk=-((L+fpp)*cos(e)+2*fp*sin(e))/(L*L+fp*fp)
    rr=(1/(1/4.2+kk),1/(cos(e)*(1/b-1/(7.5-4.2*cos(e)))))
    ab=hertz(load,*sorted(rr))
    return rr,ab


def bearing(h,hi,span=14.,jr=2.,tr=3.,mu=.005):
    # No arbitrary opposed thrust preload; one locating thrust pair and
    # one floating radial journal. Distributed contact summed by linearity.
    y=h.width(hi);R=h.rc+y
    # sum journal loads <= (1+2*y/span)*F_perp + 2R/span*|F_axial|.
    # Opposing radial reactions from a couple are included. One thrust face
    # carries axial load. Journal torque coefficients are assumptions.
    j=hypot(1+2*y/span,2*R/span)*hypot(1,h.mu)
    v=mu*hypot(jr*(1+2*y/span),jr*2*R/span+tr)*hypot(1,h.mu)
    return j,v,h.opening(hi)-v


if __name__=='__main__':
    for L,hi in ((18.,.54),(20.,.5)):
        h=Horn(L)
        ang,pos,lo,up=pressure(h,hi)
        print('L, smooth-pole angle / displacement and angular range:',L,
              np.round([ang,pos,lo,up],5))
        print('radial sum/N; bearing drag/normal; net Nmilli-m per N',
              np.round(bearing(h,hi),4))
        for mass in (70.,90.,110.):
            j=.001*mass*9.80665*(3*37.5+3*18.566)
            cfg=test(-90.,11.,6.,58.,ang,pos+.30,mass,(j,1.4*j))
            if cfg:
                print('mass, replacement joint service/fault, draws and trial Fx',
                      mass,round(j,1),round(j*1.4,1),np.round(cfg[1],1),
                      round(cfg[0]*(cos(h.beta)+tan(radians(ang)+atan(.23))*sin(h.beta))+5*.001*mass*9.80665,1))
        for load in (92.,150.,200.):
            rr,ab=stresses(h,load)
            print('nominal curvatures as radii, load, patch axes, pressure GPa',
                  np.round(rr,3),load,np.round(ab[:2],4),round(ab[-1]/1000,3))
