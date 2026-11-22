"""Replace the obstructing fore bridge. Nominal rigid geometry, not a rating."""
from pathlib import Path
from runpy import run_path
from math import cos,hypot,radians,sin,sqrt
import numpy as np
from backed_face import lands,beams


def geometry():
    g=run_path(str(Path(__file__).with_name('horn-package-take48.py')))
    b,n,f=lands();face=[g['poly'](name,list(map(tuple,p))) for name,p in f+beams(f)]
    return g,b,face


def coupled_tail(g,b,p=37.5,clock=0.):
    a=[s for s in g['tail48'](p,0.) if not s[0].startswith(('boss','heavy neck'))]
    for i,boss in enumerate(b):
        x=18.75
        rr=sqrt(7.5**2-(x-15)**2)
        path=[boss,(22.5,0.,0.)] if i==0 else [boss,(x,boss[1],boss[2]),(x,boss[1],0.),(x,np.sign(boss[1])*rr,0.)]
        for j,(v,w) in enumerate(zip(path,path[1:])):
            a.append(g['cap'](f'heavy neck{i}/{j}',tuple(np.array(v)-[p,0,0]),tuple(np.array(w)-[p,0,0]),4.2))
    return [g['yaw'](s,radians(clock)) if s[0].startswith('sector web') else s for s in a]


def joint(g,ang=75.,clock=0.):
    old=g['joint48']();box=g['box']
    keys=('hinge pin','stationary central knuckle','fixed hinge foot','compound lower bearing',
          'compound upper bush','compound shaft','compound input 42T','compound output 18T')
    m=['yaw gearmotor','yaw motor quill','yaw pinion 18T','yaw saddle','quill nose bush']
    x,y=-3.5+7.5*cos(radians(ang)),11.25+7.5*sin(radians(ang))
    moved=[g['move'](s,(x-3.70,y-13.35,0)) for s in old if s[0] in m]
    # Motor case and bush, upper compound bush and stationary knuckle are
    # mounted independently to the same rear frame. Sector is above the
    # base, not cut through an imaginary rigid two-axis clearance volume.
    fr=[box('rear spine',(-.70,.70),(-4.90,-3.75),(-15.85,1.40)),
        box('upper hinge elbow',(-3.75,.68),(-4.85,-3.80),(-1.80,1.20)),
        box('lower hinge elbow',(-3.85,.68),(-5.15,-3.82),(-16.25,-15.10)),
        box('lower bridge',(-4.85,-2.05),(-5.95,y+1.2),(-16.55,-15.35)),
        box('lower bush seat',(-4.85,-2.05),(9.85,12.65),(-15.60,-14.35)),
        box('lower case wing',(min(x-1.5,-4.8),max(x+1.5,-2.2)),(y-1.3,y+2.2),(-16.55,-15.35)),
        box('compound upper bridge',(-4.7,-2.3),(11.25,14.35),(-6.95,-5.65)),
        box('compound riser',(-4.7,-2.3),(17.05,18.15),(-15.7,-5.65)),
        box('compound cross',(-4.7,-2.3),(14.15,18.15),(-6.95,-5.65)),
        box('motor strap heel',(x-1.1,x+1.1),(y+2.85,y+4.15),(-8.9,-7.15)),
        box('motor post',(x-1.1,x+1.1),(y+3.8,y+4.95),(-16.35,-7.2)),
        box('motor base',(x-1.12,x+1.12),(y+1.2,y+4.95),(-16.55,-15.35))]
    fixed=[s for s in old if s[0] in keys and not s[0].startswith('compound')]
    fixed+=fr[:3]
    # Base plate swings about H. Keep direct overlap with the lower elbow.
    turned=[s for s in old if s[0] in keys and s[0].startswith('compound')]+moved+fr[3:]
    return fixed+[g['yaw'](s,radians(clock)) for s in turned]


D=2.40
CLOCK=12.
AZIMUTH=76.


def retracted_joint(g):
    return [g['mx'](s,-D) for s in joint(g,AZIMUTH,CLOCK)]


def shorter_tail(g,b,p=37.5):
    a=[]
    for s in coupled_tail(g,b,p,CLOCK):
        n,v,r,axis=s
        if n.startswith(('tail ','sector web','fork tip')):
            s=g['mx'](s,-D)
        elif n.startswith('fork'):
            s=(n,((23.15-p,v[0][1],v[0][2]),(v[1][0]-D,*v[1][1:])),r,axis)
        elif n=='heavy stem':
            s=(n,(v[0],(23.35-p,*v[1][1:])),r,axis)
        a.append(s)
    return a


def yaw_check(g,fixed,t,d=D):
    # Work in the old yaw routine's frame, equally translating both bodies.
    return g['ytest']([g['mx'](s,d) for s in fixed],[g['mx'](s,d) for s in t],1)


def hood(g,rear=1.65):
    # Intersect original front with x>=rear; close the cut except where
    # joined to the actual rotating-stock chamber. This blank is conservative.
    a=[g['clip'](s,rear,False) for s in g['roof48']()]
    panel=g['poly']('aft blank',[(x,sg*(8.26-.30*x),z) for x in (rear,rear+.20)
                  for sg in (-1,1) for z in (g['guardfloor'](x),23.95-.32*x)])
    return [s for s in a if s is not None]+[panel]


def main():
    import json
    g,b,face=geometry();t=shorter_tail(g,b);j=retracted_joint(g)
    inputs=Path(__file__).resolve().parents[1]/'cand-d-forced-section'
    v3=json.loads((inputs/'take51-interface-v3.json').read_bytes())
    for key,parts in [('joint',j),('own_tail_straight',t),('face_home',face)]:
        assert json.loads(json.dumps(parts))==v3[key],key
    cap=json.loads((inputs/'take49-low-cap-v3-sweep.json').read_bytes())
    bars=[]
    for a,b,phase in cap['phases']:
        ends=[cap['states'][key]['solids'] for key in (a,b)]
        assert [s[0] for s in ends[0]]==[s[0] for s in ends[1]]
        for (n,v,_,_),(_,w,_,_) in zip(*ends):
            bars.append(g['poly'](phase+'/'+n,v+w))
    no_mesh=[s for s in j if s[0] not in ('hinge pin','compound output 18T')]
    print('joint vs all four-tile phases',g['fastpair'](j,bars)[:1])
    for name,group in [('own joint (excludes intended bearing/mesh)',no_mesh),
                       ('separator',bars),('swept U-face',g['fp'](face)),('short hood',hood(g))]:
        print(name,'vs own tail through ±15 degrees',yaw_check(g,group,t)[:1])


if __name__=='__main__':main()
