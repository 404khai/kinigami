"""Loaded indexed face: existence of compressive carrier forces, not assembly."""
import sys
from itertools import product
from math import asin, atan, cos, degrees, hypot, pi, radians, sin, sqrt, tan
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'cand-d-expanding-plug'))
from crown import envelope
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'cand-d-drawbolt'))
from edge_hertz import hertz

X,Y,Z = np.eye(3)
A,r,b = 5.,2.7,1.25
site = 8.5


def pin_data(z_error, tilt_deg=2., mu=.23):
    # Circular pin axis fixed along Y. The ellipse support h is at least
    # B=A*cos(tilt). Its core point has tangential offset <= (A²-B²)/(2B)
    # from the radial line of the projected unit normal n. Hence q=p-d*n,
    # the projected C-to-pin-axis vector, has that same tangential offset.
    lo,hi=A-.025,A+.025
    a=radians(tilt_deg)
    radial=lo*cos(a)-(r+.015+b+.010)
    tangent=hi*sin(a)**2/(2*cos(a))
    nangle=asin((z_error+tangent)/radial)
    lateral=tan(nangle+atan(mu))
    # Patch excursion .15 mm, centre-to-registry error .08 mm: trial limits.
    # Y contact is on the cylinder opposite the core point. True z contact
    # differs from the pin centre-line by at most b_hi*sin(nangle).
    arm_y=hi*sin(a)+.15+.08
    arm_z=z_error+(b+.010)*sin(nangle)+.15+.08
    return nangle,lateral,hypot(arm_y,arm_z)


def seats(alpha):
    cols=[]
    for phase in (90,210,330):
        l=cos(radians(phase))*Y+sin(radians(phase))*Z
        for sg in (-1,1):
            n=cos(alpha)*X+sg*sin(alpha)*np.cross(X,l)
            cols.append(np.r_[n,np.cross(l,n)])
    return np.array(cols).T


def pulls(mass, degrees_face, zerr):
    alpha=radians(degrees_face)
    J=seats(alpha)
    H=np.linalg.inv(J)
    nangle,K,off=pin_data(zerr)
    dn=2*sin(radians(.6)/2); dp=.19/site
    assert np.linalg.svd(J,compute_uv=False)[-1] > sqrt(6)*hypot(dn,dn+dp)
    # All six carriers are normal forces on registered spherical pads.
    # Inverse columns about the pad-centre triangle at x=18 mm. Nominal
    # pin pressure centre is x=12.70 mm: lever arm is NOT zero.
    req=[]
    for case in ('service','table','fault'):
        e=envelope(mass,case,site,wide='take23')
        need=0.
        for d in H:
            f,m=d[:3],d[3:]
            loss=(np.linalg.norm(f)*dn+np.linalg.norm(m)*(dn+dp))/cos(alpha+radians(.6))
            g=f+np.cross(m,-5.30*X)/site
            pad=K*np.linalg.norm(g[1:])+((off+.25*K)*np.linalg.norm(m[1:])
                                            +off*K*abs(m[0]))/site
            slope=f[0]-pad-loss
            if slope <= 0:
                need=float('inf');break
            need=max(need,(abs(d)@e+loss*e[0])/slope)
        req.append(need)
    return req


def strength(F,L=25.8):
    # Single nominal central load between simple supports: stated load split
    # follows equilibrium for this load location. F*L/4 also bounds maximum
    # moment for ANY single transverse point load between those supports.
    diam=2*b
    stress=32*(F*L/4)/(pi*diam**3)
    sag=F*L**3/(48*200000*(pi*diam**4/64))
    # Inner equator of aligned eye: z principal curvature NEGATIVE
    # -1/(A-r); other curvature 1/r; cylindrical pin contributes 1/b in z.
    ra=1/(1/b-1/(A-r)); rb=r
    a,c,p=hertz(F,*sorted((ra,rb)))
    print(f'{F:.3f} N central, {L:g} mm span: nominal bending {stress:.1f} MPa, '
          f'elastic sag {sag:.4f} mm; aligned Hertz {p/1000:.3f} GPa, axes {a:.4f}/{c:.4f} mm')


if __name__=='__main__':
    for z,face in product((.025,.050,.100),(45.,55.,62.)):
        ang,K,off=pin_data(z)
        print(f'z {z:.3f}, {face:g} deg; normal angle {degrees(ang):.3f}, '
              f'side/draw {K:.4f}; required axial N:',
              *[round(v,3) for v in pulls(70.,face,z)])
    f=max(pulls(70.,62.,.050)); assert np.isfinite(f)
    strength(f)
