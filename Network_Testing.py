# Code created 22/04/21

# Oscar Bond
# Inital testing

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import random


edgelist=[(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8)]
H=nx.Graph(edgelist)
#nx.draw(H)


# creating a simple graph
edgelist=[(1,2),(1,3),(1,4),(1,5),(2,3),(3,4),(4,5),(2,5)]
G=nx.Graph(edgelist)


# give attributes to nodes and edges
G.nodes[1]['Number'] = 11
G.nodes[2]['Number'] = 12
G.nodes[3]['Number'] = 13
G.nodes[4]['Number'] = 14
G.nodes[5]['Number'] = 15

G.edges[1,2]['Time'] = 2
G.edges[1,3]['Time'] = 2
G.edges[1,4]['Time'] = 2
G.edges[1,5]['Time'] = 2

G.edges[2,3]['Time'] = 5
G.edges[3,4]['Time'] = 5
G.edges[4,5]['Time'] = 5
G.edges[5,2]['Time'] = 5


pos = nx.spring_layout(G)


#nx.draw(G, with_labels=True)
nx.draw(G,pos, with_labels=True)
node_labels = nx.get_node_attributes(G,'Time')
nx.draw_networkx_labels(G, pos, labels = node_labels)
edge_labels = nx.get_edge_attributes(G,'Time')
nx.draw_networkx_edge_labels(G, pos, edge_labels)
#plt.savefig('SimpleWeightedNetwork.png')
plt.show()