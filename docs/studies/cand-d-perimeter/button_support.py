"""Take 65, exploratory. Correlated .48 leaf, finite seats, individual tail buttons."""
from math import acos, cos, degrees, hypot, pi, radians, sin, sqrt
import numpy as np
from fixed_face import BACK, BC, DELTA, MU, POS, faces, reactions
from edge_hertz import hertz
from tail_buttons import bound

Q, PH, ANG = .48, 60., 65.
CASES = ('service','table','fault')


def plunger():
    # KIPP K2396.206 drawing: uncompressed axial projection H is also stroke.
    H, F1, F2 = 1.50, 22., 40.
    h=BACK*(1-cos(radians(ANG)))
    move=H-h
    print('minimum exposed cap / max compression before pole hidden / linear-spring force there',
          np.round([h,move,F1+(F2-F1)*move/H],4))
    print('36 N interpolation: exposed cap / accessible angle',
          H*(F2-36)/(F2-F1),degrees(acos(1-H*(F2-36)/((F2-F1)*BACK))))
    # Uncompressed body envelope against the insert at t=2.96 (r local=0).
    # Not proof of occupation of unspecified internal cartridge material.
    hx=BC-BACK+H
    print('uncompressed rim end x / difference from insert cap x at t=2.96',
          hx,hx-(-5.0))
    assert hx< -5.0 and move<.06


def linear():
    for a in (60.,65.):
        print('required nominal with 10% scatter at jaw .48, seat angle',a,
              np.round([bound(Q,PH,.10,c,angle=a) for c in CASES],4))
    margin=faces(ANG)
    for k in (0.,.015,.05,.10,.15,.21):
        upper=reactions(mu=MU,guide=k,lo=32.4,hi=39.6,angle=ANG,qx=Q,phase=PH,tail_springs=True)
        print('guide drag coefficient / seat,jaw LP upper estimates',k,np.round(upper,3))
        F=upper[:,0].max()
        if np.isfinite(F):
            a,b,p=hertz(F,BACK,BACK)
            print('one steel ball on flat: patch radius / peak GPa / margin after location and patch',
                  np.round([a,p/1000,margin-POS-a],4))
    # Analytic, separate from LP: pair of forces pushing on individual slider.
    ns, nj = cos(radians(ANG)+DELTA), cos(acos(Q)+DELTA)
    cs, cj = ns-MU*sqrt(1-ns**2), nj-MU*sqrt(1-nj**2)
    for k in (0.,.05):
        pair=(39.6+.5)/(cs-k)
        all_jaw=(3*(39.6+.5+k*pair)+5*.070*9.80665)/cj
        print('analytic k / one seat-pair sum / entire jaw sum',k,round(pair,3),round(all_jaw,3))


def rocker():
    # Tail button is a sphere on a radial lever. Pin is tangential. Torque,
    # not spring compression, is its conjugate load. No angular hard stop.
    span, e=5.20, 1.96
    eta=e/span
    # Includes actual radial arm, pivot direction, tilt and centre displacement
    # relative to the pivot; a separate budget from the rigid-body wrench arms.
    for dv in (0.,.01,.02,.03):
        print('rocker speed error / service,table,fault nominal N equivalent',dv,
              np.round([bound(Q,PH,.10,c,angle=ANG,eta=eta,dv=dv) for c in CASES],3))
    S,hi,bar,free,G=50.,55.,1.45,9.,79300.
    torque=S*span; real_hi=hi*span
    k=G*pi*bar**4/(32*free)
    print('torsion bar M / degrees at midpoint / usable axial band / clean peak shear MPa',
          np.round([torque,degrees(torque/k),2*span*sin((real_hi-torque)/k),16*real_hi/(pi*bar**3)],4))
    # At a spherical working pole a = -t_hat (opening sense). Normal force
    # passes through ball centre. Friction also has a moment ABOUT that centre.
    # Nominal pole velocity per unit span: X + (eta+R*cos(angle)/span)*r_hat.
    dn=2*sin(DELTA/2)
    nx=cos(radians(ANG))
    b=eta+BACK*nx/span
    # Inclining the contact normal perturbs both its tangent projector
    # (spectral norm <= sin(delta)) and the local pole velocity. Trial dv=.02
    # includes centre and axis uncertainty for b_center; .006 rad axis error
    # for the ball offset lever, .01 radius error.
    dc=.02
    dp=dc+BACK/span*(dn+.006)+.01/span
    bn=hypot(1,b)
    good=nx-dn*hypot(1,eta)-dc
    good-=MU*(sqrt(bn*bn-nx*nx)+bn*sin(DELTA)+dp)
    print('rocker axial-work transfer before journal drag',round(good,5))
    # Simple radial-bearing envelope for two constrained stations spacing 5:
    # sum radial <= |F|+2*|M_orthogonal|/5, plus a separate thrust collar.
    # NOT a universal load-to-drag bound for a preloaded or jammed bearing.
    # Bearing model: moment/axial-force debit scaled to equivalent N.
    arm=hypot(span,e)+BACK+.19
    k_rad=hypot(1,MU)*(1+2*arm/5)*1.85/span
    k_thrust=hypot(1,MU)*2.15/span
    for mu_pin in (.02,.05,.10,.23):
        loss=mu_pin*(k_rad+k_thrust)
        print('assumed journal coefficient / debit / pair N screening bound',
              mu_pin,round(loss,5),round((hi+.5)/(good-loss),2) if good>loss else 'no bound')


if __name__=='__main__':
    linear()
    plunger()
    rocker()
