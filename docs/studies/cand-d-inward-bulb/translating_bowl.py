"""Exploratory Take 24. Run beside mushroom.py. Actual dimensions in mm."""
from math import asin, atan, cos, degrees, hypot, pi, radians, sin, sqrt, tan
from mushroom import (A, D, H, L, P, W, b, bh, bl, drift, f, gap, hhi, mu,
                      p, projection, show)


def mouth():
    # z points along slide; v denotes forward uphill tangent to original facet.
    # z=min(0,max(-.40-v*tan8, -.32*(5.30-rho))). No material is added.
    t, k, rc = tan(radians(8)), .32, 5.30
    x=(k*rc-.40)/(k+t)
    depth=.40+t*x
    assert x>A and depth<.90
    show('trim max depth, at radius, nominal minimum flat-to-return gap at bore',
         depth,x,k*(rc-A)-(.40+t*A))
    # On .32 conical return use .34 maximum as-ground slope, facet error .3deg.
    m=(sin(f-radians(.3))-.34*cos(f-radians(.3)))/hypot(1,.34)
    lip=radians(44.)-asin(2.56/p)
    side_dist=hypot(max(abs(p-2*2.455),abs(p-2*A)),1.6)
    sag=p-sqrt(p*p-2.54**2)
    show('return min projected, empty tilted ring min draft deg/projected, side probe opposite ring distance',
         projection(m),degrees(lip),projection(sin(lip)),side_dist)
    show('plane -0.82 throat sag, back wall -1.50 inaccessible by',sag,1.50-.82-sag)
    assert min(projection(m),projection(sin(lip)),1.50-.82-sag,p-side_dist)>0


def cut_port():
    # Full hemisphere only: c>=0. Lower part is a cylinder, not an exposed
    # sphere with a slender neck. Intact top annulus alone suffices.
    cmax,hmin,WW=.315,-4.12,5.35
    worst=0.
    for i in range(1200):
        lo,hi=cmax*i/1200,cmax*(i+1)/1200
        r0=(p+bl)*sqrt(1-hi*hi)-drift
        r1=(p+bh)*sqrt(1-lo*lo)+drift
        for j in range(70):
            zl=(p+bl)*lo+hmin+(hhi-hmin)*j/70
            zh=(p+bh)*hi+hmin+(hhi-hmin)*(j+1)/70
            worst=max(worst,hypot(gap(r0,r1,WW,W),gap(zl,zh,0,0)))
    show('recessed collar strict exclusion c<=.315, overlap',p-worst-1.e-9)
    assert p-worst>.05
    # Equator-side cylinder normals c=0 at all accessible heights. For
    # z<=0 upper ring suffices to depth -4; behind that, fixed sleeve.
    assert hypot(p+bh+drift-W,4.0)<p and p+bh+drift-A<p
    deepest,shallow=-4.12,-4.08
    tip=shallow+bh
    show('total plunger travel, parked clearance behind back blank (-1.55)',
         hhi-deepest, -1.55-tip)
    assert -1.55-tip>.10
    for s in (0.,4.,9.):
        shift=s*sin(f-radians(.30))
        show('yoke travel; sphere behind moved back incl .06 relative error; behind deepest tail through port',
             s,-1.55+shift-tip-.06,-.82-(p-sqrt(p*p-2.54**2))+shift-tip-.06)


def band():
    # The circular inner cone clips unused polygon corners; it does NOT
    # remove the guard witnesses. Bound r of a full axis-normal disk using
    # its meridian coordinate s, t^2<=W^2-s^2. Interval not sampling.
    deck=3.30
    slope=tan(radians(16))
    worst=0.
    for i in range(2000):
        lo=-W+2*W*i/2000; hi=-W+2*W*(i+1)/2000
        tt=W*W-max(0.,lo,-hi)**2
        rho=sqrt((P[1]+hi*sin(f))**2+tt)
        worst=max(worst,rho+(deck-P[0]-lo*cos(f))*slope)
    # Slightly reducing the inner bore doesn't remove material at the collar;
    # use larger OUTER blank. To avoid covering the opening itself check local
    # extension including outer plane -1.55 at its complete radius A.
    show('entire planar port disk max radius extrapolated to deck at 16deg; clip radius',worst,17.70)
    show('x-front collar, moving rim home radius',P[0]+W*cos(f),18.25)
    assert worst<17.60
    # No W ring at -1 needed for low-c bounds: all probe centres have r>W.
    assert (p+bl)*sqrt(1-.315**2)-drift>W
    # For c<=.315 the guard above with WW..W at 0 and the blind sleeve
    # covers every positive-height centre; all z<=0 centres also satisfy
    # top witness down to -4.12. No buried full disk required.
    assert hypot(p+bh+drift-W,4.12)<p
    floor=-12.70
    clear=((17.70+(-6.15-deck)*slope)-6.68)*cos(radians(16))-p
    show('circular inner cone rolling-core clearance, floor clearance at home',clear,-6.15-p-floor)
    assert min(clear,-6.15-p-floor)>.7
    # 1.30 mm deep circular end band: exposed inside a fixed flaring sleeve.
    # Budget .55 radial shell, .14 radial gap, .40 outer wall on the sleeve.
    R=17.70+.55+.14
    for s in (4.,6.,9.):
        rf=R+(s+.30)*tan(radians(14.4))
        show('stroke, fixed guide OD incl wall, half-width margin to 20',s,2*(rf+.40),20-rf-.40)
    g=.14+4.3*tan(radians(14.4))+.10
    show('sleeve-to-band worst gap, maximum penetration into slit, +x min guide N/N',
         g,p-sqrt(p*p-(g/2)**2),projection(sin(radians(13.8))))
    assert g<2*p*cos(radians(17)) and p-sqrt(p*p-(g/2)**2)<.10
    # Three deep fixed shoe guides DO NOT fit a uniform 40 square centred on
    # the axis straight behind each port. This is a point on real plunger OD.
    dep=4.12+hhi+.20+2.20+.15
    y=(P[1]+dep*cos(f))*cos(radians(15))+bh*sqrt(1-(cos(f)*cos(radians(15)))**2)
    show('straight rear barrel worst extent, overshoot at centred 15deg clock',y,y-20)
    F,M=164.3,623.5
    show('LWL2 screening F/C0+M/640, LWL1 F/C0, rear direct rail length minimum',
         F/381+M/640,F/113,12.5+hhi+4.12)
    show('two 2.2-spaced rows total normal bound, allowed effective start ratio incl moment',
         F+2*M/2.2,.035*145.07/(F+2*M/2.2))


if __name__=='__main__':
    mouth()
    cut_port()
    band()
