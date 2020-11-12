import math
import random
import matplotlib.pyplot as plt
import numpy as np
from math import exp

#figure, axes = plt.subplots()

def distance(a,b):
    x = (a['beacon'][1]-b['x'])**2
    y = (a['beacon'][2]-b['y'])**2
    dist = math.sqrt(x+y)
    return dist

def distancePoint(a,b):
    x = (a['x']-b['x'])**2
    y = (a['y']-b['y'])**2
    dist = math.sqrt(x+y)
    return dist

def get_intersections(a, r1, b, r2):
    distance = np.linalg.norm(a-b)
    
    #Case 1: they don't intersect since they are too far
    if distance > r1 + r2:
        return None
    
    #Case 2: they don't intersect since one circle is contained inside the other
    if distance < abs(r1 - r2):
        return None
    
    #Case 3: they intersect in infinite points since they are coincident
    if distance == 0 and r1 == r2:
        return None
    
    #Case 4: they intersect in two points, which we will calculate
    x = (r1 ** 2 - r2 ** 2 + distance ** 2) / (distance * 2)
    y = math.sqrt(r1 ** 2 - x ** 2)

    x3 = a[0] + x * (b[0] - a[0]) / distance
    y3 = a[1] + x * (b[1] - b[1]) / distance

    x4 = x3 + y * (b[1] - a[1]) / distance
    y4 = y3 - y * (b[0] - a[0]) / distance

    x5 = x3 - y * (b[1] - b[0]) / distance
    y5 = y3 + y * (b[0] - a[0]) / distance
    
    return ({'x1': round(x4,5),'y1': round(y4,5),'x2':round(x5,5),'y2':round(y5,5)})

def approximate(p1, r1, p2, r2):
    """Approximate a circle intersection point."""
    d = np.linalg.norm(p1-p2)
    if abs(d)<exp(1e-5): 
        return None
    dr1, dr2 = r1 / d, r2 / d
    p = p2-p1
    dp1, dp2 = dr1*p, dr2*p
    p11, p12, p21, p22 = p1 + dp1, p1-dp1, p2 + dp2, p2-dp2 # Find nearest pair of intersection point belonging to different # circles.
    n1, n2 = p11, p21
    d1, dt = np.linalg.norm(p11-p21), np.linalg.norm(p11-p22)
    if dt < d1: d1, n2 = dt, p22
    dt = np.linalg.norm(p12-p21)
    if dt < d1: d1, n1, n2 = dt, p12, p21
    dt = np.linalg.norm(p12-p22)
    if dt < d1: n1, n2 = p12, p22
    # return middle of line between two nearest points as result 
    return n1 / 2 + n2 / 2

def filterdata(circles,distances,intersections):
    inter = []
    inte_not_dupl = []
    for i in intersections:
        counter = 0
        for c in range(len(circles)):
            if distances[c]>=np.linalg.norm(circles-i['p']):
                counter+=1
        if counter>=(1):
            inter.append(i)
        counter=0
    for e in inter:
        if e not in inte_not_dupl:
            inte_not_dupl.append(e)
    return inte_not_dupl

def mean(arr):
    summ = 0
    for e in arr:
        summ+=e
    return summ/len(arr)
        
def sortdict(arr): 
    n = len(arr) 
    for i in range(n): 
        for j in range(0, n-i-1): 
            if arr[j]['m'] > arr[j+1]['m'] : 
                arr[j], arr[j+1] = arr[j+1], arr[j] 

def centroid(intersection):
    xw = 0
    yw = 0
    w = 0
    for k in intersection:
        xw+=k['p'][0]*k['w']
        yw+=k['p'][1]*k['w']
        w+=k['w']
    return {'x':xw/w,'y':yw/w}

def plot(positions,distances):
    x = []
    y = []
    centroidcond = False
    inter = []

    for k in range(len(positions)):
        for j in range(len(positions)):
            i = None
            i = get_intersections(positions[k], distances[k],positions[j],distances[j])
            if i is None:
                i = approximate(positions[k],distances[k],positions[j],distances[j])
                if i is not None:
                    inter.append({'p':[i[0],i[1]],'w':1})
            else:
                inter.append({'p':[i['x1'],i['y1']],'w':3})
                inter.append({'p':[i['x2'],i['y2']],'w':3})

    inter_filtered=filterdata(positions, distances, inter)

    if len(inter_filtered)<=3:
        centre = centroid(inter_filtered)
    else:
        centre = centroid(inter_filtered)
    return [centre['x'],centre['y']]