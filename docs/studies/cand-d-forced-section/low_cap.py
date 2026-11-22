"""Take 49 compact revision: telescoping roof tiles, cropped side plates."""
from itertools import product
from json import dump, loads
from math import dist, hypot, sqrt
from pathlib import Path
import sys

from separator import (FRONT, G, LAG, NOSE, P0, TS, V2, guides, low, parts,
                       section_work, side, top)


def shape(n, rows):
    return [n,rows,0,None]


def cuboid(n,b):
    return shape(n,list(product(*b)))


def solids(p,s=0.,c=0.):
    old=parts(p,s,c)
    stock=[cuboid(n,b) for n,b in old if n not in ('upper','side-1','side1')]
    x=p+c
    b=side(p-LAG-TS)+G
    zs=(-6.50,16.,19.,22.,25.)
    widths=(10.,10.,8.,5.,2.)
    for sign in (-1,1):
        yz=[(sign*b,zs[0]),(sign*b,zs[-1])]+[
            (sign*(b+w),z) for w,z in reversed(list(zip(widths,zs)))]
        stock.append(shape('cropped side'+str(sign),[(xx,y,z)
                           for xx in (x-LAG-TS,x-LAG) for y,z in yz]))
    zh=top(p-.35)+G
    spread=max(0.,(p-P0)/(NOSE-P0))*(25.-1.55-(top(NOSE-.35)+G))
    for j,(xl,xh) in enumerate(((-.35,-.18),(-.15,0),(.03,.19),(.22,.39))):
        z=zh+j*spread/3
        stock.append(cuboid('roof tile'+str(j),((x+xl,x+xh),(-9.,9.),(z,z+1.55))))
    for j,(n,bb) in enumerate(guides(p,s,c)):
        stock.append(cuboid(f'guide{j:02d}/{n}',bb))
    return stock


states=[('home',P0,0,0),('relieved',P0-1.5,0,0),('home_return',P0,0,0),
        ('at_nose',NOSE,0,0),('nose_closed',NOSE,1,0),
        ('terminal',NOSE,1,1.50),('optional_end',NOSE,1,2.65)]


def export():
    dump({'take':'49 compact B, replaces first compact stack',
          'units':'mm; mated head, unshifted local Z; +X eject',
          'stock':'Each [name, hull_vertices, 0, null] is real solid material. Guides are unchanged. No rotor, garage, stationary joint, X-drive, upper-tile drive or stationary blank included.',
          'phases':[['home','relieved','co-relief'],['relieved','relieved','park horn'],
                    ['relieved','home_return','return before cap spread'],
                    ['home_return','at_nose','track/expand cap'],
                    ['at_nose','nose_closed','close laterally at fixed X'],
                    ['nose_closed','terminal','closed carry'],
                    ['terminal','optional_end','optional extra carry']],
          'interpolation':'Corresponding vertices affine within each phase; home_return is required. Intersect solids at common time. Dwell keeps the same stock.',
          'states':{k:{'p':p,'shut':s,'carry':c,'face_X':p+c-P0,
                       'solids':solids(p,s,c)} for k,p,s,c in states}},
         sys.stdout,separators=(',',':'))
    print()


def tests():
    home=solids(P0)
    motor=(-20.936,-15.65,-22.489)
    def far(pt):
        return max((dist(q,pt),n,q) for n,v,_,_ in home for q in v)
    print('exploratory; actual home vertices vs supplied motor rim:',far(motor))
    print('old tall corner:',dist((1.25,16,32.812),motor))
    feet=list(product((-13.30,-10.70,9.70,12.30),(-9.75,-7.25,7.25,9.75),(-23.50,-22.15)))
    f=max((d,n,q,pt) for pt in feet for d,n,q in [far(pt)])
    def motor_dist(q):
        return hypot(hypot(q[0]+20.120151,q[2]+19.670)+3,
                     max(abs(q[1]+15.65),abs(q[1]-13.05)))
    m=max((motor_dist(q),n,q) for n,v,_,_ in home for q in v)
    print('four entire feet / updated motor cylinder: maximum cross-distances',f,m)
    assert max(f[0],m[0]) < 60
    c=(-5.7314,-.5403,-1.9922)
    subrad=max(far(c)[0],max(dist(c,q) for q in feet),motor_dist(c))
    print('common sphere for cap + four feet + X motor ONLY',c,subrad)
    assert subrad<29.90
    v3=loads(Path(__file__).with_name('take51-interface-v3.json').read_text())
    def zsup(row):
        n,v,r,a=row
        return max(q[2] for q in v)+r*(sqrt(max(0,1-a[2]**2)) if a else 1)
    znew=min(q[2] for _,p,s,carry in states for n,v,_,_ in solids(p,s,carry)
             if n in ('roof tile2','roof tile3') for q in v)
    for part in ('joint','own_tail_straight'):
        gap=znew-max(map(zsup,v3[part]))
        print('additional tile vs v3',part,'full sweep Z gap',gap)
        assert gap>3.45
    qroot=v3['own_tail_straight']
    root=next(s[1][0] for s in qroot if s[0]=='fork1')
    stem=next(s[1][-1] for s in qroot if s[0]=='heavy stem')
    print('v3 fork connection reserve',4.2-1.45-dist(root,stem))
    assert dist(root,stem)+1.45<4.2
    # Dual enclosing-radius witness. Positive weights, four occupied points.
    ct=(-5.90574144,-.29368827,-1.80294541)
    b=next(s[1][0] for s in qroot if s[0]=='heavy neck1/0')
    near=tuple(q+4.2*(q-t)/dist(b,ct) for q,t in zip(b,ct))
    cen=(-20.120151,-15.65,-19.67)
    d=hypot(cen[0]-ct[0],cen[2]-ct[2])
    rim=(cen[0]+3*(cen[0]-ct[0])/d,cen[1],cen[2]+3*(cen[2]-ct[2])/d)
    hood=(15.4,3.64,19.022)
    assert any(dist(q,hood)<1e-8 for n,v,_,_ in v3['hood_blank'] if n=='fore end' for q in v)
    pts=[near,hood,(12.30,9.75,-23.50),rim]
    w=[.18137544,.35189829,.12099926,1.-.18137544-.35189829-.12099926]
    mean=[sum(t*q[j] for t,q in zip(w,pts)) for j in range(3)]
    bound=sqrt(sum(t*dist(q,mean)**2 for t,q in zip(w,pts)))
    print('neck/hood/foot/motor: any enclosing diameter >=',2*bound,'weights',w)
    assert min(w)>0 and bound>30.05
    assert far(motor)[0]<60
    assert len(set(n for n,_,_,_ in home))==len(home)
    # The lower sheet meets the apron even at its highest position. At
    # its lowest, the upper edge still lies above the side-plate cutoff.
    assert parts(NOSE)[0][1][2][0]<-6.70 and low(P0-1.5-.35)-G>-6.50
    # Top sheet covers centre of aperture. At terminal all layers still
    # have x support >=p-.40; no uncovered vertical interval between tiles.
    z0=top(NOSE-.35)+G
    lap=1.55-(25-1.55-z0)/3
    print('terminal: top / tile overlap / min width (half) of guaranteed window',25.,lap,9.)
    assert lap>.16 and side(P0-1.50-LAG-TS)+G<9
    # At z<=16 cropped sides project to b+10. Above that, their
    # outer boundary is concave, piecewise linear. It suffices to check
    # the affine p endpoints at z=zh(p), where the cap takes over.
    def width(z):
        return min(10.,10.-(z-16)*2/3,8.-(z-19))
    for _,p,s,carry in states:
        sy=side(p-LAG-TS)+G
        assert sy+10>=14 and sy+width(top(p-.35)+G)>9
        ss=solids(p,s,carry)
        roof=[v for n,v,_,_ in ss if n.startswith('roof tile')]
        assert max(q[2] for v in roof for q in v)>=25.-1e-10
        assert max(q[0] for v in roof for q in v)<=p+carry+FRONT
        assert all(max(q[2] for q in u)-min(q[2] for q in v)>.16
                   for u,v in zip(roof,roof[1:]))
    envelope=[q for n,v,_,_ in qroot if n.startswith(('eye','fork','heavy')) for q in v]
    # Eye chord endpoints share the xy circle; exact ±7.5 centreline.
    yh=max(7.5,max(abs(q[1]) for q in envelope))
    zlo=min(q[2] for q in envelope); zhi=max(q[2] for q in envelope)
    margin=min(14-yh,zlo-(-16.2),16-zhi)
    print('v3 aligned generator clearance to conservative low-window rim',margin)
    assert margin>1.44 and section_work(1.45)>.08065
    # Rigid v3 mated necks + real ring + first fork. Segment maxima
    # occur at endpoints; the farthest circular generator is analytic.
    gen=[(q,r) for n,v,r,_ in qroot if n.startswith(('fork','heavy')) for q in v]
    diam=max([15+2*4.2]+[dist(i,j)+r+s for i,r in gen for j,s in gen]+[
        hypot(7.5+hypot(x-(15-v3['own_pitch']),y),z)+4.2+r for (x,y,z),r in gen])
    print('v3 diameter through first fork',diam)
    assert diam<35.94242
    # Bearing webs extend at most 8.70 from inner side; their z<=16.
    assert max(v[2] for n,bb in guides(NOSE,1) if 'web' in n for v in product(*bb))<16
    # Caps and blades share x intervals only on different z levels.
    assert z0+2*(25.-1.55-z0)/3 > top(NOSE)+.65
    # The stationary gear still cuts the lower sheet/apron at HOME.
    gear=next(row for row in V2['joint'] if row[0]=='compound input 42T')
    _,vv,r,_=gear
    q=(1.20,11.25,-11.75)
    lo=parts(P0)[0][1]
    assert all(l<v<h for v,(l,h) in zip(q,lo))
    print('v2 lower-sheet witness',q,'gear radial penetration',r-dist(q[:2],vv[0][:2]))
    assert r-dist(q[:2],vv[0][:2])>.79
    # Supplied Take 50 horn motor X (not the transverse X-stage motor).
    # Three independently moved parts contain points inside the motor
    # at HOME. For the convex side polygon, the axis is between its
    # inner edge and the actual interpolated outer edge at z=18.2.
    axis=(-11.95,18.20)
    cy,cz=axis; sy=side(P0-LAG-TS)+G
    assert sy < -cy < sy+width(cz)
    for n,x,y,z in [('cropped side-1',P0-LAG-TS/2,cy,cz),
                    ('blade-1',P0+.24,cy,cz),
                    ('guide00/root-1',1.335,-12.665,15.522)]:
        vs=next(v for name,v,_,_ in home if name==n)
        assert all(min(w[i] for w in vs)<c<max(w[i] for w in vs)
                   for i,c in enumerate((x,y,z)))
        assert -18.469035<x<10.230965
        reserve=3.-hypot(y-cy,z-cz)
        print('home horn-motor witness',n,(x,y,z),'motor radial depth',reserve)
        assert reserve>.21


if __name__=='__main__':
    export() if '--json' in sys.argv else tests()
