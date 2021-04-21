import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.animation as animation

#CREATE STARTING CONDITIONS
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
pos_st = np.column_stack((xpos, ypos, state))

re_pos_st=np.array([],dtype=int)
for z in range(0,len(pos_st)):
    if pos_st[z,2]==2:
        re_pos_st=np.append(re_pos_st,infheat)
    if pos_st[z,2]==1:
        re_pos_st=np.append(re_pos_st,susheat)
pos_st=np.column_stack((pos_st,re_pos_st))

inf_count=np.array([],dtype=int)
iteration=np.array([],dtype=int)
x=0
y=0
fig, axs = plt.subplots(1)
line1, = axs[0].plot(x,y, color = "r")

def animation_frame(hey):
    for o in range(0,iter):
        inf_count=np.append(inf_count,np.count_nonzero(pos_st[:, 2] == 2))
        iteration=np.append(iteration,int(o))
        line1.set_xdata(inf_count)
        line1.set_ydata(iteration)
        return line1

axs[0].plot(inf_count,iteration)
axs[0].set_title('Infected per iteration')
axs[0].set(xlabel='Population', ylabel='Number of iterations')
plt.xlabel('Population')
plt.ylabel('Number of iterations')
plt.show()
