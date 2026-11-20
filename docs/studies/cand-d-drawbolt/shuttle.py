"""Take 16: exploratory sizing inequalities; NOT package or motion evidence.
Units mm, N, N mm. Input limits below are proposed fixture acceptance limits.
"""
from math import atan, cos, hypot, pi, radians, sin, sqrt, tan
from scipy.optimize import brentq
import numpy as np
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'cand-d-exact-pairs'))
from take11 import matrix, const_load, cert, exit_bound

def screws(lead):
    # Rectangular enclosure over working radii 1.12..1.50, lead +-0.02,
    # flank normal error <=0.5 degrees. No both-flank interference.
    h0,h1=(lead-.02)/(2*pi),(lead+.02)/(2*pi)
    z=sqrt(1+tan(pi/6)**2+(h1/1.12)**2)
    delta=radians(.5)
    c=z*sin(atan(.23)+delta)
    plus=brentq(lambda k:k-h1-c*hypot(1.5,k),0,2)
    minus=brentq(lambda k:k+h0-c*hypot(1.5,k),0,2)
    floor=brentq(lambda k:h0-k-z*sin(delta)*hypot(1.5,k),0,1)
    return plus,minus,floor

def pads():
    k0=np.array([24.,12.]); k1=np.array([28.,16.])
    trip0=np.array([5.4,2.8]); trip1=np.array([6.,3.])
    gap=(.03,.09); pickup=.010; backoff=.015; height=.350
    print('far-seat trip compression min,max',trip0/k1,trip1/k0)
    print('minimum far-seat force after index recoil',trip0-k1*backoff)
    print('earliest/latest free-tip height at far-seat trip',gap[0]+trip0/k1,gap[1]+trip1/k0)
    assert np.all(gap[1]+trip1/k0+pickup<=height+1e-12)
    assert np.all(trip0-k1*backoff>const_load(50,'service')[[0,3]])
    b=k1*height
    P=.37/.70*3*sum(b)+2
    print('pad maxima, preloader input',b,P)
    H=matrix(); I=np.eye(6); bias=np.repeat(b,3)
    for m in (46,50):
        for load in ('service','correction','fault'):
            base=const_load(m,load)
            q,hard=cert(H,base+(I+H)@bias,list(range(6)))
            print(m,load,'ideal, biased hard upper, collocated total upper, rho<=',
                  base[[0,3]],hard[[0,3]],(hard+bias)[[0,3]],q)
    return P

def keeper(resist):
    mu=.23; R=6.; span=6.; arm=5.; e=.12
    D=(resist+3*.8)/(1-.468)
    A=1.190*D
    # All three follower forces can add adversely. Radial guide normals from
    # the two y/z lands and pitch/yaw couple including eccentric axial contact.
    normals=sqrt(2)*((1+2*arm/span)*D+2*R/span*A)
    res=[]
    for g in (.012,mu):
        res.append((A+g*normals+1)/(1-g*2*sqrt(2)*e/span))
    print('keeper Rres,D,A,guide sum (before input eccentricity), working input rolling/sliding',
          resist,D,A,normals,*res)
    return res[0]

def eject():
    assert exit_bound(50)[-1]<10
    S=sin(radians(.5))+.23; X=1+.23*sin(radians(.5)); R=4.88
    N=sqrt(2)*((1+2*5/6)*S+2*R/6*X)+2*R*S/6
    p=(10.30*(X+.23*N)+1)/(1-.23*2*sqrt(2)*.12/6)
    # Grounded motion converter with axial output and centred input; efficiency
    # includes ALL side-thrust at the converter and the input carriage.
    print('eject: rear seat sum requirement, design sum, output crosshead, input',
          exit_bound(50)[-1],10.30,p,1.15*p/.80+2)
    return 1.15*p/.80+2

if __name__=='__main__':
    np.set_printoptions(precision=5,suppress=True)
    for lead in (1.5,2.):
        kp,km,ko=screws(lead); J=37/ko
        print('lead, k_raise, k_lower+, k_min, jam F, reverse torque, other torque left, work F',
              lead,kp,km,ko,J,km*J,30-km*J,(30-5)/kp)
    A=pads()
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument('--resist',type=float,default=10.18,
                    help='up-rounded mixed.py --focus drive result at intended orientation/load')
    K=keeper(ap.parse_args().resist); E=eject()
    phase=(.360/.35,1.63/tan(radians(35)),2.80/1.10,.20)
    print('selected stroke allocations',phase,'sum',sum(phase))
    print('go/no-go centre work',max(A,K,E),'vs 4-start at min clutch',(30-5)/screws(2.)[0])
