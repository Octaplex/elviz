#!/usr/bin/python2

from visual import vector, display

from physics import *
from shapes import *
from ui import Elviz

e = Elviz()
d = e.scene

#w1 = Wire(vector(0, 0, 0), vector(0, 10, 0), 1, d)
w2 = Wire(vector(-3, 5, 4), vector(7, 10, 4), 0.01, d)
#w3 = Wire(vector(1, 9, 6), vector(-3, -6, 2), 1, d)

#r = Coil(vector(0, 1, 0), 2, vector(0, 1, 1), 0.0000005, d)

bar = Bar(vector(0, 0, 0), vector(0, 1, 0), 1, 10, d)

p = Particle(vector(-1, 5, 2), 0.1*vector(3, 1, -2), d)

B = BField(d, color = (0.8, 0.5, 0))
#B.add_inducer(w1)
B.add_inducer(w2)
#B.add_inducer(w3)
#B.add_inducer(r)
B.add_inducer(bar)
B.add_inducer(p)

B.draw(vector(-10, -10, -10), vector(20, 20, 20), 3)
