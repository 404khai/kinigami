"""Independent read-only check of the Take 67 seated radial slide load path."""
from pathlib import Path
from runpy import run_path
import numpy as np

g=run_path(str(Path(__file__).with_name('quill-install67.py')))
X=g['X'];f=g['chassis']()
for a in g['AZ']:
    n=g['U'](a+90);r=g['U'](a)
    q=g['sliders'](a,g['A0'])
    pin=next(s for s in q if s[0]=='slider link pin '+str(a))
    roller=next(s for s in q if s[0]=='face roller '+str(a))
    beam=next(s for s in q if s[0]=='axial transfer beam '+str(a))
    mean=lambda s:np.mean(g['ext'](s,X[None]))
    cheeks=[s for s in f if s[0].startswith(f'slider guide cheek ({a},')]
    assert len(cheeks)==4
    gap=min(max(g['ext'](c,(sg*n)[None])[0][0]-g['ext'](beam,(sg*n)[None])[1][0]
                for sg in (-1,1)) for c in cheeks)
    # Any normal reaction parallel to t, wherever applied, has no t moment.
    arm=mean(pin)-mean(roller)
    proj=np.cross(arm*X,r)@n
    assert abs(proj-arm)<1e-8 and gap>0
    print('azimuth, cheek flank gap, pitch couple per radial N, sum normal / F for hypothetical 5mm span',
          a,round(gap,4),round(proj,4),round(2*abs(proj)/5,4))
