from containment79 import *
def txt(a):return '['+','.join('%.7g'%x for x in a)+']'
def solid(q):
 n,v,r,d=q;a=np.array(v);r=float(r);d=None if d is None else np.array(d)
 if r==0:
  h=ConvexHull(a);simp=[]
  for f,eq in zip(h.simplices,h.equations):
   f=f.copy()
   if np.cross(a[f[1]]-a[f[0]],a[f[2]]-a[f[0]])@eq[:3]>0:f=f[::-1]
   simp.append(txt(f))
  return 'polyhedron(['+','.join(map(txt,a))+'],['+','.join(simp)+']);'
 if d is None:
  if len(a)>8:
   return 'minkowski(){'+solid(sol(n,v))+' sphere('+str(r)+');}'
  return 'hull(){'+''.join('translate('+txt(p)+') sphere('+str(r)+');' for p in a)+'}'
 if np.linalg.norm(a[-1]-a[0])<1e-8:return ''
 return 'bar('+txt(a[0])+','+txt(a[-1])+','+str(r)+');'
def scene():
 dw,v,vi,vo=covers();f,e,t=rest()
 with open(D/'cutaway79.scad','w') as h:
  def w(s):h.write(s+'\n')
  w('// Take 79 exploratory cutaway; presentation poses do not impose contact.\n$fn=48; key_open=0; input_y=0; latch_angle=0; cover=true; mating_tail=false; section=true;')
  w('module bar(a,b,r){u=b-a; h=norm(u); translate(a) if(norm(cross([0,0,1],u))>1e-6) rotate(acos(u.z/h),cross([0,0,1],u)) cylinder(h=h,r=r); else if(u.z>=0) cylinder(h=h,r=r); else rotate([180,0,0]) cylinder(h=h,r=r);}')
  def mod(n,f):
   w('module '+n+'(){union(){')
   for q in f:w('// '+q[0]+'\n'+solid(q))
   w('}}')
  mod('fixed_frame',[q for q in fixed() if not (q[0].startswith('driver blocking material') or q[0]=='drive pin at rear dwell')]+enclosure());mod('key_carriage',keyplus()+followers(0));mod('input_cup',bridge(0));mod('cam_lock',eccentric(0));mod('relay_driver',regmat());mod('neighbor',tail());mod('other',f+e+t);mod('ram',ejection()[:1]);mod('sleeve',ramfixed())
  w('module physicalwheel(){translate(['+str(LX)+','+str(LY)+','+str(ZW[0])+']) rotate([0,0,270]) linear_extrude('+str(ZW[1]-ZW[0])+') difference(){circle('+str(RO)+');square(1.292,center=true);for(a=[0:90:270])rotate(a){translate([0,-5.5])circle(2.748);rotate(-45)translate([5.5-5.5/sqrt(2)-.45,-.44])square([5,.88]);}}}')
  w('module skin(){difference(){'+solid(sol('outer',vo))+solid(sol('inner',vi))+'bar([-9.68,0,0],[5,0,0],14.10);bar([-49,0,0],[-23.60,0,0],10.85);}}')
  w('module coil(k){L=11.40+input_y-key_open; for(i=[0:159]){a=20*360*i/320;b=20*360*(i+1)/320;bar(['+str(RX)+'+1.675*cos(a),.80+key_open+.275+(L-.55)*i/160,k*7.65+1.675*sin(a)],['+str(RX)+'+1.675*cos(b),.80+key_open+.275+(L-.55)*(i+1)/160,k*7.65+1.675*sin(b)],.275);}}')
  w('module drawing(){color("Gainsboro")fixed_frame(); color("DarkOrange")translate([0,key_open,0])key_carriage();color("Teal")translate([0,input_y,0])input_cup();for(k=[-1,1])color("SaddleBrown")coil(k);color("RoyalBlue")translate(['+str(LX)+','+str(LY)+',0])rotate([0,0,latch_angle])translate(['+str(-LX)+','+str(-LY)+',0]){cam_lock();physicalwheel();}color("DimGray")relay_driver();color("LightGray")other();color([.9,.1,.1,.2]){sleeve();ram();}if(cover)color([.2,.5,.7,.24])skin();if(mating_tail)color("Wheat")neighbor();}\nif(section)intersection(){drawing();translate([-80,-50,-45])cube([90,100,52]);}else drawing();')
if __name__=='__main__':scene();print('editable sectional SCAD generated; aggregate material/gear envelopes not a tolerance model')
