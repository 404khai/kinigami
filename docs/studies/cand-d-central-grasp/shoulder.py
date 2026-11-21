"""Take 18: facing branch, pure-side necessary tilt and flange-head overlap."""
from math import sin,cos,asin,acos,atan,tan,hypot,radians,degrees,sqrt

def out(k,*v):print(k,*(round(x,6) for x in v))
a,ah,b=cos(radians(60.5)),cos(radians(59.5)),sin(radians(59.5))
ml,mh=.39,.41
q=.615
k,kh=1/tan(radians(35.5)),1/tan(radians(34.5))
T=.34+.19+.98
B=3.185
g=.19+(B-sqrt(B*B-.64**2))*hypot(1,mh)
xmin=(b*T-g)/mh
xmax=3.436608+.015+(4.83-2.035802+q*hypot(1,kh))/k
lmin=B-1.02
# At a pure side the shaft interior has d_t=0, its far cap d_t<=0
# on the +t side. Thus O_t>=T, irrespective of cap angle. A near cap is
# buried inside the large sphere. Use both adjacent guard walls for the
# upper bound on r_O and the worst slotted relief for xmin.
rhs=(k-mh/a)*xmin+2.035802-k*(3.436608+.015)-q*hypot(1,kh)-(.19-b*T)/ah
tilt=atan(k)+asin(min(0,rhs/lmin)/hypot(1,k))
out('pure-side: min Ox, max shaft-contact x, min exposed l, min direct pitch deg',
    xmin,xmax,lmin,degrees(tilt))
# xh lies below actual solid plateau. Candidate test points are a line in
# the tail flange, in the horizontal head plane x=xh.
xh=3.08;llo,lhi=4.30,4.36;W=0;Amin=20;Amax=-20
for i in range(1000):
    lo=tilt+(radians(90)-tilt)*i/1000
    hi=tilt+(radians(90)-tilt)*(i+1)/1000
    sl,sh=sin(lo),sin(hi);cl,ch=cos(hi),cos(lo)
    xhio=xmax-lmin*cl
    lat=(g+mh*xhio)/cos(radians(30.5))
    W=max(W,(xhio+lhi*ch-xh)/sl,(xh-xmin)/sl)
    Amax=max(Amax,lat+(lhi+(xhio-xh)*ch)/sl)
    Amin=min(Amin,-lat+(llo+(xmin-xh)*ch)/sh)
out('flange crossing at x=3.08: |downslope coordinate|, head A min,max',W,Amin,Amax)
rlo,rhi=9.10,10.40
assert 0<Amin and Amax<rhi
f=hypot(W,rhi)
# On the branch nearest O_perp (v coordinate), changing head radius
# produces a continuous azimuth arc. If A>rlo it starts at azimuth 0.
arc=min(acos(Amin/rhi)-acos(Amin/rlo),acos(Amax/rhi))
out('sufficient full tail flange radius, guaranteed head azimuth span deg',f,degrees(arc))
assert f<12 and arc>0
# The old 80 degree neck pose is NOT an assembly counterexample.
# The head rays miss its projected flange; the active blade itself intersects it.
e=radians(80);ox,r,t=3.6,-.35,1.53;L=4.33;wid=12
low=r+L*sin(e)-wid*cos(e);hi=r+L*sin(e)+wid*cos(e)
out('80 degree: full flange projected r min,max, nearest R9 positive ray r',
    low,hi,9*cos(radians(30)))
X=3.436608
R=r+(L-(X-ox)*cos(e))/sin(e)
out('80 degree: flange crosses existing working blade at x,r,t',X,R,0)
assert 3.565802<R<6.30 and hi<9*cos(radians(30)) and low>0
