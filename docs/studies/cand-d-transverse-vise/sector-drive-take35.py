"""Take 35 exploratory rotary toe study. mm, N; pure Python. No gate run."""
from itertools import product
from math import atan, atan2, cos, degrees, hypot, pi, radians, sin, sqrt, tan
from pathlib import Path
from runpy import run_path

D=run_path(str(Path(__file__).with_name('oblique-drive.py')))
X,Y,Z,O,H,P=[D[k] for k in ('X','Y','Z','O','H','P')]
dot,plus,sub,mul,rot,box,poly,proj,far,move,sweep,yaw,sep,check,unit,tail=[D[k] for k in
    ('dot','plus','sub','mul','rot','box','poly','proj','far','move','sweep','yaw','sep','check_pair','unit','tail')]
M=run_path(str(Path(__file__).with_name('sector-contact-take34.py')))
BASE=D['BASIC']
B=(.6,.8,0.);V=(-.8,.6,0.)
def pivot(R):return (15.-.6*R,3.50-.8*R,0.)
def uv(R,u,v,z):return plus(pivot(R),plus(mul(u,B),plus(mul(v,V),mul(z,Z))))
def plate(R,name,u,v,z):return poly(name,[uv(R,*p) for p in product(u,v,z)])
def zc(name,p,z,r):return poly(name,[(p[0],p[1],k) for k in z],r,Z)
def arc(s,R,d):
    c=pivot(R);a=radians(d)
    return poly(s[0],[plus(c,rot(sub(p,c),a)) for p in s[1]],s[2],rot(s[3],a) if s[3] else None)
def core(R):return poly('working core',[M['loc'](R,0.,p) for p in M['vertices'](M['P'])])
def seat(R):
    return poly('END seat',[M['loc'](R,radians(101),p) for p in
                     product((-3.85,-3.14),(-2.99,5.80),(-5.59,5.59))])
def negative(R):
    # Load arm/crossbar reaches the far corner on the *front* of the working
    # end, not behind the aft surface of the compulsory terminal seat.
    c=pivot(R);p=(22.0,5.4,0.);n=unit(sub(p,c));l=(-n[1],n[0],0.)
    arm=poly('plate',[plus(c,plus(mul(a,n),plus(mul(b,l),mul(z,Z))))
                      for a,b,z in product((12.2,hypot(*sub(p,c))+.5),(-2.4,2.4),(-15.60,-13.05))])
    return [core(R),arm,box('forward crossbar',(20.6,23.4),(4.,6.8),(-15.6,2.5)),
            box('finger',(15.15,22.65),(4.65,6.8),(-1.6,1.6))]
def band(R):
    # An 8..171 deg annulus in 10-degree hull boxes, conservatively circumscribed
    # on the OD and filled to the chord on the ID, so the gap between stations
    # is not mistaken for material. Covers pitch radius 13.50; m=.50.
    c=pivot(R);out=[]
    for j,a in enumerate(range(8,171,10)):
        b=min(a+10,171);od=14.0/cos(radians((b-a)*.5))
        out.append(poly('rack '+str(j),[(c[0]+r*cos(radians(k)),c[1]+r*sin(radians(k)),z)
            for r,k,z in product((10.1,od),(a,b),(-15.60,-13.05))]))
    return out
def retained13():
    e=[]
    for s in D['retained']():
        if s[0]!='blade':e.append(s);continue
        e.extend([box('blade centre',(3.35,4.15),(-1.5,3.30),(-5.15,5.15)),
                  box('blade outside−',(3.35,4.15),(-1.5,4.7),(-10.65,-5.15)),
                  box('blade outside+',(3.35,4.15),(-1.5,4.7),(5.15,10.65))])
    return e
def branch(R):
    e=retained13();es=[sweep(s,mul(15.,X)) if s[0].startswith('blade') or s[0]=='eject nut' else s for s in e]
    u=negative(R)+band(R);f=[seat(R)]
    t=tail(15.-P);tpose=[(yaw(s,radians(a)),a) for s in t for a in range(-15,16)]
    hits={};mins={}
    def tally(n,s,t,a,j,eps,ax=BASE):
        g=max(check(s,t,ax)-eps,sep(s,t,Z)-.20)
        if s[0]=='working core' and t[0]=='blade centre' and a!=101:
            g=max(g,radial_gap(R)-.20)
        mins[n]=min(mins.get(n,99.),g)
        if g<0:
            key=n,s[0],t[0];v=round(g,4),round(a,2),j
            if key not in hits or v<hits[key]:hits[key]=v
    for s in f:
        for t in es:tally('seat vs own',s,t,0,0,.20)
        for t,j in tpose:tally('seat vs own tail',s,t,0,j,.20+2*far(t,H)*sin(radians(.25)))
    for s in u:
        rs=far(s,pivot(R))
        for a in range(102):
            b=arc(s,R,a);eps=.20+2*rs*sin(radians(.25))
            ax=BASE+(rot(B,radians(a)),rot(V,radians(a)),rot(X,radians(a)),rot(Y,radians(a)))
            for t in (es if a==101 else e):tally('ram vs own',b,t,a,0,eps,ax)
            for t,j in tpose:tally('ram vs own tail',b,t,a,j,eps+2*far(t,H)*sin(radians(.25)),ax)
            for t in tail(15.):
                if (s[0],t[0])!=('working core','upper ball'):tally('ram vs mate',b,t,a,0,eps,ax)
            if s[0]!='working core':
                for t in f:tally('seat vs extras',b,t,a,0,eps,ax)
    print('R',R,'D',max((round(2*far(s,O),3),s[0]) for s in u+e+f))
    for n in mins:
        vals=sorted((v,s,t) for (k,s,t),v in hits.items() if k==n)
        print(n,round(mins[n],3),len(vals),vals[:9])

def radial_gap(R):
    # Supporting plane at the rear lower vertex is tangent to a circle
    # about the pivot. All core vertices outside that halfspace prove an
    # inner radius for the whole convex core; not a minimum of radii alone.
    c=pivot(R);s=core(R);q=min(s[1],key=lambda q:hypot(q[0]-c[0],q[1]-c[1]))
    n=unit((q[0]-c[0],q[1]-c[1],0.))
    blade=next(k for k in retained13() if k[0]=='blade centre')
    return proj(s,n)[0]-dot(c,n)-max(hypot(p[0]-c[0],p[1]-c[1]) for p in blade[1])
def polar(R,name,angles,rad,z):
    pts=[];c=pivot(R)
    for r,a,h in product(rad,angles,z):
        rr=(r/cos(radians((angles[1]-angles[0])/2)) if r==max(rad) else r)
        pts.append((c[0]+rr*cos(radians(a)),c[1]+rr*sin(radians(a)),h))
    return poly(name,pts)
def installation(R):
    c=pivot(R);a=radians(160);n=rot(X,a);t=rot(Y,a)
    p=plus((c[0],c[1],-14.325),mul(15.0,n))
    def wc(nm,r,v):return poly(nm,[plus(p,mul(i,t)) for i in v],r,t)
    b=plus(p,mul(-7.,t));m=(-10.,12.,0.);ell=hypot(b[0]-m[0],b[1]-m[1])
    f=[wc('worm blank',1.875,(-2.9,2.9)),wc('worm shaft',.85,(-7.95,4.5)),
       wc('thrust aft',1.9,(-4.9,-3.05)),wc('thrust fore',1.9,(3.05,4.5)),
       wc('worm bevel blank',1.85,(-8.25,-6.0)),zc('pinion bevel blank',b,(-14.4,-12.3),1.85),
       zc('bevel shaft',b,(-13.7,-11.65),.85),
       zc('driven blank',b,(-12.83,-11.83),ell-2.+.3),
       zc('6mm GP motor',m,(-10.8,17.9),3.2),zc('6mm GP saddle',m,(6.5,8.2),3.5),
       zc('driver blank',m,(-12.83,-11.83),2.30)]
    # Two fixed capture stations (outer lips, inner radial cheeks and return
    # via a common backbone) on the inner ring edge, one flexibly preloaded.
    for j in (124,165):
        for nm,r,z in [('outside lip',(8.5,11.7),(-16.09,-15.84)),
                       ('inside lip',(8.5,11.7),(-12.81,-11.50)),
                       ('guide body',(8.5,9.85),(-16.09,-11.50))]:
            f.append(polar(R,nm+' '+str(j),(j-5,j+5),r,z))
    f += [box('track tie',(-2.7,1.65),(-10.85,2.65),(-12.65,-11.55)),
          box('interior bridge',(-2.7,1.65),(-10.85,-9.5),(-12.6,-8.5)),
          box('backbone',(-2.7,15.9),(-10.85,-9.50),(-9.75,-7.15)),
          box('cheek pier',(12.5,15.9),(-10.85,-6.2),(-9.75,-7.15))]
    feet=[box('foot '+str((x,z)),(x-1.5,x+1.5),(-23.,-21.0),(z-1.3,z+1.3))
          for x in (-12.6,9.) for z in (-8.2,8.2)]
    return f+feet
def swept_blocks(s,R,lo,hi):
    # Hull of the two endpoint copies over each short interval + sagitta.
    # Merge the interval hulls into a coarser envelope for broad checks.
    q=list(range(lo,hi,3))+[hi];v=tuple(p for a in q for p in arc(s,R,a)[1])
    err=far(s,pivot(R))*(1-cos(radians(1.5)))
    assert not s[2]
    return poly(s[0],v,err)
def extra(R):
    m=negative(R)+band(R);f=installation(R)+[seat(R)]
    e=retained13();ee=[sweep(s,mul(15.,X)) if s[0].startswith('blade') or s[0]=='eject nut' else s for s in e]
    print('full named stowed inventory D',max((round(2*far(s,O),3),s[0]) for s in m+f+e+tail(15-P)))
    for n,u,v in [('fixed frame/drive vs retained',f,ee),('fixed frame/drive vs swinging tail',f,tail(15-P))]:
        bad,minimum=D['setscan'](u,v,list(range(-15,16)) if 'swinging' in n else [0],0,.20,{('cheek pier','V-cheek')})
        print(n,len(bad),bad[:12],minimum)
    full=[swept_blocks(s,R,0,101) for s in m]
    ax=range(-15,16)
    for n,u,v,p in [('next existing vs new swept',ee,full+f,P),
                    ('new swept vs next complete',full+f,full+f+ee,P),
                    ('fixed motor/frame vs local full ram',full,f,0.)]:
        bad,minimum=D['setscan'](u,v,list(ax) if p else [0],p,.20,travel=15. if p else 0.)
        print(n,len(bad),bad[:9],minimum)
    # Refine unseparated with actual point-inside-solid witnesses.
    g=next(s for s in f if s[0]=='driven blank');b=m[2];z=-12.33;cc=g[1][0]
    a=90;pt=arc(poly('bar middle',[(22.,5.4,z)]),R,a)[1][0]
    print('moving bar centre vs driven OD at q90; OD minus centre distance',pt,g[2]-hypot(pt[0]-cc[0],pt[1]-cc[1]))
    pts=[arc(poly('bar middle',[(22.,5.4,z)]),R,j)[1][0] for j in range(102)]
    # Continuous gear web inside the root circle, excluding hub hole if close.
    ds=[hypot(pt[0]-cc[0],pt[1]-cc[1]) for pt in pts]
    print('driven tooth root and nearest & index',g[2]-.675,min(ds),ds.index(min(ds)))
    print('named moving stock ymin',min(proj(s,Y)[0] for s in full),'floor = -23')
    left=min(proj(yaw(s,radians(a)),X)[0]-2*far(s,H)*sin(radians(.25))
             for a in range(-30,31) for s in full+f+ee)
    print('third head axial gap',P*(1+cos(radians(15)))+left-max(proj(s,X)[1] for s in full+f+ee)-.20)
def witnesses():
    # Centreline points inside BOTH of the positive-volume solids, rather
    # than interpreting unseparated broad-phase hulls as interference.
    for R in (12.,13.,15.,18.,20.):
        w=[]
        for x,y,z,key in [(-16.,0,6.062,'boss'),(-12.5,0,7.5,'arm root'),(-9.,0,7.5,'arm')]:
            for j in range(-15,16):
                p=yaw(poly('p',[(x,y,z)]),radians(j))[1][0]
                for a in range(65,102):
                    h=arc(poly('p',[p]),R,-a)[1][0]
                    g=min(h[0]-12.65,17.35-h[0],h[1]-4.95,7.55-h[1],h[2]+15.88,19.48-h[2])
                    if g>0:w.append((round(g,3),key,j,a))
        print('U hard witness: R, inside bar, tail feature, yaw, q',R,max(w))
def cheek_nominal(x,z):
    # Take 27 raw profile: 35° finite radial grooves, central relief, falling rim.
    r=hypot(x,z);k=tan(radians(35))
    h=min(-1.75-1.20*max(0.,r-8.04),-3.86+k*max(0.,r-1.75))
    for a in (180,60,-60):
        c=cos(radians(a));s=sin(radians(a));xx=x-7*c;zz=z-7*s
        d=hypot(max(0.,abs(xx*c+zz*s)-.70),-xx*s+zz*c)
        h=min(h,-3/cos(radians(35))+k*d)
    return h
def buried(R,a,j,p,down=0.):
    v=M['loc'](R,radians(a),p)
    pt=plus(plus((P,0.,0.),H),rot(sub(v,H),radians(j)))
    x,y,z=pt;x-=15;y-=down
    # The centre may sit a little below the witness. The complete .45 ball
    # stays in the disk, above its backed bottom, below the smoothed top.
    # The same ball is therefore present after morphological opening by .45.
    assert 0<=down<.45
    reserve=min(10.75-hypot(x,z)-.45,y+6.5-.45,
                cheek_nominal(x,z)-y-.45*hypot(1,1.20)-.06*1.20)
    return reserve,pt
def collisions():
    cases=[('seat',12,101,15,(-3.80,5.75,0),.40),
           ('seat',13,101,15,(-3.50,4.625,0),0),
           ('core',13,101,15,(-2.85,4.70,0),0),
           ('core',15,101,14,(-2.6,3,0),0),
           ('core',18,101,-5,(-2.6,1,0),0),
           ('core',20,101,-13,(-2.2,-1,0),0),
           ('core',12,110,15,(-2.85,4.70,0),0)]
    for n,R,a,j,p,down in cases:
        if n=='core':assert all(dot(v,p)<h-.15*hypot(*v) for v,h in M['P'])
        else:assert -3.85<p[0]<-3.14 and -2.99<p[1]<5.80 and abs(p[2])<5.59
        gap,pt=buried(R,a,j,p,down)
        print('preceding cheek actual metal',n,R,a,j,p,'point',tuple(round(v,4) for v in pt),
              'ball containment spare',round(gap,4))
        assert gap>0
    print('radial blade separator R13, R12 incl .20',radial_gap(13.)-.20,radial_gap(12.)-.20)
    end=arc(box('bar',(20.6,23.4),(4,6.8),(-15.6,2.5)),13.,101)
    n=rot((-1.,0.,0.),radians(101));ev=unit((1.,2.05,0.))
    print('additional terminal crossbar -x facing normal, e dot',n,dot(ev,n))
def loads(R):
    # Force at any point of the Ø5 actually loaded home flat. Tolerance
    # allowance .10 per radius; pure +y with a whole .23 transverse disk.
    arm=.6*R+2.6;rad=.8*R;z=14.325+2.60
    F=85.; T0=F*(arm+.23*rad); M=F*(z+.23*rad)
    st=2*10.1*sin(radians((165-124)/2));N=F*(1+.23)+2*M/st
    gear_radius=13.475;worm_radius=1.525;mod=.35
    lam=atan(mod/(2*worm_radius));alpha=radians(20)
    print('T0, M transverse, shoe span, reaction sum screen one moment',T0,M,st,N)
    for mu in [.04,.08,.12,.23]:
        Tg=T0+mu*10.1*N
        eff=tan(lam)/tan(lam+atan(.18/cos(alpha)))
        Ft=Tg/gear_radius
        # Worm axes intersect at a right angle; thrusts can approach Ft.
        Tw=Tg/(77*eff)+Ft*.1*1.3+1.5
        print('guide mu, sector Nmm, tooth force, worm Nmm, GP Nmm',mu,Tg,Ft,Tw,Tw/(3.50*.85*.85))
    print('worm lead deg, mu flank lower threshold, zero-friction hold at worm',degrees(lam),
          tan(lam)*cos(alpha),T0/77)
    print('C lip width, t, free length, foot reaction, bending MPa',
          10.1*radians(10),.25,1.6,M/st,(M/st)*1.6/(10.1*radians(10)*.25**2/6))
    print('backbone rectangular section y,z, out-of-plane torque before 3D joint analysis',1.35,2.60,85*14.325)
    print('crossbar cantilever 85N normal, outer fibre bending MPa',
          F*z/(2.8*2.8**2/6))
if __name__=='__main__':
    witnesses()
    collisions()
    branch(13.)
    extra(13.)
    loads(13.)
