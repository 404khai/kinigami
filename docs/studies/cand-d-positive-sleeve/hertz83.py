"""Exact quadratic elliptical Hertz via complete elliptic integrals (mm, N, MPa)."""
from geo83 import *
from scipy.special import ellipk,ellipe
Estar=210000/(2*(1-.30**2))
def hertz(F,Rlong,Rshort):
    # semiaxes a,b. J_i = int ds / ((i^2+s)*sqrt(s*(a²+s)*(b²+s))).
    # J_long=2(K-E)/(a³ m); J_short=2(E/(1-m)-K)/(a³ m)
    def terms(z):
        m=1-z*z; K=ellipk(m);E=ellipe(m)
        return 2*(K-E)/m,2*(E/(1-m)-K)/m
    z=brentq(lambda z:terms(z)[1]/terms(z)[0]-Rlong/Rshort,.0001,.99999)
    j=terms(z)[0]
    a=(3*F*j*Rlong/(2*pi*Estar))**(1/3);b=a*z
    return dict(a=a,b=b,p=3*F/(2*pi*a*b))
if __name__=='__main__':
    print(json.dumps(dict(label="exploratory",radius_cases={str(R):hertz(60,R,.75) for R in [4,12,30,60,100,200,400,800,1600]}),indent=2))
