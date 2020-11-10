import numpy as np
from numpy.linalg import inv

def lls(P, R):
    """P is a 2xN matrix of landmark positions. R is a vector of
    distances measured from each landmark N."""
    if len(R) < 3: return None

    A = np.array([[P[i, 0] - P[-1, 0], P[i, 1] - P[-1, 1]]
                 for i in range(P.shape[0] - 1)])
    b = np.array([(P[i, 0] ** 2 - P[-1, 0] ** 2 + \
                  P[i, 1] ** 2 - P[-1, 1] ** 2 + \
                  R[-1] ** 2 - R[i] ** 2) * 0.5 \
                 for i in range(P.shape[0] - 1)])
    return inv((A.transpose().dot(A))).dot((A.transpose().dot(b)))