"""Registered two-body checks. No aperture or approach guarantee from carried poses."""
from check82 import *
def neighbors():
 b=book();rows=[];phases=[('LOCK',0),('DRAW',1),('UNLOCK',1),('EJECT',.5),('EJECT',1)]
 # The two shells and installed motor housings are sufficient hard-counterexample targets.
 shell=['outer clamshell 0','outer clamshell 1','V seat annulus','barrel','ejector lip','sleeve 0615 + 06/1','draw 0615 + 06/1','eject 0615 + 06/1']
 for ph,t in phases:
  for ha in [-15,0,15]:
   host=pose(b,ph,t,ha);dx=phase(ph,t)['guest'][0]
   for ga in [-15,0,15]:
    # Inverse yaw about the neighboring pivot removes its tail's rotation.
    # +40.30 then registers that tip; body and motor follow the opposite turn.
    ss=pose(b,'LOCK',0,ga);gx={}
    for k,q in ss.items():
     if b[k][3] in ('air','teeth'):continue
     gx[k]=q.translate(-PIV).rotate([0,0,-ga]).translate(PIV+[40.30+dx,0,0])
    hits=[]
    for n in shell:
     m=host[n];bb=flat(m)
     for k,z in gx.items():
      if aabb(bb,flat(z)):
       v=common(m,z)
       if v>1.e-5:hits.append([round(v,6),n,k])
    hits.sort(reverse=True)
    rows.append(dict(phase=ph,fraction=t,host_yaw=ha,guest_yaw=ga,assumed_aligned_displacement_mm=dx,largest_five=hits[:5],guest_floor_z=min(flat(m)[2] for m in gx.values())))
 dump('neighbor82.json',dict(label='exploratory',warning='Registered axial motion is imposed only as a collision probe, not mechanically imposed ejection. Eight host bodies vs whole registered neighbor; not a complete global approach sweep.',rows=rows))
def witnesses():
 # Checks are on original analytic solids, not intersections of inflated AABBs.
 # Eject spider crosses fixed yaw axis at stroke 1.965. Own yaw is about that axis.
 b=book();t=1.965/8.1;m=pose(b,'EJECT',t,-15,True)
 qa=m['ejector spider'];qb=m['yaw shaft'];x,y,z=PIV
 # Actual yaw shaft stock is a centered cylinder; radius from 79's data.
 margins=[.295,1.82,hypot(y,z)-2.74,6.37-hypot(y,z)]
 dump('witness82.json',dict(label='exploratory',eject_at_axis=dict(point=PIV.tolist(),eject_stroke=1.965,analytic_ball_radius=.29,margins=margins,mesh_overlap_mm3=common(qa,qb),yaw='all; own shaft rotates about its own symmetric axis'),bush_at_draw=dict(clock=180,x=-10.1,r=6.415,t=0,radius=.08,remaining_bush_outer_depth=5.82+.68-6.415,remaining_sleeve_inner_depth=6.415-6.33,owns='fixed aft liner OD and sleeve internal web away from all three working pockets'),bare_sleeve_nominal_radial_clearance=.05))
if __name__=='__main__':neighbors();witnesses()
