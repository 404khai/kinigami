"""All-stock sample ledger; no exemptions for designed joins or thread/tooth envelopes."""
from survey84 import *
from itertools import combinations
def poses():
 return [('LOCK',0)]+[(p,t) for p,ts in [('DRAW',[.5,1]),('UNLOCK',[0,.25,1/3,.5,.625,.75,.875,1]),('PARK',[0]),('EJECT',[.15,.4,.65,1])] for t in ts]
def raw():
 b=book();names=list(b);cache={};worst={};rows=[]
 for ph,t in poses():
  v=phase(ph,t);unlock=ph=='UNLOCK' and 1/3<t<1;draw=ph=='DRAW' and 0<t<1 or ph=='UNLOCK' and 0<t<1/3
  for yaw in [-15.,0.,15.]:
   m=pose(b,ph,t,yaw,True);bounds=np.array([bb(m[n]) for n in names]);hits=[]
   tags={**{k:tuple(x) for k,x in v.items()},'yaw':yaw,'cam':(unlock,draw),'spin':unlock,'dpin':draw,'nut':v['sleeve'][0],'drot':v['draw'][0],'coil':(v['cage'][0],v['draw'][0])}
   for i,n in enumerate(names):
    ids=np.where(np.all(np.minimum(bounds[i,3:],bounds[i+1:,3:])-np.maximum(bounds[i,:3],bounds[i+1:,:3])>1e-8,axis=1))[0]+i+1
    for j in ids:
     k=names[j];g=b[n][1];h=b[k][1];key=(n,k) if g==h and g!='coil' else (n,k,tags[g],tags[h])
     if key not in cache:cache[key]=max(0.,(m[n]^m[k]).volume())
     vol=cache[key]
     if vol>1e-7:
      hits.append((i,int(j),round(vol,7)));pair=n+' | '+k
      if pair not in worst or vol>worst[pair][0]:worst[pair]=[vol,ph,t,yaw]
   rows.append([ph,t,yaw,hits])
 dump('phase-pairs84.json',dict(label='exploratory',names=names,poses=rows,worst=worst,threshold_mm3=1e-7,note='Full Cartesian 3D material intersections at sampled poses, incl intentional joins, screw and tooth envelopes and guest; not all are faults. Lists [first part index,second part index,overlap mm3]; no loads or tolerances.'))
def sweep():
 b=book();rr=[];raws=[];a=PH[0];key='slotted sleeve and skirt';ds=law()
 states=[('DRAW',t) for t in np.linspace(0,1,25)]+[('UNLOCK',t) for t in np.linspace(0,1,145)]+[('PARK',0)]+[('EJECT',t) for t in np.linspace(0,1,41)]+[('LOCK',0)]
 bush=[n for n in b if n.startswith(('eject bush','bush spine','bush bridge','pilot web'))]
 names=['rail-free cage','roller 0',key,'guest tri-flat pin']+bush+['eject crosshead','yaw shaft','V plate','pilot','annular ejector']
 for ph,t in states:
  d=phase(ph,t);mm={n:b[n][0].translate(d.get(b[n][1],[0,0,0])) for n in names};vals={}
  for n,k in list(combinations(names[:4],2))+[(key,n) for n in bush]+[(key,'V plate'),('rail-free cage','V plate'),('eject crosshead','yaw shaft')]:
   q,z=mm[n],mm[k];vol=max(0.,(q^z).volume()) if cand(bb(q),bb(z)) else 0;vals[n+' | '+k]=round(vol,10)
  rr.append([ph,t,vals])
 # For finite components with fixed orientation, a convex hull of both interval endpoints encloses the entire sweep.
 # To avoid filling the annular/sleeve bores, handle simple cylinder/plane proofs separately.
 out=dict(label='exploratory',rows=rr,rail_free=True,three_station_symmetry='centered strict guest, rollers and cheeks repeat every 120 degrees. Finite assembly raw check includes all three.',slot_halfwidth=4.46,eject_bush_hole_R=.80,eject_bush_max_R=.68,guide_nominal_radial_gap=.12,guide_note='R.80 cuts span all relevant fixed bush centers; bridges separately scanned. Local aligned contact model, no release guarantee.',crosshead_shaft_min_x_gap=(-26.24)-(-30+1.82),crosshead_shaft_proof='minimum x of any crosshead metal occurs at HOME; rotation of the shaft about its own axis cannot increase its x maximum beyond −28.18.')
 dump('local84.json',out)
if __name__=='__main__':
 import sys
 for n in sys.argv[1:] or ['raw','local']:{'raw':raw,'local':sweep}[n]()
