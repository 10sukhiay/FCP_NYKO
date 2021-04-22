import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.animation as animation

#CREATE STARTING CONDITIONS
iter=100
infheat=100
susheat=-100
pop_size = 10 # total number of individuals
xsize = 50  # number of cell or pixels in the xaxis
ysize = 50  # number of cells or pixels in the yaxis
heat = np.zeros((xsize,ysize)) # heat map array, currently all cold
edges = np.zeros((xsize,ysize)) # boundary array, will have values where there are boundaries, values can dictate behaviour

xpos = np.random.randint(0,xsize-1, size=(pop_size,1))  # random x coordinates in column vector
ypos = np.random.randint(0,ysize-1, size=(pop_size,1))  # random y coordinates in column vector
map_pos=np.column_stack((xpos,ypos))
random_states = [1, 2]  # 1 means healthy, 2 means infectious
weights = [96, 4] # lists the states and weightings (has no bearing on real weights)
state = np.transpose([np.array(random.choices(random_states, weights=weights, k=pop_size))]) #randomly picks state using weighting probability, convert to column vector
if np.any(np.where(state == 2)) == False: # checks if we have 0 infected individuals
    state[np.random.randint(0,pop_size)] = 2 # adds 1 infected at random
pos_st = np.column_stack((xpos, ypos, state))



#def addheat_inf(foundinf):
   # num=np.array([],dtype=int)
   # for z in range(0,len(foundinf)-1):
        #num=np.append(old_inf,infheat,axis=0)
    #return num

#def addheat_sus(foundsus):
    #num2=np.array([],dtype=int)
    #for y in range(0,len(foundsus)-1):
        #num2=np.append(old_sus,susheat,axis=0)
    #return num2


#adds heat based on states
re_pos_st=np.array([],dtype=int)
for z in range(0,len(pos_st)):
    if pos_st[z,2]==2:
        re_pos_st=np.append(re_pos_st,100)
    if pos_st[z,2]==1:
        re_pos_st=np.append(re_pos_st,-100)
pos_st=np.column_stack((pos_st,re_pos_st))
print(re_pos_st)
print(pos_st)
