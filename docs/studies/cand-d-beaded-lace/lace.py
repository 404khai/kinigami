"""Take 52: deterministic local fixture screens, not physical validation."""
from itertools import product
from json import dump
from math import asin, atan2, ceil, cos, degrees, dist, exp, hypot, pi, radians, sin, sqrt, tan
import sys


RMIN, RMAX, PITCH, STEM = 1.15, 1.25, 3.40, .35
LIP, BORE, TURN, LEG = 1.25, 1.65, 6., 3.5
ARM, DIST, SERVICE, STOP = 6., 10., radians(17), radians(20)
ERROR, DRAG, MU, DRAW, ECC = radians(3), .50, .23, 39., .08


def show(name, *v):
    print(name, *(f'{x:.8f}' for x in v))


def leg_lengths(t, d=DIST):
    return [hypot(d+s*ARM*sin(t), ARM*(1-cos(t))) for s in (-1,1)]


def equilibrium(matrix, target):
    a=[list(row)+[b] for row,b in zip(matrix,target)]
    for j in range(len(a)):
        k=max(range(j,len(a)),key=lambda k:abs(a[k][j]))
        a[j],a[k]=a[k],a[j]
        assert abs(a[j][j])>1e-10
        c=a[j][j];a[j]=[v/c for v in a[j]]
        for k in range(len(a)):
            if k==j:continue
            c=a[k][j];a[k]=[x-c*y for x,y in zip(a[k],a[j])]
    return [row[-1] for row in a]


def cross(a,b):
    return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]


def dot(a,b):
    return sum(x*y for x,y in zip(a,b))


def seats():
    cols=[]
    for j in range(3):
        a=j*2*pi/3
        q=[0,13*cos(a),13*sin(a)]
        for s in (-1,1):
            n=[.5,-s*sqrt(3)/2*sin(a),s*sqrt(3)/2*cos(a)]
            cols.append(n+cross(q,n))
    mat=list(zip(*cols))
    # This is an existence witness with zero tangential force at six sites.
    for wrench in ([DRAW,0,0,0,0,0],[DRAW,0,.6864655,0,34.87,14.5]):
        f=equilibrium(mat,wrench)
        assert min(f)>0
        assert max(abs(dot(row,f)-t) for row,t in zip(mat,wrench))<1e-10
    show('six-land example minimum/maximum normal, not all-wrench certificate',min(f),max(f))


def tests():
    print('exploratory; mm, N, Nmm. Every geometric tolerance and friction bound below is provisional.')
    # If a solid-radius lip could touch a connector capsule, one adjacent
    # bead would intersect it first. This is a 3D distance inequality.
    minlip=(PITCH**2/4+STEM**2-RMIN**2)/(2*(RMIN-STEM))
    reserve=LIP+RMIN-hypot(LIP+STEM,PITCH/2)
    show('minimum rolling lip radius / chosen / endpoint exclusion reserve',minlip,LIP,reserve)
    assert reserve>.065 and minlip<LIP
    # An unloaded terminal sphere cannot stick on ONE convex rolling
    # lip: its upstream full bead excludes a pulling direction lying in
    # the opposing friction cone. Multiple contacts are different.
    c=PITCH/(2*(LIP+RMIN))
    drive=sqrt(1-c*c)-MU*c
    show('single-lip terminal sliding force fraction lower bound',drive)
    assert c<1/sqrt(1+MU*MU) and drive>.54
    show('sharp-edge counterexample: connector contact / nearest bead distance',STEM,hypot(STEM,PITCH/2))
    assert hypot(STEM,PITCH/2)>RMIN
    gamma=2*asin(PITCH/(2*TURN))
    chord=TURN-sqrt(TURN**2-(PITCH/2)**2)
    show('return length / link turn degrees / chord sag / bore radial room',
         2*LEG+pi*TURN,degrees(gamma),chord,BORE-RMAX)
    assert chord<BORE-RMAX
    # Initial straight-leg fit is a target, not a sourced articulation
    # envelope. It must not be substituted for the bead/rod sweep above.
    show('leg insertion tolerance margin at 3deg/.10',BORE-RMAX-.10-LEG*tan(ERROR))
    assert BORE-RMAX-.10-LEG*tan(ERROR)>0
    diff=leg_lengths(SERVICE)[1]-leg_lengths(SERVICE)[0]
    show('equalizer +/-17deg: differential / one pitch / +20deg stop differential',
         diff,PITCH,leg_lengths(STOP)[1]-leg_lengths(STOP)[0])
    assert diff>PITCH
    mmin=ARM*cos(SERVICE+ERROR)-ECC
    mmax=ARM+ECC
    ratio=mmax/mmin
    total=DRAW/cos(ERROR)
    tmax=(mmax*total+DRAG)/(mmin+mmax)
    tmin=(mmin*DRAW-DRAG)/(mmin+mmax)
    show('arm min / ratio factor / additive tension bound / Tmax / Tmin',mmin,ratio,DRAG/mmin,tmax,tmin)
    assert tmin>0 and tmax<20.45
    beta=atan2(ARM*(1-cos(SERVICE)),DIST-ARM*sin(SERVICE))
    show('nominal direct-leg angle / window sensitivity if extra 3deg+.10',
         degrees(beta),BORE-RMAX-.10-2.5*tan(beta+ERROR))
    assert beta<ERROR
    assert BORE-RMAX-.10-2.5*tan(beta+ERROR)>0
    # For every |theta|<=17, |beta|<=3: h>=a cos20-ecc.
    for i in range(-170,171):
        t=radians(i/10)
        for s in (-1,1):
            e=[-s*ARM*sin(t),s*ARM*cos(t),0]
            v=[DIST-e[0],s*ARM-e[1],0]
            l=hypot(*v);v=[q/l for q in v]
            h=abs(cross(e,v)[2])
            assert h>=mmin
    # Useful load existence, not a transfer of an old reciprocal certificate.
    seats()
    show('stock #3 average tensile / T_max ratio, NOT working factor',25*4.4482216153,25*4.4482216153/tmax)
    show('stock #6 average tensile, NOT working load',45*4.4482216153)
    show('one-sided service draw comparison, owner datum',184.)
    show('smooth-belt pi friction comparison ONLY',exp(MU*pi))
    # Close guide zigzag: compression is supportable only if articulation,
    # compressed pitch, input force and every guide wall are qualified.
    tilt=asin(2*(BORE-RMIN)/PITCH)
    step=(1+MU*tan(tilt))/(1-MU*tan(tilt))
    n=ceil((2*LEG+pi*TURN+2*DIST)/PITCH)
    show('supported zigzag link angle / per-bead factor / bead count / force factor',
         degrees(2*tilt),step,n,step**n)
    assert MU*tan(tilt)<1
    show('R4.2 ball penetration at bore disk / R1.45 fork fits bore',
         4.2-sqrt(4.2**2-BORE**2),BORE-1.45)
    for radius in (6.,8.,10.,12.):
        show('U radius / required link angle degrees',radius,degrees(2*asin(PITCH/(2*radius))))
    # A closed two-lip throat supports the smooth terminal bead itself.
    # Bead centre O, two full lip balls tangent; no material intersections.
    alpha=radians(20); d=RMIN+LIP
    q=[(-d*sin(alpha),s*d*cos(alpha),0) for s in (-1,1)]
    throat=dist(*q)-2*LIP
    assert dist(*q)>2*LIP and 2*STEM<throat<2*RMIN
    for x in q:
        assert abs(hypot(*x)-d)<1e-12
        assert dist(x,(-PITCH,0,0))>RMIN+LIP
        assert abs(x[1])>LIP+STEM
    # Force on bead from each lip is (sin(alpha), +/-cos(alpha),0)*N.
    # Pure -X pull is resisted even at mu=0. No +X pusher promise removes it.
    pull=20.; normal=pull/(2*sin(alpha))
    show('two-body last-bead throat / bead diameter / shaft diameter / N each at pull20',
         throat,2*RMIN,2*STEM,normal)
    # The open starting throat admits the full bead. Independent tail
    # approach closes it continuously without any lip/lip collision.
    start_sep=2*(RMIN+LIP)+.2
    show('open-to-pinched lip-centre approach distance',start_sep-dist(*q))
    show('simply supported latch pin screen at T_max: d1.0 span2 sigma MPa',
         8*tmax*2/pi)
    show('pusher margin example 5N, 70g, mu_table .5, no lace/guide force',
         5-.07*9.80665*1.5)


def geometry():
    # Exact CSG primitives with analytic curves, not a sampled solid shell.
    return {
      'label':'exploratory Take 52 local fixture; not a Kin package',
      'units':'mm N Nmm; head negative X, tail positive X, face x=0',
      'passive_tail':{
        'centreline':[{'segment':[[0,-TURN,0],[LEG,-TURN,0]]},
                      {'arc':{'centre':[LEG,0,0],'radius':TURN,'plane':'XY',
                              'x':'LEG+TURN*sin(t)','y':'TURN*cos(t)','t':[0,pi]}},
                      {'segment':[[LEG,TURN,0],[0,TURN,0]]}],
        'bore_radius':BORE,'outside_radius':BORE+2*LIP,
        'material':'outer swept tube minus bore, ends as specified rounded lip caps',
        'end_caps':[{'torus':{'centre':[LIP,s*TURN,0],'axis':[1,0,0],
                               'major':BORE+LIP,'minor':LIP},
                     'join':'outer/bore straight tube begins x=LIP'} for s in (-1,1)],
        'joining':'No zero-thickness seams; monolithic machined metal or joined halves with continuous internal finish; strength/join unresolved'},
      'head_equalizer':{'pivot':[-DIST,0,0],'axis':[0,0,1],
        'tip_centres':'(-DIST +/- ARM*sin(theta), +/- ARM*cos(theta),0)',
        'halfspan':ARM,'service_degrees':[-17,17],'unloaded_stops_degrees':[-20,20],
        'bar_local_box':[[-.8,.8],[-6.4,6.4],[-.8,.8]],
        'line_support':'direct legs, no separate fixed loaded fairlead; support/feed tracks must withdraw or ride on arms',
        'endpoints':'permanent anchor and reversible tip pocket/latch on opposite arms',
        'draw_slide':'translating, stroke and physical preload limiter unresolved',
        'bearing':'bilaterally supported Z trunnion, drag bound .50 target not source-rated',
        'force_line_eccentricity_max':ECC},
      'six_land_face':{'radius':13,'sites_deg':[0,120,240],
        'normal_x':.5,'normal_tangential':'+/-sqrt(3)/2','offset_y_target':.5},
      'lace_gauge_targets':{'bead_r_min':RMIN,'bead_r_max':RMAX,'pitch_max':PITCH,
        'external_connector_capsule_radius_max':STEM,'smooth_end':'last bead only; NO dumbbell stub beyond it',
        'chain':'hypothetical gauged #3 stainless; source averages are not tolerances'},
      'pinch_witness':{'bead_centre':[0,0,0],'bead_radius':RMIN,
        'lip_ball_radius':LIP,
        'lip_centres':[[-(RMIN+LIP)*sin(radians(20)),s*(RMIN+LIP)*cos(radians(20)),0] for s in (-1,1)],
        'finite_lip_capsules':[
          {'centreline':[[-(RMIN+LIP)*sin(radians(20)),s*(RMIN+LIP)*cos(radians(20)),z] for z in (-5,5)],
           'radius':LIP} for s in (-1,1)],
        'pull_direction':[-1,0,0],
        'scope':'two disjoint finite rounded mouth edges; no claimed collision-checked full-head/tail path'},
      'excluded':['drive motor','reel','positive latch cam','tip receiver drive','all bearings',
        'loaded feed guide','pusher','frame','physical validation','full stow and arbitrary-attitude release'] }


if __name__=='__main__':
    if '--json' in sys.argv:
        dump(geometry(),sys.stdout,sort_keys=True,indent=2);print()
    else:tests()
