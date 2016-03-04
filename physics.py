import math

#constants
muNot = 4*math.pi*10**-7
print(muNot)

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
        
                                    
        
        
        

class Field:
    def __call__(self, x, y, z): raise NotImplementedError
    strength = __call__

class BField(Field):

    def __init__(self, ducs):
        self.ducs = ducs

    def __call__(self, x, y, z):
        return sum(duc.bfield_strength(x, y, z) for duc in self.ducs)
