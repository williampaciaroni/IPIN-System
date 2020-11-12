import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np

#Get data from XML file and initializing variables
tree = ET.parse('data/map10_gt2.xml')
map = tree.getroot()
fig, ax = plt.subplots()
timestamp = 0
plt.xlabel("Time: "+str(timestamp))

#Parse data from XML into beacons array and plot map obstacles
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
                        plt.plot([float(obstacle.get('x1')), float(obstacle.get('x2'))], [float(obstacle.get('y1')), float(obstacle.get('y2'))])
                if outline.tag == 'beacons':
                    for beacon in outline:
                        plt.plot(float(beacon.get('x')), float(beacon.get('y')), 'ro')