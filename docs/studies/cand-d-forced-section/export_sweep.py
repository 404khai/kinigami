"""Export exact piecewise-linear compact separator sweep in mated coordinates."""
from itertools import product
from json import dump
from sys import stdout

from separator import NOSE, P0, guides, parts


def solids(p, shut, carry):
    stock=parts(p,shut,carry)+guides(p,shut,carry)
    return [[f'{i:02d}/{name}',list(product(*bounds)),0,None]
            for i,(name,bounds) in enumerate(stock)]


def main():
    states=[
        ('home',P0,0.,0.),('relieved',P0-1.5,0.,0.),
        ('at_nose',NOSE,0.,0.),('nose_closed',NOSE,1.,0.),
        ('terminal',NOSE,1.,1.50),('optional_end',NOSE,1.,2.65)]
    phases=[('X relief','home','relieved'),('horn park dwell','relieved','relieved'),
            ('contour tracking','relieved','at_nose'),('lateral closure X dwell','at_nose','nose_closed'),
            ('closed co-travel','nose_closed','terminal'),('optional full X-stage travel','terminal','optional_end')]
    dump({'units':'mm','frame':'mated head, unshifted local Z, +X out; no yaw applied',
          'model':'Take49 compact. moving separator only, not rotor or fixed garage. Use actual horn and independently checked Take51 skins; aft blank is not stock.',
          'geometry':'[id, eight true box corners, radius=0, axis=null]; union per rigid group. Same vertex order in all states.',
          'sweep':'Linear interpolation of corresponding vertices is exact per phase; each individual solid sweeps its endpoint convex hull. For collisions at equal time interpolate both parts, not independent hull intersections.',
          'groups':'00/01 upper and lower have independent Z motions; 02/04 side plates carry bearing blocks. 03/05 blades carry respective root/rail. 06 apron follows X only. Root/rail/blade and each bearing/backweb/side overlap at joints by design.',
          'phase_endpoints':phases,
          'states':{key:{'p':p,'shut':s,'carry':c,'face_X':p+c-P0,'solids':solids(p,s,c)}
                    for key,p,s,c in states}},stdout,separators=(',',':'))
    stdout.write('\n')


if __name__=='__main__':
    main()
