#!/usr/bin/python2

from visual import *
from physics import BField
from shapes import Wire

w = Wire(vector(0, -5, 0), vector(0, 5, 0), 10**8)

B = BField()
B.add_inducer(w)

B.draw(vector(-10, -10, -10), vector(11, 11, 11), 5)
