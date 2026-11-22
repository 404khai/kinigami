"""Finite crowned line/edge pressure, frictionless elastic half-spaces, cell-integrated kernel."""
from hertz83 import *
from scipy.fft import rfft2,irfft2,next_fast_len
from pathlib import Path
def profile(t):
    return t*t/1600+np.maximum(abs(t)-1.20,0)**2/6 # blended parabolic end relief
def bem(F,tilt,Rs=.75,nx=48,nt=144):
    dx=.18/nx;dt=2.96/nt; area=dx*dt
    x=(np.arange(nx)+.5)*dx-.09;t=(np.arange(nt)+.5)*dt-1.48
    H=x[:,None]**2/(2*Rs)+profile(t)[None,:]+sin(rad(tilt))*t
    m,n=next_fast_len(2*nx),next_fast_len(2*nt)
    xx=np.minimum(np.arange(m),m-np.arange(m))[:,None]*dx;tt=np.minimum(np.arange(n),n-np.arange(n))[None,:]*dt
    def P(x,y):return x*np.arcsinh(y/abs(x))+y*np.arcsinh(x/abs(y))
    G=(P(xx+dx/2,tt+dt/2)-P(xx-dx/2,tt+dt/2)-P(xx+dx/2,tt-dt/2)+P(xx-dx/2,tt-dt/2))/(pi*Estar)
    k=rfft2(G); target=F/area
    def K(p):return irfft2(k*rfft2(p,s=(m,n)),s=(m,n))[:nx,:nt]
    def proj(v):
        s=np.sort(v.ravel())[::-1];avg=(np.cumsum(s)-target)/(np.arange(len(s))+1);cut=avg[np.where(s>avg)[0][-1]]
        return np.maximum(v-cut,0)
    p=np.zeros_like(H);y=p.copy();L=float(k.real.max())
    for i in range(2001):
        g=K(y)+H; q=proj(y-g/L)
        y=q+i/(i+3)*(q-p);p=q
        if i%25==0:
            gap=K(q)+H;res=float((gap*q).sum()/target-gap.min())
            if res<1e-9:break
    mask=p>.01*p.max()
    return dict(tilt=tilt,F=F,n=[nx,nt],max_MPa=p.max(),halfwidth_x=(max(x[mask.any(axis=1)])+dx/2),
        t_extent=[min(t[mask.any(axis=0)])-dt/2,max(t[mask.any(axis=0)])+dt/2],normal_residual=abs(p.sum()*area-F),
        complementarity_mm=res,iterations=i+1)
if __name__=='__main__':
    peak=json.loads((Path(__file__).parent/'toe83.json').read_text())['cases']
    f=peak['0.0']['cage45_table']['F'];light=peak['0.2']['cage45_fault']['F']
    print(json.dumps(dict(label='exploratory',elliptic_nominal=hertz(41.204,800,.75),actual_toe_hertz=hertz(f,800,.75),
        actual_toe_F=f,reset_example_F=light,
        pressures=[bem(F,a,nx=n,nt=n*3) for F,a in [(41.204,0),(60,0),(60,.25),(60,1.0),(f,0),(f,.25),(light,0),(light,.25)] for n in [32,64]]),indent=2))
