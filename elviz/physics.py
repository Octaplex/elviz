from __future__ import division, print_function

from visual import cone, vector

from operator import add
from util import interpolate, avg

class BInducer:
    """
    A magnetic (B) field inducer.
    """

    def bfield_at(self, P):
        """Calculate the magnetic field vector at a point."""
        raise NotImplementedError


class EInducer:
    """
    An electric (E) field inducer.
    """

    def efield_at(self, P):
        """Calculate the electric field vector at a point."""
        raise NotImplementedError


class Field:
    """
    The abstract base class for all fields.

    All fields are callable objects; the return value is a vector denoting the
    field strength and direction at a point. Calculation of this vector must be
    implemented in every concrete subclass. It is typically the superposition
    of fields for every inducer in the field.

    Fields maintain a list of inducers called ducs.
    """

    def __init__(self, scene, ducs = [], color = (0, 1, 0)):
        self.scene = scene
        self.ducs = ducs
        self.color = color
        self.Ps = {}

    def add_inducer(self, duc):
        """Add an inducer to this field."""
        self.ducs += [duc]

    def draw_at(self, P, step):
        """Draw the field vector at the given point."""
        B = self[P]
        if self.avg_mag == 0:
            val = 0
        else:
            #get value in between smallest and largest
            val = 1-((B.mag-self.smallest_mag)\
                     /(self.largest_mag-self.smallest_mag))
        #set size of pointers, radius = step/rad
        rad = 15
        cone(pos = P, axis = B.norm(), radius=step/rad, length=step,
                display = self.scene, color = interpolate(self.color, val),
                opacity = val)


    def draw(self, origin, size, step, radius = -1):
        """
        Draw field vectors periodically within a region.

        Drawing begins at the origin and continues by the given step up to
        and including the size. Both the size and step may be vectors or
        scalars. Scalars are equivalent to vectors with equal dimensions.
        """

        # get the origin coordinates
        x0, y0, z0 = origin

        try:
            l, h, w = size
        except TypeError:
            l = w = h = size

        try:
            step_x, step_y, step_z = step
        except TypeError:
            step_x = step_y = step_z = step

        xs = range(int(x0), int(x0+l)+1, int(step_x))
        ys = range(int(y0), int(y0+h)+1, int(step_y))
        zs = range(int(z0), int(z0+w)+1, int(step_z))

        #getting values for color interpolation
        for x in xs:
            for y in ys:
                for z in zs:
                    self[vector(x, y, z)] = self(vector(x, y, z))
        self.avg_mag = avg(B.mag for B in self.Ps.values())
        self.largest_mag = max(B.mag for B in self.Ps.values())
        #smallest mag is estimate due to absolute smallest being zero, not useful
        self.smallest_mag = self.largest_mag- 2*(self.largest_mag - self.avg_mag)

        for x in xs:
            for y in ys:
                for z in zs:
                    if (radius == -1 or (x**2 + y**2 + z**2)**0.5 <= radius):
                        self.draw_at(vector(x, y, z), step)

    def __getitem__(self, P):
        if P in self.Ps:
            return self.Ps[P]
        else:
            B = self(P)
            self.Ps[P] = B
            return B

    def __setitem__(self, P, B):
        self.Ps[P] = B

    def __call__(self, P): raise NotImplementedError


class BField(Field):
    """
    A magnetic (B) field.
    """

    def __call__(self, P):
        dbs = [duc.bfield_at(P) for duc in self.ducs]
        return reduce(add, dbs, vector(0, 0, 0))


class EField(Field):
    """
    An electric (E) field.
    """

    def __call__(self, P):
        des = [duc.efield_at(P) for duc in self.ducs]
        return reduce(add, des, vector(0, 0, 0))

