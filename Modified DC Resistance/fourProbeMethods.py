from math import *
import mpmath as mpmath
import numpy as np

from pymeasure.instruments.keithley import Keithley7001


# F. S. Olivera et al.

def H1(L1, L2, n=10):
    """ Exact series equation H1 - converges faster than H2 """
    total = 0
    for i in range(n):
        total += 1 / ((2 * i + 1) * np.sinh(pi * (2 * i + 1) * (L1 / L2)))

    return 1 / ((8 / pi) * total)


def H2(L1, L2, n=10):
    """ Equation for H2 given H1 (converges quicker """
    return -pi / (log(1 - exp(-pi / H1(L1, L2, n))))


def const(L1, L2, n=10):
    """ """
    H = H1(L1, L2, n)
    return 1 / (pi / H - log(1 - exp(-pi / H)))


# This is the f(L2/L1) equation
# def f(L1, L2, n=10):
#     return 2 * log(2) * const(L1, L2, n)


def Rs(R1, R2, L1, L2, n=10):
    """ Numerical equation for Rs using L1 and L2 """
    return pi * (R1 + R2) * const(L1, L2, n)

    ##################
    # APPROXIMATIONS #
    ##################


def RsG(R1, R2):
    """ Rs solved using G approximation """
    G = 0.5 * (1 / pi * log(R2 / R1) + sqrt(pow(1 / pi * log(R2 / R1), 2) + 4))
    return pi / 8 * (R1 + R2) * (1 / (mpmath.csch(pi * G) + mpmath.csch(pi / G)))


def RsGL(R1, R2, L1, L2):
    """ Rs solved using G approximation """
    G = L2 / L1
    return pi / 8 * (R1 + R2) * (1 / (mpmath.csch(pi * G) + mpmath.csch(pi / G)))


def checker(R1, R2):
    R = RsG(R1, R2)
    return exp((-pi * R1) / R) + exp((-pi * R2) / R)


if __name__ == "__main__":
    R1 = .7
    R2 = .7
    print(RsG(R1, R2))
    print(RsG(R2, R1))
    print(checker(R1, R2))
    print((pi * R1) / (log(2)))

"""
R(12,34) = V(34)/I(12)

V(34) -> 3: -V, 4: +V

"""

"""

we want -V to connect to: a, c, b, d; b, d, c, a
we want +V to connect to: b, d, a, c; c, a, b, d
we want -I to connect to: c, a, d, b; d, b, a, c
we want +I to connect to: d, b, c, a; a, c, d, b

"""
