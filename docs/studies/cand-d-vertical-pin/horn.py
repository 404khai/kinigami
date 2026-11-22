"""Exploratory curved-button section, dimensions mm; no gate input."""
from dataclasses import dataclass
from math import atan, cos, degrees, exp, hypot, log, pi, radians, sin, sqrt, tan
import numpy as np
from scipy.optimize import differential_evolution, minimize_scalar


@dataclass
class Horn:
    L: float = 16.  # pivot to actual aft working pole at lock
    b: float = .9   # polar section radius at working angle
    beta: float = atan(.32)
    mu: float = .23
    def __post_init__(self):
        self.rc=self.L+self.b
        self.rate=tan(self.beta)*self.L/(self.rc+self.b)
        self.ox=7.5+4.2*cos(self.beta)-self.L
        self.oz=4.2*sin(self.beta)
        self.lo=log((self.rc+.22)/(self.rc+self.b))/self.rate
    def width(self,t):
        return self.b+(self.rc+self.b)*np.expm1(self.rate*t)
    def opening(self,t):
        f=self.width(t); r=self.rc-f
        a=atan(self.rate)-radians(1.)
        # Worst tangent-plane friction, no assumed cancellation or load split.
        return r*(sin(a)-self.mu*cos(a))
    def dist(self,pose,psi,theta,phi=0.):
        # Distance from one ball centre to the disk of horn material at theta.
        x,y,z=pose(psi); u=theta+phi; c,s=np.cos(u),np.sin(u)
        r,t=(x-self.ox)*c+(z-self.oz)*s,-(x-self.ox)*s+(z-self.oz)*c
        return np.hypot(t,np.maximum(0.,np.hypot(r-self.rc,y)-self.width(theta)))
    def cut(self,high,park,stock=.4):
        # Conservative sampled angle intervals: each true rotating slice
        # can be enclosed in a corresponding sampled disk inflated by eps.
        # For fixed total angle u, the widest disk is at min(u, high).
        m=tan(radians(28)); H=7.53675; xp=12.389796
        us=np.linspace(self.lo,high+park,4097)
        dt=us[1]-us[0];f=self.width(np.minimum(high,us))
        Rmax=self.rc+self.width(high)
        eps=(Rmax+self.rate*Rmax)*dt/2+1.e-8
        K=self.oz-H-m*(self.ox-xp)
        A=np.sin(us)-m*np.cos(us)
        pad=eps*hypot(1,m)
        rl,ru=self.rc-f,self.rc+f
        # K+A*r must lie in the band [-pad, stock+pad].
        good=(K+np.minimum(A*rl,A*ru)<=stock+pad)&(K+np.maximum(A*rl,A*ru)>=-pad)
        rl,ru,f,A,u=rl[good],ru[good],f[good],A[good],us[good]
        nz=abs(A)>1.e-13
        p=(-K-pad)/np.where(nz,A,1.);q=(stock+pad-K)/np.where(nz,A,1.)
        rl=np.where(nz,np.maximum(rl,np.minimum(p,q)),rl)
        ru=np.where(nz,np.minimum(ru,np.maximum(p,q)),ru)
        w=np.sqrt(np.maximum(0.,f*f-np.maximum(0.,np.maximum(rl-self.rc,self.rc-ru))**2))
        x1=rl*np.cos(u); x2=ru*np.cos(u)
        return (self.ox+min(np.minimum(x1,x2))-eps,self.ox+max(np.maximum(x1,x2))+eps,max(w)+eps)
    def depth(self,lo,hi,phi):
        # Signed normal height of every parked disk above the inclined floor.
        a=radians(28); t=np.linspace(lo,hi,1025); u=t+phi
        v=(self.oz-7.53675)*cos(a)-(self.ox-12.389796)*sin(a)
        F=self.width(t); s=np.sin(u-a)
        d=v+self.rc*s-F*abs(s)
        return min(d)-(t[1]-t[0])*(self.rc+self.width(hi))*(1+self.rate)/2


def ring(p):return (15+7.5*np.cos(p),7.5*np.sin(p),0.)


def run(L=16.,high=.8):
    h=Horn(L); lo=h.lo
    for phi in np.arange(.40,1.5,.01):
        cut=h.cut(high,phi)
        if cut[-1]+.16>=4.2:continue
        half=cut[-1]+.16; reach=5.70-sqrt(4.20**2-half**2)
        depth=h.depth(lo,high,phi)
        if depth>reach+.4*cos(radians(28))+.25:break
    else:return None
    # The upper end and attached support must remain wholly behind the skin
    # during lock/withdrawal, not just in the parked position. Distances
    # to the actual sides, aft wall and top, including axle, are separate.
    end=[h.depth(high-.000001,high,g) for g in np.linspace(0,phi,101)]
    start=min(end)-phi/200*(h.rc+h.width(high))
    return (h,high,phi,cut,reach,depth,start)


if __name__=='__main__':
    for L in (10.,12.,14.,16.,18.,20.,24.):
        res=next((v for hi in np.arange(.38,1.35,.02) if (v:=run(L,hi)) and v[-1]>4.),None)
        if not res: print('no covered end in sweep',L);continue
        h,hi,phi,cut,reach,depth,start=res
        D=differential_evolution(lambda a:h.dist(ring,*a),[(0,2*pi),(h.lo,hi)],seed=0,tol=1e-11)
        print('L, arc end/park deg, cut (xmin,xmax,w), reach/depth/root, torque/N, home gap:',
              L,np.round(np.degrees([hi,phi]),2),np.round(cut,3),np.round([reach,depth,start,h.opening(hi),D.fun-4.2],4))
