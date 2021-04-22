# Code created 22/04/21

# Oscar Bond
# Inital testing

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import random


# creating a simple graph
edgelist=[(1,2),(1,3),(1,4),(1,5),(2,3),(3,4),(4,5),(2,5)]
G=nx.Graph(edgelist)
#nx.draw(G)

# give attributes to nodes. Edge attributes to be added later.
G.nodes[1]['Number'] = 11
G.nodes[2]['Number'] = 12
G.nodes[3]['Number'] = 13
G.nodes[4]['Number'] = 14
G.nodes[5]['Number'] = 15



nx.draw(G, with_labels=True)

plt.show()