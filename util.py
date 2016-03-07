from __future__ import division, print_function

from numpy.linalg import norm

def normalize(u):
    return u / norm(u)
