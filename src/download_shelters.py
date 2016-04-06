# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 19:30:07 2016

@author: alanschoen
"""


from bs4 import BeautifulSoup
import sqlite3


"""
import urllib
# get website content
target = 'http://tnlandforms.us/at/'
req = urllib.request.Request(url=target)
f = urllib.request.urlopen(req)
xhtml = f.read().decode('utf-8')
"""

def writeSqlite(shelters):
# Store in sqlite database
    conn = sqlite3.connect('../output/shelters.db')
    #conn.execute('''DROP TABLE shelters''')
    conn.execute('''CREATE TABLE shelters
                 (_id INTEGER PRIMARY KEY, Name text, NoboMile real, Elev real, County text, State text)''')
    conn.executemany('INSERT INTO shelters VALUES (NULL,?,?,?,?,?)', shelters)
    conn.execute('''CREATE TABLE android_metadata (locale TEXT DEFAULT 'en_US')''')
    conn.execute('''INSERT INTO android_metadata VALUES ('en_US')''')
    # Save (commit) the changes
    conn.commit()
    # Close db file
    conn.close()

def writeFlat(shelters):
    f = open('../output/shelters.csv', 'w')
    for s in shelters:
        f.write(", ".join(s) + "\n")   
    f.close()


fname = "../data/shelters_table.html"
output_type  = "FLAT"

f = open(fname, 'r')
html = f.read()
f.close()

headings = ["Name","NoboMile","MilesToNext","Elev","County","State","Waypoint"]

soup = BeautifulSoup(html)
table = soup.find("table", attrs={"class":"boldtable"})

# The first tr contains the field names.
#headings = [th.get_text() for th in table.find("tr").find_all("th")]

shelters = []
for row in table.find_all("tr")[1:]:
    item = tuple(td.get_text() for td in row.find_all("td"))
    if item[2].strip() == "off":
        continue
    item = (item[0],) + (item[1], item[3].strip("' ")) + item[4:6]
    shelters.append(item)

if output_type == "FLAT":
    writeFlat(shelters)
if output_type == "SQLITE":
    writeSqlite(shelters)






