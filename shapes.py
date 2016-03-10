from __future__ import division, print_function

from visual import *

from math import *

import numpy as np
import scipy as sp
import numpy.linalg as la

from scipy import integrate

from physics import *
from constants import mu_0

class Wire(BInducer):
    """
    A straight wire.

    Wires connect two points A and B in three-dimensional space. In addition,
    wires have scalar current I; the current flows from A to B if it is
    positive, and from B to A if it is negative.
    """

    def __init__(self, A, B, I, radius=0.1):
        # coordinates
        self.A = A
        self.B = B

        # length
        self.BA = self.B - self.A
        self.l = self.BA.mag
        self.l2 = self.BA.mag2

        # current
        self.I = norm(self.BA) * I

        # the rod
        self.rod = cylinder(pos = self.A, axis = self.BA, radius=radius)


    def bfield_at(self, P):
        # compute the shortest distance d from the wire to point P
        # V is the closest point on the wire to point P (needed to calculate
        # the direction of the field, see below)
        #
        # adapted from
        # http://mathworld.wolfram.com/Point-LineDistance3-Dimensional.html


##        t = -dot(self.A - P, self.BA) / self.l2
##        V = self.A + t*self.BA
##        r = P - V
##        d = mag(r)
##
##        # the magnitude of the field
##        Bmag = mu_0 * self.I / (2*pi*d)
##
##        # normalized (unit) vector in the direction of the field
##        Bhat = norm(cross(r, V))
##
##        # return field vector
##        return Bmag*Bhat

        t = dot(self.A - P, self.B - self.A) / mag(self.B - self.A)**2
        d = vector(
                (self.A[0] - P[0]) - (self.B[0] - P[0]),
                (self.A[1] - P[1]) - (self.B[1] - P[1]),
                (self.A[2] - P[2]) - (self.B[2] - P[2])
                )

        direction = norm(self.I.cross(d))
        magnitude = 1
        #mu_0*mag(self.I) / (2*math.pi*abs(d))
        print(magnitude)
        return direction*magnitude


class Coil(BInducer):
    """
    A coil of wire.
    """

    def __init__(self, center, radius, normal, I):
        self.center = center
        self.radius = radius
        self.normal = normal
        self.I = I
        # rotation matrices for this coil, rotating so norm becomes z axis
        rotate = find_rotmatrix(normal, vec3d(0, 0, 1))
        antiRotate = inv(rotate)


    # 1st and 2nd kind of elliptic integrals, K(k) and E(k) respectively
    # http://www.mhtlab.uwaterloo.ca/courses/me755/web_chap3.pdf
    def K(k):
        return integrate.quad(lambda t: ((1-t**2)*(1-k**2*t**2))**-0.5, 0, 1)[0]

    def E(k):
        return integrate.quad(lambda t: ((1-k**2*t**2)/(1-t**2))**0.5, 0, 1)[0]

    def find_rotmatrix(a, b):
        # http://math.stackexchange.com/questions/180418/calculate-rotation-matrix-to-align-vector-a-to-vector-b-in-3d
        a, b = normalize(a), normalize(b)
        v = cross(a, b)
        s = abs(v) #sin of angle
        c = a*b #cos of angle

        #creating [v]x, skew symmetric matrix
        #https://en.wikipedia.org/wiki/Skew-symmetric_matrix
        vx = np.matrix([[0,    -v.z, v.y],
                        [v.z,  0,    -v.x],
                        [-v.y, v.x,  0]])
        I = np.matrix([[1,0,0],
                       [0,1,0],
                       [0,0,1]])
        return I + vx + (vx*vx) * (1-c)/(s**2)


    def bfield_at(self, x, y, z):
        #translating center to origin and all associated points
        newX, newY, newZ = x-self.center.x, y-self.center.y, z-self.center.z

        #rotating coil so normal vector is on z axis
        newCoordinates = np.dot(rotate, np.matrix([[newX],[newY],[newZ]]))
        newX, newY, newZ = newCoordinates[0], newCoordinates[1], newCoordinates[2]

        #defining variables for equation
        #http://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20010038494.pdf
        r = abs(vec3d(newX, newY, newZ)) #spherical coordinate equivalent of magnitude

        rhoSq = newX**2 + newY**2
        rSq = newX**2 + newY**2 + newZ**2
        alphaSq = radius**2 + r**2 - 2*radius*(rhoSq**0.5)
        betaSq = radius**2 + r**2 + 2*radius*(rhoSq**0.5)
        kSq = 1 - (alphaSq/betaSq)
        gamma = newX**2 - newY**2
        C = mu_0*I/math.pi

        #component calculations
        Bx = (C*newX*newZ / (2*alphaSq*(betaSq**0.5)*rhoSq)) * \
             ((radius**2 + r**2) * E(kSq) - alphaSq * K(kSq))
        By = Bx * (newY/newX)
        Bz = (C/(2*alphaSq*(betaSq**0.5))) * \
             ((radius**2 + r**2) * E(kSq) - alphaSq * K(kSq))

        #rotating field components to original rotate state
        finalB = np.dot(antiRotate, np.matrix([[Bx], [By], [Bz]]))
        return vec3d(finalB[0], finalB[1], finalB[2])


#class Solenoid: rectangular prism of coils
 
