"""A temporary pneumatic transfer chuck, NOT structural retention. N, mm, kPa.

Does not infer effective seal diameter, elastomer stiffness, uniform pressure,
leakage, or simultaneous contact from input motion. All numerical settings
except the reference gravity and ideal gas balance are design sensitivities.
"""
from itertools import product
from math import cos, hypot, pi, radians, sin, sqrt
from pathlib import Path
import sys

import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'cand-d-central-grasp'))
from seats import H, D, ANGERR, ALPHA, sphere_flat


def vacuum_wrench(ro, ri, edge, diff, spread):
    # In the FLAT plane of the passive seal land, actual wet boundary may
    # vary by +/-edge independently at every azimuth. Contact holes/ports
    # with a different pressure would have to be removed too. diff = middle
    # differential pressure; bound spread across face and sensor error.
    lo,hi=(pi*((ro-e)**2-(ri+e)**2) for e in (edge,-edge))
    # For a directional first moment, dual integral of cos(phi) over its
    # positive half-circle is 2. Choose worst outer AND inner boundary
    # independently on EACH half; not a concentricity assumption.
    dJ=2/3*((ro+edge)**3-(ro-edge)**3+(ri+edge)**3-(ri-edge)**3)
    # Nonuniform dp field relative to its nominal may have either sign.
    jabs=4/3*((ro+edge)**3-(ri-edge)**3)
    return lo*(diff-spread)/1000,hi*(diff+spread)/1000,(diff*dJ+spread*jabs)/1000


def margin(mass,R,Pside,Pmom,Pmin,Pmax,mode,axial=0):
    W=mass*9.80665/1000
    load=np.array([4*W+axial,W,W,25.4*W/R,50.8*W/R,(52.2 if mode=='fault' else 14.5)/R])
    if mode=='table':
        load+=np.array([W,0,0,W*(12.7+2.42)/R,W*(37.2-11.23)/R,W*hypot(50.8,25.4)/R])
    dl=.035/R+.15/R*(1+.035/R)
    # At first zero under a homotopy of the support normals, the other
    # five are nonnegative; use x equilibrium to bound their sum.
    sumN=(Pmax+load[0])/cos(ALPHA+ANGERR)
    loss=[]
    for d in H.T:
        loss.append(abs(d)@load+np.linalg.norm(d[1:3])*Pside+np.linalg.norm(d[3:])*Pmom/R
                    +(np.linalg.norm(d[:3])*D+np.linalg.norm(d[3:])*(dl+D))*sumN)
    return min(H.T[:,0]*Pmin-loss)


def test_seats(mass,rad,ro,ri,edge,dp,spread,seal,seal_m):
    L,U,M=vacuum_wrench(ro,ri,edge,dp,spread)
    # Tilt of force on tail land relative to nominal x plus centre shift
    # relative to triangle. Extra SEAL wrench is a required measured
    # envelope including pressure-induced lip edge tension, not a generic
    # rubber constant; soft film can transfer significant membrane tension.
    ang=.15/rad+radians(.2)
    side=U*sin(ang)+.23*seal
    couple=M+U*.08+abs(2*U*sin(ang))+seal_m
    return L,U,M,min(margin(mass,rad,side,couple,L*cos(ang),U,k,seal)
                      for k in ('fault','table'))


def isothermal_step(pc, chamber, swept, dead, ambient, crack, leak, period):
    # Perfect volumetric efficiency except stated gas clearance. At full
    # compression dead gas remains at the discharge pressure; the inlet
    # opens only if expanded cylinder pressure < chamber minus cracking.
    # leak in std cm3/min (reference 101.325 kPa at SAME temperature).
    vol=dead+swept
    if dead*(ambient+crack)/vol < pc-crack:
        pc=(pc*chamber+(ambient+crack)*dead+crack*vol)/(chamber+vol)
    return min(ambient,pc+101.325*1000/60*leak*period/chamber)


def pump(cv=190.,stroke=62.,dead=3.,ambient=100.,crack=2.,leak=.05,freq=6.):
    pc=ambient
    for n in range(1,241):
        pc=isothermal_step(pc,cv,stroke,dead,ambient,crack,leak,1/freq)
        if ambient-pc>=85:
            return n,n/freq,pc
    return None,None,pc


if __name__=='__main__':
    assert vacuum_wrench(12,6,0.,80.,0.)[2]==0
    for mass,dp in product((50,60,70),(75.,85.,93.)):
        print('g, dp, min/max pressure force, boundary moment, least N on a face',
              mass,dp,*[round(x,3) for x in test_seats(mass,9.25,12.75,5.90,.08,dp,.30,.75,3.)])
    for leak,hz in product((0,.05,.30,1.),(1,6)):
        print('leak (sccm), Hz, strokes/time/absolute kPa last',leak,hz,pump(leak=leak,freq=hz))
    # If the pump stops, the margin is a FINITE time, not a passive lock.
    for leak in (.05,.30,1.,10.):
        print('10kPa rise on 190 mm3, leak sccm/sec',leak,10*190/(101.325*1000/60*leak))
    # Maximum diameter of a coaxial pair of annular plates at working
    # radius, ignoring the stud and the rest of the package.
    print('two complete R13.25 rims x50.8 min enclosing diameter',hypot(50.8,26.5))
