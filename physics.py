class Inducer: pass

class BInducer:
    def bfield_strength(self, x, y, z): raise NotImplementedError

class Wire(BInducer):

    def __init__(self, A, B, I):
        self.A = A
        self.B = B
        self.I = I

    def bfield_strength(x, y, z):
        C = vec3d(x, y, z)
        # TODO calculations

class Field:
    def __call__(self, x, y, z): raise NotImplementedError
    strength = __call__

class BField(Field):

    def __init__(self, ducs):
        self.ducs = ducs

    def __call__(self, x, y, z):
        return sum(duc.bfield_strength(x, y, z) for duc in self.ducs)
