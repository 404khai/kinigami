"""Compact fixed X screw/rails plus folded vertical rack; exploratory."""
from pathlib import Path
from runpy import run_path
d=run_path(str(Path(__file__).with_name('fixed-z-route-take42.py')))
globals().update({k:v for k,v in d.items() if not k.startswith('__')})
YS=-12.0;ZS=12.70; SX=-2.35; SY=-13.95
PARK=11.25;DZ=PARK-TIP
def zs():
    s=[]
    for a in route_z():
        n=a[0]
        if n.startswith(('B wheel','Z gear cover','Z motor pinion','Z gearmotor','Z motor saddle')):
            a=mx(a,9.95)
            if n.startswith(('Z motor pinion','Z gearmotor','Z motor saddle')):
                a=move(a,(0.,5.8,(-sqrt(7.7**2-4.3**2)+sqrt(7.7**2-1.5**2))))
        if n=='B axle':a=cyl(n,X,(7.75,17.8),15.50,4.20,1.10)
        s.append(a)
    s.extend([cyl('B near bush',X,(10.1,11.2),15.50,4.20,1.65),cyl('B far bush',X,(17.2,18.15),15.5,4.20,1.65),
              box('Z cover rail',(10.15,11.0),(16.9,17.65),(3.10,12.50))])
    for sg in (-1,1):
        y=2.75*sg
        s.append(poly('roof strap '+str(sg),[(x,yy,z) for x in (10.6,11.9)
            for yy in (y-.45,y+.45) for z in (x-4.53+.52,13.50)]))
        s.append(box('clear beam '+str(sg),(12.40,13.5),(y-.40,y+.40),(10.77,11.08)))
    return s
def slide3():
    s=[a for a in slide() if not a[0].startswith(('slide bar','translating screw','thrust bridge','roll link','outer tie'))]
    # Threaded nut contains the screw, including full standby/eject travel.
    s += [cyl('X moving nut',X,(SX-1.5,SX+1.5),YS,ZS,2.05),
          box('nut saddle',(SX-1.45,SX+1.20),(-15.65,-13.55),(11.35,14.15)),
          box('force spring cage',(SX-2.60,1.02),(-15.85,-13.55),(8.65,11.72)),
          box('master carriage',(-6.78,1.10),(-16.05,-13.55),(5.05,8.40)),
          box('master link',(-.62,1.07),(-15.70,-13.50),(3.43,10.15)),
          box('master lower tie',(-.65,1.12),(-14.65,-13.16),(-4.62,4.50)),
          box('roll carriage',(-6.78,1.10),(4.20,6.60),(5.10,8.30)),
          box('roll link',(-.65,1.12),(4.05,5.95),(3.48,7.95))]
    return s
def xs():
    z=ZS;y=YS;x=-8.75
    s=[cyl('X screw',X,(-11.80,16.35),y,z,1.25),
       cyl('X front radial bush',X,(15.4,16.80),y,z,2.7),
       cyl('X rear thrust race',X,(-7.55,-5.60),y,z,2.90),
       cyl('X worm wheel',X,(x-1.05,x+1.05),y,z,4.72),
       cyl('X friction clutch',X,(-11.05,-9.86),y,z,3.25),
       cyl('X brake drum',X,(-12.45,-11.10),y,z,3.45),
       cyl('X worm',Z,(z-1.95,z+1.95),x,y-5.70,1.6),
       cyl('X motor',Z,(z-31.05,z-2.35),x,y-5.70,3.00),
       cyl('X motor saddle',Z,(-12.20,-10.90),x,y-5.7,3.45),
       cyl('worm outer thrust',Z,(z+2.0,z+3.25),x,y-5.70,2.05),
       box('X pawl',(-12.6,-11.0),(-17.15,-14.70),(z+.8,z+2.65)),
       box('X dog lifter',(-12.8,-10.6),(-18.3,-16.15),(z+2.1,z+4.35)),
       box('front limit pad',(16.60,17.40),(-15.85,-13.6),(8.75,10.70)),
       box('rear limit pad',(-8.95,-8.20),(-15.80,-13.55),(5.30,8.10))]
    # Rails project past the moving sleeve ends. Outer sleeves and tracks
    # overlap by design; actual guide surfaces need specified clearance.
    for y,z in [(-14.80,6.70),(5.40,6.75)]:
        s.append(cyl('X guide '+str(y),X,(-9.05,17.65),y,z,.85))
        for a,b in [(-10.60,-9.10),(17.70,19.10)]:s.append(cyl('guide support '+str((y,a)),X,(a,b),y,z,1.85))
    s.extend([box('nut fixed bracket',(-7.40,-5.75),(-12.80,-8.30),(ZS+1.55,ZS+3.75)),
              box('upper frame beam',(-7.4,2.1),(-9.5,-6.65),(ZS+2.5,ZS+4.0)),
              box('root crossbeam',(.65,2.65),(-8.75,3.40),(15.75,17.15)),
              box('front screw hanger',(15.60,16.70),(-13.45,-10.4),(ZS+1.1,ZS+3.10))])
    return s
def body3(ang=-90):
    a=[s for s in routed_body() if s[0] not in ('joint motor','joint pinion')]
    # Clock the motor and its whole mating sector together (not just motor).
    for s in routed_body():
        if s[0] in ('joint motor','joint pinion'):a.append(yaw(s,radians(ang)))
    a.append(box('direct spring pickup',(-7.25,-5.70),(-16.65,-15.9),(9.25,10.95)))
    return a
def stow(p,o,ss):return max((round(2*far(a,o),3),a[0]) for a in ss+tail(p))
def stages():
    s=slide3();p=pin()
    return [('C',[sweep(mx(a,REL),(-REL,0,0)) for a in s],p),('W',[mx(a,REL) for a in s],[sweep(a,(0,0,DZ)) for a in p]),('E',[sweep(mx(a,REL),(STROKE-REL,0,0)) for a in s],pin(DZ))]
def report3():
    z,x,b=zs(),xs(),body3();s=slide3();p=pin();f=z+x+b
    for n,a,pp in stages():
        pair(n+' slide v U+Z hardware',a,pp+z);pair(n+' slide v body',a,b)
        pair(n+' slide v X hardware',a,x)
    pair('both fixed actuators',x,z);pair('X vs body',x,b);pair('Z vs body',z,b)
    pair('U continuous vs X hardware and body',[sweep(a,(0,0,DZ)) for a in p],x+b)
    pair('U continuous vs own fixed Z incl intended fits and meshes',[sweep(a,(0,0,DZ)) for a in p],z)
    for pp in (33.,35.,36.,37.5):
        print('D, chosen centre',pp,centre(f+s+p+tail(pp)+[yaw(v,-pi/2) for v in sector()]))
    for pp in [35.,36.,37.5]:
        rigs={n:a+v+f for n,a,v in stages()}
        for i in 'CWE':
            for j in 'CWE':
                bad,mn=setscan(rigs[i],rigs[j],list(range(-15,16,3)),pp,.20,travel=STROKE)
                print('neighbours',pp,i+j,len(bad),bad[:6],mn)
        bad,mn=setscan([a for a in rigs['E']+p if not a[0].startswith(('hinge','joint pinion'))],tail(pp)+[yaw(a,-pi/2) for a in sector()],list(range(-15,16)),0.,.20)
        print('local articulated',pp,len(bad),bad[:6])
if __name__=='__main__':report3()
