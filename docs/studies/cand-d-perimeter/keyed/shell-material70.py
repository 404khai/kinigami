from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('shell-assembly70.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
# Positive steel drive rings are not plated aluminum. Each ring has three
# integral radial tabs with two tangential flanks AND two axial faces.
def bands():return [(O-20.29,O-9.07,9.78,11.99),(O-11.38,O-9.04,14.95,20.84),(W-1.29,W+1.29,18.56,19.80)]
def lugs():
 return sum(([sec('disk shaft tab',(-15.31,-14.12),(11.82,12.80),(-.72,.72),a),
              sec('face drive tab',(-10.73,-9.63),(13.79,15.28),(-.92,.92),a),
              sec('wheel tab',(W-O-.63,W-O+.63),(17.59,18.81),(-.74,.74),a)] for a in (13,133,253)),[])
def camlift(p):
 # Non-periodic travel defined over physical stops; not an endless crank.
 if p<=12:return 16.29-.11*sin(radians(90*p/12))
 if p>=156:return 18.15
 return 16.18+1.97*(1-cos(pi*(p-12)/144))/2
def dogcam():
 # Cut entire groove in world (UA face axis), continuous cutter rounded
 # at each end. End walls survive regardless of unrelated power or sensors.
 v=[]
 for p in np.arange(-2,159.001,.25):
  z=camlift(float(p))-S0[2];a=radians(p);v.append([p,-z*sin(a),z*cos(a)])
 return v
def tailcore():
 # Rotation-free local tail in installed source frame, not a visual mesh.
 return np.array(tail()[0][1])-O*X
def run():
 import json
 c=json.loads((D/'shell-cam70.json').read_text());v=tailcore();hv=ConvexHull(v);cv=(hv.equations[:,:3]*(np.cross(v[hv.simplices[:,1]]-v[hv.simplices[:,0]],v[hv.simplices[:,2]]-v[hv.simplices[:,0]]))).sum(1);idx=np.where(cv>0,hv.simplices.T,hv.simplices[:,::-1].T).T # OpenSCAD left-hand polygons below
 model=dict(steel_bands=bands(),steel_lugs=lugs(),tail_core_local=v.tolist(),tail_outer_offset=2.50,tail_inner_offset=1.66,button_ports=[[-4.76,7.22,2.64,a] for a in BAZ],dog_cam_path_mm=dogcam())
 (D/'shell-material70.json').write_text(json.dumps(model,separators=(',',':'))+'\n')
 j=lambda x:json.dumps(x,separators=(',',':'))
 sc='''// Take70 editable nominal cut stock, local tail vs powered WORLD for rotor. Not fabrication files.
$fn=72; part="steel"; // steel, aluminum, tail, dog, star
module ax(x,l,r){translate([x,0,0])rotate([0,90,0])cylinder(h=l,r=r);}
module ann(x,y,i,o){difference(){ax(x,y-x,o);ax(x-.01,y-x+.02,i);}}
module disktool(x,a){rotate([a,0,0])translate([x,9.47980,0])rotate([-90,0,0])cylinder(h=2.30040,r=1.05620);}
'''
 sc+='module rotor(){difference(){union(){'+''.join('ann(%f,%f,%f,%f);'%tuple(row[1:]) for row in annuli())+'}\n'
 sc+='for(a=[-30,90,210],q='+j(c['disk']['trajectory_deg_X_or_rad'])+')disktool(17.04+q[1],a+q[0]);\n'
 sc+='for(a=[-90,30,150],q='+j(c['leaf']['trajectory_deg_X_or_rad'])+')rotate([a+q[0],0,0])translate([0,q[1],0])ax(5.91585,2.62830,.93415);}}\n'
 sc+='module inserts(){union(){'+''.join('ann(%f,%f,%f,%f);'%tuple(row) for row in bands())
 for q in lugs():sc+='hull(){' + ''.join('translate('+j(p)+')cube(.00001,center=true);' for p in q[1])+'}'
 sc+='}}\nmodule core(){polyhedron(points='+j(v.tolist())+',faces='+j(idx[:,::-1].tolist())+');}\n'
 sc+='''module roll(r){minkowski(){core();sphere(r=r);}}
module inside(){roll(1.66);}
module shell(){difference(){union(){difference(){roll(2.5);inside();}
 intersection(){inside();union(){for(a=[-30,90,210])rotate([a,0,0])translate([-5,0,-.31])cube([15,14,.62]);ax(4.87,.62,12);}}}
 for(a=[-30,90,210])rotate([a,0,0])translate([0,10.30,0])ax(-5.,14.,2.59);}}
module cup(){// blind back closure over rear of sensor stem, continuous end
 for(a=[-30,90,210])rotate([a,0,0])translate([0,10.30,0]){ann(-2.25,6.62,2.21,2.61);ann(6.62,8.19,2.21,2.67);ax(8.18,.39,2.67);}}
module star(){difference(){cylinder(h=1.44,r=1.76);translate([-.653,-.653,-.01])cube([1.306,1.306,1.47]);for(a=[-90:30:240]) rotate(a)translate([1.31,0,-.01]){cylinder(h=1.46,r=.245);translate([0,0,1.28])cylinder(h=.18,r1=.245,r2=.285);}}}
'''
 sc+='module dog(){difference(){cylinder(h=1.3,r=3.56);translate([0,0,-.01])cylinder(h=1.33,r=.51);for(q='+j(dogcam())+')translate([q[1],q[2],-.01])cylinder(h=1.33,r=.351);}}\n'
 sc+='if(part=="steel")intersection(){rotor();inserts();} if(part=="aluminum")difference(){rotor();inserts();} if(part=="tail")union(){shell();cup();} if(part=="dog")dog();if(part=="star")star();\n'
 (D/'shell-working70.scad').write_text(sc);print('SCAD includes mating Al and finite steel rotor rings (hob tooth cut is analytical only in worm script), tail shell, cam groove and 12-hole dog. Tabbed steel in Al slots, no friction credit.')
 for (n,t,h),r in zip([('disk',1.19,.81),('face',1.10,1.16),('wheel',1.26,.97)],(12,14.95,18.56)):print('one-tab-only 500Nmm edge average bearing',n,500/(r*t*h),'MPa; plus axial loads and slot corner concentration not rated')
 print('dog cam radial wall out/in',3.56-(19.30-min(camlift(p) for p in range(159)))-.351,(19.30-18.15)-.351-.51,'min lift point, parked end z',camlift(12),camlift(0))
 print('backdrive from extraction, at p=0 toward parked negative end flank, dx/dtheta',-.11*pi/2/radians(12),'mm/rad. An inward load has the opposite sign: no unconditional hold.')
 print('peak motion slope, worm dog extraction torque for clean 500/130/1.31 w mu .23 at pin',1.97*pi/(2*radians(144)),1.97*pi/(2*radians(144))*.23*500/130/1.31,'Nmm, vs optimistic 3V motor rated x4x.90=',.156*4*.9,'Nmm, no credit unloading absent load sensing.')
if __name__=='__main__':run()
