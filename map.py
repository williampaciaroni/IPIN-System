import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np

tree = ET.parse('data/map10_gt2.xml')
map = tree.getroot()
fig, ax = plt.subplots()
timestamp = 0
plt.xlabel("Time: "+str(timestamp))

for floors in map:
    if floors.tag == 'floors':
        for floor in floors:
            for outline in floor:
                if outline.tag == 'outline':
                    #There are two
                    for polygon in outline:
                        points_x = []
                        points_y = []
                        for point in polygon:
                            points_x.append(float(point.get('x')))
                            points_y.append(float(point.get('y')))
                        plt.plot(points_x, points_y, '-k')
                if outline.tag == 'obstacles':
                    for obstacle in outline:
                        #TODO: Types and material analysis
                        plt.plot([float(obstacle.get('x1')), float(obstacle.get('x2'))], [float(obstacle.get('y1')), float(obstacle.get('y2'))])
                """ if outline.tag == 'gtpoints':
                    for gtpoint in outline:
                        plt.plot(float(gtpoint.get('x')), float(gtpoint.get('y')), 'yo') """
                #if outline.tag == 'accesspoints':
                    #for accesspoint in outline:
                        #plt.plot(float(accesspoint.get('x')), float(accesspoint.get('y')), 'bo')
                if outline.tag == 'beacons':
                    for beacon in outline:
                        plt.plot(float(beacon.get('x')), float(beacon.get('y')), 'ro')