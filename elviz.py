################################################################################

#DO NOT EDIT CONTENT ENCLOSED, THE CONSEQUENCES WILL BE SEVERE

#!/usr/bin/python2

from visual import vector, display

from physics import *
from shapes import *
from ui import Elviz

e = Elviz()
d = e.scene
################################################################################

#Edit here, after reading Instructions.txt

#Example wire:
w = Wire(vector(0, -5, 0), vector(0, 5, 0), 1, d)

#Example coil:
r = Coil(vector(-3, 0, 0), 2, vector(1, 0, 0), 1, d, loops = 6, pitch=1)

#Example bar magnet:
bar = Bar(vector(0, 0, 0), vector(0, 0, 1), 1, 10, d)

#Example dipole particle:
p = Particle(vector(0, 5, 0), 0.5*vector(0, -1, 0), d)

#Set color, default is celeste blue
B = BField(d, color = (0.5, 1, 1))

#Add inducers
B.add_inducer(w)
B.add_inducer(r)
B.add_inducer(bar)
B.add_inducer(p)

#Set display field
B.draw(vector(-8, -8, -8), vector(17, 17, 17), 3)
