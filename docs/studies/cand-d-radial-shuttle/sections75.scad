// Exploratory Take75. Coordinates are local to lip unless part="pods" (WORLD).
// Smooth analytic intent; facets are display discretization. Not shop files.
use <pods75.scad>
$fn=120;
part="front"; // front, plug, rotor, dog, star, pods
q=0; // radial displacement from LOCK (0..1.8391)
function rad(x)=max(14.56+.52*x,14.56-(.52-.25)*1.095+.25*x);
module cutbore(x1,x2){
 translate([x1,0,0])rotate([0,90,0])cylinder(h=x2-x1,r1=rad(x1),r2=rad(x2));
}
module rawblock(a,b,c,d,e,f){translate([a,c,e])cube([b-a,d-c,f-e]);}
module ann(l,h,i,o){difference(){translate([l,0,0])rotate([0,90,0])cylinder(h=h-l,r=o);translate([l-.01,0,0])rotate([0,90,0])cylinder(h=h-l+.02,r=i);}}
module parktoe(){difference(){
 rawblock(-1.04,-.125,0,19.7391,-2.25,2.25);
 cutbore(-1.041,-.124);
 linear_extrude(height=6,center=true)polygon([[-1.041,0],[-.124,0],[-.124,12.75-.75*(-.124+.75)+1.8391],[-1.041,12.75-.75*(-1.041+.75)+1.8391]]);
}}
module plug(){union(){
 translate([0,q-1.8391,0])parktoe();
 translate([0,q,0])union(){
 rawblock(-4.50,-.70,15.72,16.55,-.89,.89);rawblock(-4.50,-2.04,15.72,20.72,-.89,.89);
 for(b=[[16.05,16.70],[20.0,20.70]],s=[-1,1])rawblock(-4.50,-2.04,b[0],b[1],min(s*.75,s*2.20),max(s*.75,s*2.20));
 translate([-6.95,18.35,0])rotate([0,90,0])cylinder(h=3.15,r=.60);
 translate([-6.89,18.35,0])rotate([0,90,0])difference(){cylinder(h=1.70,r=.90);translate([0,0,-.01])cylinder(h=1.72,r=.605);}
 }}}
module roof(l,h,top,tl,th){difference(){rawblock(l,h,0,top,tl,th);if(l < -1.095){cutbore(l-.001,-1.095);cutbore(-1.095,h+.001);}else cutbore(l-.001,h+.001);}}
module front(){roof(-.075,0,17.90,-3.15,3.15);roof(-7.0,-1.09,15.46,-3.15,3.15);for(s=[-1,1])roof(-1.09,-.075,17.90,min(2.30*s,3.15*s),max(2.30*s,3.15*s));
 for(s=[-1,1],x=[[-4.86,-4.503],[-2.037,-1.69]])rawblock(x[0],x[1],15.76,22.64,min(s*1.03,s*2.61),max(s*1.03,s*2.61));
}
function clip(x,l,h)=min(h,max(l,x));
function travel(a)=1.8391*(1-cos(180*clip((a-4)/64,0,1)))/2;
module cutter(a,j){rotate([j-a,0,0])translate([-6.97,18.35+travel(a),0])rotate([0,90,0])cylinder(h=2.0,r=.90422,$fn=60);}
module rotor(){difference(){union(){ann(-7.03,-5.03,16.75,21.61);ann(-8.28,-7.02,18.68,20.99);ann(-8.62,-8.26,16.4,19.63);ann(-9.99,-8.23,15.91,18.61);}for(j=[-90,30,150],a=[-4:.125:75.875])hull(){cutter(a,j);cutter(a+.125,j);}}} // wheel blank: tooth material defined by swept worm in lock75.py
module star(){difference(){cylinder(h=1.46,r=2.75);translate([-.596,-.596,-.01])cube([1.192,1.192,1.48]);for(a=[0:30:330])rotate([0,0,a])translate([0,-2.08,-.01])cylinder(h=1.48,r=.382);}}
function retract(a)=2.04*(1-cos(180*clip((a-4)/116,0,1)))/2;
module dc(a){rotate([0,0,-a])translate([0,-3.03+retract(a),-.76])cylinder(h=1.52,r=.286);}
module dog(){difference(){translate([0,0,-.72])cylinder(h=1.44,r=3.44);for(a=[-4:.25:123.75])hull(){dc(a);dc(a+.25);}}}
if(part=="front"){for(a=[-90,30,150])rotate([a,0,0]){front();color("gold")plug();}}
if(part=="plug")plug(); if(part=="rotor")rotor();if(part=="dog")dog();if(part=="star")star();if(part=="pods")pods();
