"""Installed barrier (all keepers closed), free partial pose, and drive budget."""
from math import acos,cos,hypot,pi,radians,sin,sqrt,tan,degrees
from barrel import hertz
theta=radians(3);R=6.
h=3.53*(1-sqrt(1-((.5+.08+R*(1-cos(theta)))/3.47)**2))
q=.045+(3.97-sqrt(3.97**2-(.18+h)**2))+.08+R*(1-cos(theta))/2
tau=(.09+.16+h)/(1.5*R)
ct=1-(1-sqrt(1-tau*tau)+(q/R)**2/(1+cos(theta)))
print('closed barrier: lift, tangent residual, yz shift, rotation degrees',h,q,4*q/3,degrees(acos(ct)))
assert 4*q/3<.5 and degrees(acos(ct))<3
print('one open, 12 degree chord: free axial and radial shift',
      1.5*R*sin(radians(12)),1.5*R*(1-cos(radians(12))))
for f in [36.93,38.47,43.10,69.71,325.57]:
    print('one pole N; Hertz MPa, patch half-axes',f,hertz(f,1.985,1.48,1.985))
for g,res in [(.10,14.17),(.23,24.91)]:
    for deg in (29,37):
        w=(tan(radians(deg))+.23)/(1-.23*tan(radians(deg)))
        d=(res+2.4)/(1-g*(1.15*w+.10));a=w*d
        normals=sqrt(2)*((1+10/6)*d+2*10.3/6*a)
        print('guide, track degrees, radial, cam axial, stage axial',
              g,deg,d,a,(a+.012*normals+1)/(1-.012*2*sqrt(2)*.12/6))
