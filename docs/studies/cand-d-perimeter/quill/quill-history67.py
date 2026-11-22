from pathlib import Path
from runpy import run_path
def run():
 d=Path(__file__).parent;au=(d/'quill-audit67.py').read_text()
 for name in ('first','pretrim'):
  ctx={'__file__':str(d/'quill-audit67.py'),'__name__':'historical'}
  code=au.replace('quill-install67.py',f'quill-{name}67.py')
  exec(code,ctx);print('===',name)
  if name=='first':
   g=ctx['yaw'].__globals__;g['H']=ctx['H'];ctx['audit']()
  else:
   lo=ctx['leaf'](-90.,0.);cc=ctx['chassis']();print('bearing pin / mount',ctx['cp'](ctx['subset'](lo,('bearing pin','external park')),ctx['subset'](cc,('leaf mount','park stop outer','leaf bearing cap')),2));print('parking disk / motor',ctx['cp'](ctx['subset'](cc,('16 hole',)),ctx['subset'](cc,('clamp motor',)),1))
if __name__=='__main__':run()
