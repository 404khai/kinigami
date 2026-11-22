"""Planar polar material extruded along X in the indexed screw drive.
Checks blocking scallop and roller tangencies independent of registration flags.
"""
from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('sleeve-short62.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
from scipy.optimize import brentq
def run():
 # local horizontal line joins wheel centre (0,0) to crank (D,0).
 d=hypot(1.05,4.43);sw=4.21;dw=2.05;pin=.37;c=sin(pi/8);l=d*c;rim=d*(1-c)
 wg=.41;clear=.06;aa=np.arange(8)*pi/4;uv=lambda t:np.stack((np.cos(t),np.sin(t)),axis=-1);V0=uv(aa);Vs=uv(aa+pi/8)
 def depth(p):  # safe inner-ball radius vs wheel boundary & cutouts
  r0=np.linalg.norm(p,axis=1)
  g=np.minimum(sw-r0,r0-1.30)
  for v in V0:g=np.minimum(g,np.linalg.norm(p-d*v,axis=1)-(dw+clear))
  for v in Vs:
   b=np.maximum(p@v,rim);g=np.minimum(g,np.linalg.norm(p-b[:,None]*v,axis=1)-wg)
  return g
 # Keep an arc around the direction AWAY from the driver pin. End detent
 # pin points away from wheel, leaving the arc toward the registered pocket.
 gh=np.linspace(-pi/3.5,pi/3.5,103);rh=np.linspace(.12,dw-.004,63)
 r,t=np.meshgrid(rh,gh);v=uv(t.ravel())*r.ravel()[:,None]
 def test(beta,q):
  # theta relative to driver inward direction, positive CCW here.
  ang=radians(beta);yaw=radians(q)
  a=ang+pi;ma=np.array([[cos(a),-sin(a)],[sin(a),cos(a)]])
  b=pi;vb=v@ma.T;vb[:,0]*=-1;vb[:,0]+=d
  # unrotate the wheel, whose registry scallop initially points at driver
  mm=np.array([[cos(yaw),-sin(yaw)],[sin(yaw),cos(yaw)]])
  dep=depth(vb@mm);return max(dep)
 for yaw in (-3,-2,-1.5,-1,-.5,0,.5,1,1.5,2,3):
  print('wheel turn at blocked input, deg, witness depth in wheel mm',yaw,test(180,yaw))
 # Sample a continuous ideal wheel kinematic trace for sector penetration.
 # This check is not an all-angle manufacturing certificate.
 vv=[]
 for beta in np.linspace(180,-180,361):
  rad=radians(beta);e=degrees(acos(c))
  if beta>=e:q=0
  elif beta<=-e:q=-45
  else:q=degrees(atan2(l*sin(rad),d-l*cos(rad)))-22.5
  vv.append((test(beta,q),beta,q))
 print('worst wheel-vs-sector sample depth, beta, wheel angle',max(vv))
 print('driver wheel axial overlap/OD',1.33,2*sw,'crank radius pin diameter',l,2*pin,'slot radial reach',rim-wg,sw,'slot radii tolerance',wg-pin)
 # True angular ratio for successive 0.0625mm screw increments. Sample
 # actual halfway through a reachable stroke, with the final .38 rounded shoe.
 for typ in ('barrel','short'):
  for step in (9,10,15,16,17):
   nut=(step+.5)*.0625
   if typ=='barrel':p=brentq(lambda th:law(th)[2]-nut,0,105);s=law(p)[0];der=(law(p+.00001)[0]-law(p-.00001)[0])/(law(p+.00001)[2]-law(p-.00001)[2])
   else:p=nut;s=laws(p)[0];der=(laws(p+.00001)[0]-laws(p-.00001)[0])/.00002
   if not 0<s<.0456:continue
   qx=J['tip_x']+s/.38;rw=10.75+2.50/hypot(1,.38);q=np.array([qx,rw-s,0]);pl=np.array(J['halfspaces']);nn=pl[:,:3]/np.linalg.norm(pl[:,:3],axis=1)[:,None];b=pl[:,3]/np.linalg.norm(pl[:,:3],axis=1);n=nn[5];co=q-.12*n;ds=b-.12-nn@co;pr=np.sqrt(np.maximum(0,1-(nn@n)**2));patch=min(ds[pr>1e-6]/pr[pr>1e-6])
   fa=3*(33+6*(.12-s/.38)/.252) # nominal linear interpolation only
   nr=fa*(1+.23*.38)/(.38-.23)
   t=nr*der*.5/(2*pi*.28)*c/(1-c)*(16/30)/(.72*.80)
   print('actual mid-index compress stroke',typ,step,nut,p,s,patch,fa,nr*der,t)
 # Full physical cut profile definitions; all lengths in mm. Wheel indexed
 # via pin on active interval, never by backdriving the locking sector.
 (D/'sleeve-lock62.json').write_text(json.dumps(dict(wheel=dict(ro=sw,bore=1.30,thickness=1.45,scallops=[(list(d*v),dw+clear) for v in V0],slot_centerline_r0=rim,slot_radius=wg,azimuths_deg=list(np.arange(8)*45.+22.5)),driver=dict(centre=[d,0],blocking_radius=dw,retained_half_angle_deg=180/3.5,crank_pin_radius=pin,crank_radius=l,blocking_thickness=1.38,crank_cheek_thickness=.80)),separators=(',',':'))+'\n')
if __name__=='__main__':run()
