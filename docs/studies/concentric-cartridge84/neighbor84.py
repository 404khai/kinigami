from survey84 import *
import subprocess,tempfile,os
def neighbor():
 b=book();m=pose(b,'LOCK',0,0)
 names=[n for n in m if n.startswith(('clamshell','cell lid','pcb lid','cell cassette','pcb cassette','cell M2','pcb M2','cell screw lug','pcb screw lug','foot '))]
 tris=[]
 for n in names:
  me=m[n].to_mesh64();vv=me.vert_properties[:,:3];tris.extend(vv[me.tri_verts])
 with tempfile.TemporaryDirectory() as tmp:
  bin=os.path.join(tmp,'tube');subprocess.run(['c++','-std=c++17','-O2','tube84.cpp','-o',bin],check=True)
  from io import StringIO
  f=StringIO();print(*PIV[:2],PITCH,100.,len(tris),file=f);np.savetxt(f,np.asarray(tris).reshape(-1,9),fmt='%.17g')
  vals=subprocess.check_output([bin],input=f.getvalue(),text=True).split()
 # Handle the rear yaw fairings separately: guest fairing is invariant under registration,
 # host fairing orbits far to the rear; conservative X extrema over its own yaw.
 def ext(verts):
  r=verts-PIV;cand=np.stack([PIV[0]+r[:,0]*cos(k)-r[:,1]*sin(k) for k in np.deg2rad(np.arange(-15.,15.01,.5))])
  d=max(np.linalg.norm(r[:,:2],axis=1))*2*sin(radians(.125))
  return np.min(cand)-d,np.max(cand)+d
 q=m['tail fairing'];hx=ext(mesh(q))[1];gx=bb(q)[0]+PITCH;hfront=max(bb(m[n])[3] for n in names);gback=min(ext(mesh(m[n]))[0] for n in names)+PITCH
 assert hx<gback and hfront<gx and hx<gx
 # Sample full Kin near sensitive heads/shells to distinguish shell certificate from installed compatibility.
 rows=[]
 for ph,t in [('LOCK',0),('DRAW',1),('PARK',0),('EJECT',.25),('EJECT',1)]:
  dx=phase(ph,t)['guest'][0]
  for ha in [-15.,0.,15.]:
   host=pose(b,ph,t,ha);sel={n:q for n,q in host.items() if bb(q)[3]>-8}
   for ga in [-15.,0.,15.]:
    ss=pose(b,'LOCK',0,ga);gg={'guest '+k:q.translate(-PIV).rotate([0,0,-ga]).translate(PIV+[PITCH+dx,0,0]) for k,q in ss.items()}
    gg={n:q for n,q in gg.items() if bb(q)[0]<10};h=contacts(sel,gg);rows.append([ph,t,ha,ga,h[:12]])
 out=dict(label='exploratory',fixed_exterior=names,yaw_angle_intervals_closed=int(vals[0]),unresolved=int(vals[1]),triangle_pair_tests=int(vals[2]),accepted_width_degrees=list(map(float,vals[3:])),circumferential_fairings=dict(guest_min_x=gx,host_max_x=hfront,host_fairing_max_x=hx,guest_min_x_conservative=gback),method='SAT separates every finite host triangle from the convex outer enclosure of a guest triangle, its complete +0..7.50 mm translation, and its entire yaw cell (XY pad 2*r*sin(cellwidth/4)). Strict separation at all cells proves no surface crossings; positive X ordering checked using the extended-ray repeat in code. Own host housing does not move with its rear hinge. No allowance for assemblies, wall deflection or off-axis escape. Sampled metal near nose includes intended joins.',sample_rows=rows)
 dump('neighbor84.json',out);print(vals)
if __name__=='__main__':neighbor()
