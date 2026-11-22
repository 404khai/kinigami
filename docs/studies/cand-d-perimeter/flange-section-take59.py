"""Local meridian cut, explicitly not a 3D clearance calculation."""
from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('flange-cam-take59.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
plt.rcParams.update({'svg.hashsalt':'flange-59','font.size':8,'font.family':'DejaVu Sans'})
def diagram():
 fig,axes=plt.subplots(1,2,figsize=(8.2,3.8),sharey=True)
 for ax,s,dx,title in zip(axes,(0,ST),(0,TR),('Loaded geometry · nominal','Open jaws · hypothetical following tail')):
  cx=-2.25+dx;t=np.linspace(-pi/2,pi/2,100);xy=np.vstack(([cx-RE,0],np.c_[cx+RE*np.sin(t),R+RE*np.cos(t)],[cx+RE,0]))
  def poly(v,color,label):ax.add_patch(Polygon(v,facecolor=color,edgecolor='#25374a',lw=.7,label=label))
  poly(xy,'#92b89f','solid flange')
  m=.38;xw=J['tip_x'];rw=R+RE/hypot(1,m);x=np.linspace(-3.50,-.38,130);r=np.maximum.reduce((rw-m*(x-xw),14.514+2.20*(x+.38),x*0+11.33))
  poly(np.vstack((np.c_[x,r+s],[-.38,16.60+s],[-3.50,16.60+s])),'#ce915e','radial shoe')
  x0=HOME+dx;poly([(x0-1.45,0),(x0-1.45,RD-.42),(x0,RD),(x0,0)],'#77a6c6','solid ejector')
  for l,h in ((HOME-.10,-3.61),(-.27,0)):poly([(l,14.5+.28*l),(h,14.5+.28*h),(h,16.02),(l,16.02)],'#b9bcc6',None)
  ax.plot([HOME-.1,0],[14.5+.28*(HOME-.1),14.5],':',color='#5a6578',label='bore datum at window')
  ax.axvline(0,color='#576477',alpha=.55,lw=.8);ax.set(aspect='equal',xlim=(-8.5,8.5),ylim=(0,19.25),xlabel='local X (mm)',title=title);ax.grid(alpha=.17)
 axes[0].set_ylabel('radius at jaw centre plane (mm)')
 h,l=axes[0].get_legend_handles_labels();fig.legend(h,l,ncol=4,loc='lower center',frameon=False)
 fig.suptitle('Take 59 · peripheral clamp and solid ejector',fontweight='bold')
 fig.subplots_adjust(bottom=.18,top=.84,wspace=.10)
 path=D/'flange-section-take59.svg'
 fig.savefig(path,metadata={'Date':None},bbox_inches='tight')
 path.write_text(''.join(line.rstrip()+'\n' for line in path.read_text().splitlines()))
if __name__=='__main__':diagram()
