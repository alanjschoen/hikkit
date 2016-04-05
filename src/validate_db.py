# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 20:17:27 2016

@author: alanschoen
"""

import sqlite3

conn = sqlite3.connect('../data/shelters.db')

print "Tables:"
for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'"):
    print row

print "Shelters:"
for row in conn.execute('SELECT * FROM shelters ORDER BY NoboMile LIMIT 5'):
        print row


conn.close()