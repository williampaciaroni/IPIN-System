from numpy import power, array, random

def trilateration(P, R):
    if len(R) < 3: return None
    # To avoid division by 0 rotate anchors and measurements
    if abs(P[1,0] - P[0,0]) < 1e-5:
        P[[2,0,1]] = P[[0,1,2]]
        R[2], R[0], R[1] = R[0], R[1], R[2]
    ps = power(P[2, 0], 2) - power(P[1, 0], 2) + \
         power(P[2, 1], 2) - power(P[1, 1], 2)
    pt = power(P[0, 0], 2) - power(P[1, 0], 2) + \
         power(P[0, 1], 2) - power(P[1, 1], 2)
    bs = (P[1, 0] - P[2, 0]) * (P[0, 1] - P[1, 1]) - \
         (P[2, 1] - P[1, 1]) * (P[1, 0] - P[0, 0])
    s = (ps + power(R[1], 2) - power(R[2], 2)) / 2.0
    t = (pt + power(R[1], 2) - power(R[0], 2)) / 2.0
    if bs == 0:
        return None
    try:
        y = (t * (P[1, 0] - P[2, 0]) - s * (P[1, 0] - P[0, 0])) / bs
    except:
        return None
    x = (y * (P[0, 1] - P[1, 1]) - t) / (P[1, 0] - P[0, 0])
    return [x, y]
