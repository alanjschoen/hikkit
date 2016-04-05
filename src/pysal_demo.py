# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 17:34:17 2016

@author: alanschoen
"""

import pysal

shfilename = '../AT_Centerline_12-23-2014/at_centerline.shp'

w = pysal.rook_from_shapefile(shfilename)
w.n
w.s0
w.pct_nonzero

wq = pysal.queen_from_shapefile(shfilename)
wq.s0
wq.histogram