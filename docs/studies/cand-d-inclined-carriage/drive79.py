from installed79 import *
SZ=9.85;MZ=SZ;MX=SX-5.40
def screwdriver():
 f=[ax('threaded key lead screw',1,7.04,22.35,(SX,SZ),1.75),ax('screw lower journal',1,-1.42,7.18,(SX,SZ),1.24),ax('screw upper journal',1,22.22,24.06,(SX,SZ),1.15),
    ax('screw 36T wheel',1,22.58,23.83,(SX,SZ),3.79),ax('shaft crown 18 teeth',1,.70,2.10,(SX,SZ),3.16),
    ax('screw integral thrust flange',1,5.37,5.84,(SX,SZ),2.51)]
 for lo,hi in ((4.35,5.35),(5.86,6.94)):
  f+=ann('screw thrust bush',[SX,lo,SZ],[SX,hi,SZ],1.26,2.23)
 f +=[ax('motor 18T pinion',1,22.57,23.84,(MX,MZ),1.99),ax('motor fuse spindle',1,20.29,23.90,(MX,MZ),.49),ax('key 0615 256',1,-12.43,20.37,(MX,MZ),3.0),
    cyl('screw thrust bridge',[SX-2.06,5.95,SZ],[SX-4.10,6.19,SZ+2.25],.59),
    cyl('motor rear mount',[MX-2.7,-9.5,MZ],[MX-4.00,-9.5,MZ+2.65],.75)]
 return f
def car(c):
 f=[q for q in driver(0) if not q[0].startswith(('antirotating input nut','driver roof tie','driver pickup ledge'))]
 f+=ann('travel nut steel',[SX,11.15,SZ],[SX,13.85,SZ],1.44,2.20,32)
 # A real, transverse rear crossmember connects the far spring even with
 # the screw moved off the 78 center corridor; no bridge through the ram.
 f +=[bx('spring input crossmember',(SX+.61,SX+2.40),(12.19,12.89),(-ZR-.66,SZ+.48))]
 for k in (-1,1):
  z=k*ZR
  f +=[bx('spring roof root '+str(k),(SX+.64,RX+.54),(12.19,12.91),(z-.89,z+.89)),bx('catch ledge '+str(k),(RX-1.02,RX+.85),(12.20,12.85),sorted((z+k*.21,z+k*1.89)))]
 # Carriage anti-roll: two axially long through-rods in split bushings;
 # fixed rods at x=-17.93, z +/-6.65, not on the key or contact branch.
 for k in (-1,1):
  z=k*7.43
  f+=ann('input slide bushing '+str(k),[-18.03,10.90,z],[-18.03,14.14,z],.91,1.42)
  f.append(cyl('input bushing root '+str(k),[-17.00,12.45,z],[-14.38,12.45,z],.63))
 return move(f,c*Y)
def fixedguide():
 f=[]
 for k in (-1,1):
  z=k*7.43
  f.append(ax('input anti-roll rail '+str(k),1,9.49,23.15,(-18.03,z),.88))
  for y in (9.88,22.83):f.append(cyl('input rail pedestal '+str((k,y)),[-18.03,y,z],[-19.70,y,z+1.23*k],.83))
 # end shoulders for output catches define physical s_min and s_max even
 # with socket absent. Stop captures the rear runner's outside wing.
 for k in (-1,1):
  z=k*(ZR+2.80)
  f += [bx('key open stop '+str(k),(RX-.76,RX+.37),(18.88+4.88,18.88+5.44),sorted((z-.18,z+.18))),
        bx('key inner limit '+str(k),(RX-.76,RX+.37),(-1.00,-.49),sorted((z-.18,z+.18)))]
 return f
def rest():
 F=move(ref['yaw_fixed'],JR)+move(ref['feet'],SH)
 E=move(ref['elec'],SH)+[bx('brake bridge addition',(-26.,-22.6),(8.3,12.2),(-4.0,-2.4))]
 A=move(tail(),-PITCH*X)+move(ref['yaw_turn'],JR)
 return F,E,A
def springvalues():
 return 79000*.55**4/(8*3.35**3*8),14.80,10*.55
def show():
 k,free,solid=springvalues()
 print('two spring .55 wire/3.35 mean/8 active, k each, free, solid, lock/park/early jam forces. units N')
 for s,c in ((0,0),(4.85,8.07),(4.85,0),(-.30,0)):
  L=11.40+c-s;print(s,c,L,max(0,2*(free-L)*k),L-solid)
 print('worst jam test before solid if margin <=0; no force limit after coil bind')
 print('4.5-turn nut lead .60, 8.07 motion ACTUAL rev',CMAX/.60,'guide parking allowances - self-lock not credited')
if __name__=='__main__':show()
