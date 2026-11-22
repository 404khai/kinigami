"""Optional drawing (matplotlib); calculations do not depend on it."""
from pathlib import Path
from runpy import run_path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Wedge, Polygon
d=run_path(str(Path(__file__).with_name('fixed-z-stage-take42.py')))
globals().update({k:v for k,v in d.items() if not k.startswith('__')})
f,(a,b,c)=plt.subplots(1,3,figsize=(15,6),layout='constrained')
green,blue,orange,grey='#46856e','#3e6086','#c9823e','#7d7370'
def rect(ax,x,y,k,alpha=.78):
    ax.add_patch(Rectangle((x[0],y[0]),x[1]-x[0],y[1]-y[0],fc=k,alpha=alpha,lw=0))
def label(ax,xy,at,msg):ax.annotate(msg,xy,at,fontsize=8,arrowprops=dict(arrowstyle='->',color='#626a72'))
a.add_patch(Wedge((C,0),R+TUBE,0,360,width=2*TUBE,fc=green,alpha=.65))
for v in BS:a.add_patch(Circle(v[:2],TUBE,fc=green))
for s in slide3():
    if s[0].startswith(('tine','face cross-tie','central stripper')):rect(a,proj(s,X),proj(s,Y),orange,.60)
a.add_patch(Circle((XP,0),PIN,fc=blue))
for s in xs()+zs()+pin():
    if s[0] in ('X motor','Z gearmotor','moving rack stock','X screw','X worm wheel'):
        rect(a,proj(s,X),proj(s,Y),blue,.60)
label(a,(7,-5.04),(2,-23),'rear boss');label(a,(XP,0),(20,6),'pin')
a.set(title='Plan • closed',xlim=(-16,32),ylim=(-26,27),xlabel='X separation [mm]',ylabel='Y [mm]')
for x in (C-R,C+R):b.add_patch(Circle((x,0),TUBE,fc=green))
for x in ((9.75,XP-1.85),(XP+1.85,18.60)):
    b.add_patch(Polygon([(v,v-4.53+t) for v,t in ((x[0],0),(x[1],0),(x[1],.65),(x[0],.65))],fc=grey))
for x in ((XP-3.15,XP-1.80),(XP+1.80,XP+3.15)):rect(b,x,(JMIN,JMAX),grey)
for z in (-4.,4.):rect(b,(.3,16.0),(z-.52,z+.52),orange,.45)
for lift,alpha in ((DZ,.26),(0,.78)):
    rect(b,(XP-PIN,XP+PIN),(TIP+PIN+lift,17.95+lift),blue,alpha)
    b.add_patch(Wedge((XP,TIP+PIN+lift),PIN,180,360,fc=blue,alpha=alpha))
    for s in pin(lift):
        if s[0] in ('U pin crossbar','moving rack stock','pin shank'):rect(c,proj(s,Y),proj(s,Z),blue,alpha)
    c.add_patch(Wedge((0,TIP+PIN+lift),PIN,180,360,fc=blue,alpha=alpha))
for y in ((-3.15,-1.80),(1.80,3.15)):rect(c,y,(JMIN,JMAX),grey)
c.add_patch(Circle((15.50,11.70),2.4,fc=orange))
label(c,(15.50,11.70),(17,4),'fixed pinion')
label(c,(6,36),(-10,32),'raised U')
label(b,(15.6,14),(20,23),'sleeve')
label(b,(16.5,12.0),(21,9),'roof')
b.set(title='XZ • section at Y=0',xlim=(0,34),ylim=(-25,40),xlabel='X [mm]',ylabel='Z withdrawal [mm]')
c.set(title='YZ • folded rack projection',xlim=(-12,30),ylim=(-25,40),xlabel='Y [mm]',ylabel='Z [mm]')
for ax in (b,c):ax.axhline(-23.65,color=grey,lw=.8,ls='--')
for ax in (a,b,c):ax.set_aspect('equal');ax.grid(True,alpha=.13);ax.set_axisbelow(True)
f.suptitle('Take 42 | Fixed upper sleeve, moving indexed face • exploratory, installation rejected')
f.savefig(Path(__file__).with_suffix('.png'),dpi=140)
