from __future__ import division, print_function

from scipy import integrate

def interpolate(color, val, base = (1, 1, 1)):
    if val > 1: val = 1
    return tuple(b + (c-b)*val for c, b in zip(color, base))

def avg(xs):
    xs = list(xs)
    return sum(xs)/len(xs)

# 1st and 2nd kind of elliptic integrals, K(k) and E(k) respectively
# http://www.mhtlab.uwaterloo.ca/courses/me755/web_chap3.pdf
def K(k):
    return integrate.quad(lambda t: ((1-t**2)*(1-k**2*t**2))**-0.5, 0, 1)[0]

def E(k):
    return integrate.quad(lambda t: ((1-k**2*t**2)/(1-t**2))**0.5, 0, 1)[0]
