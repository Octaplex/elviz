#!/usr/bin/python2

from visual import *
from physics import BField
from shapes import Wire, Coil

w = Wire(vector(0, 10, 0), vector(0, 0, 0), 1)

#r = Coil(vector(0, 0, 0), 10, vector(0, 1, 0), 10)

B = BField(color = (0, 0.8, 0.2))
B.add_inducer(w)

B.draw(vector(-10, 0, -10), (20, 20, 10), 2)
