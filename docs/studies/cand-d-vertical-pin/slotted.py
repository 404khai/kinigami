"""One-sided tapered button through a forward-open roof slot. mm, N."""
from math import asin, atan, cos, degrees, hypot, pi, radians, sin, sqrt, tan
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'cand-d-drawbolt'))
from edge_hertz import hertz


def work(a,mu=.23):return sin(a)-mu*cos(a)


def check(R=7.50,r=4.20,b=.48,k=.32,angle=28.,mu=.23):
    a=radians(angle); m=tan(a); beta=atan(k); error=radians(1.)
    # r-spine torus in XY at (15,0,0). Cone radius at height z is b+k*z.
    # Aft bore wall tangent; cone below that station has a flat rounded-off
    # end, all face normals in the same downward cone. No far support.
    dx=b+r/cos(beta); xp=15-R+dx; H=r/cos(a)+m*dx+.18
    zbot=-.8
    assert b+k*zbot>0
    # Through-stock cut includes .40 projected roof thickness AND .16 radial
    # reserve. Intersecting the infinite cone with z=H+.40+m*(x-xp)
    # gives an ellipse with the following x extrema and transverse radius.
    u=b+k*(H+.40); h=k*m
    p=u/sqrt(1-h*h)+.16
    xmin=xp-u/(1+h)-.16
    xmax=xp+u/(1-h)+.16
    # Fixed slotted plate may be completed by a gallery, but anything above
    # or beside this slot reachable from its ends needs its own check.
    theta=asin(sin(a)*sqrt(1-(p/r)**2))
    gx=work(theta-error,mu);gz=work(beta-error,mu)
    zc=r*sin(beta);rho=b+k*zc
    # A *full exposed cone* must reach the highest crossing. Turning it to
    # a vertical shank earlier leaves a lower-slope contact in the open slot.
    # A conservative fully parked test: put the whole bottom face above the
    # roof at the forwardmost pin projection, allowing the r-backed ball's
    # sag into the slot plus .20 normal. User hardware can choose a tighter
    # bound if it actually restricts the end/side approaches.
    sag=r-sqrt(r*r-p*p)
    zshoulder=(H+m*b+(sag+.20)/cos(a))/(1-m*k)+.12
    radius=b+k*zshoulder
    lift=H+m*radius+(sag+.20)/cos(a)-zbot
    # Centre-loaded, correctly oriented analytic Hertz screen. The cone and
    # torus principal transverse curvatures are opposite, not additive.
    ra=1/(cos(beta)*(1/rho-1/(R-r*cos(beta))))
    hs=[hertz(F,*sorted((ra,r))) for F in (50.,120.)]
    print('R,r,b,k,alpha',R,r,b,k,angle)
    print('x axis/H, through cut x rear/forward, slot halfwidth, post root z/r',
          *(round(x,5) for x in (xp,H,xmin,xmax,p,zshoulder,radius)))
    print('normal coefficients open pin +Z / slot ejection +X, cutter span, lift',
          *(round(x,6) for x in (gz,gx,xmax-xmin,lift)))
    print('axial contact rise, radius; pressure GPa @ 50/120N',zc,rho,
          [round(v[-1]/1000,3) for v in hs])
    # Rolling guide with two effective bands. Worst external point load N,
    # |transverse| <= hypot(1,mu)N, axial pressure centre offset <= radius.
    # All bending couples, including axial tangential forces; not a 50/50
    # split or a claim that the bands have the same contact direction.
    L=12.; over=14.; drag0=.50;gmu=.005
    Hf=hypot(1,mu); j=Hf*(1+2*(over+radius)/L)
    # Use only for statically determinate 2-plane lateral reaction resultants
    # with bounded/qualified moment drag. Not valid for a tight plain bore.
    print('trial guide reaction amplification, allowable effective friction, '
          'net lift/N and no-static-balance normal if drive free',
          j,gz/j,gz-j*gmu,drag0/(gz-j*gmu) if gz>j*gmu else None)
    assert gx>0 and gz>0 and p<r
    return gx,gz


if __name__=='__main__':check()
