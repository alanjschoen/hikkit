from geopy.distance import vincenty
import numpy as np

def getNearbySegs(pt, rad, data):
    ll = []
    ur = []
    for (ind,seg) in enumerate(data):
        ll.append(seg.bbox[0:2])
        ur.append(seg.bbox[2:4])
    llDist = np.array([vincentyDist(pt, rpt) for rpt in ll])
    urDist = np.array([vincentyDist(pt, rpt) for rpt in ur])
    
    (closeSegInds,) = np.where(np.logical_or((llDist < rad), (urDist < rad)))
        
    
    return [data[i] for i in closeSegInds.tolist()]

def vincentyDist(c1, c2):
    c1 = tuple(c1[::-1])
    c2 = tuple(c2[::-1])
    return vincenty(c1, c2).miles

segBeg = np.zeros([npts,2])
segEnd = np.zeros([npts,2])
for (i,s) in enumerate(cLine.data):
    segBeg[i,:] = s.points[0,:]
    segEnd[i,:] = s.points[-1,:]

gaps = []
for (c1,c2) in zip(segEnd[:-2], segBeg[1:]):
    gaps.append(vincentyDist(c1, c2))

print zip(np.sort(gaps)[::-1][:10], np.argsort(gaps)[::-1][:10])


pt = cLine.data[1744].points[-1,:]
nearby =  getNearbySegs(pt, 1, cLine.data)
nearby = cLine.data[3330:3332]

colors = ["r", "b", "g"]
for (i, s) in enumerate(nearby):
    plt.plot(s.points[:,0], s.points[:,1], color=colors[i%3], linestyle="-")
    
plt.plot(pt[0], pt[1], color='k', marker="^")
    

