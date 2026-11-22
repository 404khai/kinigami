"""Exploratory incremental Hertz/elastic closure at a fixed integral top crown.

Assumed independent normal supports. This is not a model of the old free
ball race, of the screw/arm support structure, or of impacts in acquisition.
"""
from itertools import product
from math import atan, cos, pi, radians, sin, sqrt, tan
import numpy as np
from scipy.optimize import linprog
from vise import X,Y,envelope,seats,wrench

R=7.
K=39
I=np.eye(K)
P=I[24]


def hertz(force,radius):
    return (force/(4/3*115380*sqrt(radius)))**(2/3)


def tangent(n,r):
    h=hertz(n,r)
    return h/3,2*h/(3*n)


def model(mass,initial,limit,active,qt,theta,lower_c,top_c,dn=.009,reg=.015,
          drag=.23,corner='table',cross=0.):
    """Unknown reference indentation q0 is shared by the two load states.
    fc columns are axial projection and tangent components in a fixed set of
    axes. Upper/lower normal force bounds use the OUTER friction cone.
    """
    rows=[];rhs=[]
    def put(row,b):
        rows.append(row);rhs.append(b)
    faces=seats(R,radians(35),pi)
    q=I[:6]
    bounds=[(-qt,qt)]*3+[(-R*sin(theta),R*sin(theta))]*3
    bounds.extend([(0,None),(None,None),(None,None)]*7+[(0,None)]*6+[(None,None)]*6)
    W=np.zeros((6,K));err=np.zeros((6,K))
    load=envelope(mass,corner,R,'take23')
    # Rotate the componentwise service envelope into the paddle frame.
    tilt=dn+theta
    for off in (0,3):
        load[off:off+3]+=2*sin(tilt/2)*np.linalg.norm(load[off:off+3])
    p0lo,p0hi=initial
    # True normal/projection ratio at the nominal axes.
    nlo=1/(1+drag*sin(tilt))
    nhi=1/(cos(tilt)-drag*sin(tilt))
    mu=tan(atan(drag)+tilt)
    w=mass*.001*9.80665
    uy=cos(radians(35)+dn)-drag*sin(radians(35)+dn)
    # Reference is closed under the indicated central load, no external
    # vise wrench other than its own weight. q0[6] are TRUE normal forces.
    put(sum(I[27:33]),(p0hi*sqrt(1+drag**2)+w)/uy)
    # Clip at a closed boundary to be tested (not an inferred working load).
    put(P,limit)
    # Physical lower normal upper bound obtained from equilibrium in the
    # head Y direction, while physical top norm <=limit*nhi.
    lower_max=(limit*nhi*sqrt(1+drag**2)+np.linalg.norm(load[:3]))/uy
    for i,(ctr,n) in enumerate([*faces,(-4.5*Y,-Y)]):
        f,t,s=I[6+3*i:9+3*i]
        a=np.cross(n,X);a/=np.linalg.norm(a);b=np.cross(n,a)
        r=3. if i<6 else 8.
        pos=ctr-r*n
        for direction,variable in zip((n,a,b),(f,t,s)):
            W+=np.outer(wrench(pos,direction,R),variable)
        for j in range(24):
            ang=2*pi*j/24
            put(cos(ang)*t+sin(ang)*s-mu*f,0.)
        # Sphere's actual contact point is ctr-r*n_true. Enclose its
        # difference from the fixed moment pole, not a relocation of ctr.
        err[3:]+=(reg+r*2*sin(tilt/2))*sqrt(1+(mu/cos(pi/24))**2)/R*f
        J=wrench(ctr,n,R)@q
        c=lower_c if i<6 else top_c
        cmin,cmax=c
        if i<6:
            ref=I[27+i];d0=I[33+i];refmax=(p0hi*sqrt(1+drag**2)+w)/uy
            for nref in (1.,4.,12.,30.,60.,100.):
                ic,sl=tangent(nref,r)
                put(d0-(cmax+sl)*ref,ic)
            # An unloaded reference land may have up to .040 of air.
            put((cmin+hertz(refmax,r)/refmax)*ref-d0,.040)
            nmax=lower_max
        else:
            # q=0 is the as-closed reference, at a known force interval.
            # Actual top indentation (including series elasticity) is then
            # between these two absolute values.
            d0=0.*P
            top0lo=cmin*p0lo+hertz(p0lo,r)
            top0hi=cmax*p0hi+hertz(p0hi,r)
            nmax=limit*nhi
        # A common displacement increment bounds normal gauge error. A
        # rough pose band is only a starting enclosure for this trial.
        eb=2*sin(dn/2)*(sqrt(3)*qt+np.linalg.norm(ctr)*2*sin(theta/2))
        eb+=(np.linalg.norm(ctr)+reg)*(1-cos(theta))+reg*2*sin(theta/2)+cross
        if i==6 or active[i]:
            put((cmin+hertz(nmax,r)/nmax)*nlo*f-d0+J,eb+(top0hi if i==6 else 0))
            for nf in (1.,5.,15.,35.,75.,150.,300.,600.):
                ic,sl=tangent(nf,r)
                put(d0-J-(sl+cmax)*nhi*f,ic+eb-(top0lo if i==6 else 0))
        else:
            put(f,0)
            put(d0-J,eb)
    for j in range(6):
        put(W[j]-err[j],load[j]);put(-W[j]-err[j],load[j])
    # Upper contact remains engaged only on the checked compressive branch.
    return np.array(rows),np.array(rhs),bounds


def extrema(mass=70,initial=(45.,55.),limit=250.,qt=.12,theta=.035,
            lower_c=(.00002,.00006),top_c=(.00020,.00024),**kw):
    best=-1.;weak=None
    for active in product((False,True),repeat=6):
        if not any(active):continue
        A,b,bounds=model(mass,initial,limit,active,qt,theta,lower_c,top_c,**kw)
        sol=linprog(-P,A_ub=A,b_ub=b,bounds=bounds)
        if sol.status==2:continue
        assert sol.success and max(A@sol.x-b)<1e-6
        if -sol.fun>best:
            best=-sol.fun;weak=(active,sol.x[:6],sol.x[6:27:3])
    return best,weak


if __name__=='__main__':
    for tilt in (.01,.02,.035):
        val,who=extrema(theta=tilt)
        print('relative angle limit, upper projection N, most permissive active set',tilt,val,who)
