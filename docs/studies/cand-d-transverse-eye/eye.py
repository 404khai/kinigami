"""Take 38. Rigid contact/linear elastic screens, mm N MPa. Stdlib only."""
from math import acos, asin, atan, cos, degrees, hypot, pi, radians, sin, sqrt, tan

R, r, p, h, mu = 5., 2.7, 1.25, 1.35, .23
S, H = r+p, hypot(1., mu)
alpha, eta = radians(45), radians(1)
X0, xp = 6.03, 15.


def out(title, *a):
    print(title + ':', ' '.join(f'{x:.6f}' for x in a))


def lip(Rb):
    # Exact worst +x coefficient at 45 degrees on a straight, x-slotted port.
    a = alpha-asin(h*cos(alpha)/Rb)
    return degrees(a), sin(a-eta)-mu*cos(a-eta)


def ports():
    out('parallel edge tangent/in-plane semiaxes', h/cos(alpha), h)
    out('stipulated coarsest tube/nominal/largest; angle, work per N',
        *lip(2.6), *lip(r), *lip(2.9))
    rr = h*cos(alpha)/sin(alpha-eta-atan(mu))
    sag = r-sqrt(r*r-h*h)
    out('required uniform radius; nominal ball sag; first journal buffer',
        rr, sag, 11.65-(xp+h-X0+sag/cos(alpha)))
    out('rounded tip apex required after relief; actual reserve',
        xp-X0+p*(1/cos(alpha)-1)+.2/cos(alpha),
        10.50-(xp-X0+p*(1/cos(alpha)-1)+.2/cos(alpha)))
    assert lip(r)[1] > .184 and abs(lip(rr)[1]) < 1e-10


def mixed():
    # Tilt about z; x-y tilted minor axis and z major axis.
    theta, t = radians(36), radians(60)
    c, s = cos(theta), sin(theta)
    g = hypot(sin(t)/c, cos(t))
    x, z = R*c*sin(t)-S*sin(t)/(c*g), R*cos(t)-S*cos(t)/g
    ys, cy = R*s*sin(t), R*s
    def nearest(y):
        d, b = x*c+y*s, -x*s+y*c
        w = hypot(z, d)
        return hypot(R-w, b)-S, ((R*c*d/w-x)/S, (R*s*d/w-y)/S, (R*z/w-z)/S)
    lo, hi = -1.38, -1.34
    assert nearest(lo)[0] < 0 < nearest(hi)[0]
    for _ in range(64):
        mid = (lo+hi)/2
        if nearest(mid)[0] < 0:
            lo = mid
        else:
            hi = mid
    # f' has at most three roots; cap exit (f' positive), following local
    # maximum, then strict shank minimum. Check curvature/derivative signs.
    def deriv(y):
        d = x*c+y*s
        w = hypot(z,d)
        return 2*(y-R*d*s/w), 2*(1-R*s*s*z*z/w**3)
    assert deriv(hi)[0] > 0 and abs(deriv(ys)[0]) < 1e-10 and deriv(ys)[1] > 0
    # f(ys) local min, f''(y) stays positive for y>=ys.
    assert x*c+hi*s < 0 < x*c+ys*s and abs(nearest(ys)[0]) < 1e-10
    n1, n2 = nearest(ys)[1], nearest(hi)[1]
    Cx = xp-x
    clear = min((Cx-X0-sgn*cy)/sqrt(2)-R*abs(c-sgn*s)/sqrt(2)-r
                for sgn in (-1, 1))
    out('mixed witness Cx,Cy,Cz; cheek gap', Cx, cy, -z, clear)
    out('mixed shank centre y, tip centre y, apex y', cy+ys, cy+hi, cy+hi-p)
    out('mixed shank then hemisphere normal into eye', *n1, *n2)
    assert clear > .83 and -.20 < n2[1] < -.19
    # Two horizontal shank normals at concentric pinch, offset eye in y.
    th = acos(S/R)
    out('centred pinch deg, axial separation, earth y offset, wall clearance at x13.95',
        degrees(th), 2*R*sin(th), R*sin(th), (13.95-X0-S)/sqrt(2)-r)
    out('one-contact curvature threshold deg', degrees(acos(sqrt(S/R))))
    return (x*c+hi*s)/hypot(z,x*c+hi*s), n2


def wrench():
    cut = 1.60
    g = sqrt(1-(cut/2)**2)-mu*cut/2
    L = min(S,R-S)*cut
    den = L-p*mu*(1+H)
    out('near-normal g; far separation and denominator', g, L, den)
    out('sum N <= cM |M_C| + cF |F| (also covers aligned pair)',
        (1+H)/den, max(1/g, ((1+H)*(R+S)+L)/den))
    out('symmetric pinch normal sum per Nmm about pin midpoint (no net radial used)',
        1/(sqrt(R*R-S*S)-p*mu))
    assert den > 1.09 and g > .41
    th = radians(40)
    out('radially outward r2.70 stem: reserve at relative tilt 40deg, axis offset 1.05',
        R*cos(th)-1.05-S*sin(th))
    out('terminal R3.0 ball centred at radius 7: all-line pin clearance same domain',
        7*cos(th)-1.05-(3+p))


def journals():
    # Each fixed guide solid exterior to a cylinder of MINIMUM clear radius h.
    # D, beta are bounds on the LOADED generator offsets and pin inclination.
    for ang,D in ((.5,.18),(1,.18),(4,.35)):
        b = radians(ang)
        g = (h*h-D*D-p*p)/(2*p)-D*tan(b)-mu*(D/cos(b)+p*tan(b))
        ad = sin(b)+mu
        out('beta deg, offset, centring work/N, max drive eccentricity (or 0)',
            ang,D,g,max(0,g)/(ad*tan(b)))
    out('short race maximum cocking: slope budget before sec(beta) correction deg',
        degrees(atan(2*(h-p)/2.50)))


def hertz(k1, k2, force, Estar):
    # Hertz ellipse via the two principal surface-gap curvatures.
    # Long semiaxis a, b/a=l. Integrate after s=tan(u)^2 with a=1.
    assert k1 > 0 and k2 > 0
    k1,k2 = sorted((k1,k2))
    count = 512
    def integrals(l):
        a = b = 0.
        for i in range(count+1):
            u = (pi/2)*i/count
            c2,s2 = cos(u)**2,sin(u)**2
            v = l*l*c2+s2
            w = (1 if i in (0,count) else 4 if i%2 else 2)*2*c2/sqrt(v)
            a += w
            b += w/v
        return a*pi/(6*count), b*pi/(6*count)
    lo,hi = .01,1.
    for _ in range(48):
        l=(lo+hi)/2
        ix,iy=integrals(l)
        if iy/ix > k2/k1:
            lo=l
        else:
            hi=l
    a=(3*force*integrals(hi)[0]/(2*pi*Estar*k1))**(1/3)
    return a, a*hi, 3*force/(2*pi*a*a*hi)*.001


def stress(mixed_minor,n):
    E,nu,F=205000.,.30,50.
    Es=E/(2*(1-nu*nu))
    ar = mixed_minor*(cos(radians(36))*n[0]+sin(radians(36))*n[1])+sqrt(1-mixed_minor**2)*n[2]
    for name,a,b in (('loaded inner-shank',1/r,1/p-1/(R-r)),
                     ('mixed cap',1/p+1/r,1/p-ar/(R-r*ar)),
                     ('outer tip limiting curvatures',1/p+1/r,1/p+1/(R+r))):
        out(name+' principal curvatures; 50N ellipse mm, p0 GPa',a,b,*hertz(a,b,F,Es))
    K=1/p
    assert abs(hertz(K,K,F,Es)[0]-(3*F/(4*K*Es))**(1/3)) < 1e-10
    I=pi*p**4/4
    L,Hf=11.65,11.65+(xp+h-X0)
    tip=F*L**2*(3*Hf-L)/(6*E*I)
    out('near-clamped L, end station, 50N deflection at load/port, first contact N',
        L,Hf,F*L**3/(3*E*I),tip,F*(h-p)/tip)
    out('50N ideal double-support centred / single-support nominal pin bending MPa',
        F*(25.8/4)*p/I,F*L*p/I)
    out('single r2.70 section: force shear avg; bending 5 mm offset MPa',
        F/(pi*r*r),4*(F*5)/(pi*r**3))


if __name__ == '__main__':
    ports()
    minor, normal = mixed()
    wrench()
    journals()
    stress(minor,normal)
