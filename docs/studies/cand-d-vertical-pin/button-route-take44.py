"""Forward-set base, instrumented stalk, isolated guide and outboard screw."""
from pathlib import Path
from runpy import run_path
d=run_path(str(Path(__file__).with_name('button-face-take44.py')))
globals().update({k:v for k,v in d.items() if not k.startswith('__')})
def face2():
    a=[]
    for s in face():
        n=s[0]
        if n.startswith('beam'):
            x,y,z=(proj(s,k) for k in (X,Y,Z))
            if n in ('beam 1.0','beam 2.0'):
                yy=(.80 if n=='beam 1.0' else -.80)
                y=(y[0]+yy,y[1]+yy)
            if n in ('beam 1.1','beam 2.1'):
                # Keep inward flank off the torus; not a reduction to a thin finger.
                yy=.56 if n=='beam 1.1' else -.56;y=(y[0]+yy,y[1]+yy)
            s=box(n,(5.12,x[1]),y,z)
        elif n=='lower bridge':s=box(n,(5.05,7.60),(-13.85,13.85),(-11.90,-8.50))
        elif n.startswith('stripper column'):s=box(n,(.4,2.85),(-1.45,1.45),(-8.35,1.45))
        elif n=='force stalk':s=box(n,(2.90,5.25),(-9.0,-5.80),(-11.8,-9.00))
        elif 'pillar' in n or 'bridge' in n:
            sg=-1 if '-1' in n else 1
            y=tuple(sorted(v*sg for v in ((10.80,13.85) if 'pillar' in n else (5.4,13.85) if 'upper' in n else (11.0,14.10))))
            s=box(n,(5.05,7.15),y,proj(s,Z))
        a.append(s)
    a+=[box('stripper low return',(.4,6.20),(-1.45,1.45),(-10.25,-7.80))]
    return a
def mover2():
    a=[]
    for s in mover():
        n=s[0]
        if n=='moving 3 rail':s=move(s,(0,0,-1.0))
        elif n=='rail backing spar':s=box(n,(-13.85,20.90),(-8.60,-5.20),(-14.50,-12.80))
        elif n=='series bridge':s=box(n,(-3.80,1.00),(-18.85,-7.50),(-12.75,-10.10))
        else:s=move(s,(0,-4.40,1.35))
        a.append(s)
    return a+[box('stalk rear support',(.50,3.15),(-9.20,-5.5),(-13.10,-8.95))]
def xd2():
    a=[]
    for s in xdrive():
        n=s[0]
        if n in ('MGN3H fixed block','block mounting foot'):s=move(s,(0,0,-1))
        elif n=='foot return':s=box(n,(2.10,4.85),(-4.8,-3.55),(-19.1,-14.55))
        else:s=move(s,(0,-4.40,1.35))
        a.append(s)
    return a
def bf(p=0):
    a=[]
    for s in tucked_tail(p):
        if s[0] in ('metal neck1','metal neck2'):
            sg=1 if s[0]=='metal neck1' else -1
            t=radians(65*sg)
            b=plus(BOSS[sg if sg==1 else 2],(-p,0,0))
            s=cap(s[0],(15-p+R*cos(t),R*sin(t),0),b,2.0)
        a.append(s)
    return a
def zz2():
    a=[]
    for s in zfixed():
        n=s[0]
        if n.startswith(('rack','Z final','Z motor','Z saddle','Z torque','Z end')):
            s=move(s,(-3.0,-2.20,2.50))
        a.append(s)
    a+= [cyl('lost motion face cam',X,(-.1,5.95),(-21.75,13.9),4.05),
         box('bolt follower bridge',(3.75,5.90),(-20.0,.75),(17.85,19.95)),
         box('X pawl cam follower',(-12.95,3.85),(-22.25,-20.55),(12.85,14.8)),
         box('X pawl vertical link',(-12.80,-11.2),(-22.35,-20.85),(-10.90,14.25))]
    return a+roofs()
def b2():
    a=[]
    for s in button():
        if s[0]=='rack':s=box('rack',(5.35,9.55),(-19.65,-16.9),(-1.22,17.85))
        if s[0]=='folded bridge':s=poly(s[0],[(x,y,z) for x,y in ((10,-3.85),(14.72,-3.85),(9.55,-19.65),(5.35,-19.65)) for z in (15.65,18.10)])
        a.append(s)
    return a
def state(n):
    p=face2()+mover2()
    return ([sweep(mx(a,REL),((END if n=='E' else 0 if n=='C' else REL)-REL,0,0)) for a in p],
            [move(s,(0,0,LIFT)) if n=='E' else sweep(s,(0,0,LIFT)) if n=='W' else s for s in b2()],
            [dog(n!='C')])
def whole():return xd2()+zz2()+tucked_joint()+electr()
def shift(A,k):return [move(s,(0,0,k)) for s in A]
def tailshift(p,k):
    a=[]
    for s in bf(p):
        n=s[0]
        if n.startswith(('eye','boss','metal neck','main stem')):s=move(s,(0,0,k))
        if n in ('fork1','fork-1'):s=cap(n,plus(s[1][0],(0,0,k)),s[1][1],s[2])
        a.append(s)
    return a
def report():
    ex=tucked_joint()+electr();Zs=zz2()
    for k in (0,-5,-7):
        a=tailshift(P,k);b=shift(face2()+mover2()+b2()+xd2()+Zs+[dog(0)],k)
        print('offset joint v fitted tail',k,scan(tucked_joint(),a,0,ex=mated)[0],
              'electronics',scan(electr(),a,0)[0])
        print('offset stock diameter',k,centre(a+b+ex),'bottom',min((proj(s,Z)[0],s[0]) for s in a+b+ex))
    for n in 'CWE':
        p,u,d=state(n);v=p[:len(face2())]
        for label,A,B in [('face v joint and body',v,ex),('face v roof and pin incl fixed support',v,roofs()+u+d+Zs[:36]),('face v ALL Z',v,Zs+u+d),('face v X',v,xd2()),('U v X',u,xd2()),('U v joint and body',u,ex)]:
            q=pair(A,B);print(n,label,sum(v[0]<0 for v in q),q[:5])
    print('face v ring/neck closed',pair(face2(),[s for s in bf(0) if s[0].startswith(('eye','metal neck','main stem'))])[:6])
    print('endpoints joint v electronics',pair(tucked_joint(),electr())[:3])
    f=whole()
    for pp in (36.,37.5):
        for n in 'CE':
            for m in 'CE':
                a,u,d=state(n);b,v,e=state(m)
                best,bad=scan(a+u+d+f,b+v+e+f,pp,3,END)
                print('routed neighbours',pp,n+m,len(bad),best,bad[:3])
        p,u,d=state('E')
        best,bad=scan(p+u+b2()+xd2()+zz2()+d,bf(pp),0)
        print('routed own articulated',pp,len(bad),best,bad[:4])
if __name__=='__main__':report()
