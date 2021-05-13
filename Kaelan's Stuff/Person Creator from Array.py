#!/usr/bin/env python3

# Code created 10/01/21
# Kaelan Melville
# Heat Mapping

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import random
import numpy as np
from numpy.random import randint


N = 10 #number of people across the network
room_size_x = 10
room_size_y = 10
number_infected = 1
number_nodes = 5

# Statuses
# 1 Susceptible
# 2 Contracted
# 3 Infectious
# 4 Infectious Asymptomatic
# 5 Recovered
# 6 Deceased

def create_people_array():
    x_position = randint(0,room_size_x+1,N) # randomly assign x values for each person
    y_position = randint(0,room_size_y+1,N) # randomly assign y values for each person
    start_nodes = randint(1, number_nodes+1, N)
    start_status = np.concatenate((([1]*number_infected), ([0]*(N-number_infected))))
    #start_status = start_status.transpose()
    data_in = np.stack((x_position, y_position, start_nodes, start_status), axis=1)
    position_state = pd.DataFrame(data=data_in, columns=['x', 'y', 'node', 'status'])
    return(position_state)

position_state = create_people_array()
#------------------------------------------------------------------------
# Nathan's person class code.....
class person(object):
    def __init__(self, x, y, node):
        self.x =  x #creates random number x coord 1 to room_size
        self.y =  y #creates random number y coord 1 to room_size
        self.node = node
        #self.step_x = self.make_new_step_size() #calls function to create a new step size for person
        #self.step_y = self.make_new_step_size()


#------------------------------------------------------------------------
# Initialise people

people = [person(x = position_state.iloc[i, 0], y = position_state.iloc[i, 1], node = position_state.iloc[i, 2]) for i in range(len(position_state))] #creates people for each row in the array





print(position_state) # original array

position_state.iloc[:, :2] = 0
print(position_state) #array emptied


# this code adds values from people objects back into array
k = 0
for t in people:

    position_state.iloc[k, 0] = t.x
    position_state.iloc[k, 1] = t.y
    position_state.iloc[k, 2] = t.node
    k +=1 # iterator for picking the correct row


print(position_state) # array refilled