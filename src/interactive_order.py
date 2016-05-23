# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 13:53:01 2016

@author: alanschoen
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 13:16:34 2016

@author: alanschoen
"""

import shapefile
import numpy as np
import matplotlib.pyplot as plt
import math
from readatc import CenterLine


# Calculate distance from two coords
# Latitude: 1 deg = 110.54 km
# Longitude: 1 deg = 111.320*cos(latitude) km
def coords2dist( pt1, pt2 ):
    middle_lat = abs(pt1[1] - pt2[1])/2
    lat_dist = abs(pt1[1] - pt2[1])/(111.320*math.cos(middle_lat))*0.621371
    lon_dist = abs(pt1[0] - pt2[0])*110.54*0.621371
    return math.sqrt(lat_dist*lat_dist + lon_dist*lon_dist)


# Hike through AT, ordering sections and removing alternate routes
def interact(data):
    # List beginnings of segments
    segInfo = []
    for (i,s) in enumerate(data):
        segB = s.points[0,:]
        segE = s.points[-1,:]
        segInfo.append((i, segB, segE))
    
    # go through each segment and find the next segment
    queue = list(segInfo)
    curpt = np.array([-84.1939, 34.6272]) #start at springer
    endpt = np.array([-68.9216, 45.9044]) #end at Katahdin
    command = [""]
    colors = ["r", "b", "g"]
    hike_path = []
    hikeData = []
    while queue:
        dists = [coords2dist(curpt, p[1]) for p in queue]
        rankord = np.argsort(dists).tolist()
        #ind = np.argmin(np.sum(np.abs(curpt - segBegins), axis=1))
        plt.plot(curpt[0],curpt[1], 'ko', mfc='none')
        for i in range(2):
            qInd = rankord[i]
            sInd = queue[qInd][0]

            
            plt.plot(data[sInd].points[:,0], data[sInd].points[:,1], color=colors[i], linestyle="-")
            plt.plot(data[sInd].points[-1,0], data[sInd].points[-1,1], color=colors[i], marker="^")
        plt.show()
        command = raw_input().strip().split(' ')
        special = ""
        if len(command)>1:
            special = command[0]
            del command[0]
        
        if command[0] in colors:
            next_qInd = rankord[colors.index(command[0])]
            next_sInd = queue[next_qInd][0]
            
            if special == "rev":
                data[next_sInd].points = data[next_sInd].points[::-1,:]
            curpt = data[next_sInd].points[-1,:]
            hikeData.append(data[next_sInd])
            hike_path.append((special, next_sInd))
            print next_sInd
            print curpt
        else:
            break
        del queue[next_qInd]
    return hikeData
        
        
# Instructions
# After running interact(), look at the plot
# Black circle represents current point
# Colored lines are choices for the next segment, with a triangle marking the end
# Enter a command with the first letter of the color of the line you choose, e.g. "r" or "b" and hit enter
# If the segment is backwards, type "rev r" or "rev b"

shapefile_name = "../testdata/AT_Centerline_12-23-2014/at_centerline"
cLine = CenterLine(shapefile_name)
print "Number of records: " + str(len(cLine.data))
nSeg = len(cLine.data)

hikeData = interact(cLine.data)

