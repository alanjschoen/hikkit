# -*- coding: utf-8 -*-
"""
Created on Wed Apr 6 13:18:00 2016
Math functions for cartographic things.  maybe should be called cartomath

@author: alanschoen
"""


import math

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