"""Take 38/39 continuation, mm and N; local rigid solids, not a gate."""
from math import acos, asin, atan, cos, degrees, hypot, radians, sin, sqrt, tan


def study(A=5., r=2.7, b=1.25, port=1.35, angle=45., reserve=.15, mu=.23):
    # Local origin is on the pin axis, +x towards departing tail.
    assert A > r+b and r > port > b
    a=radians(angle); k=tan(a); d=r+b
    tc=acos(d/A)
    arm=A*sin(tc)
    # |y| <= H + k*x. Offset the faces by r before testing the core circle.
    # Fully drawn, centred and untilted: C=(A-d,0,0), rear core x=-d.
    H=r*hypot(1,k)+d*k+reserve
    # At opposite-pole contact, solve BOTH wall inequalities for cy.
    # Their two lower bounds on H have an optimal common value at midrange.
    Hpair=r*hypot(1,k)+max(arm,d*k)
    # Front-facing wall work applies to an *unbroken planar* wall only.
    # For a p-backed mating body and full sharp rim, the circular disk of
    # intersection in the port plane must fit along its short ellipse axis.
    # This excludes deep intrusion from the front; not a lip-strength test.
    local=a-asin(port/r)-radians(1)
    fx=sin(local)-mu*cos(local)
    print(f'A={A:g}, r={r:g}, pin={b:g}, flare={angle:g}: symmetric home H={H:.4f}, '
          f'pinch tilt={degrees(tc):.3f} deg, H needed={Hpair:.4f}, H-Hpair={H-Hpair:.4f}')
    print(f'  collinear contact station separation {2*arm:.4f}; '
          f'port signed axial work/N {fx:.5f}; lower flare for positive work '
          f'{degrees(atan(mu)+asin(port/r))+1:.3f} deg')
    if k >= tan(tc):
        # Analytic path: rear core always (-d,0,0). Entire core lies on
        # y=(x+d)tan(t), x>=-d. Restoring its tube radius fits the same walls.
        # Projection in xz has semiaxes A*cos(t), A; pin is INSIDE the eye.
        # dist²(axis,centreline)-d² = (1+u)[2*B*(B-d)
        #                                     + A² sin²(t)*(1-u)], u=cos(q).
        # Both terms nonnegative. At t=tc, u=±1 attain zero simultaneously.
        for i in range(51):
            t=tc*i/50; B=A*cos(t)
            for j in range(65):
                q=j*2*3.141592653589793/64; u=cos(q)
                x=B*(1+u)-d; y=A*sin(t)*(1+u); z=A*sin(q)
                assert H+k*x-abs(y) >= r*hypot(1,k)-1e-10
                v=(1+u)*(2*B*(B-d)+(A*sin(t))**2*(1-u))
                assert v>=-1e-10 and abs((x*x+z*z-d*d)-v)<1e-10
        print('  continuous bare-eye path to two cylindrical contacts fits')
    # Opposite x forces are not by themselves self-stress. Moment at middle
    # of contact stations opposes tilt by arm*N per contact. Even an adverse
    # axial friction at x=±b subtracts at most b*mu*N from that moment.
    print(f'  at the symmetric pinch: restoring moment / total N >= {arm-b*mu:.4f} mm; '
          f'withdrawal friction <= {mu:.2f} per N (no guide friction included)')
    return H,Hpair,fx


if __name__=='__main__':
    h,j,f=study(); assert h>j and f>0
    h,j,f=study(A=6.5); assert h<j and f>0
    h,j,f=study(angle=36.); assert f<0
