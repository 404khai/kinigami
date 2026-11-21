"""Three-site candidate study, not an implemented component; mm, radians.
Intersect convex one-sided barrels. The exposed meridians form circles.
Extend each circle by an angular guard past its equator before a tangent
continues the profile; a loaded edge need not straddle a curvature jump there.
"""
from math import cos,sin,sqrt,radians,pi,hypot,asin
from edge_hertz import hertz
B,H,GUARD=1.045,20.,radians(12)

def profile(u):
    return B-u*u/(H+sqrt(H*H-u*u))

def half_support(x,y):
    # sup dot((x,y),n) over n with n_x >= -sin(GUARD)
    a=hypot(x,y)
    return a if x>=-a*sin(GUARD) else -x*sin(GUARD)+abs(y)*cos(GUARD)

def margin(x,r,t):
    return profile(t)-half_support(x,r),profile(r)-half_support(-x,t)

def support(a,tilt):
    # primary meridian direction cos(a),sin(a); includes all guards
    nt=sin(tilt); t=H*nt; L=profile(t)
    return L*cos(a),L*sin(a),t

def screen():
    # Both surface families are mirror copies. For a working window plus
    # curvature guard at each end, bound the OTHER constraint analytically:
    # on x<0 (overrun), use full norm; on x>=0 use the guarded support.
    W=.70
    worst=max(hypot(B*sin(GUARD),W),B*sin(GUARD)+W*cos(GUARD),W/cos(GUARD))
    guarantee=profile(B)-worst
    print('minimum other-surface margin bound in +/-',W,'mm strip',guarantee)
    assert guarantee>0
    for tilt in (.5,1.,1.5,2.,3.,5.):
        a=radians(tilt)
        t=H*sin(a);offset=(H-B)*2*sin(a/2)
        print(f'tilt {tilt:.1f} deg, centreline t {t:.3f}, equivalent normal lever shift {offset:.3f} mm')
    for F in (18.,30.,43.1,80.):
        _,b,p=hertz(F,1/(1/B+1/.6),H)
        allowed=asin((W-b-.04)/H)*180/pi
        print(f'F {F:g} N patch b={b:.3f} pressure={p/1e3:.3f} GPa; max tilt within verified strip with .04 edge margin {allowed:.2f} deg')
    for i in range(103):
        a=(pi/2+GUARD)*i/102
        for u in (-W,0,W):
            x,r,t=support(a,asin(u/H))
            m=margin(x,r,t)
            assert abs(m[0])<1e-12 and m[1]>=guarantee-1e-12
if __name__=='__main__': screen()
