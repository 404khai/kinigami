"""Continuous finite-solid clearance for designated non-contact pairs by interval bounds."""
from survey84 import *
def main():
 b=book();sl='slotted sleeve and skirt';ca='rail-free cage';he='guest tri-flat pin';xc=-4.22
 b.put('pin extensions',union(zpin(xc,G0,t,.5) for t in [(-3.84,-1.50),(1.50,3.84)]),'r0')
 b.put('bonded bush and bridge set',union(v[0] for n,v in b.items() if n.startswith(('eject bush','bush spine','bush bridge','pilot web','cage reset abutment'))))
 pairs=[(sl,ca),(sl,'pin extensions'),(sl,he),(ca,he),(sl,'bonded bush and bridge set'),(sl,'V plate'),(ca,'V plate'),('pin extensions',he),('pin extensions','V plate')]
 rows=[]
 for n,k in pairs:
  mg=b[n][1];ng=b[k][1]
  for ph in ['DRAW','UNLOCK','EJECT']:
   def vec(t):
    d=phase(ph,(1+2*t)/3 if ph=='UNLOCK' else t)
    return np.asarray(d[mg])-d[ng]
   # Split at the change of axial tail speed during eject. Within each interval
   # each component of relative displacement is monotone (arc/line/flat profiles).
   ff=[0,.60/8.10,1] if ph=='EJECT' else [0,1];lower=100;bad=[];cells=0
   def visit(l,h,dep):
    nonlocal lower,cells
    m=(l+h)/2;lo,mi,hi=vec(l),vec(m),vec(h)
    D=float(np.linalg.norm(np.maximum(np.abs(mi-lo),np.abs(hi-mi))))+1e-10
    if D>.48 and dep<12:return (visit(l,m,dep+1),visit(m,h,dep+1))
    q=b[n][0].translate(mi);z=b[k][0];sep=q.min_gap(z,.50)
    if sep>D+1e-8:cells+=1;lower=min(lower,sep-D);return
    if dep==12 or D<1e-8:bad.append([l,h,sep,D,max(0.,(q^z).volume())]);return
    visit(l,m,dep+1);visit(m,h,dep+1)
   for l,h in zip(ff,ff[1:]):visit(l,h,0)
   rows.append(dict(parts=[n,k],phase=ph,strictly_separated_cells=cells,lower_polygon_gap_mm=lower if not bad else None,unresolved_count=len(bad),first_unresolved=bad[:1]))
 dump('interval84.json',dict(label='exploratory',rows=rows,slot_analytic='At a station, |roller_x−cheek_x|≤.025, roller y within 4.93066..7.04, capsule center segment y4.89..7.10. Therefore R.50 trunnion lies in R.525 capsule; equality possible at DRAW. No positive spacing claimed at bearing contact.',note='Upper working roller/sleeve and loaded roller/tail interfaces intentionally touch; see finite overlap residuals in local84.json, not classified as strictly separated. t-symmetric local trunnion pair uses 0° station; whole assembly sampled independently. WALK over reset trajectory uses DRAW in reverse then UNLOCK sleeve segment. Only nominal, aligned, polygonal.'))
if __name__=='__main__':main()
