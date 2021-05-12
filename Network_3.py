# Code created 22/04/21

# Oscar Bond
# Network setup

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import random
import numpy as np
from numpy.random import randint

#global variable - to be called from Nathan Code when bug is fixed

N = 10 #number of people across the network
room_size_x = 10
room_size_y = 10
number_infected = 1

# setup the edgelist
#edgelist=[(1,2),(1,3),(1,4),(1,5),(2,3),(3,4),(4,5),(2,5)]

edgelist=[(1,2),(1,4),(2,5),(3,5),(2,3)]

#edgelist=[(1,2),(1,3),(2,3),(3,4)]

# Create a networkx graph from the edgelist.
G = nx.Graph(edgelist)
nx.draw(G, with_labels=True)
#plt.show()   # this displays the graph - turn on as required.

number_nodes = G.number_of_nodes()
print(number_nodes)

def create_people_array():
    x_position = randint(0,room_size_x+1,N) # randomly assign x values for each person
    y_position = randint(0,room_size_y+1,N) # randomly assign y values for each person
    start_nodes = randint(1, number_nodes+1, N)
    start_status = np.concatenate((([1]*number_infected), ([0]*(N-number_infected))))
    #start_status = start_status.transpose()
    data_in = np.stack((x_position, y_position, start_nodes, start_status), axis=1)
    position_state = pd.DataFrame(data=data_in, columns=['x', 'y', 'node', 'status'])
    return(position_state)

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

parameters = create_people_array()
print(parameters)

# initialise people - x, y, node, status
person1 = Position(parameters.iloc[1,1],2,3,0)
#person1 = Position(parameters.iloc[1,:].to_string(header=False, index=False)) # playing around with inputting data
# from the data frame. Not currently working. Could do it simply and select each column but long.
person2 = Position(2,2,3,0)
person3 = Position(2,2,4,0)


# calling function for instance of the class

check = person1.move_node_connected()
print(check)
check2 = person3.move_node_connected()
#print(check2)
person3_node = check2
#print(person3_node)

print(parameters.iloc[1,:].to_string(header=False, index=False))

## need to edit the code to be able to integrate with Kaelan

# look into the way to integrate with the command line.