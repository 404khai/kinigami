"""Exploratory: L18 purely tangential swing; no L19 linkage/straight-slide credit."""
from math import acos, asin, atan, cos, degrees, hypot, pi, radians, sin, sqrt
from mushroom import A, P, W, b, bh, bl, drift, f, hertz, mu, p, show

L,H0,HLOCK=18.,2.450,3.020
HM,HP=-4.120,3.055
RS,K,HALF,WIDTH=1.55,6.15,1.10,4.40
def q(h): return asin((h-H0)/L)
def t(h): return L*(cos(q(HLOCK))-cos(q(h)))
kb=(t(0.)-t(-1.55))/1.55
def bore(z): return t(0.)+.007+kb*z


def layer():
    sphere=stem=0.
    # Circle (at constant z=n) to oblique bore axis. The maximum over its
    # azimuth is a concave quadratic in the cosine. Enclose whole h,z boxes.
    for i in range(1100):
        hl=HM+(HP-HM)*i/1100; hh=HM+(HP-HM)*(i+1)/1100
        ts=[t(hl),t(hh)]+([t(H0)] if hl<=H0<=hh else [])
        qs=[q(hl),q(hh)]
        for j in range(160):
            zl=-1.55+1.55*j/160; zh=zl+1.55/160
            dh=max(0.,hl-zh,zl-hh)
            dd=max(abs(x-bore(z)) for x in ts for z in (zl,zh))
            if dh<bh:
                r=sqrt(bh*bh-dh*dh)
                u=min(1.,dd/(r*kb*kb))
                sphere=max(sphere,sqrt(r*r*(1-u*u)+(dd+r*u)**2/(1+kb*kb)))
            # Infinite cylinder about shank axis, ellipse in z plane; only
            # the part aft of the sphere exists. This is deliberately larger.
            if zl<=hh+RS*max(abs(sin(y)) for y in qs):
                dm=max(abs(x+(z-h)*sin(y)/cos(y)-bore(z)) for x in ts
                       for h in (hl,hh) for z in (zl,zh) for y in qs)
                stem=max(stem,dm+RS/min(cos(y) for y in qs))
    show('L18 tilted wall: intercept/slope/deg, sphere plus drift, stem plus drift, running spare',
         bore(0),kb,degrees(atan(kb)),sphere+drift,stem+drift,2.475-sphere-drift)
    assert max(sphere,stem)+drift<2.475
    # Ellipse in 45-degree mouth plane: empty lip disk MUST fit within its
    # minor semiaxis, the true perpendicular bore radius (not its major)!
    sag=p-sqrt(p*p-2.51**2)
    # All q on the backside opening have |e|<=2.51+.02. Moving collar itself
    # is 1.50..1.55 below original plane. Gauge the two surfaces, not a depth dial.
    reach=(1.50-.42-2.53*.15)*cos(radians(8.5))-sag
    show('minimum backside-to-front-branch clearance along tilted face normal',reach)
    assert reach>.10


def free():
    best=2.; cb=3.; stemz=-1.e3; rr=0.
    # Front-connected chamber assumption: rear slot not an external route.
    # For sphere-centres at contacts C, |e|<=p+b+.020. If C_z<-1.70,
    # C_x is behind the front deck and C is outside the entire bowl blank.
    front=P[0]+.035+(p+bh+drift)*cos(f-radians(.30))-1.70*sin(f-radians(.30))
    assert front<3.27
    for j in range(380):
        hl=HM+(HP-HM)*j/380; hh=HM+(HP-HM)*(j+1)/380
        ts=max(abs(t(h)) for h in (hl,hh,H0))+drift
        ang=max(abs(q(h)) for h in (hl,hh))
        # Exposed cylindrical shank begins at sqrt(b^2-RS^2) behind centre.
        stemz=max(stemz,hh-sqrt(bl*bl-RS*RS)*cos(ang)+(p+RS)*sin(ang))
        rr=max(rr,ts+(p+RS)+K*sin(ang))
        for i in range(1200):
            l=-1+2*i/1200; r=-1+2*(i+1)/1200
            zl=max(-1.70,hl+min((p+bl)*l,(p+bh)*l))
            zh=hh+max((p+bl)*r,(p+bh)*r)
            if zh<zl: continue
            r0=(p+bl)*sqrt(1-max(l*l,r*r))-ts
            r1=(p+bh)*sqrt(1-(0 if l<=0<=r else min(l*l,r*r)))+ts
            if hypot(max(0.,5.35-r0,r1-W),max(abs(zl),abs(zh)))<p-1.e-9: continue
            a=cos(min(pi,acos(l)+ang+radians(.50)))
            best=min(best,a-mu*(sqrt(1-a*a)+bh/L))
            cb=min(cb,l)
    ds=hypot(max(5.35,rr-W),max(stemz,1.70))
    show('whole arc opening N/N inc spin; lowest c; stem overlap mm, behind deck x max',best,cb,p-ds,front)
    assert best>.026 and ds<p
    for bias in [.4,1.4]:
        N=bias/(best-.008)
        show('conditional bias N, leading normal / convex p GPa',bias,N,hertz(N,1/(1/bl+1/p))[1])
    # Only the rear span between elbow and offset web, not the pivot/riser.
    # Top of the rectangular shank-beam over all arm positions: linear in
    # distance from pivot, so its maximum is at one of the two ends.
    maxz=max(HP-(K-HALF)*cos(q(HP)),H0-(K-HALF)*min(cos(q(HM)),cos(q(HP))))
    show('horizontal beam top; clearance to throat terminating at -1.90',maxz,-1.90-maxz)
    assert maxz< -1.95


def structure():
    # 90g force caps from the separate nine-contact wrench calculation.
    nr,nv,nt,force=213.731,147.301,192.064,198.
    for N,Rlo,Rhi in [(nr,7.95,8.05),(nv,1/(1/bl-1/4.22),1/(1/bh-1/4.18))]:
        show('seated N, p0_GPa, largest radius mm',N,hertz(N,Rlo)[1],hertz(N,Rhi)[0])
    rear_patch=hertz(nr,8.05)[0]
    show('rear .40 land at .012 and .028 rad tilt',.40-.04-8.05*.012-rear_patch,.40-.04-8.05*.028-rear_patch)
    M=force*K+mu*nt*bh
    show('root moment Nmm, gross circular stem MPa; full arm moment upper',
         M,4*M/(pi*RS**3)+force/(pi*RS*RS),force*hypot(L,K)+mu*nt*bh)
    # If all that bending were about the weak section: cannot certify using
    # the neat little rectangular beam for its entire length.
    sect=WIDTH*(2*HALF)**2/6
    show('weak Z mm3, uncorrelated full-arm bending screen MPa (not yield evidence)',
         sect,(force*hypot(L,K)+mu*nt*bh)/sect)
    h=HM; av=(sin(q(h)),cos(q(h)))
    show('park elbow relative P (t,z); radial section incl +half e, -half a',
         t(h)-K*av[0],h-K*av[1],P[1]-(h-(K+HALF)*av[1])*cos(f)+WIDTH/2*sin(f))


if __name__=='__main__':
    layer()
    free()
    structure()
