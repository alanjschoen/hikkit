# -*- coding: utf-8 -*-
"""
Created on Tue May 24 15:59:21 2016

@author: alanschoen
"""

segs = cLine.unused[3:5]
for (i, s) in enumerate(segs):
    plt.plot(s.points[:,0], s.points[:,1], color=colors[i%3], linestyle="-")