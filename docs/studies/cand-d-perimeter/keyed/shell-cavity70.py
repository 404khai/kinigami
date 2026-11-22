from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('shell-material70.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def run():
 # Separate alternative FIT coupon only. Six flats on one solid plate,
 # capped spherical cup and one coaxial compression coil inside integral
 # rim; not added to Take70 mass or granted any Take70 retention result.
 # Sectional rings bounded inside a true spherical shell (intersect radial
 # envelopes for all X in an axial slab); true material for overlap tests.
 sc='''// Separate trial coupon in HOME face chart, not a Take70 interface.
$fn=96;
module ax(x,h,r){translate([x,0,0])rotate([0,90,0])cylinder(h=h,r=r);}
module ann(x,h,i,o){difference(){ax(x,h,o);ax(x-.01,h+.02,i);}}
module sec(a){rotate([a,0,0])translate([0,10.3,0])for(k=[-1,1])scale([1,1,k])hull(){for(p=[[-6.95,.76],[-6.95,3.80],[-5.30,2.69],[-5.30,1.88]],y=[-.98,.98])translate([p[0],y,p[1]])cube(.001);}}
module seat(){intersection(){sphere(r=8.);translate([-8,-8,-8])cube([2.35,16,16]);}}
module bowl(){intersection(){difference(){sphere(r=8.72);sphere(r=8.05);}translate([-9,-9,-9])cube([3.35,18,18]);}}
union(){ann(-8.55,1.60,12.04,12.42);ax(-8.43,1.48,11.97);for(a=[-30,90,210])sec(a);translate([-2.2,0,0])seat();translate([-2.2,0,0])bowl();
for(i=[0:239])hull(){for(j=[i,i+1])translate([-14.89+3.96*j/240,2.03*cos(6*j),2.03*sin(6*j)])sphere(r=.32);}}
'''
 (D/'shell-coupon70.scad').write_text(sc)
 # inner certificate for the central bowl floor: axial shell on axis spans
 # -10.92..-10.25; exact contained ball lies on central normal.
 c=O*X+(-2.20-(8.72+8.05)/2)*X;r=(8.72-8.05)/2
 print('trial spherical bowl sphere center',sh(c),'radius',r,'within fixed quill radial .335 <3.44 and inside its X stubs',float(c[0]-O-r),float(c[0]-O+r))
 print('one spring R2.03 mean +.32 wire; center x -14.89..-10.93 fully inside quill even with wire; plate needs angular travel, spring limiting and inclinations/load measurement unproved')
 print('coupon fails at HOME alone; translating coupon all 8.53 mm cannot fix home. Does not exclude all sector or shallow architectures. Alternative only, not part of mass or rotor holds.')
if __name__=='__main__':run()
