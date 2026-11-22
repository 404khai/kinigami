from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('shell-tilt70.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def run():
 f=chassis()+pads();e=json.loads((D/'shell-elec70.json').read_text());tt=move(tail(),-P)+joint()[1]
 el=e[:24];print('cell fixed all physical stock',fine(el,f),'body/rotor/full stroke support',pairs(el,head()))
 t=tailbound();scores=[]
 for y in np.arange(-15,15.01,.5):
  for q in yaw(t,y): scores.append((pairs(el,[q])[0]-2*far(q,H)*sin(radians(.125)),q[0],y))
 print('cell to independent own tail all yaws with half step debit',min(scores))
 a=AZ[0];ls=subset(f,('pitched X way','X way outer','X way return','X way root','slider guide cheek','way anchor'))
 for p in (-3.294,0,15,30,42):
  an,h=phase(p);px,rp,rd=link(an);q=subset(sliders(a,an),('crosshead X face','radial crosshead'))
  print('ring, guide reaction overlap with actual fixed cheeks',p,cp(q,ls,1),'minimum axial face gap .040 per side; full registration inner and outer',min(rd-5.34-13.05,22.44-(rd+.94)))
 print('opposite +/-X reactions per unit radial force, worst moment t (9.5mm) / shortest bearing pitch',9.5/4.60,'each; minimum .65 x .82mm bearing; .05 sliding drag from BOTH rows per radial force',2*.05*9.5/4.60)
 print('at nominal Take67 conditional 140N link load use conservative F_rad=140 N; X per row, one pad worst MPa, two-face drag',140*9.5/4.6,(140*9.5/4.6)/(.65*.82),2*.05*140*9.5/4.6)
 park=parkmotor();gg=subset(f,('aft cantilever','cantilever radial','cross rail','outer axial rail','fixed wall heel','foot forward','foot rear','park motor saddle','park saddle','park cam bearing tie'))
 for y in (-15,0,15):
  print('fitted rear structure vs yaw bodies and fixed motors (nominal housing intersections; known mount contacts not removed)',y,cp(gg,yaw(tt,y)+subset(f,('clamp motor','yaw motor body')),5))
 # Independent yaws: retain only finite actual peer pieces when a convex
 # aggregated half-stroke screen cannot separate neighbors.
 yawm=np.arange(-15,15.001,3);z=[]
 for p in (-3.2,0,20,42,105):
  h=subset(state(p),('external park lever','bearing pin','radial slide fork','slider link pin','axial transfer','centre clevis link'))
  pf=subset(pads(),('foot rear riser','foot (','foot rear flange'));cache=[yaw(h,a) for a in yawm];cc=[move(yaw(pf,b),P) for b in yawm]
  ee=[extlist(q) for q in cc]
  for i,u in enumerate(cache):
   eu=extlist(u)
   for j,v in enumerate(cc):
    if pairs(u,v,eu,ee[j])[0]>0:continue
    b=cp(u,v,1)
    if b:z.append((b[0],p,yawm[i],yawm[j]))
 print('max TRUE adjacent intersection among named full stock with independent yaw, excluding clevis bores where applicable',max(z) if z else 'none, not all-pairs proof')
if __name__=='__main__':run()
