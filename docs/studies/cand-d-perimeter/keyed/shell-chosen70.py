from runpy import run_path
from pathlib import Path
g=run_path(str(Path(__file__).with_name('shell-cell70.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
def run():
 n=U(-90);u=U(0);m=np.cross(n,u);M=np.column_stack((u,m,n));z=cell();r=offset([sol(q[0],np.array(q[1])@M.T,q[2]) for q in z],np.array([-7.5,0.,-17.5]));(D/'shell-cell70.json').write_text(json.dumps(r,separators=(',',':'))+'\n');print('world cell axes L/W/T, center',M,[-7.5,0,-17.5])
if __name__=='__main__':run()
