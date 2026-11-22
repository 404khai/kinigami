"""Re-seat the actual cell and MCU against the named Take 44 stock, mm."""
import argparse
from itertools import product
from math import cos, pi
from pathlib import Path
from runpy import run_path
import numpy as np
from box_search import certificate, project, axes, search, slices, stock
from slot_stock import moving_slots


def hinge(s,H,angles,p=0.,depart=0.,inverse=False):
    # Positive transforms are H + (p+d)X + R(s-H); inverse transforms
    # rotate the complete (p+d) offset too. Convex overbound; both adjacent
    # bodies can move. Non-vertical disk radius becomes a ball if rotated.
    pts=np.asarray(s[1])-H
    x=np.array([1.,0.,0.]); out=[]; rad=0.
    for d in set((0.,depart)):
        v=pts-(p+d)*x if inverse else pts
        rad=max(rad,np.linalg.norm(v[:,:2],axis=1).max())
        for a in angles:
            c,t=np.cos(a),np.sin(a)
            R=np.array([[c,-t,0],[t,c,0],[0,0,1.]])
            out.extend(v@R.T+H+(0. if inverse else p+d)*x)
    sag=rad*(1-cos(abs(angles[1]-angles[0])/2))
    axis=s[3]
    if axis and abs(axis[2])<1-1e-10:axis=None
    return (s[0],tuple(map(tuple,out)),s[2],axis),sag


def make(g,k,model):
    box,move=g['box'],g['move']; H=np.array(g['H']); P=g['P']; END=g['END']
    angles=np.arange(-15,16,5)*pi/180
    base=g['tucked_joint']()+[s for s in g['electr']() if s[0] not in ('cell','MCU')]
    fx=g['face3']()
    if model=='full':fx+=g['mover2']()
    hd=[g['sweep'](g['mx'](s,g['REL']),(END-g['REL'],0.,0.)) for s in fx]
    hd+=g['roofs']()
    # All electronics stay outside the entire Take 43 guard, including its
    # void. No credit for occupying the open slot or sharing its swept space.
    hood=run_path(str(Path(__file__).resolve().parents[1]/'cand-d-parked-button'/'guard.py'))
    vs=[]
    for x in (hood['REAR'],hood['FRONT']):
        dx=x-hood['XP']
        for sg in (-1,1):
            for z in (hood['lip'](x),28.2-.26*dx):
                vs.append((x,sg*(4.935-.25*dx),z))
    hd.append(g['poly']('closed hood allocation',vs))
    un=[s for s in g['b2']() if model=='full' or s[0]=='cone']
    hd += [g['sweep'](s,(0.,0.,g['LIFT'])) for s in un]
    if model=='full': hd+=g['xd2']()+g['zz2']()+[g['dog'](i) for i in (0,1)]
    boxes,roll=moving_slots(); reserve=g['LIFT']-12.7
    for j,a,b in boxes+roll:
        # stock calculator uses 12.70; include .10 more Z clearance to
        # enclose the 12.80 trial sweep; upper end cap location also debited.
        b=b+[0,0,reserve]; hd.append(box('guide '+str(j),*zip(a,b)))
    hd=g['shift'](hd,k)
    local=hd+base
    all_=[(s,0.) for s in local]
    all_ += [hinge(s,H,angles) for s in g['tailshift'](P,k)]
    # A direct-presented mating eye translates through the stripping stroke.
    # Excludes free, tilted, post-capture recontact and the undeveloped shell.
    all_ += [(g['sweep'](s,(END,0.,0.)),0.) for s in g['tailshift'](0.,k)
             if s[0].startswith(('eye','boss','metal neck','main stem'))]
    for inv in (False,True):all_ += [hinge(s,H,angles,P,END,inv) for s in local]
    return all_


def endpoints(samples,dims,old,lim=200):
    # Search several frames, not just the nearest position in one frame.
    pool=[]
    for cs,f in samples:
        order=np.argsort(np.linalg.norm(cs-old,axis=1),kind='stable')[:lim]
        pool.extend((np.linalg.norm(c-old),c,f) for c in cs[order])
    return sorted(pool,key=lambda a:a[0])[:lim]


def solve(args):
    g=run_path(str(args.source)); core=make(g,args.shift,args.model)
    ori=tuple(args.origin); dims=[args.cell,(22.,17.8,5.7)]
    old=[np.array([-7.45,0,-19.]),np.array([-2.1,0,21.2])]
    pools=[]
    for name,d,target in zip(('cell','MCU'),dims,old):
        poss=(slices if args.slices else search)(core,d,ori,grid=args.grid)
        total=sum(len(cs) for cs,f in poss)
        print(name,'verified grid placements',total,flush=True)
        pools.append(endpoints(poss,d,target))
    if not all(pools): return
    ns=axes(); H=np.array(g['H']); A=np.arange(-15,16,5)*pi/180
    def placements(pool,dim,name):
        for _,c,f in pool:
            q=stock(name,c,dim,f)
            selfn=[hinge(q,H,A,g['P'],g['END'],inv) for inv in (False,True)]
            lo,hi=project(q,ns)
            nei=[(a-debit,b+debit) for t,debit in selfn for a,b in [project(t,ns)]]
            if all(max(np.maximum(lo-b,a-hi))>=.30 for a,b in nei):
                yield c,f,q,[(lo,hi)]+nei
    L=list(placements(pools[0],dims[0],'cell'))
    B=list(placements(pools[1],dims[1],'MCU'))
    for c,f,q,lp in L:
        for u,m,r,rp in B:
            checks=[(lp[0],j) for j in rp]+[(rp[0],j) for j in lp]
            gap=min(max(np.maximum(a-d,b-x)) for (a,x),(b,d) in checks)
            if gap<.30:continue
            for where,frame,s in [(c,f,q),(u,m,r)]:
                print(s[0],np.round(where,3),np.round(frame,4).tolist(),
                      'minimum gap',certificate(s,core))
            print('min electronics/one another incl repeated pair',gap)
            return
    print('no pair in shortlisted placements')


if __name__=='__main__':
    a=argparse.ArgumentParser()
    a.add_argument('--source',type=Path,default=Path(__file__).with_name('button-bounds-take44.py'))
    a.add_argument('--grid',type=float,default=2.)
    a.add_argument('--slices',action='store_true')
    a.add_argument('--shift',type=float,default=-7.)
    a.add_argument('--origin',type=float,nargs=3,default=(-3.5,0.,0.))
    a.add_argument('--model',choices=['full','core'],default='core')
    a.add_argument('--cell',type=float,nargs=3,default=(20.70,30.66,5.40))
    solve(a.parse_args())
