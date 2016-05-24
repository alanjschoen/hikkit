from geopy.distance import vincenty
import numpy as np

def vincentyDist(c1, c2):
    c1 = tuple(c1[::-1])
    c2 = tuple(c2[::-1])
    return vincenty(c1, c2).miles

segBeg = np.zeros([npts,2])
segEnd = np.zeros([npts,2])
for (i,s) in enumerate(cLine.data):
    segBeg[i,:] = s.points[0,:]
    segEnd[i,:] = s.points[-1,:]


gaps = [0]
for c1,c2 in zip(segEnd[:-2], segBeg[1:]):
    gaps.append(vincentyDist(c1, c2))

print zip(np.sort(gaps)[::-1][:30], np.argsort(gaps)[::-1][:30])



colors = ["r", "b", "g"]
#plt.plot(cLine.data[i].points[:,0], cLine.data[i].points[:,1], color=colors[1], linestyle="-")