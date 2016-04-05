from __future__ import division, print_function

from visual_common.primitives import arrow
from visual_common.cvisual import vector

from operator import add
from util import interpolate, avg

class Inducer:
    """
    The abstract base class for all field inducers.
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


class EInducer:
    """
    An electric (E) field inducer.

    Like inducer, this class is more or less a placeholder. It does define the
    method efield_strength which must be implemented by all subclasses.
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

    def __init__(self, ducs = [], color = (0, 1, 0)):
        self.ducs = ducs
        self.color = color
        self.Ps = {}

    def add_inducer(self, duc):
        """Add an inducer to this field."""
        self.ducs += [duc]

    def draw_at(self, P):
        """Draw the field vector at the given point."""

        B = self[P]

        #conflict
        val = B.mag
        arrow(pos = P, axis = 1.5*B.norm(), shaftwidth = 0.1,
                color = interpolate(self.color, val), opacity = 2*val)
        val = B.mag/self.avg_mag
        arrow(pos = P, axis = val*B.norm(), shaftwidth = 0.1,
                color = interpolate(self.color, val), opacity = val)


    def draw(self, origin, size, step):
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

        for x in xs:
            for y in ys:
                for z in zs:
                    self[vector(x, y, z)] = self(vector(x, y, z))

        self.avg_mag = avg(B.mag for B in self.Ps.values())

        for x in xs:
            for y in ys:
                for z in zs:
                    self.draw_at(vector(x, y, z))


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
