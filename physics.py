from math import *

import numpy as np
import scipy as sp

from scipy import integrate
from numpy.linalg import norm

mu_0 = 4*pi*10**-7

class Inducer:
    """
    The abstract base class for all field inducers.

    This class is just the placeholder for the root of the inducer tree; it is
    used by Field to do some preliminary argument checking. It defines no
    methods on its own.
    """
    pass


class BInducer:
    """
    A magnetic (B) field inducer.

    Like inducer, this class is more or less a placeholder. It does define the
    method bfield_strength which must be implemented by all subclasses.
    """

    def bfield_at(self, P):
        """Calculate the magnetic field vector at a point."""
        raise NotImplementedError


class Wire(BInducer):
    """
    A straight wire.

    Wires connect two points A and B in three-dimensional space. In addition,
    wires have scalar current I; the current flows from A to B if it is
    positive, and from B to A if it is negative.
    """

    def __init__(self, A, B, I):
        self.A = A
        self.B = B
        self.I = I

    def bfield_at(self, P):
        t = dot(self.A - P, self.B - self.A) / norm(self.B - self.A)**2
        d = np.array(
                (self.A[0] - P[0]) - (self.B[0] - P[0]),
                (self.A[1] - P[1]) - (self.B[1] - P[1]),
                (self.A[2] - P[2]) - (self.B[2] - P[2])
                )

        direction = normalize(((self.B-self.A) * I).cross(d))
        magnitude = mu_0*self.I / (2*math.pi*abs(d))
        return vec3d(direction.x*magnitude, direction.y*magnitude, direction.z*magnitude)


class Coil(BInducer):
    """
    A coil of wire.
    """

    def __init__(self, center, radius, norm, I):
        self.center = center
        self.radius = radius
        self.norm = norm
        self.I = I

    # rotation matrices for this coil, rotating so norm becomes z axis
    rotate = find_rotmatrix(norm, vec3d(0, 0, 1))
    antiRotate = find_rotmatrix(vec3d(0, 0, 1), norm)

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


class Field:
    """
    The abstract base class for all fields.

    All fields are callable objects; the return value is a vector denoting the
    field strength and direction at a point. Calculation of this vector must be
    implemented in every concrete subclass. It is typically the superposition
    of fields for every inducer in the field.

    Fields maintain a list of inducers called ducs.
    """

    def __init__(self):
        self.ducs = []

    def add_inducer(self, duc):
        """Add an inducer to this field."""
        self.ducs += [duc]

    def draw(self, x, y, z):
        """Draw the field vector at the given point."""
        v = self(x, y, z)

    def __call__(self, x, y, z): raise NotImplementedError

class BField(Field):
    """
    A magnetic (B) field.
    """

    def __call__(self, x, y, z):
        return sum(duc.bfield_at(x, y, z) for duc in self.ducs)
