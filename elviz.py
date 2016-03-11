#!/usr/bin/python2

from visual import *
from physics import BField
from shapes import Wire

w = Wire(vector(0, 0, 0), vector(0, 10, 0), 100000000)

B = BField()
B.add_inducer(w)

B.draw(vector(-20, -20, -20), vector(20, 20, 20), 5)
