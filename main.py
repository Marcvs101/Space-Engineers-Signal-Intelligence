from sklearn.cluster import AffinityPropagation

from random import randint

import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Init plot
fig = plt.figure()
ax = plt.axes(projection="3d")

# Read and parse points
# TAG:NAME:X:Y:Z
f = open(file="./data.txt",mode="r")
lines = f.readlines()
f.close()

x = list()
y = list()
z = list()
datamatrix = list()

for line in lines:
    data = line.split(":")
    datamatrix.append([float(data[2]),float(data[3]),float(data[4])])

# Run clustering algorithm
af = AffinityPropagation().fit(datamatrix)

cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_
n_clusters_ = len(cluster_centers_indices)

print('Estimated number of clusters: %d' % n_clusters_)
print("Estimated GPS coordinates of centroids:")
counter = 0
for center in af.cluster_centers_:
    print("GPS:Cluster "+str(counter)+":"+str(center[0])+":"+str(center[1])+":"+str(center[2])+":")
    counter = counter+1

clusterlist = list()
for i in range(n_clusters_):
    clusterlist.append([list(),list(),list()])
clustercolors = cm.rainbow(np.linspace(0, 1, n_clusters_))

counter = 0
for item in labels:
    clusterlist[item][0].append(datamatrix[counter][0])
    clusterlist[item][1].append(datamatrix[counter][1])
    clusterlist[item][2].append(datamatrix[counter][2])
    counter = counter + 1
    
# Draw plot
for cluster in range(n_clusters_):
    ax.scatter(clusterlist[cluster][0],clusterlist[cluster][1],clusterlist[cluster][2],
               color=clustercolors[cluster],marker='.',alpha=0.3,label=str(cluster))

counter = 0
for center in af.cluster_centers_:
    ax.scatter(center[0],center[1],center[2],
               color=clustercolors[counter],marker='v',alpha=1)
    counter = counter+1

ax.legend()
plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()
