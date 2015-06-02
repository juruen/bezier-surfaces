#!/usr/bin/env python

# Copyright (c) 2015 Javier Uruen Val (javi.uruen@gmail.com)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import itertools

def casteljau_curve(points, t):
    """Use casteljau to compute a point of a Bezier curve given the control
       points and a fixed parametized t"""
    p, n = points, len(points)
    for r in range(1,n):
        for i in range(n - r):
            p[i] = (1 - t) * p[i] + t * p[i + 1]

    return p[0]

def casteljau_surface(points, u, v):
    """Given control points of a surface and fixing u and v, compute an
       interpolated 3d point of the surface"""
    xis = list()
    yis = list()
    zis = list()

    for ps in points:
        xis.append(casteljau_curve([j[0] for j in ps], u))
        yis.append(casteljau_curve([j[1] for j in ps], u))
        zis.append(casteljau_curve([j[2] for j in ps], u))

    return (casteljau_curve(xis, v), casteljau_curve(yis, v),
            casteljau_curve(zis, v))


def control_points(sections=8, radio=1, points_section=8, reflection=1):
    """Generate control points for a spehere. Note that we use a naive
       algorithm for clarity"""
    points = list()

    for x in np.linspace(-radio, radio, sections):
        radio_section = np.sqrt(radio**2 - x**2)
        row = list()
        for y in np.linspace(-radio_section, radio_section, points_section):
            z = np.sqrt(radio_section**2 - y**2)
            row.append((x, y, z * reflection))
        points.append(row)

    return points


if __name__ == "__main__":

    # Fetch control points for the two semi-speheres
    cp_up = control_points()
    cp_down = control_points(reflection=-1)

    xas = list()
    yas = list()
    zas = list()

    xbs = list()
    ybs = list()
    zbs = list()

    intervals_u_v = 40
    for u in np.linspace(0.0, 1.0, intervals_u_v):
        for v in np.linspace(0.0, 1.0, intervals_u_v):
            p = casteljau_surface(cp_up, u, v)
            xas.append(p[0])
            yas.append(p[1])
            zas.append(p[2])

            p = casteljau_surface(cp_down, u, v)
            xbs.append(p[0])
            ybs.append(p[1])
            zbs.append(p[2])



    # Draw the two aproximated surfaces
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(xas, yas, zas)
    ax.scatter(xbs, ybs, zbs)

    # Draw control points
    cxs = list()
    cys = list()
    czs = list()

    for fila in itertools.chain(cp_up, cp_down):
        for p in fila:
            cxs.append(p[0])
            cys.append(p[1])
            czs.append(p[2])

    ax.scatter(cxs, cys, czs, c='red')

    plt.show()
