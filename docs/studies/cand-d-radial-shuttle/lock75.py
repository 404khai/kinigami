from carrier75 import *
pp=pi*.30
def worm(x,y,z,a,e=0.):
 r=np.hypot(y-WY,x-(O+WX));ph=np.arctan2(y-WY,x-(O+WX));dz=abs((z-pp*(ph-a)/(2*pi)+pp/2)%pp-pp/2)
 return np.maximum.reduce((abs(z)-3.64-e,r-1.89-e,np.minimum(r-1.235-e,dz-pp/4-(1.60-r)*tan(radians(20))-e)))
def verify():
 # Finite-stock bilateral tooth. Hob overcuts tooth, test ball lies OUT
 # of entire inflated hob sweep (including intersample surface advance).
 a=np.radians(np.arange(-16,16.00001,.008));rb=.007;extra=(2*18.7+2.7+1)*radians(.004)+2*rb;good=[]
 for r in (18.20,18.34,18.48,18.55):
  for b in np.arange(-4.25,3.001,.022):
   ang=radians(b)+a
   if min(worm(0*a+O+WX,r*np.cos(ang),r*np.sin(ang),-122*a,.016))>extra:good.append((r,radians(b)))
 r,b=np.array(good).T
 play=.032+.019+.038*(10.01-8.2)/(11.98-10.84)
 square=degrees(asin(.596/(sqrt(2)*.585))-pi/4)
 rotp=degrees(2*asin(play/(2*2.08)))+square
 print('dog full LOCK shank, release clearance, nominal diametrical play, square/journal and total shaft play',9.66-8.20,9.86-9.66,.064,square,rotp)
 for sg in (-1,1):
  res=[]
  for j in range(12):
   p=radians(j*360/(12*122));hit=None
   for d in np.arange(.01,.70,.01):
    l=b+p+sg*radians(d)
    m=worm(np.full(len(l),O+WX),r*np.cos(l),r*np.sin(l),-122*p)
    if min(m)<-(2*rb+.015+pp*rotp/360):hit=round(d,3);break
   res.append(hit)
  print('12 hole phases, wheel deflection (deg) guaranteeing tooth obstruction, sign',sg,res)
 print('registered park gear angle vs available [68,76]',360*293/(122*12))
 print('disk tooth/spline and self-lock not credited. Input shaft over/under travel & independent power-off unlocking unknown outside registered landed pin.')
if __name__=='__main__':verify()
