"""Exploratory 3-D Take 39 layout. Coordinates/forces/torques: mm, N, N mm."""
from itertools import product
from math import sin,cos,tan,asin,atan,sqrt,radians,pi,hypot
from pathlib import Path
from runpy import run_path
D=run_path(str(Path(__file__).resolve().parents[1]/'cand-d-transverse-vise'/'oblique-drive.py'))
globals().update({k:D[k] for k in ('X','Y','Z','O','H','poly','box','proj','dot','mul','plus','sub','rot','far','sweep','move','yaw','sep','unit','retained','BASIC','check_pair','setscan')})
C=15.;P=33.;R=5.;r=2.70;rp=1.25;delta=(R-r-rp);close=C-delta
def cyl(n,v,span,a,b,r):
    i=(X,Y,Z).index(v)
    def end(h):
        p=[a,b];p.insert(i,h);return tuple(p)
    return poly(n,[end(h) for h in span],r,v)
def ball(n,p,r):return poly(n,[p],r)
def rod(n,p,q,r):return poly(n,[p,q],r,unit(sub(q,p)))
def hull(n,p,q,r):return poly(n,[p,q],r)
def mx(s,a):return move(s,mul(a,X))
def gate(x):return x-6.03
def wedge(n,a,b,z,sgn):
    return poly(n,[(x,sgn*(gate(x)+t),h) for x,t,h in product((a,b),(0.,.75),z)])
def seat(c):
    f=[]; t=[]
    for ind,a in enumerate([90.,210.,330.]):
        radial=(0.,cos(radians(a)),sin(radians(a)))
        lat=(0.,-radial[2],radial[1])
        b=plus((c+4.20,0.,0.),mul(9.,radial))
        u=plus(b,(-2*sqrt(2),0.,0.))
        t+=[ball('registry ball '+str(ind),b,2.),hull('registry spoke '+str(ind),(c+8.,0.,0.),b,1.15)]
        for sg in [-1,1]:
            f.append(poly('V%d/%d'%(ind,sg),[plus(u,plus(mul(w,radial),plus(mul(sg*v,lat),mul(x,X))))
                     for w in [-.85,.85] for v in [0.,2.20] for x in [-1.25,v]]))
        f.append(hull('V back rib '+str(ind),plus(u,(-1.05,0,0)),plus((5.5,0,0),mul(9.,radial)),.90))
    return f,t
def tail(c):
    # Each 15deg chord plus outer sag bound covers an actual swept R2.7 ball.
    s=[]
    def center(a):return (c+R*cos(radians(a)),0.,R*sin(radians(a)))
    for a in range(0,360,15):
        s.append(hull('torus%03d'%a,center(a),center(a+15),r+R*(1-cos(radians(7.5)))))
    s += [hull('neck',(c+5,0,0),(c+10.2,0,0),r),*seat(c)[1]]
    # Split body fork turns towards retained yaw pin (in own-tail coordinates).
    for sg in [-1,1]:
        s.append(hull('tail clevis '+str(sg),(c+10.20,0,1.1*sg),(c+11.50,-7.80,7.50*sg),1.2))
    return s
def ee():
    out=[]
    for s in retained():
        if s[0] in ('blade','blade dogleg joint','blade positive wing','blade negative wing','V-cheek'):continue
        if s[0]=='cell':s=box('cell',(-10.55,10.15),(-15.325,15.325),(-22.35,-16.95))
        out.append(s)
    out += [box('eject nose',(5.40,7.05),(-1.75,1.75),(-3.,3.)),
            box('eject spine',(2.30,5.70),(-.50,1.30),(-1.95,1.95)),
            box('eject bridge',(2.30,3.90),(.65,2.05),(-12.60,17.70))]
    return out
def pushed(s):
    return s[0].startswith(('blade','eject nose','eject spine','eject bridge')) or s[0]=='eject nut'
def fixed():
    f=[cyl('Y spindle',Y,(-21.1,21.3),7.50,-9.5,1.25),
       cyl('Y outer bearing',Y,(-21.30,-19.25),7.50,-9.5,2.65),
       cyl('Y near bearing',Y,(16.80,19.15),7.50,-9.5,2.65),
       cyl('Y drive wheel',Y,(-23.10,-21.65),7.50,-9.5,7.5),
       cyl('Y pinion',Y,(-23.10,-21.65),-1.3,-13.4,2.95),
       cyl('Y motor',Y,(-20.90,7.80),-1.3,-13.4,3.20),
       cyl('Y motor register',Y,(-21.45,-20.10),-1.3,-13.4,2.85),
       cyl('Y motor saddle',Y,(-10.6,-8.6),-1.3,-13.4,3.45),
       cyl('Y wheel hub',Y,(-23.35,-20.55),7.50,-9.5,1.80),
       box('Y rail',(2.40,3.90),(-19.9,18.7),(-15.20,-13.65)),
       box('X carrier rail',(10.25,17.65),(11.50,13.90),(-5.80,-4.15)),
       box('X far rail',(10.25,17.65),(-13.90,-11.50),(-5.80,-4.15)),
       box('spring stop',(6.50,7.50),(9.55,13.20),(-10.4,-6.7)),
       box('drive sensor',(-1.5,1.8),(-9.1,-4.0),(-7.6,-5.3)),
       box('H bridges',(-1.5,8.),(9.6,17.4),(12.1,14.6)),
       box('pin actual sensor',(12.1,17.1),(15.6,17.7),(1.55,3.65)),
       box('eject end switch',(15.7,18.0),(-10.1,-8.2),(10.4,12.3)),
       box('power socket',(-13.1,-9.2),(6.0,10.1),(14.2,18.7)),
       box('joint harness',(-9.2,-3.5),(-10.1,-6.4),(8.9,12.7))]
    # Material flares either side of reserved elongated x-slot; separate
    # upper/lower wall strips, plus the end strips (local aperture z +-1.35).
    for sg in (-1,1):
        f.extend(wedge('flare '+str((sg,z)),5.20,18.6,z,sg) for z in [(-8.5,-1.35),(1.35,8.5)])
        # Exterior flares start at x>6.03; the deep apex cut is added below.
        f.extend(wedge('flare port end '+str((sg,x)),*x,(-1.35,1.35),sg)
                 for x in [(6.40,12.60),(16.35,18.6)])
    for x,y in product((-11.,11.),(-7.,7.)):
        f.append(box('foot '+str((x,y)),(x-1.4,x+1.4),(y-1.3,y+1.3),(-23.5,-22.35)))
    f.extend([box('base rail L',(-10.8,11.5),(-7.9,-6.4),(-22.85,-22.50)),
              box('base rail R',(-10.8,11.5),(6.4,7.9),(-22.85,-22.50))])
    return f+seat(C)[0]
def hinge():
    f=[]
    for z in [(-9.3,-7.05),(7.05,9.3)]:
        f.append(cyl('hinge ear'+str(z),Z,z,H[0],H[1],2.3))
    f.append(cyl('joint pinion',Z,(-13.30,-12.),-7.9613,-18.1978,2.10))
    for a in range(-119,-77,3):
        f.append(poly('joint sector '+str(a),[(H[0]+r*cos(radians(v)),H[1]+r*sin(radians(v)),z)
                     for v,r,z in product((a,a+3),(4.5,9./cos(radians(1.5))),(-13.30,-12.))]))
    return f
def drive(t,cm):
    # t=0 testing a fully compressed setting, 6=unloaded, 32.05=retracted.
    # cm is x travel of actual carrier (spring extension is not carrier travel).
    x=close+cm; apex=-21.55+t; bar=15.25+t; yc=-17.+t
    s=[cyl('pin full shank',Y,(apex+rp,bar),x,0.,rp),ball('pin cap bound',(x,apex+rp,0.),rp),
       cyl('Y nut',Y,(yc-1.1,yc+1.1),7.5,-9.5,2.05),
       box('Y shoe',(2.10,4.20),(yc-1.55,yc+1.55),(-15.65,-13.40)),
       box('moving nut tie',(2.55,7.70),(yc-.8,yc+.8),(-14.20,-9.1)),
       box('moving pushrod',(2.45,3.95),(yc,bar),(-13.25,-11.85)),
       box('outboard link',(2.45,16.05),(bar-1.,bar+.55),(-13.25,-11.70)),
       box('outboard leg',(12.35,16.05),(bar-1.,bar+.55),(-12.20,1.35)),
       cyl('near race',Y,(11.65,14.15),x,0.,2.6),cyl('far race',Y,(-14.15,-11.65),x,0.,2.6)]
    for k in (-1,1):
        y=k*12.95
        s.append(box('moving ear '+str(k),(x-1.9,x+1.90),(y-1.12,y+1.12),(-7.45,0.)))
    s.extend([box('carrier tie',(x-1.65,x+1.65),(-13.8,13.8),(-9.75,-7.35)),
              box('spring pocket',(x-5.35,x+1.2),(9.95,13.0),(-9.60,-7.45)),
              box('cam track',(7.25,13.60),(-19.1,-8.9),(-13.2,-10.35))])
    return s
def cn(s):return tuple(sum(p[i] for p in s[1])/len(s[1]) for i in range(3))
def gap(s,t):
    n=sub(cn(s),cn(t));axes=BASIC+(unit(n),) if hypot(*n) else BASIC
    return check_pair(s,t,axes)-.20
def summary(n,u,v,skip=()):
    bad=sorted((round(gap(s,t),3),s[0],t[0]) for s in u for t in v if s[0]!=t[0] and (s[0],t[0]) not in skip and gap(s,t)<0)
    print(n,len(bad),bad[:9])
def main():
    print('EXPLORATORY only. Nominal design geometry, mm / N / N mm.')
    closed,rel,op=drive(0,0),drive(6,delta),drive(32.05,delta)
    h=hinge();e=ee();f=fixed();t=tail(C-P);sector=[s for s in h if s[0].startswith('joint sector')]
    st=f+closed+t+e+h;print('straight empty standby D extremes',sorted([(round(2*far(s,O),4),s[0]) for s in st],reverse=True)[:12])
    print('terminal moving outer y, floor z straight',max(proj(s,Y)[1] for s in op),min(proj(s,Z)[0] for s in st+op))
    for n,stg in [('closed',closed),('relieved',rel),('open',op)]:
        summary('actuator vs retained '+n,stg,e)
        summary('drive/guide vs retained '+n,f,e)
    # Continuous translation bounds at two endpoint stages. During relief x
    # motion is not assumed proportional to y (there is a live series spring).
    A=[sweep(sweep(s,mul(delta,X)),mul(6,Y)) for s in closed[:2]+closed[6:8]]
    # The first sweep conservatively includes all relative x/y translations.
    S=[poly(s[0],s[1]+k[1],s[2],s[3]) for s,k in zip(rel,op)]
    f2=[s for s in f+h if not s[0].startswith('joint sector')]
    summary('shaft/link relief vs fixed (incl intended fits)',A,f2)
    summary('relieved/open travel vs retained (eject parked)',S,e)
    summary('pin mechanism vs independently stroked ejector',op+f,[sweep(s,mul(15,X)) for s in e if pushed(s)])
    # For the local fork ignore only hinge hardware itself; articulated fork
    # and sector are not rigidly included in the same head-side comparison.
    bad,mn=setscan(f+closed+e,t+sector,list(range(-15,16)),0,.20)
    print('own moving tail incl sector, unseparated',len(bad),bad[:8])
    red=[s for s in h if not s[0].startswith('joint sector')]
    def nb(p,l,r):
        b,m=setscan(l,r,list(range(-15,16)),p,.20,travel=15.);return len(b),b[:5]
    # Each head-side test includes fixed hardware and fully stroked ejector
    # only after full withdrawal. Eye and registry of the departing neighbour
    # interact intentionally with seats and pin; do not count as a clear pair.
    for p in [P,36.]:
        for n,a,ea,b,eb in [('C/C',closed,e,closed,e),('C/O',closed,e,op,[sweep(s,mul(15,X)) if pushed(s) else s for s in e]),
                              ('O/C',op,[sweep(s,mul(15,X)) if pushed(s) else s for s in e],closed,e),
                              ('O/O',op,[sweep(s,mul(15,X)) if pushed(s) else s for s in e],op,[sweep(s,mul(15,X)) if pushed(s) else s for s in e])]:
            l=a+f+ea+red;r=b+f+eb+red
            print('neighbours',p,n,nb(p,l,r))
        tx=tail(C-p);print('alternatively extending own tail (no extended clevis correction) eye-only D',p,max(2*far(s,O) for s in tx if s[0].startswith('torus')))
if __name__=='__main__':main()
