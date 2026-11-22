"""Routed Take 42 alternative. Imports geometry without performing official tests."""
from pathlib import Path
from runpy import run_path
d=run_path(str(Path(__file__).with_name('fixed-z-take42.py')))
globals().update({k:v for k,v in d.items() if not k.startswith('__')})
STROKE=15.25; YM=-13.85; ZM=6.80; YS=-13.10; ZS=ZM+sqrt(6.45**2-(YS-YM)**2)
def route_z():
    a=zdrive(); out=[]
    old=(8.15,10.2075);new=(15.50,4.20)
    oldm=(old[0]+4.6,old[1]-sqrt(7.7**2-4.6**2));newm=(14.,4.2-sqrt(7.7**2-1.5**2))
    for s in a:
        n=s[0]
        if n.startswith(('B ','Z gear cover')):s=move(s,(0,new[0]-old[0],new[1]-old[1]))
        if n.startswith(('Z motor','Z gearmotor')):s=move(s,(0,newm[0]-oldm[0],newm[1]-oldm[1]))
        if n=='main bulkhead':s=box(n,(-2.95,-1.75),(-6.25,3.10),(8.90,11.15))
        out.append(s)
    return out
def route_face():
    a=[s for s in slide() if not s[0].startswith(('slide bar','translating screw','thrust bridge','roll link','outer tie'))]
    # Route screw above the -Y outboard land, not across pin or passive eye.
    a += [cyl('translating screw',X,(-18.80,10.58),YS,ZS,1.25),
          box('thrust collar',(9.78,11.0),(YS-1.50,YS+1.50),(ZS-1.45,ZS+1.5)),
          box('outboard upstand',(9.78,11.0),(-14.65,-12.96),(3.70,ZS+.45)),
          box('master pull link',(-.65,1.12),(-15.55,-13.85),(-4.42,4.25)),
          box('master slide bar',(-27.20,1.05),(-15.55,-13.75),(-1.60,.20)),
          box('roll link',(-.65,1.12),(4.05,5.95),(3.48,7.95)),
          box('roll slide bar',(-25.35,.82),(4.60,6.30),(6.30,8.00))]
    # Upper/lower rims meet the outboard pull link, not a thin single root.
    a.extend(box('outboard spar '+str(z),(-.65,11.0),(-14.65,-13.10),(z-.60,z+.60)) for z in [-4.,4.])
    a.append(box('tip strut',(9.78,11.0),(-14.65,-13.40),(-4.60,4.60)))
    return a
def route_x():
    a=[]
    for n,h,r in [('X rear nut race',(1.10,3.95),3.05),('X nut gear',(4.0,5.8),5.10),
                  ('X front nut race',(5.85,7.6),3.0),('X clutch',(-.55,1.05),4.15),
                  ('X brake drum',(-1.65,-.6),3.55)]:
        a.append(cyl(n,X,h,YS,ZS,r))
    for n,h,r in [('X gearmotor',(-24.90,3.80),3.),('X pinion',(3.95,5.85),1.95),
                  ('X motor saddle',(-16.4,-14.8),3.45)]:
        a.append(cyl(n,X,h,YM,ZM,r))
    a += [box('X dog',(-1.7,-.6),(-17.2,-15.3),(ZS+.35,ZS+2.45)),
          box('X dog lifter',(-2.3,-.30),(-18.8,-16.65),(ZS+.30,ZS+3.30)),
          box('torque pickup',(-.60,.80),(-10.45,-8.85),(ZS+1.90,ZS+3.8))]
    # Fixed bearing-length gibs. End at -4: relief doesn't run a bridge into a guide.
    for j,(y,z,w,zr,xx) in enumerate([(-14.65,-.70,.90,.90,(-11.70,-3.90)),(5.45,7.15,.85,.85,(-9.80,-3.90))]):
        for k in [-1,1]:
            a.append(box('gibY'+str((j,k)),xx,(y+k*(w+.64)-.50,y+k*(w+.64)+.50),(z-zr-.62,z+zr+.62)))
            a.append(box('gibZ'+str((j,k)),xx,(y-w-.1,y+w+.1),(z+k*(zr+.64)-.50,z+k*(zr+.64)+.50)))
    # Stiff bridge links the stationary thrust housing to forked sleeve support.
    a += [box('upper frame beam',(1.05,3.75),(-13.10,3.42),(15.70,17.10)),
          box('nut holder',(1.13,3.73),(-15.95,-13.25),(ZS+.30,16.95)),
          box('travel stop',(11.18,12.28),(-16.95,-15.55),(ZS+.75,ZS+2.1))]
    return a
def routed_body():
    a=[]
    for s in body():
        if s[0]=='slide actual switch':s=box('slide direct pickup',(1.65,3.7),(-17.9,-16.1),(2.25,4.60))
        if s[0]=='series load pickup':continue
        if s[0].startswith('foot'):s=move(s,(-.65 if s[1][0][0]>0 else .65,0.,0.))
        a.append(s)
    return a
def centre(s):
    o=O
    for h in (.4,.2,.1,.05,.02,.01,.005):
        es=[a for a in s if far(a,o)>max(far(v,o) for v in s)-2] if False else s
        for i in range(30):
            m=max(far(a,o) for a in es); vs=[a for a in es if far(a,o)>m-2*h*sqrt(3)-1e-8]
            v=min((max(far(a,d) for a in vs),d) for d in [plus(o,(x*h,y*h,z*h)) for x,y,z in product((-1,0,1),repeat=3)])
            if v[1]==o:break
            o=v[1]
    return o,sorted([(round(2*far(a,o),4),a[0]) for a in s],reverse=True)[:5]
def report():
    s=route_face();z=route_z();x=route_x();b=routed_body();p=pin()
    stages=[('locked',s,p),('relief',[sweep(mx(i,REL),(-REL,0.,0.)) for i in s],p),
            ('withdraw',[mx(i,REL) for i in s],[sweep(i,(0.,0.,DZ)) for i in p]),
            ('eject',[sweep(mx(i,REL),(STROKE-REL,0,0)) for i in s],pin(DZ))]
    for n,a,pp in stages:
        pair(n+' slide vs U+stationary roof',a,pp+z)
        pair(n+' slide vs body',a,b)
    pair('Xdrive vs Zdrive',x,z);pair('Xdrive vs body',x,b);pair('Zdrive vs body',z,b)
    pair('U deploy vs Xdrive+body',[sweep(i,(0.,0.,DZ)) for i in p],x+b)
    for pp in (33.,35.,36.,37.5):
        print('trial sphere',pp,centre(s+x+z+b+p+tail(pp)+sector()))
    f=x+z+b
    for pp in [33.,36.,37.5]:
        rigs=[a+gg+f for n,a,gg in stages]
        for a,aa in [('C',rigs[1]),('E',rigs[3])]:
            for bb,bbx in [('C',rigs[1]),('E',rigs[3])]:
                bad,mn=setscan(aa,bbx,list(range(-15,16,3)),pp,.20,travel=STROKE)
                print('neighbours',pp,a+bb,len(bad),bad[:6],mn)
        bad,mn=setscan([k for k in rigs[-1]+p if not k[0].startswith(('hinge','joint pinion'))],tail(pp)+sector(),list(range(-15,16)),0.,.2)
        print('own articulated tail incl sector',pp,len(bad),bad[:6])
if __name__=='__main__':report()
