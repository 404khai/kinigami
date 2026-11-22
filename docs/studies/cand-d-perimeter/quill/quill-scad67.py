from pathlib import Path
import json
def run():
 d=Path(__file__).parent;c=json.loads((d/'quill-cam67.json').read_text());b=json.loads((d/'quill-bolt67.json').read_text());j=json.dumps
 # All geometries in powered frame, mm. Default cutters fully sampled.
 p="""// Take 67: finished-track, bolt, clevis and worm inspection pieces, not a fabrication drawing.
$fn=96; O=17.04; W=2.80; WR=21; part="cam"; // cam, bolt, link, worm, saddle_port
module ax(x,l,r){translate([x,0,0])rotate([0,90,0])cylinder(h=l,r=r);}
module ann(x,h,i,o){difference(){ax(x,h-x,o);ax(x-.01,h-x+.02,i);}}
module cutrad(x,a,lo,hi,r){rotate([a,0,0])translate([x,lo,0])rotate([-90,0,0])cylinder(h=hi-lo,r=r);}
"""
 p+='disk='+j(c['disk']['trajectory_deg_X_or_rad'])+';\nleaf='+j(c['leaf']['trajectory_deg_X_or_rad'])+';\n'
 p+='''module cam(){difference(){union(){
 ann(O-20.29,O-9.07,9.78,13.19);ann(-6.03,-.81,5.97,6.68);ann(-4.18,-3.56,6.32,13.15);ann(-3.85,-3.06,11.93,13.15);
 ann(O-11.69,O-9.04,12.89,20.84);ann(W-.97,W+.97,12.91,18.77);ann(W-1.29,W+1.29,18.56,19.80);}
 for(a=[-30,90,210],q=disk)cutrad(O+q[1],a+q[0],9.47980,11.78020,1.05620);
 for(a=[-90,30,150],q=leaf) rotate([a+q[0],0,0])translate([0,q[1],0])ax(O-11.12415,2.62830,.93415);
 }} // wheel teeth left on finishing blank in this view; analytic generating profile in quill-worm67.py
module bolt(){difference(){translate([W,WR,18.51])cylinder(h=1.55,r=4.53);translate([W,WR,18.49])cylinder(h=1.60,r=.96);
 translate([W+.60,WR-.307,18.49])cube([.65,.614,1.59]);
 for(i=[0:15])translate([W,WR,18.5])rotate(acos(2.60/3.56)+i*22.5)translate([3.56,0,0])union(){cylinder(h=1.60,r=.50);cylinder(h=.17,r1=.66,r2=.50);}}}
module link(){difference(){linear_extrude(.75)hull(){circle(r=.91);translate([4.66,0])circle(r=.91);}translate([0,0,-.01])cylinder(h=.77,r=.626);translate([4.66,0,-.01])cylinder(h=.77,r=.716);}}
module worm(){pitch=PI*.30;h=7.04;steps=900; // genuine axial trapezoid helicoid with a root cylinder
 intersection(){translate([-1.801,-1.801,-3.52])cube([3.602,3.602,h]);union(){translate([0,0,-4.6])cylinder(h=9.2,r=1.145);
 points=[for(i=[0:steps],k=[0:3])let(a=360*i/steps*10,r=(k==0||k==3)?1.144:1.80,w=pitch/4+(1.5-r)*tan(20),z=-5*pitch+pitch*a/360+w*((k<2)?-1:1)) [r*cos(a),r*sin(a),z]];
 faces=concat([[3,2,1,0]],[for(i=[0:steps-1],k=[0:3])[4*i+k,4*i+(k+1)%4,4*(i+1)+(k+1)%4,4*(i+1)+k]],[[4*steps,4*steps+1,4*steps+2,4*steps+3]]);
 polyhedron(points=points,faces=faces,convexity=16);}}}
if(part=="cam")cam(); if(part=="bolt")bolt(); if(part=="link")link(); if(part=="worm")worm();
'''
 (d/'quill-working67.scad').write_text(p);print('editable nominal parts:',len(p),'bytes. Finished cam cuts are applied to all united blanks; tooth hob in independent predicate.')
if __name__=='__main__':run()
