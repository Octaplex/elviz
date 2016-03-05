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
        direction = ((self.B-self.A) * I).cross(d) / abs(((self.B-self.A) * I).cross(d))
        magnitude = muNot*self.I / (2*math.pi*abs(d))
        return magnitude*direction

    def bfield_draw(self, x, y, z):
        B = self.bfield_strength(x, y, z)
        arrow(pos=(x,y,z), axis=tuple(B))

class Coil(BInducer):

    def __init__(self, center, radius, norm, I):
        self.center = center
        self.radius = radius
        self.norm = norm
        self.I = I

    #1st and 2nd kind of elliptic integrals, K(k) and E(k) respectively
    #http://www.mhtlab.uwaterloo.ca/courses/me755/web_chap3.pdf
    def K(k):
        return integrate.quad(lambda t: ((1-t**2)*(1-k**2*t**2))**-0.5, 0, 1)[0]

    def E(k):
        return integrate.quad(lambda t: ((1-k**2*t**2)/(1-t**2))**0.5, 0, 1)[0]
    
    def bfield_strength(self, x, y, z):
        return None #WIP

class Field:
    def __call__(self, x, y, z): raise NotImplementedError
    strength = __call__

class BField(Field):

    def __init__(self, ducs):
        self.ducs = ducs

    def __call__(self, x, y, z):
        return sum(duc.bfield_strength(x, y, z) for duc in self.ducs)
