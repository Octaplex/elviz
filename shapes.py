from __future__ import division, print_function

from visual import *
from math import pi, sin, cos
from physics import *
from constants import mu_0
from util import K, E

class Wire(BInducer):
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


    def bfield_at(self, P):
        # compute the shortest distance d from the wire to point P
        # V is the closest point on the wire to point P (needed to calculate
        # the direction of the field, see below)
        #
        # adapted from
        # http://mathworld.wolfram.com/Point-LineDistance3-Dimensional.html

        # get nearest point to wire
        t = -self.BA.dot(self.A - P) / self.l2
        r = P - (self.A + t*self.BA)

        # special case to avoid division by 0
        if r.mag == 0: return vector(0, 0, 0)

        return (mu_0 * self.I.mag / (2*pi*r.mag)) * r.cross(self.I).norm()


class Coil(BInducer):
    """
    A coil of wire.
    """

    def __init__(self, center, radius, normal, I, loops = 1, pitch = 1):
        self.center = center
        self.radius = radius
        self.normal = normal
<<<<<<< HEAD
        self.I = I
        # rotation matrices for this coil, rotating so norm becomes z axis
        self.rotate = self.find_rotmatrix(normal, vector(0, 0, 1))
        self.antiRotate = la.inv(self.rotate)
=======
>>>>>>> origin/master

        self.loops = loops
        self.pitch = pitch
        self.length = loops*pitch

        self.I = I

        # some consonants
        self.C = mu_0*I/math.pi
        self.oner = matrix([[1,0,0], [0,1,0], [0,0,1]])

<<<<<<< HEAD
    # 1st and 2nd kind of elliptic integrals, K(k) and E(k) respectively
    # http://www.mhtlab.uwaterloo.ca/courses/me755/web_chap3.pdf
    def K(self, k):
        return integrate.quad(lambda t: ((1-t**2)*(1-k**2*t**2))**-0.5, 0, 1)[0]

    def E(self, k):
        return integrate.quad(lambda t: ((1-k**2*t**2)/(1-t**2))**0.5, 0, 1)[0]
=======
        # rotation matrices for this coil, rotating so norm becomes z axis
        self.rotate = self.find_rotmatrix(normal.norm(), vector(0, 0, 1))
        self.antiRotate = linalg.inv(self.rotate)

        # the helix
        if loops == 1:
            self.helix = ring(pos = center, axis = normal*self.length,
                    radius = radius, thickness = 0.1)
        else:
            self.helix = helix(pos = center, axis = normal*self.length,
                    radius = radius, coils = loops, thickness = 0.1)
>>>>>>> origin/master

    def find_rotmatrix(self, a, b):
        if a.x==0 and a.y==0: #if no rotation needed
            return np.matrix([[1,0,0],
                              [0,1,0],
                              [0,0,1]])
        # http://math.stackexchange.com/questions/180418/calculate-rotation-matrix-to-align-vector-a-to-vector-b-in-3d
        v = cross(a, b)
<<<<<<< HEAD
        s = v.mag #sin of angle
        c = dot(a, b) #cos of angle

        #creating [v]x, skew symmetric matrix
        #https://en.wikipedia.org/wiki/Skew-symmetric_matrix
        vx = np.matrix([[0,    -v.z, v.y],
                        [v.z,  0,    -v.x],
                        [-v.y, v.x,  0]])
        I = np.matrix([[1,0,0],
                       [0,1,0],
                       [0,0,1]])
        return I + vx + (vx*vx) * (1-c)/(s**2)


    def bfield_at(self, P):
        #translating center to origin and all associated points
        newX, newY, newZ = P.x-self.center.x, \
                           P.y-self.center.y, \
                           P.z-self.center.z

        #rotating coil so normal vector is on z axis
        transCoords = np.matrix([[newX],[newY],[newZ]])
        newCoordinates = np.dot(self.rotate, transCoords)
        newX, newY, newZ = newCoordinates[0], newCoordinates[1], newCoordinates[2]

        #defining variables for equation
        #http://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20010038494.pdf
        r = mag(vector(newX, newY, newZ)) #spherical coordinate equivalent of magnitude
        rhoSq = newX**2 + newY**2
        rSq = newX**2 + newY**2 + newZ**2
        alphaSq = self.radius**2 + r**2 - 2*self.radius*(math.sqrt(rhoSq))
        betaSq = self.radius**2 + r**2 + 2*self.radius*(math.sqrt(rhoSq))
        kSq = 1 - (alphaSq/betaSq)
        gamma = newX**2 - newY**2
        C = mu_0*self.I/math.pi

        #component calculations
        Bx = (C*newX*newZ / (2*alphaSq*(math.sqrt(betaSq))*rhoSq)) * \
             ((self.radius**2 + r**2) * self.E(kSq) - alphaSq * self.K(kSq))
        By = Bx * (newY/newX)
        Bz = (C/(2*alphaSq*(math.sqrt(betaSq)))) * \
             ((self.radius**2 + r**2) * self.E(kSq) - alphaSq * self.K(kSq))

        #rotating field components to original rotate state
        finalB = np.dot(self.antiRotate, np.matrix([[Bx], [By], [Bz]]))
        return vector(finalB[0], finalB[1], finalB[2])


 
=======

        # creating [v]x, skew symmetric matrix
        # https://en.wikipedia.org/wiki/Skew-symmetric_matrix
        vx = matrix([[ 0,  -v.z, v.y],
                     [ v.z, 0,  -v.x],
                     [-v.y, v.x, 0  ]])

        return self.oner + vx + vx**2 * (1 - dot(a, b)) / v.mag2


    def bfield_at(self, P):
        # translate center to origin and align normal to z axis
        Pr = vector(dot(self.rotate, matrix(P - self.center).transpose()))
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
        B = vector(Bx, By, Bz)
        return vector(dot(self.antiRotate, matrix(B).transpose()))
>>>>>>> origin/master
