from __future__ import division, print_function

from visual import *

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

    def draw_at(self, P):
        """Draw the field vector at the given point."""

        # draw a skinny arrow
        arrow(pos = P, axis = P + self(P), shaftwidth = 0.1)

    def draw(self, origin, size, step):
        """
        Draw field vectors periodically within a region.

        Drawing begins at the origin and continues by the given step up to
        and including the size. Both the size and step may be vectors or
        scalars. Scalars are equivalent to vectors with equal dimensions.
        """

        x0, y0, z0 = origin

        try:
            l, w, h = size
        except TypeError:
            l = w = h = size

        try:
            step_x, step_y, step_z = step
        except TypeError:
            step_x = step_y = step_z = step

        for x in range(int(x0), int(l), int(step_x)):
            for y in range(int(y0), int(h), int(step_y)):
                for z in range(int(z0), int(w), int(step_z)):
                    self.draw_at(vector(x, y, z))

    def __call__(self, P): raise NotImplementedError

class BField(Field):
    """
    A magnetic (B) field.
    """

    def __call__(self, P):
        tot = vector(0, 0, 0)
        for duc in self.ducs:
            tot += duc.bfield_at(P)

        return tot
