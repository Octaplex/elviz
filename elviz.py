#!/usr/bin/python2

from visual import *
from physics import BField
from shapes import Wire, Coil

w = Wire(vector(0, 0, 0), vector(0, 10, 0), 100000000)

r = Coil(vector(0, 0, 0), 10, vector(0, 0, 1), 10000000)

B = BField()
B.add_inducer(r)

B.draw(vector(-20, -20, -20), vector(20, 20, 20), 5)
