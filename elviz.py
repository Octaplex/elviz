#!/usr/bin/python2

from visual import *
from physics import BField
from shapes import Wire, Coil

#w = Wire(vector(0, 0, 0), vector(0, 1, 0), 100000000)

r = Coil(vector(0, 1, 0), 5, vector(0, 1, 1), 1000000)

B = BField(color = (0, 0.8, 0.2))
B.add_inducer(r)

B.draw(vector(-10, -10, -10), vector(20, 20, 20), 5)
