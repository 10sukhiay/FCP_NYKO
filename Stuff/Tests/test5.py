import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.animation as animation

iter=100
pop_size = 10 # total number of individuals
xsize = 50  # number of cell or pixels in the xaxis
ysize = 50  # number of cells or pixels in the yaxis
infheat=100
susheat=-100
heat = np.zeros((xsize,ysize)) # heat map array, currently all cold

xpos = np.random.randint(0,xsize-1, size=(pop_size,1))  # random x coordinates in column vector
ypos = np.random.randint(0,ysize-1, size=(pop_size,1))  # random y coordinates in column vector
map_pos=np.column_stack((xpos,ypos))
random_states = [1, 2]  # 1 means healthy, 2 means infectious
weights = [96, 4] # lists the states and weightings (has no bearing on real weights)
state = np.transpose([np.array(random.choices(random_states, weights=weights, k=pop_size))]) #randomly picks state using weighting probability, convert to column vector
if np.any(np.where(state == 2)) == False: # checks if we have 0 infected individuals
    state[np.random.randint(0,pop_size)] = 2 # adds 1 infected at random
position_state = np.column_stack((xpos, ypos, state))

def find_sus(position_state):
    old_sus=np.array([],dtype=int)
    for r in range(0,pop_size-1):
        if position_state[r,2]==1:
            new1=map_pos[r]
            old_sus=np.append(old_sus,new1,axis=0)
    sv1= np.reshape(old_sus,(-1,2),order='C')
    return sv1

print(find_sus(position_state))
print(position_state)
print(len(position_state))

inf_count=np.array([],dtype=int)

for z in range(0,10):
    new2=np.array([np.count_nonzero(position_state[:, 2] == 2)])
    inf_count=np.append(inf_count,new2,axis=0)

print(inf_count)


        