"""Schematic from the same datums; section projections do not prove clearance."""
from pathlib import Path
from runpy import run_path
g=run_path(str(Path(__file__).with_name('bore-audit-take53.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig,ax=plt.subplots(1,2,figsize=(11,5),constrained_layout=True)
for a in ax:
    a.set_aspect('equal');a.grid(alpha=.2);a.set_xlabel('World X (mm)');a.set_ylabel('World Y (mm)')
a=ax[0];x=F;t=np.linspace(0,pi,200);xx=np.r_[x,x+LEG+R*np.sin(t),x];yy=np.r_[R,R*np.cos(t),-R]
for c,w in [('#bacbd7',11),('white',4),('#006d77',1.5)]:a.plot(xx,yy,color=c,lw=w)
o=A.copy()-[.6,0,0];v=trj(np.array([o+[0,-R,0],o+[0,R,0]]),YMAX,o)
a.plot(v[:,0],v[:,1],color='#9b3c44',lw=5,label='Whiffletree at +17°')
for h,m in zip(v,(-R,R)):a.plot([h[0],F],[h[1],m],color='#006d77',lw=2)
a.plot(o[0],0,'ko',ms=4);a.axvline(F,color='#7c8895',ls=':');a.text(F+.4,-10,'Mating plane')
a.annotate('Head trunnion',o[:2],xytext=(2,3),arrowprops={'arrowstyle':'->'});a.set(xlim=(0,31),ylim=(-15,15),title='Service strands and passive return')
a.legend(loc='upper left',fontsize=8)
a=ax[1]
v=np.array([(A[0],-6,mz),(mx,-6,mz)]+[(mx+magR*sin(t),my+magR*cos(t),mz) for t in np.linspace(0,pi,160)]+[(-16,my-magR,mz)])
for u,shft,lab,col in [(17,0,'Head 1 at +17°','#007d87'),(-17,P,'Head 2 at −17°','#c35542')]:
    w=trj(v,radians(u),A)-[.6,0,0]+[shft,0,0]
    a.plot(w[:,0],w[:,1],c=col,lw=8,alpha=.32);a.plot(w[:,0],w[:,1],c=col,label=lab)
m=adjwall(17,-17,0,.6,.6)[1];a.plot(*m[:2],'k*',ms=10,label='3D solid-wall witness');a.set_title('Adjacent magazine jackets at zero joint yaw');a.set_ylim(-30,6);a.legend(fontsize=8)
fig.suptitle('Take 53 • Bore-laced coupler • exploratory rejected installation',fontsize=13)
fig.savefig(D/'bore-section-take53.png',dpi=145);plt.close(fig)
