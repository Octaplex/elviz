from __future__ import division, print_function
import math

def interpolate(color, val, base = (0, 0, 0)):
    return tuple(b + (c-b)*val for c, b in zip(color, base))

    

def avg(xs):
    xs = list(xs)
    return sum(xs)/len(xs)

#function from Simpson's Rule Wikipedia example: https://en.wikipedia.org/wiki/Simpson%27s_rule

def integrate(f, a, b, n=10):
    if n % 2 == 1:
        n += 1

    h = (b - a) / n
    s = f(a) + f(b)

    for i in range(1, n, 2):
        s += 4 * f(a + i * h)
    for i in range(2, n - 1, 2):
        s += 2 * f(a + i * h)

    return s * h / 3

# 1st and 2nd kind of elliptic integrals, K(k) and E(k) respectively
# http://www.mhtlab.uwaterloo.ca/courses/me755/web_chap3.pdf
def K(k):
    return integrate(lambda t: (1-k**2*math.sin(t)**2)**-0.5, 0, math.pi/2)

def E(k):
    return integrate(lambda t: (1-k**2*math.sin(t)**2)**0.5, 0, math.pi/2)


#matrix operations

def dotProduct(m1, m2, row, col): #helper
    total = 0
    for x in range (0, len(m2)):
        total += m1[row][x] * m2[x][col]
    return total

def matrixDot(m1, m2):
    if len(m1[0]) != len(m2):
        return None
    result = [[0] * len(m2[0]) for x in range (len(m1))]
    for row in range (0, len(m1)):
        for col in range (0, len(m2[0])):
            result[row][col] = dotProduct(m1, m2, row, col)
    return result


def det3D(a): #helper
    first = a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
    second = -a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
    third = a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    return first + second + third

def det2D(a): #helper
    return a[0][0]*a[1][1] - a[0][1]*a[1][0]

def inverse(a):
    det = det3D(a)
    oneOne = det2D([[a[1][1], a[1][2]], [a[2][1], a[2][2]]]) / det
    oneTwo = det2D([[a[0][2], a[0][1]], [a[2][2], a[2][1]]]) / det
    oneThr = det2D([[a[0][1], a[0][2]], [a[1][1], a[1][2]]]) / det
    twoOne = det2D([[a[1][2], a[1][0]], [a[2][2], a[2][0]]]) / det
    twoTwo = det2D([[a[0][0], a[0][2]], [a[2][0], a[2][2]]]) / det
    twoThr = det2D([[a[0][2], a[0][0]], [a[1][2], a[1][0]]]) / det
    thrOne = det2D([[a[1][0], a[1][1]], [a[2][0], a[2][1]]]) / det
    thrTwo = det2D([[a[0][1], a[0][0]], [a[2][1], a[2][0]]]) / det
    thrThr = det2D([[a[0][0], a[0][1]], [a[1][0], a[1][1]]]) / det
    return [[oneOne, oneTwo, oneThr],
            [twoOne, twoTwo, twoThr],
            [thrOne, thrTwo, thrThr]]


def scalarProd(a, p):
    rep = [[0 for col in range(len(a[0]))] for row in range(len(a))]
    for row in range (len(a)):
        for col in range (len(a)):
            rep[row][col] = a[row][col] * p
    return rep


def matrixAdd(a, b):
    rep = [[0 for col in range(len(a[0]))] for row in range(len(a))]
    for row in range (len(a)):
        for col in range (len(b)):
            rep[row][col] = a[row][col] + b[row][col]
    return rep


