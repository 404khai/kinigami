from survey84 import *
def run():
 b=book();m=pose(b,'LOCK',0,0);bounds={n:bb(q) for n,q in m.items()};rows={}
 def test(n,q,dr,L,obs,step=.50):
  d=np.asarray(dr);tt=np.linspace(0,L,int(ceil(L/step))+1);a=bb(q);ball=np.r_[np.minimum(a[:3],a[:3]+d*L),np.maximum(a[3:],a[3:]+d*L)]
  names=[k for k in obs if cand(ball+np.r_[[-.30]*3,[.30]*3],bounds[k])];worst=(0,None,None);ming=.30
  for t in tt:
   z=q.translate(d*t);aa=bb(z)
   for k in names:
    if np.any(np.minimum(aa[3:],bounds[k][3:])-np.maximum(aa[:3],bounds[k][:3])<-.30):continue
    if cand(aa,bounds[k]):
     v=(z^m[k]).volume()
     if v>worst[0]+1e-9:worst=(v,k,t)
    if ming>0:ming=min(ming,z.min_gap(m[k],.30))
  rows[n]=dict(direction=d.tolist(),travel=L,samples=len(tt),largest_sample_overlap_mm3=worst[0],obstacle=worst[1],at=worst[2],min_mesh_gap_mm=ming,interval_gap_lower_mm=max(0,ming-(tt[1]/2 if len(tt)>1 else 0)),scope=len(obs),nearby=names)
 def filt(*terms):return [n for n in m if n.startswith(terms)]
 for tag,a,y,w,xx in [('cell',CELL,22,9.08,[-27,-15.2]),('pcb',PCB,22.9,8.70,[-30.2,-19.9])]:
  screws=[tag+' M2 screw '+str(i) for i in range(2)]
  for i,x in enumerate(xx):
   z=(w+1.32)*(1 if i==0 else -1)
   tool=loc(M.cylinder(34,1.82,1.82,N).rotate([-90,0,0]).translate([x,y+1.02,z]),a)
   obs=[n for n in m if n!=screws[i]];test(screws[i]+' tool shank',tool,[0,*at(1,a)],0,obs)
   tip=M.cylinder(.63,1.25/sqrt(3),1.25/sqrt(3),6).rotate([-90,0,0]).translate([x,y+.56,z])
   bit=loc(tip,a)+tool
   # Only the non-targets see the large shank. Verify target screw with the narrow engaged tip too.
   rows[screws[i]+' engaged bit']=dict(overlap=contacts({'seated hex bit':bit},m),depth_into_head=.46,radial_flats_clearance=.025,stop_floor_gap=.07)
   test(screws[i]+' screw withdrawal',m[screws[i]],[0,*at(1,a)],8,[n for n in m if n!=screws[i]],.25)
  obs=[n for n in m if n not in screws+[tag+' lid']];test(tag+' lid outward',m[tag+' lid'],[0,*at(1,a)],12,obs,.22)
 cellparts=[q[0] for q in json.load(open('catalog-reserves79.json'))['elec'][:24]]
 obs=[n for n in m if n not in cellparts+['cell lid','cell M2 screw 0','cell M2 screw 1']]
 test('cell with tabs and protection, lid removed',union(m[n] for n in cellparts),[0,*at(1,CELL)],15,obs,.35)
 # Whole straight extraction, independent of sampling: each convex endpoint hull bounds one pack component.
 sweeps=[(m[n]+m[n].translate([0,*at(15,CELL)])).hull() for n in cellparts]
 stock=union(sweeps);rows['cell whole swept hulls']=dict(overlap=contacts({'moving pack sweep':stock},{k:m[k] for k in obs}),direction=[0,*at(1,CELL)],travel=15)
 lid=m['cell lid'];q=loc(lid,-CELL).rotate([90,0,0]);zs=bb(q);cs=q.slice((zs[2]+zs[5])*.5)
 swept=loc(cs.extrude(zs[5]-zs[2]+12).translate([0,0,zs[2]]).rotate([-90,0,0]),CELL)
 obs=[n for n in m if n not in ['cell lid','cell M2 screw 0','cell M2 screw 1']]
 rows['cell lid full prism']=dict(overlap=contacts({'lid motion':swept},{k:m[k] for k in obs}),note='Lid has invariant cross-section along extraction normal. Extrusion of its middle section through full axial thickness +12 mm, retaining both screw holes.')
 test('bare sleeve rear through guide bands',m['slotted sleeve and skirt'],[-1,0,0],20,filt('sleeve band','barrel','V plate','spline ','eject bush','bush spine','bush bridge','pilot web'),.09)
 test('front ring with guides bonded',m['annular ejector'],[1,0,0],10,filt('eject bush','bush bridge','pilot','V plate','barrel'),.20)
 test('eject thrust bearing off bare screw',m['eject F3-8M 0'],[-1,0,0],14,['eject M3 screw','eject thrust flange'],.25)
 test('screw and flange through assembled thrust pair',m['draw M3 screw']+m['draw thrust flange'],[-1,0,0],34,filt('draw F3','draw thrust abutment'),.25)
 test('hollow nut out through rear seat',m['rotating hollow nut'],[-1,0,0],18,['cross roller CRBT205A','cross roller support split'],.25)
 test('barrel nose through installed cover',m['barrel'],[1,0,0],22,filt('clamshell'),.35)
 test('shell 0 closure',m['clamshell 0'],[0,-1,0],26,[n for n in m if not n.startswith('clamshell')],.5)
 dump('service84.json',dict(label='exploratory',rows=rows,note='Single isolated Kin LOCK, yaw=0. Driver shaft is entire installed access volume; trial 1.25-AF bit in a 1.30-AF socket; no thread tightening or stripped torque model. Lid translated after removing its two screws, all other listed stocks installed. Zero lower bound can mean designed seating contact, not a clearance certificate. No wire disconnection or arbitrary servicing in swarm guaranteed.'))
if __name__=='__main__':run()
