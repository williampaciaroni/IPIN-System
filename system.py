import codecs
import csv
import time
import xml.etree.ElementTree as ET
import math
import os
import os.path
import nlls
import map as mp
import numpy as np
import trilateration_test as trilateration
import clustering as cluster
from matplotlib.animation import FuncAnimation

#Initializing variables
beacons = []
filtered_beacons = []
time_beacons = []
previous_ts = 0
gamma = 2.3

#Parsing of bluetooth beacons from XML
def parse_beacons(xml_path):
    tree = ET.parse(xml_path)
    map = tree.getroot()
    for floors in map:
        if floors.tag == 'floors':
            for floor in floors:
                for outline in floor:
                    if outline.tag == 'beacons':
                        for beacon in outline:
                            beacons.append([(beacon.get('mac').replace(':', '')), float(beacon.get('x')), float(beacon.get('y'))])

#Retuns distance using formula specified in the PDF
def beacon_distance(rssi):
    return 10 ** ((-rssi - 56) / (10 * gamma))

#Parse beacon and insert it into a dictionary
def beacon_event(data):
    timestamp = data[0]
    mac = data[2]
    rssi = data[3]
    txPower = data[4]
    for i in beacons:
        if mac in i[0]:
            beac = {'beacon': i, 'time': int(float(timestamp)*1e-10),'distance':beacon_distance(int(rssi))}
            filtered_beacons.append(beac)

#Parse Wifi FTM data, not used
def wifi_ftm_event(data):
    #Was the measurement successful
    successful = data[2]
    #Mac address of the partner
    mac = data[3]
    #Distance estimate, field is in mm
    dist = float(data[4]) / 1000
    #Standard deviation of distance estimate, field is in mm
    sdev = float(data[5]) / 1000
    #Receive signal strength indication
    rssi = data[6]
    #Number of attempts taken to estimate distance
    if len(data) > 7:
        attemps = data[7]
    else:
        attemps = 1
    #Number of attempts that were successful
    if len(data) > 8:
        attemps = data[8]
    else:
        attemps = 1

#Parse csv file selecting only Bluetooth beacons and WiFi FTM readings
def parse_csv(csv_path):
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            #Beacon
            if row[1] == '9':
                beacon_event(row)
            #WiFi FTM
            elif row[1] == '17':
                wifi_ftm_event(row)
            
#Check if time is inside the array
def timeIsInVector(array,time):
    if len(array)==0:
        return -1
    else:
        for a in range(len(array)):
            if array[a]['time']==time:
                return a
        return -1

#Group beacons with same timestamp
def filterBeacons():      
    for f in filtered_beacons:
        index = timeIsInVector(time_beacons,f['time'])
        if index != -1:
            time_beacons[index]['beacons'].append({'beacon':f['beacon'],'distance':f['distance']})
        else:
            time = []
            time.append({'beacon':f['beacon'],'distance':f['distance']})
            time_beacons.append({'beacons':time,'time':f['time']})

#Given a beacon array with same timestamp it checks if there are duplicates, 
    #removes them and finally calculate the avg distance for each point
def average_beacons(array):
    different = []
    final_points = []
    for a in array:
        if a['beacon'][0] not in different:
            different.append(a['beacon'][0])
    for d in different:
        distance = 0
        counter = 0
        beacon = None
        for a in array:
            if d==a['beacon'][0]:
                counter+=1
                distance+=a['distance']
                beacon = a['beacon']
        final_points.append({'beacon':beacon,'distance':distance/counter})
    return final_points

#Return positions and distances
def position_distances(index):
    positions = []
    distances = []
    average = average_beacons(time_beacons[index]['beacons'])
    for a in average:
        pos = [a['beacon'][1],a['beacon'][2]]
        distances.append(a['distance'])
        positions.append(pos)
    return positions,distances

#Using trilateration with MLE, it returns an array of points
def points_mle():
    points = []
    for t in range(len(time_beacons)):
        pos,dist = position_distances(t)
        try:
            points.append({'point':nlls.nlls(np.array(pos),np.array(dist)),'time':time_beacons[t]['time']})
        except:
            pass
    return points

#Using trilateration without MLE, it returns an array of points
def points_no_mle():
    points = []
    for t in range(len(time_beacons)):
        pos,dist = position_distances(t)
        try:
            points.append({'point':trilateration.trilateration(np.array(pos),np.array(dist)),'time':time_beacons[t]['time']})
        except:
            pass
    return points

#Using Clustering, it returns an array of points
def points_clustering():
    points = []
    for t in range(len(time_beacons)):
        pos,dist = position_distances(t)
        try:
            v = cluster.core(np.array(pos),np.array(dist))
            if v[0]!=0 and v[1]!=0:
                points.append({'point':[v[0],v[1]],'time':time_beacons[t]['time']})
        except:
            pass
    return points

xml_path = 'data/map10_gt2.xml'
csv_path = 'data/Pixel3a/3783363286825.csv'

parse_beacons(xml_path)
parse_csv(csv_path)

######Points######
filterBeacons()

ptrian = points_mle()
ptrian_nomle = points_no_mle()
pcluster = points_clustering()

#------------------Trilateration with MLE---------------
ppmle = []
#Removes points that are not in the map
for p in ptrian:
    if p['point'] is not None:
        if p['point'][0]>=0 and p['point'][0]<=220:
            if p['point'][1]>=60 and p['point'][1]<=155:
                ppmle.append(p)

#------------------Trilateration without MLE---------------
ppnomle = []
#Removes points that are not in the map
for p in ptrian_nomle:
    if p['point'] is not None:
        if p['point'][0]>=0 and p['point'][0]<=220:
            if p['point'][1]>=60 and p['point'][1]<=155:
                ppnomle.append(p)

#------------------Clustering------------------------------
ppcluster = []
#Removes points that are not in the map
for p in pcluster:
    if p['point'] is not None:
        if p['point'][0]>=0 and p['point'][0]<=220:
            if p['point'][1]>=60 and p['point'][1]<=155:
                ppcluster.append(p)

prev_point = None

#------------------ANIMATION FOR EACH METHOD----------------

def animatemle(dot):
    global prev_point
    d = ppmle[dot]
    mp.plt.plot(d['point'][0],d['point'][1],'mo')
    mp.plt.xlabel("Time: "+str(d['time']))
    if prev_point is not None:
        mp.plt.plot([prev_point[0], d['point'][0]], [prev_point[1], d['point'][1]],color='magenta')
    prev_point = d['point']

def animatenomle(dot):
    global prev_point
    d = ppnomle[dot]
    mp.plt.plot(d['point'][0],d['point'][1],'bo')
    mp.plt.xlabel("Time: "+str(d['time']))
    if prev_point is not None:
        mp.plt.plot([prev_point[0], d['point'][0]], [prev_point[1], d['point'][1]],color='blue')
    prev_point = d['point'] 

def animatecluster(dot):
    global prev_point
    d = ppcluster[dot]
    mp.plt.plot(d['point'][0],d['point'][1],'go')
    mp.plt.xlabel("Time: "+str(d['time']))
    if prev_point is not None:
        mp.plt.plot([prev_point[0], d['point'][0]], [prev_point[1], d['point'][1]],color='green')
    prev_point = d['point']   

#Call the method that you want to use

anim_mle = FuncAnimation(mp.fig, animatemle, interval=500, frames=len(ppmle)-1)

#anim_no_mle = FuncAnimation(mp.fig, animatenomle, interval=500, frames=len(ppnomle)-1)

#anim_cluster = FuncAnimation(mp.fig, animatecluster, interval=500, frames=len(ppcluster)-1)

#Show result
mp.plt.draw()
mp.plt.show()