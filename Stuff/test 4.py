import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.animation as animation

x_pos = np.random.randint(1,49, size=(10,1))  # random x coordinates in column vector
y_pos = np.random.randint(1,49, size=(10,1))  # random y coordinates in column vector
state = np.zeros((10,1))
random_states = [1, 2]  # 1 means healthy, 2 means infectious
weights = [96, 4] # lists the states and weightings (has no bearing on real weights)
state = np.transpose([np.array(random.choices(random_states, weights=weights, k=10))]) #randomly picks state using weighting probability, convert to column vector
if np.any(np.where(state == 2)) == False: # checks if we have 0 infected individuals
    state[np.random.randint(0,10)] = 2 # adds 1 infected at random
position_state = np.hstack((x_pos, y_pos, state)) # horizontal stack into 1 array

n=0
i=0
while n < 100:

    #Transmission(position_state, heat)
    #heat = map1.calculate_heat_new()

    #if (n / 2).is_integer():  # only move every other iteration
        #Move(position_state)
    
    inf_count=np.array([],dtype=int)
    iteration=np.array([],dtype=int)
    inf_count=np.append(inf_count,np.count_nonzero(position_state[:, 2] == 2),axis=0)
    iteration=np.append(iteration,int(n))

    print(inf_count)
    print(iteration)
    #map1 = COVID_MAP(heat, position_state, boundary, xsize, ysize)

    i += 1
    n += 1

