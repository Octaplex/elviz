class vec3d:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def dot(self, other):
        return self.x*other.x + self.y*other.y + self.z*other.z

    def cross(self, other):
        return vec3d(self.y*other.z - self.z*other.y,
                     self.z*other.x - self.x*other.z,
                     self.x*other.y - self.y*other.x)

    def __add__(self, other):
        return vec3d(self.x + other.x, self.y + other.y, self.z + other.z)

    __sub__ = __add__

    __mul__ = dot
