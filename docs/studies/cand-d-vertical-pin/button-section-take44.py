"""Orthographic study views (illustrative; not collision tests)."""
from runpy import run_path
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle,Polygon
g=run_path(str(Path(__file__).with_name('button-bounds-take44.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def runfig():
    fig,ax=plt.subplots(1,3,figsize=(14,5),constrained_layout=True)
    for a,h in zip(ax,['A   Face alone: YZ projection','B   Own tail: XY at +15°','C   Lowered interface: XZ']):
        a.set_title(h,loc='left',weight='bold',fontsize=12);a.set_aspect('equal');a.grid(True,lw=.4,alpha=.3);a.set_axisbelow(True)
    def rect(a,s,i,j,c,alpha=.25):
        ax0=(X,Y,Z);lo,hi=proj(s,ax0[i]);b,t=proj(s,ax0[j]);a.add_patch(Rectangle((lo,b),hi-lo,t-b,facecolor=c,edgecolor=c,alpha=alpha))
    a=ax[0]
    for axn in face3():
        if axn[0].startswith(('beam','lower bridge','side pillar','upper bridge','middle bridge','stripper','force stalk')):rect(a,axn,1,2,'#197065',.35)
    for j,b in enumerate(BOSS):
        a.add_patch(Circle(b[1:],r,facecolor='#f4d497',edgecolor='#7f501c',alpha=.8))
        for p in POLES[j]:a.plot(p[1],p[2],'o',c='#982c32',ms=5)
    a.set(xlim=(-17,17),ylim=(-15,15),xlabel='y (mm)',ylabel='z (mm)');a.text(0,-14.4,'6 working lands; 4 × 4 mm beams',ha='center',fontsize=9)
    a=ax[1];zm=next(s for s in zz2() if s[0]=='Z motor');rect(a,zm,0,1,'#a92c3c',.48)
    t=bf(36);bb=yaw(next(s for s in t if s[0]=='boss2'),radians(15))[1][0]
    for j in range(3):
        b=yaw(next(s for s in t if s[0]=='boss'+str(j)),radians(15))[1][0]
        a.add_patch(Circle(b[:2],r,facecolor='#e6b65c',edgecolor='#7f501c',alpha=.75))
    for n,c in [('yaw gearmotor','#225e8c'),('stationary central knuckle','#4b5158')]:
        s=next(s for s in tucked_joint() if s[0]==n);a.add_patch(Circle(s[1][0][:2],s[2],color=c,alpha=.8))
    q=nearest(bb,zm);a.plot(*q[:2],marker='x',c='black',ms=8);a.annotate('Z motor / boss',q[:2],(-16,-25),arrowprops={'arrowstyle':'->'},fontsize=8)
    a.text(-3.5,23.1,'yaw motor',ha='center',fontsize=8)
    a.set(xlim=(-35,7),ylim=(-27,26),xlabel='x (mm)',ylabel='y (mm)')
    a=ax[2];s=next(s for s in electr() if s[0]=='cell');rect(a,s,0,2,'#4c5e73',.55)
    b=plus(BOSS[0],(-36,0,-7));a.add_patch(Circle((b[0],b[2]),r,facecolor='#e6b65c',edgecolor='#7f501c',alpha=.7))
    shoe=move(next(s for s in xd2() if s[0]=='block mounting foot'),(0,0,-7));rect(a,shoe,0,2,'#197065',.7)
    a.axhline(-23.65,color='#933',ls='--');a.text(-22,-25.2,'floor −23.65',fontsize=8)
    a.plot(-17.60,-16.50,'kx');a.text(-15.4,-18,'cell',color='white',fontsize=9);a.text(8.4,-25,'guide foot',ha='center',fontsize=8)
    a.set(xlim=(-26,22),ylim=(-30,-5),xlabel='x (mm)',ylabel='z (mm)')
    fig.suptitle('Take 44  |  Moving registry and two installed-volume witnesses',weight='bold',fontsize=16)
    fig.savefig(Path(__file__).with_name('button-section-take44.png'),dpi=155)
if __name__=='__main__':runfig()
