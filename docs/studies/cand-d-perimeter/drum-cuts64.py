"""Constructive solid cutters. All drum radii are from X and all X local.
Point inclusion functions use a finite union of swept radial roller cutters.
Arc/x offsets in drum-grooves64.json are reference-radius visualizations only.
"""
from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('drum-strength64.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
N=8;Dg=hypot(3.58,2.81);cr=Dg*sin(pi/8);dw=2.03;wheel_R=4.22;halfa=51.;pin_r=.37;slot_r=.42;T=np.linspace(-3.75,106.5,442)
def xp(t,inner):
 an,h=phase(t);return -19.03+h if inner else -16.8+horn(an)[0]-HX
def cuts():
 # Overbound the continuous tool strip by extending radial ends and
 # increasing half-width for half a sample step of centre motion. Opening
 # front + rear caps included. The annular core starts OUTSIDE all ID cuts.
 # Rolling journal nose radius never exceeds the recessed roller cutter.
 csg={}
 for inner in [True,False]:
  rr=(9.50,11.81) if inner else (16.06,20.05)
  rad=1.045 if inner else .86
  st=BAZ if inner else tuple(a+degrees(atan2(4.68,16.42)) for a in AZ)
  cen=np.array([xp(t,inner) for t in T]);dt=radians(T[1]-T[0]);B=(hypot(rr[1],15 if inner else 7)*dt)/2
  n='disk' if inner else 'leaf'
  csg[n]=dict(operation='difference from UNION of axisymmetric ring stocks',tool='union of radial cylinders at sampled poses; extra halfstep support on radial ends and roller radius',rangeR=[rr[0]-B,rr[1]+B],tool_R=rad+B,azimuths=st,poses_deg_x=np.column_stack((-T,cen)).round(8).tolist())
  print('sampled cutter',n,'radial end/radius enlargement',B,'radial core remaining',13.19-(rr[1]+B) if inner else rr[0]-B-14.06)
  # Land between tracks and side/back wall at closest axial edge.
  print('thinnest end-wall axial after overcut',n,min(min(cen)-(rad+B)-(-20.29 if inner else -17.94),(-9.39 if inner else -12.39)-max(cen)-(rad+B)))
 # Direct material witness in the revised core beyond every cut (including
 # the long journal nose). Use the TRUE inscribed arc tiles from the audit.
 gg=run_path(str(D/'drum-check64.py'));ip=gg['innring']('finished drum core ',-20.21,-9.47,11.90,13.12);print('finished cam outside all sampled tool cuts vs rear spine',gg['cp'](ip,[s for s in fixture() if s[0]=='rear spine'])[:1])
 (D/'drum-cuts64.json').write_text(json.dumps(csg,separators=(',',':'))+'\n')
def index():
 uv=lambda t:np.stack((np.cos(t),np.sin(t)),axis=-1)
 v0=uv(np.arange(8)*pi/4);v1=uv(np.arange(8)*pi/4+pi/8)
 def depth(p):
  r=np.linalg.norm(p,axis=1);g=np.minimum(wheel_R-r,r-1.02)
  for v in v0:g=np.minimum(g,np.linalg.norm(p-Dg*v,axis=1)-(dw+.060))
  for v in v1:g=np.minimum(g,np.linalg.norm(p-np.maximum(p@v,Dg-cr)[:,None]*v,axis=1)-slot_r)
  return g
 def wheel(beta):
  return 0 if beta>=67.5 else -45 if beta<=-67.5 else degrees(atan2(cr*sin(radians(beta)),Dg-cr*cos(radians(beta))))-22.5
 ra,ba=np.meshgrid(np.linspace(.01,dw,34),np.linspace(-halfa,halfa,139));va=ra.ravel()[:,None]*uv(np.radians(ba.ravel()));p0=np.array([Dg,0])
 def mat(phi):
  z=radians(phi);return np.array([[cos(z),-sin(z)],[sin(z),cos(z)]])
 def test(beta,q):return max(depth((p0+va@mat(-beta).T)@mat(q)))
 print('index continuous ideal sample, max sector sample in registered wheel, beta, q',max((test(b,wheel(b)),b,wheel(b)) for b in np.linspace(-180,180,361)))
 for q in (-4,-3,-2,0,2,3,4):
  print('180° blocked input; output trial rotation; maximum sampled material depth (mm)',q,test(180,q))
 for b in (180,115,100,90,80,70,67.5,62,50,0):
  q=wheel(b);pa=p0+cr*uv(radians(180-b));r=np.linalg.norm(pa)
  print('beta°, ideal q, nominal pin outside wheel rim? ring play diagnostic for ±3° wheel vs sector',b,q,r-pin_r>wheel_R,test(b,q-3),test(b,q+3))
 (D/'drum-index64.json').write_text(json.dumps(dict(axes='Y; wheel=(O-9.11,-19.5) in world XZ; +local x toward quill axis',spacing=Dg,crank_R=cr,pin_R=pin_r,slot_halfwidth=slot_r,slot_centerline_radial_start=Dg-cr,scallop_center_R=Dg,scallop_R=dw+.060,slot_azimuth_deg=list(np.arange(8)*45.+22.5),scallop_azimuth_deg=list(np.arange(8)*45.),wheel_R=wheel_R,hub_R=1.02,thickness=1.51,blocking_R=dw,blocking_half_angle=halfa,sector_t=1.44,pin_Y=[-9.12,-7.34]),separators=(',',':'))+'\n')
if __name__=='__main__':cuts();index()
