"""Refold the two drives on opposite decks; material witnesses, not gate evidence."""
from runpy import run_path
from pathlib import Path
from math import atan2,degrees
d=run_path(str(Path(__file__).with_name('eye-pin-take39.py')))
globals().update({k:v for k,v in d.items() if not k.startswith('__')})
def mirror(s):
    def m(p):return (p[0],p[1],-p[2])
    return poly(s[0],list(map(m,s[1])),s[2],m(s[3]) if s[3] else None)
def upper():
    f=[]
    for s in fixed():
        if s[0].startswith(('Y ','X carrier rail','X far rail','spring stop','drive sensor')):
            s=mirror(s)
            if s[0]=='Y drive wheel':s=(*s[:2],6.35,s[3])
            if s[0]=='Y pinion':s=(*s[:2],4.02,s[3])
        elif s[0].startswith(('flare','eject end switch')):continue
        f.append(s)
    for sign in [-1,1]:
        for z in [(-8.5,-1.35),(1.35,8.5)]:f.append(wedge('side flare '+str((sign,z)),9.50,18.60,z,sign))
        for x in [(9.50,12.60),(16.35,18.6)]:f.append(wedge('port end '+str((sign,x)),*x,(-1.35,1.35),sign))
    f.extend([cyl('dog pivot',Z,(11.0,14.1),5.3,-15.8,1.10),
              box('normal-open hold dog',(4.2,8.4),(-17.5,-14.6),(11.7,13.4)),
              box('cam follower sensors',(5.8,9.8),(-17.2,-14.0),(14.0,16.0)),
              box('actual pin target pickup',(12.0,16.9),(14.9,16.8),(-3.4,-1.7)),
              # Brake tooth plate and positive spring seat travel are separate
              # allocations; sensing them is not evidence of clamp release.
              box('force foil',(8.9,11.6),(9.2,13.3),(9.8,10.3)),
              box('upper base tie',(1.5,14.9),(-17.8,-16.5),(10.4,11.8))])
    return f
def moving(t,cm):
    out=[]
    for s in drive(t,cm):
        if s[0] not in ('pin full shank','pin cap bound','near race','far race'):s=mirror(s)
        out.append(s)
    return out
def lower():
    f=[cyl('X eject screw',X,(-16.35,18.5),-6.20,-13.50,1.0),
       cyl('X rear thrust',X,(-14.8,-12.10),-6.20,-13.50,2.65),
       cyl('X nose bush',X,(16.0,18.25),-6.20,-13.50,2.20),
       cyl('X transmission web',X,(-16.50,-15.20),-6.20,-13.50,6.53),
       cyl('X pinion',X,(-16.50,-15.20),2.90,-13.50,3.22),
       cyl('X motor',X,(-14.75,13.95),2.90,-13.50,3.20),
       cyl('X mount',X,(-8.2,-6.25),2.90,-13.50,3.45),
       box('X master rail',(-10.4,17.7),(-9.6,-8.05),(-15.65,-14.15)),
       box('X roll rail',(-10.4,17.7),(-2.1,-.80),(-12.30,-11.10)),
       box('lower plate',(-10.4,17.7),(-10.5,-7.75),(-16.25,-15.75)),
       box('eject position switch',(12.2,15.7),(-9.4,-7.8),(-12.3,-10.5))]
    # Separate lower guides 6.95 lateral / 3.20 vertical apart. Finger
    # rises below the eye, not through a full transverse crossbar.
    m=[cyl('X nut',X,(-1.70,.50),-6.20,-13.50,1.85),
       box('master shoe',(-8.2,.8),(-10.15,-7.70),(-16.1,-13.80)),
       box('roll shoe',(-8.2,.8),(-2.45,-.45),(-12.65,-10.75)),
       box('eject crosslink',(-.70,.8),(-9.65,.75),(-13.90,-11.45)),
       box('eject axial rib',(-.7,6.8),(-.8,.8),(-12.50,-10.10)),
       box('eject upright',(5.0,6.8),(-.8,.8),(-11.5,1.25)),
       box('eject face',(5.65,7.05),(-1.65,1.65),(-1.75,1.75))]
    return f,m
def kept():return [s for s in ee() if s[0] in ('cell','MCU','joint pin','joint motor')]
def pusherloads():
    span=9.;F=15.;mu=.23;dist=hypot(13.5+1.75,6.2+1.65)
    # Relative to screw; nonsymmetric guides, single corner included.
    M=F*dist; pair=2*M/span
    print('15 N face to screw transverse eccentricity, moment, summed guide reactions, friction-only axial demand',dist,M,pair,F+mu*pair)
    for q in [0,6,32.05]:
        x=close if q==0 else C;tip=-21.55+q
        print('q, x, apex, shank end, clearance of cap to inclined port plane',q,x,tip,15.25+q,(tip+rp-gate(x))/sqrt(2)-rp)
    I=pi*2.5**4/64;L=25.8;F=85
    print('locked pin 85N centre simply supported span/M/stress MPa/deflection',L,F*L/4,32*(F*L/4)/(pi*2.5**3),F*L**3/(48*205000*I))
    a=11.65;b=11.65+10.32;k=a*a*(3*b-a)/(6*205000*I)
    print('post-far-race cantilever compliance mm/N at far rim, rub threshold, deflection at 50N',k,.10/k,50*k)
    # Screw preload and efficiency are not ratings. Pitch dia for M2.5x.45.
    dm=2.5-.64952*.45;lam=atan(.45/(pi*dm));mu=.18
    # 3.2 mm x input over 6 mm y, with .10 roller-friction screening equiv.
    slope=3.2/6;F=85.;Fy=F*tan(atan(slope)+atan(.10))+.23*F
    T=Fy*((dm/2)*tan(lam+atan(mu/cos(radians(30))))+.08*1.45)
    print('clamp cam Fy, screw Nmm, gearhead Nmm at .80 efficiency',Fy,T,T/(5.95/(hypot(8.8,3.9)-5.95)*.80))
    print('service spring x at 65/85N (k45N/mm); command travel total',(65/45,85/45),1.05+85/45)
    F=15+pair*.23;dm=2.-.64952*.40
    torque=F*((dm/2)*tan(atan(.4/(pi*dm))+atan(.18/cos(radians(30))))+.08*1.2)
    print('eject screw Nmm, gear motor Nmm @.8 eff before guide feedback etc',torque,torque/(6.1/3./.8**-1))
def cases():
    h=hinge();es,em=lower();f=upper()+es+kept();t=tail(C-P)
    cl=moving(0,0);re=moving(6,delta);op=moving(32.05,delta)
    print('refold D component limits',sorted([(round(2*far(s,O),4),s[0]) for s in f+em+h+cl+t],reverse=True)[:10])
    print('deployed max y',max(proj(s,Y)[1] for s in op))
    print('ground z / nonfoot min / after eject',min(proj(s,Z)[0] for s in f),min(proj(s,Z)[0] for s in f+em+cl+t+h if not s[0].startswith('foot')),min(proj(s,Z)[0] for s in op+em))
    summary('refold fixed upper vs lower',upper(),es+em+kept())
    for n,s in [('closed',cl),('relieved',re),('open',op)]:
        summary('refold actuator vs lower '+n,s,es+em+kept())
        summary('refold actuator vs table-top hardware '+n,s,upper())
    summary('full ejection vs upper and open pin',[sweep(s,mul(15,X)) for s in em],upper()+op)
    # A whole-body relative test includes both heads at independent endpoints,
    # plus an independent 0..15 mm departure of the second head and 1deg yaw.
    jointfixed=[s for s in h if not s[0].startswith('joint sector')]
    for p in [33.,36.]:
        for an,a in [('C',cl),('O',op)]:
            for bn,b in [('C',cl),('O',op)]:
                l=f+jointfixed+a+([sweep(s,mul(15,X)) for s in em] if an=='O' else em)
                right=f+jointfixed+b+([sweep(s,mul(15,X)) for s in em] if bn=='O' else em)
                bad,mn=setscan(l,right,list(range(-15,16)),p,.20,travel=15.)
                print('folded neighbours',p,an+bn,len(bad),bad[:5],mn)
    # Don't include the designed hinge bore/shaft overlap or the eye of the
    # adjacent unit intentionally on seats/in the pin. Other contacts count.
    sector=[a for a in h if a[0].startswith('joint sector')]
    bad,mn=setscan([a for a in f+em+cl if a[0]!='joint pin'],t+sector,list(range(-15,16)),0.,.20)
    print('local yawed fork/sector with controls',len(bad),bad[:7])
    # Is the bare, previously mated torus/spider actually outside at stroke?
    print('aligned, maintained leading-crown contact: terminal crown/mouth nominal gap',7.05+15.-18.60)
    print('parked crown gap',15-5-2.7-7.05)
    # Extra crosshead retreat would be required if stow had to be READY open.
    print('open pin end to most negative own-eye extreme (pair alone D lower bound)',hypot(15-(C-P-R-r),47.30))
if __name__=='__main__':
    pusherloads();cases()
