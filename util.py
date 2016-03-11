from __future__ import division, print_function

def interpolate(color, val, base = (1, 1, 1)):
    return tuple(b + (c-b)*val for c, b in zip(color, base))
