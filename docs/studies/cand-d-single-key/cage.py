"""Take 77 — connected-component bound for seven finite unilateral flats (mm)."""
from math import asin, cos, degrees, hypot, radians, sin, tan

import numpy as np

from compare import BR, R, tilted


def lands():
    v = radians(65)
    k, s = tan(v), sin(v)
    t, h = R * s, 2.68 - R * cos(v)
    seat = min(
        (2.12 - h) / s,
        h / s,
        ((3.81 - t) * k - h) / (2 * s),
        (1.35 * k - h) / hypot(k, s),
        ((12.20 - hypot(BR, t)) * tan(radians(64)) - h) * cos(radians(64)),
    )
    p = tilted()[0][0]
    a, fil = radians(18), .35
    x0, x1 = -3.3821130325903073, -.7021130325903071
    y0, y1 = -.8954915028125263, 13.35
    xc, yc = p[:2] + fil * np.array([cos(a), sin(a)])
    key = min(
        (xc - x0 - fil) / sin(a),
        (x1 - fil - xc) / sin(a),
        (yc - y0 - fil) / cos(a),
        (y1 - fil - yc) / cos(a),
        1.65 - fil,
    )
    return np.r_[key, np.full(6, seat)]


def cage():
    _, n, c = tilted()
    c -= [-3.20, 0, 0]
    radius = np.linalg.norm(c, axis=1)
    A = np.column_stack((n, np.cross(c, n) / BR))
    weights = np.r_[1., np.full(6, 1 / (6 * cos(radians(65))))]
    assert np.linalg.norm(weights @ A) < 1.e-12 and np.linalg.matrix_rank(A) == 6

    beta = radians(1.95)
    H = np.r_[.190, np.full(6, .460)]
    delta = np.radians([2.0] + [.60] * 6)
    E = np.r_[.065, np.full(6, .025)]
    curve = (1 - cos(beta)) * radius
    cost = H + R * np.tan(delta) + .040
    margin = lands() - cost
    assert np.min(margin) > .02

    e = E + 2 * np.sin(delta / 2) * H + curve
    vs = np.array([
        np.linalg.solve(np.delete(A, j, 0), -np.delete(e, j))
        for j in range(7)
    ])
    assert (vs @ A.T + e).min() > -1.e-11
    m = np.max([
        np.linalg.norm(v[:3] + np.cross(v[3:], c) / BR, axis=1)
        for v in vs
    ], axis=0)
    theta = asin(max(np.linalg.norm(v[3:]) / BR for v in vs))
    disp = m + (1 - cos(theta)) * radius
    assert np.min(H - disp) > .008 and beta - theta > radians(.15)
    t = max(np.linalg.norm(v[:3]) for v in vs)
    print('land radii key/seat, reserve:', lands()[[0, 1]], margin[[0, 1]])
    print('translation mm / rotation deg:', t, degrees(theta))
    print('finite center displacements lug and registry:', disp[[0, 1]])
    assert t < .17 and degrees(theta) < 1.80


def guides():
    p = tilted()[0][0, :2]
    xc, yc = (-3.3821130325903073 - .7021130325903071) / 2, (8.60 + 12.70) / 2
    a, rot = radians(18), radians(.50)
    tilt_x = (12.70 - yc) * tan(rot) + 1.34 * (1 / cos(rot) - 1)
    assert tilt_x < .04
    Q = np.array([[cos(rot), -sin(rot)], [sin(rot), cos(rot)]])
    disp = (Q - np.eye(2)) @ (p - np.array([xc, yc]))
    actual_n = Q @ np.array([-cos(a), -sin(a)])
    recess = -actual_n @ disp
    print('original guide X used, normal plane recession:', tilt_x, recess)
    assert recess > .085

    trial = .020 * (1 + 2 * (4.50 - p[1]) / (12.70 - 4.50))
    print('trial two-row X offset at key pole in XY only:', trial)
    full = p[1] + (p[0] + 3.3821130325903073) / tan(a)
    print('rear full shank starts at lock / park (before rounding):',
          full, full + 4.85)
    assert full < 4.5 < 5.35 < full + 4.85


if __name__ == '__main__':
    cage()
    guides()
