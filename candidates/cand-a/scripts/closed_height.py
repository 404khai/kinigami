"""Spread of the output-pin height (body z) at the closed and open crank stops over the tolerance corners,
and per-factor sensitivity at the closed stop. Uses fourbar.py."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fourbar import *

if __name__ == '__main__':
    for k, t in CASES.items():
        zc = [solve(p, p['th_closed'], 1, 1)[1][1] for p in corners(t)]
        zo = [solve(p, p['th_open'], 1, 1)[1][1] for p in corners(t)]
        print(k, 'closed z %.3f..%.3f (spread %.3f)' % (min(zc), max(zc), max(zc) - min(zc)),
              'open z %.3f..%.3f' % (min(zo), max(zo)))
    t = CASES['class_f_size']
    base = dict(NOM, th_open=18.86, th_closed=221.39)
    z0 = solve(base, 221.39, 1, 1)[1][1]
    for k in ['Cx', 'Cz', 'Px', 'Pz', 'r', 'b', 'a', 'L', 'delta']:
        d = []
        for s in (-1, 1):
            p = dict(base); p[k] += s * t[k]
            d.append(solve(p, 221.39, 1, 1)[1][1] - z0)
        print('closed-z sensitivity', k, ['%+.3f' % x for x in d])
