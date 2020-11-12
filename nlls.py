from numpy import power
from residual import residual
from lls import lls
import numpy as np
from numpy.linalg import inv

def distance(A,B):
    return np.linalg.norm(A-B)

def nlls(P, R, N=100, start=lls):
    """Non-linear least squares algorithm"""
    if len(R) < 3: return None

    S = start(P, R)
    iterations = 0
    e1, e2 = None, residual(P, R, S)
    while iterations < N:
        if not all([ distance(S, p) >= 1e-5 for p in P]):
            return S
        A = np.array([[(S[0] - p[0]) / distance(S, p),(S[1] - p[1]) / distance(S, p)] for p in P])
        b = np.array([(R[i] - distance(S, P[i])) + (A[i][0] * S[0] + A[i][1] * S[1]) for i in range(len(R))])
        # Solve using the closed form solution $(A^TA)^{-1}(A^Tb)$
        try:
            S = inv((A.transpose().dot(A))).dot((A.transpose().dot(b)))
        except ZeroDivisionError:
            return S
        e1, e2 = e2, residual(P, R, S)
        if e1 - e2 < 1e-5: return S
        iterations = iterations + 1
    return S