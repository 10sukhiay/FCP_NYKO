import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.animation as animation

pop_size = 10 # total number of individuals
xsize = 20  # number of cell or pixels in the xaxis
ysize = 20  # number of cells or pixels in the yaxis
heat = np.zeros((xsize,ysize)) # heat map array, currently all cold
boundary = np.zeros((xsize,ysize)) # boundary array, will have values where there are boundaries, values can dictate behaviour

xpos = np.random.randint(0,xsize-1, size=(pop_size,1))  # random x coordinates in column vector
ypos = np.random.randint(0,ysize-1, size=(pop_size,1))  # random y coordinates in column vector
map_pos=np.column_stack((xpos,ypos))
random_states = [1, 2]  # 1 means healthy, 2 means infectious
weights = [96, 4] # lists the states and weightings (has no bearing on real weights)
state = np.transpose([np.array(random.choices(random_states, weights=weights, k=pop_size))]) #randomly picks state using weighting probability, convert to column vector
if np.any(np.where(state == 2)) == False: # checks if we have 0 infected individuals
    state[np.random.randint(0,pop_size)] = 2 # adds 1 infected at random
pos_st = np.column_stack((xpos, ypos, state))

print (pos_st)

print(pos_st[1,2])

def find_inf(pos_st):
    for t in range(0,pop_size-1):
        old_inf=np.array([],dtype=int)
        if pos_st[t,2]==2:
            new=map_pos[t]
            cur_inf=np.append(old_inf,new)
    print (cur_inf)

find_inf(pos_st)

