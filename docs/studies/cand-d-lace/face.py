"""Six axial-V seats with two tension-only lace legs. Exploratory, N and mm."""
from math import acos,asin,cos,degrees,exp,hypot,pi,radians,sin,sqrt,tan
from pathlib import Path
import sys
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'cand-d-crosspin'))
from registry import X,Y,Z,envelope


def setup(radius,angle,clock=0.):
    arms=np.array([cos(a+clock)*Y+sin(a+clock)*Z for a in (0,2*pi/3,4*pi/3)])
    points=np.repeat(radius*arms,2,axis=0)
    normals=np.array([cos(angle)*X+sg*sin(angle)*np.cross(X,l) for l in arms for sg in (-1,1)])
    J=np.column_stack([np.r_[n,np.cross(p,n)/radius] for p,n in zip(points,normals)])
    return points,normals,J


def budget(mass,radius,angle,ys,ratio,port_angle=3.,p=37.5,foot=20.65,x=-.5,clock=0.,crown_shift=0.):
    # All bending couples in this calculation are about the boss triangle's centre.
    _,_,J=setup(radius,radians(angle),radians(clock))
    H=np.linalg.inv(J);f,m=H[:,:3],H[:,3:]
    dn=2*sin(radians(.6)/2);dm=dn+(.19+abs(crown_shift)*dn)/radius
    assert np.linalg.svd(J,compute_uv=False)[-1]>sqrt(6)*hypot(dn,dm)
    k=tan(radians(port_angle))
    # Enclose any two axial fractions in [1/(1+kappa), kappa/(1+kappa)].
    # Lateral components may point independently. Sum of linearised force
    # and arm terms, divided by total axial force, is affine in the fractions.
    ends=[]
    for y in ys:
        d=np.array([x,y,0.])
        v=f+np.cross(m,d)/radius
        ends.append(v[:,0]-k*np.linalg.norm(v[:,1:],axis=1)
                    -.18*hypot(1,k)*np.linalg.norm(m,axis=1)/radius)
    lo=0. if np.isinf(ratio) else 1/(1+ratio)
    assert 0<=lo<=.5
    A,B=ends
    slope=np.minimum(lo*A+(1-lo)*B,(1-lo)*A+lo*B)
    loss=(np.linalg.norm(f,axis=1)*dn+np.linalg.norm(m,axis=1)*dm)/cos(radians(angle+.6))
    slope-=loss
    if min(slope)<=0:return np.full(3,np.inf)
    out=[]
    for case in ('service','table','fault'):
        w=envelope(mass,case,radius,wide='take23')
        tq=.001*mass*9.80665*3*(p+foot)*(1.4 if case=='fault' else 1)
        w[-1]+=(tq-(52.2 if case=='fault' else 14.5))/radius
        out.append(max((abs(H)@w+loss*w[0])/slope))
    return np.array(out)


def report():
    for a in (4.,6.,8.):
        for ratio in (1.,exp(.23*pi),np.inf):
            best=(np.inf,None)
            for y0 in np.linspace(-1.,4.,51):
                for ang in (40.,45.,50.,55.,60.):
                    ys=(y0-a,y0+a)
                    f=budget(70.,13.,ang,ys,ratio)
                    if max(f)<best[0]:best=(max(f),(y0,ang,*f))
            print('bend R/ratio, best y-offset/V-angle, service/table/fault N',a,ratio,
                  np.round(best[1],2) if best[1] else 'no certificate')


def compare():
    # A rocker balanced around an axial draw gives both ends finite travel.
    # p is the TOTAL differential length excursion allowed in either direction.
    p=304.8/93; s=6.; arm=s+p**2/(16*s); theta=asin(p/(2*arm))
    walk=arm-s
    # Sum of lateral and bearing moments, and a trial independent 1 N mm bias
    # above 35 N draw. y error of each pivot/anchor is included separately.
    k=tan(radians(3))
    h=(arm*sin(theta)*k+.23*1.2*hypot(1,k)+.10+1./35)/(arm*cos(theta))
    ratio=(1+h)/(1-h)
    print('equalizer arm/angle/walk/ratio/free span',np.round(
        [arm,degrees(theta),walk,ratio,(walk+.18)/k],3))
    print('R13 60deg y0=.5 U, total axial draw',
          np.round(budget(70,13,60,(-5.5,6.5),ratio),2))
    # Alternative: bring the ports together, sacrificing length in the
    # tail. Each inverse bend is tangent to the middle major arc.
    for a,off,alpha in ((2.,1.,62.),(6.,.5,60.)):
        R=6.; leg=3.5; th=acos((a+R)/(2*R))
        depth=leg+R*(1+2*sin(th)); length=2*leg+R*(pi+4*th)
        w=budget(70.,13.,alpha,(off-a,off+a),float('inf'))
        print('leg halfspan/centreline depth/length/all splits',np.round([a,depth,length,*w],2))


if __name__=='__main__':report();compare()
