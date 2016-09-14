#!/usr/bin/python2

# Imports (DO NOT EDIT)
from visual import vector, display
from physics import *
from shapes import *
from ui import Elviz

# Initial setup
e = Elviz(1600, 900) # (width, height)
d = e.scene
B = BField(d, color = (1, 1, 0)) # color tuples are in (r, g, b) format

# Constructor parameters:
#
# Wire(start, end, current, scene)
# Coil(center, radius, normal vector, current, scene, loops(default=1), pitch(default=1))
# Bar(start, direction, magnetic moment, length, scene, height(default=1), width(default=0.5))
# Particle(center, magnetic moment, scene)
#
# See `shapes.py` for more precise definitions.

# Example shapes
#w = Wire(vector(0, -15, 15), vector(0, 15, -15), 1, d)
r = Coil(vector(0, 0, 0), 10, vector(0, 1, 1), 10, d, 10, 0.5)
#bar = Bar(vector(10, 0, 0), vector(0, 0, 1), 1, 10, d)
#p = Particle(vector(0, 10, 0), 0.5*vector(0, -1, 0), d)


# Add inducers
#B.add_inducer(w)
B.add_inducer(r)
#B.add_inducer(bar)
#B.add_inducer(p)

# Set display field
B.draw(vector(-30, -30, -30), vector(60, 60, 60), 3, 30)
