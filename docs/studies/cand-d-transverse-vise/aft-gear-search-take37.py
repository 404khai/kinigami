"""Take 37 extra checks: actual gear-body witnesses, rear stop, lift/twist. Exploratory."""
from runpy import run_path
from pathlib import Path
d=run_path(str(Path(__file__).with_name('aft-drive-take37.py')))
globals().update({k:v for k,v in d.items() if not k.startswith('__')})

def gear_witness(c):
    j,i,m=gear(c)[2]
    # Test a common point strictly inside BOTH solids (not OD stock SAT).
    for dx,a,px,py in [(0.,5,15.40,7.15),(0.,15,14.95,5.95),
                        (3.,10,18.45,7.40),(3.,15,18.30,6.20)]:
        p=(px,py,0.);ax=plus((P+dx,0,0),theta(plus(m,(dx,0,0)),H,a))
        gj=jaw_depth(sub(p,(dx,0.,0.)));gm=3.-hypot(px-ax[0],py-ax[1])
        assert min(gj,gm)>0
        print('p/yaw, witness at z0, inside home jaw & next R3 motor',P+dx,a,p,round(gj,4),round(gm,4))
    # Negative-z cell face actual conservative if specified cell is solid;
    # use trial rectangular pack and Ø6 body, not a purchased teardown.
    p=(-11.90,10.54,-17.9);axis=plus(m,(3.,0,0));g=3.-hypot(p[0]-axis[0],p[1]-axis[1])
    print('37.5 local motor v unchanged cell, point and depth in Ø6',p,round(g,4))
    assert g>0 and -12.35<p[0]<8.35 and -14.30<p[1]<16.35 and -21.75<p[2]<-16.35
    # A point inside the BORE PIN (not merely in its bearing OD) and the
    # specified round root. Use full 3D capsule projecting actual spine.
    root=next(s for s in tail(15-P) if s[0]=='root1');u,v=yaw(root,radians(-15))[1]
    for dx in [0.,3.]:
        best=(-100.,)
        for k in range(101):
            p=plus(u,mul(k/100.,sub(v,u)));r=hypot(p[0]-i[0]-dx,p[1]-i[1])
            best=max(best,(1.20+1.05-r,k,p))
        print('I shaft vs yaw -15 root (sum radii minus radial axis distance)',P+dx,best)
def rear_stop(c):
    r=next(s for s in tail(15.) if s[0]=='rear cap')
    for a in [5,10,90]:
        x=proj(arc(r,c,a),X)[0]; shift=4.15+.20-x
        print('rear park to clear full crown OUTER BOX only angle/xmin/additional stroke',a,round(x,5),round(shift,5))
    pt=theta((4.60,.48,0.),c,10);require=4.15+.20-pt[0]
    print('actual 10 degree witness alone minimum rear move',require)
    # Rear carriage cannot simply overhang its specified supported travel.
    # Nut rear and bevel front already only .30 apart in x, concentric yz.
    print('10 degree 1.00 mm rear park: blade face, master-carriage end, nut rear',4.15-1.,-9.70-1.,2.20-1.)
    print('master guide rear, bevel face, remaining nut-to-bevel x gap',-9.85,1.90,2.20-1.-1.90)
    gg=-(pt[1]-c[1])-abs(pt[0]-c[0]);print('adverse flat at witness, mu1, Nmm/N',gg)
    # Illustrative only: residual opening torque after independent losses is B.
    print('10 deg face if 50 Nmm verified residual: necessary nominal flat force cap N',50./-gg)
def alt(c):
    jaw=stowed(c);L=21.5
    peak=max(proj(move(arc(s,c,q),mul(L,Y)),Y)[1] for q in range(91) for s in jaw)
    print('vertical lift then twist: raised axis y, sampled peak y, terminal xmax',
          c[1]+L,peak,max(proj(move(arc(s,c,90),mul(L,Y)),X)[1] for s in jaw))
    print('no-shared-load 5 mm spaced guide couple N, top stop load Nmm',85.*17/5,85.*17)
    print('arm end reach above deck at 21.5 lift, nominal cap vs flat x gap during pure lift',3.50+L,4.55-4.15)
def frames(c):
    f=frame(c);e=eject(inventory(0));m=stowed(c)
    # Exclude stationary designed union with the cheek only. Remaining
    # negative gaps are unresolved; fulcrum intersection handled as intended.
    for title,u,v in [('web and foot vs other stock',f,[s for s in e if s[0]!='V-cheek']),
                      ('compact landing vs arms', [seat(c,90)], [arc(s,c,a) for a in range(91) for s in m[:-1]])]:
        print(title,clear(u,v))
    fs=[box('floorpad',(x-1.50,x+1.50),(-23.,-21.),(z-1.30,z+1.30)) for x,z in product((-12.6,9.),(-8.2,8.2))]
    print('four trial foot pads: lowest y at -15/0/+15', [round(min(proj(yaw(s,radians(a)),Y)[0] for s in fs),3) for a in [-15,0,15]])
    # For the central compact-core seat, tailside z separation for the arms,
    # but expanded jaw still has unmasked rear surface outside z+-5.188.
    print('actual full jaw terminal widest z, compact seat z',proj(m[-1],Z),proj(seat(c,90),Z))
    print('load: outer flat point 85 N normal-only vs optimistic 30mNm*76.8*.7 output',85*(17.772705-c[0]),30*76.8*.7)

def arcbox(s,c,a,b):
    # Endpoint chord hull, enlarged by maximum arc sagitta. z-normal disk
    # primitives stay unchanged; non-z cylinders would need a separate bound.
    assert s[3] in (None,Z)
    va=arc(s,c,a)[1]+arc(s,c,b)[1]
    R=max(hypot(p[0]-c[0],p[1]-c[1]) for p in s[1])
    return poly(s[0],va,s[2]+R*(1-cos(radians((b-a)/2))))
def prefix(c,dx):
    full=[sh(arcbox(s,c,q,q+5),dx) for q in range(0,90,5) for s in stowed(c)[:3]+[wide()]]
    cheek=next(s for s in inventory(dx) if s[0]=='V-cheek')
    # All trimmed profiles stay strictly inside their Take28 outer cylinder.
    # Seat is stationary; scan its approach to preceding cheek separately.
    for title,l,r in [('preceding cheek vs whole jaw/arms prefix',[cheek],full),
                      ('preceding cheek vs compact terminal seat',[cheek],[sh(seat(c,90),dx)]),
                      ('preceding jaw/arms sweep vs next cheek',full,[cheek])]:
        bad,mn=setscan(l,r,list(range(-15,16)),P+dx,.2,travel=15.)
        print('pitch',P+dx,title,'unseparated',len(bad),'minimum capped lower bound',mn)

if __name__=='__main__':
    c=(-2.,-4.,0.);gear_witness(c);rear_stop(c);frames(c);alt(c);prefix(c,0.);prefix(c,3.)
