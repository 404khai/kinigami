"""Take 18: analytic lamella neighbour certificate. Python 3, mm, N, MPa."""
from math import sqrt, hypot, sin, cos, tan, atan, radians, pi


def show(label, *v):
    print(label, *(round(x, 6) for x in v))


mu = .23
k = 1/tan(radians(34.5))
ell = .60
glo, ghi = .42, .52   # working core-to-core gap, before final edge rounding
hlo, hhi = .09, .10
step = .020           # additional differential radial recession of sister core
debit = 2*sin(radians(.5))
def envelope(p, e, slope, hlow, hhigh):
    a = slope+e/glo
    b = ghi*(1+a*a)/(2*(p+hlow))+(hhigh-hlow)/glo
    # |u_x| <= k c, |u_t| <= a c + b, c = -u_r before alignment debit.
    A = 1+k*k+a*a
    assert b < 1
    c = (sqrt(A-(A-a*a)*b*b)-a*b)/A-debit
    q = c-mu*sqrt(1-c*c)
    if q<=.12:
        return c, q, float('inf'), float('inf')
    return c, q, .55/(q-.12), (.55+1.08*1.2)/(q-.12)


for p in [.95, 3.185]:
    show('p, c, radial N/N, free N, closing N (matched h, zero differential)', p,
         *envelope(p, 0, ell, hhi, hhi))
    show('p, c, radial N/N, free N, closing N (toleranced)', p,
         *envelope(p, step, ell, hlo, hhi))
show('toleranced .90 taper (infinite means screen fails)',
     *envelope(.95, step, .90, hlo, hhi))
_, q, free, closing = envelope(.95, step, ell, hlo, hhi)
assert q>.20 and free<6.84 and closing<22.95
W = .05*9.80665
show('delivered static push at k=0,1,3 free leading combs',
     *(5*W+i*hypot(1, mu)*free for i in (0,1,3)))
# Shared friction budget is not needed: separate adverse extrema enclose it.
cmin=envelope(.95,step,ell,hlo,hhi)[0]+debit
ratio=0.
for i in range(1000):
    lo=cmin+(1-cmin)*i/1000
    hi=cmin+(1-cmin)*(i+1)/1000
    rr=lo-debit
    ax=min(1/hypot(1,mu),k*hi+debit, sqrt(1-rr*rr))
    ratio=max(ratio,(ax+mu*sqrt(1-ax*ax))/(rr-mu*sqrt(1-rr*rr)-.12))
pushes=[5*W+i*.55*ratio for i in (0,1,3)]
show('angle-coupled delivered push at k=0,1,3, pointwise summed',*pushes)


# Backed globe flat fit. Use the worst unloading centre even at full draw.
land = .70/2
def hertz(F, r):
    rad = (3*F*r/(4*115400))**(1/3)
    return 3*F/(2*pi*rad*rad)/1000, rad
def eff(p, h): return p*h/(p+h)
Nback = 39.865971
pressure, patch = hertz(Nback, 3.185)
tx = .131706 + 3.215*sin(radians(1)) + .020
show('central flat pressure GPa, patch radius, transverse remaining land',
     pressure, patch, land-tx-patch)
assert land-tx-patch > .04

# Elastic illustration at a straight cut-line round and a doubly curved vertex.
def ellipse(F, p, h, major):
    kx = 1/p+1/h
    ky = 1/p+(1/major if major else 0)
    def integrals(t):
        sums=[0.,0.]
        for i in range(301):
            co=cos(pi*i/600)**2
            d=1+(t*t-1)*co
            v=(1 if i in (0,300) else (4 if i%2 else 2))*2*co/sqrt(d)
            sums[0]+=v; sums[1]+=v/d
        return tuple(v*pi/1800 for v in sums)
    lo,hi=1.,32.
    for _ in range(55):
        t=(lo+hi)/2; u,v=integrals(t)
        if u/v<kx/ky:lo=t
        else:hi=t
    a=(3*F*u/(2*pi*115400*kx))**(1/3)
    return 3*F/(2*pi*t*a*a)/1000,a,t*a
assert abs(ellipse(10, .95, hlo, hlo)[0]-hertz(10,eff(.95,hlo))[0])<1.e-8
for p,F in [(3.185, Nback),(.95,free),(.95,closing)]:
    show('rolling sphere radius, one-edge load, straight lip p0 GPa/half-axes',
         p,F,*ellipse(F,p,hlo,None))
    show('same sphere on .09 x .09 vertex, p0 GPa, contact radius',*hertz(F,eff(p,hlo)))

# Cantilever screens; demonstration section sizes, not measured stresses.
L=4.; E=200000.
txw, width=1.80, .70
Fx=Nback*(cos(radians(34))+mu*sin(radians(34)))
Ft=Nback*(sin(radians(1))+mu)
Fr=Nback*(sin(radians(36))+mu*cos(radians(36)))
show('single central root component envelope MPa without stress concentration',
     Fr/(width*txw)+6*L*Fx/(width*txw**2)+6*L*Ft/(txw*width**2))
I=txw*.60**3/12
force=hypot(1,mu)*closing
show('thin tooth: trial all-lateral F, deflection at 4mm, arm at .015mm deflection',
     force, force*L**3/(3*E*I),(3*E*I*.015/force)**(1/3))

# Signed plane distance: d=(r-m*x-A0)/sqrt(1+m^2), increasing into wall.
ml, mh = .39,.41
wide_slot=.52
sag=.95-sqrt(.95**2-wide_slot**2)
nx=sin(atan(ml))*sqrt(1-(wide_slot/.95)**2)-2*sin(radians(.25))
show('largest fixed slot: sag, axial normal, outward N/N',
     sag,nx,nx-mu*sqrt(1-nx*nx))
show('all-parked and three-free one possible fixed lip load ceilings',
     pushes[0]/(nx-mu*sqrt(1-nx*nx)),pushes[2]/(nx-mu*sqrt(1-nx*nx)))
cut=sag+2*hhi+(ell*ghi+step)/hypot(1,ml)+.05
show('required local backing trim plane normal distance, incl .05 debit',cut)
xv,rv=3.436608,2.065802
park=.19+mh*(xv+.015)-(rv-.030)+(3.215+.82+sag+.05)*hypot(1,mh)
show('aligned entire comb nominal-plane effective parked stroke requirement',park)
# Hex packaging witness: central .92 moving tooth, regular .60 teeth and
# .30 moving gaps. Fourth outer centre is 1.06+3*.90=3.76.
t=3.76
A=.16+3.20*hypot(1,.4)+.4*xv
r=2*(A-t*sin(pi/3))
base=rv+max(0.,ell*(t-.48))
show('adjacent unslotted hex plane x,r,t; radial core offset, clip margin',
     xv,r,t,base-r,4.80-r)
assert 0<base-r<.70 and r<min(A,4.80) and t>A/sqrt(3)

# Actual single-lip globe tangent, inside even the unperforated guard.
# Take shifted globe (1.25,0,.54), central core t in [-.36,.36],
# preoffset .70. In this meridian |t|<.48, the uncut nose is cylindrical.
B=3.20; h=.10; pre=.70
ox,ot=1.25,.54
v=(ot-.36)/(B+h)
z=sqrt(1-v*v); D=pre+(B+h)*z
dx=xv-ox
dr=sqrt(D*D-dx*dx)
s=dr-rv
assert dr/D>sin(radians(35)) and dx/D<cos(radians(35))
rr=z*dr/D
q=rr-mu*sqrt(1-rr*rr)
Nfree=.55/(q-.12); Nclose=(.55+1.08*1.2)/(q-.12)
# The next core begins at t=.86; enclosing it by the same cylindrical nose
# relaxes its actual tangential taper. Its distance thus has a lower bound.
sister=hypot(D-pre,.86-ot)-B-h
major=pre/z+h
show('single nominal lip x/r/t, stroke, uncut wall slack, sister clearance',
     ox,0,ot,s,.16+.4*ox-ot*sqrt(3)/2,sister)
show('single lip: no-tilt q, free/closing cap, p0 GPa at 1N / both caps',
     q,Nfree,Nclose,*(ellipse(f,B,h,major)[0] for f in (1,Nfree,Nclose)))
assert sister>.01 and s>0 and rv+s-.80>1.02
