import math
import numpy as np
import scipy as sp
import scipy.integrate as integrate

#constants
muNot = 4*math.pi*10**-7

class Inducer: pass

class BInducer:
    def bfield_strength(self, x, y, z): raise NotImplementedError

class Wire(BInducer):

    def __init__(self, A, B, I):
        self.A = A
        self.B = B
        self.I = I

    def bfield_strength(self, x, y, z):
        C = vec3d(x, y, z)

        t = (self.A - self.C)*(self.B - self.A) / abs(self.B - self.A)**2
        d = vec3d((self.A.x-C.x) - (self.B.x-C.x),
                  (self.A.y-C.y) - (self.B.y-C.y),
                  (self.A.z-C.z) - (self.B.z-C.z))
        direction = normalize(((self.B-self.A) * I).cross(d))
        magnitude = muNot*self.I / (2*math.pi*abs(d))
        return vec3d(direction.x*magnitude, direction.y*magnitude, direction.z*magnitude)

    def bfield_draw(self, x, y, z):
        B = self.bfield_strength(x, y, z)
        arrow(pos=(x,y,z), axis=tuple(B))

class Coil(BInducer):

    def __init__(self, center, radius, norm, I):
        self.center = center
        self.radius = radius
        self.norm = norm
        self.I = I

    #rotation matrices for this coil, rotating so norm becomes z axis
    rotate = findRotateMatrix(norm, vec3d(0, 0, 1))
    antiRotate = findRotateMatrix(vec3d(0, 0, 1), norm)

    #1st and 2nd kind of elliptic integrals, K(k) and E(k) respectively
    #http://www.mhtlab.uwaterloo.ca/courses/me755/web_chap3.pdf
    def K(k):
        return integrate.quad(lambda t: ((1-t**2)*(1-k**2*t**2))**-0.5, 0, 1)[0]

    def E(k):
        return integrate.quad(lambda t: ((1-k**2*t**2)/(1-t**2))**0.5, 0, 1)[0]

    def findRotateMatrix(a, b):
        #http://math.stackexchange.com/questions/180418/calculate-rotation-matrix-to-align-vector-a-to-vector-b-in-3d
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
        
        
    
    def bfield_strength(self, x, y, z):
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
        C = muNot*I/math.pi

        #component calculations
        Bx = (C*newX*newZ / (2*alphaSq*(betaSq**0.5)*rhoSq)) * \
             ((radius**2 + r**2) * E(kSq) - alphaSq * K(kSq))
        By = Bx * (newY/newX)
        Bz = (C/(2*alphaSq*(betaSq**0.5))) * \
             ((radius**2 + r**2) * E(kSq) - alphaSq * K(kSq))

        #rotating field components to original rotate state
        finalB = np.dot(antiRotate, np.matrix([[Bx], [By], [Bz]]))
        return vec3d(finalB[0], finalB[1], finalB[2])


    def bfield_draw(self, x, y, z):
        B = self.bfield_strength(x, y, z)
        arrow(pos=(x,y,z), axis=tuple(B))
        
        

class Field:
    def __call__(self, x, y, z): raise NotImplementedError
    strength = __call__

class BField(Field):

    def __init__(self, ducs):
        self.ducs = ducs

    def __call__(self, x, y, z):
        return sum(duc.bfield_strength(x, y, z) for duc in self.ducs)
