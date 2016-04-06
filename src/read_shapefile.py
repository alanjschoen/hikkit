# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 13:16:34 2016
Reads AT centerline shapefile obtained from ATC webpage
Implements CenterLine class to store information

@author: alanschoen
"""

import shapefile
import numpy as np
import matplotlib.pyplot as plt

import matplotlib.patches as mpatches
import shapely.geometry as sgeom
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader

import cartopy
from geomath import coords2dist


def plotSeg(seg):
    if len(seg)>1:
        for s in seg:
            plt.plot(s["POINTS"][:,0], s["POINTS"][:,1])
    else:
        plt.plot(seg["POINTS"][:,0], seg["POINTS"][:,1])
    
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
        self.data = data

    def separateAlternate(self):
        for d in self.data:
            if not d["STATUS"] == 'Official A.T. Route':
                self.alt.append(d)
                self.data.remove(d)
            
        
    # Hike through AT, ordering sections and removing alternate routes
    def autoHike(self):
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
        hikePath = []
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
            hikePath.append(next_sInd)
            del queue[next_qInd%nQ]
        self.data = hikeData
        self.unused = [data[q[0]] for q in queue]
            
# Function to plot the map (not part of object)
def plotMap(line):
    plt.figure(num=None, figsize=(12, 9), dpi=150, facecolor='w', edgecolor='k')
    # Plot AT centerline
    ax = plt.axes(projection=cartopy.crs.PlateCarree())
    
    ax.set_extent([-88, -66.5, 20, 50]) # US East Coast
    
    ax.add_feature(cartopy.feature.LAND)
    ax.add_feature(cartopy.feature.OCEAN)
    ax.add_feature(cartopy.feature.COASTLINE)
    ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
    ax.add_feature(cartopy.feature.LAKES, alpha=0.5)
    ax.add_feature(cartopy.feature.RIVERS)
    
    shapename = 'admin_1_states_provinces_lakes_shp'
    states_shp = shpreader.natural_earth(resolution='110m',
                                             category='cultural', name=shapename)
    # convert to Shapely type
    track = sgeom.LineString(line)
    for state in shpreader.Reader(states_shp).geometries():
        # pick a default color for the land with a black outline,
        # this will change if the storm intersects with our track
        facecolor = [0.9375, 0.9375, 0.859375]
        edgecolor = 'black'
        if state.intersects(track):
            facecolor = [0.9, 0.9, 0.92]
        ax.add_geometries([state], ccrs.PlateCarree(),
                          facecolor=facecolor, edgecolor=edgecolor)
    
    # Plot AT Course
    ax.add_geometries([track], ccrs.PlateCarree(),facecolor='none', edgecolor='red', linewidth=2)

    # # Show Springer and Katahdin
    # # Coords of springer: 34.6272° N, 84.1939° W
    # # Coords of Katahdin: 45.9044° N, 68.9216° W
    # plt.plot([-84.1939],[34.6272], 'bo', [-68.9216],[45.9044], 'bo')  
            

shapefile_name = "../testdata/AT_Centerline_12-23-2014/at_centerline"
cLine = CenterLine(shapefile_name)
npts = len(cLine.data)  

print "Number of records: " + str(npts)
    
segBegins = np.zeros([npts,2])
totalLen = 0.0
for (i,s) in enumerate(cLine.data):
    segBegins[i,:] = s["POINTS"][0,:]
    totalLen += float(s["2D_Miles"])

plotMap(segBegins)



"""
import geocoder
g = geocoder.elevation([34.6272, -84.1939]) #need to reverse order
print (g.feet)

p = geocoder.google([34.6272, -84.1939], method='reverse')
p.state

"""
