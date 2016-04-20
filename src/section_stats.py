# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 20:21:15 2016

@author: alanschoen
"""

import matplotlib.pyplot as plt


from readatc import CenterLine
import numpy as np

from geomath import coords2dist

shapefile_name = "../testdata/AT_Centerline_12-23-2014/at_centerline"
cLine = CenterLine(shapefile_name)
cLine.separateAlternate()
cLine.autoHike()

lens = []
gaps = []
for (i,s) in enumerate(cLine.data):
    lens.append(float(s["2D_Miles"]))
    if i>0:
        gaps.append(coords2dist(s["POINTS"][0,:], cLine.data[i-1]["POINTS"][0,:]))


# the histogram of the data
n, bins, patches = plt.hist(lens, 20, facecolor='green', alpha=0.75)
plt.xlabel('Miles')
plt.ylabel('Probability')
plt.title('Histogram of section lengths')
#plt.axis([40, 160, 0, 0.03])
#plt.grid(True)
plt.show()


# the histogram of the data
n, bins, patches = plt.hist(gaps, 20, facecolor='green', alpha=0.75)
plt.xlabel('Miles')
plt.ylabel('Probability')
plt.title('Histogram of gaps between trail segments')
#plt.axis([40, 160, 0, 0.03])
#plt.grid(True)
plt.show()
