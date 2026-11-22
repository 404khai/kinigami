"""Exploratory. mm, N, N mm. Use no face forces from an earlier mechanism."""
from math import acos, atan, cos, degrees, hypot, pi, radians, sin, sqrt, tan
from pathlib import Path
import sys

import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'cand-d-lace'))
from face import X, Y, Z, envelope, setup


A, B, K = 12.63, 14.50, .28
RIM, BACK, CX = 10.75, 2.50, -2.25
RR, OFFSET = 8.40, 1.36
HEIGHT, STATION, ANGLE = 1.48, 2.18, 45.
CLOCK = -90.
BC = CX-OFFSET
HOME = BC - (HEIGHT - STATION*tan(radians(ANGLE)) + BACK/cos(radians(ANGLE)))
PARK = 1.05


def section():
    a = radians(ANGLE)
    body_gap = CX-BACK-(HOME+HEIGHT)
    pole = STATION-BACK*sin(a)
    print('home / stroke / nominal home edge gap / puck-to-bore normal clearance',
          np.round([HOME, PARK-HOME,B+K*HOME-A,
                    (B+K*CX-RIM)/hypot(1,K)-BACK],5))
    print('button to base / belly to peak / pole to peak / pole height / '
          'outermost cone base radius',np.round([BC-BACK-HOME,body_gap,pole,
          HEIGHT-pole*tan(a),hypot(RR,STATION)+HEIGHT/tan(a)],5))
    # A finite cylinder of full disk radius behind the plate is NOT admissible
    # in this continuously flared bore. Trial conical rear stock instead.
    print('home max full-R axial thickness before collision',
          round((B+K*HOME-A)/K,5))


def seam(gap, rho, p_min, p_max, mu=.23, err=.6):
    assert 0 < gap < rho and 0 < p_min <= p_max < rho
    s=sqrt(1-(gap/rho)**2)
    nx=min(s,1-p_max/rho)
    def work(c):
        a=acos(c)+radians(err)
        return cos(a)-mu*sin(a)
    slope=sin(atan(K))
    return p_min-rho*(1-s), nx, work(nx), work(slope),work(cos(radians(ANGLE)))


def eject(mass, c, Fextra=0., guide=.23):
    # Applies AFTER all jaws have parked and only specified surfaces can touch.
    # Sum of all axial forces on tail balances external Fx; fixed faces assist.
    f=5*.001*mass*9.80665+Fextra
    N=f/c
    side=sqrt(1+.23**2-c*c)*N
    # Two transverse supports, equal-and-opposite torsion key couple, central
    # thrust; a fixture bound on summed guide drag, not a bushing force rating.
    L, arm, key=7.,14.,9.
    moment=A*f+arm*side
    rails=side+2*moment/L+A*side/key
    return [f,N,side,rails, f+guide*rails+.7]


def preload(angle, qx, mu, scatter, jaw_phase, radius=RR, button_x=BC):
    """N per clamp pole, positive frictionless solution on six nominal seats.

    Clamp traction and clamp normal scatter are independent; no equal sharing.
    Nominal setup plus actual lever/normal allowances by first loss of positivity.
    """
    _,_,J=setup(radius,radians(angle),radians(CLOCK))
    H=np.linalg.inv(J); f,m=H[:,:3],H[:,3:]
    dn=2*sin(radians(.6)/2)
    dm=dn+.19/radius
    if np.linalg.svd(J,compute_uv=False)[-1]<=sqrt(6)*hypot(dn,dm):
        raise ValueError('singular uncertainty set')
    loss=(np.linalg.norm(f,axis=1)*dn+np.linalg.norm(m,axis=1)*dm)/cos(radians(angle+.6))
    qr=sqrt(1-qx*qx); weights=[]
    for j in range(3):
        p=radians(CLOCK+jaw_phase)+j*2*pi/3
        rad=cos(p)*Y+sin(p)*Z
        q=qx*X+qr*rad
        d=(CX+BACK*qx-button_x)*X+(RIM+BACK*qr)*rad
        v=f+np.cross(m,d)/radius
        vq=v@q
        w=vq-mu*np.linalg.norm(v-vq[:,None]*q,axis=1)
        w-=np.linalg.norm(v,axis=1)*dn*(1+mu)+.19*hypot(1,mu)*np.linalg.norm(m,axis=1)/radius
        # Worst clamp axial component available to generate additional uncertain
        # seat loads; at initial loss all six reactions are still non-negative.
        w-=loss*(qx+mu*qr+dn*(1+mu))
        weights.append(w)
    weights=np.array(weights)
    margin=(weights-scatter*abs(weights)).sum(axis=0)
    if min(margin)<=0:return np.full(3,np.inf)
    out=[]
    for case in ('service','table','fault'):
        w=envelope(70.,case,radius,wide='take23')
        tq=.070*9.80665*3*(38+20.65)*(1.4 if case=='fault' else 1)
        w[-1]+=(tq-(52.2 if case=='fault' else 14.5))/radius
        out.append(max((abs(H)@w+loss*w[0])/margin))
    return np.array(out)


def finite_pole(N):
    from edge_hertz import hertz
    a=radians(ANGLE)
    pole=STATION-BACK*sin(a)
    # On the side of a cone the circumferential principal curvature is sin(a)/pole.
    return (hertz(N,1/(1/BACK+sin(a)/pole),BACK),hertz(N,BACK,BACK))


def check_gap():
    # Sample the sharp convex rim on an actual swept-sphere contact. At y=0
    # by axial symmetry the candidate centre is (p+rho*cos(t), A+rho*sin(t)).
    # The analytic proof, not this sampling, covers intermediate states.
    rho=BACK-.05
    gap=B-A+.05
    p0,p1=1.,1.10
    g=seam(gap,rho,p0,p1)
    for p in np.linspace(HOME,p1,121):
        for t in np.linspace(0.,pi/2,201):
            x=p+rho*cos(t); h=rho*sin(t)
            if x<0:continue # h>=0 and gap<rho: cannot enter from bore side.
            if hypot(x,max(gap-h,0.))>=rho:
                assert cos(t)+1e-12>=g[1]
    for d in np.linspace(0.,gap,81):
        # At terminal a sphere touching disk cannot have a smaller X at this
        # centre radius even where the stationary lip does not support it.
        assert p0+sqrt(rho*rho-d*d)-rho >= g[0]-1e-12


if __name__=='__main__':
    check_gap()
    section()
    # Nominal bore/plate/lip plus .05 all-in transverse gap growth; -.05
    # rolling-ball radius, plus/minus .05 actual travel relative to fixed lip.
    g=seam(B-A+.05,BACK-.05,PARK-.05,PARK+.05)
    print('terminal lift for centres in mouth / rim nx / rim, wall, seat '
          'work per N',np.round(g,5))
    print('70g max axial resistance / piston N / lateral / guide normals / drive N',
          np.round(eject(70,min(g[2],g[4])),4))
    print('conditional *all* normals in static balance after jaw park, N',
          round(5*.07*9.80665/min(g[2:]),3))
    for phase in (0.,60.):
        for q,mu,spread in ((.38/hypot(1,.38),0.,.10),(.38/hypot(1,.38),.23,.10),(.90,.23,.10),(.90,.05,.05)):
            print('phase / jaw nx / mu / fractional scatter / per-pole nominal '
                  'service,table,fault:',phase,q,mu,spread,
                  np.round(preload(ANGLE,q,mu,spread,phase),2))
    # A pressure sensitivity, not an actual bound on the heaviest locked pole.
    print('100 N one pole: R2.5 on cone vs tangent flat; (a,b mm,p0 MPa)',
          np.round(finite_pole(100),4))
