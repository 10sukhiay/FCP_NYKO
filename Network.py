# Code created 22/04/21

# Oscar Bond
# Network setup

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import random

######## this is an attempt to call variable from Nathan's code but currently giving me and error.
#from NW_dots_move3 import N


#global variable - to be called from Nathan Code when bug is fixed

N = 10 #number of people across the network
#number_nodes = 4


def create_network(edgelist):
# creating a simple graph based on the input edgelist
    G =nx.Graph(edgelist)
    nx.draw(G, with_labels=True)
    return G

def nodes(G):
# calculating the number of nodes in the network
    nodes = G.nodes()
    return nodes


def network_paths(G):
# list the paths of the network based on all start and end node combinations
# note the cutoff value can be changed depending on the number of nodes that you want people to visit.
    paths =[]
    path = []
    nodes = G.nodes()
    for i in range(1, len(nodes), 1):
        for j in range(1, len(nodes), 1):
        #paths = list(nx.all_simple_paths(G, source=i, target=4, cutoff=4))
            node_paths = list(nx.all_simple_paths(G, source=i, target=j, cutoff=4))
            path.append(node_paths)
            #print(path)
    return path


#class Position(object):
# this is to positions people on the first iterations and then
# update their position at the end of each day
# where day is 100 iterations of the low level code
#    def __init__(self, node, infected):
#        self.node = random.randint(1,number_nodes)
#        self.infected = random.randint(0,1)
#    def initial_position(self):
#        """Compute inital node for person"""
#        self.node = random.randint(1,4) ##### if here i want to call nodes, how??
#        return self.node




# setup the edgelist
edgelist=[(1,2),(1,3),(1,4),(1,5),(2,3),(3,4),(4,5),(2,5)]

#edgelist=[(1,2),(1,3),(2,3),(3,4)]
# Input
G = create_network(edgelist)
nodes = nodes(G)
# Processing
path = network_paths(G)
#person1 = Position(2,0)
#person2 = Position(3,0)

#print(person1.initial_position())
#print(person2.initial_position())

#positions = [Position() for i in range(N)]  # creates N amount of people from the object person eg person(1), person(2) ect



#positions = [position() for i in range(N)]

print(path)



plt.show()