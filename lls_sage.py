#from sage.all import *
from numpy import power
from distance import distance

def distance(x1, y1, x2, y2):
    return 

def lls(P, R):
    """P is a 2xN matrix of landmark positions. R is a vector of
    distances measured from each landmark N."""
    if len(R) < 3: return None

    A = Matrix([[p[0] - P[-1][0], p[1] - P[-1][1]]
                for p in P[:-1]])
    b = vector([(P[i][0] ** 2 - P[-1][0] ** 2 + \
                 P[i][1] ** 2 - P[-1][1] ** 2 + \
                 R[-1] ** 2 - R[i] ** 2) * 0.5 \
                for i in xrange(P.nrows() - 1)])
    return (A.T * A).I * (A.T * b)

if __name__ == "__main__":
    import simulate
    simulate.main(lls, N=10)
