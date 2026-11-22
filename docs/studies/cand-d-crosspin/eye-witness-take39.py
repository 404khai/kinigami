"""Take 39 material points and idealized beam comparison. Exploratory, mm/N."""
from math import acos, asin, atan, cos, degrees, hypot, pi, radians, sin, sqrt


def contacts():
    R, r, b, s = 5., 2.7, 1.25, 1.35
    d = r+b
    theta = acos(d/R)
    arm = sqrt(R*R-d*d)
    H = 13.95-6.03
    # Tilt about Z keeping the rear core at (10,0,0). At every intermediate
    # angle the whole core lies on y=(x-10)tan(t), x>=10. Tube adds r*sqrt(2)
    # to either 45-degree plane. Projected radius in xz >= d from pin
    # follows from (1+u)[2B(B-d)+R² sin²t (1-u)] >= 0, B=R cos t, |u|<=1.
    assert theta<pi/4 and H-d-r*sqrt(2)>0
    print('bare eye tilt, opposed contact y separation, wall y-coordinate spare',
          degrees(theta), 2*arm, H-d-r*sqrt(2))
    for rr in [r,2.00,1.15]:
        if rr<=s:
            print('backing radius',rr,'does not bridge slot');continue
        error=asin(s/rr)
        alpha=radians(45-1)-error
        print('Rback, sag angle, signed X/N at 1deg error and mu=.23',
              rr,degrees(error),sin(alpha)-.23*cos(alpha))
    # At 20deg along this same path, the 330deg registry ball crosses the
    # positive wall. Reflect about Y=0 to exchange the two lower balls.
    for j in [-1,1]:
        t=radians(j*20)
        x,y,z=19.2, j*9*cos(radians(330)),9*sin(radians(330))
        centre=(10+(x-10)*cos(t)-y*sin(t),(x-10)*sin(t)+y*cos(t),z)
        w=(16.20,j*(16.20-6.03+.375),-4.60)
        depth=2.-hypot(*(x-y for x,y in zip(w,centre)))
        assert depth>1.74 and 1.35<abs(w[2])<8.5
        print('tilted ball vs wall t, material point, depth into R2',j*20,w,depth)


def journals():
    x,y=17.45,11.70
    wall=y-(x-6.03)
    assert 16.35<x<18.6 and 0<wall<.75 and 11.65<y<14.15 and 1.35<x-15.<2.60
    print('relieved race/cheek point', (x,y,0), 'race radius, wall Y from inner/outer',x-15,wall,.75-wall)
    print('min Y at relieved journal forward OD for exterior of wall with .20 Y reserve',
          15+2.6-6.03+.75+.2)
    print('at full park cap normal gap to wall inner/outer',
          *((10.50+1.25-(15.-6.03)-off)/sqrt(2)-1.25 for off in (0,.75)))
    # Ideal near clamp, point side load, and a rigid X-only far stop. Not
    # the skew, friction cone, indentation, or wear law of a finite bore rim.
    a=11.65; rim=a+10.32; I=pi*2.5**4/64; EI=205000*I
    k=a*a*(3*rim-a)/(6*EI)
    compliance=rim**3/(3*EI)
    print('apex/transition/rim Y; free compliance and rubbing onset',
          (-11.60,-10.35,-10.32),k,.1/k)
    for F in (30,50,85):
        reaction=max(0,(k*F-.10)/compliance)
        print('F, free displacement, ideal port reaction, near force, near moment, mu*.Rport',
              F,k*F,reaction,F-reaction,F*a-reaction*rim,.23*reaction)
    print('12-tooth screw dog maximum single tooth spring payout and force drop',
          .45/12*3.2/6,.45/12*3.2/6*45)


if __name__=='__main__':
    print('EXPLORATORY; material witnesses and provisional elastic/friction assumptions')
    contacts()
    journals()
