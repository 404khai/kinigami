"""Take 76: two compatible local seat states at the same force and stroke. N, mm."""
from math import cos, hypot, pi, sin

import numpy as np
from scipy.optimize import linprog

from fixed_face import RAD, X
from slide_support import contacts


def witness(recess, draw=100., stiffness=5000.):
    # Clock the complete Take 71 triplet -60 degrees to the Take 73 plugs.
    a = -pi / 3
    rotation = np.array([[1, 0, 0], [0, cos(a), -sin(a)], [0, sin(a), cos(a)]])
    poles, normals = [np.array(v) @ rotation.T for v in contacts()]
    normals[6:] *= -1

    # Prescribe finite axial motions, not nine independent contact forces.
    depth_s, depth_j = np.array([31., 55.]) * (draw / 100) / stiffness
    u = depth_j / -normals[6, 0]
    stroke = u + depth_s / normals[0, 0]
    closure = -u * normals[:, 0]
    closure[:6] += stroke * normals[:6, 0]
    closure[0] -= recess
    depth, gap = np.maximum(closure, 0), np.maximum(-closure, 0)
    assert max(depth) < .020 and stroke < .050 and np.all(depth * gap == 0)
    normal = stiffness * depth

    # In a pure translation every actual tail pole moves by u*X. The
    # wrench origin moves with the tail; this does not change zero wrench.
    # Only tangential forces are free; normals come from unilateral springs.
    frame = []
    for n in normals:
        t = np.cross(n, X)
        t /= np.linalg.norm(t)
        frame.append([t, np.cross(n, t)])
    frame = np.array(frame)
    normal_f = normal[:, None] * normals
    rows = np.vstack((frame.reshape(-1, 3).T,
                      np.cross(poles[:, None, :], frame).reshape(-1, 3).T / RAD,
                      np.r_[frame[:6, :, 0].ravel(), np.zeros(6)]))
    rhs = np.r_[-normal_f.sum(axis=0), -np.cross(poles, normal_f).sum(axis=0) / RAD,
                draw - normal_f[:6, 0].sum()]
    m = 32
    th = 2 * pi * np.arange(m) / m
    A = np.kron(np.eye(9), np.column_stack((np.cos(th), np.sin(th))))
    # Inscribed polygon: a feasible vector lies inside true Coulomb friction.
    r = linprog(np.zeros(18), A_ub=A, b_ub=np.repeat(.19 * cos(pi/m) * normal, m),
                A_eq=rows, b_eq=rhs, bounds=(None, None), method='highs')
    assert r.success, r.message
    tangent_f = np.einsum('ijk,ij->ik', frame, r.x.reshape(9, 2))
    f = normal_f + tangent_f
    moment = np.cross(poles, f).sum(axis=0)
    assert np.max(abs(moment)) < 1.e-8 and np.max(abs(f.sum(axis=0))) < 1.e-10
    assert abs(f[:6, 0].sum() - draw) < 1.e-10
    assert np.max(np.linalg.norm(tangent_f, axis=1) - .19 * normal) < 1.e-10
    if recess:
        assert gap[0] > 0 and normal[0] == 0 and min(normal[1:]) > 0
    else:
        assert np.all(normal > 0)
    # Tangent shift relative to each face, including its normal compression.
    rel = np.ones(9) * u
    rel[:6] -= stroke
    shift = abs(rel) * np.sqrt(1 - normals[:, 0] ** 2)
    print('recess / draw / tail X / disk X / first gap / max pole shift:',
          np.round([recess, draw, u, stroke, gap[0], max(shift)], 6))
    print('normal forces:', np.round(normal, 5))
    return stroke


def spring_pocket():
    axes = hypot(10.30 - 8.58, 2.07)
    overlap = 1.70 + 1.10 - axes
    print('pocket/post axis distance, radial interference:', round(axes, 6), round(overlap, 6))
    assert overlap > .108


if __name__ == '__main__':
    for draw in (96., 100., 112.):
        assert abs(witness(.020, draw) - witness(0., draw)) < 1.e-12
    spring_pocket()
