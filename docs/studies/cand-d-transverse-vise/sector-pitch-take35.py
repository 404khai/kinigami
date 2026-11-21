"""Take 35 independent-pose installation variants. Units mm and degrees."""
from runpy import run_path
from pathlib import Path
from itertools import product
from math import cos,hypot,radians,sin
d=run_path(str(Path(__file__).with_name('sector-drive-take35.py')))
globals().update({k:v for k,v in d.items() if not k.startswith('__')})

def sh(s,dx):return move(s,mul(dx,X))
def section(dx,A,R,dog):
    def piece(n,zs):
        # Sheared bars: preserve the original large crop at the bottom corner.
        return poly(n,[(x+a,y,z) for x,y in product((20.6,23.4),(4.,6.8)) for a,z in zs])
    m=negative(R)+band(R);f=installation(R)
    if R==12:
        m[0]=poly('working core',[(x,y,k*z) for x,y,z in [(17.77271,3.5,1.624738),
            (12.,3.5,4.488),(15.463623,8.118164,4.488)] for k in (-1,1)])
        cuts=((-3.20,-2.49),(-2.5,4.672705),(-5.188,5.188))
    else:cuts=((-3.85,-3.14),(-2.99,5.80),(-5.59,5.59))
    f.append(poly('END seat',[M['loc'](R,radians(A),p) for p in product(*cuts)]))
    if dx and dog:
        # Input local to translated head; lower arm terminates at old global x22.
        c=pivot(R);p=(22.-dx,5.4,0.);n=unit(sub(p,c));l=(-n[1],n[0],0.)
        m[1]=poly('plate',[plus(c,plus(mul(a,n),plus(mul(b,l),mul(z,Z))))
                  for a,b,z in product((12.2,hypot(*sub(p,c))+.5),(-2.4,2.4),(-15.6,-13.05))])
        m[2:3]=[piece('bar outer',[(-dx,-15.6),(-dx,-14.50)]),
                piece('bar slope',[(-dx,-14.5),(0.,-10.3)]),
                piece('bar upper',[(0.,-10.3),(0.,2.5)])]
    e=[]
    for t in retained13():
        if t[0]=='V-cheek' or t[0].startswith(('blade centre','blade outside')):
            t=sh(t,dx)
        elif t[0] in ('blade dogleg joint','blade negative wing'):
            t=sweep(t,mul(dx,X))
        e.append(t)
    return m,[sh(t,dx) if not t[0].startswith('foot') else t for t in f],e

def report(dx,A,R,dog):
    m,f,e=section(dx,A,R,dog);pitch=P+dx
    seat=next(s for s in f if s[0]=='END seat')
    yawset=[i*.5 for i in range(-30,31)]
    n=unit((1.,1/1.2,0.))
    # Support of the previous actual falling deck (not its full cylinder).
    # Convolution and the .06 height datum included; morphological opening
    # cannot add material. Plane-smoothing debit is conservative.
    base=(15+dx+8.04-1.75/1.2+.06+.06/1.2)*n[0]
    def cheek_margin(l):
        return min(proj(yaw(s,radians(j),pitch),n)[0]-base-.20-2*far(s,H)*sin(radians(.125))
                   for s in l for j in yawset)
    rr=[sh(s,dx) for s in m];t=tail(15-P)
    envelope=max((round(2*far(s,O),4),s[0]) for s in rr+e+f+t)
    coreblocks=[sh(swept_blocks(m[0],R,k,min(A,k+8)),dx) for k in range(0,A,8)]
    print('variant (pitch,A,R,bent), D, cheek seat/core margins incl .20, .06 smoothing, .06 height',
          (pitch,A,R,dog),envelope,round(cheek_margin([seat]),3),round(cheek_margin(coreblocks),3))
    if not dog and dx:return
    full=[sh(swept_blocks(s,R,0,A),dx) for s in m]
    ee=[sweep(s,mul(15,X)) if s[0].startswith('blade') or s[0]=='eject nut' else s for s in e]
    b,mn=D['setscan'](full+f,full+f+ee,list(range(-15,16)),pitch,.20,travel=15.)
    b2,mn2=D['setscan'](ee,full+f,list(range(-15,16)),pitch,.20,travel=15.)
    print('two heads broad unseparated (sector vs all; retained vs sector)',len(b),len(b2),b[:8],b2[:8])
    # Certify the separating plane on front-ramp tests, and distinguish OTHER
    # coupled-motion hits with actual points (never classify a hull hit).
    # One centre point inside both the real metal bar and the GP motor body.
    bars=[s for s in m if s[0].startswith(('bar ','forward crossbar'))]
    motor=next(k for k in f if k[0]=='6mm GP motor');wh=[]
    for j in range(-15,16):
        mot=yaw(motor,radians(j),pitch);lo,hi=proj(mot,Z);c=mot[1][0]
        for s in bars:
            for z in [-10.,-7.,0.,2.]:
                # All variants have the same x/y centre line here.
                if not proj(s,Z)[0]<z<proj(s,Z)[1] or not lo<z<hi:continue
                for a in range(A+1):
                    v=sh(arc(poly('p',[(22.,5.4,z)]),R,a),dx)[1][0]
                    wh.append((round(3.0-hypot(v[0]-c[0],v[1]-c[1]),4),a,j,z,v))
    print('bar centre vs next actual R3 motor: inside radius / q / yaw / z',max(wh)[:4])
    w=[]
    for j in range(-15,16):
        cen=yaw(motor,radians(j),pitch)[1][0]
        for a in range(A+1):
            x,y,_=arc(poly('axis',[(cen[0]-dx,cen[1],0.)]),R,-a)[1][0]
            # Use a point strictly inside the bar (inset .05), not its AABB.
            bx=min(max(x,20.65),23.35);by=min(max(y,4.05),6.75)
            w.append((round(3.-hypot(bx-x,by-y),3),a,j,bx,by))
    print('bar inset point inside next R3 motor',max(w))
    c=pivot(R);theta=radians(170.50+A);r=10.18
    x=c[0]+dx+r*cos(theta);y=c[1]+r*sin(theta)
    print('solid rear rack heel vs parked eject motor actual R3 at z-14',3.-hypot(x-12.6,y+15.37))
    for lo,hi in [(4,275),(155,275)]:
        g=[sh(polar(R,'lid '+nm,(a,min(a+8,hi)),rs,z),dx) for a in range(lo,hi,8)
           for nm,rs,z in [('near',(9.80,14.65),(-12.80,-12.48)),('far',(9.80,14.65),(-16.09,-15.85)),
                           ('rim',(14.25,14.65),(-15.85,-12.80))]]
        bad,mn=D['setscan'](g,ee,[0],0,.20)
        print('trial guard (start, end), guard-only D; own retained unseparated',lo,hi,
              round(max(2*far(k,O) for k in g),3),bad[:5])
    fs=[s for s in f if s[0].startswith('foot')]
    print('lowest pad vs fixed table -23 at yaw -15,0,+15',[round(min(proj(yaw(s,radians(a)),Y)[0] for s in fs),3)
         for a in (-15,0,15)])
    # Local drive conflicts, own fork, terminal departing aligned tail, foot.
    path=[sh(swept_blocks(s,R,k,min(A,k+8)),dx) for s in m[:6] for k in range(0,A,8)]
    b3,mn3=D['setscan'](path,t,list(range(-15,16)),0.,.20)
    b4,mn4=D['setscan'](f+[sh(arc(s,R,A),dx) for s in m],
                         [sweep(s,mul(15,X)) for s in tail(15+dx)],[0.],0.,.20)
    print('own fork (bar,core,finger and plate), open aligned eject tail',len(b3),mn3,len(b4),mn4)
    gv=next(s for s in f if s[0]=='driven blank');g=gv[1][0];hits=[]
    for a in range(A+1):
        z=-12.33;bf=1. if not (dx and dog) else (z+14.5)/4.2
        p=sh(arc(poly('p',[(22.-(1.-bf)*dx,5.4,z)]),R,a),dx)[1][0]
        rad=hypot(p[0]-g[0],p[1]-g[1]);hits.append((min(rad-.85,gv[2]-.675-rad),a))
    print('bar centre inside local wheel web / q',tuple(round(v,3) for v in max(hits)))
    eps=max((2*far(s,H)*sin(radians(.25)) for s in full+f+ee))
    left=min(proj(yaw(s,radians(a)),X)[0] for a in range(-30,31) for s in full+f+ee)-eps
    print('third head conservative axial gap mm',round(pitch*(1+cos(radians(15)))+left-max(proj(s,X)[1] for s in full+f+ee)-.20,3))
def straight_bound(dx):
    # Max squared point distance about any centre >= weighted variance.
    pts=[(-29.95,.48,0.),(19.05,-17.3,15.15),(23.4+dx,6.8,-15.60),
         (-11.,-8.9,25.55),(19.5,-12.70,18.74)]
    o=pts[0];var=0.
    for i in range(5000):
        v=max((sub(q,o) for q in pts),key=lambda v:dot(v,v));ds=dot(v,v)
        step=(ds-var)/(2*ds);o=plus(o,mul(step,v));var=(1-step)*(var+step*ds)
    return 2*sqrt(var)
if __name__=='__main__':
    print('straight-bar stocks any-centre D lower bound at dx+2/+2.5/+3',
          [round(straight_bound(j),3) for j in (2.,2.5,3.)])
    for case in [(0.,89,13.,False),(0.,101,12.,False),(2.,101,13.,False),(3.,101,13.,False),
                 (2.,101,13.,True),(2.5,101,13.,True),(3.,101,13.,True)]:
        report(*case)
