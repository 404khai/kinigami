from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('quill-load67.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def cuts():
 o={};th=np.linspace(-4.25,106.75,889)
 for key in ('disk','leaf'):
  # Real tool sweeps: static drum frame, x-axis z=O+local X. The 3 repeated
  # cuts are applied to the UNION. Sampled cylinders inflated for half-step
  # angular, radial, and axial motion, including barrel-journal nose.
  if key=='disk':
   xmin,xmax=9.50,11.76;rd=1.036;B=.5*radians(.125)*hypot(11.76,14.3);st=BAZ
   a=np.array([[-t,-19.03+phase(t)[1]] for t in th]);v=np.c_[D0*np.radians(a[:,0]),a[:,1]];direction='radial only at listed azimuth, independent of X'
  else:
   xmin,xmax=-11.10,-8.52;rd=.91;B=.5*radians(.125)*hypot(21.,7.);st=AZ
   a=np.array([[-t,link(phase(t)[0])[2]-2] for t in th]);v=np.c_[np.cos(np.radians(a[:,0]))*a[:,1],np.sin(np.radians(a[:,0]))*a[:,1]];direction='along X between listed x values'
  o[key]=dict(stations_deg=st,axis=direction,extent=[xmin-B,xmax+B],R=rd+B,trajectory_deg_X_or_rad=a.round(8).tolist())
  da=np.gradient(v,axis=0);d2=np.gradient(da,axis=0);rho=np.min(np.linalg.norm(da,axis=1)**3/np.maximum(1e-16,abs(da[:,0]*d2[:,1]-da[:,1]*d2[:,0])))
  if key=='leaf':
   mat=np.array([[cos(2*pi/3),-sin(2*pi/3)],[sin(2*pi/3),cos(2*pi/3)]]);prev=v@mat.T;inner=a[:,1].min()-rd-B-12.89;outer=20.84-a[:,1].max()-rd-B;back=(-11.1-B)-(-11.69)
  else:prev=v+np.array([D0*2*pi/3,0]);inner=13.19-xmax-B;back=a[:,1].min()-rd-B+20.29;outer=-9.07-a[:,1].max()-rd-B
  gap=min(np.linalg.norm(prev-z,axis=1).min() for z in v)-2*(rd+B)
  print(key,'cut inflation, sampled curvature R, walls inner/core, outer/front, back, closest repeated land',B,rho,inner,outer,back,gap)
  dd=np.gradient(a[:,1],np.radians(th));den=D0 if key=='disk' else a[:,1];print(key,'max pressure angle, signed slope at work',degrees(max(np.arctan(abs(dd)/den))),dd[np.argmin(abs(th))])
  print('last draw theta ±3° local remained end wall minimum',key,min(inner,outer,back))
 (D/'quill-cam67.json').write_text(json.dumps(o,separators=(',',':'))+'\n')
 # Toe/roller is captured in the actual ring, not on an assumed surface.
 for th0 in (-3,0,10,42,105):
  an,h=phase(th0);px,rp,rd=link(an)
  print('ring, working pin, leaf roller rad, disk roller X, annulus groove axial shoulder length',th0,(px,rp),rd-2,-19.03+h,1.65)
 for obj,s0,s1 in [('park ring steel limit',105,107),('draw ring steel limit',-4.2,-3)]:
  q=next(q for q in chassis() if q[0]==obj);print('actual first hard-stop common surface',obj,brentq(lambda t:ball(q,lug(t))[3],s0,s1))
def screw():
 # Actual bolt insertion depth; actuator remains in permanent mesh. Check
 # independent alignment/entry vs square shank and power-off shear flanks.
 ph=np.arange(16)*2*pi/16;sx=W+2.60;sy=WR+sqrt(3.56**2-2.60**2);a=atan2(sy-WR,sx-W);vc=np.c_[W+3.56*np.cos(a+ph),WR+3.56*np.sin(a+ph)]
 o=dict(star_center_world=[W,WR],axis='world Z',R=4.53,z=[13.45,15.0],bore_R=.96,holes=vc.tolist(),hole_R=.50,lead_chamfer=[.66,.16],pin_axis_world=[sx,sy],pin_R=.44,pilot_R=.26,pilot_height=.18,tip_z_extended=15.22,tip_z_retracted=13.23,return_stroke=1.99,bush_z=[11.78,13.34],bush_inner_R=.46,bush_outer_R=1.12)
 for k in ('z','bush_z'):o[k]=[x+5.06 for x in o[k]]
 for k in ('tip_z_extended','tip_z_retracted'):o[k]+=5.06
 (D/'quill-bolt67.json').write_text(json.dumps(o,separators=(',',':'))+'\n')
 for deg in (0,.50,.97,1.5,11.25):
  off=2*3.56*sin(radians(deg)/2);print('bolt misalignment °, center shift, straight shank clearance, tip-to-mouth',deg,off,.50-.44-off,.66-.26-off)
 print('extended straight shank overlap worst excluding chamfer, retracted nose X-clear',min(15.,15.22-.18)-(13.45+.16),13.45-13.23)
if __name__=='__main__':cuts();screw()
