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
number_nodes = 5

# setup the edgelist
#edgelist=[(1,2),(1,3),(1,4),(1,5),(2,3),(3,4),(4,5),(2,5)]

edgelist=[(1,2),(1,4),(2,5),(3,5),(2,3)]

#edgelist=[(1,2),(1,3),(2,3),(3,4)]
G = nx.Graph(edgelist)
nx.draw(G, with_labels=True)
plt.show()


class Position(object):
# this is to positions people on the first iterations and then
# update their position at the end of each day
# where day is 100 iterations of the low level code
    def __init__(self, x, y, node, status):
        self.x = x
        self.y = y
        self.node = node
        self.infected = status
        self.possible_nodes = self.network_paths_near()
    def move_node_random(self):
        """Update node for person for random node in network"""
        self.node = random.randint(1, number_nodes) # updates value of node for person

        return self.node
    def move_node_connected(self):
        """Update node for person to a node that is connected to their current position"""
        self.node = random.choice(self.possible_nodes)
        return  self.node
    def network_paths_near(self):
        # possible nodes to travel to from individual node
        possible_nodes = list(nx.single_source_shortest_path(G, source=self.node, cutoff=1))
        return possible_nodes


# Input


# initialise people - x, y, node, status
person1 = Position(1,1,2,0)
person2 = Position(2,2,3,0)

# calling function for instance of the class
nodes = []
#for i in range(1,N)
check = person1.move_node_connected()
print(check)
