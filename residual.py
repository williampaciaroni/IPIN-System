from numpy import power
import numpy as np

def distance(A,B):
    return np.linalg.norm(A-B)

def residual(P, R, S, p=2.0):
    """Returns the p-distance between two points."""
    return sum([ power(abs(distance(P[i], S) - R[i]), p)
                 for i in range(len(R))])