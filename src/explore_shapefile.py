# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 18:14:31 2016

@author: alanschoen
"""

import shapefile
import numpy as np
import matplotlib.pyplot as plt
import math

shapefile_name = "../AT_Centerline_12-23-2014/at_centerline"

sf = shapefile.Reader(shapefile_name)

records = sf.records();

fields = sf.fields # fields has extra DeletionFlag field
shapes = sf.shapes() #bbox, points

fieldNames = fields[1:]


for (f,r) in zip(fieldNames, records[1000]): # ignore DeletionFlag field
    print "%s (%c): %s" % (f[0], f[1], str(r))


# Filter shapes and get results
segments = []
for (r,s) in zip(records, shapes):
    newSeg = {}
    newSeg['points'] = s.points
    newSeg['bbox'] = s.bbox
    segments.append(newSeg)

trailMiles = 0.0;
altMiles = 0.0
trailTypes = set()
trailSegments = []
altSegments = []
trailBbox = []
for (r,s) in zip(records, shapes):
    trailTypes.add(r[0])
    if math.isnan(s.bbox[1]):
        next
    elif r[0] == "Official A.T. Route":
        trailMiles += float(r[29])
        trailSegments.append(np.array(s.points))
        trailBbox.append(s.bbox)
    else:
        altMiles += float(r[29])
        altSegments.append(np.array(s.points))
        
trailBbox = np.array(trailBbox)
    
print "Trail miles: %f, Alternate miles: %f" % (trailMiles, altMiles)


edges  = []
for i in range(0,len(trailSegments)):
    for j in range(0,len(trailSegments)):
        end1 = trailSegments[i][-1,:]
        beg2 = trailSegments[j][0,:]
        if np.allclose(end1, beg2, 1e-8):
            edges.append((i,j))

plt.imshow(edges)

