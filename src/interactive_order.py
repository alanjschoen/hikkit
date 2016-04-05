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


# Calculate distance from two coords
# Latitude: 1 deg = 110.54 km
# Longitude: 1 deg = 111.320*cos(latitude) km
def coords2dist( pt1, pt2 ):
    middle_lat = abs(pt1[1] - pt2[1])/2
    lat_dist = abs(pt1[1] - pt2[1])/(111.320*math.cos(middle_lat))*0.621371
    lon_dist = abs(pt1[0] - pt2[0])*110.54*0.621371
    return math.sqrt(lat_dist*lat_dist + lon_dist*lon_dist)


class CenterLine:
    def __init__(self, in_filename):
        self.type = "centerline"        
        self.filename = in_filename
        self.data = []
        self.alt = []
        self.unused = []
        self.read(self.filename)
        
    def read(self, fname):
        sf = shapefile.Reader(fname)
        
        records = sf.records();
        
        fields = sf.fields # fields has extra DeletionFlag field
        shapes = sf.shapes() #bbox, points
        
        data = []
        fieldNames = fields[1:]
        
        keepFields = ['STATUS', 'SURFACE', 'CLUB', '2D_Miles', 'ATC_REGION', 'FEAT_NAME', 'SHARED_USE', 'SOURCE']
        for (r,s) in zip(records, shapes):
            if not s.points:
                continue
            tmpShape = {}
            for (ind,fn) in enumerate(fieldNames):
                if fn[0] in keepFields:
                    tmpShape[fn[0]] = r[ind]
                    tmpShape["POINTS"] = np.array(s.points)
                    tmpShape["BBOX"] = s.bbox
            data.append(tmpShape)
        #(self.data, self.alt, self.unused) = self.doHike(data)
        for (i,d) in enumerate(data):
            d["ORDER"] = i
        self.data = data
            


# Hike through AT, ordering sections and removing alternate routes
def interact(data):
    # List beginnings of segments
    segInfo = []
    for (i,s) in enumerate(data):
        segB = s["POINTS"][0,:]
        segE = s["POINTS"][-1,:]
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
        nQ = len(queue)
        dists = [coords2dist(curpt, p[1]) for p in queue] + [coords2dist(curpt, p[2]) for p in queue]
        rankord = np.argsort(dists).tolist()
        #ind = np.argmin(np.sum(np.abs(curpt - segBegins), axis=1))
        plt.plot(curpt[0],curpt[1], 'ko', mfc='none')
        for i in range(2):
            qInd = rankord[i]
            sInd = queue[qInd%nQ][0]
            if qInd>nQ: # if segment is backwards, remove forwards version
                rankord.remove(qInd%nQ)
            else:
                rankord.remove(qInd + nQ)
            if data[sInd]["STATUS"] == "Official A.T. Route":
                style = "-"
            else:
                style = "--"
            
            plt.plot(data[sInd]["POINTS"][:,0], data[sInd]["POINTS"][:,1], color=colors[i], linestyle=style)
            plt.plot(data[sInd]["POINTS"][-1,0], data[sInd]["POINTS"][-1,1], color=colors[i], marker="^")
        plt.show()
        command = raw_input().strip().split(' ')
        special = ""
        if len(command)>1:
            special = command[0]
            del command[0]
        
        if command[0] in colors:
            next_qInd = rankord[colors.index(command[0])]
            next_sInd = queue[next_qInd%nQ][0]
            if next_qInd > nQ:
                special = "rev"
            
            if special == "rev":
                data[next_sInd]["POINTS"] = data[next_sInd]["POINTS"][::-1,:]
            curpt = data[next_sInd]["POINTS"][-1,:]
            hikeData.append(data[next_sInd])
            hike_path.append((special, next_sInd))
            print next_sInd
            print curpt
        else:
            break
        del queue[next_qInd%nQ]
        return hikeData
        

def autoHike(data):
    # List beginnings of segments
    segInfo = []
    for (i,s) in enumerate(data):
        segB = s["POINTS"][0,:]
        segE = s["POINTS"][-1,:]
        segInfo.append((i, segB, segE))
    
    # go through each segment and find the next segment
    queue = list(segInfo)
    curpt = np.array([-84.1939, 34.6272]) #start at springer
    endpt = np.array([-68.9216, 45.9044]) #end at Katahdin
    hike_path = []
    hikeData = []
    while queue:
        nQ = len(queue)
        dists = [coords2dist(curpt, p[1]) for p in queue] + [coords2dist(curpt, p[2]) for p in queue]
        if min(dists) > 5:
            # print "Distance to Baxter: " + str(np.sum(coords2dist(curpt, endpt)))
            # print dists[:3]
            # print hikeData[-1]
            break
        next_qInd = np.argmin(dists)
        #ind = np.argmin(np.sum(np.abs(curpt - segBegins), axis=1))

        next_sInd = queue[next_qInd%nQ][0]
        if next_qInd > nQ:
            data[next_sInd]["POINTS"] = data[next_sInd]["POINTS"][::-1,:]
        curpt = data[next_sInd]["POINTS"][-1,:]
        hikeData.append(data[next_sInd])
        hike_path.append(next_sInd)

        del queue[next_qInd%nQ]
        
    return hikeData
        


shapefile_name = "../AT_Centerline_12-23-2014/at_centerline"
cLine = CenterLine(shapefile_name)
print "Number of records: " + str(len(cLine.data))
nSeg = len(cLine.data)

hikeData = autoHike(cLine.data)

