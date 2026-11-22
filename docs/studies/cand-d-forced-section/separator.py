"""Take 49 local section. Right-handed mm, exploratory; Python standard library."""
from json import loads
from pathlib import Path
from math import asin, cos, hypot, pi, radians, sin, sqrt, tan


P0, NOSE, AFT, SLOT, HALF = 1.25, 15.40, -1.15, 8.77, 3.065
R, RF, K = 4.20, 1.45, tan(radians(28))
G, TV, LAG, TS = .15, .35, .40, .35
BACK, FRONT, SEAM = .08, .40, .10
OUTY, LOWZ, HIGHZ = 16., -16.20, 25.
XB, YB, ZB = 11.538278384125135, 9.526279441628827, 7.066987172218985
BOTTOM = (16.567077881337568, 0., -8.648011256569864)
ROOT, ELBOW, TIP = 25.25, 28.90, 30.65  # p37.5 fork, Kin-local x
U51=loads(Path(__file__).with_name('take51-face-v1.json').read_text())
V2=loads(Path(__file__).with_name('take51-face-v2.json').read_text())


def low(x): return 7.53675+K*(x-12.389796)
def top(x): return 23.95-.32*x
def side(x): return 8.26-.30*x
def work(nx):
    a = asin(nx)-radians(1.)
    return sin(a)-.23*cos(a)


def result(label, *vals):
    print(label, *(f"{v:.6f}" for v in vals))


def box(name, x, y, z):
    assert all(lo < hi for lo, hi in (x,y,z))
    return name, (x,y,z)


def parts(p, shut=0., carry=0., fixture=False):
    """Six actual rectangular solids. shut=0..1 at nose; carry after closure."""
    assert P0-1.50 <= p <= NOSE and 0 <= shut <= 1 and carry >= 0
    assert (not shut or p == NOSE) and (not carry or shut == 1)
    x = p+carry
    sy = side(p-LAG-TS)+G
    zl, zh = low(p-TV)-G, top(p-TV)+G
    vs, ss = (x-TV,x), (x-LAG-TS,x-LAG)
    w,bot,hi=(46.,-37.,62.) if fixture else (OUTY,LOWZ,HIGHZ)
    a = [box('lower', vs, (-w,w), (zl-16,zl)),
         box('upper', vs, (-w,w), (zh,zh+(44 if fixture else 9)))]
    ys = (1-shut)*(sy+.07)+shut*SEAM/2
    for s in (-1,1):
        yy = lambda l,h: tuple(sorted((s*l,s*h)))
        a += [box('side'+str(s), ss, yy(sy,sy+(43 if fixture else 13)), (bot,hi)),
              box('blade'+str(s), (x+BACK,x+FRONT), yy(ys,ys+4.55),
                  (low(NOSE)-.65,top(NOSE)+.65))]
    return a+[box('bottom apron',(x+.03,x+.23),(-w,w),(bot,-6.70))]


def overlap(a,b):
    return tuple(min(h,k)-max(l,j) for (l,h),(j,k) in zip(a,b))


def guides(p, shut=0., carry=0.):
    """One blade root/rail per side. Each through-bearing is four REAL strips."""
    a = parts(p,shut,carry)
    x = p+carry
    sy=side(p-LAG-TS)+G
    y0=(1-shut)*(sy+.07)+shut*SEAM/2
    zm=(low(NOSE)+top(NOSE))/2
    out=[]
    for s in (-1,1):
        yy=lambda l,h: tuple(sorted((s*l,s*h)))
        def block(n,l,h,i,j,b,t):
            return box(n+str(s),(x+l,x+h),yy(i,j),(zm+b,zm+t))
        root=block('root',-.30,.30,y0+4.12,y0+4.55,-2.,2.)
        rail=block('rail',-.26,.02,y0+4.25,y0+14.55,-1.,1.)
        assert min(overlap(root[1],a[3 if s==-1 else 5][1]))>0
        assert min(overlap(root[1],rail[1]))>0
        out.extend([root,rail])
        for dy in (5.25,8.00):
            lo,hi=sy+dy,sy+dy+.70
            assert y0+4.25 < lo < hi < y0+14.55
            sleeve=[block('backweb',-.55,-.30,lo,hi,-1.40,1.40),
                    block('frontweb',.06,.16,lo,hi,-1.40,1.40)]
            for z in (-1.40,1.04):
                sleeve.append(block('bridge',-.32,.08,lo,hi,z,z+.36))
            assert min(overlap(sleeve[0][1],a[2 if s==-1 else 4][1]))>0
            assert all(min(overlap(b,rail[1]))<=0 for _,b in sleeve)
            assert all(min(overlap(b,root[1]))<=0 for _,b in sleeve)
            out.extend(sleeve)
    return out


def section(r):
    # Bounds at the ACTUAL front face, not an infinite filled hood plane.
    gz, gt, gy = G+TV*K, G+.32*TV, G+.30*(LAG+TS)
    a = (2+gz)/2
    d = min(sqrt(r*r-a*a), r-LAG, sqrt(r*r-gy*gy-max(gz,gt)**2))
    nx = (d-FRONT)/r
    result('radius / front centre setback / closing edge nx / work',r,d,nx,work(nx))
    assert d > FRONT and work(nx)>0
    # In the closed slab every projected point is occupied, except for the
    # .10 split, within .05 of a blade. All supporting stock is x>=p-.40.
    worst = LAG+r-sqrt(r*r-(SEAM/2)**2)
    result('maximum aft surface reach / gap to fixed nose after +1.50',worst,1.5-worst)
    # From the FRONT side after closure, ball normals at any sheet, including
    # a rear cap or perimeter of a blade (no lateral escape at outer rim).
    closing_d = sqrt(r*r-(SEAM/2)**2)-LAG
    result('post-close worst exposed edge g',work((closing_d-FRONT)/r))
    assert work((closing_d-FRONT)/r)>0
    return work(nx)


def machines():
    print('exploratory; mm, N/N. No actuator or load capacity inferred.')
    initial, final = parts(P0), parts(NOSE,1)
    # Common cross-section in which all three sheet layers actually extend.
    # For all p: lower edge is highest at nose, upper edge lowest at nose.
    yl = min(OUTY,side(NOSE-LAG-TS)+G+13)
    zl = LOWZ
    zh = min(HIGHZ,top(NOSE-TV)+G+9)
    result('certified window +-y / lower z / upper z',yl,zl,zh)
    assert zl<low(P0-TV)-G and top(P0-TV)+G<zh
    assert low(NOSE-TV)-G-16 < -6.70
    result('terminal inner bars: half-y / lower z / upper z',
           side(NOSE-LAG-TS)+G,low(NOSE-TV)-G,top(NOSE-TV)+G)
    sy=side(NOSE-LAG-TS)+G
    assert SEAM/2+4.55>sy and low(NOSE)-.65<low(NOSE-TV)-G
    assert top(NOSE)+.65>top(NOSE-TV)+G
    # Axially disjoint for the entire cam law. Symmetric opposing pairs
    # remain separated; initial parked blade never sweeps through its hood.
    assert LAG>TV and BACK>0
    for a in (initial,parts(NOSE),final,parts(NOSE,1,1.5,True)):
        for j,(_,b) in enumerate(a):
            assert all(min(overlap(b,c))<=0 for _,c in a[j+1:])
    for p,shut in ((P0,0),(NOSE,0),(NOSE,1)):
        guides(p,shut)
    for r in (R,RF):
        section(r)
    # Conditional quasistatic reaction bounds per unit opposing +X load.
    g=min(section_work(r) for r in (R,RF))
    mult=hypot(1,.23)/g
    span=2.75
    e=hypot(1.04,.18)
    off=hypot(.52,(top(NOSE)-low(NOSE))/2+.65)
    arm=hypot(side(NOSE-LAG-TS)+G+5.60-SEAM/2,off)
    feed=2*sqrt(2)*.23*e/span
    s0=sqrt(2)*(1+2*arm/span)+2*off/2.
    result('guide span / arm / transverse offset / friction feedback',
           span,arm,off,feed)
    result('per Fx: normal sum / resultant / ideal guide normals / blade input',
           1/g,mult,mult*s0/(1-feed),mult*(1+.23*s0/(1-feed)))
    assert feed<1
    # Home overlap of a real solid registry return, NOT a bounding-box proxy.
    old = ((2.60,6.20),(-1.45,1.45),(-10.25,-7.80))
    ov = overlap(parts(2.90)[0][1],old)
    result('rejected 2.90 home face3 low return / lower bar overlap xyz',*ov)
    assert min(ov)>0
    # A uniform conformal shroud also meets the true crown, behind slot.
    d = low(7.5)*cos(radians(28))
    foot=(7.5-d*sin(radians(28)),0.,d*cos(radians(28)))
    result('hood roof foot on intact floor; available normal gap',*foot,d-R)
    assert AFT<foot[0]<SLOT and .15<d-R<.35
    result('0.15 running gap + 0.20 skin intrusion',.35-(d-R))
    # Three coaxial sleeves: inner wall at b_z+4.35, x=b_x+2; a point on
    # the bottom oblique R4.20 route. Top of sphere at that x from its
    # local generator already inside the proposed 0.30-thick sleeve.
    dx=2.; slope=-BOTTOM[2]/(22.5-BOTTOM[0]); rise=dx*slope
    depth=R-abs(4.50-rise)
    result('bottom boss coaxial R4.35/4.65 sleeve; stock point inside neck',depth)
    assert depth>0
    result('forward bar xmin / relieved xmin / minimum aft duct side gap',
           P0-LAG-TS,P0-1.50-LAG-TS,G-(.206941*hypot(1,.30)-.20))
    # Same X stage: these relative axial and height separators are invariant
    # through co-relief, nose dwell and carry. Rib/return need a Z exception
    # only for blade and bearing stock that projects forward of the X plane.
    for n,v,r,axis in U51['face_home']:
        assert not r and axis is None
        xmin=min(pt[0] for pt in v); zmax=max(pt[2] for pt in v)
        if n in ('centre','return'):
            assert xmin-P0>=.30-1e-12 and zmax<low(NOSE)-.65
            assert xmin-(P0+.23)>=.07-1e-12
        else:
            assert xmin-(P0+FRONT)>=1.95-1e-12
    result('U51 rib/return vs primary bar / bottom apron; other U vs frontmost metal',
           1.55-P0,1.55-P0-.23,3.60-P0-FRONT)


def section_work(r):
    a=(2+G+TV*K)/2
    d=min(sqrt(r*r-a*a),r-LAG,
          sqrt(r*r-(G+.30*(LAG+TS))**2-max(G+TV*K,G+.32*TV)**2))
    return work((d-FRONT)/r)


def installed():
    assert V2['boss']==U51['boss'] and V2['neck_at_mated_origin']==U51['neck_at_mated_origin']
    for n,v,r,axis in V2['face_home']:
        xmin=min(pt[0] for pt in v); zmax=max(pt[2] for pt in v)
        if n=='centre':
            result('v2 rib: X gap to main bars / apron (co-motion)',xmin-P0,xmin-P0-.23)
            assert xmin>P0+.23 and zmax<low(NOSE)-.65
        else:
            assert xmin>=4.80 and xmin-P0-FRONT>=3.15-1e-10
    _,v,r,axis=next(s for s in V2['joint'] if s[0]=='compound input 42T')
    cx,cy,zl=v[0]; zh=v[1][2]
    assert axis==[0,0,1] and zl<zh
    # A strictly interior witness in actual finite cylinder and positive bar.
    q=(P0-LAG-TS/2,cy,(zl+zh)/2)
    b=parts(P0)[4][1]
    assert all(lo<t<hi for t,(lo,hi) in zip(q,b))
    result('v2 home witness / radial gear penetration',*q,r-hypot(q[0]-cx,q[1]-cy))
    assert r-hypot(q[0]-cx,q[1]-cy)>1.3
    req=cx+r+LAG+TS+1.50
    result('co-relieved starboard bar: required home p / eye upper limit / deficit',
           req,15-7.5-R,req-(15-7.5-R))
    for p in (P0-1.50,3.30):
        assert side(p-LAG-TS)+G<cy<side(p-LAG-TS)+G+13
    result('v2 open rear at x=1.65: uncovered axial run home / relieved',1.65-P0,1.65-(P0-1.50))
    # Prove real rim stock at all four sides. Convex hulls contain the
    # segment joining their actual vertices. No filled rear face needed.
    rim=1.65
    for n,v,_,_ in V2['hood_blank']:
        zz=(low(rim),top(rim))
        corners=[]
        if n.startswith('front hood side'):
            y=(1 if n.endswith('1') and not n.endswith('-1') else -1)*side(rim)
            corners=[(rim,y,z) for z in zz]
        if n=='hood top':
            corners=[(rim,y,zz[1]) for y in (-side(rim),side(rim))]
        if n.startswith('slot floor(-1.15'):
            y=side(rim)*(-1 if n.endswith('-1)') else 1)
            corners=[(rim,t,zz[0]) for t in (0,y)]
        for q in corners:
            assert min(hypot(*(i-j for i,j in zip(q,b))) for b in v)<.000003
    gap=(rim-P0+1.5)*hypot(1,.30,K)+.000003
    result('v2 actual open rim: greatest distance from virtual side / R4.2 reserve',gap,R-gap)
    assert gap<R and side(NOSE)<R


def poses():
    # A full-tail, not point-probe, witness on the vertical slot wall.
    # Maps the stem-end to upper-fork-tip unit vector onto inward roof normal.
    dist=hypot(TIP-26,6.15)
    ux,uz=(TIP-26)/dist,6.15/dist
    sn,cs=sin(radians(28)),cos(radians(28))
    nx,nz=-sn,cs
    ax=(ux*nx-uz*cs,ux*nz-uz*sn)
    az=(uz*nx+ux*cs,uz*nz+ux*sn)
    # xz rotation here reverses xz orientation; also reverse y for a proper R.
    sy=1 if ax[0]*az[1]-az[0]*ax[1]>0 else -1
    p=(13.00,HALF-RF,low(13.00)+.20)
    def pose(q):
        x,y,z=q; x-=TIP;z-=6.15
        return p[0]+ax[0]*x+az[0]*z,p[1]+sy*y,p[2]+ax[1]*x+az[1]*z
    def below(q):
        x,y,z=pose(q)
        return (low(x)-z)*cs
    thick=[(26,0,0),(22.5,0,0),BOTTOM]+[
        q for s in (-1,1) for q in ((XB,s*YB,ZB),(16.5,s*YB,ZB),
                                     (16.5,s*YB,0.),(16.5,s*sqrt(54),0.))]
    # Exact support of the entire circle; all other segment extrema are endpoints.
    thick_gap=min([below(q) for q in thick]+[below((15.,0,0))-7.5*abs(ux)])-R
    thick_x=min([pose(q)[0] for q in thick]+[pose((15.,0,0))[0]-7.5*abs(ax[0])])-R
    f=[(x,0,s*z) for s in (-1,1) for x,z in ((ROOT,.85),(ELBOW,6.15),(TIP,6.15))]
    forkx=min(pose(q)[0] for q in f)-RF
    result('fork tip centre; thick-to-lower-plane gap; fork min x',*p,thick_gap,forkx)
    assert thick_gap>0 and min(thick_x,forkx)>P0+FRONT
    u=[q for _,vs,r,axis in U51['neck_at_mated_origin'] for q in vs]
    u+= [(26,0,0),(22.5,0,0)]+U51['boss']
    ugap=min([below(q) for q in u]+[below((15.,0,0))-7.5*abs(ux)])-R
    uxgap=min([pose(q)[0] for q in u]+[pose((15.,0,0))[0]-7.5*abs(ax[0])])-R
    result('U51 replacement: thick stock gap to roof / smallest material x',
           ugap,uxgap)
    assert ugap>0 and uxgap>P0+FRONT
    # Finite separating-axis certificates for this pose against the entire
    # imported U. Chord sag covers the circle; no reliance on point sampling.
    segs=[(pose(a),pose(b),R) for _,(a,b),_,_ in U51['neck_at_mated_origin']]
    segs+=[(pose((22.5,0,0)),pose((26,0,0)),R)]
    ring=[pose((15+7.5*cos(i*pi/48),7.5*sin(i*pi/48),0)) for i in range(96)]
    segs += [(a,b,R+7.5*(1-cos(pi/96))) for a,b in zip(ring,ring[1:]+ring[:1])]
    segs += [(pose(a),pose(b),RF) for j in (0,3) for a,b in zip(f[j:j+2],f[j+1:j+3])]
    dirs=[(i/s,j/s,k/s) for i in range(-3,4) for j in range(-3,4)
          for k in range(-3,4) if (s:=hypot(i,j,k))]
    dot=lambda a,b: sum(i*j for i,j in zip(a,b))
    sep=float('inf')
    for _,v,_,_ in V2['face_home']:
        axes=[(d,max(dot(d,q) for q in v)) for d in dirs]
        for a,b,r in segs:
            sep=min(sep,max(min(dot(d,a),dot(d,b))-h for d,h in axes)-r)
    result('fork witness: separating-plane gap to complete U51 v2 at home',sep)
    assert sep>0
    # All fork points have |y|<=HALF. Only tangencies on the vertical sides;
    # exclude the closed rear floor and the front skin for any high material.
    # Upper branch x intervals enlarge toward root; its only high portion
    # is near tip. Even both branches lie ahead of the slot's blind end or
    # below the floor: linear support-by-subsegments with real radii.
    for s in (-1,1):
        chain=[(x,0,s*z) for x,z in ((ROOT,.85),(ELBOW,6.15),(TIP,6.15))]
        for a,b in zip(chain,chain[1:]):
            for j in range(80):
                seg=[tuple((1-t)*u+t*v for u,v in zip(a,b))
                     for t in (j/80,(j+1)/80)]
                if min(below(q) for q in seg)>RF: continue
                xx=[pose(q)[0] for q in seg]
                assert min(xx)-RF>SLOT
    assert max(-below(q) for q in f)+RF<2*cs
    result('slot contact nx / axial friction work at nominal normal',0,-.23)
    # Every generator to stem anchor: farthest circle point is analytic.
    # For the whole *surface*, add its own ball radius.
    dr=max([hypot(x-26,y,z)+R for x,y,z in thick]+[11+7.5+R,dist+RF])
    result('all material reach from (26,0,0) / fork reach',dr,dist+RF)
    ur=max([hypot(x-26,y,z)+R for x,y,z in u]+[11+7.5+R,dist+RF])
    result('U51 whole-material reach from stem end',ur)
    # Exact maximum diameter: convex distance on segments, analytic farthest
    # point on the circular eye (max over all radii, not angular samples).
    gen=[(q,R) for q in u]+[(q,RF) for q in f]
    diam=max([15+2*R]+[hypot(7.5+hypot(x-15,y),z)+R+rad
                        for (x,y,z),rad in gen]+[
        hypot(*(i-j for i,j in zip(a,b)))+ra+rb for a,ra in gen for b,rb in gen])
    # Fixture B only: any generator going around these edges is already
    # laterally farther than the diameter from the entire original hood.
    reserve=min(46-side(AFT),low(AFT)+37,62-top(AFT))-diam
    result('U51 diameter / large finite fixture lateral separation reserve',diam,reserve)
    assert reserve>0 and side(NOSE-LAG-TS)+G+43>46 and top(NOSE-TV)+G+44>62
    result('anchored fork root offset; interior containment reserve',
           hypot(26-ROOT,.85),R-RF-hypot(26-ROOT,.85))


if __name__ == '__main__':
    machines()
    installed()
    poses()
