"""Take39 refined folded head: real closed/swept sections and conditional extraction."""
from pathlib import Path
from runpy import run_path
D1=run_path(str(Path(__file__).with_name('eye-fold-take39.py')))
globals().update({k:v for k,v in D1.items() if not k.startswith('__')})
def refinedupper():
    out=[]
    for s in upper():
        if s[0] in ('H bridges','spring stop','upper base tie','normal-open hold dog','force foil','cam follower sensors'):continue
        if s[0].startswith('foot'):s=move(s,(0,0,-.30))
        if s[0].startswith('base rail'):s=move(s,(0,0,-.20))
        out.append(s)
    out.extend([box('dual H bridge',(-8.3,1.2),(-2.8,5.0),(17.15,19.2)),
                box('power and current monitor',(2.1,9.0),(-4.0,4.1),(17.35,19.20)),
                box('spring unload pickup',(4.5,8.5),(-16.6,-14.9),(6.5,9.0)),
                # OD includes clearance, sheet thickness, both end faces. Full
                # guard disk used as outer bound; gear is free INSIDE the can.
                cyl('Y wheel can',Y,(-23.45,-21.30),7.50,9.50,6.70),
                cyl('Y pinion can',Y,(-23.45,-21.30),-1.30,13.40,4.37),
                cyl('12-notch lock drum OD',Y,(-21.70,-19.40),7.50,9.50,6.30),
                box('brake pawl body',(8.3,12.4),(-20.6,-18.6),(14.4,16.4)),
                box('pin witness optical head',(14.45,15.65),(14.62,14.88),(1.75,3.65)),
                box('dog spring lifter',(7.0,13.0),(-20.6,-18.6),(16.2,18.8))])
    return out
def refinedmoving(t,cm):
    x=close+cm
    out=[s for s in moving(t,cm) if s[0] not in ('carrier tie','spring pocket','cam track')]
    for sg in [-1,1]:
        y=12.95*sg
        out.append(box('carrier side link '+str(sg),(x-12.2,x+1.1),(y-1.15,y+1.15),(4.85,7.1)))
    out.append(box('aft carrier tie',(x-12.2,x-10.1),(-14.1,14.1),(4.85,7.1)))
    # Compressive series element between powered cap and carrier, with
    # a hard positive RETURN shoulder. Input and output x positions differ.
    z=9.15;y=-13.0;dx=max(0,6.-t)*3.20/6.;xl=x-11.7;xr=(C-11.7+11.50)-dx
    out += [cyl('series spring OD',X,(xl,xr),y,z,2.55),
            box('spring carrier seat',(xl-.85,xl+.25),(y-2.65,y+2.65),(5.05,11.80)),
            box('powered spring cap',(xr,xr+1.0),(y-2.65,y+2.65),(6.50,12.05)),
            box('powered draw lug',(xr-.65,xr+1.0),(-16.8,-14.3),(8.7,13.9)),
            box('return shoulder',(xl-1.05,xl-.40),(-15.8,-14.8),(7.3,10.45)),
            box('draw cam stock',(9.0-dx,14.95-dx),(-18.9,-10.5),(11.35,13.50)),
            box('brake flag',(10.-dx,11.8-dx),(-17.9,-16.8),(13.3,14.6))]
    return out
def refinedlower():
    es,em=lower();f=[]
    for s in es:
        if s[0] in ('X transmission web','X pinion','X rear thrust','X motor','X mount'):s=mx(s,3.9)
        if s[0]=='X eject screw':s=cyl(s[0],X,(-12.65,16.2),-6.2,-13.5,1.0)
        if s[0]=='X nose bush':s=cyl(s[0],X,(14.25,16.25),-6.2,-13.5,2.2)
        if s[0] in ('X master rail','X roll rail','lower plate'):s=poly(s[0],[(min(x,15.65),y,z) for x,y,z in s[1]])
        f.append(s)
    f+=[box('front eject stop',(13.80,14.55),(-4.5,-3.5),(-13.70,-12.00)),
        box('rear eject stop',(-1.45,-.70),(-4.5,-3.5),(-13.70,-12.00)),
        cyl('X wheel can',X,(-13.0,-11.02),-6.2,-13.5,6.90),
        cyl('X pinion can',X,(-13.,-11.02),2.9,-13.5,3.57)]
    return f,em
def envelope(s):
    # Feasible alternative centre, not a claim of optimality.
    for o in [O,(.095,-1.482,-.1195)]:
        print('closed fixed-centre dimension',o,max((round(2*far(k,o),4),k[0]) for k in s))
def own_tail(p):
    t=tail(C-p)
    return [s if not s[0].startswith('tail clevis') else hull(s[0],s[1][0],(H[0],H[1],s[1][1][2]),s[2]) for s in t]
def test():
    lo,em=refinedlower();u=refinedupper();f=u+lo+kept();cl=refinedmoving(0,0);op=refinedmoving(32.05,delta)
    h=hinge();jf=[s for s in h if not s[0].startswith('joint sector')]
    print('13mm eject: face xmax',7.05+13,'nominal gap to fixed metal mouth',7.05+13-18.6)
    for p in [33.,36.]:
        t=own_tail(p);envelope(f+cl+em+h+t)
        for n,a in [('C',cl),('O',op)]:
            for n2,b in [('C',cl),('O',op)]:
                l=a+f+jf+([sweep(s,(13,0,0)) for s in em] if n=='O' else em)
                r=b+f+jf+([sweep(s,(13,0,0)) for s in em] if n2=='O' else em)
                bad,mn=setscan(l,r,list(range(-15,16)),p,.20,travel=13.)
                print('refined neighbours',p,n+n2,len(bad),bad[:5],mn)
        bad,mn=setscan([s for s in f+cl+em if s[0]!='joint pin'],t+[s for s in h if s[0].startswith('joint sector')],list(range(-15,16)),0.,.20)
        print('own articulated tail, sector',p,len(bad),bad[:6])
    summary('refined cross-deck fixed',u,lo+em+kept());summary('full eject vs open upper',op+u,[sweep(s,(13,0,0)) for s in em])
    # No box intersection equals a material interpenetration. Check separate
    # physical arm/eye against the actual spring/ram walls below.
    paddle=tail(15.)
    bad,mn=setscan([s for s in f+op if not s[0].startswith(('V0/','V1/','V2/'))],[sweep(s,(13.,0,0)) for s in paddle],[0.],0.,.20)
    print('aligned eye+registry full ejection vs open head (six seat flanks excluded)',bad[:8],mn)
    summary('refined open actuator vs cap/force pickup',op,u)
    summary('refined closed actuator vs cap/force pickup',cl,u)
    # Deployed yaw through a stationary horizontal floor leaves Z invariant.
    print('z lowest fixed pads / stock other than feet',min(proj(s,Z)[0] for s in f),min(proj(s,Z)[0] for s in f+em+h+cl+op if not s[0].startswith('foot')))
def motorwitness():
    for p,de,stroke,j in [(33,2.,13,15),(36,1.,15,15),(37.5,0.,15,15)]:
        q=(6.7+stroke,.73,-12.45);v=plus(H,rot(sub(q,plus(H,(p+de,0,0))),radians(-j)))
        z=min(v[0]+14.75,13.95-v[0],3.-hypot(v[1]-2.90,v[2]+13.50))
        print('first refold true rib v next Ø6, pitch/departure/eject/yaw/point/depth',p,de,stroke,j,q,z)
    # Independent of ring or reaching a long stroke: both fixed axes with
    # p33 at zero yaw. The second wheel web is solid r=1.15..5.70.
    # Offset point at r1.55 inside front journal annulus (r1.08..2.2).
    q=(17.20,-4.65,-13.50)
    print('p33 fixed no-yaw common point own front bush/next wheel web',q,'next x',q[0]-33)
    assert 16<q[0]<18.25 and -16.5<q[0]-33<-15.2 and 1.15<1.55<2.2
    # Independently of exterior drives, crosshead nose may enter X motor.
    p=(6.2,.75,-12.40); depth=3.-hypot(p[1]-2.90,p[2]+13.50)
    assert -.7<p[0]<6.8 and -.8<p[1]<.8 and -12.5<p[2]<-10.1 and depth>.55
    print('lower Ø6 motor vs real eject axial rib closed (both refolds)',p,depth)
    print('retained motor vs real locked pin axis',3.-abs(close-12.60))
    # Three smooth point contacts pairs on a perfectly axisymmetric torus
    # can never carry M_y about C by normals alone. Registry balls are
    # deliberately nonaxisymmetric; compute dimensionless full rank separately.
    mat=[]
    for a in [90,210,330]:
        radial=(0,cos(radians(a)),sin(radians(a)));t=(0,-radial[2],radial[1])
        for sg in [-1,1]:
            n=mul(1/sqrt(2),plus(X,mul(sg,t)));mat.append(list(n)+list(D['cross'](radial,n)))
    det=1.
    for i in range(6):
        k=max(range(i,6),key=lambda j:abs(mat[j][i]))
        if k!=i:mat[i],mat[k]=mat[k],mat[i];det=-det
        h=mat[i][i];det*=h
        for j in range(i+1,6):
            r=mat[j][i]/h;mat[j]=[x-r*y for x,y in zip(mat[j],mat[i])]
    print('registry normalized nominal rank test determinant',det)
if __name__=='__main__':motorwitness();test()
