// Separate trial coupon in HOME face chart, not a Take70 interface.
$fn=96;
module ax(x,h,r){translate([x,0,0])rotate([0,90,0])cylinder(h=h,r=r);}
module ann(x,h,i,o){difference(){ax(x,h,o);ax(x-.01,h+.02,i);}}
module sec(a){rotate([a,0,0])translate([0,10.3,0])for(k=[-1,1])scale([1,1,k])hull(){for(p=[[-6.95,.76],[-6.95,3.80],[-5.30,2.69],[-5.30,1.88]],y=[-.98,.98])translate([p[0],y,p[1]])cube(.001);}}
module seat(){intersection(){sphere(r=8.);translate([-8,-8,-8])cube([2.35,16,16]);}}
module bowl(){intersection(){difference(){sphere(r=8.72);sphere(r=8.05);}translate([-9,-9,-9])cube([3.35,18,18]);}}
union(){ann(-8.55,1.60,12.04,12.42);ax(-8.43,1.48,11.97);for(a=[-30,90,210])sec(a);translate([-2.2,0,0])seat();translate([-2.2,0,0])bowl();
for(i=[0:239])hull(){for(j=[i,i+1])translate([-14.89+3.96*j/240,2.03*cos(6*j),2.03*sin(6*j)])sphere(r=.32);}}
