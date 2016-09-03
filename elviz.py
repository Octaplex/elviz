################################################################################

#DO NOT EDIT CONTENT ENCLOSED, THE CONSEQUENCES WILL BE SEVERE

#!/usr/bin/python2

from visual import vector, display

from physics import *
from shapes import *
from ui import Elviz

################################################################################
#Set width, height, and primary color
e = Elviz(1600, 900)
d = e.scene
B = BField(d, color = (1, 1, 0))

#Edit here, after reading Instructions.txt
#Wire(starting point, ending point, current, scene)
#Coil(center, radius, normal vector, current, scene, loops(default=1), pitch(default=1))
#Bar(starting point, direction, magnetic moment, length, scene, height(default=1), width(default=0.5))
#Particle(center, magnetic moment*vector in direction of north pole, scene)

#Example wire:
#w = Wire(vector(0, -15, 15), vector(0, 15, -15), 1, d)

#Example coil:
r = Coil(vector(0, 0, 0), 10, vector(0, 1, 1), 10, d, 10, 0.5)

#Example bar magnet:
#bar = Bar(vector(10, 0, 0), vector(0, 0, 1), 1, 10, d)

#Example dipole particle:
#p = Particle(vector(0, 10, 0), 0.5*vector(0, -1, 0), d)


#Add inducers
#B.add_inducer(w)
B.add_inducer(r)
#B.add_inducer(bar)
#B.add_inducer(p)

#Set display field
B.draw(vector(-30, -30, -30), vector(60, 60, 60), 3, 30)
