# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 18:14:31 2016

@author: alanschoen
"""

import shapefile
import numpy as np
import matplotlib.pyplot as plt
import math

shapefile_name = "../testdata/AT_Centerline_12-23-2014/at_centerline"

sf = shapefile.Reader(shapefile_name)

records = sf.records();

fields = sf.fields # fields has extra DeletionFlag field
shapes = sf.shapes() #bbox, points

fieldNames = fields[1:]


for (f,r) in zip(fieldNames, records[1000]): # ignore DeletionFlag field
    print "%s (%c): %s" % (f[0], f[1], str(r))


