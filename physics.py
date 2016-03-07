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

    def draw(self, P):
        """Draw the field vector at the given point."""
        v = self(P)

    def __call__(self, P): raise NotImplementedError

class BField(Field):
    """
    A magnetic (B) field.
    """

    def __call__(self, P):
        return sum(duc.bfield_at(P) for duc in self.ducs)
