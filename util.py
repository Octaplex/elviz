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

    __mul__ = dot

    def __abs__(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5
