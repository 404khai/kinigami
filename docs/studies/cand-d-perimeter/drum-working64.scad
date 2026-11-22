// Exploratory cut parts. X head-local; units mm; no worm teeth/contact rating.
// Choose "cam", "index", "button", or "fork". Axis directions for standalone
// index = +Z and button = +X. Phase is in ring degrees, not motor degrees.
part="cam"; phase=0; $fn=64;
a0=-(atan(.28)+asin(.48));
function ac(z)= z<=10 ? a0+.35*z : z>=44 ? 0 :
 let(v=(z-10)/34) (2*v*v*v-3*v*v+1)*(a0+3.5)+(v*v*v-2*v*v+v)*(.35*34);
function lift(z)=8.35*(1-cos(180*max(0,min(1,(z-48)/51))))/2;
module xc(l,h,r){translate([l,0,0])rotate([0,90,0])cylinder(h=h-l,r=r);}
module tube(l,h,ri,ro){difference(){xc(l,h,ro);xc(l-.01,h+.01,ri);}}
module tool(z,az,inner){
 B=inner?.041650662:.046331553;
 r0=inner?9.5:16.06;r1=inner?11.81:20.05;
 x=inner?-19.03+lift(z):-16.8-4.4*sin(ac(z));cutr=(inner?1.045:.86)+B;
 translate([x,0,0])rotate([az-z,0,0])translate([0,r0-B,0])
 rotate([-90,0,0])cylinder(h=r1-r0+2*B,r=cutr,$fn=48);
}
module rotor(){difference(){
 union(){
 tube(-20.29,-9.39,9.78,13.19);tube(-17.94,-12.39,14.06,17.01);
 tube(-17.90,-16.89,12.82,16.91);tube(-10.41,-7.81,16.84,18.28);
 tube(-12.00,-9.96,16.86,17.33);tube(-12.62,-11.68,14.71,17.37);
 }
 for(j=[0:2],z=[-3.75:.25:106.5]){
 tool(z,-30+j*120,true);tool(z,-90+j*120+atan2(4.68,16.42),false);}
}}
d=sqrt(3.58*3.58+2.81*2.81);c=d*sin(22.5);
module indexwheel(){linear_extrude(1.51) difference(){circle(r=4.22);circle(r=1.02);
 for(j=[0:7])rotate(j*45){translate([d,0])circle(r=2.09);
 rotate(22.5)hull(){translate([d-c,0])circle(r=.42);translate([5,0])circle(r=.42);}}}}
module button(){ // sectional test cartridge with front ball and captive stops
 for(q=[[6.37,7.10,.87,2.49],[1.84,6.52,.87,1.18],[-1.53,-.86,1.17,1.62],
 [-.28,6.61,2.20,2.57],[-.44,.68,1.20,2.54]])tube(q[0],q[1],q[2],q[3]);
 color("orange")union(){translate([-4.31,0,0])sphere(r=2.50);
 xc(-3.05,1.32,1.10);xc(1.08,1.62,2.03);xc(1.45,7.83,.80);}
}
module leafFork(){
 // this model is already shifted to LOCAL horn coordinates in X
 difference(){translate([-1.24,15.70,4.33])cube([2.48,3.90,1.38]);
 translate([-.83,15.65,4.28])cube([1.66,3.94,1.50]);}
}
if(part=="cam")rotate([phase,0,0])rotor();
if(part=="index")indexwheel();
if(part=="button")button();
if(part=="fork")leafFork();
