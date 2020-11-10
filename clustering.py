import math
import random
import matplotlib.pyplot as plt

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

def get_intersections(x1, y1, r1, x2, y2, r2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
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

    x3 = x1 + x * (x2 - x1) / distance
    y3 = y1 + x * (y2 - y1) / distance

    x4 = x3 + y * (y2 - y1) / distance
    y4 = y3 - y * (x2 - x1) / distance

    x5 = x3 - y * (y2 - y1) / distance
    y5 = y3 + y * (x2 - x1) / distance
    
    return ({'x1': round(x4,5),'y1': round(y4,5),'x2':round(x5,5),'y2':round(y5,5)})

def filterdata(circles,intersections):
    inter = []
    inte_not_dupl = []
    for i in intersections:
        counter = 0
        for c in circles:
            if c['distance']>=distance(c,i):
                counter+=1
        if counter>=(len(circles)-2):
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

def medianfilter(data):
    dist = []
    for p in data:
        distances = []
        for e in data:
            if p!=e:
                distances.append(distancePoint(p,e))
        dist.append({'x':p['x'],'y':p['y'],'m':sum(distances)})
    sortdict(dist)
    med = dist[int(len(dist)/2)]['m']
    for d in dist:
       if d['m']>=med:
           dist.remove(d)
    return dist

        
def sortdict(arr): 
    n = len(arr) 
    for i in range(n): 
        for j in range(0, n-i-1): 
            if arr[j]['m'] > arr[j+1]['m'] : 
                arr[j], arr[j+1] = arr[j+1], arr[j] 

def centroid(intersection,weight):
    xw = 0
    yw = 0
    w=1
    for k in intersection:
        xw+=k['x']*weight
        yw+=k['y']*weight
        w+=weight
    return {'x':xw/w,'y':yw/w}

def plot(positions):
    x = []
    y = []
    centroidcond = False
    inter = []
    for e in positions:
        x.append(e['beacon'][1])
        y.append(e['beacon'][2])
    
    for k in positions:
        for j in positions:
            i=(get_intersections(k['beacon'][1],k['beacon'][2],k['distance'],j['beacon'][1],j['beacon'][2],j['distance']))
            if i is not None:
                inter.append({'x':i['x1'],'y':i['y1']})
                inter.append({'x':i['x2'],'y':i['y2']})

    inter_filtered=filterdata(positions,inter)
    if len(inter_filtered)<=3:
        centre = centroid(inter_filtered,3.0*len(inter_filtered))
        centroidcond=True
    else:
        inter_filtered=medianfilter(inter_filtered) 
    """for intersection in inter_filtered:
        plt.plot(intersection['x'],intersection['y'],'yo') """
    if centroidcond==False:
        centre = centroid(inter_filtered,3.0*len(inter_filtered))
    return [centre['x'],centre['y']]