from __future__ import division, print_function

from visual_common.primitives import cylinder, ring, helix
from visual_common.cvisual import vector
from numpy import matrix
from numpy.linalg import inv
from math import pi, sin, cos

from physics import *
from constants import mu_0, eps_0
from util import K, E

class Wire(BInducer, EInducer):
    """
    A straight wire.
    """

    def __init__(self, A, B, I):
        # coordinates
        self.A = A
        self.B = B

        # length
        self.BA = self.B - self.A
        self.l = self.BA.mag
        self.l2 = self.BA.mag2

        # current
        self.I = self.BA.norm() * I

        # the rod
        self.rod = cylinder(pos = self.A, axis = self.BA, radius = 0.1)

    def ray_to(self, P):
        """
        Calculate the shortest vector from the wire to a point P.

        Adapted from:
        http://mathworld.wolfram.com/Point-LineDistance3-Dimensional.html
        """

        t = -self.BA.dot(self.A - P) / self.l2
        return P - (self.A + t*self.BA)


    def bfield_at(self, P):
        r = self.ray_to(P)

        # special case to avoid division by 0
        if r.mag == 0: return vector(0, 0, 0)

        return (mu_0 * self.I.mag / (2*pi*r.mag)) * r.cross(self.I).norm()


    def efield_at(self, P):
        r = self.ray_to(P)

        # special case to avoid division by 0
        if r.mag == 0: return vector(0, 0, 0)

        return (self.I / (2*pi*eps_0*self.l*r)) * r.norm()


class Coil(BInducer):
    """
    A coil of wire.
    """

    def __init__(self, center, radius, normal, I, loops = 1, pitch = 1):
        self.center = center
        self.radius = radius
        self.normal = normal

        self.loops = loops
        self.pitch = pitch
        self.length = loops*pitch

        self.I = I

        # some consonants
        self.C = mu_0*I/pi
        self.oner = matrix([[1,0,0], [0,1,0], [0,0,1]])

        # rotation matrices for this coil, rotating so norm becomes z axis
        self.rotate = matrix([[1,0,0],[0,1,0],[0,0,1]])
        self.rotate = self.find_rotmatrix(normal.norm(), vector(0, 0, 1))    #TESTING
        self.antiRotate = matrix([[1,0,0],[0,1,0],[0,0,1]])
        self.antiRotate = inv(self.rotate)     #TESTING

        # the helix
        if loops == 1:
            self.helix = ring(pos = center, axis = normal*self.length,
                    radius = radius, thickness = 0.1)
        else:
            self.helix = helix(pos = center, axis = normal*self.length,
                    radius = radius, coils = loops, thickness = 0.1)

    def find_rotmatrix(self, a, b):
        # http://math.stackexchange.com/questions/180418/calculate-rotation-matrix-to-align-vector-a-to-vector-b-in-3d
        v = a.cross(b)

        # creating [v]x, skew symmetric matrix
        # https://en.wikipedia.org/wiki/Skew-symmetric_matrix
        vx = matrix([[ 0,  -v.z, v.y],
                     [ v.z, 0,  -v.x],
                     [-v.y, v.x, 0  ]])

        return self.oner + vx + vx**2 * (1 - a.dot(b)) / v.mag2


    def bfield_at(self, P):
        # translate center to origin and align normal to z axis
        Pr = vector(self.rotate.dot(matrix(P - self.center).transpose()))
        rx, ry, rz = Pr

        # defining variables for equation
        # http://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20010038494.pdf
        r = Pr.mag

        rho = (rx**2 + ry**2)**0.5
        alpha = (self.radius**2 + r**2 - 2*self.radius*(rho))**0.5
        beta = (self.radius**2 + r**2 + 2*self.radius*(rho))**0.5
        gamma = rx**2 - ry**2
        k = (1 - (alpha**2/beta**2))**0.5

        if alpha == 0 or beta == 0 or rho == 0 or rx == 0: return vector(0, 0, 0)

        # components
        Bx = (self.C*rx*rz / (2*alpha**2*beta*rho**2)) * \
             ((self.radius**2 + r**2) * E(k**2) - alpha**2 * K(k**2))
        By = Bx * (ry/rx)
        Bz = (self.C/(2*alpha**2*(beta))) * \
             ((self.radius**2 + r**2) * E(k**2) - alpha**2 * K(k**2))

        # untranslate points and re-align to actual normal

        #conflict
        #B = norm(vector(Bx, By, Bz))
        B = vector(Bx, By, Bz)
        return vector(dot(self.antiRotate, matrix(B).transpose()))
        B = vector(Bx, By, Bz).norm()
        #B = vector(Bx, By, Bz)
        return vector(self.antiRotate.dot(matrix(B).transpose()))
