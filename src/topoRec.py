import numpy as np
import os
import re
import matplotlib.pyplot as plt
import networkx as nx

def prims(corrMat):
    V = len(corrMat)
    # arbitrarily choose initial vertex from graph
    vertex = 0
    # initialize empty edges array and empty MST
    MST = []
    edges = []
    visited = []
    maxEdge = [None,None,float(0)]
    # run prims algorithm until we create an MST that contains every vertex from the graph
    while len(MST) != V-1:
        # mark this vertex as visited
        visited.append(vertex)
        # add each edge to list of potential edges
        for r in range(0, V):
            if corrMat[vertex][r] != 0:
                edges.append([vertex,r,corrMat[vertex][r]])
        # find edge with the biggest correlation to a vertex that has not yet been visited
        for e in range(0, len(edges)):
            if edges[e][2] > maxEdge[2] and edges[e][1] not in visited:
                maxEdge = edges[e]
        # remove min weight edge from list of edges
        edges.remove(maxEdge)
        # push min edge to MST
        MST.append(maxEdge)
        # start at new vertex and reset min edge
        vertex = maxEdge[1]
        maxEdge = [None,None,float(0)]
    return MST


def show_graph_with_labels(edges):
    gr = nx.Graph()
    gr.add_edges_from(edges)
    nx.draw(gr, node_size=500, with_labels=True)
    plt.show()


topo = "ieee13"

files = os.listdir("../"+topo)

csvList = []
for f in files:
    if f.endswith(".csv"):
        csvList.append(f)

nodeList = [re.findall('\d+',csv) for csv in csvList]
nodeList  = np.squeeze(np.array(nodeList))

rawData = []

for csv in csvList:
    csvData = np.genfromtxt("../"+topo+"/"+csv, delimiter=',')
    rawData.append(csvData[:,1:])

rawData = np.array(rawData)

# axis shifting for the ease of corelation matrix calc
corrData = np.moveaxis(rawData,-1,0)

corrMats = []

for attr in corrData:
    corrMats.append(np.corrcoef(attr))

corrMats = np.array(corrMats)

corrMats[np.isnan(corrMats)] = 0

avgCorr = np.mean(corrMats, axis=0)
np.fill_diagonal(avgCorr, 1)

G = prims(avgCorr)


edges = [[nodeList[i[0]],nodeList[i[1]]] for i in G]

show_graph_with_labels(edges)
