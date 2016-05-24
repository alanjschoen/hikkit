# -*- coding: utf-8 -*-
"""
Created on Wed Apr 6 13:18:00 2016
Math functions for cartographic things.  maybe should be called cartomath

@author: alanschoen
"""


import math
from geopy.distance import vincenty

# Calculate distance from two coords
# Latitude: 1 deg = 110.54 km
# Longitude: 1 deg = 111.320*cos(latitude) km
def coords2dist( pt1, pt2 ):
    middle_lat = abs(pt1[1] - pt2[1])/2
    lat_dist = abs(pt1[1] - pt2[1])/(111.320*math.cos(middle_lat))*0.621371
    lon_dist = abs(pt1[0] - pt2[0])*110.54*0.621371
    return math.sqrt(lat_dist*lat_dist + lon_dist*lon_dist)

# Calculate size of BBOX in square miles
def coords2square( pt1, pt2 ):
    middle_lat = abs(pt1[1] - pt2[1])/2
    lat_dist = abs(pt1[1] - pt2[1])/(111.320*math.cos(middle_lat))*0.621371
    lon_dist = abs(pt1[0] - pt2[0])*110.54*0.621371
    return math.sqrt(lat_dist*lon_dist)
    
def vincentyDist(c1, c2):
    c1 = tuple(c1[::-1])
    c2 = tuple(c2[::-1])
    return vincenty(c1, c2).miles

"""
def vincentyDist():
    from geopy.distance import vincenty
    newport_ri = (41.49008, -71.312796)
    cleveland_oh = (41.499498, -81.695391)
    print(vincenty(newport_ri, cleveland_oh).miles)

def gcDist():
    from geopy.distance import great_circle
    newport_ri = (41.49008, -71.312796)
    cleveland_oh = (41.499498, -81.695391)
    print(great_circle(newport_ri, cleveland_oh).miles)
"""