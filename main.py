from mpl_toolkits import mplot3d
from sklearn.cluster import AffinityPropagation

from random import randint

import numpy as np
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
    x.append(float(data[2]))
    y.append(float(data[3]))
    z.append(float(data[4]))
    datamatrix.append([float(data[2]),float(data[3]),float(data[4])])

# Run clustering algorithm
clustering = AffinityPropagation().fit(datamatrix)
print(len(clustering.cluster_centers_))
print(clustering.labels_)

clustercolorlist = list()
clustercolors = cm.rainbow(np.linspace(0, 1, len(clustering.cluster_centers_)))
for item in clustering.labels_:
    clustercolorlist.append(clustercolors[item])

# Draw plot
ax.scatter(x,y,z,c=clustercolorlist,marker='.',alpha=0.6)
plt.show()
