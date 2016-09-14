from __future__ import division, print_function

from visual import vector, cylinder, ring, helix, box, sphere, materials

from math import pi, sin, cos

from physics import *
from constants import mu_0, eps_0
from util import K, E, matrixDot, matrixAdd, inverse, scalarProd

class Shape:
    """
    The mostly abstract base class of all shapes.

    Implements drag-and-drop behaviour. Subclasses must have an attribute
    `obj' which refers to the VPython object that represents the shape.
    """

    def __init__(self, scene):
        scene.bind('mousedown', self.grab)

    def grab(self, evt):
        """Grab the mouse and bind some more events."""
        if evt.pick == self:
            self.drag_pos = evt.pickpos
            self.scene.bind('mousemove', self.move)
            self.scene.bind('mouseup', self.drop)

    def move(self, evt):
        """Move the object when the mouse moves."""
        new_pos = self.scene.mouse.project(normal=(0,0,1))
        if new_pos != self.drag_pos:
            self.moveto(new_pos - self.drag_pos)
            self.drag_pos = new_pos

    def drop(self, evt):
        """Unbind events and clean up when the mouse is released."""
        self.scene.unbind('mousemove', self.move)
        self.scene.unbine('mouseup', self.drop)

    def moveto(self, pos):
        """Move the VPython object to a new position."""
        self.obj.pos += pos


class Wire(Shape, BInducer, EInducer):
    """
    A straight wire.
    """

    def __init__(self, A, B, I, scene):
        Shape.__init__(self, scene)

        self.A = A
        self.B = B

        self.BA = self.B - self.A
        self.l = self.BA.mag
        self.l2 = self.BA.mag2

        self.I = self.BA.norm() * I

        self.obj = cylinder(pos = self.A, axis = self.BA, radius = 0.1,
                display = scene, material = materials.silver)

    def ray_to(self, P):
        """
        Calculate the shortest vector from the wire to a point P.

        Adapted from:
        http://mathworld.wolfram.com/Point-LineDistance3-Dimensional.html
        """

        t = -self.BA.dot(self.A - P) / self.l2
        return P - (self.A + t*self.BA)

    def bfield_at(self, P):
        r = self.ray_to(P)

        if r.mag == 0: return vector(0, 0, 0)
        return (mu_0 * self.I.mag / (2*pi*r.mag)) * r.cross(self.I).norm()

    def efield_at(self, P):
        r = self.ray_to(P)

        if r.mag == 0: return vector(0, 0, 0)
        return (self.I / (2*pi*eps_0*self.l*r)) * r.norm()


class Coil(Shape, BInducer):
    """
    A coil of wire.
    """

    def __init__(self, center, radius, normal, I, scene, loops = 1, pitch = 1):
        Shape.__init__(self, scene)

        self.center = center
        self.radius = radius
        self.normal = normal

        self.loops = loops
        self.pitch = pitch
        self.length = loops*pitch

        self.I = I

        # some consonants
        self.C = mu_0*I/pi
        self.oner = [[1,0,0], [0,1,0], [0,0,1]]

        # rotation matrices for this coil, rotating so norm becomes z axis
        self.rotate = self.find_rotmatrix(normal.norm(), vector(0, 0, 1))
        self.antiRotate = inverse(self.rotate)


        if loops == 1:
            self.obj = ring(pos = center, axis = normal*self.length,
                    radius = radius, thickness = 0.1, display = scene,
                    material = materials.chrome)
        else:
            self.obj = helix(pos = center, axis = normal*self.length,
                    radius = radius, coils = loops, thickness = 0.1,
                    display = scene, material = materials.chrome)

    def find_rotmatrix(self, a, b):
        if a == vector(0, 0, 1):
            return [[1,0,0],[0,1,0],[0,0,1]]
        elif a == vector(0, 0, -1):
            return [[1,0,0],[0,1,0],[0,0,-1]]

        # http://math.stackexchange.com/questions/180418/calculate-rotation-matrix-to-align-vector-a-to-vector-b-in-3d
        v = a.cross(b)

        # creating [v]x, skew symmetric matrix
        # https://en.wikipedia.org/wiki/Skew-symmetric_matrix
        vx = [[ 0,   -v.z,  v.y],
              [ v.z,  0,   -v.x],
              [-v.y,  v.x,  0  ]]
        
        return matrixAdd(self.oner, matrixAdd(vx, scalarProd(matrixDot(vx, vx), (1 - a.dot(b))/v.mag)))



    def bfield_at(self, P):
        res = vector(0, 0, 0)

        for l in range(0, self.loops):
            C = self.center + self.normal*self.pitch*l
        
            # translate center to origin and align normal to z axis
            comp1 = matrixDot(self.rotate, [[(P - C).x], [(P - C).y], [(P - C).z]])
            Pr = vector([comp1[0][0], comp1[1][0], comp1[2][0]])  #dot product returns 2d array so need 2 entries
            rx, ry, rz = Pr
            # defining variables for equation
            # http://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20010038494.pdf
            r = Pr.mag

            rho = (rx**2 + ry**2)**0.5
            alpha = (self.radius**2 + r**2 - 2*self.radius*(rho))**0.5
            beta = (self.radius**2 + r**2 + 2*self.radius*(rho))**0.5
            gamma = rx**2 - ry**2
            k = (1 - (alpha**2/beta**2))**0.5
            C = mu_0*self.I / pi

            
            if alpha == 0 or beta == 0 or rho == 0: continue
            # components
            
            Bx = (C*rx*rz / (2*alpha**2*beta*rho**2)) * \
                 ((self.radius**2 + r**2) * E(k**2) - alpha**2 * K(k**2))
            if rx != 0:
                By = Bx * (ry/rx)
            else:
                By = (C*rx*rz / (2*alpha**2*beta*rho**2)) * \
                     ((self.radius**2 + r**2) * E(k**2) - alpha**2 * K(k**2))
            Bz = (C/(2*alpha**2*beta)) * \
                 ((self.radius**2 - r**2) * E(k**2) + alpha**2 * K(k**2))

            # untranslate points and re-align to actual normal
            B = vector(Bx, By, Bz).norm()
            comp2 = matrixDot(self.antiRotate, [[B.x], [B.y], [B.z]])
            res += vector([comp2[0][0], comp2[1][0], comp2[2][0]])

        return res


class Bar(Shape, BInducer):
    """
    A static bar magnet.

    Characteristics are as for the `box` object in VPython: pos is in the
    center, axis defines the direction of the bar. To switch south and north
    poles you can take the negative of the axis.
    """

    def __init__(self, pos, axis, moment, length, scene, height = 1, width = 0.5):
        Shape.__init__(self, scene)

        self.pos = pos
        self.axis = axis

        self.south = Particle(pos - axis*(length/2), moment*axis)
        self.north = Particle(pos + axis*(length/2), moment*axis)
        self.length = length

        self.obj = box(pos = pos, axis = axis, length = length,
                height = height, width = width, display = scene,
                material = materials.chrome)

    def bfield_at(self, P):
        return self.north.bfield_at(P) + self.south.bfield_at(P)


class Particle(Shape, BInducer):
    """
    A point particle.
    """

    def __init__(self, pos, moment, scene = None):
        self.pos = pos
        self.moment = moment

        if scene:
            Shape.__init__(self, scene)
            self.obj = sphere(pos = pos, radius = 0.5, display = scene)

    def bfield_at(self, P):
        r = P - self.pos
        rhat = r.norm()

        if r.mag2 == 0: return vector(0, 0, 0)
        return (mu_0/(4*pi))*(3*self.moment.dot(rhat)*rhat - self.moment)/(r.mag**3)

