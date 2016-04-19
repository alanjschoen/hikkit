# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 13:16:34 2016
Reads AT centerline shapefile obtained from ATC webpage
Implements CenterLine class to store information

@author: alanschoen
"""

import shapefile
import numpy as np
from geomath import coords2dist
    
def getNearbySegs(pt, rad, data):
    ll = []
    ur = []
    for (ind,seg) in enumerate(data):
        ll.append(seg["BBOX"][0:2])
        ur.append(seg["BBOX"][2:4])
    llDist = [coords2dist(pt, rpt) for rpt in ll]
    urDist = [coords2dist(pt, rpt) for rpt in ur]
    
    (closeSegInds,) = np.where(np.logical_or((llDist < rad), (urDist < rad)))   
    return [data[i] for i in closeSegInds.tolist()]

class CenterLine:
    def __init__(self, in_filename):
        self.type = "centerline"        
        self.filename = in_filename
        self.data = []
        self.alt = []
        self.unused = []
        self.read(self.filename)
        self.separateAlternate()
        self.autoHike()
        
    def read(self, fname):
        sf = shapefile.Reader(fname)
        
        records = sf.records();
        
        fields = sf.fields # fields has extra DeletionFlag field
        shapes = sf.shapes() #bbox, points
        
        data = []
        fieldNames = fields[1:]
        
        keepFields = ['STATUS', 'SURFACE', 'CLUB', '2D_Miles', '2D_Feet', 'ATC_REGION', 'FEAT_NAME', 'SHARED_USE', 'SOURCE']
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
        print "Read %d trail sections from %s" % (len(data), fname)
        self.data = data

    def deleteNull(self):
        numNull = 0
        numOne = 0
        print "Deleting %d null segments" % (numNull)
        print "Deleting %d sements with only one point" % (numOne)
    def separateAlternate(self):
        for d in self.data:
            if not d["STATUS"] == 'Official A.T. Route':
                self.alt.append(d)
                self.data.remove(d)
        print "Removing %d alternate-route segments" % (len(self.alt))
            
        
    # Hike through AT, ordering sections and removing alternate routes
    def autoHike(self):
        print "Simulating NoBo AT through hike..."
        print "Acting like total hiker trash"
        data = self.data
        # List beginnings of segments
        segInfo = []
        for (i,s) in enumerate(data):
            segB = s["POINTS"][0,:]
            segE = s["POINTS"][-1,:]
            segInfo.append((i, segB, segE))
        # go through each segment and find the next segment
        queue = list(segInfo)

        # Set start and end points to Springer and Katahdin
        # Coords of Springer: 34.6272° N, 84.1939° W
        # Coords of Katahdin: 45.9044° N, 68.9216° W
        curpt = np.array([-84.1939, 34.6272])
        endpt = np.array([-68.9216, 45.9044])
        
        # Store ordered data        
        hikePath = []
        hikeData = []
        
        # Count segments flipped and straight
        numFlipped = 0
        numStraight = 0
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
                numFlipped += 1
            else:
                numStraight += 1
            curpt = data[next_sInd]["POINTS"][-1,:]
            hikeData.append(data[next_sInd])
            hikePath.append(next_sInd)
            del queue[next_qInd%nQ]
        self.data = hikeData
        self.unused = [data[q[0]] for q in queue]
        print "Reached Katahdin. Fleeing Baxter State Security Service (B.S. S.S.)"
        print "Flipped %d sections.  %d were already straight." % (numFlipped, numStraight)
            


"""
import geocoder
g = geocoder.elevation([34.6272, -84.1939]) #need to reverse order
print (g.feet)

p = geocoder.google([34.6272, -84.1939], method='reverse')
p.state

"""
