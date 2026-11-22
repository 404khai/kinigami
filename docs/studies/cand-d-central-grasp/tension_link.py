"""Tangent-beam discriminator for a central draw filament; N, mm, radians.

Euler--Bernoulli beam in tension P. A flexible wire does not transmit
only an axial force when clamps have a pose error. Not a finite-strain
certificate or an upper bound on a real cable's allowable working load.
"""
from itertools import product
from math import exp, pi, radians, sqrt

import numpy as np
from seats import need_pull


def influence(L, d, E, P):
    # y=a+b*x+c*exp(-kx)+f*exp(-k(L-x)); [y0,y1,theta0,theta1].
    I = pi*d**4/64
    k = sqrt(P/(E*I))
    h = exp(-k*L)
    bc = np.array([[1,0,1,h], [1,L,h,1], [0,1,-k,k*h], [0,1,-k*h,k]])
    _, b, c, f = np.linalg.inv(bc)
    return P*b, P*(c+h*f), P*(h*c+f)


def screen(L, d, rear, n=1, Rw=0.):
    # Here rear = positive distance from ball centre aft to front clamp.
    # Manufacturing offsets are net end-to-end ball-datum displacement,
    # plus independent clamp and cage tilts. Bounds are Euclidean norms
    # in the transverse plane; both axes use the same signed coefficients.
    # All are TRIAL metrology limits, including the cage attitude, NOT
    # consequences of the outer face's rigid-fit analysis.
    E, P = 205000., 45.
    V, M0, M1 = influence(L, d, E, P/n)
    pose = np.array([[0,0,0,0], [1,-rear,0,0], [0,0,1,0], [0,1,0,1]])
    err = np.array([.13,radians(1.),radians(.2),radians(.2)])
    def bound(a):
        return np.abs(a@pose)@err
    # Beam applies -V and -M1 on the front clamp. The triangle is 3.53
    # ahead of the ball, so its moment from transverse shear has opposite
    # sign to the end couple. Axial lever includes lateral translation.
    lever = 3.53+rear
    # y of the front clamp ABOUT THE MOVING TRIANGLE is -rear*theta_cage
    # minus the tilted triangle's own 3.53-mm arm. Do not charge absolute
    # ball translation once at each end of the external moment arm.
    mom = (-M1+lever*V)@pose + (P/n)*np.array([0,-rear,0,0])
    # For n independent wires on a ring (if proposed), tilting the end
    # spider changes extension. Charge a full unilateral worst increment;
    # without measured assembly tensions this is NOT a load-share proof.
    area=pi*d*d/4
    dforce=E*area*Rw/L*err[1]
    stretch=P/n/area/E*L
    side=n*bound(V)+.25
    couple=n*(abs(mom)@err+Rw*dforce)+.90+P*(.035+3.53*radians(1.37))
    torsion=n*(E/(2*(1+.30)))*(pi*d**4/32)/L*radians(2)
    couple+=torsion
    stress=(P/n+dforce)/area+32*max(bound(M1),bound(M0))/(pi*d**3)
    pmin=max(need_pull(side,couple,k) for k in ('service','table','fault'))
    return side,couple,stress,pmin,stretch


if __name__=='__main__':
    # Rigid lateral translation/straight rotation gives pure string
    # reaction and no bending. Test sign convention at both clamps.
    V,M0,M1=influence(12.,.4,205000.,45.)
    straight=np.array([.1,.34,.02,.02])
    assert abs(V@straight-.9)<1e-9 and max(abs(M0@straight),abs(M1@straight))<1e-9
    for L,rear in product((10.,14.,18.),(1.,3.,5.)):
        print('L, aft clamp offset, sum lateral / face couple / peak nominal MPa / needed draw / wire extension',
              L,rear,*[round(i,3) for i in screen(L,.40,rear)])
